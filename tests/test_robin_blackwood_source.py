from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT_SECONDARY = ROOT / "game" / "NPC" / "Secondary" / "InitSecondaryNPC.rpy"
INIT_ROBIN = ROOT / "game" / "NPC" / "Secondary" / "InitRobin.rpy"
ROBIN_TALK = ROOT / "game" / "NPC" / "Secondary" / "IntRobinTalk.rpy"
BLACKWOOD = ROOT / "game" / "NPC" / "Secondary" / "SherwoodTravel.rpy"
ROBIN_CAMP = ROOT / "game" / "NPC" / "Secondary" / "RobinCampDestructionThread.rpy"
STORY_RUNTIME = ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
CLARA_BOOKLET = ROOT / "game" / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy"
PEOPLE_RUNTIME = ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"
MIGRATION = ROOT / "game" / "TractirSaveSync.rpy"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_robin_is_default_secondary_npc_object():
    source = _source(INIT_ROBIN)
    people = _source(PEOPLE_RUNTIME)

    assert "class RobinData(PeopleData):" in source
    assert "class RobinInfo(BaseNPC):" in source
    assert "define RobinStaticData = RobinData()" in source
    assert "default Robin = RobinInfo()" in source
    assert "people.register(RobinStaticData, Robin)" in source
    assert 'default_location="BlackwoodRoad"' in source
    assert 'self.location = "BlackwoodRoad"' not in source
    assert 'Robin.location = "BlackwoodRoad"' not in _source(BLACKWOOD)
    assert "def people_initial_location" not in people

    info_class = source.split("class RobinInfo(BaseNPC):", 1)[1]
    assert "STORY_DEFAULTS" not in info_class
    assert "ensure_story_defaults" not in info_class
    assert "def robin_story_defaults(" not in source
    for field_name in (
        "identity_known", "complaint_explained", "place_explained",
        "weapon_source_explained", "robbery_count", "negotiation_stage",
        "knows_big_tits_village", "mongol_safe_pass",
        "kunidell_deliveries", "blackwood_road_open",
    ):
        assert "self.%s =" % field_name in info_class
    assert "self.kunidell_opened =" not in info_class

    live_source = "\n".join((source, _source(ROBIN_TALK), _source(BLACKWOOD)))
    for legacy_access in (
        "Robin.var", "Robin.var_int", "Robin.set_var_int", "Robin.add_var_int",
        "Robin.set_story_value_min",
    ):
        assert legacy_access not in live_source

    assert "Robin.knows_big_tits_village = True" in _source(BLACKWOOD)


def test_blackwood_road_owns_robin_ambush_room_and_labels():
    source = _source(BLACKWOOD)
    room_entry = source.split("label BlackwoodRoad:", 1)[1].split(
        "label story_robin_blackwood_ambush_0:", 1
    )[0]

    assert 'BlackwoodRoadRoomDefinition = Room(' in source
    assert 'code_name="BlackwoodRoad"' in source
    assert "label BlackwoodRoad:" in source
    assert "label SherwoodTravel" not in source
    assert '"legacy_location"' not in source
    for label in [
        "label story_robin_blackwood_ambush_0:",
        "label story_robin_blackwood_approach:",
        "label story_robin_blackwood_mongol_pass:",
        "label story_robin_blackwood_first_robbery:",
        "label story_robin_blackwood_repeat_robbery:",
        "label story_robin_blackwood_robbed_return:",
        "label story_robin_blackwood_return_to_city:",
    ]:
        assert label in source
    assert 'vscene "images/Robin/robin.png"' in source
    assert 'vscene "images/Robin/mongolAndRobin1.png"' in source
    assert "renpy.random" not in source
    assert "jump BlackwoodRoad" not in room_entry
    assert "while True:\n        call screen main_ui" in room_entry
    assert room_entry.rstrip().endswith("call screen main_ui")


def test_robin_thread_and_mongol_escape_unlock_use_objects():
    runtime = _source(STORY_RUNTIME)
    booklet = _source(CLARA_BOOKLET)
    talk = _source(ROBIN_TALK)
    blackwood = _source(BLACKWOOD)

    assert "define robinThreadList = [" in runtime
    assert '"robin": robinThreadList' in runtime
    assert '"story_robin_blackwood_ambush_0"' in runtime
    assert '"BlackwoodRoad"' in runtime
    assert "Robin.mongol_safe_pass = True" in booklet
    assert "Robin.blackwood_road_open = True" in booklet
    assert "RobinVar" not in talk
    assert 'vscene "images/Robin/robin1.png"' in talk
    mongol_pass = blackwood.split("label story_robin_blackwood_mongol_pass:", 1)[1].split(
        "label story_robin_blackwood_first_robbery:", 1
    )[0]
    assert "event_runtime.active_thread" not in mongol_pass


def test_robin_camp_thread_owns_assault_then_report_and_stops_ambush_on_victory():
    runtime = _source(STORY_RUNTIME)
    camp = runtime.split('LThreadData(0, "robin", "CampDestruction"', 1)[1].split(
        'LThreadData(0, "robin", "BlackwoodRoadAmbush"', 1
    )[0]
    ambush = runtime.split('LThreadData(0, "robin", "BlackwoodRoadAmbush"', 1)[1].split(
        "define sherwoodThreadList", 1
    )[0]

    assert '"#int(Zimmer.robin_complaint_stage or 0) >= 3"' in camp
    assert camp.index('"story_robin_blackwood_camp_assault_0"') < camp.index(
        '"story_robin_blackwood_camp_report_1"'
    )
    assert '"BlackwoodRoad"' in camp
    assert '"enter"' in camp
    assert "-100" in camp
    assert '"talk_zimmer"' in camp
    assert '"robin_camp_report"' in camp
    assert '"#int(threads[\'robinCampDestruction\'].num or 0) == 0"' in ambush


def test_robin_camp_fight_advances_only_after_victory():
    source = _source(ROBIN_CAMP)
    assault = source.split("label story_robin_blackwood_camp_assault_0:", 1)[1].split(
        "label story_robin_blackwood_camp_report_1:", 1
    )[0]
    victory = assault.split('if _robin_camp_outcome == "victory":', 1)[1].split(
        'elif _robin_camp_outcome == "defeat":', 1
    )[0]
    failure = assault.split('elif _robin_camp_outcome == "defeat":', 1)[1]

    assert 'fight_begin("street_crook", 3, "BlackwoodRoad"' in assault
    assert 'fight.last_result.get("outcome", "")' in assault
    assert "$ event_runtime.active_thread.advance()" in victory
    assert "active_thread.advance" not in failure
    assert "player.add_money" not in assault
    assert "player.add_item" not in assault


def test_robin_camp_report_closes_zimmer_case_without_parallel_flag():
    source = _source(ROBIN_CAMP)
    report = source.split("label story_robin_blackwood_camp_report_1:", 1)[1]

    assert "$ Zimmer.robin_complaint_stage = 4" in report
    assert "$ Zimmer.mark_talked(1)" in report
    assert "$ event_runtime.active_thread.advance()" in report
    assert "default " not in source
    assert "Robin.var" not in source


def test_blackwood_terminal_outcomes_return_directly_to_tavern():
    source = _source(BLACKWOOD)
    terminal_labels = (
        ("story_robin_blackwood_mongol_pass", "story_robin_blackwood_first_robbery"),
        ("story_robin_blackwood_robbed_return", "story_robin_blackwood_return_to_city"),
        ("story_robin_blackwood_return_to_city", None),
    )

    for label, next_label in terminal_labels:
        block = source.split("label %s:" % label, 1)[1]
        if next_label is not None:
            block = block.split("label %s:" % next_label, 1)[0]
        assert '"Домой":' in block
        assert "jump TavernMain" in block
        assert "return True" not in block


def test_robin_v58_migration_consumes_old_map_once():
    migration = _source(MIGRATION)
    block = migration.split("def updateSave_V58():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 92" in migration
    assert "if loaded_version < 59:" in migration
    assert "updateSave_V58()" in migration
    for old_key, field_name in (
        ("KnowHim", "identity_known"),
        ("KnowComplaint", "complaint_explained"),
        ("KnowPlace", "place_explained"),
        ("KnowWeapon", "weapon_source_explained"),
        ("RobbedNum", "robbery_count"),
        ("Negotiate", "negotiation_stage"),
        ("KnowBigTitsVillage", "knows_big_tits_village"),
        ("MongolSafePass", "mongol_safe_pass"),
        ("KunidellOpened", "kunidell_opened"),
        ("KunidellDeliveries", "kunidell_deliveries"),
        ("BlackwoodRoadOpen", "blackwood_road_open"),
    ):
        assert 'robin_var.pop("%s"' % old_key in block
        assert "Robin.%s =" % field_name in block
    assert 'globals().pop("RobinVar", None)' in block

    v87 = migration.split("def updateSave_V87():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]
    assert 'getattr(Robin, "kunidell_opened", False)' in v87
    assert 'Robin.__dict__.pop("kunidell_opened", None)' in v87
