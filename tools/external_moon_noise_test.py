#!/usr/bin/env python3
"""Exercise lunar noise progression using copied scripts and temporary saves."""
from pathlib import Path
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    import copy
    def external_noise_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption) for item in choice.scope.get("items", [])] if choice else []

    def external_noise_prepare(repeated=False):
        Mongol.arrival_due_day = -1
        for thread in threads.values():
            thread.abort()
        threads["melissaBatProblem"].advanceTo(threads["melissaBatProblem"].data.length, complete_at_end=True)
        threads["melissaBatProblem"].day = 18
        tavern.renovations["roof"].status = "completed"
        noise = threads["melissaMoonNoise"]
        noise.advanceTo(4 if repeated else 0, complete_at_end=repeated, force_active=not repeated)
        threads["melissaMoonNoiseRepeat"].forceEnable()
        calendar_v2.day, calendar_v2.daysInGame = 17, 44
        calendar_v2.hour, calendar_v2.minute = 22, 0
        event_runtime.fired_keys_today = []
        event_runtime.evaluation_time = None
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        for info in (Amanda, Melissa):
            info.set_sex_stat("virginity", True)
            info.set_sex_busy(False)
        rooms.enter("TavernUpstairs")
        renpy.show_screen("main_ui")

    def external_noise_breakfast():
        calendar_v2.advance_minutes(600 - calendar_v2.clock_minutes() + 1440)
        player.tavern_management.breakfast.event_active = True
        player.tavern_management.breakfast.present_ids = ["sandra", "amanda", "melissa"]
        rooms.enter("TavernKitchen")
        event_runtime.evaluation_time = None

testsuite global:
    teardown:
        exit

testcase external_noise_monthly_corridor:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_noise_prepare(True)
    assert eval (story_event_available("TavernUpstairs", "enter"))
    run Jump("TavernUpstairs")
    advance until eval (len(external_noise_choices()) == 1) timeout 20.0
    assert eval ("волосы растрёпаны" in scene_runtime.text and "ночные сорочки" in scene_runtime.text)
    assert eval ("Я тоже слышу" in scene_runtime.text)
    assert eval (main_ui_runtime.action_items == [] and renpy.get_screen("main_ui") is not None)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    assert eval (threads["melissaMoonNoiseRepeat"].num == 0 and threads["melissaMoonNoiseRepeat"].day == 44)
    assert eval (not story_event_available("TavernUpstairs", "enter"))
    $ external_noise_breakfast()
    assert eval (threads["melissaMoonNoise"].completed and not story_event_available("TavernKitchen", "breakfast"))
    $ calendar_v2.advance_minutes(720)
    assert eval (not story_event_available("TavernUpstairs", "enter"))
    $ calendar_v2.advance_minutes(27 * 1440)
    assert eval (story_event_available("TavernUpstairs", "enter"))
    run Jump("TavernUpstairs")
    advance until eval (len(external_noise_choices()) == 1) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    assert eval (threads["melissaMoonNoiseRepeat"].day == 72 and not threads["melissaMoonNoiseRepeat"].completed)

testcase external_noise_investigation:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_noise_prepare()
    run Jump("TavernUpstairs")
    advance until eval (len(external_noise_choices()) == 1) timeout 20.0
    assert eval ("Аманда" in scene_runtime.text and "Мелисса" in scene_runtime.text)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    assert eval (threads["melissaMoonNoise"].num == 1)
    $ external_noise_breakfast()
    run Call("checkTriggers", "TavernKitchen", "breakfast", 0)
    advance until eval (external_noise_choices() == ["Пообещать снова осмотреть чердак"]) timeout 20.0
    assert eval ("Аманда" in scene_runtime.text and "Мелисса" in scene_runtime.text)
    assert eval ("Аманда молчит" in scene_runtime.text)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    assert eval (threads["melissaMoonNoise"].num == 2)
    $ rooms.enter("TavernAtic")
    run Call("checkTriggers", "TavernAtic", "enter", 0)
    advance until eval (external_noise_choices() == ["Вернуться вниз с этим известием"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    assert eval (threads["melissaMoonNoise"].num == 3)
    $ external_noise_breakfast()
    run Call("checkTriggers", "TavernKitchen", "breakfast", 0)
    advance until eval (external_noise_choices() == ["Попросить Сандру продолжить"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_noise_choices() == ["Выслушать ответ Сандры"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_noise_choices() == ["Слушать про старую печь"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_noise_choices() == ["Вспомнить старую печь в сарае"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    assert eval (threads["melissaMoonNoise"].completed)
    $ calendar_v2.advance_minutes(1320 - calendar_v2.clock_minutes())
    assert eval (story_event_available("TavernUpstairs", "enter"))
    run Jump("TavernUpstairs")
    advance until eval (len(external_noise_choices()) == 1) timeout 20.0
    assert eval ("После того, что Сандра рассказала" in scene_runtime.text)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    assert eval (not story_event_available("TavernUpstairs", "enter"))

testcase external_noise_hired_listener:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_noise_prepare(True)
    $ Amanda.set_sex_stat("virginity", False)
    $ Melissa.set_sex_stat("virginity", False)
    $ Liza.set_hired(True)
    $ Liza.set_sex_stat("virginity", True)
    $ LizaStaticData.set_schedule([NPCScheduleEntry(location="TavernKitchen", priority=999, awake=True, talkable=True)])
    $ LizaStaticData.invalidate_daily_schedule()
    assert eval (moon_noise_listener_ids() == ["liza"])
    run Jump("TavernUpstairs")
    advance until eval (len(external_noise_choices()) == 1) timeout 20.0
    assert eval (people_display_name("liza") in scene_runtime.text)
    assert eval ("Я тоже слышу" not in scene_runtime.text and "Они нас разбудили" in scene_runtime.text)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    $ external_noise_breakfast()
    assert eval ("liza" in tavern_breakfast_present_ids())
    assert eval (not story_event_available("TavernKitchen", "breakfast"))
    assert eval (threads["melissaMoonNoiseRepeat"].num == 0)

testcase external_noise_old_unthreaded_scene:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_noise_prepare(True)
    run Jump("Forest")
    advance until eval (rooms.current_code == "Forest" and not external_noise_choices()) timeout 20.0
    $ event_runtime.active_thread = None
    run Call("story_melissa_moon_noise_repeat")
    advance until eval (len(external_noise_choices()) == 1) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_noise_choices()) timeout 20.0
    assert eval (threads["melissaMoonNoiseRepeat"].num == 0 and threads["melissaMoonNoiseRepeat"].day == 44)

testcase external_noise_loaded_repeat_progress:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_noise_prepare(True)
    $ threads["melissaMoonNoiseRepeat"].num = 1
    $ threads["melissaMoonNoiseRepeat"].completed = True
    $ threads["melissaMoonNoiseRepeat"].day = 44
    $ tractir_save_patch_loaded_state()
    assert eval (threads["melissaMoonNoiseRepeat"].num == 0 and not threads["melissaMoonNoiseRepeat"].completed)
    assert eval (threads["melissaMoonNoiseRepeat"].day == 44 and threads["melissaMoonNoise"].completed)
    assert eval (threads["melissaBatProblem"].completed)
    assert eval (tavern.renovation_complete("roof"))
    $ _old_repeat = copy.copy(threads["melissaMoonNoiseRepeat"].data)
    $ _old_repeat.triggers = [[copy.copy(_old_repeat.triggers[0][0])], [copy.copy(_old_repeat.triggers[0][0])]]
    $ _old_repeat.triggers[1][0].target = "story_melissa_moon_breakfast_repeat"
    $ _old_repeat.length = 2
    $ threads["melissaMoonNoiseRepeat"].data = _old_repeat
    $ threads["melissaMoonNoiseRepeat"].num = 1
    $ threads["melissaMoonNoiseRepeat"].done = [True, False]
    $ tractir_save_patch_loaded_state()
    $ initThreads()
    assert eval (threads["melissaMoonNoiseRepeat"].data.length == 1 and threads["melissaMoonNoiseRepeat"].num == 0)
    assert eval (threads["melissaMoonNoiseRepeat"].done == [False] and threads["melissaMoonNoiseRepeat"].day == 44)
    assert eval (threads["melissaMoonNoise"].completed and threads["melissaBatProblem"].completed and tavern.renovation_complete("roof"))
'''


def main():
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_moon_noise_"))
    copied.TEST_RPY = TEST_RPY
    project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
    savedir = project / ".test-saves"
    savedir.mkdir()
    print(f"Isolated project: {project}", flush=True)
    commands = [["compile"], ["lint"]]
    commands.extend(["test", "--hide-execution", "all", name, "--report-detailed"] for name in (
        "external_noise_monthly_corridor", "external_noise_investigation",
        "external_noise_hired_listener", "external_noise_old_unthreaded_scene",
        "external_noise_loaded_repeat_progress"))
    for index, command in enumerate(commands):
        result = subprocess.run([copied.isolated.RENPY_DEFAULT, str(project), "--savedir", str(savedir),
            *command],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace", timeout=120)
        (project / f"noise-{index}.log").write_text(result.stdout, encoding="utf-8")
        copied.isolated.safe_print(result.stdout)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
