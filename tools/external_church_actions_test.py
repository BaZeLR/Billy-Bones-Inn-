#!/usr/bin/env python3
"""Count actual Church action widgets in an isolated native Ren'Py project."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_church_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_church_actions():
        return [str(item.caption or "") for item in main_ui_runtime.action_items]

    def external_church_rendered_text():
        from renpy.test.testfocus import focus_from_displayable
        from renpy.text.text import Text
        rows = []
        seen = set()
        def collect(displayable):
            if id(displayable) in seen or not isinstance(displayable, Text):
                return
            seen.add(id(displayable))
            if focus_from_displayable(displayable) is not None:
                rows.append("".join(part for part in displayable.text if isinstance(part, str)))
        for name in ("main_ui", "choice", "say"):
            screen = renpy.get_screen(name)
            if screen is not None:
                screen.visit_all(collect)
        return rows

    def external_church_single_actions(captions):
        rows = external_church_rendered_text()
        return bool(captions) and len(captions) == len(set(captions)) and all(rows.count(caption) == 1 for caption in captions)

    def external_church_prepare(hour):
        for thread in threads.values():
            thread.abort()
        event_runtime.available.clear()
        event_runtime.active_thread = None
        event_runtime.evaluation_time = None
        player.tavern_management.breakfast.event_active = False
        calendar_v2.daysInGame = 34
        calendar_v2.week = 7
        calendar_v2.hour = hour
        calendar_v2.minute = 0
        Becky.gerhard_talk_stage = 0
        Georgett.known = True
        Georgett.rel = 2
        Georgett.set_sex_stat("sexacts", 3)
        Georgett.set_story_value("askkids", 0)
        Georgett.set_story_value("georgettadmit", 1)
        Georgett.set_story_value("fuckinchurch", 1)
        Georgett.set_story_value("lizasawinchurch", 0)
        main_ui_runtime.clear_contexts()
        main_ui_runtime.overlay = ""

testsuite global:
    teardown:
        exit

testcase external_church_room_actions_render_once:
    parameter hour = [8, 10, 11]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_church_prepare(hour)
    run Jump("Church")
    advance until eval (rooms.current_code == "Church") timeout 20.0
    assert eval (external_church_single_actions(external_church_actions())) timeout 5.0
    assert eval (len(external_church_actions()) == (1 if hour == 10 else 2)) timeout 5.0
    $ print("CHURCH ROOM hour=%s action_count=%s unique=%s" % (hour, len(external_church_actions()), external_church_single_actions(external_church_actions())))

testcase external_church_attendee_georgette_actions_render_once_after_return:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_church_prepare(8)
    run Jump("Church")
    advance until eval (rooms.current_code == "Church") timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.action_title == "Прихожане") timeout 20.0
    assert eval (len(external_church_actions()) == 6 and external_church_single_actions(external_church_actions())) timeout 5.0
    click id "choice_panel_button_4" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.action_title == "Жоржетта") timeout 20.0
    assert eval (len(external_church_actions()) == 2 and external_church_single_actions(external_church_actions())) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.action_title == "Прихожане") timeout 20.0
    assert eval (len(external_church_actions()) == 6 and external_church_single_actions(external_church_actions())) timeout 5.0
    click id "choice_panel_button_5" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.action_title == "Действия") timeout 20.0
    assert eval (len(external_church_actions()) == 2 and external_church_single_actions(external_church_actions())) timeout 5.0

testcase external_church_walk_native_choices_render_once:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_church_prepare(11)
    run Jump("Church")
    advance until eval (rooms.current_code == "Church") timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (len(external_church_choices()) == 1 and external_church_single_actions(external_church_choices())) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_church_choices() == ["Назад"]) timeout 20.0
    assert eval (external_church_single_actions(external_church_choices())) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_church_choices()) timeout 20.0
    assert eval (len(external_church_actions()) == 2 and external_church_single_actions(external_church_actions())) timeout 5.0

testcase external_church_confession_native_choices_render_once:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_church_prepare(10)
    run Jump("Church")
    advance until eval (rooms.current_code == "Church") timeout 20.0
    run Call("ChurchIspoved", 1)
    advance until screen "choice" timeout 20.0
    assert eval (len(external_church_choices()) == 3 and external_church_single_actions(external_church_choices())) timeout 5.0
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--saved-file", type=Path, action="append", default=[], help="Load only a temporary copy of this save for additional Church checks.")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_church_actions_"))
    try:
        copied.TEST_RPY = TEST_RPY
        for index, save_file in enumerate(args.saved_file):
            if not save_file.is_file():
                raise FileNotFoundError(save_file)
            copied.TEST_RPY += r'''

testcase external_church_saved_actions_INDEX:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    python:
        # Inspect the copied save without resuming its unrelated script stack.
        _church_saved_data = renpy.get_save_data("external-church-save-INDEX")
        assert _church_saved_data is not None
        rooms = _church_saved_data["rooms"]
        main_ui_runtime = _church_saved_data["main_ui_runtime"]
        _church_saved_actions = [row.action_id for row in rooms.get("Church").action_menus]
        _church_saved_panel = external_church_actions()
        print("CHURCH SAVED INDEX room=%s version=%s action_ids=%r panel_count=%s panel_unique=%s" % (rooms.current_code, _church_saved_data.get("saveVersion"), _church_saved_actions, len(_church_saved_panel), len(set(_church_saved_panel))))
        assert len(_church_saved_actions) == len(set(_church_saved_actions))
        assert _church_saved_actions == [row.action_id for row in roomDefinitions["Church"].action_menus]
        tractir_after_load_restore_ui()
    $ external_church_prepare(8)
    run Jump("Church")
    advance until eval (rooms.current_code == "Church") timeout 20.0
    assert eval (len(external_church_actions()) == 2 and external_church_single_actions(external_church_actions())) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.action_title == "Прихожане") timeout 20.0
    assert eval (len(external_church_actions()) == 6 and external_church_single_actions(external_church_actions())) timeout 5.0
    $ external_church_prepare(11)
    run Jump("Church")
    advance until eval (rooms.current_code == "Church" and main_ui_runtime.action_title == "Действия") timeout 20.0
    assert eval (len(external_church_actions()) == 2 and external_church_single_actions(external_church_actions())) timeout 5.0
'''.replace("INDEX", str(index))
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        if args.saved_file:
            # Preserve the shipped statement-name map needed by actual saved
            # return stacks. These are copies, never writable source links.
            source_game = copied.isolated.project_root() / "game"
            for compiled in source_game.rglob("*.rpyc"):
                relative = compiled.relative_to(source_game)
                if relative.parts[0] in {"cache", "saves", "saves_test_run", "images", "audio", "music", "sounds", "gui", "fonts"}:
                    continue
                target = project / "game" / relative
                if target.parent.is_dir():
                    shutil.copy2(compiled, target)
        savedir = project / ".test-saves"
        savedir.mkdir()
        for index, save_file in enumerate(args.saved_file):
            shutil.copy2(save_file, savedir / f"external-church-save-{index}-LT1.save")
        print(f"Temporary Church action test project: {project}", flush=True)
        result = subprocess.run(
            [args.renpy, str(project), "--savedir", str(savedir), "test", "--hide-execution", "all", "--report-detailed"],
            text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        copied.isolated.safe_print(result.stdout)
        return int(result.returncode)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary Church action test project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_church_actions_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
