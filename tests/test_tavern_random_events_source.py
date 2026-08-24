from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_tavern_random_events_are_typed_definitions():
    source = read_rel("game/Inn/TavernRandomEvents.rpy")

    assert "class TavernWorkEventDefinition" in source
    assert "self.event = Event(" in source
    assert 'define tavern_work_events_by_type = {' in source

    for event_type in ("harrass", "small_fight", "tavern_story", "theft", "big_fight", "mandatory"):
        assert f'"{event_type}"' in source

    for code in ("WaitressHarass", "CleaningHarass", "FightSmall", "AmandaLizaTalk", "WineForDance"):
        assert code in source


def test_tavern_random_events_are_wired_to_thread_runtime():
    runtime = read_rel("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    tavern = read_rel("game/Inn/TavernRandomEvents.rpy")
    main = read_rel("game/Inn/TavernMain.rpy")

    assert "define tavernThreadList = [" in runtime
    assert 'RThreadData(0, "tavern", "WorkRandomEvents"' in runtime
    assert '"TavernWorkEventTrigger"' in runtime
    assert '"TavernMain"' in runtime and '"tavern_work"' in runtime
    assert "+ tavernThreadList" in runtime
    assert "def tavern_work_planned_for" in tavern
    assert "label TavernWorkEventTrigger:" in tavern
    assert 'call checkTriggers("TavernMain", "tavern_work", 0)' in main
    assert "call DisplayTavernEventShort(time, 1)" not in main


def test_create_tavern_events_has_no_forced_waitress_fallback():
    source = read_rel("game/Inn/CreateTavernEvents.rpy")

    assert "$ tavern_work_build_daily_plan()" in source
    assert ("New" + "Events") not in source
    assert "if _total_random <= 0" not in source


def test_tavern_daily_plan_appends_random_selection():
    source = read_rel("game/Inn/TavernRandomEvents.rpy")

    assert "event_runtime.tavern_work_events.append(tavern_work_plan_row(selected, period))" in source
    assert "continue\n                event_runtime.tavern_work_events.append" not in source


def test_tavern_dispatch_uses_planned_event_pop():
    source = read_rel("game/Utilities/General/Common/DisplayTavernEventShort.rpy")

    assert "tavern_work_pop_planned_event(time_period, eyewitness > 0, rooms.current_code)" in source
    assert "def tavern_event_pop_code" not in source
    assert "call expression _event_target pass (eyewitness,)" in source
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
    assert '"images/breakfast/amanda_breakfast/amanda_tease_1.jpg"' in kitchen_source
    assert '"images/breakfast/amanda_breakfast/amanda_tease_3.jpg"' in kitchen_source
    assert '"images/breakfast/amanda_breakfast/amanda_tease_5.jpg"' in kitchen_source
    assert "tavern_breakfast_tease_picture(_tease_girl, _tease_tier)" in kitchen_source
