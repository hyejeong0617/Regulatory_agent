# EU Food Regulatory Agent — AI Architecture Evaluation

**Scientific AI Builder · Project 003 | Food Safety × Regulatory Intelligence × Applied AI**

A case-driven research project investigating how **retrieval, tools and agentic investigation** affect the correctness, evidence grounding and completeness of EU food-regulatory answers.

**[▶ Open the AI Architecture Evaluation Explorer](https://regulatoryagent-comparison.streamlit.app/)** · [View the Streamlit source](evaluation_explorer/app.py) · [Compare all five implementations](docs/PROJECT003_COMPARISON.md) · [Explore the independent Codex-built agent](https://github.com/hyejeong0617/regulatory-investigation-agent)

> **Research demo, not a live regulatory assistant.** The Streamlit app displays original, saved Q1–Q10 answers and selected supporting records. It does **not** generate new answers, validate current legislation or provide legal advice. The hosted URL was supplied after deployment by the project owner; full hosted/browser QA has not been independently verified here.

## Project at a glance

| | Research scope |
| --- | --- |
| **Research question** | How do increasing levels of retrieval, tools and investigation change **Correct**, **Grounded** and **Complete** outcomes? |
| **Case** | Türkiye-origin dried figs with aflatoxin B1 detected |
| **Benchmark** | 10 related questions about **one** case; five frozen EU-law HTML snapshots |
| **Implementations** | Four human-guided Track A builds + one independent Codex-built Track B agent |
| **Interactive demo** | Read-only Streamlit Explorer showing **50 saved question–implementation answers/records** |
| **Central finding** | Stronger source grounding did **not** consistently lead to greater correctness or completeness |

### Try the interactive demo

The **[AI Architecture Evaluation Explorer](https://regulatoryagent-comparison.streamlit.app/)** lets visitors:

1. Inspect five implementations' frozen Yes-only evaluation totals.
2. Select Q1–Q10 and compare **original saved answers side by side**, including Build 03-B versus Build 04 v3.
3. Expand available retrieved legal excerpts, run metadata and original GitHub source links.
4. Explore documented failure modes, including Codex v1's **incomplete Q9 run**.

All answer texts come from the original published artifacts bundled with the app. There is **no OpenAI API key, paid inference or live law lookup**. See [Explorer methodology and local setup](evaluation_explorer/README.md).

## From RASFF data analysis to a regulatory AI research question

This project started with exploratory analysis of EU Rapid Alert System for Food and Feed (**RASFF**) notifications from 2020–2025, rather than an arbitrary chatbot prompt.

```text
RASFF notification EDA
    ↓ origin × food category × hazard patterns
Three candidate regulatory scenarios
    ↓ research selection
Türkiye · dried figs · aflatoxin B1
    ↓ ten related regulatory questions + frozen EU legal corpus
Prompt-only → Hybrid RAG → Tools → Investigation Agent
    ↘ independent Codex-built implementation and comparative evaluation
```

The three candidate scenarios were **Poland / poultry / Salmonella Enteritidis**, **Türkiye / dried figs / aflatoxin B1** and **India / sesame seeds / ethylene oxide**. The Türkiye scenario was selected for a focused, multi-provision regulatory investigation, including contaminant limits, import controls, operator responsibilities and source-based synthesis.

**Public case-selection evidence:** [category-level RASFF candidates](https://github.com/hyejeong0617/rasff_risk_predictor/blob/main/RASFF_Rebuild/artifacts/regulatory_agent_case_candidates.csv), [individual-hazard candidates](https://github.com/hyejeong0617/rasff_risk_predictor/blob/main/RASFF_Rebuild/artifacts/regulatory_agent_individual_hazard_candidates.csv) and [subject/product drilldown](https://github.com/hyejeong0617/rasff_risk_predictor/blob/main/RASFF_Rebuild/artifacts/regulatory_agent_subject_drilldown.csv).

The saved analysis includes **297** Türkiye-origin *fruits and vegetables* notifications involving aflatoxin B1—**not 297 dried-fig-only notifications**. Notification frequencies do not measure product-specific incidence or population risk, and the scenario was **not** selected by a statistically validated optimization algorithm.

**RASFF was used for case discovery and research design only:** it was **not** model-training data, the agent's runtime retrieval corpus or the legal answer reference. Regulatory assessment used five frozen historical EUR-Lex snapshots and a separately maintained owner-verified reference.

## Architecture design — Track A

| Build | Approach | What was tested |
| --- | --- | --- |
| **01 · Prompt-only** | LLM without retrieved legal evidence | Baseline response generation |
| **02 · Hybrid RAG** | Legal-aware chunks, dense retrieval + BM25 + reciprocal rank fusion, fixed Top-5 context | Whether static retrieval improves evidence grounding |
| **03-B · Tools** | Retrieval plus targeted search and related tool calls | Whether targeted evidence gathering closes missing-provision gaps |
| **04 v3 · Investigation** | Plan → retrieve/tools → validate → check issue coverage → re-search → report | Whether multi-step investigation improves grounded and complete analysis |

**Build 04 v3 is the frozen final Track A implementation.** Build 04 v4 Lean RAG and Adaptive Agent were **three-question (Q5/Q9/Q10) exploratory pilots**, not replacements for its final benchmark.

The companion **[Track B — Codex-built Regulatory Agent v1](https://github.com/hyejeong0617/regulatory-investigation-agent)** was independently architected and coded by Codex under human-defined requirements, source materials, evaluation constraints and budget. It is a distinct implementation, **not a fifth Track A notebook** and not a controlled human-versus-AI productivity study.

## Frozen evaluation results

The same ten related questions were assessed for **Correct** (material conclusions), **Grounded** (traceable legal evidence) and **Complete** (coverage of required issues/conditions). The categorical ratings were **Yes / Partial / No**; the numbers below count **Yes only**.

| Implementation | Correct | Grounded | Complete |
| --- | ---: | ---: | ---: |
| Build 01 · Prompt-only | 5/10 | 0/10 | 2/10 |
| Build 02 · Hybrid RAG | 5/10 | 9/10 | 2/10 |
| **Build 03-B · Tools** | **9/10** | 6/10 | **4/10** |
| **Build 04 v3 · Investigation** | 8/10 | **10/10** | 3/10 |
| Codex-built v1 | 5/10 | 8/10 | 2/10 |

**What the results show within this case:**

- **Grounding ≠ completeness.** Static RAG greatly improved the number of grounded responses over the prompt-only baseline without improving the count of complete responses.
- **More agent steps ≠ best answer quality.** Build 04 v3 had the highest grounding count, while Build 03-B had the highest correctness and completeness counts.
- **Failure analysis matters.** The independent Codex-built agent exposed quotation-validation over-rejection (Q2), complex Annex/table and procedural gaps, and an **incomplete execution at Q9**. The latter is an execution limitation, **not** demonstrated erroneous legal reasoning.

**Evidence and grading boundary:** Track A totals are historical owner-reviewed aggregates; not every final question-level judgment can be reconstructed from the public worksheets, and the detailed reference is private. Track B's initial AI-assisted question-level ratings (2026-10-22) were individually confirmed by the owner (2026-10-23) without changes, **not independently externally validated**. Codex Q5 is a retained development-exposed smoke run. See [Track A evaluation](docs/EVALUATION.md), [combined methodology and scores](docs/PROJECT003_COMPARISON.md) and [Track B quality evaluation](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/QUALITY_EVALUATION.md).

### Efficiency is an exploratory observation, not a controlled comparison

The frozen Build 04 v3 Q1–Q10 run recorded **527,148 tokens, 69 LLM calls, 64 searches and 2,232.93 seconds**. A later pilot limited to Q5/Q9/Q10 recorded:

| Pilot Q5/Q9/Q10 | Tokens | LLM calls | Run time |
| --- | ---: | ---: | ---: |
| Build 04 v3 | 200,983 | 22 | 748.86 s |
| Lean RAG v4 | 21,487 | 4 | 95.12 s |
| Adaptive Agent v4 | 20,619 | 7 | 97.11 s |

The Lean pilot used development-informed **question-ID-specific routes**, so these figures **do not establish blind generalization, controlled latency/cost superiority or equivalent answer quality**.

## My contribution and AI collaboration

**Project owner:** problem formulation; RASFF-informed scenario selection; regulatory research and benchmark question design; human-guided architecture direction for Track A; evaluation criteria, answer review, interpretation and scientific limitations.

**AI-assisted implementation:** code and documentation support for Track A. **Codex-led independent development:** Track B architecture and implementation within owner-specified research requirements, frozen legal corpus and budget. This work does not claim sole manual coding authorship or independently certified regulatory accuracy.

**Methods / technologies:** Python, Jupyter, legal-source parsing, dense retrieval, BM25, reciprocal rank fusion (RRF), LLMs, tool calling, investigation workflows, structured run logs, evidence/coverage checking, Streamlit and GitHub CI.

## Explore code, results and reproducibility

| Resource | What to inspect |
| --- | --- |
| [Explorer](evaluation_explorer/README.md) · [source](evaluation_explorer/app.py) | Read-only demo with bundled Q1–Q10 answer records, two-column comparison and local setup |
| [Benchmark questions](data/benchmark/benchmark_questions_v1.json) | Ten fixed questions; private verified legal-answer reference excluded |
| [Canonical notebooks](notebooks/) | Build sequence and original experiments |
| [Track A frozen results](results/) | Saved generation outputs, tool runs, agent outputs and three-question v4 pilots |
| [Five-implementation comparison](docs/PROJECT003_COMPARISON.md) | Track A/B boundaries, evidence provenance and quality scores |
| [Offline validation](docs/VALIDATION.md) | Checks performed, historical dense parity and reproducibility boundaries |
| [Track B repository](https://github.com/hyejeong0617/regulatory-investigation-agent) | Separate Codex-built CLI, frozen Q1–Q10 records and execution report |

### Run the Explorer locally

```bash
python -m pip install -r evaluation_explorer/requirements.txt
python -B evaluation_explorer/test_data.py
streamlit run evaluation_explorer/app.py
```

The Explorer uses **bundled public historical output** and requires no API key. For the research notebooks and offline checks, use **Python 3.11**, install `requirements.txt`, then run:

```bash
python tests/check_layout.py
python tests/check_notebooks.py
python tests/offline_smoke.py
```

The current post-redaction checkout passed selective layout, notebook syntax/root discovery, **94 frozen artifact hash** and guarded non-dense offline smoke checks on 2026-11-05. Historical dense retrieval parity was **not** rerun; neither were paid generation, complete notebooks or live-law checks. **Do not run all notebooks casually:** some historical export cells can overwrite saved output paths. Details: [validation](docs/VALIDATION.md), [migration/privacy provenance](docs/MIGRATION.md).

## Limitations and research status

1. **Limited evaluation scope:** one dried-fig case, ten related and development-exposed questions; no independent, held-out multi-case evaluation.
2. **Evaluation provenance:** private reference, incomplete public Track A individual grading trail, and no independent external adjudication.
3. **Unequal implementation conditions:** architectures, prompts, search strategies and budgets differed; results do not prove one development approach is generally superior.
4. **Historical law and retrieval gaps:** five archived EU-law versions, complex Annex conditions and missing external provisions; **not current compliance guidance or a production system**.

**Status: Research builds and frozen outputs complete; interactive historical-results Explorer deployed (owner-reported URL).** Future work could evaluate unseen regulatory cases and establish a multi-case benchmark with independently reviewed grading and standardized budgets; these **have not been implemented**.

## License and source materials

Original software and project-authored documentation available under the [MIT License](LICENSE) (Copyright © 2026 Hyejeong Lee). Third-party EUR-Lex HTML snapshots and other external materials retain their original rights and applicable reuse conditions. This is an independent research portfolio project, not an official EU or OpenAI service.
