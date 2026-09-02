import json
import ast
import re
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


def test_church_go_around_action_matches_qsp_and_is_restored_for_loaded_saves():
    church = read("game/Town/Church/Church.rpy")
    qsp_reference = read("devdocs/characters/full_logic/clarisse_full_logic.md")
    migration = read("game/TractirSaveSync.rpy")

    assert "Church.txt:143 | act 'Обойти собор':gt 'ChurchAfterCermon', 1" in qsp_reference
    assert 'RoomAction(action_id="after_cermon_walk", label="Обойти собор", hook="ui_call", target="ChurchAfterCermon", args=(1,), condition=church_after_cermon_action_visible)' in church
    assert "return int(calendar_v2.week or 0) == 7 and church_minutes_between(11 * 60, 12 * 60 + 59)" in church

    assert "define currentVersion = 81" in migration
    assert "if loaded_version < 81:" in migration
    v80 = migration.split("def updateSave_V80():", 1)[1].split("# Saved objects must be upgraded", 1)[0]
    assert 'old_room = rooms.get("Church")' in v80
    assert 'definition = roomDefinitions.get("Church", None)' in v80
    assert "upgraded_room = definition.runtime_copy()" in v80
    assert 'upgraded_room.state.update(dict(getattr(old_room, "state", {}) or {}))' in v80
    assert "rooms.register(upgraded_room)" in v80


def test_tavern_household_relationships_and_adult_ages_have_one_definition():
    intro = read("game/Inn/Intro.rpy")
    sandra = read("game/NPC/Girls/Sandra/InitSandra.rpy")
    melissa = read("game/NPC/Girls/Melissa/InitMelissa.rpy")
    amanda = read("game/NPC/Girls/Amanda/InitAmanda.rpy")
    migration = read("game/TractirSaveSync.rpy")

    assert "Ваш дядя, Джон Лонгкок" in intro
    assert "Сандра, возлюбленная вашего покойного дяди" in intro
    assert "осиротевшие племянницы Мелисса и Аманда" in intro
    assert "они сестры по матери, но от разных отцов" in intro
    assert "не состоят с вами в родстве; вы их домовладелец и хозяин трактира" in intro

    sources = {"sandra": sandra, "melissa": melissa, "amanda": amanda}
    expected_ages = {"sandra": 34, "melissa": 20, "amanda": 18}
    for name, source in sources.items():
        match = re.search(r"self\.birth_date = (\{[^\n]+\})", source)
        assert match is not None, name
        birth = ast.literal_eval(match.group(1))
        age = 1100 - birth["cycle"]
        if (1, 1) < (birth["period"], birth["day"]):
            age -= 1
        assert age == expected_ages[name]
        assert age >= 18

    v80 = migration.split("def updateSave_V80():", 1)[1].split("# Saved objects must be upgraded", 1)[0]
    assert "(SandraStaticData, Sandra)" in v80
    assert "(MelissaStaticData, Melissa)" in v80
    assert "(AmandaStaticData, Amanda)" in v80
    assert "people.register(static_data, runtime_object)" in v80


def test_player_interactions_do_not_describe_tavern_team_as_his_family():
    interaction_sources = "\n".join([
        read("game/NPC/Girls/Sandra/IntSandraTalk.rpy"),
        read("game/NPC/Girls/Sandra/IntSandraDressChange.rpy"),
        read("game/NPC/Girls/Melissa/IntMelissaTalk.rpy"),
        read("game/NPC/Girls/Melissa/IntMelissaDressChange.rpy"),
        read("game/NPC/Girls/Amanda/IntAmandaSex.rpy"),
    ])

    for forbidden in (
        "помириться с мамой",
        "купить мамуле",
        "Мамочка, дорогая",
        "хороший сыночек",
        "к своей сестренке",
        "любимым братом",
        "купить сестренке",
        "спросили вы сестру",
        "спасибо, братик",
        "Сестричка слезла",
        "Братик, это было",
    ):
        assert forbidden not in interaction_sources

    church = read("game/Town/Church/Church.rpy")
    assert 'MenuItem("Найти Мелиссу и Аманду", Call("ChurchServiceSisters"))' in church
