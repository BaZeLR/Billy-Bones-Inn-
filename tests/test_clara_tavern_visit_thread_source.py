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
CLARA_SCHEDULE = PROJECT_ROOT / "game" / "NPC" / "Schedules" / "clara.json"
MELISSA_SCHEDULE = PROJECT_ROOT / "game" / "NPC" / "Schedules" / "melissa.json"
SCHEDULE_RULES = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "GameObjectTemplate.rpy"


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
    assert '"story_clara_tavern_protection_lessons_6"' in source
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
    clara_init = read(CLARA_INIT)
    schedule_rules = read(SCHEDULE_RULES)

    clara_block = source.split("# clara_tavern_visit", 1)[1].split("define eddieThreadList", 1)[0]
    assert "(12, 17)" in clara_block
    bar_2_time_line = clara_block.split('"story_clara_tavern_visit_bar_2"', 1)[1].splitlines()[1]
    assert "(12, 17)" in bar_2_time_line
    assert "(18, 22)" not in bar_2_time_line
    assert "(16, 22)" in clara_block
    assert "clock_minutes" not in clara_block
    assert "str(people.location('clara') or '') == 'TavernMain'" in source
    assert "str(people.location('melissa') or '') == 'TavernMain'" in source
    assert "str(people.location('clara') or '') == 'TavernMelissaRoom'" in source
    assert "str(people.location('melissa') or '') == 'TavernMelissaRoom'" in source
    assert "Clara.var.get('tavern_visit_bar_0_seen'" not in source
    assert "bool(Melissa.drawings_booklet_read)" in source
    assert "bool(Melissa.drawings_booklet_left)" in source
    assert "player.item_count('melissa_drawings_booklet_001')" in source
    assert "calendar_v2.advance_minutes(45)" in labels
    assert "event_runtime.active_thread.advance()" in labels
    assert "Clara.sync_clara_maps()" not in labels
    assert "Clara.change_social(" in labels
    assert "def tavern_visit_active(self):" in clara_init
    assert "return ((current_game_day() + week_value) % 4) == 0" in clara_init
    assert "def clara_tavern_visit_active" not in clara_init
    assert "def clara_melissa_visit_active" not in clara_init
    assert "return bool(Clara.tavern_visit_active())" in schedule_rules
    for schedule_path in (CLARA_SCHEDULE, MELISSA_SCHEDULE):
        schedule = read(schedule_path)
        assert '"rule": "clara_tavern_visit"' in schedule
        assert '"location": "TavernMain"' in schedule
        assert '"start": "12:00"' in schedule
        assert '"end": "17:59"' in schedule


def test_room_files_no_longer_own_clara_visit_state():
    tavern_main = read(TAVERN_MAIN)
    tavern_bar = read(TAVERN_BAR)
    melissa_room = read(MELISSA_ROOM)

    assert "def tavern_main_register_clara_melissa_visit" not in tavern_main
    assert "tavern_melissa_visit_count" not in tavern_main
    assert "story_event_available(\"TavernMain\", \"clara_tavern_visit\")" not in tavern_main
    assert "checkTriggers\", \"TavernMain\", \"clara_tavern_visit\"" not in tavern_main
    assert "story_event_available(\"TavernMain\", \"clara_tavern_visit\")" in tavern_bar
    assert "checkTriggers(\"TavernMain\", \"clara_tavern_visit\", 0)" in tavern_bar

    assert "tavern_melissa_room_clara_scene_paths" not in melissa_room
    assert "tavern_melissa_room_clara_visit_active" not in melissa_room
    assert "tavern_melissa_room_locked_from_inside" not in melissa_room
    assert "tavern_melissa_room_register_clara_visit" not in melissa_room
    assert "story_event_available(\"TavernMelissaRoom\", \"clara_room_visit\")" in melissa_room
    assert "checkTriggers\", \"TavernMelissaRoom\", \"clara_room_visit\"" in melissa_room


def test_clara_thread_stage_replaces_visit_boolean_mirrors():
    init_source = read(CLARA_INIT)
    runtime_source = read(STORY_RUNTIME)
    label_source = read(CLARA_TAVERN_VISIT)
    board_source = read(STORY_BOARD)

    for mirror in (
        "tavern_visit_bar_0_seen",
        "tavern_visit_bar_1_seen",
        "tavern_visit_bar_2_seen",
        "melissa_room_visit_0_seen",
        "melissa_room_visit_1_seen",
        "melissa_room_visit_2_seen",
        "melissa_room_visit_count",
    ):
        assert mirror not in init_source
        assert mirror not in runtime_source
        assert mirror not in label_source

    assert 'LThreadData(2, "clara", "TavernVisit"' in runtime_source
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


def test_clara_visit_media_remains_until_native_continue_then_restores_room():
    labels = read(CLARA_TAVERN_VISIT)
    expected_pictures = (
        "images/clara/tavern_visit.png",
        "images/clara/tavern_visit_size.png",
        "images/clara/melissa_talk.png",
        "images/clara/melissa Pillow fight.png",
        "images/clara/melissa_doodleTimes.png",
        "images/clara/melissa_doodles.png",
    )

    assert labels.count("main_ui_begin_native_scene_state(") == 7
    assert labels.count("main_ui_end_native_scene_state()") == 7
    assert labels.count("show screen main_ui") == 7
    assert labels.count("menu:") == 9
    for picture in expected_pictures:
        assert f'vscene "{picture}"' in labels

    for block in labels.split("\nlabel story_clara_")[1:]:
        assert block.index("vscene ") < block.index("menu:") < block.index("main_ui_end_native_scene_state()") < block.index("return True")


def test_third_bar_talk_reveals_clara_and_melissa_as_close_friends():
    labels = read(CLARA_TAVERN_VISIT)
    third_bar = labels.split("label story_clara_tavern_visit_bar_2:", 1)[1].split("\n\nlabel ", 1)[0]

    assert "приглушенный смех" in third_bar
    assert "тихие стоны и звуки поцелуев" in third_bar
    assert "очень близкими подругами" in third_bar
    assert 'vscene "images/clara/melissa_talk.png"' in third_bar


def test_protection_lesson_updates_domain_owners_without_replacing_melissa_sex_rules():
    runtime = read(STORY_RUNTIME)
    labels = read(CLARA_TAVERN_VISIT)
    melissa_sex = read(PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "IntMelissaSex.rpy")

    assert "#int(threads['claraForestSofa'].num or 0) >= 1" in runtime
    assert 'Sandra.skills["waitress"]' in labels
    assert 'Amanda.skills["waitress"]' in labels
    assert 'Melissa.skills["waitress"]' in labels
    assert "player.tavern_management.visitors" in labels
    assert "clara_anal_training" not in runtime
    assert "clara_anal_training" not in labels
    assert "clara_anal_training" not in melissa_sex
    assert '"Войти сзади" if _hse_full_engine and player.intimacy.can_cum()' in melissa_sex
    assert 'threads["claraTavernVisit"].completed' in melissa_sex
