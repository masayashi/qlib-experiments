# Qlib Experiment Project

This repo is for running and tracking experiments using the Qlib framework.

## Quick Start

1. Create a Python virtual environment.
2. Install dependencies from `requirements.txt`.
3. Configure your experiment under `experiments/`.
4. Run your experiment and save results under `results/`.

## Suggested Layout

- `experiments/` : Experiment config files (YAML/JSON)
- `scripts/`     : Runner scripts and utilities
- `results/`     : Output logs, metrics, plots
- `docs/`        : Notes, references, experiment summaries

## First Experiment

- Start from `experiments/baseline.yaml`
- Run your experiment script (to be added in `scripts/`)
- Save outputs to `results/YYYYMMDD_expid/`

## Notes

- Keep configuration files versioned for reproducibility.
- Store large datasets outside Git and link them in docs.
