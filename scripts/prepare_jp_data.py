"""Download JP stock data via yfinance and save as Qlib-compatible CSV.

The output CSV format matches Qlib dump_bin expectations:
- one CSV per symbol
- includes date, open, close, high, low, volume, factor
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd
import yfinance as yf


def read_tickers(path: Path) -> list[str]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    return [line for line in lines if line and not line.startswith("#")]


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    # yfinance columns: Open, High, Low, Close, Adj Close, Volume
    df = df.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
            "Date": "date",
        }
    )

    # If Date is index, move it to a column
    if "date" not in df.columns:
        df = df.reset_index().rename(columns={"Date": "date"})

    df = df.dropna(subset=["close"])

    # Adjust prices using adj_close/close factor
    df["factor"] = (df["adj_close"] / df["close"]).replace([float("inf"), -float("inf")], pd.NA)
    df["factor"] = df["factor"].fillna(1.0)

    for col in ["open", "high", "low", "close"]:
        df[col] = df[col] * df["factor"]

    out = df[["date", "open", "close", "high", "low", "volume", "factor"]].copy()
    out["date"] = pd.to_datetime(out["date"]).dt.strftime("%Y-%m-%d")
    return out


def download_one(symbol: str, start: str | None, end: str | None, interval: str) -> pd.DataFrame:
    data = yf.download(symbol, start=start, end=end, interval=interval, auto_adjust=False, progress=False)
    if data is None or data.empty:
        return pd.DataFrame()
    return normalize_ohlcv(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download JP stocks via yfinance and save CSV for Qlib")
    parser.add_argument("--tickers-file", required=True, help="Path to tickers list (one per line)")
    parser.add_argument("--start", default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default=None, help="End date (YYYY-MM-DD)")
    parser.add_argument("--interval", default="1d", help="Interval (default: 1d)")
    parser.add_argument(
        "--csv-dir",
        default=str(Path.home() / ".qlib" / "csv_data" / "jp_data"),
        help="Output CSV directory",
    )

    args = parser.parse_args()

    tickers = read_tickers(Path(args.tickers_file))
    if not tickers:
        raise SystemExit("No tickers found in tickers file")

    out_dir = Path(args.csv_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    failed: list[str] = []
    for t in tickers:
        df = download_one(t, args.start, args.end, args.interval)
        if df.empty:
            failed.append(t)
            continue
        out_path = out_dir / f"{t}.csv"
        df.to_csv(out_path, index=False)

    print(f"Saved CSVs to: {out_dir}")
    if failed:
        print("Failed tickers:")
        for t in failed:
            print(f"- {t}")


if __name__ == "__main__":
    main()
