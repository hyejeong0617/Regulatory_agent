# AI Architecture Evaluation Explorer

A read-only Streamlit companion to Project 003, showing original saved Q1–Q10 results from five implementations.

## Features

- Choose one of ten related benchmark questions and compare up to five answer records.
- Four Track A builds: prompt-only, hybrid RAG, tool-supported search, full investigation v3.
- One Track B implementation: independently Codex-built v1.
- Display the original recorded answer, retrieved source snippets (when available), execution status and metadata.
- Show frozen owner-reviewed **aggregate** Yes-only Correct/Grounded/Complete scores across all ten questions.
- Display published **question-level** grades for Track B only; no reconstructed or invented Track A question-level scores.
- Identify the Codex Q9 run as **incomplete**, not a legal-reasoning error.
- Surface historical research limitations, sources and failure cases.

All files are read from **public, revision-pinned** GitHub raw endpoints. No credentials, new inference or paid APIs are used. The app needs network access to GitHub. Saved sources are historical legal snapshots; the app is **not legal advice**.

## Local launch

From the root of this repository:

```bash
python -m venv .venv
# Activate .venv as appropriate to your shell
python -m pip install -r evaluation_explorer/requirements.txt
streamlit run evaluation_explorer/app.py
```

## Streamlit Community Cloud deployment

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
2. New app → Repository: `hyejeong0617/Regulatory_agent`, Branch: `main`, Main file path: `evaluation_explorer/app.py`.
3. Configure Python 3.11 or a supported version, then deploy. Requirements are in `evaluation_explorer/requirements.txt`.
4. Once deployment succeeds, test Q1 and Q9 across Track A and Track B, long answers, source expansions, and narrow/mobile layouts.
5. Only after the hosted app has been checked, add its actual URL to the main README and your portfolio website.

There is no public app URL until Streamlit hosting is deployed. A GitHub commit alone does not launch a Streamlit service.

## Architecture and provenance

- Track A frozen raw records are pinned to commit `db9803c2f0b8c39ccb6aa4dcd825eefd48c9c5ac`.
- Track B frozen raw records are pinned to commit `73d4ce039183ec8d395cf8b6cd02613b01a668e6`.
- In Track A, Build 01/02 use `results/build01_02/nb04b_context_repaired_openai_luna_generation_results.jsonl`; Build 03/04 use `results/build03/Q*.json` and `results/build04/Q*.json`.
- In Track B, each question uses its published `evaluation/v1/raw/Q*/question-Q*-<run-id>.json` file.
- Input questions are read from the original baseline generation results.
- Track B individual labels follow the published [quality evaluation](https://github.com/hyejeong0617/regulatory-investigation-agent/blob/main/docs/QUALITY_EVALUATION.md). Track A's individual owner-reviewed grades are not fully publicly reconstructable.

The app fetches the source records in the viewer's session and caches responses in memory for one hour. A temporary GitHub outage or network restriction may prevent loading records; the app fails visibly rather than substituting fabricated content. Public links to historical source versions are provided for inspection.

## Boundaries

- One case, ten interrelated and development-exposed questions: **not** ten independent cases.
- Frozen counts are Yes-only and have incomplete public grading provenance for Track A.
- Source snippets are retrieved evidence, not necessarily valid legal citations.
- Q5 in the Codex-built set is a retained development smoke run; Q9 is incomplete.
- Historical EUR-Lex snapshots are not a current-law service.
- No new model execution, live EUR-Lex checking or reranking/benchmarking occurs here.

## Testing

Static syntax check (no installation required):

```bash
python -m py_compile evaluation_explorer/app.py
```

Local app smoke test (after dependency installation):

```bash
streamlit run evaluation_explorer/app.py
```

Check Q1 and Q9 with both tracks. Full hosted interaction testing and any Streamlit Cloud deployment must be separately confirmed; they are not implied by the repository release.
