from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT_SECONDARY = ROOT / "game" / "NPC" / "Secondary" / "InitSecondaryNPC.rpy"
INIT_ROBIN = ROOT / "game" / "NPC" / "Secondary" / "InitRobin.rpy"
ROBIN_TALK = ROOT / "game" / "NPC" / "Secondary" / "IntRobinTalk.rpy"
BLACKWOOD = ROOT / "game" / "NPC" / "Secondary" / "SherwoodTravel.rpy"
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
        "knows_big_tits_village", "mongol_safe_pass", "kunidell_opened",
        "kunidell_deliveries", "blackwood_road_open",
    ):
        assert "self.%s =" % field_name in info_class

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

    assert "define robinThreadList = [" in runtime
    assert '"robin": robinThreadList' in runtime
    assert '"story_robin_blackwood_ambush_0"' in runtime
    assert '"BlackwoodRoad"' in runtime
    assert "Robin.mongol_safe_pass = True" in booklet
    assert "Robin.blackwood_road_open = True" in booklet
    assert "RobinVar" not in talk
    assert 'vscene "images/Robin/robin1.png"' in talk


def test_robin_v58_migration_consumes_old_map_once():
    migration = _source(MIGRATION)
    block = migration.split("def updateSave_V58():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 79" in migration
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
