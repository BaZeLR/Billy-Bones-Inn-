from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest

from tests.test_tavern_renovations_runtime import _exec_definitions


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Utilities/General/Screens/main_layout.rpy"


@pytest.mark.parametrize("mode", ["scene", "event", "talk"])
def test_native_paragraph_remains_with_its_next_menu_in_every_label_context(mode):
    scene = SimpleNamespace(text="Opening paragraph", location_text="Room description")
    ui = SimpleNamespace(mode=mode, action_items=[object()])
    items = ui.action_items
    say = SimpleNamespace(scope={"what": "First fitting step"})
    namespace = dict(scene_runtime=scene, main_ui_runtime=ui,
                     renpy_module=SimpleNamespace(get_screen=lambda name: say if name == "say" else object()))
    _exec_definitions("Utilities/General/Screens/main_layout.rpy", {"main_ui_dialogue_text"}, namespace)
    callback = namespace["main_ui_dialogue_text"]
    # This project's Ren'Py callback compatibility mode does not pass `what`.
    callback("show_done")
    assert scene.text == "First fitting step"
    say.scope["what"] = "Reaction before the next choice"
    callback("show_done")
    callback("end", what="")
    assert scene.text == "Reaction before the next choice"
    assert scene.location_text == "Room description"
    assert ui.mode == mode and ui.action_items is items


@pytest.mark.parametrize("event,interact,what,visible", [
    ("end", True, "Unplayed text", True),
    ("show_done", False, "Predicted text", True),
    ("show_done", True, "", True),
    ("show_done", True, "Non-HUD text", False),
])
def test_only_played_native_dialogue_updates_the_existing_hud_text(event, interact, what, visible):
    scene = SimpleNamespace(text="Current paragraph")
    say = SimpleNamespace(scope={"what": what})
    namespace = dict(scene_runtime=scene, main_ui_runtime=SimpleNamespace(mode="scene"),
                     renpy_module=SimpleNamespace(get_screen=lambda name: (say if name == "say" else object()) if visible else None))
    _exec_definitions("Utilities/General/Screens/main_layout.rpy", {"main_ui_dialogue_text"}, namespace)
    namespace["main_ui_dialogue_text"](event, interact=interact, what=what)
    assert scene.text == "Current paragraph"


@pytest.mark.parametrize("mode", ["scene", "event", "talk", "mc", "tavern", "fight"])
def test_load_preserves_active_menu_and_return_context(mode):
    source = SOURCE.read_text(encoding="utf-8-sig")
    code = textwrap.dedent("    def tractir_after_load_restore_ui():" + source.split(
        "    def tractir_after_load_restore_ui():", 1
    )[1].split("init -5:", 1)[0])
    menu = [object()]
    origin = {"mode": "scene", "items": [object()]}
    ui = SimpleNamespace(mode=mode, action_items=menu, action_content=None,
                         object_id="myroom_window_001", scene_origin=origin,
                         talk_origin=origin, card_origin=origin, action_title="Owned menu")
    namespace = dict(main_ui_runtime=ui, rooms=SimpleNamespace(current_code="TavernMyRoom"))
    exec(code, namespace)
    namespace["tractir_after_load_restore_ui"]()
    assert ui.mode == mode
    assert ui.action_items is menu
    assert ui.scene_origin is origin
    assert ui.talk_origin is origin
    assert ui.card_origin is origin
    assert ui.object_id == "myroom_window_001"
    assert ui.action_title == "Owned menu"


def test_room_fallback_does_not_supply_actions_to_non_room_contexts():
    source = SOURCE.read_text(encoding="utf-8-sig")
    panel = source.split("screen current_action_panel(", 1)[1].split("screen main_ui_status_item", 1)[0]
    assert 'elif main_ui_runtime.mode == "scene" and rooms.current is not None:' in panel
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    assert "tractir_save_clear_room_ui_cache" not in migration


@pytest.mark.parametrize("mode", ["event", "talk", "mc", "fight"])
def test_load_does_not_fill_empty_non_room_menus_with_navigation(mode):
    source = SOURCE.read_text(encoding="utf-8-sig")
    code = textwrap.dedent("    def tractir_after_load_restore_ui():" + source.split(
        "    def tractir_after_load_restore_ui():", 1
    )[1].split("init -5:", 1)[0])
    ui = SimpleNamespace(mode=mode, action_items=[], action_content=None)
    namespace = dict(main_ui_runtime=ui, rooms=SimpleNamespace(current_code="TavernMyRoom"))
    exec(code, namespace)
    namespace["tractir_after_load_restore_ui"]()
    assert ui.mode == mode
    assert ui.action_items == []
