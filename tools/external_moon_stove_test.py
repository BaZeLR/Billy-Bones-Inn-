#!/usr/bin/env python3
"""Play moon-stove native menus in copied scripts with isolated test saves."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_moon_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_moon_button(caption):
        return "choice_panel_button_%d" % external_moon_choices().index(caption)

    def external_moon_prepare(stage=4):
        for thread in threads.values():
            thread.abort()
        noise = threads["melissaMoonNoise"]
        noise.advanceTo(4, complete_at_end=True)
        ritual = threads["melissaMoonStoveRitual"]
        ritual.reset()
        ritual.advanceTo(stage, force_active=True)
        ritual.ritual_result = None
        ritual.day = 48
        calendar_v2.daysInGame = 49
        calendar_v2.day = 19
        calendar_v2.week = 2
        calendar_v2.hour = 23
        calendar_v2.minute = 15
        rooms.get("ShedRuinedChamber").is_hidden = False
        rooms.enter("ShedRuinedChamber")
        for npc in (Amanda, Melissa):
            npc.set_sex_stat("virginity", True)
            npc.set_sex_busy(False)
            npc.fun = 30
            npc.openness = 30
        player.condition.fun = 30
        if player.item_count("fur_glove_001"):
            player.remove_item("fur_glove_001", player.item_count("fur_glove_001"))
        player.equipment.hand = ""
        event_runtime.active_thread = None
        event_runtime.evaluation_time = None
        event_runtime.fired_keys_today = []
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.action_items = rooms.current.build_exit_items()
        renpy.show_screen("main_ui")
        assert moon_stove_npc_available("amanda")
        assert moon_stove_npc_available("melissa")

testsuite global:
    teardown:
        exit

testcase external_moon_ambush:
    parameter glove = ["absent", "owned", "equipped", "equip_in_scene"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_moon_prepare()
    if eval (glove != "absent"):
        $ player.add_item("fur_glove_001", 1)
    if eval (glove == "equipped"):
        $ player.equip("fur_glove_001", "hand")
    $ _moon_test_day = calendar_v2.daysInGame
    assert eval (story_event_available("ShedRuinedChamber", "stove_hide_wait"))
    run Call("checkTriggers", "ShedRuinedChamber", "stove_hide_wait", 0)
    advance until eval ("Затаиться до полуночи" in external_moon_choices()) timeout 20.0
    assert eval (main_ui_runtime.action_items == [] and renpy.get_screen("main_ui") is not None)
    if eval (glove == "equip_in_scene"):
        click id (external_moon_button("Надеть меховую перчатку и ждать")) pos (0.5, 0.5)
    else:
        click id (external_moon_button("Затаиться до полуночи")) pos (0.5, 0.5)
    advance until eval (external_moon_choices() == ["Остаться в укрытии"]) timeout 20.0
    assert eval (calendar_v2.daysInGame == _moon_test_day + 1 and calendar_v2.clock_minutes() == 0)
    click id (external_moon_button("Остаться в укрытии")) pos (0.5, 0.5)
    if eval (glove in ("equipped", "equip_in_scene")):
        python:
            _moon_test_pictures = [
                "amanda/amanda_stove.png", "amanda/AmandaTrialF.png", "amanda/amanda_fur_touch.png",
                "amanda/amanda_surprised_closeup.png", "amanda/amanda_laughing_stove_closeup.png",
                "melissa/melissa_stove.png", "melissa/MelissaTrialF.png", "melissa/melissa_fur_touch.png",
                "melissa/melissa_surprised_closeup.png", "melissa/melissa_laughing_stove_closeup.png",
            ]
GLOVE_BEATS
        advance until eval (external_moon_choices() == ["Далее"]) timeout 20.0
        click id (external_moon_button("Далее")) pos (0.5, 0.5)
    else:
        advance until eval (external_moon_choices() == ["Далее"]) timeout 20.0
        assert eval (scene_runtime.picture.endswith("amanda/amanda_surprised_closeup.png"))
        click id (external_moon_button("Далее")) pos (0.5, 0.5)
        advance until eval (external_moon_choices() == ["Далее"]) timeout 20.0
        assert eval (scene_runtime.picture.endswith("melissa/melissa_surprised_closeup.png"))
        click id (external_moon_button("Далее")) pos (0.5, 0.5)
    advance until eval (external_moon_choices() == ["Выбраться из печи и вернуться в трактир"]) timeout 20.0
    click id (external_moon_button("Выбраться из печи и вернуться в трактир")) pos (0.5, 0.5)
    advance until eval (threads["melissaMoonStoveRitual"].completed) timeout 20.0
    assert eval (threads["melissaMoonStoveRitual"].ritual_result["route"] == ("glove" if glove in ("equipped", "equip_in_scene") else "no_glove"))
    assert eval (threads["melissaMoonStoveRitual"].ritual_result["ritual_participants"] == ["amanda", "melissa"])
    assert eval (calendar_v2.daysInGame == _moon_test_day + 1 and calendar_v2.clock_minutes() == 10)
    assert eval (player.condition.fun == (35 if glove in ("equipped", "equip_in_scene") else 33))
    assert eval (Amanda.sex_stat("virginity", True) and Melissa.sex_stat("virginity", True))
    assert eval (not story_event_available("ShedRuinedChamber", "stove_hide_wait"))

testcase external_moon_leave_early:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_moon_prepare()
    run Call("ShedRuinedStove")
    advance until eval ("Спрятаться в печи и ждать" in external_moon_choices()) timeout 20.0
    click id (external_moon_button("Спрятаться в печи и ждать")) pos (0.5, 0.5)
    advance until eval ("Передумать и выбраться" in external_moon_choices()) timeout 20.0
    click id (external_moon_button("Передумать и выбраться")) pos (0.5, 0.5)
    advance until eval (not external_moon_choices() and main_ui_runtime.scene_origin is None) timeout 20.0
    assert eval (threads["melissaMoonStoveRitual"].num == 4 and threads["melissaMoonStoveRitual"].day == 48)
    assert eval (threads["melissaMoonStoveRitual"].ritual_result is None and player.condition.fun == 30)
    assert eval (calendar_v2.clock_minutes() == 1395 and story_event_available("ShedRuinedChamber", "stove_hide_wait"))

testcase external_moon_crafting:
    parameter donor = ["warm_fur_cloak_001", "fur_bedroll_001"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_moon_prepare(1)
    assert eval (get_game_item("fur_glove_001") is FurGloveItem)
    assert eval (player.item_count("fur_glove_001") == 0 and player.equipment.hand == "")
    $ player.add_item(donor, 1)
    $ _moon_donor_count = player.item_count(donor)
    run Call("PlayerCardMakeFurGlove", donor)
    advance until eval (player.item_count("fur_glove_001") == 1) timeout 20.0
    assert eval (player.item_count(donor) == _moon_donor_count and calendar_v2.clock_minutes() == 1415)
    run Call("PlayerCardMakeFurGlove", donor)
    pause 0.2
    assert eval (player.item_count("fur_glove_001") == 1 and calendar_v2.clock_minutes() == 1415)
    run Call("PlayerCardEquipItem", "fur_glove_001")
    advance until eval (player.equipment.hand == "fur_glove_001") timeout 20.0

testcase external_moon_window_routes:
    parameter stage = [0, 2]
    parameter follow = [False, True]
    parameter late = [False, True]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_moon_prepare(stage)
    $ calendar_v2.day = (20 if stage == 0 else 21) if late else (17 if stage == 0 else 18)
    $ calendar_v2.hour = 22
    $ calendar_v2.minute = 0
    $ rooms.enter("TavernMyRoom")
    run Call("TavernMyRoomWindowLookBackyard")
    if eval (stage == 0):
        advance until eval (external_moon_choices() == ["Далее"]) timeout 20.0
        assert eval (scene_runtime.picture.endswith("windowAmand.png"))
        click id (external_moon_button("Далее")) pos (0.5, 0.5)
        advance until eval (external_moon_choices() == ["Да", "Нет"]) timeout 20.0
        click id (external_moon_button("Да" if follow else "Нет")) pos (0.5, 0.5)
        if eval (follow):
            advance until eval (external_moon_choices() == ["Далее"]) timeout 20.0
            assert eval (rooms.current_code == "ShedRuinedChamber")
            click id (external_moon_button("Далее")) pos (0.5, 0.5)
            pause 0.1
            click id (external_moon_button("Далее")) pos (0.5, 0.5)
            advance until eval (external_moon_choices() == ["пойду-ка я отсюда."]) timeout 20.0
            assert eval ("чудом не были замечены" in scene_runtime.text)
            click id (external_moon_button("пойду-ка я отсюда.")) pos (0.5, 0.5)
    else:
        advance until eval ("Пойти проверить" in external_moon_choices()) timeout 20.0
        assert eval (scene_runtime.picture.endswith("ghostEvent/window_clue.png"))
        click id (external_moon_button("Пойти проверить" if follow else "Пока остаться у окна")) pos (0.5, 0.5)
        if eval (follow):
            advance until eval (external_moon_choices() == ["Послушать"]) timeout 20.0
            click id (external_moon_button("Послушать")) pos (0.5, 0.5)
SECOND_NIGHT_BEATS
            advance until eval (external_moon_choices() == ["Вернуться в трактир и подготовиться к завтрашней ночи"]) timeout 20.0
            click id (external_moon_button("Вернуться в трактир и подготовиться к завтрашней ночи")) pos (0.5, 0.5)
    advance until eval (not external_moon_choices() and rooms.current_code == "TavernMyRoom") timeout 20.0
    assert eval (threads["melissaMoonStoveRitual"].num == stage + (2 if follow else 1))
    assert eval (main_ui_runtime.scene_origin is None and main_ui_runtime.action_items)
    assert eval (not story_event_available("ShedRuinedChamber", "stove_hide_wait"))
    if eval (late and stage == 2 and follow):
        $ calendar_v2.advance_minutes(1380 - calendar_v2.clock_minutes())
        assert eval (not story_event_available("ShedRuinedChamber", "stove_hide_wait"))
        $ calendar_v2.advance_minutes(1440)
        assert eval (calendar_v2.day == 22 and story_event_available("ShedRuinedChamber", "stove_hide_wait"))

testcase external_moon_individual_visits:
    parameter npc = ["amanda", "melissa"]
    parameter accept = [False, True]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_moon_prepare()
    python:
        ritual = threads["melissaMoonStoveRitual"]
        ritual.advanceTo(5, complete_at_end=True)
        ritual.ritual_result = {"route": "no_glove", "participants": ["amanda", "melissa"], "ritual_participants": ["amanda", "melissa"]}
        for key in ("amanda", "melissa"):
            threads[key + "MoonProtection"].reset()
            people.get_info(key).anger_with_player = 0
            relationship_state(key)["anger"] = 0
        Melissa.storage_rat_help_day = 0
        Melissa.drawings_returned = True
        Melissa.drawings_booklet_left = True
        threads["melissaBatProblem"].advanceTo(threads["melissaBatProblem"].data.length, complete_at_end=True)
        tavern.renovations["roof"].status = "completed"
        calendar_v2.hour = 22 if npc == "amanda" else 23
        calendar_v2.minute = 0
        rooms.enter("TavernMyRoom")
        _moon_visit_accept = "Пустить её и выслушать" if npc == "amanda" else "Пригласить Мелиссу"
        _moon_visit_decline = "Проводить её обратно" if npc == "amanda" else "Проводить её в комнату"
    assert eval (story_event_available("TavernMyRoom", "bedtime"))
    run Call("checkTriggers", "TavernMyRoom", "bedtime", 0)
    advance until eval (_moon_visit_accept in external_moon_choices()) timeout 20.0
    click id (external_moon_button(_moon_visit_accept if accept else _moon_visit_decline)) pos (0.5, 0.5)
    advance until eval (not external_moon_choices() and main_ui_runtime.scene_origin is None) timeout 20.0
    assert eval (threads[npc + "MoonProtection"].completed == accept)
    assert eval (not threads[("melissa" if npc == "amanda" else "amanda") + "MoonProtection"].completed)

testcase external_moon_legacy_stages:
    parameter stage = [0, 1, 2, 3]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_moon_prepare()
    python:
        old_data = LThreadData(0, "melissa", "MoonStoveRitual", None, list([
            (target, None, None, None, 1, None, None, None, "TavernMyRoom", "enter", 30)
            for target in ("story_melissa_moon_window_clue_0", "story_melissa_moon_stove_wait_1", "story_melissa_moon_room_protection_2")
        ]))
        old_ritual = LThreadInfo(old_data)
        del old_ritual.ritual_result
        old_ritual.advanceTo(stage, complete_at_end=True)
        threads["melissaMoonStoveRitual"] = old_ritual
        threads["amandaMoonProtection"].reset()
        threads["melissaMoonProtection"].reset()
        _moon_migration_fun = player.condition.fun
        updateSave_V109()
        assert threads["melissaMoonStoveRitual"].num == (5 if stage >= 2 else stage)
        assert player.condition.fun == _moon_migration_fun
        if stage >= 2:
            assert threads["melissaMoonStoveRitual"].ritual_result["route"] == "glove"
            assert threads["melissaMoonStoveRitual"].completed
        else:
            assert threads["melissaMoonStoveRitual"].ritual_result is None
        assert threads["amandaMoonProtection"].completed == (stage == 3)
        _moon_migration_state = (old_ritual.num, old_ritual.completed, old_ritual.ritual_result)
        updateSave_V109()
        assert (old_ritual.num, old_ritual.completed, old_ritual.ritual_result) == _moon_migration_state
'''

BEAT = r'''
        advance until eval (external_moon_choices() == ["Далее"]) timeout 20.0
        assert eval (scene_runtime.picture == "images/tavern/backyard/shed/ghostEvent/" + _moon_test_pictures[INDEX])
        assert eval (main_ui_runtime.action_items == [])
        click id (external_moon_button("Далее")) pos (0.5, 0.5)
        pause 0.1
'''
TEST_RPY = TEST_RPY.replace("GLOVE_BEATS", "".join(BEAT.replace("INDEX", str(index)) for index in range(10)))
SECOND_BEAT = r'''
            advance until eval (external_moon_choices() == ["Далее"]) timeout 20.0
            assert eval (scene_runtime.picture.endswith("ghostEvent/stove_conversation.png") and main_ui_runtime.action_items == [])
            click id (external_moon_button("Далее")) pos (0.5, 0.5)
            pause 0.1
'''
TEST_RPY = TEST_RPY.replace("SECOND_NIGHT_BEATS", SECOND_BEAT * 11)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_moon_stove_"))
    try:
        copied.TEST_RPY = TEST_RPY
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary moon-stove project: {project}", flush=True)
        result = subprocess.run(
            [args.renpy, str(project), "--savedir", str(savedir), "test", "--hide-execution", "all", "--report-detailed"],
            text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        (project / "moon-stove-test.log").write_text(result.stdout, encoding="utf-8")
        copied.isolated.safe_print(result.stdout)
        return result.returncode
    finally:
        if args.keep_temp:
            print(f"Keeping temporary moon-stove project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_moon_stove_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
