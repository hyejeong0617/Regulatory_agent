"""Execute an explicit allowlist of real notebook cells, never the paid-run cells.

Network connections and writes inside the checkout are denied by a Python audit
hook. Outputs from parsing/chunking/parity cells are redirected to a temporary
directory by replacing only their output-path assignment, not their algorithms.
Use --dense only when the original embedding model is already cached locally.
"""
import argparse
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile

from check_notebooks import ROOT, check_integrity

sys.dont_write_bytecode = True
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1")


def guard(event, args):
    if event in {"socket.connect", "socket.getaddrinfo", "subprocess.Popen", "os.system"}:
        raise RuntimeError(f"Offline smoke blocked {event}")
    if event == "open":
        path, mode, flags = args
        writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writing and isinstance(path, (str, bytes, os.PathLike)):
            if Path(os.fsdecode(path)).resolve().is_relative_to(ROOT):
                raise RuntimeError(f"Frozen checkout write blocked: {path}")
    if event in {"os.remove", "os.rename", "os.rmdir"}:
        for path in args[:2] if event == "os.rename" else args[:1]:
            if isinstance(path, (str, bytes, os.PathLike)) and Path(os.fsdecode(path)).resolve().is_relative_to(ROOT):
                raise RuntimeError(f"Frozen checkout mutation blocked: {event}")


def notebook(pattern):
    return next(ROOT.rglob(pattern))


def run(path, indices, scope=None, outputs=None):
    scope = scope if scope is not None else {"__name__": "offline_notebook", "display": lambda *a, **k: None}
    cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
    for index in indices:
        tree = ast.parse("".join(cells[index]["source"]))
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
                if outputs and name in outputs:
                    node.value = ast.Call(func=ast.Name(id="Path", ctx=ast.Load()), args=[ast.Constant(str(outputs[name]))], keywords=[])
        ast.fix_missing_locations(tree)
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(tree, f"{path.name}:cell {index}", "exec"), scope)
    return scope


def same_json(generated, frozen):
    assert json.loads(generated.read_text(encoding="utf-8")) == json.loads((ROOT / frozen).read_text(encoding="utf-8")), frozen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dense", action="store_true", help="Require cached original model; recompute retrieval, no downloads")
    options = parser.parse_args()
    # Import packages before restricting subprocesses used for library/platform discovery.
    import pandas as pd
    import numpy
    import bs4
    import lxml
    import requests
    import rank_bm25
    import agents
    import langgraph.graph
    import openai
    import pydantic
    import sentence_transformers
    from IPython.display import display

    check_integrity()
    sys.addaudithook(guard)
    os.chdir(ROOT)
    try:
        with tempfile.TemporaryDirectory(prefix="regulatory-offline-") as folder:
            temp = Path(folder)
            parsed, naive, legal = [temp / name for name in ("parsed.json", "naive.json", "legal.json")]
            run(notebook("NB01_regulation_library.ipynb"), [2, 4, 7, 9, 30], outputs={"OUT_JSON": parsed})
            same_json(parsed, "data/processed/parsed_regulation_library.json")
            print("PASS: NB01 parses all five HTML snapshots; complete JSON equals frozen library")
            run(notebook("NB02_chunking_v2_rowgroup_fix.ipynb"), [2, 4, 6, 8, 10, 12, 14, 36], outputs={"NAIVE_OUT": naive, "LEGAL_OUT": legal})
            same_json(naive, "data/processed/chunks_naive.json")
            same_json(legal, "data/processed/chunks_legal_aware.json")
            chunks = json.loads(legal.read_text(encoding="utf-8"))
            grouped = [c for c in chunks if "annexII_row14_turkiye_figs" in c["chunk_id"]]
            assert len(chunks) == 1383 and len(grouped) == 1
            print("PASS: NB02 naive/legal chunks equal frozen JSON, including Annex row group (1,383 legal chunks)")
            run(notebook("NB04b_context_repaired_full_rerun_OpenAI_GPT6_Luna_v2.ipynb"), [2, 3, 5, 7, 9, 10, 11, 12, 13])
            print("PASS: NB04b benchmark/config/50 retrieval rows and prompt builders initialize")

            nb03 = notebook("NB03_final_hybrid_static_RAG.ipynb")
            n3 = run(nb03, [1, 2, 6])
            if options.dense:
                run(nb03, [8, 10, 12, 14, 16], n3)
                baseline = pd.read_csv(ROOT / "data/processed/retrieval_results_nb03_final_hybrid_static_rag.csv")
                assert n3["retrieval_df"][["qid", "rank", "chunk_id"]].to_dict("records") == baseline[["qid", "rank", "chunk_id"]].to_dict("records")
                print("PASS: NB03 cached dense + BM25/RRF retrieval reproduces 50/50 ordered chunk IDs")
            else:
                n3["query_ids"] = list(n3["questions"])
                run(nb03, [10], n3)
                print("PASS: NB03 frozen corpus and BM25 initialize")
                print("NOT TESTED: dense retrieval/parity (use --dense with cached original model)")

            for pattern, law, cellar, parity in [("NB08_build03B_Q1_Q10_gap_analysis.ipynb", 12, 13, 10), ("NB09_v3.ipynb", 11, 12, 9)]:
                path = notebook(pattern)
                scope = run(path, [2, 3, 5])
                if options.dense:
                    run(path, [7, 8, parity], scope, {"PARITY_PATH": temp / f"{path.stem}-parity.csv"})
                    assert scope["matched"] == 50
                    print(f"PASS: {path.stem} real retrieval parity 50/50")
                run(path, [law, cellar], scope)
                if pattern.startswith("NB08"):
                    run(path, [15, 19], scope)
                    assert len(scope["agent_B"].tools) == 2
                    print("PASS: NB08 tool registration, Agent initialization and mocked Cellar parser tests")
                else:
                    run(path, [14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36], scope)
                    assert scope["CLIENT"] is None and not scope["RUN_OFFICIAL"]
                    print("PASS: NB09 graph compilation and existing evidence/coverage/reporting tests; no LLM client")

            for path in sorted((ROOT / "experiments/build04_v4_pilots").glob("*.ipynb")):
                scope = run(path, [1, 3, 5, 9])
                assert not scope["RUN_PAID"]
                assert len(scope["rows"]) > 0
                print(f"PASS: {path.stem} local preview and cross-build saved-result comparison")

            for build in ("build03", "build04"):
                for i in range(1, 11):
                    record = json.loads((ROOT / "results" / build / f"Q{i}.json").read_text(encoding="utf-8"))
                    assert record["qid"] == f"Q{i}"
                print(f"PASS: {build} Q1–Q10 saved records loaded")
    finally:
        check_integrity()
    print("NOT TESTED: paid model generation, full notebook Run All, live law services; intentionally excluded")


if __name__ == "__main__":
    main()
