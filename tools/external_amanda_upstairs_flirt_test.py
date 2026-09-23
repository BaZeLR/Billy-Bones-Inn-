#!/usr/bin/env python3
"""Exercise Amanda's two upstairs variants in copied scripts and temporary saves."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import tempfile
import external_tavern_renovations_test as copied

TEST_RPY = r'''
init python:
    def external_amanda_flirt_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_amanda_flirt_button(caption):
        return "choice_panel_button_%d" % external_amanda_flirt_choices().index(caption)

    def external_amanda_flirt_text_count():
        from renpy.text.text import Text
        from renpy.test.testfocus import focus_from_displayable
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
        return sum(row.count(scene_runtime.text) for row in rows) if scene_runtime.text else 0

    def external_amanda_flirt_prepare(bedroom):
        for thread in threads.values():
            thread.abort()
        event_runtime.available.clear()
        event_runtime.active_thread = None
        event_runtime.evaluation_time = None
        event_runtime.fired_keys_today = []
        daily_events.rows = []
        calendar_v2.week = 2
        calendar_v2.hour = 14
        calendar_v2.minute = 0
        for day in range(30, 90):
            calendar_v2.daysInGame = day
            if (procedural_random("amanda_tavern_seduction_bedroom") < 0.5) == bedroom:
                break
        else:
            raise AssertionError("No actual calendar seed found for requested variant")
        Amanda.rel = 20
        Amanda.corruption = 60
        Amanda.legare_forbidden = False
        Amanda.set_var_int("prohibitliza", 0)
        Amanda.set_var_int("gloryscold", 0)
        Amanda.set_var_int("lizafriends", 1)
        Amanda.set_var_int("suckyou", 0)
        Amanda.set_var_int("fuckyou", 0)
        Amanda.set_var_int("beddeflower", 0)
        Amanda.set_sex_stat("virginity", False)
        Amanda.set_sex_stat("pregnancy", 0)
        Amanda.set_sex_stat("ConceptionChance", 0)
        Amanda.fucked_today = 0
        Amanda.set_sex_busy(False)
        Amanda.wear_day_clothes()
        player.intimacy.came_today = 0
        player.condition.energy = 100
        player.condition.fun = 100
        rooms.enter("TavernMain")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_title = "AMANDA_FLIRT_ORIGIN"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = rooms.current.build_exit_items()
        scene_runtime.picture = tavern_main_picture()
        scene_runtime.text = "AMANDA_FLIRT_ORIGIN_TEXT"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

define external_amanda_flirt_beats = [{"text":"you decided to wait a liltle bit and when follows Amanda upstares to her room.","picture":""},{"text":"Aamanda ,already in her neglege runs into you trembling with passion, and kisses you pationately .","picture":"close up.jpg"},{"text":"then she stops and goes toward second bed, which is empty. smailes misteriously .","picture":"onbed.jpg"},{"text":"she slowly removes her last cloth giggling...and quickly hydes her lower body under blanket,,,","picture":"Boobs.png"},{"text":"like what you see, maister?","picture":"onbedCloseUp.jpg"},{"text":"You came claose and stand near bed,...","picture":""},{"text":"Amanda removes her blanket ... make it quick how ever I want you to make me come,,,","picture":"beforeSex.jpg"}]

testsuite global:
    teardown:
        exit

testcase external_amanda_upstairs_variants:
    parameter bedroom = [False, True]
    parameter finish = ["inside", "outside"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_amanda_flirt_prepare(bedroom)
    $ _flirt_origin = main_ui_context_snapshot()
    $ _flirt_minutes = calendar_v2.clock_minutes()
    $ _flirt_wardrobe = dict(Amanda.wardrobe.current_layers)
    $ _flirt_orgasms = Amanda.sex_stat("orgasms_given", 0)
    $ _flirt_acts = Amanda.sex_stat("sexacts", 0)
    $ _flirt_inside = Amanda.sex_stat("cuminside", 0)
    assert eval (Amanda.date_intimacy_available() and player.intimacy.can_cum())
    run Call("story_amanda_tavern_seduction_0")
    advance until screen "choice" timeout 20.0
    assert eval ("Позвать наверх" in external_amanda_flirt_choices())
    click id (external_amanda_flirt_button("Позвать наверх")) pos (0.5, 0.5)
    if eval (bedroom):
BEDROOM_BEATS
    else:
        advance until eval ("Подойти к Аманде сзади" in external_amanda_flirt_choices()) timeout 20.0
        assert eval (scene_runtime.picture == "images/amanda/Room/flirtUpstares/flirts_new room.jpg")
        click id (external_amanda_flirt_button("Подойти к Аманде сзади")) pos (0.5, 0.5)
        advance until eval ("Шлепнуть Аманду по ягодицам" in external_amanda_flirt_choices()) timeout 20.0
        click id (external_amanda_flirt_button("Шлепнуть Аманду по ягодицам")) pos (0.5, 0.5)
    advance until eval ("Кончить в Аманду" in external_amanda_flirt_choices()) timeout 20.0
    assert eval (len(external_amanda_flirt_choices()) == 2 and Amanda.sex_stat("orgasms_given", 0) == _flirt_orgasms + 1)
    assert eval (player.intimacy.came_today == 0 and Amanda.sex_stat("sexacts", 0) == _flirt_acts)
    if eval (bedroom):
        assert eval (scene_runtime.picture.endswith("/beforeSex.jpg") and scene_runtime.text.startswith("you enter her"))
        pause 0.1
        assert eval (external_amanda_flirt_text_count() == 1)
    click id (external_amanda_flirt_button("Кончить в Аманду" if finish == "inside" else "Вытащить и кончить на ягодицы")) pos (0.5, 0.5)
    if eval (bedroom):
        advance until eval (external_amanda_flirt_choices() == ["Далее"]) timeout 20.0
        assert eval (scene_runtime.picture == "images/amanda/sexroom/minet9.jpg" and scene_runtime.text.endswith("slurp slurp..."))
        assert eval (player.intimacy.came_today == 1 and Amanda.sex_stat("sexacts", 0) == _flirt_acts + 1)
        click id (external_amanda_flirt_button("Далее")) pos (0.5, 0.5)
        advance until eval (external_amanda_flirt_choices() == ["Завершить"]) timeout 20.0
        assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.scene_origin is not None)
        click id (external_amanda_flirt_button("Завершить")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.scene_origin is None and not external_amanda_flirt_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _flirt_origin and rooms.current_code == "TavernMain")
    assert eval (player.intimacy.came_today == 1 and Amanda.fucked_today == 1)
    assert eval (Amanda.sex_stat("orgasms_given", 0) == _flirt_orgasms + 1 and Amanda.sex_stat("sexacts", 0) == _flirt_acts + 1)
    assert eval (Amanda.sex_stat("cuminside", 0) == _flirt_inside + int(finish == "inside"))
    assert eval (Amanda.detailed_sex_history[-1]["CumTarget"] == finish and Amanda.detailed_sex_history[-1]["DudeName"] == "Вы")
    assert eval (Amanda.wardrobe.current_layers == _flirt_wardrobe and Amanda.wardrobe.context == "day" and not Amanda.sex_busy())
    assert eval (calendar_v2.clock_minutes() == _flirt_minutes + 40)

testcase external_amanda_upstairs_original_gates:
    parameter gate = ["friendship", "corruption", "virginity", "guidance"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_amanda_flirt_prepare(True)
    python:
        if gate == "friendship":
            Amanda.rel = 11
        elif gate == "corruption":
            Amanda.corruption = 34
        elif gate == "virginity":
            Amanda.set_sex_stat("virginity", True)
        else:
            Amanda.set_var_int("lizafriends", 0)
    run Call("story_amanda_tavern_seduction_0")
    advance until screen "choice" timeout 20.0
    assert eval ("Позвать наверх" not in external_amanda_flirt_choices())
    click id (external_amanda_flirt_button("Подыграть")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.scene_origin is None and not external_amanda_flirt_choices()) timeout 20.0
    assert eval (player.intimacy.came_today == 0 and Amanda.fucked_today == 0)
'''

# Expand test interactions before Ren'Py parses the test DSL (no test while statement).
BEAT = r'''
        advance until eval (external_amanda_flirt_choices() == ["Далее"]) timeout 20.0
        assert eval (scene_runtime.text == external_amanda_flirt_beats[INDEX]["text"])
        assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
        if eval (external_amanda_flirt_beats[INDEX]["picture"]):
            assert eval (scene_runtime.picture == "images/amanda/Room/flirtUpstares/" + external_amanda_flirt_beats[INDEX]["picture"])
        if eval (INDEX == 1):
            assert eval (Amanda.current_dress() == "nightshirt")
        if eval (INDEX >= 3):
            assert eval (Amanda.wardrobe.naked())
        pause 0.1
        assert eval (external_amanda_flirt_text_count() == 1)
        assert eval (scene_runtime.text == external_amanda_flirt_beats[INDEX]["text"])
        click id (external_amanda_flirt_button("Далее")) pos (0.5, 0.5)
'''
TEST_RPY = TEST_RPY.replace("BEDROOM_BEATS", "".join(BEAT.replace("INDEX", str(index)) for index in range(7)))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_amanda_flirt_"))
    try:
        copied.TEST_RPY = TEST_RPY
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary Amanda flirt project: {project}", flush=True)
        for command in (["compile"], ["lint"], ["test", "--hide-execution", "all", "--report-detailed"]):
            result = subprocess.run(
                [args.renpy, str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            log = project / f"amanda-flirt-{command[0]}.log"
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            copied.isolated.safe_print(result.stdout)
            if result.returncode:
                return result.returncode
        return 0
    finally:
        if args.keep_temp:
            print(f"Keeping temporary Amanda flirt project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_amanda_flirt_"):
                raise RuntimeError(f"Refusing to remove unexpected path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)

if __name__ == "__main__":
    raise SystemExit(main())
