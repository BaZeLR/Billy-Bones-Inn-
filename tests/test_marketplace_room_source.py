    assert "images/market/LocMarketPlaceClosed.jpg" not in source    assert "images/market/LocMarketPlaceClosed.jpg" not in source    assert "images/market/LocMarketPlaceClosed.jpg" not in sourcefrom pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_marketplace_schedule_uses_clock_hours_not_time_slots():
    source = read_rel("game/Town/Market/MarketPlace.rpy")
    room_block = source.split("MarketPlaceRoom = Room(", 1)[1].split("default BlindPirateMarketEventSeen", 1)[0]

    assert 'schedule=RoomSchedule(' in room_block
    assert 'start="07:00"' in room_block
    assert 'end="17:59"' in room_block
    assert "time_slots=" not in room_block
    assert "int(clock_minutes" not in source
    assert "MarketPlaceRoom.is_open(week, time)" not in source
    assert "_market_room.is_open(week, time)" not in source


def test_marketplace_room_does_not_duplicate_exits_as_objects():
    source = read_rel("game/Town/Market/MarketPlace.rpy")
    room_block = source.split("MarketPlaceRoom = Room(", 1)[1].split("default BlindPirateMarketEventSeen", 1)[0]

    assert 'object_id="market_stalls"' in room_block
    for duplicate_route in ("grocery_route", "wine_route", "guard_office", "hunter_club_route"):
        assert duplicate_route not in room_block


def test_marketplace_uses_direct_picture_paths_without_fallback_helper():
    source = read_rel("game/Town/Market/MarketPlace.rpy")

    assert 'MARKETPLACE_CLOSED_PICTURE = "images/general/closedVenue default.png"' in source
    assert "def marketplace_closed_picture" not in source
    assert "images/general/LocMarketPlaceClosed.jpg" not in source
    assert "vscene scene_image" in source


def test_marketplace_has_no_ui_wait_loop_or_special_refresh_branch():
    market_source = read_rel("game/Town/Market/MarketPlace.rpy")
    layout_source = read_rel("game/Utilities/General/Screens/main_layout.rpy")

    assert "while _market_ui_return is None" not in market_source
    assert "marketplace_action_items" not in market_source
    assert "marketplace_int" not in market_source
    assert "marketplace_closed_action_items" not in market_source
    assert "label MarketPlaceBuildActions" not in market_source
    assert 'room_code == "MarketPlace"' not in layout_source


def test_marketplace_mongol_presence_is_conditional_schedule_not_default_location():
    market_source = read_rel("game/Town/Market/MarketPlace.rpy")
    secondary_source = read_rel("game/NPC/Secondary/InitSecondaryNPC.rpy")
    people_source = read_rel("game/Utilities/General/NPC/PeopleRuntime.rpy")
    schedule_source = read_rel("game/Utilities/General/NPC/NPCScheduleModel.rpy")

    mongol_block = secondary_source.split('"mongol": {', 1)[1].split('"zimmer": {', 1)[0]
    assert '"location": ""' in mongol_block
    assert '"mongol": ""' in people_source
    assert 'npc_schedule_set("mongol"' in market_source
    assert 'condition=marketplace_mongol_visible' in market_source
    assert 'if key.lower() == "mongol":' in schedule_source
    assert 'return "MarketPlace" if marketplace_mongol_visible() else ""' in schedule_source
    assert "procedural_randint(1, 4" in market_source
    assert 'MongolVar.get("MarketRollDay", -1) or -1' not in market_source
    assert "renpy.random.randint(1, 4)" not in market_source
