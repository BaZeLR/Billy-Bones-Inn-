from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
SAVE_PATH = ROOT / "game/TractirSaveSync.rpy"


def _migration_namespace(attribute_month=-1, var_month=-1, already_traded=-1, installed=False):
    clara = SimpleNamespace(
        merchant_contact_unlocked=True,
        merchant_contact_month_key=attribute_month,
        market_day_roll_day=8,
        market_day_roll=True,
        market_evening_roll=True,
        rel=7,
        var={
            "merchant_contact_unlocked": True,
            "merchant_contact_month_key": var_month,
            "market_day_roll_day": 8,
            "market_day_roll": True,
            "retained_story_fact": 12,
        },
    )
    hordus = SimpleNamespace(known=False, last_trade_month=already_traded, last_meeting_day=-1)
    sofa = SimpleNamespace(installed=installed)
    tavern = SimpleNamespace(game_items=["fireplace", "cursed_sofa_001", "chest"])
    registered = {}
    thread_rebinds = []

    def register(data, info):
        registered[data] = info

    def object_id(item):
        return item if isinstance(item, str) else item.object_id

    namespace = {
        "Clara": clara,
        "Hordus": hordus,
        "HordusStaticData": "hordus",
        "Sofa": sofa,
        "SofaStaticData": "sofa",
        "people": SimpleNamespace(register=register),
        "rooms": {"TavernMain": tavern},
        "people_to_int": lambda value, default: int(value) if value is not None else default,
        "get_object_id": object_id,
        "_room_has_item_by_id": lambda room, item_id: any(object_id(row) == item_id for row in room.game_items),
        "game_object_registry": {"cursed_sofa_001": object(), "fireplace": object()},
        "CursedSofaObject": object(),
        "initThreads": lambda: thread_rebinds.append(True),
        "registered": registered,
        "thread_rebinds": thread_rebinds,
        "player": SimpleNamespace(money=320, inventory={"special_mushroom_001": 3}),
        "threads": {"claraForestSofa": SimpleNamespace(num=7, completed=False)},
    }
    source = SAVE_PATH.read_text(encoding="utf-8-sig")
    block = "    def updateSave_V92():" + source.split("    def updateSave_V92():", 1)[1].split(
        "    # Saved objects must be upgraded", 1
    )[0]
    exec(textwrap.dedent(block), namespace)
    return namespace


@pytest.mark.parametrize("attribute_month,var_month,already_traded,expected", [
    (108005, -1, -1, 108005),
    (-1, 108006, -1, 108006),
    (108005, 108006, -1, 108006),
    (108005, 108006, 108007, 108007),
    (-1, -1, -1, -1),
])
def test_old_monthly_cap_moves_once_without_auto_introduction(attribute_month, var_month, already_traded, expected):
    namespace = _migration_namespace(attribute_month, var_month, already_traded)
    namespace["updateSave_V92"]()
    assert namespace["Hordus"].last_trade_month == expected
    assert namespace["Hordus"].known is False
    assert namespace["Hordus"].last_meeting_day == -1
    for legacy in (namespace["Clara"].__dict__, namespace["Clara"].var):
        for key in ("merchant_contact_month_key", "merchant_contact_unlocked", "market_day_roll_day", "market_day_roll"):
            assert key not in legacy
    assert namespace["Clara"].market_evening_roll is True
    assert namespace["Clara"].var["retained_story_fact"] == 12


def test_installed_sofa_leaves_no_old_room_or_registry_owner():
    namespace = _migration_namespace()
    tavern = namespace["rooms"]["TavernMain"]
    tavern.game_items.append(SimpleNamespace(object_id="cursed_sofa_001"))
    namespace["updateSave_V92"]()
    assert namespace["Sofa"].installed is True
    assert tavern.game_items == ["fireplace", "chest"]
    assert "cursed_sofa_001" not in namespace["game_object_registry"]
    assert "fireplace" in namespace["game_object_registry"]
    assert "CursedSofaObject" not in namespace
    assert namespace["registered"]["hordus"] is namespace["Hordus"]
    assert namespace["registered"]["sofa"] is namespace["Sofa"]


@pytest.mark.parametrize("installed", [False, True])
def test_missing_old_sofa_preserves_new_owner_state(installed):
    namespace = _migration_namespace(installed=installed)
    namespace["rooms"]["TavernMain"].game_items = ["fireplace"]
    namespace["Clara"].var = None
    namespace["updateSave_V92"]()
    assert namespace["Sofa"].installed is installed


def test_migration_is_repeatable_and_keeps_money_inventory_and_story_progress():
    namespace = _migration_namespace(attribute_month=108003)
    thread = namespace["threads"]["claraForestSofa"]
    player = namespace["player"]
    for _ in range(2):
        namespace["updateSave_V92"]()
        assert namespace["Hordus"].last_trade_month == 108003
        assert namespace["Sofa"].installed is True
        assert namespace["threads"]["claraForestSofa"] is thread
        assert (thread.num, thread.completed) == (7, False)
        assert (player.money, player.inventory) == (320, {"special_mushroom_001": 3})
        assert namespace["Clara"].rel == 7
    assert len(namespace["thread_rebinds"]) == 2


def test_new_npcs_have_fresh_and_loaded_registration_paths():
    save_source = SAVE_PATH.read_text(encoding="utf-8-sig")
    people_source = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
    assert int(save_source.split("define currentVersion = ", 1)[1].splitlines()[0]) >= 104
    assert "if loaded_version < 93:\n            updateSave_V92()\n            loaded_version = 93" in save_source
    fresh = people_source.split("label InitGameNPCs:", 1)[1]
    assert "call register_hordus_secondary" in fresh
    assert "call register_nostar_secondary" in fresh
    assert "call register_sofa_secondary" in fresh
    assert "if loaded_version < 104:\n            updateSave_V103()\n            loaded_version = 104" in save_source
    assert "people.register(NostarStaticData, Nostar)" in save_source
    for key in ("merchant_contact_unlocked", "merchant_contact_month_key", "market_day_roll_day", "market_day_roll"):
        assert "Clara.%s =" % key not in save_source


def test_sofa_object_serialization_does_not_require_retired_action_functions():
    source = (ROOT / "game/Utilities/General/Classes/GameObjectTemplate.rpy").read_text(encoding="utf-8-sig")
    registry = {}
    namespace = {
        "game_object_registry": registry,
        "get_game_object": registry.get,
        "get_game_item": lambda item_id: None,
        "register_room_rule": lambda condition: condition,
    }
    for start, end in (
        ("    def restore_game_object_runtime", "    class RoomAction"),
        ("    class GameObject(object):", "    RoomObject = GameObject"),
    ):
        block = start + source.split(start, 1)[1].split(end, 1)[0]
        exec(textwrap.dedent(block), namespace)
    old_sofa = namespace["GameObject"](
        object_id="cursed_sofa_001", actions=[lambda: True], state={"saved": 1},
    )
    restore, args = old_sofa.__reduce__()
    registry.clear()
    assert args == ("cursed_sofa_001", {"state": {"saved": 1}, "hidden": False, "locked": False, "owner": ""})
    restored = restore(*args)
    assert restored.object_id == "cursed_sofa_001"
    assert restored.actions == []
    assert restored.state == {"saved": 1}
