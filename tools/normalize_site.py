#!/usr/bin/env python3
"""Come sono bravo? のサイト構成をそろえるスクリプト。

ページを追加・修正したら、リポジトリのルートで次を実行する：
    python3 tools/normalize_site.py

やること（何度実行しても同じ結果になる）：
  1. 全ページの <title> を「ページ名｜Come sono bravo?」にそろえる
  2. 新デザイン（/assets/research.css）のページの上部メニューを共通メニューにそろえる
  3. KOF研究ページ（research/kofXX/）にパンくずがなければ付ける
  4. 全ページ一覧（/sitemap.html）を作り直す
  5. トップの検索窓で使う検索用データ（/search-index.json）を作り直す
"""
import html
import os
import re
from collections import defaultdict

SITE = "Come sono bravo?"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GLOBAL_NAV = (
    '<nav class="nav" aria-label="主要ナビゲーション">'
    '<a href="/">トップ</a>'
    '<a href="/kof-top.html">KOF</a>'
    '<a href="/sonota.html">作品一覧</a>'
    '<a href="/msx/">MSX</a>'
    '<a href="/puyo/death-tower/">ぷよぷよ</a>'
    '<a href="/sitemap.html">全ページ一覧</a>'
    "</nav>"
)

# research/kofXX/ のパンくず
RESEARCH = {
    "kof94": ("KOF'94", "/kof94-top.html"),
    "kof95": ("KOF'95", "/kof95-top.html"),
    "kof96": ("KOF'96", "/kof96-top.html"),
    "kof97": ("KOF'97", "/kof97-top.html"),
    "kof98": ("KOF'98", "/kof98-top.html"),
    "kof99": ("KOF'99", "/kof99-top.html"),
    "kof2000": ("KOF2000", "/kof00-top.html"),
    "kof2002um": ("KOF2002UM", "/kof02um-top.html"),
}


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def write(p, t):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


def all_pages():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "tools"]
        for f in files:
            if f.endswith((".htm", ".html")):
                yield os.path.relpath(os.path.join(root, f), ROOT).replace(os.sep, "/")


# 全ページ一覧と検索に出さないページ（URLは残す）。理由も書いておく
HIDDEN = {
    "seorii-top.html",  # クラッシュ攻略トップ（crush-top.html）の初期版
    "timechart-gakusann.html",  # timechart.html の旧版（85%一致）
    "スタッフロール.html",  # 94staff.html の旧版（91%一致）
    "ローリングへの反撃技表.html",  # cvss2-rorin-hanngeki.html の旧版（97%一致）
    "02umtop-1.html",  # 本文が空
    "frame-ann.html",  # 本文が空
    "02umtop-2.html",  # KOF2002UMトップのキャラ一覧の旧版
    "02umtop-3.html",  # KOF2002UMトップのキャラ一覧の旧版
    "02umtop-4.html",  # KOF2002UMトップのキャラ一覧の旧版
    "02umtop-5.html",  # KOF2002UMトップのキャラ一覧の旧版
    "02umtop-6.html",  # KOF2002UMトップのキャラ一覧の旧版
    "02umtop-7.html",  # KOF2002UMトップのキャラ一覧の旧版
    "02K'-maxima-koutyokusa.html",  # K’のページの複製。マキシマの正式版は 02maxima-kakuwaza-koutyokusa.html
}


def is_redirect(t):
    return bool(re.search(r'http-equiv=["\']refresh', t, re.I))


# ---------- 1. タイトル ----------
def fix_title(path, t):
    def repl(m):
        title = m.group(2).strip()
        if path == "index.html":
            return m.group(1) + SITE + m.group(3)
        pre = re.match(r"^Come sono bravo\?\s*[－\-‐]\s*(.*)$", title)
        if pre:
            title = re.sub(r"^[－\s　]+|(?<=[^｜])[－\s　]+(?=｜|$)", "", pre.group(1).strip())
        parts = [s.strip() for s in title.split("｜")]
        parts = [s for s in parts if s and not s.startswith("MOT") and s != SITE]
        body = "｜".join(parts)
        return m.group(1) + (body + "｜" + SITE if body else SITE) + m.group(3)

    return re.sub(r"(<title>)(.*?)(</title>)", repl, t, count=1, flags=re.S | re.I)


# ---------- 2. 共通メニュー ----------
def fix_nav(path, t):
    if "/assets/research.css" not in t:
        return t
    t = t.replace('class="brand">MOT <span>GAME NOTES</span>', 'class="brand">' + SITE)
    return re.sub(
        r'(<header class="header">.*?)<nav class="nav"[^>]*>.*?</nav>(.*?</header>)',
        lambda m: m.group(1) + GLOBAL_NAV + m.group(2),
        t,
        count=1,
        flags=re.S,
    )


# ---------- 3. KOF研究ページのパンくず ----------
def fix_research_crumbs(path, t):
    m = re.match(r"research/(kof\d+)/(.+)$", path)
    if not m or m.group(1) not in RESEARCH or "breadcrumbs" in t:
        return t
    name, top = RESEARCH[m.group(1)]
    sep = '<span aria-hidden="true"> / </span>'
    last = "<b>研究アーカイブ</b>" if m.group(2) == "index.html" else '<a href="./index.html">研究アーカイブ</a>'
    crumbs = (
        '<div class="crumbbar"><div class="wrap breadcrumbs">'
        f'<a href="/">トップ</a>{sep}<a href="/kof-top.html">KOF</a>{sep}'
        f'<a href="{top}">{name}</a>{sep}{last}</div></div>'
    )
    return re.sub(r"(</header>)", r"\1" + crumbs, t, count=1)


# ---------- 4. 全ページ一覧 ----------
GROUP_ORDER = [
    "KOFシリーズ", "KOF'94", "KOF'94 研究アーカイブ", "KOF'94・'95", "KOF'95", "KOF'95 研究アーカイブ", "KOF'96", "KOF'96 研究アーカイブ",
    "KOF'97", "KOF'97 研究アーカイブ", "KOF'98", "KOF'98 研究アーカイブ", "KOF'98UM", "KOF'99", "KOF2000", "KOF2000 研究アーカイブ",
    "KOF2001", "KOF2002", "KOF2002UM", "KOF2002UM 研究アーカイブ", "KOF2003", "KOF NEOWAVE", "KOF XI",
    "餓狼伝説", "サムライスピリッツ", "その他の格闘ゲーム",
    "アイドルマスター シンデレラガールズ",
    "MSX", "信長の野望・武将風雲録（MSX2版）", "ぷよぷよ・デスタワー", "サイト共通・その他",
]


def page_label(t, path):
    m = re.search(r"<title>(.*?)</title>", t, re.S | re.I)
    s = html.unescape(m.group(1).strip()) if m else ""
    s = re.sub(r"｜?" + re.escape(SITE) + r"$", "", s).strip("｜ ")
    if not s:
        h = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S | re.I)
        s = re.sub(r"<[^>]+>", "", h.group(1)).strip() if h else ""
    lines = [x.strip() for x in re.split(r"[\r\n]+", s) if x.strip()]
    s = lines[0][:40] if lines else ""
    return s or path


FILE_RULES = [
    (r"^kof94-top", "KOF'94"), (r"^kof95-top", "KOF'95"), (r"^kof96-top", "KOF'96"),
    (r"^kof97-top", "KOF'97"), (r"^kof98um-top", "KOF'98UM"), (r"^kof98-top", "KOF'98"),
    (r"^kof99-top", "KOF'99"), (r"^kof00-top", "KOF2000"), (r"^kof01-top", "KOF2001"),
    (r"^kof02um-top", "KOF2002UM"), (r"^kof02-top", "KOF2002"), (r"^kof03-top", "KOF2003"),
    (r"^kofnw-top", "KOF NEOWAVE"), (r"^kofxi-top", "KOF XI"),
    (r"^02", "KOF2002"), (r"^94", "KOF'94"), (r"^96", "KOF'96"), (r"^98", "KOF'98"), (r"^99", "KOF'99"),
    (r"^(ff3|ffsp|rb1|mow)", "餓狼伝説"), (r"^(zansamu|samuzero)", "サムライスピリッツ"),
    (r"^(cvss|nbc|crush|seorii|tyouseikannkei|ローリング)", "その他の格闘ゲーム"),
]
MERGE = {
    "餓狼伝説SP": "餓狼伝説", "餓狼伝説3": "餓狼伝説", "リアルバウト餓狼伝説": "餓狼伝説", "餓狼MOW": "餓狼伝説",
    "CvsS2": "その他の格闘ゲーム", "NBC": "その他の格闘ゲーム", "CAPCOM VS. SNK 2": "その他の格闘ゲーム",
    "ネオジオバトルコロシアム": "その他の格闘ゲーム", "クラッシュ攻略": "その他の格闘ゲーム", "調整関係": "その他の格闘ゲーム",
}


def page_group(t, path):
    g = _page_group(t, path)
    g = MERGE.get(g, g)
    if "/" not in path and g in ("KOFシリーズ", "サイト共通・その他"):
        for pat, name in FILE_RULES:
            if re.match(pat, path):
                return name
    if g == "サイト共通・その他" and (path.startswith("kof") or re.match(r"KOF|ＫＯＦ", page_label(t, path))):
        return "KOFシリーズ"
    return g


def _page_group(t, path):
    if path.startswith("research/"):
        k = path.split("/")[1]
        return (RESEARCH[k][0] + " 研究アーカイブ") if k in RESEARCH else "KOFシリーズ"
    if path.startswith("social/idolmaster-cinderella-girls/"):
        return "アイドルマスター シンデレラガールズ"
    if path.startswith("msx/nobunaga-fuunroku/"):
        return "信長の野望・武将風雲録（MSX2版）"
    if path.startswith("msx/"):
        return "MSX"
    if path.startswith("puyo/"):
        return "ぷよぷよ・デスタワー"
    m = re.search(r'<p class="crumb">(.*?)</p>', t, re.S)
    if m:
        items = [html.unescape(x).strip() for x in re.findall(r"<a[^>]*>([^<]*)</a>", m.group(1))][1:]
        if len(items) >= 2 and items[0] == "KOF":
            g = items[1].replace("’", "'")
            return {"KOF NW": "KOF NEOWAVE", "KOFNEOWAVE": "KOF NEOWAVE", "KOFXI": "KOF XI"}.get(g, g)
        if items:
            g = items[0]
            if g == "KOF":
                return "KOFシリーズ"
            if g in ("CAPCOM VS. SNK 2", "ネオジオバトルコロシアム", "クラッシュ攻略", "調整関係"):
                return "その他の格闘ゲーム"
            return g
    return "サイト共通・その他"


def build_sitemap(pages):
    groups = defaultdict(list)
    for p, t in pages.items():
        if p in ("index.html", "sitemap.html") or p in HIDDEN or is_redirect(t):
            continue
        groups[page_group(t, p)].append((page_label(t, p), p))
    order = {g: i for i, g in enumerate(GROUP_ORDER)}
    keys = sorted(groups, key=lambda g: (order.get(g, len(order)), g))
    total = sum(len(v) for v in groups.values())
    toc = "".join(f'<li><a href="#g{i}">{html.escape(g)}</a>（{len(groups[g])}）</li>' for i, g in enumerate(keys))
    body = []
    for i, g in enumerate(keys):
        items = "".join(
            f'<li><a href="/{html.escape(p, quote=True)}">{html.escape(label)}</a></li>'
            for label, p in sorted(groups[g], key=lambda x: x[1])
        )
        body.append(f'<section class="section" id="g{i}"><h2>{html.escape(g)}（{len(groups[g])}）</h2><ul class="contents">{items}</ul></section>')
    return (
        '<!doctype html>\n<html lang="ja"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>全ページ一覧｜{SITE}</title>"
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&display=swap">'
        '<link rel="stylesheet" href="/assets/research.css"></head><body>'
        f'<header class="header"><div class="wrap topline"><a href="/" class="brand">{SITE}</a>{GLOBAL_NAV}</div></header>'
        '<div class="hero"><div class="wrap"><div class="breadcrumbs"><a href="/">トップ</a>'
        '<span aria-hidden="true"> / </span><b>全ページ一覧</b></div>'
        f'<h1>全ページ一覧</h1><p>サイト内の全{total}ページを作品別に並べています。このページは tools/normalize_site.py で自動生成しています。</p></div></div>'
        f'<main class="main"><div class="wrap"><section class="section"><h2>目次</h2><ul class="contents">{toc}</ul></section>'
        + "".join(body)
        + f'</div></main><footer class="footer"><div class="wrap">{SITE} ｜ 作成：MOT</div></footer></body></html>\n'
    )


# ---------- 5. 検索用データ ----------
def build_search_index(pages):
    import json
    import unicodedata
    out = []
    for p, t in sorted(pages.items()):
        if p in ("index.html", "sitemap.html") or p in HIDDEN or is_redirect(t):
            continue
        b = re.sub(r"<(script|style|head|header|footer|nav)\b[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
        b = re.sub(r'<p class="crumb">.*?</p>', " ", b, flags=re.S)
        b = html.unescape(re.sub(r"<[^>]+>", " ", b))
        b = unicodedata.normalize("NFKC", b)
        b = re.sub(r"[’‘`´]", "'", b)
        b = re.sub(r"\s+", " ", b).strip()
        label = unicodedata.normalize("NFKC", page_label(t, p)).replace("’", "'")
        out.append({"u": "/" + p, "t": label, "g": page_group(t, p), "x": b})
    return json.dumps(out, ensure_ascii=False, separators=(",", ":"))


def main():
    pages, changed = {}, 0
    for p in all_pages():
        full = os.path.join(ROOT, p)
        t = read(full)
        n = t if p == "sitemap.html" else fix_research_crumbs(p, fix_nav(p, fix_title(p, t)))
        if n != t:
            write(full, n)
            changed += 1
        pages[p] = n
    sm = build_sitemap(pages)
    full = os.path.join(ROOT, "sitemap.html")
    if read(full) != sm:
        write(full, sm)
        changed += 1
    idx = build_search_index(pages)
    full = os.path.join(ROOT, "search-index.json")
    if not os.path.exists(full) or read(full) != idx:
        write(full, idx)
        changed += 1
    print(f"{changed} files updated")


if __name__ == "__main__":
    main()
