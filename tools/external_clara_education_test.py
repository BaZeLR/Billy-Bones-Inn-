#!/usr/bin/env python3
"""Exercise Clara's card-night discovery with real Ren'Py menus, isolated saves."""

import argparse
from pathlib import Path
import subprocess
import tempfile

import external_event_text_test as text_probe
import external_tavern_renovations_test as project_copy


TEST_RPY = text_probe.TEST_RPY.split("\nlabel ExternalEventTextScenario(", 1)[0]
TEST_RPY += r'''
init python:
    def education_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption) for item in choice.scope["items"]] if choice else []

    def education_prepare():
        global saveVersion
        saveVersion = currentVersion
        # Jumping to the dev checkpoint skips before_main_menu. Initialize the
        # same real condition objects as normal startup/load before arranging it.
        initStoryEventRuntime(True)
        for value in threads.values():
            value.abort()
        for key in ("claraPaintingsPath", "claraTavernVisit"):
            threads[key].completed = True
        threads["claraTavernEducation"].reset()
        for key in ("peephole", "glory_hole"):
            tavern.renovations[key].status = "completed"
        for girl in (Clara, Amanda, Melissa):
            girl.set_sex_busy(False)
        Clara.day_location_override_code = ""
        Melissa.temp_room_code = ""
        event_runtime.available.clear()
        event_runtime.fired_keys_today = []
        event_runtime.evaluation_time = None
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        household.morning_state.clear()
        calendar_v2.daysInGame = 140
        calendar_v2.week = 1
        calendar_v2.hour = 20
        calendar_v2.minute = 0
        rooms.enter("MarketPlace")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_items = []
        scene_runtime.picture = MARKETPLACE_CLOSED_PICTURE
        scene_runtime.text = "EDUCATION_STATIC_ROOM_SENTINEL"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

screen education_reload():
    textbutton "Reload education save":
        id "education_reload_save"
        xalign 1.0
        yalign 0.0
        action [Hide("education_reload"), Function(renpy.load, "education-window")]

testsuite global:
    before testcase:
        run Jump("dev_after_report_checkpoint")
        advance until screen "main_ui" timeout 25.0
        $ education_prepare()
    teardown:
        exit

testcase education_weekday_hour_boundaries:
    parameter clock = [(1,19,59,False), (1,20,0,True), (1,23,59,True), (1,0,0,False), (2,21,0,False), (3,21,0,False), (4,21,0,False), (5,21,0,False), (6,19,59,False), (6,20,0,True), (6,23,59,True), (7,21,0,False)]
    python:
        calendar_v2.week, calendar_v2.hour, calendar_v2.minute, expected = clock
        available = story_event_available("MarketPlace", "enter")
        assert available == expected, (clock, threads["claraTavernEducation"].checkActive(), claraEducationCardsEvent.auditChecks(threads["claraTavernEducation"].day))
        for key in ("clara", "amanda", "melissa"):
            assert (people.location(key) == "WineStoreBasement") == expected, (key, clock, people.location(key))
            if expected:
                assert not people.can_talk(key)
                assert key not in people.ids_at("TavernMain")
        assert rooms.get("WineStoreBasement") is not None

testcase education_prerequisites_and_saved_progress:
    python:
        lesson = threads["claraTavernEducation"]
        for key in ("peephole", "glory_hole"):
            tavern.renovations[key].status = "unrequested"
            lesson.metconds = False
            assert not story_event_available("MarketPlace", "enter"), (key, tavern.renovations[key].status, lesson is threads["claraTavernEducation"], lesson.metconds, [(str(c), c.eval()) for c in lesson.data.conds], list(event_runtime.available.get("MarketPlace", {}).keys()))
            assert people.location("amanda") != "WineStoreBasement"
            tavern.renovations[key].status = "completed"
        for key in ("claraPaintingsPath", "claraTavernVisit"):
            threads[key].completed = False
            lesson.metconds = False
            assert not story_event_available("MarketPlace", "enter")
            threads[key].completed = True
        lesson.metconds = False
        assert story_event_available("MarketPlace", "enter")
        lesson.advance()
        initStoryEventRuntime(True)
        assert lesson.num == 1 and lesson.done == [True, False]
        assert not story_event_available("MarketPlace", "enter")
        assert people.location("amanda") != "WineStoreBasement"
        lesson.advance()
        initStoryEventRuntime(True)
        assert lesson.completed and lesson.num == 2
        assert not story_event_available("MarketPlace", "enter")
        assert people.location("melissa") != "WineStoreBasement"

testcase education_tavern_clues:
    $ calendar_v2.hour = 19
    $ rooms.enter("TavernMain")
    assert eval (all(people.location(key) == "TavernMain" for key in ("clara", "melissa", "amanda")))
    assert eval (story_event_available("TavernMain", "enter"))
    run Call("checkTriggers", "TavernMain", "enter", 0)
    advance until eval ("Заняться своими делами" in education_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "event")
    assert eval ("шепчутся" in scene_runtime.text)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (renpy.get_screen("choice") is None) timeout 20.0
    assert eval (threads["claraTavernEducation"].num == 0)
    assert eval (not story_event_available("TavernMain", "enter"))
    $ calendar_v2.hour = 20
    assert eval (story_event_available("TavernMain", "enter"))
    run Call("checkTriggers", "TavernMain", "enter", 0)
    advance until eval ("Продолжить вечер" in education_choices()) timeout 20.0
    assert eval ("вспоминаете" in scene_runtime.text)
    assert eval (all(people.location(key) == "WineStoreBasement" for key in ("clara", "melissa", "amanda")))
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (renpy.get_screen("choice") is None) timeout 20.0
    assert eval (threads["claraTavernEducation"].num == 0)
    assert eval (story_event_available("MarketPlace", "enter"))

testcase education_busy_participant_blocks_outing:
    parameter person = ["clara", "melissa", "amanda"]
    python:
        girl = people.get_info(person)
        girl.set_sex_busy(True)
        assert not story_event_available("MarketPlace", "enter")
        assert all(people.location(key) != "WineStoreBasement" for key in ("clara", "melissa", "amanda"))
        girl.set_sex_busy(False)
        assert story_event_available("MarketPlace", "enter")

testcase education_detention_or_abort_blocks_outing:
    python:
        case = threads["claraMongolAccusation"]
        case.done[0], case.done[2] = True, False
        assert Clara.mongol_case_detained()
        assert not story_event_available("MarketPlace", "enter")
        assert people.location("amanda") != "WineStoreBasement"
        case.done[2] = True
        assert story_event_available("MarketPlace", "enter")
        threads["claraTavernEducation"].abort()
        assert not story_event_available("MarketPlace", "enter")
        assert all(people.location(key) != "WineStoreBasement" for key in ("clara", "melissa", "amanda"))

testcase education_complete_market_route:
    $ education_before_rel = Clara.rel
    run Jump("MarketPlace")
    advance until eval ("Пойти проверить" in education_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    assert eval (scene_runtime.picture == MARKETPLACE_CLOSED_PICTURE)
    assert eval (external_event_text_count("Рынок опустел.") == 1) timeout 5.0
    $ education_text_origin = external_event_text_position("Рынок опустел.")
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Обойти лавку" in education_choices()) timeout 20.0
    assert eval (scene_runtime.picture == "images/general/closedVenue default.png")
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Заглянуть в окно" in education_choices()) timeout 20.0
    assert eval (scene_runtime.picture == "images/clara/education/basement_window_night.png")
    assert eval (external_event_text_count("Позади лавки") == 1) timeout 5.0
    assert eval (external_event_text_same_position(education_text_origin, external_event_text_position("Позади лавки"))) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
'''

for index in range(12):
    TEST_RPY += f'''
    advance until eval (scene_runtime.picture == "images/clara/education/cardplay{index}.jpg" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    assert eval (rooms.current_code == "MarketPlace")
    assert eval (external_event_text_count(scene_runtime.text) == 1) timeout 5.0
    assert eval (external_event_text_count("Сейчас уже поздно и рынок закрыт.") == 0)
    assert eval (external_event_text_same_position(education_text_origin, external_event_text_position(scene_runtime.text))) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
'''

TEST_RPY += r'''
    advance until eval (main_ui_runtime.mode == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (rooms.current_code == "MarketPlace")
    assert eval (scene_runtime.picture == MARKETPLACE_CLOSED_PICTURE)
    assert eval (scene_runtime.text == rooms.get("MarketPlace").schedule.closed_text)
    assert eval (any(item.caption == "Вернуться к трактиру" for item in main_ui_runtime.action_items))
    assert eval (threads["claraTavernEducation"].num == 1)
    assert eval (Clara.rel == education_before_rel)
    assert eval (all(people.location(key) != "WineStoreBasement" for key in ("clara", "melissa", "amanda")))
    assert eval (not story_event_available("MarketPlace", "enter"))

testcase education_leave_without_progress:
    parameter stop = [0, 1, 2, 3, 7, 10, 11, 12, 13]
    run Jump("MarketPlace")
    advance until eval ("Пойти проверить" in education_choices()) timeout 20.0
'''

for step in range(13):
    TEST_RPY += f'''
    if eval (stop > {step}):
        $ education_old_picture = scene_runtime.picture
        click id "choice_panel_button_0" pos (0.5, 0.5)
        advance until eval (scene_runtime.picture != education_old_picture and renpy.get_screen("choice") is not None) timeout 20.0
'''

TEST_RPY += r'''
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (rooms.current_code == "MarketPlace")
    assert eval (scene_runtime.picture == MARKETPLACE_CLOSED_PICTURE)
    assert eval (threads["claraTavernEducation"].num == 0)
    assert eval (story_event_available("MarketPlace", "enter"))
    $ calendar_v2.hour = 0
    $ calendar_v2.week = 2
    assert eval (all(people.location(key) != "WineStoreBasement" for key in ("clara", "melissa", "amanda")))
    assert eval (not story_event_available("MarketPlace", "enter"))

testcase education_save_during_window:
    run Jump("MarketPlace")
    advance until eval ("Пойти проверить" in education_choices()) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Обойти лавку" in education_choices()) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Заглянуть в окно" in education_choices()) timeout 20.0
    $ renpy.save("education-window", include_screenshot=False)
    assert eval (renpy.can_load("education-window"))
    $ education_saved = renpy.get_save_data("education-window")
    assert eval (education_saved["threads"]["claraTavernEducation"].num == 0)
    assert eval (education_saved["rooms"].current_code == "MarketPlace")
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (scene_runtime.picture == "images/clara/education/cardplay0.jpg") timeout 20.0
    run Show("education_reload")
    click id "education_reload_save" pos (0.5, 0.5)
    advance until eval ("Заглянуть в окно" in education_choices()) timeout 20.0
    assert eval (scene_runtime.picture == "images/clara/education/basement_window_night.png")
    assert eval (threads["claraTavernEducation"].num == 0 and main_ui_runtime.mode == "event")
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (rooms.current_code == "MarketPlace" and scene_runtime.picture == MARKETPLACE_CLOSED_PICTURE)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_education_"))
    project_copy.TEST_RPY = TEST_RPY
    project = project_copy.build_temp_project(project_copy.isolated.project_root(), temp_root)
    savedir = project / ".test-saves"
    savedir.mkdir()
    print(f"Isolated project: {project}", flush=True)
    for command in (["compile"], ["lint"], ["test", "--hide-execution", "all", "--report-detailed"]):
        result = subprocess.run(
            [project_copy.isolated.RENPY_DEFAULT, str(project), "--savedir", str(savedir), *command],
            text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        log = project / ("education-%s.log" % command[0])
        log.write_text(result.stdout, encoding="utf-8")
        print(f"{command[0]}: exit {result.returncode}; {log}", flush=True)
        project_copy.isolated.safe_print(result.stdout)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
