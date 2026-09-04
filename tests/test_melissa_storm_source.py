from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (PROJECT_ROOT / path).read_text(encoding="utf-8-sig")


def test_sleep_dispatches_hidden_story_event_instead_of_melissa_fallback():
    actions = source("game/Utilities/General/Common/Actions.rpy")
    household = source("game/Inn/HouseholdRuntimeEvents.rpy")

    assert 'if story_event_available(_sleep_target, "sleep"):' in actions
    assert 'call checkTriggers(_sleep_target, "sleep", 0)' in actions
    assert "melissa_night_wake_event_ready" not in actions + household
    assert "label MelissaNightWakeEvent:" not in household


def test_amanda_pre_liza_intimacy_stops_at_teasing_boundary():
    amanda = source("game/NPC/Girls/Amanda/InitAmanda.rpy")
    room = source("game/Inn/TavernAmandaRoom.rpy")

    assert "def liza_sex_guidance_received(self):" in amanda
    assert 'self.var_int("lizafriends", 0) > 0' in amanda
    assert "if not self.liza_sex_guidance_received() and reaction in (1, 4):" in amanda
    assert "self.liza_sex_guidance_received()" in amanda.split("def can_grant_sexual_favor", 1)[1]
    assert 'if not Amanda.liza_sex_guidance_received():' in room
    assert 'return "tease"' in room
    assert 'elif _amanda_window_outcome == "tease":' in room
