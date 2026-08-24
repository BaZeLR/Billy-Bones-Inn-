from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_vscene_media_state_has_one_runtime_owner():
    source = (ROOT / "game/01vscene.rpy").read_text(encoding="utf-8-sig")
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert "class SceneRuntimeState(object):" in source
    assert "default scene_runtime = SceneRuntimeState()" in source
    for field in ("movie", "fullscreen", "controller_from_timer"):
        assert f"scene_runtime.{field}" in source
    assert "default sceneMovie" not in source
    assert "default sceneFullScreen" not in source
    assert "vcFromTimer" not in source
    assert "def updateSave_V31():" in migration
    assert 'globals().pop("sceneMovie", False)' in migration
    assert 'globals().pop("sceneFullScreen", False)' in migration


def test_media_resolver_reads_canonical_runtime_state_directly():
    source = (ROOT / "game/Utilities/General/Screens/ShowImage.rpy").read_text(encoding="utf-8-sig")

    assert "import renpy.store as store" not in source
    assert "store.time" not in source
    assert "store.location" not in source
    assert "getattr(store," not in source
    assert "calendar_v2.time_slot()" in source
    assert "_normalize_media_ref(location_code or rooms.current_code)" in source
    assert "MEDIA_ASSET_CASE_INDEX" in source
    assert "renpy.list_files()" in source
    assert "transfn" not in source
    assert "os.path.isfile" not in source


def test_legacy_fight_result_uses_project_rng_not_python_random():
    source = (ROOT / "game/Utilities/Fight/FightResult.rpy").read_text(encoding="utf-8-sig")

    assert "import random" not in source
    assert "random.randint" not in source
    assert "procedural_randint(" in source
    assert "calendar_v2.clock_minutes()" in source
