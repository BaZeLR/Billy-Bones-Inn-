from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Screens" / "StoryThreadBoard.rpy"
MAIN_LAYOUT_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Screens" / "main_layout.rpy"
DEBUG_TOOLS_PATH = PROJECT_ROOT / "game" / "Utilities" / "General" / "Common" / "DebugTools.rpy"


def test_story_board_has_no_thread_mutation_controls():
    source = BOARD_PATH.read_text(encoding="utf-8-sig")

    assert "def story_board_force_enable" not in source
    assert "def story_board_abort" not in source
    assert "def story_board_reactivate" not in source
    assert "def story_board_reset" not in source
    assert "screen story_thread_control" not in source
    assert "forceEnable()" not in source
    assert ".abort()" not in source
    assert ".reset()" not in source


def test_story_board_is_read_only_for_normal_clicks():
    source = BOARD_PATH.read_text(encoding="utf-8-sig")
    main_layout = MAIN_LAYOUT_PATH.read_text(encoding="utf-8-sig")
    debug_tools = DEBUG_TOOLS_PATH.read_text(encoding="utf-8-sig")

    assert "renpy.call_replay" not in source
    assert "ToggleField(tinfo" not in source
    assert "action Show(\"story_thread_control\"" not in source
    assert "action Function(story_board_show_scene" not in source
    assert "action NullAction()" in source
    assert "def story_board_refresh" not in source
    assert 'on "show" action Function(story_board_refresh)' not in source
    assert "story_board_refresh" not in main_layout
    assert "story_board_refresh" not in debug_tools


def test_story_board_conditions_use_familylife_style_rows():
    source = BOARD_PATH.read_text(encoding="utf-8-sig")

    assert "def story_board_condition_lines" in source
    assert "rows.append(str(cond.show()).replace(\"[\", \"[[\"))" in source
    assert "for _cond_line in story_board_condition_lines(tinfo.data.conds):" in source
    assert "for _cond_line in story_board_condition_lines(evt.conds):" in source
    assert 'text "Checks:' not in source
    assert "def story_board_show_event_checks" not in source


def test_story_board_marks_active_threads_with_distinct_color():
    source = BOARD_PATH.read_text(encoding="utf-8-sig")

    assert '"active": "#38bdf8"' in source
    assert 'return STORY_BOARD_COLORS["active"]' in source
    assert "def story_board_thread_status_label" in source
    assert 'text "Status: " + story_board_thread_status_label(tinfo) color story_board_thread_color(tinfo)' in source
    assert "Thread colors: active blue" in source


def test_story_board_gives_the_thread_event_pane_more_readable_space():
    source = BOARD_PATH.read_text(encoding="utf-8-sig")

    assert "STORY_BOARD_LEFT_WIDTH = 1120" in source
    assert "STORY_BOARD_DETAIL_WIDTH = 800" in source
    assert "STORY_BOARD_THREAD_TITLE_WIDTH = 280" in source
    assert "STORY_BOARD_ROW_HEIGHT = 24" in source
    assert "STORY_BOARD_EMPTY_ROW_HEIGHT = 24" in source
    assert "STORY_BOARD_CELL_SIZE = 24" in source
    assert source.count("xpos STORY_BOARD_LEFT_WIDTH") == 2
    assert source.count("xsize STORY_BOARD_DETAIL_WIDTH") == 2
    assert "xsize STORY_BOARD_THREAD_TITLE_WIDTH ysize STORY_BOARD_ROW_HEIGHT" in source
    assert "xysize (STORY_BOARD_CELL_SIZE, STORY_BOARD_CELL_SIZE)" in source
    assert source.count("null height STORY_BOARD_EMPTY_ROW_HEIGHT") == 2
    assert "if _pos > 0:" in source
    assert "spacing STORY_BOARD_EMPTY_ROW_HEIGHT" not in source
