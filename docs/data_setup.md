# データ準備（Qlib）

このドキュメントは、Qlib のデータ準備手順を日本語でまとめたものです。

## 重要な注意

- 公式のデータセットは一時的に無効化されている旨が公式リポジトリに記載されています。公開データで試す場合は、コミュニティ提供データの利用が案内されています。
- 公開データは Yahoo Finance 由来であり、品質の保証はありません。高品質なデータがある場合はそちらの利用が推奨されています。

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

- 公式リポジトリの「Data Preparation」セクション
- Qlib のデータ関連ドキュメント
