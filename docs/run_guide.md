# 実行手順

以下は最初のベースライン実験を動かすための最小手順です。

## 1. 環境セットアップ

```powershell
cd C:\home\github\qlib-experiments
.\scripts\setup_env.ps1
python .\scripts\check_qlib.py
```

**補足（Windows）**

- Qlib の一部は Cython 拡張を含むため、環境によっては
  Microsoft C++ Build Tools（MSVC）が必要です。

## 2. データ準備（JP / yfinance）

```powershell
python .\scripts\prepare_jp_data.py --tickers-file .\docs\jp_tickers.txt --start 2015-01-01
$env:QLIB_REPO = "C:\home\github\microsoft\qlib"
python .\scripts\convert_csv_to_qlib.py
```

`dump_bin.py` により、`~/.qlib/qlib_data/jp_data/instruments/all.txt` が生成されます。
この `all` を `experiments/baseline.yaml` の `instruments` に指定しています。

## 3. 実験の実行

```powershell
python .\scripts\run_experiment.py
```

## 4. レポート出力

```powershell
python .\scripts\export_report.py
```

`results/report_YYYYMMDD_HHMMSS/` にサマリが出力されます。

## 5. 結果の保存先

実行結果は Qlib のワークフロー管理下に保存されます。
通常は `~/.qlib/qlib_data/.log` や `~/.qlib/` 配下の
実験ディレクトリに保存されます。

確認方法は今後の運用に合わせて整理してください。

## 6. 記録

実験を回したら `docs/experiment_log.md` に記録してください。
