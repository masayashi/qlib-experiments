# データ準備（Qlib）

このドキュメントは、Qlib のデータ準備手順を日本語でまとめたものです。

## 重要な注意

- Qlib の公式ドキュメント上で、既定の地域設定は中国（CN）と米国（US）に対応しています。
- 日本市場（JP）で利用する場合は、**自分でデータを用意し、Qlib形式に変換**して使う前提になります。

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

## 日本市場（JP）で使う場合

Qlib は既定で CN/US の地域設定を想定しています。そのため JP を使う場合は以下が必要です。

1. **日本株データの取得**
   - 例: JPX（J-Quants API / DataCube）などの公式データソース
2. **Qlib形式への変換**
   - Qlib のデータ形式に合わせて `~/.qlib/qlib_data/jp_data` に保存
3. **設定の更新**
   - `experiments/baseline.yaml` の `qlib_data.provider_uri` を JP データのパスに変更
   - `market` / `benchmark` / `backtest_config` を JP 市場仕様に合わせて調整

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
