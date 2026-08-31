from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_daily_event_rows_own_their_call_contract():
    runtime = (ROOT / "game/Utilities/General/Common/CheckDailyEvent.rpy").read_text(encoding="utf-8-sig")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    assert 'call_mode="none"' in runtime
    assert '"CallMode": str(call_mode or "none")' in runtime
    assert '_daily_call_mode = str(_daily_row.get("CallMode", "none")' in runtime
    assert "def _daily_dispatch_args(" not in runtime
    assert "def _daily_extract_label_name(" not in runtime
    for line in game_sources.splitlines():
        if "daily_events.add(" in line:
            assert any('"%s"' % mode in line for mode in ("none", "girl", "girl_location")), line


def test_saved_daily_events_gain_call_contract_once_on_load():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert "define currentVersion = 74" in migration
    assert "def updateSave_V16():" in migration
    assert "def updateSave_V22():" in migration
    assert "def updateSave_V23():" in migration
    assert "def updateSave_V24():" in migration
    assert 'row["CallMode"]' in migration


def test_live_daily_event_callers_use_the_defined_procedure_label():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "label check_daily_event(" in game_sources
    assert "call CheckDailyEvent" not in game_sources
    assert 'renpy.has_label("CheckDailyEvent")' not in game_sources


def test_morning_sickness_queries_the_daily_event_owner_without_a_global_mirror():
    runtime = (ROOT / "game/Utilities/General/Common/CheckDailyEvent.rpy").read_text(encoding="utf-8-sig")
    morning = (ROOT / "game/NPC/Girls/Common/MorningSickness.rpy").read_text(encoding="utf-8-sig")
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    assert "DailyEventsList" not in live_sources
    assert "def exists(self, girl_name=\"\", event_type=\"\", location_name=\"\", current_time=None):" in runtime
    assert "daily_events.exists(" in morning
    assert "def morning_sickness_daily_event_ready(" not in morning
