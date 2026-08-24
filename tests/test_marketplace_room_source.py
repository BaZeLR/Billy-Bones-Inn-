from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_marketplace_schedule_uses_clock_hours_not_time_slots():
    source = read_rel("game/Town/Market/MarketPlace.rpy")
    room_block = source.split("MarketPlaceRoomDefinition = Room(", 1)[1].split("label MarketPlace:", 1)[0]

    assert 'schedule=RoomSchedule(' in room_block
    assert 'start="06:00"' in room_block
    assert 'end="18:59"' in room_block
    assert "time_slots=" not in room_block
    assert "int(clock_minutes" not in source
    assert "rooms.get(\"MarketPlace\").is_open(week, time)" not in source
    assert "_market_room.is_open(week, time)" not in source


def test_marketplace_room_does_not_duplicate_exits_as_objects():
    source = read_rel("game/Town/Market/MarketPlace.rpy")
    room_block = source.split("MarketPlaceRoomDefinition = Room(", 1)[1].split("label MarketPlace:", 1)[0]

    assert "game_items=[]" in room_block
    assert 'object_id="market_stalls"' not in room_block
    for duplicate_route in ("grocery_route", "wine_route", "guard_office", "hunter_club_route"):
        assert duplicate_route not in room_block


def test_marketplace_uses_direct_picture_paths_without_fallback_helper():
    source = read_rel("game/Town/Market/MarketPlace.rpy")

    assert 'MARKETPLACE_CLOSED_PICTURE = "images/market/LocMarketPlaceClosed.jpg"' in source
    assert "def marketplace_closed_picture" not in source
    assert "images/general/LocMarketPlaceClosed.jpg" not in source
    assert "vscene scene_runtime.picture" in source


def test_marketplace_has_no_ui_wait_loop_or_special_refresh_branch():
    market_source = read_rel("game/Town/Market/MarketPlace.rpy")
    layout_source = read_rel("game/Utilities/General/Screens/main_layout.rpy")

    assert "while _market_ui_return is None" not in market_source
    assert "def marketplace_action_items():" in market_source
    assert "marketplace_int" not in market_source
    assert "marketplace_closed_action_items" not in market_source
    assert "label MarketPlaceBuildActions" not in market_source
    assert 'room_code == "MarketPlace"' not in layout_source


def test_marketplace_has_no_synthetic_object_menu():
    source = read_rel("game/Town/Market/MarketPlace.rpy")
    assert "label MarketPlaceObjectMenu" not in source
    assert "label MarketPlaceObjectText" not in source
    assert 'object_menu_label' not in source


def test_marketplace_mongol_presence_is_conditional_schedule_not_default_location():
    market_source = read_rel("game/Town/Market/MarketPlace.rpy")
    mongol_source = read_rel("game/NPC/Secondary/InitMongol.rpy")
    people_source = read_rel("game/Utilities/General/NPC/PeopleRuntime.rpy")
    schedule_source = read_rel("game/Utilities/General/NPC/PeopleRuntime.rpy")

    assert 'default_location=""' in mongol_source
    assert "def people_initial_location" not in people_source
    assert 'MongolStaticData.set_schedule([' in mongol_source
    assert 'NPCScheduleEntry(location="MarketPlace"' in mongol_source
    assert 'condition=marketplace_mongol_visible' in mongol_source
    assert 'def schedule_entry(self, person=""' in schedule_source
    assert "procedural_randint(1, 3" in market_source
    assert 'MongolVar.get("MarketRollDay", -1) or -1' not in market_source
    assert "renpy.random.randint(1, 4)" not in market_source
