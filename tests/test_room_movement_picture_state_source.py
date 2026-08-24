from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (PROJECT_ROOT / path).read_text(encoding="utf-8-sig")


def test_movement_action_clears_selection_before_ui_jump():
    source = read_rel("game/Utilities/Time/TimeTurnSystem.rpy")
    movement = source.split('def apply_movement_time(movement_minutes=0, destination=""):', 1)[1]
    action_builder = source.split('def movement_actions(target_label="", movement_minutes=0):', 1)[1].split("def apply_movement_time", 1)[0]

    assert 'main_ui_runtime.object_id = ""' in movement
    assert 'main_ui_runtime.girl_key = ""' in movement
    assert "jump expression" not in movement
    assert 'Function(apply_movement_time, movement_cost, destination), Jump(destination)' in action_builder
    assert "label MoveToRoom" not in source
    assert "label AdvanceMovementTime" not in source


def test_room_event_gate_does_not_overwrite_room_authored_picture():
    source = read_rel("game/Utilities/General/Common/RoomEnterPipeline.rpy")

    assert "scene_runtime.picture" not in source
    assert "bg_picture" not in source


def test_external_room_actions_use_real_clicks_not_python_dispatcher():
    source = read_rel("tools/external_click_play_test.py")

    assert "external_all_room_action_clicks" in source
    assert "click id FULL_CLICK_BUTTON_ID" in source
    assert "external_room_action_dispatch" not in source
    assert "ACTION_AUDIT_DISPATCHED" not in source
    assert "audit_run_current_action" not in source


def test_vscene_lint_checks_literal_assets_without_evaluating_runtime_state():
    source = read_rel("game/01vscene.rpy")
    lint = source.split("def vscene_lint(obj):", 1)[1].split(
        "renpy.register_statement", 1
    )[0]

    assert 'source = str(expression or "").strip()' in lint
    assert "source[0] not in" in lint
    assert "return" in lint
    assert "renpy.loadable(filename)" in lint
    assert 'renpy.error("Unable to find %s" % filename)' in lint


def test_room_screens_and_shop_results_do_not_reenter_their_location():
    storage = read_rel("game/Inn/TavernStorage.rpy")
    street = read_rel("game/Town/StreetTavern.rpy")
    grocery = read_rel("game/Town/GroceryStore.rpy")
    wine = read_rel("game/Town/WineStore.rpy")
    grocery_apply = grocery.split("label GroceryStoreBuyStockApply", 1)[1].split(
        "label GroceryStoreBuyFancyNightBowl", 1
    )[0]
    wine_apply = wine.split("label WineStoreBuyStockApply", 1)[1]

    assert "jump TavernStorage" not in storage
    assert "jump StreetTavern" not in street.split("label street_tavern_menu", 1)[0]
    assert "jump GroceryStore" not in grocery_apply
    assert "jump WineStore" not in wine_apply
    assert "call GroceryStoreBuyStockMenu(True)" in grocery_apply
    assert 'call WineStoreObjectMenu("wine_stock", True)' in wine_apply
