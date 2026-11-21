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

## 第3段階（2026-11-22）— 5件の個別照合

- 本段階の個別内容確認：5件（すべて本人はてなブログ原文）
- 既存研究・共通記事への収録を確認：3件
- 既存記事への追記：1件
- 要確認（既存掲載先の探索未完）：1件
- 今回の新規記事：0件
- 累計：既存収録確認15件、既存記事への追記3件、要確認1件、未照合1170件、暫定対象外529件、全1718候補。
- 改訂した原文入り全件CSV：会話内添付 `kof98_recovery_ledger_20261122_phase3.csv`（本リポジトリへは未アップロード）。
- 今回5件の照合詳細：会話内添付 `kof98_verified_phase3_20261122.csv`。

| 2024年原資料 | 判定 | 既存掲載先・作業 |
| --- | --- | --- |
| [10/26 大ジャンプ残像](https://comesonobravo.hatenadiary.org/entry/2024/10/26/202037) | 既存収録 | [本人のKOF98残像3個・12F](./jump-afterimage-kof95-2002-2024.html) と一致 |
| [9/3 236入力後のレバー方向](https://comesonobravo.hatenadiary.org/entry/2024/09/03/072820) | 既存収録 | [コマンド受付研究](./input-command-frames-2018-2024.html) に「789×〇〇／4N6×〇〇／123×××」等が掲載済み |
| [6/23 暗転同時投げ](https://comesonobravo.hatenadiary.org/entry/503737736.html) | 要確認 | 98・99・2002横断。既存記事の一括照合未了のため未収録とは断定しない。0F暗転／有利フラグ／レオナ覚醒の例外（2002）を分ける |
| [2/18 出せない超投げ・打撃投げ](https://comesonobravo.hatenadiary.org/entry/502398657.html) | 既存収録 | [確定地雷震の共通解説](/kof-kakuteizirai.html) に発見者・本人再現・技別結果が収録済み |
| [1/22 仕込み地震判定コンボ（仮）](https://comesonobravo.hatenadiary.org/entry/502143932.html) | 既存記事へ追記 | [大門の地雷震連続技](./daimon-jigoku-jirai-combo-2023.html) に **1ゲージ未満・立CD→6321463214A→弱地雷震** を別条件で追加（commit `63f2003bfd5b47d384947c8194d7c708fa2d4104`） |

注：2024年1月原稿の着想にはM-Ryan氏の投稿が明示される。本人による再現を出典元の独自発見と取り違えない。KOF2002の別技・別条件は98と混同しない。

**続き**：台帳判定「未照合」1170件から進める。「要確認」1件（暗転同時投げ）は既存サイト一括検索後に判定。特にリポスト・98UM中心の暫定除外529件を再点検する。既存記事に対する全行逐語照合、`python3 tools/normalize_site.py`、sitemap/search-index再生成、GitHub Pagesの配信確認は未実施。

## 第4段階（2026-11-22）— 旧サイト原稿5件を再分類
- 個別確認：5件（旧サイトZIPからの本文と現行GitHubを比較）
- 既存収録確認：1件（[98においての戦法と対策](/KOF98での戦法.html) は旧URLのまま現存）
- 対象外確定：4件（KOF98UMのシステム原稿1、98UM掲示板・案内の索引3）
- 新たな本文統合：0件、新規記事：0件
- [研究アーカイブ目次](./index.html) に旧戦法表へのリンクを追加（commit `9f4a3fe83dc195980c30619d26929294c78da9ca`）
- 第4段階原文台帳（全1718候補）：会話添付 `kof98_recovery_ledger_20261122_phase4.csv`
- 今回5件の詳細台帳：会話添付 `kof98_verified_phase4_20261122.csv`

**累計（第4段階後）**：1718候補＝既存収録確認16（旧URL9＋統合記事7）＋追記3＋要確認1＋未照合1165＋対象外533（暫定529、今回確定4）。

**重要**：「98においての戦法と対策」には紅丸の真空片手駒、チョイのウキー、ブライアンのめくりSBP、庵JDなどが原稿のまま掲載される。見出し・主要な対策を確認したが、全文の一字一句照合は未実施。98UM掲示板索引は無印98BBSへのリンクがあっても攻略研究資料とは判定しない。

## 第5・第6段階（2026-11-22）— X原文4件・ブログ1件を照合
- 本回の個別確認：**5件**。2016年の画面端入力に関する本人X投稿2件を**新しい研究記事1件**に統合、2017年の本人X投稿2件は既存記事収録を確認、2024年のはてなブログ1件（前回からの要確認）を既存研究へ追記。
- [新規：2016年の画面端の入力と表ロバート6B](./corner-direction-input-robert-2016.html)（本人X [8月14日・ロバート実測](https://x.com/mot_csb/status/764752056242450432)／[8月11日・左端の逆入力について伝聞を含むメモ](https://x.com/mot_csb/status/763613406444212224)）。本文掲載 commit `cf9ac497`、研究目次導線 `6931641d`。
- [共通「気になること」](../../kof-kininaru.html#kof98)に、1P/2P・端・直前行動・空キャン条件の未解明事項を追加（commit `60fffc68`）。
- [既存の垂直J・タメ延長・仕込み入力](./jump-input-buffer-tactics-2017.html)には、2017年5月10日[X投稿862306760891088905](https://x.com/mot_csb/status/862306760891088905)の滞空+2Fと2017年3月15日[X投稿841868129122844674](https://x.com/mot_csb/status/841868129122844674)の未検証ダッシュ623仕込みがすでに収録されていると確認。重複させない。
- 前回の要確認「暗転同時投げ」は、[暗転入力・ガード研究](./superflash-input-guard-2021.html)へ2024年6月23日の本人原稿を新節として追記（commit `35cad237`）。投げのダメージ・気絶値引継ぎ、0F暗転と有利フラグの説明を保存。2002レオナ覚醒の例外をKOF'98の成立事実へ流用しない。
- 改訂CSV：`kof98_recovery_ledger_20261122_phase6.csv`（会話添付、1718行）。個別明細は`kof98_verified_phase5_20261122.csv`（2件）、`kof98_verified_phase6_20261122.csv`（3件）。
- **累計の判定**（1718件）：既存収録確認18、新規記事へ統合2、既存記事へ追記4、対象外533（暫定529・確定4）、未照合1161。要確認0。
- 累計個別照合28件。補足：対象外暫定529件は内容再点検前なので個別照合済みには含めない。
- `tools/normalize_site.py`、sitemap/search-index更新、GitHub Pages HTTP確認はこの段階でも未実施（リポジトリ連携からの編集のみ）。
