from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_tavern_event_plan_has_no_legacy_queue_projection_anywhere():
    source = "\n".join(path.read_text(encoding="utf-8-sig") for path in (ROOT / "game").rglob("*.rpy"))
    for legacy in ("Events" + "Count", "New" + "Events", "tavern_work_sync_legacy_queue", "build_tavern_events_queue_python"):
        assert legacy not in source
    assert "def tavern_work_codes_for_period(" in source
    assert "def tavern_work_has_period(" in source
    assert "while tavern_work_has_period(10, True):" in source
