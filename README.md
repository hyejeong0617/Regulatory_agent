# EU Food Regulatory Agent — Architecture Learning Lab

**Scientific AI Builder · Human-guided, AI-assisted development · October 2026**

A controlled learning experiment comparing **Prompt-only → Static RAG → Tools → Investigation Agent** on one frozen EU food-regulatory case: **Türkiye-origin dried figs with aflatoxin B1 detected**.

> **Status:** Builds 01–04 completed and evaluated. **Build04 Full Investigation v3** is the frozen final implementation. Lean RAG and Adaptive Agent v4 are exploratory Q5/Q9/Q10 pilots, not final replacements. This is **not** a production regulatory compliance tool or legal advice.

## At a glance

Ten questions (Q1–Q10), one fixed case, five versioned EUR-Lex HTML snapshots. Each build was evaluated on **Correct**, **Grounded** and **Complete**, labeled Yes / Partial / No. Values below count **Yes only**, not Partial.

| Build | Correct | Grounded | Complete | Outcome |
| --- | ---: | ---: | ---: | --- |
| 01 · Prompt-only | 5/10 | 0/10 | 2/10 | Initial baseline; incorrect dried-fig sorting generalization |
| 02 · Static hybrid RAG | 5/10 | 9/10 | 2/10 | Better grounding, fixed Top-5 evidence coverage gaps |
| **03-B · Tools** | **9/10** | 6/10 | **4/10** | Highest Correct and Complete counts |
| **04 v3 · Investigation** | 8/10 | **10/10** | 3/10 | Highest Grounded count; costly iterative investigation |

These results describe one benchmark, not general regulatory accuracy. The human-guided builds used AI coding assistance.

## Canonical notebooks

| Stage | Files | Purpose |
| --- | --- | --- |
| Build01–02 · Source preparation | [NB01](notebooks/build01_02/NB01_regulation_library.ipynb) → [NB02](notebooks/build01_02/NB02_chunking_v2_rowgroup_fix.ipynb) | Parse frozen HTML laws and build legal-aware chunks |
| Build02 · Retrieval | [NB03](notebooks/build01_02/NB03_final_hybrid_static_RAG.ipynb) | Freeze Dense + BM25 + Reciprocal Rank Fusion (Top-5) |
| Build01–02 · Benchmark | [NB04b](notebooks/build01_02/NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb) | Matched prompt-only versus RAG Q1–Q10 run |
| Build03-B · Tools | [NB08](notebooks/build03/NB08_build03B_Q1_Q10_gap_analysis.ipynb) | Dynamic evidence/tool retrieval and Q1–Q10 evaluation |
| **Build04 · Final** | **[NB09_v3](notebooks/build04/NB09_v3.ipynb)** | Full Investigation workflow, frozen Q1–Q10 |

Exploratory notebooks belong in [Build03 diagnostics](experiments/build03_diagnostics) and [Build04 v4 pilots](experiments/build04_v4_pilots). Superseded variants stay under [archive](archive). Do **not** interpret pilot results as replacement Build04 scores.

## How the architectures differ

```text
Frozen EU-law documents
  ├─ Build01: prompt-only LLM (no retrieved evidence)
  ├─ Build02: parsing → legal chunks → dense/BM25/RRF → fixed Top-5 → LLM
  ├─ Build03: baseline retrieval + targeted tools and additional lookups
  └─ Build04: plan → retrieve/tools → validate → check coverage → re-search → report
```

**Observation:** Additional retrieval improves grounding when the right provision is available; more agent steps do not guarantee higher answer completeness.

## Repository layout

```text
notebooks/
  build01_02/     # canonical NB01–NB04b
  build03/        # canonical NB08
  build04/        # frozen NB09_v3
experiments/
  build03_diagnostics/
  build04_v4_pilots/
data/             # FROZEN LEGACY PATH — still used by existing notebooks
archive/          # prior notebook versions and older diagnostics
README.md
```

**Migration status:** This branch organizes notebooks without altering their execution logic. The originally recorded notebooks access `Path("data")` relative to the **current working directory**. Therefore, open and run them with the **repository root as the Jupyter working directory**; do not switch CWD to the notebook's folder. The desired `data/legal_sources`, `data/benchmark`, `data/processed` and `results/` split is **not yet applied**: moving those files without a coordinated path migration would break the frozen notebooks. See the migration PR before merging.

## Running the notebooks

From the **repository root**:

```bash
jupyter lab
```

In Jupyter, navigate to the notebook in `notebooks/` and verify `Path.cwd()` points to the repository root. Run notebook cells in NB01 → NB02 → NB03 → NB04b order to rebuild the early pipeline; NB08/NB09 depend on frozen upstream artifacts in `data/`. Install the imports required by each notebook in an appropriate environment; a consolidated dependency lockfile has **not** yet been verified.

**Important:** Paid execution is opt-in (see notebook-specific flags and credentials). The notebooks contain historical research runs; reproduction may invoke paid APIs. Do not rerun frozen benchmark outputs merely to view results. Internet access is required for some law-version checks.

## Build04 evaluation and experimental pilots

The full NB09 v3 Q1–Q10 evaluation recorded **527,148 tokens, 69 LLM calls, 64 searches**, and **2,232.93 s** aggregate elapsed time. Its Grounded result was strongest, but Correct and Complete remained below Build03-B.

The v4 pilot compared Q5/Q9/Q10 using existing [run outputs](data/):

| Q5/Q9/Q10 only | Build04 v3 | Lean RAG v4 | Adaptive Agent v4 |
| --- | ---: | ---: | ---: |
| Tokens | 200,983 | 21,487 | 20,619 |
| LLM calls | 22 | 4 | 7 |
| Model-run time | 748.86s | 95.12s | 97.11s |

The Lean pilot uses QID-specific legal-article routes discovered during development; it is not a blind autonomous discovery benchmark. Pilot quality scores remain provisional. These figures do not establish controlled cost or latency superiority.

## Related independent experiment

A separate **Codex-built Regulatory Agent v1** was autonomously implemented as an AI-led coding experiment against the same domain brief. Ten run JSON records were obtained, including an incomplete Q9 execution. Its reviewed findings and comparison are kept in [Notion's Codex-built comparison](https://app.notion.com/p/401695ed0f6281989347c86c678e376e). The Codex implementation is **not part of this repository**; a separate source-only repository is planned.

The earlier **Claude-built parallel comparison was cancelled**. No claim of AI-led or human-guided general superiority follows from one case and differently resourced systems.

## Reproducibility, sources and limitations

- [Benchmark questions](data/benchmark_questions_v1.json); fixed user-verified Gold Standard is maintained separately from generation inputs.
- The five original EUR-Lex files and derived datasets are kept under `data/` during migration. Their consolidation dates are historical snapshots, **not live legal advice**.
- Some intermediate/diagnostic run outputs in `data/` predate the final build. Use the canonical links above for definitive implementations.
- See [4-Week Sprint](https://app.notion.com/p/3f0695ed0f62807ab467ce8fcf5f6432), [Verified Reference & Build Comparison](https://app.notion.com/p/3f3695ed0f6281889dd9eae76ddcf0b6), and [2026 AI × Domain Roadmap](https://app.notion.com/p/3ef695ed0f62817fbc75d0517b32abf1).
