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
    assert "#int(ClaraVar.get('market_day_roll_day', -1) or -1) == int(dayspassed or 0)" in clara_thread
    assert "#int(ClaraVar.get('market_day_roll', 0) or 0) == 1" in clara_thread
    assert "#int(ClaraVar.get('market_evening_roll_day', -1) or -1) == int(dayspassed or 0)" in clara_thread
    assert "#int(ClaraVar.get('market_evening_roll', 0) or 0) == 1" in clara_thread


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
    assert "#int(AskedToday.get('melissa', 0) or 0) == 0" in paintings_thread
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
    assert "thread.advanceTo(" in booklet


def test_clara_market_follow_label_is_simple_repeat_until_success():
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    follow = labels.split("label story_clara_market_booklet_follow:", 1)[1].split("label story_clara_market_booklet_2_direct_follow:", 1)[0]

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
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    ignore = labels.split("label story_clara_market_booklet_ignore:", 1)[1].split("label story_clara_market_booklet_follow:", 1)[0]

    assert "call story_clara_market_follow_cost" in ignore
    assert "call story_clara_market_restore_room_result" in ignore
    assert 'MenuItem("Вернуться к рынку", Jump("MarketPlace"))' not in ignore
    assert "current_action_items" not in ignore
    assert "menu:" not in ignore
    assert "call screen main_ui" not in ignore
    assert "jump MarketPlace" not in ignore
    assert "return" in ignore


def test_clara_market_follow_cost_spends_time_and_energy():
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    cost = labels.split("label story_clara_market_follow_cost:", 1)[1].split("label story_clara_market_restore_room_result:", 1)[0]
    restore = labels.split("label story_clara_market_restore_room_result:", 1)[1].split("label story_clara_market_booklet_ignore:", 1)[0]

    assert "$ LastAdvancedMinutes = 30" in cost
    assert "$ calendar_v2.advance_minutes(30)" in cost
    assert 'player_state().change_stat("energy", -5)' in cost
    assert "call stat" in cost
    assert '$ CurrentRoom = MarketPlaceRoom' in restore
    assert '$ CurLoc = "MarketPlace"' in restore
    assert "call ReturnMainUISceneMode" in restore


def test_clara_market_intro_uses_main_ui_middle_action_panel():
    labels = _source(Path("game") / "NPC" / "Girls" / "Clara" / "ClaraBookletMarketThread.rpy")
    intro = labels.split("label story_clara_market_booklet_0:", 1)[1].split("label story_clara_market_booklet_confront:", 1)[0]

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
