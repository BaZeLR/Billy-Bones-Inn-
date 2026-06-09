from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_hall_job_rollover_defaults_missing_tomorrow_assignments():
    source = (ROOT / "game/Utilities/General/NPC/ChangeTommorowHallJob.rpy").read_text(encoding="utf-8")

    assert "jobkitchentomorrow[GirlName]" not in source
    assert "jobcleaningtomorrow[GirlName]" not in source
    assert "jobwaitresstomorrow[GirlName]" not in source

    assert "jobkitchentomorrow.get(person, jobkitchen.get(person, 0))" in source
    assert "jobcleaningtomorrow.get(person, jobcleaning.get(person, 0))" in source
    assert "jobwaitresstomorrow.get(person, jobwaitress.get(person, 0))" in source
