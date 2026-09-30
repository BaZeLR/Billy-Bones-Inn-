from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_breakfast_tease_is_dispatched_as_an_event_not_a_menu_action():
    breakfast = (ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
    events = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")

    assert '"TavernKitchenBreakfastTease", None, (6, 11)' in events
    assert 'None, "TavernKitchen", "breakfast_tease", 100)' in events
    assert 'call checkTriggers("TavernKitchen", "breakfast_tease", 0)' in breakfast
    assert '"Заметить провокацию за столом"' not in breakfast
    assert '"Ответить на её поддразнивание"' not in breakfast
