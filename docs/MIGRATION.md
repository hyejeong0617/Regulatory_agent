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

## Running notebooks

Run Jupyter from the repository root, rather than from inside `notebooks/`. Some historical code still uses `Path("data")` as a working-directory assertion, so `Path.cwd()` must be the repository root. If notebooks open in a Jupyter environment that changes the kernel CWD to their own folders, configure the notebook to run at root before executing.

Suggested sequence: NB01 → NB02 → NB03 → NB04b → NB08 → NB09_v3. The latter builds depend on earlier frozen artifacts; do not overwrite historical outputs with casual reruns. Paid calls require explicit notebook-specific opt-in.

## Verification status

- **Verified through GitHub object tree:** all 94 original data/result file blobs still exist unchanged (same SHA).
- **Verified through GitHub object tree:** README file links resolve to stored files.
- **Statically inspected:** 16 active and experimental notebooks for explicit file references after moving paths.
- **Not verified:** actually executing Jupyter notebooks, parsing HTML end-to-end, package dependency installation, external law APIs, paid model inference, and workflow parity after migration. The current environment could not clone the repository to run Python/Jupyter. Do not describe notebooks as runtime-tested.

## Additional offline checks

From a clone of this branch and a clean Python environment, check source files and generated artifacts exist, run `python tests/check_layout.py` (no API calls), and open the notebooks with `Path.cwd()` set to repository root. Next, selectively run read-only input-loading/parsing cells offline and compare expected row counts/identifiers before merging into `main`. A complete deterministic dependency lockfile remains future work.
