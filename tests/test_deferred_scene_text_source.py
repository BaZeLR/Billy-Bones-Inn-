import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"

DEFERRED_LOCAL_SUBSTITUTION = re.compile(
    r"(?:scene_runtime\.(?:text|location_text)|MainTxt|textLocRef)\s*=\s*"
    r"(?:\"[^\"\n]*(?:\[_|\[\(_)|'[^'\n]*(?:\[_|\[\(_))"
)


def test_deferred_scene_text_does_not_reference_label_locals():
    violations = []
    for path in GAME.rglob("*.rpy"):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), start=1
        ):
            if DEFERRED_LOCAL_SUBSTITUTION.search(line):
                violations.append(f"{path.relative_to(ROOT)}:{line_number}")

    assert not violations, (
        "Resolve label-local values before storing text for later screen rendering: "
        + ", ".join(violations)
    )
