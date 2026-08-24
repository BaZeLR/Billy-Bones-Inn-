from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHORES_PATH = PROJECT_ROOT / "game" / "Inn" / "PlayerChoresSystem.rpy"
CAULDRON_PATH = PROJECT_ROOT / "game" / "Inn" / "TavernKitchenCauldron001.rpy"


def test_kitchen_cauldron_resolves_to_kitchen_hearth_fire():
    source = CHORES_PATH.read_text(encoding="utf-8-sig")
    resolver = source.split("def _pc_fire_object", 1)[1].split("def _pc_water_object", 1)[0]

    assert '"hearth_001"' in resolver
    assert '"cauldron_001"' in resolver
    assert "return TavernKitchenHearthObject" in resolver
    assert "return TavernMainFireplaceObject" in resolver


def test_cauldron_action_uses_contextual_kitchen_arguments():
    source = CAULDRON_PATH.read_text(encoding="utf-8-sig")

    assert 'target="BoilWater"' in source
    assert 'args=("cauldron_001", "TavernKitchen", "", "cauldron_001")' in source


def test_kitchen_fire_is_derived_from_expiry_and_daily_actions_live_on_objects():
    chores_source = CHORES_PATH.read_text(encoding="utf-8-sig")
    hearth_source = (PROJECT_ROOT / "game" / "Inn" / "TavernKitchenHearth001.rpy").read_text(encoding="utf-8-sig")
    cauldron_source = CAULDRON_PATH.read_text(encoding="utf-8-sig")
    new_day_source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay_NewDayEvents.rpy").read_text(encoding="utf-8-sig")

    assert '"fireOn"' not in hearth_source
    assert '"madeFireToday": 0' in hearth_source
    assert '"canBoilWater"' not in cauldron_source
    assert '"boiledWaterToday": 0' in cauldron_source
    assert 'def _pc_fire_is_active(fire_object):' in chores_source
    assert 'return _pc_fire_until_minute(fire_object) > _pc_calendar_total_minutes()' in chores_source
    assert '_set_object_state_int(_fire_object, "madeFireToday", 1)' in chores_source
    assert '_set_object_state_int(_water_object, "boiledWaterToday", 1)' in chores_source
    assert 'tavern_kitchen_sync_hearth_state' not in chores_source + hearth_source + cauldron_source
    assert "tavern_kitchen_reset_daily_hearth_state()" in new_day_source


def test_chores_mutate_tavern_management_owner_without_scalar_mirrors():
    source = CHORES_PATH.read_text(encoding="utf-8-sig")

    assert "player.tavern_management.cleanliness" in source
    assert "player.tavern_management.ashes_dirty_days" in source
    assert "player.tavern_management.upstairs_rooms_dirty" in source
    assert "global taverncleanliness" not in source
    assert "global ashesdirtydays" not in source
    assert "global upstairsroomsdirty" not in source
