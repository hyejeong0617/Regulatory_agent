# Offline refactor validation — 2026-10-23

This validates the repository reorganization and selected real notebook cells.
It does not rerun Q1–Q10 generation, regrade answers, or establish current law.

## Results

| Check | Status | Evidence / boundary |
| --- | --- | --- |
| Required layout and canonical input paths | PASS | Five HTML sources and 13 essential paths |
| Notebook JSON / Python syntax | PASS | All 16 active/experimental notebooks; 223 code cells; only two `%pip` installation lines excluded |
| Root discovery | PASS | Every notebook tested from root, own directory and external CWD with explicit environment override |
| NB01 HTML parsing | PASS | All five complete parsed document records equal frozen JSON; output only in temporary directory |
| NB02 chunking | PASS | Naive and legal-aware JSON equal frozen artifacts; 1,383 legal chunks, including Annex II logical row 14 |
| NB03 retrieval | PASS | BM25 initialization; cached dense/BM25/RRF returns the same 50 ordered chunk IDs as saved retrieval |
| NB04b data / config | PASS | Ten questions, 50 retrieval rows, configuration assertions and prompt builders initialize |
| NB08 | PASS | Real retrieval parity 50/50, two SDK tools and Agent initialize, existing mocked Cellar tests pass |
| NB09 v3 | PASS | Real retrieval parity 50/50; graph compiles; original deterministic evidence, citation, coverage, queue, stop and fallback report tests pass |
| Build03 / Build04 saved records | PASS | Q1–Q10 loaded for each build; QIDs checked |
| Lean / both Adaptive v4 notebooks | PASS | Local preview, input loading and comparison against saved v3/pilot records |
| Frozen integrity | PASS | 94 SHA-256 hashes before/after; original main's 94 Git blobs preserved; existing notebook cell outputs/execution counts unchanged |
| Python 3.11 clean GitHub Actions runtime | PASS | [Successful run](https://github.com/hyejeong0617/Regulatory_agent/actions/runs/39931930020): dependency installation, pip check, runtime suite and tracked-file preservation |
| Paid LLM generation / complete benchmark rerun | NOT TESTED | Deliberately excluded; no API key used |
| Live law/version services | NOT TESTED | Network denied during smoke execution; mocked parsing does not certify live currentness |
| Complete notebooks / archived notebooks | NOT TESTED | Only allowlisted cells executed; archive and historical export workflows are not certified |

No unresolved local smoke-test failures remain. Initial sandbox temporary-directory
permissions and a test harness's handling of diagnostic `%pip` commands were
resolved without changing research computations. Linux directory-relative temporary-file cleanup was also tested and corrected in the harness; the subsequent complete CI run passed. The HTML parser emitted its
existing XML-as-HTML warning; its complete output nevertheless equals the frozen
artifact. The pre-existing local Anaconda environment also warned about optional
`numexpr`; the core tests passed. Prefer the clean environment below.

## Environment and exact commands

Python **3.11** is recommended and used by CI. Local full dense verification used
Windows Python **3.13.5** with the existing model cache. `requirements.txt` specifies
direct imports with compatible API-family bounds; it is **not** a reconstruction
of the unavailable original research environment or a fully transitive lockfile.
CI uploads its resolved `pip freeze` as `python311-validation-dependencies`.

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
python tests/check_layout.py
python tests/check_notebooks.py
python tests/offline_smoke.py
```

The first two tests require only Python's standard library. The smoke runner needs
the notebook imports, but its default mode does not construct a dense model.
It tests BM25 and deterministic workflow components; it explicitly reports dense
parity as NOT TESTED in that mode. It does not substitute fake embeddings or
claim that tool registration alone validates real retrieval.

For full dense parity, prepare the original model once with internet access:

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"
python tests/offline_smoke.py --dense
```

The separate cache-preparation command downloads a free embedding model, not a
paid LLM. Local verification used cache revision
`e8f8c211226b894fcb81acc59f3b34ba3efd5f42`. Notebook code still uses its original
model identifier; future upstream model revisions or dependency changes may
change rankings. `--dense` requires local availability and asserts parity against
the original ordered chunk IDs. It fails rather than download or rewrite baselines.

Local direct dependency versions: beautifulsoup4 4.12.3, lxml 5.3.0,
numpy 2.5.4, pandas 3.0.6, rank-bm25 0.2.2, sentence-transformers 6.1.0,
requests 2.32.5, openai 3.35.1, openai-agents 0.24.0, pydantic 2.14.1,
langgraph 1.2.16 and IPython 8.30.0; torch 2.9.1 and transformers 5.19.0.
Python 3.11 resolves a compatible NumPy version rather than the local 3.13 build.

For Jupyter only: `python -m pip install -r requirements-notebooks.txt`, then
`jupyter lab`. Run the first code cell before selecting later cells. The bootstrap
sets CWD to the repository root; set `REGULATORY_AGENT_ROOT` for external kernels.

## Safety and interpretation

The smoke runner executes an explicit allowlist of actual cells, blocks network
connections/subprocesses during execution and blocks writes/deletion within the
checkout. Only export-path assignments for NB01/NB02 and retrieval parity audits
are redirected to a temporary directory; algorithms and constants are unchanged.
Full JSON equality is checked for parsing/chunking; dense retrieval is checked by
ordered chunk IDs, not bitwise floating-point score equality. Hash checks always
run again, including when a smoke assertion fails.

Paid and live-probe flags default to False, including NB09's later override cell.
This is not a blanket write-protection mechanism for interactive notebooks:
historical export/config/summary cells can overwrite saved paths even with paid
calls disabled. Use this harness for inspection; choose fresh paths before any
deliberate new experiment. Frozen config files retain historical provenance paths
(for example old chunk-source locations); the active loaders use explicit migrated
paths and do not dereference those provenance strings. Those JSON files were not edited.

No original HTML, question, saved answer, evaluation judgment or historical record
was modified. No model prompt, retrieval algorithm, threshold or agent workflow
was changed. The separate Codex-built project was not changed. The existing PR
remains open; no merge is performed by this validation.

The integrity manifest records original Git-blob SHA-256 hashes and their exact
LF-to-CRLF checkout equivalents for Windows `core.autocrlf`. No files are normalized
or rewritten by the check. This avoids treating Git's checkout line-ending expansion
as research-data corruption while still rejecting any content changes.

## Merge recommendation

**READY TO MERGE** for the repository refactor, subject to final human review.
Local dense parity and clean Python 3.11 offline CI pass; no remaining refactor
blockers are known. This recommendation does not certify paid model reruns,
live law checks, archive execution, or unrestricted notebook Run All.
