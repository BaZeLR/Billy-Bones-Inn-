from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "game/Town/BeckyHome.rpy").read_text(encoding="utf-8-sig")
OBJECTS = (ROOT / "game/Town/BeckyHomeObjects.rpy").read_text(encoding="utf-8-sig")


def test_becky_home_has_no_active_boolean_or_restore_builder_wrappers():
    assert "BeckyHomeActive" not in SOURCE
    assert "label BeckyHomeBuildActions:" not in SOURCE
    assert "label BeckyHomeRestore:" not in SOURCE
    assert "label BeckyHomeReturnFromObject:" not in SOURCE
    assert "call BeckyHomeBuildActions" not in SOURCE
    assert "call BeckyHomeRestore" not in SOURCE
    assert "def becky_home_action_items():" not in SOURCE


def test_becky_home_preserves_arrival_story_without_invented_objects():
    for mode in ("FromDances", "FromDinner", "SvalnyiGreh"):
        assert mode in SOURCE
    for object_id in ("becky_home_bed", "becky_home_chests", "becky_home_dinner_table"):
        assert object_id not in SOURCE
    assert "GameObject(" not in OBJECTS
    assert "call IntEddieBeckySex" in SOURCE
    assert 'call checkTriggers("BeckyHome", "enter", 0)' in SOURCE
    assert "call IntBeckyGuest" in SOURCE
    assert "call IntBeckySex(GirlName)" in SOURCE
    assert "call IntBeckySex(GirlName)\n        jump BeckyHomeAfterSex" in SOURCE
    assert 'threads["beckyHome"].advanceTo(2, force_active=True)' in SOURCE
    assert 'rooms.get("BeckyHome").build_exit_items()' in SOURCE
    assert "label BeckyHomeObjectMenu" not in SOURCE
    assert "label BeckyHomeObjectText" not in SOURCE


def test_becky_home_is_not_closed_before_its_evening_story_event():
    room_definition = SOURCE.split("BeckyHomeRoomDefinition = Room(", 1)[1].split("label BeckyHome", 1)[0]

    assert "schedule=" not in room_definition
    assert "game_items=[]" in room_definition
    assert '"object_menu_label"' not in room_definition
    assert "<br>" not in SOURCE
