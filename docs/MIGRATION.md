# Repository layout migration

**Current state:** canonical and experimental notebook files were separated in a dedicated branch. The original `data/` directory (including source HTML, benchmark, processed caches and evaluation outputs) remains in its original location **intentionally** because frozen notebooks directly read and write `Path("data")`.

**Proposed future data migration:**
- `data/EU_*.html` → `data/legal_sources/`
- `data/benchmark_questions_v1.json` and benchmark/config manifests → `data/benchmark/`
- `data/parsed_regulation_library.json`, `data/chunks_*.json`, retrieval artifacts → `data/processed/`
- `data/build03_nb08_B_official_runs` → `results/build03/`
- `data/build04_nb09_v3_runs` → `results/build04/`
- Previous Build01–02 run outputs → `results/build01_02/`
- Other diagnostic results → `experiments/` or `archive/`

**Before moving data:** introduce a small, single path configuration shared by every canonical notebook, or use compatibility migration that preserves the original baseline. Validate static references and notebook CWD, then execute offline smoke checks from the root using a clean environment. Re-running paid Q1–Q10 is not required to confirm file-load paths. Keep immutable historical results and original Git history intact.

**Reproduction caution:** moving `.ipynb` files is not equivalent to changing process CWD. Start Jupyter from the project root; check `Path.cwd()` rather than assuming the current notebook folder is used.
