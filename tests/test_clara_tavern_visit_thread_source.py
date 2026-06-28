from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STORY_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
CLARA_TAVERN_VISIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Clara" / "ClaraTavernVisitThread.rpy"
CLARA_BOOKLET = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy"
TAVERN_MAIN = PROJECT_ROOT / "game" / "Inn" / "TavernMain.rpy"
TAVERN_BAR = PROJECT_ROOT / "game" / "Inn" / "TavernMainBar001.rpy"
MELISSA_ROOM = PROJECT_ROOT / "game" / "Inn" / "TavernMelissaRoom.rpy"
CLARA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Clara" / "InitClara.rpy"
STORY_BOARD = PROJECT_ROOT / "game" / "Utilities" / "General" / "Screens" / "StoryThreadBoard.rpy"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def test_clara_tavern_visit_thread_is_clara_owned():
    source = read(STORY_RUNTIME)
    labels = read(CLARA_TAVERN_VISIT)

    assert '"clara", "TavernVisit"' in source
    assert '"story_clara_tavern_visit_bar_0"' in source
    assert '"story_clara_tavern_visit_bar_1"' in source
    assert '"story_clara_tavern_visit_bar_2"' in source
    assert '"story_clara_melissa_room_visit_0"' in source
    assert '"story_clara_melissa_room_visit_1"' in source
    assert '"story_clara_melissa_room_visit_2"' in source
    assert '"TavernMain",\n            "clara_tavern_visit"' in source
    assert '"TavernMelissaRoom",\n            "clara_room_visit"' in source
    assert "melissaClaraOverheard" not in source
    assert '"melissa", "ClaraOverheard"' not in source
    assert "label story_clara_tavern_visit_bar_0:" not in source
    assert "label story_clara_melissa_room_visit_0:" not in source
    assert "label story_clara_tavern_visit_bar_0:" in labels
    assert "label story_clara_melissa_room_visit_0:" in labels


def test_clara_visit_conditions_use_clock_schedule_and_classes():
    source = read(STORY_RUNTIME)
    labels = read(CLARA_TAVERN_VISIT)

    clara_block = source.split("# clara_tavern_visit", 1)[1].split("define eddieThreadList", 1)[0]
    assert "(12, 17)" in clara_block
    assert "(18, 22)" in clara_block
    assert "(16, 22)" in clara_block
    assert "clock_minutes" not in clara_block
    assert "str(getLocation('clara') or '') == 'TavernMain'" in source
    assert "str(getLocation('melissa') or '') == 'TavernMain'" in source
    assert "str(getLocation('clara') or '') == 'TavernMelissaRoom'" in source
    assert "str(getLocation('melissa') or '') == 'TavernMelissaRoom'" in source
    assert "Clara.var.get('tavern_visit_bar_0_seen'" in source
    assert "Melissa.var.get('drawings_booklet_read'" in source
    assert "calendar_v2.advance_minutes(45)" in labels
    assert "Clara.sync_clara_maps()" not in labels
    assert "Clara.change_social(" in labels


def test_room_files_no_longer_own_clara_visit_state():
    tavern_main = read(TAVERN_MAIN)
    tavern_bar = read(TAVERN_BAR)
    melissa_room = read(MELISSA_ROOM)

    assert "def tavern_main_register_clara_melissa_visit" not in tavern_main
    assert "tavern_melissa_visit_count" not in tavern_main
    assert "story_event_available(\"TavernMain\", \"clara_tavern_visit\")" in tavern_main
    assert "checkTriggers\", \"TavernMain\", \"clara_tavern_visit\"" in tavern_main
    assert "story_event_available(\"TavernMain\", \"clara_tavern_visit\")" in tavern_bar
    assert "checkTriggers(\"TavernMain\", \"clara_tavern_visit\", 0)" in tavern_bar

    assert "tavern_melissa_room_clara_scene_paths" not in melissa_room
    assert "tavern_melissa_room_clara_visit_active" not in melissa_room
    assert "tavern_melissa_room_locked_from_inside" not in melissa_room
    assert "tavern_melissa_room_register_clara_visit" not in melissa_room
    assert "story_event_available(\"TavernMelissaRoom\", \"clara_room_visit\")" in melissa_room
    assert "checkTriggers\", \"TavernMelissaRoom\", \"clara_room_visit\"" in melissa_room


def test_clara_defaults_and_story_board_include_new_thread():
    init_source = read(CLARA_INIT)
    board_source = read(STORY_BOARD)

    for flag in (
        "tavern_visit_bar_0_seen",
        "tavern_visit_bar_1_seen",
        "tavern_visit_bar_2_seen",
        "melissa_room_visit_0_seen",
        "melissa_room_visit_1_seen",
        "melissa_room_visit_2_seen",
        "melissa_room_visit_count",
    ):
        assert flag in init_source

    assert "story_clara_tavern_visit_bar_0" in board_source
    assert "story_clara_melissa_room_visit_0" in board_source
    assert "story_clara_market_booklet_0" in board_source
    assert "ClaraBookletMarketThread.rpy" in board_source
    assert '"clara_tavern_visit": "Clarissa tavern visit"' in board_source
    assert '"clara_room_visit": "Clarissa visits Melissa room"' in board_source
    assert "tavern_melissa_visit_count" not in init_source
    assert "tavern_melissa_overheard" not in init_source


def test_story_runtime_has_no_clara_authored_labels():
    runtime_source = read(STORY_RUNTIME)
    booklet_source = read(CLARA_BOOKLET)

    assert "label story_clara_market_booklet_0:" not in runtime_source
    assert "label story_clara_market_booklet_0:" in booklet_source
    assert "label story_clara_market_booklet_release_mongol:" in booklet_source
