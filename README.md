# Regulatory Agent

A learning project for testing how different AI architectures handle the **same EU food-regulation benchmark**.

The project is part of **Scientific AI Builder** and uses a fixed regulatory case:

> **Türkiye → dried figs → aflatoxin B1**

The goal is not simply to build an agent, but to understand what changes when the same Q1–Q10 benchmark is answered with:

**Prompt-only → Frozen Static RAG → Tools → Agent**

## Current status

| Stage | Build | Status | Main finding |
|---|---|---:|---|
| Week 1 | Build01 · Prompt-only | ✅ | Broad reasoning is possible, but legal claims can be weakly grounded and plausibly wrong. |
| Week 2 | Build02 · Frozen Static RAG | ✅ | Exact retrieved evidence improves grounding, but fixed Top-5 retrieval struggles with multi-provision questions. |
| Week 3 | Build03 · Tools | ⏳ Next | Test dynamic regulation search and current-law/version checking. |
| Week 4 | Build04 · Agent | ⏳ Planned | Add planning, evidence checking, retry/re-search, and uncertainty handling. |

## Week 1–2 architecture

```text
5 EUR-Lex source files
        ↓
NB01 — parse regulation library
        ↓
NB02 — legal-aware chunking
        ↓
NB03 — Dense + BM25 + RRF + diversification
        ↓
Frozen single-query Top-5 retrieval
        ↓
NB04b — same benchmark context + same LLM
        ↓
Prompt-only vs RAG evaluation
```

### Frozen Build02 retrieval

- Dense semantic retrieval: `sentence-transformers/all-MiniLM-L6-v2`
- Lexical retrieval: BM25
- Fusion: Reciprocal Rank Fusion (RRF, K=60)
- Candidate depth: 50
- Diversification: max 2 chunks per file/article-location group
- Final context: fixed Top-5
- Query decomposition: **off**
- LLM used during retrieval: **no**
- Iterative retrieval: **no**

This was intentionally frozen so that later Builds can be compared against a stable static-RAG baseline.

## Official notebooks

These are the main notebooks for the completed Build01/02 baseline.

| Notebook | Purpose |
|---|---|
| [`NB01_regulation_library.ipynb`](NB01_regulation_library.ipynb) | Parse the five EUR-Lex HTML files into a structured regulation library. |
| [`NB02_chunking_v2_rowgroup_fix.ipynb`](NB02_chunking_v2_rowgroup_fix.ipynb) | Create legal-aware chunks, including the Türkiye dried-fig Annex II row-group fix. |
| [`NB03_final_hybrid_static_RAG.ipynb`](NB03_final_hybrid_static_RAG.ipynb) | Freeze the final single-query hybrid retrieval baseline. |
| [`NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb`](NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb) | Official full Q1–Q10 Prompt-only vs RAG generation run with shared benchmark context. |

Intermediate retrieval experiments and superseded notebooks are kept under [`archive/`](archive/).

## Benchmark

The benchmark contains 10 regulatory questions about one shared case. The fixed question file is:

- [`data/benchmark_questions_v1.json`](data/benchmark_questions_v1.json)

Evaluation uses three labels:

- **Correct** — is the legal conclusion materially correct?
- **Grounded** — are major claims supported by the cited legal evidence?
- **Complete** — are the important conditions, exceptions, and uncertainties covered?

Each dimension is scored **Yes / Partial / No**.

## Build01 vs Build02 — key results

| Q | Prompt-only C / G / Comp | RAG C / G / Comp | Main observation |
|---|---|---|---|
| Q1 | Yes / Partial / Partial | Yes / Yes / Partial | RAG grounding improved; broader legal framework still incomplete. |
| Q2 | Yes / Partial / Partial | Yes / Yes / Partial | Both found 6/10; RAG grounded the values to the dried-fig row. |
| Q3 | No / No / No | Yes / Yes / Partial | Strongest RAG win: it corrected a false sorting-limit generalization. |
| Q4 | Partial / Partial / Partial | Yes / Yes / Yes | Exact Türkiye dried-fig Annex II row solved the question completely. |
| Q5 | Yes / Partial / Partial | Partial / Yes / No | Static Top-5 missed multiple required provisions. |
| Q6 | Yes / Partial / Partial | Partial / Yes / Partial | RAG found FBO duties but missed border/third-country authority evidence. |
| Q7 | Yes / Partial / Partial | Partial / Yes / No | Top-5 missed enforcement provisions already present in the library. |
| Q8 | Partial / Partial / Partial | Yes / Yes / Partial | Frozen RAG cannot establish whether the stored legal snapshot is still current law. |
| Q9 | Partial / Partial / Partial | Partial / Yes / No | Top-5 retrieved irrelevant provisions instead of the full legal-basis set. |
| Q10 | Partial / Partial / Partial | Partial / Yes / Partial | RAG stayed evidence-bounded but lacked enough provisions for complete synthesis. |

### Main conclusion

**RAG did not uniformly outperform Prompt-only.** It traded breadth for evidence-grounded precision.

- Prompt-only can reason broadly, but may produce plausible legal hallucinations.
- Static RAG can correct those errors when the right provision is retrieved.
- The dominant remaining Build02 failure is **retrieval coverage/ranking**, not missing source material.
- A frozen legal corpus is a snapshot and cannot prove current-law status.

This motivates Build03: instead of tuning static Top-5 retrieval further, let the model **search again when evidence is missing** and **check legal version/currentness separately**.

## Data

The [`data/`](data/) directory currently contains:

- five EUR-Lex source snapshots used for Build02;
- parsed regulation library and legal-aware chunks;
- frozen retrieval configuration and Top-5 results;
- Q1–Q10 benchmark file;
- generation outputs and comparison files;
- diagnostic retrieval outputs from intermediate experiments.

The frozen source versions are part of the experiment. They should not be interpreted as proof of the law currently in force.

## Repository structure

```text
Regulatory_agent/
├── README.md
├── NB01_regulation_library.ipynb
├── NB02_chunking_v2_rowgroup_fix.ipynb
├── NB03_final_hybrid_static_RAG.ipynb
├── NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb
├── data/
│   ├── EU_*.html
│   ├── benchmark_questions_v1.json
│   ├── parsed_regulation_library.json
│   ├── chunks_legal_aware.json
│   ├── retrieval_config_nb03_final_hybrid_static_rag.json
│   ├── retrieval_results_nb03_final_hybrid_static_rag.csv
│   └── ... experiment outputs
└── archive/
    ├── diagnostics/
    └── old_notebooks/
```

## Next — Build03 Tools

Build03 will test whether dynamic tools can solve the failures observed in Build02.

1. Study only the relevant parts of Hugging Face Agents Course:
   - Unit 2: agentic frameworks + tools
   - Unit 3: Agentic RAG
2. Implement **Regulation Search Tool** over the existing five-law library.
3. Use Q7 as a smoke test: can the system recover Articles 66/67/71/72 through additional search?
4. Add **Current-law / Version Check Tool** and test Q8.
5. Add an exact Regulation + Article/Annex lookup only if needed.
6. Re-run the same Q1–Q10 benchmark and compare Build02 vs Build03.

## Scope

This is a learning/evaluation project, not legal advice and not a production compliance system.

Out of scope for this sprint: multi-agent systems, fine-tuning, production deployment, large vector-database comparisons, and a polished UI.

RASFF search/analysis is intentionally deferred to the later **Food Safety Investigation Agent** project, where it fits the task more naturally.
