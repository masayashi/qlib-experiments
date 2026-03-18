# Qlib Experiment Project

This repo is for running and tracking experiments using the Qlib framework.

## Quick Start (Windows PowerShell)

```powershell
cd C:\home\github\qlib-experiments
.\scripts\setup_env.ps1
python .\scripts\check_qlib.py
```

## Suggested Layout

- `experiments/` : Experiment config files (YAML/JSON)
- `scripts/`     : Runner scripts and utilities
- `results/`     : Output logs, metrics, plots
- `docs/`        : Notes, references, experiment summaries

## First Experiment

- Start from `experiments/baseline.yaml`
- Run your experiment script (placeholder in `scripts/run_experiment.py`)
- Save outputs to `results/YYYYMMDD_expid/`

## Notes

- Keep configuration files versioned for reproducibility.
- Store large datasets outside Git and link them in docs.
