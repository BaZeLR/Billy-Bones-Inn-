from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_main_hud_calendar_rows_use_calendar_v2_data():
    source = (PROJECT_ROOT / "game" / "Utilities" / "General" / "Screens" / "main_layout.rpy").read_text(encoding="utf-8-sig")

    assert "$ _calendar_hud = calendar_v2.hud_data()" in source
    assert 'use main_ui_status_item("time", _calendar_hud["time_name_ru"])' in source
    assert 'use main_ui_status_item("weekday", _calendar_hud["week_name_ru"])' in source
    assert 'use main_ui_status_item("day", _calendar_hud["day"])' in source
    assert 'use main_ui_status_item("days in game", _calendar_hud["days_in_game"])' in source
    assert 'use main_ui_status_item("period", _calendar_hud["period_name_ru"])' in source
    assert 'use main_ui_status_item("cycle", _calendar_hud["cycle"])' in source

    hud_status_block = source.split('$ _calendar_hud = calendar_v2.hud_data()', 1)[1].split('use main_ui_status_item("money"', 1)[0]
    assert "calendar_time_slot_name_ru" not in hud_status_block
    assert 'main_ui_status_item("weekday", week_name)' not in hud_status_block
    assert 'main_ui_status_item("period", month_name)' not in hud_status_block
