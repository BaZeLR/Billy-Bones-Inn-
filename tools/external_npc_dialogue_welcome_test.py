#!/usr/bin/env python3
"""Exercise named dialogue and the hired workers' welcome in copied Ren'Py."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_welcome_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

testsuite global:
    teardown:
        exit

testcase external_npc_welcome_dialogue:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ rooms.enter("TavernKitchen")
    $ Georgett.known = True
    $ Liza.known = True
    $ Georgett.set_hired(True)
    $ Liza.set_hired(True)
    $ Georgett.assign_tavern_service("", False)
    $ Georgett.assign_tavern_service("", True)
    $ Liza.assign_tavern_service("", False)
    $ Liza.assign_tavern_service("", True)
    $ player.tavern_management.breakfast.georgett_liza_pending = 1
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    $ tavern.client_touch_policy = "standard"
    $ Sandra.set_harass_instruction("")
    $ Melissa.set_harass_instruction("")
    $ Amanda.set_harass_instruction("")
    assert eval (dog.character is None and werecat.character is None)
    assert eval (player.character is not None and Sandra.character is not None and n is tractir_narrator_char)
    assert eval (len({player.character.who_args["color"], Sandra.character.who_args["color"], Melissa.character.who_args["color"], Amanda.character.who_args["color"], Georgett.character.who_args["color"], Liza.character.who_args["color"], n.who_args["color"]}) == 7)
    assert eval (Georgett.job_value("jobwhore", 0) == 0 and Liza.job_value("jobwhore", 0) == 0)
    run Call("TavernKitchenBreakfastAnnounceGeorgetteLiza")
    advance until eval (renpy.get_screen("say") is not None and renpy.get_screen("say").scope.get("who") == "Рассказчик") timeout 25.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    click pos (960, 560) until eval (renpy.get_screen("say") is not None and renpy.get_screen("say").scope.get("who") == player.display_name) timeout 25.0
    click pos (960, 560) until eval (renpy.get_screen("say") is not None and renpy.get_screen("say").scope.get("who") == "Сандра") timeout 25.0
    click pos (960, 560) until eval (renpy.get_screen("say") is not None and renpy.get_screen("say").scope.get("who") == "Мелисса") timeout 25.0
    click pos (960, 560) until eval (renpy.get_screen("say") is not None and renpy.get_screen("say").scope.get("who") == "Аманда") timeout 25.0
    click pos (960, 560) until eval (renpy.get_screen("say") is not None and renpy.get_screen("say").scope.get("who") == "Жоржетта") timeout 25.0
    click pos (960, 560) until eval (renpy.get_screen("say") is not None and renpy.get_screen("say").scope.get("who") == "Лизетта") timeout 25.0
    click pos (960, 560) until eval (external_welcome_choices() == ["Продолжить завтрак"]) timeout 25.0
    assert eval (player.tavern_management.breakfast.georgett_liza_pending == 1)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (player.tavern_management.breakfast.georgett_liza_pending == 0) timeout 25.0
    assert eval (tavern.client_touch_policy == "hands_off")
    assert eval (Georgett.job_value("jobwhore", 0) == 1 and Liza.job_value("jobwhore", 0) == 1)
    assert eval (Sandra.harass_instruction() == "notallow" and Melissa.harass_instruction() == "notallow" and Amanda.harass_instruction() == "notallow")

testcase external_npc_welcome_old_save:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ Georgett.set_hired(True)
    $ Liza.set_hired(True)
    $ player.tavern_management.breakfast.georgett_liza_pending = 1
    $ updateSave_V112()
    assert eval (Georgett.job_value("jobwhore", 0) == 0 and Liza.job_value("jobwhore", 0) == 0)
    $ player.tavern_management.breakfast.georgett_liza_pending = 0
    $ tavern.client_touch_policy = "standard"
    $ updateSave_V112()
    assert eval (tavern.client_touch_policy == "hands_off")
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_npc_welcome_"))
    try:
        copied.TEST_RPY = TEST_RPY
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary NPC welcome project: {project}", flush=True)
        for command in (["compile"], ["lint"], ["test", "--hide-execution", "all", "--report-detailed"]):
            result = subprocess.run(
                [args.renpy, str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=240,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            log = project / f"npc-welcome-{command[0]}.log"
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            copied.isolated.safe_print(result.stdout)
            if result.returncode:
                return result.returncode
        return 0
    finally:
        if args.keep_temp:
            print(f"Keeping temporary NPC welcome project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_npc_welcome_"):
                raise RuntimeError(f"Refusing to remove unexpected path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
