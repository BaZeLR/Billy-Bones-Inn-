from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "game/Inn/TavernAmandaRoom.rpy").read_text(encoding="utf-8-sig")
SEX_FLOW_SOURCE = (Path(__file__).resolve().parents[1] / "game/NPC/Girls/Amanda/AmandaAtHomeCode.rpy").read_text(encoding="utf-8-sig")
HOUSEHOLD_SOURCE = (Path(__file__).resolve().parents[1] / "game/Inn/HouseholdRuntimeEvents.rpy").read_text(encoding="utf-8-sig")
ROOM_ASSETS = Path(__file__).resolve().parents[1] / "game/images/amanda/Room"


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
    assert "tavern_amanda_room_pick_picture" not in SOURCE


def test_amanda_room_picture_catalog_uses_corruption_and_owned_arousal_state():
    assert 'corruption_level = npc_corruption_level("amanda")' in SOURCE
    assert "horny_state = int(Amanda.arousal_value() or 0) >= 65" in SOURCE
    assert "sleep_picture_number = 9 + max(0, min(2, dress_state))" in SOURCE
    assert '7: "images/amanda/Room/amanda_sleeps_7.png"' in SOURCE
    assert '8: "images/amanda/Room/amanda_sleeps_7.png"' in SOURCE
    assert "bedroom_picture_number = min(5, corruption_level + 1 + (1 if horny_state else 0))" in SOURCE

    for picture_name in (
        "amanda_sleeps_1.jpg",
        "amanda_sleeps_2.png",
        "amanda_sleeps_3.png",
        "amanda_sleeps_4.png",
        "amanda_sleeps_6.png",
        "amanda_sleeps_7.png",
        "amanda_sleeps_9.png",
        "amanda_sleeps_10.png",
        "amanda_sleeps_11.png",
        "amanda_bedroom_001.jpeg",
        "amanda_bedroom_002.jpeg",
        "amanda_bedroom_003.jpeg",
        "amanda_bedroom_004.jpeg",
        "amanda_bedroom_005.jpeg",
        "wakedress.jpg",
        "wakenaked.jpg",
    ):
        assert (ROOM_ASSETS / picture_name).is_file()


def test_both_amanda_wake_flows_use_the_authored_wake_pictures():
    household_wake = HOUSEHOLD_SOURCE.split('label HouseholdWakeSleepyGirl(girl_name=""):', 1)[1].split("label MelissaNightWakeEvent:", 1)[0]
    night_wake = SOURCE.split("label story_amanda_room_grope_0:", 1)[1]

    assert 'return "images/amanda/Room/wakenaked.jpg"' in SOURCE
    assert 'return "images/amanda/Room/wakedress.jpg"' in SOURCE
    assert "def tavern_amanda_room_wake_picture(sleep_dress=None):" in SOURCE
    assert "call ShowImage" not in household_wake + night_wake
    assert "vscene _wake_amanda_picture" in household_wake
    assert "vscene _amanda_wake_picture" in night_wake


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
        'story_event_available(rooms.current_code, "melissa_bats")',
        'call checkTriggers(rooms.current_code, "melissa_bats", 0)',
        "rooms.get(\"TavernAmandaRoom\").visible_game_items()",
        "rooms.get(\"TavernAmandaRoom\").build_exit_items()",
        "label story_amanda_room_grope_0:",
    ):
        assert token in SOURCE

    action_builder = SOURCE.split("def tavern_amanda_room_action_items():", 1)[1].split("label TavernAmandaRoom:", 1)[0]
    assert 'Call("checkTriggers", "TavernAmandaRoom", "melissa_bats", 0)' not in action_builder
    assert "TavernAmandaRoomGropeAction" not in SOURCE


def test_called_morning_episode_returns_without_overriding_schedule_location():
    block = SOURCE.split("label story_amanda_room_morning_window_0:", 1)[1].split("label story_amanda_room_grope_0:", 1)[0]

    assert "jump TavernAmandaRoom" not in block
    assert 'Amanda.location = "TavernAmandaRoom"' not in block
    assert "tavern_amanda_morning_window_episode_ready" not in SOURCE
    assert "attic_window_morning_day" not in SOURCE
    assert 'main_ui_begin_native_scene_state("Аманда у окна")' in block
    assert "vscene _amanda_room_picture" in block
    assert block.count("menu:") == 2
    assert '"Продолжить":' in block
    assert '"Оставить Аманду собираться":' in block
    assert "main_ui_end_native_scene_state()" in block
    assert "main_ui_runtime.action_items = tavern_amanda_room_action_items()" in block


def test_knock_uses_authoritative_schedule_presence_before_any_response_roll():
    block = SOURCE.split("label TavernAmandaRoomKnock:", 1)[1].split(
        "label TavernAmandaRoomKnockAnswer:", 1
    )[0]

    presence_check = 'if str(people.location("amanda") or "") != "TavernAmandaRoom":'
    assert presence_check in block
    assert block.index(presence_check) < block.index("procedural_randint(")
    assert 'scene_runtime.text = "Вы постучали в дверь, но ответа не последовало."' in block
    assert 'MenuItem("Попробовать войти", Call("TavernAmandaRoomEnterWithoutKnock"))' in block
