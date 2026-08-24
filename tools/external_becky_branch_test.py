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
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        CurLoc = "BeckyHome"
        location = CurLoc
        ArriveMode = "FromDances"
        Becky.home_visit_stage = 2
        Becky.eddie_join_stage = 0
        MyCurDress = "citydress"
    run Jump("BeckyHome")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(CurLoc or "") == "BeckyHome") timeout 5.0
    assert eval (str(ArriveMode or "") == "FromDances") timeout 5.0
    assert eval ("спальне" in str(MainTxt or "")) timeout 5.0
    assert eval ("зачем ты пришел" not in str(MainTxt or "")) timeout 5.0
    assert eval ("постучали" not in str(MainTxt or "")) timeout 5.0

testcase becky_home_front_from_dance_enter_house:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        week = 5
        time = 3
        hour = 20
        minute = 0
        Becky.home_visit_stage = 0
        Becky.home_front_checked_today = False
        MyCurDress = "citydress"
    run Call("BeckyHomeFront", "FromDances")
    advance until screen "choice" timeout 20.0
    assert eval (str(CurLoc or "") == "BeckyHomeFront") timeout 5.0
    assert eval (str(ArriveMode or "") == "FromDances") timeout 5.0
    assert eval (int(Becky.home_visit_stage or 0) == 1) timeout 5.0
    click "Зайти в дом" until eval (str(CurLoc or "") == "BeckyHome") timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (str(CurLoc or "") == "BeckyHome") timeout 5.0
    assert eval (str(ArriveMode or "") == "FromDances") timeout 5.0
    assert eval (int(Becky.home_visit_stage or 0) == 1) timeout 5.0
    run Jump("StreetTavern")

testcase becky_dance_accept_home_order:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        week = 5
        time = 3
        hour = 20
        minute = 0
        FridayDanceRoom.state["dance_count"] = 1
        DanceStep = 3
        DanceMaxIBD = 6
        HandsDance = "ass"
        KissDance = 1
        TitsDance = 0
        rooms.get("FridayDance").becky_home_invited = True
        Becky.home_visit_stage = 0
        Becky.home_front_checked_today = False
        Friends["becky"] = 20
        sluttiness["becky"] = 40
        HadSex["becky"] = 0
        MyCurDress = "citydress"
    run Call("int_becky_dance")
    advance until screen "choice" timeout 20.0
    click "Принять предложение вдовы" until eval (str(CurLoc or "") == "BeckyHomeFront") timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (str(CurLoc or "") == "BeckyHomeFront") timeout 5.0
    assert eval (str(ArriveMode or "") == "FromDances") timeout 5.0
    assert eval (int(FridayDanceRoom.state["dance_count"] or 0) == 5) timeout 5.0
    click "Зайти в дом" until eval (str(CurLoc or "") == "BeckyHome") timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (str(CurLoc or "") == "BeckyHome") timeout 5.0
    assert eval (str(ArriveMode or "") == "FromDances") timeout 5.0
    run Jump("StreetTavern")

testcase friday_dance_find_becky_opens_becky_dance:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        week = 5
        time = 3
        hour = 20
        minute = 0
        FridayDanceRoom.state["dance_count"] = 0
        DanceStep = 0
        Becky.left_dances = 0
        Friends["becky"] = 20
        sluttiness["becky"] = 40
    run Jump("FridayDance")
    advance until screen "choice" timeout 20.0
    click "Найти Бекки Блэнкеншип" until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (str(CurLoc or "") == "FridayDance") timeout 5.0
    assert eval (int(DanceStep or 0) == 1) timeout 5.0
    assert eval (int(FridayDanceRoom.state["dance_count"] or 0) == 1) timeout 5.0
    run Jump("StreetTavern")
'''


def build_temp_project(root: Path, temp_root: Path) -> Path:
    source_game = root / "game"
    temp_project = temp_root / "TractirExternalBeckyProject"
    temp_game = temp_project / "game"
    ensure_clean_dir(temp_game)
    for entry in source_game.iterdir():
        target = temp_game / entry.name
        if entry.is_dir():
            if entry.name in {"cache", "__pycache__", "saves_test_run"}:
                continue
            junction_dir(entry, target)
        elif entry.suffix.lower() in {".rpy", ".rpym", ".py", ".json", ".png", ".jpg", ".jpeg", ".webp"}:
            hardlink_or_copy(entry, target)
    (temp_game / "_external_becky_branch_test.rpy").write_text(TEST_RPY, encoding="utf-8")
    return temp_project


def run_renpy(renpy_exe: Path, temp_project: Path, timeout: int) -> int:
    args = [
        str(renpy_exe),
        str(temp_project),
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
        print(f"Ren'Py Becky test timed out after {timeout} seconds.")
        return 124


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=RENpy_DEFAULT)
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    root = project_root()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.exists():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")

    temp_root = Path(tempfile.mkdtemp(prefix="tractir_becky_branch_"))
    try:
        temp_project = build_temp_project(root, temp_root)
        print(f"Temporary Becky test project: {temp_project}")
        return run_renpy(renpy_exe, temp_project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary Becky test project: {temp_root}")
        else:
            remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
