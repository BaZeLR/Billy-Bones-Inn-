from functools import lru_cache
from pathlib import Path
from collections import UserDict
import pickle
import sys
import textwrap
import types


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy"


@lru_cache(maxsize=1)
def wardrobe_class():
    source = RUNTIME.read_text(encoding="utf-8-sig")
    start = source.index("    class GirlWardrobeState(object):")
    end = source.index("\n    class PeopleRegistry(object):", start)
    class_source = textwrap.dedent(source[start:end])

    module_name = "_tractir_wardrobe_test_runtime"
    module = types.ModuleType(module_name)
    module.people_to_int = lambda value, default=0: int(value if value is not None else default)
    module.DressTopPart = {
        "workdress": "worktop",
        "minidress": "minitop",
        "nightshirt": "nightshirttop",
    }
    module.DressBottomPart = {
        "workdress": "workbottom",
        "minidress": "minibottom",
        "nightshirt": "nightshirtbottom",
    }
    sys.modules[module_name] = module
    exec(class_source, module.__dict__)
    return module.GirlWardrobeState


def base_clothing():
    return {
        "day_dress": "workdress",
        "bra": "simplebra",
        "panties": "simplepanties",
        "legs": "blackstockings",
        "shoes": "simpleshoes",
    }


def test_day_night_strip_and_redress_keep_exact_layers_and_day_preference():
    wardrobe = wardrobe_class().from_base(base_clothing())

    assert wardrobe.current_dress() == "workdress"
    assert wardrobe.current_layers == {
        "top": "worktop",
        "bottom": "workbottom",
        "bra": "simplebra",
        "panties": "simplepanties",
        "legs": "blackstockings",
        "shoes": "simpleshoes",
    }

    wardrobe.wear_night(0)
    assert wardrobe.current_dress() == "nightshirt"
    assert wardrobe.current_layers == {
        "top": "nightshirttop",
        "bottom": "nightshirtbottom",
        "bra": "",
        "panties": "simplepanties",
        "legs": "",
        "shoes": "",
    }

    wardrobe.wear_night(1)
    assert wardrobe.current_dress() == ""
    assert wardrobe.layer("panties") == "simplepanties"
    assert not wardrobe.layer("top")
    assert not wardrobe.layer("bottom")
    assert not wardrobe.layer("bra")
    assert not wardrobe.layer("legs")
    assert not wardrobe.layer("shoes")

    wardrobe.wear_night(2)
    assert wardrobe.naked()
    assert wardrobe.day_dress == "workdress"
    assert wardrobe.preferred_underwear("panties") == "simplepanties"

    wardrobe.wear_night(0)
    assert wardrobe.current_dress() == "nightshirt"
    assert wardrobe.layer("panties") == "simplepanties"

    wardrobe.wear_day()
    wardrobe.set_raised("bottom", 1)
    wardrobe.remove("panties")
    assert wardrobe.current_dress() == "workdress"
    assert wardrobe.raised("bottom") == 1
    assert wardrobe.layer("panties") == ""
    assert wardrobe.preferred_underwear("panties") == "simplepanties"

    wardrobe.remove("bottom")
    assert wardrobe.current_dress() == ""
    assert wardrobe.raised("bottom") == 0
    assert wardrobe.day_dress == "workdress"

    wardrobe.wear_day()
    assert wardrobe.current_dress() == "workdress"
    assert wardrobe.layer("panties") == "simplepanties"


def test_owned_gift_and_later_choice_do_not_change_exact_current_wear():
    wardrobe = wardrobe_class().from_base(base_clothing())

    wardrobe.add_owned("minidress")
    assert wardrobe.owns("minidress")
    assert wardrobe.day_dress == "workdress"
    assert wardrobe.current_dress() == "workdress"

    wardrobe.set_day_dress("minidress")
    assert wardrobe.day_dress == "minidress"
    assert wardrobe.current_dress() == "workdress"

    wardrobe.set_day_underwear("legs", "redstockings", False)
    assert wardrobe.preferred_underwear("legs") == "redstockings"
    assert wardrobe.layer("legs") == "blackstockings"

    wardrobe.set_day_underwear("legs", "redstockings", True)
    assert wardrobe.layer("legs") == "redstockings"


def test_wardrobe_instances_do_not_share_mutable_state():
    first = wardrobe_class().from_base(base_clothing())
    second = wardrobe_class().from_base(base_clothing())

    first.add_owned("minidress")
    first.remove("panties")

    assert first.owns("minidress")
    assert not second.owns("minidress")
    assert first.layer("panties") == ""
    assert second.layer("panties") == "simplepanties"


def test_legacy_saved_dict_is_migrated_once_and_clothing_leaves_sex_state():
    legacy_wardrobe = UserDict({
        "owned": ["workdress", "simplebra", "simplepanties", "simpleshoes"],
        "gifted": ["minidress"],
        "current_dress": "workdress",
        "current_underwear": {
            "bra": "simplebra",
            "panties": "simplepanties",
            "legs": "",
            "shoes": "simpleshoes",
        },
    })
    legacy_sex = UserDict({
        "top_removed": 1,
        "bottom_removed": 0,
        "bra_removed": 1,
        "panties_removed": 0,
        "top_raised": 1,
        "bottom_raised": 1,
        "unrelated": 7,
    })

    wardrobe = wardrobe_class().from_saved(
        legacy_wardrobe,
        legacy_sex,
        base_clothing(),
    )

    assert wardrobe.owns("minidress")
    assert wardrobe.layer("top") == ""
    assert wardrobe.layer("bottom") == "workbottom"
    assert wardrobe.layer("bra") == ""
    assert wardrobe.layer("panties") == "simplepanties"
    assert wardrobe.raised("top") == 0
    assert wardrobe.raised("bottom") == 1
    assert dict(legacy_sex) == {"unrelated": 7}

    repaired = wardrobe_class().from_saved(wardrobe, legacy_sex, base_clothing())
    assert repaired is wardrobe
    assert repaired.layer("bottom") == "workbottom"


def test_wardrobe_state_is_pickle_safe_under_its_stable_class_name():
    wardrobe = wardrobe_class().from_base(base_clothing())
    wardrobe.wear_night(1)

    restored = pickle.loads(pickle.dumps(wardrobe))

    assert restored.__class__.__name__ == "GirlWardrobeState"
    assert restored.context == "night"
    assert restored.current_layers == wardrobe.current_layers
    assert restored.day_underwear == wardrobe.day_underwear
