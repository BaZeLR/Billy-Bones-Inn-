"""Run the real NPC owners without loading Ren'Py presentation or game assets."""

import ast
from collections import deque
from copy import deepcopy
from pathlib import Path
from textwrap import dedent
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
PEOPLE = ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy"
RELATIONSHIPS = ROOT / "game/Utilities/General/NPC/RelationshipDynamics.rpy"
NPC_IDS = ("amanda", "melissa", "sandra", "liza", "georgett", "clara", "becky", "future_worker")


def load_definitions(path, marker, names, namespace):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    start = lines.index(marker) + 1
    end = next(
        (index for index in range(start, len(lines)) if lines[index] and not lines[index][0].isspace() and not lines[index].startswith("#")),
        len(lines),
    )
    tree = ast.parse(dedent("\n".join(lines[start:end])), filename=str(path))
    definitions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names]
    assert {node.name for node in definitions} == set(names)
    module = ast.Module(body=definitions, type_ignores=[])
    exec(compile(module, str(path), "exec"), namespace)


class ScriptedRandom:
    def __init__(self):
        self.values = deque()
        self.calls = []

    def __call__(self, low, high):
        self.calls.append((low, high))
        assert self.values, "Unexpected extra random draw"
        value = self.values.popleft()
        assert low <= value <= high
        return value


def snapshot(npc):
    state = dict(npc.__dict__)
    state["wardrobe"] = vars(npc.wardrobe)
    return deepcopy(state)


@pytest.fixture
def runtime():
    npcs = {}
    pending = set()
    clock = SimpleNamespace(day=30)
    rng = ScriptedRandom()
    household = SimpleNamespace(
        outfit_requests={},
        barber_appointments={},
        barber_visit_last_day={},
        barber_request_last_day={},
    )
    namespace = {
        "people": SimpleNamespace(get_info=npcs.get),
        "household": household,
        "daily_events": SimpleNamespace(exists=lambda name, event, _location: (name, event) in pending),
        "current_game_day": lambda: clock.day,
        "renpy": SimpleNamespace(random=SimpleNamespace(randint=rng)),
        "DressTopPart": {},
        "DressBottomPart": {},
    }
    load_definitions(
        PEOPLE,
        "init -999 python:",
        {"people_to_int", "people_to_bool", "people_normalize_id", "GirlWardrobeState", "PeopleInfo", "BaseNPC", "Girl"},
        namespace,
    )
    load_definitions(
        RELATIONSHIPS,
        "init -42 python:",
        {"relationship_int", "relationship_key", "relationship_state", "relationship_anger", "relationship_set_anger", "relationship_calm"},
        namespace,
    )

    def make_npc(name="amanda", rel=40, cap=100, anger=0, talked=0):
        npc = namespace["Girl"](name, rel=rel)
        npc.relationship_cap = cap
        npc.anger_with_player = anger
        npc.talked_today = talked
        npc.openness = 7
        npc.corruption = 12
        npcs[name] = npc
        namespace["relationship_state"](name)
        return npc

    return SimpleNamespace(
        namespace=namespace, npcs=npcs, make_npc=make_npc,
        pending=pending, clock=clock, rng=rng, household=household,
    )


@pytest.mark.parametrize("name", NPC_IDS)
@pytest.mark.parametrize("before,after", ((40, 35), (5, 0), (3, 0), (0, 0)))
def test_negative_reaction_costs_five_clamped_at_zero(runtime, name, before, after):
    npc = runtime.make_npc(name, rel=before)
    other = runtime.make_npc("unrelated_npc")
    unchanged = snapshot(other)

    assert npc.record_negative_reaction("harass_player_watched") == after - before

    assert npc.rel == after
    assert npc.anger_with_player == 1
    assert npc.reaction_state["last_anger_reason"] == "harass_player_watched"
    assert (npc.openness, npc.corruption, npc.talked_today) == (7, 12, 0)
    assert npc.can_apologize()
    assert snapshot(other) == unchanged
    assert runtime.rng.calls == []


@pytest.mark.parametrize("name", NPC_IDS)
@pytest.mark.parametrize("gain", range(1, 6))
def test_accepted_apology_draws_half_chance_then_one_to_five(runtime, name, gain):
    npc = runtime.make_npc(name, anger=4)
    runtime.namespace["relationship_set_anger"](name, 3, 2, "kino")
    other = runtime.make_npc("unrelated_npc", anger=2)
    unchanged = snapshot(other)
    runtime.rng.values.extend((1, gain))

    assert npc.attempt_apology() == (True, gain)

    assert npc.rel == 40 + gain
    assert npc.anger_with_player == 0
    assert npc.reaction_state["last_anger_reason"] == ""
    mood = runtime.namespace["relationship_state"](name)
    assert (mood["anger"], mood["anger_reason"], mood["anger_until_day"]) == (0, "", -1)
    assert npc.talked_today == 1
    assert (npc.openness, npc.corruption) == (7, 12)
    assert runtime.rng.calls == [(1, 2), (1, 5)]
    assert not runtime.rng.values
    assert snapshot(other) == unchanged


@pytest.mark.parametrize("name", NPC_IDS)
def test_refused_apology_changes_only_talk_count(runtime, name):
    npc = runtime.make_npc(name, anger=3)
    runtime.namespace["relationship_set_anger"](name, 2, 1, "harass_player_ignored")
    before = snapshot(npc)
    runtime.rng.values.append(2)

    assert npc.attempt_apology() == (False, 0)

    before["talked_today"] += 1
    assert snapshot(npc) == before
    assert runtime.rng.calls == [(1, 2)]


@pytest.mark.parametrize("cap,start,expected", ((20, 19, 1), (20, 20, 0), (100, 98, 2), (100, 100, 0)))
def test_apology_reports_actual_gain_at_npc_relationship_cap(runtime, cap, start, expected):
    npc = runtime.make_npc(rel=start, cap=cap, anger=1)
    runtime.rng.values.extend((1, 5))
    assert npc.attempt_apology() == (True, expected)
    assert npc.rel == cap
    assert npc.anger_with_player == 0


@pytest.mark.parametrize("name", NPC_IDS)
def test_successful_apology_cannot_award_a_duplicate_gain(runtime, name):
    npc = runtime.make_npc(name, anger=1)
    runtime.rng.values.extend((1, 3))
    assert npc.attempt_apology() == (True, 3)
    after = snapshot(npc)

    assert not npc.can_apologize()
    assert npc.attempt_apology() == (False, 0)
    assert snapshot(npc) == after
    assert len(runtime.rng.calls) == 2


@pytest.mark.parametrize("rel,anger,mood,eligible", ((4, 0, 0, True), (5, 0, 0, False), (40, 1, 0, True), (40, 0, 1, True)))
def test_apology_reads_existing_anger_and_legacy_low_relationship(runtime, rel, anger, mood, eligible):
    npc = runtime.make_npc(rel=rel, anger=anger)
    if mood:
        runtime.namespace["relationship_set_anger"](npc.name, mood, 1, "weekly_chores")
    assert npc.can_apologize() is eligible


def test_three_daily_attempts_exhaust_apology_without_additional_changes(runtime):
    npc = runtime.make_npc(anger=1)
    runtime.rng.values.extend((2, 2, 2))
    for count in range(1, 4):
        assert npc.can_apologize()
        assert npc.attempt_apology() == (False, 0)
        assert npc.talked_today == count
    before = snapshot(npc)
    assert not npc.can_apologize()
    assert npc.attempt_apology() == (False, 0)
    assert snapshot(npc) == before
    assert len(runtime.rng.calls) == 3


@pytest.mark.parametrize("name", NPC_IDS + ("unhired_woman",))
@pytest.mark.parametrize("favor", ("tailor", "barber"))
@pytest.mark.parametrize("rel", (0, 15))
def test_all_female_instances_can_request_favors_without_employment_or_gift_gate(runtime, name, favor, rel):
    npc = runtime.make_npc(name, rel=rel)
    assert npc.jobs == {}
    assert npc.can_request_favor(favor)


@pytest.mark.parametrize("pending_kind", ("BuyDress", "BuyDressTom", "outfit"))
def test_pending_tailor_owner_blocks_only_the_same_woman(runtime, pending_kind):
    npc = runtime.make_npc("clara")
    other = runtime.make_npc("becky")
    if pending_kind == "outfit":
        runtime.household.outfit_requests[npc.name] = "surprise"
    else:
        runtime.pending.add((npc.name, pending_kind))
    assert not npc.can_request_favor("tailor")
    assert other.can_request_favor("tailor")
    assert npc.can_request_favor("barber")


@pytest.mark.parametrize("field", ("barber_visit_last_day", "barber_request_last_day"))
@pytest.mark.parametrize("elapsed,eligible", ((0, False), (13, False), (14, True), (15, True)))
def test_barber_uses_both_existing_fourteen_day_cooldowns(runtime, field, elapsed, eligible):
    npc = runtime.make_npc("unhired_woman")
    getattr(runtime.household, field)[npc.name] = runtime.clock.day - elapsed
    assert npc.can_request_favor("barber") is eligible
    assert npc.can_request_favor("tailor")


def test_barber_appointment_blocks_duplicate_request_only_for_its_owner(runtime):
    npc = runtime.make_npc("liza")
    other = runtime.make_npc("georgett")
    runtime.household.barber_appointments[npc.name] = 1
    assert not npc.can_request_favor("barber")
    assert other.can_request_favor("barber")
    assert npc.can_request_favor("tailor")


@pytest.mark.parametrize("favor", ("tailor", "barber"))
@pytest.mark.parametrize("anger_owner", ("npc", "relationship_mood"))
def test_existing_anger_blocks_favors_without_creating_another_state(runtime, favor, anger_owner):
    npc = runtime.make_npc()
    if anger_owner == "npc":
        npc.anger_with_player = 1
    else:
        runtime.namespace["relationship_set_anger"](npc.name, 1, 1, "kino")
    before = snapshot(npc)
    assert not npc.can_request_favor(favor)
    assert snapshot(npc) == before


def test_unknown_favor_is_unavailable(runtime):
    assert not runtime.make_npc().can_request_favor("unknown")
