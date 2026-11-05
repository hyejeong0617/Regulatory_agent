# AI Architecture Evaluation Explorer

A read-only Streamlit companion to Project 003. Explore the original saved answers for all ten questions across four human-guided builds and an independently Codex-built implementation.

## What the app shows

- **Overview:** accessible light-theme score comparison, research context and caveats.
- **Compare original answers:** choose Q1–Q10, select implementations and read the archived answer text in a single column or optional two-column layout. Each card links to the original frozen GitHub record and shows available evidence and run metadata.
- **Evidence & limitations:** source provenance, scoring boundaries and research scope.
- **Codex Q9:** clearly marked **execution incomplete**, not a completed regulatory response.
- **Question-level quality grades:** shown only for Codex-built v1 because Track A final per-question judgments are not completely public. The summary uses owner-reviewed Yes-only aggregate counts.

All 50 original answer texts are bundled in `data/Q1.json`–`data/Q10.json`, sourced from frozen public GitHub records. Evidence lists are curated excerpts from saved retrieval outputs, **not** independent validation of legal claims. Each answer links to its untouched original artifact. The app reads local files only: **no GitHub requests at runtime, no model inference, no API keys, no paid operations**.

## Run locally

From the repository root:

```bash
python -m pip install -r evaluation_explorer/requirements.txt
streamlit run evaluation_explorer/app.py
```

The project sets a light theme in `.streamlit/config.toml`. For a quick, dependency-free syntax/data integrity check:

```bash
python -B evaluation_explorer/test_data.py
```

## Deploy with Streamlit Community Cloud

1. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and connect GitHub.
2. Select repository `hyejeong0617/Regulatory_agent`, branch `main`.
3. Set the main Python file to `evaluation_explorer/app.py`.
4. Streamlit will discover `evaluation_explorer/requirements.txt`; if prompted, point it there.
5. Redeploy/reboot if the hosted app is still using a cached older commit.
6. Verify Overview contrast, Q1 and Q9 selection, all five archived answers, evidence expanders, the single/two-column layout and mobile readability.

The hosted Streamlit URL is **not recorded or independently verified here**. A GitHub commit does not itself deploy the app.

## Source and scientific integrity

Frozen input revisions:

- Track A: `db9803c2f0b8c39ccb6aa4dcd825eefd48c9c5ac` in [Regulatory_agent](https://github.com/hyejeong0617/Regulatory_agent).
- Track B: `73d4ce039183ec8d395cf8b6cd02613b01a668e6` in [regulatory-investigation-agent](https://github.com/hyejeong0617/regulatory-investigation-agent).

All benchmark question wording and answer text is preserved. Bundling does not regrade, edit, rerun or improve the historical answers. The app is a retrospective presentation layer over one case and ten related questions, **not** an independent general performance benchmark, current-law service or legal advice.

The full reference and some Track A individual grade worksheets are private. Track B quality grades were initially AI-assisted and owner-confirmed on 2026-10-23, but not independently externally validated. Codex Q5 came from a retained development smoke run. Current EU legal applicability and live generation are out of scope.
