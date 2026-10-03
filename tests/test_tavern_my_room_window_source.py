from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_player_room_window_uses_three_real_player_room_pictures():
    source = read_rel("game/Inn/TavernMyRoomWindow001.rpy")

    assert '"images/player_room/window0.png"' in source
    assert '"images/player_room/window2.png"' in source
    assert '"images/player_room/windowAmand.png"' in source
    assert "images/tavern/backyard/pees_in_backyard.png" not in source
    assert "renpy.loadable" not in source


def test_player_room_window_uses_calendar_hour_for_day_night_choice():
    source = read_rel("game/Inn/TavernMyRoomWindow001.rpy")

    assert "$ calendar_v2.sync_state()" not in source
    assert "$ _window_hour = int(calendar_v2.hour or 0)" in source
    assert "$ _window_is_night = _window_hour >= 18 or _window_hour < 6" in source
    assert 'call checkTriggers("TavernMyRoom", "window_look", 0)' in source
    assert "label story_amanda_night_bowl_window_0:" in source
    assert "amanda_night_bowl_window_event_ready" not in source
    assert "night_bowl_window_seen_day" not in source


def test_player_room_window_object_menu_selects_existing_night_picture():
    source = read_rel("game/Inn/TavernMyRoom.rpy")
    menu = source.split('label TavernMyRoomObjectMenu(', 1)[1].split('\nlabel ', 1)[0]
    assert 'if object_id == "myroom_window_001" and (int(calendar_v2.hour or 0) >= 18 or int(calendar_v2.hour or 0) < 6):' in menu
    assert '_object_picture = "images/player_room/window2.png"' in menu
    assert menu.index('_object_picture = "images/player_room/window2.png"') < menu.index('scene_runtime.picture = _object_picture')


def test_player_room_window_has_distinct_descriptions_for_each_state():
    source = read_rel("game/Inn/TavernMyRoomWindow001.rpy")

    assert "Ночь делает задний двор почти безлюдным." in source
    assert "Через маленькое окно хорошо виден задний двор трактира" in source
    assert "Без своей привычной ночной миски" in source
    assert "даже получив новый горшок" in source


def test_player_room_window_scenes_hide_object_actions_until_closed():
    source = read_rel("game/Inn/TavernMyRoomWindow001.rpy")
    look = source.split("label TavernMyRoomWindowLookBackyard:", 1)[1].split(
        "label story_amanda_night_bowl_window_0:", 1
    )[0]
    event = source.split("label story_amanda_night_bowl_window_0:", 1)[1]
    for block in (look, event):
        assert 'main_ui_begin_native_scene_state("Маленькое окно")' in block
        assert '"Закрыть окно":' in block
        assert "main_ui_end_native_scene_state()" in block
        assert "call TavernMyRoomObjectMenu" not in block
