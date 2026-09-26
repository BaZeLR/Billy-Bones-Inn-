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

    def external_renovation_save_old_owner():
        global tavern, saveVersion
        renpy.session["renovation_load_expected"] = (
            player.economy.money, dict(player.inventory.items),
            [get_object_id(item) for item in rooms.get("Shed").game_items],
            {key: info.mana for key, info in people.girl_items()},
        )
        rooms.get("TavernEmptyRoom").game_items = ["soap_001"]
        Sofa.installed = True
        TavernGuestRoomStoveObject.state["chopped_wood_stock"] = 3
        TavernGuestRoomStoveObject.state["fire_until_minute"] = _pc_calendar_total_minutes() + 600
        TavernGuestRoomStoveObject.state["ash_dirty"] = 1
        renpy.session["guest_stove_load_expected"] = dict(TavernGuestRoomStoveObject.state)
        ShedHotWaterStoveObject.state["hot_water_until_minute"] = _pc_calendar_total_minutes() + 600
        renpy.session["shed_stove_load_expected"] = dict(ShedHotWaterStoveObject.state)
        tavern = TavernInfo.__new__(TavernInfo)
        tavern.renovation_due_days = {"shed": 34}
        player.tavern_management.slogan_state = 2
        player.tavern_management.client_room_hole = 1
        player.tavern_management.glory_hole = 1
        Draupnir.glory_hole_quote_received = True
        Melissa.roof_repair_complete_day = 32
        saveVersion = 100
        for info in (Sandra, Melissa, Clara):
            del info.renovation_requests

    def external_renovation_verify_loaded_owner():
        expected = renpy.session.pop("renovation_load_expected", None)
        if expected is None:
            return
        assert saveVersion == currentVersion
        assert tavern.renovation_complete("peephole") and tavern.renovation_complete("sign")
        assert tavern.renovations["roof"].due_day == 32 and tavern.renovations["shed"].due_day == 34
        assert tavern.renovations["glory_hole"].status == "building"
        assert not hasattr(tavern, "renovation_due_days")
        assert not hasattr(player.tavern_management, "client_room_hole")
        assert expected == (player.economy.money, dict(player.inventory.items), [get_object_id(item) for item in rooms.get("Shed").game_items], {key: info.mana for key, info in people.girl_items()})
        assert rooms.get("TavernEmptyRoom").game_items == ["soap_001", "guest_room_stove_001"]
        assert TavernGuestRoomStoveObject.state == renpy.session.pop("guest_stove_load_expected")
        assert get_game_object("guest_room_stove_001") is TavernGuestRoomStoveObject
        assert ShedHotWaterStoveObject.state == renpy.session.pop("shed_stove_load_expected")
        assert get_game_object("shed_hot_water_stove") is ShedHotWaterStoveObject
        assert Sofa.installed and people.location("sofa") == "TavernEmptyRoom"
        assert people.get_info("nostar") is Nostar
        assert rooms.get("NostarHouse") is not None and rooms.get("NobilityQuarters") is not None
        assert any(exit.target == "NobilityQuarters" and exit.condition is not None and exit.is_visible() == artisans_quarter_sofa_asked() for exit in rooms.get("ArtisansQuarter").exits)
        assert Sandra.renovation_requests["shed"] is True
        assert Clara.renovation_requests["guest_room"] is False
        print("RENOVATION_FULL_LOAD_PASSED", flush=True)
        renpy.quit(0)

    config.after_load_callbacks.append(external_renovation_verify_loaded_owner)

    def external_renovation_prepare(code="shed"):
        for thread in threads.values():
            thread.abort()
        threads["tavernRenovations"] = UThreadInfo(threadData["tavernRenovations"])
        initEvents()
        event_runtime.available.clear()
        event_runtime.fired_keys_today = []
        daily_events.rows = []
        player.tavern_management.breakfast.today = True
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        tavern.renovations = {key: TavernRenovation(key) for key in TAVERN_RENOVATIONS}
        for code_key in ("backyard", "shed", "guest_room"):
            people.get_info(TAVERN_RENOVATIONS[code_key].quest_giver).renovation_requests[code_key] = False
        Sofa.installed = False
        TavernGuestRoomStoveObject.state = {"fire_started_minute": 0, "fire_until_minute": 0, "fire_adds": 0, "ash_dirty": 0, "chopped_wood_stock": 0}
        ShedHotWaterStoveObject.state = {"fire_started_minute": 0, "fire_until_minute": 0, "fire_adds": 0, "ash_dirty": 0, "chopped_wood_stock": 0, "hot_water_until_minute": 0, "boiledWaterToday": 0}
        rooms.get("ShedWashroom").is_hidden = False
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

label external_renovation_legacy_checkpoint:
    $ external_renovation_prepare()
    hide screen main_ui
    $ external_renovation_save_old_owner()
    $ renpy.block_rollback()
    pause 0.1
    $ renpy.save("renovation-v100", include_screenshot=False)
    $ renpy.load("renovation-v100")
    return

testsuite global:
    teardown:
        exit

testcase external_renovation_real_request_order_build_and_complete:
    parameter code = ["backyard", "shed", "guest_room"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare(code)
    $ _project = TAVERN_RENOVATIONS[code]
    $ _quest = threads["tavernRenovations"]
    assert eval (rooms.current.group_name == ROOM_GROUP_TAVERN)
    assert eval (not _project.order_visible and not tavern.order_renovation(code))
    run Call(people.get_info(_project.quest_giver).talk_label)
    advance until screen "choice" timeout 20.0
    click id (external_renovation_button("Обсудить")) pos (0.5, 0.5)
    advance until eval ("Хорошо, закажу работу у Драупнира" in external_renovation_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "event")
    assert eval (len(external_renovation_choices()) == 3)
    assert eval (people.get_info(_project.quest_giver).renovation_requests[code] is True and _project.order_visible)
    assert eval (story_event_available("talk_draupnir", "renovation_" + code))
    $ renpy.save("pending-member-request", include_screenshot=False)
    $ _saved_requester_name = {"backyard": "Melissa", "shed": "Sandra", "guest_room": "Clara"}[code]
    assert eval (renpy.get_save_data("pending-member-request")[_saved_requester_name].renovation_requests[code] is True)
    click id (external_renovation_button("Хорошо, закажу")) pos (0.5, 0.5)
    advance until eval ("Вернуться к разговору" in external_renovation_choices()) timeout 20.0
    assert eval (_quest.enabled and tavern.renovations[code].status == "accepted" and _project.order_visible)
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
    assert eval (tavern.renovations[code].status == "building" and not _quest.completed and not _quest.aborted)
    assert eval (player.economy.money == _cash_before - _project.price)
    assert eval (_room_item_count_by_id(rooms.get("Shed"), "lumber_001") == 40 - _project.logs)
    assert eval (_room_item_count_by_id(rooms.get("Shed"), "chopped_wood_001") == 7)
    assert eval (tavern.renovations[code].due_day == 30 + _project.days)
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
    $ calendar_v2.daysInGame = tavern.renovations[code].due_day - 1
    assert eval (not story_event_available(_project.room, "enter"))
    $ calendar_v2.daysInGame += 1
    run Call("NextDay_NewDayEvents")
    pause 0.1
    assert eval (story_event_available(_project.room, "enter"))
    run Jump(_project.room)
    advance until eval ("Осмотреть готовую работу" in external_renovation_choices()) timeout 20.0
    assert eval (tavern.renovation_complete(code) and not _quest.completed and main_ui_runtime.mode == "event")
    assert eval (people.get_info(_project.quest_giver).renovation_requests[code] is False and not _project.order_visible)
    click id (external_renovation_button("Осмотреть готовую работу")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (_quest.num == 1 and _quest.done[list(TAVERN_RENOVATIONS).index(code)] and not _quest.completed)
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
        quest = threads["tavernRenovations"]
        assert not quest.completed and not quest.aborted
        assert (tavern.renovations["shed"].status == "declined") == (decision == "Отказаться от этого улучшения")
        assert TAVERN_RENOVATIONS["shed"].order_visible == (decision == "Обсудим это позже")
        assert Sandra.renovation_requests["shed"] == (decision == "Обсудим это позже")
        calendar_v2.daysInGame += 1
        assert not story_event_available("talk_sandra", "renovation")
        assert tavern.order_renovation("shed") == (decision == "Обсудим это позже")

testcase external_renovation_insufficient_money_then_retry_same_day:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    $ tavern.renovations["shed"].request("sandra")
    $ tavern.renovations["shed"].accept()
    $ rooms.enter("StolyarWorkshop")
    $ player.set_money(0)
    run Call("DraupnirRenovations")
    advance until eval ("Прачечная и купальня в сарае" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Прачечная")) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (external_renovation_choices() == ["Назад"] and tavern.renovations["shed"].status == "accepted")
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval ("Прачечная и купальня в сарае" in external_renovation_choices()) timeout 20.0
    $ player.set_money(900)
    click id (external_renovation_button("Прачечная")) pos (0.5, 0.5)
    advance until eval ("Заказать работу" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Заказать работу")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    assert eval (tavern.renovations["shed"].status == "building" and player.economy.money == 0)

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
        updateSave_V100()
        updateSave_V99()
        updateSave_V100()
        assert tavern.renovation_complete("peephole")
        assert not hasattr(player.tavern_management, "client_room_hole")
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
        tavern.renovations["shed"].request("sandra")
        tavern.renovations["shed"].accept()
        assert tavern.order_renovation("shed")
        calendar_v2.daysInGame += 4
        tavern.finish_due_renovations()
        assert story_event_available("Shed", "enter")
    run Jump("Shed")
    advance until eval ("Осмотреть готовую работу" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Осмотреть готовую работу")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    run Jump("ShedWashroom")
    advance until eval (rooms.current_code == "ShedWashroom") timeout 20.0
    $ _bath_origin = main_ui_context_snapshot()
    run Call("ShedWashroomBath")
    advance until eval ("Назад" in external_renovation_choices()) timeout 20.0
    assert eval ("Вымыться — 15 минут" not in external_renovation_choices())
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    run Jump("Shed")
    advance until eval (rooms.current_code == "Shed") timeout 20.0
    assert eval (any(item.caption == "Печь и запас дров" for item in main_ui_runtime.action_items))
    run Call("ShedHotWaterStove")
    advance until eval ("Подготовить купальню" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Подготовить купальню")) pos (0.5, 0.5)
    advance until eval (_pc_hot_water_is_ready(ShedHotWaterStoveObject)) timeout 20.0
    assert eval (_pc_fire_is_active(ShedHotWaterStoveObject) and _object_state_int(ShedHotWaterStoveObject, "boiledWaterToday", 0) == 1)
    assert eval (player.item_count("chopped_wood_001") == 3 and calendar_v2.hour == 10)
    advance until eval ("Назад" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
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
    assert eval (calendar_v2.hour == 10 and calendar_v2.minute == 15 and rooms.current_code == "ShedWashroom")
    assert eval (main_ui_context_snapshot() == _bath_origin)

testcase external_shed_first_breakfast_reaction_once:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        tavern.renovations["shed"].status = "completed"
        threads["tavernShedRenovationBreakfast"] = createThread(threadData["tavernShedRenovationBreakfast"])
        player.tavern_management.breakfast.event_active = True
        player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
        rooms.enter("TavernKitchen")
        findAvailableEvents(True)
    assert eval (story_event_available("TavernKitchen", "breakfast"))
    run Call("checkTriggers", "TavernKitchen", "breakfast", 0)
    advance until eval ("Выслушать остальных" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Выслушать остальных")) pos (0.5, 0.5) until eval ("Продолжить разговор" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Продолжить разговор")) pos (0.5, 0.5) until eval ("Улыбнуться" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Улыбнуться")) pos (0.5, 0.5) until eval ("Продолжить завтрак" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Продолжить завтрак")) pos (0.5, 0.5) until eval (threads["tavernShedRenovationBreakfast"].completed) timeout 20.0
    assert eval (not story_event_available("TavernKitchen", "breakfast"))

testcase external_repaired_backyard_toilet_scene_once:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare("backyard")
    python:
        tavern.renovations["backyard"].status = "completed"
        threads["tavernBackyardToiletFirstUse"] = createThread(threadData["tavernBackyardToiletFirstUse"])
        calendar_v2.hour = 13
        findAvailableEvents(True)
    $ rooms.enter("Backyard")
    assert eval (backyard_dynamic_picture() in ("images/tavern/backyard/backyard_renewal_day.png", "images/tavern/backyard/backyard_renewal_rain.png"))
    run Call("BackyardObjectMenu", "backyard_toilet")
    assert eval ("BackyardUseToilet" in [str(getattr(getattr(item, "action", None), "label", "") or "") for item in main_ui_runtime.action_items]) timeout 5.0
    run Call("BackyardUseToilet")
    advance until eval ("Осмотреть рисунки" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Осмотреть рисунки")) pos (0.5, 0.5) until eval ("Выйти во двор" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Выйти во двор")) pos (0.5, 0.5) until eval (threads["tavernBackyardToiletFirstUse"].completed) timeout 20.0
    assert eval ("shit_with_comfort" in tractir_progress.achieved and not story_event_available("Backyard", "toilet_first_use"))
    $ calendar_v2.hour = 21
    assert eval (backyard_dynamic_picture() == "images/tavern/backyard/backyard_renewal_night.png")

testcase external_shed_bathday_requires_hot_water_and_plays_three_pictures:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        threads["tavernBathDay"] = RThreadInfo(threadData["tavernBathDay"])
        tavern.renovations["shed"].status = "completed"
        calendar_v2.week = 3
        calendar_v2.hour = 21
        rooms.enter("ShedWashroom")
    assert eval (not story_event_available("ShedWashroom", "enter"))
    $ _set_object_state_int(ShedHotWaterStoveObject, "hot_water_until_minute", _pc_calendar_total_minutes() + 120)
    assert eval (_pc_hot_water_is_ready(ShedHotWaterStoveObject))
    assert eval (threads["tavernBathDay"].checkActive())
    assert eval (all(row["ok"] for row in threadData["tavernBathDay"].triggers[0][0].auditChecks()))
    assert eval (story_event_available("ShedWashroom", "enter"))
    $ _bath_beauty_before = [girl.sex_stat("beauty", 0) for girl in (Sandra, Melissa, Amanda)]
    run Call("checkTriggers", "ShedWashroom", "enter", 0)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    $ _bath_pictures_seen = [str(scene_runtime.picture)]
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    $ _bath_pictures_seen.append(str(scene_runtime.picture))
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    $ _bath_pictures_seen.append(str(scene_runtime.picture))
    assert eval (len(set(_bath_pictures_seen)) == 3 and all("bathDay/" in path for path in _bath_pictures_seen))
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Вернуться в купальню" in external_renovation_choices()) timeout 20.0
    assert eval (all(girl.sex_stat("beauty", 0) == min(100, before + 10) and girl.bathday_day == current_game_day() for girl, before in zip((Sandra, Melissa, Amanda), _bath_beauty_before)))
    assert eval (not _pc_hot_water_is_ready(ShedHotWaterStoveObject))
    click id (external_renovation_button("Вернуться в купальню")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (not story_event_available("ShedWashroom", "enter"))

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
        tavern.renovations["peephole"].status = "completed"
        threads["tavernRenovations"].seen(list(TAVERN_RENOVATIONS).index("peephole"))
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
        assert eval (scene_runtime.picture == "images/tavern/guest_room/peephole_closed.png")
        run (next(item.action for item in main_ui_runtime.action_items if item.caption == "Осторожно открыть окошко"))
    advance until eval ("Подсмотреть" in external_renovation_choices()) timeout 20.0
    if eval (origin == "TavernMyRoom"):
        assert eval (scene_runtime.picture == "guest_room_peek" and "осторожно открываете" in scene_runtime.text)
    else:
        assert eval ("Из своей комнаты" in scene_runtime.text)
    click id (external_renovation_button("Подсмотреть")) pos (0.5, 0.5)
    advance until eval (external_renovation_choices() == ["Вернуться"]) timeout 20.0
    assert eval (_media_asset_exists(scene_runtime.picture) and rooms.current_code == origin)
    assert eval (str(getattr(scene_runtime, "picture_overlay", "") or "") == ("images/tavern/guest_room/peephole_frame.png" if origin == "TavernMyRoom" else ""))
    click id (external_renovation_button("Вернуться")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (rooms.current_code == origin and main_ui_runtime.scene_origin is None and not getattr(scene_runtime, "picture_overlay", ""))

testcase external_relocated_window_opens_empty_guest_room:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    $ tavern.renovations["peephole"].status = "completed"
    $ rooms.get("TavernMain").state["client_room_girl"] = ""
    run Jump("TavernMyRoom")
    advance until eval (rooms.current_code == "TavernMyRoom") timeout 20.0
    run Call("TavernMyRoomObjectMenu", "tavern_empty_room_peephole")
    advance until eval (main_ui_runtime.object_id == "tavern_empty_room_peephole") timeout 20.0
    assert eval (scene_runtime.picture == "images/tavern/guest_room/peephole_closed.png")
    run (next(item.action for item in main_ui_runtime.action_items if item.caption == "Осторожно открыть окошко"))
    advance until screen "choice" timeout 20.0
    assert eval (scene_runtime.picture == "guest_room_peek" and "никого нет" in scene_runtime.text)
    click id (external_renovation_button("Закрыть окошко")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernMyRoom" and scene_runtime.picture != "guest_room_peek" and main_ui_runtime.scene_origin is None)
    run Call("TavernMyRoomObjectMenu", "tavern_empty_room_peephole")
    advance until eval (main_ui_runtime.object_id == "tavern_empty_room_peephole") timeout 20.0
    assert eval (scene_runtime.picture == "images/tavern/guest_room/peephole_closed.png")

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
testcase external_renovation_all_payments_next_day_and_builder:
    parameter code = ["sign", "peephole", "glory_hole", "roof", "backyard", "shed", "guest_room"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    python:
        project = TAVERN_RENOVATIONS[code]
        tavern.renovations[code].request(project.quest_giver)
        tavern.renovations[code].accept()
        rooms.enter("StolyarWorkshop")
        worker_mana = {key: info.mana for key, info in people.girl_items() if info.is_tavern_worker()}
        before_time = (calendar_v2.hour, calendar_v2.minute)
    run Call("DraupnirRenovationOrder", code)
    advance until eval ("Заказать работу" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Заказать работу")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    assert eval ((calendar_v2.hour, calendar_v2.minute) == before_time)
    assert eval (people.location("draupnir") == project.room)
    assert eval (not Draupnir.social_action_allowed("talk"))
    assert eval (project.title in tavern.renovation_work_description)
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    $ calendar_v2.daysInGame += project.days
    run Call("NextDay_NewDayEvents")
    pause 0.1
    assert eval (tavern.renovation_complete(code))
    assert eval (people.location("draupnir") == "StolyarWorkshop")
    assert eval (Draupnir.social_action_allowed("talk"))
    python:
        for key, mana_before in worker_mana.items():
            assert people.get_info(key).mana == min(100, mana_before + 1 + (2 if key == project.quest_giver else 0))
        assert threads["melissaBatProblem"].num == 0
        finish_mana = {key: info.mana for key, info in people.girl_items() if key in worker_mana}
        tavern.finish_due_renovations()
        assert finish_mana == {key: info.mana for key, info in people.girl_items() if key in worker_mana}
    run Jump(project.room)
    advance until eval ("Осмотреть готовую работу" in external_renovation_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "event")
    click id (external_renovation_button("Осмотреть готовую работу")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (not story_event_available(project.room, "enter"))
    $ renpy.save("renovation-roundtrip", include_screenshot=False)
    $ _saved_renovations = renpy.get_save_data("renovation-roundtrip")["tavern"].renovations
    assert eval (_saved_renovations[code].status == "completed")
    assert eval (_saved_renovations[code].paid_maravedies == project.price)

testcase external_roof_keeps_melissa_story:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare()
    $ threads["melissaBatProblem"].reset()
    $ threads["melissaRatProblem"].complete()
    $ threads["melissaBatProblem"].advanceTo(7)
    $ rooms.enter("TavernAtic")
    assert eval (story_event_available("TavernAtic", "melissa_bats"))
    run Call("checkTriggers", "TavernAtic", "melissa_bats", 0)
    advance until eval ("Закажу починку у Драупнира" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Закажу починку")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (tavern.renovations["roof"].status == "accepted" and player.economy.money == 5000)
    assert eval (story_event_available("talk_draupnir", "renovation_roof"))
    $ rooms.enter("StolyarWorkshop")
    $ tavern.order_renovation("roof")
    assert eval (not story_event_available("talk_melissa", "melissa_breakfast_invite"))
    $ calendar_v2.daysInGame += 2
    run Call("NextDay_NewDayEvents")
    pause 0.1
    assert eval (threads["melissaBatProblem"].num == 7 and not threads["melissaBatProblem"].completed)
    assert eval (story_event_available("talk_melissa", "melissa_breakfast_invite"))

testcase external_guest_room_day_night_views:
    parameter hour = [9, 21]
    parameter installed = [False, True]
    parameter fire_lit = [False, True]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare("guest_room")
    $ tavern.renovations["guest_room"].status = "completed"
    $ threads["tavernRenovations"].seen(list(TAVERN_RENOVATIONS).index("guest_room"))
    $ calendar_v2.hour = hour
    $ Sofa.installed = installed
    if eval (fire_lit):
        $ _set_object_state_int(TavernGuestRoomStoveObject, "fire_until_minute", _pc_calendar_total_minutes() + 720)
    run Jump("TavernEmptyRoom")
    advance until eval (rooms.current_code == "TavernEmptyRoom" and main_ui_runtime.action_title == rooms.current.display_name) timeout 20.0
    assert eval (scene_runtime.picture == "images/tavern/guest_room/%s_%s_%s.png" % ("sofa" if installed else "lounge", "day" if hour == 9 else "night", "lit" if fire_lit else "cold"))
    assert eval (_media_asset_exists(scene_runtime.picture))
    $ rooms.enter("TavernMyRoom")
    run Call("TavernEmptyRoomPeekEmpty")
    advance until screen "choice" timeout 20.0
    assert eval (scene_runtime.picture == "guest_room_peek" and renpy.has_image("guest_room_peek"))
    pause 0.1
    $ renpy.screenshot(config.basedir + "/guest-peek-%s-%s-%s.png" % (hour, installed, fire_lit))
    click id (external_renovation_button("Закрыть окошко")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0

testcase external_sofa_own_portrait_and_talk:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare("guest_room")
    $ Sofa.installed = True
    $ rooms.enter("TavernEmptyRoom")
    run Call("IntSofaTalk")
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "talk")
    assert eval (scene_runtime.picture == SofaStaticData.portrait == "images/tavern/guest_room/sofa_day_cold.png")
    assert eval (people.location("sofa") == "TavernEmptyRoom")
    assert eval (SofaStaticData.selectIcon() == SofaStaticData.portrait and _media_asset_exists(SofaStaticData.portrait))
    click id (external_renovation_button("Закончить разговор")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0

testcase external_guest_stove_fire_clean_and_back:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare("guest_room")
    $ tavern.renovations["guest_room"].status = "completed"
    $ threads["tavernRenovations"].seen(list(TAVERN_RENOVATIONS).index("guest_room"))
    $ Sofa.installed = True
    $ player.condition.fun = 100
    $ player.condition.energy = 100
    $ player.inventory.items["chopped_wood_001"] = 3
    $ _hall_fire_before = dict(TavernMainFireplaceObject.state)
    $ _kitchen_fire_before = dict(TavernKitchenHearthObject.state)
    run Jump("TavernEmptyRoom")
    advance until eval (rooms.current_code == "TavernEmptyRoom") timeout 20.0
    click id ("choice_panel_button_%d" % [item.caption for item in main_ui_runtime.action_items].index("Каменная печь")) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (_guest_stove_fire_caption == "Разжечь огонь")
    click id (external_renovation_button("Сложить рядом дрова")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    assert eval (_object_state_int(TavernGuestRoomStoveObject, "chopped_wood_stock", 0) == 1 and player.item_count("chopped_wood_001") == 2)
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval (_guest_stove_fire_caption == "Разжечь огонь") timeout 20.0
    assert eval ("Сложить все дрова" in external_renovation_choices())
    click id (external_renovation_button("Сложить все дрова")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    assert eval (_object_state_int(TavernGuestRoomStoveObject, "chopped_wood_stock", 0) == 3 and player.item_count("chopped_wood_001") == 0)
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval (_guest_stove_fire_caption == "Разжечь огонь") timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    assert eval (_pc_fire_is_active(TavernGuestRoomStoveObject) and player.item_count("chopped_wood_001") == 0 and _object_state_int(TavernGuestRoomStoveObject, "chopped_wood_stock", 0) == 2)
    assert eval (scene_runtime.picture.endswith("sofa_day_lit.png"))
    $ renpy.screenshot(config.basedir + "/guest-stove-lit.png")
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Вычистить золу" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Вычистить золу")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    assert eval (_object_state_int(TavernGuestRoomStoveObject, "ash_dirty", 0) == 0)
    assert eval (_hall_fire_before == dict(TavernMainFireplaceObject.state) and _kitchen_fire_before == dict(TavernKitchenHearthObject.state))
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Назад" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernEmptyRoom" and scene_runtime.picture.endswith("sofa_day_lit.png"))

testcase external_guest_door_and_save_upgrade:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_renovation_prepare("guest_room")
    $ _guest = rooms.get("TavernEmptyRoom")
    assert eval (not any(exit.target == "TavernGloryHole" for exit in _guest.visible_exits()))
    $ tavern.renovations["glory_hole"].status = "completed"
    assert eval (any(exit.target == "TavernGloryHole" for exit in _guest.visible_exits()))
    assert eval (any(exit.target == "TavernEmptyRoom" for exit in rooms.get("TavernGloryHole").visible_exits()))
    assert eval (any(exit.target == "TavernMain" for exit in rooms.get("TavernGloryHole").visible_exits()))
    $ _guest.game_items = ["soap_001"]
    $ TavernGuestRoomStoveObject.state["chopped_wood_stock"] = 3
    $ Sofa.installed = True
    $ updateSave_V101()
    $ updateSave_V101()
    assert eval (_guest.game_items == ["soap_001", "guest_room_stove_001"])
    assert eval (Sofa.installed and TavernGuestRoomStoveObject.state["chopped_wood_stock"] == 3)
    $ threads["tavernRenovations"].seen(list(TAVERN_RENOVATIONS).index("glory_hole"))
    run Jump("TavernEmptyRoom")
    advance until eval (rooms.current_code == "TavernEmptyRoom") timeout 20.0
    click id ("choice_panel_button_%d" % [item.caption for item in main_ui_runtime.action_items].index("Пройти к глорихолу")) pos (0.5, 0.5)
    advance until eval (rooms.current_code == "TavernGloryHole") timeout 20.0
    assert eval (any(item.caption == "Вернуться в гостевую" for item in main_ui_runtime.action_items))
    click id ("choice_panel_button_%d" % [item.caption for item in main_ui_runtime.action_items].index("Вернуться в гостевую")) pos (0.5, 0.5)
    advance until eval (rooms.current_code == "TavernEmptyRoom") timeout 20.0
    assert eval (scene_runtime.picture == tavern_empty_room_picture() and scene_runtime.text == tavern_empty_room_description())

testcase external_renovation_old_save_full_load:
    enabled False
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    run Jump("external_renovation_legacy_checkpoint")
    advance until eval (False) timeout 20.0

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
        commands.append(["test", "external_renovation_old_save_full_load"])
        for command in commands:
            result = subprocess.run(
                [str(renpy_exe), str(project), "--savedir", str(savedir), *command],
                text=True, encoding="utf-8", errors="replace", timeout=args.timeout,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=environment,
            )
            load_test = "external_renovation_old_save_full_load" in command
            log = project / ("renovations-load.log" if load_test else f"renovations-{command[0]}.log")
            log.write_text(result.stdout, encoding="utf-8")
            print(f"Ren'Py {command[0]}: exit {result.returncode}; log {log}", flush=True)
            if result.stdout:
                isolated.safe_print(result.stdout)
            if result.returncode:
                return int(result.returncode)
            if load_test and "RENOVATION_FULL_LOAD_PASSED" not in result.stdout:
                raise RuntimeError("Save/load validation did not reach its assertions")
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
