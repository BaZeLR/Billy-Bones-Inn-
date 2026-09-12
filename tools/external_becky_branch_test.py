#!/usr/bin/env python3
"""Run focused Becky branch checks from a temporary Ren'Py project.

Generated Ren'Py testcase code is written only to a temp project, not to this
repository's game folder.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


RENpy_DEFAULT = r"C:\Users\blank\renpy\renpy-8.5.2-sdk\renpy.exe"


def safe_print(text: str) -> None:
    try:
        print(text, end="" if text.endswith("\n") else "\n")
    except UnicodeEncodeError:
        encoded = text.encode(sys.stdout.encoding or "utf-8", errors="replace")
        sys.stdout.buffer.write(encoded)
        if not text.endswith("\n"):
            sys.stdout.buffer.write(b"\n")


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def is_junction(path: Path) -> bool:
    probe = getattr(path, "is_junction", None)
    if callable(probe):
        try:
            return bool(probe())
        except OSError:
            return False
    return False


def remove_temp_tree(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink() and not is_junction(path):
        for child in path.iterdir():
            remove_temp_tree(child)
        path.rmdir()
        return
    if path.is_dir():
        path.rmdir()
    else:
        path.unlink(missing_ok=True)


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        remove_temp_tree(path)
    path.mkdir(parents=True, exist_ok=True)


def junction_dir(source: Path, target: Path) -> None:
    completed = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(target), str(source)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout.strip())


def hardlink_or_copy(source: Path, target: Path) -> None:
    try:
        os.link(source, target)
    except OSError:
        shutil.copy2(source, target)


TEST_RPY = r'''
testsuite global:
    teardown:
        exit

testcase becky_home_restore_gate_after_sex:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        rooms.enter("BeckyHome")
        rooms.get("BeckyHomeFront").state["arrival_mode"] = "FromDances"
        threads["beckyHome"].advanceTo(2, force_active=True)
        threads["beckyEddieSex"].reset()
        player.appearance.current_dress = "citydress"
    run Call("BeckyHomeAfterSex")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHome") timeout 5.0
    assert eval (str(rooms.get("BeckyHomeFront").state["arrival_mode"] or "") == "FromDances") timeout 5.0
    assert eval ("спальне" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ("зачем ты пришел" not in str(scene_runtime.text or "")) timeout 5.0
    assert eval ("постучали" not in str(scene_runtime.text or "")) timeout 5.0

testcase becky_home_front_from_dance_starts_home_thread:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 5
        calendar_v2.hour = 20
        calendar_v2.minute = 0
        threads["beckyHome"].reset()
        Becky.home_front_checked_today = False
        player.appearance.current_dress = "citydress"
    run Call("BeckyHomeFront", "FromDances")
    advance until screen "choice" timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHomeFront") timeout 5.0
    assert eval (str(rooms.get("BeckyHomeFront").state["arrival_mode"] or "") == "FromDances") timeout 5.0
    assert eval (int(threads["beckyHome"].num or 0) == 1) timeout 5.0
    run Jump("StreetTavern")

testcase becky_front_and_home_replace_foreign_location_text:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 19
        calendar_v2.minute = 0
        scene_runtime.text = "FOREIGN MARKET DESCRIPTION"
        scene_runtime.location_text = "FOREIGN MARKET DESCRIPTION"
        Becky.home_front_checked_today = True
        threads["beckyHome"].advanceTo(3, complete_at_end=True)
        player.appearance.current_dress = "citydress"
    run Call("BeckyHomeFront", "")
    advance until screen "say" timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHomeFront") timeout 5.0
    assert eval (str(scene_runtime.text or "") == str(rooms.get("BeckyHomeFront").visible_descriptions()[0].text or "")) timeout 5.0
    assert eval ("FOREIGN MARKET DESCRIPTION" not in str(scene_runtime.text or "") and "FOREIGN MARKET DESCRIPTION" not in str(scene_runtime.location_text or "")) timeout 5.0
    advance until screen "choice" timeout 20.0
    $ _becky_enter_home_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Зайти в дом")
    click id ("choice_panel_button_%d" % int(_becky_enter_home_index)) pos (0.5, 0.5) until eval (rooms.current_code == "BeckyHome") timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHome") timeout 5.0
    assert eval (str(scene_runtime.text or "") == str(rooms.get("BeckyHome").visible_descriptions()[0].text or "")) timeout 5.0
    assert eval ("FOREIGN MARKET DESCRIPTION" not in str(scene_runtime.text or "") and "FOREIGN MARKET DESCRIPTION" not in str(scene_runtime.location_text or "")) timeout 5.0

testcase becky_accept_home_invitation_order:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 5
        calendar_v2.hour = 20
        calendar_v2.minute = 0
        rooms.get("FridayDance").dance_count = 1
        rooms.get("FridayDance").step = 3
        rooms.get("FridayDance").max_step = 6
        rooms.get("FridayDance").hands = "ass"
        rooms.get("FridayDance").kiss = 1
        rooms.get("FridayDance").tits = 0
        rooms.get("FridayDance").becky_home_invited = True
        threads["beckyHome"].reset()
        Becky.home_front_checked_today = False
        Becky.rel = 20
        Becky.corruption = 40
        Becky.stats["sexacts"] = 0
        player.appearance.current_dress = "citydress"
    run Call("becky_accept_home_invitation")
    advance until screen "choice" timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHomeFront") timeout 5.0
    assert eval (str(rooms.get("BeckyHomeFront").state["arrival_mode"] or "") == "FromDances") timeout 5.0
    assert eval (int(rooms.get("FridayDance").dance_count or 0) == 5) timeout 5.0
    run Jump("StreetTavern")

testcase becky_from_dance_blowjob_uses_oop_group_state:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 5
        calendar_v2.hour = 20
        calendar_v2.minute = 0
        rooms.get("BeckyHomeFront").state["arrival_mode"] = "FromDances"
        threads["beckyDinner"].reset()
        Becky.home_front_checked_today = True
        Eddie.set_sex_stat("group_sex", 1)
        Becky.set_sex_busy(False)
        Becky.set_cock_position("none", "You")
        Becky.set_cock_position("none", "eddie")
        player.intimacy.came_today = 0
    run Call("BeckyHomeFront", "FromDances")
    advance until screen "choice" timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHomeFront") timeout 5.0
    $ _becky_enter_home_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Зайти в дом")
    click id ("choice_panel_button_%d" % int(_becky_enter_home_index)) pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 560) until screen "choice" timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHome") timeout 5.0
    assert eval (int(Eddie.sex_stat("group_sex", 0) or 0) == 0) timeout 5.0
    assert eval ("Предложить отсосать" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _becky_blowjob_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Предложить отсосать")
    click id ("choice_panel_button_%d" % int(_becky_blowjob_index)) pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (Becky.cock_in("mouth", "You") and int(Eddie.sex_stat("group_sex", 0) or 0) == 0) timeout 5.0

testcase becky_from_dance_sex_finish_stays_in_becky_home:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 5
        calendar_v2.hour = 20
        calendar_v2.minute = 0
        threads["beckyDinner"].reset()
        rooms.get("BeckyHomeFront").state["arrival_mode"] = "FromDances"
        Becky.set_sex_busy(False)
        Becky.set_cock_position("none", "You")
        Becky.set_cock_position("none", "eddie")
        Eddie.set_sex_stat("group_sex", 0)
    run Call("BeckyHome", "FromDances")
    advance until screen "choice" timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHome") timeout 5.0
    $ _becky_finish_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Закончить")
    click id ("choice_panel_button_%d" % int(_becky_finish_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(rooms.current_code or "") == "BeckyHome" and str(scene_runtime.text or "") == str(becky_home_restore_text() or "")) timeout 20.0
    assert eval (str(rooms.current_code or "") == "BeckyHome") timeout 5.0
    assert eval (str(scene_runtime.text or "") == str(becky_home_restore_text() or "")) timeout 5.0

testcase becky_group_session_exit_clears_oop_state:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        Eddie.set_sex_stat("group_sex", 1)
        Becky.set_sex_busy(False)
        Becky.set_cock_position("none", "You")
        Becky.set_cock_position("none", "eddie")
    run Call("IntBeckySex", "becky", "home")
    advance until screen "choice" timeout 20.0
    assert eval (int(Eddie.sex_stat("group_sex", 0) or 0) == 1) timeout 5.0
    $ _becky_finish_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Закончить")
    click id ("choice_panel_button_%d" % int(_becky_finish_index)) pos (0.5, 0.5) until eval (int(Eddie.sex_stat("group_sex", 0) or 0) == 0) timeout 20.0

testcase becky_post_dance_panties_request_is_easier_than_bra:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        rooms.enter("GroceryStore")
        threads["beckyHome"].advanceTo(2, force_active=True)
        Becky.rel = 9
        Becky.corruption = 30
        Becky.talked_today = 0
        Becky.set_sex_stat("orgasms_given", 2)
        Becky.set_default_bra("simplebra")
        Becky.set_default_panties("simplepanties")
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    $ _becky_clothes_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Поговорить с Бекки об одежде")
    click id ("choice_panel_button_%d" % int(_becky_clothes_index)) pos (0.5, 0.5) until eval ("Предложить вдове ходить без лифа" in [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _becky_bra_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Предложить вдове ходить без лифа")
    click id ("choice_panel_button_%d" % int(_becky_bra_index)) pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (Becky.has_bra() and Becky.has_panties() and str(main_ui_runtime.mode or "") == "talk") timeout 5.0
    $ _becky_clothes_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Поговорить с Бекки об одежде")
    click id ("choice_panel_button_%d" % int(_becky_clothes_index)) pos (0.5, 0.5) until eval ("Предложить вдове снять панталоны" in [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _becky_panties_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "") == "Предложить вдове снять панталоны")
    click id ("choice_panel_button_%d" % int(_becky_panties_index)) pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (Becky.has_bra() and not Becky.has_panties() and str(main_ui_runtime.mode or "") == "talk") timeout 5.0

testcase friday_dance_find_becky_opens_becky_dance:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        rooms.enter("FridayDance")
        calendar_v2.week = 5
        calendar_v2.hour = 20
        calendar_v2.minute = 0
        rooms.get("FridayDance").dance_count = 0
        rooms.get("FridayDance").step = 0
        Becky.left_dances = 0
        Becky.rel = 20
        Becky.corruption = 40
    run Call("story_becky_friday_dance_mc_0")
    advance until screen "choice" timeout 20.0
    assert eval (str(rooms.current_code or "") == "FridayDance") timeout 5.0
    assert eval (int(rooms.get("FridayDance").step or 0) == 1) timeout 5.0
    assert eval (int(rooms.get("FridayDance").dance_count or 0) == 1) timeout 5.0
    run Jump("StreetTavern")

testcase becky_evening_georgette_visit_is_reachable:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 2
        calendar_v2.hour = 20
        calendar_v2.minute = 0
        rooms.enter("BeckyHome")
        threads["beckyDinner"].reset()
        threads["beckyDinner"].advanceTo(2, force_active=True)
        threads["beckySex"].reset()
        threads["beckySex"].advanceTo(1, force_active=True)
        Becky.eddie_home_visit_state = 4
        Eddie.saw_mother_sex = True
        TodaySexEvents_Clear()
        TodaySexEvents_Add("georgett", 99, 99, "EddieHomeVisit")
        initStoryEventRuntime(True)
    assert eval (rooms.get("BeckyHome").is_open()) timeout 5.0
    assert eval (story_event_available("BeckyHome", "georgett_home_visit")) timeout 5.0

testcase becky_visit_clock_and_market_invitation:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 13
        calendar_v2.minute = 0
        threads["beckyHome"].advanceTo(3, complete_at_end=True)
    assert eval (people.location("becky") == "GroceryStore" and not marketplace_becky_home_visible())
    $ calendar_v2.hour = 19
    assert eval (people.location("becky") == "BeckyHome" and marketplace_becky_home_visible())
    python:
        calendar_v2.week = 2
        Becky.sandra_kitchen_friendship_progress = 3
    assert eval (people.location("becky") == "TavernKitchen" and not marketplace_becky_home_visible())
    python:
        calendar_v2.hour = 20
        calendar_v2.minute = 30
    assert eval (people.location("becky") == "BeckyHome" and marketplace_becky_home_visible())
    $ calendar_v2.hour = 23
    assert eval (not marketplace_becky_home_visible())
    python:
        calendar_v2.week = 5
        calendar_v2.hour = 22
        calendar_v2.minute = 0
        rooms.get("FridayDance").dance_count = 5
        rooms.get("FridayDance").becky_home_invited = True
        threads["beckyHome"].reset()
        rooms.enter("MarketPlace")
        event_runtime.fired_keys_today = []
    assert eval (marketplace_becky_home_visible())
    run movement_actions("BeckyHomeFront", 10)
    advance until screen "choice" timeout 20.0
    assert eval (rooms.current_code == "BeckyHomeFront")
    assert eval (rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances")
    assert eval (threads["beckyHome"].num == 1)
    assert eval (calendar_v2.hour == 22 and calendar_v2.minute == 10)
    assert eval (any(item.caption == "Зайти в дом" for item in renpy.get_screen("choice").scope["items"]))
    assert eval (not any(item.caption == "Вернуться на рынок" for item in renpy.get_screen("choice").scope["items"]))

testcase inga_grocery_morning_event_cycle:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 7
        calendar_v2.minute = 0
        threads["beckyIngaLucasPath"].reset()
        Inga.known = False
        Inga.acquaintance_stage = 0
        Becky.talked_today = 0
        event_runtime.fired_keys_today = []
        initStoryEventRuntime(True)
    assert eval (grocery_store_active_grocer_id() == "inga")
    assert eval (story_event_available("GroceryStore", "enter"))
    assert eval (event_runtime.available["GroceryStore"]["enter"].target == "story_inga_grocery_morning_0")
    run Jump("GroceryStore")
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    assert eval ("Лавка уже открыта" in scene_runtime.text)
    screenshot "inga_grocery_morning_start.png"
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("мгновенно становится тихо" in scene_runtime.text) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("Я Ингенборг" in scene_runtime.text) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("Хороший завтрак" in scene_runtime.text) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (threads["beckyIngaLucasPath"].num == 1) timeout 10.0
    assert eval (rooms.current_code == "GroceryStore" and main_ui_runtime.mode == "scene") timeout 5.0
    assert eval (scene_runtime.picture == rooms.get("GroceryStore").bg_picture)
    screenshot "inga_grocery_morning_return.png"
    assert eval (Inga.known and Inga.acquaintance_stage >= 1)
    assert eval (story_event_available("talk_becky", "becky_talk_inga1"))
    assert eval (not story_event_available("GroceryStore", "enter") or event_runtime.available["GroceryStore"]["enter"].target != "story_inga_grocery_morning_0")

testcase becky_regular_evening_visit_enters_dinner:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 19
        calendar_v2.minute = 0
        threads["beckyHome"].advanceTo(3, complete_at_end=True)
        player.appearance.current_dress = "citydress"
        Becky.home_front_checked_today = True
        _home_visits_before = Becky.home_visit_count
        rooms.enter("MarketPlace")
    run movement_actions("BeckyHomeFront", 10)
    advance until screen "choice" timeout 20.0
    assert eval (rooms.get("BeckyHomeFront").state["arrival_mode"] == "")
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (rooms.current_code == "BeckyHome") timeout 10.0
    screenshot "becky_home_admission.png"
    assert eval (main_ui_runtime.action_items == [] and main_ui_runtime.action_title == rooms.get("BeckyHome").display_name)
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and any(item.caption == "Осмотреть Ребекку" for item in renpy.get_screen("choice").scope.get("items", []))) timeout 20.0
    assert eval (rooms.current_code == "BeckyHome")
    assert eval (Becky.home_visit_count == _home_visits_before + 1)
    assert eval (scene_runtime.picture == "images/becky/dinner/DinnerInga.jpg")
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.scene_origin is not None and main_ui_runtime.action_items == [])
    assert eval (any(item.caption == "Осмотреть Ребекку" for item in renpy.get_screen("choice").scope["items"]))

testcase becky_dinner_refusal_keeps_authored_farewell:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        rooms.enter("BeckyHome")
        threads["beckyDinner"].reset()
        calendar_v2.week = 1
        calendar_v2.hour = 19
        calendar_v2.minute = 0
        main_ui_runtime.mode = "scene"
        main_ui_runtime.scene_origin = None
        main_ui_runtime.action_items = rooms.get("BeckyHome").build_exit_items()
    run Call("IntBeckyGuest")
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    $ dinnertime = 5
    $ _eat_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Кушать")
    click id ("choice_panel_button_%d" % _eat_index) pos (0.5, 0.5)
    click pos (960, 900) until eval (renpy.get_screen("choice") is not None and any(item.caption == "Взять Бекки под руку и идти наверх в спальню" for item in renpy.get_screen("choice").scope.get("items", []))) timeout 20.0
    $ _upstairs_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Взять Бекки под руку и идти наверх в спальню")
    click id ("choice_panel_button_%d" % _upstairs_index) pos (0.5, 0.5)
    advance until screen "say" timeout 20.0
    assert eval (rooms.current_code == "BeckyHome" and main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    click pos (960, 900) until eval (renpy.get_screen("choice") is not None and [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Попрощаться и идти домой"]) timeout 20.0
    assert eval (rooms.current_code == "BeckyHome" and main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    click id "choice_panel_button_0" pos (0.5, 0.5)
    click pos (960, 900) until eval (rooms.current_code == "MarketPlace") timeout 20.0
    assert eval (calendar_v2.hour == 20 and calendar_v2.minute == 0 and main_ui_runtime.scene_origin is None)

testcase becky_dinner_reads_current_wear_panties:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        rooms.enter("BeckyHome")
        Becky.reset_sex_clothing_state()
        Becky.set_current_underwear("panties", "simplepanties")
    run Call("IntBeckyGuest")
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    $ _grope_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Полапать под столом Бекки")
    click id ("choice_panel_button_%d" % _grope_index) pos (0.5, 0.5)
    click pos (960, 900) until eval (int(dinnerbecky or 0) == 1 and renpy.get_screen("choice") is not None) timeout 10.0
    $ _grope_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Полапать под столом Бекки")
    click id ("choice_panel_button_%d" % _grope_index) pos (0.5, 0.5)
    click pos (960, 900) until eval (int(dinnerbecky or 0) == 2 and renpy.get_screen("choice") is not None) timeout 10.0
    $ Becky.remove_clothing_layer("panties")
    assert eval (Becky.clothing_layer("panties") == "")
    $ _grope_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Полапать под столом Бекки")
    click id ("choice_panel_button_%d" % _grope_index) pos (0.5, 0.5)
    click pos (960, 900) until eval (int(dinnerbecky or 0) == 3 and renpy.get_screen("choice") is not None) timeout 10.0
    $ _grope_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Полапать под столом Бекки")
    click id ("choice_panel_button_%d" % _grope_index) pos (0.5, 0.5)
    click pos (960, 900) until eval (int(dinnerbecky or 0) == 4 and renpy.get_screen("choice") is not None) timeout 10.0
    assert eval (int(dinnertime or 0) == 4 and Becky.clothing_layer("panties") == "")

testcase inga_grocery_morning_clock_gates:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        threads["beckyIngaLucasPath"].reset()
        initStoryEventRuntime(True)
        _morning_event = next(evt for evt in threads["beckyIngaLucasPath"].data.triggers[0] if evt.target == "story_inga_grocery_morning_0")
        calendar_v2.week = 1
        calendar_v2.hour = 5
    assert eval (not _morning_event.checkHour())
    $ calendar_v2.hour = 6
    assert eval (_morning_event.checkHour() and _morning_event.checkDay() and _morning_event.checkConditions())
    $ calendar_v2.hour = 8
    assert eval (not _morning_event.checkHour())
    python:
        calendar_v2.week = 7
        calendar_v2.hour = 7
    assert eval (not _morning_event.checkDay())

testcase inga_grocery_morning_leave_keeps_progress:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 7
        calendar_v2.minute = 0
        threads["beckyIngaLucasPath"].reset()
        event_runtime.fired_keys_today = []
        initStoryEventRuntime(True)
    run Jump("GroceryStore")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (rooms.current_code == "MarketPlace") timeout 10.0
    assert eval (threads["beckyIngaLucasPath"].num == 0)
    assert eval (main_ui_runtime.scene_origin is None)

testcase becky_legacy_progress_migrates_to_threads:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        threads["beckyHome"].reset()
        threads["beckyDinner"].reset()
        threads["beckySex"].reset()
        threads["beckyEddieSex"].reset()
        Becky.home_visit_stage = 7
        Becky.home_sex_unlocked = True
        Becky.open_oral_stage = 1
        Becky.eddie_join_stage = 4
        updateSave_V81()
    assert eval (threads["beckyHome"].completed and int(threads["beckyHome"].num or 0) == 3) timeout 5.0
    assert eval (threads["beckyDinner"].completed and int(threads["beckyDinner"].num or 0) == 3) timeout 5.0
    assert eval (threads["beckySex"].completed and int(threads["beckySex"].num or 0) == 2) timeout 5.0
    assert eval (threads["beckyEddieSex"].completed and int(threads["beckyEddieSex"].num or 0) == 5) timeout 5.0
    assert eval (not hasattr(Becky, "home_visit_stage")) timeout 5.0
    assert eval (not hasattr(Becky, "home_sex_unlocked")) timeout 5.0
    assert eval (not hasattr(Becky, "open_oral_stage")) timeout 5.0
    assert eval (not hasattr(Becky, "eddie_join_stage")) timeout 5.0

testcase becky_kitchen_friendship_survives_repeat_visit:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 2
        calendar_v2.hour = 19
        calendar_v2.minute = 0
        Becky.sandra_kitchen_friendship_progress = 3
        rooms.enter("TavernKitchen")
    run Call("story_becky_sandra_kitchen_visit")
    advance until screen "choice" timeout 20.0
    assert eval (Becky.sandra_kitchen_friendship_progress == 3)
    assert eval (Becky.sandra_friendship_stage() == 2)
    assert eval (scene_runtime.text.startswith("Зайдя вечером на кухню") and scene_runtime.text == scene_runtime.location_text)
    screenshot "becky_kitchen_visit.png"
    $ _leave_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Не мешать разговору")
    click id ("choice_panel_button_%d" % _leave_index) pos (0.5, 0.5) until eval (scene_runtime.text.startswith("Вы не стали мешать")) timeout 10.0
    assert eval (renpy.get_screen("choice").scope["items"][0].caption == "Вернуться к своим делам")
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (main_ui_runtime.mode != "event") timeout 10.0

testcase becky_clothes_offer_schedules_one_appointment:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 14
        calendar_v2.minute = 0
        Becky.rel = 9
        Becky.talked_today = 0
        daily_events.delete("becky", "BuyDressTom")
        daily_events.delete("becky", "BuyDress")
        rooms.enter("GroceryStore")
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    $ _clothes_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Поговорить с Бекки об одежде")
    click id ("choice_panel_button_%d" % _clothes_index) pos (0.5, 0.5) until eval (any(item.caption == "Предложить купить вдовушке обновку" for item in renpy.get_screen("choice").scope["items"])) timeout 10.0
    $ _clothes_buy_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Предложить купить вдовушке обновку")
    click id ("choice_panel_button_%d" % _clothes_buy_index) pos (0.5, 0.5) until eval (scene_runtime.text.startswith('\"Бекки, а давай к портнихе')) timeout 10.0
    screenshot "becky_clothes_offer.png"
    assert eval (scene_runtime.text == scene_runtime.location_text and not renpy.get_screen("say"))
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (scene_runtime.text.startswith('\"Прямо аттракцион')) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (scene_runtime.text.startswith('\"Да, давай завтра')) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (any(item.caption == "Закончить разговор" for item in renpy.get_screen("choice").scope["items"])) timeout 10.0
    assert eval (rooms.current_code == "GroceryStore" and main_ui_runtime.mode == "talk")
    assert eval (daily_events.exists("becky", "BuyDressTom") == 1)
    assert eval (sum(row["GirlName"] == "becky" and row["EventType"] == "BuyDressTom" for row in daily_events.rows) == 1)
    assert eval (Becky.talk_count() == 1 and not Becky.dress_change_flags()["can_buy"])
    python:
        daily_events.end_day(2)
        calendar_v2.week = 2
        calendar_v2.hour = 9
        calendar_v2.minute = 0
        Becky.reset_daily()
    assert eval (daily_events.exists("becky", "BuyDressTom") == 0 and daily_events.exists("becky", "BuyDress") == 1)
    run Jump("DressShop")
    advance until screen "dress_shop_catalog_page" timeout 20.0
    assert eval (rooms.current_code == "DressShop" and renpy.get_screen("dress_shop_catalog_page").scope["girl_name"] == "becky")
    assert eval (daily_events.exists("becky", "BuyDress") == 0 and daily_events.exists("becky", "DressNoShow") == 0)
    screenshot "becky_tailor_appointment.png"
    run Hide("dress_shop_catalog_page")

testcase becky_kitchen_visits_then_honey_tea:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.daysInGame = 31
        calendar_v2.week = 2
        calendar_v2.hour = 19
        calendar_v2.minute = 0
        Becky.sandra_kitchen_friendship_progress = 0
        player.add_item("energy_tea_001", 1)
        _tea_before = player.item_count("energy_tea_001")
        rooms.enter("TavernKitchen")
    assert eval (people.location("becky") == "TavernKitchen" and people.location("sandra") == "TavernKitchen")
    run Call("story_becky_sandra_kitchen_visit")
    advance until screen "choice" timeout 20.0
    assert eval (Becky.sandra_kitchen_friendship_progress == 1 and not tavern_kitchen_can_share_tea_with_sandra_and_becky())
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (scene_runtime.text.startswith("Вы не стали мешать")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (main_ui_runtime.mode != "event") timeout 10.0
    run Call("story_becky_sandra_kitchen_visit")
    advance until screen "choice" timeout 20.0
    assert eval (Becky.sandra_kitchen_friendship_progress == 2 and tavern_kitchen_can_share_tea_with_sandra_and_becky())
    $ _tea_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Угостить Сандру и Бекки бодрящим чаем")
    click id ("choice_panel_button_%d" % _tea_index) pos (0.5, 0.5) until eval (Becky.sandra_kitchen_friendship_progress == 3) timeout 10.0
    assert eval (player.item_count("energy_tea_001") == _tea_before - 1 and Becky.sandra_friendship_stage() == 2)
    assert eval (str(scene_runtime.picture).endswith("becky_visit_1.png"))
    screenshot "becky_kitchen_tea.png"
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (main_ui_runtime.mode != "event") timeout 10.0

testcase becky_regular_invitation_reads_objections_before_unlock:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 14
        calendar_v2.minute = 0
        Becky.rel = 13
        Becky.talked_today = 0
        threads["beckyHome"].reset()
        threads["beckyHome"].advanceTo(2)
        threads["beckyIngaLucasPath"].advanceTo(4, complete_at_end=True)
        threads["beckyEddieBackstory"].advanceTo(2, complete_at_end=True)
        threads["beckyHusbandBackstory"].advanceTo(2)
        player.appearance.current_dress = "citydress"
        event_runtime.fired_keys_today = []
        rooms.enter("GroceryStore")
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    $ _invite_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Попробовать напросится в гости")
    click id ("choice_panel_button_%d" % _invite_index) pos (0.5, 0.5) until eval (scene_runtime.text.startswith("Вы решили попробовать напросится")) timeout 10.0
    assert eval (scene_runtime.text == scene_runtime.location_text and not renpy.get_screen("say"))
    assert eval (threads["beckyHome"].num == 2)
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (scene_runtime.text.startswith('\"Вот черт языкастый!')) timeout 20.0
    assert eval (threads["beckyHome"].num == 2 and Becky.talk_count() == 0)
    screenshot "becky_invitation_consent.png"
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (Becky.talk_count() == 1) timeout 10.0
    assert eval (threads["beckyHome"].num == 3 and rooms.current_code == "GroceryStore")
    assert eval (any(item.caption == "Закончить разговор" for item in renpy.get_screen("choice").scope["items"]))

testcase becky_sherwood_disclosure_returns_to_talk:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        calendar_v2.week = 1
        calendar_v2.hour = 14
        Becky.rel = 17
        Becky.talked_today = 0
        Becky.trade_offer_stage = 1
        Becky.admitted_sherwood_stage = 0
        Becky.knows_blackwood = True
        rooms.enter("GroceryStore")
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    $ _sherwood_index = next(i for i, item in enumerate(renpy.get_screen("choice").scope["items"]) if item.caption == "Насчет дороги в Куниделл")
    click id ("choice_panel_button_%d" % _sherwood_index) pos (0.5, 0.5) until eval (scene_runtime.text.startswith('\"Дорожка в Куниделл')) timeout 10.0
    assert eval (Becky.admitted_sherwood_stage == 0 and Becky.talk_count() == 0)
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (scene_runtime.text.startswith('\"Через него')) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (scene_runtime.text.startswith('\"А там никто')) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (scene_runtime.text.startswith('\"Ну как тебе сказать')) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (scene_runtime.text == '\"И что?\"') timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (Becky.admitted_sherwood_stage == 1) timeout 10.0
    screenshot "becky_sherwood_disclosure.png"
    assert eval (renpy.get_screen("choice").scope["items"][0].caption == "Вернуться к разговору")
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (any(item.caption == "Закончить разговор" for item in renpy.get_screen("choice").scope["items"])) timeout 10.0
    assert eval (rooms.current_code == "GroceryStore" and main_ui_runtime.mode == "talk")
    assert eval (Becky.talk_count() == 1)
    assert eval (any(item.caption == "Так что же ты меня дурила-то?" for item in renpy.get_screen("choice").scope["items"]))
'''


def build_temp_project(root: Path, temp_root: Path) -> Path:
    source_game = root / "game"
    temp_project = temp_root / "TractirExternalBeckyProject"
    temp_game = temp_project / "game"
    ensure_clean_dir(temp_game)
    for entry in source_game.iterdir():
        target = temp_game / entry.name
        if entry.is_dir():
            if entry.name in {"cache", "__pycache__", "saves", "saves_test_run"}:
                continue
            junction_dir(entry, target)
        elif entry.suffix.lower() in {".rpy", ".rpym", ".py", ".json", ".png", ".jpg", ".jpeg", ".webp"}:
            hardlink_or_copy(entry, target)
    (temp_game / "_external_becky_branch_test.rpy").write_text(TEST_RPY, encoding="utf-8")
    return temp_project


def run_renpy(renpy_exe: Path, temp_project: Path, timeout: int, only: str = "global") -> int:
    test_savedir = temp_project / ".test-saves"
    test_savedir.mkdir(parents=True, exist_ok=True)
    args = [
        str(renpy_exe),
        str(temp_project),
        "--savedir",
        str(test_savedir),
        "test",
        only,
        "--hide-execution",
        "no",
        "--report-detailed",
    ]
    try:
        completed = subprocess.run(
            args,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if completed.stdout:
            safe_print(completed.stdout)
        return int(completed.returncode or 0)
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        if output:
            safe_print(output)
        print(f"Ren'Py Becky test timed out after {timeout} seconds.")
        return 124


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=RENpy_DEFAULT)
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--only", default="global", help="Ren'Py testcase or suite name")
    args = parser.parse_args()

    root = project_root()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.exists():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")

    temp_root = Path(tempfile.mkdtemp(prefix="tractir_becky_branch_"))
    try:
        temp_project = build_temp_project(root, temp_root)
        print(f"Temporary Becky test project: {temp_project}")
        return run_renpy(renpy_exe, temp_project, args.timeout, args.only)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary Becky test project: {temp_root}")
        else:
            remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
