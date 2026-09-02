#!/usr/bin/env python3
"""Run Ren'Py story event branch checks from a temporary project.

This keeps generated testcase labels out of the real game directory. The test
uses the existing StoryEventRuntime classes/data in-game: threadData,
createThreads(), initEvents(), and the real event labels/actions.
"""

from __future__ import annotations

import argparse
import os
import re
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


def label_set(root: Path) -> set[str]:
    labels: set[str] = set()
    for path in (root / "game").rglob("*.rpy"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        labels.update(re.findall(r"^label\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(|:)", text, re.M))
    return labels


def story_event_labels(root: Path) -> list[str]:
    labels = label_set(root)
    source_paths = [
        root / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy",
    ]
    text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in source_paths if path.exists())
    found: list[str] = []
    for match in re.finditer(r'\(\s*"([A-Za-z_][A-Za-z0-9_]*)"\s*,\s*(?:None|\d|\(|\[)', text):
        name = match.group(1)
        if name in labels and name not in found:
            found.append(name)
    for match in re.finditer(r"^label\s+([A-Za-z_][A-Za-z0-9_]*)\s*:", text, re.M):
        name = match.group(1)
        if name.startswith(("story_", "melissaClaraOverheard_", "sandraWeeklyEvaluation_")) and name in labels and name not in found:
            found.append(name)
    return found


TEST_HEADER = r'''
testsuite global:
    teardown:
        exit

testcase instantiate_story_threads:
    $ renpy.test.testsettings._test.timeout = 60.0
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        threadData = loadThreadData(threadList)
        threads = createThreads()
        initEvents()
        assert len(dict(threadData or {})) > 0
        assert len(dict(threads or {})) == len(dict(threadData or {}))
        print("THREADS_INSTANTIATED", len(dict(threads or {})))

'''


EVENT_TEMPLATE = r'''
testcase event_{safe_name}:
    $ renpy.test.testsettings._test.timeout = 60.0
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        threadData = loadThreadData(threadList)
        threads = createThreads()
        initEvents()
        initStoryEventRuntime(True)
        calendar_v2.week = 7
        calendar_v2.hour = 12
        calendar_v2.minute = 0
        calendar_v2.daysInGame = max(int(calendar_v2.daysInGame or 0), 30)
        player.stats.exploration = max(int(player.stats.exploration or 0), 250)
        player.set_money(max(int(player.economy.money or 0), 500))
        for _girl in ("amanda", "sandra", "melissa", "clara", "georgett", "liza", "becky"):
            _girl_info = getPersonInfo(_girl)
            _girl_info.rel = max(int(_girl_info.rel or 0), 20)
            _girl_info.corruption = max(int(_girl_info.corruption or 0), 20)
            _girl_info.openness = max(int(_girl_info.openness or 0), 20)
            _girl_info.asked_today = 0
        set_bedroom_door_locked("TavernSandraRoom", False)
        Melissa.drawings_found = True
        threads["melissaBatProblem"].advanceTo(threads["melissaBatProblem"].data.length, complete_at_end=True)
        Clara.drawings_secret_known = True
        Clara.flirt_count = max(int(Clara.flirt_count or 0), 1)
        Clara.commission_followup_day = 0
        Clara.murder_day = 0
        werecat_state()["adopted"] = 1
        CurLoc = "TavernMain"
        location = CurLoc
        thread = None
        thread_stage = None
        for _thread_name, _thread_info in dict(threads or {{}}).items():
            for _thread_index, _trigger_group in enumerate(list(getattr(getattr(_thread_info, "data", None), "triggers", []) or [])):
                for _evt in list(_trigger_group or []):
                    if str(getattr(_evt, "target", "") or "") == "{label_name}":
                        thread = _thread_info
                        thread_stage = _thread_index
                        break
                if thread is not None:
                    break
            if thread is not None:
                break
        if thread is not None and thread_stage is not None:
            thread.advanceTo(thread_stage, force_active=True)
        event_runtime.active_thread = thread
        print("EVENT_LABEL_START", "{label_name}")
    run Call("{label_name}")
    pause 0.1
    python:
        print("EVENT_LABEL_DONE", "{label_name}", "items", len(list(current_action_items or [])))

'''

BRANCH_TEMPLATE = r'''
testcase event_{safe_name}_branch_{branch_index}:
    $ renpy.test.testsettings._test.timeout = 60.0
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 20.0
    python:
        threadData = loadThreadData(threadList)
        threads = createThreads()
        initEvents()
        initStoryEventRuntime(True)
        calendar_v2.week = 7
        calendar_v2.hour = 12
        calendar_v2.minute = 0
        calendar_v2.daysInGame = max(int(calendar_v2.daysInGame or 0), 30)
        player.stats.exploration = max(int(player.stats.exploration or 0), 250)
        player.set_money(max(int(player.economy.money or 0), 500))
        for _girl in ("amanda", "sandra", "melissa", "clara", "georgett", "liza", "becky"):
            _girl_info = getPersonInfo(_girl)
            _girl_info.rel = max(int(_girl_info.rel or 0), 20)
            _girl_info.corruption = max(int(_girl_info.corruption or 0), 20)
            _girl_info.openness = max(int(_girl_info.openness or 0), 20)
            _girl_info.asked_today = 0
        set_bedroom_door_locked("TavernSandraRoom", False)
        Melissa.drawings_found = True
        threads["melissaBatProblem"].advanceTo(threads["melissaBatProblem"].data.length, complete_at_end=True)
        Clara.drawings_secret_known = True
        Clara.flirt_count = max(int(Clara.flirt_count or 0), 1)
        Clara.commission_followup_day = 0
        Clara.murder_day = 0
        werecat_state()["adopted"] = 1
        CurLoc = "TavernMain"
        location = CurLoc
        thread = None
        thread_stage = None
        for _thread_name, _thread_info in dict(threads or {{}}).items():
            for _thread_index, _trigger_group in enumerate(list(getattr(getattr(_thread_info, "data", None), "triggers", []) or [])):
                for _evt in list(_trigger_group or []):
                    if str(getattr(_evt, "target", "") or "") == "{label_name}":
                        thread = _thread_info
                        thread_stage = _thread_index
                        break
                if thread is not None:
                    break
            if thread is not None:
                break
        if thread is not None and thread_stage is not None:
            thread.advanceTo(thread_stage, force_active=True)
        event_runtime.active_thread = thread
    run Call("{label_name}")
    pause 0.1
    python:
        _external_branch_count = len(list(current_action_items or []))
        _external_branch_safe = False
        if _external_branch_count > {branch_index}:
            _external_branch_action_text = str(current_action_items[{branch_index}].action)
            for _token in (
                "story_",
                "TownStreet",
                "TownRandom",
                "melissaClaraOverheard",
                "sandraWeeklyEvaluation",
                "TavernStorageRatChoice",
                "MelissaRoomPestsChoice",
                "MelissaNightWakeChoice",
                "HouseholdSoapRequest",
                "HouseholdBarberRequest",
                "HouseholdRevealDressRequest",
            ):
                if _token in _external_branch_action_text:
                    _external_branch_safe = True
                    break
        print("EVENT_BRANCH_READY", "{label_name}", {branch_index}, "items", _external_branch_count, "safe", _external_branch_safe)
    if eval (_external_branch_count > {branch_index} and _external_branch_safe):
        run current_action_items[{branch_index}].action
        pause 0.1
        python:
            print("EVENT_BRANCH_DONE", "{label_name}", {branch_index}, str(CurLoc or ""), len(list(current_action_items or [])))

'''


def build_test_rpy(labels: list[str], max_branches: int) -> str:
    pieces = [TEST_HEADER]
    for label in labels:
        safe = re.sub(r"[^A-Za-z0-9_]", "_", label)
        pieces.append(EVENT_TEMPLATE.format(label_name=label, safe_name=safe))
        for branch_index in range(max(0, max_branches)):
            pieces.append(BRANCH_TEMPLATE.format(label_name=label, safe_name=safe, branch_index=branch_index))
    return "".join(pieces)


def build_temp_project(root: Path, temp_root: Path, labels: list[str], max_branches: int) -> Path:
    source_game = root / "game"
    temp_project = temp_root / "TractirExternalEventProject"
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
    (temp_game / "_external_event_branch_test.rpy").write_text(build_test_rpy(labels, max_branches), encoding="utf-8")
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
        print(f"Ren'Py event test timed out after {timeout} seconds.")
        return 124


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=RENpy_DEFAULT)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--branches", type=int, default=4)
    args = parser.parse_args()

    root = project_root()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.exists():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")

    labels = story_event_labels(root)
    if args.offset > 0:
        labels = labels[args.offset :]
    if args.limit > 0:
        labels = labels[: args.limit]

    temp_root = Path(tempfile.mkdtemp(prefix="tractir_event_branch_"))
    try:
        temp_project = build_temp_project(root, temp_root, labels, args.branches)
        print(f"Temporary event test project: {temp_project}")
        print(f"Story event labels under test: {len(labels)}")
        print(f"Branch slots per event label: {max(0, args.branches)}")
        return run_renpy(renpy_exe, temp_project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary event test project: {temp_root}")
        else:
            remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
