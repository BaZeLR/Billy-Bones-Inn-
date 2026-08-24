from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_NAMES = (
    "KidBirthPosobie",
    "SleepWakeHourOverride",
    "SleepWakeMinuteOverride",
    "BlockTimeAdvance",
)


def test_lifecycle_and_time_state_have_domain_owners():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    assert "player.economy.child_birth_benefit_notice" in runtime
    assert "player.sleep_wake_hour_override" in runtime
    assert "player.sleep_wake_minute_override" in runtime
    assert "calendar_v2.time_advance_blocked" in runtime
    for legacy_name in LEGACY_NAMES:
        assert legacy_name not in runtime


def test_lifecycle_and_time_have_no_legacy_save_authority():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    for legacy_name in LEGACY_NAMES:
        assert legacy_name not in migration
    assert "tractir_save_migrate_time_and_lifecycle_state" not in migration
