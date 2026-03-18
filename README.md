# Qlib 実験プロジェクト

このリポジトリは、Qlib を使った実験の実行と記録のための作業場所です。

## クイックスタート（Windows PowerShell）

```powershell
cd C:\home\github\qlib-experiments
.\scripts\setup_env.ps1
python .\scripts\check_qlib.py
python .\scripts\prepare_jp_data.py --tickers-file .\docs\jp_tickers.txt --start 2015-01-01
$env:QLIB_REPO = "C:\home\github\microsoft\qlib"
python .\scripts\convert_csv_to_qlib.py
python .\scripts\run_experiment.py
```

## ディレクトリ構成

- `experiments/` : 実験設定ファイル（YAML/JSON）
- `scripts/`     : 実行スクリプト・ユーティリティ
- `results/`     : 実行結果（ログ、指標、図など）
- `docs/`        : メモ、参考、実験サマリ

## 最初の実験

- `experiments/baseline.yaml` を起点にする
- 実験スクリプトを実行（`scripts/run_experiment.py`）
- 出力は Qlib ワークフロー管理下に保存されます

## データ準備

データの準備方法は `docs/data_setup.md` にまとめています。

## 実行手順

詳細は `docs/run_guide.md` を参照してください。

## メモ

- 設定ファイルは必ずバージョン管理する（再現性のため）。
- 大きなデータは Git 管理外に置き、必要に応じて `docs/` で参照する。
