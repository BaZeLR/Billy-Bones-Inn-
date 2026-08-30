from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_clara_uses_normal_data_and_runtime_instances():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")

    assert "class ClaraData(PeopleData):" in source
    assert "class ClaraInfo(Girl):" in source
    assert "define ClaraStaticData = ClaraData()" in source
    assert "default Clara = ClaraInfo()" in source

    init_label = source.split("label InitClara:", 1)[1]
    assert "GirlName = Clara.code_name" not in init_label
    assert "Clara.var =" not in init_label
    assert "Clara.initialize_new_game_state()" in init_label
    assert "people.register(ClaraStaticData, Clara)" in init_label
    assert "Clara.install_schedule()" not in init_label


def test_clara_schedule_uses_json_interval_contract_not_duplicate_slot_schedule():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    schedule_model = _source(Path("game") / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy")

    assert "def install_schedule(self):" not in source
    assert 'self.schedule_source = "schedules/clara.json"' in source
    assert "$ npc_interval_schedule_load_all(True)" in schedule_model
    assert "npc_schedule_sync_currentloc" not in source
    assert "npc_daily_schedule_set(" not in source
    assert "npc_schedule_set(" not in source
    assert "NPCScheduleEntry(" not in source
    assert "def clara_wine_store_shift_active" not in source
    assert "def clara_extra_location_code" not in source
    assert "clara_extra_location" not in schedule_model


def test_clara_does_not_own_alber_portraits():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")

    assert "alber_random_portrait" not in source
    assert "images/Alber/" not in source


def test_clara_old_peopleinfo_bridge_is_removed():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    assert "Auto-attach .var for PeopleInfo consistency" not in source
    assert "ClaraVar" not in source
    assert "sync_from_clara_maps" not in source
    assert "sync_clara_maps" not in source
    assert "Clara.var =" not in source
    assert "if 'peopleInfo' not in dir()" not in source
    assert "class Clara(Girl):" not in source
    assert "peopleInfo['clara'] = Clara(" not in source
    assert "girls.append(peopleInfo['clara'])" not in source
    assert 'Clara.var["trust"]' not in game_sources
    assert 'Clara.var.get("trust"' not in game_sources
    assert "Clara.var" not in game_sources
    assert "Clara.set_var" not in game_sources
    assert "Clara.var_int" not in game_sources
    assert 'self.var["trust"]' not in source
    assert 'self.var.get("trust"' not in source


def test_clara_social_and_gift_logic_belongs_to_clara_instance():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    talk_source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy")
    people_runtime = _source(Path("game") / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy")
    social_topics = _source(Path("game") / "Utilities" / "General" / "NPC" / "SocialTalkTopics.rpy")
    relationship = _source(Path("game") / "Utilities" / "General" / "NPC" / "RelationshipDynamics.rpy")

    clara_class = source.split("class ClaraInfo(Girl):", 1)[1].split("define ClaraStaticData", 1)[0]
    for old_map in [
        'Friends.get("clara"',
        'Friends["clara"]',
        'Talked.get("clara"',
        'TalkedToday.get("clara"',
        'AskedToday.get("clara"',
        'FlirtedToday.get("clara"',
        'GiftedToday.get("clara"',
        'otkroven.get("clara"',
        'otkroven["clara"]',
        'sluttiness.get("clara"',
        'sluttiness["clara"]',
        'CurrentLoc["clara"]',
    ]:
        assert old_map not in clara_class

    for method_name in [
        "wine_store_talk_picture",
        "wine_store_flirt_picture",
        "forest_picture",
        "visible_at_friday_dance",
        "can_start_social_events",
        "can_receive_gifts",
        "has_caught_cat_gift",
        "can_accept_horse_ride",
        "giftable_entries",
        "has_giftable_entries",
        "remove_gift_entry",
    ]:
        assert f"def {method_name}(self" in clara_class

    for removed_global in [
        "def clara_wine_store_talk_picture",
        "def clara_wine_store_flirt_picture",
        "def clara_forest_picture",
        "def clara_visible_at_friday_dance",
    ]:
        assert removed_global not in source

    assert "except Exception" not in source
    assert "def ensure_story_defaults(self" not in clara_class
    assert "def reset_daily(self" not in clara_class
    assert "Clara.wine_store_talk_picture()" in talk_source
    assert "Clara.wine_store_flirt_picture()" in talk_source
    assert "Clara.forest_picture(" in talk_source
    assert '_clara_flirted_before = Clara.flirted_today' in talk_source
    assert "Clara.flirt_count =" in talk_source
    for duplicate_social_method in ["social_outcome", "apply_result_counters", "apply_social_result"]:
        assert f"def {duplicate_social_method}(self" not in clara_class
    for duplicate_social_key in ['"positive":', '"neutral":', '"negative":', '"lastsocial":']:
        assert duplicate_social_key not in clara_class

    for old_name in [
        "def clara_can_start_social_events",
        "def clara_can_receive_gifts",
        "def clara_has_caught_cat_gift",
        "def clara_can_accept_horse_ride",
        "def clara_giftable_entries",
        "def clara_has_giftable_entries",
        "def clara_remove_gift_entry",
        "def clara_social_outcome",
        "def clara_apply_result_counters",
        "def clara_apply_social_result",
    ]:
        assert old_name not in source
        assert old_name not in talk_source

    assert 'social_interaction_allowed_for_npc(girl_name, "flirt")' in talk_source
    assert "Clara.giftable_entries()" in talk_source
    assert "Clara.remove_gift_entry(_selected)" in talk_source
    assert 'SocialTalkTopicMenu(girl_name, "talk")' in talk_source
    assert 'SocialTalkTopicMenu(girl_name, "flirt")' in talk_source
    assert "label IntClaraTalkMenu:" not in talk_source
    assert "jump IntClaraTalkMenu" not in talk_source
    assert "while True:" not in talk_source
    assert "jump IntClaraTalk" not in talk_source
    assert "if _clara_talk_new:" in talk_source
    assert 'main_ui_runtime.talk_picture = _clara_talk_picture' in talk_source
    assert 'str(rooms.current_code or "") == "WineStore"' in talk_source
    assert 'str(rooms.current_code or "") in ("ForestClearing", "ForestSpring", "ForestLake")' in talk_source
    assert talk_source.index('main_ui_begin_talk_state("Разговор с Клариссой", girl_name)') < talk_source.index("vscene _clara_talk_picture")
    assert "Clara.can_receive_gifts()" not in people_runtime
    assert "def npc_gift_action_available" not in people_runtime
    assert "Clara.has_giftable_entries()" not in people_runtime
    assert "Clara.has_caught_cat_gift()" in social_topics
    clara_requirements = relationship.split('"clara": {', 1)[1].split('"becky": {', 1)[0]
    assert '"flirt": {"score": 0, "friend": 5, "open": 0, "slut": 0}' in clara_requirements

    assert "label IntClaraTalkApply" not in talk_source
    assert "choice_code" not in talk_source
    assert 'call IntClaraTalkApply' not in talk_source
    gift_menu = talk_source.split("label IntClaraGiftMenu", 1)[1]
    assert "menu:" in gift_menu
    assert "renpy.display_menu" not in gift_menu
    assert '"Назад":' in gift_menu
    assert "main_ui_runtime.action_items" not in gift_menu
    assert "label IntClaraGiftApply" not in talk_source


def test_clara_random_logic_uses_project_random_engine():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    talk_source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy")

    assert "procedural_randint(" in source
    assert "random.randint" not in source
    assert "renpy.random.randint" not in source
    assert "random.randint" not in talk_source
    assert "renpy.random.randint" not in talk_source


def test_clara_rewards_use_their_system_owners_without_wrappers():
    paintings = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraPaintingsThread.rpy")
    crafting = _source(Path("game") / "Items" / "Crafting" / "SoapCraftAndAtticItems.rpy")
    progress = _source(Path("game") / "Utilities" / "General" / "Common" / "AchievementsEndings.rpy")
    barber = _source(Path("game") / "Town" / "Arts" / "BarberShop.rpy")

    assert "clara_paintings_special_cream_recipe_unlocked" not in paintings + crafting
    assert "self.special_cream_recipe_unlocked = False" in crafting
    assert "crafting.special_cream_recipe_unlocked = True" in paintings
    assert "unlock_condition=lambda: bool(crafting.special_cream_recipe_unlocked)" in crafting
    assert "self.sergio_discount_percent = 0" in progress
    assert "tractir_progress.sergio_discount_percent = 25" in paintings
    assert "int(tractir_progress.sergio_discount_percent or 0)" in barber


def test_clara_story_state_uses_explicit_properties_and_one_time_migration():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    migration = _source(Path("game") / "TractirSaveSync.rpy")
    clara_class = source.split("class ClaraInfo(Girl):", 1)[1].split("define ClaraStaticData", 1)[0]
    migration_block = migration.split("def updateSave_V51():", 1)[1].split("label before_load:", 1)[0]

    for property_name in (
        "flirt_count", "drawings_secret_known", "market_intro_seen",
        "market_follow_failed_day", "market_follow_failed_hour", "market_day_roll_day",
        "market_day_roll", "market_evening_roll_day", "market_evening_roll",
        "day_location_override_day", "day_location_override_code",
        "merchant_contact_unlocked", "merchant_contact_month_key",
        "old_water_pump_hint_seen", "commission_followup_day", "murder_day",
    ):
        assert f"self.{property_name} =" in clara_class

    assert "STORY_DEFAULTS = {" not in clara_class
    assert "self.var =" not in clara_class
    assert "self.ensure_story_defaults()" not in clara_class
    assert "def updateSave_V51():" in migration
    assert "if loaded_version < 52:" in migration
    for legacy_key in (
        "flirt", "drawings_secret_known", "market_intro_seen", "market_follow_failed_day",
        "market_follow_failed_hour", "market_day_roll_day", "market_day_roll",
        "market_evening_roll_day", "market_evening_roll", "day_location_override",
        "merchant_contact_unlocked", "merchant_contact_month_key", "old_water_pump_hint_seen",
        "commission_followup_day", "murder_day", "special_cream_recipe_unlocked", "sergio_discount",
    ):
        assert f'"{legacy_key}"' in migration_block


def test_clara_departures_end_talk_and_use_day_bounded_location_state():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    talk_source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy")

    assert "def set_day_location_override(self" in source
    assert "def getLocation(self, wday=None, hour=None):" in source
    assert "Clara.location =" not in talk_source
    assert talk_source.count("$ main_ui_end_talk_state()") >= 3
