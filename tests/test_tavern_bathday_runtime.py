"""Focused checks for the shed-owned bathday event and hot-water gate."""

from pathlib import Path
from types import SimpleNamespace
import textwrap


ROOT = Path(__file__).resolve().parents[1]
WASHROOM = (ROOT / "game/Inn/ShedWashroom.rpy").read_text(encoding="utf-8-sig")
THREADS = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
BREAKFAST = (ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
RENOVATIONS = (ROOT / "game/Inn/TavernRenovations.rpy").read_text(encoding="utf-8-sig")
SHED = (ROOT / "game/Inn/Shed.rpy").read_text(encoding="utf-8-sig")


def load_function(source, name, namespace):
    lines = source.splitlines()
    start = next(index for index, line in enumerate(lines) if line.lstrip().startswith(f"def {name}("))
    indent = len(lines[start]) - len(lines[start].lstrip())
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) > indent):
        end += 1
    exec(textwrap.dedent("\n".join(lines[start:end])), namespace)
    return namespace[name]


def test_three_distinct_pictures_come_only_from_bathday_folder():
    folder = "images/tavern/backyard/shed/bathDay/"
    files = [f"{folder}bath{i}.jpg" for i in range(1, 15)] + ["images/other/bath1.jpg"]
    calls = []
    namespace = {
        "renpy": SimpleNamespace(list_files=lambda: files),
        "current_game_day": lambda: 42,
        "procedural_randint": lambda low, high, key: calls.append((low, high, key)) or high,
    }
    pictures = load_function(WASHROOM, "tavern_bathday_pictures", namespace)()
    assert len(pictures) == len(set(pictures)) == 3
    assert all(picture.startswith(folder) for picture in pictures)
    assert [high for _, high, _ in calls] == [13, 12, 11]


def test_sandra_request_is_breakfast_only_after_renovation():
    calendar = SimpleNamespace(week=6, hour=9)
    breakfast = SimpleNamespace(present_ids=["sandra", "melissa", "amanda"])
    renovated = SimpleNamespace(done=True)
    namespace = {
        "calendar_v2": calendar,
        "player": SimpleNamespace(tavern_management=SimpleNamespace(breakfast=breakfast)),
        "tavern": SimpleNamespace(renovation_complete=lambda code: code == "shed" and renovated.done),
    }
    ready = load_function(WASHROOM, "tavern_bathday_breakfast_request_ready", namespace)
    assert ready()
    calendar.hour = 11
    assert ready()
    calendar.hour = 12
    assert not ready()
    calendar.week, calendar.hour = 3, 9
    assert ready()
    calendar.week = 5
    assert not ready()
    calendar.week = 6
    renovated.done = False
    assert not ready()


def test_bathday_is_room_entry_event_not_a_competing_breakfast_trigger():
    bath_thread = THREADS.split('RThreadData(0, "tavern", "BathDay"', 1)[1].split('RThreadData(0, "tavern", "SundayDinner"', 1)[0]
    assert '("story_tavern_bathday", 3, (21, 23)' in bath_thread
    assert '("story_tavern_bathday", 6, (18, 22)' in bath_thread
    assert bath_thread.count('"ShedWashroom", "enter"') == 2
    assert '"TavernKitchen", "breakfast"' not in bath_thread
    assert "_bathday_request_now = tavern_bathday_breakfast_request_ready()" in BREAKFAST
    assert bath_thread.count("tavern_bathday_ready") == 2


def test_renovated_washroom_has_tub_and_exit_and_old_chamber_is_inaccessible():
    washroom_entry = WASHROOM.split("label ShedWashroom:", 1)[1].split("\nlabel ", 1)[0]
    old_chamber_entry = (ROOT / "game/Inn/ShedRuinedChamber.rpy").read_text(encoding="utf-8-sig")
    assert "rooms.current.build_action_items() + rooms.current.build_exit_items()" in washroom_entry
    assert 'not tavern.renovation_complete("shed") and not rooms.get("ShedRuinedChamber").is_hidden' in SHED
    assert "if not shed_ruined_chamber_accessible():" in old_chamber_entry


def test_shed_has_one_direct_bath_preparation_action():
    stove = RENOVATIONS.split("label ShedHotWaterStove:", 1)[1].split("\nlabel ", 1)[0]
    assert 'action_id="prepare_shed_bath", label="Подготовить купальню", hook="call", target="ShedHotWaterStove"' in RENOVATIONS
    assert stove.count('call MakeFire("chopped_wood_001", "Shed", "", "shed_hot_water_stove")') == 1
    assert stove.count('call BoilWater("shed_hot_water_stove", "Shed", "", "shed_hot_water_stove")') == 1
    assert stove.count("menu:") == 1
    assert '"Разжечь огонь или подложить дрова"' not in stove
    assert '"Вскипятить воду"' not in stove
    assert '"Вычистить золу"' not in stove
    assert '"Вернуться в сарай"' in stove


def test_shed_keeps_one_log_splitting_route_and_existing_fuel_check():
    lumber = (ROOT / "game/Items/Resources/LumberItem.rpy").read_text(encoding="utf-8-sig")
    chores = (ROOT / "game/Inn/PlayerChoresSystem.rpy").read_text(encoding="utf-8-sig")
    assert '"chop_lumber_with_old_axe"' in SHED.split("def build_shed_action_items():", 1)[1].split("\nlabel Shed:", 1)[0]
    assert 'action_id="chop_lumber"' in lumber
    assert 'target="Chop"' in lumber
    assert 'if key == "make_fire" and not _pc_fire_fuel_available(where_id, object_id):' in chores
    assert '"Сначала нужно наколоть бревна на дрова."' in chores
