from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_werecat_forest_search_keeps_the_persistent_main_ui_visible():
    source = (ROOT / "game/Forest/Forest.rpy").read_text(encoding="utf-8-sig")
    block = source.split("label WerecatForestSearch", 1)[1].split("label ForestSpawnedItemMenu", 1)[0]

    assert "vscene werecat_info_picture_path()" in block
    assert "hide screen main_ui" not in block
