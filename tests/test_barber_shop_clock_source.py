from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BARBER_SHOP = PROJECT_ROOT / "game" / "Town" / "Arts" / "BarberShop.rpy"


def test_barber_shop_open_hours_use_calendar_clock_not_display_slot():
    source = BARBER_SHOP.read_text(encoding="utf-8-sig")
    body = source.split("def barber_shop_is_open_at(weekday_value=None, time_value=None):", 1)[1].split("\n    def ", 1)[0]

    assert "calendar_v2.sync_state()" not in body
    assert "calendar_v2.week" in body
    assert "npc_schedule_clock_minute(time_value)" in body
    assert "12 * 60" in body
    assert "17 * 60 + 59" in body
    assert "8 * 60" in body
    assert "11 * 60 + 59" in body
    assert "time_slot" not in body
    assert "int(time" not in body
    assert "return barber_shop_is_open_at()" in source
