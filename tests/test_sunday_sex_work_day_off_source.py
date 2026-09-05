import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_sunday_sex_work_uses_one_day_off_rule():
    clients = read("game/Utilities/General/Sex/WhoreNextDayClients.rpy")
    finish_day = read("game/Utilities/Time/NextDay_FinishDayEvents.rpy")
    report = read("game/Utilities/General/NPC/DailySetstatdefault.rpy")

    assert "def tavern_sex_work_day_allowed(week_value=None):" in clients
    assert "return people_to_int(week_value, 0) != 7" in clients
    assert "if not tavern_sex_work_day_allowed():" in clients
    assert '_wnd_girl.set_sex_stat("clients_day_total", 0)' in clients

    assert 'girl in ("georgett", "liza")' in finish_day
    assert 'place in ("Prostitution", "Glory")' in finish_day
    assert "if tavern_sex_work_day_allowed():" in report

    assert "glory_max_i = (glory_max_i * 3) // 4" not in clients
    assert "if week_val == 7:" not in clients


def test_georgette_and_lisette_have_no_sunday_work_schedule():
    for npc_id in ("georgett", "liza"):
        schedule_path = ROOT / "game" / "NPC" / "Schedules" / (npc_id + ".json")
        schedule = json.loads(schedule_path.read_text(encoding="utf-8-sig"))
        work_entries = [
            row
            for row in schedule["entries"]
            if row.get("location") in ("TavernMain", "PortStreets")
        ]

        assert work_entries
        assert all(7 not in row.get("weekdays", []) for row in work_entries)
