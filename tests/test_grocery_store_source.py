from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GROCERY = ROOT / "game" / "Town" / "GroceryStore.rpy"
WINESTORE = ROOT / "game" / "Town" / "WineStore.rpy"
CHARACTER_HUB = ROOT / "game" / "Utilities" / "General" / "NPC" / "CharacterActionHub.rpy"
EDDIE_TALK_INIT = ROOT / "game" / "NPC" / "Secondary" / "InitEddieTalk.rpy"
EDDIE_TALK = ROOT / "game" / "NPC" / "Secondary" / "IntEddieTalk.rpy"
BECKY_TALK = ROOT / "game" / "NPC" / "Girls" / "Becky" / "IntBeckyTalk.rpy"


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def test_grocery_uses_merchant_picture_sequences_not_hunter_store():
    source = _source(GROCERY)

    assert 'bg_picture="images/general/butchers_street.png"' in source
    assert "images/general/hunter_store.jpg" not in source
    assert "grocery_store_grocer_picture" in source
    assert '"images/eddie/portraits/portrait_%s.png"' in source
    assert '"images/becky/portraits/portrait_%s.png"' in source


def test_grocery_merchant_state_is_room_custom_properties_not_grocer_global():
    source = _source(GROCERY)

    assert '"first_visit_seen": False' in source
    assert '"current_grocer_id": ""' in source
    assert '"current_grocer_name": "продавец"' in source
    assert "GrocerName" not in source
    assert "label GroceryStoreBuildActions" not in source
    assert "while _grocery_ui_return is None" not in source


def test_grocery_visible_npc_is_merchant_until_known():
    hub_source = _source(CHARACTER_HUB)
    grocery_source = _source(GROCERY)

    assert 'room_key == "GroceryStore" and key in ("eddie", "becky", "inga")' in hub_source
    assert 'data["unknown_name"] = "Торговец"' in hub_source
    assert 'data["title"] = "Торговец"' in hub_source
    assert 'str(grocer_data.get("title", "") or "Торговец")' in grocery_source


def test_grocery_provision_object_uses_room_owned_action_menu_state():
    source = _source(GROCERY)

    assert 'object_id="food_stock"' in source
    assert 'ObjectAction(action_id="buy_provisions", label="Купить провизию", hook="call", target="GroceryStoreBuyStockMenu"' in source
    assert "def grocery_store_open_object_menu_state" in source
    assert "def grocery_store_show_object_text_state" in source
    assert "Function(grocery_store_open_object_menu_state" in source
    assert "Function(grocery_store_show_object_text_state" in source
    assert "items.extend(GroceryStoreRoom.build_object_items())" not in source
    assert '"object_menu_label": "GroceryStoreObjectMenu"' not in source
    assert "label GroceryStoreObjectMenu" not in source
    assert "label GroceryStoreObjectText" not in source


def test_grocery_buy_stock_is_direct_room_flow():
    source = _source(GROCERY)
    buy_menu = source.split("label GroceryStoreBuyStockMenu", 1)[1].split("label GroceryStoreBuyStockApply", 1)[0]
    buy_apply = source.split("label GroceryStoreBuyStockApply", 1)[1].split("label GroceryStoreBuyFancyNightBowl", 1)[0]

    assert "label GroceryStoreBuyMenu" not in source
    assert "label GroceryStoreBuyApply" not in source
    assert 'Call("GroceryStoreBuyStockApply"' in buy_menu
    assert "call ReturnToMainUI" in buy_menu
    assert "$ productnum += int(add_amount or 0)" in buy_apply
    assert "$ money -= int(cost or 0)" in buy_apply
    assert "$ grocery_store_set_notice(MainTxt)" in buy_apply
    assert "jump GroceryStore" in buy_apply


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
        assert "current_action_title" in menu
        assert "current_action_items = [MenuItem(\"Ничего не покупать\"" in menu
        assert "call ReturnToMainUI" in menu

    assert "$ productnum += int(add_amount or 0)" in grocery_apply
    assert "$ winenum += int(add_amount or 0)" in wine_apply
    for apply_block, room_label, notice_fn in (
        (grocery_apply, "GroceryStore", "grocery_store_set_notice"),
        (wine_apply, "WineStore", "wine_store_set_notice"),
    ):
        assert "$ money -= int(cost or 0)" in apply_block
        assert "%s(MainTxt)" % notice_fn in apply_block
        assert "jump %s" % room_label in apply_block


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
    assert 'vscene "images/eddie/portraits/portrait_0.png"' not in eddie_source
    assert 'vscene "images/eddie/portraits/fingal.png"' not in eddie_source
    assert '"images/becky/portraits/portrait_1.png"' not in becky_source


def test_action_menu_preserves_custom_entity_data_for_talk_and_look():
    hub_source = _source(CHARACTER_HUB)

    assert "Function(NpcActionTalkState, npc_key, room_key, dict(normalized))" in hub_source
    assert "Function(NpcActionLookState, npc_key, room_key, dict(normalized))" in hub_source
