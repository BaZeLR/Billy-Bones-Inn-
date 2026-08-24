from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_shed_notice_and_discovery_are_room_owned():
    combined = "\n".join(
        source(path)
        for path in (
            "game/Inn/Shed.rpy",
            "game/Items/Resources/OldAxeItem.rpy",
            "game/Items/Resources/LumberItem.rpy",
            "game/Utilities/General/Common/Actions.rpy",
        )
    )
    assert 'rooms.get(\"Shed\").state["notice_text"]' in combined
    assert 'rooms.get(\"Shed\").state["notice_pending"]' in combined
    assert 'rooms.get(\"Shed\").state["bucket_found"]' in combined
    assert "default ShedNotice" not in combined
    assert "default ShedBucketFound" not in combined


def test_attic_hatch_discovery_is_tavern_room_owned():
    hatch = source("game/Inn/TavernMyRoomAtticHatch001.rpy")
    assert 'rooms.get("TavernMyRoom").state["attic_hatch_found"] = True' in hatch
    assert "default TavernMyRoomAtticHatchFound" not in hatch


def test_room_discovery_has_no_legacy_save_authority():
    migration = source("game/TractirSaveSync.rpy")
    for legacy_name in (
        "ShedNoticeText",
        "ShedNoticePending",
        "ShedBucketFound",
        "TavernMyRoomAtticHatchFound",
    ):
        assert legacy_name not in migration
