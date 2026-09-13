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

    assert "define currentVersion = 90" in migration
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


def test_morning_sickness_uses_tavern_worker_ownership_instead_of_a_fixed_roster():
    morning = (ROOT / "game/NPC/Girls/Common/MorningSickness.rpy").read_text(encoding="utf-8-sig")

    assert "def tavern_morning_sickness_girl():" in morning
    assert "for girl_key, girl_info in people.girl_items():" in morning
    assert "not girl_info.is_tavern_worker()" in morning
    assert "calendar_v2.hour" not in morning
    assert "current_slot = calendar_v2.time_slot()" in morning
    assert "people.location(girl_key)" not in morning
    assert 'daily_events.exists(girl_key, "MorningSickness", "TavernKitchen", current_slot)' in morning
    assert 'for girl in ("sandra", "melissa", "amanda")' not in morning


def test_morning_sickness_is_a_standalone_event_before_breakfast_starts():
    morning = (ROOT / "game/NPC/Girls/Common/MorningSickness.rpy").read_text(encoding="utf-8-sig")
    breakfast_source = (ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
    daily_setup = (ROOT / "game/Utilities/General/NPC/DailySetstatdefault.rpy").read_text(encoding="utf-8-sig")
    event_label = morning.split("label MorningSickness(girl_name):", 1)[1].split(
        "label morning_sickness_step2", 1
    )[0]
    breakfast_label = breakfast_source.split("label TavernKitchenBreakfast:", 1)[1].split(
        "label TavernKitchenBreakfastMenu:", 1
    )[0]
    dispatch = 'call check_daily_event(_morning_sick_girl, "MorningSickness", "TavernKitchen", calendar_v2.time_slot())'

    assert 'main_ui_begin_native_scene_state("Утреннее недомогание")' in event_label
    assert "main_ui_end_native_scene_state()" in event_label
    assert "while _morning_sick_girl != \"\":" in breakfast_label
    assert breakfast_label.count(dispatch) == 1
    assert breakfast_label.index(dispatch) < breakfast_label.index("breakfast.present_ids")
    assert breakfast_label.index(dispatch) < breakfast_label.index("vscene tavern_kitchen_breakfast_picture()")
    assert "_breakfast_morning_sick_girl" not in breakfast_label
    assert 'daily_events.add(girl_name, "TavernKitchen", 2, "<", 1, 8, "MorningSickness", "MorningSickness", "girl")' in daily_setup
