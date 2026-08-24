import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_legacy_wardrobe_maps_are_absent_from_live_game_code():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    legacy_names = (
        "dressdefault",
        "topdressdef",
        "bottomdressdef",
        "bradef",
        "pantiesdef",
        "legsdef",
        "shoesdef",
        "topdress",
        "bottomdress",
        "topraised",
        "bottomraised",
    )

    for name in legacy_names:
        assert not re.search(r"\b%s\b" % name, game_sources), name


def test_current_clothing_is_owned_by_girl_wardrobe_and_scene_state():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "def current_dress(self):" in runtime
    assert "def scene_dress(self):" in runtime
    assert "def clothing_layer(self, layer):" in runtime
    assert "def set_layer_raised(self, layer, value=1):" in runtime
    assert "def remove_clothing_layer(self, layer):" in runtime


def test_underwear_mutations_do_not_publish_a_compatibility_mirror():
    sources = "\n".join(
        (ROOT / path).read_text(encoding="utf-8-sig")
        for path in (
            "game/NPC/Girls/Amanda/InitAmanda.rpy",
            "game/NPC/Girls/Amanda/IntAmandaDressChange.rpy",
            "game/NPC/Girls/Liza/IntLizaDressChange.rpy",
        )
    )

    assert "publish_wardrobe_state" not in sources


def test_scene_dress_has_one_base_implementation():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert runtime.count("def scene_dress(self):") == 1
