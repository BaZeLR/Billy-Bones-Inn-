from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_clara_market_follow_uses_event_thread_source_of_truth():
    market = _source(Path("game") / "Town" / "Market" / "MarketPlace.rpy")
    clara_init = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    events = _source(Path("game") / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy")
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")

    assert "clara_market_story_label" not in market
    assert "clara_market_story_caption" not in market
    assert "def clara_market_story_label" not in clara_init
    assert "def clara_market_story_caption" not in clara_init
    assert "label story_clara_market_action_direct" not in events
    assert "label story_clara_market_booklet_0:" not in events
    assert "label story_clara_market_booklet_0:" in labels

    clara_thread = events.split('define claraThreadList = [', 1)[1].split('define mongolThreadList', 1)[0]
    assert '"story_clara_market_booklet_0"' in clara_thread
    assert '"MarketPlace"' in clara_thread
    assert '"enter"' in clara_thread
    assert "market_follow_failed_day" in clara_thread
    assert "market_follow_failed_hour" in clara_thread
    assert "market_follow_failed_time" not in clara_thread
    assert '"story_clara_market_booklet_1"' not in clara_thread
    assert "ClaraMarketFollowExtraAdvance" not in events
    assert "ClaraMarketFollowExtraAdvance" not in labels


def test_clara_market_event_checks_are_explicit_tuple_conditions():
    clara_init = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    events = _source(Path("game") / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy")
    next_day = _source(Path("game") / "Utilities" / "Time" / "NextDay.rpy")
    clara_thread = events.split('LThreadData(0, "clara", "BookletMarket"', 1)[1].split('LThreadData(1, "clara", "PaintingsPath"', 1)[0]

    for helper_name in [
        "clara_market_visit_active",
        "clara_mongol_evening_market_active",
        "clara_market_daytime_roll_active",
        "clara_market_evening_roll_active",
    ]:
        assert f"def {helper_name}" not in clara_init
        assert helper_name not in clara_thread

    assert 'def prepare_daily_event_rolls(self):' in clara_init
    assert 'procedural_randint(1, 2, "clara_market_day_%s_%s"' in clara_init
    assert 'procedural_randint(1, 3, "clara_market_evening_%s_%s"' in clara_init
    assert "$ Clara.prepare_daily_event_rolls()" in next_day
    assert "#int(Clara.var.get('market_day_roll_day', -1) or -1) == int(dayspassed or 0)" in clara_thread
    assert "#int(Clara.var.get('market_day_roll', 0) or 0) == 1" in clara_thread
    assert "#int(Clara.var.get('market_evening_roll_day', -1) or -1) == int(dayspassed or 0)" in clara_thread
    assert "#int(Clara.var.get('market_evening_roll', 0) or 0) == 1" in clara_thread


def test_clara_paintings_events_use_event_checks_not_ready_helpers():
    events = _source(Path("game") / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy")
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraPaintingsThread.rpy")
    clara_talk = _source(Path("game") / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy")
    melissa_talk = _source(Path("game") / "NPC" / "Girls" / "Melissa" / "IntMelissaTalk.rpy")
    wine_store = _source(Path("game") / "Town" / "WineStore.rpy")
    tavern_main = _source(Path("game") / "Inn" / "TavernMain.rpy")
    church = _source(Path("game") / "Town" / "Church" / "Church.rpy")
    schedule_model = _source(Path("game") / "Utilities" / "General" / "NPC" / "NPCScheduleModel.rpy")

    forbidden = [
        "clara_paintings_melissa_question_ready",
        "clara_paintings_cellar_ready",
        "clara_paintings_comfort_ready",
        "clara_paintings_second_ask_ready",
        "clara_paintings_church_fiance_ready",
        "clara_paintings_commission_ready",
        "clara_paintings_commission_followup_ready",
        "clara_paintings_evening_peek_ready",
        "clara_paintings_confession_ready",
        "clara_paintings_murder_ready",
        "clara_paintings_tavern_caption",
        "clara_paintings_wine_caption",
        "clara_paintings_confession_schedule_active",
        "clara_paintings_evening_watch_schedule_active",
    ]
    combined = "\n".join([labels, clara_talk, melissa_talk, wine_store, tavern_main, church, schedule_model])
    for name in forbidden:
        assert name not in combined

    paintings_thread = events.split('LThreadData(1, "clara", "PaintingsPath"', 1)[1].split('LThreadData(2, "clara", "TavernVisit"', 1)[0]
    assert '"WineStore",\n            "clara_paintings",\n            3,' in paintings_thread
    assert 'story_event_available("WineStore", "clara_paintings")' in clara_talk
    assert 'story_event_available("talk_melissa", "clara_paintings")' in melissa_talk
    assert 'Call("checkTriggers", "talk_melissa", "clara_paintings", 0)' in melissa_talk
    assert 'Call("checkTriggers", "WineStore", "clara_paintings", 0)' in wine_store
    assert 'Call("checkTriggers", "TavernMain", "clara_paintings", 0)' in tavern_main
    assert 'call checkTriggers("Church", "clara_paintings", 0)' in church
    assert 'call preEvent("claraPaintingsPath")' not in labels


def test_clara_story_labels_use_thread_methods_directly():
    booklet = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    paintings = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraPaintingsThread.rpy")
    tavern = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraTavernVisitThread.rpy")
    combined = "\n".join([booklet, paintings, tavern])

    assert "story_thread_advance_current()" not in combined
    assert "$ thread.advance()" in combined
    assert "thread.abort()" in paintings
    assert "thread.advanceTo(" not in booklet


def test_clara_market_follow_label_is_simple_repeat_until_success():
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    follow = labels.split("label story_clara_market_booklet_follow:", 1)[1].split("label story_clara_market_booklet_confront:", 1)[0]

    assert "if int(exploration or 0) < 80:" in follow
    assert 'Clara.var["market_follow_failed_day"] = int(dayspassed or 0)' in follow
    assert 'Clara.var["market_follow_failed_hour"] = int(hour or 0)' in follow
    assert 'Clara.var["booklet_market_seen"] = 1' in follow
    assert "$ thread.advance()" in follow
    assert "story_thread_advance_current()" not in follow
    assert "advanceTo(" not in follow
    assert "effective_player_exploration" not in follow
    assert "vscene" in follow
    assert "menu:" in follow
    assert "\"[MainTxt]\"" in follow
    assert "call screen main_ui" not in follow
    assert "call story_clara_market_booklet" not in follow
    assert "jump story_clara_market_booklet_confront" in follow
    assert "jump story_clara_market_booklet_follow_success_leave" in follow
    assert "QueuePagedPanelText" not in follow
    assert "ShowImage" not in follow
    assert "Jump(\"MarketPlace\")" not in follow


def test_clara_market_ignore_prepares_state_without_self_loop():
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    ignore = labels.split("label story_clara_market_booklet_ignore:", 1)[1].split("label story_clara_market_booklet_follow:", 1)[0]

    assert "$ calendar_v2.advance_minutes(15)" in ignore
    assert 'Clara.var["market_follow_failed_day"] = int(dayspassed or 0)' in ignore
    assert "return True" in ignore
    assert 'MenuItem("Вернуться к рынку", Jump("MarketPlace"))' not in ignore
    assert "current_action_items" not in ignore
    assert "call screen main_ui" not in ignore
    assert "jump MarketPlace" not in ignore
    assert "ShowImage" not in ignore
    assert "QueuePagedPanelText" not in ignore
    assert "return" in ignore


def test_clara_market_time_costs_are_visible_at_consequence_points():
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")

    assert "label story_clara_market_booklet_follow_cost" not in labels
    assert "$ LastAdvancedMinutes = 30" in labels
    assert "$ calendar_v2.advance_minutes(30)" in labels
    assert "$ LastAdvancedMinutes = 15" in labels
    assert "$ calendar_v2.advance_minutes(15)" in labels
    assert 'player_state().change_stat("energy", -5)' in labels
    assert "call stat" in labels
    assert "label story_clara_market_restore_room_result" not in labels


def test_clara_market_intro_uses_authored_scene_text_and_menu_order():
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    intro = labels.split("label story_clara_market_booklet_0:", 1)[1].split("label story_clara_market_booklet_confront:", 1)[0]

    assert 'vscene "images/clara/market_day.png"' in intro
    assert '"[MainTxt]"' in intro
    assert "menu:" in intro
    assert '"Проследить за Клариссой":' in intro
    assert '"Не вмешиваться":' in intro
    assert "jump story_clara_market_booklet_follow" in intro
    assert "jump story_clara_market_booklet_ignore" in intro
    assert "call story_clara_market_booklet" not in intro
    assert 'Clara.var["market_intro_seen"] = 1' in intro
    assert "main_ui_event_overlay" not in intro
    assert "show screen main_ui" not in intro
    assert "current_action_items" not in intro
    assert "call screen main_ui" not in intro
    assert "jump MarketPlace" not in intro
    assert "ShowImage" not in intro
    assert "QueuePagedPanelText" not in intro
    assert "ShowImageSeq(\"general\", \"\", \"LocMarketPlace\"" not in intro

    assert intro.index('vscene "images/clara/market_day.png"') < intro.index('"[MainTxt]"') < intro.index("menu:")


def test_clara_market_thread_file_has_no_direct_wrappers_or_paged_panels():
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    clara_talk = _source(Path("game") / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy")
    city_guard = _source(Path("game") / "Town" / "CityGuard.rpy")
    stolyar = _source(Path("game") / "Town" / "StolyarWorkshop.rpy")
    hunter = _source(Path("game") / "Town" / "HunterClub.rpy")

    for forbidden in [
        "story_clara_market_booklet_wine_talk_direct",
        "story_clara_market_booklet_city_guard_direct",
        "story_clara_market_booklet_feed_mongol_direct",
        "story_clara_market_booklet_lockpicks_order_direct",
        "story_clara_market_booklet_release_mongol_direct",
        "QueuePagedPanelText",
        "call preEvent(\"claraBookletMarket\")",
        "current_action_items",
        "call screen main_ui",
        "call story_clara_market_booklet",
    ]:
        assert forbidden not in labels

    assert "ShowImage" not in labels
    assert "ClaraVar" not in labels
    assert "Clara.var" in labels
    assert 'Call("checkTriggers", "WineStore", "clara_talk", 0)' in clara_talk
    assert 'Call("checkTriggers", "CityGuard", "enter", 0)' in city_guard
    assert 'Call("checkTriggers", "StolyarWorkshop", "enter", 0)' in stolyar
    assert 'call checkTriggers("HunterClub", "overheard", 0)' in hunter


def test_main_ui_keeps_standard_three_section_layout():
    layout = _source(Path("game") / "Utilities" / "General" / "Screens" / "main_layout.rpy")

    assert "main_ui_event_overlay" not in layout
    assert "modal True" in layout
    assert "use current_action_panel" in layout
    assert 'text "Персонажи" size 20' in layout
    assert 'str(UI_mode or "") != "event"' in layout
