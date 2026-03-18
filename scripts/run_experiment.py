"""Run Qlib workflow via qlib CLI module.

This script runs the workflow using qlib.cli.run and the current Python executable.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Qlib workflow")
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "experiments" / "baseline.yaml"),
        help="Path to workflow config YAML",
    )
    args = parser.parse_args()

    cfg = Path(args.config).resolve()
    if not cfg.exists():
        raise SystemExit(f"Config not found: {cfg}")

    cmd = [sys.executable, "-m", "qlib.cli.run", str(cfg)]
    print("Running:", " ".join(cmd))
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
