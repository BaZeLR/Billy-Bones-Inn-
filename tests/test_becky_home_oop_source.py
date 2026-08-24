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
    assert "def becky_home_action_items():" in SOURCE


def test_becky_home_preserves_arrival_story_and_objects():
    for mode in ("FromDances", "FromDinner", "SvalnyiGreh"):
        assert mode in SOURCE
    for object_id in ("becky_home_bed", "becky_home_chests", "becky_home_dinner_table"):
        assert f'"{object_id}"' in SOURCE
        assert f'object_id="{object_id}"' in OBJECTS
    assert "call IntEddieBeckySex" in SOURCE
    assert "call BeckyEddieJoinFirst" in SOURCE
    assert "call IntBeckyGuest" in SOURCE
    assert "call IntBeckySex(GirlName)" in SOURCE
    assert "Becky.home_visit_stage = max(Becky.home_visit_stage, 2)" in SOURCE
    assert 'SetField(main_ui_runtime, "action_items", becky_home_action_items())' in SOURCE
