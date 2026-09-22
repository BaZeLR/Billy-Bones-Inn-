#!/usr/bin/env python3
"""Click breakfast reconciliation in copied scripts with isolated temporary saves."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_reconcile_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_reconcile_button(caption):
        return "choice_panel_button_%d" % external_reconcile_choices().index(caption)

    def external_reconcile_text_count():
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
        return sum(row.count(scene_runtime.text) for row in rows) if scene_runtime.text else 0

    def external_reconcile_stats():
        return (
            tuple((girl.rel, girl.openness, girl.corruption, girl.arousal_value(), girl.mana,
                   girl.talked_today, girl.asked_today) for girl in (Sandra, Amanda, Melissa)),
            player.economy.money, player.condition.fun,
            calendar_v2.daysInGame, calendar_v2.hour, calendar_v2.minute,
        )

    def external_reconcile_at_scene():
        return (main_ui_runtime.mode == "event"
                and event_runtime.active_thread is threads["sandraAmandaReconciliation"]
                and external_reconcile_choices() == ["Продолжить"])

    def external_reconcile_prepare(stage=0, booklet=False):
        for thread in threads.values():
            thread.abort()
        event_runtime.available.clear()
        event_runtime.active_thread = None
        event_runtime.evaluation_time = None
        event_runtime.fired_keys_today = []
        daily_events.rows = []
        calendar_v2.daysInGame = 30
        calendar_v2.week = 2
        calendar_v2.hour = 8
        calendar_v2.minute = 0
        household.morning_state.clear()
        player.tavern_management.breakfast.today = False
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        thread = threads["sandraAmandaReconciliation"]
        thread.reset()
        thread.advanceTo(stage)
        thread.day = 28 if stage == 1 else 0
        bat = threads["melissaBatProblem"]
        bat.advanceTo(8 if booklet else 9)
        bat.aborted = not booklet
        bat.metconds = True
        bat.day = 29
        Melissa.roof_repair_complete_day = 28
        rooms.enter("TavernKitchen")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.overlay = ""
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_title = "EXTERNAL_BREAKFAST_ORIGIN"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []
        scene_runtime.picture = tavern_kitchen_picture()
        scene_runtime.text = "EXTERNAL_BREAKFAST_ORIGIN_TEXT"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

testsuite global:
    teardown:
        exit
'''


def paragraph_count(label: str) -> int:
    source = (copied.isolated.project_root() / "game/NPC/Girls/Sandra/SandraEvents.rpy").read_text(encoding="utf-8-sig")
    body = source.split(f"label {label}:", 1)[1].split("\nlabel ", 1)[0]
    count = len(re.findall(r'^    menu:\s*$', body, re.MULTILINE))
    assert count > 0
    assert len(re.findall(r'^        "Продолжить":\s*$', body, re.MULTILINE)) == count
    return count


def direct_scene_case(stage: int, label: str) -> str:
    case = r'''
testcase external_reconcile_direct_stage_STAGE_preserves_context_and_stats:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_reconcile_prepare(STAGE)
    $ player.tavern_management.breakfast.event_active = True
    $ player.tavern_management.breakfast.present_ids = ["sandra", "amanda", "melissa"]
    $ _reconcile_origin = main_ui_context_snapshot()
    $ _reconcile_stats = external_reconcile_stats()
    assert eval (story_event_available("TavernKitchen", "breakfast")) timeout 5.0
    run Call("checkTriggers", "TavernKitchen", "breakfast", 0)
    advance until eval (external_reconcile_at_scene()) timeout 20.0
'''.replace("STAGE", str(stage))
    for beat in range(paragraph_count(label)):
        case += r'''
    assert eval (external_reconcile_choices() == ["Продолжить"] and renpy.get_screen("main_ui") is not None) timeout 5.0
    assert eval (external_reconcile_text_count() == 1 and bool(scene_runtime.picture) and renpy.loadable(scene_runtime.picture)) timeout 5.0
    assert eval (threads["sandraAmandaReconciliation"].num == STAGE and external_reconcile_stats() == _reconcile_stats) timeout 5.0
    $ _reconcile_previous_text = scene_runtime.text
    click id "choice_panel_button_0" pos (0.5, 0.5)
'''.replace("STAGE", str(stage))
        if beat + 1 < paragraph_count(label):
            case += r'''
    advance until eval (scene_runtime.text != _reconcile_previous_text and external_reconcile_at_scene()) timeout 20.0
'''
    case += r'''
    advance until eval (threads["sandraAmandaReconciliation"].num == NEXT and not external_reconcile_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _reconcile_origin and main_ui_runtime.scene_origin is None) timeout 5.0
    assert eval (external_reconcile_stats() == _reconcile_stats and player.tavern_management.breakfast.event_active) timeout 5.0
    assert eval (threads["sandraAmandaReconciliation"].completed == COMPLETED and threads["melissaBatProblem"].num == 9) timeout 5.0
    assert eval (not story_event_available("TavernKitchen", "breakfast")) timeout 5.0
'''.replace("NEXT", str(stage + 1)).replace("COMPLETED", str(stage == 1))
    return case


TEST_RPY += direct_scene_case(0, "story_sandra_amanda_argument_0")
TEST_RPY += direct_scene_case(1, "story_sandra_amanda_reconciliation_1")
TEST_RPY += r'''
testcase external_reconcile_normal_breakfast_old_progress_and_two_day_followup:
    parameter stage = [0, 1]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_reconcile_prepare(stage)
    python:
        if stage == 0:
            _reconcile_old_bat = threads["melissaBatProblem"]
            _reconcile_old_bat_state = (_reconcile_old_bat.num, _reconcile_old_bat.day, _reconcile_old_bat.completed)
            threads.pop("sandraAmandaReconciliation")
            initStoryEventRuntime(True)
            assert threads["melissaBatProblem"] is _reconcile_old_bat
            assert (_reconcile_old_bat.num, _reconcile_old_bat.day, _reconcile_old_bat.completed) == _reconcile_old_bat_state
            assert threads["sandraAmandaReconciliation"].num == 0
    run Call("TavernKitchenBreakfast")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (external_reconcile_at_scene()) timeout 30.0
    $ _reconcile_breakfast_origin = dict(main_ui_runtime.scene_origin)
    $ _reconcile_stats = external_reconcile_stats()
    assert eval (external_reconcile_text_count() == 1 and player.tavern_management.breakfast.event_active) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (threads["sandraAmandaReconciliation"].num == stage + 1) timeout 30.0
    advance until eval ("Закончить завтрак" in external_reconcile_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "scene" and main_ui_runtime.scene_origin is None) timeout 5.0
    assert eval (scene_runtime.picture == _reconcile_breakfast_origin["picture"] and scene_runtime.text == _reconcile_breakfast_origin["main_text"]) timeout 5.0
    assert eval (scene_runtime.text == player.tavern_management.breakfast.base_text and external_reconcile_text_count() == 1) timeout 5.0
    assert eval (external_reconcile_stats() == _reconcile_stats and threads["melissaBatProblem"].num == 9) timeout 5.0
    assert eval (not story_event_available("TavernKitchen", "breakfast") and threads["sandraAmandaReconciliation"].day == 30) timeout 5.0
    # Isolate the kitchen return from independent, unchanged room-entry stories.
    $ household_ai_mark_seen("household_event_kitchen_amanda_sandra_spark", "TavernKitchen")
    $ household_ai_mark_seen("household_event_kitchen_melissa_practical_complaint", "TavernKitchen")
    click id (external_reconcile_button("Закончить завтрак")) pos (0.5, 0.5)
    advance until eval (not player.tavern_management.breakfast.event_active and not external_reconcile_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernKitchen" and main_ui_runtime.scene_origin is None and scene_runtime.picture == tavern_kitchen_picture()) timeout 5.0

testcase external_reconcile_original_booklet_breakfast_continues_then_restores_kitchen:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_reconcile_prepare(booklet=True)
    assert eval (story_event_available("TavernKitchen", "enter")) timeout 5.0
    run Call("checkTriggers", "TavernKitchen", "enter", 0)
    advance until screen "choice" timeout 20.0
    assert eval (event_runtime.active_thread is threads["melissaBatProblem"] and threads["melissaBatProblem"].num == 8) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (external_reconcile_at_scene()) timeout 30.0
    $ _reconcile_stats = external_reconcile_stats()
    assert eval (threads["melissaBatProblem"].num == 9 and player.tavern_management.breakfast.today and player.tavern_management.breakfast.event_active) timeout 5.0
    assert eval (external_reconcile_text_count() == 1 and main_ui_runtime.scene_origin is not None) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (threads["sandraAmandaReconciliation"].num == 1) timeout 30.0
    advance until eval (not player.tavern_management.breakfast.event_active and not external_reconcile_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernKitchen" and main_ui_runtime.mode == "scene" and main_ui_runtime.scene_origin is None) timeout 5.0
    assert eval (scene_runtime.picture == tavern_kitchen_picture() and scene_runtime.text == build_kitchen_description() and external_reconcile_text_count() == 1) timeout 5.0
    assert eval (external_reconcile_stats() == _reconcile_stats and threads["melissaBatProblem"].num == 9 and threads["sandraAmandaReconciliation"].day == 30) timeout 5.0
    assert eval (player.tavern_management.breakfast.present_ids is None and not story_event_available("TavernKitchen", "breakfast")) timeout 5.0
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--compile-lint", action="store_true")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_breakfast_reconciliation_"))
    try:
        copied.TEST_RPY = TEST_RPY
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary breakfast reconciliation project: {project}", flush=True)
        commands = [["test", "--hide-execution", "all", "--report-detailed"]]
        if args.compile_lint:
            commands.extend([["compile"], ["lint"]])
        for command in commands:
            result = subprocess.run(
                [args.renpy, str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            log = project / f"breakfast-reconciliation-{command[0]}.log"
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            copied.isolated.safe_print(result.stdout if command[0] != "lint" else "\n".join(result.stdout.splitlines()[-15:]))
            if result.returncode:
                return int(result.returncode)
        return 0
    finally:
        if args.keep_temp:
            print(f"Keeping temporary breakfast reconciliation project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_breakfast_reconciliation_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
