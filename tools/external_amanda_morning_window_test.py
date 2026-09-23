#!/usr/bin/env python3
"""Test Amanda's staged morning visits in copied scripts and temporary saves."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile

import external_tavern_renovations_test as copied
import external_amanda_upstairs_flirt_test as upstairs


# Reuse the already exercised native choice/display inspection helpers only.
TEST_RPY = upstairs.TEST_RPY.split('    def external_amanda_flirt_prepare', 1)[0]
TEST_RPY += r'''
    def external_window_prepare(stage=0, booklet=False, argument=False):
        initThreads()
        initEvents()
        for thread in threads.values():
            thread.abort()
        event_runtime.available.clear()
        event_runtime.active_thread = None
        event_runtime.evaluation_time = None
        event_runtime.fired_keys_today = []
        daily_events.rows = []
        calendar_v2.daysInGame = 40
        calendar_v2.week = 2
        calendar_v2.hour = 8
        calendar_v2.minute = 0
        household.morning_state = {
            "amanda:40": {"issue": "sleepy", "resolved": 0, "indecent": 0},
            "sandra:40": {"issue": "", "resolved": 1, "indecent": 0},
            "melissa:40": {"issue": "", "resolved": 1, "indecent": 0},
        }
        household.meta["friction"] = 0
        household.meta["convergence"] = 0
        household_ai_mark_seen("household_event_kitchen_amanda_sandra_spark", "TavernKitchen")
        household_ai_mark_seen("household_event_kitchen_melissa_practical_complaint", "TavernKitchen")
        threads["melissaBatProblem"].advanceTo(6)
        window = threads["amandaMorningWindowEpisode"]
        window.reset()
        window.advanceTo(stage, force_active=True)
        window.day = 39
        Amanda.room_entry_blocked_today = False
        Amanda.corruption = 20 if argument else 50
        Amanda.rebellion = 10
        Amanda.rel = 10
        Amanda.talked_today = 0
        Amanda.anger_with_player = 0
        Amanda.attic_window_favor_stage = 0
        Amanda.set_harass_instruction("notallow" if argument else "allow")
        Melissa.drawings_found = booklet
        player.tavern_management.breakfast.today = False
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        player.intimacy.came_today = 0
        rooms.enter("TavernUpstairs")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.action_title = "WINDOW_ORIGIN"
        main_ui_runtime.action_items = rooms.current.build_exit_items()
        scene_runtime.picture = rooms.current.bg_picture
        scene_runtime.text = "WINDOW_ORIGIN"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")
        return window

    def external_window_old_definition(window):
        window.data = LThreadData(0, "amanda", "MorningWindowEpisode", None, [AmandaMorningWindowEpisodeEvent()], False, False)
        window.done = [False]

testsuite global:
    teardown:
        exit
'''

ARRIVAL = r'''
    advance until eval (external_amanda_flirt_choices() == ["Войти"]) timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    assert eval (threads["amandaMorningWindowEpisode"].num == STAGE)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_amanda_flirt_choices() == ["Продолжить"]) timeout 20.0
    assert eval (scene_runtime.picture == "images/amanda/Room/Masturbation/amanda_bedroom_00PICTURE.jpeg")
    assert eval (renpy.loadable(scene_runtime.picture) and Amanda.wardrobe.naked())
    pause 0.1
    assert eval (external_amanda_flirt_text_count() == 1)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_amanda_flirt_choices() == ["Посмотреть в окно"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_amanda_flirt_choices() == ["Посмотреть на Аманду"]) timeout 20.0
    assert eval (attic_neighbor_sex_scene_text() in scene_runtime.text)
    click id "choice_panel_button_0" pos (0.5, 0.5)
'''

LEAVE = r'''
    advance until eval (external_amanda_flirt_choices() == ["Вернуться на кухню"]) timeout 20.0
    assert eval (threads["amandaMorningWindowEpisode"].num == STAGE)
    pause 0.1
    assert eval (external_amanda_flirt_text_count() == 1)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (rooms.current_code == "TavernKitchen" and main_ui_runtime.mode == "scene") timeout 25.0
    assert eval (threads["amandaMorningWindowEpisode"].num == NEXT and threads["amandaMorningWindowEpisode"].done[STAGE])
    assert eval (threads["amandaMorningWindowEpisode"].day == 40)
    assert eval (not threads["amandaMorningWindowEpisode"].getAvailableEvents())
    assert eval (not external_amanda_flirt_choices() and main_ui_runtime.scene_origin is None)
    assert eval (Amanda.wardrobe.context == "day" and not Amanda.wardrobe.naked())
    assert eval (scene_runtime.picture == tavern_kitchen_picture() and "Amanda" not in scene_runtime.text)
    assert eval (Amanda.attic_window_favor_stage == 0 and player.intimacy.came_today == 0)
'''

for stage in range(3):
    TEST_RPY += r'''
testcase external_window_stage_STAGE:
    parameter door = [False, True]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_window_prepare(STAGE)
    $ _window_corruption = Amanda.corruption
    if eval (door):
        run Call("TavernAmandaRoomEnterWithoutKnock")
    else:
        run Jump("TavernAmandaRoom")
'''.replace("STAGE", str(stage))
    TEST_RPY += ARRIVAL.replace("STAGE", str(stage)).replace("PICTURE", str(4 - stage))
    for _ in range(2 if stage == 2 else 1):
        TEST_RPY += r'''
    advance until eval (external_amanda_flirt_choices() == ["Продолжить"]) timeout 20.0
    pause 0.1
    assert eval (external_amanda_flirt_text_count() == 1)
    click id "choice_panel_button_0" pos (0.5, 0.5)
'''
    TEST_RPY += LEAVE.replace("STAGE", str(stage)).replace("NEXT", str(stage + 1))
    TEST_RPY += r'''
    assert eval (Amanda.corruption == _window_corruption)
    assert eval (calendar_v2.clock_minutes() == 8 * 60 + 20 + (5 if door else 0))
'''
    if stage == 2:
        TEST_RPY += r'''
    assert eval (threads["amandaMorningWood"].checkActive() and threads["amandaMorningWood"].day == 40)
    assert eval (not threads["amandaMorningWood"].getAvailableEvents())
'''

TEST_RPY += r'''
testcase external_window_fourth_choices:
    parameter show = [False, True]
    parameter booklet = [False, True]
    parameter argument = [False, True]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_window_prepare(3, booklet, argument)
    $ _window_corruption = Amanda.corruption
    $ _window_rebellion = Amanda.rebellion
    $ _window_delta = -1 if procedural_random("amanda_morning_window_listen") < 0.5 else 1
    run Jump("TavernAmandaRoom")
'''
TEST_RPY += ARRIVAL.replace("STAGE", "3").replace("PICTURE", "1")
TEST_RPY += r'''
    advance until eval (external_amanda_flirt_choices() == ["Показать", "Не показывать"]) timeout 20.0
    click id (external_amanda_flirt_button("Показать" if show else "Не показывать")) pos (0.5, 0.5)
    advance until eval (external_amanda_flirt_choices() == ["Продолжить"]) timeout 20.0
    assert eval (("poor horny bastard" if show else "prude as Melissa") in scene_runtime.text)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_amanda_flirt_choices() == ["Продолжить"]) timeout 20.0
    assert eval ("Girls have many secrets!" in scene_runtime.text)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    if eval (booklet):
        advance until eval (external_amanda_flirt_choices() == ["Продолжить"]) timeout 20.0
        assert eval ("booklet you found" in scene_runtime.text)
        click id "choice_panel_button_0" pos (0.5, 0.5)
    if eval (argument):
        advance until eval (external_amanda_flirt_choices() == ["Продолжить"]) timeout 20.0
        assert eval ("hypocrisy" in scene_runtime.text and Amanda.can_apologize())
        click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_amanda_flirt_choices() == ["Вернуться на кухню"]) timeout 20.0
    assert eval (scene_runtime.picture == "images/amanda/Room/Masturbation/amanda_bedroomAPI.webp" and renpy.loadable(scene_runtime.picture))
'''
TEST_RPY += LEAVE.replace("STAGE", "3").replace("NEXT", "4")
TEST_RPY += r'''
    assert eval (threads["amandaMorningWindowEpisode"].completed)
    assert eval (Amanda.corruption == _window_corruption + 1 and Amanda.rebellion == _window_rebellion + _window_delta)
    assert eval (Amanda.can_apologize() == argument and Amanda.rel == 10)

testcase external_window_gates_delay_and_save:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_window_prepare()
    python:
        window = threads["amandaMorningWindowEpisode"]
        assert len(window.data.triggers) == 4
        assert window.getAvailableEvents()
        threads["melissaBatProblem"].num = 5
        assert not window.getAvailableEvents()
        threads["melissaBatProblem"].num = 6
        for hour in (0, 5, 12, 20, 23):
            calendar_v2.hour = hour
            assert not window.getAvailableEvents()
        calendar_v2.hour = 11
        calendar_v2.minute = 59
        assert window.getAvailableEvents()
        calendar_v2.hour = 8
        calendar_v2.minute = 0
        household.morning_state["amanda:40"]["issue"] = "sick"
        assert not window.getAvailableEvents()
        household.morning_state["amanda:40"]["issue"] = "sleepy"
        player.tavern_management.breakfast.event_active = True
        player.tavern_management.breakfast.present_ids = ["amanda"]
        assert not window.getAvailableEvents()
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.today = True
        assert not window.getAvailableEvents()
        player.tavern_management.breakfast.today = False
        Amanda.room_entry_blocked_today = True
        assert not window.getAvailableEvents()
        Amanda.room_entry_blocked_today = False
        for stage in (1, 2, 3):
            window.advanceTo(stage, force_active=True)
            window.day = 40
            assert not window.getAvailableEvents()
            window.day = 39
            assert window.getAvailableEvents()[0].target.endswith("_%d" % stage)
        window.abort()
        assert not window.getAvailableEvents()
        window.advanceTo(4, complete_at_end=True)
        assert window.completed and not window.getAvailableEvents()
        # Rebind an older one-step definition, retaining save progress and ownership.
        window.reset()
        external_window_old_definition(window)
        initThreads()
        assert threads["amandaMorningWindowEpisode"] is window
        assert window.num == 0 and window.done == [False] * 4
        assert window.data.triggers[0][0].threaded
        window.advanceTo(2, force_active=True)
        window.day = 39
        from renpy.compat.pickle import dumps, loads
        restored = loads(dumps(window))
        assert (restored.num, restored.day, restored.done) == (2, 39, [True, True, False, False])
        assert isinstance(restored.data.triggers[2][0], AmandaMorningWindowEpisodeEvent)

testcase external_window_breakfast_wake_route:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_window_prepare()
    $ player.tavern_management.breakfast.event_active = True
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa"]
    run Call("TavernKitchenBreakfastMorningIssue")
    advance until screen "choice" timeout 20.0
    assert eval (any(caption.startswith("Разбудить ") for caption in external_amanda_flirt_choices()))
    click id (external_amanda_flirt_button(next(caption for caption in external_amanda_flirt_choices() if caption.startswith("Разбудить ")))) pos (0.5, 0.5)
    advance until eval (external_amanda_flirt_choices() == ["Войти"]) timeout 20.0
    assert eval (event_runtime.active_thread is threads["amandaMorningWindowEpisode"])

testcase external_window_unlock_morning_visit:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_window_prepare(3)
    $ threads["amandaMorningWood"].reset()
    assert eval (not threads["amandaMorningWood"].checkActive())
    $ threads["amandaMorningWood"].forceEnable()
    $ threads["amandaMorningWood"].setDay()
    $ calendar_v2.hour = 6
    assert eval (not threads["amandaMorningWood"].getAvailableEvents())
    $ calendar_v2.daysInGame = 41
    $ rooms.enter("TavernMyRoom")
    assert eval (story_event_available("TavernMyRoom", "morning"))
    run Call("checkTriggers", "TavernMyRoom", "morning", 0)
    advance until eval (external_amanda_flirt_choices() == ["Продолжить утро"]) timeout 20.0
    assert eval (renpy.loadable(scene_runtime.picture) and main_ui_runtime.mode == "event")
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (threads["amandaMorningWood"].completed) timeout 20.0
    assert eval (not story_event_available("TavernMyRoom", "morning"))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_amanda_window_"))
    try:
        copied.TEST_RPY = TEST_RPY
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary Amanda morning project: {project}", flush=True)
        for command in (["compile"], ["lint"], ["test", "--hide-execution", "all", "--report-detailed"]):
            result = subprocess.run(
                [args.renpy, str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            log = project / f"amanda-window-{command[0]}.log"
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            copied.isolated.safe_print(result.stdout)
            if result.returncode:
                return result.returncode
        return 0
    finally:
        if args.keep_temp:
            print(f"Keeping temporary Amanda morning project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_amanda_window_"):
                raise RuntimeError(f"Refusing to remove unexpected path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
