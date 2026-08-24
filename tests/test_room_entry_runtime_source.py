from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_room_entry_pipeline_keeps_no_saved_cache_owner():
    pipeline = (ROOT / "game/Utilities/General/Common/RoomEnterPipeline.rpy").read_text(encoding="utf-8-sig")
    assert "class RoomEntryRuntimeState" not in pipeline
    assert "room_entry_runtime" not in pipeline
    for legacy_name in ("RoomEnterPresentIds", "RoomEnterLastRoom", "RoomEnterLastEventFired"):
        assert legacy_name not in pipeline


def test_room_entry_has_no_legacy_save_authority():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    for legacy_name in ("RoomEnterPresentIds", "RoomEnterLastRoom", "RoomEnterLastEventFired"):
        assert legacy_name not in migration
    assert "tractir_save_migrate_room_entry_runtime" not in migration
    assert 'globals().pop("room_entry_runtime", None)' in migration
