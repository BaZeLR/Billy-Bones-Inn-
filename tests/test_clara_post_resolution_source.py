from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy"
VISITS = ROOT / "game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy"
POST = ROOT / "game/NPC/Girls/Clara/ClaraPostResolutionThreads.rpy"
WINE_STORE = ROOT / "game/Town/WineStore.rpy"


def source(path):
    return path.read_text(encoding="utf-8-sig")


def label_block(text, name):
    block = text.split("label %s:" % name, 1)[1]
    return block.split("\nlabel ", 1)[0]


def test_clara_owns_warning_revenge_and_education_threads():
    runtime = source(RUNTIME)
    clara = runtime.split("define claraThreadList = [", 1)[1].split(
        "define beckyThreadList = [", 1
    )[0]
    georgett = runtime.split("define georgettThreadList = [", 1)[1].split(
        "define franThreadList = [", 1
    )[0]

    for name in ("AmandaWarning", "LegareRevenge", "TavernEducation"):
        assert '"clara", "%s"' % name in clara
        assert '"clara", "%s"' % name not in georgett

    for duplicate in (
        "clara_revenge_started",
        "clara_revenge_done",
        "clara_lessons_started",
        "clara_nobles_unlocked",
    ):
        assert duplicate not in runtime
        assert duplicate not in source(POST)


def test_existing_visit_cursor_keeps_length_but_no_longer_owns_lessons():
    runtime = source(RUNTIME)
    visit = runtime.split('LThreadData(2, "clara", "TavernVisit"', 1)[1].split(
        'LThreadData(0, "clara", "AmandaWarning"', 1
    )[0]
    labels = source(VISITS)

    assert visit.count('"story_clara_') == 7
    assert '"story_clara_tavern_visit_close_6"' in visit
    assert "story_clara_tavern_protection_lessons_6" not in visit
    close = label_block(labels, "story_clara_tavern_visit_close_6")
    assert "event_runtime.active_thread.advance()" in close
    assert 'skills["waitress"]' not in close
    assert "player.tavern_management.visitors" not in close


def test_revenge_is_an_ordered_three_event_story_and_fight_retries():
    runtime = source(RUNTIME)
    post = source(POST)
    thread = runtime.split('LThreadData(0, "clara", "LegareRevenge"', 1)[1].split(
        'LThreadData(0, "clara", "TavernEducation"', 1
    )[0]

    targets = (
        "story_clara_legare_revenge_amanda_tells_liza_0",
        "story_clara_legare_revenge_request_1",
        "story_clara_legare_revenge_fight_2",
    )
    assert [thread.index(target) for target in targets] == sorted(
        thread.index(target) for target in targets
    )
    assert "threads['claraPaintingsPath'].completed" in thread
    assert "threads['claraAmandaWarning'].completed" in thread
    assert "Liza.can_work_tavern()" in thread
    assert "ROOM_GROUP_TAVERN" in thread
    assert '"WineStore"' in thread
    assert '"enter"' in thread

    fight = label_block(post, "story_clara_legare_revenge_fight_2")
    assert 'fight_begin("legare", 1, "WineStore"' in fight
    assert "call FightLoop" in fight
    victory = fight.split('if _clara_revenge_outcome == "victory":', 1)[1].split(
        "else:", 1
    )[0]
    retry = fight.split("else:", 1)[1]
    assert "event_runtime.active_thread.advance()" in victory
    assert "event_runtime.active_thread.advance()" not in retry
    assert "amanda_conflict_stage" not in fight
    assert "legare_departure_code" not in fight


def test_education_waits_for_existing_innovations_and_uses_room_actions():
    runtime = source(RUNTIME)
    post = source(POST)
    wine = source(WINE_STORE)
    thread = runtime.split('LThreadData(0, "clara", "TavernEducation"', 1)[1].split(
        "# After Clarissa has moved in", 1
    )[0]

    for condition in (
        "threads['claraPaintingsPath'].completed",
        "threads['claraTavernVisit'].completed",
        "player.tavern_management.client_room_hole",
        "player.tavern_management.glory_hole",
    ):
        assert condition in thread
    assert thread.index("story_clara_tavern_education_cards_0") < thread.index(
        "story_clara_tavern_education_manners_1"
    )
    assert '"WineStore"' in thread
    assert '"clara_education_cards"' in thread
    assert '"TavernMain"' in thread
    assert '"bar_001"' in thread
    assert 'story_event_available("WineStore", "clara_education_cards")' in wine
    assert 'Call("checkTriggers", "WineStore", "clara_education_cards", 0)' in wine

    cards = label_block(post, "story_clara_tavern_education_cards_0")
    manners = label_block(post, "story_clara_tavern_education_manners_1")
    for block in (cards, manners):
        assert "main_ui_begin_native_scene_state(" in block
        assert "menu:" in block
        assert "main_ui_runtime.action_items" not in block
        assert '"[scene_runtime.text]"' not in block
        assert "event_runtime.active_thread.advance()" in block
    assert 'skills["waitress"]' in manners
    assert "player.tavern_management.visitors" in manners
    assert "player.change_tavern_fame(3)" in manners


def test_post_resolution_images_exist():
    for relative in (
        "game/images/Liza/lizaNew/liza_amanda_work_talk.png",
        "game/images/amanda/liazaamandatalk.webp",
        "game/images/clara/panishment/panishment1.jpg",
        "game/images/Alber/fight/streetdraw.jpg",
        "game/images/clara/wineSellar_clara_talk_6.png",
        "game/images/clara/tavern_visit.png",
    ):
        assert (ROOT / relative).is_file()
