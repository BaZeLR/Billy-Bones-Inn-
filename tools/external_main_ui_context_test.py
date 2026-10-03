#!/usr/bin/env python3
"""Exercise menu ownership and actual loads in copied scripts/isolated saves."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_ui_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption) for item in choice.scope.get("items", [])] if choice else []

    def external_ui_items():
        return [str(item.caption) for item in main_ui_runtime.action_items]

    def external_ui_prepare():
        global saveVersion
        saveVersion = currentVersion
        for thread in threads.values():
            thread.abort()
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        calendar_v2.hour = 12
        calendar_v2.minute = 0

    def external_ui_remember_menu():
        renpy.session["ui_expected"] = {
            "mode": main_ui_runtime.mode,
            "title": main_ui_runtime.action_title,
            "items": external_ui_items(),
            "choices": external_ui_choices(),
            "scene_origin": main_ui_runtime.scene_origin is not None,
            "talk_origin": main_ui_runtime.talk_origin is not None,
            "card_origin": main_ui_runtime.card_origin is not None,
        }

    def external_ui_loaded():
        if "ui_expected" in renpy.session:
            renpy.session["ui_verify_pending"] = True

    def external_ui_load_interaction():
        if renpy.session.get("ui_verify_pending") and renpy.get_screen("main_ui") is not None:
            renpy.session["ui_verify_pending"] = False
            # Evaluate the resumed screen before inspecting its widgets. This
            # avoids relying on a timer while the test runner is loading.
            choice = renpy.get_screen("choice")
            if choice is not None:
                choice.update()
            renpy.get_screen("main_ui").update()
            external_ui_verify_load()

    config.after_load_callbacks.append(external_ui_loaded)
    config.interact_callbacks.append(external_ui_load_interaction)

    def external_ui_verify_load():
        expected = renpy.session["ui_expected"]
        assert main_ui_runtime.mode == expected["mode"], (main_ui_runtime.mode, expected)
        if expected.get("user_save"):
            assert rooms.current_code == "TavernMyRoom"
            assert "Вернуться в коридор наверху" in external_ui_items()
        else:
            assert main_ui_runtime.action_title == expected["title"]
            assert external_ui_items() == expected["items"]
            assert external_ui_choices() == expected["choices"], (external_ui_choices(), expected["choices"])
            assert (main_ui_runtime.scene_origin is not None) == expected["scene_origin"]
            assert (main_ui_runtime.talk_origin is not None) == expected["talk_origin"]
            assert (main_ui_runtime.card_origin is not None) == expected["card_origin"]
        assert renpy.get_widget("main_ui", "choice_panel_button_0") is not None
        if expected["mode"] == "event":
            assert not renpy.get_screen("main_ui").scope["_room_actions_visible"]
        else:
            assert renpy.get_screen("main_ui").scope["_room_actions_visible"]
        print("UI_CONTEXT_LOAD_PASSED", repr(expected), flush=True)
        renpy.quit(0)

label external_ui_dialogue_event:
    $ main_ui_begin_native_scene_state("UI regression event")
    show screen main_ui
    "UI regression paragraph."
    menu:
        "UI next beat":
            pass
    $ scene_runtime.text = "UI regression second beat."
    menu:
        "UI finish event":
            pass
    $ main_ui_end_native_scene_state()
    return

testsuite global:
    teardown:
        exit

testcase external_ui_owned_menu_flow:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    run Jump("TavernMyRoom")
    advance until eval (main_ui_runtime.mode == "scene" and "Кровать" in external_ui_items()) timeout 20.0
    assert eval (renpy.get_widget("main_ui", "choice_panel_button_0") is not None)
    run Call("TavernMyRoomObjectMenu", "myroom_window_001")
    advance until eval (external_ui_items() == ["Посмотреть во двор", "Назад"]) timeout 20.0
    assert eval ("Вернуться в коридор наверху" not in external_ui_items())
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_ui_choices() == ["Закрыть окно"]) timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    assert eval (renpy.get_widget("main_ui", "choice_panel_button_0") is not None)
    assert eval (not renpy.get_screen("main_ui").scope["_room_actions_visible"])
    click id "main_ui_inventory_button" pos (0.5, 0.5)
    pause 0.1
    assert eval (main_ui_runtime.mode == "event" and not main_ui_runtime.inventory_dropdown_open)
    assert eval (renpy.get_widget("main_ui", "main_ui_entity_button_player_you") is None)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_ui_choices() and external_ui_items() == ["Посмотреть во двор", "Назад"]) timeout 20.0
    run Call("external_ui_dialogue_event")
    advance until eval (renpy.get_screen("say") is not None and renpy.get_screen("say").scope.get("what") == "UI regression paragraph.") timeout 20.0
    assert eval (renpy.get_widget("main_ui", "choice_panel_button_0") is None)
    assert eval (not renpy.get_screen("main_ui").scope["_room_actions_visible"])
    click pos (0.2, 0.6)
    advance until eval (external_ui_choices() == ["UI next beat"]) timeout 20.0
    assert eval (renpy.get_widget("main_ui", "choice_panel_button_0") is not None)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_ui_choices() == ["UI finish event"]) timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_ui_items() == ["Посмотреть во двор", "Назад"] and not external_ui_choices()) timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval ("Вернуться в коридор наверху" in external_ui_items()) timeout 20.0
    assert eval (renpy.get_screen("main_ui").scope["_room_actions_visible"])

testcase external_ui_empty_say_does_not_cover_room_text:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    run Jump("TavernMain")
    advance until eval (rooms.current_code == "TavernMain" and main_ui_runtime.action_items) timeout 20.0
    $ renpy.show_screen("say", who=None, what="")
    $ renpy.get_screen("say").update()
    pause 0.2
    assert eval (renpy.get_screen("say") is not None and not renpy.get_screen("say").scope.get("what"))
    $ renpy.screenshot(config.basedir + "/room-text-empty-say.png")
    assert eval (renpy.get_widget("say", "window") is None)
    assert eval (renpy.get_widget("main_ui", "main_ui_scene_text") is not None)
    assert eval (renpy.get_widget("main_ui", "choice_panel_button_0") is not None)

testcase external_ui_dress_purchase_keeps_text_and_choices_in_order:
    parameter girl = ["amanda", "melissa", "sandra"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    python:
        calendar_v2.week = 2
        player.set_money(5000)
        dress_shop.produced = ""
        people.get_info(girl).corruption = 0
        people.get_info(girl).wardrobe.owned_items = []
        _dress = ""
        for item in dress_shop_catalog_items("female"):
            code = dress_shop_item_code(item)
            if code in DressTopPart and not _gds_dress_objection(girl, code):
                _dress = code
                break
        assert _dress, girl
        _dress_cost = _gds_dress_cost(_dress)
        _dress_money_before = player.economy.money
    run Jump("DressShop")
    advance until eval (rooms.current_code == "DressShop" and main_ui_runtime.action_items) timeout 20.0
    run Call("GirlDressBuy", girl)
    advance until screen "dress_shop_catalog_page" timeout 20.0
    assert eval ("Там вас уже ожидала" in scene_runtime.text)
    click id ("dress_shop_catalog_offer_" + _dress) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (external_ui_choices() == ["Подождать, пока Ирма снимет мерку", "Пройти вместе с девушками за занавеску", "Предложить снять мерку прямо на месте"])
    python:
        assert "мерку сейчас и снимет" in scene_runtime.text and "Там вас уже ожидала" not in scene_runtime.text, (main_ui_runtime.mode, scene_runtime.text, config.character_callback_compat)
    assert eval (renpy.get_screen("dress_shop_catalog_page") is None)
    assert eval (not renpy.get_screen("main_ui").scope["_room_actions_visible"])
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (external_ui_choices() == ["Попросить разрешить вам остаться", "Покаяться и заплатить"]) timeout 20.0
    assert eval ("достойный отпор" in scene_runtime.text and "Там вас уже ожидала" not in scene_runtime.text)
    assert eval (renpy.get_screen("main_ui").scope["_desc"] == scene_runtime.text)
    $ renpy.screenshot(config.basedir + "/dress-fitting-" + girl + ".png")
    click id "main_ui_inventory_button" pos (0.5, 0.5)
    pause 0.1
    assert eval (not main_ui_runtime.inventory_dropdown_open and external_ui_choices() == ["Попросить разрешить вам остаться", "Покаяться и заплатить"])
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (rooms.current_code == "ArtisansQuarter") timeout 20.0
    assert eval (dress_shop.produced == _dress and people.get_info(girl).wardrobe.owns(_dress))
    assert eval (player.economy.money == _dress_money_before - _dress_cost and player.appearance.girl_dresses_bought == 1)
    assert eval (not external_ui_choices() and main_ui_runtime.mode == "scene")

testcase external_ui_shopping_clothing_description_and_catalog_back:
    parameter girl = ["amanda", "melissa", "sandra"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    $ calendar_v2.week = 2
    run Jump("DressShop")
    advance until eval (rooms.current_code == "DressShop" and main_ui_runtime.action_items) timeout 20.0
    run Call("GirlDressBuy", girl)
    advance until screen "dress_shop_catalog_page" timeout 20.0
    click id "dress_shop_catalog_next" pos (0.5, 0.5)
    advance until eval (renpy.get_screen("dress_shop_catalog_page").scope["catalog_page"] == 1) timeout 20.0
    python:
        _clothing_origin = main_ui_context_snapshot()
        _clothing_money = player.economy.money
        _clothing_order = dress_shop.produced
        _clothing_layers = dict(people.get_info(girl).wardrobe.current_layers)
        _clothing_text = "\n\n".join(_girls_desc_build_lines(girl, clothing_only=True))
        _clothing_index = external_ui_items().index("Посмотреть во что одета " + people_display_name(girl))
    click id ("choice_panel_button_%d" % _clothing_index) pos (0.5, 0.5)
    advance until eval (external_ui_choices() == ["Назад"]) timeout 20.0
    assert eval (renpy.get_screen("dress_shop_catalog_page") is None and main_ui_runtime.mode == "event")
    assert eval (scene_runtime.text == _clothing_text and scene_runtime.picture == _clothing_origin["picture"])
    assert eval (renpy.get_screen("main_ui").scope["_desc"] == _clothing_text)
    assert eval ("Кожа:" not in scene_runtime.text and "кухарка" not in scene_runtime.text)
    $ renpy.screenshot(config.basedir + "/clothing-description-" + girl + ".png")
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (renpy.get_screen("dress_shop_catalog_page") is not None and main_ui_runtime.mode == "scene") timeout 20.0
    assert eval (renpy.get_screen("dress_shop_catalog_page").scope["catalog_page"] == 1)
    assert eval (main_ui_context_snapshot() == _clothing_origin)
    click id "dress_shop_catalog_back" pos (0.5, 0.5)
    advance until eval (renpy.get_screen("dress_shop_catalog_page") is None) timeout 20.0
    assert eval ("Выбрать одежду" in external_ui_items() and "Уйти из лавки" in external_ui_items())
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until screen "dress_shop_catalog_page" timeout 20.0
    assert eval (renpy.get_screen("dress_shop_catalog_page").scope["girl_name"] == girl)
    assert eval (player.economy.money == _clothing_money and dress_shop.produced == _clothing_order)
    assert eval (people.get_info(girl).wardrobe.current_layers == _clothing_layers)

testcase external_ui_standalone_catalog_back:
    parameter rack = ["male", "female"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    $ calendar_v2.week = 2
    run Jump("DressShop")
    advance until eval (rooms.current_code == "DressShop" and main_ui_runtime.action_items) timeout 20.0
    run Call("DressShopOpenCatalog", rack)
    advance until screen "dress_shop_catalog_page" timeout 20.0
    click id "dress_shop_catalog_back" pos (0.5, 0.5)
    advance until eval (renpy.get_screen("dress_shop_catalog_page") is None) timeout 20.0
    assert eval (external_ui_items() == ["Назад"])
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.object_id == "" and "Женские образцы" in external_ui_items()) timeout 20.0

testcase external_ui_georgett_departure_returns_to_room:
    parameter location = ["PortStreets", "TavernMain"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    $ Georgett.known = True
    $ Georgett.rel = 8
    $ Georgett.talked_today = 0
    $ Georgett.set_story_value("TalkChurchAfterCermonLiza", 0)
    $ Liza.witnessed_church_after_sermon = True
    $ _girl_loc = "street" if location == "PortStreets" else "tavern"
    $ _return_caption = "На портовые улицы" if _girl_loc == "street" else "Вернуться в трактир"
    run Jump(location)
    advance until eval (rooms.current_code == location and main_ui_runtime.mode == "scene" and bool(external_ui_items())) timeout 20.0
    $ _room_before = main_ui_context_snapshot()
    $ _day_before = calendar_v2.daysInGame
    $ _relation_before = Georgett.rel
    run Call("IntGeorgettTalk", "georgett", _girl_loc)
    advance until eval ("Рассказать про Лизетту и отца Герхарда" in external_ui_choices()) timeout 20.0
    $ _tell_index = external_ui_choices().index("Рассказать про Лизетту и отца Герхарда")
    click id ("choice_panel_button_%d" % _tell_index) pos (0.5, 0.5)
    advance until eval (external_ui_choices() == [_return_caption]) timeout 20.0
    assert eval ("с этими словами она удаляется" in scene_runtime.text)
    assert eval (not renpy.get_screen("main_ui").scope["_room_actions_visible"])
    assert eval (Georgett.story_value("TalkChurchAfterCermonLiza", 0) == 1 and Georgett.talk_count() == 1 and Georgett.rel == _relation_before + 1)
    screenshot ("georgett-departure-" + location + ".png")
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene" and not external_ui_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _room_before and rooms.current_code == location)
    assert eval (main_ui_runtime.talk_origin is None and calendar_v2.daysInGame == _day_before)
    assert eval (renpy.get_screen("main_ui").scope["_room_actions_visible"])
    # The later report has no departure and must retain the normal talk menu.
    run Call("IntGeorgettTalk", "georgett", _girl_loc)
    advance until eval ("Рассказать про Лизетту и отца Герхарда" in external_ui_choices()) timeout 20.0
    $ _tell_index = external_ui_choices().index("Рассказать про Лизетту и отца Герхарда")
    click id ("choice_panel_button_%d" % _tell_index) pos (0.5, 0.5)
    advance until eval ("Закончить разговор" in external_ui_choices() and "Вы рассказываете Жоржетте что вы снова видели" in scene_runtime.text) timeout 20.0
    assert eval (main_ui_runtime.mode == "talk" and _return_caption not in external_ui_choices() and Georgett.rel == _relation_before + 1 and Georgett.talk_count() == 2)
    $ _finish_index = external_ui_choices().index("Закончить разговор")
    click id ("choice_panel_button_%d" % _finish_index) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene" and not external_ui_choices()) timeout 20.0
    $ _exit_index = external_ui_items().index("Идти в храм Эллоны" if location == "PortStreets" else "Пройти на кухню")
    click id ("choice_panel_button_%d" % _exit_index) pos (0.5, 0.5)
    advance until eval (rooms.current_code == ("EllonaTemple" if location == "PortStreets" else "TavernKitchen")) timeout 20.0

testcase external_ui_clock_pictures:
    parameter hour = [0, 5, 6, 9, 12, 16, 17, 18, 19, 23]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    $ calendar_v2.week = 7
    $ calendar_v2.hour = hour
    $ calendar_v2.minute = 59
    $ _is_day = 6 <= hour < 18
    $ _artisan_day = ["images/general/LocArtisansQuarter1.jpg", "images/general/LocArtisansQuarter2.jpg", "images/general/LocArtisansQuarter3.jpg"]
    $ _artisan_night = ["images/general/LocArtisansQuarter3.png", "images/general/LocArtisansQuarter4.jpg"]
    run Jump("ArtisansQuarter")
    advance until eval (rooms.current_code == "ArtisansQuarter" and "Мастерские" in external_ui_items()) timeout 20.0
    assert eval (scene_runtime.picture in (_artisan_day if _is_day else _artisan_night))
    assert eval (resolve_main_ui_picture(rooms.current) == scene_runtime.picture)
    run Call("ArtisansQuarterObjectMenu", "workshops")
    advance until eval (external_ui_items() == ["Осмотреть мастерские", "Назад"]) timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval ("Мастерские" in external_ui_items()) timeout 20.0
    assert eval (scene_runtime.picture in (_artisan_day if _is_day else _artisan_night))
    # The closed carpenter uses the same street pictures, not the old mixed pool.
    run Jump("StolyarWorkshop")
    advance until eval (rooms.current_code == "StolyarWorkshop" and "Мастерская закрыта" in scene_runtime.text or rooms.current_code == "StolyarWorkshop" and "мастерская закрыта" in scene_runtime.text) timeout 20.0
    assert eval (scene_runtime.picture in (_artisan_day if _is_day else _artisan_night))
    run Jump("MarketPlace")
    advance until eval (rooms.current_code == "MarketPlace" and "Сегодня воскресенье и рынок закрыт." in scene_runtime.text) timeout 20.0
    assert eval (not rooms.current.is_open())
    assert eval (scene_runtime.picture == ("images/market/LocMarketPlace2.jpg" if _is_day else MARKETPLACE_CLOSED_PICTURE))
    assert eval (resolve_main_ui_picture(rooms.current) == scene_runtime.picture)
    assert eval ("Вернуться к трактиру" in external_ui_items() and "Идти в продуктовую лавку вдовы Блэнкеншип" not in external_ui_items())
    run Jump("TavernMyRoom")
    advance until eval (rooms.current_code == "TavernMyRoom" and "Кровать" in external_ui_items()) timeout 20.0
    run Call("TavernMyRoomObjectMenu", "myroom_window_001")
    advance until eval (external_ui_items() == ["Посмотреть во двор", "Назад"]) timeout 20.0
    assert eval (scene_runtime.picture == ("images/player_room/window0.png" if _is_day else "images/player_room/window2.png"))
    assert eval (resolve_main_ui_picture(rooms.current) == scene_runtime.picture)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_ui_choices() == ["Закрыть окно"]) timeout 20.0
    assert eval (scene_runtime.picture == ("images/player_room/window0.png" if _is_day else "images/player_room/window2.png"))
    assert eval (not renpy.get_screen("main_ui").scope["_room_actions_visible"])
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_ui_choices() and external_ui_items() == ["Посмотреть во двор", "Назад"]) timeout 20.0
    assert eval (scene_runtime.picture == ("images/player_room/window0.png" if _is_day else "images/player_room/window2.png"))

testcase external_ui_becky_front_text_matches_menu:
    parameter registered_arrival = [False, True]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    $ calendar_v2.hour = 20
    $ calendar_v2.week = 5
    python:
        while procedural_randint(1, 4, key="procedural:Town/BeckyHomeFront.rpy:entry_roll") == 4:
            calendar_v2.daysInGame += 1
        Becky.home_front_checked_today = True
        if registered_arrival:
            threads["beckyHome"].advanceTo(0, force_active=True)
            initStoryEventRuntime(True)
    # A caller's call-screen can be gone before the next authored label starts.
    run Hide("main_ui")
    run Call("BeckyHomeFront", "FromDances")
    advance until eval (external_ui_choices() == ["Зайти в дом", "Осторожно заглянуть за угол"]) timeout 20.0
    assert eval (rooms.current_code == "BeckyHomeFront" and rooms.current.state["inga_scene_roll"] == 3)
    assert eval ("Вдруг какое-то движение в темном углу за крыльцом привлекло ваше внимание." in scene_runtime.text)
    assert eval ("Что делать?" in scene_runtime.text and "По дороге к дому Бекки" not in scene_runtime.text)
    assert eval (scene_runtime.picture == becky_homefront_withbecky_picture())
    assert eval (renpy.get_screen("main_ui") is not None and not renpy.get_screen("main_ui").scope["_room_actions_visible"])
    assert eval (not registered_arrival or int(threads["beckyHome"].num) == 1)
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (external_ui_choices() == ["Зайти в дом"]) timeout 20.0
    assert eval ("Наверное, показалось: вы заглянули за крыльцо, но там никого не было." == scene_runtime.text)
    assert eval ("По дороге к дому Бекки" not in scene_runtime.text)

testcase external_ui_tavern_event_finish_restores_bar:
    parameter event_code = ["WaitressHarass", "CleaningHarass", "FightSmall"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    $ event_runtime.tavern_work_events = []
    $ event_runtime.tavern_work_plan_day = current_game_day()
    $ calendar_v2.week = 1
    run Jump("TavernMain")
    advance until eval ("Барная стойка" in external_ui_items()) timeout 20.0
    run Call("TavernMainObjectMenu", "bar_001")
    advance until eval (external_ui_items() == ["Наблюдать за происходящим в зале", "Выпить эля", "Позвать кого-нибудь выпить", "Назад"]) timeout 20.0
    python:
        calendar_v2.hour = 13
        calendar_v2.minute = 0
        for girl_id, girl in people.girl_items():
            girl.set_job_value("jobwaitress", 0)
            girl.set_job_value("jobcleaning", 0)
        AmandaStaticData.set_schedule([NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=999, working=True)])
        Amanda.set_job_value("jobwaitress" if event_code == "WaitressHarass" else "jobcleaning", 1)
        Amanda.set_harass_instruction("notallow")
        tavern.client_touch_policy = ""
        event_runtime.tavern_work_events = [tavern_work_plan_row(tavern_work_definition(event_code), calendar_v2.time_slot())]
        event_runtime.tavern_played_today = []
        event_runtime.tavern_report_rows = []
        threads["tavernWorkRandomEvents"].advanceTo(0, force_active=True)
        initStoryEventRuntime(True)
        _external_bar_origin = main_ui_context_snapshot()
        _external_bar_back = list(main_ui_runtime.action_items[-1].action)
    assert eval (story_event_available("TavernMain", "enter"))
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and not renpy.get_screen("main_ui").scope["_room_actions_visible"])
    if eval (event_code == "FightSmall"):
        click id "choice_panel_button_0" pos (0.5, 0.5)
        advance until eval (external_ui_choices() == ["Вернуться к своим делам"] or (not external_ui_choices() and main_ui_runtime.mode == "scene")) timeout 20.0
    else:
        click id "choice_panel_button_2" pos (0.5, 0.5)
        advance until eval ("Промолчать" in external_ui_choices()) timeout 20.0
        $ _external_free_choice = "choice_panel_button_%s" % next(i for i, caption in enumerate(external_ui_choices()) if "поступала как считает нужным" in caption)
        click id _external_free_choice pos (0.5, 0.5)
        advance until eval (external_ui_choices() == ["Вернуться к делам"]) timeout 20.0
        assert eval ("ее решением" in scene_runtime.text and "оказанное ей доверие" in scene_runtime.text)
        assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    if eval external_ui_choices():
        click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_ui_choices() and main_ui_runtime.mode == "scene") timeout 20.0
    assert eval (scene_runtime.text == _external_bar_origin["main_text"])
    assert eval (scene_runtime.location_text == _external_bar_origin["location_text"])
    assert eval (scene_runtime.picture == _external_bar_origin["picture"] and main_ui_runtime.scene_origin is None)
    assert eval (main_ui_runtime.action_title == "Барная стойка" and external_ui_items() == ["Наблюдать за происходящим в зале", "Выпить эля", "Позвать кого-нибудь выпить", "Назад"])
    assert eval (event_runtime.tavern_played_today == [event_code] and len(event_runtime.tavern_report_rows) == 1 and not event_runtime.tavern_work_events)
    assert eval (calendar_v2.hour == 14 and calendar_v2.minute == 0)
    click id "choice_panel_button_3" pos (0.5, 0.5)
    advance until eval (main_ui_runtime.action_title == "Действия в трактире") timeout 20.0
    assert eval (scene_runtime.text.startswith("Главная зала трактира") and "ее решением" not in scene_runtime.text and "Что вы намеренны предпринять?" not in scene_runtime.text)
    assert eval (scene_runtime.text == _external_bar_back[1].value and scene_runtime.location_text == _external_bar_back[2].value and scene_runtime.picture == _external_bar_back[0].value)
    assert eval (event_runtime.tavern_played_today == [event_code])

testcase external_ui_object_load:
    enabled False
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    run Jump("TavernMyRoom")
    advance until eval ("Кровать" in external_ui_items()) timeout 20.0
    run Call("TavernMyRoomObjectMenu", "myroom_window_001")
    advance until eval (external_ui_items() == ["Посмотреть во двор", "Назад"]) timeout 20.0
    $ external_ui_remember_menu()
    $ renpy.save("ui-object", include_screenshot=False)
    run FileLoad("ui-object", slot=True, confirm=False)
    advance until eval (False) timeout 30.0

testcase external_ui_event_load:
    enabled False
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    run Jump("TavernMyRoom")
    advance until eval ("Кровать" in external_ui_items()) timeout 20.0
    run Call("TavernMyRoomObjectMenu", "myroom_window_001")
    advance until eval (external_ui_items() == ["Посмотреть во двор", "Назад"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (external_ui_choices() == ["Закрыть окно"]) timeout 20.0
    $ external_ui_remember_menu()
    $ renpy.save("ui-event", include_screenshot=False)
    run FileLoad("ui-event", slot=True, confirm=False)
    advance until eval (False) timeout 30.0

testcase external_ui_card_load:
    enabled False
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_ui_prepare()
    run Jump("TavernMyRoom")
    advance until eval ("Кровать" in external_ui_items()) timeout 20.0
    run Call("PlayerCardMainMenu")
    advance until eval (main_ui_runtime.mode == "mc") timeout 20.0
    $ external_ui_remember_menu()
    $ renpy.save("ui-card", include_screenshot=False)
    run FileLoad("ui-card", slot=True, confirm=False)
    advance until eval (False) timeout 30.0

testcase external_ui_user_save_load:
    enabled False
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ renpy.session["ui_expected"] = {"mode": "scene", "user_save": True}
    run FileLoad("ui-user", slot=True, confirm=False)
    advance until eval (False) timeout 30.0
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renpy", default=copied.isolated.RENPY_DEFAULT)
    parser.add_argument("--saved-file", type=Path)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--testcase", action="append", help="Run selected native testcases after compile/lint")
    args = parser.parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="tractir_ui_context_"))
    try:
        copied.TEST_RPY = TEST_RPY
        root = copied.isolated.project_root()
        project = copied.build_temp_project(root, temp_root)
        savedir = project / ".test-saves"
        savedir.mkdir()
        if args.saved_file:
            # Preserve statement identities for the copied user's return stack.
            for compiled in (root / "game").rglob("*.rpyc"):
                relative = compiled.relative_to(root / "game")
                if relative.parts[0] in {"cache", "images", "audio", "music", "sounds", "gui", "fonts", "saves", "saves_test_run"}:
                    continue
                target = project / "game" / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(compiled, target)
            shutil.copy2(args.saved_file, savedir / "ui-user-LT1.save")
        print(f"Isolated UI project: {project}", flush=True)
        commands = [["compile"], ["lint"], ["test", "external_ui_dress_purchase_keeps_text_and_choices_in_order"],
                    ["test", "external_ui_georgett_departure_returns_to_room"],
                    ["test", "external_ui_clock_pictures"],
                    ["test", "external_ui_becky_front_text_matches_menu"],
                    ["test", "external_ui_tavern_event_finish_restores_bar"],
                    ["test", "external_ui_shopping_clothing_description_and_catalog_back"],
                    ["test", "external_ui_standalone_catalog_back"],
                    ["test", "external_ui_empty_say_does_not_cover_room_text"],
                    ["test", "external_ui_owned_menu_flow"],
                    ["test", "external_ui_object_load"],
                    ["test", "external_ui_event_load"],
                    ["test", "external_ui_card_load"]]
        if args.saved_file:
            commands.append(["test", "external_ui_user_save_load"])
        if args.testcase:
            commands = [["compile"], ["lint"]] + [["test", name] for name in args.testcase]
        for index, command in enumerate(commands):
            result = subprocess.run([args.renpy, str(project), "--savedir", str(savedir), *command],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    encoding="utf-8", errors="replace", timeout=90)
            (project / f"ui-context-{index}.log").write_text(result.stdout, encoding="utf-8")
            copied.isolated.safe_print(result.stdout)
            if result.returncode:
                return result.returncode
            if "load" in command[-1] and "UI_CONTEXT_LOAD_PASSED" not in result.stdout:
                raise RuntimeError("Actual save-load assertions were not reached")
        return 0
    finally:
        if args.keep_temp:
            print(f"Keeping isolated UI project: {temp_root}", flush=True)
        else:
            resolved = temp_root.resolve()
            if resolved.parent != Path(tempfile.gettempdir()).resolve() or not resolved.name.startswith("tractir_ui_context_"):
                raise RuntimeError(f"Unexpected temporary path: {resolved}")
            copied.isolated.remove_temp_tree(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
