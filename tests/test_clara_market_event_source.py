from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_clara_market_follow_uses_event_thread_source_of_truth():
    market = _source(Path("game") / "Town" / "Market" / "MarketPlace.rpy")
    clara_init = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    events = _source(Path("game") / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy")

    assert "clara_market_story_label" not in market
    assert "clara_market_story_caption" not in market
    assert "def clara_market_story_label" not in clara_init
    assert "def clara_market_story_caption" not in clara_init
    assert "label story_clara_market_action_direct" not in events

    clara_thread = events.split('define claraThreadList = [', 1)[1].split('define mongolThreadList', 1)[0]
    assert '"story_clara_market_booklet_0"' in clara_thread
    assert '"MarketPlace"' in clara_thread
    assert '"enter"' in clara_thread
    assert "market_follow_failed_day" in clara_thread
    assert "market_follow_failed_hour" in clara_thread
    assert "market_follow_failed_time" not in clara_thread
    assert '"story_clara_market_booklet_1"' not in clara_thread
    assert "ClaraMarketFollowExtraAdvance" not in events


def test_clara_market_follow_label_is_simple_repeat_until_success():
    events = _source(Path("game") / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy")
    follow = events.split("label story_clara_market_booklet_follow:", 1)[1].split("label story_clara_market_booklet_2_direct_follow:", 1)[0]

    assert "call story_clara_market_follow_cost" in follow
    assert "call story_clara_market_restore_room_result" in follow
    assert "if int(exploration or 0) < 80:" in follow
    assert 'ClaraVar["market_follow_failed_day"] = int(dayspassed or 0)' in follow
    assert 'ClaraVar["market_follow_failed_hour"] = int(hour or 0)' in follow
    assert 'ClaraVar["booklet_market_seen"] = 1' in follow
    assert "$ thread.advance()" in follow
    assert "story_thread_advance_current()" not in follow
    assert "advanceTo(" not in follow
    assert "effective_player_exploration" not in follow
    assert "call screen main_ui" not in follow
    assert 'MenuItem("Вернуться к рынку", Jump("MarketPlace"))' not in follow
    assert 'MenuItem("Тихо уйти", Jump("MarketPlace"))' not in follow
    assert "menu:" not in follow
    assert "ShowImageSeq(\"general\", \"\", \"LocMarketPlace\"" not in follow


def test_clara_market_ignore_prepares_state_without_self_loop():
    events = _source(Path("game") / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy")
    ignore = events.split("label story_clara_market_booklet_ignore:", 1)[1].split("label story_clara_market_booklet_follow:", 1)[0]

    assert "call story_clara_market_follow_cost" in ignore
    assert "call story_clara_market_restore_room_result" in ignore
    assert 'MenuItem("Вернуться к рынку", Jump("MarketPlace"))' not in ignore
    assert "current_action_items" not in ignore
    assert "menu:" not in ignore
    assert "call screen main_ui" not in ignore
    assert "jump MarketPlace" not in ignore
    assert "return" in ignore


def test_clara_market_follow_cost_spends_time_and_energy():
    events = _source(Path("game") / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy")
    cost = events.split("label story_clara_market_follow_cost:", 1)[1].split("label story_clara_market_restore_room_result:", 1)[0]
    restore = events.split("label story_clara_market_restore_room_result:", 1)[1].split("label story_clara_market_booklet_ignore:", 1)[0]

    assert "$ LastAdvancedMinutes = 30" in cost
    assert "$ calendar_v2.advance_minutes(30)" in cost
    assert 'player_state().change_stat("energy", -5)' in cost
    assert "call stat" in cost
    assert '$ CurrentRoom = MarketPlaceRoom' in restore
    assert '$ CurLoc = "MarketPlace"' in restore
    assert "call ReturnMainUISceneMode" in restore


def test_clara_market_intro_uses_main_ui_middle_action_panel():
    events = _source(Path("game") / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy")
    intro = events.split("label story_clara_market_booklet_0:", 1)[1].split("label story_clara_market_booklet_confront:", 1)[0]

    assert 'MenuItem("Проследить за Клариссой", Call("story_clara_market_booklet_follow"))' in intro
    assert 'MenuItem("Не вмешиваться", Call("story_clara_market_booklet_ignore"))' in intro
    assert "main_ui_event_overlay" not in intro
    assert "show screen main_ui" not in intro
    assert "current_action_items" in intro
    assert "call screen main_ui" in intro
    assert "menu:" not in intro
    assert "jump MarketPlace" in intro
    assert "ShowImageSeq(\"general\", \"\", \"LocMarketPlace\"" not in intro


def test_main_ui_keeps_standard_three_section_layout():
    layout = _source(Path("game") / "Utilities" / "General" / "Screens" / "main_layout.rpy")

    assert "main_ui_event_overlay" not in layout
    assert "modal True" in layout
    assert "use current_action_panel" in layout
    assert 'text "Персонажи" size 20' in layout
    assert 'str(UI_mode or "") != "event"' in layout
