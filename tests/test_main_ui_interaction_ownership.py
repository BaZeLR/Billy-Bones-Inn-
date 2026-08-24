from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_main_ui_room_calls_have_stable_interaction_owners():
    violations = []
    for path in (ROOT / "game").rglob("*.rpy"):
        source = path.read_text(encoding="utf-8-sig")
        lines = source.splitlines()
        for index, line in enumerate(lines):
            if "call screen main_ui" not in line or " as " in line:
                continue
            previous = lines[index - 1].strip() if index else ""
            if previous.startswith("while "):
                continue
            violations.append(f"{path.relative_to(ROOT)}:{index + 1}")

    assert violations == []


def test_main_ui_room_flow_has_no_call_then_return_or_self_jump():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert not re.search(
        r"(?m)^(?P<indent>[ \t]*)call screen main_ui[ \t]*\n(?P=indent)(?:return|jump\s+\w+)",
        runtime,
    )
