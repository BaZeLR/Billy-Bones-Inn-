import json
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


def test_each_hall_job_allows_all_available_workers():
    report_source = (ROOT / "game/Inn/menu_tavernstat.rpy").read_text(encoding="utf-8-sig")
    layout_source = (ROOT / "game/Utilities/General/Screens/main_layout.rpy").read_text(encoding="utf-8-sig")

    assert "TAVERN_HALL_JOB_CAPACITY" not in report_source
    assert "toggle_hall_job_with_limit" not in report_source + layout_source
    assert "_tavern_can_toggle_hall_job" not in report_source
    assert '"hall_job_capacity"' not in report_source
    assert '"kitchen_assigned": _tavern_job_load("jobkitchentomorrow")' in report_source
    assert '"cleaning_assigned": _tavern_job_load("jobcleaningtomorrow")' in report_source
    assert '"waitress_assigned": _tavern_job_load("jobwaitresstomorrow")' in report_source
    for job_key in ("jobkitchentomorrow", "jobcleaningtomorrow", "jobwaitresstomorrow"):
        assert f'Function(toggle_job_assignment, "{job_key}", person)' in report_source
        assert f'Function(toggle_job_assignment, "{job_key}", _worker)' in layout_source


def test_staff_work_schedules_read_current_jobs_from_the_npc_owner():
    expected = {
        "amanda": {
            "working_kitchen": ("TavernKitchen", ["jobkitchen"]),
            "working_hall": ("TavernMain", ["jobcleaning", "jobwaitress"]),
        },
        "sandra": {
            "working_kitchen": ("TavernKitchen", ["jobkitchen"]),
            "working_waitressing": ("TavernMain", ["jobwaitress"]),
            "working_cleaning": (["TavernMain", "TavernStorage", "Backyard"], ["jobcleaning"]),
        },
    }

    for person, work_rows in expected.items():
        schedule = json.loads((ROOT / "game/NPC/Schedules" / f"{person}.json").read_text(encoding="utf-8"))
        entries = {row["label"]: row for row in schedule["entries"]}
        for label, (location, jobs) in work_rows.items():
            row = entries[label]
            condition = row["condition"]
            actual_jobs = list(condition.get("jobs", []))
            if condition.get("job"):
                actual_jobs.append(condition["job"])
            assert row["location"] == location
            assert condition["rule"] == "any_job_assigned"
            assert condition["people"] == [person]
            assert actual_jobs == jobs

    melissa_schedule = json.loads((ROOT / "game/NPC/Schedules/melissa.json").read_text(encoding="utf-8"))
    melissa_work_rows = [row for row in melissa_schedule["entries"] if row.get("label") == "working_day"]
    assert len(melissa_work_rows) == 1
    melissa_work = melissa_work_rows[0]
    assert melissa_work["condition"] == {
        "rule": "any_job_assigned",
        "people": ["melissa"],
        "jobs": ["jobkitchen", "jobcleaning", "jobwaitress"],
    }
    assert {
        (choice["location"], choice["condition"]["job"])
        for choice in melissa_work["location_choices"]
    } == {
        ("TavernKitchen", "jobkitchen"),
        ("TavernMain", "jobwaitress"),
        ("TavernMain", "jobcleaning"),
        ("TavernStorage", "jobcleaning"),
        ("Backyard", "jobcleaning"),
    }

    rule_source = (ROOT / "game/Utilities/General/Classes/GameObjectTemplate.rpy").read_text(encoding="utf-8-sig")
    job_rule = rule_source.split('if rule_name == "any_job_assigned":', 1)[1].split("\n        return False\n        return False", 1)[0]
    assert "info.job_value(current_job, 0)" in job_rule
    assert 'getattr(info, "jobs"' not in job_rule
