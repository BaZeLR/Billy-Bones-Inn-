from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_clara_continuation_has_one_ordered_story_authority():
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    block = runtime.split('LThreadData(1, "clara", "ForestSofa"', 1)[1].split(
        'LThreadData(2, "clara", "TavernVisit"', 1
    )[0]

    stages = [
        "story_clara_forest_lake_0",
        "story_clara_forest_sofa_stash_1",
        "story_clara_sofa_first_talk_2",
        "story_clara_sofa_ritual_3",
    ]
    assert all(block.count(stage) == 1 for stage in stages)
    assert [block.index(stage) for stage in stages] == sorted(block.index(stage) for stage in stages)
    assert "#threads['claraBookletMarket'].completed" in block
    assert "#int(threads['claraPaintingsPath'].num or 0) >= 2" not in block
    assert "people.location('clara')" not in block.split('"story_clara_forest_sofa_stash_1"', 1)[0]


def test_planned_entry_event_can_run_after_a_location_closes():
    events = source("game/Utilities/General/Events/events.rpy")

    assert 'if str(self.action or "").strip() != "enter" and not _story_location_is_open(self.location):' in events
    assert 'add("location_open", action_key == "enter" or _story_location_is_open(self.location)' in events


def test_clara_clue_tool_and_sofa_use_their_domain_owners():
    items = source("game/Items/Resources/ClaraQuestItems.rpy")
    wine_store = source("game/Town/WineStore.rpy")
    forest = source("game/Forest/Forest.rpy")
    forest_story = source("game/NPC/Girls/Clara/ClaraForestSofaThread.rpy")
    merchant = source("game/NPC/Secondary/IntMongolTalk.rpy")
    sofa = source("game/Inn/TavernCursedSofa.rpy")

    assert items.count('object_id="clara_pantaloons_001"') == 1
    assert items.count('object_id="shovel_001"') == 1
    assert 'player.add_item("clara_pantaloons_001", 1)' in forest_story
    assert 'player.add_item("clara_pantaloons_001", 1)' not in wine_store
    assert 'story_event_available(room_code, "clara_stash")' in forest
    assert '_room_add_item_by_id(rooms.get("TavernMain"), "cursed_sofa_001")' in merchant
    assert 'player.add_item("cursed_sofa_001"' not in merchant
    assert 'object_id="cursed_sofa_001"' in sofa

    combined = "\n".join((items, wine_store, forest, forest_story, merchant, sofa))
    for duplicate_flag in (
        "pantaloons_taken",
        "stash_found",
        "sofa_owned",
        "sofa_installed_flag",
        "sofa_freed_flag",
        "sofa_blessed",
    ):
        assert duplicate_flag not in combined


def test_sofa_ritual_uses_existing_story_and_npc_state_then_rewards_once():
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    sofa = source("game/Inn/TavernCursedSofa.rpy")
    ritual = sofa.split("label story_clara_sofa_ritual_3:", 1)[1].split(
        "label CursedSofaRepeatStory:", 1
    )[0]

    assert "#threads['claraPaintingsPath'].completed" in runtime
    assert "#bool(Clara.sex_stat('virginity', True))" in runtime
    assert "#bool(Melissa.sex_stat('virginity', True))" in runtime
    assert "#int(player.tavern_management.client_room_hole or 0) > 0" in runtime
    assert "#int(player.tavern_management.glory_hole or 0) == 2" in runtime
    assert "#str(people.location('clara') or '') == 'TavernMain'" in runtime
    assert "#str(people.location('melissa') or '') == 'TavernMain'" in runtime
    assert ritual.count("player.intimacy.can_cum_daily += 1") == 1
    assert ritual.count('set_sex_stat("virginity", False)') == 2
    assert ritual.count("event_runtime.active_thread.complete()") == 1


def test_forest_confession_uses_native_branch_and_thread_as_protection_authority():
    runtime = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    forest = source("game/Forest/Forest.rpy")
    labels = source("game/NPC/Girls/Clara/ClaraForestSofaThread.rpy")

    assert '"ForestClearing",\n            "clara_follow"' in runtime
    assert 'Call("checkTriggers", room_code, "clara_follow", 0)' in forest
    assert 'vscene "images/clara/forest_clara_bath.png"' in labels
    assert 'vscene "images/clara/forest_clara_bath_4.png"' in labels
    assert '"Простить Клариссу и взять под свою защиту":' in labels
    assert '"Отказать и не скрывать ее вину":' in labels
    assert 'event_runtime.active_thread.abort()' in labels
    for mirror in ("protection_granted", "clara_protected", "forest_confession_seen"):
        assert mirror not in runtime
        assert mirror not in labels


def test_legare_confrontation_uses_fight_authority_and_keeps_story_alive():
    fight_runtime = source("game/Utilities/Fight/FightSystemRuntime.rpy")
    paintings = source("game/NPC/Girls/Clara/ClaraPaintingsThread.rpy")
    confrontation = paintings.split("label story_clara_paintings_confront_legare:", 1)[1].split(
        "label story_clara_paintings_artisans_2:", 1
    )[0]

    assert '"legare": FightEnemyDefinition(' in fight_runtime
    assert 'fight_begin("legare"' in confrontation
    assert "call FightLoop" in confrontation
    assert "event_runtime.active_thread.advance()" in confrontation
    assert "event_runtime.active_thread.abort()" not in confrontation


def test_amanda_and_melissa_favors_are_owned_by_their_talk_flows():
    amanda_info = source("game/NPC/Girls/Amanda/InitAmanda.rpy")
    amanda_talk = source("game/NPC/Girls/Amanda/IntAmandaTalk.rpy")
    melissa_talk = source("game/NPC/Girls/Melissa/IntMelissaTalk.rpy")

    assert "def can_grant_sexual_favor(self):" in amanda_info
    assert '"Попросить Аманду о сексуальном одолжении" if Amanda.can_grant_sexual_favor():' in amanda_talk
    assert '"Подарить маленький подарок" if social_interaction_allowed_for_npc(girl_name, "gift"):' in melissa_talk
    assert 'call PlayerCardGiftToFixedTargetMenu(girl_name)\n                $ _melissa_repeat_menu = True' in melissa_talk
    assert melissa_talk.count('"Попросить Мелиссу о сексуальном одолжении"') == 1
    assert "not Melissa.is_working()" in melissa_talk
