from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Utilities/General/Common/RoomEnterPipeline.rpy"


def test_room_entry_calls_registered_people_events_and_household_directly():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert "room_enter_present_ids" not in source
    assert "room_enter_story_action_ready" not in source
    assert "room_enter_capture_presence" not in source
    assert "list(people.ids_at(_room_enter_code) or [])" in source
    assert 'story_event_available(_room_enter_code, "enter")' in source
    assert "except Exception" not in source
    assert 'renpy.has_label("HouseholdEvent_Try")' not in source
    assert 'call HouseholdEvent_Try(_room_enter_code, "room")' in source
