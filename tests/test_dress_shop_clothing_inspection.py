from pathlib import Path
from types import SimpleNamespace

from tests.test_tavern_renovations_runtime import _exec_definitions


ROOT = Path(__file__).resolve().parents[1]


def test_clothing_only_description_reads_current_layers_without_full_npc_profile():
    layers = {"top": "closed_top", "bottom": "long_skirt", "shoes": "simpleshoes"}

    def unexpected(*args):
        raise AssertionError("Full NPC inspection must not run")

    info = SimpleNamespace(
        wardrobe=SimpleNamespace(worn_condition_lines=lambda: ["платье в хорошем состоянии"]),
        clothing_layer=lambda slot: layers.get(slot, ""),
        layer_raised=lambda slot: False,
        sex_stat=lambda key, default=0: default,
        skin_description=unexpected, appearance_description=unexpected,
        tits_visible=unexpected, pussy_visible=unexpected, cum_state=unexpected,
    )
    namespace = {
        "people": SimpleNamespace(get_info=lambda key: info, get_data=lambda key: SimpleNamespace(
            cname="Аманда", fullname="Аманда", genitive="Аманды", description="Full NPC biography")),
        "people_normalize_id": lambda name: name.lower(),
        "DressPartDesc": {"closed_top": "закрытую блузку", "long_skirt": "длинную юбку"},
        "DressPartSlut": {}, "FullDressDesc": {},
        "_girls_desc_recent_barber_line": unexpected,
    }
    _exec_definitions("NPC/Girls/Common/GirlsDesc.rpy", {
        "_girls_desc_get", "_girls_desc_resolve_key", "_girls_desc_build_lines",
    }, namespace)
    describe = namespace["_girls_desc_build_lines"]
    assert describe("amanda", clothing_only=True) == [
        "Состояние одежды: платье в хорошем состоянии.",
        "Она одета в закрытую блузку.",
        "Также она одета в длинную юбку.",
        "На ее ногах простые башмаки.",
    ]
    layers["top"] = "another_top"
    namespace["DressPartDesc"]["another_top"] = "другую блузку"
    assert "Она одета в другую блузку." in describe("amanda", clothing_only=True)


def test_shopping_clothing_inspection_is_a_returnable_text_only_scene():
    source = (ROOT / "game/NPC/Girls/Common/GirlDressBuy.rpy").read_text(encoding="utf-8-sig")
    label = source.split('label GirlDressBuyClothing(GirlName=""):', 1)[1].split("label GirlDressBuyLeave", 1)[0]
    assert 'Call("GirlDressBuyClothing", girl_name)' in source
    assert 'Show("dress_shop_catalog_page", rack_type="female", girl_name=girl_name)' in source
    assert label.index("hide screen dress_shop_catalog_page") < label.index("main_ui_begin_native_scene_state")
    assert '_girls_desc_build_lines(GirlName, clothing_only=True)' in label
    assert 'menu:\n        "Назад":\n            pass' in label
    assert 'main_ui_end_native_scene_state()' in label
    assert 'renpy.set_screen_variable("catalog_page", _dress_clothing_page' in label
    for forbidden in ("scene black", "ShowImage", "vscene", "check_visibility", "wear_day_clothes", "jump DressShop"):
        assert forbidden not in label


def test_catalog_back_closes_the_list_without_consuming_the_shopping_visit():
    source = (ROOT / "game/Town/Arts/Dress/DressShop.rpy").read_text(encoding="utf-8-sig")
    back = source.split('textbutton "Назад":', 1)[1].split('textbutton "<":', 1)[0]
    assert 'id "dress_shop_catalog_back"' in back
    assert 'action Hide("dress_shop_catalog_page")' in back
    assert "GirlDressBuyLeave" not in back
    assert "Jump(" not in back
