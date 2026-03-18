# データ準備（Qlib）

このドキュメントは、Qlib のデータ準備手順を日本語でまとめたものです。

## 重要な注意

- Qlib の公式ドキュメント上で、既定の地域設定は中国（CN）と米国（US）に対応しています。
- 日本市場（JP）で利用する場合は、**自分でデータを用意し、Qlib形式に変換**して使う前提になります。

## 日本市場（JP）で使う場合（yfinance）

### 1. 銘柄リストを用意

テキストファイルで銘柄コードを用意します（1行1銘柄）。

例: `docs/jp_tickers.txt`

```
7203.T
6758.T
9984.T
9432.T
```

### 2. yfinance で日次データを取得

```powershell
python .\scripts\prepare_jp_data.py --tickers-file .\docs\jp_tickers.txt --start 2015-01-01
```

出力先は既定で `~/.qlib/csv_data/jp_data` です。

### 3. Qlib形式に変換

Qlib の `dump_bin.py` を使って変換します。

```powershell
# Qlibリポジトリをクローンしている場合
$env:QLIB_REPO = "C:\home\github\microsoft\qlib"
python .\scripts\convert_csv_to_qlib.py
```

出力先は既定で `~/.qlib/qlib_data/jp_data` です。

## JP向けのコスト設定について

`experiments/baseline.yaml` では JP 向けに**仮の取引コスト**を設定しています。
実運用や精緻な評価を行う場合は、あなたのブローカー条件に合わせて調整してください。

## 方式A: Qlib の取得スクリプトでダウンロード

Qlib 付属スクリプトでデータを取得し、Qlib形式に整形します。

### 中国市場（CN）

```bash
# 1日足データ
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# 1分足データ
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data_1min --region cn --interval 1min
```

### 米国市場（US）

```bash
# 1日足データ
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/us_data --region us
```

## 方式B: Qlib CLI でダウンロード

Qlib の CLI 経由で取得する方法もあります。

```bash
# 1日足データ
python -m qlib.cli.data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# 1分足データ
python -m qlib.cli.data qlib_data --target_dir ~/.qlib/qlib_data/cn_data_1min --region cn --interval 1min
```

## Qlib の初期化例

データを配置したら、以下のように初期化します。

```python
import qlib
from qlib.constant import REG_CN

qlib.init(provider_uri='~/.qlib/qlib_data/cn_data', region=REG_CN)
```

US を使う場合は、以下のように `REG_US` と `us_data` を指定します。

```python
import qlib
from qlib.config import REG_US

qlib.init(provider_uri='~/.qlib/qlib_data/us_data', region=REG_US)
```

## 参考

- 公式ドキュメントの初期化と地域設定
- JPX（J-Quants API / DataCube）
