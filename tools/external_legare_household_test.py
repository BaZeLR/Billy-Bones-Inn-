#!/usr/bin/env python3
"""Click the real household lore menus in an isolated native Ren'Py testcase run.

Only fixture state is seeded; the disclosure, gates, reward and returns execute
the production labels. User saves are never loaded or written.
"""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import external_tavern_premium_test as isolated


TEST_RPY = r'''
init python:
    def external_legare_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_legare_button(caption):
        return "choice_panel_button_%d" % external_legare_choices().index(caption)

    def external_legare_prepare(rel=6, trust=0, paintings=0, completed=False, room="WineStore"):
        for thread in threads.values():
            thread.abort()
        threads["claraPaintingsPath"].num = paintings
        threads["claraPaintingsPath"].completed = completed
        Clara.rel = rel
        Clara.trust = trust
        Clara.asked_today = 0
        Clara.talked_today = 0
        event_runtime.available.clear()
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        rooms.enter(room)
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_title = "EXTERNAL_LEGARE_ORIGIN"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []
        scene_runtime.picture = rooms.get(room).bg_picture
        scene_runtime.text = "EXTERNAL_LEGARE_ORIGIN_TEXT"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

testsuite global:
    teardown:
        exit

testcase external_legare_public_question_entry_gate:
    parameter seed = [(5, 0), (6, 1)]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_legare_prepare(seed[0])
    $ Clara.asked_today = seed[1]
    run Call("IntClaraTalk")
    advance until eval ("Назад" in external_legare_choices()) timeout 20.0
    assert eval ("Спросить Клариссу о семье" not in external_legare_choices()) timeout 5.0
    click id (external_legare_button("Назад")) pos (0.5, 0.5) until eval (not external_legare_choices()) timeout 20.0
    assert eval (Clara.rel == seed[0] and Clara.trust == 0 and Clara.asked_today == seed[1]) timeout 5.0
'''


def disclosure_case(depth: int, seeds: str) -> str:
    """Expand explicit click paths; no production gate or flow is reimplemented."""
    case = r'''
testcase external_legare_disclosure_back_depth_DEPTH:
    parameter seed = SEEDS
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_legare_prepare(*seed[:4])
    $ _legare_origin = main_ui_context_snapshot()
    run Call("IntClaraTalk")
    advance until eval ("Спросить Клариссу о семье" in external_legare_choices()) timeout 20.0
    $ _legare_talk = main_ui_context_snapshot()
    click id (external_legare_button("Спросить Клариссу о семье")) pos (0.5, 0.5) until eval ("Вернуться к разговору" in external_legare_choices()) timeout 20.0
    assert eval (Clara.rel == seed[0] + 1 and Clara.trust == seed[1] + 1 and Clara.asked_today == 1 and Clara.talked_today == 1) timeout 5.0
    assert eval (renpy.get_screen("main_ui") is not None and main_ui_runtime.mode == "event") timeout 5.0
    assert eval (scene_runtime.picture == "images/clara/portrait.png" and "профессиональная гувернантка" in scene_runtime.text and "наложницей" not in scene_runtime.text) timeout 5.0
'''.replace("DEPTH", str(depth)).replace("SEEDS", seeds)
    if depth == 0:
        case += r'''
    assert eval (("Узнать о пансионе подробнее" in external_legare_choices()) == seed[4]) timeout 5.0
'''
    if depth >= 1:
        case += r'''
    click id (external_legare_button("Узнать о пансионе подробнее")) pos (0.5, 0.5) until eval ("взрослая пансионерка" in scene_runtime.text) timeout 20.0
    assert eval ("не дочь Легаре" in scene_runtime.text and "наложницей" not in scene_runtime.text) timeout 5.0
    assert eval (("Спросить о будущем воспитанниц" in external_legare_choices()) == seed[4]) timeout 5.0
'''
    if depth == 2:
        case += r'''
    click id (external_legare_button("Спросить о будущем воспитанниц")) pos (0.5, 0.5) until eval ("наложницей" in scene_runtime.text) timeout 20.0
    assert eval (external_legare_choices() == ["Вернуться к разговору"] and renpy.get_screen("main_ui") is not None) timeout 5.0
'''
    case += r'''
    click id (external_legare_button("Вернуться к разговору")) pos (0.5, 0.5) until eval ("Назад" in external_legare_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "talk" and main_ui_runtime.selected_char == "clara" and main_ui_runtime.scene_origin is None) timeout 5.0
    assert eval (main_ui_context_snapshot() == _legare_talk and "Спросить Клариссу о семье" not in external_legare_choices()) timeout 5.0
    assert eval (threads["claraPaintingsPath"].num == seed[2] and threads["claraPaintingsPath"].completed == seed[3]) timeout 5.0
    click id (external_legare_button("Назад")) pos (0.5, 0.5) until eval (not external_legare_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _legare_origin and main_ui_runtime.talk_origin is None) timeout 5.0
    run Call("IntClaraTalk")
    advance until eval ("Назад" in external_legare_choices()) timeout 20.0
    assert eval ("Спросить Клариссу о семье" not in external_legare_choices() and Clara.rel == seed[0] + 1 and Clara.trust == seed[1] + 1 and Clara.asked_today == 1 and Clara.talked_today == 1) timeout 5.0
    click id (external_legare_button("Назад")) pos (0.5, 0.5) until eval (not external_legare_choices()) timeout 20.0
'''
    return case


TEST_RPY += disclosure_case(0, "[(6, 0, 0, False, False), (6, 3, 4, False, False), (7, 2, 4, False, False), (7, 3, 3, False, False), (7, 3, 4, False, True)]")
TEST_RPY += disclosure_case(1, "[(7, 3, 4, False, False), (8, 5, 6, False, False), (9, 4, 6, False, False), (9, 5, 5, False, False), (9, 5, 6, False, True)]")
TEST_RPY += disclosure_case(2, "[(9, 5, 6, False, True), (9, 5, 4, True, True), (12, 10, 10, True, True)]")

TEST_RPY += r'''
testcase external_legare_church_household_and_closeup_restore:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_legare_prepare(room="Church")
    $ _legare_origin = main_ui_context_snapshot()
    run Call("ChurchServiceLegare")
    advance until eval ("Рассмотреть Элоизу и Полину" in external_legare_choices()) timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and main_ui_runtime.mode == "event") timeout 5.0
    assert eval (scene_runtime.picture == "images/Alber/church/household_school.png" and renpy.loadable(scene_runtime.picture)) timeout 5.0
    assert eval ("взрослая воспитанница" in scene_runtime.text and "а не дочь Легаре" in scene_runtime.text) timeout 5.0
    click id (external_legare_button("Назад")) pos (0.5, 0.5) until eval (not external_legare_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _legare_origin and main_ui_runtime.scene_origin is None) timeout 5.0
    run Call("ChurchServiceLegare")
    advance until eval ("Рассмотреть Элоизу и Полину" in external_legare_choices()) timeout 20.0
    click id (external_legare_button("Рассмотреть Элоизу и Полину")) pos (0.5, 0.5) until eval ("Вернуться к прихожанам" in external_legare_choices()) timeout 20.0
    assert eval (scene_runtime.picture == "images/Alber/church/aloise_pauline_school.png" and renpy.loadable(scene_runtime.picture)) timeout 5.0
    assert eval ("молитвенник" in scene_runtime.text and renpy.get_screen("main_ui") is not None) timeout 5.0
    click id (external_legare_button("Вернуться к прихожанам")) pos (0.5, 0.5) until eval (not external_legare_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _legare_origin and main_ui_runtime.scene_origin is None and rooms.current_code == "Church") timeout 5.0
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renpy", default=isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=480)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--compile-lint", action="store_true")
    args = parser.parse_args()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.is_file():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_legare_household_"))
    try:
        isolated.TEST_RPY = TEST_RPY
        project = isolated.build_temp_project(isolated.project_root(), temp_root)
        print(f"Temporary household test project: {project}", flush=True)
        if args.compile_lint:
            for command in ("compile", "lint"):
                result = subprocess.run(
                    [str(renpy_exe), str(project), "--savedir", str(project / ".test-saves"), command],
                    text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                log = project / f"legare-{command}.log"
                log.write_text(result.stdout, encoding="utf-8")
                print(f"Ren'Py {command}: exit {result.returncode}; log {log}", flush=True)
                if result.returncode:
                    isolated.safe_print(result.stdout)
                    return int(result.returncode)
        return isolated.run_renpy(renpy_exe, project, args.timeout)
    finally:
        if args.keep_temp:
            print(f"Keeping temporary household test project: {temp_root}")
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_legare_household_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            isolated.remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
