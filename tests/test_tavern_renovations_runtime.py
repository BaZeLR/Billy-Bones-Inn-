"""Exercise the authored renovation owner without starting the Ren'Py UI."""

import ast
from copy import deepcopy
from pathlib import Path
import re
import textwrap
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
EXPECTED = {
    "sign": (200, 0, 1),
    "peephole": (100, 0, 1),
    "glory_hole": (700, 0, 1),
    "roof": (2000, 0, 2),
    "backyard": (600, 8, 3),
    "shed": (900, 12, 4),
    "guest_room": (700, 8, 3),
}


def _python_nodes(relative):
    source = (GAME / relative).read_text(encoding="utf-8-sig")
    nodes = []
    for match in re.finditer(r"^init(?:\s+-?\d+)?\s+python:\s*\n", source, re.MULTILINE):
        lines = []
        for line in source[match.end():].splitlines():
            if line.strip() and not line.startswith((" ", "\t")):
                break
            lines.append(line)
        nodes.extend(ast.parse(textwrap.dedent("\n".join(lines))).body)
    for match in re.finditer(r"^define\s+(\w+)\s*=\s*", source, re.MULTILINE):
        declaration = match.group(1) + " = "
        for line in source[match.end():].splitlines():
            declaration += line + "\n"
            try:
                parsed = ast.parse(declaration)
            except SyntaxError:
                continue
            nodes.extend(parsed.body)
            break
    return nodes


def _exec_definitions(relative, names, namespace):
    selected = []
    found = set()
    for node in _python_nodes(relative):
        node_names = {getattr(node, "name", "")}
        if isinstance(node, ast.Assign):
            node_names.update(target.id for target in node.targets if isinstance(target, ast.Name))
        if node_names & names:
            selected.append(node)
            found.update(node_names & names)
    assert found == names, f"Missing authored definitions in {relative}: {names - found}"
    exec(compile(ast.Module(body=selected, type_ignores=[]), relative, "exec"), namespace)


def _runtime(day=30, money=10000, logs=40):
    calendar = SimpleNamespace(daysInGame=day, day=3, week=2, hour=9, minute=20)
    shed = SimpleNamespace(game_items=["old_axe_001", "soap_001"] + ["lumber_001"] * logs + ["chopped_wood_001"] * 7)
    player = SimpleNamespace(economy=SimpleNamespace(money=money), inventory=SimpleNamespace(items={"lumber_001": 5}), tavern_management=SimpleNamespace())
    spent, rewards = [], []
    def spend_money(amount):
        if player.economy.money < amount:
            return False
        player.economy.money -= amount
        spent.append(amount)
        return True
    player.spend_money = spend_money
    team = [(key, SimpleNamespace(is_tavern_worker=lambda: True, reward_need_fulfilled=lambda amount, reason, key=key: rewards.append((key, amount, reason)))) for key in ("amanda", "melissa", "sandra", "clara", "liza", "georgett")]
    team.append(("becky", SimpleNamespace(is_tavern_worker=lambda: False)))
    namespace = {
        "calendar_v2": calendar, "player": player,
        "rooms": {"Shed": shed, "ShedWashroom": SimpleNamespace(is_hidden=True), "StolyarWorkshop": SimpleNamespace(is_open=lambda: True, action_menus=[])},
        "people": SimpleNamespace(girl_items=lambda: team, get_info=lambda key: dict(team)[key]),
        "get_object_id": lambda item: item if isinstance(item, str) else item.object_id,
        "player_to_int": lambda value, default=0: int(value) if value is not None else default,
        "threads": {}, "_story_num_day": lambda: calendar.daysInGame,
        "_story_level_enabled": lambda *args: True,
        "Draupnir": SimpleNamespace(), "Melissa": SimpleNamespace(),
        "initThreads": lambda: None,
    }
    _exec_definitions("Inn/TavernRenovations.rpy", {"TavernRenovationDefinition", "TavernRenovation", "TAVERN_RENOVATIONS", "TavernInfo"}, namespace)
    _exec_definitions("Utilities/General/Common/Actions.rpy", {"_room_item_count_by_id", "_room_remove_item_by_id"}, namespace)
    _exec_definitions("Utilities/General/Events/threads.rpy", {"ThreadInfo", "UThreadInfo"}, namespace)
    data = SimpleNamespace(length=7, highlight=True, level=0, person="tavern", checkConditions=lambda: True)
    namespace["threads"]["tavernRenovations"] = namespace["UThreadInfo"](data)
    namespace["threads"]["melissaBatProblem"] = SimpleNamespace(num=7)
    namespace["tavern"] = namespace["TavernInfo"]()
    return SimpleNamespace(owner=namespace["tavern"], calendar=calendar, player=player, shed=shed, spent=spent, rewards=rewards, namespace=namespace, catalog=namespace["TAVERN_RENOVATIONS"])


def accept(runtime, code):
    job = runtime.owner.renovations[code]
    job.request(runtime.catalog[code].quest_giver)
    job.accept()
    return job


def snapshot(runtime):
    return deepcopy((runtime.player.economy.money, runtime.player.inventory.items, runtime.shed.game_items, {key: job.__dict__ for key, job in runtime.owner.renovations.items()}, runtime.rewards))


def test_catalog_preserves_prices_and_approved_peephole_duration():
    r = _runtime()
    assert set(r.catalog) == set(EXPECTED)
    for code, expected in EXPECTED.items():
        assert (r.catalog[code].price, r.catalog[code].logs, r.catalog[code].days) == expected
    assert all(job.status == "unrequested" for job in r.owner.renovations.values())


@pytest.mark.parametrize("code", EXPECTED)
@pytest.mark.parametrize("day", [0, 30, 363])
def test_exact_once_payment_completion_and_motivation(code, day):
    price, logs, days = EXPECTED[code]
    r = _runtime(day=day, money=price, logs=logs)
    job = accept(r, code)
    assert r.owner.order_renovation(code)
    assert r.spent == [price] and r.player.economy.money == 0
    assert r.shed.game_items == ["old_axe_001", "soap_001"] + ["chopped_wood_001"] * 7
    assert r.player.inventory.items == {"lumber_001": 5}
    assert job.started_day == day and job.due_day == day + days
    assert job.paid_maravedies == price and job.used_logs == logs
    assert (r.calendar.hour, r.calendar.minute) == (9, 20)
    assert r.owner.active_renovation is job
    assert not r.owner.order_renovation(code)
    r.calendar.daysInGame = job.due_day - 1
    r.owner.finish_due_renovations()
    assert not r.owner.renovation_complete(code) and not r.rewards
    r.calendar.daysInGame += 1
    r.owner.finish_due_renovations()
    assert r.owner.renovation_complete(code) and r.owner.active_renovation is None
    assert len(r.rewards) == (6 if job.requester == "player" else 7)
    assert all(sum(amount for who, amount, _ in r.rewards if who == key) == (3 if key == job.requester else 1) for key in ("amanda", "melissa", "sandra", "clara", "liza", "georgett"))
    before = snapshot(r)
    r.owner.finish_due_renovations()
    assert not r.owner.order_renovation(code)
    assert snapshot(r) == before
    assert r.namespace["threads"]["melissaBatProblem"].num == 7


@pytest.mark.parametrize("code", EXPECTED)
@pytest.mark.parametrize("failure", ["unrequested", "requested", "declined", "poor", "closed", "busy"])
def test_rejected_orders_never_change_resources(code, failure):
    r = _runtime()
    job = accept(r, code)
    if failure in ("unrequested", "requested", "declined"):
        job.status = failure
    elif failure == "poor":
        r.player.economy.money = r.catalog[code].price - 1
    elif failure == "closed":
        r.namespace["rooms"]["StolyarWorkshop"].is_open = lambda: False
    else:
        other = next(key for key in r.catalog if key != code)
        accept(r, other)
        assert r.owner.order_renovation(other)
    before = snapshot(r)
    assert r.owner.renovation_order_error(code)
    assert not r.owner.order_renovation(code)
    assert snapshot(r) == before


@pytest.mark.parametrize("code", ["backyard", "shed", "guest_room"])
def test_split_or_carried_wood_cannot_replace_shed_logs(code):
    r = _runtime(logs=0)
    accept(r, code)
    before = snapshot(r)
    assert not r.owner.order_renovation(code)
    assert snapshot(r) == before


def test_next_job_can_start_after_completion():
    r = _runtime()
    accept(r, "peephole")
    accept(r, "shed")
    assert r.owner.order_renovation("peephole")
    assert not r.owner.order_renovation("shed")
    r.calendar.daysInGame += 1
    r.owner.finish_due_renovations()
    assert r.owner.order_renovation("shed")
    assert r.owner.renovation_complete("peephole")


def test_migration_preserves_paid_pending_completed_and_declined_projects():
    r = _runtime()
    del r.owner.renovations
    r.owner.renovation_due_days = {"backyard": 29, "shed": 34, "guest_room": 35}
    r.player.tavern_management.__dict__.update(slogan_state=2, client_room_hole=1, glory_hole=1)
    r.namespace["Melissa"].roof_repair_complete_day = 32
    r.namespace["Draupnir"].__dict__.update(slogan_quote_received=True, peep_hole_quote_received=True, glory_hole_quote_received=True)
    for who in ("melissa", "sandra", "clara"):
        r.namespace["threads"][who + "TavernRenovation"] = SimpleNamespace(num=2, completed=False, aborted=False)
    _exec_definitions("TractirSaveSync.rpy", {"updateSave_V100"}, r.namespace)
    cash, items, logs = r.player.economy.money, deepcopy(r.player.inventory.items), list(r.shed.game_items)
    r.namespace["updateSave_V100"]()
    assert r.owner.renovation_complete("peephole") and r.owner.renovation_complete("sign")
    assert r.owner.renovation_complete("backyard")
    assert r.owner.renovations["roof"].due_day == 32
    assert r.owner.renovations["glory_hole"].due_day == 31
    assert r.owner.renovations["shed"].due_day == 34 and r.owner.renovations["guest_room"].due_day == 35
    assert not hasattr(r.owner, "renovation_due_days")
    assert not r.player.tavern_management.__dict__
    assert not r.namespace["Draupnir"].__dict__ and not r.namespace["Melissa"].__dict__
    assert all(not key.endswith("TavernRenovation") for key in r.namespace["threads"])
    assert not r.rewards and r.player.economy.money == cash
    assert r.player.inventory.items == items and r.shed.game_items == logs
    assert not r.namespace["threads"]["tavernRenovations"].done[list(r.catalog).index("backyard")]
    before = snapshot(r)
    r.namespace["updateSave_V100"]()
    assert snapshot(r) == before


def test_migration_preserves_quote_and_explicit_refusal():
    r = _runtime()
    r.namespace["Draupnir"].slogan_quote_received = True
    r.namespace["threads"]["sandraTavernRenovation"] = SimpleNamespace(num=0, completed=False, aborted=True)
    _exec_definitions("TractirSaveSync.rpy", {"updateSave_V100"}, r.namespace)
    r.namespace["updateSave_V100"]()
    assert r.owner.renovations["sign"].status == "accepted"
    assert r.owner.renovations["shed"].status == "declined"
    assert not r.namespace["threads"]["tavernRenovations"].aborted


def test_live_code_has_no_retired_renovation_authorities():
    pattern = re.compile(r"(?:self|Melissa)\.roof_repair_complete_day|(?:self|Draupnir)\.(?:slogan_quote_received|peep_hole_quote_received|glory_hole_quote_received)|(?:self|player\.tavern_management)\.(?:slogan_state|client_room_hole|glory_hole)\b|renovation_due_days")
    for path in GAME.rglob("*.rpy"):
        if path.name == "TractirSaveSync.rpy":
            continue
        assert not pattern.search(path.read_text(encoding="utf-8-sig")), path


def test_authored_followups_use_existing_unordered_thread_not_dispatchers():
    source = (GAME / "Inn/TavernRenovations.rpy").read_text(encoding="utf-8-sig")
    assert 'UThreadData(0, "tavern", "Renovations"' in source
    assert "event_runtime.active_thread.seen(" in source
    assert not re.search(r"^label\s+\w*(?:Refresh|Rebuild|Dispatch)\w*", source, re.MULTILINE)
