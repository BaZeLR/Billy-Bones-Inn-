from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_friday_dance_and_church_daily_state_have_domain_owners():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    friday = (ROOT / "game/Town/Market/FridayDance.rpy").read_text(encoding="utf-8-sig")
    assert "class FridayDanceRoom(Room):" in friday
    assert 'self.state.setdefault("dance_count", 0)' in friday
    assert 'self.state.setdefault("becky_home_invited", False)' in friday
    assert 'schedule=RoomSchedule(weekdays=[5], start="18:00", end="21:59")' in friday
    assert 'rooms.get("FridayDance").is_open()' in friday
    assert "def slot_is_active" not in friday
    assert 'rooms.get(\"FridayDance\").dance_count' in runtime
    assert "player.economy.church_donated_today" in runtime
    assert "FridayDancesCount" not in runtime
    assert "ChurchDonatedToday" not in runtime


def test_town_street_daily_reset_is_owned_and_preserves_cooldowns():
    source = (ROOT / "game/Utilities/Time/NextDay_FinishDayEvents.rpy").read_text(encoding="utf-8-sig")
    runtime = (ROOT / "game/Town/RandomTownEvents.rpy").read_text(encoding="utf-8-sig")

    assert "TownStreet.reset_day()" in source
    reset = runtime.split("def reset_day(self):", 1)[1].split("def time_event_key", 1)[0]
    for field in ("events_today", "patrols_today", "fights_today", "curfew_caught_today", "story_seen_keys"):
        assert "self.%s" % field in reset
    assert "cooldowns" not in reset
    for retired_field in ("daily_plan", "last_event_text", "self.context", "fired_labels_today", "fired_locations_today"):
        assert retired_field not in runtime
    for legacy_name in (
        "TownStreetStorySeenKeys",
        "TownStreetDailyPlan",
        "TownStreetLastEventText",
        "TownStreetContext",
        "TownStreetCooldowns",
    ):
        assert legacy_name not in source
