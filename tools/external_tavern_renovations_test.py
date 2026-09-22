#!/usr/bin/env python3
"""Check renovations in a copied native Ren'Py project with temporary saves."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import external_tavern_premium_test as isolated


TEST_RPY = r'''
init python:
    def external_renovation_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_renovation_button(prefix):
        index = next(index for index, caption in enumerate(external_renovation_choices()) if caption.startswith(prefix))
        return "choice_panel_button_%d" % index

    def external_renovation_prepare():
        for thread in threads.values():
            thread.abort()
        event_runtime.available.clear()
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        tavern.renovation_due_days = {}
        for project in TAVERN_RENOVATIONS.values():
            project.is_hidden = True
        rooms.get("ShedWashroom").is_hidden = True
        player.set_money(5000)
        player.inventory.items["lumber_001"] = 5
        player.inventory.items["chopped_wood_001"] = 4
        shed = rooms.get("Shed")
        shed.game_items = [item for item in shed.game_items if get_object_id(item) not in ("lumber_001", "chopped_wood_001")]
        _room_add_item_units(shed, "lumber_001", 40)
        _room_add_item_units(shed, "chopped_wood_001", 7)
        calendar_v2.daysInGame = 30
        calendar_v2.week = 2
        calendar_v2.hour = 9
        calendar_v2.minute = 0
        rooms.enter("Shed")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_items = []
        scene_runtime.picture = shed_picture()
        scene_runtime.text = "EXTERNAL_RENOVATION_ORIGIN"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

testsuite global:
    teardown:
        exit

testcase external_renovation_defined_but_hidden_without_conversations:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        assert rooms.get("ShedWashroom").is_hidden
        assert rooms.get("ShedWashroom").descriptions[0].text
        assert rooms.get("ShedWashroom").exits[0].target == "Shed"
        assert "shed_wash_tub" in rooms.get("ShedWashroom").game_items
        assert not any(exit.target == "ShedWashroom" for exit in rooms.get("Shed").visible_exits())
        assert renpy.has_label("DraupnirRenovations")
        assert all(project.is_hidden for project in TAVERN_RENOVATIONS.values())
        assert not tavern.order_renovation("shed")
        assert not renpy.has_label("story_tavern_bathroom_request")
        assert not any(name in threads for name in ("tavernBathroomRenovation", "tavernBackyardRenovation", "tavernGuestRoomRenovation"))
        assert TAVERN_RENOVATIONS["backyard"].quest_giver == "melissa"
        assert TAVERN_RENOVATIONS["shed"].quest_giver == "sandra"
        assert TAVERN_RENOVATIONS["guest_room"].quest_giver == "clara"
        tavern.renovation_due_days["shed"] = 30
        assert not any(exit.target == "ShedWashroom" for exit in rooms.get("Shed").visible_exits())
    run Jump("ShedWashroom")
    advance until eval (rooms.current_code == "Shed" and scene_runtime.picture == shed_picture()) timeout 20.0

testcase external_renovation_prepared_owner_charges_once_without_activating_rooms:
    parameter code = ["backyard", "shed", "guest_room", "player_peephole"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        if code == "player_peephole":
            tavern.renovation_due_days["guest_room"] = 30
        definition = TAVERN_RENOVATIONS[code]
        definition.is_hidden = False
        assert tavern.order_renovation(code)
        assert player.economy.money == 5000 - definition.price
        assert _room_item_count_by_id(rooms.get("Shed"), "lumber_001") == 40 - definition.logs
        assert _room_item_count_by_id(rooms.get("Shed"), "chopped_wood_001") == 7
        assert player.item_count("lumber_001") == 5
        assert player.item_count("chopped_wood_001") == 4
        assert not tavern.renovation_complete(code)
        assert not tavern.order_renovation(code)
        calendar_v2.daysInGame = 30 + definition.days
        assert tavern.renovation_complete(code)
        assert not tavern.order_renovation(code)
        assert player.economy.money == 5000 - definition.price
        assert rooms.get("ShedWashroom").is_hidden

testcase external_renovation_save_migration_preserves_supplies_and_hidden_room:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        TAVERN_RENOVATIONS["backyard"].is_hidden = False
        assert tavern.order_renovation("backyard")
        rooms.get("Shed").state["renovation_test_marker"] = "preserve"
        before_items = list(rooms.get("Shed").game_items)
        before_dates = dict(tavern.renovation_due_days)
        updateSave_V93()
        updateSave_V93()
        assert rooms.get("Shed").game_items == before_items
        assert rooms.get("Shed").state["renovation_test_marker"] == "preserve"
        assert tavern.renovation_due_days == before_dates
        assert rooms.get("ShedWashroom").is_hidden
        assert len([exit for exit in rooms.get("Shed").exits if exit.target == "ShedWashroom"]) == 1
        import pickle
        restored = pickle.loads(pickle.dumps(tavern))
        assert restored.renovation_due_days == before_dates

testcase external_renovation_hidden_room_preview_bath_and_navigation:
    parameter hour = [9, 22]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        tavern.renovation_due_days["shed"] = 30
        rooms.get("ShedWashroom").is_hidden = False
        calendar_v2.hour = hour
    run Jump("Shed")
    advance until eval (rooms.current_code == "Shed" and scene_runtime.picture == shed_picture()) timeout 20.0
    run (next(item.action for item in rooms.current.build_exit_items() if "купальню" in item.caption))
    advance until eval (rooms.current_code == "ShedWashroom" and scene_runtime.picture == shed_washroom_picture()) timeout 20.0
    assert eval (scene_runtime.picture.endswith("washroom.png" if hour == 9 else "washroom_night.png")) timeout 5.0
    $ _renovation_bath_origin = main_ui_context_snapshot()
    run Call("ShedWashroomBath")
    advance until screen "choice" timeout 20.0
    click id (external_renovation_button("Вымыться")) pos (0.5, 0.5)
    advance until eval ("Назад" in external_renovation_choices()) timeout 20.0
    assert eval (calendar_v2.hour == hour and calendar_v2.minute == 16) timeout 5.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _renovation_bath_origin and rooms.current_code == "ShedWashroom") timeout 5.0
    run (rooms.current.build_exit_items()[0].action)
    advance until eval (rooms.current_code == "Shed" and scene_runtime.picture == shed_picture()) timeout 20.0
    assert eval (calendar_v2.minute == 17) timeout 5.0

testcase external_renovation_object_menu_returns_picture_text_and_navigation:
    parameter label_name = ["ShedRuinedStove", "ShedHotWaterStove", "TavernMyRoomPeephole"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    $ _renovation_origin = main_ui_context_snapshot()
    run Call(label_name)
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and main_ui_runtime.mode == "event") timeout 5.0
    click id (external_renovation_button("Закрыть окошко" if label_name == "TavernMyRoomPeephole" else "Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _renovation_origin and main_ui_runtime.scene_origin is None) timeout 5.0

testcase external_renovation_draupnir_options_exist_but_are_hidden:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    run Call("IntDraupnirTalk")
    advance until screen "choice" timeout 20.0
    assert eval ("Обустройство трактира" not in external_renovation_choices()) timeout 5.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    run Call("DraupnirRenovations")
    advance until screen "choice" timeout 20.0
    assert eval (external_renovation_choices() == ["Назад"]) timeout 5.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
'''


def build_temp_project(root: Path, temp_root: Path) -> Path:
    """Copy scripts/data; only immutable media directories point at the workspace."""
    project = temp_root / "TractirExternalRenovationsProject"
    game = project / "game"
    game.mkdir(parents=True)
    for entry in (root / "game").iterdir():
        target = game / entry.name
        if entry.name in {"cache", "__pycache__", "saves", "saves_test_run"}:
            continue
        if entry.is_dir() and entry.name in {"images", "audio", "music", "sounds", "gui", "fonts"}:
            isolated.junction_dir(entry, target)
        elif entry.is_dir():
            shutil.copytree(entry, target, ignore=shutil.ignore_patterns("*.rpyc", "*.rpymc", "*.pyc", "__pycache__"))
        elif entry.suffix.lower() not in {".rpyc", ".rpymc", ".pyc"}:
            shutil.copy2(entry, target)
    (game / "_external_tavern_renovations_test.rpy").write_text(TEST_RPY, encoding="utf-8")
    return project


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--compile-lint", action="store_true")
    args = parser.parse_args()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.is_file():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_renovations_"))
    environment = dict(os.environ)
    try:
        project = build_temp_project(isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary renovation test project: {project}", flush=True)
        commands = [["compile"], ["lint"]] if args.compile_lint else []
        commands.append(["test", "--hide-execution", "all", "--report-detailed"])
        for command in commands:
            result = subprocess.run(
                [str(renpy_exe), str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=environment,
            )
            log = project / f"renovations-{command[0]}.log"
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            if result.stdout:
                isolated.safe_print(result.stdout)
            if result.returncode:
                return int(result.returncode)
        return 0
    except subprocess.TimeoutExpired as exc:
        print(f"Ren'Py renovation checks timed out after {args.timeout} seconds: {exc}", flush=True)
        return 124
    finally:
        if args.keep_temp:
            print(f"Keeping temporary renovation test project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_renovations_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
