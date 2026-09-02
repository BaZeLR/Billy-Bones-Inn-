from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_time_change_screen_defines_clock_targets_and_sets_clock_directly():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "TimeChangeMenu.rpy").read_text(encoding="utf-8-sig")

    assert "TIME_CHANGE_PERIOD_TARGETS" in source
    assert "calendar_v2.hud_data()" in source
    assert "def _time_minutes_to_hour(target_hour):" in source
    assert "current_minutes = (int(calendar_v2.hour or 0) % 24) * 60" in source
    assert "target_minutes = (int(target_hour or 0) % 24) * 60" in source
    assert 'Call("AdvanceTimeOnly", int(minutes_to_add or 0))' in source
    assert "label ApplyTimeSkip" not in source
    assert "jump expression return_loc" not in source
    assert "label ShowTimeChangeMenu" not in source
    assert "label HideTimeChangeMenu" not in source
    assert "calendar_v2.set_time_slot" not in source
    assert "screen time_change_panel():" in source
    assert "time_change_card_overlay" not in source
    assert "Hide(" not in source
    assert 'SetField(main_ui_runtime, "overlay", "")' in source

    assert "current_time = int(time or 0)" not in source
    assert "target_time" not in source
    assert "_time_label" not in source


def test_nextday_after_midnight_detection_uses_calendar_hour_not_old_slot():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay.rpy").read_text(encoding="utf-8-sig")
    body = source.split("def nextday_started_after_midnight():", 1)[1].split("label NextDay(", 1)[0]

    assert "int(calendar_v2.hour or 0) % 24" in body
    assert "return 0 <= current_hour < 6" in body
    assert "current_time = int(time or 0)" not in body
    assert "current_time == 4" not in body


def test_nextday_reports_completed_events_before_current_day_deliveries():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay.rpy").read_text(encoding="utf-8-sig")
    body = source.split("label NextDay(", 1)[1].split("default next_day_runtime", 1)[0]

    event_date = body.index("_nextday_event_day_number = int(calendar_v2.daysInGame or 0)")
    previous_day = body.index("_nextday_event_day_number = max(0, _nextday_event_day_number - 1)")
    event_summary = body.index("call DisplayTavernEventsSummary(_nextday_event_date")
    calendar_roll = body.index("calendar_v2.day += 1")
    new_day_events = body.index("call NextDay_NewDayEvents(retlocname)")
    delivery = body.index("# Handle dress delivery")

    assert event_date < previous_day < event_summary < calendar_roll < new_day_events < delivery
    assert "calendar_v2.day_number_to_parts(_nextday_event_day_number)" in body
    assert "player.appearance.replace_dress(dress_shop.produced, int(current_game_day()))" in body


def test_nextday_blocks_time_during_report_then_releases_it_before_room_return():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay.rpy").read_text(encoding="utf-8-sig")
    body = source.split("label NextDay(", 1)[1].split("default next_day_runtime", 1)[0]

    block_start = body.index("$ calendar_v2.time_advance_blocked = 1")
    report = body.index("call screen nextday_report_card_overlay")
    sleep_events = body.index('call checkTriggers("TavernMyRoom", "sleep", 0)')
    block_end = body.index("$ calendar_v2.time_advance_blocked = 0")
    room_return = body.index("jump expression _nextday_return_label")

    assert block_start < report < sleep_events < block_end < room_return
