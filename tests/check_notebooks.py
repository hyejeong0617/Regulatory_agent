"""Static checks, root discovery and frozen bytes; no third-party dependencies."""
import ast
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def check_integrity():
    manifest = json.loads((ROOT / "tests/frozen_artifacts.json").read_text())
    for name, digest in manifest["sha256"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    print(f"PASS: {len(manifest['sha256'])} frozen artifact SHA-256 hashes")


def main():
    check_integrity()
    notebooks = sorted((ROOT / "notebooks").rglob("*.ipynb")) + sorted((ROOT / "experiments").rglob("*.ipynb"))
    cells = 0
    magics = 0
    old_cwd = Path.cwd()
    old_root = os.environ.pop("REGULATORY_AGENT_ROOT", None)
    try:
        for path in notebooks:
            doc = json.loads(path.read_text(encoding="utf-8"))
            first = True
            for i, cell in enumerate(doc["cells"]):
                if cell["cell_type"] != "code":
                    continue
                source = "".join(cell["source"])
                # Compile every Python statement, excluding only IPython command lines.
                lines = source.splitlines(keepends=True)
                for j, line in enumerate(lines):
                    if line.lstrip().startswith("%pip "):
                        lines[j] = line[:len(line) - len(line.lstrip())] + "pass\n"
                        magics += 1
                source = "".join(lines)
                compile(source, f"{path}:{i}", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
                cells += 1
                if first:
                    bootstrap = source.split("_repo_os.chdir(REPO_ROOT)", 1)[0] + "_repo_os.chdir(REPO_ROOT)"
                    for start in (ROOT, path.parent):
                        os.chdir(start)
                        exec(bootstrap, {})
                        assert Path.cwd() == ROOT
                    with tempfile.TemporaryDirectory() as external:
                        os.chdir(external)
                        os.environ["REGULATORY_AGENT_ROOT"] = str(ROOT)
                        exec(bootstrap, {})
                        assert Path.cwd() == ROOT
                        del os.environ["REGULATORY_AGENT_ROOT"]
                    first = False
                for node in ast.walk(ast.parse(source)):
                    if isinstance(node, ast.Call) and isinstance(node.func, (ast.Name, ast.Attribute)):
                        name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr
                        if name == "Path" and node.args and isinstance(node.args[0], ast.Constant):
                            value = node.args[0].value
                            if isinstance(value, str) and value.startswith(("data/", "results/", "experiments/")):
                                target = ROOT / value
                                assert target.exists() or target.parent.is_dir(), (path, value)
        print(f"PASS: {len(notebooks)} notebooks, {cells} compiled cells; root/nested/external CWDs and path parents")
        print(f"NOT TESTED: {magics} IPython command lines (package installation magics)")
    finally:
        os.chdir(old_cwd)
        if old_root is not None:
            os.environ["REGULATORY_AGENT_ROOT"] = old_root


if __name__ == "__main__":
    main()
