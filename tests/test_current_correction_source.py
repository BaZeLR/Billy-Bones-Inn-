import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def schedule(npc_id):
    return json.loads(read(f"game/NPC/Schedules/{npc_id}.json"))["entries"]


def entry_at(entries, weekday, clock):
    minute = int(clock[:2]) * 60 + int(clock[3:])
    matches = []
    for row in entries:
        if weekday not in row.get("weekdays", []):
            continue
        start = int(row["start"][:2]) * 60 + int(row["start"][3:])
        end = int(row["end"][:2]) * 60 + int(row["end"][3:])
        if start <= minute <= end:
            matches.append(row)
    return max(matches, key=lambda row: row.get("priority", 0)) if matches else None


def test_sandra_scene_does_not_reduce_player_intimacy_capacity():
    achievement = read("game/Utilities/General/Common/AchievementsEndings.rpy")
    migration = read("game/TractirSaveSync.rpy")

    function = achievement.split("def tractir_apply_sandra_secured_future():", 1)[1].split(
        "def tractir_progress_rows", 1
    )[0]
    assert "can_cum_daily" not in function
    assert "def updateSave_V78():" in migration
    assert "player.intimacy.can_cum_daily" in migration.split("def updateSave_V78():", 1)[1]


def test_becky_kitchen_visit_uses_friendship_and_schedule_as_authority():
    becky = read("game/NPC/Girls/Becky/InitBecky.rpy")
    breakfast = read("game/Inn/TavernKitchenBreakfast.rpy")
    kitchen = read("game/Inn/TavernKitchen.rpy")

    assert "def sandra_friendship_stage(self):" in becky
    assert "return Becky.sandra_friendship_stage() >= 1" in breakfast
    assert 'people.location("becky")' in kitchen
    assert "sandra_kitchen_visit_period" not in becky + breakfast + kitchen


def test_soap_inventory_changes_only_after_a_chosen_use_or_gift():
    breakfast = read("game/Inn/TavernKitchenBreakfast.rpy")
    household = read("game/Inn/HouseholdRuntimeEvents.rpy")

    assert "player_remove_soap_pieces" not in breakfast
    assert 'player.remove_item(_soap_item, 1)' in household
    assert 'label HouseholdSoapRequestGiveNow' in household


def test_tavern_team_has_complete_sunday_day_schedule():
    expected = {
        "amanda": {"10:00": "TavernStable", "13:00": "TavernKitchen"},
        "melissa": {"10:00": "TavernMain", "13:00": "TavernKitchen"},
        "sandra": {"10:00": "TavernKitchen", "13:00": "TavernKitchen"},
    }
    for npc_id, locations in expected.items():
        entries = schedule(npc_id)
        for hour in range(6, 23):
            assert entry_at(entries, 7, f"{hour:02d}:00") is not None
        for clock, location in locations.items():
            assert entry_at(entries, 7, clock)["location"] == location
