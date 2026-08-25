from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "game/Town/Market/MarketPlace.rpy"
THREADS = ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy"
BREAKFAST = ROOT / "game/Inn/TavernKitchenBreakfast.rpy"
PLAYER = ROOT / "game/Utilities/General/Player/Player.rpy"


def test_blind_pirate_uses_event_engine_and_authored_label():
    market = MARKET.read_text(encoding="utf-8")
    event = market.split("label story_city_blind_pirate_fall_0:", 1)[1].split(
        "label MarketPlaceApproachMongol", 1
    )[0]

    assert '$ findAvailableEvents(forced=True)' in market
    assert 'call checkTriggers("MarketPlace", "enter", 0)' in market
    assert market.index('call checkTriggers("MarketPlace", "enter", 0)') < market.index('$ scene_runtime.text = _market_room.descriptions[0].text')
    assert "label MarketPlaceBlindPirateEvent:" not in market
    assert "town_street" not in market
    assert "vscene " in event
    assert event.count('$ scene_runtime.text = ') == 4
    assert event.count('"[scene_runtime.text]"') == 4
    assert "_market_room.descriptions" not in event
    assert "scene_runtime.location_text" not in event
    assert "menu:" in event
    assert 'threads["cityBlindPirateFall"].advance()' in event
    assert "jump MarketPlace" not in event
    assert event.rstrip().endswith("return True")
    assert "main_ui_runtime.action_items" not in event
    assert "QueuePagedPanelText" not in event


def test_blind_pirate_thread_tuple_is_the_availability_authority():
    threads = THREADS.read_text(encoding="utf-8")
    block = threads.split('LThreadData(0, "city", "BlindPirateFall"', 1)[1].split(
        "RThreadData", 1
    )[0]

    assert '"story_city_blind_pirate_fall_0"' in block
    assert "marketplace_blind_pirate_event_ready" in block
    assert '"MarketPlace"' in block
    assert '"enter"' in block
    assert '"enter",\n            -100,' in block
    assert '"TavernKitchenBreakfastBlindPirateStory"' in block
    assert '"Breakfast"' in block
    assert '"market_talk"' in block

    clara_block = threads.split('LThreadData(0, "clara", "BookletMarket"', 1)[1].split(
        'LThreadData(1, "clara", "PaintingsPath"', 1
    )[0]
    assert '"enter",\n            0,' in clara_block


def test_blind_pirate_progress_is_one_chapter_value_not_boolean_mirrors():
    sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (MARKET, THREADS, BREAKFAST, PLAYER)
    )

    assert "blind_pirate_breakfast_pending" not in sources
    assert "blind_pirate_seen" not in sources
    assert "blind_pirate_stage" not in sources
    assert 'threads["cityBlindPirateFall"].num' in sources
    assert sources.count('threads["cityBlindPirateFall"].advance()') == 2
