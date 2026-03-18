# 実行手順

以下は最初のベースライン実験を動かすための最小手順です。

## 1. 環境セットアップ

```powershell
cd C:\home\github\qlib-experiments
.\scripts\setup_env.ps1
python .\scripts\check_qlib.py
```

## 2. データ準備

`docs/data_setup.md` を参照してデータを取得してください。

## 3. Qlib の初期化

Qlib は `qrun` 実行時に設定ファイルの `qlib_data` を読んで初期化されます。

現在の `experiments/baseline.yaml` は以下を想定しています。

- `~/.qlib/qlib_data/cn_data`
- 中国市場（CN）

別のデータを使う場合は `experiments/baseline.yaml` の
`qlib_data.provider_uri` と `qlib_data.region` を変更してください。

## 4. 実験の実行

```powershell
python .\scripts\run_experiment.py
```

## 5. 結果の確認

出力は Qlib のワークフロー管理により保存されます。
必要に応じて `docs/experiment_log.md` に記録してください。
