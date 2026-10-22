# Regulatory Agent — Scientific AI Builder

> **Status (2026-10-22): Build04 FINAL frozen at Full Investigation v3.** This is an **AI-agent architecture learning and development-productivity experiment**, not a production-ready regulatory-compliance service.

## Start here — frozen decisions

| Track | Canonical artifact | Status |
| --- | --- | --- |
| Build01 Prompt-only | [NB04b](NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb) | Frozen, evaluated on Q1–Q10 |
| Build02 Static RAG | [NB03](NB03_final_hybrid_static_RAG.ipynb) + [NB04b](NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb) | Frozen, evaluated |
| Build03 Tools | [NB08](NB08_build03B_Q1_Q10_gap_analysis.ipynb) | Completed, evaluated |
| **Build04 FINAL — Full Investigation Agent v3** | **[NB09_v3.ipynb](NB09_v3.ipynb)** | **FROZEN / 10 questions evaluated** |
| Build04 experimental Lean RAG v4 | [NB09_v4_lean_Q5_Q9_Q10.ipynb](NB09_v4_lean_Q5_Q9_Q10.ipynb) | Completed Q5/Q9/Q10 ablation; **not final** |
| Build04 experimental Adaptive v4 | [NB09_v4_adaptive_Q5_Q9_Q10_fixed.ipynb](NB09_v4_adaptive_Q5_Q9_Q10_fixed.ipynb) | Completed Q5/Q9/Q10 ablation; **not final** |
| Next — ChatGPT-built versus Claude-built | Common neutral task brief (to be prepared) | Priority: independently build and evaluate |

The original [Adaptive v4 notebook](NB09_v4_adaptive_Q5_Q9_Q10.ipynb) is kept for provenance; the **fixed** notebook is the executed revision. Earlier NB09 variants remain in Git history/repository for learning and traceability. **Do not overwrite frozen Build04 v3 run JSONs**.

## Why this project exists

This deliberately uses the *same one-case, ten-question* benchmark (Türkiye-origin dried figs / aflatoxin B1) to study **Prompt → RAG → Tools → Investigation** architectures. It then asks a second question: **how do human-guided, AI-assisted development and independently AI-led ChatGPT/Claude development differ in elapsed time, human effort, implementation quality, inference cost and benchmark outcomes?** It does *not* claim regulatory generalization or live legal validity.

## Frozen Build01–04 evaluation

Independent user-reviewed labels against the unchanged Notion Gold Standard, **Yes counts out of 10**, not percentage accuracy:

| Build | Correct Yes | Grounded Yes | Complete Yes |
| --- | ---: | ---: | ---: |
| 01 Prompt | 5 | 0 | 2 |
| 02 Static RAG | 5 | 9 | 2 |
| 03 Tools | 9 | 6 | 4 |
| **04 Full Investigation v3 (Final)** | **8** | **10** | **3** |

Build04 v3 employs planning, hybrid/exact law retrieval, validation, coverage tracking, gap-driven research and final report/audit. It achieved highest Grounded among the four, **not** highest Correct or Complete. Its ten runs recorded **527,148 tokens**, **69 LLM calls**, **64 searches** and **2,232.93 seconds**.

## Three-question v4 pilot (Q5 / Q9 / Q10 only)

| Measurement | Full Investigation v3 | Lean RAG v4 | Adaptive Agent v4 |
| --- | ---: | ---: | ---: |
| Total tokens | 200,983 | 21,487 | 20,619 |
| LLM calls | 22 | 4 | 7 |
| Elapsed model-run time | 748.86s | 95.12s | 97.11s |

- v3 pilot source: [data/build04_nb09_v3_runs](data/build04_nb09_v3_runs)
- Lean source: [data/build04_nb09_v4_lean_runs](data/build04_nb09_v4_lean_runs)
- Adaptive source: [data/build04_nb09_v4_adaptive_runs](data/build04_nb09_v4_adaptive_runs)
- **Lean RAG uses QID-specific, previously discovered legal-article targets**. Its low-cost performance cannot establish autonomous regulation/provision discovery and is **development-set/overfit-sensitive**.
- **Adaptive Agent plans tool calls** but its coverage check is mostly presence/lookup oriented; it can miss core obligations despite successful searches.
- **Full Investigation v3** is the canonical educational implementation; its iterative evaluation is cost-heavy and not guaranteed complete.
- The v4 Q5/Q9/Q10 Correct / Grounded / Complete judgments are **proposals pending user confirmation**. Citation-format audit pass is not legal entailment verification.
- Token totals are **not a verified EUR cost calculation**. Scope, search implementation, prompting and call policy differ, so pilot results are not controlled causal comparisons.

## Next major experiment: AI-built Agent

Planned within the original sprint window:
1. **Oct 23:** prepare one neutral task brief and predefine input files, accepted output behavior and measurement protocol. Do not give initial AI builders past code, Gold answers or failure logs.
2. **Oct 26:** ChatGPT-led AI-built Agent, independently designed and executed.
3. **Oct 27:** Claude-led AI-built Agent under comparable constraints.
4. **Oct 28–29:** freeze artifacts and run unchanged Q1–Q10; compare Correct/Grounded/Complete, errors, evidence quality, elapsed time, active human time, intervention count, build/inference spend.
5. **Oct 30:** retrospective and Scientific AI Builder blog/portfolio summary.

**Deferred:** Full Investigation v4 refactor, new product/hazard cases and generalization, production hardening, deployment and live RASFF integration.

## Running and preservation

Run notebooks at the repository root (relative `data/` paths), using the same five frozen law snapshots and benchmark questions. Paid API runs are gated with explicit `RUN_OFFICIAL` (v3) / `RUN_PAID` (experimental v4) switches. Consult each notebook for dependencies. Keep the original Q1–Q10 Gold Standard separate from agent inputs; it is evaluation-only.

**Legal warning:** All outputs are experimental educational research based on dated legal snapshots; a consolidation date does not establish live applicability. Verify the operative law, product classification and shipment facts with competent sources before any compliance decision.

## References

- [4-Week Regulatory Agent Sprint (Notion)](https://app.notion.com/p/3f0695ed0f62807ab467ce8fcf5f6432)
- [Verified Reference & Build Comparison (Notion)](https://app.notion.com/p/3f3695ed0f6281889dd9eae76ddcf0b6)
- [2026 AI × Domain Roadmap (Notion)](https://app.notion.com/p/3ef695ed0f62817fbc75d0517b32abf1)

---
<details><summary>Historical README (Build01–02 phase, retained for research provenance)</summary>

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

</details>
