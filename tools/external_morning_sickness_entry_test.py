#!/usr/bin/env python3
"""Run the real morning-sickness entry flow in a copied Ren'Py project."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_morning_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_morning_button(prefix):
        index = next(index for index, caption in enumerate(external_morning_choices()) if caption.startswith(prefix))
        return "choice_panel_button_%d" % index

    def external_morning_prepare(room_code="TavernMyRoom", hour=8):
        for thread in threads.values():
            thread.abort()
        event_runtime.available.clear()
        event_runtime.active_thread = None
        event_runtime.evaluation_time = None
        daily_events.rows = []
        player.tavern_management.breakfast.today = False
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.glory_hole = 2
        calendar_v2.daysInGame = 30
        calendar_v2.week = 2
        calendar_v2.hour = hour
        calendar_v2.minute = 0
        rooms.get("ShedWashroom").is_hidden = False
        tavern.renovation_due_days["shed"] = 30
        for event_code in ("household_event_kitchen_amanda_sandra_spark", "household_event_kitchen_melissa_practical_complaint", "household_event_breakfast_squirrel_mockery", "household_event_amanda_private_pressure", "household_event_sandra_private_check", "household_event_three_women_converge"):
            household_ai_mark_seen(event_code, room_code)
        Sandra.rel = 20
        for info in (Sandra, Georgett):
            info.set_job_value("jobkitchen", 1)
            info.set_sex_stat("pregnancy", 1)
            info.set_sex_stat("cuminside", 0)
            info.set_sex_stat("kids", 0)
        rooms.enter(room_code)
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.overlay = ""
        main_ui_runtime.action_content = None
        main_ui_runtime.action_title = "EXTERNAL_MORNING_ORIGIN"
        main_ui_runtime.action_items = [MenuItem("EXTERNAL_ORIGIN_ACTION", NullAction())]
        scene_runtime.picture = "images/church/churchEntryDay.png"
        scene_runtime.text = "EXTERNAL_MORNING_TEXT"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

    def external_morning_add(girl_name):
        daily_events.add(girl_name, "alllocs", 2, "<", 1, 8, "MorningSickness", "MorningSickness", "girl")

label ExternalMorningEntryProbe(room_code="TavernMyRoom"):
    $ _external_morning_origin = main_ui_context_snapshot()
    $ _external_morning_returned = False
    call RoomEnterEventGate(room_code, False)
    $ _external_morning_returned = True
    return

label ExternalMorningNextStory:
    $ _external_morning_next_story = True
    $ main_ui_begin_native_scene_state("EXTERNAL_NEXT_STORY")
    menu:
        "EXTERNAL_NEXT_STORY_CONTINUE":
            pass
    $ main_ui_end_native_scene_state()
    return True

testsuite global:
    teardown:
        exit

testcase external_morning_entry_real_room_and_picture:
    parameter room_code = ["TavernKitchen", "TavernMyRoom", "TavernUpstairs", "Backyard", "Shed", "ShedWashroom", "TavernAtic", "TavernSandraRoom", "TavernGloryHole"]
    $ daily_events.rows = []
    $ player.tavern_management.breakfast.today = True
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_morning_prepare(room_code)
    $ external_morning_add("sandra")
    run Jump(room_code)
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.action_title == "Утреннее недомогание" and main_ui_runtime.mode == "event") timeout 5.0
    assert eval (scene_runtime.picture == SandraStaticData.image_path("morning", "sickness") and rooms.current_code == room_code) timeout 5.0
    assert eval (not player.tavern_management.breakfast.today and not player.tavern_management.breakfast.event_active) timeout 5.0
    click id (external_morning_button("Бросилась")) pos (0.5, 0.5)
    advance until eval (any(caption.startswith("Да ладно") for caption in external_morning_choices())) timeout 20.0
    click id (external_morning_button("Да ладно")) pos (0.5, 0.5)
    advance until eval (not external_morning_choices() and main_ui_runtime.mode == "scene" and main_ui_runtime.scene_origin is None and main_ui_runtime.action_title != "EXTERNAL_MORNING_ORIGIN") timeout 20.0
    assert eval (rooms.current_code == room_code and scene_runtime.picture and scene_runtime.picture != SandraStaticData.image_path("morning", "sickness")) timeout 5.0
    assert eval (daily_events.exists("sandra", "MorningSickness") == 0 and (main_ui_runtime.action_items or build_room_action_items(rooms.current))) timeout 5.0
    run Jump(room_code)
    advance until eval (rooms.current_code == room_code and main_ui_runtime.mode == "scene" and not external_morning_choices()) timeout 20.0
    assert eval (daily_events.exists("sandra", "MorningSickness") == 0 and scene_runtime.picture != SandraStaticData.image_path("morning", "sickness")) timeout 5.0

testcase external_morning_entry_drains_workers_then_returns_context:
    parameter after_first_hour = [8, 11]
    $ daily_events.rows = []
    $ player.tavern_management.breakfast.today = True
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_morning_prepare()
    $ external_morning_add("sandra")
    $ external_morning_add("georgett")
    $ _external_morning_first = tavern_morning_sickness_girl()
    $ _external_morning_second = "georgett" if _external_morning_first == "sandra" else "sandra"
    run Call("ExternalMorningEntryProbe")
    advance until screen "choice" timeout 20.0
    assert eval (scene_runtime.picture == people.get_data(_external_morning_first).image_path("morning", "sickness")) timeout 5.0
    assert eval (daily_events.exists(_external_morning_first, "MorningSickness") == 0 and daily_events.exists(_external_morning_second, "MorningSickness") == 1) timeout 5.0
    click id (external_morning_button("Бросилась")) pos (0.5, 0.5)
    advance until eval (any(caption.startswith("Да ладно") for caption in external_morning_choices())) timeout 20.0
    $ calendar_v2.hour = after_first_hour
    click id (external_morning_button("Да ладно")) pos (0.5, 0.5)
    if eval (after_first_hour == 8):
        advance until eval ("Проверить, что это с ней" in external_morning_choices()) timeout 20.0
        assert eval (scene_runtime.picture == people.get_data(_external_morning_second).image_path("morning", "sickness")) timeout 5.0
        click id (external_morning_button("Бросилась")) pos (0.5, 0.5)
        advance until eval (any(caption.startswith("Да ладно") for caption in external_morning_choices())) timeout 20.0
        click id (external_morning_button("Да ладно")) pos (0.5, 0.5)
    advance until eval (_external_morning_returned) timeout 20.0
    assert eval (main_ui_context_snapshot() == _external_morning_origin and main_ui_runtime.scene_origin is None) timeout 5.0
    assert eval (daily_events.exists(_external_morning_second, "MorningSickness") == int(after_first_hour == 11)) timeout 5.0
    assert eval (not player.tavern_management.breakfast.today and not player.tavern_management.breakfast.event_active) timeout 5.0

testcase external_morning_entry_continues_to_normal_story_event:
    $ daily_events.rows = []
    $ player.tavern_management.breakfast.today = True
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_morning_prepare()
    $ external_morning_add("sandra")
    python:
        _external_morning_next_story = False
        _morning_test_data = LThreadData(0, "external", "MorningNext", None, ("ExternalMorningNextStory", None, None, None, 1, None, None, None, "TavernMyRoom", "enter", 0), highlight=False, threaded=True)
        _morning_test_data.initConditions()
        threads[_morning_test_data.name] = createThread(_morning_test_data)
        threads[_morning_test_data.name].forceEnable()
    run Call("ExternalMorningEntryProbe")
    advance until screen "choice" timeout 20.0
    assert eval (not _external_morning_next_story) timeout 5.0
    click id (external_morning_button("Бросилась")) pos (0.5, 0.5)
    advance until eval (any(caption.startswith("Да ладно") for caption in external_morning_choices())) timeout 20.0
    click id (external_morning_button("Да ладно")) pos (0.5, 0.5)
    advance until eval (external_morning_choices() == ["EXTERNAL_NEXT_STORY_CONTINUE"]) timeout 20.0
    assert eval (_external_morning_next_story and daily_events.exists("sandra", "MorningSickness") == 0) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (_external_morning_returned) timeout 20.0
    assert eval (main_ui_context_snapshot() == _external_morning_origin) timeout 5.0

testcase external_morning_entry_blocked_before_six_after_eleven_or_breakfast:
    parameter state = ["before_six", "after_eleven", "breakfast_done", "breakfast_active", "outside"]
    $ daily_events.rows = []
    $ player.tavern_management.breakfast.today = True
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_morning_prepare("StreetTavern" if state == "outside" else "TavernMyRoom", 5 if state == "before_six" else 11 if state == "after_eleven" else 8)
    $ external_morning_add("sandra")
    $ player.tavern_management.breakfast.today = state == "breakfast_done"
    $ player.tavern_management.breakfast.event_active = state == "breakfast_active"
    run Call("ExternalMorningEntryProbe", rooms.current_code)
    advance until eval (_external_morning_returned) timeout 20.0
    assert eval (daily_events.exists("sandra", "MorningSickness") == 1 and not external_morning_choices()) timeout 5.0
    assert eval (main_ui_context_snapshot() == _external_morning_origin) timeout 5.0
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--compile-lint", action="store_true")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_morning_entry_"))
    try:
        copied.TEST_RPY = TEST_RPY
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary morning entry test project: {project}", flush=True)
        commands = [["test", "--hide-execution", "all", "--report-detailed"]]
        if args.compile_lint:
            commands.extend([["compile"], ["lint"]])
        for command in commands:
            result = subprocess.run(
                [args.renpy, str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            log = project / f"morning-entry-{command[0]}.log"
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            copied.isolated.safe_print(result.stdout if command[0] != "lint" else "\n".join(result.stdout.splitlines()[-15:]))
            if result.returncode:
                return int(result.returncode)
        return 0
    finally:
        if args.keep_temp:
            print(f"Keeping temporary morning entry test project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_morning_entry_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
