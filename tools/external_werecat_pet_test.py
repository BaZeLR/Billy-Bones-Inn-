#!/usr/bin/env python3
"""Native catch choices, pet roaming and old-save migration in an isolated copy."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_cat_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption) for item in choice.scope.get("items", [])] if choice else []

    def external_cat_button(caption):
        return "choice_panel_button_%d" % external_cat_choices().index(caption)

    def external_cat_prepare():
        global saveVersion
        saveVersion = currentVersion
        for thread in threads.values():
            thread.abort()
        Mongol.arrival_due_day = -1
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        calendar_v2.daysInGame = 40
        calendar_v2.hour = 9
        calendar_v2.minute = 0
        player.tavern_management.breakfast.event_active = False
        werecat.owned = False
        werecat.stats = werecat_pet_defaults()
        werecat_state().clear()
        werecat_state().update(werecat_story_defaults())
        werecat_state().update(hunter_tease_day=0, tracks_seen=1, woods_exploration=200)
        WerecatStaticData.invalidate_daily_schedule()
        rooms.enter("Forest")
        findAvailableEvents(True)

    def external_cat_arm_trap():
        werecat_state()["trap_rooms"] = {"Forest": {"day": 38}}

    def external_cat_verify_load():
        expected = renpy.session.pop("cat_load_expected", None)
        if expected is None:
            return
        assert saveVersion == currentVersion
        assert werecat.owned and werecat.pet_name == "Луна"
        assert werecat_state()["sold_count"] >= 1
        assert werecat_state()["gifted_clara"] == 1
        assert werecat.var == {}
        assert not {"adopted", "sold", "name", "adopted_count"}.intersection(werecat_state())
        assert people.get_info("werecat") is werecat
        assert people.location("werecat")
        assert werecat_visible_text(people.location("werecat"))
        assert werecat_can_search("Forest")
        if expected != "user":
            assert werecat.stats["trust"] == 13 and werecat.stats["comfort"] == 15
            assert werecat.adopted_day == 8 and werecat.adoption_breakfast_seen
            assert werecat.first_month_thanks_day == 38
            assert player.economy.money == expected["money"]
            assert dict(player.inventory.items) == expected["inventory"]
        print("WERECAT_LOAD_PASSED", expected, werecat.stats, people.location("werecat"), flush=True)
        renpy.quit(0)

    config.after_load_callbacks.append(external_cat_verify_load)

label external_cat_legacy_checkpoint:
    $ external_cat_prepare()
    $ werecat.var = {"adopted": 1, "adopted_count": 1, "sold": 1, "gifted_clara": 1, "name": "Луна", "adopted_day": 8, "adoption_breakfast_seen": 1, "first_month_thanks_day": 38}
    $ werecat.stats.update(trust=13, comfort=15)
    $ saveVersion = 110
    $ renpy.session["cat_load_expected"] = {"money": player.economy.money, "inventory": dict(player.inventory.items)}
    hide screen main_ui
    $ renpy.block_rollback()
    pause 0.1
    $ renpy.save("cat-legacy", include_screenshot=False)
    $ renpy.load("cat-legacy")
    return

label external_cat_user_checkpoint:
    $ renpy.session["cat_load_expected"] = "user"
    hide screen main_ui
    $ renpy.load("cat-user")
    return

testsuite global:
    teardown:
        exit

testcase external_cat_repeatable_catches:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_cat_prepare()
    run Jump("Forest")
    advance until eval (rooms.current_code == "Forest" and not external_cat_choices()) timeout 20.0
    $ external_cat_arm_trap()
    run Call("WerecatCheckTrap", "Forest")
    advance until eval ("Забрать ее домой" in external_cat_choices()) timeout 20.0
    assert eval ("Продать работорговцам за 5000" in external_cat_choices())
    click id (external_cat_button("Забрать ее домой")) pos (0.5, 0.5)
    advance until eval (werecat.owned and not external_cat_choices()) timeout 20.0
    assert eval (werecat.pet_name == "Луна" and werecat.stats["trust"] == 6 and werecat.stats["comfort"] == 8)
    $ _cat_pet_stats = dict(werecat.stats)
    $ _cat_adopted_day = werecat.adopted_day
    $ _cat_location = people.location("werecat")
    assert eval (bool(_cat_location) and bool(werecat_visible_text(_cat_location)))
    assert eval (werecat.display_name() == "Луна")
    $ _cat_money = player.economy.money
    $ external_cat_arm_trap()
    run Call("WerecatCheckTrap", "Forest")
    advance until eval ("Продать работорговцам за 5000" in external_cat_choices()) timeout 20.0
    assert eval ("Забрать ее домой" not in external_cat_choices())
    assert eval ("Подарить ее Клариссе" in external_cat_choices())
    click id (external_cat_button("Продать работорговцам за 5000")) pos (0.5, 0.5)
    advance until eval (werecat_state()["sold_count"] == 1 and not external_cat_choices()) timeout 20.0
    assert eval (werecat.owned and werecat.adopted_day == _cat_adopted_day and werecat.stats == _cat_pet_stats)
    assert eval (player.economy.money == _cat_money + 5000 and werecat_can_search("Forest"))
    assert eval (people.location("werecat") == _cat_location)
    $ _cat_clara_friend = Clara.rel
    $ external_cat_arm_trap()
    run Call("WerecatCheckTrap", "Forest")
    advance until eval ("Подарить ее Клариссе" in external_cat_choices()) timeout 20.0
    click id (external_cat_button("Подарить ее Клариссе")) pos (0.5, 0.5)
    advance until eval (werecat_state()["gifted_clara"] == 1 and not external_cat_choices()) timeout 20.0
    assert eval (Clara.rel == min(Clara.relationship_cap, _cat_clara_friend + 3))
    assert eval (werecat.owned and werecat.stats == _cat_pet_stats and werecat_can_search("Forest"))
    $ external_cat_arm_trap()
    run Call("WerecatCheckTrap", "Forest")
    advance until eval ("Продать работорговцам за 5000" in external_cat_choices()) timeout 20.0
    assert eval ("Подарить ее Клариссе" not in external_cat_choices() and "Забрать ее домой" not in external_cat_choices())
    assert eval ("Отпустить" in external_cat_choices())
    click id (external_cat_button("Продать работорговцам за 5000")) pos (0.5, 0.5)
    advance until eval (werecat_state()["sold_count"] == 2 and not external_cat_choices()) timeout 20.0
    assert eval (werecat.owned and werecat.stats == _cat_pet_stats and werecat_can_search("Forest"))
    assert eval (player.economy.money == _cat_money + 10000)

testcase external_cat_hourly_roaming:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_cat_prepare()
    run Jump("Forest")
    advance until eval (rooms.current_code == "Forest" and not external_cat_choices()) timeout 20.0
    $ werecat.owned = True
    $ WerecatStaticData.invalidate_daily_schedule()
    python:
        locations = set()
        for hour in range(24):
            calendar_v2.hour = hour
            room = people.location("werecat")
            assert room in {"Backyard", "TavernKitchen", "TavernMain", "TavernStorage", "TavernMyRoom", "TavernMelissaRoom", "TavernAmandaRoom", "TavernSandraRoom"}
            assert "Луна" in werecat_visible_text(room)
            assert people.action_data_for_room("werecat", room) is not None
            locations.add(room)
        assert len(locations) > 1
    $ calendar_v2.hour = 9
    $ rooms.enter(people.location("werecat"))
    run Call("IntWerecatTalk")
    advance until eval ("Погладить кошку" in external_cat_choices()) timeout 20.0
    click id (external_cat_button("Погладить кошку")) pos (0.5, 0.5)
    advance until eval ("Закончить разговор" in external_cat_choices()) timeout 20.0
    assert eval (werecat.stats["trust"] == 1 and werecat.stats["comfort"] == 1)
    click id (external_cat_button("Закончить разговор")) pos (0.5, 0.5)
    advance until eval (not external_cat_choices()) timeout 20.0

testcase external_cat_old_save_load:
    enabled False
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    run Jump("external_cat_legacy_checkpoint")
    advance until eval (False) timeout 30.0

testcase external_cat_user_save_load:
    enabled False
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    run Jump("external_cat_user_checkpoint")
    advance until eval (False) timeout 30.0
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--saved-file", type=Path)
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_werecat_"))
    try:
        copied.TEST_RPY = TEST_RPY
        project = copied.build_temp_project(copied.isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        if args.saved_file:
            shutil.copy2(args.saved_file, savedir / "cat-user-LT1.save")
        print(f"Isolated project: {project}", flush=True)
        commands = [["compile"], ["lint"], ["test", "--hide-execution", "all", "--report-detailed"], ["test", "external_cat_old_save_load"]]
        if args.saved_file:
            commands.append(["test", "external_cat_user_save_load"])
        for index, command in enumerate(commands):
            result = subprocess.run([copied.isolated.RENPY_DEFAULT, str(project), "--savedir", str(savedir), *command],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace", timeout=120)
            (project / f"werecat-{index}.log").write_text(result.stdout, encoding="utf-8")
            copied.isolated.safe_print(result.stdout)
            if result.returncode:
                return result.returncode
            if command[-1].endswith("save_load") and "WERECAT_LOAD_PASSED" not in result.stdout:
                raise RuntimeError("Save-load assertions were not reached")
        return 0
    finally:
        if args.keep_temp:
            print(f"Keeping isolated project: {temp_root}", flush=True)
        else:
            copied.isolated.remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
