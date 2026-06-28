from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT_SECONDARY = ROOT / "game" / "NPC" / "Secondary" / "InitSecondaryNPC.rpy"
INIT_ROBIN = ROOT / "game" / "NPC" / "Secondary" / "InitRobin.rpy"
ROBIN_TALK = ROOT / "game" / "NPC" / "Secondary" / "IntRobinTalk.rpy"
BLACKWOOD = ROOT / "game" / "NPC" / "Secondary" / "SherwoodTravel.rpy"
STORY_RUNTIME = ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
CLARA_BOOKLET = ROOT / "game" / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy"
PEOPLE_RUNTIME = ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_robin_is_default_secondary_npc_object():
    source = _source(INIT_ROBIN)
    people = _source(PEOPLE_RUNTIME)

    assert "class RobinData(PeopleData):" in source
    assert "class RobinInfo(BaseNPC):" in source
    assert "define RobinStaticData = RobinData()" in source
    assert "default Robin = RobinInfo()" in source
    assert 'peopleData["robin"] = RobinStaticData' in source
    assert 'peopleInfo["robin"] = Robin' in source
    assert 'default_location="BlackwoodRoad"' in source
    assert 'self.location = "BlackwoodRoad"' in source
    assert '"robin": "BlackwoodRoad"' in people


def test_blackwood_road_owns_robin_ambush_room_and_labels():
    source = _source(BLACKWOOD)

    assert 'BlackwoodRoadRoom = Room(' in source
    assert 'code_name="BlackwoodRoad"' in source
    assert "label BlackwoodRoad:" in source
    assert "label SherwoodTravel(OnHorse=0):" in source
    assert "jump BlackwoodRoad" in source
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


def test_robin_thread_and_mongol_escape_unlock_use_objects():
    runtime = _source(STORY_RUNTIME)
    booklet = _source(CLARA_BOOKLET)
    talk = _source(ROBIN_TALK)

    assert "define robinThreadList = [" in runtime
    assert '"robin": robinThreadList' in runtime
    assert '"story_robin_blackwood_ambush_0"' in runtime
    assert '"BlackwoodRoad"' in runtime
    assert 'Robin.var["MongolSafePass"] = 1' in booklet
    assert 'Robin.var["BlackwoodRoadOpen"] = 1' in booklet
    assert "RobinVar" not in talk
    assert 'vscene "images/Robin/robin1.png"' in talk
