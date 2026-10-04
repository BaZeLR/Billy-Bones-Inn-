import ast
from pathlib import Path
import textwrap
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
PURCHASE = ROOT / "game/NPC/Girls/Common/GirlDressSuggest.rpy"
MY_ROOM = ROOT / "game/Inn/TavernMyRoom.rpy"


def purchase_function():
    source = PURCHASE.read_text(encoding="utf-8-sig")
    body = source.split("init python:\n", 1)[1].split("\nlabel GirlDressSuggest", 1)[0]
    tree = ast.parse(textwrap.dedent(body))
    node = next(row for row in tree.body if isinstance(row, ast.FunctionDef) and row.name == "_gds_apply_purchase")
    namespace = {}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(PURCHASE), "exec"), namespace)
    return namespace["_gds_apply_purchase"]


def purchase_harness(deferred):
    retired = []
    spent = []
    wardrobe = SimpleNamespace(
        day_garment_needing_attention=lambda maximum, replacement: "workdress",
        retire_replaced_item=lambda old, new: retired.append((old, new)) or True,
    )
    girl = SimpleNamespace(wardrobe=wardrobe)
    shop = SimpleNamespace(produced="", buyer="", replacement_old_item="")
    player = SimpleNamespace(
        spend_money=lambda cost: spent.append(cost),
        appearance=SimpleNamespace(girl_dresses_bought=0),
    )
    chest = []
    function = purchase_function()
    function.__globals__.update(
        people=SimpleNamespace(get_info=lambda name: girl),
        _gds_dress_cost=lambda code: 120,
        player=player,
        dress_shop=shop,
        tavern_my_room_store_retired_clothing=lambda code: chest.append(code),
        household_mark_revealing_dress_order=lambda *args: None,
        household_schedule_outfit_reward=lambda *args: None,
    )
    function("melissa", "workdress", set_produced=deferred)
    return shop, spent, retired, chest


def test_order_defers_transfer_until_delivery():
    shop, spent, retired, chest = purchase_harness(True)
    assert spent == [120]
    assert shop.produced == "workdress"
    assert shop.buyer == "melissa"
    assert shop.replacement_old_item == "workdress"
    assert retired == []
    assert chest == []


def test_immediate_replacement_moves_old_copy_to_chest():
    shop, spent, retired, chest = purchase_harness(False)
    assert spent == [120]
    assert shop.produced == ""
    assert retired == [("workdress", "workdress")]
    assert chest == ["workdress"]


def test_chest_keeps_multiple_retired_copies_of_the_same_garment():
    source = MY_ROOM.read_text(encoding="utf-8-sig")
    body = source.split("    def tavern_my_room_store_retired_clothing(dress_code):", 1)[1]
    body = "def tavern_my_room_store_retired_clothing(dress_code):" + body.split("\n    def ", 1)[0]
    namespace = {}
    exec(compile(ast.parse(body), str(MY_ROOM), "exec"), namespace)
    chest = SimpleNamespace(state={})
    function = namespace["tavern_my_room_store_retired_clothing"]
    function.__globals__["tavern_my_room_get_object"] = lambda code: chest
    assert function("workdress")
    assert function("workdress")
    assert chest.state["retired_clothes"] == ["workdress", "workdress"]
