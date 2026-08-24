from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_fight_and_hunt_use_direct_initialized_owners():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    assert "default fight = FightInfo()" in runtime
    assert "default hunt = HuntInfo()" in runtime
    assert "fight_info()" not in runtime
    assert "hunt_info()" not in runtime
    assert "default Fight" not in runtime
    assert "default Hunt" not in runtime


def test_legacy_combat_singletons_cannot_overwrite_canonical_owners_after_load():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    assert '"Fight"' not in migration
    assert '"Hunt"' not in migration
    assert "tractir_save_migrate_combat_singletons" not in migration
