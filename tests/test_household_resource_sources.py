from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_household_pressure_reads_real_tavern_and_inventory_resources():
    source = (ROOT / "game/Utilities/General/NPC/HouseholdAI_ren.rpy").read_text(encoding="utf-8-sig")
    assert "player.tavern_management.productnum" in source
    assert "player.tavern_management.cleanliness" in source
    assert "tavern_kitchen_food_stock_count()" in source
    assert 'player.item_count("cloth_scrap_001")' in source
    assert '"wolf_skin_001"' in source
    assert '"bear_fur_brown_001"' in source
    assert "renpy.store" not in source
    assert 'getattr(store, "food_stock"' not in source
    assert 'getattr(store, "fur_supply"' not in source
    assert 'getattr(store, "cloth_supply"' not in source
    assert "taverncleanliness" not in source
    assert "HouseholdAISeen" not in source
    assert "HouseholdAIState" not in source
    assert "household.seen[household_ai_seen_key" in source
    assert 'household.meta["last_event_day"]' in source


def test_fire_and_hot_water_use_timestamp_authority_without_unit_mirrors():
    runtime_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game/Inn").rglob("*.rpy")
    )
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert '"fire_units"' not in runtime_sources
    assert '"hot_water_units"' not in runtime_sources
    assert '"fire_until_minute"' in runtime_sources
    assert '"hot_water_until_minute"' in runtime_sources
    assert 'state.pop("fire_units"' in migration
    assert 'water_state.pop("hot_water_units"' in migration


def test_household_owns_the_only_barber_visit_day_map():
    household = (ROOT / "game/Utilities/General/NPC/HouseholdAI_ren.rpy").read_text(encoding="utf-8-sig")
    decision = (ROOT / "game/Utilities/General/NPC/GirlDecisionModel.rpy").read_text(encoding="utf-8-sig")
    descriptions = (ROOT / "game/NPC/Girls/Common/GirlsDesc.rpy").read_text(encoding="utf-8-sig")
    breakfast = (ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "self.barber_visit_last_day = {}" in household
    assert "self.barber_appointments = {}" in household
    assert 'household.barber_visit_last_day.get(girl, -99)' in decision
    assert 'household.barber_visit_last_day.get(key, -99)' in descriptions
    assert 'household.barber_visit_last_day.get(npc_id, -99)' in breakfast
    assert 'info.var.get("barber_visit_last_day"' not in game_sources
    assert 'people.get_info(npc_id).var.get("barber_visit_last_day"' not in game_sources
    assert 'var.get("barber_invite_pending"' not in game_sources
    assert 'var["barber_invite_pending"]' not in game_sources
