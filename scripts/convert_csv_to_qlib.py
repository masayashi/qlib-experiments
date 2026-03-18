"""Convert CSV data to Qlib binary format using dump_bin.py.

This script searches for dump_bin.py in a local Qlib repo. If not found,
please clone Qlib and set QLIB_REPO to its path.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def find_dump_bin() -> Path | None:
    candidates: list[Path] = []

    env_repo = os.environ.get("QLIB_REPO")
    if env_repo:
        candidates.append(Path(env_repo))

    # Common local clone location under the workspace
    candidates.append(Path(__file__).resolve().parents[2] / "microsoft" / "qlib")
    candidates.append(Path(__file__).resolve().parents[2] / "qlib")

    for repo in candidates:
        script = repo / "scripts" / "dump_bin.py"
        if script.exists():
            return script

    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert CSV to Qlib bin via dump_bin.py")
    parser.add_argument(
        "--csv-dir",
        default=str(Path.home() / ".qlib" / "csv_data" / "jp_data"),
        help="CSV directory (one CSV per symbol)",
    )
    parser.add_argument(
        "--qlib-dir",
        default=str(Path.home() / ".qlib" / "qlib_data" / "jp_data"),
        help="Output Qlib data directory",
    )
    args = parser.parse_args()

    dump_bin = find_dump_bin()
    if dump_bin is None:
        raise SystemExit(
            "dump_bin.py not found. Clone Qlib repo and set QLIB_REPO to its path."
        )

    repo_root = dump_bin.parent.parent

    csv_dir = Path(args.csv_dir).expanduser().resolve()
    qlib_dir = Path(args.qlib_dir).expanduser().resolve()
    qlib_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(dump_bin),
        "dump_all",
        f"--data_path={csv_dir}",
        f"--qlib_dir={qlib_dir}",
        "--include_fields=open,close,high,low,volume,factor",
        "--date_field_name=date",
    ]

    env = os.environ.copy()
    # Use Qlib source without compiling extensions
    env["PYTHONPATH"] = str(repo_root)

    print("Running:", " ".join(cmd))
    raise SystemExit(subprocess.call(cmd, env=env))


if __name__ == "__main__":
    main()
