import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_all_tavern_job_rollover_is_owned_by_each_npc():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
    next_day = (ROOT / "game/Utilities/Time/NextDay_TavernDaily.rpy").read_text(encoding="utf-8-sig")
    apply_plan = runtime.split("def apply_tavern_job_plan(self):", 1)[1].split("def tavern_regular_job_schedule_entry", 1)[0]

    for current_key, tomorrow_key in (
        ("jobkitchen", "jobkitchentomorrow"),
        ("jobcleaning", "jobcleaningtomorrow"),
        ("jobwaitress", "jobwaitresstomorrow"),
    ):
        assert '("%s", "%s")' % (current_key, tomorrow_key) in apply_plan
    assert "self.set_job_value(current_key" in apply_plan
    assert "for _tavern_worker in people.girl_values():" in next_day
    assert "_tavern_worker.apply_tavern_job_plan()" in next_day
    assert "apply_tomorrow_hall_job" not in next_day
    assert not (ROOT / "game/Utilities/General/NPC/ChangeTommorowHallJob.rpy").exists()


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


def test_scheduler_offers_all_five_jobs_to_every_tavern_worker():
    report_source = (ROOT / "game/Inn/menu_tavernstat.rpy").read_text(encoding="utf-8-sig")
    layout_source = (ROOT / "game/Utilities/General/Screens/main_layout.rpy").read_text(encoding="utf-8-sig")

    assert "TAVERN_HALL_JOB_CAPACITY" not in report_source
    assert "toggle_hall_job_with_limit" not in report_source + layout_source
    assert "_tavern_can_toggle_hall_job" not in report_source
    assert '"hall_job_capacity"' not in report_source
    assert '"kitchen_assigned": _tavern_job_load("jobkitchentomorrow")' in report_source
    assert '"cleaning_assigned": _tavern_job_load("jobcleaningtomorrow")' in report_source
    assert '"waitress_assigned": _tavern_job_load("jobwaitresstomorrow")' in report_source
    assert "return [person for person, info in people.girl_items() if info.is_tavern_worker()]" in report_source
    for job_key in (
        "jobkitchentomorrow", "jobcleaningtomorrow", "jobwaitresstomorrow",
        "jobgloryholeTommorow", "jobwhoreTommorow",
    ):
        assert '("%s",' % job_key in report_source
    assert "for job_key, title, description_index, button_id in TAVERN_JOB_OPTIONS:" in report_source
    assert "for _job_key, _job_title, _job_description_index, _job_button_id in TAVERN_JOB_OPTIONS:" in layout_source
    assert "jobHallAvail\")" not in layout_source


def test_all_tavern_workers_use_the_npc_owned_job_schedule():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
    report_source = (ROOT / "game/Inn/menu_tavernstat.rpy").read_text(encoding="utf-8-sig")
    layout_source = (ROOT / "game/Utilities/General/Screens/main_layout.rpy").read_text(encoding="utf-8-sig")
    georgett_talk = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8-sig")

    assert "Georgett.set_hired(True)" in georgett_talk
    assert "Liza.set_hired(True)" in georgett_talk
    assert 'Georgett.jobs["jobGloryHoleAvail"] = 1' in georgett_talk
    assert 'Liza.jobs["jobGloryHoleAvail"] = 1' in georgett_talk
    assert "def is_tavern_worker(self):" in runtime
    assert "def tavern_job_available(self, job_key):" in runtime
    assert "def tavern_regular_job_schedule_entry(self, weekday_value=None, time_value=None):" in runtime
    assert 'if people_to_int(self.job_value("jobHallAvail", 0), 0) > 0:' in runtime
    assert 'self.tavern_regular_job_schedule_entry(weekday_value, time_value)' in runtime
    assert 'info.assign_tavern_service("" if current else "intimate", True)' in report_source
    assert 'info.assign_tavern_service("" if current else "gloryhole", True)' in report_source
    assert "_tavern_can_assign_whore" not in report_source + layout_source
    assert "_tavern_can_assign_gloryhole" not in report_source + layout_source
    assert "def assign_special_job(" not in report_source


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
