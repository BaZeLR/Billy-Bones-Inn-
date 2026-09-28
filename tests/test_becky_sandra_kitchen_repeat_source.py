from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_repeat_visit_is_entry_event_only_after_friendship_visits():
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    repeat = runtime.split('RThreadData(0, "becky", "SandraKitchenVisitRepeat"', 1)[1].split(
        'LThreadData(0, "becky", "Home"', 1
    )[0]
    assert "#threads['beckySandraKitchenVisit'].completed" in repeat
    assert "#int(current_game_day() or 0) > int(threads['beckySandraKitchenVisit'].day or 0)" in repeat
    assert "#str(people.location('becky') or '') == 'TavernKitchen'" in repeat
    assert "#str(people.location('sandra') or '') == 'TavernKitchen'" in repeat
    assert '"TavernKitchen", "enter", 20' in repeat
    assert "threaded=False" in repeat


def test_each_visit_shows_both_women_and_they_react_to_mc():
    kitchen = source("game/Inn/TavernKitchen.rpy")
    first_visits = kitchen.split("label story_becky_sandra_kitchen_visit:", 1)[1].split(
        "label story_becky_sandra_kitchen_visit_repeat:", 1
    )[0]
    repeat = kitchen.split("label story_becky_sandra_kitchen_visit_repeat:", 1)[1].split(
        "label BeckySandraTipsyKitchenTalk:", 1
    )[0]
    assert 'vscene "images/tavern/kitchen/becky_visit_0.png"' in first_visits
    assert "Сандра замечает вас у двери" in first_visits
    assert 'vscene "images/tavern/kitchen/becky_visit_0.png"' in repeat
    assert 'vscene "images/tavern/kitchen/becky_visit_1.png"' in repeat
    assert "Сандра" in repeat and "Бекки" in repeat
    assert "Подсесть к подругам" in repeat
    assert (ROOT / "game/images/tavern/kitchen/becky_visit_0.png").is_file()
    assert (ROOT / "game/images/tavern/kitchen/becky_visit_1.png").is_file()
