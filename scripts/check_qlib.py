"""Smoke check for Qlib installation."""

from __future__ import annotations


def main() -> None:
    try:
        import qlib  # type: ignore
    except Exception as exc:  # pragma: no cover - diagnostic path
        print("Qlib import failed.")
        print(f"Error: {exc}")
        raise SystemExit(1)

    version = getattr(qlib, "__version__", "unknown")
    print(f"Qlib import OK. Version: {version}")


if __name__ == "__main__":
    main()
