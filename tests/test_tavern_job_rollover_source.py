from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_hall_job_rollover_is_owned_by_npc_jobs():
    source = (ROOT / "game/Utilities/General/NPC/ChangeTommorowHallJob.rpy").read_text(encoding="utf-8")

    assert "jobkitchentomorrow[GirlName]" not in source
    assert "jobcleaningtomorrow[GirlName]" not in source
    assert "jobwaitresstomorrow[GirlName]" not in source

    assert 'info.job_value(tomorrow_key, 0)' in source
    assert 'info.job_value(tomorrow_key, info.job_value(current_key, 0))' not in source
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


def test_default_staff_jobs_define_today_and_tomorrow_in_the_npc_owner():
    expected = {
        "Sandra": (1, 0, 0),
        "Melissa": (0, 1, 1),
        "Amanda": (0, 1, 1),
    }
    for name, values in expected.items():
        source = (ROOT / "game/NPC/Girls" / name / ("Init%s.rpy" % name)).read_text(encoding="utf-8-sig")
        for key, value in zip(("jobkitchen", "jobcleaning", "jobwaitress"), values):
            assert '"%s": %d' % (key, value) in source
        for key, value in zip(("jobkitchentomorrow", "jobcleaningtomorrow", "jobwaitresstomorrow"), values):
            assert '"%s": %d' % (key, value) in source


def test_old_save_staff_job_plan_is_repaired_once_before_live_readers_run():
    source = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert "tractir_save_normalize_tavern_staff_jobs()" in source
    repair = source.split("def tractir_save_normalize_tavern_staff_jobs():", 1)[1].split("def ", 1)[0]
    assert 'for person in ("sandra", "melissa", "amanda")' in repair
    assert "if tomorrow_key not in jobs:" in repair
    assert "info.set_job_value(tomorrow_key" in repair


def test_report_and_staff_cards_share_job_text_projection():
    report_source = (ROOT / "game/Inn/menu_tavernstat.rpy").read_text(encoding="utf-8-sig")
    card_source = (ROOT / "game/NPC/Girls/Common/GirlCard.rpy").read_text(encoding="utf-8-sig")

    assert "def _tavern_worker_current_jobs(person):" in report_source
    assert "_tavern_worker_current_jobs(person)" in report_source
    assert '("Работа сегодня", _tavern_worker_current_jobs(key))' in card_source
    assert '("Работа завтра", _tavern_worker_tomorrow_jobs(key))' in card_source


def test_each_hall_job_uses_one_three_worker_capacity_rule():
    report_source = (ROOT / "game/Inn/menu_tavernstat.rpy").read_text(encoding="utf-8-sig")
    layout_source = (ROOT / "game/Utilities/General/Screens/main_layout.rpy").read_text(encoding="utf-8-sig")

    assert "define TAVERN_HALL_JOB_CAPACITY = 3" in report_source
    assert "def toggle_hall_job_with_limit(job_key, person):" in report_source
    assert "def _tavern_can_toggle_hall_job(job_key, person):" in report_source
    assert "max_slots" not in report_source
    assert '"hall_job_capacity": TAVERN_HALL_JOB_CAPACITY' in report_source
    assert "toggle_hall_job_with_limit, \"jobkitchentomorrow\", _worker, 2" not in layout_source
