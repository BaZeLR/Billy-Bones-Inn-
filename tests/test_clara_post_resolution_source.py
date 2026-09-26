from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy"
VISITS = ROOT / "game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy"
POST = ROOT / "game/NPC/Girls/Clara/ClaraPostResolutionThreads.rpy"
CARDS = ROOT / "game/NPC/Girls/Clara/ClaraEducationCards.rpy"
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


def test_education_keeps_gates_and_uses_market_discovery():
    runtime = source(RUNTIME)
    post = source(POST)
    wine = source(WINE_STORE)
    thread = runtime.split('LThreadData(0, "clara", "TavernEducation"', 1)[1].split(
        "# After Clarissa has moved in", 1
    )[0]

    for condition in (
        "threads['claraPaintingsPath'].completed",
        "threads['claraTavernVisit'].completed",
        "tavern.renovation_complete('peephole')",
        "tavern.renovation_complete('glory_hole')",
    ):
        assert condition in thread
    assert thread.index("claraEducationCardsEvent") < thread.index(
        "story_clara_tavern_education_manners_1"
    )
    card_source = source(CARDS)
    assert 'range(1, 7, 5), (20, 23)' in card_source
    assert 'None, "MarketPlace", "enter", 0, True' in card_source
    assert '"TavernMain"' in thread
    assert '"bar_001"' in thread
    assert '"clara_education_cards"' not in wine

    cards = label_block(card_source, "story_clara_tavern_education_cards_0")
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


def test_card_images_and_native_choices_follow_numeric_order():
    cards = label_block(source(CARDS), "story_clara_tavern_education_cards_0")
    pictures = ['vscene "images/clara/education/cardplay%d.jpg"' % n for n in range(12)]
    assert [cards.index(picture) for picture in pictures] == sorted(cards.index(picture) for picture in pictures)
    assert cards.index('"Пойти проверить"') < cards.index('"Обойти лавку"') < cards.index('"Заглянуть в окно"') < cards.index(pictures[0])
    assert cards.count('"Уйти":') == 11
    assert cards.count("active_thread.advance()") == 1
    assert cards.index('"Закончить наблюдение и вернуться на рынок"') < cards.index("active_thread.advance()")
    assert "change_social" not in cards
    assert "jump MarketPlace" not in cards
    for forbidden in ("QueuePagedPanelText", "main_ui_set_action_panel", "main_ui_runtime.action_items", "while True"):
        assert forbidden not in cards


def test_hints_and_schedules_do_not_own_another_progress_state():
    content = source(CARDS)
    for name in ("story_clara_education_whispers", "story_clara_education_absence"):
        hint = label_block(content, name)
        assert "advance()" not in hint
        assert "set_var" not in hint
    assert "start_hour=_education_event.hour[0]" in content
    assert "weekdays=list(_education_event.day)" in content
    assert 'location=_education_location' in content
    assert '"WineStoreBasement"' in content
    assert "default " not in content


def test_card_assets_exist():
    for name in ["basement_window_night.png"] + ["cardplay%d.jpg" % n for n in range(12)]:
        assert (ROOT / "game/images/clara/education" / name).is_file()


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
