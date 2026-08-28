from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
GROCERY = ROOT / "game" / "Town" / "GroceryStore.rpy"
WINESTORE = ROOT / "game" / "Town" / "WineStore.rpy"
PEOPLE_RUNTIME = ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"
EDDIE_TALK_INIT = ROOT / "game" / "NPC" / "Secondary" / "InitEddieTalk.rpy"
EDDIE_TALK = ROOT / "game" / "NPC" / "Secondary" / "IntEddieTalk.rpy"
BECKY_TALK = ROOT / "game" / "NPC" / "Girls" / "Becky" / "IntBeckyTalk.rpy"
BECKY_TOPICS = ROOT / "game" / "NPC" / "Girls" / "Becky" / "IntBeckyTalkTopics.rpy"
BECKY_SHERWOOD = ROOT / "game" / "NPC" / "Girls" / "Becky" / "IntBeckyTalkSherwood.rpy"
BECKY_SCHEDULE = ROOT / "game" / "NPC" / "Schedules" / "becky.json"
GROCERY_ROOM_PICTURE = ROOT / "game" / "images" / "general" / "grocery_shop.png"
GROCERY_NPC_OWNERS = [
    ROOT / "game" / "NPC" / "Secondary" / "InitEddie.rpy",
    ROOT / "game" / "NPC" / "Girls" / "Becky" / "InitBecky.rpy",
    ROOT / "game" / "NPC" / "Girls" / "Inga" / "InitInga.rpy",
]


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def test_becky_staffs_grocery_store_until_the_store_closes():
    schedule = json.loads(_source(BECKY_SCHEDULE))
    entries = {row["label"]: row for row in schedule["entries"]}
    people_runtime = _source(PEOPLE_RUNTIME)

    assert entries["grocery_afternoon_shift"]["end"] == "17:59"
    assert entries["eddie_absent_grocery_cover"]["end"] == "17:59"
    save_sync = _source(ROOT / "game" / "TractirSaveSync.rpy")
    assert "config.after_load_callbacks.append(npc_schedule_after_load)" not in people_runtime
    assert "$ npc_schedule_after_load()" in save_sync


def test_grocery_uses_merchant_picture_sequences_not_hunter_store():
    source = _source(GROCERY)
    entry = source.split("label GroceryStore:", 1)[1].split("label GroceryStoreObjectMenu", 1)[0]
    main_text = source.split("def grocery_store_main_text():", 1)[1].split("def grocery_store_set_notice", 1)[0]

    assert 'bg_picture="images/general/grocery_shop.png"' in source
    assert GROCERY_ROOM_PICTURE.is_file()
    assert "images/general/hunter_store.jpg" not in source
    assert "$ scene_runtime.picture = _grocery_room.bg_picture" in entry
    assert "grocery_store_background_picture" not in source
    assert "grocery_store_eddie_picture()" not in entry
    assert "grocery_store_inga_picture()" not in entry
    assert "grocery_store_becky_picture()" not in entry
    assert "active_grocer" not in main_text
    assert '$ scene_runtime.picture = grocery_store_grocer_picture()' in source
    assert 'SetField(scene_runtime, "picture", rooms.get("GroceryStore").bg_picture)' in source
    assert "main_ui_restart_interaction" not in source
    assert "grocery_store_grocer_picture" in source
    assert '"images/eddie/portraits/portrait_0.png"' in source
    assert '"images/eddie/portraits/portrait_2.png"' in source
    assert '"images/becky/portraits/portrait_1.png"' in source
    assert '"images/becky/portraits/portrait_4.png"' in source


def test_grocery_merchant_state_comes_from_npc_schedule_not_room_mirror():
    source = _source(GROCERY)

    assert '"first_visit_seen": False' in source
    assert "def grocery_store_active_grocer_id" in source
    assert 'people.location("eddie")' in source
    assert 'people.location("inga")' in source
    assert 'people.location("becky")' in source
    assert "current_grocer_id" not in source
    assert "current_grocer_name" not in source
    assert "GrocerName" not in source
    assert "label GroceryStoreBuildActions" not in source
    assert "while _grocery_ui_return is None" not in source


def test_grocery_visible_npc_is_merchant_until_known():
    people_runtime = _source(PEOPLE_RUNTIME)
    grocery_source = _source(GROCERY)

    registry = people_runtime.split("class PeopleRegistry(object):", 1)[1].split(
        "def npc_schedule_clock_minute", 1
    )[0]
    assert 'room_key == "GroceryStore" and key in ("eddie", "becky", "inga")' not in registry
    assert "grocery_store_grocer_picture" not in registry
    for owner_path in GROCERY_NPC_OWNERS:
        owner_source = _source(owner_path)
        assert 'if str(where_id or "").strip() == "GroceryStore":' in owner_source
        assert "if not self.known:" in owner_source
        assert 'data["title"] = "Торговец"' in owner_source
        assert 'data["picture_path"] = grocery_store_grocer_picture(self.name)' in owner_source
    assert 'data = info.action_data("GroceryStore") if info is not None else {}' in grocery_source
    assert 'str(data.get("title", "") or "Торговец")' in grocery_source


def test_grocery_provision_object_uses_direct_object_labels():
    source = _source(GROCERY)

    assert 'object_id="food_stock"' in source
    assert 'ObjectAction(action_id="buy_provisions", label="Купить провизию", hook="call", target="GroceryStoreBuyStockMenu"' in source
    assert "def grocery_store_open_object_menu_state" not in source
    assert "def grocery_store_show_object_text_state" not in source
    assert "Function(grocery_store_open_object_menu_state" not in source
    assert "Function(grocery_store_show_object_text_state" not in source
    assert "items.extend(rooms.get(\"GroceryStore\").build_object_items())" not in source
    assert "def grocery_store_action_items():" in source
    assert "label GroceryStoreObjectMenu" in source
    assert "label GroceryStoreObjectText" in source


def test_grocery_buy_stock_is_direct_room_flow():
    source = _source(GROCERY)
    buy_menu = source.split("label GroceryStoreBuyStockMenu", 1)[1].split("label GroceryStoreBuyStockApply", 1)[0]
    buy_apply = source.split("label GroceryStoreBuyStockApply", 1)[1].split("label GroceryStoreBuyFancyNightBowl", 1)[0]

    assert "label GroceryStoreBuyMenu" not in source
    assert "label GroceryStoreBuyApply" not in source
    assert 'Call("GroceryStoreBuyStockApply"' in buy_menu
    assert 'MenuItem("Назад", Call("GroceryStoreObjectMenu", "food_stock", True))' in buy_menu
    assert "call screen main_ui" not in buy_menu
    assert "$ player.tavern_management.productnum += int(add_amount or 0)" in buy_apply
    assert "$ player.spend_money(int(cost or 0))" in buy_apply
    assert "$ grocery_store_set_notice(scene_runtime.text)" in buy_apply
    assert "jump GroceryStore" not in buy_apply
    assert "call GroceryStoreBuyStockMenu(True)" in buy_apply


def test_grocery_and_wine_store_use_same_stock_purchase_flow():
    grocery = _source(GROCERY)
    wine = _source(WINESTORE)

    assert 'target="GroceryStoreBuyStockMenu"' in grocery
    assert 'target="WineStoreBuyStockMenu"' in wine
    assert "label GroceryStoreBuyMenu" not in grocery
    assert "label WineStoreBuyMenu" not in wine
    assert "label GroceryStoreBuyApply" not in grocery
    assert "label WineStoreBuyApply" not in wine

    grocery_menu = grocery.split("label GroceryStoreBuyStockMenu", 1)[1].split("label GroceryStoreBuyStockApply", 1)[0]
    wine_menu = wine.split("label WineStoreBuyStockMenu", 1)[1].split("label WineStoreBuyStockApply", 1)[0]
    grocery_apply = grocery.split("label GroceryStoreBuyStockApply", 1)[1].split("label GroceryStoreBuyFancyNightBowl", 1)[0]
    wine_apply = wine.split("label WineStoreBuyStockApply", 1)[1]

    for menu in (grocery_menu, wine_menu):
        assert "main_ui_runtime.action_title" in menu
        assert "main_ui_runtime.action_items = [MenuItem(\"Ничего не покупать\"" in menu
        assert "call screen main_ui" not in menu

    assert "$ player.tavern_management.productnum += int(add_amount or 0)" in grocery_apply
    assert "$ player.tavern_management.winenum += int(add_amount or 0)" in wine_apply
    for apply_block, notice_fn in (
        (grocery_apply, "grocery_store_set_notice"),
        (wine_apply, "wine_store_set_notice"),
    ):
        assert "$ player.spend_money(int(cost or 0))" in apply_block
        assert "%s(scene_runtime.text)" % notice_fn in apply_block
    assert "jump GroceryStore" not in grocery_apply
    assert "call GroceryStoreBuyStockMenu(True)" in grocery_apply
    assert "jump WineStore" not in wine_apply
    assert 'call WineStoreObjectMenu("wine_stock", True)' in wine_apply


def test_grocery_talk_identifies_eddie_and_becky():
    eddie_source = _source(EDDIE_TALK_INIT)
    becky_source = _source(BECKY_TALK)

    assert "Сейчас за прилавком стоит Эдди" in eddie_source
    assert "старший сын вдовы Блэнкеншип" in eddie_source
    assert "За прилавком стоит сама Бекки Блэнкеншип" in becky_source


def test_grocery_talk_pictures_use_room_sequence_for_eddie_and_becky():
    eddie_source = _source(EDDIE_TALK)
    becky_source = _source(BECKY_TALK)

    assert 'vscene grocery_store_grocer_picture("eddie")' in eddie_source
    assert 'vscene grocery_store_grocer_picture("becky")' in becky_source
    assert eddie_source.index("main_ui_begin_talk_state") < eddie_source.index('vscene grocery_store_grocer_picture("eddie")')
    assert becky_source.index("main_ui_begin_talk_state") < becky_source.index('vscene grocery_store_grocer_picture("becky")')
    assert 'vscene "images/eddie/portraits/portrait_0.png"' not in eddie_source
    assert 'vscene "images/eddie/portraits/fingal.png"' not in eddie_source
    assert '"images/becky/portraits/portrait_1.png"' not in becky_source


def test_becky_talk_uses_native_menu_for_all_story_topics():
    source = _source(BECKY_TALK)

    assert "label IntBeckyTalkMenu:" not in source
    assert "while True:" not in source
    assert "jump IntBeckyTalkMenu" not in source
    assert "menu:" in source
    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert 'story_event_available("talk_becky", "becky_talk_inga1")' in source
    assert 'call story_becky_talk_eddie_after_sex_0(_becky_name)' in source
    assert 'call story_becky_sherwood_warned_0(_becky_name)' in source
    assert 'call checkTriggers("talk_becky", "becky_talk_inga1", 0)' in source
    assert 'Becky.robin_robbery_stage == 2' in source
    assert "$ main_ui_end_talk_state()" in source
    assert "jump IntBeckyTalk" not in _source(BECKY_TOPICS)
    assert "jump IntBeckyTalk" not in _source(BECKY_SHERWOOD)


def test_visible_npc_buttons_use_npc_owned_talk_data_directly():
    people_runtime = _source(PEOPLE_RUNTIME)
    layout_source = _source(ROOT / "game/Utilities/General/Screens/main_layout.rpy")

    registry = people_runtime.split("class PeopleRegistry(object):", 1)[1].split(
        "def npc_schedule_clock_minute", 1
    )[0]
    assert "return info.action_data(room_key)" in registry
    assert "def npc_action_data(" not in registry
    assert "npc_examine_label" not in registry
    assert "people.action_data_for_room(npc_key, current_location)" in layout_source
    assert "Call(_talk_label, *_talk_args)" in layout_source
    assert "call_in_new_context" not in registry
