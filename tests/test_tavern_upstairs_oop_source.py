from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELIEF_EVENTS = ROOT / "game/Inn/TavernUpstairsBedroomRelief.rpy"


def test_upstairs_uses_pure_action_list_without_build_label_or_room_loop():
    source = (ROOT / "game/Inn/TavernUpstairs.rpy").read_text(encoding="utf-8-sig")

    assert "def tavern_upstairs_action_items" in source
    assert "label TavernUpstairsBuildActions:" not in source
    assert "call TavernUpstairsBuildActions" not in source
    assert "while _upstairs_ui_return" not in source
    assert "rooms.get(\"TavernUpstairs\").visible_exits()" in source
    assert 'Call("TavernAmandaRoomDoor")' in source
    assert "movement_actions(target)" in source


def test_upstairs_callers_do_not_restore_through_build_wrapper():
    sandra = (ROOT / "game/Inn/TavernSandraRoom.rpy").read_text(encoding="utf-8-sig")
    amanda = (ROOT / "game/Inn/TavernAmandaRoom.rpy").read_text(encoding="utf-8-sig")

    assert "TavernUpstairsBuildActions" not in sandra + amanda
    assert "tavern_upstairs_action_items()" in sandra
    assert "label TavernAmandaRoomDoorLeave:" not in amanda


def test_upstairs_bedroom_sounds_are_not_a_repeatable_room_description_projection():
    source = (ROOT / "game/Inn/TavernUpstairs.rpy").read_text(encoding="utf-8-sig")

    assert "def tavern_upstairs_bedroom_sound_lines" not in source
    assert "tavern_upstairs_bedroom_sound_lines()" not in source
    assert "tavern_upstairs_description()" in source


def test_upstairs_bedroom_relief_is_three_npc_specific_daily_entry_events():
    source = RELIEF_EVENTS.read_text(encoding="utf-8-sig")
    event_model = source.split("class TavernUpstairsBedroomReliefEvent(Event):", 1)[1].split(
        "\n\n    AmandaUpstairsBedroomRelief", 1
    )[0]

    assert '"TavernUpstairs"' in event_model
    assert '"enter"' in event_model
    assert "500" in event_model
    assert "self.repeatable = False" in event_model
    assert 'str(people.location(self.npc_id) or "") == self.room_code' in event_model
    assert "people.is_awake(self.npc_id)" in event_model
    assert "npc_friend_level(self.npc_id) >= 2" in event_model
    assert "npc_corruption_level(self.npc_id) >= 2" in event_model
    assert "int(info.arousal_value() or 0) >= 65" in event_model
    assert "tavern_kitchen_fertility_bonus_active()" in event_model

    assert '"amanda",\n        "TavernAmandaRoom"' in source
    assert '"melissa",\n        "TavernMelissaRoom"' in source
    assert '"sandra",\n        "TavernSandraRoom"' in source
    assert source.count("= TavernUpstairsBedroomReliefEvent(") == 3
    assert '"story_amanda_upstairs_bedroom_relief",\n        (20, 22)' in source
    assert '"story_melissa_upstairs_bedroom_relief",\n        (20, 22)' in source
    assert '"story_sandra_upstairs_bedroom_relief",\n        (20, 23)' in source
    assert ".trust" not in source
    assert "bedroom_door_locked" not in source
    assert "MenuItem(" not in source


def test_each_upstairs_relief_label_owns_sound_time_arousal_and_relationship_gain():
    source = RELIEF_EVENTS.read_text(encoding="utf-8-sig")

    for npc_name, display_name in (
        ("amanda", "Аманды"),
        ("melissa", "Мелиссы"),
        ("sandra", "Сандры"),
    ):
        label = source.split(f"label story_{npc_name}_upstairs_bedroom_relief:", 1)[1].split(
            "\n\nlabel ", 1
        )[0]
        runtime_name = npc_name.capitalize()

        assert display_name in label
        assert "закрыт" in label
        assert "скрип кровати" in label
        assert f"$ {runtime_name}.set_arousal(0)" in label
        assert f'$ {runtime_name}.apply_social_chance(20, 1, 1, 0, 0, 0, "upstairs_bedroom_relief")' in label
        assert "$ calendar_v2.advance_minutes(15)" in label
        assert "main_ui_begin_native_scene_state(" in label
        assert "show screen main_ui" in label
        assert "$ scene_runtime.text = " in label
        assert "$ scene_runtime.location_text = scene_runtime.text" in label
        assert 'menu:\n        "Продолжить":\n            pass' in label
        assert "$ main_ui_end_native_scene_state()" in label
        assert "Call(" not in label


def test_upstairs_bedroom_relief_events_are_registered_once_under_their_npc_owners():
    runtime = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")

    for npc_name, runtime_name in (
        ("amanda", "Amanda"),
        ("melissa", "Melissa"),
        ("sandra", "Sandra"),
    ):
        registration = 'LThreadData(0, "%s", "UpstairsBedroomRelief", None, [\n        %sUpstairsBedroomRelief,\n    ], highlight=False, threaded=False)' % (npc_name, runtime_name)
        assert runtime.count(registration) == 1
