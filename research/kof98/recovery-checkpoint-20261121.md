# KOF'98 旧研究資料回収・第1次チェックポイント（2026-11-21）
本台帳は回収の進捗であり、未収録資料の一覧ではありません。KOF'98UMは別作品として扱います。

## 回収結果
- 全候補: 1718件（X 1341 / はてなブログ 360 / 旧サイト原稿 17）
- 暫定未照合: 1189件
- リポストによる暫定対象外: 399件
- KOF'98UMのみの可能性がある暫定対象外: 130件
- 内容・既存記事との個別突合せ: 未着手
- 既存記事の収録確認: 0件（未調査を意味する。未収録と判定したものではない）
- 新たな本文統合: 0件
- 新規研究記事: 0件

## 元資料
- `tweetまとめ.zip` 内の4つの tweets*.js（ID重複排除）
- `comesonobravo.hatenadiary.org.export.txt`（エントリーごとに原文抽出）
- `ＵＰしたもの.zip` の旧98系HTML/TXT
- `kof98.zip` はROMのみであり研究原稿として扱っていない

## 台帳
フルCSV（約3 MB、原文・日時・出典URL・キャラ・テーマ・状態）は2026-11-21の会話添付 `kof98_recovery_ledger_20261121.csv` に保存。大容量のためGitHubには本チェックポイントのみ登録した。

## 次の作業
1. 暫定対象外の誤判定を再点検する。
2. 既存の `research/kof98/index.html` と各記事本文・旧記事を個別に照合する。
3. 既存収録確認／要追記／未照合／要確認／対象外を確定し、台帳を更新する。
4. 本人の原文と他者引用、仮説と確定事項を区別して既存記事へ統合する。
5. 未解決事項は既存の `/kof-kininaru.html#kof98` に追加する。
6. `python3 tools/normalize_site.py` の実行と検索索引・サイトマップの再生成を行う。

既存URL、既存記事の本文はこのチェックポイントでは変更していない。


## 第2段階（2026-11-21）— 14件の個別照合
- 追加で原資料と既存サイトを照合: 14件
- 既存掲載先を確認: 12件（旧サイト同名URL 8件、はてなブログ研究の既存統合 4件）
- 既存記事に新たに追記: 2件（いずれもブログ原文由来の別論点）
- 新規研究記事: 0件
- 暫定未照合: **1175件**（第1段階1189件から14件処理）
- 暫定対象外（リポスト399／98UM中心130）: 529件（再点検は未実施）
- 全1,718件の原文入り改訂台帳: 会話添付 `kof98_recovery_ledger_20261121_phase2.csv`

### 既存掲載を確認した旧サイト原稿（8件）
| 原稿 | GitHub掲載先 |
| --- | --- |
| 98andy-tuuzyou.html | /98andy-tuuzyou.html |
| 98gsokushi.htm | /98gsokushi.htm |
| 98joe.html | /98joe.html |
| 98memo.html | /98memo.html |
| 98staff.html | /98staff.html |
| 98to02notigai.htm | /98to02notigai.htm |
| 98yu-zyunni.html | /98yu-zyunni.html |
| kof98-top.html | /kof98-top.html |

### 既存研究記事に本人原文の収録を確認したはてなブログ資料（4件）
| 原資料 | 既存掲載先 |
| --- | --- |
| [2025/04/15 防御力の計算推定](https://comesonobravo.hatenadiary.org/entry/2025/04/15/124835) | /research/kof98/defense-rating-2005-2025.html |
| [2024/12/29 大門の236A仕込み裏投げ](https://comesonobravo.hatenadiary.org/entry/2024/12/29/202331) | /research/kof98/daimon-previous-input-ura-nage-distance-2024.html |
| [2024/10/26 アテナ特殊版フェニックスアロー入力](https://comesonobravo.hatenadiary.org/entry/2024/10/26/200939) | /research/kof98/athena-phoenix-arrow-simultaneous-buttons-2015.html |
| [2024/08/13 見切れてバグ](https://comesonobravo.hatenadiary.org/entry/504336762.html) | /research/kof98/daimon-unfavorable-flag-mikirete-2024.html |

### 新たに追記した原資料（2件）
1. [2024/08/02 隙に無敵技等を入れ込む](https://comesonobravo.hatenadiary.org/entry/504217254.html) のうち **KOF'98・庵の屑風後の無敵技入れ込み**。既存 `iori-kuzukaze-hitstance-2008.html` に攻守が異なる研究として追記（commit `d6ee2b4f7b0bdc362e20df705108ec6fa462b142`）。
2. [2024/08/01 直接当たらない距離で通常技等⇒必殺技等の仕込み](https://comesonobravo.hatenadiary.org/entry/504208871.html) のうち **KOF'98京・屈A→無式の仕込み**。既存 `kyo-2362a-hold-36-input-2009.html` に2009年の入力手順とは別の間合い戦術として追記（commit `f7cd8acbc5bfe2071249e654b945c29444be2793`）。

### 限界・引き継ぎ
「既存収録確認」は原資料の代表的な主題・主要条件を既存本文と突合せたもので、全行の逐語一致・全数値検査を意味しない。対象外候補の再判定、未照合1175件の処理、全記事への導線追加、`python3 tools/normalize_site.py` と検索索引・サイトマップの再生成、およびPagesの配信検証は今後の作業。
