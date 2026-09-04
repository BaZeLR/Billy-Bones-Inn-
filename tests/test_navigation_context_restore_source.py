from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def label_block(source, label_name):
    return source.split("label %s" % label_name, 1)[1].split("\nlabel ", 1)[0]


def test_port_lane_action_owns_its_scene_and_restores_the_calling_room_context():
    source = read("game/Town/PortStreets.rpy")
    block = label_block(source, "PortStreetsExamineLanes:")

    assert '$ main_ui_begin_native_scene_state("Осмотр переулков")' in block
    assert 'menu:\n        "Назад":' in block
    assert "$ main_ui_end_native_scene_state()" in block
    assert "rooms.current.build_action_items()" not in block
    assert "jump PortStreets" not in block


def test_church_attendee_actions_restore_the_attendee_menu_picture_and_text():
    source = read("game/Town/Church/Church.rpy")

    for label_name in (
        "ChurchServiceMother:",
        "ChurchServiceSisters:",
        "ChurchServiceLegare:",
        "ChurchServiceBlanken:",
    ):
        block = label_block(source, label_name)
        assert "main_ui_begin_native_scene_state(" in block
        assert 'menu:\n        "Назад":' in block
        assert "$ main_ui_end_native_scene_state()" in block
        assert "call ChurchServiceMenu(False)" not in block

    becky_talk = label_block(source, "becky_church_talk:")
    assert '$ main_ui_begin_native_scene_state("Разговор с отцом Герхардом")' in becky_talk
    assert 'menu:\n        "Назад":' in becky_talk
    assert "$ main_ui_end_native_scene_state()" in becky_talk
    assert "jump Church" not in becky_talk


def test_backyard_object_back_restores_dynamic_room_picture_and_text():
    source = read("game/Inn/Backyard.rpy")
    block = label_block(source, 'BackyardObjectMenu(object_id="", display_text=""):')

    back = block.split('MenuItem("Назад", [', 1)[1].split("]))", 1)[0]
    assert 'SetField(scene_runtime, "picture", backyard_dynamic_picture())' in back
    assert 'SetField(scene_runtime, "text", backyard_dynamic_text())' in back
    assert 'SetField(scene_runtime, "location_text", backyard_dynamic_text())' in back


def test_empty_church_walk_is_a_returnable_scene_that_restores_the_church_context():
    source = read("game/Town/Church/ChurchAfterCermon.rpy")
    block = label_block(source, "ChurchAfterCermon(entry_arg=0):")

    assert '$ main_ui_begin_native_scene_state("Обход собора")' in block
    assert 'if _church_after_event is not None:\n        $ main_ui_end_native_scene_state()' in block
    assert 'menu:\n        "Назад":' in block
    assert "$ main_ui_end_native_scene_state()" in block
    assert '"[scene_runtime.text]"' not in block
    assert "jump Church" not in block


def test_object_menus_that_replace_room_pictures_restore_their_room_projection():
    cases = (
        ("game/Forest/Forest.rpy", "ForestObjectMenu", "forest_pick_background()"),
        ("game/Forest/Forest.rpy", "ForestSpawnedItemMenu", "forest_pick_background()"),
        ("game/Forest/Forest.rpy", "ForestSubroomSpawnedItemMenu", "rooms.current.bg_picture"),
        ("game/Inn/TavernAmandaRoom.rpy", "tavern_amanda_room_object_menu", "tavern_amanda_room_picture("),
        ("game/Inn/TavernAtic.rpy", "TavernAticObjectMenu", "attic_room_picture_path()"),
        ("game/Inn/TavernEmptyRoom.rpy", "TavernEmptyRoomObjectMenu", 'rooms.get("TavernEmptyRoom").bg_picture'),
        ("game/Inn/TavernKitchen.rpy", "TavernKitchenDepositMenu", "tavern_kitchen_picture()"),
        ("game/Inn/TavernKitchenCauldron001.rpy", "TavernKitchenCauldronMenu", "tavern_kitchen_picture()"),
        ("game/Inn/TavernKitchenHearth001.rpy", "TavernKitchenHearthMenu", "tavern_kitchen_picture()"),
        ("game/Inn/TavernMain.rpy", "TavernMainObjectMenu", "tavern_main_picture()"),
        ("game/Inn/TavernMelissaRoom.rpy", "TavernMelissaRoomObjectMenu", "tavern_melissa_room_picture()"),
        ("game/Inn/TavernMyRoom.rpy", "TavernMyRoomObjectMenu", "tavern_my_room_dynamic_picture()"),
        ("game/Inn/TavernSandraRoom.rpy", "TavernSandraRoomObjectMenu", "tavern_sandra_room_picture()"),
        ("game/Inn/TavernStable.rpy", "tavern_stable_object_menu", "tavern_stable_picture()"),
        ("game/Town/Arts/ArtisansQuarter.rpy", "ArtisansQuarterObjectMenu", 'rooms.get("ArtisansQuarter").bg_picture'),
        ("game/Town/Arts/Dress/DressShop.rpy", "DressShopObjectMenu", 'SetField(scene_runtime, "picture", "")'),
        ("game/Town/BeckyHome.rpy", "BeckyHomeObjectMenu", "becky_home_picture("),
        ("game/Town/CityGuard.rpy", "CityGuardShowPlacat", "city_guard_room_picture()"),
        ("game/Town/WineStore.rpy", "WineStoreObjectMenu", "wine_store_scene_picture()"),
    )

    for relative_path, label_name, picture_resolver in cases:
        block = label_block(read(relative_path), label_name)
        back = block.split('MenuItem("Назад", [', 1)[1]
        assert 'SetField(scene_runtime, "picture",' in back
        assert picture_resolver in back
        assert 'SetField(scene_runtime, "text",' in back
        assert 'SetField(scene_runtime, "location_text",' in back


def test_street_tavern_object_back_restores_the_authoritative_location_text():
    source = read("game/Town/StreetTavern.rpy")
    entry = label_block(source, "StreetTavern:")
    object_menu = label_block(source, "StreetTavernObjectMenu")
    back = object_menu.split('MenuItem("Назад", [', 1)[1].split("]))", 1)[0]

    assert "def street_tavern_location_text():" in source
    assert "$ scene_runtime.text = street_tavern_location_text()" in entry
    assert 'SetField(scene_runtime, "text", street_tavern_location_text())' in back
    assert 'SetField(scene_runtime, "location_text", street_tavern_location_text())' in back


def test_wine_store_back_consumes_one_shot_location_text_once():
    source = read("game/Town/WineStore.rpy")
    object_menu = label_block(source, "WineStoreObjectMenu")

    assert "$ _wine_return_text = wine_store_entry_text()" in object_menu
    assert object_menu.count("wine_store_entry_text()") == 1
    assert 'SetField(scene_runtime, "text", _wine_return_text)' in object_menu
    assert 'SetField(scene_runtime, "location_text", _wine_return_text)' in object_menu


def test_tavern_main_uses_one_picture_resolver_for_entry_and_object_return():
    source = read("game/Inn/TavernMain.rpy")
    entry = label_block(source, "TavernMain:")
    object_menu = label_block(source, 'TavernMainObjectMenu(object_id=""):')

    assert "def tavern_main_picture():" in source
    assert "$ scene_runtime.picture = tavern_main_picture()" in entry
    assert 'SetField(scene_runtime, "picture", tavern_main_picture())' in object_menu
