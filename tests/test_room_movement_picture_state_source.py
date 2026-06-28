from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (PROJECT_ROOT / path).read_text(encoding="utf-8-sig")


def test_advance_movement_time_clears_selected_object_and_npc_before_jump():
    source = read_rel("game/Utilities/Time/TimeTurnSystem.rpy")
    label = source.split('label AdvanceMovementTime(target_label=""):', 1)[1].split("if renpy.has_label(movement_target):", 1)[0]

    assert '$ current_object_id = ""' in label
    assert '$ current_girl_key = ""' in label
