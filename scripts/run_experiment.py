"""Simple placeholder runner.

Replace with actual Qlib experiment pipeline.
"""

from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    exp = base / "experiments" / "baseline.yaml"
    results = base / "results"
    results.mkdir(exist_ok=True)

    print(f"Using config: {exp}")
    print(f"Results dir: {results}")
    print("TODO: integrate Qlib pipeline")


if __name__ == "__main__":
    main()
