from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_NAMES = (
    "NextDayReportTitle",
    "NextDayReportBody",
    "tractir_activated_achievements",
    "tractir_achieved",
    "tractir_endings",
    "tractir_progress_view",
    "TractirEndingTitle",
    "TractirEndingBody",
)
DEAD_CHECKPOINT_NAMES = (
    "_tractir_progress_revision",
    "_tractir_last_autosave_reason",
    "checkpoint_tractir_progress",
    "request_tractir_autosave",
    "mark_tractir_progress",
)


def test_reports_and_progress_have_aggregate_runtime_owners():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    assert "class NextDayRuntimeState" in runtime
    assert "default next_day_runtime = NextDayRuntimeState()" in runtime
    assert "self.current_day = {}" in runtime
    assert 'renpy.dynamic("visitorshappy"' in runtime
    assert "$ CurDay = next_day_runtime.current_day" in runtime
    breakfast = (ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
    assert 'next_day_runtime.current_day.get("rat_food_loss", 0)' in breakfast
    assert "class TractirProgressRuntimeState" in runtime
    assert "default tractir_progress = TractirProgressRuntimeState()" in runtime
    assert "self.maid_revenge_ready = False" in runtime
    assert "self.maid_revenge_reason = \"\"" in runtime
    assert "self.sandra_secured_future_day = -1" in runtime
    assert "Sandra.var" not in (ROOT / "game/Utilities/General/Common/AchievementsEndings.rpy").read_text(encoding="utf-8-sig")
    for legacy_name in LEGACY_NAMES:
        assert legacy_name not in runtime
    for dead_name in DEAD_CHECKPOINT_NAMES:
        assert dead_name not in runtime


def test_report_and_progress_have_no_legacy_save_authority():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    for legacy_name in LEGACY_NAMES:
        assert legacy_name not in migration
    assert "tractir_save_migrate_report_and_progress_runtime" not in migration
    assert 'globals().pop("_tractir_progress_revision", None)' in migration
    assert 'globals().pop("_tractir_last_autosave_reason", None)' in migration
