#!/usr/bin/env python3
"""Run focused Eddie/Becky/Sherwood branch checks from a temporary Ren'Py project.

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
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        CurLoc = "TavernMain"
        location = CurLoc
        CurrentLoc["georgett"] = "TavernMain"
        Friends["eddie"] = 10
        Talked["eddie"] = 0
        EddieVar["SawWithGeorgett"] = 1
        EddieVar["SawMomSex"] = 1
        BeckyVar["HomeSex"] = 1
        BeckyVar["EddieTryToFuck"] = 0
    run Call("IntEddieTalk")
    advance until screen "main_ui" timeout 20.0
    assert eval (any(getattr(item, "caption", "") == "Предложить помочь подкатится к хозяйке лавки." for item in current_action_items)) timeout 5.0
    click "Предложить помочь подкатится к хозяйке лавки." until eval (int(BeckyVar.get("EddieTryToFuck", 0) or 0) == 1) timeout 20.0
    assert eval (int(Talked.get("eddie", 0) or 0) == 1) timeout 5.0

testcase becky_from_dinner_runs_eddie_first_join:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        CurLoc = "BeckyHome"
        location = CurLoc
        MyCurDress = "citydress"
        BeckyHomeActive = 0
        BeckyVar["visitedhome"] = 5
        BeckyVar["HomeSex"] = 1
        BeckyVar["EddieTryToFuck"] = 1
        BeckyVar["PriestAdvice"] = 3
        Friends["becky"] = 20
        Friends["eddie"] = 10
        sluttiness["becky"] = 55
    run Call("BeckyHome", "FromDinner")
    advance until screen "choice" timeout 20.0
    click "Поцеловать Бекки и незаметно открыть засов"
    advance until screen "choice" timeout 20.0
    click "Кивком показать Эдди, чтобы он уважил просьбу Бекки"
    advance until eval (int(BeckyVar.get("EddieTryToFuck", 0) or 0) == 4) timeout 20.0

testcase georgett_sponsor_creates_eddie_home_visit:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        CurLoc = "TavernMain"
        location = CurLoc
        CurrentLoc["georgett"] = "TavernMain"
        Friends["georgett"] = 10
        Talked["georgett"] = 0
        BeckyVar["EddieGeorg"] = 1
        BeckyVar["EddieWhoreHome"] = 0
        BeckyVar["visitedhome"] = 5
        BeckyVar["HomeSex"] = 1
        EddieVar["SawMomSex"] = 1
        EddieVar["WhoreVisitFreq"] = 1
        money = 100
    run Call("IntGeorgettTalk", "georgett", "tavern")
    advance until screen "main_ui" timeout 20.0
    assert eval (any(getattr(item, "caption", "") == "Предложить Жоржетте проспонсировать ее визит к Эдди домой" for item in current_action_items)) timeout 5.0
    click "Предложить Жоржетте проспонсировать ее визит к Эдди домой" until eval (int(BeckyVar.get("EddieWhoreHome", 0) or 0) == 1) timeout 20.0
    python:
        _eddie_saved_randint = renpy.random.randint
        renpy.random.randint = lambda a, b: 1
        TodaySexEvents_Clear()
        Talked["georgett"] = 0
        week = 1
    run Call("NextDay_NewDayEvents")
    python:
        renpy.random.randint = _eddie_saved_randint
    assert eval (int(BeckyVar.get("EddieWhoreHome", 0) or 0) == 4) timeout 5.0
    assert eval (any(row.get("GirlName") == "georgett" and row.get("Place") == "EddieHomeVisit" for row in TodaySexEvents)) timeout 5.0

testcase eddie_tavern_client_event_uses_same_view:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        CurLoc = "TavernMain"
        location = CurLoc
        CurrentLoc["georgett"] = "TavernMain"
        EddieVar["TalkedAboutWhores"] = 1
        EddieVar["WhoreVisitFreq"] = 1
        week = 1
        time = 3
        TodaySexEvents_Clear()
        _eddie_saved_randint = renpy.random.randint
        renpy.random.randint = lambda a, b: 1
    run Call("NextDay_NewDayEvents")
    python:
        renpy.random.randint = _eddie_saved_randint
    assert eval (any(row.get("GirlName") == "georgett" and int(row.get("EventType", 0) or 0) == 99 and row.get("Place") == "Prostitution" for row in TodaySexEvents)) timeout 5.0
    run Call("TavernProstClients", 1, "georgett")
    advance until screen "choice" timeout 20.0
    assert eval (int(EddieVar.get("SawWithGeorgett", 0) or 0) == 1) timeout 5.0
    click "Вернуться в трактир" until screen "main_ui" timeout 20.0

testcase sherwood_offer_stable_and_robbery_flow:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click "Приступить к управлению трактиром" until screen "main_ui" timeout 20.0
    python:
        CurLoc = "MarketPlace"
        location = CurLoc
        BeckyVar["TradeOffer"] = 0
        BeckyVar["SherwoodWarn"] = 0
        BeckyVar["SherwoodSuspect"] = 0
        Friends["becky"] = 20
        GiveOrgasms["becky"] = 10
    run Call("BeckyQuestInit")
    advance until screen "choice" timeout 20.0
    click "А кто ж не хочет?"
    advance until screen "choice" timeout 20.0
    assert eval (int(BeckyVar.get("TradeOffer", 0) or 0) == 1) timeout 5.0
    assert eval (int(BeckyVar.get("SherwoodWarn", 0) or 0) == 1) timeout 5.0
    click "Пойти подумать над предложением" until screen "main_ui" timeout 20.0

    python:
        CurLoc = "TavernStable"
        location = CurLoc
        MyStallion = "Буцефал"
        money = 500
        time = 0
        week = 1
        BeckyVar["TradeOffer"] = 1
        BeckyVar["SherwoodSuspect"] = 5
    run Jump("TavernStable")
    advance until screen "main_ui" timeout 20.0
    assert eval (any(getattr(item, "caption", "") == "Купить провизию для эльфов у Бекки и отправится в Куниделл верхом" for item in current_action_items)) timeout 5.0
    assert eval (any(getattr(item, "caption", "") == "Пойти в Куниделл пешком и налегке" for item in current_action_items)) timeout 5.0

    python:
        money = 100
        MyStallion = "Буцефал"
        RobinVar["RobbedNum"] = 0
        RobinVar["KnowHim"] = 0
        RobinVar["MongolSafePass"] = 0
        BeckyVar["RobbedByRobin"] = 0
    run Call("SherwoodTravel", 1)
    advance until screen "choice" timeout 20.0
    click "Ехать дальше"
    advance until screen "choice" timeout 20.0
    click "Уйти"
    advance until screen "choice" timeout 20.0
    click "Попрощаться"
    advance until screen "choice" timeout 20.0
    assert eval (int(RobinVar.get("RobbedNum", 0) or 0) == 1) timeout 5.0
    assert eval (int(BeckyVar.get("RobbedByRobin", 0) or 0) >= 1) timeout 5.0
    assert eval (str(MyStallion or "") == "") timeout 5.0
    assert eval (int(money or 0) == 50) timeout 5.0
    click "Домой" until screen "main_ui" timeout 20.0
'''


def build_temp_project(root: Path, temp_root: Path) -> Path:
    source_game = root / "game"
    temp_project = temp_root / "TractirExternalEddieProject"
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
    (temp_game / "_external_eddie_branch_test.rpy").write_text(TEST_RPY, encoding="utf-8")
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
