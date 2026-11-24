"""キャラ別フレームデータの「キャラ選択」を作る。

使い方: python3 tools/chara_roster.py kof2002um
  - tools/rosters/<作品>.json を読み、作品トップの <!-- roster:start --> ～ <!-- roster:end -->
    の間にチーム別のキャラ選択を書き出す。
  - 各キャラのページ（フレームデータ・ダメージ値・研究ページ・X投稿メモ）の本文冒頭に、
    そのキャラのページ一覧とキャラ選択へ戻るリンク（<!-- chara-nav:start --> ～ end）を入れる。
    X投稿メモのようにキャラが複数載るページは、キャラの見出しに id を付けるだけにする。
何度実行しても同じ結果になる。数値や本文は変更しない。
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# X投稿メモの見出し名 → キャラid（見出しの表記がキャラ選択と違うもの）
X_ALIASES = {"表クリス": "chris", "表ロバート": "robert", "シャンフェイ": "xiangfei", "リン": "lin"}


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def write(p, t):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="") as f:
        f.write(t)


def title_of(path):
    m = re.search(r"<title>(.*?)</title>", read(path.split("#")[0]), re.S)
    t = html.unescape(m.group(1)) if m else os.path.basename(path)
    return t.split("｜")[0].strip()


def frame_label(fn, title):
    if fn.endswith("-frame-data-2011.html"):
        return "ブログの表（2011年）"
    if fn.startswith("frame/"):
        return "ブログの表（2011年）"
    if "frame-data-" in fn and "-team-" in fn or "rugal-forms" in fn:
        return "ブログの表（チーム別ページ内）"
    if "frame-data-2025" in fn:
        return "ブログのまとめ（2025年）"
    if "frame-consolidation" in fn:
        return "統合版（2025年）"
    if "frame-sources" in fn or "original-frame-notes" in fn:
        return "ブログの表（2009年）と再編纂版"
    if fn.startswith("early-frame"):
        return "発売直後の硬直差（2009年）"
    m = re.search(r"（([0-9～]+年)）", title)
    return "ブログの表（" + (m.group(1) if m else "2009年") + "）"


def research_label(name, title, game):
    t = title.replace(game + " ", "").replace(game + "：", "")
    for pre in (name + "：", "表" + name + "：", "対" + name + "：", "KOF2002UM "):
        if t.startswith(pre):
            t = t[len(pre):]
    return t


def load(game):
    d = json.loads(read(f"tools/rosters/{game}.json"))
    base = d["base"]
    for team in d["teams"]:
        for c in team["chars"]:
            c["pages"] = []  # (種類, ファイル名, 表示名)
            for fn in c.get("frame", []):
                c["pages"].append(("frame", fn, frame_label(fn, title_of(base + fn))))
            for fn in c.get("data", []):
                c["pages"].append(("data", fn, "ダメージ・ガークラ値"))
            for fn in c.get("research", []):
                c["pages"].append(("research", fn, research_label(c["name"], title_of(base + fn), d["game"])))
            if c.get("x"):
                c["pages"].append(("x", c["x"] + "#c-" + c["id"], "X投稿メモ"))
    return d


def esc(s):
    return html.escape(s, quote=True)


def roster_html(d):
    base = "/" + d["base"]
    out = ['<div class="roster">']
    for team in d["teams"]:
        out.append(f'<section class="team"><h3>{esc(team["name"])}</h3><ul>')
        for c in team["chars"]:
            frames = [p for p in c["pages"] if p[0] == "frame"]
            others = [p for p in c["pages"] if p[0] != "frame"]
            if frames:
                main = f'<a class="cn" href="{base}{frames[0][1]}">{esc(c["name"])}</a>'
            else:
                main = f'<span class="cn">{esc(c["name"])}</span>'
            sub = []
            for kind, fn, label in frames[1:]:
                sub.append(f'<a href="{base}{fn}">{esc(label)}</a>')
            for kind, fn, label in others:
                if kind == "research":
                    continue
                sub.append(f'<a href="{base}{fn}">{esc(label)}</a>')
            research = [p for p in others if p[0] == "research"]
            line = f'<li id="c-{c["id"]}">{main}'
            if frames:
                line += f'<a class="fbtn" href="{base}{frames[0][1]}">フレームデータ</a><span class="fl">{esc(frames[0][2])}</span>'
            else:
                line += '<span class="fl">フレームデータ未掲載</span>'
            if sub:
                line += '<span class="sub">' + "".join(sub) + "</span>"
            if research:
                items = "".join(f'<li><a href="{base}{fn}">{esc(label)}</a></li>' for _, fn, label in research)
                line += f'<details><summary>研究・対策 {len(research)}件</summary><ul>{items}</ul></details>'
            line += "</li>"
            out.append(line)
        out.append("</ul></section>")
    out.append("</div>")
    return "\n".join(out)


def nav_html(d, c, here):
    base = "/" + d["base"]
    top = "/" + d["top"]

    def link(fn, label):
        return f"<b>{esc(label)}</b>" if fn.split("#")[0] == here else f'<a href="{base}{fn}">{esc(label)}</a>'

    main = [link(fn, label) for kind, fn, label in c["pages"] if kind in ("frame", "data")]
    if c.get("x"):
        main.append(f'<a href="{base}{c["x"]}#c-{c["id"]}">X投稿メモ</a>')
    research = [(fn, label) for kind, fn, label in c["pages"] if kind == "research"]
    out = (
        '<!-- chara-nav:start --><nav class="chara-nav" aria-label="キャラクター別のページ">'
        f'<p class="cn-head"><a href="{top}#c-{c["id"]}">{esc(d["game"])} キャラ選択</a><span>›</span><b>{esc(c["name"])}</b></p>'
        f'<p class="cn-links">{" ／ ".join(main)}</p>'
    )
    if research:
        opened = " open" if any(fn.split("#")[0] == here for fn, _ in research) else ""
        items = "".join(f"<li>{link(fn, label)}</li>" for fn, label in research)
        out += f'<details{opened}><summary>研究・対策 {len(research)}件</summary><ul>{items}</ul></details>'
    return out + "</nav><!-- chara-nav:end -->"


def put_nav(path, nav):
    t = read(path)
    t = re.sub(r"<!-- chara-nav:start -->.*?<!-- chara-nav:end -->", "", t, flags=re.S)
    m = re.search(r'<main class="main"><div class="wrap[^"]*">', t)
    if not m:
        print("  main が見つからない:", path)
        return
    t = t[: m.end()] + nav + t[m.end():]
    write(path, t)


def main(game):
    d = load(game)
    base = d["base"]
    # 1. 作品トップのキャラ選択
    top = read(d["top"])
    new = re.sub(
        r"<!-- roster:start -->.*?<!-- roster:end -->",
        lambda m: "<!-- roster:start -->\n" + roster_html(d) + "\n<!-- roster:end -->",
        top,
        flags=re.S,
    )
    if new == top and "<!-- roster:start -->" not in top:
        print("作品トップに roster の目印がありません:", d["top"])
    write(d["top"], new)
    # 2. 各ページのキャラ別ナビ（1ページを複数キャラが共有する場合は最初のキャラ）
    owner = {}
    for team in d["teams"]:
        for c in team["chars"]:
            for kind, fn, label in c["pages"]:
                if kind != "x":
                    lst = owner.setdefault(fn.split("#")[0], [])
                    if c not in lst:
                        lst.append(c)
    for fn, cs in owner.items():
        if len(cs) == 1:
            put_nav(base + fn, nav_html(d, cs[0], fn))
        elif all(len([p for p in c["pages"] if p[0] != "x"]) == 1 for c in cs):
            # チーム別ページなど、1ページに数キャラの表だけが載る場合は1本にまとめる
            names = " ／ ".join(
                f'<a href="{base}{c["pages"][0][1]}">{esc(c["name"])}</a>' if "#" in c["pages"][0][1] else f"<b>{esc(c['name'])}</b>"
                for c in cs
            )
            put_nav(base + fn, '<!-- chara-nav:start --><nav class="chara-nav" aria-label="キャラクター別のページ">'
                    f'<p class="cn-head"><a href="/{d["top"]}#chara">{esc(d["game"])} キャラ選択</a><span>›</span>{names}</p></nav><!-- chara-nav:end -->')
        else:
            navs = "".join(nav_html(d, c, fn) for c in cs)
            navs = navs.replace("<!-- chara-nav:end --><!-- chara-nav:start -->", "")
            put_nav(base + fn, navs)
    # 3. X投稿メモの見出しに id
    names = {}
    for team in d["teams"]:
        for c in team["chars"]:
            names[c["name"]] = c["id"]
    names.update(X_ALIASES)
    for xp in sorted({c["x"] for t in d["teams"] for c in t["chars"] if c.get("x")}):
        t = read(base + xp)

        def repl(m):
            name = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            if name in names:
                return f'<h2 id="c-{names[name]}">{m.group(2)}</h2>'
            return m.group(0)

        t = re.sub(r'<h2( id="c-[^"]*")?>(.*?)</h2>', repl, t)
        write(base + xp, t)
    print("done:", game, len(owner), "pages")


if __name__ == "__main__":
    main(sys.argv[1])
