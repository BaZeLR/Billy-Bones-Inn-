from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_tavern_random_events_are_typed_definitions():
    source = read_rel("game/Inn/TavernRandomEvents.rpy")

    assert "class TavernWorkEventDefinition" in source
    assert "self.event = Event(" in source
    assert 'define tavern_work_events_by_type = {' in source

    for event_type in ("harrass", "work_mishap", "small_fight", "tavern_story", "theft", "big_fight", "mandatory"):
        assert f'"{event_type}"' in source

    for code in ("WaitressHarass", "CleaningHarass", "MelissaWaitressFall", "FightSmall", "AmandaLizaTalk", "WineForDance"):
        assert code in source


def test_tavern_random_events_are_wired_to_thread_runtime():
    runtime = read_rel("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    tavern = read_rel("game/Inn/TavernRandomEvents.rpy")
    main = read_rel("game/Inn/TavernMain.rpy")
    events = read_rel("game/Utilities/General/Events/events.rpy")

    assert "define tavernThreadList = [" in runtime
    assert 'RThreadData(0, "tavern", "WorkRandomEvents"' in runtime
    assert '"TavernWorkEventTrigger"' in runtime
    assert '"TavernMain"' in runtime and '"enter"' in runtime
    assert "+ tavernThreadList" in runtime
    assert "def tavern_work_planned_for" in tavern
    assert "label TavernWorkEventTrigger:" in tavern
    assert "tavern_work_planned_for('', 'TavernMain', calendar_v2.time_slot())" in runtime
    assert runtime.count('"TavernWorkEventTrigger", None, None, None') == 1
    assert 'call checkTriggers("TavernMain", "tavern_work", 0)' not in main
    assert 'self.repeatable = bool(evt[11]) if len(evt) > 11 else False' in events
    assert '"enter",\n            200,\n            True,' in runtime
    assert 'call RoomEnterEventGate(rooms.current_code, False)' in main
    assert "call DisplayTavernEventShort(time, 1)" not in main


def test_create_tavern_events_has_no_forced_waitress_fallback():
    source = read_rel("game/Inn/CreateTavernEvents.rpy")

    assert "$ tavern_work_build_daily_plan()" in source
    assert "call AmandaLegareDanceSequence" in source
    assert ("New" + "Events") not in source
    assert "if _total_random <= 0" not in source


def test_tavern_daily_plan_appends_random_selection():
    source = read_rel("game/Inn/TavernRandomEvents.rpy")

    assert "event_runtime.tavern_work_events.append(tavern_work_plan_row(selected, period))" in source
    assert "continue\n                event_runtime.tavern_work_events.append" not in source


def test_tavern_daily_plan_schedules_two_harassments_per_authored_job():
    source = read_rel("game/Inn/TavernRandomEvents.rpy")
    harassment_catalog = source.split('"harrass": [', 1)[1].split('    ],', 1)[0]

    assert 'if event_type == "harrass":' in source
    assert 'for event_def in candidates:' in source
    assert 'for period_offset in range(min(2, len(periods))):' in source
    assert 'periods[(first_period_index + period_offset) % len(periods)]' in source
    assert 'event_runtime.tavern_work_events.append(tavern_work_plan_row(event_def, period))' in source
    assert harassment_catalog.count('required_job="jobwaitress"') == 1
    assert harassment_catalog.count('required_job="jobcleaning"') == 1


def test_sunday_daily_plan_is_empty_and_cannot_reach_the_next_report():
    source = read_rel("game/Inn/TavernRandomEvents.rpy")
    plan = source.split("def tavern_work_build_daily_plan():", 1)[1].split("def tavern_work_pending_mandatory_code", 1)[0]

    assert "event_runtime.tavern_work_plan_day = current_day" in plan
    assert "if tavern_work_int(calendar_v2.week, 0) == 7:" in plan
    assert "return []" in plan


def test_tavern_work_events_respect_open_work_phase_and_present_assigned_staff():
    source = read_rel("game/Inn/TavernRandomEvents.rpy")

    assert 'periods=(2, 3, 4)' in source
    assert "if not player.tavern_management.isTavernOpen:" in source
    assert 'play_condition=tavern_work_melissa_waitress_fall_playable' in source
    assert 'str(people.location("melissa") or "") == "TavernMain"' in source
    assert "event_def.can_play(loc_key)" in source
    assert "event_def.can_play(room_key)" in source


def test_tavern_dispatch_uses_planned_event_pop():
    source = read_rel("game/Utilities/General/Common/DisplayTavernEventShort.rpy")

    assert "tavern_work_pop_planned_event(time_period, eyewitness > 0, rooms.current_code)" in source
    assert "def tavern_event_pop_code" not in source
    assert "call expression _event_target pass (eyewitness,)" in source
    assert '_event_pick.get("label", "")' in source
    assert '"WaitressHarass":' not in source
    assert '"CleaningHarass":' not in source
    assert '"FightSmall":' not in source
    assert '"AmandaLizaTalk":' not in source
    assert 'return _event_result' in source
    assert "CurEventCode" not in source
    assert "CurEventDescFin" not in source
    assert ("Events" + "Count") not in source
    assert "tavern_work_codes_for_period" in read_rel("game/Inn/TavernRandomEvents.rpy")


def test_tavern_mandatory_wine_uses_planned_list():
    wine_source = read_rel("game/Inn/EventWineForDance.rpy")
    kitchen_source = read_rel("game/Inn/TavernKitchen.rpy")

    assert 'tavern_work_pending_mandatory_code("WineForDance", "TavernKitchen")' in wine_source
    assert 'tavern_work_pop_mandatory_code("WineForDance", "TavernKitchen")' in wine_source
    assert 'return tavern_work_pending_mandatory_code("", "TavernKitchen")' in kitchen_source


def test_breakfast_tease_uses_step_picture_assets():
    kitchen_source = read_rel("game/Inn/TavernKitchenBreakfast.rpy")

    assert "def tavern_breakfast_tease_picture" in kitchen_source
    for picture_number in range(1, 7):
        assert '"images/amanda/breakfastTease/breakfastTease%s.jpg"' % picture_number in kitchen_source
    for picture_number in range(4):
        assert '"images/breakfast/melissa_breakfast/melissa_breakfast_%s.jpg"' % picture_number in kitchen_source
    assert "AMANDA_BREAKFAST_TEASE_PICTURES[picture_number]" in kitchen_source
    assert "MELISSA_BREAKFAST_TEASE_PICTURES[tease_tier]" in kitchen_source
    assert "vscene BREAKFAST_GIRLS_TEASE_PICTURE" in kitchen_source
    assert "horny_state = int(Amanda.arousal_value() or 0) >= 65" in kitchen_source
    assert "picture_number = 6 if horny_state else 5" in kitchen_source
    assert "picture_number = 4 if horny_state else 3" in kitchen_source
    assert "images/breakfast/amanda_breakfast" not in kitchen_source
    assert "MelissaStaticData.image_sequence(\"kitchen\", \"breakfast\")" not in kitchen_source
    assert not (ROOT / "game/images/breakfast/amanda_breakfast").exists()
    assert "tavern_breakfast_tease_picture(_tease_girl, _tease_tier)" in kitchen_source
