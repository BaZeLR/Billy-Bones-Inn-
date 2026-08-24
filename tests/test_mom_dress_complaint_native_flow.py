from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/NPC/Girls/Common/MomDressComplaint.rpy"


def test_mom_dress_complaint_is_native_label_driven_story_flow():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert source.count("\n        menu:\n") >= 2
    assert source.count("\n    menu:\n") >= 4
    assert "QueuePagedPanelText" not in source
    assert "ReturnToMainUI" not in source
    assert "MenuItem(" not in source
    assert "mom_dress_complaint_return_items" not in source
    assert source.count("jump MomDressComplaintFinish") == 9
    assert 'rooms.get(\"TavernMain\").state["block_events"]' not in source
    assert "main_ui_end_native_scene_state()" in source
    assert 'Jump("TavernMain")' not in source
