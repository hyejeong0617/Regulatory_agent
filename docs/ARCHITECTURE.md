# Architecture overview

This learning benchmark uses one regulatory case (Türkiye dried figs, aflatoxin B1) and five frozen EUR-Lex HTML snapshots.

| Stage | Canonical notebook | Architectural idea |
| --- | --- | --- |
| Build01 | `notebooks/build01_02/NB04b_*.ipynb` | Prompt-only generation |
| Build02 | `notebooks/build01_02/NB01–NB04b` | HTML parsing, legal-aware chunks, Dense + BM25 + RRF, fixed Top-5 |
| Build03-B | `notebooks/build03/NB08_*.ipynb` | Additional retrieval and targeted tools |
| Build04 v3 | `notebooks/build04/NB09_v3.ipynb` | Planning, retrieval, validation, gap-driven re-search and report |

The v4 Lean RAG and Adaptive Agent notebooks in `experiments/` are *ablations* using Q5/Q9/Q10, not replacements for Build04 v3.

**Execution boundary:** Canonical notebooks expect `Path("data")` with the **repository root as process CWD**. Reorganizing the notebook files alone should preserve their paths to `data/` under that launch convention. This has been statically inspected, not end-to-end executed. Do not move the `data/` directory without a compatibility/path migration.
