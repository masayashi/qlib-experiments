# 実行手順

以下は JP データで Qlib を使う最小手順です。

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

## 3. ルールベース戦略の単体実行

```powershell
python .\scripts\run_rule_backtest.py
```

`results/rule_backtest_YYYYMMDD_HHMMSS/` に以下が出力されます。

- `summary.md`
- `report_normal.csv`
- `benchmark_return.csv`
- `excess_return_without_cost.csv`
- `excess_return_with_cost.csv`

## 4. ルールベース戦略の比較実行（推奨）

```powershell
python .\scripts\run_rule_sweep.py
```

`results/rule_sweep_YYYYMMDD_HHMMSS/` に以下が出力されます。

- `summary.md`
- `sweep_results.csv`
- 各ケースの `report_lb*_k*_d*.csv`

## 5. 学習モデルベース実験の実行（必要な場合）

```powershell
python .\scripts\run_experiment.py
python .\scripts\export_report.py
```

## 6. 結果の保存先

実行結果は Qlib のワークフロー管理下に保存されます。
通常は `~/.qlib/qlib_data/.log` や `~/.qlib/` 配下の
実験ディレクトリに保存されます。

## 7. 記録

実験を回したら `docs/experiment_log.md` に記録してください。
