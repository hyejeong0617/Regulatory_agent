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

| Track A build | Correct Yes | Grounded Yes | Complete Yes | Assessment status |
| --- | ---: | ---: | ---: | --- |
| 01 — Prompt-only | 5/10 | 0/10 | 2/10 | Owner-reviewed against frozen verified reference |
| 02 — Static hybrid RAG | 5/10 | 9/10 | 2/10 | Owner-reviewed against frozen verified reference |
| 03-B — Tools | 9/10 | 6/10 | 4/10 | Owner-reviewed against frozen verified reference |
| 04 v3 — Investigation | 8/10 | 10/10 | 3/10 | Owner-reviewed against frozen verified reference |

These published Track A aggregate numbers are preserved from [its existing evaluation record](../EVALUATION.md). Detailed reviewer judgments/reference are not fully represented in the public repository's worksheet templates, so the aggregate ratings cannot be independently reconstructed from the public files alone.

### Track B evaluation status — provisional, not a finalized Gold Standard score

The Codex repository publishes the Q1–Q10 source questions, outputs, event logs, and [execution report](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/evaluation/v1/EVALUATION_REPORT.md). That report describes **nine** selected `partial` assessments and **one** `incomplete` run (Q9). These are **execution/coverage statuses, not correctness scores**.

A separate AI-assisted comparison has been discussed, but its original per-question scoring record has **not been verified from these public repositories** and has **not been human-verified**. Consequently no numerical Codex Correct/Grounded/Complete claim is placed in the main scored table. When a verifiable grading artifact is available, record its provenance and version and label it **AI-reviewed (provisional)** until owner review is complete.

**Q5 provenance:** the selected Q5 result was a pre-freeze development smoke test using the subsequently frozen v1 code, matching model/reasoning, corpus and runtime limits, with no prior answer supplied. It was retained rather than rerun. The other nine questions were attempted independently post-freeze. Q5 is comparable as a selected v1 run but is **not** a held-out post-freeze test. Do not describe these as ten independently held-out evaluations.

## What the comparison does and does not show

- Track A illustrates the trade-offs of progressively adding retrieval, tools, and planning/verification. Improved evidence grounding did not consistently increase correct or complete answers.
- Track B illustrates how an AI coding agent can implement a testable, auditable agent from requirements without inheriting Track A's code or responses. Its citation checking rejects exact-quote mismatches but cannot guarantee correct legal entailment.
- Both systems can miss conditions buried in complex Annex tables, external referenced acts, and date-specific law. The Codex v1 Q9 interruption is an observed execution limitation.
- Different retrieval, prompts, development sequences and execution budgets mean the tracks are **not** identical-condition controlled trials. Ten interrelated questions on one case do not measure general regulatory accuracy.
- Human review of Track B's provisional grading remains outstanding. Future held-out evaluations should use new cases not exposed during development.

## Evidence and source links

- [Track A notebooks and frozen evaluation](https://github.com/hyejeong0617/Regulatory_agent)
- [Track A evaluation summary](EVALUATION.md)
- [Track A offline validation](VALIDATION.md)
- [Track B independent implementation](https://github.com/hyejeong0617/regulatory-investigation-agent)
- [Track B evaluation protocol](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/evaluation_protocol.md)
- [Track B retained v1 execution results](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/evaluation/v1/EVALUATION_REPORT.md)

**Research status:** Both implementations and their original outputs are frozen. This document is a provenance-aware portfolio comparison, not a legal advice service.
