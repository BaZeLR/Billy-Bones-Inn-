#!/usr/bin/env python3
"""Run Ren'Py click-play checks without adding test labels to this project.

The harness builds a temporary project tree outside the repository. Root game
files are copied, large game subdirectories are linked, and the generated
Ren'Py testcase is written only into that temporary tree.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOM_LABELS = [
    "TavernMain",
    "TavernKitchen",
    "Backyard",
    "Shed",
    "TavernStorage",
    "TavernStable",
    "TavernUpstairs",
    "TavernMyRoom",
    "TavernAmandaRoom",
    "TavernSandraRoom",
    "TavernMelissaRoom",
    "TavernEmptyRoom",
    "TavernAtic",
    "StreetTavern",
    "PortStreets",
    "EllonaTemple",
    "EllonaBirthRoom",
    "MarketPlace",
    "HunterClub",
    "WineStore",
    "GroceryStore",
    "CityGuard",
    "ArtisansQuarter",
    "StolyarWorkshop",
    "DressShop",
    "BarberShop",
    "Church",
    "Forest",
    "ForestClearing",
    "ForestLake",
    "ForestSpring",
    "ForestWaterfall",
    "ForestHiddenPath",
    "ForestDarkWoods",
    "ForestCave",
]

ROOM_ACTION_INDEX_LIMIT = 24


def safe_print(text: str) -> None:
    try:
        print(text, end="" if text.endswith("\n") else "\n")
    except UnicodeEncodeError:
        encoded = text.encode(sys.stdout.encoding or "utf-8", errors="replace")
        sys.stdout.buffer.write(encoded)
        if not text.endswith("\n"):
            sys.stdout.buffer.write(b"\n")


TEST_HEADER = r'''
testsuite global:
    teardown:
        exit

testcase external_room_clock_clicks:
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0

'''


ROOM_CHECK_TEMPLATE = r'''
    $ week = 1
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ Friends["sandra"] = max(int(Friends.get("sandra", 0) or 0), 10)
    $ SandraVar["RoomUnlocked"] = 1
    $ BedroomDoorStates["TavernSandraRoom"] = 0

    run Jump("{room_name}")
    advance until screen "main_ui" timeout 20.0
    pause 0.1
    assert eval (str(CurLoc or "") == "{room_name}") timeout 5.0
    click id "main_ui_time_button" pos (0.5, 0.5) until eval (str(main_ui_overlay or "") == "time") timeout 10.0
    click id "time_change_back_button" pos (0.5, 0.5) until eval (str(main_ui_overlay or "") == "") timeout 10.0

    click pos (1748, 179) until eval (str(main_ui_overlay or "") == "story") timeout 10.0
    click pos (1748, 227) until eval (str(main_ui_overlay or "") == "people") timeout 10.0
    click id "main_ui_time_button" pos (0.5, 0.5) until eval (str(main_ui_overlay or "") == "time") timeout 10.0
    click id "time_change_back_button" pos (0.5, 0.5) until eval (str(main_ui_overlay or "") == "") timeout 10.0
'''


SHOP_ACTION_CHECKS = r'''
testcase external_shop_action_logic:
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ npc_schedule_sync_all()
    $ CurrentLoc["eddie"] = "GroceryStore"

    $ CurrentRoom = GroceryStoreRoom
    $ CurLoc = "GroceryStore"
    $ location = CurLoc
    $ GrocerName = "Эдди"
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Провизия' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Купить провизию' not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("GroceryStoreObjectMenu", "food_stock")
    assert eval (str(current_action_title or "") == 'Провизия') timeout 5.0
    assert eval ('Купить провизию' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Купить крынку молока' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Осмотреть товар' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("GroceryStoreObjectText", "food_stock", "examine_food_stock")
    assert eval (str(current_action_title or "") == 'Провизия') timeout 5.0
    assert eval ('Мешки, капуста' in str(MainTxt or "")) timeout 5.0
    assert eval ('Купить провизию' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Назад' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ Talked["eddie"] = 0
    $ TalkedToday["eddie"] = 0
    $ Friends["eddie"] = 0
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    $ renpy.call_in_new_context("IntEddieTalk")
    assert eval (str(current_action_title or "") == 'Разговор с Эдди') timeout 5.0
    assert eval ('Поболтать с Эдди о разной фигне.' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Call' in str(type([i.action for i in current_action_items if str(i.caption or "") == 'Поболтать с Эдди о разной фигне.'][0]))) timeout 5.0
    $ renpy.call_in_new_context("IntEddieTalkApply", "smalltalk")
    assert eval ('Вы некоторое время болтаете с Эдди' in str(MainTxt or "")) timeout 5.0
    assert eval (int(Talked.get("eddie", 0) or 0) == 1) timeout 5.0
    assert eval (int(TalkedToday.get("eddie", 0) or 0) == 1) timeout 5.0
    assert eval ('Поболтать с Эдди о разной фигне.' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ Talked["eddie"] = 3
    $ renpy.call_in_new_context("IntEddieTalkApply", "smalltalk")
    assert eval ('Ничего нового из разговора вы не узнали.' in str(MainTxt or "")) timeout 5.0

    $ week = 1
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ npc_schedule_sync_all()

    $ CurrentRoom = WineStoreRoom
    $ CurLoc = "WineStore"
    $ location = CurLoc
    $ GrocerName = "Альбер"
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Бочки с вином' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ([str(i.caption or "") for i in current_action_items].count('Купить вино') == 0) timeout 5.0
    $ renpy.call_in_new_context("WineStoreObjectMenu", "wine_stock")
    assert eval (str(current_action_title or "") == 'Бочки с вином') timeout 5.0
    assert eval ([str(i.caption or "") for i in current_action_items].count('Купить вино') == 1) timeout 5.0
    $ _wine_picture_before = str(_layout_last_picture or "")
    $ renpy.call_in_new_context("WineStoreObjectText", "wine_stock", "examine_wine")
    assert eval (str(current_action_title or "") == 'Бочки с вином') timeout 5.0
    assert eval ('Повсюду бочки' in str(MainTxt or "")) timeout 5.0
    assert eval ('Купить вино' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (str(_layout_last_picture or "") == _wine_picture_before) timeout 5.0

    $ week = 1
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ npc_schedule_sync_all()

    $ CurrentRoom = MarketPlaceRoom
    $ CurLoc = "MarketPlace"
    $ location = CurLoc
    $ MainTxt = MarketPlaceRoom.descriptions[0].text + "\n\n" + MarketPlaceRoom.descriptions[1].text + "\n\n" + MarketPlaceRoom.descriptions[2].text
    $ CurLocDesc = MainTxt
    $ MarketPlaceSavedText = MainTxt
    $ market_mongol_visible = 0
    $ market_mongol_mode = ""
    $ MyStallion = "test-horse"
    $ _layout_last_picture = MarketPlaceRoom.bg_picture
    $ renpy.call_in_new_context("MarketPlaceBuildActions")
    assert eval ('Рыночные лотки' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Осмотреть рыночные лотки' not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ _market_picture_before = str(_layout_last_picture or "")
    $ renpy.call_in_new_context("MarketPlaceObjectMenu", "market_stalls")
    assert eval (str(current_action_title or "") == 'Рыночные лотки') timeout 5.0
    assert eval ('Осмотреть лотки' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("MarketPlaceObjectText", "market_stalls", "examine_market_stalls")
    assert eval (str(current_action_title or "") == 'Рыночные лотки') timeout 5.0
    assert eval ('Торговцы расхваливают товар' in str(MainTxt or "")) timeout 5.0
    assert eval ('Осмотреть лотки' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (str(_layout_last_picture or "") == _market_picture_before) timeout 5.0
'''


DOG_ENTITY_ACTION_CHECKS = r'''
testcase external_dog_entity_actions:
    $ week = 1
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ ensure_dog_runtime()
    $ dog.owned = True
    $ dog.in_company = False
    $ dog.booth_built = True
    $ dog.loyalty = max(int(dog.loyalty or 0), 12)
    $ dog.health = dog.max_health

    run Jump("Backyard")
    advance until screen "main_ui" timeout 20.0
    assert eval (dog_is_available_here("Backyard")) timeout 5.0
    assert eval ("dog" in [str(row.get("id", "") or "") for row in _character_action_grid_entries(CurrentRoom)]) timeout 5.0

    $ open_dog_action_menu_state("Backyard")
    assert eval (str(action_menu_entity_type or "") == "dog") timeout 5.0
    assert eval (str(action_menu_entity_id or "") == "dog") timeout 5.0
    assert eval ("Осмотреть" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Поговорить" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ DogActionLookState("Backyard")
    assert eval (str(UI_mode or "") == "dog") timeout 5.0
    assert eval (len(list(dog_card_lines() or [])) > 0) timeout 5.0
    assert eval (len(list(current_action_items or [])) > 0) timeout 5.0
    assert eval ("Поиграть с псом" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Позаниматься дрессировкой" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Взять пса на охоту" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Назад" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ renpy.call_in_new_context("IntDogTalk", "Backyard")
    assert eval (str(current_action_title or "") == "Пес рядом") timeout 5.0
    assert eval ("Осмотреть" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Поиграть с псом" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
'''


ACTUAL_ACTION_BUTTON_CLICK_CHECKS = r'''
init -1 python:
    def external_prepare_market_click_state():
        global week, time, hour, minute, BlockTimeAdvance, TavernEventOngoing
        global BlindPirateMarketEventSeen, main_ui_overlay, main_ui_inventory_dropdown_open
        global action_menu_specs, current_action_content, UI_mode
        global CurrentRoom, CurLoc, location, MainTxt, CurLocDesc, MarketPlaceSavedText
        global market_mongol_visible, market_mongol_mode, MyStallion, _layout_last_picture
        global current_action_title, current_action_items
        week = 1
        time = 1
        hour = 12
        minute = 0
        BlockTimeAdvance = 0
        TavernEventOngoing = ""
        BlindPirateMarketEventSeen = 1
        main_ui_overlay = ""
        main_ui_inventory_dropdown_open = False
        action_menu_specs = []
        current_action_content = None
        UI_mode = "scene"
        CurrentRoom = MarketPlaceRoom
        CurLoc = "MarketPlace"
        location = CurLoc
        MainTxt = MarketPlaceRoom.descriptions[0].text + "\n\n" + MarketPlaceRoom.descriptions[1].text + "\n\n" + MarketPlaceRoom.descriptions[2].text
        CurLocDesc = MainTxt
        MarketPlaceSavedText = MainTxt
        market_mongol_visible = 0
        market_mongol_mode = ""
        MyStallion = "test-horse"
        _layout_last_picture = MarketPlaceRoom.bg_picture
        current_action_title = "Действия"
        current_action_items = marketplace_action_items()

label external_market_click_entry:
    $ external_prepare_market_click_state()
    while True:
        call screen main_ui

testcase external_actual_grocery_click:
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ CurrentLoc["eddie"] = "GroceryStore"
    $ npc_schedule_sync_all()
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Провизия' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == 'Провизия') timeout 20.0
    assert eval ('Купить провизию' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval ('Мешки, капуста' in str(MainTxt or "")) timeout 20.0

testcase external_actual_wine_click:
    $ week = 1
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ money = max(int(money or 0), 1000)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Бочки с вином' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == 'Бочки с вином') timeout 20.0
    assert eval ('Купить вино' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == 'Покупка вина') timeout 20.0
    assert eval ('Купить один бочонок' in [str(i.caption or "") for i in current_action_items]) timeout 5.0

testcase external_actual_market_click:
    $ week = 1
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Jump("external_market_click_entry")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Рыночные лотки' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == 'Рыночные лотки') timeout 20.0
    assert eval ('Осмотреть лотки' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ('Торговцы расхваливают товар' in str(MainTxt or "")) timeout 20.0
'''


ACTUAL_RANDOM_TOWN_CLICK_CHECKS = r'''
label external_random_town_sink:
    $ current_action_title = "External click sink"
    $ current_action_items = []
    call screen main_ui
    return

testcase external_actual_random_town_continue_click:
    $ week = 2
    $ time = 4
    $ hour = 22
    $ minute = 0
    $ dayspassed = 5
    $ CurLoc = "external_random_town_sink"
    $ location = CurLoc
    $ CurrentRoom = StreetTavernRoom
    $ exploration = 300
    $ notoriety = 60
    $ money = 500
    $ tavernfame = 10
    $ TownStreetEventsToday = 0
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ GuardCaptainVar = {}
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ renpy.random.seed(11)
    run Jump("TownRandomChronicleEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Городские слухи") timeout 5.0
    assert eval (str(TownStreetLastEventText or "") != "") timeout 5.0
    assert eval (len(str(TownStreetLastEventText or "")) > 80 and TownStreetEventsToday == 1) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == "External click sink") timeout 20.0

testcase external_actual_random_town_click:
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ BlindPirateMarketEventSeen = 1
    $ TownStreetEventsToday = 2
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0

    $ week = 2
    $ time = 4
    $ hour = 22
    $ minute = 0
    $ dayspassed = 5
    $ CurLoc = "StreetTavern"
    $ location = CurLoc
    $ CurrentRoom = StreetTavernRoom
    $ _layout_last_picture = "bg StreetTavern"
    $ exploration = 300
    $ notoriety = 60
    $ money = 500
    $ tavernfame = 10
    $ TownStreetEventsToday = 0
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ GuardCaptainVar = {}
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Jump("TownStreetPatrolEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Ночной патруль") timeout 5.0
    assert eval ("Спрятаться и уйти дворами" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click pos (1500, 555)
    pause 0.2
    assert eval (TownStreetPatrolsToday >= 1 and exploration >= 308 and town_street.random_seen_this_slot(CurLoc)) timeout 5.0

    $ week = 3
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ dayspassed = 0
    $ CurLoc = "MarketPlace"
    $ location = CurLoc
    $ CurrentRoom = MarketPlaceRoom
    $ _layout_last_picture = "bg MarketPlace"
    $ exploration = 100
    $ notoriety = 0
    $ tavernfame = 0
    $ TownStreetEventsToday = 2
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ TavernBlackworkerCandidates = []
    $ TavernBlackworkers = []
    $ TownStreetContext = {}
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Jump("TownStreetHelpEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Уличная просьба") timeout 5.0
    assert eval ("Дать еды и предложить грязную работу при трактире" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click pos (1500, 485)
    pause 0.2
    assert eval (len(TavernBlackworkerCandidates) >= 1 and tavernfame >= 1 and exploration >= 105) timeout 5.0

    $ week = 4
    $ time = 3
    $ hour = 18
    $ minute = 0
    $ dayspassed = 1
    $ CurLoc = "ArtisansQuarter"
    $ location = CurLoc
    $ CurrentRoom = ArtisansQuarterRoom
    $ _layout_last_picture = "bg ArtisansQuarter"
    $ exploration = 300
    $ notoriety = 0
    $ TownStreetEventsToday = 2
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Jump("TownStreetThugsEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Уличные громилы") timeout 5.0
    assert eval ("Попробовать спугнуть их криком" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click pos (1500, 520)
    pause 0.2
    assert eval (exploration >= 306 and notoriety >= 2) timeout 5.0
'''


ROOM_ACTION_DISPATCH_CHECKS = r'''
init -1 python:
    import renpy.exports as _audit_renpy

    ACTION_AUDIT_ROOM_LABELS = [
        "TavernMain",
        "TavernKitchen",
        "Backyard",
        "Shed",
        "TavernStorage",
        "TavernStable",
        "TavernUpstairs",
        "TavernMyRoom",
        "TavernAmandaRoom",
        "TavernSandraRoom",
        "TavernMelissaRoom",
        "TavernEmptyRoom",
        "TavernAtic",
        "StreetTavern",
        "PortStreets",
        "EllonaTemple",
        "EllonaBirthRoom",
        "MarketPlace",
        "HunterClub",
        "WineStore",
        "GroceryStore",
        "CityGuard",
        "ArtisansQuarter",
        "StolyarWorkshop",
        "DressShop",
        "BarberShop",
        "Church",
        "Forest",
        "ForestClearing",
        "ForestLake",
        "ForestSpring",
        "ForestWaterfall",
        "ForestHiddenPath",
        "ForestDarkWoods",
        "ForestCave",
    ]

    ACTION_AUDIT_REPORT = []
    ACTION_AUDIT_FAILURES = []
    ACTION_AUDIT_CAPTURED = 0
    ACTION_AUDIT_DISPATCHED = 0

    def _audit_text(value):
        try:
            return str(value or "")
        except Exception:
            return ""

    def _audit_action_type(action):
        try:
            return type(action).__name__
        except Exception:
            return ""

    def _audit_action_target(action):
        if action is None:
            return ""
        for attr in ("label", "target", "name", "callable", "function"):
            try:
                value = getattr(action, attr)
            except Exception:
                continue
            if value:
                return _audit_text(value)
        try:
            return repr(action)
        except Exception:
            return _audit_action_type(action)

    def _audit_state_signature():
        captions = []
        try:
            captions = [_audit_text(getattr(i, "caption", "")) for i in list(current_action_items or [])]
        except Exception:
            captions = []
        return (
            _audit_text(CurLoc),
            _audit_text(current_action_title),
            _audit_text(MainTxt),
            _audit_text(_layout_last_picture),
            tuple(captions),
        )

    def _audit_prepare_common():
        global week, time, hour, minute, BlockTimeAdvance, TavernEventOngoing
        global BlindPirateMarketEventSeen, main_ui_overlay, main_ui_inventory_dropdown_open
        global action_menu_specs, current_action_content, UI_mode
        week = 1
        time = 1
        hour = 12
        minute = 0
        BlockTimeAdvance = 0
        TavernEventOngoing = ""
        BlindPirateMarketEventSeen = 1
        main_ui_overlay = ""
        main_ui_inventory_dropdown_open = False
        action_menu_specs = []
        current_action_content = None
        UI_mode = "scene"
        try:
            Friends["sandra"] = max(int(Friends.get("sandra", 0) or 0), 10)
            SandraVar["RoomUnlocked"] = 1
            BedroomDoorStates["TavernSandraRoom"] = 0
            CurrentLoc["eddie"] = "GroceryStore"
            CurrentLoc["becky"] = "GroceryStore"
            CurrentLoc["irma"] = "DressShop"
            CurrentLoc["alber"] = "WineStore"
            CurrentLoc["zimmer"] = "CityGuard"
            CurrentLoc["fran"] = "EllonaTemple"
            knowsMC["eddie"] = True
            knowsMC["becky"] = True
            knowsMC["irma"] = True
            knowsMC["alber"] = True
            knowsMC["zimmer"] = True
            knowsMC["fran"] = True
        except Exception:
            pass
        try:
            npc_schedule_sync_all()
        except Exception:
            pass

    def _audit_enter_room(room_label):
        _audit_prepare_common()
        _audit_renpy.jump(room_label)

    def audit_capture_room_actions(room_label):
        global ACTION_AUDIT_CAPTURED
        room_key = _audit_text(room_label)
        items = list(current_action_items or [])
        rows = []
        if not items:
            ACTION_AUDIT_FAILURES.append("{}: no visible current_action_items".format(room_key))
        for index, item in enumerate(items):
            caption = _audit_text(getattr(item, "caption", ""))
            action = getattr(item, "action", None)
            if not caption.strip():
                ACTION_AUDIT_FAILURES.append("{}[{}]: empty caption".format(room_key, index))
            if action is None:
                ACTION_AUDIT_FAILURES.append("{}[{}] {}: action is None".format(room_key, index, caption))
            rows.append((index, caption, _audit_action_type(action), _audit_action_target(action)))
        ACTION_AUDIT_CAPTURED += len(rows)
        ACTION_AUDIT_REPORT.append("{}: {}".format(room_key, ", ".join([row[1] for row in rows])))
        return rows

    def audit_run_current_action(room_label, index, caption, action_type, action_target):
        global ACTION_AUDIT_DISPATCHED
        if int(index) >= len(list(current_action_items or [])):
            return
        before = _audit_state_signature()
        item = list(current_action_items or [])[int(index)]
        caption = _audit_text(getattr(item, "caption", caption))
        action = getattr(item, "action", None)
        action_type = _audit_action_type(action)
        action_target = _audit_action_target(action)
        if action is None:
            ACTION_AUDIT_FAILURES.append("{}[{}] {}: action is None at dispatch".format(room_label, index, caption))
            return
        ACTION_AUDIT_DISPATCHED += 1
        _audit_renpy.run(action)
        after = _audit_state_signature()
        if before == after:
            ACTION_AUDIT_FAILURES.append("{}[{}] {}: dispatch {} {} made no visible state change".format(room_label, index, caption, action_type, action_target))

    def audit_assert_no_failures():
        if int(ACTION_AUDIT_CAPTURED or 0) <= 0:
            raise AssertionError("Action audit captured no room actions.")
        if int(ACTION_AUDIT_DISPATCHED or 0) <= 0:
            raise AssertionError("Action audit dispatched no room actions.")
        if ACTION_AUDIT_FAILURES:
            raise AssertionError("\n".join(ACTION_AUDIT_FAILURES[:80]))

testcase external_room_action_dispatch:
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
'''


ALL_ROOM_ACTION_CLICK_CHECKS = r'''
init -1 python:
    import renpy.exports as _full_click_renpy

    FULL_CLICK_ROOM = ""
    FULL_CLICK_INDEX = -1
    FULL_CLICK_BUTTON_ID = ""
    FULL_CLICK_CAPTION = ""
    FULL_CLICK_BEFORE = None
    FULL_CLICK_SKIP = False
    FULL_CLICK_SKIP_REASON = ""
    FULL_CLICK_REPORT = []

    def full_click_text(value):
        try:
            return str(value or "")
        except Exception:
            return ""

    def full_click_state_signature():
        captions = []
        try:
            captions = [full_click_text(getattr(i, "caption", "")) for i in list(current_action_items or [])]
        except Exception:
            captions = []
        overlay_screens = []
        for screen_name in (
            "dress_shop_female_catalog_overlay",
            "dress_shop_male_catalog_overlay",
            "girl_card_overlay",
            "player_card_overlay",
            "hunter_club_trade_overlay",
            "story_thread_board",
        ):
            try:
                if _full_click_renpy.get_screen(screen_name) is not None:
                    overlay_screens.append(screen_name)
            except Exception:
                pass
        return (
            full_click_text(CurLoc),
            full_click_text(current_action_title),
            full_click_text(MainTxt),
            full_click_text(CurLocDesc),
            full_click_text(_layout_last_picture),
            full_click_text(main_ui_overlay),
            full_click_text(current_girl_key),
            full_click_text(current_object_id),
            tuple(captions),
            tuple(overlay_screens),
        )

    def full_click_prepare_common():
        global week, time, hour, minute, BlockTimeAdvance, TavernEventOngoing
        global BlindPirateMarketEventSeen, main_ui_overlay, main_ui_inventory_dropdown_open
        global action_menu_specs, current_action_content, UI_mode
        global evalTime
        week = 1
        time = 1
        hour = 12
        minute = 0
        BlockTimeAdvance = 0
        TavernEventOngoing = ""
        BlindPirateMarketEventSeen = 1
        main_ui_overlay = ""
        main_ui_inventory_dropdown_open = False
        action_menu_specs = []
        current_action_content = None
        UI_mode = "scene"
        try:
            EventsCount.clear()
            NewEvents.clear()
        except Exception:
            pass
        try:
            threads.clear()
            availEvents.clear()
            evalTime = None
        except Exception:
            pass
        try:
            Friends["sandra"] = max(int(Friends.get("sandra", 0) or 0), 10)
            SandraVar["RoomUnlocked"] = 1
            BedroomDoorStates["TavernSandraRoom"] = 0
            AmandaVar["kickyoufromroom"] = 0
            CurrentLoc["eddie"] = "GroceryStore"
            CurrentLoc["becky"] = "GroceryStore"
            CurrentLoc["irma"] = "DressShop"
            CurrentLoc["alber"] = "WineStore"
            CurrentLoc["zimmer"] = "CityGuard"
            CurrentLoc["fran"] = "EllonaTemple"
            knowsMC["eddie"] = True
            knowsMC["becky"] = True
            knowsMC["irma"] = True
            knowsMC["alber"] = True
            knowsMC["zimmer"] = True
            knowsMC["fran"] = True
        except Exception:
            pass
        try:
            npc_schedule_sync_all()
        except Exception:
            pass

    def full_click_start_room(room_name, action_index):
        global FULL_CLICK_ROOM, FULL_CLICK_INDEX, FULL_CLICK_BUTTON_ID
        global FULL_CLICK_CAPTION, FULL_CLICK_BEFORE, FULL_CLICK_SKIP, FULL_CLICK_SKIP_REASON
        FULL_CLICK_ROOM = full_click_text(room_name)
        FULL_CLICK_INDEX = int(action_index)
        FULL_CLICK_BUTTON_ID = "choice_panel_button_%d" % FULL_CLICK_INDEX
        FULL_CLICK_CAPTION = ""
        FULL_CLICK_BEFORE = None
        FULL_CLICK_SKIP = False
        FULL_CLICK_SKIP_REASON = ""
        full_click_prepare_common()
        _full_click_renpy.jump(FULL_CLICK_ROOM)

    def full_click_capture_before():
        global FULL_CLICK_CAPTION, FULL_CLICK_BEFORE, FULL_CLICK_SKIP, FULL_CLICK_SKIP_REASON
        items = list(current_action_items or [])
        if FULL_CLICK_INDEX >= len(items):
            FULL_CLICK_SKIP = True
            FULL_CLICK_SKIP_REASON = "missing index"
            return
        item = items[FULL_CLICK_INDEX]
        FULL_CLICK_CAPTION = full_click_text(getattr(item, "caption", ""))
        if not FULL_CLICK_CAPTION.strip():
            raise AssertionError("{}[{}]: empty caption".format(FULL_CLICK_ROOM, FULL_CLICK_INDEX))
        if getattr(item, "action", None) is None:
            raise AssertionError("{}[{}] {}: action is None".format(FULL_CLICK_ROOM, FULL_CLICK_INDEX, FULL_CLICK_CAPTION))
        FULL_CLICK_BEFORE = full_click_state_signature()

    def full_click_has_item():
        return not bool(FULL_CLICK_SKIP)

    def full_click_changed():
        if FULL_CLICK_SKIP:
            return True
        try:
            if _full_click_renpy.get_screen("main_ui") is None:
                return True
        except Exception:
            return True
        return full_click_state_signature() != FULL_CLICK_BEFORE

    def full_click_assert_changed():
        if FULL_CLICK_SKIP:
            return
        if not full_click_changed():
            raise AssertionError("{}[{}] {}: click made no visible state change".format(FULL_CLICK_ROOM, FULL_CLICK_INDEX, FULL_CLICK_CAPTION))
        FULL_CLICK_REPORT.append("{}[{}] {}".format(FULL_CLICK_ROOM, FULL_CLICK_INDEX, FULL_CLICK_CAPTION))

testcase external_all_room_action_clicks:
    parameter (room_name, action_index) = __ROOM_ACTION_CLICK_PARAMS__
    run Function(full_click_start_room, room_name, action_index)
    advance until screen "main_ui" timeout 20.0
    $ full_click_capture_before()
    if eval full_click_has_item():
        if eval (FULL_CLICK_INDEX >= 7):
            scroll amount 2 pos (1700, 760)
        if eval (FULL_CLICK_INDEX >= 10):
            scroll amount 2 pos (1700, 760)
        if eval (FULL_CLICK_INDEX >= 13):
            scroll amount 2 pos (1700, 760)
        if eval (FULL_CLICK_INDEX >= 16):
            scroll amount 2 pos (1700, 760)
        if eval (FULL_CLICK_INDEX >= 19):
            scroll amount 2 pos (1700, 760)
        if eval (FULL_CLICK_INDEX >= 22):
            scroll amount 2 pos (1700, 760)
        click id FULL_CLICK_BUTTON_ID pos (0.5, 0.5)
        pause 0.2
        $ full_click_assert_changed()
    else:
        pass
'''


ROOM_ACTION_DISPATCH_TEMPLATE = r'''
    run Function(_audit_enter_room, "{room_name}")
    advance until screen "main_ui" timeout 20.0
    $ _audit_rows = audit_capture_room_actions("{room_name}")
    $ _audit_room_rows = list(_audit_rows)
'''


ROOM_ACTION_DISPATCH_ACTION_TEMPLATE = r'''
    run Function(_audit_enter_room, "{room_name}")
    advance until screen "main_ui" timeout 20.0
    $ audit_run_current_action("{room_name}", {index}, "", "", "")
    advance until screen "main_ui" timeout 20.0
'''


def build_test_rpy() -> str:
    room_action_click_params = [
        (room_name, action_index)
        for room_name in ROOM_LABELS
        for action_index in range(ROOM_ACTION_INDEX_LIMIT)
    ]
    room_action_sections = [ROOM_ACTION_DISPATCH_CHECKS]
    for room_name in ROOM_LABELS:
        room_action_sections.append(ROOM_ACTION_DISPATCH_TEMPLATE.format(room_name=room_name))
        for index in range(16):
            room_action_sections.append(
                ROOM_ACTION_DISPATCH_ACTION_TEMPLATE.format(room_name=room_name, index=index)
            )
    room_action_sections.append('    assert eval (int(ACTION_AUDIT_CAPTURED or 0) > 0) timeout 5.0\n')
    room_action_sections.append('    assert eval (int(ACTION_AUDIT_DISPATCHED or 0) > 0) timeout 5.0\n')
    room_action_sections.append('    $ audit_assert_no_failures()\n')
    all_room_action_click_checks = ALL_ROOM_ACTION_CLICK_CHECKS.replace(
        "__ROOM_ACTION_CLICK_PARAMS__", repr(room_action_click_params)
    )
    return TEST_HEADER + "".join(
        ROOM_CHECK_TEMPLATE.format(room_name=room_name) for room_name in ROOM_LABELS
    ) + "\n\n" + SHOP_ACTION_CHECKS + "\n\n" + DOG_ENTITY_ACTION_CHECKS + "\n\n" + ACTUAL_ACTION_BUTTON_CLICK_CHECKS + "\n\n" + ACTUAL_RANDOM_TOWN_CLICK_CHECKS + "\n\n" + all_room_action_click_checks + "\n\n" + "".join(room_action_sections)


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        remove_temp_tree(path)
    path.mkdir(parents=True, exist_ok=True)


def junction_dir(source: Path, target: Path) -> None:
    completed = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(target), str(source)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout.strip())


def hardlink_or_copy(source: Path, target: Path) -> None:
    try:
        os.link(source, target)
    except OSError:
        shutil.copy2(source, target)


def build_temp_project(root: Path, temp_root: Path) -> Path:
    source_game = root / "game"
    temp_project = temp_root / "TractirExternalClickProject"
    temp_game = temp_project / "game"
    ensure_clean_dir(temp_game)

    for entry in source_game.iterdir():
        target = temp_game / entry.name
        if entry.is_dir():
            if entry.name in {"cache", "__pycache__", "saves_test_run"}:
                continue
            junction_dir(entry, target)
        elif entry.suffix.lower() in {".rpy", ".rpym", ".py", ".json", ".png", ".jpg", ".jpeg", ".webp"}:
            hardlink_or_copy(entry, target)

    (temp_game / "_external_click_play_test.rpy").write_text(build_test_rpy(), encoding="utf-8")
    return temp_project


def is_junction(path: Path) -> bool:
    probe = getattr(path, "is_junction", None)
    if callable(probe):
        try:
            return bool(probe())
        except OSError:
            return False
    return False


def remove_temp_tree(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink() and not is_junction(path):
        for child in path.iterdir():
            remove_temp_tree(child)
        path.rmdir()
        return
    if path.is_dir():
        path.rmdir()
    else:
        path.unlink(missing_ok=True)


def run_renpy(renpy_exe: Path, temp_project: Path, timeout: int, test_name: str) -> int:
    args = [
        str(renpy_exe),
        str(temp_project),
        "test",
        test_name,
        "--hide-execution",
        "no",
        "--report-detailed",
    ]
    try:
        completed = subprocess.run(
            args,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if completed.stdout:
            safe_print(completed.stdout)
        return int(completed.returncode or 0)
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        if output:
            safe_print(output)
        print(f"Ren'Py test timed out after {timeout} seconds.")
        return 124


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--renpy",
        default=r"C:\Users\blank\renpy\renpy-8.5.2-sdk\renpy.exe",
        help="Path to renpy.exe.",
    )
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument(
        "--only",
        action="append",
        choices=[
            "external_room_clock_clicks",
            "external_shop_action_logic",
            "external_dog_entity_actions",
            "external_actual_grocery_click",
            "external_actual_wine_click",
            "external_actual_market_click",
            "external_actual_random_town_continue_click",
            "external_actual_random_town_click",
            "external_all_room_action_clicks",
            "external_room_action_dispatch",
        ],
        help="Run only the named Ren'Py testcase. Can be passed more than once.",
    )
    args = parser.parse_args()

    root = project_root()
    renpy_exe = Path(args.renpy)
    if not renpy_exe.exists():
        raise SystemExit(f"Ren'Py executable not found: {renpy_exe}")

    temp_root = Path(tempfile.mkdtemp(prefix="tractir_click_play_"))
    try:
        temp_project = build_temp_project(root, temp_root)
        print(f"Temporary test project: {temp_project}")
        print(f"Rooms under click-clock test: {len(ROOM_LABELS)}")
        result = 0
        test_names = args.only or [
            "external_room_clock_clicks",
            "external_shop_action_logic",
            "external_dog_entity_actions",
            "external_actual_grocery_click",
            "external_actual_wine_click",
            "external_actual_market_click",
            "external_actual_random_town_continue_click",
            "external_actual_random_town_click",
            "external_all_room_action_clicks",
            "external_room_action_dispatch",
        ]
        for test_name in test_names:
            result = max(result, run_renpy(renpy_exe, temp_project, args.timeout, test_name))
        return result
    finally:
        if args.keep_temp:
            print(f"Keeping temporary test project: {temp_root}")
        else:
            remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
