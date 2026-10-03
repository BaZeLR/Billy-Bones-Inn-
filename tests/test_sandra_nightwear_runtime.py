from pathlib import Path
from types import SimpleNamespace

import pytest

from tests.test_tavern_renovations_runtime import _exec_definitions


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def runtime():
    cycle = {"horny": 0.10}
    calendar = SimpleNamespace(hour=23)
    thread = SimpleNamespace(num=0)
    schedule = {"location": "TavernSandraRoom", "awake": True, "label": "evening_room"}
    room = SimpleNamespace(bg_picture="images/tavern/secondfloor/sandra_room.png",
                           descriptions=[SimpleNamespace(text="Комната Сандры.")])
    ns = {
        "Girl": type("Girl", (), {}), "calendar_v2": calendar,
        "threads": {"sandraWeeklyEvaluation": thread},
        "girl_decision_cycle_state": lambda code: cycle,
        "people": SimpleNamespace(location=lambda code: schedule["location"],
                                  is_awake=lambda code: schedule["awake"],
                                  schedule_state=lambda code: schedule),
        "rooms": SimpleNamespace(get=lambda code: room),
        "renpy": SimpleNamespace(loadable=lambda path: (ROOT / "game" / path).is_file()),
        "household_morning_issue_type": lambda code: "",
        "household_room_issue_notice_text": lambda code: "",
        "werecat_append_visible_text": lambda text, room: text,
    }
    _exec_definitions("Items/Clothes/InitDressDesc.rpy", {"DressTopPart", "DressBottomPart"}, ns)
    _exec_definitions("Utilities/General/NPC/PeopleRuntime.rpy",
                      {"people_to_int", "people_clamp", "GirlWardrobeState"}, ns)
    _exec_definitions("NPC/Girls/Sandra/InitSandra.rpy", {"SandraInfo"}, ns)
    sandra = ns["SandraInfo"].__new__(ns["SandraInfo"])
    sandra.code_name, sandra.corruption, sandra.rel = "sandra", 20, 5
    sandra.arousal = 0
    sandra.arousal_value = lambda: sandra.arousal
    sandra.wardrobe = ns["GirlWardrobeState"].from_base({
        "day_dress": "workdresszhilet", "bra": "simplebra", "panties": "simplepanties",
        "legs": "", "shoes": "simpleshoes",
    })
    sandra.current_dress = sandra.wardrobe.current_dress
    ns["Sandra"] = sandra
    _exec_definitions("Inn/TavernSandraRoom.rpy", {
        "tavern_sandra_room_picture", "tavern_sandra_room_text", "tavern_sandra_room_nightwear_now",
    }, ns)
    return SimpleNamespace(ns=ns, sandra=sandra, cycle=cycle, calendar=calendar,
                           thread=thread, schedule=schedule, room=room)


@pytest.mark.parametrize("virgin", [True, False])
@pytest.mark.parametrize("corruption,friend,arousal,horny,invited,naked", [
    (20, 5, 0, .10, False, False),
    (29, 20, 90, .35, False, False),
    (30, 10, 64, .10, False, False),
    (30, 10, 65, .10, False, True),
    (30, 10, 0, .20, False, True),
    (49, 9, 90, .35, False, False),
    (50, 0, 0, .10, False, True),
    (20, 10, 0, .10, True, True),
    (20, 9, 0, .10, True, False),
])
def test_sandra_policy_uses_her_live_state_not_virginity(runtime, virgin, corruption, friend, arousal, horny, invited, naked):
    s = runtime.sandra
    s.stats = {"virginity": virgin}
    s.corruption, s.rel, s.arousal = corruption, friend, arousal
    runtime.cycle["horny"] = horny
    runtime.thread.num = 4 if invited else 0
    preferred = dict(s.wardrobe.day_underwear)
    owned = list(s.wardrobe.owned_items)
    s.wear_night_clothes()
    assert s.wardrobe.context == "night"
    assert s.wardrobe.naked() is naked
    assert s.wardrobe.layer("bra") == s.wardrobe.layer("shoes") == ""
    if not naked:
        assert s.current_dress() == "nightshirt"
        assert bool(s.wardrobe.layer("panties")) == (corruption < 30)
    assert s.wardrobe.day_underwear == preferred and s.wardrobe.owned_items == owned


def test_invitation_is_not_a_permanent_naked_flag(runtime):
    runtime.sandra.rel = 10
    runtime.thread.num = 4
    runtime.calendar.hour = 21
    runtime.sandra.wear_night_clothes()
    assert runtime.sandra.current_dress() == "nightshirt"


def test_explicit_authored_mode_and_day_clothes_remain_authoritative(runtime):
    s = runtime.sandra
    s.corruption = 70
    s.wear_night_clothes(0)
    assert s.current_dress() == "nightshirt" and s.wardrobe.layer("panties") == "simplepanties"
    s.wardrobe.wear_day()
    assert s.current_dress() == "workdresszhilet" and s.wardrobe.layer("bra") == "simplebra"


def test_room_picture_follows_actual_wear_presence_and_sleep(runtime):
    s, ns = runtime.sandra, runtime.ns
    s.wear_night_clothes()
    assert ns["tavern_sandra_room_picture"]() == "images/sandra/player_room_sandra_0.jpg"
    runtime.schedule["awake"] = False
    assert ns["tavern_sandra_room_picture"]() == "images/sandra/sleeps .png"
    s.corruption = 50
    s.wear_night_clothes()
    # There is no verified naked sleeping CG; do not substitute an awake pose.
    assert ns["tavern_sandra_room_picture"]() == runtime.room.bg_picture
    assert "спит" in ns["tavern_sandra_room_text"]() and "без одежды" in ns["tavern_sandra_room_text"]()
    runtime.schedule["awake"] = True
    assert ns["tavern_sandra_room_picture"]() == "images/sandra/thanks/sandraInHerRoonm.jfif"
    runtime.schedule["location"] = "TavernKitchen"
    assert ns["tavern_sandra_room_picture"]() == runtime.room.bg_picture
    assert "Сандра без одежды" not in ns["tavern_sandra_room_text"]()


def test_native_entries_and_finish_use_sandra_policy_without_changing_amanda():
    def read(path):
        return (ROOT / "game" / path).read_text(encoding="utf-8-sig")
    room = read("Inn/TavernSandraRoom.rpy").split("label TavernSandraRoom:", 1)[1]
    assert room.index("Sandra.wear_night_clothes()") < room.index("call RoomEnterEventGate")
    thanks = read("NPC/Girls/Sandra/SandraEvents.rpy").split("label TavernSandraNightThanksScene:", 1)[1]
    assert thanks.index("Sandra.wear_night_clothes()") < thanks.index('call HouseholdSexEngine')
    finish = read("NPC/Girls/Melissa/IntMelissaSex.rpy").split("label HouseholdSexFinish:", 1)[1]
    assert 'if _hse_girl == "sandra":' in finish and "_hse_info.wear_night_clothes()" in finish
    assert "_hse_info.wear_night_clothes(0)" in finish
    engine = read("NPC/Girls/Melissa/IntMelissaSex.rpy").split("label HouseholdSexEngine", 1)[1]
    assert engine.count('tavern_sandra_room_picture() if _hse_girl == "sandra"') == 3
    wake = read("Inn/HouseholdRuntimeEvents.rpy").split('label HouseholdWakeSleepyGirl', 1)[1]
    assert 'tavern_amanda_room_sleep_dress() if _wake_girl == "amanda" else 0' in wake
