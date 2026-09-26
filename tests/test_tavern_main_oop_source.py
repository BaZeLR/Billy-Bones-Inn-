from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")


def test_tavern_main_has_one_action_source_without_builder_restore_or_loop():
    assert "def tavern_main_action_items():" in SOURCE
    assert "label TavernMainBuildActions:" not in SOURCE
    assert "label TavernMainRestore:" not in SOURCE
    assert "TavernMainBuildActions" not in SOURCE
    assert "TavernMainRestore" not in SOURCE
    assert "while _main_ui_return is None:" not in SOURCE


def test_tavern_main_has_no_object_menu_mirror_or_boolean_protocol():
    assert "TavernMainObjectMenuId" not in SOURCE
    assert "refresh_only" not in SOURCE
    assert 'label TavernMainObjectMenu(object_id=""):' in SOURCE
    assert "$ object_id = main_ui_runtime.object_id" in SOURCE


def test_tavern_main_preserves_room_objects_exits_clients_and_story_events():
    for token in (
        "rooms.get(\"TavernMain\").build_menu_sections()", 'Call("TavernProstClients", client_girl)',
        'client_girl in tavern_main_intimate_workers()', 'CheckIfSexEventExist(client_girl, calendar_v2.time_slot(), "Prostitution") > 0',
        'story_event_available("TavernMain", "overheard")',
        '"book_001"', '"fireplace_001"', '"bar_001"',
    ):
        assert token in SOURCE

    assert "tavern.renovation_complete('peephole') and client_girl" not in SOURCE
    assert 'Call("checkTriggers", "TavernMain", "clara_tavern_visit", 0)' not in SOURCE
    assert 'story_event_available("TavernMain", "clara_paintings")' not in SOURCE
