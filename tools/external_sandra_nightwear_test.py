#!/usr/bin/env python3
"""Check Sandra's native bedroom/invitation flow using isolated scripts and saves."""
from pathlib import Path
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_sandra_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption) for item in choice.scope.get("items", [])] if choice else []

    def external_sandra_button(caption):
        return "choice_panel_button_%d" % external_sandra_choices().index(caption)

    def external_sandra_schedule(awake=True, location="TavernSandraRoom"):
        SandraStaticData.set_schedule([NPCScheduleEntry(location=location, awake=awake,
            talkable=awake, priority=999, label="evening_room")])
        SandraStaticData.invalidate_daily_schedule()

    def external_sandra_prepare():
        for thread in threads.values():
            thread.abort()
        main_ui_runtime.clear_contexts()
        calendar_v2.hour, calendar_v2.minute = 23, 0
        Sandra.rel, Sandra.corruption = 20, 20
        Sandra.set_arousal(0)
        external_sandra_schedule()

testsuite global:
    teardown:
        exit

testcase external_sandra_room_nightwear:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_sandra_prepare()
    run Jump("TavernSandraRoom")
    advance until eval (rooms.current_code == "TavernSandraRoom" and not external_sandra_choices()) timeout 20.0
    assert eval (Sandra.current_dress() == "nightshirt" and Sandra.clothing_layer("bra") == "")
    assert eval (scene_runtime.picture == "images/sandra/player_room_sandra_0.jpg")
    assert eval (scene_runtime.text == tavern_sandra_room_text())
    assert eval (any(exit.target == "TavernUpstairs" for exit in rooms.get("TavernSandraRoom").visible_exits()))
    $ Sandra.corruption = 50
    run Jump("TavernSandraRoom")
    advance until eval (Sandra.wardrobe.naked() and scene_runtime.picture == "images/sandra/thanks/sandraInHerRoonm.jfif") timeout 20.0
    assert eval ("Сандра без одежды" in scene_runtime.text)
    $ external_sandra_schedule(False)
    run Jump("TavernSandraRoom")
    advance until eval ("Она спит" in scene_runtime.text) timeout 20.0
    assert eval (scene_runtime.picture == rooms.get("TavernSandraRoom").bg_picture)
    $ Sandra.corruption = 20
    run Jump("TavernSandraRoom")
    advance until eval (scene_runtime.picture == "images/sandra/sleeps .png") timeout 20.0
    assert eval (Sandra.current_dress() == "nightshirt")
    $ external_sandra_schedule(True, "TavernKitchen")
    run Jump("TavernSandraRoom")
    advance until eval (scene_runtime.picture == rooms.get("TavernSandraRoom").bg_picture) timeout 20.0
    assert eval ("Сандра без одежды" not in scene_runtime.text)

testcase external_sandra_invitation_nightwear:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_sandra_prepare()
    $ threads["sandraWeeklyEvaluation"].advanceTo(4, force_active=True)
    run Jump("TavernSandraRoom")
    advance until eval (rooms.current_code == "TavernSandraRoom" and Sandra.wardrobe.naked() and not external_sandra_choices()) timeout 20.0
    assert eval (scene_runtime.picture == "images/sandra/thanks/sandraInHerRoonm.jfif")
    run Call("TavernSandraNightThanksScene")
    advance until eval ("Остановиться" in external_sandra_choices()) timeout 20.0
    assert eval (Sandra.wardrobe.naked() and scene_runtime.picture == "images/sandra/thanks/sandraInHerRoonm.jfif")
    click id (external_sandra_button("Осмотреть её")) pos (0.5, 0.5)
    advance until eval ("Остановиться" in external_sandra_choices()) timeout 20.0
    assert eval (scene_runtime.picture == "images/sandra/thanks/sandraInHerRoonm.jfif")
    click id (external_sandra_button("Остановиться")) pos (0.5, 0.5)
    advance until eval ("Закончить близость" in external_sandra_choices()) timeout 20.0
    assert eval (Sandra.wardrobe.context == "night" and Sandra.wardrobe.naked())
    click id (external_sandra_button("Закончить близость")) pos (0.5, 0.5)
    advance until eval (threads["sandraWeeklyEvaluation"].num != 4 and not external_sandra_choices()) timeout 20.0
    assert eval (main_ui_runtime.action_title == "Комната Сандры")
'''


def main():
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_sandra_nightwear_"))
    copied.TEST_RPY = TEST_RPY
    project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
    savedir = project / ".test-saves"
    savedir.mkdir()
    print(f"Isolated project: {project}", flush=True)
    for index, command in enumerate((["compile"], ["lint"],
            ["test", "--hide-execution", "all", "external_sandra_room_nightwear", "--report-detailed"],
            ["test", "--hide-execution", "all", "external_sandra_invitation_nightwear", "--report-detailed"])):
        result = subprocess.run([copied.isolated.RENPY_DEFAULT, str(project), "--savedir", str(savedir), *command],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace", timeout=120)
        (project / f"sandra-{index}.log").write_text(result.stdout, encoding="utf-8")
        copied.isolated.safe_print(result.stdout)
        print(f"Ren'Py {command[0]}: exit {result.returncode}", flush=True)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
