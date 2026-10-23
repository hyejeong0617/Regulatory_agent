# Project 003 — Regulatory Agent Architecture & Development Comparison

**Scientific AI Builder · October 2026 · Frozen research case**

Two complementary approaches investigate EU food-regulatory questions using the same ten-question case and five frozen EUR-Lex HTML snapshots.

| Track | Repository | Development approach | Main implementation |
| --- | --- | --- | --- |
| A — Architecture learning | [Regulatory_agent](https://github.com/hyejeong0617/Regulatory_agent) | Human-guided, AI-assisted experiments progressing through four builds | Notebooks: prompt-only → static dense/BM25 RAG → tools → multi-step investigation |
| B — Independent Codex build | [regulatory-investigation-agent](https://github.com/hyejeong0617/regulatory-investigation-agent) | Codex-designed and implemented under human-set goals, source corpus, budget and evaluation rules; no access to Track A answers/implementation during its independent build | Python package/CLI: legal record parser → BM25 → search/lookup/neighbors/linked → model-directed investigation → citation checks → same-model review |

## Evaluation definitions and scope

All scores concern **one case**: Türkiye-origin dried figs with aflatoxin B1 detection and unspecified material shipment facts. The five law documents are dated snapshots; this is not a current-law compliance benchmark.

- **Correct**: material regulatory conclusions match the verified reference and do not introduce material legal errors.
- **Grounded**: material conclusions are supported by relevant, traceable source provisions.
- **Complete**: the answer covers the key issues required by the reference, including relevant conditions and missing evidence.

Ratings use **Yes / Partial / No**. The table counts **Yes only**; partial ratings do not contribute to the numerator.

| Implementation | Correct Yes | Grounded Yes | Complete Yes | Assessment status |
| --- | ---: | ---: | ---: | --- |
| 01 — Prompt-only | 5/10 | 0/10 | 2/10 | Owner-reviewed against frozen verified reference |
| 02 — Static hybrid RAG | 5/10 | 9/10 | 2/10 | Owner-reviewed against frozen verified reference |
| 03-B — Tools | 9/10 | 6/10 | 4/10 | Owner-reviewed against frozen verified reference |
| 04 v3 — Investigation | 8/10 | 10/10 | 3/10 | Owner-reviewed against frozen verified reference |
| **Codex-built v1** | **5/10** | **8/10** | **2/10** | **Human-confirmed 2026-10-23** |

## Evaluation provenance and detailed reports

**Track A — Human-guided Builds 01–04:** Owner-reviewed against the frozen Verified Reference. The [Track A evaluation](EVALUATION.md) describes each architecture's outcomes, trade-offs and supporting records. Public worksheet templates do not expose every final individual human grading judgment.

**Track B — Codex-built v1:** A separate AI-assisted question-level review on **2026-10-22** produced the provisional **5/10 Correct, 8/10 Grounded, 2/10 Complete** Yes-only counts. The owner **confirmed all Q1–Q10 judgments individually on 2026-10-23** against the original run records and frozen Gold Standard; none of the provisional ratings changed. See the [dedicated Track B quality evaluation](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/QUALITY_EVALUATION.md) .

**Execution caveats:** Codex Q5 was retained from a pre-freeze development smoke test with matching v1 settings, not rerun as a held-out post-freeze test. Codex Q9 was incomplete and counted No in the preliminary quality review. The agent's `partial` and `incomplete` workflow statuses are **not** Correct/Grounded/Complete judgments. See the [Track B execution report](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/evaluation/v1/EVALUATION_REPORT.md).

## What the comparison does and does not show

- Track A illustrates the trade-offs of progressively adding retrieval, tools, and planning/verification. Improved evidence grounding did not consistently increase correct or complete answers.
- Track B illustrates how an AI coding agent can implement a testable, auditable agent from requirements without inheriting Track A's code or responses. Its citation checking rejects exact-quote mismatches but cannot guarantee correct legal entailment.
- Both systems can miss conditions buried in complex Annex tables, external referenced acts, and date-specific law. The Codex v1 Q9 interruption is an observed execution limitation.
- Different retrieval, prompts, development sequences and execution budgets mean the tracks are **not** identical-condition controlled trials. Ten interrelated questions on one case do not measure general regulatory accuracy.
- Human review of Track B's initial AI-assisted grading was completed on 2026-10-23; the numerical Codex scores above reflect the documented provisional AI-assisted review dated 2026-10-22. Future held-out evaluations should use new cases not exposed during development.

## Evidence and source links

- [Track A notebooks and frozen evaluation](https://github.com/hyejeong0617/Regulatory_agent)
- [Track A Build 1–4 quality evaluation](EVALUATION.md)
- [Track A offline validation](VALIDATION.md)
- [Track B independent implementation](https://github.com/hyejeong0617/regulatory-investigation-agent)
- [Track B evaluation protocol](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/evaluation_protocol.md)
- [Track B dedicated quality evaluation (human-confirmed)](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/QUALITY_EVALUATION.md)
- [Track B retained v1 execution results](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/evaluation/v1/EVALUATION_REPORT.md)

**Research status:** Both implementations and their original outputs are frozen. This document is a provenance-aware portfolio comparison, not a legal advice service.
