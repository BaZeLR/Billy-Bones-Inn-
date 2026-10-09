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


def test_main_ui_npc_grid_cells_fit_the_sidebar():
    source = (ROOT / "game/Utilities/General/Screens/main_layout.rpy").read_text(
        encoding="utf-8-sig"
    )
    grid = source.split("grid 3 3:", 1)[1].split("if _room_actions_visible and str(main_ui_runtime.overlay", 1)[0]

    assert "_npc_cell_width = max(1, (int((config.screen_width - 36) * 0.28) - 32) // 3)" in source
    assert grid.count("xsize _npc_cell_width") == 4
    assert "xminimum 150" not in grid
    for width in (800, 1280, 1728, 1920):
        panel_width = int((width - 36) * 0.28)
        cell_width = max(1, (panel_width - 32) // 3)
        assert 3 * cell_width + 12 <= panel_width - 20
