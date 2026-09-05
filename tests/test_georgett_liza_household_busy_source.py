import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_georgett_and_liza_use_shared_work_interruption_rule():
    people = source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    georgett = json.loads(source("game/NPC/Schedules/georgett.json"))
    liza = source("game/NPC/Girls/Liza/InitLiza.rpy")

    port_shift = next(row for row in georgett["entries"] if row["label"] == "portstreets_work")
    assert port_shift["working"] is True
    assert "work_socializing_locations" not in liza
    assert "def interrupt_work(self):" in people
    assert "self.change_social(friend_delta=-1)" in people


def test_household_roster_is_the_only_daily_food_headcount():
    household = source("game/Utilities/General/NPC/HouseholdAI_ren.rpy")
    player = source("game/Utilities/General/Player/Player.rpy")
    daily = source("game/Utilities/Time/NextDay_TavernDaily.rpy")
    invitation = source("game/NPC/Girls/Georgett/IntGeorgettTalk.rpy")

    assert 'BASE_RESIDENT_IDS = ("you", "sandra", "melissa", "amanda")' in household
    assert 'HIRED_RESIDENT_IDS = ("georgett", "liza")' in household
    assert "info.can_work_tavern()" in household
    assert "kids_count_for_mothers(*mothers)" in household
    assert "household.member_count()" in daily
    assert "household_members" not in player
    assert "household_members" not in invitation
