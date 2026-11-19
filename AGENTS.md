# Come sono bravo? サイト作業ルール

このリポジトリは MOT のゲーム攻略サイト「Come sono bravo?」（https://mot-csb.github.io/）です。
ページを追加・修正するAI・人は、以下に従ってください。

## サイト構成（2026/11/19 確定）

```
トップ（/index.html）
├ KOFシリーズ（/kof-top.html）
│   ├ 各作品トップ（/kof94-top.html 〜 /kofxi-top.html、/kofnw-top.htm）
│   │   └ 旧ページ（トップ直下の 02xxx.htm など）
│   └ 研究アーカイブ（/research/kof96/、/research/kof98/）← 新しいKOF研究はここ
├ 餓狼伝説・サムライスピリッツ・その他の格闘ゲーム（トップ直下の各 -top.html）
├ MSX（/msx/）└ 信長の野望・武将風雲録（/msx/nobunaga-fuunroku/）
├ ぷよぷよ（/puyo/death-tower/）
└ サイト情報（/sitemap.html＝全ページ一覧、/sonota.html、/main.html など）
```

## 必ず守ること

1. **既存ページのURLは変えない・移動しない。** トップ直下の旧ページ（約650件）は外部からリンクされているため、その場に置いたままにする。
2. **新しいページはフォルダに置く。** KOFの研究は `research/kofXX/`、MSXは `msx/作品名/`、ぷよぷよは `puyo/` の下。トップ直下に新しいページを増やさない。新しい作品は `作品分類/作品名/index.html` を入口にする。
3. **`arcade/` には何も置かない。** 中身は旧URL用の転送ページだけ。
4. **タイトルは「ページ名｜Come sono bravo?」。** 「MOT研究」「MOT KOF'96攻略研究」などの別名は付けない。トップページだけ「Come sono bravo?」。
5. **左上のロゴ表記は「Come sono bravo?」。** 新デザイン（`/assets/research.css`）のページの上部メニューは共通メニュー（トップ／KOF／作品一覧／MSX／ぷよぷよ／全ページ一覧）にする。作品ごとの移動はパンくず（例：トップ / KOF / KOF'96 / 研究アーカイブ）で行う。
6. **ページを追加したら、作品のトップ（例：/kof96-top.html、research/kof96/index.html）からリンクを張る。** どこからもリンクされていないページを作らない。
7. **作業の最後に `python3 tools/normalize_site.py` を実行する。** タイトル・共通メニュー・研究ページのパンくずをそろえ、全ページ一覧（/sitemap.html）とトップの検索用データ（/search-index.json）を作り直す。この2つは手で編集しない。
