"""Offline integrity checks for bundled, historical evaluation explorer data.

Use: python evaluation_explorer/test_data.py
No network access or external dependencies required.
"""
from pathlib import Path
import json
import ast

ROOT = Path(__file__).resolve().parent
app_text = (ROOT / "app.py").read_text(encoding="utf-8")
ast.parse(app_text)
expected = {"Build 01", "Build 02", "Build 03-B", "Build 04 v3", "Codex-built v1"}
for i in range(1, 11):
    qid = f"Q{i}"
    d = json.loads((ROOT / "data" / f"{qid}.json").read_text(encoding="utf-8"))
    assert d["qid"] == qid and isinstance(d["question"], str) and d["question"], qid
    assert set(d["builds"]) == expected, (qid, sorted(d["builds"]))
    for name, record in d["builds"].items():
        assert isinstance(record["answer"], str) and record["answer"].strip(), (qid, name)
        assert isinstance(record["url"], str) and record["url"].startswith("https://github.com/"), (qid, name)
        assert isinstance(record["evidence"], list), (qid, name)
        assert isinstance(record["metrics"], dict), (qid, name)
    if qid == "Q9":
        assert d["builds"]["Codex-built v1"]["status"] == "incomplete"
assert "requests.get" not in app_text, "The explorer should not fetch data at runtime."
assert "OPENAI_API_KEY" not in app_text and "st.secrets" not in app_text
print("PASS: 10 questions, 50 saved answers, source links, Q9 status, offline loading design, syntax.")
