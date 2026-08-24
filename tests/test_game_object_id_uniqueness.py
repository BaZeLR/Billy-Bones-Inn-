import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"


def test_literal_game_object_ids_are_globally_unique():
    definitions = defaultdict(list)
    constructor = re.compile(r"\b(?:GameObject|GameItem)\s*\(")
    object_id = re.compile(r"\bobject_id\s*=\s*(['\"])([^'\"]+)\1")

    for path in GAME.rglob("*.rpy"):
        source = path.read_text(encoding="utf-8-sig")
        for match in constructor.finditer(source):
            block = source[match.start() : match.start() + 1800]
            id_match = object_id.search(block)
            if id_match is None:
                continue
            line = source.count("\n", 0, match.start()) + 1
            definitions[id_match.group(2)].append(f"{path.relative_to(ROOT)}:{line}")

    duplicates = {
        key: locations for key, locations in definitions.items() if len(locations) > 1
    }
    assert duplicates == {}, duplicates


def test_becky_rooms_reference_their_registered_object_owners():
    home = (GAME / "Town" / "BeckyHome.rpy").read_text(encoding="utf-8-sig")
    front = (GAME / "Town" / "BeckyHomeFront.rpy").read_text(encoding="utf-8-sig")
    objects = (GAME / "Town" / "BeckyHomeObjects.rpy").read_text(encoding="utf-8-sig")

    for object_id in (
        "becky_home_bed",
        "becky_home_chests",
        "becky_home_dinner_table",
    ):
        assert f'"{object_id}"' in home
        assert f'object_id="{object_id}"' in objects

    for object_id in ("becky_home_back_door", "becky_home_dark_corner"):
        assert f'"{object_id}"' not in front
        assert f'object_id="{object_id}"' not in objects

    assert "GameObject(" not in home
    assert "GameObject(" not in front
    assert "becky_homefront_peek_available" not in front
    assert "condition=becky_homefront_peek_available" not in objects
