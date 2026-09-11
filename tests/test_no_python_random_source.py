from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_live_rpy_uses_project_procedural_random_engine():
    violations = []
    for path in (ROOT / "game").rglob("*.rpy"):
        source = path.read_text(encoding="utf-8-sig")
        if "import random" in source or "random." in source:
            violations.append(str(path.relative_to(ROOT)))

    assert violations == []


def test_procedural_random_mixes_seed_before_probability_projection():
    source = (ROOT / "game" / "script.rpy").read_text(encoding="utf-8-sig")
    body = source.split("    def procedural_random", 1)[1].split("\n    def ", 1)[0]

    assert "procedural_index(1000000, key)" not in body
    assert "procedural_seed(key)" in body
    assert "value ^= value >> 16" in body
    assert "4294967296.0" in body
