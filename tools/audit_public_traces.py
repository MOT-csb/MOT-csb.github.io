#!/usr/bin/env python3
"""Read-only audit of reader-visible published HTML/HTM for analysis and workflow traces.

Never alters published pages. Reports are created outside repository and uploaded
as a CI artifact; candidates require human review before editing.
"""
from __future__ import annotations
import argparse
import collections
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = {
    "internal_resource": r"Notion|notion\.so|app\.notion\.com|資料台帳|元資料台帳|作業台帳|内部研究記録|内部の解析根拠|解析根拠|原文台帳|内部台帳",
    "chat_or_editorial": r"本会話|このチャット|当チャット|AIが作業|ChatGPTとの会話|初回追記|AIによる編集|作業用メモ|内部管理",
    "analysis_method": r"ROM解析|RAM解析|逆アセンブ|逆アセン|ディスアセン|バイナリ解析|プログラム解析|解析スクリプト|実行アドレス|コードを解析|ROMを解析|ROMを調べ",
    "addresses": r"(?<![0-9A-Za-z])0x[0-9A-Fa-f]{4,8}\b|(?<![0-9A-Za-z])\$[0-9A-Fa-f]{4,8}\b|(?<![0-9A-Za-z])&H[0-9A-Fa-f]{4,8}\b",
    "code_trace": r"\b(?:MOVE\.[BWL]|LEA|JSR|JMP|RTS|LDIR|OUTI|INIR)\b|<code[^>]*>.*?(?:0x[0-9A-Fa-f]{4,8}|\$[0-9A-Fa-f]{4,8}).*?</code>",
}
REGEX = {k: re.compile(v, re.I | re.S if k=="code_trace" else re.I) for k,v in PATTERNS.items()}

class VisibleHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bits = []
        self.skip = 0
        self.skipping = []
    def handle_starttag(self, tag, attrs):
        if tag in ("script","style","svg","noscript"):
            self.skip += 1
            self.skipping.append(tag)
        if self.skip:
            return
        if tag in ("p","h1","h2","h3","h4","li","td","th","section","article","div"):
            self.bits.append("\n")
        for k,v in attrs:
            if k in ("href","src") and v and ("notion" in v.lower() or "gist.github" in v.lower()):
                self.bits.append(" " + v + " ")
    def handle_endtag(self, tag):
        if self.skipping and self.skipping[-1] == tag:
            self.skipping.pop()
            self.skip -= 1
        if not self.skip and tag in ("p","li","tr"):
            self.bits.append("\n")
    def handle_data(self, data):
        if not self.skip:
            self.bits.append(data)
    def get_text(self):
        return html.unescape(" ".join(self.bits))

def clip(s, a, b, radius=90):
    return re.sub(r"\s+", " ", s[max(0,a-radius):min(len(s),b+radius)]).strip()

def run(out: Path):
    files = sorted(p for p in ROOT.rglob("*") if p.is_file()
                   and p.suffix.lower() in (".html",".htm")
                   and ".git" not in p.parts and ".github" not in p.parts)
    markdown_records = sum(1 for p in ROOT.rglob("*.md") if ".git" not in p.parts and ".github" not in p.parts)
    results = []
    totals = collections.Counter()
    failed = []
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        try:
            raw = p.read_text("utf-8")
        except Exception as ex:
            failed.append({"path":rel,"error":str(ex)})
            continue
        if p.suffix.lower() in (".html",".htm"):
            parser = VisibleHTML()
            try: parser.feed(raw)
            except Exception as ex:
                failed.append({"path":rel,"error":"HTML parse: "+str(ex)})
            body = parser.get_text()
        else:
            body = raw
        hits = []
        for category, regex in REGEX.items():
            for match in regex.finditer(body):
                hits.append({"kind":category,
                             "excerpt":clip(body,match.start(),match.end()),
                             "match":match.group(0)[:100]})
                totals[category]+=1
        if hits:
            results.append({"path":rel, "hits":hits[:60], "total_hits":len(hits),
                            "more_hits_omitted":max(0,len(hits)-60)})
    payload = {
        "examined_files":len(files),
        "repository_markdown_records_not_scanned":markdown_records,
        "files_with_candidates":len(results),
        "candidate_hits":dict(totals),
        "read_errors":failed,
        "pages":results
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf8")
    print("FILES_SCANNED",len(files))
    print("REPOSITORY_MARKDOWN_RECORDS_EXCLUDED",markdown_records)
    print("FILES_WITH_CANDIDATES",len(results))
    print("CANDIDATE_COUNTS",json.dumps(dict(totals),ensure_ascii=False))
    print("READ_ERRORS",len(failed))
    for x in results[:85]:
        print("PAGE",x["path"],"HITS",x["total_hits"])
        for h in x["hits"][:3]:
            print(" ",h["kind"],h["excerpt"][:240])
    print("FULL_REPORT_JSON",str(out))
    return len(files)

if __name__=="__main__":
    arg=argparse.ArgumentParser()
    arg.add_argument("--output",default="/tmp/csb-audit/public-traces.json")
    args=arg.parse_args()
    try:
        count=run(Path(args.output))
        if count==0:
            sys.exit("No public pages found")
    except Exception:
        raise
