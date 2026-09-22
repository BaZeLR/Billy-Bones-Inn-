#!/usr/bin/env python3
"""Exercise spring entry, bottle conversion and native return in an isolated copy."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_water_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_water_button():
        index = next(index for index, item in enumerate(main_ui_runtime.action_items) if item.caption == "Набрать родниковую воду")
        return "choice_panel_button_%d" % index

    def external_water_feedback_count():
        from renpy.text.text import Text
        rows = []
        seen = set()
        def collect(displayable):
            if id(displayable) in seen or not isinstance(displayable, Text):
                return
            seen.add(id(displayable))
            rows.append("".join(part for part in displayable.text if isinstance(part, str)))
        for name in ("main_ui", "choice", "say"):
            screen = renpy.get_screen(name)
            if screen is not None:
                screen.visit_all(collect)
        return sum(row.count(scene_runtime.text) for row in rows)

    def external_water_prepare(bottles=1, dusk=False):
        for thread in threads.values():
            thread.abort()
        event_runtime.available.clear()
        event_runtime.active_thread = None
        event_runtime.evaluation_time = None
        daily_events.rows = []
        player.tavern_management.breakfast.today = True
        player.tavern_management.breakfast.event_active = False
        calendar_v2.daysInGame = 30
        calendar_v2.week = 2
        calendar_v2.hour = 19 if dusk else 8
        calendar_v2.minute = 30 if dusk else 0
        player.inventory.items.pop("empty_bottle_001", None)
        if bottles:
            player.inventory.items["empty_bottle_001"] = bottles
        player.inventory.items["spring_water_001"] = 2
        player.inventory.items["cork_001"] = 4
        player.set_money(123)
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.overlay = ""

    def external_water_uncharged():
        return (calendar_v2.daysInGame, calendar_v2.hour, calendar_v2.minute, player.economy.money, player.item_count("cork_001")) == (30, 8, 0, 123, 4)

label ExternalWaterBlockedCall:
    $ _external_water_returned = False
    call ForestSpringFillBottle
    $ _external_water_returned = True
    return

testsuite global:
    teardown:
        exit

testcase external_water_real_spring_inventory_and_picture_return:
    parameter bottles = [0, 1, 3]
    $ daily_events.rows = []
    $ player.tavern_management.breakfast.today = True
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_water_prepare(bottles)
    run Jump("ForestSpring")
    advance until eval (rooms.current_code == "ForestSpring" and main_ui_runtime.action_title == "Родник") timeout 20.0
    python:
        _external_water_origin = main_ui_context_snapshot()
        _external_water_expected = dict(player.inventory.items)
        if bottles:
            _external_water_expected["spring_water_001"] += 1
            if bottles == 1:
                _external_water_expected.pop("empty_bottle_001")
            else:
                _external_water_expected["empty_bottle_001"] -= 1
    assert eval (get_game_item("spring_water_001") is SpringWaterItem and SpringWaterItem.stackable) timeout 5.0
    assert eval (sum(item.caption == "Набрать родниковую воду" for item in main_ui_runtime.action_items) == 1) timeout 5.0
    click id (external_water_button()) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (external_water_choices() == ["Назад"] and main_ui_runtime.mode == "event") timeout 5.0
    assert eval (dict(player.inventory.items) == _external_water_expected and external_water_uncharged()) timeout 5.0
    assert eval (scene_runtime.picture == _external_water_origin["picture"] and rooms.current_code == "ForestSpring") timeout 5.0
    assert eval (("нужна пустая бутылка" in scene_runtime.text) if bottles == 0 else ("наполняете" in scene_runtime.text)) timeout 5.0
    assert eval (external_water_feedback_count() == 1) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene" and not external_water_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _external_water_origin and main_ui_runtime.scene_origin is None) timeout 5.0
    assert eval (dict(player.inventory.items) == _external_water_expected and external_water_uncharged()) timeout 5.0

testcase external_water_repeated_clicks_conserve_bottles:
    $ daily_events.rows = []
    $ player.tavern_management.breakfast.today = True
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_water_prepare(2)
    run Jump("ForestSpring")
    advance until eval (rooms.current_code == "ForestSpring" and main_ui_runtime.action_title == "Родник") timeout 20.0
    $ _external_water_origin = main_ui_context_snapshot()
    click id (external_water_button()) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (player.item_count("empty_bottle_001") == 1 and player.item_count("spring_water_001") == 3) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene") timeout 20.0
    click id (external_water_button()) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (player.item_count("empty_bottle_001") == 0 and player.item_count("spring_water_001") == 4) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene") timeout 20.0
    click id (external_water_button()) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (player.item_count("empty_bottle_001") == 0 and player.item_count("spring_water_001") == 4 and "нужна пустая бутылка" in scene_runtime.text) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene") timeout 20.0
    assert eval (main_ui_context_snapshot() == _external_water_origin and external_water_uncharged()) timeout 5.0

testcase external_water_wrong_room_and_dusk_preserve_inventory:
    parameter state = ["outside", "dusk"]
    $ daily_events.rows = []
    $ player.tavern_management.breakfast.today = True
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_water_prepare(1, state == "dusk")
    $ _external_water_room = "ForestLake" if state == "outside" else "ForestSpring"
    run Jump(_external_water_room)
    advance until eval (rooms.current_code == _external_water_room and main_ui_runtime.action_title in ("Родник", "Озеро")) timeout 20.0
    $ _external_water_origin = main_ui_context_snapshot()
    $ _external_water_inventory = dict(player.inventory.items)
    assert eval (not any(item.caption == "Набрать родниковую воду" for item in main_ui_runtime.action_items)) timeout 5.0
    run Call("ExternalWaterBlockedCall")
    advance until eval (_external_water_returned) timeout 20.0
    assert eval (dict(player.inventory.items) == _external_water_inventory and main_ui_context_snapshot() == _external_water_origin) timeout 5.0
    assert eval (not external_water_choices() and main_ui_runtime.scene_origin is None) timeout 5.0
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--compile-lint", action="store_true")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_spring_water_"))
    try:
        copied.TEST_RPY = TEST_RPY
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary spring water test project: {project}", flush=True)
        commands = [["test", "--hide-execution", "all", "--report-detailed"]]
        if args.compile_lint:
            commands.extend([["compile"], ["lint"]])
        for command in commands:
            result = subprocess.run(
                [args.renpy, str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            log = project / f"spring-water-{command[0]}.log"
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            copied.isolated.safe_print(result.stdout if command[0] != "lint" else "\n".join(result.stdout.splitlines()[-15:]))
            if result.returncode:
                return int(result.returncode)
        return 0
    finally:
        if args.keep_temp:
            print(f"Keeping temporary spring water test project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_spring_water_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
