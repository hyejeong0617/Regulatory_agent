"""Offline repository layout check. Never imports notebooks or calls external APIs."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCES = sorted((ROOT / "data/legal_sources").glob("EU_*.html"))
assert len(SOURCES) == 5, f"Expected five frozen EU law sources, got {len(SOURCES)}"
REQUIRED = [
    "data/benchmark/benchmark_questions_v1.json",
    "data/processed/parsed_regulation_library.json",
    "data/processed/chunks_legal_aware.json",
    "data/processed/retrieval_results_nb03_final_hybrid_static_rag.csv",
    "results/build01_02/nb04b_context_repaired_openai_luna_answers_comparison.csv",
    "results/build03/manifest.json",
    "results/build04/manifest.json",
    "notebooks/build01_02/NB01_regulation_library.ipynb",
    "notebooks/build01_02/NB02_chunking_v2_rowgroup_fix.ipynb",
    "notebooks/build01_02/NB03_final_hybrid_static_RAG.ipynb",
    "notebooks/build01_02/NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb",
    "notebooks/build03/NB08_build03B_Q1_Q10_gap_analysis.ipynb",
    "notebooks/build04/NB09_v3.ipynb",
]
missing = [f for f in REQUIRED if not (ROOT / f).is_file()]
assert not missing, f"Missing required files: {missing}"

benchmark = json.loads((ROOT / "data/benchmark/benchmark_questions_v1.json").read_text(encoding="utf-8"))
assert benchmark, "Benchmark empty"
for path in (ROOT / "notebooks").rglob("*.ipynb"):
    obj = json.loads(path.read_text(encoding="utf-8"))
    assert "cells" in obj and isinstance(obj["cells"], list), path
print(f"PASS: {len(SOURCES)} EU files, {len(REQUIRED)} essential paths and notebook JSON structures")
print("NOTE: This does not execute any notebook or validate API behavior.")
