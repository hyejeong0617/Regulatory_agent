# EU Food Regulatory Agent — Architecture Learning Lab

**Scientific AI Builder · Project 003 · Track A: Human-guided, AI-assisted development · October 2026**

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

## Companion implementation and shared comparison

This repository is **Track A** of [Scientific AI Builder — Project 003](docs/PROJECT003_COMPARISON.md). An [independent Codex-built Agent v1](https://github.com/hyejeong0617/regulatory-investigation-agent) was implemented under human-defined requirements without reusing these notebooks or answers. It is a separate Track B, **not** a fifth notebook build. See the [shared architecture and evaluation comparison](docs/PROJECT003_COMPARISON.md) for scope, provenance, and differences in assessment status. Track B's preliminary AI-assisted ratings have not yet been human-verified and are not included in the owner-reviewed Track A table above.

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
data/
  legal_sources/  # five frozen EUR-Lex HTML snapshots
  benchmark/      # fixed Q1–Q10 question set
  processed/      # parsed/chunked library and retrieval artifacts
results/
  build01_02/     # generated baseline records
  build03/        # NB08 Q1–Q10 execution outputs
  build04/        # NB09 v3 outputs + v4 pilot subfolders
docs/             # architecture, evaluation, limitations, migration notes
archive/          # prior notebook versions and older diagnostics
README.md
```

**Validation status:** Offline parsing and chunking reproduce the frozen JSON; local cached-model retrieval matches all 50 ordered chunks in NB03, NB08 and NB09 v3. Build04 graph initialization and its deterministic evidence/coverage/reporting tests pass. All 94 original data/result artifacts remain unchanged. This is selective offline validation, not proof that complete notebooks or paid generation reproduce historical runs. See [validation report](docs/VALIDATION.md).

## Reproducing the offline checks

Use **Python 3.11** and a fresh environment. Dependency installation needs internet; the tests themselves block network connections and writes to tracked research files.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python tests/check_layout.py
python tests/check_notebooks.py
python tests/offline_smoke.py
```

The default smoke test needs no model download or API key. For full local Dense + BM25 + RRF parity, pre-cache `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, then run `python tests/offline_smoke.py --dense`. The dense test fails if the model is unavailable; it does not download it. See [environment and cache instructions](docs/VALIDATION.md).

For interactive exploration, install `requirements-notebooks.txt` and run `jupyter lab`. The first code cell in each active/experimental notebook discovers the repository root from the kernel's current directory and parents. For a kernel launched outside the checkout, set `REGULATORY_AGENT_ROOT` to its absolute path before running that cell. Archived notebooks retain their historical assumptions.

Paid generation/live-probe flags now default to **False**, including the later NB09 override cell. **Do not Run All to inspect frozen results:** NB01–03 export cells and some later summary/config cells still write historical output paths even with paid calls disabled. Use the smoke script, which redirects permitted exports to a temporary directory and compares them with frozen artifacts. Any deliberate new experiment needs separate output paths before executing export or generation cells. Model prompts, retrieval algorithms, thresholds, and existing notebook outputs are unchanged.

## Build04 evaluation and experimental pilots

The full NB09 v3 Q1–Q10 evaluation recorded **527,148 tokens, 69 LLM calls, 64 searches**, and **2,232.93 s** aggregate elapsed time. Its Grounded result was strongest, but Correct and Complete remained below Build03-B.

The v4 pilot compared Q5/Q9/Q10 using existing [run outputs](results/build04/):

| Q5/Q9/Q10 only | Build04 v3 | Lean RAG v4 | Adaptive Agent v4 |
| --- | ---: | ---: | ---: |
| Tokens | 200,983 | 21,487 | 20,619 |
| LLM calls | 22 | 4 | 7 |
| Model-run time | 748.86s | 95.12s | 97.11s |

The Lean pilot uses QID-specific legal-article routes discovered during development; it is not a blind autonomous discovery benchmark. Pilot quality scores remain provisional. These figures do not establish controlled cost or latency superiority.

## Related independent experiment

A separate **Codex-built Regulatory Agent v1** was autonomously implemented as an AI-led coding experiment against the same domain brief. Ten run JSON records were obtained, including an incomplete Q9 execution. Its reviewed findings and comparison are kept in [Notion's Codex-built comparison](https://app.notion.com/p/401695ed0f6281989347c86c678e376e). The Codex implementation is **not part of this repository**; the [independent Codex-built repository](https://github.com/hyejeong0617/regulatory-investigation-agent) is available.

No claim of AI-led or human-guided general superiority follows from one case and differently resourced systems.

## Reproducibility, sources and limitations

- [Benchmark questions](data/benchmark/benchmark_questions_v1.json); fixed user-verified Gold Standard is maintained separately from generation inputs.
- The five original EUR-Lex files are under `data/legal_sources/`, the fixed questions under `data/benchmark/`, and derived datasets under `data/processed/`. Their consolidation dates are historical snapshots, **not live legal advice**.
- Some intermediate/diagnostic run outputs in `experiments/` and `archive/` predate the final build. Use the canonical links above for definitive implementations.
- See [4-Week Sprint](https://app.notion.com/p/3f0695ed0f62807ab467ce8fcf5f6432), [Verified Reference & Build Comparison](https://app.notion.com/p/3f3695ed0f6281889dd9eae76ddcf0b6), and [2026 AI × Domain Roadmap](https://app.notion.com/p/3ef695ed0f62817fbc75d0517b32abf1).

## License and third-party materials

Original software code and project-authored documentation for which the copyright holder can grant permission are available under the [MIT License](LICENSE) (Copyright © 2026 Hyejeong Lee).

**Third-party materials are not relicensed under MIT.** In particular, the EU legislation HTML snapshots in `data/legal_sources/` retain their original provenance and applicable reuse conditions. Other third-party materials, if any, remain subject to their own rights and licenses. See the frozen source metadata and repository documentation. The software is a research/portfolio implementation, not legal advice or an official EU or OpenAI service.
