from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
CAMP = ROOT / "game" / "NPC" / "Secondary" / "RobinCampDestructionThread.rpy"
ITEMS = ROOT / "game" / "Items" / "Resources" / "BlackwoodCampLootItems.rpy"
GROCERY = ROOT / "game" / "Town" / "GroceryStore.rpy"
SAVE = ROOT / "game" / "TractirSaveSync.rpy"


def source(path):
    return path.read_text(encoding="utf-8")


def test_postcamp_events_follow_completed_victory_and_report_on_old_saves():
    events = source(EVENTS)
    loot = events.split('LThreadData(0, "robin", "CampLoot"', 1)[1].split(
        'LThreadData(0, "robin", "EddieRecovery"', 1
    )[0]
    recovery = events.split('LThreadData(0, "robin", "EddieRecovery"', 1)[1].split(
        'LThreadData(0, "robin", "BlackwoodRoadAmbush"', 1
    )[0]

    assert '"#int(threads[\'robinCampDestruction\'].num or 0) >= 1"' in loot
    assert '"BlackwoodRoad",\n            "enter"' in loot
    assert '"#int(threads[\'robinCampDestruction\'].num or 0) >= 2"' in recovery
    assert '"#int(Zimmer.robin_complaint_stage or 0) >= 4"' in recovery
    assert "#int(Eddie.fingal_talk_stage or 0) >= 2 or int(Becky.eddie_robbed_day or 0) > 0" in recovery
    assert '"#grocery_store_active_grocer_id() == \'becky\'"' in recovery
    assert '"GroceryStore",\n            "enter"' in recovery
    assert 'call RoomEnterEventGate(rooms.current_code, False)' in source(GROCERY)
    assert 'initStoryEventRuntime(True)' in source(SAVE)


def test_optional_camp_search_awards_catalog_items_once():
    camp = source(CAMP)
    item_source = source(ITEMS)
    loot = camp.split('label story_robin_blackwood_camp_loot_0:', 1)[1]
    found = (
        "blackwood_smooth_plug_001",
        "blackwood_carved_toy_001",
        "blackwood_pigments_001",
        "blackwood_lingerie_001",
    )
    for item_id in found:
        assert 'player.add_item("%s", 1)' % item_id in loot
        assert 'object_id="%s"' % item_id in item_source
    assert loot.count("event_runtime.active_thread.advance()") == 1
    assert loot.index("Обыскать сундук") < loot.index("event_runtime.active_thread.advance()")
    assert loot.index("Не трогать чужой сундук") > loot.index("event_runtime.active_thread.advance()")
    assert 'player.add_money(2000)' in loot


def test_recovery_returns_eddies_property_to_becky_without_player_money():
    camp = source(CAMP)
    report = camp.split('label story_robin_blackwood_camp_report_1:', 1)[1].split(
        'label story_robin_blackwood_eddie_recovery_0:', 1
    )[0]
    recovery = camp.split('label story_robin_blackwood_eddie_recovery_0:', 1)[1].split(
        'label story_robin_blackwood_camp_loot_0:', 1
    )[0]
    assert 'if Eddie.fingal_talk_stage >= 2 or Becky.eddie_robbed_day > 0:' in report
    assert 'коня Эдди и нашли его кошель' in report
    assert 'Вы передаёте ей повод и кошель' in recovery
    assert 'Becky.add_relation(2, cap=100)' in recovery
    assert recovery.count("event_runtime.active_thread.advance()") == 1
    assert "player.add_money" not in recovery


def test_trade_route_rewards_and_mongol_arrival_are_one_time_threads():
    events = source(EVENTS)
    camp = source(CAMP)
    mongol = source(ROOT / "game" / "NPC" / "Secondary" / "MongolTavernArrival.rpy")
    recovery = camp.split('label story_robin_blackwood_eddie_recovery_0:', 1)[1].split(
        'label story_robin_blackwood_camp_loot_0:', 1
    )[0]
    assert 'player.tavern_management.visitors += 20' in recovery
    assert 'player.economy.tavern_fame += 3' in recovery
    assert 'Mongol.arrival_due_day = current_game_day() + 3' in recovery
    arrival = events.split('LThreadData(0, "mongol", "TavernArrival"', 1)[1].split(
        'LThreadData(0, "mongol", "MoonSabbathGuide"', 1
    )[0]
    assert "#current_game_day() >= int(Mongol.arrival_due_day or 0)" in arrival
    assert 'player.horse.add_stable_horse(_mongol_reward_horse)' in mongol
    assert 'player.horse.carriage_ready = True' in mongol
    assert 'Mongol.tavern_servant = True' in mongol
    assert 'tractir_activate_achievement("mongol_household")' in mongol
    assert mongol.count('event_runtime.active_thread.advance()') == 1


def test_inga_pregnancy_uses_shared_girl_lifecycle():
    pregnancy = source(ROOT / "game" / "NPC" / "Girls" / "Common" / "PregnancyCheck.rpy")
    nextday = source(ROOT / "game" / "Utilities" / "Time" / "NextDay_FinishDayEvents.rpy")
    inga = source(ROOT / "game" / "NPC" / "Girls" / "Inga" / "IngaSherwoodThanks.rpy")
    assert 'isinstance(girl_info, Girl)' in pregnancy
    assert '[info.name for info in people.values() if isinstance(info, Girl)]' in nextday
    assert 'Inga.player_cum("inside")' in inga
    assert 'Inga.player_cum("outside")' in inga


def test_mongol_service_and_moon_guide_follow_existing_owners():
    mongol = source(ROOT / "game" / "NPC" / "Secondary" / "InitMongol.rpy")
    daily = source(ROOT / "game" / "Utilities" / "Time" / "NextDay_TavernDaily.rpy")
    household = source(ROOT / "game" / "Utilities" / "General" / "NPC" / "HouseholdAI_ren.rpy")
    events = source(EVENTS)
    assert 'ExtraEvents += Mongol.perform_tavern_service()' in daily
    assert 'self.last_service_day = day' in mongol
    assert '_room_add_item_units(shed, "chopped_wood_001", 10)' in mongol
    assert '"hot_water_until_minute"' in mongol
    assert 'residents.append("mongol")' in household
    assert "TotalDay['HorseFood'] += 3 *" in daily
    assert 'LThreadData(0, "mongol", "MoonSabbathGuide"' in events
    assert '"#calendar_v2.moon_phase_name_en() == \'Full Moon\'"' in events


def test_becky_store_unlock_uses_pregnancy_path():
    becky = source(ROOT / "game" / "NPC" / "Girls" / "Becky" / "BeckySherwoodStore.rpy")
    info = source(ROOT / "game" / "NPC" / "Girls" / "Becky" / "InitBecky.rpy")
    assert '"#bool(threads[\'robinEddieRecovery\'].completed)"' in source(EVENTS)
    assert 'Becky.sherwood_store_private_available()' in source(EVENTS)
    assert 'self.can_have_sex_today()' in info
    assert 'Becky.player_cum("inside")' in becky
    assert 'Becky.player_cum("outside")' in becky
