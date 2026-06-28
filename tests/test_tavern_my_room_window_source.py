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

    assert "$ calendar_v2.sync_state()" in source
    assert "$ _window_hour = int(calendar_v2.hour or 0)" in source
    assert "$ _window_is_night = _window_hour >= 18 or _window_hour < 6" in source
    assert "amanda_night_bowl_window_event_ready()" in source


def test_player_room_window_has_distinct_descriptions_for_each_state():
    source = read_rel("game/Inn/TavernMyRoomWindow001.rpy")

    assert "Ночь делает задний двор почти безлюдным." in source
    assert "Через маленькое окно хорошо виден задний двор трактира" in source
    assert "Без своей привычной ночной миски" in source
    assert "даже получив новый горшок" in source
