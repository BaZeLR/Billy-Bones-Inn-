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


def _runtime(day=30, money=10000, logs=40, chopped=7, carried_logs=0, ready_for=""):
    calendar = SimpleNamespace(daysInGame=day, day=3, week=2, hour=9, minute=0)
    shed = SimpleNamespace(game_items=["old_axe_001", "soap_001"] + ["lumber_001"] * logs + ["chopped_wood_001"] * chopped)
    player = SimpleNamespace(
        economy=SimpleNamespace(money=money),
        inventory=SimpleNamespace(items={"lumber_001": carried_logs}),
        tavern_management=SimpleNamespace(slogan_state=0, client_room_hole=0, glory_hole=0),
    )
    spent = []

    def spend_money(amount):
        amount = int(amount)
        if player.economy.money < amount:
            return False
        player.economy.money -= amount
        spent.append(amount)
        return True

    player.spend_money = spend_money
    player.item_count = lambda key: player.inventory.items.get(key, 0)
    namespace = {
        "calendar_v2": calendar,
        "current_game_day": lambda: calendar.daysInGame,
        "player": player,
        "rooms": {"Shed": shed, "StolyarWorkshop": SimpleNamespace(is_open=lambda: True)},
        "get_object_id": lambda item: item if isinstance(item, str) else item.object_id,
        "player_to_int": lambda value, default=0: int(value) if value is not None else default,
        "threads": {},
        "_story_num_day": lambda: calendar.daysInGame,
        "_story_level_enabled": lambda *args: True,
    }
    _exec_definitions("Inn/TavernRenovations.rpy", {"TavernRenovationDefinition", "TAVERN_RENOVATIONS", "TavernInfo"}, namespace)
    _exec_definitions("Utilities/General/Common/Actions.rpy", {"_room_item_count_by_id", "_room_remove_item_by_id"}, namespace)
    namespace["tavern"] = namespace["TavernInfo"]()
    _exec_definitions("Utilities/General/Events/threads.rpy", {"ThreadInfo", "LThreadInfo"}, namespace)
    for project in namespace["TAVERN_RENOVATIONS"].values():
        data = SimpleNamespace(length=3, highlight=True, level=0, person=project.quest_giver, checkConditions=lambda: True)
        thread = namespace["LThreadInfo"](data)
        thread.enable()
        thread.advance()
        namespace["threads"][project.thread_name] = thread
    return SimpleNamespace(
        owner=namespace["tavern"], calendar=calendar, player=player,
        shed=shed, spent=spent, namespace=namespace,
        catalog=namespace["TAVERN_RENOVATIONS"],
    )


def _transaction_state(runtime):
    return (
        runtime.player.economy.money,
        list(runtime.shed.game_items),
        deepcopy(runtime.player.inventory.items),
        dict(runtime.owner.renovation_due_days),
        list(runtime.spent),
    )


def test_catalog_has_three_requested_renovations_without_second_window_purchase():
    runtime = _runtime()
    assert set(runtime.catalog) == set(EXPECTED)
    for code, expected in EXPECTED.items():
        definition = runtime.catalog[code]
        assert definition.code == code
        assert (definition.price, definition.logs, definition.days) == expected
        assert definition.title.strip() and definition.description.strip()
    assert runtime.owner.renovation_due_days == {}


@pytest.mark.parametrize("code", EXPECTED)
@pytest.mark.parametrize("day", [0, 30, 363])
def test_purchase_charges_exact_cost_once_and_uses_absolute_completion_day(code, day):
    price, logs, days = EXPECTED[code]
    runtime = _runtime(day=day, money=price, logs=logs, chopped=7, carried_logs=5, ready_for=code)
    before_due = dict(runtime.owner.renovation_due_days)
    assert runtime.owner.renovation_order_error(code) == ""
    assert runtime.owner.order_renovation(code) is True
    assert runtime.player.economy.money == 0
    assert runtime.spent == [price]
    assert runtime.shed.game_items == ["old_axe_001", "soap_001"] + ["chopped_wood_001"] * 7
    assert runtime.player.inventory.items == {"lumber_001": 5}
    assert runtime.owner.renovation_due_days == {**before_due, code: day + days}
    assert runtime.owner.renovation_days_left(code) == days
    assert runtime.owner.renovation_complete(code) is False


@pytest.mark.parametrize("code", EXPECTED)
@pytest.mark.parametrize("missing", ["money", "logs", "only_chopped", "only_carried"])
def test_failed_purchase_never_partially_charges_or_consumes_inventory(code, missing):
    price, logs, _ = EXPECTED[code]
    runtime = _runtime(
        money=price - 1 if missing == "money" else price,
        logs=logs if missing == "money" else logs - 1 if missing == "logs" else 0,
        chopped=100 if missing == "only_chopped" else 0,
        carried_logs=100 if missing == "only_carried" else 0,
        ready_for=code,
    )
    before = _transaction_state(runtime)
    assert runtime.owner.renovation_order_error(code)
    assert runtime.owner.order_renovation(code) is False
    assert _transaction_state(runtime) == before


@pytest.mark.parametrize("code", EXPECTED)
def test_duplicate_pending_and_completed_orders_cannot_charge_again(code):
    runtime = _runtime(ready_for=code)
    assert runtime.owner.order_renovation(code)
    before = _transaction_state(runtime)
    assert runtime.owner.renovation_order_error(code)
    assert runtime.owner.order_renovation(code) is False
    assert _transaction_state(runtime) == before
    runtime.calendar.daysInGame = runtime.owner.renovation_due_days[code]
    assert runtime.owner.renovation_complete(code)
    assert runtime.owner.renovation_order_error(code)
    assert runtime.owner.order_renovation(code) is False
    assert _transaction_state(runtime) == before


@pytest.mark.parametrize("code", EXPECTED)
def test_completion_and_explicit_day_queries_do_not_mutate_authoritative_dates(code):
    runtime = _runtime(day=100, ready_for=code)
    assert runtime.owner.order_renovation(code)
    due = runtime.owner.renovation_due_days[code]
    before = _transaction_state(runtime)
    for day, complete, days_left in [(due - 1, False, 1), (due, True, 0), (due + 40, True, 0)]:
        runtime.calendar.daysInGame = day
        assert runtime.owner.renovation_complete(code) is complete
        assert runtime.owner.renovation_days_left(code) == days_left
    assert runtime.owner.renovation_complete(code, due - 1) is False
    assert runtime.owner.renovation_complete(code, due) is True
    assert _transaction_state(runtime) == before


def test_day_of_month_alone_never_finishes_construction():
    runtime = _runtime(day=0)
    assert runtime.owner.order_renovation("shed")
    runtime.calendar.day = 28
    assert runtime.owner.renovation_complete("shed") is False
    assert runtime.owner.renovation_days_left("shed") == 4


def test_unpurchased_and_unknown_projects_are_not_complete():
    runtime = _runtime()
    before = _transaction_state(runtime)
    assert runtime.owner.renovation_complete("not_a_project") is False
    assert all(not runtime.owner.renovation_complete(code) for code in EXPECTED)
    assert _transaction_state(runtime) == before


def test_new_projects_do_not_modify_legacy_upgrade_ownership():
    runtime = _runtime()
    runtime.player.tavern_management.slogan_state = 2
    runtime.player.tavern_management.client_room_hole = 1
    runtime.player.tavern_management.glory_hole = 2
    before = deepcopy(runtime.player.tavern_management.__dict__)
    for code in EXPECTED:
        assert runtime.owner.order_renovation(code)
    assert set(runtime.owner.renovation_due_days) == set(EXPECTED)
    assert before == runtime.player.tavern_management.__dict__
    assert not hasattr(runtime.player.tavern_management, "renovation_due_days")


def test_quest_givers_link_to_existing_thread_objects():
    runtime = _runtime()
    assert runtime.catalog["backyard"].quest_giver == "melissa"
    assert runtime.catalog["shed"].quest_giver == "sandra"
    assert runtime.catalog["guest_room"].quest_giver == "clara"
    for project in runtime.catalog.values():
        assert project.thread_name in runtime.namespace["threads"]
        assert project.order_visible
        assert not hasattr(project, "is_hidden")


@pytest.mark.parametrize("code", EXPECTED)
@pytest.mark.parametrize("state", ["not_requested", "aborted", "completed"])
def test_unaccepted_aborted_and_completed_quests_cannot_charge(code, state):
    runtime = _runtime()
    thread = runtime.namespace["threads"][runtime.catalog[code].thread_name]
    if state == "not_requested":
        thread.reset()
    elif state == "aborted":
        thread.abort()
    else:
        thread.advance()
        thread.complete()
    before = _transaction_state(runtime)
    assert runtime.owner.renovation_order_error(code)
    assert runtime.owner.order_renovation(code) is False
    assert _transaction_state(runtime) == before


def test_observation_window_is_not_a_second_construction_project():
    runtime = _runtime()
    runtime.player.tavern_management.client_room_hole = 1
    before = _transaction_state(runtime)
    assert "player_peephole" not in runtime.catalog
    assert runtime.owner.order_renovation("guest_room")
    runtime.calendar.daysInGame = runtime.owner.renovation_due_days["guest_room"]
    assert runtime.player.tavern_management.client_room_hole == 1


def test_closed_workshop_does_not_take_payment_or_materials():
    runtime = _runtime()
    runtime.namespace["rooms"]["StolyarWorkshop"].is_open = lambda: False
    before = _transaction_state(runtime)
    assert runtime.owner.renovation_order_error("backyard")
    assert runtime.owner.order_renovation("backyard") is False
    assert _transaction_state(runtime) == before


def test_serialized_owner_restores_pending_dates_without_a_second_progress_store():
    runtime = _runtime()
    assert runtime.owner.order_renovation("backyard")
    restored = runtime.namespace["TavernInfo"].__new__(runtime.namespace["TavernInfo"])
    restored.__dict__.update(deepcopy(runtime.owner.__dict__))
    runtime.namespace["tavern"] = restored
    assert restored.renovation_due_days == {"backyard": 33}
    assert restored.renovation_days_left("backyard") == 3
    runtime.calendar.daysInGame = 33
    assert restored.renovation_complete("backyard") is True


def test_new_labels_are_authored_flow_not_refresh_or_dispatch_layers():
    source = (GAME / "Inn/TavernRenovations.rpy").read_text(encoding="utf-8-sig")
    assert "label DraupnirRenovations:" in source
    assert "label DraupnirRenovationOrder(" in source
    assert "menu:" in source
    assert "call screen main_ui" not in source
    assert not re.search(r"^label\s+\w*(?:Refresh|Rebuild|Dispatch)\w*", source, re.MULTILINE)
