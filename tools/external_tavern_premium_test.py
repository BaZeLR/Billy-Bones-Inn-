#!/usr/bin/env python3
"""Run focused tavern-premium gameplay checks in a temporary Ren'Py project.

Generated Ren'Py testcase code is written only to the temporary project, not
to this repository's game folder.
"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


RENPY_DEFAULT = r"C:\Users\blank\renpy\renpy-8.5.2-sdk\renpy.exe"


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
    try:
        return bool(os.lstat(path).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except (AttributeError, OSError):
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
init python:
    EXTERNAL_PREMIUM_JOB_KEYS = (
        "jobHallAvail", "jobWhoreAvail", "jobGloryHoleAvail",
        "jobkitchen", "jobcleaning", "jobwaitress", "jobwhore", "jobgloryhole",
        "jobkitchentomorrow", "jobcleaningtomorrow", "jobwaitresstomorrow",
        "jobwhoreTommorow", "jobgloryholeTommorow",
    )

    def external_prepare_tavern_premium(stamp="premium-test-week", money=2000):
        for girl_id, info in people.girl_items():
            for job_key in EXTERNAL_PREMIUM_JOB_KEYS:
                info.set_job_value(job_key, 0)
        Amanda.set_job_value("jobwaitress", 1)
        Melissa.set_job_value("jobkitchen", 1)
        Amanda.set_skill("waitress", 10)
        Melissa.set_skill("cooking", 20)
        Amanda.skill_gains_today = {}
        Melissa.skill_gains_today = {}
        Amanda.rel = 5
        Melissa.rel = 6
        Amanda.mana = 10
        Melissa.mana = 20
        Amanda.corruption = 7
        Melissa.corruption = 8
        Sandra.rel = 10
        Sandra.asked_today = 0
        Sandra.talked_today = 0
        player.set_money(money)
        player.tavern_management.weekly_chores_last_eval_stamp = str(stamp)
        player.tavern_management.team_premium_last_eval_stamp = ""

        rooms.enter("TavernSandraRoom")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.talk_picture = ""
        main_ui_runtime.action_title = "Комната Сандры"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = tavern_sandra_room_action_items()
        scene_runtime.picture = tavern_sandra_room_picture()
        scene_runtime.text = tavern_sandra_room_text()
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

        worker_ids = [girl_id for girl_id, info in people.girl_items() if info.is_tavern_worker()]
        assert len(worker_ids) == 2
        assert set(worker_ids) == set(("amanda", "melissa"))
        return worker_ids

    def external_prepare_liza_premium(stamp="liza-premium-test-week", money=2000):
        for girl_id, info in people.girl_items():
            for job_key in EXTERNAL_PREMIUM_JOB_KEYS:
                info.set_job_value(job_key, 0)
        Liza.set_job_value("jobwaitress", 1)
        Liza.set_skill("waitress", 10)
        Liza.skill_gains_today = {}
        Liza.rel = 18
        Liza.corruption = 5
        Liza.mana = 10
        Sandra.rel = 10
        Sandra.asked_today = 0
        Sandra.talked_today = 0
        player.set_money(money)
        player.tavern_management.weekly_chores_last_eval_stamp = str(stamp)
        player.tavern_management.team_premium_last_eval_stamp = ""

        rooms.enter("TavernSandraRoom")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.talk_picture = ""
        main_ui_runtime.action_title = "Комната Сандры"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = tavern_sandra_room_action_items()
        scene_runtime.picture = tavern_sandra_room_picture()
        scene_runtime.text = tavern_sandra_room_text()
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

        worker_ids = [girl_id for girl_id, info in people.girl_items() if info.is_tavern_worker()]
        assert worker_ids == ["liza"]
        return worker_ids


testsuite global:
    teardown:
        exit

testcase tavern_team_premium_and_personal_reward:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        _premium_test_workers = external_prepare_tavern_premium("1100:2:7:7", 2000)
        _premium_test_other = "amanda"
        _premium_test_personal = "melissa"
        _premium_test_other_info = people.get_info(_premium_test_other)
        _premium_test_personal_info = people.get_info(_premium_test_personal)
        _premium_test_before = {
            girl_id: {
                "rel": int(info.rel or 0),
                "mana": int(info.mana or 0),
                "corruption": int(info.corruption or 0),
                "skill": int(info.skill_value("waitress" if girl_id == "amanda" else "cooking", 0) or 0),
            }
            for girl_id, info in ((_premium_test_other, _premium_test_other_info), (_premium_test_personal, _premium_test_personal_info))
        }
        _premium_origin = main_ui_context_snapshot()
    run Call("TavernSandraLedgerScene")
    advance until screen "choice" timeout 20.0
    assert eval ([str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Продолжить"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (any(str(item.caption or "").startswith("Выдать по 100 мараведи") for item in renpy.get_screen("choice").scope.get("items", []))) timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and str(main_ui_runtime.action_title or "") == "Трактирные книги" and main_ui_runtime.action_items == []) timeout 5.0
    assert eval (int(_premium_total_100 or 0) == 200) timeout 5.0
    $ _premium_100_index = next(index for index, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "").startswith("Выдать по 100 мараведи"))
    click id ("choice_panel_button_%d" % int(_premium_100_index)) pos (0.5, 0.5) until eval ([str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Раздать премии"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ([str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Продолжить"]) timeout 20.0
    assert eval (str(scene_runtime.text or "") == "\n\n".join([tavern_premium_reaction_text(girl_id, _premium_test_before[girl_id]["corruption"]) for girl_id in _premium_test_workers])) timeout 5.0
    assert eval (str(scene_runtime.picture or "") == "images/tavern/mainhall/tavern_crew.jpg") timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("Выделить еще одну личную премию" in [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (int(player.economy.money or 0) == 1800) timeout 5.0
    assert eval (all(int(people.get_info(girl_id).rel or 0) == _premium_test_before[girl_id]["rel"] + 1 for girl_id in _premium_test_workers)) timeout 5.0
    assert eval (all(int(people.get_info(girl_id).mana or 0) == _premium_test_before[girl_id]["mana"] + 3 for girl_id in _premium_test_workers)) timeout 5.0
    assert eval (int(Amanda.skill_value("waitress", 0) or 0) == 11 and int(Melissa.skill_value("cooking", 0) or 0) == 21) timeout 5.0
    assert eval (int(Amanda.skill_gains_today.get("waitress", 0) or 0) == 1 and int(Melissa.skill_gains_today.get("cooking", 0) or 0) == 1) timeout 5.0
    assert eval (all(int(people.get_info(girl_id).corruption or 0) == _premium_test_before[girl_id]["corruption"] for girl_id in _premium_test_workers)) timeout 5.0
    assert eval (str(player.tavern_management.team_premium_last_eval_stamp or "") == "1100:2:7:7") timeout 5.0
    $ _premium_personal_index = [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])].index("Выделить еще одну личную премию")
    click id ("choice_panel_button_%d" % int(_premium_personal_index)) pos (0.5, 0.5) until eval (any(str(item.caption or "").startswith("Дополнительно наградить") for item in renpy.get_screen("choice").scope.get("items", []))) timeout 20.0
    $ _premium_personal_captions = [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])]
    assert eval (len([caption for caption in _premium_personal_captions if caption.startswith("Дополнительно наградить")]) == 2) timeout 5.0
    assert eval (all(any(name in caption for caption in _premium_personal_captions) for name in ("Аманду", "Мелиссу"))) timeout 5.0
    assert eval (not any(name in caption for caption in _premium_personal_captions for name in ("Сандру", "Лизетту", "Жоржетту"))) timeout 5.0
    assert eval ("Рассмотреть следующую кандидатуру" not in _premium_personal_captions) timeout 5.0
    $ _premium_melissa_index = next(index for index, caption in enumerate(_premium_personal_captions) if caption.startswith("Дополнительно наградить") and "Мелиссу" in caption)
    click id ("choice_panel_button_%d" % int(_premium_melissa_index)) pos (0.5, 0.5) until eval ([str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Продолжить"]) timeout 20.0
    assert eval (int(player.economy.money or 0) == 1700) timeout 5.0
    assert eval (int(_premium_test_other_info.rel or 0) == _premium_test_before[_premium_test_other]["rel"] + 1 and int(_premium_test_other_info.mana or 0) == _premium_test_before[_premium_test_other]["mana"] + 3 and int(_premium_test_other_info.corruption or 0) == _premium_test_before[_premium_test_other]["corruption"]) timeout 5.0
    assert eval (int(_premium_test_personal_info.rel or 0) == _premium_test_before[_premium_test_personal]["rel"] + 2 and int(_premium_test_personal_info.mana or 0) == _premium_test_before[_premium_test_personal]["mana"] + 6 and int(_premium_test_personal_info.corruption or 0) == _premium_test_before[_premium_test_personal]["corruption"] + 1) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (main_ui_runtime.scene_origin is None and str(main_ui_runtime.action_title or "") == str(_premium_origin["title"] or "")) timeout 5.0
    assert eval (str(scene_runtime.picture or "") == str(_premium_origin["picture"] or "") and str(scene_runtime.text or "") == str(_premium_origin["main_text"] or "") and str(scene_runtime.location_text or "") == str(_premium_origin["location_text"] or "")) timeout 5.0
    assert eval ([str(item.caption or "") for item in main_ui_runtime.action_items] == [str(item.caption or "") for item in _premium_origin["items"]]) timeout 5.0
    python:
        _premium_repeat_money = int(player.economy.money or 0)
        _premium_repeat_other = (int(_premium_test_other_info.rel or 0), int(_premium_test_other_info.mana or 0), int(_premium_test_other_info.corruption or 0))
        _premium_repeat_personal = (int(_premium_test_personal_info.rel or 0), int(_premium_test_personal_info.mana or 0), int(_premium_test_personal_info.corruption or 0))
        _premium_repeat_origin = main_ui_context_snapshot()
    run Call("TavernSandraLedgerScene")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (int(player.economy.money or 0) == _premium_repeat_money) timeout 5.0
    assert eval ((int(_premium_test_other_info.rel or 0), int(_premium_test_other_info.mana or 0), int(_premium_test_other_info.corruption or 0)) == _premium_repeat_other) timeout 5.0
    assert eval ((int(_premium_test_personal_info.rel or 0), int(_premium_test_personal_info.mana or 0), int(_premium_test_personal_info.corruption or 0)) == _premium_repeat_personal) timeout 5.0
    assert eval (main_ui_runtime.scene_origin is None and str(main_ui_runtime.action_title or "") == str(_premium_repeat_origin["title"] or "") and str(scene_runtime.picture or "") == str(_premium_repeat_origin["picture"] or "")) timeout 5.0

testcase tavern_liza_team_and_personal_premium_are_visible:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        _premium_test_workers = external_prepare_liza_premium("1100:4:7:7", 2000)
        _liza_before = {
            "rel": int(Liza.rel or 0),
            "corruption": int(Liza.corruption or 0),
            "mana": int(Liza.mana or 0),
            "skill": int(Liza.skill_value("waitress", 0) or 0),
        }
    run Call("TavernSandraLedgerScene")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (any(str(item.caption or "").startswith("Выдать по 200 мараведи") for item in renpy.get_screen("choice").scope.get("items", []))) timeout 20.0
    $ _premium_200_index = next(index for index, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if str(item.caption or "").startswith("Выдать по 200 мараведи"))
    click id ("choice_panel_button_%d" % int(_premium_200_index)) pos (0.5, 0.5) until eval ([str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Раздать премии"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ([str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Продолжить"]) timeout 20.0
    assert eval (str(scene_runtime.text or "") == tavern_premium_reaction_text("liza", _liza_before["corruption"])) timeout 5.0
    assert eval (str(scene_runtime.picture or "") == str(LizaStaticData.image_path("tavern", "wench_happy") or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("Выделить еще одну личную премию" in [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _premium_personal_index = [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])].index("Выделить еще одну личную премию")
    click id ("choice_panel_button_%d" % int(_premium_personal_index)) pos (0.5, 0.5) until eval (any("Лизетту" in str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", []))) timeout 20.0
    $ _premium_liza_index = next(index for index, item in enumerate(renpy.get_screen("choice").scope.get("items", [])) if "Лизетту" in str(item.caption or ""))
    click id ("choice_panel_button_%d" % int(_premium_liza_index)) pos (0.5, 0.5) until eval ([str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Продолжить"]) timeout 20.0
    assert eval (str(scene_runtime.text or "") == tavern_premium_reaction_text("liza", _liza_before["corruption"])) timeout 5.0
    assert eval (int(Liza.rel or 0) == _liza_before["rel"] + 2 and int(Liza.corruption or 0) == _liza_before["corruption"] + 1) timeout 5.0
    assert eval (int(Liza.mana or 0) == _liza_before["mana"] + 8 and int(Liza.skill_value("waitress", 0) or 0) == _liza_before["skill"] + 1) timeout 5.0
    assert eval (int(player.economy.money or 0) == 1600 and str(player.tavern_management.team_premium_last_eval_stamp or "") == "1100:4:7:7") timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0

testcase tavern_team_premium_defer_then_decline:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        _premium_test_workers = external_prepare_tavern_premium("1100:3:7:7", 2000)
        _premium_test_before = {
            girl_id: (int(info.rel or 0), int(info.mana or 0), int(info.corruption or 0))
            for girl_id, info in people.girl_items()
            if girl_id in _premium_test_workers
        }
        _premium_origin = main_ui_context_snapshot()
    run Call("TavernSandraLedgerScene")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("Вернуться к решению позже" in [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _premium_defer_index = [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])].index("Вернуться к решению позже")
    click id ("choice_panel_button_%d" % int(_premium_defer_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (str(player.tavern_management.team_premium_last_eval_stamp or "") == "" and int(player.economy.money or 0) == 2000) timeout 5.0
    assert eval (all((int(people.get_info(girl_id).rel or 0), int(people.get_info(girl_id).mana or 0), int(people.get_info(girl_id).corruption or 0)) == _premium_test_before[girl_id] for girl_id in _premium_test_workers)) timeout 5.0
    assert eval (main_ui_runtime.scene_origin is None and str(main_ui_runtime.action_title or "") == str(_premium_origin["title"] or "") and str(scene_runtime.picture or "") == str(_premium_origin["picture"] or "")) timeout 5.0
    run Call("TavernSandraLedgerScene")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("На этой неделе оставить команду без премии" in [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _premium_decline_index = [str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])].index("На этой неделе оставить команду без премии")
    click id ("choice_panel_button_%d" % int(_premium_decline_index)) pos (0.5, 0.5) until eval ([str(item.caption or "") for item in renpy.get_screen("choice").scope.get("items", [])] == ["Закончить подсчеты"]) timeout 20.0
    assert eval (str(player.tavern_management.team_premium_last_eval_stamp or "") == "1100:3:7:7" and int(player.economy.money or 0) == 2000) timeout 5.0
    assert eval (all((int(people.get_info(girl_id).rel or 0), int(people.get_info(girl_id).mana or 0), int(people.get_info(girl_id).corruption or 0)) == _premium_test_before[girl_id] for girl_id in _premium_test_workers)) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (main_ui_runtime.scene_origin is None and str(main_ui_runtime.action_title or "") == str(_premium_origin["title"] or "")) timeout 5.0
    assert eval (str(scene_runtime.picture or "") == str(_premium_origin["picture"] or "") and str(scene_runtime.text or "") == str(_premium_origin["main_text"] or "") and str(scene_runtime.location_text or "") == str(_premium_origin["location_text"] or "")) timeout 5.0
    assert eval ([str(item.caption or "") for item in main_ui_runtime.action_items] == [str(item.caption or "") for item in _premium_origin["items"]]) timeout 5.0

testcase tavern_team_premium_old_marker_migration:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    assert eval (calendar_v2.day_number_to_parts(6) == {"year": 1100, "month": 1, "day": 7, "week": 7}) timeout 5.0
    assert eval (calendar_v2.day_number_to_parts(7) == {"year": 1100, "month": 1, "day": 8, "week": 1}) timeout 5.0
    python:
        player.tavern_management.weekly_chores_last_eval_stamp = "1100:1:7:7"
        player.tavern_management.__dict__.pop("team_premium_last_eval_stamp", None)
        household.runtime_event_seen.clear()
        household.runtime_event_seen.update({
            "tavern_team_premium:6": 1,
            "tavern_team_premium:1": 1,
            "tavern_team_premium:bad": 1,
            "unrelated_event:6": 1,
        })
        tractir_save_patch_loaded_state()
    assert eval (str(player.tavern_management.team_premium_last_eval_stamp or "") == "1100:1:7:7") timeout 5.0
    assert eval (not any(str(key or "").startswith("tavern_team_premium:") for key in household.runtime_event_seen.keys())) timeout 5.0
    assert eval (int(household.runtime_event_seen.get("unrelated_event:6", 0) or 0) == 1) timeout 5.0
    python:
        player.tavern_management.weekly_chores_last_eval_stamp = "1100:1:7:7"
        player.tavern_management.__dict__.pop("team_premium_last_eval_stamp", None)
        household.runtime_event_seen.clear()
        household.runtime_event_seen.update({
            "tavern_team_premium:7": 1,
            "tavern_team_premium:2": 0,
            "unrelated_event:7": 1,
        })
        tractir_save_patch_loaded_state()
    assert eval (str(player.tavern_management.team_premium_last_eval_stamp or "") == "1100:1:7:7") timeout 5.0
    assert eval (not any(str(key or "").startswith("tavern_team_premium:") for key in household.runtime_event_seen.keys())) timeout 5.0
    assert eval (int(household.runtime_event_seen.get("unrelated_event:7", 0) or 0) == 1) timeout 5.0
    python:
        player.tavern_management.weekly_chores_last_eval_stamp = "1100:1:7:7"
        player.tavern_management.__dict__.pop("team_premium_last_eval_stamp", None)
        household.runtime_event_seen.clear()
        household.runtime_event_seen.update({
            "tavern_team_premium:1": 1,
            "tavern_team_premium:6": 0,
            "tavern_team_premium:bad": 1,
            "unrelated_event:1": 1,
        })
        tractir_save_patch_loaded_state()
    assert eval (str(player.tavern_management.team_premium_last_eval_stamp or "") == "") timeout 5.0
    assert eval (not any(str(key or "").startswith("tavern_team_premium:") for key in household.runtime_event_seen.keys())) timeout 5.0
    assert eval (int(household.runtime_event_seen.get("unrelated_event:1", 0) or 0) == 1) timeout 5.0
'''


def build_temp_project(root: Path, temp_root: Path) -> Path:
    source_game = root / "game"
    temp_project = temp_root / "TractirExternalTavernPremiumProject"
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
    (temp_game / "_external_tavern_premium_test.rpy").write_text(TEST_RPY, encoding="utf-8")
    return temp_project


def run_renpy(renpy_exe: Path, temp_project: Path, timeout: int) -> int:
    test_savedir = temp_project / ".test-saves"
    test_savedir.mkdir(parents=True, exist_ok=True)
    args = [
        str(renpy_exe),
        str(temp_project),
        "--savedir",
        str(test_savedir),
        "test",
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
        print(f"Ren'Py tavern-premium test timed out after {timeout} seconds.")
        return 124


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=480)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    root = project_root()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.exists():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")

    temp_root = Path(tempfile.mkdtemp(prefix="tractir_tavern_premium_"))
    try:
        temp_project = build_temp_project(root, temp_root)
        print(f"Temporary tavern-premium test project: {temp_project}")
        return run_renpy(renpy_exe, temp_project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary tavern-premium test project: {temp_root}")
        else:
            remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
