# Track A — Human-guided Builds 01–04: Quality Evaluation

**Scientific AI Builder · Project 003 · Owner-reviewed (historical evaluation)**

This document records the existing Build 01–04 evaluation results and their interpretation. It is the **Track A** companion to the [five-implementation Project 003 comparison](PROJECT003_COMPARISON.md). The independently [Codex-built v1 quality evaluation](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/QUALITY_EVALUATION.md) belongs to Track B.

## Case, reference and scoring

All four builds were applied to the same ten related questions (Q1–Q10) about **Türkiye-origin dried figs with aflatoxin B1 detected**, with concentration and shipment stage unspecified. Five frozen EUR-Lex snapshots support source-based analysis; the corpus is not verified current law. The project owner reviewed the original comparison against a separately maintained frozen reference. The detailed reference is not published with this repository.

The three dimensions were **Correct** (materially accurate conclusions), **Grounded** (relevant, traceable source support) and **Complete** (coverage of key legal issues, conditions and unknowns). Each was rated **Yes / Partial / No**. Values below count **Yes only**; Partial is not counted as half a point.

| Build | Correct Yes | Grounded Yes | Complete Yes | Evaluation status |
| --- | ---: | ---: | ---: | --- |
| 01 — Prompt-only | 5/10 | 0/10 | 2/10 | Owner-reviewed |
| 02 — Static hybrid RAG | 5/10 | 9/10 | 2/10 | Owner-reviewed |
| 03-B — Tools | 9/10 | 6/10 | 4/10 | Owner-reviewed |
| 04 v3 — Investigation | 8/10 | 10/10 | 3/10 | Owner-reviewed |

The same figures appeared in the pre-existing Track A evaluation summary; no results were regraded for this documentation revision. Public manual-evaluation worksheets include unfilled or REVIEW fields, and the full reference-based judgment trail remains outside this GitHub repository; these aggregate figures therefore cannot be independently reconstructed from those worksheets alone.

## Build-by-build interpretation

### Build 01 — Prompt-only

A baseline without supplied retrieved legal evidence. It established the starting point for measuring the effect of later retrieval and tool use. **Correct 5/10; Grounded 0/10; Complete 2/10.** The recorded limitation includes incorrect generalization about dried-fig sorting/processing conditions. The absence of traceable retrieval evidence is central to the low Grounded result.

### Build 02 — Static hybrid RAG

Added legally oriented chunks and a fixed **dense + BM25 + reciprocal rank fusion (Top-5)** evidence retrieval stage before answer generation. **Correct 5/10; Grounded 9/10; Complete 2/10.** The evidence traceability improved, but fixed retrieval could omit operative or connected provisions, and the additional citations did not translate into higher Correct or Complete Yes counts.

### Build 03-B — Tools

Added targeted retrieval and tool access beyond fixed Top-5. **Correct 9/10; Grounded 6/10; Complete 4/10.** This is the highest Correct and Complete count among these four builds, although not the highest Grounded count. Availability of further tool calls alone did not ensure every final claim was comparably source-traceable.

### Build 04 v3 — Full Investigation

Added explicit investigation, targeted evidence gathering, validation, coverage checks and possible re-search. **Correct 8/10; Grounded 10/10; Complete 3/10.** This build attained the highest Grounded count, but neither Correct nor Complete improved over Build 03-B. Greater investigation complexity incurred substantially more resource use without establishing a monotonic performance improvement.

The frozen Build04 v3 run recorded **527,148 tokens, 69 LLM calls, 64 searches, and 2,232.93 seconds** across Q1–Q10. These are *reported runtime metrics*, not comparable normalized efficiency measurements across different builds.

## Key findings and limits

- **Grounding and correctness are different:** Build 02 improved Grounded while Correct remained unchanged; Build 04 improved Grounded relative to Build 03-B while Correct and Complete declined slightly.
- **Fixed retrieval and complex Annex tables matter:** Answering a multi-provision regulatory question may depend on adjacent rows, exceptions and procedural provisions not included among initial hits.
- **More agent steps are not automatically better:** Tool invocation, checking and repeated retrieval can improve evidence access without guaranteeing that all required requirements are synthesized into the final answer.
- **One benchmark case:** Ten related questions on one frozen case cannot be interpreted as ten independent food-regulatory scenarios, market accuracy or real-world compliance reliability.
- **Provenance:** The human-guided experiments used AI coding assistance. The owner-led architectural sequence is distinct from Track B's independent Codex-led implementation.

## Reproducible artifacts and related documents

- [Canonical notebooks](../README.md#canonical-notebooks) for the implemented Build 01–04 workflow.
- [Frozen Build 1–2 outputs](../results/build01_02/), [Build 3 outputs](../results/build03/), [Build 4 outputs](../results/build04/).
- [Offline validation and boundaries](VALIDATION.md).
- [Project 003 — All five implementations](PROJECT003_COMPARISON.md).
- [Track B — Codex quality assessment (AI-reviewed, provisional)](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/QUALITY_EVALUATION.md).

Build04's experimental Lean/Adaptive v4 Q5/Q9/Q10 pilots are **not** substitutes for the frozen Build04 v3 score. The completed v1 results are preserved; none were modified by this documentation update.
