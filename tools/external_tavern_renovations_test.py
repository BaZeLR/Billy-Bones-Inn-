#!/usr/bin/env python3
"""Check renovations in a copied native Ren'Py project with temporary saves."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import external_tavern_premium_test as isolated


TEST_RPY = r'''
init python:
    def external_renovation_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_renovation_button(prefix):
        index = next(index for index, caption in enumerate(external_renovation_choices()) if caption.startswith(prefix))
        return "choice_panel_button_%d" % index

    def external_renovation_prepare(code="shed"):
        for thread in threads.values():
            thread.abort()
        for project in TAVERN_RENOVATIONS.values():
            threads[project.thread_name].reset()
        initEvents()
        event_runtime.available.clear()
        event_runtime.fired_keys_today = []
        daily_events.rows = []
        player.tavern_management.breakfast.today = True
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        tavern.renovation_due_days = {}
        rooms.get("ShedWashroom").is_hidden = True
        player.set_money(5000)
        player.inventory.items["lumber_001"] = 5
        player.inventory.items["chopped_wood_001"] = 4
        shed = rooms.get("Shed")
        shed.game_items = [item for item in shed.game_items if get_object_id(item) not in ("lumber_001", "chopped_wood_001")]
        _room_add_item_units(shed, "lumber_001", 40)
        _room_add_item_units(shed, "chopped_wood_001", 7)
        calendar_v2.daysInGame = 30
        calendar_v2.week = 2
        calendar_v2.hour = 9
        calendar_v2.minute = 0
        threads["claraPaintingsPath"].advanceTo(14)
        project = TAVERN_RENOVATIONS[code]
        rooms.enter(people.location(project.quest_giver))
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_items = []
        scene_runtime.picture = rooms.current.bg_picture
        scene_runtime.text = "EXTERNAL_RENOVATION_ORIGIN"
        scene_runtime.location_text = scene_runtime.text
        findAvailableEvents(True)
        renpy.show_screen("main_ui")

testsuite global:
    teardown:
        exit

testcase external_renovation_real_request_order_build_and_complete:
    parameter code = ["backyard", "shed", "guest_room"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare(code)
    $ _project = TAVERN_RENOVATIONS[code]
    $ _quest = threads[_project.thread_name]
    assert eval (rooms.current.group_name == ROOM_GROUP_TAVERN)
    assert eval (not _project.order_visible and not tavern.order_renovation(code))
    run Call(people.get_info(_project.quest_giver).talk_label)
    advance until screen "choice" timeout 20.0
    click id (external_renovation_button("Обсудить")) pos (0.5, 0.5)
    advance until eval ("Хорошо, закажу работу у Драупнира" in external_renovation_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "event")
    assert eval (len(external_renovation_choices()) == 3)
    click id (external_renovation_button("Хорошо, закажу")) pos (0.5, 0.5)
    advance until eval ("Вернуться к разговору" in external_renovation_choices()) timeout 20.0
    assert eval (_quest.enabled and _quest.num == 1 and _project.order_visible)
    click id (external_renovation_button("Вернуться к разговору")) pos (0.5, 0.5)
    advance until eval ("Назад" in external_renovation_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "talk")
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    $ rooms.enter("StolyarWorkshop")
    run Call("IntDraupnirTalk")
    advance until eval ("Обустройство трактира" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Обустройство трактира")) pos (0.5, 0.5)
    advance until eval (_project.title in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button(_project.title)) pos (0.5, 0.5)
    advance until eval ("Заказать работу" in external_renovation_choices()) timeout 20.0
    $ _cash_before = player.economy.money
    click id (external_renovation_button("Заказать работу")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    assert eval (_quest.num == 2 and not _quest.completed and not _quest.aborted)
    assert eval (player.economy.money == _cash_before - _project.price)
    assert eval (_room_item_count_by_id(rooms.get("Shed"), "lumber_001") == 40 - _project.logs)
    assert eval (_room_item_count_by_id(rooms.get("Shed"), "chopped_wood_001") == 7)
    assert eval (tavern.renovation_due_days[code] == 30 + _project.days)
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval (_project.title in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button(_project.title)) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (external_renovation_choices() == ["Назад"])
    assert eval (not tavern.order_renovation(code) and player.economy.money == _cash_before - _project.price)
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (_project.title in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval ("Обустройство трактира" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    $ calendar_v2.daysInGame = tavern.renovation_due_days[code] - 1
    assert eval (not story_event_available(_project.room, "enter"))
    $ calendar_v2.daysInGame += 1
    python:
        assert story_event_available(_project.room, "enter"), (_quest.num, _quest.aborted, calendar_v2.daysInGame, tavern.renovation_due_days, _quest.getevent(2).auditChecks())
    run Jump(_project.room)
    advance until eval ("Осмотреть готовую работу" in external_renovation_choices()) timeout 20.0
    assert eval (_quest.num == 2 and not _quest.completed and main_ui_runtime.mode == "event")
    click id (external_renovation_button("Осмотреть готовую работу")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (_quest.num == 3 and _quest.completed and all(_quest.done))
    assert eval (rooms.current_code == _project.room and main_ui_runtime.scene_origin is None)
    python:
        if code == "shed":
            assert not rooms.get("ShedWashroom").is_hidden
            assert any(exit.target == "ShedWashroom" for exit in rooms.get("Shed").visible_exits())
    assert eval (not story_event_available(_project.room, "enter"))
    $ renpy.save("renovation-" + code, include_screenshot=False)

testcase external_renovation_postpone_or_abort:
    parameter decision = ["Обсудим это позже", "Отказаться от этого улучшения"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    run Call("checkTriggers", "talk_sandra", "renovation", 0)
    advance until eval (decision in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button(decision)) pos (0.5, 0.5)
    advance until eval ("Вернуться к разговору" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Вернуться к разговору")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    python:
        quest = threads["sandraTavernRenovation"]
        assert quest.num == 0 and not quest.completed
        assert quest.aborted == (decision == "Отказаться от этого улучшения")
        assert not TAVERN_RENOVATIONS["shed"].order_visible
        assert not tavern.order_renovation("shed")
        calendar_v2.daysInGame += 1
        assert story_event_available("talk_sandra", "renovation") == (not quest.aborted)

testcase external_renovation_insufficient_money_then_retry_same_day:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    $ threads["sandraTavernRenovation"].enable()
    $ threads["sandraTavernRenovation"].advance()
    $ rooms.enter("StolyarWorkshop")
    $ player.set_money(0)
    run Call("DraupnirRenovations")
    advance until eval ("Прачечная и купальня в сарае" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Прачечная")) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (external_renovation_choices() == ["Назад"] and threads["sandraTavernRenovation"].num == 1)
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval ("Прачечная и купальня в сарае" in external_renovation_choices()) timeout 20.0
    $ player.set_money(900)
    click id (external_renovation_button("Прачечная")) pos (0.5, 0.5)
    advance until eval ("Заказать работу" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Заказать работу")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    assert eval (threads["sandraTavernRenovation"].num == 2 and player.economy.money == 0)

testcase external_renovation_window_migration_keeps_owned_items:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        player.tavern_management.client_room_hole = 1
        old_room = rooms.get("TavernEmptyRoom")
        old_room.game_items.append("tavern_empty_room_peephole")
        old_room.game_items.append("soap_001")
        bedroom = rooms.get("TavernMyRoom")
        bedroom.game_items.append("myroom_guest_peephole")
        _logs_before = list(rooms.get("Shed").game_items)
        updateSave_V99()
        updateSave_V99()
        assert player.tavern_management.client_room_hole == 1
        assert [get_object_id(item) for item in bedroom.game_items].count("tavern_empty_room_peephole") == 1
        assert not any(get_object_id(item) in ("myroom_guest_peephole", "tavern_empty_room_peephole") for item in old_room.game_items)
        assert "soap_001" in old_room.game_items
        assert _logs_before == rooms.get("Shed").game_items
        assert not any("окошко" in str(item.caption).lower() for item in tavern_empty_room_action_items())
        assert "player_peephole" not in TAVERN_RENOVATIONS
    run Jump("TavernMyRoom")
    advance until eval (rooms.current_code == "TavernMyRoom") timeout 20.0
    assert eval (any(obj.object_id == "tavern_empty_room_peephole" for obj in rooms.current.visible_objects()))
    run Call("TavernMyRoomObjectMenu", "tavern_empty_room_peephole")
    advance until eval (main_ui_runtime.object_id == "tavern_empty_room_peephole") timeout 20.0
    run Call("TavernEmptyRoomPeekEmpty")
    advance until eval ("Закрыть окошко" in external_renovation_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernMyRoom")
    click id (external_renovation_button("Закрыть окошко")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernMyRoom")

testcase external_renovation_room_navigation_and_bathing:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        threads["sandraTavernRenovation"].advance()
        threads["sandraTavernRenovation"].advance()
        tavern.renovation_due_days["shed"] = 30
        assert story_event_available("Shed", "enter"), threads["sandraTavernRenovation"].getevent(2).auditChecks()
    run Jump("Shed")
    advance until eval ("Осмотреть готовую работу" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Осмотреть готовую работу")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    run Jump("ShedWashroom")
    advance until eval (rooms.current_code == "ShedWashroom") timeout 20.0
    $ _bath_origin = main_ui_context_snapshot()
    run Call("ShedWashroomBath")
    advance until eval ("Вымыться — 15 минут" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Вымыться")) pos (0.5, 0.5)
    advance until eval ("Назад" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (calendar_v2.minute == 15 and rooms.current_code == "ShedWashroom")
    assert eval (main_ui_context_snapshot() == _bath_origin)

testcase external_relocated_window_observes_existing_guest_scene:
    parameter girl = ["georgett", "liza"]
    parameter origin = ["TavernMyRoom", "TavernMain"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        calendar_v2.hour = 14
        info = people.get_info(girl)
        info.set_hired(True)
        info.assign_tavern_service("intimate", False)
        player.tavern_management.client_room_hole = 1
        SexEvents.delete_girl_today(girl)
        SexEvents.add_today(girl, calendar_v2.time_slot(), 2, "Prostitution")
        rooms.get("TavernMain").state["client_room_girl"] = girl
        threads["lizaTavernClientRoom"].reset()
    run Jump(origin)
    advance until eval (rooms.current_code == origin) timeout 20.0
    assert eval (tavern_empty_room_peephole_has_client())
    if eval (origin == "TavernMain"):
        run (next(item.action for item in main_ui_runtime.action_items if item.caption == "Пойти проверить отдельную комнату"))
    else:
        run Call("TavernMyRoomObjectMenu", "tavern_empty_room_peephole")
        advance until eval (main_ui_runtime.object_id == "tavern_empty_room_peephole") timeout 20.0
        run (next(item.action for item in main_ui_runtime.action_items if item.caption == "Подглядеть в комнату"))
    advance until eval ("Подсмотреть" in external_renovation_choices()) timeout 20.0
    assert eval ("Из своей комнаты" in scene_runtime.text)
    click id (external_renovation_button("Подсмотреть")) pos (0.5, 0.5)
    advance until eval (external_renovation_choices() == ["Вернуться"]) timeout 20.0
    assert eval (_media_asset_exists(scene_runtime.picture) and rooms.current_code == origin)
    click id (external_renovation_button("Вернуться")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (rooms.current_code == origin and main_ui_runtime.scene_origin is None)

testcase external_renovation_object_returns:
    parameter label_name = ["ShedRuinedStove", "ShedHotWaterStove"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    $ _origin = main_ui_context_snapshot()
    run Call(label_name)
    advance until screen "choice" timeout 20.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _origin)
'''


def build_temp_project(root: Path, temp_root: Path) -> Path:
    """Copy scripts/data; only immutable media directories point at the workspace."""
    project = temp_root / "TractirExternalRenovationsProject"
    game = project / "game"
    game.mkdir(parents=True)
    for entry in (root / "game").iterdir():
        target = game / entry.name
        if entry.name in {"cache", "__pycache__", "saves", "saves_test_run"}:
            continue
        if entry.is_dir() and entry.name in {"images", "audio", "music", "sounds", "gui", "fonts"}:
            isolated.junction_dir(entry, target)
        elif entry.is_dir():
            shutil.copytree(entry, target, ignore=shutil.ignore_patterns("*.rpyc", "*.rpymc", "*.pyc", "__pycache__"))
        elif entry.suffix.lower() not in {".rpyc", ".rpymc", ".pyc"}:
            shutil.copy2(entry, target)
    (game / "_external_tavern_renovations_test.rpy").write_text(TEST_RPY, encoding="utf-8")
    return project


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=isolated.RENPY_DEFAULT)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--compile-lint", action="store_true")
    args = parser.parse_args()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.is_file():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_renovations_"))
    environment = dict(os.environ)
    try:
        project = build_temp_project(isolated.project_root(), temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        print(f"Temporary renovation test project: {project}", flush=True)
        commands = [["compile"], ["lint"]] if args.compile_lint else []
        commands.append(["test", "--hide-execution", "all", "--report-detailed"])
        for command in commands:
            result = subprocess.run(
                [str(renpy_exe), str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=environment,
            )
            log = project / f"renovations-{command[0]}.log"
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            if result.stdout:
                isolated.safe_print(result.stdout)
            if result.returncode:
                return int(result.returncode)
        return 0
    except subprocess.TimeoutExpired as exc:
        print(f"Ren'Py renovation checks timed out after {args.timeout} seconds: {exc}", flush=True)
        return 124
    finally:
        if args.keep_temp:
            print(f"Keeping temporary renovation test project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_renovations_"):
                raise RuntimeError(f"Refusing to remove unexpected temporary path: {resolved}")
            isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
