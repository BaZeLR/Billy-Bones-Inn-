from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/NPC/Girls/Melissa/MelissaEvents.rpy"


def test_attic_window_story_decision_is_a_native_menu():
    source = SOURCE.read_text(encoding="utf-8-sig")
    block = source.split("label story_melissa_bat_problem_3:", 1)[1].split(
        "label story_melissa_bat_problem_fall:", 1
    )[0]

    assert "\n    menu:\n" in block
    assert '"Податься ближе":' in block
    assert '"Отступить от окна":' in block
    assert "call story_melissa_bat_problem_fall" in block
    assert "QueuePagedPanelText" not in block
    assert "MenuItem(" not in block
    assert "jump TavernAtic" not in block
    assert "main_ui_runtime.action_items" not in block
