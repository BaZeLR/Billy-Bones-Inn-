from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_scene_runtime_is_the_only_live_picture_authority():
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    vscene = read_rel("game/01vscene.rpy")
    layout = read_rel("game/Utilities/General/Screens/main_layout.rpy")
    media = read_rel("game/Utilities/General/Screens/ShowImage.rpy")

    assert "scene_image" not in live_sources
    assert "_layout_last_picture" not in live_sources
    assert "scene_runtime.picture = scene_runtime.picture" not in live_sources
    assert 'self.picture = ""' in vscene
    assert 'scene_runtime.picture = str(filename or "")' in vscene
    assert '"picture": str(scene_runtime.picture or "")' in layout
    assert "explicit_picture = _normalize_media_ref(scene_runtime.picture)" in media


def test_old_scene_picture_names_are_one_way_save_migration_only():
    migration = read_rel("game/TractirSaveSync.rpy")

    assert "define currentVersion = 78" in migration
    assert "def updateSave_V34():" in migration
    assert 'globals().pop("_layout_last_picture", "")' in migration
    assert 'globals().pop("scene_image", "")' in migration
    assert "legacy_layout_present" in migration


def test_scene_runtime_is_the_only_live_text_authority():
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    vscene = read_rel("game/01vscene.rpy")
    migration = read_rel("game/TractirSaveSync.rpy")

    assert 'self.text = ""' in vscene
    assert 'self.location_text = ""' in vscene
    assert "scene_runtime.text" in live_sources
    assert "scene_runtime.location_text" in live_sources
    assert re.search(r"\bMainTxt\b", live_sources) is None
    assert re.search(r"\bCurLocDesc\b", live_sources) is None
    assert "def updateSave_V38():" in migration
    assert 'globals().pop("MainTxt"' in migration
    assert 'globals().pop("CurLocDesc"' in migration
