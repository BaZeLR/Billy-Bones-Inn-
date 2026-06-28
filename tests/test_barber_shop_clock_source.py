from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BARBER_SHOP = PROJECT_ROOT / "game" / "Town" / "Arts" / "BarberShop.rpy"


def test_barber_shop_open_hours_use_calendar_clock_not_display_slot():
    source = BARBER_SHOP.read_text(encoding="utf-8-sig")
    body = source.split("def barber_shop_is_open():", 1)[1].split("\n    def ", 1)[0]

    assert "calendar_v2.sync_state()" in body
    assert "calendar_v2.week" in body
    assert "calendar_v2.hour" in body
    assert "calendar_v2.minute" in body
    assert "12 * 60" in body
    assert "17 * 60 + 59" in body
    assert "8 * 60" in body
    assert "11 * 60 + 59" in body
    assert "time_slot" not in body
    assert "int(time" not in body
