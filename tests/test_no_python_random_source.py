from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_live_rpy_uses_project_procedural_random_engine():
    violations = []
    for path in (ROOT / "game").rglob("*.rpy"):
        source = path.read_text(encoding="utf-8-sig")
        if "import random" in source or "random." in source:
            violations.append(str(path.relative_to(ROOT)))

    assert violations == []
