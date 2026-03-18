"""Run Qlib workflow via qrun.

This script assumes Qlib is installed and a workflow config exists.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Qlib workflow with qrun")
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "experiments" / "baseline.yaml"),
        help="Path to workflow config YAML",
    )
    args = parser.parse_args()

    cfg = Path(args.config).resolve()
    if not cfg.exists():
        raise SystemExit(f"Config not found: {cfg}")

    cmd = ["qrun", str(cfg)]
    print("Running:", " ".join(cmd))
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
