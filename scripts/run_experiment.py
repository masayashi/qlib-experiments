"""Run Qlib workflow via qlib CLI module.

This script runs the workflow using qlib.cli.run and the current Python executable.
If QLIB_REPO is set, it will be added to PYTHONPATH to use source code.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def resolve_qlib_repo() -> Path | None:
    env_repo = os.environ.get("QLIB_REPO")
    if env_repo:
        p = Path(env_repo)
        if p.exists():
            return p

    # Try common local locations
    candidates = [
        Path(__file__).resolve().parents[2] / "microsoft" / "qlib",
        Path(__file__).resolve().parents[2] / "qlib",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


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

    cmd = [sys.executable, "-m", "qlib.cli.run", "workflow", str(cfg)]
    env = os.environ.copy()

    repo = resolve_qlib_repo()
    if repo is not None:
        env["PYTHONPATH"] = str(repo)

    print("Running:", " ".join(cmd))
    raise SystemExit(subprocess.call(cmd, env=env))


if __name__ == "__main__":
    main()
