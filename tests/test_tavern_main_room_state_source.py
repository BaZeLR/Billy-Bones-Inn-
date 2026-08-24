from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_NAMES = (
    "TavernClosed",
    "TavernEventOngoing",
    "GeorgettAvail",
    "LizaAvail",
    "TavernMainExtraDesc",
    "TavernMainGloryDesc",
    "TavernMainClientRoomGirl",
    "TavernMainBlockEvents",
)


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_tavern_main_runtime_state_is_owned_by_the_room():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    tavern = source("game/Inn/TavernMain.rpy")
    for field in (
        "client_room_girl",
    ):
        assert 'rooms.get(\"TavernMain\").state["%s"]' % field in runtime
        assert '"%s":' % field in tavern
    for derived_field in ("closed_text", "georgett_available", "liza_available", "glory_desc", "extra_desc", "block_events"):
        assert 'rooms.get("TavernMain").state["%s"]' % derived_field not in runtime
        assert 'rooms.get("TavernMain").state.get("%s"' % derived_field not in runtime
        assert '"%s":' % derived_field not in tavern
    assert 'rooms.get(\"TavernMain\").state["event_ongoing"]' not in runtime
    assert '"event_ongoing":' not in tavern
    for legacy_name in LEGACY_NAMES:
        assert "default %s" % legacy_name not in runtime
        assert legacy_name not in runtime


def test_tavern_main_has_no_legacy_save_authority():
    migration = source("game/TractirSaveSync.rpy")
    for legacy_name in LEGACY_NAMES:
        assert legacy_name not in migration
    assert "tractir_save_migrate_room_owned_state" not in migration
