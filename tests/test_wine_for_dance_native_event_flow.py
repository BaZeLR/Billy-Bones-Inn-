from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT / "game" / "Inn" / "EventWineForDance.rpy"
BREAKFAST = ROOT / "game" / "Inn" / "TavernKitchenBreakfast.rpy"
KITCHEN = ROOT / "game" / "Inn" / "TavernKitchen.rpy"


def _label_block(source, label_name, next_label):
    return source.split(f"label {label_name}", 1)[1].split(f"label {next_label}", 1)[0]


def test_wine_for_dance_uses_native_menus_and_canonical_state():
    event = EVENT.read_text(encoding="utf-8-sig")

    assert "wine_for_dance_apply_choice" not in event
    assert "EventWineForDanceApply" not in event
    assert "EventWineForDanceFinish" not in event
    assert "main_ui_runtime.action_items" not in event
    assert "MenuItem(" not in event
    assert "label WineForDanceOutcome(reaction_code=1, _crew_appreciation=None):" in event
    assert "$ YourReaction1 =" not in event
    assert "player.tavern_management.dance_sponsor = 1" in event
    assert "player.tavern_management.dance_sponsor_pledge_day" in event
    assert "player.spend_money(" in event
    assert 'main_ui_begin_native_scene_state("Пятничные танцы")' in event
    assert "main_ui_end_native_scene_state()" in event
    assert '"[scene_runtime.text]"' not in event
    assert event.count("menu:") == 2


def test_breakfast_dance_decision_is_a_native_story_menu():
    source = BREAKFAST.read_text(encoding="utf-8-sig")
    block = _label_block(
        source,
        "TavernKitchenBreakfastDanceMenu:",
        "TavernKitchenFinishBreakfastEvent:",
    )

    assert "\n    menu:\n" in block
    assert "call WineForDanceOutcome(1)" in block
    assert "call WineForDanceOutcome(2)" in block
    assert "call WineForDanceOutcome(3)" in block
    assert "main_ui_runtime.action_items" not in block
    assert "MenuItem(" not in block
    assert "QueuePagedPanelText" not in block
    assert "ReturnToMainUI" not in block


def test_kitchen_rebuilds_room_after_standalone_dance_event_without_legacy_flag():
    source = KITCHEN.read_text(encoding="utf-8-sig")
    entry = source.split("label TavernKitchen:", 1)[1].split("while True:", 1)[0]

    assert "CurEventCode" not in entry
    assert "_kitchen_wine_event_text" not in entry
    assert "call DisplayTavernEventShort" in entry
    assert entry.index("call DisplayTavernEventShort") < entry.index("$ scene_runtime.text = build_kitchen_description()")
    after_event = entry.split("call DisplayTavernEventShort", 1)[1]
    assert "$ scene_runtime.picture = tavern_kitchen_picture()" in after_event
