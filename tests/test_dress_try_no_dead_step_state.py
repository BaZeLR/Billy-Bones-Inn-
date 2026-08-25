from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_dress_try_does_not_persist_unused_step_counter():
    source = (ROOT / "game/Utilities/General/Clothes/DressTry.rpy").read_text(encoding="utf-8-sig")
    assert "DressTryStep" not in source
    for label in ("DressTryUnderwear", "DressTryNakedThink", "DressTryNakedFantasy"):
        assert "label %s" % label in source


def test_dress_try_story_flow_uses_native_menus_and_returns_to_shop_owner():
    source = (ROOT / "game/Utilities/General/Clothes/DressTry.rpy").read_text(encoding="utf-8-sig")
    shop = (ROOT / "game/Town/Arts/Dress/DressShop.rpy").read_text(encoding="utf-8-sig")

    assert source.count("menu:") == 3
    assert "main_ui_runtime.action_items" not in source
    assert "DressShopRoomActions" not in source
    assert "label DressTryPayExtra:" not in source
    assert "label DressTryRefuseExtra:" not in source
    assert "jump DressShop" not in source
    assert 'call DressTry("You", _dress_code)' in shop
    assert "main_ui_runtime.action_items = rooms.get(\"DressShop\").build_object_items() + rooms.get(\"DressShop\").build_exit_items()" in shop
    assert "show screen main_ui" in shop
    assert '$ pregnancy_check("irma", "mouth", 1, "Вы")' in source


def test_dress_shop_has_no_refresh_label_or_recursive_room_reentry():
    shop = (ROOT / "game/Town/Arts/Dress/DressShop.rpy").read_text(encoding="utf-8-sig")
    events = (ROOT / "game/NPC/Girls/Irma/IrmaTailorEvents.rpy").read_text(encoding="utf-8-sig")
    talk = (ROOT / "game/NPC/Girls/Irma/IntIrmaTalk.rpy").read_text(encoding="utf-8-sig")

    assert "DressShopRoomActions" not in shop + events + talk
    assert "_dress_ui_return" not in shop
    assert "while _dress_ui_return" not in shop
    assert len(re.findall(r"while True:\n\s+call screen main_ui", shop)) == 2
    assert shop.count("call screen main_ui") == 2
    assert "dress_shop_male_catalog_overlay" not in shop
    assert "dress_shop_female_catalog_overlay" not in shop
    assert "def dress_shop_catalog_action_items(rack_type):" not in shop
    assert 'screen dress_shop_catalog_page(rack_type="male", girl_name=""):' in shop
    assert 'show screen dress_shop_catalog_page(rack_type=_rack_type)' in shop
    catalog = shop.split('screen dress_shop_catalog_page(rack_type="male", girl_name=""):', 1)[1].split(
        "label DressShop:", 1
    )[0]
    assert "viewport:" not in catalog
    assert 'SetScreenVariable("catalog_page"' in catalog
    assert 'for _dress_item in _page_items:' in catalog
    assert 'call ShowGirlCard("irma")' in talk


def test_girl_card_does_not_accept_fake_navigation_callback():
    source = (ROOT / "game/NPC/Girls/Common/GirlCard.rpy").read_text(encoding="utf-8-sig")

    assert 'label ShowGirlCard(girl_name=""):' in source
    assert "return_label" not in source
    assert "$ main_ui_runtime.action_items = []" in source
    assert 'menu:\n        "Назад":' in source
    assert "$ main_ui_end_card_state()" in source
    assert "label HideGirlCard:" in source
