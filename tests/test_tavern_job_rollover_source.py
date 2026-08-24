from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_hall_job_rollover_is_owned_by_npc_jobs():
    source = (ROOT / "game/Utilities/General/NPC/ChangeTommorowHallJob.rpy").read_text(encoding="utf-8")

    assert "jobkitchentomorrow[GirlName]" not in source
    assert "jobcleaningtomorrow[GirlName]" not in source
    assert "jobwaitresstomorrow[GirlName]" not in source

    assert 'info.job_value(tomorrow_key, info.job_value(current_key, 0))' in source
    assert 'info.set_job_value(current_key, value)' in source
    assert 'info.set_job_value(tomorrow_key, value)' in source
    for legacy_map in ("jobkitchen", "jobcleaning", "jobwaitress", "jobkitchentomorrow", "jobcleaningtomorrow", "jobwaitresstomorrow"):
        assert f"{legacy_map}.get(" not in source
        assert f"{legacy_map}[" not in source


def test_tavern_report_does_not_initialize_or_sync_job_state_while_reading():
    source = (ROOT / "game/Inn/menu_tavernstat.rpy").read_text(encoding="utf-8-sig")

    assert "ensure_default_tavern_jobs" not in source
    report = source.split("def BuildTavernReport():", 1)[1].split("def ", 1)[0]
    assert ".set_job_value(" not in report
    assert ".jobs.setdefault(" not in report
