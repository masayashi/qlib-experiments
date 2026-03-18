"""Export latest Qlib run artifacts into a readable report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import pandas as pd


def find_latest_artifact(root: Path, name: str) -> Path | None:
    candidates = list(root.rglob(name))
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def load_pickle(path: Path):
    return pd.read_pickle(path)


def write_df(obj, path: Path) -> None:
    if isinstance(obj, pd.DataFrame):
        obj.to_csv(path, index=True)
        return
    if isinstance(obj, dict):
        # Prefer common keys if present
        if "risk" in obj and isinstance(obj["risk"], pd.DataFrame):
            obj["risk"].to_csv(path, index=True)
            return
        # Fallback to JSON
        path.write_text(json.dumps(obj, default=str, indent=2), encoding="utf-8")
        return
    # Fallback to text
    path.write_text(str(obj), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export latest Qlib run artifacts")
    parser.add_argument(
        "--mlruns",
        default=str(Path(__file__).resolve().parents[1] / "mlruns"),
        help="Path to mlruns directory",
    )
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parents[1] / "results"),
        help="Output directory",
    )
    args = parser.parse_args()

    mlruns = Path(args.mlruns)
    if not mlruns.exists():
        raise SystemExit(f"mlruns not found: {mlruns}")

    latest_pred = find_latest_artifact(mlruns, "pred.pkl")
    latest_port = find_latest_artifact(mlruns, "port_analysis_1day.pkl")
    latest_ind = find_latest_artifact(mlruns, "indicator_analysis_1day.pkl")

    if latest_pred is None and latest_port is None and latest_ind is None:
        raise SystemExit("No artifacts found in mlruns")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out) / f"report_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_lines: list[str] = []
    summary_lines.append("# Qlib Report")
    summary_lines.append("")
    summary_lines.append(f"Generated: {ts}")
    summary_lines.append("")

    if latest_pred is not None:
        pred = load_pickle(latest_pred)
        if isinstance(pred, pd.DataFrame):
            pred_head = pred.head(50)
        else:
            pred_head = pd.DataFrame(pred).head(50)
        pred_path = out_dir / "pred_head.csv"
        pred_head.to_csv(pred_path, index=True)
        summary_lines.append(f"- pred: {pred_path}")

    if latest_port is not None:
        port = load_pickle(latest_port)
        port_path = out_dir / "port_analysis_1day.csv"
        write_df(port, port_path)
        summary_lines.append(f"- port_analysis: {port_path}")

    if latest_ind is not None:
        ind = load_pickle(latest_ind)
        ind_path = out_dir / "indicator_analysis_1day.csv"
        write_df(ind, ind_path)
        summary_lines.append(f"- indicator_analysis: {ind_path}")

    summary_path = out_dir / "summary.md"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"Report written to: {out_dir}")


if __name__ == "__main__":
    main()
