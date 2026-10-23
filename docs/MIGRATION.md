# Repository migration and verification

## Current organization

- `notebooks/build01_02/`: canonical NB01–NB04b
- `notebooks/build03/`: canonical NB08
- `notebooks/build04/`: frozen NB09_v3
- `experiments/build03_diagnostics/`: exploratory tools and historical diagnostic data
- `experiments/build04_v4_pilots/`: Lean/Adaptive pilot notebooks
- `data/legal_sources/`: five original versioned EUR-Lex snapshots
- `data/benchmark/`: Q1–Q10 benchmark questions
- `data/processed/`: parsed library, chunks and retrieval artifacts
- `results/build01_02/`, `results/build03/`, `results/build04/`: saved generation and evaluation outputs
- `archive/`: superseded notebooks and older diagnostic outputs

94 original `data/` blobs were moved without modifying their Git blob hashes. Source versions and saved answers were not regenerated. Notebook source references were edited to use the reorganized paths, preserving execution algorithms and existing paid-run switches.

## Path compatibility and execution defaults

All 16 canonical/experimental notebooks discover the repository root in their first code cell. Root and nested kernel directories are supported; external kernels require `REGULATORY_AGENT_ROOT`. The helper explicitly changes the kernel working directory to that root. Existing relative data, result, and cross-build paths then resolve consistently. Archived notebooks are historical records and were not changed.

Generation/live-probe defaults were disabled in NB04b, NB08, NB09 v3 (including its later override), and the three v4 pilots. This changes execution opt-in only, not prompts, algorithms, thresholds, or saved results. Existing export cells still target frozen paths; use `tests/offline_smoke.py` for safe inspection, not Run All. Future experiments must choose fresh output paths.

## Verification

See [VALIDATION.md](VALIDATION.md) for exact commands, dependency scope, results, and exclusions. The earlier clone/network limitation has been resolved. Selective real notebook cells now run offline with temporary outputs, while frozen artifact hashes are checked before and after execution.

`tests/frozen_artifacts.json` records SHA-256 hashes for all 94 historical HTML/JSON/JSONL/CSV artifacts at pre-validation commit `92dd5a2b33e2a52bdf18286ff2f1b82f7aab7d2c`. The original main commit `d04694c0b7bf9915ee47e7cd14a8f7bcc8c4fa2e` has the same 94 data blobs in the reorganized tree. No migration was repeated and no historical records were deleted.
