#!/usr/bin/env python3
"""Run focused Eddie/Becky/church branch checks from a temporary Ren'Py project.

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

testcase eddie_talk_opens_becky_join_setup:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ threads["beckySex"].advanceTo(1, force_active=True)
    $ threads["beckyEddieSex"].advanceTo(0, force_active=True)
    $ Eddie.rel = 9
    $ Eddie.talked_today = 0
    $ Eddie.saw_mother_sex = True
    $ Eddie.seen_with_georgett = True
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_eddie", "becky_eddie_sex")) timeout 5.0
    assert eval (str(event_runtime.available["talk_eddie"]["becky_eddie_sex"].target or "") == "IntEddieTalkMomHelper") timeout 5.0
    run Call("checkTriggers", "talk_eddie", "becky_eddie_sex", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyEddieSex"].num or 0) == 1 and int(Eddie.talked_today or 0) == 1) timeout 20.0

testcase eddie_failed_offer_allows_the_second_authored_attempt:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ threads["beckySex"].advanceTo(1, force_active=True)
    $ threads["beckyEddieSex"].advanceTo(0, force_active=True)
    $ Eddie.rel = 3
    $ Eddie.talked_today = 0
    $ Eddie.saw_mother_sex = True
    $ Eddie.seen_with_georgett = True
    $ event_runtime.fired_keys_today = []
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_eddie", "becky_eddie_sex")) timeout 5.0
    run Call("checkTriggers", "talk_eddie", "becky_eddie_sex", 0)
    click pos (0.5, 0.5) until eval (int(Eddie.talked_today or 0) == 1) timeout 20.0
    assert eval (int(threads["beckyEddieSex"].num or 0) == 0)
    assert eval (story_event_available("talk_eddie", "becky_eddie_sex")) timeout 5.0
    run Call("checkTriggers", "talk_eddie", "becky_eddie_sex", 0)
    click pos (0.5, 0.5) until eval (int(Eddie.talked_today or 0) == 2) timeout 20.0
    assert eval (not story_event_available("talk_eddie", "becky_eddie_sex")) timeout 5.0

testcase becky_from_dinner_runs_eddie_first_join:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ threads["beckyEddieSex"].advanceTo(1, force_active=True)
    $ rooms.get("BeckyHomeFront").state["arrival_mode"] = "FromDances"
    $ Becky.priest_advice_stage = 3
    $ Becky.rel = 20
    $ Becky.corruption = 55
    $ Eddie.rel = 10
    $ initStoryEventRuntime(True)
    assert eval (not story_event_available("BeckyHome", "enter")) timeout 5.0
    $ rooms.get("BeckyHomeFront").state["arrival_mode"] = "FromDinner"
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("BeckyHome", "enter")) timeout 5.0
    assert eval (str(event_runtime.available["BeckyHome"]["enter"].target or "") == "BeckyEddieJoinFirst") timeout 5.0
    $ _eddie_join_start_minutes = int(calendar_v2.daysInGame or 0) * 1440 + calendar_v2.clock_minutes()
    run Call("checkTriggers", "BeckyHome", "enter", 0)
    advance until screen "choice" timeout 20.0
    assert eval ("Поцеловать Бекки и незаметно открыть засов" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Идти за вдовой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    click pos (960, 900) until screen "choice" timeout 20.0
    assert eval ("Кивком показать Эдди, чтобы он уважил просьбу Бекки" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    click pos (960, 900) until eval (int(threads["beckyEddieSex"].num or 0) == 4 and str(rooms.current_code or "") == "MarketPlace") timeout 30.0
    assert eval (int(Becky.rel or 0) == 20 and int(Becky.corruption or 0) == 60 and int(Eddie.rel or 0) == 15) timeout 5.0
    assert eval ((int(calendar_v2.daysInGame or 0) * 1440 + calendar_v2.clock_minutes()) - _eddie_join_start_minutes == 60) timeout 5.0

testcase becky_church_priority_and_eddie_service_schedule:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ calendar_v2.day = 7
    $ calendar_v2.week = 7
    $ calendar_v2.period = 1
    $ calendar_v2.cycle = 1100
    $ calendar_v2.daysInGame = 6
    $ calendar_v2.hour = 8
    $ calendar_v2.minute = 0
    $ rooms.enter("Church")
    assert eval (str(people.location("eddie") or "") == "Church" and str(people.schedule_state("eddie").get("label", "") or "") == "sunday_service") timeout 5.0
    run Call("ChurchServiceBlanken")
    advance until screen "choice" timeout 20.0
    assert eval (str(scene_runtime.picture or "") == "images/becky/church/cermon.png") timeout 5.0
    assert eval ("Эдди, ее рыжий управляющий лавкой" in str(scene_runtime.location_text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (renpy.get_screen("choice") is None) timeout 20.0
    $ calendar_v2.hour = 9
    $ calendar_v2.minute = 29
    assert eval (str(people.location("eddie") or "") == "Church") timeout 5.0
    $ calendar_v2.minute = 30
    assert eval (str(people.location("eddie") or "") == "BeckyHome") timeout 5.0
    $ calendar_v2.day = 22
    $ calendar_v2.daysInGame = 21
    $ calendar_v2.hour = 8
    $ calendar_v2.minute = 0
    assert eval (str(people.location("eddie") or "") == "OutOfTown") timeout 5.0

    $ calendar_v2.day = 7
    $ calendar_v2.daysInGame = 6
    $ calendar_v2.hour = 12
    $ Georgett.known = True
    $ Liza.known = True
    $ Georgett.set_story_value("churchgeorgettadmit", 1)
    $ Georgett.set_story_value("SawChurchAfterCermon", 0)
    $ Georgett.set_story_value("churchlizaadmit", 1)
    $ Becky.priest_advice_stage = 1
    $ initStoryEventRuntime(True)
    assert eval (str(event_runtime.available["Church"]["after_cermon_walk"].target or "") == "story_becky_church_after_sermon") timeout 5.0
    $ Becky.priest_advice_stage = 2
    $ initStoryEventRuntime(True)
    assert eval (str(event_runtime.available["Church"]["after_cermon_walk"].target or "") == "story_becky_church_after_sermon") timeout 5.0
    $ Becky.priest_advice_stage = 3
    $ initStoryEventRuntime(True)
    assert eval (str(event_runtime.available["Church"]["after_cermon_walk"].target or "") == "story_georgett_church_after_sermon") timeout 5.0
'''


def build_temp_project(root: Path, temp_root: Path) -> Path:
    source_game = root / "game"
    temp_project = temp_root / "TractirExternalEddieProject"
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
    (temp_game / "_external_eddie_branch_test.rpy").write_text(TEST_RPY, encoding="utf-8")
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
        print(f"Ren'Py Eddie test timed out after {timeout} seconds.")
        return 124


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=RENpy_DEFAULT)
    parser.add_argument("--timeout", type=int, default=480)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    root = project_root()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.exists():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")

    temp_root = Path(tempfile.mkdtemp(prefix="tractir_eddie_branch_"))
    try:
        temp_project = build_temp_project(root, temp_root)
        print(f"Temporary Eddie test project: {temp_project}")
        return run_renpy(renpy_exe, temp_project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary Eddie test project: {temp_root}")
        else:
            remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
