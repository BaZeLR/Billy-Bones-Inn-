from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return path.read_text(encoding="utf-8-sig")


def test_dress_order_runtime_has_one_owner():
    runtime = read(ROOT / "game/Town/Arts/Dress/DressShop.rpy")
    assert "class DressShopRuntimeState" in runtime
    assert 'self.produced = ""' in runtime
    assert 'self.buyer = ""' in runtime
    assert "default dress_shop = DressShopRuntimeState()" in runtime

    gameplay = "\n".join(
        read(path)
        for path in (ROOT / "game").rglob("*.rpy")
    )
    assert "DressProduced" not in gameplay
    assert "DressBuyer" not in gameplay
    assert "GirlDressBlock" not in gameplay


def test_tailor_order_consumers_use_dress_shop_owner():
    paths = [
        ROOT / "game/Utilities/General/Clothes/DressTry.rpy",
        ROOT / "game/Utilities/Time/NextDay.rpy",
        ROOT / "game/Town/Arts/Dress/DressShopDressItems.rpy",
        ROOT / "game/Town/Arts/Dress/DressShopWorktable001.rpy",
    ]
    combined = "\n".join(read(path) for path in paths)
    assert "dress_shop.produced" in combined
    assert "dress_shop.buyer" in combined


def test_catalog_page_reads_oop_items_without_menu_or_item_action_mirrors():
    shop = read(ROOT / "game/Town/Arts/Dress/DressShop.rpy")
    rack_items = read(ROOT / "game/Town/Arts/Dress/DressShopDressItems.rpy")
    catalog = shop.split('screen dress_shop_catalog_page(rack_type="male", girl_name=""):', 1)[1].split(
        "label DressShop:", 1
    )[0]

    assert 'dress_shop_catalog_items(_rack_type)' in catalog
    assert 'return list(dress_shop_rack_items(rack_type))' in shop
    assert "def dress_shop_populate_rack_contents" not in shop
    assert "dress_shop_populate_rack_contents()" not in shop
    assert 'getattr(_dress_item, "name", "")' in catalog
    assert 'getattr(_dress_item, "description", "")' in catalog
    assert 'getattr(_dress_item, "price", 0)' in catalog
    assert 'dress_shop_item_owned(_dress_item)' in catalog
    assert 'dress_shop_can_buy_item(_dress_item)' in catalog
    assert "def dress_shop_catalog_action_items" not in shop
    assert "DressShopFemaleBuyInfo" not in shop
    assert "def dress_shop_prepare_dress_item" not in rack_items
    assert "item_obj.actions =" not in rack_items
    assert "ObjectAction(" not in rack_items


def test_female_catalog_selects_through_existing_girl_agreement_flow():
    shop = read(ROOT / "game/Town/Arts/Dress/DressShop.rpy")
    buy = read(ROOT / "game/NPC/Girls/Common/GirlDressBuy.rpy")
    suggest = read(ROOT / "game/NPC/Girls/Common/GirlDressSuggest.rpy")
    catalog = shop.split('screen dress_shop_catalog_page(rack_type="male", girl_name=""):', 1)[1].split(
        "label DressShop:", 1
    )[0]
    actions = buy.split("def girl_dress_buy_actions(girl_name):", 1)[1].split(
        "label GirlDressBuy", 1
    )[0]

    assert 'id "dress_shop_catalog_offer_" + _dress_code' in catalog
    assert 'Call("GirlDressSuggest", _girl_name, _dress_code)' in catalog
    assert '_gds_has_dress_for_girl(_girl_name, _dress_code)' in catalog
    assert '_dress_price > int(player.economy.money or 0)' in catalog
    assert 'sensitive _female_can_offer' in catalog
    assert 'action ([Hide("dress_shop_catalog_page"), Call("GirlDressSuggest", _girl_name, _dress_code)] if _girl_name else NullAction())' in catalog
    assert catalog.index('textbutton "Выбрать":') < catalog.index('if not _girl_name:')
    assert 'show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)' in buy
    assert "FemaleDressCodes" not in actions
    assert 'Call("GirlDressSuggest"' not in actions
    assert 'get_game_item("dress_" + str(dress_code or ""))' in suggest
    assert "_gds_get_dict(" not in buy + suggest
    assert "DressObman" not in buy
    assert 'if str(dress_shop.produced or "") == str(DressToBuy or ""):' in suggest
    assert "jump ArtisansQuarter" in suggest
