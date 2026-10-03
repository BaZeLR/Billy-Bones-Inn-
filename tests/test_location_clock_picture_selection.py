from pathlib import Path
from types import SimpleNamespace

import pytest

from tests.test_tavern_renovations_runtime import _exec_definitions


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("hour", [0, 5, 6, 9, 12, 16, 17, 18, 19, 23])
@pytest.mark.parametrize("pick", [0, 1, 2])
def test_artisans_picture_pool_keeps_day_and_night_assets_separate(hour, pick):
    namespace = {
        "calendar_v2": SimpleNamespace(hour=hour),
        "procedural_choice": lambda seq, key: seq[pick % len(seq)],
    }
    _exec_definitions("Town/Arts/ArtisansQuarter.rpy", {"artisans_quarter_picture"}, namespace)
    picture = namespace["artisans_quarter_picture"]()
    expected = (
        {"images/general/LocArtisansQuarter1.jpg", "images/general/LocArtisansQuarter2.jpg", "images/general/LocArtisansQuarter3.jpg"}
        if 6 <= hour < 18 else
        {"images/general/LocArtisansQuarter3.png", "images/general/LocArtisansQuarter4.jpg"}
    )
    assert picture in expected
    assert (ROOT / "game" / picture).is_file()


def test_artisans_entry_object_return_and_closed_workshop_share_picture_owner():
    quarter = (ROOT / "game/Town/Arts/ArtisansQuarter.rpy").read_text(encoding="utf-8-sig")
    workshop = (ROOT / "game/Town/StolyarWorkshop.rpy").read_text(encoding="utf-8-sig")
    assert '$ scene_runtime.picture = artisans_quarter_picture()' in quarter
    assert 'SetField(scene_runtime, "picture", artisans_quarter_picture())' in quarter
    assert workshop.count('$ scene_runtime.picture = artisans_quarter_picture()') == 2
    assert '"LocArtisansQuarter", 4' not in quarter + workshop


@pytest.mark.parametrize("hour", [0, 5, 6, 9, 12, 16, 17, 18, 23])
def test_closed_market_lighting_does_not_depend_on_sunday_or_open_hours(hour):
    source = (ROOT / "game/Town/Market/MarketPlace.rpy").read_text(encoding="utf-8-sig")
    closed = source.split('if int(calendar_v2.week or 0) == 7:', 1)[1].split('# Restore the room-owned scene', 1)[0]
    assignments = [line.strip().split(' = ', 1)[1] for line in closed.splitlines() if '$ scene_runtime.picture = ' in line]
    assert len(assignments) == 2
    namespace = {"calendar_v2": SimpleNamespace(hour=hour), "MARKETPLACE_CLOSED_PICTURE": "images/market/LocMarketPlaceClosed.jpg"}
    for expression in assignments:
        picture = eval(expression, namespace)
        assert picture == ("images/market/LocMarketPlace2.jpg" if 6 <= hour < 18 else namespace["MARKETPLACE_CLOSED_PICTURE"])
        assert (ROOT / "game" / picture).is_file()
    assert 'start="06:00"' in source and 'end="18:59"' in source
    assert 'Сегодня воскресенье и рынок закрыт.' in source
