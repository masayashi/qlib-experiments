"""Run a rule-based strategy backtest on Qlib data.

Rule example:
- score = N-day return (close_t / close_{t-N} - 1)
- rank by score each day
- trade via TopkDropoutStrategy
"""

from __future__ import annotations

import argparse
import pickle
from datetime import datetime
from pathlib import Path

import pandas as pd

import qlib
from qlib.contrib.evaluate import backtest_daily
from qlib.contrib.evaluate import risk_analysis
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.data import D


def build_signal(instruments: str, start: str, end: str, lookback: int) -> pd.Series:
    # Pull close prices in Qlib feature format
    inst_obj = D.instruments(instruments) if isinstance(instruments, str) else instruments
    feat = D.features(inst_obj, ["$close"], start_time=start, end_time=end)
    if feat.empty:
        raise ValueError("No feature data loaded. Check provider_uri/instruments/date range.")

    close = feat["$close"].unstack(level="instrument").sort_index()
    score = close / close.shift(lookback) - 1.0
    score = score.stack().dropna()
    score.name = "score"
    return score


def run_backtest(
    signal: pd.Series, start: str, end: str, benchmark: str, topk: int, n_drop: int, cost: float
):
    strategy = TopkDropoutStrategy(signal=signal, topk=topk, n_drop=n_drop)
    report_normal, positions_normal = backtest_daily(
        start_time=start,
        end_time=end,
        strategy=strategy,
        account=100000000,
        benchmark=benchmark,
        exchange_kwargs={
            "deal_price": "close",
            "open_cost": cost,
            "close_cost": cost,
            "min_cost": 5,
            "limit_threshold": 0.1,
        },
    )

    analysis = {
        "benchmark_return": risk_analysis(report_normal["bench"]),
        "excess_return_without_cost": risk_analysis(report_normal["return"] - report_normal["bench"]),
        "excess_return_with_cost": risk_analysis(
            report_normal["return"] - report_normal["bench"] - report_normal["cost"]
        ),
    }
    return report_normal, positions_normal, analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Rule-based strategy backtest with Qlib")
    parser.add_argument("--provider-uri", default="~/.qlib/qlib_data/jp_data")
    parser.add_argument("--region", default="cn")
    parser.add_argument("--instruments", default="all")
    parser.add_argument("--benchmark", default="7203.T")
    parser.add_argument("--start", default="2023-01-01")
    parser.add_argument("--end", default="2026-03-17")
    parser.add_argument("--lookback", type=int, default=20)
    parser.add_argument("--topk", type=int, default=10)
    parser.add_argument("--n-drop", type=int, default=2)
    parser.add_argument("--cost", type=float, default=0.001)
    parser.add_argument("--out-dir", default=str(Path(__file__).resolve().parents[1] / "results"))
    args = parser.parse_args()

    qlib.init(provider_uri=args.provider_uri, region=args.region)

    signal = build_signal(args.instruments, args.start, args.end, args.lookback)
    report, positions, analysis = run_backtest(
        signal, args.start, args.end, args.benchmark, args.topk, args.n_drop, args.cost
    )

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out_dir) / f"rule_backtest_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(report, pd.DataFrame):
        report.to_csv(out_dir / "report_normal.csv")
    else:
        with open(out_dir / "report_normal.pkl", "wb") as f:
            pickle.dump(report, f)

    if isinstance(positions, pd.DataFrame):
        positions.to_pickle(out_dir / "positions_normal.pkl")
    else:
        with open(out_dir / "positions_normal.pkl", "wb") as f:
            pickle.dump(positions, f)

    summary_lines = [
        "# Rule-Based Backtest Summary",
        "",
        f"Generated: {ts}",
        f"Lookback: {args.lookback}",
        f"TopK: {args.topk}",
        f"NDrop: {args.n_drop}",
        f"Cost: {args.cost}",
        "",
    ]

    for name, df in analysis.items():
        out_csv = out_dir / f"{name}.csv"
        df.to_csv(out_csv)
        summary_lines.append(f"## {name}")
        summary_lines.append("")
        try:
            summary_lines.append(df.to_markdown())
        except Exception:
            summary_lines.append(df.to_string())
        summary_lines.append("")

    (out_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"Rule-based backtest report written to: {out_dir}")


if __name__ == "__main__":
    main()
