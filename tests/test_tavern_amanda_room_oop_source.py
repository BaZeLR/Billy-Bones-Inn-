from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "game/Inn/TavernAmandaRoom.rpy").read_text(encoding="utf-8-sig")
SEX_FLOW_SOURCE = (Path(__file__).resolve().parents[1] / "game/NPC/Girls/Amanda/AmandaAtHomeCode.rpy").read_text(encoding="utf-8-sig")


def test_amanda_room_has_one_action_source_without_builder_restore_or_loops():
    assert "def tavern_amanda_room_action_items():" in SOURCE
    assert "label TavernAmandaRoomBuildActions:" not in SOURCE
    assert "label TavernAmandaRoomRestore:" not in SOURCE
    assert "TavernAmandaRoomBuildActions" not in SOURCE
    assert "TavernAmandaRoomRestore" not in SOURCE
    assert "while _amanda_room_ui_return is None:" not in SOURCE
    assert "while _amanda_locked_ui_return is None:" not in SOURCE


def test_amanda_room_has_no_object_or_sleep_presentation_mirrors():
    assert "tavern_amanda_room_object_menu_id" not in SOURCE
    assert "tmpSleepDress" not in SOURCE
    assert 'label tavern_amanda_room_object_menu(object_id=""):' in SOURCE
    assert "$ object_id = main_ui_runtime.object_id" in SOURCE
    assert "calendar_v2.time_slot()" not in SOURCE
    assert 'not people.is_awake("amanda")' in SOURCE
    assert "tavern_amanda_room_sleep_scene()" in SOURCE


def test_amanda_sleep_dress_is_one_scene_local_value_across_the_authored_call_chain():
    assert '"_amanda_sleep_dress"' in SOURCE
    assert "$ _amanda_sleep_dress = _grope_sleep_dress" in SOURCE
    assert "tmpSleepDress" not in SOURCE + SEX_FLOW_SOURCE
    assert "if _amanda_sleep_dress == 0:" in SEX_FLOW_SOURCE
    assert "$ _amanda_sleep_dress = 2" in SEX_FLOW_SOURCE


def test_amanda_room_preserves_events_issues_search_objects_and_exits():
    for token in (
        'story_event_available("TavernAmandaRoom", "amanda_morning_window")',
        'Call("checkTriggers", "TavernAmandaRoom", "amanda_morning_window", 0)',
        'household_room_issue_action_specs("amanda")',
        'Call("DoChore", "clean_upstairs_rooms", "TavernAmandaRoom", "", "")',
        'Call("UpstairsRoomSearch", "TavernAmandaRoom")',
        'story_event_available("TavernAmandaRoom", "melissa_bats")',
        'Call("checkTriggers", "TavernAmandaRoom", "melissa_bats", 0)',
        "rooms.get(\"TavernAmandaRoom\").visible_game_items()",
        "rooms.get(\"TavernAmandaRoom\").build_exit_items()",
        "label story_amanda_room_grope_0:",
    ):
        assert token in SOURCE
    assert "TavernAmandaRoomGropeAction" not in SOURCE


def test_called_morning_episode_returns_without_overriding_schedule_location():
    block = SOURCE.split("label story_amanda_room_morning_window_0:", 1)[1].split("label story_amanda_room_grope_0:", 1)[0]

    assert "jump TavernAmandaRoom" not in block
    assert 'Amanda.location = "TavernAmandaRoom"' not in block
    assert "tavern_amanda_morning_window_episode_ready" not in SOURCE
    assert "attic_window_morning_day" not in SOURCE
    assert "main_ui_runtime.action_items = tavern_amanda_room_action_items()" in block
