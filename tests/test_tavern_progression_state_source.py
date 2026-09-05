from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def runtime_source():
    return "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )


def test_tavern_progression_days_and_stamps_are_player_tavern_owned():
    runtime = runtime_source()
    assert "player.tavern_management.dance_sponsor_pledge_day" in runtime
    assert "player.tavern_management.weekly_chores_last_eval_stamp" in runtime
    assert "DanceSponsorPledgeDay" not in runtime
    assert "WeeklyChoresLastEvalStamp" not in runtime


def test_tavern_resources_and_construction_have_one_runtime_owner():
    runtime = runtime_source()

    for legacy_name in (
        "IngaVar",
        "_nd_ensure_dict",
        "_nd_ensure_scalar",
        "default tavernvisitors =",
        "default productnum =",
        "default winenum =",
        "default SloganFixed =",
        "default TavernHole =",
        "default TavernGloryHole =",
        "default BreakfastToday =",
        "default StolenHorseDays =",
    ):
        assert legacy_name not in runtime

    for owner_path in (
        "player.tavern_management.visitors",
        "player.tavern_management.productnum",
        "player.tavern_management.winenum",
        "player.tavern_management.slogan_state",
        "player.tavern_management.client_room_hole",
        "player.tavern_management.glory_hole",
        "player.tavern_management.breakfast.today",
        "household.member_count()",
        "player.horse.stolen_days",
    ):
        assert owner_path in runtime


def test_breakfast_runtime_state_is_owned_by_player_tavern_breakfast():
    runtime = runtime_source()

    assert "TavernBreakfast" not in runtime
    assert "TavernSundayDinner" not in runtime
    for field_name in (
        "event_active",
        "present_ids",
        "base_text",
        "soap_announced_day",
        "food_perk_day",
        "drink_perk_day",
        "lewd_series_day",
        "sunday_dinner_last_day",
    ):
        assert "player.tavern_management.breakfast.%s" % field_name in runtime


def test_tavern_report_selection_is_main_ui_session_state():
    runtime = runtime_source()

    assert "TavernReportSelectedPerson" not in runtime
    assert 'self.tavern_report_person = ""' in runtime
    assert "main_ui_runtime.tavern_report_person" in runtime


def test_tavern_progression_legacy_scalars_are_not_save_authorities():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    assert "DanceSponsorPledgeDay" not in migration
    assert "WeeklyChoresLastEvalStamp" not in migration


def test_save_repair_has_no_legacy_store_import_or_migration_layer():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    for forbidden in (
        "import renpy.store as store",
        "getattr(store",
        "delattr(store",
        "tractir_save_migrate_",
    ):
        assert forbidden not in migration

    runtime = runtime_source()
    assert "player.tavern_management.household_members" not in runtime
    assert 'player.tavern_management.__dict__.pop("household_members", None)' in migration

    assert "tractir_save_normalize_rooms()" in migration
    assert "tractir_save_remove_owned_unique_items_from_rooms()" in migration
    assert "tractir_save_clear_room_ui_cache()" in migration
