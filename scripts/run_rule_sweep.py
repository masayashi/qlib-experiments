"""Sweep rule-based strategy parameters and compare performance."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd

import qlib
from run_rule_backtest import build_signal, run_backtest


def parse_int_list(raw: str) -> list[int]:
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


def metric_value(df: pd.DataFrame, key: str) -> float:
    if key in df.index:
        return float(df.loc[key, "risk"])
    return float("nan")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rule-based strategy parameter sweep")
    parser.add_argument("--provider-uri", default="~/.qlib/qlib_data/jp_data")
    parser.add_argument("--region", default="cn")
    parser.add_argument("--instruments", default="all")
    parser.add_argument("--benchmark", default="7203.T")
    parser.add_argument("--start", default="2023-01-01")
    parser.add_argument("--end", default="2026-03-17")
    parser.add_argument("--lookbacks", default="5,10,20,60")
    parser.add_argument("--topks", default="5,10,20")
    parser.add_argument("--n-drops", default="1,2,5")
    parser.add_argument("--cost", type=float, default=0.001)
    parser.add_argument("--out-dir", default=str(Path(__file__).resolve().parents[1] / "results"))
    args = parser.parse_args()

    lookbacks = parse_int_list(args.lookbacks)
    topks = parse_int_list(args.topks)
    n_drops = parse_int_list(args.n_drops)

    qlib.init(provider_uri=args.provider_uri, region=args.region)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out_dir) / f"rule_sweep_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []

    for lb in lookbacks:
        signal = build_signal(args.instruments, args.start, args.end, lb)
        for topk in topks:
            for nd in n_drops:
                report, _positions, analysis = run_backtest(
                    signal, args.start, args.end, args.benchmark, topk, nd, args.cost
                )

                bench = analysis["benchmark_return"]
                ex_wo = analysis["excess_return_without_cost"]
                ex_wc = analysis["excess_return_with_cost"]

                row = {
                    "lookback": lb,
                    "topk": topk,
                    "n_drop": nd,
                    "benchmark_annualized_return": metric_value(bench, "annualized_return"),
                    "benchmark_information_ratio": metric_value(bench, "information_ratio"),
                    "benchmark_max_drawdown": metric_value(bench, "max_drawdown"),
                    "excess_wo_cost_annualized_return": metric_value(ex_wo, "annualized_return"),
                    "excess_wo_cost_information_ratio": metric_value(ex_wo, "information_ratio"),
                    "excess_wo_cost_max_drawdown": metric_value(ex_wo, "max_drawdown"),
                    "excess_w_cost_annualized_return": metric_value(ex_wc, "annualized_return"),
                    "excess_w_cost_information_ratio": metric_value(ex_wc, "information_ratio"),
                    "excess_w_cost_max_drawdown": metric_value(ex_wc, "max_drawdown"),
                }
                rows.append(row)

                case_name = f"lb{lb}_k{topk}_d{nd}"
                if isinstance(report, pd.DataFrame):
                    report.to_csv(out_dir / f"report_{case_name}.csv")

    df = pd.DataFrame(rows)
    df = df.sort_values(by=["excess_w_cost_annualized_return", "excess_w_cost_information_ratio"], ascending=False)
    df.to_csv(out_dir / "sweep_results.csv", index=False)

    top = df.head(10)
    summary_lines = [
        "# Rule Sweep Summary",
        "",
        f"Generated: {ts}",
        f"Cases: {len(df)}",
        f"Lookbacks: {lookbacks}",
        f"TopKs: {topks}",
        f"NDrops: {n_drops}",
        "",
        "## Top 10 by excess_w_cost_annualized_return",
        "",
    ]

    try:
        summary_lines.append(top.to_markdown(index=False))
    except Exception:
        summary_lines.append(top.to_string(index=False))

    (out_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"Rule sweep report written to: {out_dir}")


if __name__ == "__main__":
    main()
