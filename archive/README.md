# Archive

This directory keeps intermediate experiments and superseded notebooks so the repository root stays focused on the official Build01/02 pipeline.

## diagnostics/

Retrieval and generation experiments used to understand failures before freezing Build02:

- dense-only retrieval baseline;
- hybrid retrieval diagnosis;
- deterministic multi-query/query-decomposition diagnosis;
- early Gemini / dense-RAG evaluation runs;
- initial OpenAI generation runs before the context-repaired NB04b rerun.

These notebooks are useful for tracing design decisions, but they are **not** the official final Build02 baseline.

## old_notebooks/

Earlier superseded notebook versions kept for provenance and learning history.

## Official Build01/02 notebooks

The current official notebooks remain at repository root:

1. `NB01_regulation_library.ipynb`
2. `NB02_chunking_v2_rowgroup_fix.ipynb`
3. `NB03_final_hybrid_static_RAG.ipynb`
4. `NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb`
