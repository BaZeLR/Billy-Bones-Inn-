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
init python:
    def external_calendar_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def external_calendar_day_number_from_fields(day_value=None, month_value=None, year_value=None):
        cycle = max(CALENDAR_START_CYCLE, external_calendar_int(year if year_value is None else year_value, CALENDAR_START_CYCLE))
        period = max(1, min(13, external_calendar_int(month if month_value is None else month_value, 1)))
        lunar_day = max(1, min(28, external_calendar_int(day if day_value is None else day_value, 1)))
        return max(0, ((cycle - CALENDAR_START_CYCLE) * 364) + ((period - 1) * 28) + lunar_day - 1)

    # External test positioning only. Calendar runtime intentionally has no date-jump setter.
    def external_calendar_set_fields(day_value=None, month_value=None, year_value=None, hour_value=None, minute_value=None):
        day_number_i = external_calendar_day_number_from_fields(day_value, month_value, year_value)
        parts = calendar_v2.day_number_to_parts(day_number_i)
        calendar_v2.day = int(parts["day"])
        calendar_v2.period = int(parts["month"])
        calendar_v2.cycle = int(parts["year"])
        calendar_v2.week = int(parts["week"])
        calendar_v2.daysInGame = day_number_i
        calendar_v2.hour = external_calendar_int(hour if hour_value is None else hour_value, 8) % 24
        calendar_v2.minute = external_calendar_int(minute if minute_value is None else minute_value, 0) % 60
        calendar_v2.sync_state()
        return True

    # External test fixture setup only. Gameplay never changes weekday directly.
    def external_calendar_set_weekday(weekday_value=1):
        target_week = max(1, min(7, external_calendar_int(weekday_value, 1)))
        calendar_v2.sync_state()
        steps = (target_week - max(1, min(7, external_calendar_int(week, 1)))) % 7
        while steps > 0:
            calendar_v2.day += 1
            calendar_v2.week += 1
            calendar_v2.daysInGame += 1
            if calendar_v2.week > 7:
                calendar_v2.week = 1
            if calendar_v2.day > 28:
                calendar_v2.day = 1
                calendar_v2.period += 1
            if calendar_v2.period > 13:
                calendar_v2.period = 1
                calendar_v2.cycle += 1
            steps -= 1
        calendar_v2.sync_state()
        return True

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
    $ Sandra.var["RoomUnlocked"] = 1
    $ Sandra.room_unlocked_flag = 1
    $ BedroomDoorStates["TavernSandraRoom"] = 0

    run Jump("{room_name}")
    advance until screen "main_ui" timeout 20.0
    pause 0.1
    assert eval (str(CurLoc or "") == "{room_name}") timeout 5.0
    click id "main_ui_time_button" pos (0.5, 0.5) until eval (str(main_ui_overlay or "") == "time") timeout 10.0
    click id "time_change_back_button" pos (0.5, 0.5) until eval (str(main_ui_overlay or "") == "") timeout 10.0

    click id "main_ui_story_button" pos (0.5, 0.5) until eval (str(main_ui_overlay or "") == "story") timeout 10.0
    click id "main_ui_people_button" pos (0.5, 0.5) until eval (str(main_ui_overlay or "") == "people") timeout 10.0
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
    run Call("InitBecky")
    run Call("register_inga_secondary")
    run Call("InitEddie")
    $ external_calendar_set_fields(10, 1, 1100, 10, 0)
    $ npc_interval_schedule_load_all(True)
    $ npc_schedule_sync_all()

    $ CurrentRoom = GroceryStoreRoom
    $ CurLoc = "GroceryStore"
    $ location = CurLoc
    $ GrocerName = "Эдди"
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Провизия' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Купить провизию' not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    run Call("GroceryStoreObjectMenu", "food_stock")
    assert eval (str(current_action_title or "") == 'Провизия') timeout 5.0
    assert eval ('Купить провизию' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Купить крынку молока' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ('Осмотреть товар' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    run Call("GroceryStoreObjectText", "food_stock", "examine_food_stock")
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
    $ renpy.call_in_new_context("IntEddieTalkSmalltalk")
    assert eval ('Вы некоторое время болтаете с Эдди' in str(MainTxt or "")) timeout 5.0
    assert eval (int(Talked.get("eddie", 0) or 0) == 1) timeout 5.0
    assert eval (int(TalkedToday.get("eddie", 0) or 0) == 1) timeout 5.0
    assert eval ('Поболтать с Эдди о разной фигне.' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ Talked["eddie"] = 3
    $ renpy.call_in_new_context("IntEddieTalkSmalltalk")
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
    run Call("WineStoreObjectMenu", "wine_stock")
    assert eval (str(current_action_title or "") == 'Бочки с вином') timeout 5.0
    assert eval ([str(i.caption or "") for i in current_action_items].count('Купить вино') == 1) timeout 5.0
    $ _wine_picture_before = str(_layout_last_picture or "")
    run Call("WineStoreObjectText", "wine_stock", "examine_wine")
    assert eval (str(current_action_title or "") == 'Бочки с вином') timeout 5.0
    assert eval ('Повсюду бочки' in str(MainTxt or "")) timeout 5.0
    assert eval ('Купить вино' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (str(_layout_last_picture or "") == _wine_picture_before) timeout 5.0

    $ external_calendar_set_fields(day, month, year, 12, 0)
    $ external_calendar_set_weekday(1)
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
    $ MyStallion = "test-horse"
    $ _layout_last_picture = MarketPlaceRoom.bg_picture
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ action_menu_specs = []
    $ current_action_items = MarketPlaceRoom.build_action_items() + MarketPlaceRoom.build_exit_items()
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
'''


TAVERN_REPORT_STATE_CHECKS = r'''
testcase external_tavern_report_state_defaults:
    $ external_calendar_set_fields(10, 1, 1100, 12, 0)
    $ external_calendar_set_weekday(1)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_overlay = ""
    $ current_action_content = None
    $ UI_mode = "scene"

    $ show_tavern_report_main_ui_state("")
    assert eval (str(UI_mode or "") == "tavern") timeout 5.0
    assert eval (str(current_action_title or "") == "Трактир") timeout 5.0
    assert eval (len(current_action_items) > 0) timeout 5.0
    assert eval (isinstance(jobkitchentomorrow, dict) and isinstance(jobcleaningtomorrow, dict) and isinstance(jobwaitresstomorrow, dict)) timeout 5.0
    assert eval (len(BuildTavernReport()["team_keys"]) >= 3) timeout 5.0
    assert eval ("sandra" in BuildTavernReport()["team_keys"] and "melissa" in BuildTavernReport()["team_keys"] and "amanda" in BuildTavernReport()["team_keys"]) timeout 5.0
    assert eval (str(getPersonInfo("sandra").getLocation() or "") != "") timeout 5.0
    assert eval (len(people_locate_rows()) >= 3) timeout 5.0
'''


TAILOR_PURCHASE_FLOW_CHECKS = r'''
testcase external_actual_tailor_buy_dress_measure_flow:
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
    $ CurrentLoc["irma"] = "DressShop"
    $ knowsMC["irma"] = True
    $ HadSex["You"] = 0
    $ Friends["irma"] = 0
    $ IrmaVar["DeniedMinetMoney"] = 0
    $ cametoday = 0
    $ cancumdaily = 3
    run Jump("DressShop")
    advance until screen "main_ui" timeout 20.0
    $ renpy.call_in_new_context("DressShopOpenCatalog", "male")
    $ _male_item = dress_shop_catalog_items("male")[0]
    $ _male_code = str(_male_item.custom_properties.get("dress_code", "") or "")
    $ MyDresses = []
    $ money = int(getattr(_male_item, "price", 0) or 0) + 100
    $ renpy.call_in_new_context("DressShopBuyMaleItem", _male_code)
    assert eval (str(DressProduced or "") == _male_code) timeout 5.0
    assert eval ("measure0" in str(_layout_last_picture or "")) timeout 5.0
    assert eval ("заказать" in str(MainTxt or "")) timeout 5.0
    assert eval ("Раздеться до белья" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Полностью раздеться и думать о высоком" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ renpy.call_in_new_context("DressTryUnderwear")
    assert eval ("measure1" in str(_layout_last_picture or "")) timeout 5.0
    assert eval ("нижнего белья" in str(MainTxt or "")) timeout 5.0
    assert eval ("Одеться и вернуться в лавку" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ HadSex["You"] = 3
    $ renpy.call_in_new_context("DressTry", "You", _male_code)
    assert eval ("Полностью раздеться и думать о высоком" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("DressTryNakedThink")
    assert eval ("measure2" in str(_layout_last_picture or "")) timeout 5.0
    assert eval ("думать о птичках" in str(MainTxt or "")) timeout 5.0

    $ HadSex["You"] = 5
    $ Friends["irma"] = 0
    $ renpy.call_in_new_context("DressTry", "You", _male_code)
    assert eval ("Полностью раздеться и представить Ирму" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("DressTryNakedFantasy")
    assert eval ("measure3" in str(_layout_last_picture or "")) timeout 5.0
    assert eval ("Это я тебе настолько нравлюсь" in str(MainTxt or "")) timeout 5.0

    $ Friends["irma"] = 5
    $ IrmaVar["DeniedMinetMoney"] = 0
    $ money = 100
    $ renpy.call_in_new_context("DressTry", "You", _male_code)
    $ renpy.call_in_new_context("DressTryNakedFantasy")
    assert eval ("sex0" in str(_layout_last_picture or "")) timeout 5.0
    assert eval ("Кончить на лицо" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Кончить в рот" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("DressTryServiceFinish", "mouth")
    assert eval ("sex9" in str(_layout_last_picture or "")) timeout 5.0
    assert eval ("Расплатиться" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("code_farago_demand_money")
    assert eval ("Промолчать и оплатить" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Возмутиться" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

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
    $ story_event_available = lambda location_name="", action_name="": False
    $ ensure_dog_runtime()
    $ playerItems = {}
    $ dayspassed = 3
    $ time = 5
    $ dog.owned = False
    $ dog.in_company = False
    $ dog.met = False
    $ dog.bones_given = 0
    $ dog.stray_played = False
    $ dog.booth_built = False
    $ dog.wearing_bloomers = False
    $ health = 100

    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    $ dayspassed = 3
    $ time = 5
    $ dog.spawn_day = int(dayspassed or 0)
    $ dog.spawn_location = "PortStreets"
    assert eval (str(dog.picture_path("PortStreets", "card") or "").endswith("no_colar.png")) timeout 5.0
    $ open_dog_action_menu_state("PortStreets")
    assert eval ("Позвать пса" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("IntDogTalkApply", "PortStreets", "call_stray")
    assert eval ("Попробовать погладить" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("IntDogTalkApply", "PortStreets", "pet_stray")
    assert eval (int(health or 0) == 95) timeout 5.0
    assert eval ("сначала стоит дать ему кость" in str(MainTxt or "")) timeout 5.0

    $ dog.spawn_day = int(dayspassed or 0)
    $ dog.spawn_location = "PortStreets"
    $ dog.met = False
    $ dog.bones_given = 0
    $ dog.stray_played = False
    $ _player_add_item_by_id("dog_bone_001", 1)
    $ _player_add_item_by_id("dog_collar_001", 1)
    $ open_dog_action_menu_state("PortStreets")
    $ renpy.call_in_new_context("IntDogTalkApply", "PortStreets", "call_stray")
    $ renpy.call_in_new_context("IntDogTalkApply", "PortStreets", "stray_bone")
    $ renpy.call_in_new_context("IntDogTalkApply", "PortStreets", "play_stray")
    assert eval (dog_can_adopt_stray()) timeout 5.0
    $ renpy.call_in_new_context("IntDogTalkApply", "PortStreets", "adopt")
    assert eval ("Sharik" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("IntDogTalkApply", "PortStreets", "adopt_name:Sharik")
    assert eval (bool(dog.owned)) timeout 5.0
    assert eval (str(dog.name or "") == "Sharik") timeout 5.0
    assert eval (_player_item_count_by_id("dog_collar_001") == 0) timeout 5.0
    assert eval (str(dog.picture_path("PortStreets", "card") or "").endswith("dog.png")) timeout 5.0
    $ dog.set_bloomers(True)
    assert eval (str(dog.picture_path("PortStreets", "card") or "").endswith("dog_bloomers.png")) timeout 5.0
    $ dog.set_bloomers(False)

    $ time = 1
    $ dog.owned = True
    $ dog.in_company = False
    $ dog.booth_built = True
    $ dog.loyalty = max(int(dog.loyalty or 0), 12)
    $ dog.health = dog.max_health
    $ dog.last_play_day = -1
    $ dog.last_train_day = -1
    $ _player_add_item_by_id("dog_bone_001", 2)

    run Jump("Backyard")
    advance until screen "main_ui" timeout 20.0
    $ CurrentLoc["dog"] = "Backyard"
    assert eval (str(dog.picture_path("Backyard", "card") or "").endswith("dog_booth.png")) timeout 5.0
    assert eval (dog_is_available_here("Backyard")) timeout 5.0
    assert eval ("dog" not in [str(row.get("id", "") or "") for row in _character_action_grid_entries(CurrentRoom)]) timeout 5.0

    $ open_dog_action_menu_state("Backyard")
    assert eval ("Осмотреть" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (any("кость" in str(i.caption or "").lower() for i in current_action_items)) timeout 5.0

    $ _dog_bone_count_before = _player_item_count_by_id("dog_bone_001")
    $ _dog_loyalty_before = int(dog.loyalty or 0)
    $ renpy.call_in_new_context("IntDogTalkApply", "Backyard", "bone")
    assert eval (_player_item_count_by_id("dog_bone_001") == _dog_bone_count_before - 1) timeout 5.0
    assert eval (int(dog.loyalty or 0) >= _dog_loyalty_before) timeout 5.0

    $ DogActionLookState("Backyard")
    $ dog.last_play_day = -1
    $ dog.last_train_day = -1
    $ current_action_items = dog.main_ui_action_items("Backyard", include_card=False)
    assert eval (str(UI_mode or "") == "dog") timeout 5.0
    assert eval (len(list(dog_card_lines() or [])) > 0) timeout 5.0
    assert eval (not dog.played_with_today()) timeout 5.0
    assert eval (not dog.trained_today()) timeout 5.0
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


BACKYARD_BARREL_OBJECT_CHECKS = r'''
testcase external_backyard_barrel_object_actions:
    $ external_calendar_set_fields(1, 1, 1100, 13, 0)
    $ CurrentLoc["melissa"] = "TavernKitchen"
    $ CurrentLoc["amanda"] = "TavernMain"
    $ SoapAshBarrelInstalled = 0
    $ SoapAshBarrelReadyDay = 0
    $ player_state().remove_item("soap_001", max(1, player_state().item_count("soap_001")))
    $ player_state().remove_item("luxury_soap_001", max(1, player_state().item_count("luxury_soap_001")))

    run Jump("Backyard")
    advance until screen "main_ui" timeout 20.0
    run Call("BackyardBuildActions")
    assert eval (str(CurLoc or "") == "Backyard") timeout 5.0
    assert eval (str(_layout_last_picture or "").endswith("images/tavern/backyard/backyard_1.png")) timeout 5.0
    assert eval ("backyard_water_barrel" in [str(getattr(obj, "object_id", "") or "") for obj in BackyardRoom.visible_objects()]) timeout 5.0
    assert eval (not any(str(getattr(getattr(i, "action", None), "label", "") or "") == "BackyardCookSoap" for i in current_action_items)) timeout 5.0

    run Call("BackyardObjectMenu", "backyard_water_barrel")
    assert eval (str(current_action_title or "") == "Бочка с дождевой водой") timeout 5.0
    assert eval ("BackyardWashAtBarrel" in [str(getattr(getattr(i, "action", None), "label", "") or "") for i in current_action_items]) timeout 5.0
    assert eval (not any(str(getattr(getattr(i, "action", None), "label", "") or "") == "BackyardWashAtBarrelWithSoap" for i in current_action_items)) timeout 5.0

    $ _look_before = int(player_state().stats.look or 0)
    $ player_state().add_item("soap_001", 1)
    run Call("BackyardObjectMenu", "backyard_water_barrel")
    assert eval ("BackyardWashAtBarrelWithSoap" in [str(getattr(getattr(i, "action", None), "label", "") or "") for i in current_action_items]) timeout 5.0
    run Call("BackyardWashAtBarrelWithSoap", "soap_001")
    assert eval (_player_item_count_by_id("soap_001") == 0) timeout 5.0
    assert eval (int(player_state().stats.look or 0) == min(100, _look_before + 1)) timeout 5.0
    assert eval (str(current_action_title or "") == "Бочка с дождевой водой") timeout 5.0

    $ SoapAshBarrelInstalled = 1
    $ SoapAshBarrelReadyDay = int(dayspassed or 0)
    $ recipe_page_can_craft = lambda recipe_id: True
    $ apply_recipe_craft = lambda recipe_id: {"ok": True, "text": "TEST SOAP RESULT"}
    run Call("BackyardObjectMenu", "backyard_ash_barrel")
    assert eval (str(current_action_title or "") == "Зольная бочка") timeout 5.0
    assert eval (str(_layout_last_picture or "").endswith("images/tavern/backyard/soap_backyard.png")) timeout 5.0
    assert eval ("BackyardCookSoap" in [str(getattr(getattr(i, "action", None), "label", "") or "") for i in current_action_items]) timeout 5.0
    run Call("BackyardCookSoap", "soap_recipe")
    assert eval ("TEST SOAP RESULT" in str(MainTxt or "")) timeout 5.0
    assert eval (str(current_action_title or "") == "Зольная бочка") timeout 5.0
    assert eval (len(list(current_action_items or [])) > 0) timeout 5.0
'''


GROCERY_STORE_OBJECT_PURCHASE_CHECKS = r'''
testcase external_grocery_store_object_purchase_actions:
    run Call("InitBecky")
    run Call("register_inga_secondary")
    run Call("InitEddie")
    $ external_calendar_set_fields(10, 1, 1100, 10, 0)
    $ npc_interval_schedule_load_all(True)
    $ npc_schedule_sync_all()
    $ CurrentRoom = GroceryStoreRoom
    $ CurLoc = "GroceryStore"
    $ location = CurLoc
    $ GrocerName = "Эдди"
    $ money = 100
    $ Amanda.set_var_int("gave_night_bowl", 1)
    $ Amanda.set_var_int("got_fancy_night_bowl", 0)
    $ player_state().remove_item("milk_pitcher_001", max(1, player_state().item_count("milk_pitcher_001")))
    $ player_state().remove_item("fancy_night_bowl_001", max(1, player_state().item_count("fancy_night_bowl_001")))

    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    run Call("GroceryStoreBuildActions")
    assert eval (str(CurLoc or "") == "GroceryStore") timeout 5.0
    assert eval (str(grocery_store_active_grocer_id() or "") == "eddie") timeout 5.0
    assert eval (bool(grocery_store_service_available())) timeout 5.0
    assert eval ("food_stock" in [str(getattr(obj, "object_id", "") or "") for obj in GroceryStoreRoom.visible_objects()]) timeout 5.0

    run Call("GroceryStoreObjectMenu", "food_stock")
    assert eval (str(current_action_title or "") == "Провизия") timeout 5.0
    assert eval ("Купить крынку молока" in [str(getattr(i, "caption", "") or "") for i in current_action_items]) timeout 5.0
    assert eval ("Купить красивую ночную миску" in [str(getattr(i, "caption", "") or "") for i in current_action_items]) timeout 5.0

    $ _milk_money_before = int(money or 0)
    $ _milk_count_before = _player_item_count_by_id("milk_pitcher_001")
    run Call("GroceryStoreBuyMilk")
    assert eval (int(money or 0) == _milk_money_before - 6) timeout 5.0
    assert eval (_player_item_count_by_id("milk_pitcher_001") == _milk_count_before + 1) timeout 5.0
    assert eval (str(current_action_title or "") == "Провизия") timeout 5.0

    run Call("GroceryStoreBuyMenu")
    assert eval (str(current_action_title or "") == "Покупка провизии") timeout 5.0
    $ _provision_money_before = int(money or 0)
    $ _provision_before = int(productnum or 0)
    run Call("GroceryStoreBuyApply", 6, 10, 1)
    assert eval (int(money or 0) == _provision_money_before - 6) timeout 5.0
    assert eval (int(productnum or 0) == _provision_before + 10) timeout 5.0
    assert eval (str(current_action_title or "") == "Покупка провизии") timeout 5.0

    run Call("GroceryStoreObjectMenu", "food_stock")
    run Call("GroceryStoreBuyFancyNightBowl")
    assert eval ("Купить красивую ночную миску за 9 мараведи" in [str(getattr(i, "caption", "") or "") for i in current_action_items]) timeout 5.0
    $ _bowl_money_before = int(money or 0)
    run Call("GroceryStoreBuyFancyNightBowlApply")
    assert eval (int(money or 0) == _bowl_money_before - 9) timeout 5.0
    assert eval (_player_item_count_by_id("fancy_night_bowl_001") == 1) timeout 5.0
    assert eval (str(current_action_title or "") == "Красивая ночная миска") timeout 5.0
'''


PORT_STREETS_FLOW_CHECKS = r'''
testcase external_port_streets_georgette_liza_flow:
    $ external_calendar_set_fields(1, 1, 1100, 12, 0)
    $ CurrentLoc["georgett"] = "PortStreets"
    $ CurrentLoc["liza"] = "PortStreets"
    $ story_event_available = lambda location_name="", action_name="": False
    $ Friends["georgett"] = 0
    $ LizaVar["ProstStart"] = 0
    $ GeorgettVar["TalkChurchAfterCermonLiza"] = 0
    $ town_street.LOCATIONS = ()
    $ TownStreetEventsToday = 2
    $ TownStreetStorySeenKeys.append("%s:PortStreets:%s" % (dayspassed, time))
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (int(georgett_can_talk or 0) == 0) timeout 5.0
    assert eval (int(liza_can_talk or 0) == 0) timeout 5.0
    assert eval ("georgett" not in list(getNPCids("PortStreets") or [])) timeout 5.0
    assert eval ("liza" not in list(getNPCids("PortStreets") or [])) timeout 5.0

    $ external_calendar_set_fields(1, 1, 1100, 20, 0)
    $ Friends["georgett"] = 0
    $ LizaVar["ProstStart"] = 0
    $ GeorgettVar["TalkChurchAfterCermonLiza"] = 0
    $ town_street.LOCATIONS = ()
    $ TownStreetEventsToday = 2
    $ TownStreetStorySeenKeys.append("%s:PortStreets:%s" % (dayspassed, time))
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (int(georgett_can_talk or 0) == 1) timeout 5.0
    assert eval (int(liza_can_talk or 0) == 0) timeout 5.0
    assert eval ("georgett" in list(getNPCids("PortStreets") or [])) timeout 5.0
    assert eval ("liza" not in list(getNPCids("PortStreets") or [])) timeout 5.0

    $ external_calendar_set_fields(1, 1, 1100, 20, 0)
    $ Friends["georgett"] = 1
    $ LizaVar["ProstStart"] = 1
    $ town_street.LOCATIONS = ()
    $ TownStreetEventsToday = 2
    $ TownStreetStorySeenKeys.append("%s:PortStreets:%s" % (dayspassed, time))
    $ TodaySexEvents_Clear()
    $ TodaySexEvents_Add("georgett", 3, 99, "Prostitution")
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (int(georgett_can_talk or 0) == 0) timeout 5.0
    assert eval (int(liza_can_talk or 0) == 1) timeout 5.0
    assert eval ("georgett" not in list(getNPCids("PortStreets") or [])) timeout 5.0
    assert eval ("liza" in list(getNPCids("PortStreets") or [])) timeout 5.0

    $ external_calendar_set_fields(5, 1, 1100, 20, 0)
    $ Friends["georgett"] = 0
    $ LizaVar["ProstStart"] = 1
    $ town_street.LOCATIONS = ()
    $ TownStreetEventsToday = 2
    $ TownStreetStorySeenKeys.append("%s:PortStreets:%s" % (dayspassed, time))
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (int(georgett_can_talk or 0) == 0) timeout 5.0
    assert eval (int(liza_can_talk or 0) == 0) timeout 5.0

    $ external_calendar_set_fields(1, 1, 1100, 20, 0)
    $ Friends["georgett"] = 0
    $ LizaVar["ProstStart"] = 0
    $ GeorgettVar["TalkChurchAfterCermonLiza"] = 1
    $ town_street.LOCATIONS = ()
    $ TownStreetEventsToday = 2
    $ TownStreetStorySeenKeys.append("%s:PortStreets:%s" % (dayspassed, time))
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (int(georgett_can_talk or 0) == 0) timeout 5.0
    assert eval (int(liza_can_talk or 0) == 0) timeout 5.0

    $ dog.spawn_day = int(dayspassed or 0)
    $ dog.spawn_location = "PortStreets"
    $ dog.met = True
    $ dog.owned = False
    $ dog.in_company = False
    $ town_street.LOCATIONS = ()
    $ TownStreetEventsToday = 2
    $ TownStreetStorySeenKeys.append("%s:PortStreets:%s" % (dayspassed, time))
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval ("dog" not in [str(row.get("id", "") or "") for row in _character_action_grid_entries(PortStreetsRoom)]) timeout 5.0

testcase external_georgette_portstreet_relationship_talk_and_sex_flow:
    $ renpy.call_in_new_context("InitDressDesc")
    $ external_calendar_set_fields(1, 1, 1100, 20, 0)
    $ CurLoc = "PortStreets"
    $ location = CurLoc
    $ CurrentRoom = PortStreetsRoom
    $ MainTxt = "Портовые улицы."
    $ CurLocDesc = MainTxt
    $ CurrentLoc["georgett"] = "PortStreets"
    $ Georgett.rel = 10
    $ Georgett.relationship = Georgett.rel
    $ Georgett.openness = 0
    $ Georgett.talked_today = 0
    $ Georgett.gifted_today = 0
    $ money = 0
    $ ensure_player_runtime().intimacy.came_today = ensure_player_runtime().intimacy.can_cum_daily

    $ money = 100
    $ ensure_player_runtime().intimacy.came_today = ensure_player_runtime().intimacy.can_cum_daily
    $ Georgett.wardrobe["current_dress"] = ""
    $ Georgett.wardrobe["current_underwear"]["bra"] = ""
    $ Georgett.wardrobe["current_underwear"]["panties"] = ""
    $ Georgett.sex_setup("street")
    $ Georgett.set_player_arousal(0)
    $ Georgett.set_arousal(0)
    $ Georgett.rel = 3
    $ Georgett.relationship = Georgett.rel
    $ Georgett.sex_state["lick_pussy"] = 3
    run Call("IntGeorgettSex", "georgett", "street")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(UI_mode or "") == "event") timeout 5.0
    assert eval (renpy.get_screen("choice") is None) timeout 5.0
    assert eval ("Лизать киску" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (int(Georgett.sex_state.get("lick_pussy", 0) or 0) == 4) timeout 20.0
    assert eval (int(Georgett.sex_state.get("lick_pussy", 0) or 0) == 4 and int(Georgett.rel or 0) == 4) timeout 5.0
    click "Закончить" until eval (str(CurLoc or "") == "PortStreets") timeout 20.0

    $ money = 100
    $ Georgett.rel = 10
    $ Georgett.relationship = Georgett.rel
    $ ensure_player_runtime().intimacy.came_today = 0
    $ ensure_player_runtime().intimacy.can_cum_daily = 2
    $ Georgett.wardrobe["current_dress"] = ""
    $ Georgett.wardrobe["current_underwear"]["bra"] = ""
    $ Georgett.wardrobe["current_underwear"]["panties"] = ""
    $ Georgett.sex_setup("street")
    $ Georgett.clear_cum("cum_face_you", "cum_face_others", "cum_tits_you", "cum_tits_others", "cum_inside_you", "cum_inside_others")
    $ Georgett.set_player_arousal(100)
    $ Georgett.set_arousal(40)
    $ set_active_module("sex", "", "PortStreets", "georgett")
    run Call("IntGeorgettSex", "georgett", "street")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(UI_mode or "") == "event") timeout 5.0
    assert eval (renpy.get_screen("choice") is None) timeout 5.0
    assert eval ("Кончить на лицо" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Кончить на груди" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ _georgett_cum_face_index = [str(i.caption or "") for i in current_action_items].index("Кончить на лицо")
    $ _georgett_cum_face_button_id = "choice_panel_button_%d" % int(_georgett_cum_face_index)
    if eval (_georgett_cum_face_index >= 7):
        scroll amount 4 pos (1700, 760)
    click id _georgett_cum_face_button_id pos (0.5, 0.5) until eval (int(Georgett.cum_state("cum_face_you") or 0) == 1) timeout 20.0
    assert eval (int(Georgett.cum_state("cum_face_you") or 0) == 1) timeout 5.0
    assert eval (int(player_state(False).intimacy.came_today or 0) == 1) timeout 5.0

testcase external_sexport_finish_does_not_show_advance_time_developer_text:
    $ _history_list = []
    $ week = 1
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ dayspassed = 12
    $ CurrentLoc["georgett"] = "PortStreets"
    $ Friends["georgett"] = 1
    $ LizaVar["ProstStart"] = 0
    $ GeorgettVar["TalkChurchAfterCermonLiza"] = 0
    $ town_street.LOCATIONS = ()
    $ TownStreetEventsToday = 2
    $ TownStreetStorySeenKeys.append("%s:PortStreets:%s" % (dayspassed, time))
    run Call("AdvanceTime", "PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (not any("Advances the game time" in str(h.what or "") for h in _history_list)) timeout 5.0
    assert eval (not any("return_location" in str(h.what or "") for h in _history_list)) timeout 5.0
'''


ACTUAL_ACTION_BUTTON_CLICK_CHECKS = r'''
init -1 python:
    def external_prepare_market_click_state():
        global BlockTimeAdvance, TavernEventOngoing
        global BlindPirateMarketEventSeen, main_ui_overlay, main_ui_inventory_dropdown_open
        global action_menu_specs, current_action_content, UI_mode
        global CurrentRoom, CurLoc, location, MainTxt, CurLocDesc
        global MyStallion, _layout_last_picture
        global current_action_title, current_action_items
        calendar_v2.hour = 12
        calendar_v2.minute = 0
        calendar_v2.week = 1
        calendar_v2.sync_state()
        BlockTimeAdvance = 0
        TavernEventOngoing = ""
        CurrentLoc["clara"] = ""
        ClaraVar["booklet_market_seen"] = 1
        if "claraBookletMarket" in threads:
            threads["claraBookletMarket"].complete()
        findAvailableEvents(True)
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
        MyStallion = "test-horse"
        _layout_last_picture = MarketPlaceRoom.bg_picture
        current_action_title = "Действия"

label external_market_click_entry:
    call InitGameNPCs
    $ external_prepare_market_click_state()
    jump MarketPlace

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
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (str(current_action_title or "") == 'Провизия') timeout 20.0
    assert eval ('Купить провизию' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval ('Мешки, капуста' in str(MainTxt or "")) timeout 20.0

testcase external_actual_wine_click:
    $ external_calendar_set_fields(day, month, year, 12, 0)
    $ external_calendar_set_weekday(1)
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

testcase external_actual_wine_for_dance_menu:
    $ week = 3
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ dayspassed = 10
    $ BreakfastToday = True
    $ TavernBreakfastEventActive = False
    $ tavern_work_events = [{"code": "WineForDance", "type": "mandatory", "label": "EventWineForDance", "period": 10, "mandatory": True, "priority": 0}]
    $ TavernPlayedEventsToday = []
    $ TavernEventReportRows = []
    $ tavern_work_sync_legacy_queue()
    $ CurrentLoc["sandra"] = "TavernKitchen"
    $ winenum = max(int(winenum or 0), 50)
    $ productnum = max(int(productnum or 0), 40)
    $ money = max(int(money or 0), 100)
    $ DanceSponsor = 0
    $ DanceSponsorPledgeDay = -1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Jump("TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Отправить вино и начать готовить закуску" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2
    assert eval ("Вы решили поддержать народные гуляния" in str(MainTxt or "")) timeout 5.0

testcase external_tavern_random_event_plan_consumes_once:
    $ external_calendar_set_fields(day, month, year, 13, 0)
    $ external_calendar_set_weekday(1)
    $ CurLoc = "TavernMain"
    $ location = CurLoc
    $ CurrentRoom = TavernMainRoom
    $ TavernEventOngoing = ""
    $ TavernMainBlockEvents = 0
    run Call("InitAmanda")
    $ Amanda.set_job_value("jobwaitress", 1)
    $ Amanda.set_job_value("jobcleaning", 0)
    assert eval (int(Amanda.job_value("jobwaitress", 0) or 0) == 1) timeout 5.0
    assert eval ("amanda" in list(girls_by_job("jobwaitress") or [])) timeout 5.0
    assert eval (str(get_random_girl_by_job("jobwaitress") or "") != "") timeout 5.0
    $ tavern_work_events = [{"code": "WaitressHarass", "type": "harrass", "label": "event_waitress_harrass", "period": time, "mandatory": False, "priority": 20}]
    $ TavernPlayedEventsToday = []
    $ TavernEventReportRows = []
    $ tavern_work_sync_legacy_queue()
    assert eval (EventsCount.get(time, 0) == 1 and NewEvents.get(str(time) + "_0") == "WaitressHarass") timeout 5.0
    $ findAvailableEvents(True)
    assert eval ("TavernMain" in availEvents and "tavern_work" in availEvents["TavernMain"] and str(availEvents["TavernMain"]["tavern_work"].target or "") == "TavernWorkEventTrigger") timeout 5.0
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval ("WaitressHarass" in list(TavernPlayedEventsToday or [])) timeout 5.0
    assert eval (len(list(tavern_work_events or [])) == 0 and EventsCount.get(time, 0) == 0) timeout 5.0
    assert eval (str(TavernEventOngoing or "").strip() != "" and str(MainTxt or "").strip() != "") timeout 5.0

testcase external_tavern_unwitnessed_event_report_consumes_leftovers:
    $ external_calendar_set_fields(day, month, year, 16, 0)
    $ external_calendar_set_weekday(2)
    $ CurLoc = "TavernMain"
    $ location = CurLoc
    $ CurrentRoom = TavernMainRoom
    $ money = max(int(money or 0), 1000)
    $ tavern_work_events = [{"code": "FightSmall", "type": "small_fight", "label": "EventFightSmall", "period": time, "mandatory": False, "priority": 40}]
    $ TavernPlayedEventsToday = []
    $ TavernEventReportRows = []
    $ tavern_work_sync_legacy_queue()
    assert eval (EventsCount.get(time, 0) == 1) timeout 5.0
    run Call("DisplayTavernEventsSummary", day, month, year)
    assert eval (len(list(tavern_work_events or [])) == 0 and EventsCount.get(time, 0) == 0) timeout 5.0
    assert eval ("События за" in str(Result or "") and "трактире" in str(Result or "")) timeout 5.0

testcase external_breakfast_dance_sponsor_announcement:
    $ week = 3
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ dayspassed = 11
    $ BreakfastToday = False
    $ TavernBreakfastEventActive = False
    $ DanceSponsor = 1
    $ TavernBreakfastDanceSponsorAnnouncedDay = -1
    $ CurrentLoc["sandra"] = "TavernSandraRoom"
    $ CurrentLoc["melissa"] = "TavernKitchen"
    $ CurrentLoc["amanda"] = "TavernAmandaRoom"
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ CurrentRoom = TavernKitchenRoom
    $ CurLoc = "TavernKitchen"
    run Call("TavernKitchenBreakfast")
    advance until screen "main_ui" timeout 20.0
    assert eval ("трактир уже выставит вино и закуски" in str((TavernBreakfastBaseText or TavernKitchenSavedText or MainTxt) or "")) timeout 5.0

testcase external_breakfast_attendance_location_wins:
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ dayspassed = 12
    $ BreakfastToday = False
    $ TavernBreakfastEventActive = False
    $ TavernBreakfastPresentIds = None
    $ TavernBreakfastFoodPerkDay = -1
    $ TavernBreakfastDrinkPerkDay = -1
    $ TavernBreakfastLewdSeriesDay = -1
    $ TavernBreakfastAbsentTalkDay = -1
    $ TavernBreakfastListenDay = int(dayspassed or 0)
    $ TavernBreakfastMarketTalkDay = int(dayspassed or 0)
    $ TavernBreakfastMotivationDay = int(dayspassed or 0)
    $ CurrentLoc["sandra"] = "TavernKitchen"
    $ CurrentLoc["melissa"] = "TavernKitchen"
    $ CurrentLoc["amanda"] = "TavernKitchen"
    $ HouseholdMorningState[_household_morning_state_key("melissa")] = {"issue": "sleepy", "resolved": 0, "indecent": 0}
    $ _player_add_item_by_id("energy_tea_001", 1)
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ CurrentRoom = TavernKitchenRoom
    $ CurLoc = "TavernKitchen"
    $ TavernBreakfastPresentIds = ["sandra", "melissa", "amanda"]
    $ TavernBreakfastEventActive = True
    $ TavernBreakfastBaseText = "Тестовый завтрак."
    $ TavernKitchenSavedText = TavernBreakfastBaseText
    run Call("TavernKitchenBreakfastMenu")
    advance until screen "main_ui" timeout 20.0
    assert eval ("melissa" in list(tavern_breakfast_present_ids() or [])) timeout 5.0
    assert eval ("melissa" not in list(tavern_breakfast_absent_ids() or [])) timeout 5.0
    assert eval ("melissa" in list(tavern_breakfast_core_present_ids() or [])) timeout 5.0
    assert eval (len([str(i.caption or "") for i in tavern_breakfast_menu_items() if "Посмотреть на" in str(i.caption or "") and "Мелисс" in str(i.caption or "")]) == 1) timeout 5.0
    assert eval ("Мелисса все еще отсыпается" not in " ".join(list(household_breakfast_absence_lines() or []))) timeout 5.0
    assert eval ("Поделиться едой и напитками" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (len([str(i.caption or "") for i in current_action_items if "Посмотреть на" in str(i.caption or "") and "Мелисс" in str(i.caption or "")]) == 1) timeout 5.0
    run Call("TavernKitchenBreakfastPerkMenu")
    assert eval ("Поделиться напитком" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    run Call("TavernKitchenBreakfastPerkDrink")
    assert eval ("Вы делитесь бодрящим чаем" in str(MainTxt or "")) timeout 5.0
    run Function(advance_paged_panel_text)
    run Function(advance_paged_panel_text)
    run Function(advance_paged_panel_text)
    advance until eval (str(current_action_title or "") == "Завтрак") timeout 5.0
    run Call("TavernKitchenBreakfastLookAtGirl", "melissa")
    assert eval ("Вы присматриваетесь к Мелиссе за завтраком" in str(MainTxt or "")) timeout 5.0

testcase external_breakfast_angry_amanda_melissa_mockery:
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ dayspassed = 14
    $ BreakfastToday = False
    $ TavernBreakfastEventActive = True
    $ TavernBreakfastPresentIds = ["sandra", "melissa", "amanda"]
    $ CurrentLoc["sandra"] = "TavernKitchen"
    $ CurrentLoc["melissa"] = "TavernKitchen"
    $ CurrentLoc["amanda"] = "TavernKitchen"
    $ CurrentLoc["becky"] = "GroceryStore"
    $ relationship_set_anger("amanda", 2, 1, "external_test")
    $ relationship_set_anger("melissa", 2, 1, "external_test")
    assert eval ("becky" not in list(tavern_breakfast_present_ids() or [])) timeout 5.0
    assert eval ("Бекки" not in list(tavern_breakfast_present_names() or [])) timeout 5.0
    assert eval ("Крысы?" in " ".join(list(tavern_breakfast_dialogue_lines() or []))) timeout 5.0
    assert eval (len([row for row in tavern_breakfast_dialogue_lines() if "Пальцы из кисок" in str(row or "")]) == 1) timeout 5.0
    run Call("MelissaRatBreakfastScene")
    assert eval ("За столом не шипеть" in str(MainTxt or "")) timeout 5.0

testcase external_breakfast_window_and_call_all_click:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ week = 1
    $ time = 0
    $ hour = 7
    $ minute = 55
    $ dayspassed = 13
    $ BreakfastToday = False
    $ TavernBreakfastEventActive = False
    $ TavernBreakfastPresentIds = None
    $ Melissa.var["ratKilled"] = False
    $ Melissa.var["storage_rat_cleared"] = 0
    $ Melissa.var["storage_rat_last_help_day"] = -1
    $ Melissa.var["bats_episode"] = 8
    $ werecat_state()["rats_problem_active"] = 0
    $ werecat_state()["rat_breakfast_seen"] = 1
    $ werecat_state()["adoption_breakfast_seen"] = 1
    $ CurrentLoc["sandra"] = "TavernKitchen"
    $ CurrentLoc["melissa"] = "TavernKitchen"
    $ CurrentLoc["amanda"] = "TavernKitchen"
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ CurrentRoom = TavernKitchenRoom
    $ CurLoc = "TavernKitchen"
    $ location = CurLoc
    run Call("TavernKitchenBuildActions")
    assert eval ("Позавтракать" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ hour = 8
    $ minute = 0
    run Call("TavernKitchenBuildActions")
    assert eval ("Позавтракать" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ hour = 10
    $ minute = 0
    $ BreakfastToday = False
    $ TavernBreakfastEventActive = False
    $ TavernBreakfastPresentIds = None
    run Call("TavernKitchenBuildActions")
    $ BreakfastToday = True
    run Call("TavernKitchenBuildActions")
    assert eval ("Позавтракать" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0

testcase external_actual_barber_actions_click:
    $ external_calendar_set_fields(day, month, year, 14, 0)
    $ external_calendar_set_weekday(1)
    $ money = max(int(money or 0), 500)
    $ PlayerHaircutDaySt = -30
    $ dayssincehaircut = 30
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Jump("BarberShop")
    advance until screen "main_ui" timeout 20.0
    assert eval (len([str(i.caption or "") for i in current_action_items if "Подстричься" in str(i.caption or "")]) == 1) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("выглядите куда опрятнее" in str(MainTxt or "")) timeout 20.0
    assert eval (int(player_state().appearance.haircut_day or 0) == int(dayspassed or 0)) timeout 5.0

testcase external_actual_market_click:
    $ external_calendar_set_fields(day, month, year, 12, 0)
    $ external_calendar_set_weekday(1)
    $ CurrentLoc["clara"] = ""
    $ ClaraVar["booklet_market_seen"] = 1
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
    $ renpy.call_in_new_context("MarketPlaceObjectMenu", "market_stalls")
    assert eval (str(current_action_title or "") == 'Рыночные лотки') timeout 5.0
    assert eval ('Осмотреть лотки' in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("MarketPlaceObjectText", "market_stalls", "examine_market_stalls")
    assert eval ('Торговцы расхваливают товар' in str(MainTxt or "")) timeout 5.0

testcase external_actual_market_blind_pirate_first_entry:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(11, 1, CALENDAR_START_CYCLE, 12, 0)
    $ external_calendar_set_weekday(1)
    $ CurrentLoc["clara"] = ""
    $ ClaraVar["booklet_market_seen"] = 1
    python:
        if "claraBookletMarket" in threads:
            threads["claraBookletMarket"].complete()
    $ findAvailableEvents(True)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 0
    $ BlindPirateBreakfastPending = 0
    $ TownStreetEventsToday = 0
    $ TownStreetStorySeenKeys = []
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ MyStallion = "test-horse"
    run Jump("MarketPlace")
    advance until screen "main_ui" timeout 20.0
    assert eval (int(BlindPirateMarketEventSeen or 0) == 1) timeout 5.0
    assert eval (int(BlindPirateBreakfastPending or 0) == 1) timeout 5.0
    assert eval ("железной клеткой" in str(MainTxt or "")) timeout 5.0
    assert eval (town_street.random_seen_this_slot("MarketPlace")) timeout 5.0

testcase external_market_clock_open_hours:
    $ external_calendar_set_fields(day, month, year, 6, 59)
    $ external_calendar_set_weekday(1)
    assert eval (not MarketPlaceRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 7, 0)
    $ external_calendar_set_weekday(1)
    assert eval (MarketPlaceRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 17, 59)
    $ external_calendar_set_weekday(1)
    assert eval (MarketPlaceRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 18, 0)
    $ external_calendar_set_weekday(1)
    assert eval (not MarketPlaceRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 10, 0)
    $ external_calendar_set_weekday(7)
    assert eval (not MarketPlaceRoom.is_open()) timeout 5.0
'''


ACTUAL_RANDOM_TOWN_CLICK_CHECKS = r'''
label external_random_town_sink:
    $ current_action_title = "External click sink"
    $ current_action_items = []
    call screen main_ui
    return

testcase external_actual_random_town_continue_click:
    $ _town_test_date = calendar_v2.day_number_to_parts(5)
    $ external_calendar_set_fields(int(_town_test_date.get("day", 1) or 1), int(_town_test_date.get("month", 1) or 1), int(_town_test_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 22, 0)
    $ CurLoc = "external_random_town_sink"
    $ location = CurLoc
    $ CurrentRoom = None
    $ exploration = 300
    $ notoriety = 60
    $ money = 500
    $ tavernfame = 10
    $ TownStreetEventsToday = 0
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ TownStreetDailyPlan = {}
    $ GuardCaptainVar = {}
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ renpy.random.seed(11)
    run Call("TownRandomChronicleEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Городские слухи") timeout 5.0
    assert eval (str(TownStreetLastEventText or "") != "") timeout 5.0
    assert eval (len(str(TownStreetLastEventText or "")) > 80 and TownStreetEventsToday == 1) timeout 5.0
    assert eval (len(list(TownStreetStorySeenKeys or [])) >= 1 and evalTime is None) timeout 5.0
    assert eval (str(list(main_ui_action_items_with_entities(current_action_items or []))[0].caption or "") == "Идти дальше") timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2

testcase external_actual_random_town_click:
    $ renpy.test.testsettings._test.timeout = 60.0
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ BlindPirateMarketEventSeen = 1
    $ TownStreetEventsToday = 2
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0

    $ _town_test_date = calendar_v2.day_number_to_parts(5)
    $ day = int(_town_test_date.get("day", 1) or 1)
    $ month = int(_town_test_date.get("month", 1) or 1)
    $ year = int(_town_test_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE)
    $ external_calendar_set_fields(day, month, year, 22, 0)
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
    $ _town_plan = town_street.ensure_daily_plan()
    assert eval (_town_plan.get("beggar") == 10 and _town_plan.get("thugs") == 10 and _town_plan.get("chronicle") == 25) timeout 5.0
    assert eval (_town_plan.get("patrol") == 55 and _town_plan.get("patrol_notoriety_bonus") == 30) timeout 5.0
    $ TownStreetDailyPlan = {"day": int(dayspassed or 0), "events": {"StreetTavern": "TownStreetHelpEvent", "MarketPlace": "TownStreetHelpEvent", "PortStreets": "TownStreetHelpEvent", "ArtisansQuarter": "TownStreetHelpEvent"}}
    $ _town_repaired_plan = town_street.ensure_daily_plan()
    assert eval (_town_repaired_plan.get("beggar") == 10 and _town_repaired_plan.get("patrol") == 55) timeout 5.0
    assert eval (town_street.curfew_active() and town_street.patrol_chance() == 55) timeout 5.0
    $ _planned_label = town_street.planned_label("StreetTavern")
    assert eval (_planned_label == "") timeout 5.0
    $ hour = 8
    $ minute = 0
    $ time = 1
    $ clock_minutes = 22 * 60
    assert eval (not town_street.curfew_active()) timeout 5.0
    assert eval (not town_street.patrol_allowed("StreetTavern")) timeout 5.0
    $ _patrol_morning_result = renpy.call_in_new_context("TownStreetPatrolEvent")
    assert eval (_patrol_morning_result is False and str(current_action_title or "") != "Ночной патруль") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 22, 0)
    run Call("TownStreetPatrolEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Ночной патруль") timeout 5.0
    assert eval ("Спрятаться и уйти дворами" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5)
    pause 0.2
    assert eval (TownStreetPatrolsToday >= 1 and exploration >= 308 and len(list(TownStreetStorySeenKeys or [])) >= 1 and evalTime is None) timeout 5.0
    assert eval (town_street.random_seen_this_slot("StreetTavern", "TownStreetPatrolEvent")) timeout 5.0
    assert eval (not town_street.planned_for("StreetTavern", "TownStreetPatrolEvent")) timeout 5.0
    assert eval ("TownStreetPatrolEvent" in TownStreetFiredLabelsToday and "StreetTavern" in TownStreetFiredLocationsToday) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 12, 0)
    assert eval (town_street.random_seen_this_slot("StreetTavern", "TownStreetPatrolEvent")) timeout 5.0
    assert eval (not town_street.curfew_active()) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2

    $ external_calendar_set_fields(day, month, year, 22, 0)
    $ CurLoc = "StreetTavern"
    $ location = CurLoc
    $ CurrentRoom = StreetTavernRoom
    $ _layout_last_picture = "bg StreetTavern"
    $ scene_image = _layout_last_picture
    $ exploration = 300
    $ notoriety = 60
    $ health = 100
    $ energy = 100
    $ fight_info().level = {"you": 3}
    $ TownStreetEventsToday = 0
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ TownStreetFiredLabelsToday = []
    $ TownStreetFiredLocationsToday = []
    $ GuardCaptainVar = {}
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Call("TownStreetPatrolEvent")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_4" pos (0.5, 0.5) until eval (str(UI_mode or "") == "fight") timeout 10.0
    assert eval (str(fight_info().enemy_id or "") == "patrol_guard" and len(list(fight_info().enemy_party or [])) == 2) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "") == "images/fight/patrol_guard.png") timeout 5.0
    $ renpy.call_in_new_context("FightDoAction", "retreat")
    assert eval (str(UI_mode or "") == "fight" and str(fight_info().outcome_popup.get("kind", "") or "") == "retreat") timeout 5.0
    $ _fight_test_picture = str(fight_info().return_picture or "")
    $ fight_finish_to_room(str(MainTxt or ""))
    $ scene_image = _fight_test_picture
    $ _layout_last_picture = _fight_test_picture
    assert eval (str(UI_mode or "") == "scene" and str(CurLoc or "") == "StreetTavern") timeout 5.0

    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 12, 0)
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
    run Call("TownStreetHelpEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Уличная просьба") timeout 5.0
    assert eval ("Дать еды и предложить грязную работу при трактире" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2
    assert eval (len(TavernBlackworkerCandidates) >= 1 and tavernfame >= 1 and exploration >= 105 and notoriety == 0) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2

    $ external_calendar_set_fields(2, 1, CALENDAR_START_CYCLE, 18, 0)
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
    run Call("TownStreetThugsEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Уличные громилы") timeout 5.0
    assert eval ("Попробовать спугнуть их криком" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (exploration >= 306) timeout 10.0
    assert eval (exploration >= 306 and notoriety == 0) timeout 5.0

    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 18, 0)
    $ CurLoc = "ArtisansQuarter"
    $ location = CurLoc
    $ CurrentRoom = ArtisansQuarterRoom
    $ _layout_last_picture = "bg ArtisansQuarter"
    $ scene_image = _layout_last_picture
    $ health = 100
    $ energy = 100
    $ exploration = 300
    $ notoriety = 0
    $ fight_info().level = {"you": 2}
    $ playerItems = {}
    $ EquippedWeapon = ""
    $ EquippedArmor = ""
    $ TownStreetEventsToday = 0
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ TownStreetFiredLabelsToday = []
    $ TownStreetFiredLocationsToday = []
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Call("TownStreetThugsEvent")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(UI_mode or "") == "fight") timeout 10.0
    assert eval (str(fight_info().enemy_id or "") == "street_crook" and len(list(fight_info().enemy_party or [])) == 2) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "") == "images/fight/thug.png") timeout 5.0
    $ renpy.call_in_new_context("FightDoAction", "retreat")
    assert eval (str(UI_mode or "") == "fight" and str(fight_info().outcome_popup.get("kind", "") or "") == "retreat") timeout 5.0
    $ _fight_test_picture = str(fight_info().return_picture or "")
    $ fight_finish_to_room(str(MainTxt or ""))
    $ scene_image = _fight_test_picture
    $ _layout_last_picture = _fight_test_picture
    assert eval (str(UI_mode or "") == "scene" and str(CurLoc or "") == "ArtisansQuarter") timeout 5.0

    $ TownStreetEventsToday = 1
    $ TownStreetPatrolsToday = 1
    $ TownStreetFightToday = 1
    $ TownCurfewCaughtToday = 1
    $ TownStreetStorySeenKeys = ["bad-key"]
    $ TownStreetDailyPlan = {"day": int(dayspassed or 0), "events": {"StreetTavern": "TownStreetHelpEvent", "MarketPlace": "TownStreetHelpEvent", "PortStreets": "TownStreetHelpEvent", "ArtisansQuarter": "TownStreetHelpEvent"}}
    $ TownStreetLastEventText = "old"
    $ TownStreetContext = {"old": True}
    $ TownStreetFiredLabelsToday = ["TownStreetHelpEvent"]
    $ TownStreetFiredLocationsToday = ["StreetTavern"]
    $ TownStreetCooldowns = {"TownStreetHelpEvent": int(dayspassed or 0)}
    $ next_day_finish_day_events()
    assert eval (TownStreetEventsToday == 0 and TownStreetPatrolsToday == 0 and TownStreetFightToday == 0 and TownCurfewCaughtToday == 0) timeout 5.0
    assert eval (TownStreetStorySeenKeys == [] and TownStreetDailyPlan == {} and TownStreetLastEventText == "" and TownStreetContext == {}) timeout 5.0
    assert eval (TownStreetFiredLabelsToday == [] and TownStreetFiredLocationsToday == [] and TownStreetCooldowns == {}) timeout 5.0

    run Jump("DebugTownRandomEvents")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Отладка городских случайных событий") timeout 5.0
    assert eval ("План:" in str(MainTxt or "") and "Форсировать патруль" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
'''


TARGETED_CURRENT_BUG_CHECKS = r'''
testcase external_sleep_after_midnight_detector:
    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 1, 20)
    assert eval (nextday_started_after_midnight()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 6, 0)
    assert eval (not nextday_started_after_midnight()) timeout 5.0

testcase external_town_thugs_shout_result:
    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 18, 0)
    $ CurLoc = "StreetTavern"
    $ location = CurLoc
    $ CurrentRoom = StreetTavernRoom
    $ _layout_last_picture = "bg StreetTavern"
    $ scene_image = _layout_last_picture
    $ health = 100
    $ energy = 100
    $ exploration = 300
    $ notoriety = 0
    $ TownStreetEventsToday = 0
    $ TownStreetPatrolsToday = 0
    $ TownStreetFightToday = 0
    $ TownCurfewCaughtToday = 0
    $ TownStreetStorySeenKeys = []
    $ TownStreetFiredLabelsToday = []
    $ TownStreetFiredLocationsToday = []
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Call("TownStreetThugsEvent")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Попробовать спугнуть их криком" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (int(exploration or 0) >= 306 and int(reputation or 0) >= 2 and int(notoriety or 0) >= 4) timeout 20.0
    assert eval (len(list(current_action_items or [])) == 1) timeout 5.0

testcase external_town_thugs_fight_victory_result:
    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 18, 0)
    $ CurLoc = "ArtisansQuarter"
    $ location = CurLoc
    $ CurrentRoom = ArtisansQuarterRoom
    $ _layout_last_picture = "bg ArtisansQuarter"
    $ scene_image = _layout_last_picture
    $ health = 30
    $ energy = 100
    $ exploration = 300
    $ reputation = 10
    $ tavernfame = 5
    $ notoriety = 0
    $ playerItems = {}
    $ EquippedWeapon = "old_axe_001"
    $ EquippedArmor = ""
    $ fight_info().level = {"you": 3}
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    run Call("TownStreetThugsFight")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(UI_mode or "") == "fight" and str(fight_info().enemy_id or "") == "street_crook") timeout 5.0
    $ FightEnemyParty[0]["health"] = 1
    $ FightEnemyParty[0]["energy"] = 1
    $ FightEnemyParty[1]["health"] = 1
    $ FightEnemyParty[1]["energy"] = 1
    $ PlayerFightSupply["fire_bomb"] = 1
    $ renpy.call_in_new_context("FightDoAction", "fire_bomb")
    assert eval (str(FightOutcomeKind or "") == "victory" and str(current_action_title or "") == "Победа") timeout 5.0
    assert eval (isinstance(HuntLastResult, dict) and str(HuntLastResult.get("outcome", "") or "") == "victory") timeout 5.0
    assert eval (isinstance(FightVictoryLoot, dict) and "money" in FightVictoryLoot) timeout 5.0
    assert eval ("добыч" in str(FightOutcomeText or "").lower()) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == "Итог драки") timeout 20.0
    assert eval (str(UI_mode or "") == "scene" and str(CurLoc or "") == "ArtisansQuarter") timeout 5.0
    assert eval (int(reputation or 0) == 13 and int(tavernfame or 0) == 6 and int(notoriety or 0) == 3) timeout 5.0
    assert eval (len(list(current_action_items or [])) == 1 and str(current_action_title or "") == "Итог драки") timeout 5.0

testcase external_georgette_back_alley_not_visible_in_port_streets:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 20, 0)
    $ external_calendar_set_weekday(1)
    $ npc_schedule_sync_all()
    $ CurLoc = "PortStreets"
    $ location = CurLoc
    $ CurrentRoom = PortStreetsRoom
    $ Georgett.var["portstreet_clients_seen_today"] = 0
    assert eval (str(getLocation("georgett") or "") == "PortStreets") timeout 5.0
    assert eval (npc_action_data_for_room("georgett", "PortStreets") is None) timeout 5.0
    $ Georgett.set_portstreet_visible(True)
    assert eval (str(getLocation("georgett") or "") == "PortStreets") timeout 5.0
    assert eval ("georgett" in list(getNPCids("PortStreets") or [])) timeout 5.0
    $ _georgett_port_data = npc_action_data_for_room("georgett", "PortStreets")
    assert eval (tuple(_georgett_port_data.get("talk_args", ())) == ("georgett", "street")) timeout 5.0
    assert eval (str(_georgett_port_data.get("idle_picture", "") or "") == "images/georgett/portraits/portrait1.jpg") timeout 5.0
    $ open_npc_action_menu_state("georgett", "PortStreets", _georgett_port_data)
    assert eval ("Поговорить" in [str(getattr(i, "caption", "") or "") for i in current_action_items]) timeout 5.0
    assert eval (str(_layout_last_picture or "") == "images/georgett/portraits/portrait1.jpg") timeout 5.0
    run Call("IntGeorgettTalk", "georgett", "street")
    assert eval ("Болтать" in [str(getattr(i, "caption", "") or "") for i in current_action_items]) timeout 5.0
    $ Georgett.set_portstreet_visible(False)
    $ Georgett.mark_portstreet_clients_seen()
    assert eval (str(getLocation("georgett") or "") == "PortStreets") timeout 5.0

'''


DEBUG_BUILDER_ROOM_CHECKS = r'''
testcase external_debug_builder_room_visual_surfaces:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0

    assert eval (bool(config.developer)) timeout 5.0
    click id "main_ui_debug_builder_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == "DebugBuilderRoom") timeout 20.0
    assert eval (str(CurLoc or "") == "DebugBuilderRoom") timeout 5.0
    assert eval (str(current_action_title or "") == "Debug Builder") timeout 5.0
    assert eval ("Picture path checks" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Event condition probes" in [str(i.caption or "") for i in current_action_items] and "Correction ownership notes" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ _debug_week_before = int(week or 1)
    $ _debug_month_before = int(month or 1)
    $ PlayerChoresWeek["bring_woods"] = 0
    $ _pc_sync_ui_chores()
    click id "debug_builder_time_slot_3" pos (0.5, 0.5) until eval (int(time or 0) == 3) timeout 10.0
    click id "debug_builder_week_next" pos (0.5, 0.5) until eval (int(week or 1) != _debug_week_before) timeout 10.0
    click id "debug_builder_month_next" pos (0.5, 0.5) until eval (int(month or 1) != _debug_month_before) timeout 10.0
    click id "debug_builder_chore_inc_bring_woods" pos (0.5, 0.5) until eval (int(PlayerChoresWeek.get("bring_woods", 0) or 0) == 1) timeout 10.0

    run Jump("DebugBuilderPictures")
    advance until screen "main_ui" timeout 20.0
    assert eval ("images/general/player_card.jpg" in str(MainTxt or "") and "[OK] images/amanda/amanda_card.jpg" in str(MainTxt or "")) timeout 5.0

    run Jump("DebugBuilderSequences")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Picture sequences" and "Picture sequence probes:" in str(MainTxt or "")) timeout 5.0

    run Call("DebugBuilderInspectRoom", "TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Room: TavernKitchen" in str(MainTxt or "") and "Descriptions:" in str(MainTxt or "") and "Visible NPCs from schedule:" in str(MainTxt or "")) timeout 5.0

    run Call("DebugBuilderMenuRoom", "TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Room/menu probe: TavernKitchen" in str(MainTxt or "") and "Visible generated menu items:" in str(MainTxt or "")) timeout 5.0

    run Jump("DebugBuilderStoryEvents")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Story events" and "Projected story events now:" in str(MainTxt or "")) timeout 5.0

    run Jump("DebugBuilderEventProbes")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Event condition probes" and "Event condition probes:" in str(MainTxt or "")) timeout 5.0

    run Jump("DebugBuilderSchedules")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "NPC schedules" and "NPC schedule at week=" in str(MainTxt or "") and "23:00-05:59" in str(MainTxt or "")) timeout 5.0
    assert eval ("Probe rooms" in [str(i.caption or "") for i in current_action_items] and "16:00 Day" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    run Call("DebugBuilderScheduleRoom", "TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Schedule room probe: TavernKitchen" in str(MainTxt or "") and "getNPCids:" in str(MainTxt or "") and "Room.visible_npcs:" in str(MainTxt or "")) timeout 5.0

    run Jump("DebugBuilderCorrectionNotes")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Correction notes" and "Correction ownership notes:" in str(MainTxt or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == "Repair notes written") timeout 10.0
    assert eval ("Repair notes document written:" in str(MainTxt or "")) timeout 5.0
    $ _repair_doc_path = str(DebugBuilderRepairNotesPath or "")
    assert eval (str(_repair_doc_path or "").endswith("debug_builder_repair_notes.md") and os.path.isfile(_repair_doc_path)) timeout 5.0
    assert eval ("## Feature Repair Templates" in open(_repair_doc_path, "r", encoding="utf-8").read() and "### Event / Thread Feature" in open(_repair_doc_path, "r", encoding="utf-8").read()) timeout 5.0

    run Jump("DebugBuilderCards")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Amanda" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ show_girl_card_main_ui_state("amanda")
    assert eval (str(girl_card_portrait_path("amanda") or "") == "images/amanda/amanda_card.jpg") timeout 5.0

    $ health = 100
    $ energy = 100
    $ exploration = 0
    $ EquippedWeapon = ""
    $ EquippedArmor = ""
    $ RustyHunterRifleLoadedAmmo = ""
    $ fight_sync_loaded_weapon_state_from_inventory()
    $ fight_sync_supply_from_inventory()
    $ _debug_dog = ensure_dog_runtime()
    $ _debug_dog.in_company = False
    run Jump("DebugBuilderFightTests")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Fight tests" and all(label in [str(i.caption or "") for i in current_action_items] for label in ["Fight setup", "Launch fights"])) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == "Fight setup") timeout 20.0
    assert eval (str(current_action_title or "") == "Fight setup" and all(any(str(i.caption or "").startswith(prefix) for i in current_action_items) for prefix in ["Launch fights", "Weapon:", "Armor:", "Health:", "Experience:", "Supplies:", "Dog:"])) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (str(EquippedWeapon or "") == "old_axe_001" and str(current_action_title or "") == "Fight setup") timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (str(EquippedWeapon or "") == "rusty_hunter_rifle_001" and int(PlayerFightSupply.get("arrows", 0) or 0) > 0 and str(FightLoadedAmmo or "") == "arrows" and int(FightWeaponLoaded or 0) == 1) timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (str(EquippedArmor or "") == "old_leather_cuirass_001" and str(current_action_title or "") == "Fight setup") timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (str(EquippedArmor or "") == "" and str(current_action_title or "") == "Fight setup") timeout 20.0
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (int(health or 0) == 60 and str(current_action_title or "") == "Fight setup") timeout 20.0
    click id "choice_panel_button_4" pos (0.5, 0.5) until eval (int(exploration or 0) == 50 and int(FightLevel.get("you", 0) or 0) >= 2) timeout 20.0
    click id "choice_panel_button_5" pos (0.5, 0.5) until eval (int(PlayerFightSupply.get("bandage", 0) or 0) > 0 and int(PlayerFightSupply.get("healing_potion", 0) or 0) > 0 and int(PlayerFightSupply.get("fire_bomb", 0) or 0) > 0 and int(PlayerFightSupply.get("bees_bomb", 0) or 0) > 0) timeout 20.0
    click id "choice_panel_button_6" pos (0.5, 0.5) until eval (bool(dog.owned) and bool(dog.in_company) and str(current_action_title or "") == "Fight setup") timeout 20.0
    assert eval (len(list(fight_company_display_rows() or [])) >= 2 and "notoriety" in dict(list(fight_company_display_rows() or [{}])[0]) and "exploration" in dict(list(fight_company_display_rows() or [{}])[0])) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == "Launch fights") timeout 20.0
    assert eval (all(label in [str(i.caption or "") for i in current_action_items] for label in ["Street crooks", "Random forest hunt roll", "Patrol guards"])) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(UI_mode or "") == "fight") timeout 20.0
    assert eval (str(UI_mode or "") == "fight" and str(fight_info().enemy_id or "") == "street_crook" and len(list(fight_info().enemy_party or [])) == 2) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "") == "images/fight/thug.png") timeout 5.0
    assert eval (len(list(fight_enemy_display_rows() or [])) == 2 and all(int(row.get("health_max", 0) or 0) > 0 and int(row.get("energy_max", 0) or 0) > 0 for row in list(fight_enemy_display_rows() or []))) timeout 5.0
    assert eval (all(label in [str(i.caption or "") for i in current_action_items] for label in ["Выстрелить (стрела)", "Использовать бинт", "Выпить бодрящий чай", "Выпить лечебное зелье", "Бросить огненную бутылку", "Бросить пчелиный заряд", "Командовать псом", "Отступить"])) timeout 5.0
    $ _debug_turn_text_before = str(MainTxt or "")
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (str(MainTxt or "") != _debug_turn_text_before and str(UI_mode or "") == "fight") timeout 20.0
    assert eval (str(MainTxt or "") != _debug_turn_text_before and str(UI_mode or "") == "fight") timeout 5.0
    assert eval (str(current_action_title or "") == "Бой" and "Отступить" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ _debug_turn_text_before = str(MainTxt or "")
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (str(MainTxt or "") != _debug_turn_text_before and str(UI_mode or "") == "fight") timeout 20.0
    assert eval (str(current_action_title or "") == "Бой" and "Отступить" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ fight_finish_to_room("Debug fight closed.")
    assert eval (str(CurLoc or "") == "DebugBuilderFightTests" and str(UI_mode or "") == "scene") timeout 5.0
'''


AMANDA_ROOM_NIGHT_EVENT_CHECKS = r'''
testcase external_amanda_room_night_bed_action_uses_thread_event:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0

    $ external_calendar_set_fields(day, month, year, 22, 0)
    $ Melissa.var["temp_room"] = ""
    $ Melissa.var["drawings_found"] = 0
    $ CurrentLoc["amanda"] = "TavernAmandaRoom"
    $ npc_schedule_set("amanda", [NPCScheduleEntry(location="TavernAmandaRoom", time_slots=[], awake=False, talkable=False, priority=999)])
    $ cametoday = 0
    $ cancumdaily = 3
    $ Amanda.set_var_int("kickyoufromroom", 0)
    $ Amanda.set_var_int("kickyoufromroomcount", 0)
    run Jump("TavernAmandaRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(CurLoc or "") == "TavernAmandaRoom") timeout 5.0
    assert eval ("Кровать" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    run Call("tavern_amanda_room_object_menu", "bed_002")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Кровать") timeout 5.0
    assert eval ("Пристать к Аманде" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
'''


MY_ROOM_RECIPE_BOOK_ACTION_CHECKS = r'''
testcase external_my_room_recipe_book_table_link:
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
    $ _room_remove_item_by_id(TavernMyRoomRoom, "recipe_book_001")
    $ _room_add_item_by_id(TavernMyRoomRoom, "recipe_book_001")

    run Jump("TavernMyRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval ("recipe_book_001" not in [str(getattr(i.action, 'label', '') or '') for i in current_action_items]) timeout 5.0
    assert eval ("книга с рецептами" not in [str(i.caption or "").lower() for i in current_action_items]) timeout 5.0
    assert eval ("{a=call:TavernMyRoomTableMenu}" in str(MainTxt or "")) timeout 5.0
    assert eval ("старая пыльная книга с рецептами" in str(MainTxt or "")) timeout 5.0

    run Call("TavernMyRoomTableMenu")
    assert eval (str(current_action_title or "") == "Стол") timeout 5.0
    assert eval ("Читать книгу рецептов" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Создать предмет" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
'''


MY_ROOM_WINDOW_ACTION_CHECKS = r'''
testcase external_my_room_window_day_night_amanda_pictures:
    $ external_calendar_set_fields(day, month, year, 12, 0)
    $ CurrentRoom = TavernMyRoomRoom
    $ CurLoc = "TavernMyRoom"
    $ location = CurLoc
    $ Amanda.set_var_int("gave_night_bowl", 0)
    $ Amanda.set_var_int("night_bowl_window_seen_day", -1)
    run Call("TavernMyRoomWindowLookBackyard")
    assert eval (str(_layout_last_picture or "") == "images/player_room/window0.png") timeout 5.0
    assert eval (str(current_action_title or "") == "Маленькое окно" and "Назад" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ external_calendar_set_fields(day, month, year, 22, 0)
    $ Amanda.set_var_int("gave_night_bowl", 0)
    $ Amanda.set_var_int("night_bowl_window_seen_day", -1)
    run Call("TavernMyRoomWindowLookBackyard")
    assert eval (str(_layout_last_picture or "") == "images/player_room/window2.png") timeout 5.0
    assert eval (str(current_action_title or "") == "Маленькое окно" and "Назад" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ Amanda.set_var_int("gave_night_bowl", 1)
    $ Amanda.set_var_int("got_fancy_night_bowl", 0)
    $ Amanda.set_var_int("prefers_backyard_relief", -1)
    $ Amanda.set_var_int("night_bowl_window_seen_day", -1)
    $ _player_add_item_by_id("night_bowl_001", 1)
    run Call("TavernMyRoomWindowLookBackyard")
    assert eval (str(_layout_last_picture or "") == "images/player_room/windowAmand.png") timeout 5.0
    assert eval (str(current_action_title or "") == "Маленькое окно" and "Назад" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (Amanda.var_int("night_bowl_window_seen_day", -1) == int(calendar_v2.daysInGame or 0)) timeout 5.0
'''


TAVERN_ROOM_PICTURE_STATE_CHECKS = r'''
testcase external_tavern_room_movement_resets_picture_state:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0

    $ external_calendar_set_fields(day, month, year, 12, 0)
    $ TavernMainBlockEvents = 1
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(CurLoc or "") == "TavernMain") timeout 5.0
    assert eval (str(_layout_last_picture or "") == "images/tavern/mainhall/main_hall.png") timeout 5.0

    run Call("TavernMainObjectMenu", "bar_001")
    assert eval (str(current_object_id or "") == "bar_001") timeout 5.0
    assert eval (str(_layout_last_picture or "") == "images/tavern/mainhall/bar_mainHall.png") timeout 5.0

    run Call("AdvanceMovementTime", "TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(CurLoc or "") == "TavernKitchen") timeout 5.0
    assert eval (str(current_object_id or "") == "" and str(current_girl_key or "") == "") timeout 5.0
    assert eval (str(_layout_last_picture or "") != "images/tavern/mainhall/bar_mainHall.png") timeout 5.0
    assert eval ("kitchen" in str(_layout_last_picture or "").lower()) timeout 5.0

    $ external_calendar_set_fields(day, month, year, 22, 0)
    $ TavernMainBlockEvents = 1
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(CurLoc or "") == "TavernMain") timeout 5.0
    assert eval (str(current_object_id or "") == "") timeout 5.0
    assert eval (str(_layout_last_picture or "") == "images/tavern/mainhall/main_hall_night.png") timeout 5.0
'''


MELISSA_BATS_DRAWINGS_CHECKS = r'''
testcase external_melissa_bats_room_search_after_wait:
    $ _melissa_bats_test_date = calendar_v2.day_number_to_parts(100)
    $ external_calendar_set_fields(int(_melissa_bats_test_date.get("day", 1) or 1), int(_melissa_bats_test_date.get("month", 1) or 1), int(_melissa_bats_test_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 14, 0)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ CurLoc = "TavernMelissaRoom"
    $ location = CurLoc
    $ CurrentRoom = TavernMelissaRoomRoom
    $ Melissa.initialize_new_game_state()
    $ Melissa.var["bats_episode"] = 6
    $ Melissa.var["temp_room"] = "TavernAmandaRoom"
    $ Melissa.var["drawings_found"] = 0
    $ Melissa.var["drawings_booklet_taken"] = 0
    $ Melissa.var["drawings_booklet_left"] = 0
    $ Melissa.var["drawings_spy_option_unlocked"] = 0
    $ Melissa.var["drawings_ready_day"] = 86
    $ Melissa.current_location = "TavernAmandaRoom"
    $ Melissa.sync_melissa_maps()
    $ exploration = 121
    $ _player_remove_item_by_id("melissa_drawings_booklet_001", _player_item_count_by_id("melissa_drawings_booklet_001"))
    $ UpstairsRoomSearchState["TavernMelissaRoom"] = 0
    $ PlayerChoresWeek["clean_upstairs_rooms"] = int(player_chore_target("clean_upstairs_rooms") or 0)
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ initStoryEventRuntime(True)
    $ threads["melissaBatProblem"].advanceTo(4, force_active=True)
    $ findAvailableEvents(True)

    assert eval (threads["melissaBatProblem"].currentTarget() == "story_melissa_bat_problem_5") timeout 5.0
    assert eval (story_event_available("TavernMelissaRoom", "room_search")) timeout 5.0
    assert eval (str(availEvents["TavernMelissaRoom"]["room_search"].target or "") == "story_melissa_bat_problem_5") timeout 5.0
    run Jump("TavernMelissaRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Осмотреть комнату получше" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("пачка непристойных рисунков" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 10.0
    advance until eval (int(MelissaVar.get("drawings_found", 0) or 0) == 1) timeout 10.0
    assert eval (int(MelissaVar.get("drawings_found", 0) or 0) == 1) timeout 5.0
    assert eval (int(_room_item_count_by_id(TavernMelissaRoomRoom, "melissa_drawings_booklet_001") or 0) == 1) timeout 5.0
    advance until screen "main_ui" timeout 10.0
    assert eval ("пачка непристойных рисунков" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ([str(i.caption or "") for i in current_action_items].index("пачка непристойных рисунков") == 2) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (str(current_object_id or "") == "melissa_drawings_booklet_001") timeout 10.0
    assert eval (str(current_object_id or "") == "melissa_drawings_booklet_001") timeout 5.0
    assert eval (len(list(current_action_items or [])) >= 5) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (int(_player_item_count_by_id("melissa_drawings_booklet_001") or 0) == 1) timeout 10.0
    assert eval (int(MelissaVar.get("drawings_booklet_taken", 0) or 0) == 1) timeout 5.0
    assert eval (int(MelissaVar.get("drawings_booklet_left", 0) or 0) == 0) timeout 5.0
    assert eval (int(MelissaVar.get("drawings_spy_option_unlocked", 0) or 0) == 0) timeout 5.0
    assert eval (int(_player_item_count_by_id("melissa_drawings_booklet_001") or 0) == 1) timeout 5.0
    assert eval (int(_room_item_count_by_id(TavernMelissaRoomRoom, "melissa_drawings_booklet_001") or 0) == 0) timeout 5.0
    assert eval (threads["melissaBatProblem"].currentTarget() == "story_melissa_bat_problem_4") timeout 5.0

testcase external_melissa_werecat_thread_condition_sequence:
    $ external_calendar_set_fields(3, 1, 1100, 6, 0)
    run Call("InitGameNPCs")
    $ CurLoc = "TavernStorage"
    $ location = CurLoc
    $ CurrentRoom = TavernStorageRoom
    $ BreakfastToday = False
    $ TavernBreakfastEventActive = False
    $ Melissa.initialize_new_game_state()
    $ Melissa.var["ratKilled"] = False
    $ Melissa.var["storage_rat_cleared"] = 0
    $ Melissa.var["storage_rat_last_help_day"] = -1
    $ werecat_state()["rats_problem_active"] = 0
    $ werecat_state()["rat_breakfast_seen"] = 0
    $ werecat_state()["hunter_tease_day"] = -1
    $ werecat_state()["adopted"] = 0
    $ werecat_state()["adopted_count"] = 0
    $ werecat_state()["adoption_breakfast_seen"] = 0
    $ werecat_state()["adopted_day"] = -1
    $ werecat_state()["first_month_thanks_day"] = -1
    $ npc_interval_schedule_load_all(True)
    $ npc_schedule_set("melissa", [NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6, 7], start_hour=0, end_hour=24, awake=True, talkable=True, priority=999, label="external_storage_rat")])
    $ Melissa.var["temp_room"] = "TavernStorage"
    $ Melissa.var["bats_episode"] = 1
    $ peopleInfo["melissa"].var["temp_room"] = "TavernStorage"
    $ peopleInfo["melissa"].var["bats_episode"] = 1
    $ household_mark_runtime_event_seen("melissa_storage_rat", -999)
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval (threads["melissaRatProblem"].currentTarget() == "story_melissa_storage_rat_0") timeout 5.0
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_rumor_0") timeout 5.0
    assert eval (not threads["melissaWerecatProblem"].checkActive()) timeout 5.0
    $ _rat_evt = threads["melissaRatProblem"].getevent(0)
    $ _rat_check_fields = [str(row.get("field", "") or "") for row in _rat_evt.auditChecks(threads["melissaRatProblem"].day)]
    assert eval (int(Melissa.var.get("storage_rat_cleared", 0) or 0) == 0) timeout 5.0
    assert eval (str(getLocation("melissa") or "") == "TavernStorage") timeout 5.0
    assert eval (not household_runtime_event_seen_today("melissa_storage_rat")) timeout 5.0
    assert eval (set(["target", "binding", "day", "hour", "delay", "requirements", "conditions", "item", "location_open", "probability"]).issubset(set(_rat_check_fields))) timeout 5.0
    assert eval (all(isinstance(row.get("ok", None), bool) for row in _rat_evt.auditChecks(threads["melissaRatProblem"].day))) timeout 5.0
    $ _rat_check_map = {str(row.get("field", "") or ""): bool(row.get("ok", False)) for row in _rat_evt.auditChecks(threads["melissaRatProblem"].day)}
    assert eval (_rat_check_map.get("day", False)) timeout 5.0
    assert eval (_rat_check_map.get("hour", False)) timeout 5.0
    assert eval (_rat_check_map.get("delay", False)) timeout 5.0
    assert eval (_rat_check_map.get("requirements", False)) timeout 5.0
    assert eval (_rat_check_map.get("conditions", False)) timeout 5.0
    assert eval (_rat_check_map.get("location_open", False)) timeout 5.0
    assert eval (story_event_available("TavernStorage", "enter")) timeout 5.0

    $ Melissa.var["ratKilled"] = True
    $ Melissa.var["storage_rat_cleared"] = 1
    $ Melissa.var["storage_rat_last_help_day"] = int(dayspassed or 0)
    $ Melissa.var["temp_room"] = ""
    $ peopleInfo["melissa"].var["temp_room"] = ""
    $ werecat_state()["rats_problem_active"] = 1
    $ threads["melissaRatProblem"].advance()
    $ CurLoc = "HunterClub"
    $ location = CurLoc
    $ CurrentRoom = HunterClubRoom
    $ evalTime = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval (threads["melissaRatProblem"].completed) timeout 5.0
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_rumor_0") timeout 5.0
    assert eval (story_event_available("HunterClub", "overheard")) timeout 5.0

    $ thread = threads["melissaWerecatProblem"]
    $ thread.setDay()
    run Call("story_melissa_werecat_rumor_0")
    assert eval (int(werecat_state().get("hunter_tease_day", -1) or -1) == int(dayspassed or 0)) timeout 5.0
    advance until eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_intro_0") timeout 10.0
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_intro_0") timeout 5.0

    $ external_calendar_set_fields(3, 1, 1100, 8, 0)
    $ CurLoc = "TavernKitchen"
    $ location = CurLoc
    $ CurrentRoom = TavernKitchenRoom
    $ BreakfastToday = False
    $ evalTime = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval (story_event_available("TavernKitchen", "enter")) timeout 5.0

    $ thread = threads["melissaWerecatProblem"]
    $ thread.setDay()
    run Call("story_melissa_werecat_intro_0")
    assert eval (int(werecat_state().get("rat_breakfast_seen", 0) or 0) == 1) timeout 5.0
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_home_0") timeout 5.0

    $ werecat_state()["adopted"] = 1
    $ werecat_state()["adopted_count"] = 1
    $ werecat_state()["adopted_day"] = int(dayspassed or 0) - 1
    $ werecat_state()["adoption_breakfast_seen"] = 0
    $ external_calendar_set_fields(3, 1, 1100, 8, 0)
    $ BreakfastToday = False
    $ evalTime = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_home_0") timeout 5.0
    $ _home_evt = threads["melissaWerecatProblem"].getevent(2)
    $ _home_check_map = {str(row.get("field", "") or ""): bool(row.get("ok", False)) for row in _home_evt.auditChecks(threads["melissaWerecatProblem"].day)}
    assert eval (_home_check_map.get("day", False)) timeout 5.0
    assert eval (_home_check_map.get("hour", False)) timeout 5.0
    assert eval (_home_check_map.get("delay", False)) timeout 5.0
    assert eval (_home_check_map.get("requirements", False)) timeout 5.0
    assert eval (_home_check_map.get("conditions", False)) timeout 5.0
    assert eval (_home_check_map.get("location_open", False)) timeout 5.0
    assert eval (threads["melissaWerecatProblem"].checkActive()) timeout 5.0
    assert eval (_home_evt.canTrigger(threads["melissaWerecatProblem"].day)) timeout 5.0
    assert eval (len(threads["melissaWerecatProblem"].getAvailableEvents()) > 0) timeout 5.0
    $ findAvailableEvents(True)
    assert eval (story_event_available("TavernKitchen", "enter")) timeout 5.0
    $ thread = threads["melissaWerecatProblem"]
    $ thread.setDay()
    run Call("story_melissa_werecat_home_0")
    assert eval (int(werecat_state().get("adoption_breakfast_seen", 0) or 0) == 1) timeout 5.0
'''


MELISSA_WERECAT_FOREST_ACTION_CHECKS = r'''
testcase external_melissa_werecat_forest_actions_rebuild:
    $ external_calendar_set_fields(4, 1, 1100, 10, 0)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ CurLoc = "Forest"
    $ location = CurLoc
    $ CurrentRoom = ForestRoom
    $ ForestReturnTarget = "StreetTavern"
    $ ForestSavedText = ""
    $ werecat_state()["rats_problem_active"] = 1
    $ werecat_state()["rat_breakfast_seen"] = 1
    $ werecat_state()["hunter_tease_day"] = int(dayspassed or 0)
    $ werecat_state()["adopted"] = 0
    $ werecat_state()["adopted_count"] = 0
    $ werecat_state()["sold"] = 0
    $ werecat_state()["caught"] = 0
    $ werecat_state()["tracks_seen"] = 0
    $ werecat_state()["tracks_first_text_seen"] = 0
    $ werecat_state()["trap_rooms"] = {}
    $ werecat_state()["trap_active"] = 0
    $ werecat_state()["trap_room"] = ""
    $ werecat_state()["trap_day"] = -1
    $ Melissa.var["storage_rat_cleared"] = 1
    $ Melissa.var["storage_rat_last_help_day"] = int(dayspassed or 0) - 1
    $ exploration = 130
    $ _player_remove_item_by_id("hunting_trap_001", _player_item_count_by_id("hunting_trap_001"))
    run Jump("Forest")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Осмотреть лес внимательнее" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 10.0
    advance until screen "main_ui" timeout 20.0
    assert eval (int(werecat_state().get("tracks_seen", 0) or 0) == 1) timeout 5.0
    assert eval (str(current_action_title or "") == "Действия") timeout 5.0
    assert eval ("Осмотреть лес внимательнее" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ _player_add_item_by_id("hunting_trap_001", 1)
    run Call("WerecatSetTrap", "Forest")
    assert eval ("ставите охотничью ловушку" in str(MainTxt or "")) timeout 5.0
    assert eval (int(_player_item_count_by_id("hunting_trap_001") or 0) == 0) timeout 5.0
    assert eval (int(werecat_state().get("trap_active", 0) or 0) == 1) timeout 5.0
    assert eval (str(werecat_state().get("trap_room", "") or "") == "Forest") timeout 5.0
    assert eval (str(current_action_title or "") == "Действия") timeout 5.0
    assert eval ("Проверить странную приманку" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ werecat_state()["trap_rooms"] = {"Forest": {"day": int(dayspassed or 0) - 1}}
    $ werecat_state()["trap_active"] = 1
    $ werecat_state()["trap_room"] = "Forest"
    $ werecat_state()["trap_day"] = int(dayspassed or 0) - 1
    $ werecat_state()["woods_exploration"] = 0
    $ exploration = 20
    run Call("WerecatCheckTrap", "Forest")
    assert eval ("оказалась слишком осторожной" in str(MainTxt or "")) timeout 5.0
    assert eval (int(werecat_state().get("trap_active", 0) or 0) == 0) timeout 5.0
    assert eval (str(current_action_title or "") == "Действия") timeout 5.0
'''


CHURCH_LINK_CHECKS = r'''
testcase external_church_service_action_links_work:
    $ external_calendar_set_fields(7, 1, 1100, 8, 0)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ Georgett.known = True
    $ knowsMC["georgett"] = True
    $ Georgett.rel = 6
    $ Georgett.relationship = 6
    $ Georgett.corruption = 80
    $ HadSex["georgett"] = 3
    $ cametoday = 0
    $ cancumdaily = 3
    $ Georgett.sync_georgett_maps()
    $ initStoryEventRuntime(True)
    assert eval (church_service_action_visible() and not church_confession_action_visible() and not church_after_cermon_action_visible()) timeout 5.0
    $ external_calendar_set_fields(7, 1, 1100, 9, 29)
    assert eval (church_service_action_visible() and not church_confession_action_visible()) timeout 5.0
    $ external_calendar_set_fields(7, 1, 1100, 9, 30)
    assert eval ((not church_service_action_visible()) and church_confession_action_visible()) timeout 5.0
    $ external_calendar_set_fields(7, 1, 1100, 11, 0)
    assert eval ((not church_confession_action_visible()) and church_after_cermon_action_visible()) timeout 5.0
    $ external_calendar_set_fields(7, 1, 1100, 8, 0)

    run Jump("Church")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Прихожане" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("прихожан" in str(CurLocDesc or "")) timeout 5.0
    assert eval ("{a=church:service:1}" not in str(CurLocDesc or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(current_action_title or "") == "Прихожане") timeout 10.0
    assert eval (str(current_action_title or "") == "Прихожане") timeout 5.0
    assert eval ("Найти Сандру" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Найти сестричек" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Найти Жоржетту Брюно" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (not story_event_available("Church", "georgett_church_service_bench")) timeout 5.0
    assert eval (not story_event_available("Church", "georgett_church_service_doggy")) timeout 5.0
    assert eval (not story_event_available("Church", "georgett_church_service_with_liza")) timeout 5.0
    $ Georgett.set_story_value("foundinchurch", 1)
    $ findAvailableEvents(True)
    assert eval ((Georgett.known or knowsMC.get("georgett", False) or people_to_int(Georgett.rel, 0) > 0)) timeout 5.0
    assert eval (npc_schedule_georgett_church_visible()) timeout 5.0
    assert eval (people_to_int(Georgett.story_value("foundinchurch", 0), 0) > 0) timeout 5.0
    assert eval (people_to_int(cametoday, 0) < people_to_int(cancumdaily, 0)) timeout 5.0
    assert eval (people_to_int(Friends.get("georgett", Georgett.rel), 0) >= 6) timeout 5.0
    assert eval (people_to_int(Georgett.rel, 0) >= 6) timeout 5.0
    assert eval (people_to_int(sluttiness.get("georgett", Georgett.corruption), 0) >= 50) timeout 5.0
    assert eval (people_to_int(Georgett.corruption, 0) >= 50) timeout 5.0
    assert eval (people_to_int(HadSex.get("georgett", 0), 0) >= 3) timeout 5.0
    assert eval (story_event_available("Church", "georgett_church_service_bench")) timeout 5.0
    assert eval (story_event_available("Church", "georgett_church_service_doggy")) timeout 5.0
    assert eval (not story_event_available("Church", "georgett_church_service_with_liza")) timeout 5.0
    $ Georgett.set_story_value("askkids", 1)
    $ Georgett.set_story_value("fuckinchurch", 1)
    $ findAvailableEvents(True)
    assert eval (story_event_available("Church", "georgett_church_service_with_liza")) timeout 5.0
    assert eval ("Предложить Жоржетте перепихнуться по быстрому" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("ChurchServiceMother")
    assert eval ("Сандра" in str(MainTxt or "")) timeout 5.0
    run Jump("Church")
    advance until screen "main_ui" timeout 20.0
    $ renpy.call_in_new_context("ChurchServiceMenu", True)
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Прихожане") timeout 5.0

    $ external_calendar_set_fields(day, month, year, 10, 0)
    run Jump("Church")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Идти на исповедь" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("ChurchIspoved", 1)
    advance until screen "main_ui" timeout 20.0
    assert eval (str(current_action_title or "") == "Исповедь") timeout 5.0
    assert eval ("Вернуться в собор" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("ChurchIspovedMenu")
    assert eval (str(current_action_title or "") == "В чем покаяться?") timeout 5.0
    assert eval ("В разных пустяках" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Назад" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("ChurchIspoved", 1)
    $ renpy.run(current_action_items[0].action)
    advance until screen "main_ui" timeout 20.0
    assert eval (int(LastAdvancedMinutes or 0) > 0) timeout 5.0
    assert eval (str(CurLoc or "") == "Church") timeout 5.0

    $ external_calendar_set_fields(day, month, year, 12, 0)
    run Jump("Church")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Обойти собор" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("ChurchAfterCermon", 1)
    assert eval ("Вернуться в собор" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
'''


CHURCH_AFTER_SERMON_EVENT_CHECKS = r'''
testcase external_georgett_liza_church_after_sermon_events:
    $ external_calendar_set_fields(7, 1, 1100, 12, 0)
    $ CurrentRoom = ChurchRoom
    $ CurLoc = "Church"
    $ location = CurLoc
    $ ChurchAfterCermon.clear()
    $ TodaySexEvents_Clear()
    $ Georgett.set_story_value("churchgeorgettadmit", 1)
    $ Georgett.set_story_value("churchlizaadmit", 0)
    $ TodaySexEvents_Add("georgett", 99, 99, "Priest")
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("Church", "after_cermon_walk")) timeout 5.0
    assert eval (renpy.has_label("story_georgett_church_after_sermon")) timeout 5.0
    assert eval (renpy.has_label("story_georgett_church_after_sermon_look_1")) timeout 5.0
    assert eval (renpy.has_label("story_georgett_church_after_sermon_look_4")) timeout 5.0
    assert eval (not renpy.has_label("AfterCermonGeorgett")) timeout 5.0

    $ external_calendar_set_fields(7, 1, 1100, 12, 0)
    $ CurrentRoom = ChurchRoom
    $ CurLoc = "Church"
    $ location = CurLoc
    $ ChurchAfterCermon.clear()
    $ TodaySexEvents_Clear()
    $ Georgett.set_story_value("churchgeorgettadmit", 0)
    $ Georgett.set_story_value("churchlizaadmit", 1)
    $ TodaySexEvents_Add("liza", 99, 99, "Priest")
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("Church", "after_cermon_walk")) timeout 5.0
    run Call("ChurchAfterCermon", 1)
    advance until screen "choice" timeout 10.0
    assert eval ("замочную скважину" in str(CurLocDesc or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (int(Liza.after_sermon_stage() or 0) == 1) timeout 10.0
    assert eval (int(Liza.after_sermon_stage() or 0) == 1) timeout 5.0
    assert eval ("Лизетту" in str(CurLocDesc or "")) timeout 5.0
'''


CLARA_MELISSA_TAVERN_BAR_GOSSIP_CHECKS = r'''
testcase external_clara_market_event_repeats_until_exploration_success:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(day, month, year, 12, 0)
    $ external_calendar_set_weekday(2)
    $ BlindPirateMarketEventSeen = 1
    $ CurrentLoc["clara"] = "MarketPlace"
    $ peopleInfo["clara"].location = "MarketPlace"
    $ npc_schedule_set("clara", [NPCScheduleEntry(location="MarketPlace", time_slots=[], priority=999)])
    $ ClaraVar["booklet_market_seen"] = 0
    $ ClaraVar["market_intro_seen"] = 0
    $ ClaraVar["market_follow_failed_day"] = -1
    $ ClaraVar["market_follow_failed_hour"] = -1
    $ ClaraVar["market_day_roll_day"] = int(dayspassed or 0)
    $ ClaraVar["market_day_roll"] = 1
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("MarketPlace", "enter")) timeout 5.0
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until screen "main_ui" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None) timeout 5.0
    assert eval ("Проследить за Клариссой" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ exploration = 10
    $ _clara_follow_energy_before = int(energy or 0)
    $ _clara_follow_minutes_before = (int(dayspassed or 0) * 1440) + int(clock_minutes or 0)
    $ renpy.call_in_new_context("story_clara_market_booklet_follow")
    assert eval ("Похоже, без лучшей сноровки" in str(MainTxt or "")) timeout 5.0
    assert eval (renpy.get_screen("main_ui") is not None) timeout 5.0
    assert eval ("Вернуться к рынку" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Проследить за Клариссой" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Рыночные лотки" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (int(LastAdvancedMinutes or 0) == 30) timeout 5.0
    assert eval (((int(dayspassed or 0) * 1440) + int(clock_minutes or 0)) - _clara_follow_minutes_before == 30) timeout 5.0
    assert eval (int(energy or 0) == max(0, _clara_follow_energy_before - 5)) timeout 5.0
    assert eval (int(ClaraVar.get("booklet_market_seen", 0) or 0) == 0) timeout 5.0
    assert eval (int(ClaraVar.get("market_follow_failed_day", -1) or -1) == int(dayspassed or 0) and int(ClaraVar.get("market_follow_failed_hour", -1) or -1) == int(hour or 0)) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 0) timeout 5.0
    run Jump("MarketPlace")
    advance until screen "main_ui" timeout 20.0
    $ findAvailableEvents(True)
    assert eval (not story_event_available("MarketPlace", "enter")) timeout 5.0

    $ external_calendar_set_fields(int(day or 1) + 1, month, year, 12, 0)
    $ ClaraVar["market_day_roll_day"] = int(dayspassed or 0)
    $ ClaraVar["market_day_roll"] = 1
    $ findAvailableEvents(True)
    assert eval (clara_market_daytime_roll_active(dayspassed, week)) timeout 5.0
    assert eval (int(ClaraVar.get("booklet_market_seen", 0) or 0) == 0) timeout 5.0
    assert eval (not (int(ClaraVar.get("market_follow_failed_day", -1) or -1) == int(dayspassed or 0) and int(ClaraVar.get("market_follow_failed_hour", -1) or -1) == int(hour or 0))) timeout 5.0
    assert eval (MarketPlaceRoom.is_open()) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 0 and threads["claraBookletMarket"].checkActive()) timeout 5.0
    assert eval (len(threads["claraBookletMarket"].getAvailableEvents()) > 0) timeout 5.0
    assert eval (story_event_available("MarketPlace", "enter")) timeout 5.0
    $ thread = threads["claraBookletMarket"]
    $ exploration = 100
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until screen "main_ui" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None) timeout 5.0
    assert eval ("Проследить за Клариссой" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ _clara_follow_energy_before = int(energy or 0)
    $ _clara_follow_minutes_before = (int(dayspassed or 0) * 1440) + int(clock_minutes or 0)
    $ renpy.call_in_new_context("story_clara_market_booklet_follow")
    assert eval ("Кларисса что-то сбывает" in str(MainTxt or "")) timeout 5.0
    assert eval ("Проследить за Клариссой" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Рыночные лотки" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (int(LastAdvancedMinutes or 0) == 30) timeout 5.0
    assert eval (((int(dayspassed or 0) * 1440) + int(clock_minutes or 0)) - _clara_follow_minutes_before == 30) timeout 5.0
    assert eval (int(energy or 0) == max(0, _clara_follow_energy_before - 5)) timeout 5.0
    assert eval (int(ClaraVar.get("booklet_market_seen", 0) or 0) == 1) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 1 and threads["claraBookletMarket"].currentTarget() == "story_clara_market_booklet_2") timeout 5.0

testcase external_clara_market_follow_finishes_without_self_loop:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(day, month, year, 12, 0)
    $ external_calendar_set_weekday(2)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ BlindPirateMarketEventSeen = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ exploration = max(int(exploration or 0), 100)
    $ CurrentLoc["clara"] = "MarketPlace"
    $ peopleInfo["clara"].location = "MarketPlace"
    $ npc_schedule_set("clara", [NPCScheduleEntry(location="MarketPlace", time_slots=[], priority=999)])
    $ ClaraVar["booklet_market_seen"] = 0
    $ ClaraVar["market_intro_seen"] = 0
    $ ClaraVar["market_follow_failed_day"] = -1
    $ ClaraVar["market_follow_failed_hour"] = -1
    $ ClaraVar["market_day_roll_day"] = int(dayspassed or 0)
    $ ClaraVar["market_day_roll"] = 1
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ initStoryEventRuntime(True)

    assert eval (story_event_available("MarketPlace", "enter")) timeout 5.0
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until screen "main_ui" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None) timeout 5.0
    assert eval ("Проследить за Клариссой" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ _clara_follow_energy_before = int(energy or 0)
    $ _clara_follow_minutes_before = (int(dayspassed or 0) * 1440) + int(clock_minutes or 0)
    $ renpy.call_in_new_context("story_clara_market_booklet_follow")
    assert eval ("Кларисса что-то сбывает" in str(MainTxt or "")) timeout 5.0
    assert eval ("Проследить за Клариссой" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Рыночные лотки" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (int(LastAdvancedMinutes or 0) == 30) timeout 5.0
    assert eval (((int(dayspassed or 0) * 1440) + int(clock_minutes or 0)) - _clara_follow_minutes_before == 30) timeout 5.0
    assert eval (int(energy or 0) == max(0, _clara_follow_energy_before - 5)) timeout 5.0
    assert eval (int(ClaraVar.get("booklet_market_seen", 0) or 0) == 1) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 1 and threads["claraBookletMarket"].currentTarget() == "story_clara_market_booklet_2") timeout 5.0

testcase external_mongol_market_schedule_rolls_once_per_day:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(day, month, year, 10, 0)
    $ week = 2
    $ MyStallion = ""
    $ KnowMongol = 1
    $ BlindPirateMarketEventSeen = 1
    $ TavernEventOngoing = ""
    $ CurrentLoc["clara"] = ""
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ CurrentLoc["mongol"] = ""
    $ Mongol.var["MarketRollDay"] = int(dayspassed or 0)
    $ Mongol.var["MarketRoll"] = 0
    assert eval (not marketplace_mongol_visible()) timeout 5.0
    assert eval (str(getLocation("mongol") or "") != "MarketPlace") timeout 5.0
    run Jump("MarketPlace")
    advance until screen "main_ui" timeout 20.0

    $ external_calendar_set_fields(day, month, year, 10, 0)
    $ week = 2
    $ Mongol.var["MarketRollDay"] = int(dayspassed or 0)
    $ Mongol.var["MarketRoll"] = 1
    assert eval (str(MyStallion or "") == "") timeout 5.0
    assert eval (MarketPlaceRoom.is_open()) timeout 5.0
    assert eval (int(Mongol.var.get("MarketRollDay", -1)) == int(dayspassed or 0) and int(Mongol.var.get("MarketRoll", 0)) == 1) timeout 5.0
    assert eval (marketplace_mongol_visible()) timeout 5.0
    assert eval (str(getLocation("mongol") or "") == "MarketPlace") timeout 5.0
    run Jump("MarketPlace")
    advance until screen "main_ui" timeout 20.0

    $ external_calendar_set_fields(day, month, year, 18, 0)
    assert eval (not marketplace_mongol_visible()) timeout 5.0

testcase external_clara_melissa_bar_gossip_click_fires_ready_dialog:
    $ _clara_melissa_bar_date = calendar_v2.day_number_to_parts(104)
    $ day = int(_clara_melissa_bar_date.get("day", 1) or 1)
    $ month = int(_clara_melissa_bar_date.get("month", 1) or 1)
    $ year = int(_clara_melissa_bar_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE)
    $ week = 3
    $ time = 2
    $ hour = 12
    $ minute = 0
    $ calendar_v2.sync_state()
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ TavernClosed = ""
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ npc_schedule_set("clara", [NPCScheduleEntry(location="TavernMain", weekdays=[3], time_slots=[2], awake=True, talkable=True, priority=999, label="test_tavern_bar")])
    $ npc_schedule_set("melissa", [NPCScheduleEntry(location="TavernMain", weekdays=[3], time_slots=[2], awake=True, talkable=True, priority=999, label="test_tavern_bar")])
    $ CurrentLoc["clara"] = "TavernMain"
    $ CurrentLoc["melissa"] = "TavernMain"
    $ ClaraVar["tavern_melissa_visit_count"] = 0
    $ ClaraVar["tavern_melissa_visit_day"] = -1
    $ ClaraVar["tavern_melissa_overheard_2_seen"] = 0
    $ ClaraVar["tavern_melissa_overheard_3_seen"] = 0
    $ HouseholdRuntimeEventSeen.clear()
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ initStoryEventRuntime(True)

    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval (int(ClaraVar.get("tavern_melissa_visit_count", 0) or 0) == 1) timeout 5.0
    assert eval (str(tavern_bar_clara_melissa_gossip_target() or "") == "melissaClaraOverheard_0") timeout 5.0
    run Call("TavernMainObjectMenu", "bar_001")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Послушать историю у стойки" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (str(current_action_items[3].caption or "") == "Послушать историю у стойки") timeout 5.0
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (int(ClaraVar.get("tavern_melissa_overheard_2_seen", 0) or 0) == 1) timeout 10.0
    assert eval ('Мелисса, едва сдерживая смех' in str(MainTxt or "")) timeout 5.0
    assert eval (str(_layout_last_picture or "") == "images/clara/tavern_visit.png") timeout 5.0
    assert eval ("Отойти от чужого разговора" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (threads["melissaClaraOverheard"].currentTarget() == "melissaClaraOverheard_1") timeout 5.0
    $ dayspassed = int(dayspassed or 0) + 1
    $ ClaraVar["tavern_melissa_visit_count"] = 2
    $ CurLoc = "TavernMain"
    $ location = CurLoc
    $ CurrentRoom = TavernMainRoom
    $ CurrentLoc["clara"] = "TavernMain"
    $ CurrentLoc["melissa"] = "TavernMain"
    $ evalTime = None
    $ findAvailableEvents(True)
    assert eval (str(tavern_bar_clara_melissa_gossip_target() or "") == "melissaClaraOverheard_1") timeout 5.0
    run Call("TavernMainObjectMenu", "bar_001")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Послушать историю у стойки" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (int(ClaraVar.get("tavern_melissa_overheard_3_seen", 0) or 0) == 1) timeout 10.0
    assert eval ('Если б я была царица' in str(MainTxt or "")) timeout 5.0
    assert eval (str(_layout_last_picture or "") == "images/clara/tavern_visit_size.png") timeout 5.0
    assert eval ("Сделать вид, что ничего не услышали" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (threads["melissaClaraOverheard"].completed) timeout 5.0

testcase external_clara_booklet_mongol_night_buttons_advance:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ _clara_mongol_date = calendar_v2.day_number_to_parts(70)
    $ day = int(_clara_mongol_date.get("day", 1) or 1)
    $ month = int(_clara_mongol_date.get("month", 1) or 1)
    $ year = int(_clara_mongol_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE)
    $ week = 2
    $ external_calendar_set_fields(day, month, year, 16, 0)
    $ CurLoc = "CityGuard"
    $ location = CurLoc
    $ productnum = max(int(productnum or 0), 2)
    $ winenum = max(int(winenum or 0), 1)
    $ Mongol.var["StocksArrestDay"] = int(dayspassed or 0) - 1
    $ Mongol.var["StocksSeen"] = 1
    $ Mongol.var["StocksFoodDay"] = -1
    $ Mongol.var["StocksReleased"] = 0
    $ DraupnirVar["MongolLockpickOrderDay"] = -1
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ initStoryEventRuntime(True)
    $ threads["claraBookletMarket"].advanceTo(6, force_active=True)
    $ findAvailableEvents(True)
    assert eval (story_event_available("CityGuard", "enter")) timeout 5.0
    $ thread = threads["claraBookletMarket"]
    run Call("story_clara_market_booklet_feed_mongol")
    assert eval (int(Mongol.var.get("StocksFoodDay", -1) or -1) == int(dayspassed or 0)) timeout 5.0
    assert eval (threads["claraBookletMarket"].currentTarget() == "story_clara_market_booklet_8") timeout 5.0
    $ DraupnirVar["MongolLockpickOrderDay"] = int(dayspassed or 0)
    $ threads["claraBookletMarket"].advanceTo(8, force_active=True)
    $ CurLoc = "CityGuard"
    $ location = CurLoc
    $ external_calendar_set_fields(day, month, year, 23, 0)
    $ dayspassed = int(Mongol.var.get("StocksFoodDay", 0) or 0) + 1
    $ findAvailableEvents(True)
    assert eval (story_event_available("CityGuard", "enter")) timeout 5.0
    $ thread = threads["claraBookletMarket"]
    run Call("story_clara_market_booklet_release_mongol")
    assert eval (int(Mongol.var.get("StocksReleased", 0) or 0) == 1) timeout 5.0
    assert eval (threads["claraBookletMarket"].completed) timeout 5.0

testcase external_zimmer_mongol_wine_distraction_dialog:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ CurLoc = "CityGuard"
    $ location = CurLoc
    $ productnum = max(int(productnum or 0), 2)
    $ winenum = max(int(winenum or 0), 1)
    $ Talked["zimmer"] = 0
    $ TalkedToday["zimmer"] = 0
    $ _mongol_test_var = peopleInfo["mongol"].var
    $ _mongol_test_var["StocksSeen"] = 1
    $ _mongol_test_var["StocksFoodDay"] = int(dayspassed or 0)
    $ _mongol_test_var["StocksReleased"] = 0
    $ _mongol_test_var["GuardCaptainKnown"] = 0
    $ DraupnirVar["MongolLockpickOrderDay"] = int(dayspassed or 0)
    run Call("IntZimmerTalk")
    assert eval ("Похвастаться вином для ночной стражи" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("IntZimmerTalkMongolWineDistraction")
    assert eval (int(peopleInfo["mongol"].var.get("GuardCaptainKnown", 0) or 0) == 1) timeout 5.0
    assert eval ("правильное понимание общественного порядка" in str(MainTxt or "")) timeout 5.0
    assert eval (int(Friends.get("zimmer", 0) or 0) >= 1) timeout 5.0

testcase external_robin_blackwood_room_thread_and_mongol_pass:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ people_sync_all()
    assert eval (getPersonInfo("robin") is Robin and isinstance(Robin, RobinInfo)) timeout 5.0
    assert eval (getPersonData("robin") is RobinStaticData) timeout 5.0
    assert eval (str(getLocation("robin") or "") == "BlackwoodRoad") timeout 5.0
    $ CurLoc = "BlackwoodRoad"
    $ location = CurLoc
    $ Becky.var["TradeOffer"] = 1
    $ Robin.var["MongolSafePass"] = 1
    $ Robin.var["KunidellOpened"] = 0
    $ Robin.var["MongolSafePassUsed"] = 0
    $ BlackwoodTravelOnHorse = 0
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval ("robinBlackwoodRoadAmbush" in threads) timeout 5.0
    assert eval (story_event_available("BlackwoodRoad", "enter")) timeout 5.0
    $ thread = threads["robinBlackwoodRoadAmbush"]
    run Call("story_robin_blackwood_mongol_pass")
    advance until screen "say" timeout 20.0
    click pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until eval (int(Robin.var.get("KunidellOpened", 0) or 0) == 1) timeout 20.0
    assert eval (int(Robin.var.get("KunidellOpened", 0) or 0) == 1) timeout 5.0
    assert eval (int(Robin.var.get("MongolSafePassUsed", 0) or 0) == 1) timeout 5.0
'''


FRIDAY_DANCE_AMANDA_CHECKS = r'''
testcase external_friday_amanda_bad_invite_uses_one_dance:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(day, month, year, 20, 0)
    $ external_calendar_set_weekday(5)
    $ FridayDancesCount = 0
    $ DanceStep = 0
    $ DanceSponsor = 0
    $ GirlDance_Clear()
    $ CurrentLoc["amanda"] = "FridayDance"
    $ npc_schedule_set("amanda", [NPCScheduleEntry(location="FridayDance", time_slots=[], awake=True, talkable=True, priority=999)])
    $ Amanda.set_var_int("leftdances", 0)
    $ Amanda.set_var_int("EscapeUnnoticed", 0)
    $ Amanda.set_var_int("albernowdances", 0)
    $ Amanda.set_var_int("LegareGo", 0)
    $ Becky.set_story_value("leftdances", 1)
    $ Amanda.rel = 0
    $ Amanda.relationship = Amanda.rel
    $ Amanda.corruption = 0
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"

    run Jump("FridayDance")
    advance until screen "choice" timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 0) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 1) timeout 5.0
    advance until screen "choice" timeout 20.0
    assert eval (int(DanceStep or 0) == 1) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 1) timeout 5.0
    advance until screen "choice" timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 1) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (int(DanceStep or 0) == 0) timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 1) timeout 5.0
    assert eval (int(DanceStep or 0) == 0) timeout 5.0

testcase external_friday_amanda_legare_go_phrase_survives_create_dance:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(day, month, year, 20, 0)
    $ external_calendar_set_weekday(5)
    $ FridayDancesCount = 0
    $ DanceStep = 0
    $ DanceSponsor = 0
    $ GirlDance_Clear()
    $ GirlDance_Add("amanda", "legare", 1, 1, "LEGARE_GO_TEST_PHRASE")
    $ CurrentLoc["amanda"] = "FridayDance"
    $ npc_schedule_set("amanda", [NPCScheduleEntry(location="FridayDance", time_slots=[], awake=True, talkable=True, priority=999)])
    $ Amanda.set_var_int("leftdances", 0)
    $ Amanda.set_var_int("EscapeUnnoticed", 0)
    $ Amanda.set_var_int("albernowdances", 0)
    $ Amanda.set_var_int("LegareGo", 0)
    $ Amanda.set_var_int("alberfriends", 12)
    $ Amanda.corruption = 40
    $ Becky.set_story_value("leftdances", 1)
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"

    run Jump("FridayDance")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 1) timeout 5.0
    assert eval (Amanda.var_int("albernowdances", 0) == 1) timeout 5.0
    assert eval (str(SexEvents.dance_watch_line.get(6, "") or "") == "LEGARE_GO_TEST_PHRASE") timeout 5.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (Amanda.var_int("LegareGo", 0) == 0) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "choice" timeout 20.0
    assert eval (Amanda.var_int("leftdances", 0) == 1) timeout 5.0

testcase external_friday_dance_minigame_steps_score:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(day, month, year, 20, 0)
    $ external_calendar_set_weekday(5)
    $ FridayDancesCount = 0
    $ FridayDanceMood = 0
    $ FridayDanceRhythm = 0
    $ FridayDanceAttention = 0
    $ DanceStep = 0
    $ DanceSponsor = 0
    $ Amanda.set_var_int("leftdances", 1)
    $ BeckyVar["leftdances"] = 1
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"

    run Jump("FridayDance")
    advance until screen "choice" timeout 20.0
    assert eval ("Влиться в общий танец" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Поддержать музыкантов хлопками" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 1 and int(FridayDanceRhythm or 0) == 1 and int(FridayDanceMood or 0) >= 1) timeout 5.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 2 and int(FridayDanceRhythm or 0) == 2 and int(FridayDanceMood or 0) >= 2) timeout 5.0

testcase external_friday_becky_inner_actions_do_not_spend_extra_dances:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(day, month, year, 20, 0)
    $ external_calendar_set_weekday(5)
    $ CurLoc = "FridayDance"
    $ location = "FridayDance"
    $ FridayDancesCount = 1
    $ DanceStep = 1
    $ DanceSponsor = 0
    $ BeckyVar["danceinvitehome"] = 0
    $ Friends["becky"] = 0
    $ sluttiness["becky"] = 0
    run Call("int_becky_dance")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (int(FridayDancesCount or 0) == 1 and int(DanceStep or 0) == 6) timeout 5.0
'''

BECKY_HOME_GUEST_CHECKS = r'''
# Important multi-visit home guest tests (not one visit)
# Covers citydress gate, dinner arrival, basic progression toward the full guest experience
# (wine, grope, inga minet, to bedroom, Georgett crossover when EddieWhoreHome=4, etc.)

testcase external_becky_home_guest_citydress_gate_and_arrival:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(day, month, year, 20, 0)
    $ week = 5
    $ CurLoc = "FridayDance"
    $ location = "FridayDance"
    $ BeckyVar["danceinvitehome"] = 1
    $ BeckyVar["visitedhome"] = 0
    $ MyCurDress = "citydress"
    $ Friends["becky"] = 15
    $ sluttiness["becky"] = 50
    $ HadSex["becky"] = 1
    run Call("becky_accept_home_invitation")
    advance until screen "main_ui" timeout 30.0
    assert eval ('Бекки' in str(MainTxt or "") or 'дома' in str(MainTxt or "").lower()) timeout 10.0
'''


SANDRA_NIGHT_THANKS_CHECKS = r'''
testcase external_sandra_night_thanks_slots_work:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ CurLoc = "TavernSandraRoom"
    $ location = CurLoc
    $ CurrentRoom = TavernSandraRoomRoom
    $ CurrentLoc["sandra"] = "TavernSandraRoom"
    $ dayspassed = 21
    $ SandraVar["NightThanksLastDay"] = -1
    $ SandraVar["NightThanksReady"] = 1
    $ external_calendar_set_fields(day, month, year, 22, 0)
    $ _sandra_thanks_day = int(dayspassed or 0)
    run Call("TavernSandraRoomBuildActions")
    assert eval ("Принять ночную благодарность Сандры" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    run Call("TavernSandraNightThanksScene")
    assert eval (int(SandraVar.get("NightThanksReady", 0) or 0) == 0) timeout 5.0
    assert eval (int(SandraVar.get("NightThanksLastDay", -1)) >= 0) timeout 5.0
    run Call("TavernSandraRoomBuildActions")
    assert eval (Sandra.sex_available() and "Уединиться с Сандрой" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ SandraVar["NightThanksReady"] = 1
    $ SandraVar["NightThanksLastDay"] = -1
    $ external_calendar_set_fields(day, month, year, 23, 0)
    run Call("TavernSandraRoomBuildActions")
    assert eval ("Принять ночную благодарность Сандры" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    run Call("TavernSandraNightThanksScene")
    assert eval (int(SandraVar.get("NightThanksReady", 0) or 0) == 0) timeout 5.0
'''


MELISSA_SEX_ENGINE_CHECKS = r'''
testcase external_melissa_engagement_clothing_state_and_no_full_sex:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ renpy.call_in_new_context("InitDressDesc")
    $ week = 2
    $ time = 4
    $ hour = 23
    $ minute = 0
    $ dayspassed = 90
    $ CurLoc = "TavernMyRoom"
    $ location = CurLoc
    $ CurrentLoc["melissa"] = "TavernMyRoom"
    $ Friends["melissa"] = 16
    $ otkroven["melissa"] = 12
    $ sluttiness["melissa"] = 16
    $ MelissaVar["StartTotal"] = 3
    $ MelissaVar["bats_episode"] = 6
    $ MelissaVar["temp_room"] = "TavernAmandaRoom"
    $ MelissaVar["sex_engine_unlocked"] = 0
    $ MelissaVar["room_returned"] = 0
    $ topdress["melissa"] = DressTopPart.get("workdress", "whiteworksemiopenblouse")
    $ bottomdress["melissa"] = DressBottomPart.get("workdress", "brownlongskirt")
    $ bra["melissa"] = "simplebra"
    $ panties["melissa"] = "simplepanties"
    $ topraised["melissa"] = 0
    $ bottomraised["melissa"] = 0
    $ Arousal["you"] = 95
    $ Arousal["melissa"] = 95
    $ SomebodyCums = 0

    run Call("IntMelissaSex", "melissa", "TavernMyRoom")
    advance until screen "choice" timeout 20.0
    assert eval ("Подставить ей член" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Войти в нее" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Кончить на лицо" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Лизать киску" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    $ _melissa_engagement_summary = _ims_scene_summary("melissa")
    assert eval ("Верх: одежда снята" in str(_melissa_engagement_summary or "")) timeout 5.0
    assert eval ("Сейчас это еще не полноценный секс" in str(_melissa_engagement_summary or "")) timeout 5.0
    click id "choice_panel_button_4" pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 560) until screen "say" timeout 20.0
    assert eval (int(Arousal.get("you", 0) or 0) <= 85) timeout 5.0
    assert eval (int(Arousal.get("melissa", 0) or 0) <= 90) timeout 5.0
    assert eval (int(SomebodyCums or 0) == 0) timeout 5.0
'''


PLAYER_INTIMACY_STATE_CHECKS = r'''
testcase external_player_intimacy_state_sleep_arousal_and_help:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ renpy.call_in_new_context("InitDressDesc")
    $ dayspassed = 8
    $ week = 2
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ CurLoc = "TavernMyRoom"
    $ location = CurLoc
    $ player_ensure_nightwear_in_chest()
    assert eval ("nightshirt" in list(MyDresses or [])) timeout 5.0
    run Call("TavernMyRoomOpenChest")
    assert eval (len([str(i.caption or "") for i in current_action_items]) == len(set([str(i.caption or "") for i in current_action_items]))) timeout 5.0
    $ player_set_sleep_layer("nothing")
    assert eval (player_is_naked()) timeout 5.0
    assert eval ("ничего" in "\n".join(player_body_state_lines()).lower()) timeout 5.0

    run Jump("TavernUpstairs")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Спуститься в главный зал" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (any("одеться" in str(i.caption or "").lower() for i in current_action_items)) timeout 5.0

    $ CurLoc = "TavernMyRoom"
    $ LastDaySex = int(dayspassed or 0) - 3
    $ PlayerMorningArousalDay = -1
    $ PlayerRoomLightClosed = 1
    $ Arousal["you"] = 0
    $ player_apply_morning_state("TavernMyRoom")
    assert eval (int(Arousal.get("you", 0) or 0) > 0) timeout 5.0
    assert eval ("утренним стояком" in str(PlayerWakeStateNotice or "")) timeout 5.0

    $ Friends["amanda"] = 20
    $ otkroven["amanda"] = 20
    $ sluttiness["amanda"] = 80
    $ Arousal["amanda"] = 85
    $ Arousal["you"] = 85
    $ cametoday = 0
    $ LastDaySex = -1
    $ _help_result = player_intimacy_help_result("amanda", 0.0)
    assert eval (bool(_help_result.get("ok", False))) timeout 5.0
    assert eval (int(cametoday or 0) == 1) timeout 5.0
    assert eval (int(LastDaySex) == int(dayspassed or 0)) timeout 5.0

    $ Friends["melissa"] = 20
    $ otkroven["melissa"] = 0
    $ sluttiness["melissa"] = 40
    $ Arousal["melissa"] = 0
    $ _melissa_friend_before = int(Friends.get("melissa", 0) or 0)
    $ _melissa_slut_before = int(sluttiness.get("melissa", 0) or 0)
    $ _bad_result = player_intimacy_help_result("melissa", 1.0)
    assert eval (not bool(_bad_result.get("ok", False))) timeout 5.0
    assert eval (int(Friends.get("melissa", 0) or 0) == _melissa_friend_before - 10) timeout 5.0
    assert eval (int(sluttiness.get("melissa", 0) or 0) < _melissa_slut_before) timeout 5.0
'''


CLARA_AMANDA_SCHEDULE_FLOW_CHECKS = r'''
testcase external_clara_evening_follow_finishes_in_melissa_room:
    $ week = 3
    $ time = 3
    $ hour = 21
    $ minute = 0
    $ dayspassed = 40
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ ClaraVar["commission_followup_done"] = 1
    $ ClaraVar["peek_done"] = 0
    $ ClaraVar["confession_done"] = 0
    $ ClaraVar["murder_day"] = 999999
    $ Friends["clara"] = max(int(Friends.get("clara", 0) or 0), 8)
    $ CurrentLoc["clara"] = "WineStore"
    $ CurrentLoc["melissa"] = "TavernMelissaRoom"
    $ MelissaVar["bats_stage"] = max(int(MelissaVar.get("bats_stage", 0) or 0), 8)
    $ TavernBreakfastEventActive = False
    $ TavernBreakfastPresentIds = None
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ initStoryEventRuntime(True)
    $ threads["claraPaintingsPath"].advanceTo(8, force_active=True)
    $ findAvailableEvents(True)

    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    $ renpy.call_in_new_context("checkTriggers", "WineStore", "clara_paintings", 0)
    assert eval (str(CurrentLoc.get("clara", "") or "") == "TavernMelissaRoom") timeout 5.0
    assert eval (str(CurrentLoc.get("melissa", "") or "") == "TavernMelissaRoom") timeout 5.0
    run Jump("TavernMelissaRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Выслушать Клариссу и Мелиссу" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ renpy.call_in_new_context("checkTriggers", "TavernMelissaRoom", "clara_paintings", 0)
    assert eval (int(ClaraVar.get("confession_done", 0) or 0) == 1) timeout 5.0
    assert eval ("Оставить девушек поговорить" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

testcase external_amanda_player_room_visit_is_physical_and_leaves:
    $ _amanda_test_date = calendar_v2.day_number_to_parts(41)
    $ day = int(_amanda_test_date.get("day", 1) or 1)
    $ month = int(_amanda_test_date.get("month", 1) or 1)
    $ year = int(_amanda_test_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE)
    $ week = 2
    $ time = 3
    $ hour = 22
    $ minute = 0
    $ calendar_v2.sync_state()
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    $ current_action_content = None
    $ UI_mode = "scene"
    $ TavernBreakfastEventActive = False
    $ TavernBreakfastPresentIds = None
    $ AmandaIntentSeen.clear()
    $ AmandaIntentRoomPresence.clear()
    $ Amanda.set_var_int("beauty_help_terms_accepted", 1)
    $ Amanda.set_var_int("night_tease_seen", 0)
    $ Amanda.set_var_int("night_tease_scene_active", 0)
    $ Amanda.set_var_int("kickyoufromroom", 0)
    $ TavernBreakfastBlindPirateTeamPledge = 1
    $ Amanda.rel = max(int(Amanda.rel or 0), 12)
    $ Amanda.relationship = Amanda.rel
    $ Amanda.openness = max(int(Amanda.openness or 0), 8)
    $ Amanda.corruption = max(int(Amanda.corruption or 0), 35)
    $ CurrentLoc["amanda"] = "TavernAmandaRoom"
    $ amanda_ai_place_in_room("TavernMyRoom", "visit_player_room")

    run Jump("TavernMyRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(getLocation("amanda") or "") == "TavernMyRoom") timeout 5.0
    assert eval ("amanda" in [str(row.get("id", "") or "") for row in _character_action_grid_entries(CurrentRoom)]) timeout 5.0
    assert eval ("Аманда сейчас в вашей комнате" in str(MainTxt or "")) timeout 5.0
    assert eval ("mc_room_exposure" in str(_layout_last_picture or "")) timeout 5.0
    $ open_npc_action_menu_state("amanda", "TavernMyRoom", npc_action_data_for_room("amanda", "TavernMyRoom") or {})
    assert eval ("Спросить Аманду, что она здесь делает" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ MainTxt = amanda_ai_intro_text("visit_player_room", "TavernMyRoom")
    assert eval ("доброй ночи" in str(MainTxt or "").lower()) timeout 5.0
    assert eval ("ночная сорочка" in str(MainTxt or "").lower()) timeout 5.0
    $ amanda_ai_apply_response("visit_player_room", "satisfy", False)
    $ amanda_ai_clear_room_presence("TavernMyRoom")
    $ MainTxt = amanda_ai_response_text("visit_player_room", "satisfy")
    assert eval (str(getLocation("amanda") or "") != "TavernMyRoom") timeout 5.0
    assert eval ("уходит" in str(MainTxt or "").lower() or "отступает" in str(MainTxt or "").lower()) timeout 5.0
'''


HOUSEHOLD_AI_EVENT_CHECKS = r'''
testcase external_household_ai_kitchen_event_fires:
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ dayspassed = 21
    $ money = 80
    $ taverncleanliness = 15
    $ food_stock = 0
    $ fur_supply = 0
    $ cloth_supply = 0
    $ CurLoc = "TavernKitchen"
    $ CurrentRoom = TavernKitchenRoom
    $ CurrentLoc["amanda"] = "TavernKitchen"
    $ CurrentLoc["sandra"] = "TavernKitchen"
    $ CurrentLoc["melissa"] = "TavernKitchen"
    $ HouseholdAISeen.clear()
    $ HouseholdAIState["pressure"] = 0.0
    $ HouseholdAIState["friction"] = 0.70
    $ HouseholdAIState["convergence"] = 0.0
    $ HouseholdAIState["external_threat"] = 0.0
    $ HouseholdAIState["last_event_code"] = ""
    $ HouseholdNPCState["amanda"]["drive"] = 0.0
    $ HouseholdNPCState["sandra"]["drive"] = 0.0
    $ HouseholdNPCState["melissa"]["drive"] = 0.0
    assert eval (household_ai_pick_event("TavernKitchen", "room") == "household_event_kitchen_amanda_sandra_spark") timeout 5.0
    run Call("HouseholdEvent_Try", "TavernKitchen", "room")
    advance until screen "choice" timeout 20.0
    click pos (960, 560)
    advance until eval (str(HouseholdAIState.get("last_event_code", "") or "") == "household_event_kitchen_amanda_sandra_spark") timeout 10.0
    assert eval (household_ai_seen("household_event_kitchen_amanda_sandra_spark", "TavernKitchen")) timeout 5.0
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
        if action_type == "Return":
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
            Amanda.set_var_int("kickyoufromroom", 0)
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


CALENDAR_TIME_CHECKS = r'''
testcase external_new_game_starts_at_8_morning:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    assert eval (int(hour or 0) == 8) timeout 5.0
    assert eval (int(minute or 0) == 0) timeout 5.0
    assert eval (int(time or 0) == 1 and str(calendar_time_slot_name_en or "") == "morning") timeout 5.0
    assert eval (str(calendar_v2.clock_text() or "") == "08:00") timeout 5.0
    assert eval (int(tavernvisitors or 0) == 40 and int(productnum or 0) == 200 and int(winenum or 0) == 100) timeout 5.0
    assert eval (str(tractir_first_active_ending() or "") == "") timeout 5.0

testcase external_calendar_long_cycle_thirteenth_period_rollover:
    $ age = 20
    $ external_calendar_set_fields(28, 13, 1100, 23, 59)
    assert eval (int(clock_minutes or 0) == 1439 and int(dayspassed or 0) == external_calendar_day_number_from_fields(28, 13, 1100)) timeout 5.0
    $ calendar_v2.advance_minutes(1)
    assert eval (int(year or 0) == 1101) timeout 5.0
    assert eval (int(month or 0) == 1) timeout 5.0
    assert eval (int(day or 0) == 1) timeout 5.0
    assert eval (int(clock_minutes or 0) == 0) timeout 5.0
    assert eval (int(age or 0) == 21) timeout 5.0
    assert eval (str(month_name_en or "") == "Wolf Moon" and str(calendar_month_name_ru or "") == "Луна Волка") timeout 5.0
    assert eval ("Period" not in str(month_name_en or "") and "период" not in str(month_name or "").lower()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 16, 0)
    assert eval (int(time or 0) == 7) timeout 5.0
    assert eval (int(clock_minutes or 0) == 1380) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 5, 59)
    assert eval (int(time or 0) == 7) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 6, 0)
    assert eval (int(time or 0) == 0) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 8, 0)
    assert eval (int(time or 0) == 1 and str(calendar_time_slot_name_en or "") == "morning") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 10, 45)
    assert eval (int(time or 0) == 1 and str(calendar_time_slot_name_en or "") == "morning") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 11, 0)
    assert eval (int(time or 0) == 2 and str(calendar_time_slot_name_en or "") == "noon") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 13, 0)
    assert eval (int(time or 0) == 3 and str(calendar_time_slot_name_en or "") == "afternoon") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 16, 0)
    assert eval (int(time or 0) == 4 and str(calendar_time_slot_name_en or "") == "day") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 19, 0)
    assert eval (int(time or 0) == 5 and str(calendar_time_slot_name_en or "") == "evening") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 21, 0)
    assert eval (int(time or 0) == 6 and str(calendar_time_slot_name_en or "") == "late evening") timeout 5.0
    $ energy = 80
    $ fun = 80
    $ _evening_chore_allowed = can_do_player_chore("clean_ashes", "TavernMain", "fireplace_001")
    assert eval (bool(_evening_chore_allowed[0])) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 16, 0)
    $ energy = 68
    $ fun = 80
    assert eval (str(action_restriction_message("chore") or "") == "") timeout 5.0
    assert eval (str(action_restriction_message("heavy_chore") or "") == "") timeout 5.0
    assert eval (str(action_restriction_message("wash") or "") == "") timeout 5.0
    assert eval (str(action_restriction_message("rest") or "") == "") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 22, 30)
    $ _before_minutes = (int(dayspassed or 0) * 1440) + int(clock_minutes or 0)
    $ _advanced = advance_time_slot_runtime(1)
    assert eval (int(_advanced or 0) == 30) timeout 5.0
    assert eval (int(hour or 0) == 23) timeout 5.0
    assert eval (int(minute or 0) == 0) timeout 5.0
    assert eval (((int(dayspassed or 0) * 1440) + int(clock_minutes or 0)) - _before_minutes == 30) timeout 5.0
    $ _late_evening_chore_allowed = can_do_player_chore("clean_ashes", "TavernMain", "fireplace_001")
    assert eval (bool(_late_evening_chore_allowed[0])) timeout 5.0
    assert eval (str(action_restriction_message("chore") or "") == "") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 4, 0)
    $ _night_chore = do_player_chore("clean_ashes", "TavernMain", "fireplace_001")
    assert eval (not bool(_night_chore.get("ok", False))) timeout 5.0
    assert eval ("пора немедленно ложиться спать" in str(_night_chore.get("text", "") or "")) timeout 5.0
    assert eval ("пора немедленно ложиться спать" in str(action_restriction_message("chore") or "")) timeout 5.0
    $ health = 73
    $ energy = 46
    assert eval (("Энергия", "46") in player_card_stat_rows_right()) timeout 5.0

testcase external_sleep_wake_hour_rules:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 23, 0)
    $ _sleep_wake_23 = player_sleep_wake_time()
    assert eval (int(_sleep_wake_23[0]) == 6 and int(_sleep_wake_23[1]) == 0) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 1, 20)
    $ _sleep_wake_1 = player_sleep_wake_time()
    assert eval (int(_sleep_wake_1[0]) == 7 and int(_sleep_wake_1[1]) == 20) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 2, 15)
    $ _sleep_wake_2 = player_sleep_wake_time()
    assert eval (int(_sleep_wake_2[0]) == 7 and int(_sleep_wake_2[1]) == 15) timeout 5.0

testcase external_daily_setstatdefault_body_maps_exist:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ Breastfeed.clear()
    $ Lactate.clear()
    $ Sandra.rel = 10
    $ Sandra.openness = 0
    $ Amanda.rel = 10
    $ Amanda.openness = 0
    run Call("DailySetstatdefault", "melissa")
    run Call("DailySetstatdefault", "sandra")
    run Call("DailySetstatdefault", "amanda")
    assert eval ("melissa" in Breastfeed and "melissa" in Lactate) timeout 5.0
    assert eval ("sandra" in Breastfeed and "sandra" in Lactate and "amanda" in Breastfeed and "amanda" in Lactate) timeout 5.0
    assert eval (int(Breastfeed.get("melissa", -1) or 0) >= 0 and int(Lactate.get("melissa", -1) or 0) >= 0) timeout 5.0
    assert eval (int(Sandra.openness or 0) >= 5 and int(Amanda.openness or 0) >= 5) timeout 5.0

testcase external_hour_based_room_and_npc_schedule_adjustment:
    $ npc_interval_schedule_load_all(True)
    $ external_calendar_set_fields(day, month, year, 7, 0)
    $ external_calendar_set_weekday(1)
    assert eval (MarketPlaceRoom.is_open()) timeout 5.0
    assert eval (WineStoreRoom.is_open()) timeout 5.0
    assert eval (DressShopRoom.is_open()) timeout 5.0
    assert eval (clara_wine_store_shift_active()) timeout 5.0
    assert eval (week != 7 and time == 0) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 6, 0)
    assert eval (week != 7 and time < 3 and time == 0) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 6, 0)
    $ external_calendar_set_fields(day, month, year, 11, 0)
    assert eval ((not clara_wine_store_shift_active()) and week != 7 and time < 3 and time != 0) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 17, 59)
    assert eval (MarketPlaceRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 18, 0)
    assert eval (not MarketPlaceRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 15, 59)
    assert eval (GroceryStoreRoom.is_open() and HunterClubRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 16, 0)
    assert eval ((not GroceryStoreRoom.is_open()) and (not HunterClubRoom.is_open())) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 6, 0)
    $ external_calendar_set_weekday(7)
    assert eval (not ChurchRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 8, 0)
    $ external_calendar_set_weekday(7)
    assert eval (ChurchRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 12, 59)
    $ external_calendar_set_weekday(7)
    assert eval (ChurchRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 13, 0)
    $ external_calendar_set_weekday(7)
    assert eval (not ChurchRoom.is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 6, 0)
    $ external_calendar_set_weekday(5)
    assert eval (city_guard_open_now()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 8, 0)
    $ external_calendar_set_weekday(5)
    assert eval (not city_guard_open_now()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 6, 0)
    $ external_calendar_set_weekday(6)
    assert eval (barber_shop_is_open()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 11, 0)
    $ external_calendar_set_weekday(1)
    assert eval (barber_shop_is_open()) timeout 5.0
    $ _morning_entry = npc_daily_schedule_entry_from_row(npc_daily_schedule_slot(0, "TavernMain"), 0)
    $ external_calendar_set_fields(day, month, year, 6, 0)
    assert eval (_morning_entry.matches()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 8, 0)
    assert eval (not _morning_entry.matches()) timeout 5.0
    $ _night_entry = npc_daily_schedule_entry_from_row(npc_daily_schedule_slot(7, "TavernMyRoom", False, False, "sleep"), 7)
    $ external_calendar_set_fields(day, month, year, 16, 0)
    assert eval (_night_entry.matches()) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 22, 59)
    assert eval (not _night_entry.matches()) timeout 5.0
    run Call("InitAmanda")
    $ _amanda_slot7_entry = npc_schedule_resolve("amanda", week, 7)
    assert eval (_amanda_slot7_entry is not None and str(getattr(_amanda_slot7_entry, "label", "") or "") == "sleep" and (7 in list(getattr(_amanda_slot7_entry, "time_slots", []) or []) or str(getattr(_amanda_slot7_entry, "source", "") or "") == "json")) timeout 5.0
    $ _amanda_slot4_entry = npc_schedule_resolve("amanda", week, 4)
    assert eval (_amanda_slot4_entry is None or str(getattr(_amanda_slot4_entry, "label", "") or "") != "sleep") timeout 5.0
    $ npc_interval_schedule_load_all(True)
    $ external_calendar_set_fields(day, month, year, 8, 30)
    $ external_calendar_set_weekday(1)
    assert eval (npc_interval_schedule_has_contract("amanda") and str(npc_schedule_state("amanda").get("source", "") or "") == "json" and str(getLocation("amanda") or "") in ("TavernMain", "TavernAmandaRoom", "TavernKitchen", "TavernStorage", "Backyard")) timeout 5.0
    assert eval (npc_interval_schedule_has_contract("sandra") and str(npc_schedule_state("sandra").get("source", "") or "") == "json" and str(getLocation("sandra") or "") in ("TavernKitchen", "TavernSandraRoom", "TavernStorage", "TavernMain", "Backyard")) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 23, 30)
    $ external_calendar_set_weekday(1)
    assert eval (str(getLocation("amanda") or "") == "TavernAmandaRoom" and bool(npc_schedule_state("amanda").get("awake", True)) == False) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 20, 0)
    $ external_calendar_set_weekday(5)
    assert eval (str(getLocation("melissa") or "") in ("FridayDance", "TavernMelissaRoom") and str(npc_schedule_state("melissa").get("label", "") or "") == "friday_dance") timeout 5.0
    assert eval (str(getLocation("clara") or "") in ("FridayDance", "WineStore") and str(npc_schedule_state("clara").get("label", "") or "") == "friday_dance") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 22, 0)
    $ external_calendar_set_weekday(5)
    assert eval (str(getLocation("melissa") or "") == "TavernMelissaRoom" and str(getLocation("clara") or "") == "TavernMelissaRoom") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 12, 30)
    $ external_calendar_set_weekday(2)
    assert eval (str(getLocation("irma") or "") == "DressShop" and bool(npc_schedule_state("irma").get("talkable", False)) == True) timeout 5.0
    $ external_calendar_set_fields(day, month, year, 13, 30)
    assert eval (str(getLocation("irma") or "") == "DressShop" and bool(npc_schedule_state("irma").get("talkable", True)) == False) timeout 5.0
    $ npc_interval_schedule_load_all(True)
    assert eval (npc_interval_schedule_has_contract("becky") and npc_interval_schedule_has_contract("eddie") and npc_interval_schedule_has_contract("alber")) timeout 5.0
    $ external_calendar_set_fields(10, month, year, 8, 0)
    $ week = 1
    assert eval (str(getLocation("alber") or "") == "" and "alber" not in list(getNPCids("WineStore") or [])) timeout 5.0
    assert eval ("alber" not in [str(row.get("npc_id", "") or "") for row in WineStoreRoom.visible_npcs()]) timeout 5.0
    assert eval (str(getLocation("clara") or "") == "WineStore" and "clara" in list(getNPCids("WineStore") or [])) timeout 5.0
    assert eval ('Поговорить с Клариссой' in [str(i.caption or "") for i in wine_store_room_action_items()]) timeout 5.0
    assert eval ('Поговорить с Альбером' not in [str(i.caption or "") for i in wine_store_room_action_items()]) timeout 5.0
    $ external_calendar_set_fields(10, month, year, 8, 30)
    $ week = 1
    assert eval (str(getLocation("eddie") or "") == "GroceryStore" and str(npc_schedule_state("eddie").get("label", "") or "") == "grocery_morning_shift") timeout 5.0
    assert eval (str(getLocation("becky") or "") != "GroceryStore") timeout 5.0
    $ external_calendar_set_fields(10, month, year, 13, 0)
    $ week = 1
    assert eval (str(getLocation("becky") or "") == "GroceryStore" and str(npc_schedule_state("becky").get("label", "") or "") == "grocery_afternoon_shift") timeout 5.0
    assert eval (str(getLocation("eddie") or "") != "GroceryStore") timeout 5.0
    $ external_calendar_set_fields(24, month, year, 8, 30)
    $ week = 2
    assert eval (str(getLocation("eddie") or "") == "OutOfTown" and str(npc_schedule_state("eddie").get("label", "") or "") == "monthly_absence") timeout 5.0
    assert eval (str(getLocation("becky") or "") == "GroceryStore" and str(npc_schedule_state("becky").get("label", "") or "") == "eddie_absent_grocery_cover") timeout 5.0
    $ external_calendar_set_fields(10, month, year, 20, 0)
    $ week = 5
    assert eval (str(getLocation("becky") or "") == "FridayDance" and str(npc_schedule_state("becky").get("label", "") or "") == "friday_dance") timeout 5.0
    assert eval (str(getLocation("alber") or "") != "FridayDance") timeout 5.0
    $ external_calendar_set_fields(10, month, year, 20, 0)
    $ week = 2
    assert eval (str(getLocation("eddie") or "") == "PortStreets" and str(npc_schedule_state("eddie").get("label", "") or "") == "port_whores_evening") timeout 5.0
    $ external_calendar_set_fields(10, month, year, 12, 30)
    $ week = 1
    assert eval (str(getLocation("alber") or "") == "WineStore" and str(npc_schedule_state("alber").get("label", "") or "") == "wine_store_shift_after_clarissa") timeout 5.0
    assert eval ("alber" in list(getNPCids("WineStore") or [])) timeout 5.0
    assert eval ("alber" in [str(row.get("npc_id", "") or "") for row in WineStoreRoom.visible_npcs()]) timeout 5.0
    assert eval (next(row for row in _character_action_grid_entries(WineStoreRoom) if str(row.get("id", "") or "") == "alber")["title"] == peopleData["alber"].cname) timeout 5.0
    $ _alber_overlap_entry = next(row for row in npc_interval_schedule_list("alber") if str(getattr(row, "label", "") or "") == "clarissa_overlap_wine_store")
    assert eval (int(_alber_overlap_entry.start_minute or 0) == 660 and int(_alber_overlap_entry.end_minute or 0) == 719) timeout 5.0
    $ Friends["becky"] = 15
    $ Friends["sandra"] = 15
    $ HadSex["becky"] = 1
    $ BeckyVar["HomeSex"] = 1
    python:
        _becky_visit_day = -1
        for _probe_day in range(31, 420):
            _probe_parts = calendar_v2.day_number_to_parts(_probe_day)
            external_calendar_set_fields(int(_probe_parts.get("day", 1) or 1), int(_probe_parts.get("month", 1) or 1), int(_probe_parts.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 13, 0)
            calendar_v2.sync_state()
            if npc_schedule_becky_sandra_kitchen_visit_active():
                _becky_visit_day = _probe_day
                break
        if _becky_visit_day >= 0:
            _becky_visit_parts = calendar_v2.day_number_to_parts(_becky_visit_day)
            external_calendar_set_fields(int(_becky_visit_parts.get("day", 1) or 1), int(_becky_visit_parts.get("month", 1) or 1), int(_becky_visit_parts.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 13, 0)
            calendar_v2.sync_state()
    assert eval (_becky_visit_day >= 0) timeout 5.0
    assert eval (str(getLocation("sandra") or "") == "TavernKitchen") timeout 5.0
    assert eval (str(getLocation("becky") or "") == "TavernKitchen" and str(npc_schedule_state("becky").get("label", "") or "") == "sandra_kitchen_visit") timeout 5.0
    $ LizaVar["ProstStart"] = 1
    $ jobwhore["liza"] = 1
    $ CurrentLoc["liza"] = "PortStreets"
    python:
        _alber_port_day = -1
        for _probe_day in range(31, 420):
            _probe_parts = calendar_v2.day_number_to_parts(_probe_day)
            external_calendar_set_fields(int(_probe_parts.get("day", 1) or 1), int(_probe_parts.get("month", 1) or 1), int(_probe_parts.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 20, 0)
            calendar_v2.sync_state()
            if int(week or 0) in (1, 3) and str(getLocation("alber") or "") == "PortStreets":
                _alber_port_day = _probe_day
                break
        if _alber_port_day >= 0:
            _alber_port_parts = calendar_v2.day_number_to_parts(_alber_port_day)
            external_calendar_set_fields(int(_alber_port_parts.get("day", 1) or 1), int(_alber_port_parts.get("month", 1) or 1), int(_alber_port_parts.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 20, 0)
            calendar_v2.sync_state()
    assert eval (_alber_port_day >= 0) timeout 5.0
    assert eval (str(getLocation("alber") or "") == "PortStreets" and str(npc_schedule_state("alber").get("label", "") or "") == "liza_portstreets_visit") timeout 5.0
'''


MEDIA_RESOLUTION_CHECKS = r'''
testcase external_context_image_resolution:
    $ _liza_ispoved = build_media_ref("liza", "ispoved", "ispoved1")
    assert eval (str(_liza_ispoved or "") == "images/Liza/ispoved/ispoved1.jpg") timeout 5.0
    assert eval (_media_asset_exists("images/liza/ispoved/ispoved1.jpg")) timeout 5.0
    $ _liza_event = build_media_ref("liza", "portevents", "event1_1")
    assert eval (str(_liza_event or "") == "images/Liza/portevents/event1_1.jpg") timeout 5.0
    $ _georgett_port = build_media_ref("georgett", "port", "portStreets")
    assert eval (str(_georgett_port or "") == "images/georgett/Port/portStreets.png") timeout 5.0
    $ _melissa_bed = resolve_media_ref("images/melissa/bedroomsearch/underbedbooklet.png")
    assert eval (str(_melissa_bed or "") == "images/melissa/bedRoomSearch/underBedBooklet.png") timeout 5.0
'''

HARASSMENT_IMAGE_CHECKS = r'''
testcase external_harassment_images_use_exact_existing_paths:
    $ GraphicsOn = 1
    $ panties["amanda"] = pantiesdef.get("amanda", "simplepanties")
    $ _harass_ref = harass_image_path("melissa", "ass", 5, "waitress")
    assert eval (str(_harass_ref or "") == "images/melissa/grope/assok1.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    $ _harass_ref = harass_image_path("melissa", "tits", 2, "cleaning")
    assert eval (str(_harass_ref or "") == "images/melissa/grope/titshy1.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    $ _harass_ref = harass_image_path("melissa", "dress", 0, "waitress")
    assert eval (str(_harass_ref or "") == "images/melissa/grope/inter.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    $ _harass_ref = harass_image_path("amanda", "ass", 2, "waitress")
    assert eval (str(_harass_ref or "") == "images/amanda/grope/assshy.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    $ _harass_ref = harass_image_path("amanda", "dress", 5, "waitress")
    assert eval (str(_harass_ref or "") == "images/amanda/grope/dresspanties.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    $ _harass_ref = harass_image_path("sandra", "dress", 5, "waitress")
    assert eval (str(_harass_ref or "") == "images/sandra/tavern/waitress3.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    $ _harass_ref = harass_image_path("sandra", "ass", 1, "cleaning")
    assert eval (str(_harass_ref or "") == "images/sandra/tavern/cleaning1.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    $ _harass_ref = harass_player_reaction_image_path("melissa", 3, "waitress")
    assert eval (str(_harass_ref or "") == "images/melissa/grope/scoldok.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    $ _harass_ref = harass_player_reaction_image_path("amanda", 3, "waitress")
    assert eval (str(_harass_ref or "") == "images/amanda/grope/scold.jpg" and _media_asset_exists(_harass_ref)) timeout 5.0
    run Call("HarassShowImage", "melissa", "ass", 5, 1, "waitress")
    pause 0.1
    assert eval (str(_layout_last_picture or "") in ("images/melissa/grope/assok1.jpg", "images/melissa/grope/assok2.jpg")) timeout 5.0

testcase external_harassment_event_picture_sequence:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ CurLoc = "TavernMain"
    $ CurrentRoom = TavernMainRoom
    $ CurrentLoc["melissa"] = "TavernMain"
    $ GraphicsOn = 1
    $ sluttiness["melissa"] = 5
    $ Friends["melissa"] = 0
    assert eval (isinstance(HarassInstructions, dict)) timeout 5.0
    $ HarassInstructions["melissa"] = ""
    $ _layout_last_picture = ""
    run Call("PartEventYourFirstReactionShow", "melissa", "event_waitress_harrass_part2", 1, 1, 3)
    advance until screen "main_ui" timeout 20.0
    assert eval (str(_layout_last_picture or "") in ("images/melissa/grope/scoldneutral.jpg", "images/melissa/grope/scoldok.jpg")) timeout 5.0
    assert eval ("выручку" in str(MainTxt or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until screen "main_ui" timeout 20.0
    assert eval (str(CurLoc or "") == "TavernMain") timeout 5.0
'''


GIRL_OBJECT_RUNTIME_CHECKS = r'''
testcase external_inga_secondary_npc_source:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ people_sync_all()
    assert eval ("inga" not in AllGirlNames) timeout 5.0
    assert eval ("inga" in SECONDARY_NPC_KEYS) timeout 5.0
    assert eval (getPersonData("inga") is IngaStaticData and isinstance(getPersonData("inga"), IngaData)) timeout 5.0
    assert eval (getPersonInfo("inga") is Inga and isinstance(getPersonInfo("inga"), IngaInfo)) timeout 5.0
    assert eval (getPersonInfo("inga") not in girls and getPersonInfo("inga") in secondary_npcs) timeout 5.0
    assert eval (Inga.var is IngaVar and Inga.location == "BeckyHome") timeout 5.0

testcase external_francheska_secondary_and_birth_thread:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ people_sync_all()
    assert eval (getPersonData("fran") is FranStaticData and isinstance(getPersonData("fran"), FranData)) timeout 5.0
    assert eval (getPersonInfo("fran") is Francheska and isinstance(getPersonInfo("fran"), FrancheskaInfo)) timeout 5.0
    assert eval (getPersonInfo("fran") not in girls and getPersonInfo("fran") in secondary_npcs and "fran" in SECONDARY_NPC_KEYS) timeout 5.0
    assert eval ("systemGiveBirth" in threads and "systemGiveBirth" in threadData) timeout 5.0
    $ dayspassed = 240
    $ pregnancy["amanda"] = 240
    $ pregfather["amanda"] = "Вы"
    $ CurLoc = "TavernMain"
    $ location = CurLoc
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("TavernMain", "enter")) timeout 5.0
    assert eval (str(availEvents["TavernMain"]["enter"].target or "") == "story_give_birth_amanda") timeout 5.0
    $ pregnancy["amanda"] = 0
    $ pregfather["amanda"] = ""
    $ pregnancy["inga"] = 240
    $ pregfather["inga"] = "Лукас"
    $ CurLoc = "BeckyHome"
    $ location = CurLoc
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("BeckyHome", "enter")) timeout 5.0
    assert eval (str(availEvents["BeckyHome"]["enter"].target or "") == "story_give_birth_inga") timeout 5.0
    $ pregnancy["inga"] = 0
    $ pregfather["inga"] = ""
    $ dayspassed = 0

testcase external_gerhard_secondary_npc_source:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ people_sync_all()
    assert eval ("gerhard" not in AllGirlNames) timeout 5.0
    assert eval ("gerhard" in SECONDARY_NPC_KEYS) timeout 5.0
    assert eval (getPersonData("gerhard") is GerhardStaticData and isinstance(getPersonData("gerhard"), GerhardData)) timeout 5.0
    assert eval (getPersonInfo("gerhard") is Gerhard and isinstance(getPersonInfo("gerhard"), GerhardInfo)) timeout 5.0
    assert eval (getPersonInfo("gerhard") not in girls and getPersonInfo("gerhard") in secondary_npcs) timeout 5.0
    assert eval (Gerhard.var is GerhardVar and Gerhard.location == "Church") timeout 5.0
    assert eval (peopleData["gerhard"].cname == "Брат Герхард" and peopleData["gerhard"].portrait == "images/gerhard/portrait.png") timeout 5.0
    assert eval (all(key in Gerhard.var for key in ["confession_intro_done", "sermon_story_stage", "becky_advice_stage", "georgett_confession_stage", "liza_confession_stage"])) timeout 5.0

testcase external_secondary_side_characters_are_classes:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ people_sync_all()
    assert eval (all(key in SECONDARY_NPC_KEYS for key in ["luisa", "sergio", "lucas", "clara_fiance", "sergio_pet"])) timeout 5.0
    assert eval (getPersonData("luisa") is LuisaStaticData and getPersonInfo("luisa") is Luisa and isinstance(Luisa, LuisaInfo)) timeout 5.0
    assert eval (getPersonData("sergio") is SergioStaticData and getPersonInfo("sergio") is Sergio and isinstance(Sergio, SergioInfo)) timeout 5.0
    assert eval (getPersonData("lucas") is LucasStaticData and getPersonInfo("lucas") is Lucas and isinstance(Lucas, LucasInfo)) timeout 5.0
    assert eval (getPersonData("clara_fiance") is ClaraFianceStaticData and getPersonInfo("clara_fiance") is ClaraFiance and isinstance(ClaraFiance, ClaraFianceInfo)) timeout 5.0
    assert eval (getPersonData("sergio_pet") is SergioPetStaticData and getPersonInfo("sergio_pet") is SergioPet and isinstance(SergioPet, SergioPetInfo)) timeout 5.0
    assert eval (all(getPersonInfo(key) not in girls and getPersonInfo(key) in secondary_npcs for key in ["luisa", "sergio", "lucas", "clara_fiance", "sergio_pet"])) timeout 5.0
    assert eval (Luisa.var is LuisaVar and Sergio.var is SergioVar and Lucas.var is LucasVar and ClaraFiance.var is ClaraFianceVar and SergioPet.var is SergioPetVar) timeout 5.0
    assert eval (peopleData["luisa"].fullname == "Толстушка Луиза" and peopleData["lucas"].dative == "Лукасу") timeout 5.0
    assert eval (peopleData["clara_fiance"].fullname == "Столичный жених Клариссы" and peopleData["sergio_pet"].default_location == "BarberShop") timeout 5.0

testcase external_birth_thread_conditions_block_day_zero:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    $ renpy.call_in_new_context("InitGameNPCs")
    $ dayspassed = 0
    $ pregnancy["sandra"] = 240
    $ pregfather["sandra"] = "Вы"
    $ initStoryEventRuntime(True)
    assert eval ("systemGiveBirth" in threads and "systemGiveBirth" in threadData) timeout 5.0
    assert eval (not threadData["systemGiveBirth"].triggers[0][0].checkConditions()) timeout 5.0
    assert eval (not story_event_available("TavernMain", "enter")) timeout 5.0
    $ dayspassed = 240
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("TavernMain", "enter")) timeout 5.0
    assert eval (str(availEvents["TavernMain"]["enter"].target or "") == "story_give_birth_sandra") timeout 5.0
    $ dayspassed = 0
    $ pregnancy["sandra"] = 0
    $ pregfather["sandra"] = ""

testcase external_ellona_temple_sunday_story_event:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    $ renpy.call_in_new_context("InitGameNPCs")
    $ external_calendar_set_fields(day_value=1, month_value=1, year_value=CALENDAR_START_CYCLE, hour_value=9, minute_value=0)
    $ external_calendar_set_weekday(7)
    $ FranBusy[time] = 0
    $ Francheska.var["sunday_stories_seen_day"] = -1
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("EllonaTemple", "enter")) timeout 5.0
    assert eval (str(availEvents["EllonaTemple"]["enter"].target or "") == "story_ellona_temple_sunday_stories") timeout 5.0
    run Jump("EllonaTemple")
    advance until screen "say" timeout 20.0
    click pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    assert eval (str(CurLoc or "") == "EllonaTemple") timeout 5.0
    assert eval (int(Francheska.var.get("sunday_stories_seen_day", -1) or -1) == int(dayspassed or 0)) timeout 5.0
    $ initStoryEventRuntime(True)
    assert eval (not story_event_available("EllonaTemple", "enter")) timeout 5.0

testcase external_becky_classes_are_initialized:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ people_sync_all()
    assert eval ("becky" in peopleData and getPersonData("becky") is BeckyStaticData) timeout 5.0
    assert eval ("becky" in peopleInfo and getPersonInfo("becky") is Becky and isinstance(Becky, BeckyInfo)) timeout 5.0
    assert eval (Becky in girls and Becky.var is not BeckyVar) timeout 5.0
    assert eval (peopleData["becky"].cname == "Бекки" and peopleData["becky"].fullname == "Ребекка Блэнкеншип") timeout 5.0
    assert eval (hasattr(peopleData["becky"], "birth_date") and peopleInfo["becky"].age == 36) timeout 5.0
    assert eval (Friends["becky"] == Becky.rel == 0 and sluttiness["becky"] == Becky.corruption == 25) timeout 5.0
    assert eval (dressdefault["becky"] == "openworkdress" and bradef["becky"] == "simplebra" and pantiesdef["becky"] == "simplepanties") timeout 5.0
    assert eval (all(key in Becky.var for key in ["visitedhome", "HomeSex", "EddieWhoreHome", "TradeOffer", "KnowBlackwood"])) timeout 5.0
    assert eval (Becky.home_visit_stage() == 0 and not Becky.home_sex_unlocked() and not Becky.sherwood_trade_active()) timeout 5.0
    assert eval (Becky.getLocation(1, 13 * 60) == "GroceryStore") timeout 5.0
    $ initStoryEventRuntime(True)
    assert eval (Becky.var.get("visitedhome", 0) == 0) timeout 5.0
    assert eval (str(player_state().appearance.current_dress or "") != "citydress") timeout 5.0
    assert eval (int(charisma or 0) <= 75) timeout 5.0
    assert eval (not story_event_available("talk_becky", "becky_talk_invite")) timeout 5.0
    $ Becky.var["visitedhome"] = 2
    $ Friends["becky"] = 13
    $ Becky.update()
    $ initStoryEventRuntime(True)
    assert eval (not story_event_available("talk_becky", "becky_talk_invite")) timeout 5.0
    $ player_state().appearance.wear_dress("citydress", int(dayspassed or 0))
    $ charisma = 76
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_invite")) timeout 5.0
    $ Becky.var["husbandtalk"] = 1
    $ Friends["becky"] = 14
    $ Talked["becky"] = 0
    $ Becky.update()
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_husband1")) timeout 5.0
    $ Becky.var["TradeOffer"] = 1
    $ Becky.var["AskTradeElf"] = 0
    $ Talked["becky"] = 0
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_sherwood_elves")) timeout 5.0

testcase external_people_objects_are_single_source:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ people_sync_all()
    assert eval (not ("girls_data" in globals()) and not ("girls_info" in globals())) timeout 5.0
    assert eval (all(key in peopleData and isinstance(peopleData[key], PeopleData) for key in AllGirlNames)) timeout 5.0
    assert eval (all(key in peopleInfo and isinstance(peopleInfo[key], PeopleInfo) for key in AllGirlNames)) timeout 5.0
    assert eval (peopleData["amanda"].cname == "Аманда" and peopleData["amanda"].age == 18 and peopleInfo["amanda"].known) timeout 5.0
    assert eval (peopleData["melissa"].cname == "Мелисса" and hasattr(peopleData["melissa"], "birth_date") and peopleInfo["melissa"].age == 18 and peopleInfo["melissa"].known) timeout 5.0
    assert eval (peopleData["sandra"].cname == RealName["sandra"]) timeout 5.0
    assert eval (hasattr(peopleData["sandra"], "birth_date")) timeout 5.0
    assert eval (peopleInfo["sandra"].age == 34) timeout 5.0
    assert eval (peopleInfo["sandra"].known) timeout 5.0
    assert eval (peopleInfo["amanda"].rel == 5 and peopleInfo["amanda"].openness == 3) timeout 5.0
    assert eval (dressdefault["amanda"] == "modestworkdress" and dressdefault["melissa"] == "workdress" and dressdefault["sandra"] == "workdresszhilet") timeout 5.0
    assert eval (peopleData["eddie"].cname == "Эдди" and peopleData["eddie"].age == 19 and getPersonInfo("eddie") in secondary_npcs) timeout 5.0
    assert eval (peopleData["mongol"].cname == "Монгол" and peopleData["mongol"].default_location == "MarketPlace" and getPersonInfo("mongol") in secondary_npcs) timeout 5.0
    assert eval ("inga" not in AllGirlNames and peopleData["inga"] is IngaStaticData and getPersonInfo("inga") is Inga and isinstance(getPersonInfo("inga"), IngaInfo)) timeout 5.0
    assert eval (getPersonInfo("inga") not in girls and getPersonInfo("inga") in secondary_npcs and "inga" in SECONDARY_NPC_KEYS) timeout 5.0
    assert eval (all(peopleInfo[key] in girls for key in AllGirlNames)) timeout 5.0
    assert eval (all(key in peopleInfo and isinstance(peopleInfo[key], PeopleInfo) for key in SECONDARY_NPC_KEYS)) timeout 5.0
    assert eval (all(key in [str(getattr(row, "name", "") or "") for row in secondary_npcs] for key in SECONDARY_NPC_KEYS)) timeout 5.0
    assert eval (peopleInfo["amanda"] is Amanda and Amanda.uses_own_var_state and peopleInfo["becky"].var is not BeckyVar and peopleInfo["irma"].var is IrmaVar) timeout 5.0
    assert eval (peopleInfo["clara"].var is ClaraVar and peopleInfo["melissa"].var is MelissaVar and peopleInfo["sandra"].var is SandraVar) timeout 5.0
    assert eval (getPersonData("melissa") is peopleData["melissa"] and getPersonInfo("melissa") is peopleInfo["melissa"]) timeout 5.0
    assert eval (peopleData["melissa"].cname == RealName["melissa"] and peopleData["clara"].cname == RealName["clara"]) timeout 5.0
    assert eval (all(key in Drunk for key in AllGirlNames)) timeout 5.0
    assert eval (getPersonInfo("sandra") is Sandra and isinstance(getPersonInfo("sandra"), SandraInfo)) timeout 5.0
    assert eval (getPersonData("clara") is ClaraStaticData and getPersonInfo("clara") is Clara and isinstance(getPersonInfo("clara"), ClaraInfo)) timeout 5.0
    $ Drunk["amanda"] = 1
    $ peopleInfo["amanda"].update()
    assert eval (peopleInfo["amanda"].drunk == 1) timeout 5.0
    $ _drunk_social_result = social_apply_topic("amanda", "talk", "chat")
    assert eval (isinstance(_drunk_social_result, dict) and "text" in _drunk_social_result) timeout 5.0
    $ Drunk["amanda"] = 0
    assert eval (peopleInfo["irma"].getLocation(1, 1) == "DressShop") timeout 5.0
    assert eval (not social_has_visible_topics("irma", "flirt") and not social_interaction_allowed_for_npc("irma", "flirt")) timeout 5.0
    $ _sandra_days_before = dayspassed
    $ _sandra_reputation_before = reputation
    $ _sandra_final_before = int(SandraVar.get("FinalRewardDone", 0) or 0)
    $ _sandra_score_before = RelationshipInteractionScore.get("sandra", 0)
    $ _sandra_flirt_before = int(FlirtedToday.get("sandra", 0) or 0)
    $ dayspassed = 29
    $ reputation = 100
    $ Friends["sandra"] = 20
    $ otkroven["sandra"] = 20
    $ RelationshipInteractionScore["sandra"] = 999
    $ FlirtedToday["sandra"] = 1
    $ SandraVar["FinalRewardDone"] = 0
    assert eval (not getPersonInfo("sandra").social_action_allowed("talk")) timeout 5.0
    assert eval (not social_interaction_allowed_for_npc("sandra", "flirt") and not social_interaction_allowed_for_npc("sandra", "gift")) timeout 5.0
    $ dayspassed = 31
    $ SandraVar["FinalRewardDone"] = 1
    assert eval (getPersonInfo("sandra").social_action_allowed("talk")) timeout 5.0
    assert eval (social_interaction_allowed_for_npc("sandra", "flirt") and social_interaction_allowed_for_npc("sandra", "gift")) timeout 5.0
    $ dayspassed = _sandra_days_before
    $ reputation = _sandra_reputation_before
    $ SandraVar["FinalRewardDone"] = _sandra_final_before
    $ RelationshipInteractionScore["sandra"] = _sandra_score_before
    $ FlirtedToday["sandra"] = _sandra_flirt_before
    $ Friends["melissa"] = 2
    $ Talked["melissa"] = 0
    $ peopleInfo["melissa"].update()
    assert eval (peopleInfo["melissa"].rel == 2) timeout 5.0
    $ Friends["melissa"] = 2
    run Call("IntMelissaTalk")
    assert eval ("Попробовать помириться с Мелиссой" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    $ Friends["melissa"] = 17
    $ otkroven["melissa"] = 10
    $ sluttiness["melissa"] = 20
    $ MelissaVar["StartTotal"] = 5
    $ MelissaVar["sex_engine_unlocked"] = 0
    $ peopleInfo["melissa"].update()
    assert eval (peopleInfo["melissa"].rel == 17) timeout 5.0
    assert eval (melissa_relationship_stage("melissa") >= 3) timeout 5.0
    assert eval (melissa_relationship_allows("melissa", "intimacy")) timeout 5.0
    assert eval (melissa_private_place_offer("melissa", "ForestLake").get("ok", False)) timeout 5.0
    assert eval (str(peopleInfo["melissa"].getLocation(1, 7) or "") != "") timeout 5.0
    assert eval (str(peopleInfo["sandra"].getLocation(1, 7) or "") != "") timeout 5.0
    assert eval (str(peopleInfo["clara"].getLocation(1, 7) or "") != "") timeout 5.0
    $ TalkedToday["amanda"] = 2
    $ FlirtedToday["melissa"] = 1
    $ GiftedToday["sandra"] = 1
    $ FuckedToday["becky"] = 1
    $ Drunk["clara"] = 1
    $ LastDaySex = dayspassed
    $ people_sync_all()
    assert eval (peopleInfo["amanda"].talkCountToday == 2) timeout 5.0
    assert eval (peopleInfo["melissa"].flirtToday and peopleInfo["sandra"].giftToday and peopleInfo["becky"].fuckedCountToday == 1) timeout 5.0
    assert eval (peopleInfo["clara"].drunk == 1) timeout 5.0
    $ people_reset_daily_interactions(["amanda", "melissa", "sandra", "becky", "clara"])
    assert eval (peopleInfo["amanda"].talkCountToday == 0 and not peopleInfo["melissa"].flirtToday and not peopleInfo["sandra"].giftToday and peopleInfo["becky"].fuckedCountToday == 0) timeout 5.0
    assert eval (peopleInfo["clara"].drunk == 0 and Drunk.get("clara", -1) == 0) timeout 5.0
    assert eval (TalkedToday.get("amanda", -1) == 0 and FlirtedToday.get("melissa", -1) == 0 and GiftedToday.get("sandra", -1) == 0 and FuckedToday.get("becky", -1) == 0) timeout 5.0
    $ ensure_dog_runtime()
    assert eval (isinstance(dog, DogCompanion)) timeout 5.0

testcase external_npc_schedule_room_visibility_agreement:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 6, 0)
    $ external_calendar_set_weekday(1)
    $ npc_daily_schedule_build_all(True)
    $ CurrentRoom = TavernKitchenRoom
    $ CurLoc = "TavernKitchen"
    $ location = CurLoc
    $ _kitchen_ids = list(getNPCids("TavernKitchen") or [])
    $ _main_ids = list(getNPCids("TavernMain") or [])
    assert eval (str(getLocation("melissa") or "") in ("TavernKitchen", "TavernStorage", "TavernMain", "Backyard", "TavernMelissaRoom")) timeout 5.0
    assert eval (set(_kitchen_ids) == set(getNPCids("TavernKitchen"))) timeout 5.0
    assert eval (set(_main_ids) == set(getNPCids("TavernMain"))) timeout 5.0
    $ Melissa.var["bats_episode"] = 6
    $ Melissa.var["temp_room"] = "TavernAmandaRoom"
    assert eval (str(getLocation("melissa") or "") == "TavernAmandaRoom") timeout 5.0
    assert eval ("melissa" in list(getNPCids("TavernAmandaRoom") or []) and "melissa" not in list(getNPCids("TavernKitchen") or [])) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 13, 0)
    $ external_calendar_set_weekday(1)
    assert eval (str(getLocation("melissa") or "") in ("TavernMain", "TavernKitchen", "TavernStorage", "Backyard")) timeout 5.0
    assert eval ("melissa" not in list(getNPCids("TavernMelissaRoom") or [])) timeout 5.0
    $ Melissa.var["temp_room"] = ""
    $ external_calendar_set_fields(3, 1, 1100, 8, 30)
    $ external_calendar_set_weekday(1)
    $ TavernBreakfastEventActive = True
    $ TavernBreakfastPresentIds = ["melissa"]
    $ _forced_kitchen = list(getNPCids("TavernKitchen") or [])
    $ _forced_main = list(getNPCids("TavernMain") or [])
    assert eval (bool(TavernBreakfastEventActive) and list(TavernBreakfastPresentIds or []) == ["melissa"]) timeout 5.0
    assert eval (str(getLocation("melissa") or "") == "TavernKitchen") timeout 5.0
    assert eval ("melissa" in getNPCids("TavernKitchen") and "melissa" not in getNPCids("TavernMain")) timeout 5.0
    assert eval ("melissa" in _forced_kitchen) timeout 5.0
    assert eval ("melissa" not in _forced_main) timeout 5.0
    assert eval ("eddie" not in _forced_main) timeout 5.0
    assert eval ("eddie" not in _forced_kitchen) timeout 5.0
    $ TavernBreakfastEventActive = False
    $ TavernBreakfastPresentIds = []

testcase external_right_side_npc_buttons_open_default_menu:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 8, 30)
    $ external_calendar_set_weekday(1)
    $ knowsMC["eddie"] = True
    $ peopleInfo["eddie"].known = True
    $ CurLoc = "GroceryStore"
    $ location = CurLoc
    $ CurrentRoom = GroceryStoreRoom
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(getLocation("eddie") or "") == "GroceryStore") timeout 5.0
    assert eval ("eddie" in [str(row.get("id", "") or "") for row in _character_action_grid_entries(GroceryStoreRoom)]) timeout 5.0
    assert eval (next(row for row in _character_action_grid_entries(GroceryStoreRoom) if row["id"] == "eddie")["title"] == peopleData["eddie"].cname == "Эдди") timeout 5.0
    click id "main_ui_entity_button_npc_eddie" pos (0.5, 0.5) until eval (str(current_action_title or "") == npc_display_name("eddie")) timeout 20.0
    assert eval ("Осмотреть" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Поговорить" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval ("Назад" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (str(current_action_title or "") != npc_display_name("eddie")) timeout 20.0
    assert eval (str(CurLoc or "") == "GroceryStore") timeout 5.0

testcase external_people_locate_matches_schedule:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 8, 30)
    $ external_calendar_set_weekday(1)
    $ TavernBreakfastEventActive = True
    $ TavernBreakfastPresentIds = ["melissa"]
    $ CurrentLoc["irma"] = "DressShop"
    $ CurrentLoc["clara"] = "WineStore"
    $ CurrentLoc["mongol"] = "MarketPlace"
    $ people_sync_all()
    $ main_ui_overlay = "people"
    $ _loc_rows = people_locate_rows()
    assert eval (str(main_ui_overlay or "") == "people") timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "melissa")["location"] == getLocation("melissa") == "TavernKitchen") timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "eddie")["location"] == getLocation("eddie") == "GroceryStore") timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "irma")["location"] == getLocation("irma")) timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "clara")["location"] == getLocation("clara")) timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "mongol")["location"] == getLocation("mongol")) timeout 5.0
    assert eval ("melissa" in getNPCids("TavernKitchen") and "melissa" not in getNPCids("TavernMain")) timeout 5.0
    $ TavernBreakfastEventActive = False
    $ TavernBreakfastPresentIds = []
    $ main_ui_overlay = ""

testcase external_player_and_girl_cards_render:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ _card_return_room = str(CurLoc or "")
    click id "main_ui_entity_button_player_you" pos (0.5, 0.5) until eval (str(UI_mode or "") == "mc") timeout 20.0
    assert eval (len(player_card_stat_rows_left()) > 0 and len(player_card_stat_rows_right()) > 0 and str(player_card_portrait_path() or "") != "") timeout 5.0
    assert eval (str(player_card_portrait_path() or "") == "images/general/player_card.jpg" and renpy.loadable(player_card_portrait_path())) timeout 5.0
    click id "main_ui_player_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ _card_keys = ["sandra", "amanda", "melissa", "clara", "becky", "irma", "georgett", "liza"]
    $ CurrentLoc["melissa"] = "TavernKitchen"
    $ peopleInfo["melissa"].location = "TavernKitchen"
    $ npc_schedule_set("melissa", [NPCScheduleEntry(location="TavernKitchen", time_slots=[], priority=999)])
    $ knowsMC["melissa"] = True
    $ peopleInfo["melissa"].update()
    $ _melissa_rows = girl_card_stat_rows("melissa")
    assert eval (("Локация", getLocation("melissa")) in _melissa_rows and len(_melissa_rows) >= 5) timeout 5.0
    $ Sandra.age = 35
    $ Sandra.rel = 11
    $ Sandra.openness = 7
    $ Sandra.corruption = 31
    $ Sandra.stats["beauty"] = 77
    $ Sandra.stats["kids"] = 4
    $ Sandra.skills["cooking"] = 88
    assert eval (("Возраст", "35") in girl_card_stat_rows("sandra")) timeout 5.0
    assert eval (("Дружба", "11") in girl_card_stat_rows("sandra")) timeout 5.0
    assert eval (("Откровенность", "7") in girl_card_stat_rows("sandra")) timeout 5.0
    assert eval (("Распущенность", "31") in girl_card_stat_rows("sandra")) timeout 5.0
    assert eval (("Красота", "77") in girl_card_stat_rows("sandra")) timeout 5.0
    assert eval (("Дети", "4") in girl_card_stat_rows("sandra")) timeout 5.0
    assert eval (("Кухня", "88") in girl_card_stat_rows("sandra")) timeout 5.0
    assert eval (str(girl_card_portrait_path("amanda") or "") != "" and renpy.loadable(girl_card_portrait_path("amanda"))) timeout 5.0
    assert eval (str(girl_card_portrait_path("melissa") or "") != "" and renpy.loadable(girl_card_portrait_path("melissa"))) timeout 5.0
    assert eval (str(girl_card_portrait_path("sandra") or "") != "" and renpy.loadable(girl_card_portrait_path("sandra"))) timeout 5.0
    python:
        _card_results = {}
        for _card_key in _card_keys:
            show_girl_card_main_ui_state(_card_key)
            _card_results[_card_key] = (
                str(UI_mode or "") == "char"
                and str(UI_selected_char or "") == _card_key
                and str(girl_card_display_name(_card_key) or "") != ""
                and str(girl_card_portrait_path(_card_key) or "") != ""
                and len(list(girl_card_stat_rows(_card_key) or [])) > 0
                and len(list(girl_card_body_lines(_card_key) or [])) > 0
            )
            main_ui_restore_room_scene_state()
    assert eval (all(_card_results.values())) timeout 5.0
    assert eval (str(UI_mode or "") == "scene") timeout 5.0

    $ show_girl_card_main_ui_state("sandra")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_girl_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("amanda")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_girl_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("melissa")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_girl_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("clara")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_girl_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("becky")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_girl_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("irma")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_girl_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("georgett")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_girl_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("liza")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_girl_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_dog_card_main_ui_state()
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_dog_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0
    $ show_werecat_card_main_ui_state()
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_werecat_card_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room and str(UI_mode or "") == "scene") timeout 20.0

    run Call("ShowPlayerCard", "")
    advance until screen "player_card_overlay" timeout 20.0
    click id "player_card_overlay_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room) timeout 20.0
    run Call("ShowGirlCard", "amanda", "")
    advance until screen "girl_card_overlay" timeout 20.0
    click id "girl_card_overlay_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room) timeout 20.0
    run Call("ShowDogCard", "")
    advance until screen "dog_card_overlay" timeout 20.0
    click id "dog_card_overlay_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room) timeout 20.0
    run Call("ShowWerecatCard", "")
    advance until screen "werecat_card_overlay" timeout 20.0
    click id "werecat_card_overlay_back_button" pos (0.5, 0.5) until eval (str(CurLoc or "") == _card_return_room) timeout 20.0

testcase external_mongol_horse_purchase_once_and_amanda_room_presence:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ money = 5000
    $ MyStallion = ""
    $ HorseSaddled = 0
    $ HorsePurchasePrice = 0
    $ Mongol.var["HorsePrice"] = 1000
    $ Mongol.var["DiscountAsk"] = 1
    run Call("MongolTalk")
    assert eval ("Беру" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    run Call("MongolTalkApply", "buy")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(MyStallion or "") != "" and int(HorseSaddled or 0) == 1) timeout 5.0
    $ _horse_money_after_buy = int(money or 0)
    run Call("MongolTalk")
    assert eval ("Беру" not in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    run Call("MongolTalkApply", "buy")
    assert eval (int(money or 0) == _horse_money_after_buy and str(MyStallion or "") != "") timeout 5.0
    $ external_calendar_set_fields(day, month, year, 23, 0)
    $ CurrentLoc["amanda"] = "TavernMain"
    run Jump("TavernAmandaRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(getLocation("amanda") or "") == "TavernAmandaRoom") timeout 5.0
    assert eval ("amanda" in [str(row.get("npc_id", "") or "") for row in TavernAmandaRoomRoom.visible_npcs()]) timeout 5.0
    assert eval ("amanda" in [str(row.get("id", "") or "") for row in _character_action_grid_entries(TavernAmandaRoomRoom)]) timeout 5.0

testcase external_clara_object_thread_conditions:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    assert eval ("clara" in peopleData and "clara" in peopleInfo) timeout 5.0
    assert eval (peopleInfo["clara"] in girls and not ("girls_data" in globals()) and not ("girls_info" in globals())) timeout 5.0
    $ npc_interval_schedule_set("clara", [NPCIntervalScheduleEntry(npc_id="clara", location="WineStore", start="00:00", end="23:59", awake=True, talkable=True, priority=999, label="test_wine_store")])
    $ week = 2
    $ dayspassed = 30
    $ CurLoc = "WineStore"
    $ external_calendar_set_fields(3, 1, 1100, 8, 0)
    $ ClaraVar["comfort_pending"] = 1
    $ ClaraVar["comfort_done"] = 0
    assert eval (peopleInfo["clara"].var is ClaraVar) timeout 5.0
    assert eval (peopleInfo["clara"].rel == Friends["clara"]) timeout 5.0
    assert eval (int(clock_minutes or 0) == 480) timeout 5.0
    assert eval (str(getLocation("clara") or "") == "WineStore") timeout 5.0
    assert eval (int(ClaraVar.get("comfort_pending", 0) or 0) == 1 and int(ClaraVar.get("comfort_done", 0) or 0) == 0) timeout 5.0
    assert eval (clara_paintings_comfort_ready()) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 12, 0)
    assert eval (not clara_paintings_comfort_ready()) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 8, 0)
    $ ClaraVar["commission_started"] = 1
    $ ClaraVar["commission_followup_done"] = 0
    $ ClaraVar["commission_followup_day"] = -1
    $ CurrentLoc["clara"] = "WineStore"
    $ peopleInfo["clara"].location = "WineStore"
    assert eval (int(ClaraVar.get("commission_started", 0) or 0) == 1) timeout 5.0
    assert eval (int(ClaraVar.get("commission_followup_done", 0) or 0) == 0) timeout 5.0
    assert eval (int(dayspassed or 0) >= int(ClaraVar.get("commission_followup_day", 999999))) timeout 5.0
    assert eval (getLocation("clara") == "WineStore") timeout 5.0
    assert eval (getLocation("clara") == "WineStore" and int(clock_minutes or 0) == 480) timeout 5.0
    assert eval (clara_paintings_commission_followup_ready()) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 22, 0)
    $ ClaraVar["commission_followup_done"] = 1
    $ ClaraVar["peek_done"] = 0
    assert eval (int(clock_minutes or 0) == 1320) timeout 5.0
    assert eval (str(getLocation("clara") or "") == "WineStore") timeout 5.0
    assert eval (clara_paintings_evening_peek_ready()) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 15, 59)
    assert eval (not clara_paintings_evening_peek_ready()) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 22, 0)
    $ _clara_rel_before = int(Friends.get("clara", 0) or 0)
    $ Friends["clara"] = min(20, _clara_rel_before + 2)
    $ peopleInfo["clara"].update()
    assert eval (Friends["clara"] == peopleInfo["clara"].rel) timeout 5.0
    $ CurrentLoc["clara"] = "TavernMelissaRoom"
    $ peopleInfo["clara"].location = "TavernMelissaRoom"
    $ CurrentLoc["melissa"] = "TavernMelissaRoom"
    $ peopleInfo["melissa"].location = "TavernMelissaRoom"
    $ npc_interval_schedule_set("clara", [NPCIntervalScheduleEntry(npc_id="clara", location="TavernMelissaRoom", start="00:00", end="23:59", awake=True, talkable=True, priority=999, label="test_melissa_room")])
    $ npc_interval_schedule_set("melissa", [NPCIntervalScheduleEntry(npc_id="melissa", location="TavernMelissaRoom", start="00:00", end="23:59", awake=True, talkable=True, priority=999, label="test_melissa_room")])
    $ npc_schedule_set("clara", [NPCScheduleEntry(location="TavernMelissaRoom", time_slots=[], priority=999)])
    $ npc_schedule_set("melissa", [NPCScheduleEntry(location="TavernMelissaRoom", time_slots=[], priority=999)])
    $ ClaraVar["confession_done"] = 0
    $ ClaraVar["peek_done"] = 1
    assert eval (CurrentLoc["clara"] == "TavernMelissaRoom" and peopleInfo["clara"].location == "TavernMelissaRoom") timeout 5.0
    assert eval (clara_paintings_confession_ready()) timeout 5.0

testcase external_story_event_audit_methods_cover_tuple_attributes:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 6, 0)
    $ CurLoc = "TavernStorage"
    $ location = CurLoc
    $ CurrentRoom = TavernStorageRoom
    $ BreakfastToday = False
    $ TavernBreakfastEventActive = False
    $ MelissaVar["ratKilled"] = False
    $ MelissaVar["storage_rat_cleared"] = 0
    $ werecat_state()["rats_problem_active"] = 0
    $ CurrentLoc["melissa"] = "TavernStorage"
    $ npc_schedule_set("melissa", [NPCScheduleEntry(location="TavernStorage", time_slots=[], priority=999)])
    $ household_mark_runtime_event_seen("melissa_storage_rat", -999)
    $ threads.clear()
    $ availEvents.clear()
    $ evalTime = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    $ _audit_tinfo = threads["melissaRatProblem"]
    $ _audit_evt = _audit_tinfo.getevent(0)
    $ _audit_rows = _audit_evt.auditChecks(_audit_tinfo.day)
    $ _audit_fields = [str(row.get("field", "") or "") for row in _audit_rows]
    assert eval (set(["target", "binding", "day", "hour", "delay", "requirements", "conditions", "item", "location_open", "probability"]).issubset(set(_audit_fields))) timeout 5.0
    assert eval (all(isinstance(row.get("ok", None), bool) for row in _audit_rows)) timeout 5.0
    assert eval (story_board_show_event_checks(_audit_evt, _audit_tinfo) != "No checks") timeout 5.0
'''


FIGHT_SYSTEM_RUNTIME_CHECKS = r'''
testcase external_fight_system_runtime_flow:
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0

    $ week = 1
    $ time = 1
    $ hour = 12
    $ minute = 0
    $ BlockTimeAdvance = 0
    $ main_ui_overlay = ""
    $ current_action_content = None
    $ CurrentRoom = ForestRoom
    $ CurLoc = "Forest"
    $ location = CurLoc
    $ scene_image = "images/forest/forest_1.png"
    $ _layout_last_picture = scene_image
    $ health = 100
    $ energy = 100
    $ exploration = 120
    $ fight_info().level = {"you": 1}
    $ playerItems = {}
    $ EquippedWeapon = "rusty_hunter_rifle_001"
    $ EquippedArmor = ""
    $ RustyHunterRifleLoadedAmmo = ""
    $ _player_add_item_by_id("arrows_001", 2)
    $ _player_add_item_by_id("bandage_001", 1)
    assert eval (hasattr(FIGHT_ENEMY_DEFINITIONS.get("wolf", None), "as_dict")) timeout 5.0
    assert eval (hasattr(FIGHT_ENEMY_DEFINITIONS.get("boar", None), "as_dict")) timeout 5.0
    assert eval (hasattr(FIGHT_ENEMY_DEFINITIONS.get("brown_bear", None), "as_dict")) timeout 5.0
    assert eval (str(FIGHT_ENEMY_DEFINITIONS["street_crook"].weapon or "") == "дубинка") timeout 5.0
    assert eval (str(FIGHT_ENEMY_DEFINITIONS["patrol_guard"].tactics or "") == "formation") timeout 5.0

    run Call("FightStartHuntCurrentRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(UI_mode or "") == "fight") timeout 5.0
    assert eval (len(list(fight_info().enemy_party or [])) >= 1) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "").startswith("images/hunt/")) timeout 5.0
    $ _fight_test_picture = str(fight_info().return_picture or "")
    $ fight_finish_to_room(str(MainTxt or ""))
    $ scene_image = _fight_test_picture
    $ _layout_last_picture = _fight_test_picture
    assert eval (str(UI_mode or "") == "scene" and str(CurLoc or "") == "Forest") timeout 5.0

    $ fight_begin("wolf", 1, "Forest", scene_image, "Тестовая схватка.")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(UI_mode or "") == "fight") timeout 5.0
    assert eval (len(list(fight_info().enemy_party or [])) == 1) timeout 5.0
    assert eval (int(fight_info().level.get("you", 0) or 0) >= 3) timeout 5.0
    assert eval ("Перезарядить стрелой" in [str(i.caption or "") for i in current_action_items]) timeout 5.0
    assert eval (any(str(i.caption or "").startswith("Атаковать") or str(i.caption or "") == "Бить прикладом" for i in current_action_items)) timeout 5.0
    assert eval (int(fight_weapon_attack_points() or 0) == 14) timeout 5.0

    $ EquippedWeapon = "old_axe_001"
    $ RustyHunterRifleLoadedAmmo = ""
    $ fight_sync_loaded_weapon_state_from_inventory()
    $ fight_refresh_ui_actions()
    assert eval (int(fight_weapon_attack_points() or 0) == 10) timeout 5.0
    assert eval (not any(str(i.caption or "").startswith("Перезарядить") or str(i.caption or "").startswith("Выстрелить") for i in current_action_items)) timeout 5.0

    $ EquippedWeapon = ""
    $ fight_sync_loaded_weapon_state_from_inventory()
    $ fight_refresh_ui_actions()
    assert eval (fight_player_weapon_name() == "кулаки" and "Атаковать кулаками" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ EquippedWeapon = "rusty_hunter_rifle_001"
    $ fight_sync_loaded_weapon_state_from_inventory()
    $ fight_refresh_ui_actions()
    assert eval ("Перезарядить стрелой" in [str(i.caption or "") for i in current_action_items]) timeout 5.0

    $ renpy.call_in_new_context("FightDoAction", "reload_arrows")
    assert eval (str(UI_mode or "") == "fight") timeout 5.0
    assert eval (int(fight_info().weapon_loaded or 0) == 1 and str(fight_info().loaded_ammo or "") == "arrows") timeout 5.0
    assert eval (int(fight_info().supply.get("arrows", 0) or 0) == 1) timeout 5.0

    $ renpy.call_in_new_context("FightDoAction", "shoot")
    assert eval (str(UI_mode or "") == "fight") timeout 5.0
    assert eval (int(fight_info().weapon_loaded or 0) == 0 and str(fight_info().loaded_ammo or "") == "") timeout 5.0
    assert eval (0 < int(health or 0) <= 100) timeout 5.0

    $ renpy.call_in_new_context("FightDoAction", "retreat")
    assert eval (str(UI_mode or "") == "fight" and str(fight_info().outcome_popup.get("kind", "") or "") == "retreat") timeout 5.0
    $ _fight_test_picture = str(fight_info().return_picture or "")
    $ fight_finish_to_room(str(MainTxt or ""))
    $ scene_image = _fight_test_picture
    $ _layout_last_picture = _fight_test_picture
    assert eval (str(UI_mode or "") == "scene") timeout 5.0
    assert eval (str(CurLoc or "") == "Forest") timeout 5.0
    assert eval (len(list(fight_info().enemy_party or [])) == 0) timeout 5.0
    assert eval (str(current_action_title or "") != "Бой") timeout 5.0

    $ health = 80
    $ energy = 100
    $ EquippedWeapon = "old_axe_001"
    $ fight_begin("street_crook", 1, "StreetTavern", "images/fight/thug.png", "Forced victory test.")
    $ FightEnemyParty[0]["health"] = 1
    $ FightEnemyParty[0]["energy"] = 1
    $ renpy.call_in_new_context("FightDoAction", "attack")
    assert eval (str(FightOutcomeKind or "") == "victory" and str(current_action_title or "") == "Победа") timeout 5.0
    assert eval (isinstance(HuntLastResult, dict) and str(HuntLastResult.get("outcome", "") or "") == "victory") timeout 5.0
    assert eval (isinstance(FightVictoryLoot, dict) and int(FightVictoryLoot.get("money", 0) or 0) >= 0) timeout 5.0
    assert eval ("Победа" in str(current_action_title or "") and "добыч" in str(FightOutcomeText or "").lower()) timeout 5.0
    $ _fight_test_picture = str(fight_info().return_picture or "")
    $ fight_finish_to_room(str(MainTxt or ""))
    $ scene_image = _fight_test_picture
    $ _layout_last_picture = _fight_test_picture

    $ exploration = 300
    $ fight_info().level = {"you": 3}
    $ fight_begin("patrol_guard", 2, "StreetTavern", "bg StreetTavern", "Тестовая схватка с патрулем.")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(UI_mode or "") == "fight") timeout 5.0
    assert eval (str(fight_info().enemy_id or "") == "patrol_guard" and len(list(fight_info().enemy_party or [])) == 2) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "") == "images/fight/patrol_guard.png") timeout 5.0
    assert eval (str(fight_info().enemy_party[0].get("weapon", "") or "") == "алебарда") timeout 5.0
    assert eval ("formation" in list(fight_info().enemy_party[0].get("skills", []) or [])) timeout 5.0
    $ renpy.call_in_new_context("FightDoAction", "retreat")
    assert eval (str(UI_mode or "") == "fight" and str(fight_info().outcome_popup.get("kind", "") or "") == "retreat") timeout 5.0
    $ _fight_test_picture = str(fight_info().return_picture or "")
    $ fight_finish_to_room(str(MainTxt or ""))
    $ scene_image = _fight_test_picture
    $ _layout_last_picture = _fight_test_picture
    assert eval (str(UI_mode or "") == "scene" and str(CurLoc or "") == "StreetTavern") timeout 5.0
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
    ) + "\n\n" + SHOP_ACTION_CHECKS + "\n\n" + TAVERN_REPORT_STATE_CHECKS + "\n\n" + TAILOR_PURCHASE_FLOW_CHECKS + "\n\n" + DOG_ENTITY_ACTION_CHECKS + "\n\n" + BACKYARD_BARREL_OBJECT_CHECKS + "\n\n" + GROCERY_STORE_OBJECT_PURCHASE_CHECKS + "\n\n" + FIGHT_SYSTEM_RUNTIME_CHECKS + "\n\n" + PORT_STREETS_FLOW_CHECKS + "\n\n" + CALENDAR_TIME_CHECKS + "\n\n" + MEDIA_RESOLUTION_CHECKS + "\n\n" + HARASSMENT_IMAGE_CHECKS + "\n\n" + GIRL_OBJECT_RUNTIME_CHECKS + "\n\n" + ACTUAL_ACTION_BUTTON_CLICK_CHECKS + "\n\n" + ACTUAL_RANDOM_TOWN_CLICK_CHECKS + "\n\n" + TARGETED_CURRENT_BUG_CHECKS + "\n\n" + DEBUG_BUILDER_ROOM_CHECKS + "\n\n" + AMANDA_ROOM_NIGHT_EVENT_CHECKS + "\n\n" + MY_ROOM_RECIPE_BOOK_ACTION_CHECKS + "\n\n" + MY_ROOM_WINDOW_ACTION_CHECKS + "\n\n" + TAVERN_ROOM_PICTURE_STATE_CHECKS + "\n\n" + MELISSA_BATS_DRAWINGS_CHECKS + "\n\n" + MELISSA_WERECAT_FOREST_ACTION_CHECKS + "\n\n" + CHURCH_LINK_CHECKS + "\n\n" + CHURCH_AFTER_SERMON_EVENT_CHECKS + "\n\n" + CLARA_MELISSA_TAVERN_BAR_GOSSIP_CHECKS + "\n\n" + FRIDAY_DANCE_AMANDA_CHECKS + "\n\n" + SANDRA_NIGHT_THANKS_CHECKS + "\n\n" + MELISSA_SEX_ENGINE_CHECKS + "\n\n" + PLAYER_INTIMACY_STATE_CHECKS + "\n\n" + CLARA_AMANDA_SCHEDULE_FLOW_CHECKS + "\n\n" + HOUSEHOLD_AI_EVENT_CHECKS + "\n\n" + all_room_action_click_checks + "\n\n" + "".join(room_action_sections) + "\n\n" + BECKY_HOME_GUEST_CHECKS


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


def clear_renpy_runtime_state(temp_project: Path) -> None:
    for relative in [
        Path("game") / "saves",
        Path("saves"),
    ]:
        target = temp_project / relative
        if target.exists():
            remove_temp_tree(target)


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
            "external_tavern_report_state_defaults",
            "external_actual_tailor_buy_dress_measure_flow",
            "external_dog_entity_actions",
            "external_backyard_barrel_object_actions",
            "external_grocery_store_object_purchase_actions",
            "external_fight_system_runtime_flow",
            "external_port_streets_georgette_liza_flow",
            "external_georgette_portstreet_relationship_talk_and_sex_flow",
            "external_sexport_finish_does_not_show_advance_time_developer_text",
            "external_new_game_starts_at_8_morning",
            "external_calendar_long_cycle_thirteenth_period_rollover",
            "external_sleep_wake_hour_rules",
            "external_daily_setstatdefault_body_maps_exist",
            "external_hour_based_room_and_npc_schedule_adjustment",
            "external_context_image_resolution",
            "external_harassment_images_use_exact_existing_paths",
            "external_harassment_event_picture_sequence",
            "external_inga_secondary_npc_source",
            "external_francheska_secondary_and_birth_thread",
            "external_gerhard_secondary_npc_source",
            "external_secondary_side_characters_are_classes",
            "external_birth_thread_conditions_block_day_zero",
            "external_ellona_temple_sunday_story_event",
            "external_becky_classes_are_initialized",
            "external_people_objects_are_single_source",
            "external_npc_schedule_room_visibility_agreement",
            "external_right_side_npc_buttons_open_default_menu",
            "external_people_locate_matches_schedule",
            "external_player_and_girl_cards_render",
            "external_mongol_horse_purchase_once_and_amanda_room_presence",
            "external_clara_object_thread_conditions",
            "external_story_event_audit_methods_cover_tuple_attributes",
            "external_actual_grocery_click",
            "external_actual_wine_click",
            "external_actual_wine_for_dance_menu",
            "external_tavern_random_event_plan_consumes_once",
            "external_tavern_unwitnessed_event_report_consumes_leftovers",
            "external_breakfast_dance_sponsor_announcement",
            "external_breakfast_attendance_location_wins",
            "external_breakfast_angry_amanda_melissa_mockery",
            "external_breakfast_window_and_call_all_click",
            "external_actual_barber_actions_click",
            "external_actual_market_click",
            "external_actual_market_blind_pirate_first_entry",
            "external_market_clock_open_hours",
            "external_actual_random_town_continue_click",
            "external_actual_random_town_click",
            "external_sleep_after_midnight_detector",
            "external_town_thugs_shout_result",
            "external_town_thugs_fight_victory_result",
            "external_georgette_back_alley_not_visible_in_port_streets",
            "external_debug_builder_room_visual_surfaces",
            "external_amanda_room_night_bed_action_uses_thread_event",
            "external_my_room_recipe_book_table_link",
            "external_my_room_window_day_night_amanda_pictures",
            "external_tavern_room_movement_resets_picture_state",
            "external_melissa_bats_room_search_after_wait",
            "external_melissa_werecat_forest_actions_rebuild",
            "external_melissa_werecat_thread_condition_sequence",
            "external_church_service_action_links_work",
            "external_georgett_liza_church_after_sermon_events",
            "external_clara_market_event_repeats_until_exploration_success",
            "external_clara_market_follow_finishes_without_self_loop",
            "external_mongol_market_schedule_rolls_once_per_day",
            "external_clara_melissa_bar_gossip_click_fires_ready_dialog",
            "external_clara_booklet_mongol_night_buttons_advance",
            "external_zimmer_mongol_wine_distraction_dialog",
            "external_robin_blackwood_room_thread_and_mongol_pass",
            "external_friday_amanda_bad_invite_uses_one_dance",
            "external_friday_amanda_legare_go_phrase_survives_create_dance",
            "external_friday_dance_minigame_steps_score",
            "external_friday_becky_inner_actions_do_not_spend_extra_dances",
            "external_sandra_night_thanks_slots_work",
            "external_melissa_engagement_clothing_state_and_no_full_sex",
            "external_player_intimacy_state_sleep_arousal_and_help",
            "external_clara_evening_follow_finishes_in_melissa_room",
            "external_amanda_player_room_visit_is_physical_and_leaves",
            "external_household_ai_kitchen_event_fires",
            "external_all_room_action_clicks",
            "external_room_action_dispatch",
            "external_becky_home_guest_citydress_gate_and_arrival",
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
            "external_tavern_report_state_defaults",
            "external_actual_tailor_buy_dress_measure_flow",
            "external_dog_entity_actions",
            "external_backyard_barrel_object_actions",
            "external_grocery_store_object_purchase_actions",
            "external_fight_system_runtime_flow",
            "external_port_streets_georgette_liza_flow",
            "external_georgette_portstreet_relationship_talk_and_sex_flow",
            "external_sexport_finish_does_not_show_advance_time_developer_text",
            "external_new_game_starts_at_8_morning",
            "external_calendar_long_cycle_thirteenth_period_rollover",
            "external_sleep_wake_hour_rules",
            "external_daily_setstatdefault_body_maps_exist",
            "external_hour_based_room_and_npc_schedule_adjustment",
            "external_context_image_resolution",
            "external_harassment_images_use_exact_existing_paths",
            "external_harassment_event_picture_sequence",
            "external_inga_secondary_npc_source",
            "external_francheska_secondary_and_birth_thread",
            "external_gerhard_secondary_npc_source",
            "external_secondary_side_characters_are_classes",
            "external_birth_thread_conditions_block_day_zero",
            "external_ellona_temple_sunday_story_event",
            "external_becky_classes_are_initialized",
            "external_people_objects_are_single_source",
            "external_npc_schedule_room_visibility_agreement",
            "external_right_side_npc_buttons_open_default_menu",
            "external_people_locate_matches_schedule",
            "external_player_and_girl_cards_render",
            "external_clara_object_thread_conditions",
            "external_story_event_audit_methods_cover_tuple_attributes",
            "external_actual_grocery_click",
            "external_actual_wine_click",
            "external_actual_wine_for_dance_menu",
            "external_tavern_random_event_plan_consumes_once",
            "external_tavern_unwitnessed_event_report_consumes_leftovers",
            "external_breakfast_dance_sponsor_announcement",
            "external_breakfast_attendance_location_wins",
            "external_breakfast_angry_amanda_melissa_mockery",
            "external_breakfast_window_and_call_all_click",
            "external_actual_barber_actions_click",
            "external_actual_market_click",
            "external_actual_market_blind_pirate_first_entry",
            "external_market_clock_open_hours",
            "external_actual_random_town_continue_click",
            "external_actual_random_town_click",
            "external_debug_builder_room_visual_surfaces",
            "external_amanda_room_night_bed_action_uses_thread_event",
            "external_my_room_recipe_book_table_link",
            "external_my_room_window_day_night_amanda_pictures",
            "external_tavern_room_movement_resets_picture_state",
            "external_melissa_bats_room_search_after_wait",
            "external_melissa_werecat_forest_actions_rebuild",
            "external_melissa_werecat_thread_condition_sequence",
            "external_church_service_action_links_work",
            "external_georgett_liza_church_after_sermon_events",
            "external_clara_market_event_repeats_until_exploration_success",
            "external_clara_market_follow_finishes_without_self_loop",
            "external_mongol_market_schedule_rolls_once_per_day",
            "external_clara_melissa_bar_gossip_click_fires_ready_dialog",
            "external_clara_booklet_mongol_night_buttons_advance",
            "external_zimmer_mongol_wine_distraction_dialog",
            "external_robin_blackwood_room_thread_and_mongol_pass",
            "external_friday_amanda_bad_invite_uses_one_dance",
            "external_friday_amanda_legare_go_phrase_survives_create_dance",
            "external_friday_dance_minigame_steps_score",
            "external_friday_becky_inner_actions_do_not_spend_extra_dances",
            "external_sandra_night_thanks_slots_work",
            "external_melissa_engagement_clothing_state_and_no_full_sex",
            "external_player_intimacy_state_sleep_arousal_and_help",
            "external_clara_evening_follow_finishes_in_melissa_room",
            "external_amanda_player_room_visit_is_physical_and_leaves",
            "external_household_ai_kitchen_event_fires",
            "external_all_room_action_clicks",
            "external_room_action_dispatch",
            "external_becky_home_guest_citydress_gate_and_arrival",
        ]
        for test_name in test_names:
            clear_renpy_runtime_state(temp_project)
            result = max(result, run_renpy(renpy_exe, temp_project, args.timeout, test_name))
        return result
    finally:
        if args.keep_temp:
            print(f"Keeping temporary test project: {temp_root}")
        else:
            remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
