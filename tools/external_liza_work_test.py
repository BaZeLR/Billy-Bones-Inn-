#!/usr/bin/env python3
"""Exercise Liza work and talk paths in an isolated Ren'Py test project."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import external_tavern_premium_test as premium


TEST_RPY = r'''
init python:
    def external_liza_rendered_text_count(fragment):
        from renpy.test.testfocus import focus_from_displayable
        from renpy.text.text import Text

        seen = set()
        count = [0]

        def collect(displayable):
            if id(displayable) in seen or not isinstance(displayable, Text):
                return
            seen.add(id(displayable))
            if focus_from_displayable(displayable) is None:
                return
            content = "".join(part for part in displayable.text if isinstance(part, str))
            count[0] += content.count(fragment)

        for name in ("main_ui", "say"):
            screen = renpy.get_screen(name)
            if screen is not None:
                screen.visit_all(collect)
        return count[0]

    def external_liza_prepare_volunteer_offer(accept=False):
        Liza.set_hired(True)
        Liza.set_job_value("jobGloryHoleAvail", 0)
        Liza.set_job_value("jobgloryhole", 0)
        Liza.set_job_value("jobgloryholeTommorow", 0)
        Liza.rel = 20 if accept else 0
        Liza.openness = 20 if accept else 0
        Liza.corruption = 100 if accept else 0
        Liza.mana = 100 if accept else 0
        Liza.rebellion = 0 if accept else 5
        Liza.set_arousal(100 if accept else 0)
        player.tavern_management.glory_hole = 2
        player.tavern_management.breakfast.event_active = True
        player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda", "liza"]
        player.tavern_management.breakfast.sunday_dinner_last_day = -1
        wanted = "good" if accept else "bad"
        for sunday in range(28):
            day_number = 6 + sunday * 7
            parts = calendar_v2.day_number_to_parts(day_number)
            calendar_v2.daysInGame = day_number
            calendar_v2.cycle = parts["year"]
            calendar_v2.period = parts["month"]
            calendar_v2.day = parts["day"]
            calendar_v2.week = 7
            calendar_v2.hour = 12
            calendar_v2.minute = 30
            result = girl_decide("liza", "tavern_service")
            if result["reaction"] == wanted:
                return dict(Liza.jobs)
        raise AssertionError("No Sunday dinner clock produced %s from the real decision model" % wanted)

testsuite global:
    teardown:
        exit

testcase external_liza_amanda_glory_hole_real_session:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("liza") is not None) timeout 20.0
    $ calendar_v2.week = 1
    $ calendar_v2.day = 3
    $ calendar_v2.hour = 14
    $ calendar_v2.minute = 0
    $ player.tavern_management.glory_hole = 2
    $ Georgett.set_hired(True)
    $ Georgett.set_job_value("jobGloryHoleAvail", 1)
    $ Georgett.assign_tavern_service("gloryhole", False)
    $ Liza.set_hired(True)
    $ Liza.set_job_value("jobGloryHoleAvail", 1)
    $ Liza.assign_tavern_service("gloryhole", False)
    $ Amanda.corruption = 22
    $ TodaySexEvents_Add("amanda", 99, 1, "glorytry")
    assert eval (set(tavern_glory_hole_workers()) == set(("georgett", "liza")) and tavern_glory_hole_worker() == "liza") timeout 5.0
    run Jump("TavernGloryHole")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernGloryHole" and [str(i.caption or "") for i in main_ui_runtime.action_items].count("Проверить, что происходит") == 1) timeout 5.0
    assert eval (external_liza_rendered_text_count("За ширмой в дальнем углу трактира") == 1) timeout 5.0
    assert eval (not story_event_available("TavernGloryHole", "check_glory_hole")) timeout 5.0
    $ _check_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Проверить, что происходит")
    click id ("choice_panel_button_%d" % _check_index) pos (0.5, 0.5) until screen "say" timeout 20.0
    $ print("GH_RENDER first_say static=%d" % external_liza_rendered_text_count("За ширмой в дальнем углу трактира"))
    assert eval (external_liza_rendered_text_count("За ширмой в дальнем углу трактира") == 0) timeout 5.0
    assert eval (external_liza_rendered_text_count("Вы находитесь в дальнем углу вашего трактира") == 1) timeout 5.0
    advance until screen "choice" timeout 20.0
    $ _gh_first_choice_static = external_liza_rendered_text_count("За ширмой в дальнем углу трактира")
    $ print("GH_RENDER first_choice static=%d" % _gh_first_choice_static)
    assert eval (external_liza_rendered_text_count("Что вы собираетесь делать?") == 1) timeout 5.0
    assert eval (str(player.tavern_management.glory_hole_session.girl_name or "") == "liza" and int(player.tavern_management.glory_hole_session.works or 0) == 1 and int(player.tavern_management.glory_hole_session.amanda_present or 0) == 1) timeout 5.0
    assert eval (SexEvents.today_index("amanda", 99, "glorytry") == -1) timeout 5.0
    $ _peek_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Смотреть на девочку")
    click id ("choice_panel_button_%d" % _peek_index) pos (0.5, 0.5) until screen "say" timeout 20.0
    $ print("GH_RENDER peek_say static=%d" % external_liza_rendered_text_count("За ширмой в дальнем углу трактира"))
    assert eval (external_liza_rendered_text_count("За ширмой в дальнем углу трактира") == 0) timeout 5.0
    assert eval (external_liza_rendered_text_count("Вы решили аккуратно заглянуть за ширмочку") == 1) timeout 5.0
    advance until eval (renpy.get_screen("choice") is not None and "Ваша реакция" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ print("GH_RENDER reaction_choice static=%d" % external_liza_rendered_text_count("За ширмой в дальнем углу трактира"))
    assert eval (external_liza_rendered_text_count("За ширмой в дальнем углу трактира") == 0) timeout 5.0
    assert eval (external_liza_rendered_text_count("Ваша реакция?") == 1) timeout 5.0
    assert eval (_gh_first_choice_static == 0) timeout 5.0
    assert eval (Amanda.var_int("glory_cur_state", 0) == 1 and int(player.tavern_management.glory_hole_session.menu_blocked or 0) == 1) timeout 5.0
    $ _reaction_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Ваша реакция")
    click id ("choice_panel_button_%d" % _reaction_index) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Осмотреть Аманду" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (not story_event_available("TavernGloryHole", "check_glory_hole")) timeout 5.0
    $ _leave_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Развернуться и уйти, ничего не говоря")
    $ calendar_v2.hour = 18
    click id ("choice_panel_button_%d" % _leave_index) pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (str(scene_runtime.picture or "") == str(tavern_main_picture() or "") and str(scene_runtime.text or "") == str(scene_runtime.location_text or "") and str(main_ui_runtime.action_title or "") == "Действия в трактире" and main_ui_runtime.scene_origin is None and bool(main_ui_runtime.action_items) and renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is None) timeout 5.0
    assert eval (not story_event_available("TavernGloryHole", "check_glory_hole")) timeout 5.0
    $ calendar_v2.hour = 14
    run Jump("TavernGloryHole")
    advance until screen "main_ui" timeout 20.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items].count("Проверить, что происходит") == 1) timeout 5.0
    $ _check_again_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Проверить, что происходит")
    click id ("choice_panel_button_%d" % _check_again_index) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (int(player.tavern_management.glory_hole_session.amanda_present or 0) == 0 and int(player.tavern_management.glory_hole_session.menu_blocked or 0) == 0) timeout 5.0
    assert eval ("Ваша реакция" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _back_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Вернуться в комнату")
    click id ("choice_panel_button_%d" % _back_index) pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernGloryHole" and str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (str(scene_runtime.picture or "") == "images/gloryhole/glory1.jpg" and "За ширмой" in str(scene_runtime.text or "") and not story_event_available("TavernGloryHole", "check_glory_hole")) timeout 5.0

testcase external_liza_dress_shame_corruption_floor:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ Liza.rel = 12
    $ Liza.corruption = 35
    $ Liza.talked_today = 0
    $ Liza.set_day_underwear("panties", "", True)
    run Call("IntLizaDressChange", "liza")
    advance until screen "choice" timeout 20.0
    $ _shame_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Постыдить Лизетту за отстутсвие панталон")
    click id ("choice_panel_button_%d" % _shame_index) pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 900) until eval (int(Liza.talked_today or 0) == 1) timeout 20.0
    assert eval (int(Liza.corruption or 0) == 34 and Liza.current_underwear("panties", "") == "simplepanties") timeout 5.0

testcase external_liza_dress_shame_at_floor:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ Liza.rel = 12
    $ Liza.corruption = 30
    $ Liza.talked_today = 0
    $ Liza.set_day_underwear("panties", "", True)
    run Call("IntLizaDressChange", "liza")
    advance until screen "choice" timeout 20.0
    $ _shame_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Постыдить Лизетту за отстутсвие панталон")
    click id ("choice_panel_button_%d" % _shame_index) pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 900) until eval (int(Liza.talked_today or 0) == 1) timeout 20.0
    assert eval (int(Liza.corruption or 0) == 30 and Liza.current_underwear("panties", "") == "simplepanties") timeout 5.0

testcase external_liza_dress_shame_below_floor:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ Liza.rel = 12
    $ Liza.corruption = 1
    $ Liza.talked_today = 0
    $ Liza.set_day_underwear("panties", "", True)
    run Call("IntLizaDressChange", "liza")
    advance until screen "choice" timeout 20.0
    $ _shame_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Постыдить Лизетту за отстутсвие панталон")
    click id ("choice_panel_button_%d" % _shame_index) pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 900) until eval (int(Liza.talked_today or 0) == 1) timeout 20.0
    assert eval (int(Liza.corruption or 0) == 1 and Liza.current_underwear("panties", "") == "simplepanties") timeout 5.0

testcase external_liza_volunteer_offer_refusal_keeps_jobs:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ _volunteer_jobs = external_liza_prepare_volunteer_offer(False)
    assert eval (calendar_v2.week == 7 and tavern_sunday_dinner_available() and "liza" in tavern_sunday_dinner_present_ids() and tavern_sunday_dinner_can_offer_service("liza")) timeout 5.0
    assert eval (Liza.tavern_service_available("intimate") and not Liza.tavern_service_available("gloryhole")) timeout 5.0
    run Call("TavernKitchenSundayDinnerServiceOffer", "liza")
    advance until screen "choice" timeout 20.0
    assert eval (Liza.var["decision_results"]["tavern_service"]["reaction"] == "bad") timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Вернуться к обеду"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
    assert eval (not Liza.tavern_service_available("gloryhole") and dict(Liza.jobs) == _volunteer_jobs) timeout 5.0
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = None

testcase external_liza_volunteer_offer_acceptance_only_unlocks:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ _volunteer_jobs = external_liza_prepare_volunteer_offer(True)
    assert eval (calendar_v2.week == 7 and tavern_sunday_dinner_available() and "liza" in tavern_sunday_dinner_present_ids() and tavern_sunday_dinner_can_offer_service("liza")) timeout 5.0
    assert eval (Liza.tavern_service_available("intimate") and not Liza.tavern_service_available("gloryhole")) timeout 5.0
    run Call("TavernKitchenSundayDinnerServiceOffer", "liza")
    advance until screen "choice" timeout 20.0
    assert eval (Liza.var["decision_results"]["tavern_service"]["reaction"] == "good") timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Продолжить"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
    assert eval (Liza.tavern_service_available("gloryhole") and {k: v for k, v in Liza.jobs.items() if k != "jobGloryHoleAvail"} == {k: v for k, v in _volunteer_jobs.items() if k != "jobGloryHoleAvail"}) timeout 5.0
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = None

testcase external_liza_repeated_harassment_choice_one:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    $ Liza.corruption = 35
    $ Liza.set_harass_instruction("")
    run Call("IntHarrassmentDiscuss", "liza", 1)
    advance until screen "choice" timeout 20.0
    $ _forbid_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Сказать что она не должна позволять себя лапать")
    click id ("choice_panel_button_%d" % _forbid_index) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Вернуться к делам" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (int(Liza.corruption or 0) == 35 and Liza.harass_instruction() == "notallow") timeout 5.0
    $ _return_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Вернуться к делам")
    click id ("choice_panel_button_%d" % _return_index) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
    run Call("IntHarrassmentDiscuss", "liza", 1)
    advance until screen "choice" timeout 20.0
    $ _forbid_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Сказать что она не должна позволять себя лапать")
    click id ("choice_panel_button_%d" % _forbid_index) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Вернуться к делам" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (int(Liza.corruption or 0) == 35 and Liza.harass_instruction() == "notallow") timeout 5.0
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=premium.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=480)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()
    root = premium.project_root()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.exists():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_liza_work_"))
    try:
        premium.TEST_RPY = TEST_RPY
        temp_project = premium.build_temp_project(root, temp_root)
        print(f"Temporary Liza work test project: {temp_project}")
        return premium.run_renpy(renpy_exe, temp_project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary Liza work test project: {temp_root}")
        else:
            expected_parent = Path(tempfile.gettempdir()).resolve()
            resolved = temp_root.resolve()
            if resolved.parent != expected_parent or not resolved.name.startswith("tractir_liza_work_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            premium.remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
