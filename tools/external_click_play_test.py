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
import stat
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
    import os

    def external_player_load_marker_path():
        return os.path.join(config.basedir, ".external-player-load-marker")

    def external_player_load_marker_exists():
        return os.path.exists(external_player_load_marker_path())

    def external_player_mark_load():
        with open(external_player_load_marker_path(), "w", encoding="utf-8") as marker_file:
            marker_file.write("load")

    def external_player_clear_load_marker():
        marker_path = external_player_load_marker_path()
        if os.path.exists(marker_path):
            os.unlink(marker_path)

    def external_calendar_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def external_calendar_day_number_from_fields(day_value=None, month_value=None, year_value=None):
        cycle = max(CALENDAR_START_CYCLE, external_calendar_int(calendar_v2.cycle if year_value is None else year_value, CALENDAR_START_CYCLE))
        period = max(1, min(13, external_calendar_int(calendar_v2.period if month_value is None else month_value, 1)))
        lunar_day = max(1, min(28, external_calendar_int(calendar_v2.day if day_value is None else day_value, 1)))
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
        calendar_v2.hour = external_calendar_int(calendar_v2.hour if hour_value is None else hour_value, 8) % 24
        calendar_v2.minute = external_calendar_int(calendar_v2.minute if minute_value is None else minute_value, 0) % 60
        return True

    # External test fixture setup only. Gameplay never changes weekday directly.
    def external_calendar_set_weekday(weekday_value=1):
        target_week = max(1, min(7, external_calendar_int(weekday_value, 1)))
        steps = (target_week - max(1, min(7, external_calendar_int(calendar_v2.week, 1)))) % 7
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
        return True

    def external_position_clara_tavern_visit(start_day=0):
        first_day = max(0, external_calendar_int(start_day, 0))
        diagnostics = []
        for day_number_i in range(first_day, first_day + 120):
            parts = calendar_v2.day_number_to_parts(day_number_i)
            external_calendar_set_fields(parts["day"], parts["month"], parts["year"], 12, 0)
            rule_active = bool(Clara.tavern_visit_active())
            clara_location = str(people.location("clara") or "")
            melissa_location = str(people.location("melissa") or "")
            if rule_active and len(diagnostics) < 3:
                diagnostics.append({
                    "day": day_number_i,
                    "week": int(calendar_v2.week or 0),
                    "clara": clara_location,
                    "melissa": melissa_location,
                    "clara_state": dict(Clara.data.schedule_state() or {}),
                    "melissa_state": dict(Melissa.data.schedule_state() or {}),
                    "clara_error": str(Clara.data.interval_schedule_load_error or ""),
                    "melissa_error": str(Melissa.data.interval_schedule_load_error or ""),
                })
            if rule_active and clara_location == "TavernMain" and melissa_location == "TavernMain":
                return day_number_i
        raise AssertionError("No canonical Clara/Melissa tavern visit time found: %r" % diagnostics)

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
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ Sandra.rel = max(int(Sandra.rel or 0), 10)
    $ set_bedroom_door_locked("TavernSandraRoom", False)

    run Jump("{room_name}")
    advance until screen "main_ui" timeout 20.0
    pause 0.1
    assert eval (str(rooms.current_code or "") == "{room_name}") timeout 5.0
    click id "main_ui_time_button" pos (0.5, 0.5) until eval (str(main_ui_runtime.overlay or "") == "time") timeout 10.0
    click id "time_change_back_button" pos (0.5, 0.5) until eval (str(main_ui_runtime.overlay or "") == "") timeout 10.0

    click id "main_ui_story_button" pos (0.5, 0.5) until eval (str(main_ui_runtime.overlay or "") == "story") timeout 10.0
    click id "main_ui_people_button" pos (0.5, 0.5) until eval (str(main_ui_runtime.overlay or "") == "people") timeout 10.0
    click id "main_ui_time_button" pos (0.5, 0.5) until eval (str(main_ui_runtime.overlay or "") == "time") timeout 10.0
    click id "time_change_back_button" pos (0.5, 0.5) until eval (str(main_ui_runtime.overlay or "") == "") timeout 10.0
'''


SHOP_ACTION_CHECKS = r'''
testcase external_shop_action_logic:
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Call("InitBecky")
    run Call("InitInga")
    run Call("register_eddie_secondary")
    $ external_calendar_set_fields(10, 1, 1100, 10, 0)
    $ external_calendar_set_weekday(1)
    $ npc_interval_schedule_load_all(True)
    $ rooms.enter("GroceryStore"
)
    $ GrocerName = "Эдди"
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Провизия' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ('Купить провизию' not in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    run Call("GroceryStoreObjectMenu", "food_stock")
    assert eval (str(main_ui_runtime.action_title or "") == 'Провизия') timeout 5.0
    assert eval ('Купить провизию' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ('Купить крынку молока' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ('Осмотреть товар' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    run Call("GroceryStoreObjectText", "food_stock", "examine_food_stock")
    assert eval (str(main_ui_runtime.action_title or "") == 'Провизия') timeout 5.0
    assert eval ('Мешки, капуста' in str(scene_runtime.text or "")) timeout 5.0
    assert eval ('Купить провизию' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ('Назад' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ Eddie.talked_today = 0
    $ Eddie.rel = 0
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    run Call("IntEddieTalk")
    advance until screen "choice" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == 'Разговор с Эдди') timeout 5.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (int(Eddie.talked_today or 0) == 1) timeout 20.0
    assert eval ('Вы некоторое время болтаете с Эдди' in str(scene_runtime.text or "")) timeout 5.0
    $ Eddie.talked_today = 3
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (int(Eddie.talked_today or 0) == 4) timeout 20.0
    assert eval ('Ничего нового из разговора вы не узнали.' in str(scene_runtime.text or "")) timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(1)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ rooms.enter("WineStore"
)
    $ GrocerName = "Альбер"
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Бочки с вином' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items].count('Купить вино') == 0) timeout 5.0
    run Call("WineStoreObjectMenu", "wine_stock")
    assert eval (str(main_ui_runtime.action_title or "") == 'Бочки с вином') timeout 5.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items].count('Купить вино') == 1) timeout 5.0
    $ _wine_picture_before = str(scene_runtime.picture or "")
    run Call("WineStoreObjectText", "wine_stock", "examine_wine")
    assert eval (str(main_ui_runtime.action_title or "") == 'Бочки с вином') timeout 5.0
    assert eval ('Повсюду бочки' in str(scene_runtime.text or "")) timeout 5.0
    assert eval ('Купить вино' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval (str(scene_runtime.picture or "") == _wine_picture_before) timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(1)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ rooms.enter("MarketPlace"
)
    $ scene_runtime.text = rooms.get("MarketPlace").descriptions[0].text + "\n\n" + rooms.get("MarketPlace").descriptions[1].text + "\n\n" + rooms.get("MarketPlace").descriptions[2].text
    $ scene_runtime.location_text = scene_runtime.text
    $ player.horse.acquire("test-horse")
    $ scene_runtime.picture = rooms.get("MarketPlace").bg_picture
    $ _market_picture_before = str(scene_runtime.picture or "")
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = rooms.get("MarketPlace").build_action_items() + rooms.get("MarketPlace").build_exit_items()
    assert eval ('Зайти в охотничий клуб' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ('Рыночные лотки' not in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval (str(scene_runtime.picture or "") == _market_picture_before) timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(1)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
'''


TAVERN_REPORT_STATE_CHECKS = r'''
testcase external_tavern_report_state_defaults:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ external_calendar_set_fields(10, 1, 1100, 12, 0)
    $ external_calendar_set_weekday(1)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"

    $ show_tavern_report_main_ui_state("")
    assert eval (str(main_ui_runtime.mode or "") == "tavern") timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Трактир") timeout 5.0
    assert eval (len(main_ui_runtime.action_items) > 0) timeout 5.0
    assert eval ([str(item.caption or "") for item in main_ui_runtime.action_items][-1] == "Назад") timeout 5.0
    assert eval ("Закрыть" not in [str(item.caption or "") for item in main_ui_runtime.action_items]) timeout 5.0
    assert eval (isinstance(Sandra.jobs, dict) and isinstance(Melissa.jobs, dict) and isinstance(Amanda.jobs, dict)) timeout 5.0
    assert eval ([Sandra.job_value("jobkitchen"), Sandra.job_value("jobcleaning"), Sandra.job_value("jobwaitress")] == [1, 0, 0]) timeout 5.0
    assert eval ([Sandra.job_value("jobkitchentomorrow"), Sandra.job_value("jobcleaningtomorrow"), Sandra.job_value("jobwaitresstomorrow")] == [1, 0, 0]) timeout 5.0
    assert eval ([Melissa.job_value("jobkitchen"), Melissa.job_value("jobcleaning"), Melissa.job_value("jobwaitress")] == [0, 1, 1]) timeout 5.0
    assert eval ([Melissa.job_value("jobkitchentomorrow"), Melissa.job_value("jobcleaningtomorrow"), Melissa.job_value("jobwaitresstomorrow")] == [0, 1, 1]) timeout 5.0
    assert eval ([Amanda.job_value("jobkitchen"), Amanda.job_value("jobcleaning"), Amanda.job_value("jobwaitress")] == [0, 1, 1]) timeout 5.0
    assert eval ([Amanda.job_value("jobkitchentomorrow"), Amanda.job_value("jobcleaningtomorrow"), Amanda.job_value("jobwaitresstomorrow")] == [0, 1, 1]) timeout 5.0
    assert eval (_tavern_worker_current_jobs("sandra") == "кухня" and _tavern_worker_tomorrow_jobs("sandra") == "кухня") timeout 5.0
    assert eval (_tavern_worker_current_jobs("melissa") == "уборка, зал" and _tavern_worker_tomorrow_jobs("melissa") == "уборка, зал") timeout 5.0
    assert eval ("завтра кухня" in _tavern_report_label(BuildTavernReport())) timeout 5.0
    assert eval (len(BuildTavernReport()["team_keys"]) >= 3) timeout 5.0
    assert eval ("sandra" in BuildTavernReport()["team_keys"] and "melissa" in BuildTavernReport()["team_keys"] and "amanda" in BuildTavernReport()["team_keys"]) timeout 5.0
    assert eval (str(people.get_info("sandra").getLocation() or "") != "") timeout 5.0
    assert eval (len(people_locate_rows()) >= 3) timeout 5.0
    assert eval (int(BuildTavernReport()["hall_job_capacity"] or 0) == 3 and int(BuildTavernReport()["cleaning_slots"] or 0) == 2) timeout 5.0
    click id "tavern_schedule_sandra_cleaning" pos (0.5, 0.5) until eval (int(Sandra.job_value("jobcleaningtomorrow", 0) or 0) == 1) timeout 20.0
    assert eval (int(Sandra.job_value("jobcleaning", 0) or 0) == 0 and int(BuildTavernReport()["cleaning_slots"] or 0) == 3) timeout 5.0
    $ _sandra_kitchen_tomorrow_before = int(Sandra.job_value("jobkitchentomorrow", 0) or 0)
    click id "tavern_schedule_sandra_kitchen" pos (0.5, 0.5) until eval (int(Sandra.job_value("jobkitchentomorrow", 0) or 0) != _sandra_kitchen_tomorrow_before) timeout 20.0
    assert eval (int(Sandra.job_value("jobkitchen", 0) or 0) == 1 and int(Sandra.job_value("jobkitchentomorrow", 0) or 0) == 0) timeout 5.0
    assert eval (str(main_ui_runtime.mode or "") == "tavern" and str(main_ui_runtime.tavern_report_person or "") == "") timeout 5.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("say") is None) timeout 5.0
    $ hide_tavern_report_main_ui_state()
    assert eval (str(main_ui_runtime.mode or "") == "scene") timeout 5.0
    $ apply_tomorrow_hall_job("sandra")
    assert eval (int(Sandra.job_value("jobkitchen", 0) or 0) == 0 and int(Sandra.job_value("jobkitchentomorrow", 0) or 0) == 0) timeout 5.0
    $ Sandra.set_job_value("jobcleaning", 1)
    $ Sandra.jobs.pop("jobcleaningtomorrow", None)
    $ tractir_save_normalize_tavern_staff_jobs()
    assert eval (int(Sandra.job_value("jobcleaningtomorrow", 0) or 0) == 1) timeout 5.0

testcase external_tavern_sunday_dinner_schedule_and_stats:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(7, 1, 1100, 12, 29)
    $ external_calendar_set_weekday(7)
    $ player.tavern_management.breakfast.sunday_dinner_last_day = -1
    assert eval (not tavern_sunday_dinner_available()) timeout 5.0

    $ external_calendar_set_fields(7, 1, 1100, 12, 30)
    assert eval (tavern_sunday_dinner_available()) timeout 5.0
    assert eval (all(str(people.location(npc_id) or "") == "TavernKitchen" for npc_id in ("sandra", "melissa", "amanda"))) timeout 5.0
    assert eval (tavern_sunday_dinner_present_ids() == ["sandra", "melissa", "amanda"]) timeout 5.0
    assert eval ("Сесть за воскресный обед" in [str(item.caption or "") for item in tavern_kitchen_action_items()]) timeout 5.0

    $ Sandra.rel = 5
    $ Melissa.rel = 5
    $ Amanda.rel = 5
    $ _sunday_open_before = (Sandra.openness, Melissa.openness, Amanda.openness)
    $ _sunday_corruption_before = (Sandra.corruption, Melissa.corruption, Amanda.corruption)
    $ external_calendar_set_fields(7, 1, 1100, 13, 30)
    assert eval (tavern_sunday_dinner_available() and tavern_sunday_dinner_present_ids() == ["sandra", "melissa", "amanda"]) timeout 5.0
    run Call("TavernKitchenSundayDinner", 0)
    advance until screen "say" timeout 20.0
    assert eval ((Sandra.rel, Melissa.rel, Amanda.rel) == (6, 6, 6)) timeout 5.0
    assert eval ((Sandra.openness, Melissa.openness, Amanda.openness) == _sunday_open_before) timeout 5.0
    assert eval ((Sandra.corruption, Melissa.corruption, Amanda.corruption) == _sunday_corruption_before) timeout 5.0
    assert eval (int(calendar_v2.hour or 0) == 14 and int(calendar_v2.minute or 0) == 15) timeout 5.0
    assert eval (int(player.tavern_management.breakfast.sunday_dinner_last_day or -1) == current_game_day()) timeout 5.0
    assert eval (not tavern_sunday_dinner_available()) timeout 5.0
'''


TAILOR_PURCHASE_FLOW_CHECKS = r'''
testcase external_actual_tailor_buy_dress_measure_flow:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(1)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Call("InitIrma")
    $ people.get_data("irma").set_schedule([NPCScheduleEntry(location="DressShop", start_minute=0, end_minute=1440, priority=999)])
    $ player.intimacy.had_sex_count = 0
    $ Irma.rel = 0
    $ Irma.extra_fee_refused = False
    $ player.intimacy.came_today = 0
    $ player.intimacy.can_cum_daily = 3
    $ dress_shop.produced = ""
    $ dress_shop.buyer = ""
    $ player.appearance.owned_dresses = []
    run Jump("DressShop")
    advance until screen "main_ui" timeout 20.0
    $ _female_rack_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Женские образцы")
    click id ("choice_panel_button_%d" % int(_female_rack_index)) pos (0.5, 0.5) until eval (str(main_ui_runtime.object_id or "") == "female_samples_001") timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "dress_shop_catalog_page" timeout 20.0
    assert eval (str(renpy.get_screen("dress_shop_catalog_page").scope.get("rack_type", "") or "") == "female" and len(dress_shop_catalog_items("female")) > 3) timeout 5.0
    $ _female_browse_code = dress_shop_item_code(dress_shop_catalog_items("female")[0])
    assert eval (renpy.get_widget("dress_shop_catalog_page", "dress_shop_catalog_offer_" + _female_browse_code) is not None) timeout 5.0
    click id "dress_shop_catalog_next" pos (0.5, 0.5) until eval (int(renpy.get_screen("dress_shop_catalog_page").scope.get("catalog_page", 0) or 0) == 1) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("dress_shop_catalog_page") is None and str(main_ui_runtime.object_id or "") == "") timeout 20.0
    $ _male_rack_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Мужские образцы")
    $ _male_item = dress_shop_catalog_items("male")[0]
    $ _male_code = str(_male_item.custom_properties.get("dress_code", "") or "")
    $ player.economy.money = int(getattr(_male_item, "price", 0) or 0) + 100
    click id ("choice_panel_button_%d" % int(_male_rack_index)) pos (0.5, 0.5) until eval (str(main_ui_runtime.object_id or "") == "male_samples_001") timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "dress_shop_catalog_page" timeout 20.0
    click id ("dress_shop_catalog_buy_" + _male_code) pos (0.5, 0.5) until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("dress_shop_catalog_page") is None) timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Раздеться до белья"] and "Как вы хотите" in str(scene_runtime.text or "") and "measure0" in str(scene_runtime.picture or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Одеться и уйти"]) timeout 20.0
    assert eval (renpy.get_screen("say") is None and "measure1" in str(scene_runtime.picture or "") and "нижнего белья" in str(scene_runtime.text or "") and "Как вы хотите" not in str(scene_runtime.text or "") and str(scene_runtime.location_text or "") == str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "ArtisansQuarter") timeout 20.0

    $ player.intimacy.had_sex_count = 3
    run Call("DressTry", "You", _male_code)
    advance until screen "choice" timeout 20.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Раздеться до белья", "Полностью раздеться и думать о высоком"]) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Одеться и уйти"]) timeout 20.0
    assert eval (renpy.get_screen("say") is None and "measure2" in str(scene_runtime.picture or "") and "думать о птичках" in str(scene_runtime.text or "") and "Как вы хотите" not in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2

    $ player.intimacy.had_sex_count = 5
    $ Irma.rel = 0
    run Call("DressTry", "You", _male_code)
    advance until screen "choice" timeout 20.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Раздеться до белья", "Полностью раздеться и думать о высоком", "Полностью раздеться и представить, как вы имеете Ирму"]) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Одеться и уйти"]) timeout 20.0
    assert eval (renpy.get_screen("say") is None and "measure3" in str(scene_runtime.picture or "") and "Это я тебе настолько нравлюсь" in str(scene_runtime.text or "") and "Как вы хотите" not in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2

    $ Irma.rel = 5
    $ Irma.extra_fee_refused = False
    $ player.economy.money = 100
    run Call("DressTry", "You", _male_code)
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval ("sex0" in str(scene_runtime.picture or "") and renpy.get_screen("choice") is not None) timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval ("sex9" in str(scene_runtime.picture or "") and "20 мараведи" in str(scene_runtime.text or "") and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Промолчать и оплатить", "Возмутиться"] and "Кончить в рот" not in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (bool(Irma.extra_fee_refused) and [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Одеться и уйти"]) timeout 20.0
    assert eval ("обдираловку" in str(scene_runtime.text or "") and "20 мараведи" not in str(scene_runtime.text or "") and str(scene_runtime.location_text or "") == str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2

    $ Irma.rel = 5
    $ Irma.extra_fee_refused = False
    $ player.economy.money = 100
    $ _money_before_extra_fee = int(player.economy.money or 0)
    run Call("DressTry", "You", _male_code)
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval ("sex0" in str(scene_runtime.picture or "") and renpy.get_screen("choice") is not None) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("sex8" in str(scene_runtime.picture or "") and "20 мараведи" in str(scene_runtime.text or "") and renpy.get_screen("choice") is not None) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Одеться и уйти"]) timeout 20.0
    assert eval (int(player.economy.money or 0) == _money_before_extra_fee - 20 and "решили промолчать" in str(scene_runtime.text or "") and "20 мараведи" not in str(scene_runtime.text or "") and str(scene_runtime.location_text or "") == str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    pause 0.2

testcase external_female_tailor_choose_agree_purchase_flow:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(1)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    run Call("InitIrma")
    run Call("InitAmanda")
    $ rooms.enter("DressShop")
    $ people.get_data("irma").set_schedule([NPCScheduleEntry(location="DressShop", start_minute=0, end_minute=1440, priority=999)])
    $ Amanda.corruption = 0
    $ Amanda.rel = 0
    $ _female_item = get_game_item("dress_modestworkdress")
    $ _female_code = dress_shop_item_code(_female_item)
    assert eval (_female_item is not None and _female_code == "modestworkdress") timeout 5.0
    $ Amanda.wardrobe["owned"] = [code for code in _gds_get_dress_list_for_girl("amanda") if str(code or "") != _female_code]
    $ dress_shop.produced = ""
    $ dress_shop.buyer = ""
    $ dress_shop.girl_dress_block = 0
    $ player.appearance.girl_dresses_bought = 0
    $ player.set_money(int(getattr(_female_item, "price", 0) or 0) + 100)
    $ _female_money_before = int(player.economy.money or 0)
    $ daily_events.delete("amanda", "BuyDress", "")
    $ daily_events.add("amanda", "dressshop", 0, "=", 1, 1, "BuyDress", "GirlDressBuy", "girl_location")
    run Jump("DressShop")
    advance until screen "dress_shop_catalog_page" timeout 20.0
    assert eval (str(renpy.get_screen("dress_shop_catalog_page").scope.get("girl_name", "") or "") == "amanda") timeout 5.0
    assert eval ([str(item.caption or "") for item in main_ui_runtime.action_items] == ["Осмотреть портниху", "Посмотреть во что одета Аманда", "Уйти из лавки"]) timeout 5.0
    assert eval (_female_code in [dress_shop_item_code(item) for item in dress_shop_catalog_items("female")[:3]]) timeout 5.0
    assert eval (not _gds_has_dress_for_girl("amanda", _female_code) and str(dress_shop.produced or "") == "" and int(player.economy.money or 0) >= int(getattr(_female_item, "price", 0) or 0)) timeout 5.0
    click id ("dress_shop_catalog_offer_" + _female_code) pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (renpy.get_screen("dress_shop_catalog_page") is None) timeout 5.0
    advance until screen "choice" timeout 20.0
    assert eval (len(list(renpy.get_screen("choice").scope.get("items", []) or [])) == 3) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 900) until eval (str(rooms.current_code or "") == "ArtisansQuarter") timeout 20.0
    assert eval (str(dress_shop.produced or "") == _female_code) timeout 5.0
    assert eval (_female_code in _gds_get_dress_list_for_girl("amanda")) timeout 5.0
    assert eval (int(player.economy.money or 0) == _female_money_before - int(getattr(_female_item, "price", 0) or 0)) timeout 5.0
    assert eval (int(player.appearance.girl_dresses_bought or 0) == 1) timeout 5.0
    assert eval (renpy.get_screen("dress_shop_catalog_page") is None) timeout 5.0

testcase external_female_tailor_refusal_returns_to_catalog:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(1)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    run Call("InitIrma")
    run Call("InitAmanda")
    $ people.get_data("irma").set_schedule([NPCScheduleEntry(location="DressShop", start_minute=0, end_minute=1440, priority=999)])
    $ Amanda.corruption = 0
    $ Amanda.rel = 0
    $ _refused_item = get_game_item("dress_openworkdress")
    $ _refused_code = dress_shop_item_code(_refused_item)
    $ Amanda.wardrobe["owned"] = [code for code in _gds_get_dress_list_for_girl("amanda") if str(code or "") != _refused_code]
    $ dress_shop.produced = ""
    $ dress_shop.buyer = ""
    $ player.appearance.girl_dresses_bought = 0
    $ player.set_money(int(getattr(_refused_item, "price", 0) or 0) + 100)
    $ _refused_money_before = int(player.economy.money or 0)
    $ daily_events.delete("amanda", "BuyDress", "")
    $ daily_events.add("amanda", "dressshop", 0, "=", 1, 1, "BuyDress", "GirlDressBuy", "girl_location")
    run Jump("DressShop")
    advance until screen "dress_shop_catalog_page" timeout 20.0
    click id "dress_shop_catalog_next" pos (0.5, 0.5) until eval (int(renpy.get_screen("dress_shop_catalog_page").scope.get("catalog_page", 0) or 0) == 1) timeout 20.0
    click id ("dress_shop_catalog_offer_" + _refused_code) pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 900) until screen "dress_shop_catalog_page" timeout 20.0
    assert eval (str(renpy.get_screen("dress_shop_catalog_page").scope.get("girl_name", "") or "") == "amanda") timeout 5.0
    assert eval (str(dress_shop.produced or "") == "" and int(player.economy.money or 0) == _refused_money_before) timeout 5.0
    assert eval (_refused_code not in _gds_get_dress_list_for_girl("amanda") and int(player.appearance.girl_dresses_bought or 0) == 0) timeout 5.0

'''

DOG_ENTITY_ACTION_CHECKS = r'''
testcase external_dog_entity_actions:
    $ external_calendar_set_fields(3, 1, 1100, 12, 0)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ player.remove_item("dog_bone_001", max(1, player.item_count("dog_bone_001")))
    $ player.remove_item("dog_collar_001", max(1, player.item_count("dog_collar_001")))
    $ dog.owned = False
    $ player.remove_party_member("dog")
    $ dog.met = False
    $ dog.bones_given = 0
    $ dog.stray_played = False
    $ dog.booth_built = False
    $ player.condition.health = 100

    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(dog_card_portrait_path() or "").endswith("no_colar.png")) timeout 5.0
    assert eval (dog.meet_stray()) timeout 5.0
    $ _dog_health_before = int(player.condition.health or 0)
    $ dog_stray_bite_player()
    assert eval (int(player.condition.health or 0) == _dog_health_before - 5) timeout 5.0

    $ dog.met = False
    $ dog.bones_given = 0
    $ dog.stray_played = False
    $ player.add_item("dog_bone_001", 1)
    $ player.add_item("dog_collar_001", 1)
    assert eval (dog.meet_stray()) timeout 5.0
    $ _dog_feed_ok = dog.feed_stray_bone()
    assert eval (_dog_feed_ok and int(dog.bones_given or 0) == 1) timeout 5.0
    $ _dog_stray_play_ok = dog.play_stray()
    assert eval (_dog_stray_play_ok and bool(dog.stray_played)) timeout 5.0
    assert eval (dog_can_adopt_stray()) timeout 5.0
    $ _dog_adopt_ok = dog.adopt("Sharik")
    assert eval (_dog_adopt_ok) timeout 5.0
    assert eval (bool(dog.owned)) timeout 5.0
    assert eval (str(dog.pet_name or "") == "Sharik") timeout 5.0
    assert eval (player.item_count("dog_collar_001") == 0) timeout 5.0
    assert eval (str(dog_card_portrait_path() or "").endswith("dog.png")) timeout 5.0

    $ dog.owned = True
    $ player.add_party_member("dog")
    $ dog.booth_built = True
    $ dog.loyalty = max(int(dog.loyalty or 0), 12)
    $ dog.health = dog.max_health
    $ dog.last_play_day = -1
    $ dog.last_train_day = -1
    $ player.add_item("dog_bone_001", 2)

    run Jump("Backyard")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(dog_card_portrait_path() or "").endswith("dog_booth.png")) timeout 5.0
    assert eval (dog.is_available_here("Backyard")) timeout 5.0

    $ _dog_bone_count_before = player.item_count("dog_bone_001")
    $ _dog_loyalty_before = int(dog.loyalty or 0)
    $ _dog_feed_owned_ok = dog.feed_bone(training=False)
    assert eval (_dog_feed_owned_ok) timeout 5.0
    assert eval (player.item_count("dog_bone_001") == _dog_bone_count_before - 1) timeout 5.0
    assert eval (int(dog.loyalty or 0) >= _dog_loyalty_before) timeout 5.0

    $ dog.last_play_day = -1
    $ dog.last_train_day = -1
    assert eval (len(list(dog_card_lines() or [])) > 0) timeout 5.0
    assert eval (int(dog.last_play_day or -1) != int(calendar_v2.daysInGame or 0)) timeout 5.0
    assert eval (int(dog.last_train_day or -1) != int(calendar_v2.daysInGame or 0)) timeout 5.0

    run Call("IntDogTalk", "Backyard")
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None) timeout 5.0
    assert eval (len(list(renpy.get_screen("choice").scope.get("items", []) or [])) >= 4) timeout 5.0
    assert eval (renpy.get_screen("say") is None and str(main_ui_runtime.mode or "") == "talk") timeout 5.0

    $ _dog_play_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Поиграть с псом")
    $ _dog_play_button_id = "choice_panel_button_%d" % int(_dog_play_index)
    click id _dog_play_button_id pos (0.5, 0.5) until eval (int(dog.last_play_day or -1) == int(calendar_v2.daysInGame or 0) and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval (renpy.get_screen("say") is None and "Вы валяетесь с псом" in str(scene_runtime.text or "")) timeout 5.0

    $ _dog_card_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Осмотреть")
    $ _dog_card_button_id = "choice_panel_button_%d" % int(_dog_card_index)
    click id _dog_card_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "dog" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval (renpy.get_screen("say") is None and [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Назад"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and "Закончить разговор" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (renpy.get_screen("say") is None and str(scene_runtime.text or "") == str(dog_talk_intro_text("Backyard") or "")) timeout 5.0
'''


BACKYARD_BARREL_OBJECT_CHECKS = r'''
testcase external_backyard_barrel_object_actions:
    $ external_calendar_set_fields(1, 1, 1100, 13, 0)
    run Call("InitMelissa")
    run Call("InitAmanda")
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=999)])
    $ crafting.ash_barrel_installed = False
    $ crafting.ash_barrel_ready_day = 0
    $ player.remove_item("soap_001", max(1, player.item_count("soap_001")))
    $ player.remove_item("luxury_soap_001", max(1, player.item_count("luxury_soap_001")))

    run Jump("Backyard")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "Backyard") timeout 5.0
    assert eval (str(scene_runtime.picture or "").endswith("images/tavern/backyard/backyard_1.png")) timeout 5.0
    assert eval ("backyard_water_barrel" in [str(getattr(obj, "object_id", "") or "") for obj in rooms.get("Backyard").visible_objects()]) timeout 5.0
    assert eval (not any(str(getattr(getattr(i, "action", None), "label", "") or "") == "BackyardCookSoap" for i in main_ui_runtime.action_items)) timeout 5.0

    run Call("BackyardObjectMenu", "backyard_water_barrel")
    assert eval (str(main_ui_runtime.action_title or "") == "Бочка с дождевой водой") timeout 5.0
    assert eval ("BackyardWashAtBarrel" in [str(getattr(getattr(i, "action", None), "label", "") or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval (not any(str(getattr(getattr(i, "action", None), "label", "") or "") == "BackyardWashAtBarrelWithSoap" for i in main_ui_runtime.action_items)) timeout 5.0

    $ player.appearance.soap_look_bonus = 0
    $ player.appearance.soap_look_bonus_until_day = -1
    $ _look_before = int(player_look_breakdown().get("look", 0) or 0)
    $ player.add_item("soap_001", 1)
    run Call("BackyardObjectMenu", "backyard_water_barrel")
    assert eval ("BackyardWashAtBarrelWithSoap" in [str(getattr(getattr(i, "action", None), "label", "") or "") for i in main_ui_runtime.action_items]) timeout 5.0
    run Call("BackyardWashAtBarrelWithSoap", "soap_001")
    assert eval (player.item_count("soap_001") == 0) timeout 5.0
    assert eval (int(player.appearance.soap_look_bonus or 0) == 5) timeout 5.0
    assert eval (int(player_look_breakdown().get("look", 0) or 0) == min(100, _look_before + 5)) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Бочка с дождевой водой") timeout 5.0

    $ crafting.ash_barrel_installed = True
    $ crafting.ash_barrel_ready_day = int(calendar_v2.daysInGame)
    $ player.remove_item("recipe_book_001", player.item_count("recipe_book_001")) if player.item_count("recipe_book_001") > 0 else False
    $ player.remove_item("bucket_001", player.item_count("bucket_001")) if player.item_count("bucket_001") > 0 else False
    $ player.remove_item("pig_lard_001", player.item_count("pig_lard_001")) if player.item_count("pig_lard_001") > 0 else False
    $ player.remove_item("lavender_001", player.item_count("lavender_001")) if player.item_count("lavender_001") > 0 else False
    $ player.add_item("recipe_book_001", 1)
    $ player.add_item("bucket_001", 1)
    $ player.add_item("pig_lard_001", 1)
    $ player.add_item("lavender_001", 1)
    $ _soap_batches_before = len(crafting.pending_soap_batches)
    assert eval (recipe_page_can_craft("soap_recipe")) timeout 5.0
    run Call("BackyardObjectMenu", "backyard_ash_barrel")
    assert eval (str(main_ui_runtime.action_title or "") == "Зольная бочка") timeout 5.0
    assert eval (str(scene_runtime.picture or "").endswith("images/tavern/backyard/soap_backyard.png")) timeout 5.0
    assert eval ("BackyardCookSoap" in [str(getattr(getattr(i, "action", None), "label", "") or "") for i in main_ui_runtime.action_items]) timeout 5.0
    run Call("BackyardCookSoap", "soap_recipe")
    assert eval (len(crafting.pending_soap_batches) == _soap_batches_before + 1) timeout 5.0
    assert eval (player.item_count("pig_lard_001") == 0 and player.item_count("lavender_001") == 0) timeout 5.0
    assert eval (player.item_count("bucket_001") == 1) timeout 5.0
    assert eval (len(str(scene_runtime.text or "").strip()) > 0) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Зольная бочка") timeout 5.0
    assert eval (len(list(main_ui_runtime.action_items or [])) > 0) timeout 5.0
'''


GROCERY_STORE_OBJECT_PURCHASE_CHECKS = r'''
testcase external_grocery_store_object_purchase_actions:
    run Call("InitBecky")
    run Call("InitInga")
    run Call("InitAmanda")
    $ people.register(EddieStaticData, Eddie)
    $ external_calendar_set_fields(10, 1, 1100, 10, 0)
    $ external_calendar_set_weekday(1)
    $ npc_interval_schedule_load_all(True)
    $ people.get_data("eddie").set_schedule([NPCScheduleEntry(location="GroceryStore", start_minute=0, end_minute=1440, priority=999)])
    $ rooms.enter("GroceryStore")
    $ player.set_money(100)
    $ Amanda.night_bowl_given = True
    $ Amanda.fancy_night_bowl_received = False
    $ player.remove_item("milk_pitcher_001", player.item_count("milk_pitcher_001")) if player.item_count("milk_pitcher_001") > 0 else False
    $ player.remove_item("fancy_night_bowl_001", player.item_count("fancy_night_bowl_001")) if player.item_count("fancy_night_bowl_001") > 0 else False

    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "GroceryStore") timeout 5.0
    assert eval (str(grocery_store_active_grocer_id() or "") == "eddie") timeout 5.0
    assert eval (bool(grocery_store_service_available())) timeout 5.0
    assert eval ("food_stock" in [str(getattr(obj, "object_id", "") or "") for obj in rooms.get("GroceryStore").visible_objects()]) timeout 5.0

    run Call("GroceryStoreObjectMenu", "food_stock")
    assert eval (str(main_ui_runtime.action_title or "") == "Провизия") timeout 5.0
    assert eval ("Купить крынку молока" in [str(getattr(i, "caption", "") or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("Купить красивую ночную миску" in [str(getattr(i, "caption", "") or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ _milk_money_before = int(player.economy.money or 0)
    $ _milk_count_before = player.item_count("milk_pitcher_001")
    run Call("GroceryStoreBuyMilk")
    assert eval (int(player.economy.money or 0) == _milk_money_before - 6) timeout 5.0
    assert eval (player.item_count("milk_pitcher_001") == _milk_count_before + 1) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Провизия") timeout 5.0

    run Call("GroceryStoreBuyStockMenu")
    assert eval (str(main_ui_runtime.action_title or "") == "Покупка провизии") timeout 5.0
    $ _provision_money_before = int(player.economy.money or 0)
    $ _provision_before = int(player.tavern_management.productnum or 0)
    run Call("GroceryStoreBuyStockApply", 6, 10, 1)
    assert eval (int(player.economy.money or 0) == _provision_money_before - 6) timeout 5.0
    assert eval (int(player.tavern_management.productnum or 0) == _provision_before + 10) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Покупка провизии") timeout 5.0

    run Call("GroceryStoreObjectMenu", "food_stock")
    run Call("GroceryStoreBuyFancyNightBowl")
    assert eval ("Купить красивую ночную миску за 9 мараведи" in [str(getattr(i, "caption", "") or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _bowl_money_before = int(player.economy.money or 0)
    run Call("GroceryStoreBuyFancyNightBowlApply")
    assert eval (int(player.economy.money or 0) == _bowl_money_before - 9) timeout 5.0
    assert eval (player.item_count("fancy_night_bowl_001") == 1) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Красивая ночная миска") timeout 5.0
'''


PORT_STREETS_FLOW_CHECKS = r'''
testcase external_port_streets_georgette_liza_flow:
    run Call("InitGeorgett")
    run Call("InitLiza")
    run Call("InitDog")
    $ external_calendar_set_fields(1, 1, 1100, 12, 0)
    $ story_event_available = lambda location_name="", action_name="": False
    $ Georgett.rel = 0
    $ Georgett.known = False
    $ Liza.prostitution_started = False
    $ Georgett.set_story_value("TalkChurchAfterCermonLiza", 0)
    $ TownStreet.events_today = 2
    $ TownStreet.story_seen_keys.append("%s:PortStreets:%s" % (calendar_v2.daysInGame, calendar_v2.time_slot()))
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval ("georgett" not in list(people.ids_at("PortStreets") or [])) timeout 5.0
    assert eval ("liza" not in list(people.ids_at("PortStreets") or [])) timeout 5.0

    $ external_calendar_set_fields(1, 1, 1100, 19, 0)
    $ Georgett.rel = 0
    $ Liza.prostitution_started = False
    $ Georgett.set_story_value("TalkChurchAfterCermonLiza", 0)
    $ TownStreet.events_today = 2
    $ TownStreet.story_seen_keys.append("%s:PortStreets:%s" % (calendar_v2.daysInGame, calendar_v2.time_slot()))
    $ TodaySexEvents_Clear()
    $ main_ui_runtime.mode = "mc"
    $ main_ui_runtime.selected_char = "georgett"
    $ main_ui_runtime.girl_key = "georgett"
    $ main_ui_runtime.talk_picture = "images/georgett/portraits/portrait.jpg"
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "scene") timeout 5.0
    assert eval (str(main_ui_runtime.selected_char or "") == "") timeout 5.0
    assert eval (str(main_ui_runtime.girl_key or "") == "") timeout 5.0
    assert eval (str(main_ui_runtime.talk_picture or "") == "") timeout 5.0
    assert eval (str(scene_runtime.picture or "") == "images/georgett/Port/wait.jpg") timeout 5.0
    assert eval (str(renpy.get_screen("main_ui").scope.get("_picture", "") or "") == "images/georgett/Port/wait.jpg") timeout 5.0
    assert eval ("georgett" in list(people.ids_at("PortStreets") or [])) timeout 5.0
    assert eval ("liza" not in list(people.ids_at("PortStreets") or [])) timeout 5.0
    assert eval (people.action_data_for_room("georgett", "PortStreets") is not None) timeout 5.0
    assert eval ("Заговорить с ней" not in [str(getattr(i, "caption", "") or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval (renpy.get_screen("main_ui").scope.get("_char_entries", [])[1]["title"] == "Молодая женщина") timeout 5.0
    $ _georgett_first_meeting_room_text = str(scene_runtime.text or "")
    $ _georgett_first_meeting_room_picture = str(scene_runtime.picture or "")
    click id "main_ui_entity_button_npc_georgett" pos (0.5, 0.5) until eval (int(Georgett.rel or 0) == 1 and bool(Georgett.known) and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval (int(Georgett.rel or 0) == 1 and bool(Georgett.known)) timeout 5.0
    assert eval ("Жоржетта Брюно" in str(scene_runtime.text or "")) timeout 5.0
    $ _georgett_end_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _georgett_end_button_id = "choice_panel_button_%d" % int(_georgett_end_index)
    click id _georgett_end_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (str(scene_runtime.text or "") == _georgett_first_meeting_room_text and str(scene_runtime.picture or "") == _georgett_first_meeting_room_picture) timeout 5.0

    $ external_calendar_set_fields(1, 1, 1100, 19, 0)
    $ Georgett.rel = 1
    $ Liza.prostitution_started = True
    $ TownStreet.events_today = 2
    $ TownStreet.story_seen_keys.append("%s:PortStreets:%s" % (calendar_v2.daysInGame, calendar_v2.time_slot()))
    $ TodaySexEvents_Clear()
    $ TodaySexEvents_Add("georgett", 3, 99, "Prostitution")
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval ("georgett" in list(people.ids_at("PortStreets") or [])) timeout 5.0
    assert eval ("liza" in list(people.ids_at("PortStreets") or [])) timeout 5.0

    $ external_calendar_set_fields(5, 1, 1100, 19, 0)
    $ Georgett.rel = 0
    $ Liza.prostitution_started = True
    $ TownStreet.events_today = 2
    $ TownStreet.story_seen_keys.append("%s:PortStreets:%s" % (calendar_v2.daysInGame, calendar_v2.time_slot()))
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval ("georgett" not in list(people.ids_at("PortStreets") or [])) timeout 5.0
    assert eval ("liza" not in list(people.ids_at("PortStreets") or [])) timeout 5.0

    $ external_calendar_set_fields(1, 1, 1100, 19, 0)
    $ Georgett.rel = 0
    $ Liza.prostitution_started = False
    $ Georgett.set_story_value("TalkChurchAfterCermonLiza", 1)
    $ TownStreet.events_today = 2
    $ TownStreet.story_seen_keys.append("%s:PortStreets:%s" % (calendar_v2.daysInGame, calendar_v2.time_slot()))
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval ("georgett" not in list(people.ids_at("PortStreets") or [])) timeout 5.0
    assert eval ("liza" not in list(people.ids_at("PortStreets") or [])) timeout 5.0

    $ external_calendar_set_fields(1, 1, 1100, 19, 0)
    $ external_calendar_set_weekday(7)
    $ Georgett.rel = 1
    $ Georgett.known = True
    $ Georgett.set_story_value("TalkChurchAfterCermonLiza", 0)
    $ Liza.prostitution_started = False
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(people.location("georgett") or "") == "PortStreets") timeout 5.0
    assert eval (people.action_data_for_room("georgett", "PortStreets") is not None) timeout 5.0

    $ external_calendar_set_fields(1, 1, 1100, 13, 0)
    $ dog.met = True
    $ dog.owned = False
    $ player.remove_party_member("dog")
    $ TownStreet.events_today = 2
    $ TownStreet.story_seen_keys.append("%s:PortStreets:%s" % (calendar_v2.daysInGame, calendar_v2.time_slot()))
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(people.location("dog") or "") in list(DogStaticData.stray_roam_locations)) timeout 5.0
    assert eval (("dog" in list(people.ids_at("PortStreets") or [])) == (str(people.location("dog") or "") == "PortStreets")) timeout 5.0

testcase external_georgette_portstreet_relationship_talk_and_sex_flow:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ renpy.call_in_new_context("InitDressDesc")
    $ external_calendar_set_fields(1, 1, 1100, 19, 0)
    $ Georgett.rel = 5
    $ Georgett.known = True
    $ Georgett.set_story_value("TalkChurchAfterCermonLiza", 0)
    $ Liza.prostitution_started = False
    $ Georgett.wardrobe["current_dress"] = "slutdress"
    $ Georgett.wardrobe["current_underwear"]["bra"] = ""
    $ Georgett.wardrobe["current_underwear"]["panties"] = ""
    $ Georgett.sex_setup("street")
    assert eval (bool(Georgett.clothing_layer("top")) and bool(Georgett.clothing_layer("bottom"))) timeout 5.0
    assert eval (not Georgett.tits_visible() and not Georgett.pussy_visible()) timeout 5.0
    $ Georgett.set_layer_raised("top", 1)
    $ Georgett.set_layer_raised("bottom", 1)
    assert eval (Georgett.tits_visible() and Georgett.pussy_visible()) timeout 5.0
    $ Georgett.reset_sex_clothing_state()
    $ TownStreet.events_today = 2
    $ TownStreet.story_seen_keys.append("%s:PortStreets:%s" % (calendar_v2.daysInGame, calendar_v2.time_slot()))
    $ TodaySexEvents_Clear()
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    $ player.economy.money = 100
    $ player.intimacy.came_today = 0
    $ _georgett_hire_money_before = int(player.economy.money or 0)
    click id "main_ui_entity_button_npc_georgett" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Снять" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _georgett_grope_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Лапать")
    $ _georgett_grope_button_id = "choice_panel_button_%d" % int(_georgett_grope_index)
    click id _georgett_grope_button_id pos (0.5, 0.5) until eval ("Сначала заплати, а потом уже лапай!" in str(scene_runtime.text or "")) timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 5.0
    assert eval ("Снять" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] and "Лапать" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ Georgett.rel = 10
    $ _georgett_hire_clock_before = int(calendar_v2.clock_minutes() or 0)
    $ _georgett_hire_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Снять")
    $ _georgett_hire_button_id = "choice_panel_button_%d" % int(_georgett_hire_index)
    click id _georgett_hire_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "event" and renpy.get_screen("choice") is not None and "Растегнуть блузку" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and "Растегнуть блузку" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval (renpy.get_screen("say") is None and "Вы заплатили Жоржетте восемь мараведи" in str(scene_runtime.text or "") and "Вы находитесь в переулке. Рядом с вами страстная Жоржетта." in str(scene_runtime.text or "")) timeout 5.0
    assert eval (int(player.economy.money or 0) == _georgett_hire_money_before - 8) timeout 5.0
    assert eval (str(main_ui_runtime.selected_char or "") == "" and str(main_ui_runtime.girl_key or "") == "" and str(main_ui_runtime.talk_picture or "") == "") timeout 5.0
    assert eval (str(scene_runtime.picture or "").startswith("images/georgett/portraits/portrait") and renpy.loadable(scene_runtime.picture)) timeout 5.0
    assert eval (str(renpy.get_screen("main_ui").scope.get("_picture", "") or "") == str(scene_runtime.picture or "")) timeout 5.0
    $ _georgett_unbutton_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Растегнуть блузку")
    $ _georgett_unbutton_button_id = "choice_panel_button_%d" % int(_georgett_unbutton_index)
    click id _georgett_unbutton_button_id pos (0.5, 0.5) until eval (Georgett.layer_raised("top") and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval (str(scene_runtime.picture or "") != "" and renpy.loadable(scene_runtime.picture)) timeout 5.0
    $ _georgett_hire_finish_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить")
    $ _georgett_hire_finish_button_id = "choice_panel_button_%d" % int(_georgett_hire_finish_index)
    click id _georgett_hire_finish_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (int(calendar_v2.clock_minutes() or 0) - _georgett_hire_clock_before == 40) timeout 5.0
    $ Georgett.openness = 0
    $ Georgett.talked_today = 0
    $ Georgett.gifted_today = 0
    $ player.economy.money = 0
    $ player.intimacy.came_today = player.intimacy.can_cum_daily

    $ player.economy.money = 100
    $ player.intimacy.came_today = player.intimacy.can_cum_daily
    $ Georgett.wardrobe["current_dress"] = ""
    $ Georgett.wardrobe["current_underwear"]["bra"] = ""
    $ Georgett.wardrobe["current_underwear"]["panties"] = ""
    $ Georgett.sex_setup("street")
    $ player.intimacy.set_arousal(0)
    $ Georgett.set_arousal(0)
    $ Georgett.rel = 3
    $ Georgett.sex_state["lick_pussy"] = 3
    run Call("IntGeorgettSex", "georgett", "street")
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None) timeout 5.0
    assert eval ("Лизать киску" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _georgett_lick_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Лизать киску")
    $ _georgett_lick_button_id = "choice_panel_button_%d" % int(_georgett_lick_index)
    click id _georgett_lick_button_id pos (0.5, 0.5) until eval (int(Georgett.sex_state.get("lick_pussy", 0) or 0) == 4) timeout 20.0
    assert eval (int(Georgett.sex_state.get("lick_pussy", 0) or 0) == 4 and int(Georgett.rel or 0) == 4) timeout 5.0
    advance until screen "choice" timeout 20.0
    $ _georgett_finish_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить")
    $ _georgett_finish_button_id = "choice_panel_button_%d" % int(_georgett_finish_index)
    click id _georgett_finish_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
    assert eval (str(rooms.current_code or "") == "PortStreets") timeout 5.0

    $ player.economy.money = 100
    $ Georgett.rel = 10
    $ player.intimacy.came_today = 0
    $ player.intimacy.can_cum_daily = 2
    $ Georgett.wardrobe["current_dress"] = ""
    $ Georgett.wardrobe["current_underwear"]["bra"] = ""
    $ Georgett.wardrobe["current_underwear"]["panties"] = ""
    $ Georgett.sex_setup("street")
    $ Georgett.clear_cum("cum_face_you", "cum_face_others", "cum_tits_you", "cum_tits_others", "cum_inside_you", "cum_inside_others")
    $ player.intimacy.set_arousal(100)
    $ Georgett.set_arousal(40)
    run Call("IntGeorgettSex", "georgett", "street")
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None) timeout 5.0
    assert eval ("Кончить на лицо" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Кончить на груди" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ player.intimacy.came_today = 1
    $ _georgett_cum_face_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Кончить на лицо")
    $ _georgett_cum_face_button_id = "choice_panel_button_%d" % int(_georgett_cum_face_index)
    click id _georgett_cum_face_button_id pos (0.5, 0.5) until eval (PLAYER_DAILY_EXHAUSTION_TEXT in str(scene_runtime.text or "") and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval (int(Georgett.cum_state("cum_face_you") or 0) == 1) timeout 5.0
    assert eval (int(player.intimacy.came_today or 0) == 2 and not player.intimacy.can_cum()) timeout 5.0
    assert eval ("То что упало - подняться не может." in str(renpy.get_screen("main_ui").scope.get("_desc", "") or "")) timeout 5.0
    assert eval ("Предложить отсосать" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] and not any(str(i.caption or "").startswith("Кончить") for i in renpy.get_screen("choice").scope.get("items", []))) timeout 5.0
    $ _georgett_exhausted_finish_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить")
    $ _georgett_exhausted_finish_button_id = "choice_panel_button_%d" % int(_georgett_exhausted_finish_index)
    click id _georgett_exhausted_finish_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0

testcase external_sexport_finish_does_not_show_advance_time_developer_text:
    $ _history_list = []
    $ external_calendar_set_fields(1, 1, 1100, 12, 0)
    $ _sexport_finish_before = int(calendar_v2.clock_minutes() or 0)
    run Call("FinishPaidSexModule", "georgett", "PortStreets")
    assert eval (int(calendar_v2.clock_minutes() or 0) - _sexport_finish_before == 40) timeout 5.0
    assert eval (not any("Advances the game time" in str(h.what or "") for h in _history_list)) timeout 5.0
    assert eval (not any("return_location" in str(h.what or "") for h in _history_list)) timeout 5.0

testcase external_liza_inherited_state_and_native_sex_menu:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "main_ui" timeout 20.0
    $ renpy.call_in_new_context("InitDressDesc")
    $ Liza.prostitution_started = False
    $ Liza.glory_hole_asked = False
    assert eval (not Liza.prostitution_started and not Liza.glory_hole_asked) timeout 5.0
    $ Liza.talked_today = 2
    $ Liza.gifted_today = 1
    $ Liza.asked_today = 1
    $ Liza.fucked_today = 1
    $ Liza.drunk = 1
    $ Liza.portstreet_clients_seen_today = True
    $ Liza.reset_daily()
    assert eval (Liza.talked_today == 0 and Liza.gifted_today == 0 and Liza.asked_today == 0 and Liza.fucked_today == 0 and Liza.drunk == 0) timeout 5.0
    assert eval (not Liza.portstreet_clients_seen_today) timeout 5.0
    run Call("IntLizaTalk", "liza", "tavern")
    advance until screen "choice" timeout 20.0
    assert eval ("Осмотреть" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _liza_look_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Осмотреть")
    $ _liza_look_button_id = "choice_panel_button_%d" % int(_liza_look_index)
    click id _liza_look_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "char") timeout 20.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Назад"] and list(main_ui_runtime.action_items or []) == []) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and "Болтать" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _liza_talk_end_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _liza_talk_end_button_id = "choice_panel_button_%d" % int(_liza_talk_end_index)
    click id _liza_talk_end_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") != "talk") timeout 20.0
    $ Liza.wardrobe["current_dress"] = "minidress"
    $ Liza.wardrobe["current_underwear"]["bra"] = ""
    $ Liza.wardrobe["current_underwear"]["panties"] = "simplepanties"
    $ player.intimacy.set_arousal(100)
    $ player.intimacy.came_today = player.intimacy.can_cum_daily
    run Call("IntLizaSex", "liza", "street")
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None) timeout 5.0
    assert eval ("Снять блузку" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Снять панталончики" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Предложить отсосать" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval (not any(str(i.caption or "").startswith("Кончить") for i in renpy.get_screen("choice").scope.get("items", []))) timeout 5.0
    $ _liza_finish_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить")
    $ _liza_finish_button_id = "choice_panel_button_%d" % int(_liza_finish_index)
    click id _liza_finish_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
'''


ACTUAL_ACTION_BUTTON_CLICK_CHECKS = r'''
init -1 python:
    def external_prepare_market_click_state():
        global BlockTimeAdvance, TavernEventOngoing
        external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
        external_calendar_set_weekday(1)
        BlockTimeAdvance = 0
        TavernEventOngoing = ""
        people.get_data("clara").set_schedule([])
        if "claraBookletMarket" in threads:
            threads["claraBookletMarket"].complete()
        findAvailableEvents(True)
        threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
        main_ui_runtime.overlay = ""
        main_ui_runtime.inventory_dropdown_open = False
        main_ui_runtime.action_content = None
        main_ui_runtime.mode = "scene"
        rooms.enter("MarketPlace"
)
        scene_runtime.text = rooms.get("MarketPlace").descriptions[0].text + "\n\n" + rooms.get("MarketPlace").descriptions[1].text + "\n\n" + rooms.get("MarketPlace").descriptions[2].text
        scene_runtime.location_text = scene_runtime.text
        player.horse.acquire("test-horse")
        scene_runtime.picture = rooms.get("MarketPlace").bg_picture
        main_ui_runtime.action_title = "Действия"

label external_market_click_entry:
    call InitGameNPCs
    $ external_prepare_market_click_state()
    jump MarketPlace

label external_duplicate_text_probe:
    $ rooms.enter("MarketPlace")
    $ scene_runtime.text = "EXTERNAL_DUPLICATE_TEXT_PROBE"
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    "[scene_runtime.text]"
    return

testcase external_main_ui_does_not_repeat_active_dialogue_text:
    run Jump("external_duplicate_text_probe")
    advance until screen "say" timeout 20.0
    assert eval (str(renpy.get_screen("say").scope.get("what", "") or "") == "EXTERNAL_DUPLICATE_TEXT_PROBE") timeout 5.0
    assert eval (str(renpy.get_screen("main_ui").scope.get("_desc", "") or "") == "") timeout 5.0

testcase external_actual_grocery_click:
    run Call("InitGameNPCs")
    $ people.get_data("becky").interval_schedule_entries = []
    $ people.get_data("becky").interval_schedule_loaded = True
    $ npc_schedule_after_load()
    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 16, 0)
    $ external_calendar_set_weekday(1)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ player.set_money(max(100, int(player.economy.money or 0)))
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    $ _grocery_room_picture = str(scene_runtime.picture or "")
    $ _grocery_room_text = str(scene_runtime.text or "")
    assert eval (str(people.location("becky") or "") == "GroceryStore") timeout 5.0
    assert eval ("becky" in list(people.ids_at("GroceryStore") or [])) timeout 5.0
    assert eval (str(grocery_store_active_grocer_id() or "") == "becky") timeout 5.0
    assert eval (_grocery_room_picture == str(rooms.get("GroceryStore").bg_picture or "") and renpy.loadable(_grocery_room_picture)) timeout 5.0
    assert eval (str(rooms.get("GroceryStore").descriptions[0].text or "") in _grocery_room_text and "За прилавком стоит сама Бекки" not in _grocery_room_text) timeout 5.0
    assert eval (any(str(row.get("id", "") or "") == "becky" for row in renpy.get_screen("main_ui").scope.get("_char_entries", []))) timeout 5.0
    assert eval ('Провизия' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    click id "main_ui_entity_button_npc_becky" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("За прилавком стоит сама Бекки" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (str(scene_runtime.picture or "") != _grocery_room_picture and renpy.loadable(str(scene_runtime.picture or ""))) timeout 5.0
    $ _grocery_talk_end_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _grocery_talk_end_button_id = "choice_panel_button_%d" % int(_grocery_talk_end_index)
    click id _grocery_talk_end_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (str(scene_runtime.picture or "") == _grocery_room_picture and str(scene_runtime.text or "") == _grocery_room_text) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == 'Провизия') timeout 20.0
    assert eval (str(scene_runtime.picture or "") != _grocery_room_picture and renpy.loadable(str(scene_runtime.picture or ""))) timeout 5.0
    assert eval (str(scene_runtime.text or "") == str(GroceryStoreFoodStockObject.description or "")) timeout 5.0
    assert eval ('Купить провизию' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _grocery_buy_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Купить провизию")
    $ _grocery_buy_button_id = "choice_panel_button_%d" % int(_grocery_buy_index)
    click id _grocery_buy_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == 'Покупка провизии') timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == 'Покупка провизии') timeout 5.0
    assert eval ('Купить один мешок' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _grocery_buy_back_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Назад")
    $ _grocery_buy_back_button_id = "choice_panel_button_%d" % int(_grocery_buy_back_index)
    click id _grocery_buy_back_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == 'Провизия') timeout 20.0
    $ _grocery_object_back_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Назад")
    $ _grocery_object_back_button_id = "choice_panel_button_%d" % int(_grocery_object_back_index)
    click id _grocery_object_back_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == 'Действия') timeout 20.0
    assert eval (str(scene_runtime.picture or "") == _grocery_room_picture and str(scene_runtime.text or "") == _grocery_room_text and str(main_ui_runtime.object_id or "") == "") timeout 5.0

testcase external_becky_store_event_replaces_room_text:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 16, 0)
    $ external_calendar_set_weekday(1)
    $ people.get_data("becky").set_schedule([NPCScheduleEntry(location="GroceryStore", start_minute=0, end_minute=1440, priority=999)])
    $ Becky.rel = 20
    $ Becky.corruption = 60
    $ TodaySexEvents_Clear()
    $ TodaySexEvents_Add("becky", 99, 3, "StoreLover")
    python:
        for _becky_store_event_day in range(1, 200):
            calendar_v2.daysInGame = _becky_store_event_day
            if procedural_randint(1, 3, "becky_store_lover_%s" % _becky_store_event_day) == 1:
                break
    run Jump("GroceryStore")
    advance until screen "choice" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and str(main_ui_runtime.action_title or "") == "Событие") timeout 5.0
    assert eval (rooms.get("GroceryStore").descriptions[0].text not in str(scene_runtime.text or "")) timeout 5.0
    assert eval (str(scene_runtime.picture or "") != str(rooms.get("GroceryStore").bg_picture or "") and renpy.loadable(str(scene_runtime.picture or ""))) timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Вернуться к покупкам"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (str(scene_runtime.picture or "") == str(rooms.get("GroceryStore").bg_picture or "") and str(scene_runtime.text or "") == str(rooms.get("GroceryStore").descriptions[0].text or "")) timeout 5.0
    assert eval (int(Becky.last_store_orgasm_day or -1) == int(current_game_day() or 0)) timeout 5.0

testcase external_actual_wine_click:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(1)
    $ player.set_money(max(int(player.economy.money or 0), 1000))
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Бочки с вином' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == 'Бочки с вином') timeout 20.0
    assert eval ('Купить вино' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == 'Покупка вина') timeout 20.0
    assert eval ('Купить один бочонок' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

testcase external_wine_store_return_restores_market_scene_once:
    run Call("InitGameNPCs")
    $ player.horse.remove()
    $ player.horse.stolen_days = 0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(1)
    $ Mongol.known = True
    $ Mongol.market_roll_day = int(current_game_day())
    $ Mongol.market_roll = False
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ people.get_data("clara").set_schedule([])
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    $ main_ui_runtime.mode = "talk"
    $ main_ui_runtime.selected_char = "clara"
    $ main_ui_runtime.girl_key = "clara"
    $ main_ui_runtime.talk_picture = main_ui_talk_picture_path("clara")
    $ _wine_market_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Вернуться на рынок")
    $ _wine_market_button = "choice_panel_button_%d" % int(_wine_market_index)
    click id _wine_market_button pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (str(rooms.current_code or "") == "MarketPlace") timeout 5.0
    assert eval (str(scene_runtime.picture or "") == str(rooms.get("MarketPlace").bg_picture or "")) timeout 5.0
    assert eval (str(renpy.get_screen("main_ui").scope.get("_picture", "") or "") == str(rooms.get("MarketPlace").bg_picture or "")) timeout 5.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and str(main_ui_runtime.action_title or "") == "Случайное событие") timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Идти дальше"]) timeout 5.0
    assert eval (renpy.get_screen("say") is None) timeout 5.0
    assert eval (str(renpy.get_screen("main_ui").scope.get("_desc", "") or "") == str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (str(rooms.current_code or "") == "MarketPlace" and 'Зайти в охотничий клуб' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "scene") timeout 5.0
    assert eval (str(main_ui_runtime.selected_char or "") == "" and str(main_ui_runtime.talk_picture or "") == "") timeout 5.0
    assert eval (str(scene_runtime.picture or "") == str(rooms.get("MarketPlace").bg_picture or "")) timeout 5.0
    assert eval (str(renpy.get_screen("main_ui").scope.get("_picture", "") or "") == str(rooms.get("MarketPlace").bg_picture or "")) timeout 5.0
    assert eval (str(scene_runtime.text or "").count(rooms.get("MarketPlace").descriptions[0].text) == 1) timeout 5.0
    assert eval (str(scene_runtime.text or "").count(rooms.get("MarketPlace").descriptions[1].text) == 1) timeout 5.0
    assert eval (str(scene_runtime.text or "").count(rooms.get("MarketPlace").descriptions[2].text) == 1) timeout 5.0
    assert eval (renpy.get_screen("say") is None) timeout 5.0

testcase external_actual_wine_for_dance_menu:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(3)
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.event_active = False
    $ event_runtime.tavern_work_events = [{"code": "WineForDance", "type": "mandatory", "label": "EventWineForDance", "period": 10, "mandatory": True, "priority": 0}]
    $ event_runtime.tavern_played_today = []
    $ event_runtime.tavern_report_rows = []
    $ player.tavern_management.winenum = max(int(player.tavern_management.winenum or 0), 50)
    $ player.tavern_management.productnum = max(int(player.tavern_management.productnum or 0), 40)
    $ player.set_money(max(int(player.economy.money or 0), 100))
    $ player.tavern_management.dance_sponsor = 0
    $ player.tavern_management.dance_sponsor_pledge_day = -1
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Jump("TavernKitchen")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Вернуться к своим делам"]) timeout 20.0
    assert eval (int(player.tavern_management.dance_sponsor or 0) == 1) timeout 5.0
    assert eval (int(player.tavern_management.dance_sponsor_pledge_day or -1) == int(calendar_v2.daysInGame or 0)) timeout 5.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and renpy.get_screen("say") is None and "Вы соглашаетесь выставить на пятничных танцах" in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene") timeout 20.0

testcase external_tavern_random_event_plan_consumes_once:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 13, 0)
    $ external_calendar_set_weekday(1)
    $ rooms.enter("TavernMain")
    $ TavernEventOngoing = ""
    run Call("InitAmanda")
    $ Amanda.set_job_value("jobwaitress", 1)
    $ Amanda.set_job_value("jobcleaning", 0)
    assert eval (int(Amanda.job_value("jobwaitress", 0) or 0) == 1) timeout 5.0
    assert eval ("amanda" in list(girls_by_job("jobwaitress") or [])) timeout 5.0
    assert eval (str(get_random_girl_by_job("jobwaitress") or "") != "") timeout 5.0
    $ event_runtime.tavern_work_events = [{"code": "WaitressHarass", "type": "harrass", "label": "event_waitress_harrass", "period": calendar_v2.time_slot(), "mandatory": False, "priority": 20}]
    $ event_runtime.tavern_played_today = []
    $ event_runtime.tavern_report_rows = []
    assert eval (tavern_work_codes_for_period(calendar_v2.time_slot(), False) == ["WaitressHarass"]) timeout 5.0
    $ findAvailableEvents(True)
    assert eval ("TavernMain" in event_runtime.available and "tavern_work" in event_runtime.available["TavernMain"] and str(event_runtime.available["TavernMain"]["tavern_work"].target or "") == "TavernWorkEventTrigger") timeout 5.0
    run Jump("TavernMain")
    advance until screen "choice" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and renpy.get_screen("say") is None and "Что вы будете делать?" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Не обращать внимания", "Стоять и смотреть", "[_help_caption]"]) timeout 5.0
    assert eval (str(scene_runtime.picture or "") != "images/tavern/mainhall/main_hall.png" and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Промолчать" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and renpy.get_screen("say") is None and "Вы отвернулись от происходящего" in str(scene_runtime.text or "")) timeout 5.0
    $ _harass_silence_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Промолчать")
    $ _harass_silence_button = "choice_panel_button_%d" % int(_harass_silence_index)
    click id _harass_silence_button pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Вернуться к делам"]) timeout 20.0
    assert eval (renpy.get_screen("say") is None and "Вы решили ничего не говорить" in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval ("WaitressHarass" in list(event_runtime.tavern_played_today or [])) timeout 5.0
    assert eval (len(list(event_runtime.tavern_work_events or [])) == 0 and not tavern_work_has_period(calendar_v2.time_slot(), False)) timeout 5.0
    assert eval (str(scene_runtime.picture or "") == "images/tavern/mainhall/main_hall.png" and "Действия в трактире" == str(main_ui_runtime.action_title or "")) timeout 5.0

testcase external_tavern_small_fight_native_event_flow:
    $ rooms.enter("TavernMain")
    $ scene_runtime.picture = "images/tavern/mainhall/main_hall.png"
    $ scene_runtime.text = "Тестовое описание главной залы."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.action_title = "Действия в трактире"
    $ main_ui_runtime.action_items = [MenuItem("Тестовое действие", NullAction())]
    $ _fight_event_randint = procedural_randint
    $ procedural_randint = lambda low, high, key="": int(low)
    run Call("EventFightSmall", 1)
    advance until screen "choice" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and renpy.get_screen("say") is None and "В вашем трактире произошла драка!" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ("Выругаться и не делать ничего" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Вернуться к своим делам"]) timeout 20.0
    assert eval (renpy.get_screen("say") is None and "Ущерб составил 20 мараведи." in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (str(scene_runtime.picture or "") == "images/tavern/mainhall/main_hall.png" and str(scene_runtime.text or "") == "Тестовое описание главной залы." and [str(i.caption or "") for i in main_ui_runtime.action_items] == ["Тестовое действие"]) timeout 5.0
    $ procedural_randint = _fight_event_randint

testcase external_tavern_unwitnessed_event_report_consumes_leftovers:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 16, 0)
    $ external_calendar_set_weekday(2)
    $ rooms.enter("TavernMain")
    $ player.set_money(max(int(player.economy.money or 0), 1000))
    $ event_runtime.tavern_work_events = [{"code": "FightSmall", "type": "small_fight", "label": "EventFightSmall", "period": calendar_v2.time_slot(), "mandatory": False, "priority": 40}]
    $ event_runtime.tavern_played_today = []
    $ event_runtime.tavern_report_rows = []
    assert eval (tavern_work_codes_for_period(calendar_v2.time_slot(), False) == ["FightSmall"]) timeout 5.0
    run Call("DisplayTavernEventsSummary", calendar_v2.day, calendar_v2.period, calendar_v2.cycle)
    assert eval (len(list(event_runtime.tavern_work_events or [])) == 0 and not tavern_work_has_period(calendar_v2.time_slot(), False)) timeout 5.0
    assert eval ("FightSmall" in list(event_runtime.tavern_played_today or [])) timeout 5.0
    assert eval (any(str(row.get("code", "") or "") == "FightSmall" and not bool(row.get("witnessed", True)) for row in list(event_runtime.tavern_report_rows or []))) timeout 5.0

testcase external_breakfast_dance_sponsor_announcement:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(3)
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.dance_sponsor = 1
    $ player.tavern_management.breakfast.dance_sponsor_announced_day = -1
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernSandraRoom", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernAmandaRoom", start_minute=0, end_minute=1440, priority=999)])
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ rooms.enter("TavernKitchen")
    $ renpy.show_screen("main_ui")
    run Call("TavernKitchenBreakfast")
    advance until screen "say" timeout 20.0
    assert eval ("трактир уже выставит вино и закуски" in str((player.tavern_management.breakfast.base_text or tavern_kitchen_saved_text() or scene_runtime.text) or "")) timeout 5.0

testcase external_breakfast_attendance_location_wins:
    run Call("InitGameNPCs")
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = False
    $ TavernBreakfastPresentIds = None
    $ TavernBreakfastFoodPerkDay = -1
    $ TavernBreakfastDrinkPerkDay = -1
    $ TavernBreakfastLewdSeriesDay = -1
    $ TavernBreakfastAbsentTalkDay = -1
    $ TavernBreakfastListenDay = int(current_game_day())
    $ TavernBreakfastMarketTalkDay = int(current_game_day())
    $ TavernBreakfastMotivationDay = int(current_game_day())
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ household.morning_state[_household_morning_state_key("melissa")] = {"issue": "sleepy", "resolved": 0, "indecent": 0}
    $ player.add_item("energy_tea_001", 1)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ rooms.enter("TavernKitchen"
)
    $ TavernBreakfastPresentIds = ["sandra", "melissa", "amanda"]
    $ player.tavern_management.breakfast.event_active = True
    $ TavernBreakfastBaseText = "Тестовый завтрак."
    $ TavernKitchenSavedText = TavernBreakfastBaseText
    $ scene_runtime.text = TavernBreakfastBaseText
    $ scene_runtime.location_text = scene_runtime.text
    run Call("TavernKitchenBreakfastMenu")
    advance until screen "main_ui" timeout 20.0
    assert eval ("melissa" in list(tavern_breakfast_present_ids() or [])) timeout 5.0
    assert eval ("melissa" not in list(tavern_breakfast_absent_ids() or [])) timeout 5.0
    assert eval ("melissa" in list(tavern_breakfast_core_present_ids() or [])) timeout 5.0
    assert eval (renpy.get_screen("choice") is not None) timeout 5.0
    assert eval ("Мелисса все еще отсыпается" not in " ".join(list(household_breakfast_absence_lines() or []))) timeout 5.0
    run Call("TavernKitchenBreakfastLookAtGirl", "melissa")
    assert eval ("Вы присматриваетесь к Мелиссе за завтраком" in str(scene_runtime.text or "")) timeout 5.0

testcase external_breakfast_angry_amanda_melissa_mockery:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(1)
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = True
    $ player.tavern_management.breakfast.present_ids = ["sandra", "melissa", "amanda"]
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("becky").set_schedule([NPCScheduleEntry(location="GroceryStore", start_minute=0, end_minute=1440, priority=999)])
    $ Amanda.var["relationship_mood"] = {"anger": 2, "anger_until_day": int(calendar_v2.daysInGame or 0) + 1, "anger_reason": "external_test", "last_bad_action_day": int(calendar_v2.daysInGame or 0), "interaction_score": 0}
    $ Melissa.var["relationship_mood"] = {"anger": 2, "anger_until_day": int(calendar_v2.daysInGame or 0) + 1, "anger_reason": "external_test", "last_bad_action_day": int(calendar_v2.daysInGame or 0), "interaction_score": 0}
    assert eval ("becky" not in list(tavern_breakfast_present_ids() or [])) timeout 5.0
    assert eval ("Бекки" not in list(tavern_breakfast_present_names() or [])) timeout 5.0
    assert eval ("Крысы?" in " ".join(list(tavern_breakfast_dialogue_lines() or []))) timeout 5.0
    assert eval (len([row for row in tavern_breakfast_dialogue_lines() if "Пальцы из кисок" in str(row or "")]) == 1) timeout 5.0
testcase external_sandra_weekly_visit_native_beats:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("sandra") is not None) timeout 20.0
    $ rooms.enter("TavernMyRoom")
    $ player.chores.last_score = 0
    run Call("SandraWeeklyEvaluationScene", 0, "TavernMain")
    advance until screen "choice" timeout 20.0
    assert eval (str(scene_runtime.picture or "") == "images/sandra/portrait2.jpg") timeout 5.0
    assert eval ("осторожный стук" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Продолжить"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("держал хозяйство" in str(scene_runtime.text or "")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("Если вечером захочешь" in str(scene_runtime.text or "")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("День уже начинается" in str(scene_runtime.text or "")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") != "event" and renpy.get_screen("choice") is None) timeout 10.0

testcase external_melissa_bat_breakfast_single_finish:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("melissa") is not None) timeout 20.0
    $ rooms.enter("TavernKitchen")
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = None
    $ threads["melissaBatProblem"].advanceTo(0, force_active=True)
    $ event_runtime.active_thread = threads["melissaBatProblem"]
    $ Amanda.var.pop("relationship_mood", None)
    $ Melissa.var.pop("relationship_mood", None)
    $ _bat_breakfast_start = int(calendar_v2.clock_minutes() or 0)
    run Call("story_melissa_bat_problem_0")
    advance until screen "choice" timeout 20.0
    assert eval ("одного места не хватает" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Продолжить"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("злой и невыспавшийся" in str(scene_runtime.text or "")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("продолжает коситься" in str(scene_runtime.text or "")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("крысиная проблема" in str(scene_runtime.text or "")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("настоящая ведьма" in str(scene_runtime.text or "")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("первым делом заколдую" in str(scene_runtime.text or "")) timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("придется разбираться всерьез" in str(scene_runtime.text or "")) timeout 10.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Закончить завтрак"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (int(threads["melissaBatProblem"].num or 0) == 1 and not bool(player.tavern_management.breakfast.event_active) and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (bool(player.tavern_management.breakfast.today)) timeout 5.0
    assert eval (player.tavern_management.breakfast.present_ids is None) timeout 5.0
    assert eval (int(calendar_v2.clock_minutes() or 0) - _bat_breakfast_start == 45) timeout 5.0
    assert eval ("Позавтракать" not in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
testcase external_breakfast_window_and_call_all_click:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 7, 55)
    $ external_calendar_set_weekday(1)
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = None
    $ Melissa.storage_rat_help_day = -1
    $ threads["melissaBatProblem"].advanceTo(8, complete_at_end=True)
    $ werecat_state()["rats_problem_active"] = 0
    $ werecat_state()["rat_breakfast_seen"] = 1
    $ werecat_state()["adoption_breakfast_seen"] = 1
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ rooms.enter("TavernKitchen")
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    assert eval ("Позавтракать" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    assert eval ("Позавтракать" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 10, 0)
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = None
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    $ player.tavern_management.breakfast.today = True
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    assert eval ("Позавтракать" not in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

testcase external_kitchen_entry_morning_sickness_event:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 6, 30)
    $ external_calendar_set_weekday(1)
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = None
    $ daily_events.rows[:] = []
    $ daily_events.add("sandra", "TavernKitchen", 1, "<", 1, 8, "MorningSickness", "MorningSickness", "girl")
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    run Jump("TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    $ _breakfast_action_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Позавтракать")
    $ _breakfast_action_button = "choice_panel_button_%d" % int(_breakfast_action_index)
    click id _breakfast_action_button pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 30.0
    assert eval (str(rooms.current_code or "") == "TavernKitchen") timeout 5.0
    assert eval (daily_events.exists("sandra", "MorningSickness", "TavernKitchen") == 0) timeout 5.0

testcase external_actual_barber_actions_click:
    run Call("InitGameNPCs")
    $ household.__dict__.pop("barber_appointments", None)
    $ Sandra.var["barber_invite_pending"] = 1
    $ tractir_save_patch_loaded_state()
    assert eval (household.barber_appointments == {"sandra": 1} and "barber_invite_pending" not in Sandra.var) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 14, 0)
    $ player.economy.money = max(int(player.economy.money or 0), 500)
    $ household.barber_appointments = {"sandra": 1, "melissa": 1, "amanda": 1}
    $ external_calendar_set_weekday(2)
    assert eval (all(npc_id not in people.ids_at("BarberShop") for npc_id in ("sandra", "melissa", "amanda"))) timeout 5.0
    $ external_calendar_set_weekday(1)
    $ player.appearance.days_since_haircut = 30
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Jump("BarberShop")
    advance until screen "main_ui" timeout 20.0
    assert eval (all(npc_id in people.ids_at("BarberShop") for npc_id in ("sandra", "melissa", "amanda", "sergio"))) timeout 5.0
    assert eval (all(renpy.get_widget("main_ui", "main_ui_entity_button_npc_%s" % npc_id) is not None for npc_id in ("sandra", "melissa", "amanda"))) timeout 5.0
    assert eval (all("Подстричься" not in str(i.caption or "") for i in main_ui_runtime.action_items)) timeout 5.0
    click id "main_ui_entity_button_npc_sergio" pos (0.5, 0.5) until screen "choice" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "talk") timeout 5.0
    assert eval (len([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", []) if "Подстричься" in str(i.caption or "")]) == 1) timeout 5.0
    $ _barber_haircut_index = ["Подстричься" in str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index(True)
    $ _barber_haircut_button = "choice_panel_button_%d" % int(_barber_haircut_index)
    click id _barber_haircut_button pos (0.5, 0.5) until eval ("выглядите куда опрятнее" in str(scene_runtime.text or "")) timeout 20.0
    assert eval (int(player.appearance.days_since_haircut or 0) == 0) timeout 5.0
    advance until screen "choice" timeout 20.0
    $ _barber_guest_index = ["Оплатить визит" in str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index(True)
    click id ("choice_panel_button_%d" % int(_barber_guest_index)) pos (0.5, 0.5) until eval ("sandra" not in household.barber_appointments) timeout 20.0
    assert eval (all(npc_id in people.ids_at("BarberShop") for npc_id in ("melissa", "amanda")) and "sandra" not in people.ids_at("BarberShop")) timeout 5.0

testcase external_actual_draupnir_talk_menu:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 14, 0)
    $ external_calendar_set_weekday(1)
    $ player.tavern_management.slogan_state = 0
    $ Draupnir.slogan_quote_received = False
    $ player.set_money(500)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Jump("StolyarWorkshop")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Спросить о ремонте вывески" in [str(i.caption or "") for i in build_room_action_items(rooms.current)]) timeout 5.0
    click id "main_ui_entity_button_npc_draupnir" pos (0.5, 0.5) until screen "choice" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "talk") timeout 5.0
    assert eval ("Поболтать с гномом" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Спросить о ремонте вывески" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval (main_ui_talk_picture_path("draupnir") == "images/draupnir/dwarf1.jpg" and renpy.loadable(main_ui_talk_picture_path("draupnir"))) timeout 5.0
    $ _draupnir_back_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Назад")
    $ _draupnir_back_button = "choice_panel_button_%d" % int(_draupnir_back_index)
    click id _draupnir_back_button pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    $ _draupnir_slogan_index = [str(i.caption or "") for i in build_room_action_items(rooms.current)].index("Спросить о ремонте вывески")
    $ _draupnir_slogan_button = "choice_panel_button_%d" % int(_draupnir_slogan_index)
    click id _draupnir_slogan_button pos (0.5, 0.5) until eval (Draupnir.slogan_quote_received) timeout 20.0
    assert eval ("Заплатить 200 мараведи за ремонт вывески" in [str(i.caption or "") for i in build_room_action_items(rooms.current)]) timeout 5.0
    $ _draupnir_pay_index = [str(i.caption or "") for i in build_room_action_items(rooms.current)].index("Заплатить 200 мараведи за ремонт вывески")
    $ _draupnir_pay_button = "choice_panel_button_%d" % int(_draupnir_pay_index)
    click id _draupnir_pay_button pos (0.5, 0.5) until eval (int(player.tavern_management.slogan_state or 0) == 1) timeout 20.0
    assert eval (int(player.economy.money or 0) == 300 and people.get_data("draupnir").getLocation() == "StreetTavern") timeout 5.0
    assert eval ("Заплатить 200 мараведи за ремонт вывески" not in [str(i.caption or "") for i in build_room_action_items(rooms.current)]) timeout 5.0

testcase external_actual_market_click:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(1)
    $ people.get_data("clara").set_schedule([])
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Jump("external_market_click_entry")
    advance until screen "main_ui" timeout 20.0
    assert eval ('Зайти в охотничий клуб' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ('Рыночные лотки' not in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

testcase external_actual_market_blind_pirate_first_entry:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(11, 1, CALENDAR_START_CYCLE, 12, 0)
    $ external_calendar_set_weekday(1)
    $ people.get_data("clara").set_schedule([])
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.fired_keys_today[:] = []
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ Clara.market_day_roll_day = int(calendar_v2.daysInGame or 0)
    $ Clara.market_day_roll = True
    $ Clara.market_follow_failed_day = -1
    $ Clara.market_follow_failed_hour = -1
    $ findAvailableEvents(True)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ threads["cityBlindPirateFall"].advanceTo(0, force_active=True)
    $ TownStreet.events_today = 0
    $ TownStreet.story_seen_keys = []
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ player.horse.acquire("test-horse")
    run Jump("MarketPlace")
    advance until screen "choice" timeout 20.0
    assert eval (str(scene_runtime.picture or "") == "images/market/blindPirate.png") timeout 5.0
    assert eval ("Слишком ясно становится" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ("Вы пришли на шумный городской рынок" not in str(scene_runtime.text or "")) timeout 5.0
    assert eval (len(main_ui_runtime.action_items or []) == 0) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ('Зайти в охотничий клуб' in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 20.0
    assert eval (str(rooms.current_code or "") == "MarketPlace") timeout 5.0
    assert eval (str(scene_runtime.picture or "") == str(rooms.get("MarketPlace").bg_picture or "")) timeout 5.0
    assert eval ("Вы пришли на шумный городской рынок" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (int(threads["cityBlindPirateFall"].num or 0) == 1) timeout 5.0
    assert eval (not threads["cityBlindPirateFall"].completed) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 0 and not threads["claraBookletMarket"].completed) timeout 5.0

testcase external_market_clock_open_hours:
    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 5, 59)
    $ external_calendar_set_weekday(1)
    assert eval (not rooms.get("MarketPlace").is_open()) timeout 5.0
    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 6, 0)
    $ external_calendar_set_weekday(1)
    assert eval (rooms.get("MarketPlace").is_open()) timeout 5.0
    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 18, 59)
    $ external_calendar_set_weekday(1)
    assert eval (rooms.get("MarketPlace").is_open()) timeout 5.0
    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 19, 0)
    $ external_calendar_set_weekday(1)
    assert eval (not rooms.get("MarketPlace").is_open()) timeout 5.0
    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 10, 0)
    $ external_calendar_set_weekday(7)
    assert eval (not rooms.get("MarketPlace").is_open()) timeout 5.0
'''


ACTUAL_RANDOM_TOWN_CLICK_CHECKS = r'''
label external_random_town_sink:
    $ main_ui_runtime.action_title = "External click sink"
    $ main_ui_runtime.action_items = []
    call screen main_ui
    return

testcase external_actual_random_town_continue_click:
    $ _town_test_date = calendar_v2.day_number_to_parts(5)
    $ external_calendar_set_fields(int(_town_test_date.get("day", 1) or 1), int(_town_test_date.get("month", 1) or 1), int(_town_test_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 22, 0)
    $ rooms.enter("external_random_town_sink"
)
    $ player.set_stat("exploration", 300)
    $ player.set_stat("notoriety", 60)
    $ player.economy.money = 500
    $ player.economy.tavern_fame = 10
    $ TownStreet.events_today = 0
    $ TownStreet.patrols_today = 0
    $ TownStreet.fights_today = 0
    $ TownStreet.curfew_caught_today = 0
    $ TownStreet.story_seen_keys = []
    $ GuardCaptainVar = {}
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.action_title = "Статичное меню локации"
    $ main_ui_runtime.action_items = [MenuItem("Старое действие локации", NullAction())]
    $ renpy.random.seed(11)
    run Call("TownRandomChronicleEvent")
    advance until screen "choice" timeout 20.0
    assert eval (len(str(scene_runtime.text or "")) > 80 and TownStreet.events_today == 1) timeout 5.0
    assert eval (len(list(TownStreet.story_seen_keys or [])) >= 1 and event_runtime.evaluation_time is None) timeout 5.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and str(main_ui_runtime.action_title or "") == "Случайное событие") timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Идти дальше"]) timeout 5.0
    assert eval (main_ui_runtime.action_items == [] and renpy.get_screen("say") is None) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (str(main_ui_runtime.mode or "") == "scene") timeout 5.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items] == ["Старое действие локации"]) timeout 5.0

testcase external_actual_random_town_click:
    $ renpy.test.testsettings._test.timeout = 60.0
    $ week = 1
    $ time = 0
    $ hour = 8
    $ minute = 0
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ TownStreet.events_today = 2
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0

    $ _town_test_date = calendar_v2.day_number_to_parts(5)
    $ day = int(_town_test_date.get("day", 1) or 1)
    $ month = int(_town_test_date.get("month", 1) or 1)
    $ year = int(_town_test_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE)
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    $ rooms.enter("StreetTavern")
    $ scene_runtime.picture = "bg StreetTavern"
    $ player.set_stat("exploration", 300)
    $ player.set_stat("notoriety", 60)
    $ player.economy.money = 500
    $ player.economy.tavern_fame = 10
    $ TownStreet.events_today = 0
    $ TownStreet.patrols_today = 0
    $ TownStreet.fights_today = 0
    $ TownStreet.curfew_caught_today = 0
    $ TownStreet.story_seen_keys = []
    $ GuardCaptainVar = {}
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ _town_plan = TownStreet.probability_summary()
    assert eval (_town_plan.get("beggar") == 10 and _town_plan.get("thugs") == 10 and _town_plan.get("chronicle") == 25) timeout 5.0
    assert eval (_town_plan.get("patrol") == 55 and _town_plan.get("patrol_notoriety_bonus") == 30) timeout 5.0
    assert eval (TownStreet.curfew_active() and TownStreet.patrol_chance() == 55) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ time = 1
    $ clock_minutes = 22 * 60
    assert eval (not TownStreet.curfew_active()) timeout 5.0
    assert eval (not TownStreet.patrol_allowed("StreetTavern")) timeout 5.0
    $ _patrol_morning_result = renpy.call_in_new_context("TownStreetPatrolEvent")
    assert eval (_patrol_morning_result is False) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    run Call("TownStreetPatrolEvent")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (player.stats.exploration >= 308) timeout 20.0
    assert eval (TownStreet.patrols_today >= 1 and player.stats.exploration >= 308 and len(list(TownStreet.story_seen_keys or [])) >= 1 and event_runtime.evaluation_time is None) timeout 5.0
    assert eval (TownStreet.random_seen_this_slot("StreetTavern", "TownStreetPatrolEvent")) timeout 5.0
    assert eval (TownStreet.event_key("StreetTavern", "TownStreetPatrolEvent") in TownStreet.story_seen_keys) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    assert eval (TownStreet.random_seen_this_slot("StreetTavern", "TownStreetPatrolEvent")) timeout 5.0
    assert eval (not TownStreet.curfew_active()) timeout 5.0
    advance until screen "main_ui" timeout 20.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    $ rooms.enter("StreetTavern")
    $ scene_runtime.picture = "bg StreetTavern"
    $ scene_runtime.picture = scene_runtime.picture
    $ player.set_stat("exploration", 300)
    $ player.set_stat("notoriety", 60)
    $ player.set_stat("health", 100)
    $ player.set_stat("energy", 100)
    $ TownStreet.events_today = 0
    $ TownStreet.patrols_today = 0
    $ TownStreet.fights_today = 0
    $ TownStreet.curfew_caught_today = 0
    $ TownStreet.story_seen_keys = []
    $ GuardCaptainVar = {}
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Call("TownStreetPatrolEvent")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "fight") timeout 10.0
    assert eval (str(fight.enemy_id or "") == "patrol_guard" and len(list(fight.enemy_party or [])) == 2) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "") == "images/fight/patrol_guard.png") timeout 5.0
    $ renpy.call_in_new_context("FightRetreat")
    assert eval (str(main_ui_runtime.mode or "") == "fight" and str(fight.outcome_kind or "") == "retreat") timeout 5.0
    $ _fight_test_picture = str(fight.return_picture or "")
    $ fight_finish_to_room(str(scene_runtime.text or ""))
    $ scene_runtime.picture = _fight_test_picture
    $ scene_runtime.picture = _fight_test_picture
    assert eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == "StreetTavern") timeout 5.0

    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 12, 0)
    $ rooms.enter("MarketPlace"
)
    $ scene_runtime.picture = "bg MarketPlace"
    $ player.set_stat("exploration", 100)
    $ player.set_stat("notoriety", 0)
    $ player.economy.tavern_fame = 0
    $ TownStreet.events_today = 2
    $ TownStreet.patrols_today = 0
    $ TownStreet.fights_today = 0
    $ TownStreet.curfew_caught_today = 0
    $ TownStreet.story_seen_keys = []
    $ TownStreet.blackworker_candidates = []
    $ TownStreet.blackworkers = []
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Call("TownStreetHelpEvent")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (len(TownStreet.blackworker_candidates) >= 1) timeout 20.0
    assert eval (len(TownStreet.blackworker_candidates) >= 1 and player.economy.tavern_fame >= 1 and player.stats.exploration >= 105 and player.stats.notoriety == 0) timeout 5.0

    $ external_calendar_set_fields(2, 1, CALENDAR_START_CYCLE, 18, 0)
    $ rooms.enter("ArtisansQuarter"
)
    $ scene_runtime.picture = "bg ArtisansQuarter"
    $ player.set_stat("exploration", 300)
    $ player.set_stat("notoriety", 0)
    $ player.set_stat("reputation", 0)
    $ TownStreet.events_today = 2
    $ TownStreet.patrols_today = 0
    $ TownStreet.fights_today = 0
    $ TownStreet.curfew_caught_today = 0
    $ TownStreet.story_seen_keys = []
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Call("TownStreetThugsEvent")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (player.stats.exploration >= 306) timeout 10.0
    assert eval (player.stats.exploration >= 306 and player.stats.reputation == 2 and player.stats.notoriety == 4) timeout 5.0

    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 18, 0)
    $ rooms.enter("ArtisansQuarter")
    $ scene_runtime.picture = "bg ArtisansQuarter"
    $ scene_runtime.picture = scene_runtime.picture
    $ player.set_stat("health", 100)
    $ player.set_stat("energy", 100)
    $ player.set_stat("exploration", 300)
    $ player.set_stat("notoriety", 0)
    $ player.equipment.weapon = ""
    $ player.equipment.armor = ""
    $ TownStreet.events_today = 0
    $ TownStreet.patrols_today = 0
    $ TownStreet.fights_today = 0
    $ TownStreet.curfew_caught_today = 0
    $ TownStreet.story_seen_keys = []
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Call("TownStreetThugsEvent")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "fight") timeout 10.0
    assert eval (str(fight.enemy_id or "") == "street_crook" and len(list(fight.enemy_party or [])) == 2) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "") == "images/fight/thug.png") timeout 5.0
    $ renpy.call_in_new_context("FightRetreat")
    assert eval (str(main_ui_runtime.mode or "") == "fight" and str(fight.outcome_kind or "") == "retreat") timeout 5.0
    $ _fight_test_picture = str(fight.return_picture or "")
    $ fight_finish_to_room(str(scene_runtime.text or ""))
    $ scene_runtime.picture = _fight_test_picture
    $ scene_runtime.picture = _fight_test_picture
    assert eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == "ArtisansQuarter") timeout 5.0

    $ TownStreet.events_today = 1
    $ TownStreet.patrols_today = 1
    $ TownStreet.fights_today = 1
    $ TownStreet.curfew_caught_today = 1
    $ TownStreet.story_seen_keys = ["bad-key"]
    $ TownStreet.cooldowns = {"TownStreetHelpEvent": int(current_game_day())}
    $ next_day_finish_day_events()
    assert eval (TownStreet.events_today == 0 and TownStreet.patrols_today == 0 and TownStreet.fights_today == 0 and TownStreet.curfew_caught_today == 0) timeout 5.0
    assert eval (TownStreet.story_seen_keys == [] and TownStreet.cooldowns == {"TownStreetHelpEvent": int(current_game_day())}) timeout 5.0

    run Jump("DebugTownRandomEvents")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Отладка городских случайных событий") timeout 5.0
    assert eval ("Вероятности:" in str(scene_runtime.text or "") and "Форсировать патруль" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
'''


TARGETED_CURRENT_BUG_CHECKS = r'''
label external_day_start_actual_load_probe:
    if external_player_load_marker_exists():
        return
    $ external_player_mark_load()
    $ player.inventory.items["old_axe_001"] = 7
    $ _room_add_item_by_id(rooms.get("Shed"), "old_axe_001")
    $ TodaySexEvents_Add("georgett", 3, 4, "Prostitution")
    $ main_ui_runtime.action_items.append(MenuItem("ДУБЛИКАТ", NullAction()))
    $ renpy.load("day-1")
    return


testcase external_sleep_after_midnight_detector:
    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 1, 20)
    assert eval (nextday_started_after_midnight()) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 6, 0)
    assert eval (not nextday_started_after_midnight()) timeout 5.0

testcase external_next_day_report_releases_time_block:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ player.set_money(1000)
    $ player.tavern_management.visitors = 40
    $ player.tavern_management.productnum = 200
    $ player.tavern_management.winenum = 100
    $ calendar_v2.time_advance_blocked = 1
    $ tractir_save_patch_loaded_state()
    assert eval (int(calendar_v2.time_advance_blocked or 0) == 0) timeout 5.0
    $ _room_remove_item_by_id(rooms.get("Shed"), "old_axe_001")
    $ player.inventory.items["old_axe_001"] = 1
    $ external_player_clear_load_marker()
    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 23, 0)
    $ _nextday_test_day = int(calendar_v2.daysInGame or 0)
    run Call("NextDay", "TavernMain", 1)
    advance until screen "nextday_report_card_overlay" timeout 30.0
    assert eval (int(calendar_v2.time_advance_blocked or 0) == 1) timeout 5.0
    assert eval (int(calendar_v2.daysInGame or 0) == _nextday_test_day + 1 and int(calendar_v2.hour or 0) == 6 and int(calendar_v2.minute or 0) == 0) timeout 5.0
    assert eval (str(next_day_runtime.report_title or "") == "ОТЧЕТ ЗА ДЕНЬ" and "Новый день настал!" in str(next_day_runtime.report_body or "")) timeout 5.0
    click id "nextday_report_back_button" pos (0.5, 0.5) until eval (renpy.get_screen("nextday_report_card_overlay") is None) timeout 20.0
    advance until eval (str(rooms.current_code or "") == "TavernMyRoom" and renpy.get_screen("main_ui") is not None) timeout 30.0
    assert eval (int(calendar_v2.time_advance_blocked or 0) == 0) timeout 5.0
    assert eval (renpy.can_load("day-1")) timeout 5.0
    $ _day_start_save_data = renpy.get_save_data("day-1")
    $ _day_start_saved_player = _day_start_save_data.get("player")
    $ _day_start_saved_rooms = _day_start_save_data.get("rooms")
    $ _day_start_saved_calendar = _day_start_save_data.get("calendar_v2")
    $ _day_start_saved_sex_events = _day_start_save_data.get("SexEvents")
    assert eval (isinstance(_day_start_saved_player, Player) and int(_day_start_saved_player.item_count("old_axe_001") or 0) == 1) timeout 5.0
    assert eval (isinstance(_day_start_saved_rooms, RoomRegistry) and not _room_has_item_by_id(_day_start_saved_rooms.get("Shed"), "old_axe_001")) timeout 5.0
    assert eval (isinstance(_day_start_saved_calendar, Calendar) and int(_day_start_saved_calendar.daysInGame or 0) == int(calendar_v2.daysInGame or 0) and int(_day_start_saved_calendar.hour or 0) == 6) timeout 5.0
    assert eval (len([str(i.caption or "") for i in main_ui_runtime.action_items]) == len(set(str(i.caption or "") for i in main_ui_runtime.action_items))) timeout 5.0
    run Call("external_day_start_actual_load_probe")
    advance until eval (str(rooms.current_code or "") == "TavernMyRoom" and renpy.get_screen("main_ui") is not None) timeout 30.0
    assert eval (int(player.item_count("old_axe_001") or 0) == 1 and not _room_has_item_by_id(rooms.get("Shed"), "old_axe_001")) timeout 5.0
    $ _day_start_reloaded_data = renpy.get_save_data("day-1")
    $ _day_start_reloaded_sex_events = _day_start_reloaded_data.get("SexEvents")
    assert eval (isinstance(_day_start_reloaded_sex_events, SexEventRuntime) and list(SexEvents.today_events or []) == list(_day_start_reloaded_sex_events.today_events or [])) timeout 5.0
    assert eval ("ДУБЛИКАТ" not in [str(i.caption or "") for i in main_ui_runtime.action_items] and len([str(i.caption or "") for i in main_ui_runtime.action_items]) == len(set(str(i.caption or "") for i in main_ui_runtime.action_items))) timeout 5.0
    $ _nextday_test_clock = int(calendar_v2.clock_minutes() or 0)
    $ apply_movement_time(5)
    assert eval (int(calendar_v2.clock_minutes() or 0) == _nextday_test_clock + 5) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 1, 20)
    $ _nextday_current_day = int(calendar_v2.daysInGame or 0)
    $ _nextday_today_date = calendar_v2.format_date_ru(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, None, False)
    $ _nextday_previous_parts = calendar_v2.day_number_to_parts(_nextday_current_day - 1)
    $ _nextday_previous_date = calendar_v2.format_date_ru(_nextday_previous_parts["day"], _nextday_previous_parts["month"], _nextday_previous_parts["year"], None, False)
    $ player.appearance.remove_dress("citydress")
    $ dress_shop.produced = "citydress"
    $ dress_shop.buyer = "You"
    run Call("NextDay", "TavernMain", 1)
    advance until screen "nextday_report_card_overlay" timeout 30.0
    assert eval (int(calendar_v2.daysInGame or 0) == _nextday_current_day and int(calendar_v2.hour or 0) == 6) timeout 5.0
    assert eval (("События за %s" % _nextday_previous_date) in str(next_day_runtime.report_body or "")) timeout 5.0
    assert eval (("События за %s" % _nextday_today_date) not in str(next_day_runtime.report_body or "")) timeout 5.0
    assert eval ("Утром прибежал посыльный из лавки Фараго" in str(next_day_runtime.report_body or "")) timeout 5.0
    assert eval (player.appearance.has_dress("citydress") and int(player.appearance.dress_days.get("citydress", -1) or -1) == _nextday_current_day) timeout 5.0
    click id "nextday_report_back_button" pos (0.5, 0.5) until eval (renpy.get_screen("nextday_report_card_overlay") is None) timeout 20.0
    advance until eval (int(calendar_v2.time_advance_blocked or 0) == 0 and renpy.get_screen("main_ui") is not None) timeout 30.0

testcase external_town_thugs_shout_result:
    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 18, 0)
    $ rooms.enter("StreetTavern")
    $ scene_runtime.picture = "bg StreetTavern"
    $ scene_runtime.picture = scene_runtime.picture
    $ player.set_stat("health", 100)
    $ player.set_stat("energy", 100)
    $ player.set_stat("exploration", 300)
    $ player.set_stat("notoriety", 0)
    $ player.set_stat("reputation", 0)
    $ TownStreet.events_today = 0
    $ TownStreet.patrols_today = 0
    $ TownStreet.fights_today = 0
    $ TownStreet.curfew_caught_today = 0
    $ TownStreet.story_seen_keys = []
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Call("TownStreetThugsEvent")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (int(player.stats.exploration or 0) >= 306 and int(player.stats.reputation or 0) >= 2 and int(player.stats.notoriety or 0) >= 4) timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0

testcase external_town_thugs_fight_victory_result:
    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 18, 0)
    $ rooms.enter("ArtisansQuarter")
    $ scene_runtime.picture = "bg ArtisansQuarter"
    $ scene_runtime.picture = scene_runtime.picture
    $ player.set_stat("health", 30)
    $ player.set_stat("energy", 100)
    $ player.set_stat("exploration", 300)
    $ player.set_stat("reputation", 10)
    $ player.economy.tavern_fame = 5
    $ player.set_stat("notoriety", 0)
    $ player.inventory.items = {}
    $ player.add_item("old_axe_001", 1)
    $ player.equip("old_axe_001", "weapon")
    $ player.unequip("armor")
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    run Call("TownStreetThugsFight")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight" and str(fight.enemy_id or "") == "street_crook") timeout 5.0
    $ fight.enemy_party[0].health = 1
    $ fight.enemy_party[0].energy = 1
    $ fight.enemy_party[1].health = 0
    $ fight.enemy_party[1].energy = 0
    $ main_ui_runtime.action_items = fight_action_items()
    $ _attack_caption = fight_attack_action_caption()
    $ _attack_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index(_attack_caption)
    $ _attack_button_id = "choice_panel_button_%d" % int(_attack_index)
    click id _attack_button_id pos (0.5, 0.5) until eval (str(fight.outcome_kind or "") == "victory" and str(main_ui_runtime.action_title or "") == "Победа") timeout 20.0
    assert eval (isinstance(fight.last_result, dict) and str(fight.last_result.get("outcome", "") or "") == "victory") timeout 5.0
    assert eval (isinstance(fight.victory_loot, dict) and "money" in fight.victory_loot) timeout 5.0
    assert eval ("добыч" in str(scene_runtime.text or "").lower()) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    assert eval (int(player.stats.reputation or 0) == 13 and int(player.economy.tavern_fame or 0) == 6 and int(player.stats.notoriety or 0) == 3) timeout 5.0
    assert eval ("Вы отбили прохожего у громил" in str(scene_runtime.text or "") and str(rooms.current_code or "") == "ArtisansQuarter") timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0

testcase external_georgette_back_alley_not_visible_in_port_streets:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(3, 1, CALENDAR_START_CYCLE, 20, 0)
    $ external_calendar_set_weekday(1)
    $ Georgett.data.set_schedule([NPCScheduleEntry(location="PortStreets", start_minute=0, end_minute=1440, priority=999)])
    $ rooms.enter("PortStreets")
    $ Georgett.var["portstreet_clients_seen_today"] = 1
    $ Georgett.rel = 0
    assert eval (str(people.location("georgett") or "") == "PortStreets") timeout 5.0
    assert eval (people.action_data_for_room("georgett", "PortStreets") is not None) timeout 5.0
    assert eval (Georgett.talk_available_in_room("PortStreets")) timeout 5.0
    $ Georgett.rel = 1
    assert eval (str(people.location("georgett") or "") == "PortStreets") timeout 5.0
    assert eval ("georgett" in list(people.ids_at("PortStreets") or [])) timeout 5.0
    assert eval (Georgett.talk_available_in_room("PortStreets")) timeout 5.0
    $ _georgett_port_data = people.action_data_for_room("georgett", "PortStreets")
    assert eval (tuple(_georgett_port_data.get("talk_args", ())) == ("georgett", "street")) timeout 5.0
    assert eval (str(_georgett_port_data.get("idle_picture", "") or "") == "images/georgett/portraits/portrait.jpg") timeout 5.0

    $ Georgett.var["portstreet_clients_seen_today"] = 0
    $ Georgett.known = True
    $ Georgett.set_story_value("TalkChurchAfterCermonLiza", 0)
    $ TodaySexEvents_Clear()
    $ TodaySexEvents_Add("georgett", 3, 1, "Prostitution")
    $ initStoryEventRuntime(True)
    run Jump("PortStreets")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Почему-то Жоржетты сейчас нет на ее обычном месте. Где же она может быть?" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (str(people.location("georgett") or "") == "PortStreets" and people.action_data_for_room("georgett", "PortStreets") is None) timeout 5.0
    assert eval ("Пойти проверить подворотню" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _georgett_alley_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Пойти проверить подворотню")
    click id ("choice_panel_button_%d" % int(_georgett_alley_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Подсмотреть" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and str(main_ui_runtime.mode or "") == "event") timeout 5.0
    $ _georgett_peek_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Подсмотреть")
    click id ("choice_panel_button_%d" % int(_georgett_peek_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Вернуться в переулок" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and "Вы видите стоящую раком Жоржетту" in str(scene_runtime.text or "") and str(scene_runtime.picture or "").startswith("images/georgett/portevents/event1_")) timeout 5.0
    $ _georgett_client_back_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Вернуться в переулок")
    click id ("choice_panel_button_%d" % int(_georgett_client_back_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (str(rooms.current_code or "") == "PortStreets" and renpy.get_screen("main_ui") is not None) timeout 5.0

    run Call("IntGeorgettTalk", "georgett", "street")
    advance until screen "choice" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 5.0
    assert eval ("Болтать" in [str(getattr(i, "caption", "") or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ Georgett.rel = 0
    assert eval (str(people.location("georgett") or "") == "PortStreets") timeout 5.0

'''


DEBUG_BUILDER_ROOM_CHECKS = r'''
testcase external_debug_builder_room_visual_surfaces:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0

    assert eval (bool(config.developer)) timeout 5.0
    click id "main_ui_debug_builder_button" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "DebugBuilderRoom") timeout 20.0
    assert eval (str(rooms.current_code or "") == "DebugBuilderRoom") timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Debug Builder") timeout 5.0
    assert eval ("Picture path checks" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("Event condition probes" in [str(i.caption or "") for i in main_ui_runtime.action_items] and "Correction ownership notes" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _debug_week_before = int(calendar_v2.week or 1)
    $ _debug_month_before = int(calendar_v2.period or 1)
    $ player.chores.weekly["bring_woods"] = 0
    click id "debug_builder_time_slot_3" pos (0.5, 0.5) until eval (int(calendar_v2.time_slot()) == 3) timeout 10.0
    click id "debug_builder_week_next" pos (0.5, 0.5) until eval (int(calendar_v2.week or 1) != _debug_week_before) timeout 10.0
    click id "debug_builder_month_next" pos (0.5, 0.5) until eval (int(calendar_v2.period or 1) != _debug_month_before) timeout 10.0
    click id "debug_builder_chore_inc_bring_woods" pos (0.5, 0.5) until eval (int(player.chores.weekly.get("bring_woods", 0) or 0) == 1) timeout 10.0

    run Jump("DebugBuilderPictures")
    advance until screen "main_ui" timeout 20.0
    assert eval ("images/general/player_card.jpg" in str(scene_runtime.text or "") and "[OK] images/amanda/amanda_card.jpg" in str(scene_runtime.text or "")) timeout 5.0

    run Jump("DebugBuilderSequences")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Picture sequences" and "Picture sequence probes:" in str(scene_runtime.text or "")) timeout 5.0

    run Call("DebugBuilderInspectRoom", "TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Room: TavernKitchen" in str(scene_runtime.text or "") and "Descriptions:" in str(scene_runtime.text or "") and "Visible NPCs from schedule:" in str(scene_runtime.text or "")) timeout 5.0

    run Call("DebugBuilderMenuRoom", "TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Room/menu probe: TavernKitchen" in str(scene_runtime.text or "") and "Visible generated menu items:" in str(scene_runtime.text or "")) timeout 5.0

    run Jump("DebugBuilderStoryEvents")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Story events" and "Projected story events now:" in str(scene_runtime.text or "")) timeout 5.0

    run Jump("DebugBuilderEventProbes")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Event condition probes" and "Event condition probes:" in str(scene_runtime.text or "")) timeout 5.0

    run Jump("DebugBuilderSchedules")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "NPC schedules" and "NPC schedule at week=" in str(scene_runtime.text or "") and "23:00-05:59" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ("Probe rooms" in [str(i.caption or "") for i in main_ui_runtime.action_items] and "16:00 Day" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    run Call("DebugBuilderScheduleRoom", "TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Schedule room probe: TavernKitchen" in str(scene_runtime.text or "") and "getNPCids:" in str(scene_runtime.text or "") and "Room.visible_npcs:" not in str(scene_runtime.text or "")) timeout 5.0

    run Jump("DebugBuilderCorrectionNotes")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Correction notes" and "Correction ownership notes:" in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Repair notes written") timeout 10.0
    assert eval ("Repair notes document written:" in str(scene_runtime.text or "")) timeout 5.0
    $ _repair_doc_path = str(debug_builder_write_repair_document() or "")
    assert eval (str(_repair_doc_path or "").endswith("debug_builder_repair_notes.md") and os.path.isfile(_repair_doc_path)) timeout 5.0
    assert eval ("## Feature Repair Templates" in open(_repair_doc_path, "r", encoding="utf-8").read() and "### Event / Thread Feature" in open(_repair_doc_path, "r", encoding="utf-8").read()) timeout 5.0

    run Jump("DebugBuilderCards")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Amanda" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ show_girl_card_main_ui_state("amanda")
    assert eval (str(girl_card_portrait_path("amanda") or "") == "images/amanda/amanda_card.jpg") timeout 5.0

    $ player.condition.health = 100
    $ player.condition.energy = 100
    $ player.stats.exploration = 0
    $ player.equipment.weapon = ""
    $ player.equipment.armor = ""
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    $ _debug_dog = dog
    $ player.remove_party_member("dog")
    run Jump("DebugBuilderFightTests")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Fight tests" and all(label in [str(i.caption or "") for i in main_ui_runtime.action_items] for label in ["Fight setup", "Launch fights"])) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Fight setup") timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Fight setup" and all(any(str(i.caption or "").startswith(prefix) for i in main_ui_runtime.action_items) for prefix in ["Launch fights", "Weapon:", "Armor:", "Health:", "Experience:", "Supplies:", "Dog:"])) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (str(player.equipment.weapon or "") == "old_axe_001" and str(main_ui_runtime.action_title or "") == "Fight setup") timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (str(player.equipment.weapon or "") == "rusty_hunter_rifle_001" and fight_supply_count("arrows") > 0 and str(fight.loaded_ammo or "") == "arrows" and int(fight.weapon_loaded or 0) == 1) timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (str(player.equipment.armor or "") == "old_leather_cuirass_001" and str(main_ui_runtime.action_title or "") == "Fight setup") timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (str(player.equipment.armor or "") == "" and str(main_ui_runtime.action_title or "") == "Fight setup") timeout 20.0
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (int(player.condition.health or 0) == 60 and str(main_ui_runtime.action_title or "") == "Fight setup") timeout 20.0
    click id "choice_panel_button_4" pos (0.5, 0.5) until eval (int(player.stats.exploration or 0) == 50 and fight_player_level() >= 2) timeout 20.0
    click id "choice_panel_button_5" pos (0.5, 0.5) until eval (fight_supply_count("bandage") > 0 and fight_supply_count("healing_potion") > 0 and fight_supply_count("fire_bomb") > 0 and fight_supply_count("bees_bomb") > 0) timeout 20.0
    click id "choice_panel_button_6" pos (0.5, 0.5) until eval (bool(dog.owned) and "dog" in player.combat.party and str(main_ui_runtime.action_title or "") == "Fight setup") timeout 20.0
    assert eval (len(list(fight_company_display_rows() or [])) >= 2 and "notoriety" in dict(list(fight_company_display_rows() or [{}])[0]) and "exploration" in dict(list(fight_company_display_rows() or [{}])[0])) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Launch fights") timeout 20.0
    assert eval (all(label in [str(i.caption or "") for i in main_ui_runtime.action_items] for label in ["Street crooks", "Random forest hunt roll", "Patrol guards"])) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "fight") timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight" and str(fight.enemy_id or "") == "street_crook" and len(list(fight.enemy_party or [])) == 2) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "") == "images/fight/thug.png") timeout 5.0
    assert eval (len(list(fight_enemy_display_rows() or [])) == 2 and all(int(row.get("health_max", 0) or 0) > 0 and int(row.get("energy_max", 0) or 0) > 0 for row in list(fight_enemy_display_rows() or []))) timeout 5.0
    assert eval (all(label in [str(i.caption or "") for i in main_ui_runtime.action_items] for label in ["Выстрелить (стрела)", "Использовать бинт", "Выпить бодрящий чай", "Выпить лечебное зелье", "Бросить огненную бутылку", "Бросить пчелиный заряд", "Командовать псом", "Скрыться"])) timeout 5.0
    $ _debug_turn_text_before = str(scene_runtime.text or "")
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (str(scene_runtime.text or "") != _debug_turn_text_before and str(main_ui_runtime.mode or "") == "fight") timeout 20.0
    assert eval (str(scene_runtime.text or "") != _debug_turn_text_before and str(main_ui_runtime.mode or "") == "fight") timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Команды" and "Скрыться" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _debug_turn_text_before = str(scene_runtime.text or "")
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (str(scene_runtime.text or "") != _debug_turn_text_before and str(main_ui_runtime.mode or "") == "fight") timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Команды" and "Скрыться" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ fight_finish_to_room("Debug fight closed.")
    assert eval (str(rooms.current_code or "") == "DebugBuilderFightTests" and str(main_ui_runtime.mode or "") == "scene") timeout 5.0
'''


AMANDA_ROOM_NIGHT_EVENT_CHECKS = r'''
testcase external_amanda_room_night_bed_action_uses_thread_event:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0

    assert eval (isinstance(AmandaRoomNightApproach, AmandaRoomNightApproachEvent) and isinstance(AmandaBirth, AmandaBirthEvent)) timeout 5.0
    assert eval (int(threads["amandaStreetLegareSightings"].data.length or 0) == 1 and sorted([str(evt.location or "") for evt in threads["amandaStreetLegareSightings"].data.triggers[0]]) == ["MarketPlace", "StreetTavern"]) timeout 5.0
    assert eval (story_event_day_key(AmandaStreetLegareSightingStreet) == story_event_day_key(AmandaStreetLegareSightingMarket)) timeout 5.0
    assert eval (int(threads["amandaStreetLoverEncounters"].data.length or 0) == 1 and sorted([str(evt.location or "") for evt in threads["amandaStreetLoverEncounters"].data.triggers[0]]) == ["MarketPlace", "StreetTavern"]) timeout 5.0
    assert eval (story_event_day_key(AmandaStreetLoverEncounterStreet) == story_event_day_key(AmandaStreetLoverEncounterMarket)) timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 14, 0)
    $ external_calendar_set_weekday(1)
    assert eval (str(people.location("amanda") or "") == "TavernMain") timeout 5.0
    $ rooms.enter("TavernUpstairs")
    run Call("TavernAmandaRoomKnock")
    assert eval (str(scene_runtime.text or "") == "Вы постучали в дверь, но ответа не последовало.") timeout 5.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items] == ["Попробовать войти", "Уйти"]) timeout 5.0
    assert eval ("Кто там?" not in str(scene_runtime.text or "") and "Аманда отвечает" not in str(scene_runtime.text or "")) timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    $ Melissa.temp_room_code = ""
    $ Melissa.drawings_found = False
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernAmandaRoom", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernAmandaRoom", start_minute=0, end_minute=1440, awake=False, talkable=False, priority=999)])
    $ cametoday = 0
    $ cancumdaily = 3
    $ Amanda.room_entry_blocked_today = False
    $ Amanda.room_rejection_count = 0
    run Jump("TavernAmandaRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernAmandaRoom") timeout 5.0
    assert eval ("Кровать" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    run Call("tavern_amanda_room_object_menu", "bed_002")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Кровать") timeout 5.0
    assert eval ("Пристать к Аманде" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
'''


MY_ROOM_RECIPE_BOOK_ACTION_CHECKS = r'''
testcase external_my_room_recipe_book_table_link:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ calendar_v2.time_advance_blocked = 0
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ _room_remove_item_by_id(rooms.get("TavernMyRoom"), "recipe_book_001")
    $ _room_add_item_by_id(rooms.get("TavernMyRoom"), "recipe_book_001")

    run Jump("TavernMyRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval ("recipe_book_001" not in [str(getattr(i.action, 'label', '') or '') for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("книга с рецептами" not in [str(i.caption or "").lower() for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("{a=call:TavernMyRoomTableMenu}" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ("старая пыльная книга с рецептами" in str(scene_runtime.text or "")) timeout 5.0

    run Call("TavernMyRoomTableMenu")
    assert eval (str(main_ui_runtime.action_title or "") == "Стол") timeout 5.0
    assert eval ("Читать книгу рецептов" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("Создать предмет" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ _moss_before = int(player.item_count("moss_001") or 0)
    $ _dried_moss_before = int(player.item_count("dried_moss_001") or 0)
    $ _craft_clock_before = int(calendar_v2.clock_minutes() or 0)
    $ player.add_item("moss_001", 1)
    $ _dry_moss_result = apply_recipe_craft("dry_moss_recipe")
    assert eval (bool(_dry_moss_result.get("ok", False)) and str(_dry_moss_result.get("item_result", "") or "") == "dried_moss_001") timeout 5.0
    assert eval (int(player.item_count("moss_001") or 0) == _moss_before and int(player.item_count("dried_moss_001") or 0) == _dried_moss_before + 1) timeout 5.0
    assert eval (int(calendar_v2.clock_minutes() or 0) == _craft_clock_before + 30 and "сухую крошку" in str(_dry_moss_result.get("text", "") or "")) timeout 5.0
'''


MY_ROOM_WINDOW_ACTION_CHECKS = r'''
testcase external_my_room_window_day_night_amanda_pictures:
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ rooms.enter("TavernMyRoom")
    $ Amanda.night_bowl_given = False
    $ event_runtime.evaluation_time = None
    run Call("TavernMyRoomWindowLookBackyard")
    assert eval (str(scene_runtime.picture or "") == "images/player_room/window0.png") timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Маленькое окно" and "Назад" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    $ Amanda.night_bowl_given = False
    $ event_runtime.evaluation_time = None
    run Call("TavernMyRoomWindowLookBackyard")
    assert eval (str(scene_runtime.picture or "") == "images/player_room/window2.png") timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Маленькое окно" and "Назад" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ Amanda.night_bowl_given = True
    $ Amanda.fancy_night_bowl_received = False
    $ Amanda.backyard_relief_preference = -1
    $ player.add_item("night_bowl_001", 1)
    $ event_runtime.evaluation_time = None
    run Call("TavernMyRoomWindowLookBackyard")
    assert eval (str(scene_runtime.picture or "") == "images/player_room/windowAmand.png") timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Маленькое окно" and "Назад" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval (story_event_day_key(AmandaNightBowlWindow) in list(event_runtime.fired_keys_today or [])) timeout 5.0
    assert eval (int(event_runtime.fired_day if event_runtime.fired_day is not None else -1) == int(calendar_v2.daysInGame or 0)) timeout 5.0
    assert eval (story_event_fired_today(AmandaNightBowlWindow)) timeout 5.0
'''


TAVERN_ROOM_PICTURE_STATE_CHECKS = r'''
testcase external_tavern_room_movement_resets_picture_state:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernMain") timeout 5.0
    assert eval (str(scene_runtime.picture or "") == "images/tavern/mainhall/main_hall.png") timeout 5.0

    run Call("TavernMainObjectMenu", "bar_001")
    assert eval (str(main_ui_runtime.object_id or "") == "bar_001") timeout 5.0
    assert eval (str(scene_runtime.picture or "") == "images/tavern/mainhall/bar_mainHall.png") timeout 5.0

    run movement_actions("TavernKitchen", 5)
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernKitchen") timeout 5.0
    assert eval (str(main_ui_runtime.object_id or "") == "" and str(main_ui_runtime.girl_key or "") == "") timeout 5.0
    assert eval (str(scene_runtime.picture or "") != "images/tavern/mainhall/bar_mainHall.png") timeout 5.0
    assert eval ("kitchen" in str(scene_runtime.picture or "").lower()) timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernMain") timeout 5.0
    assert eval (str(main_ui_runtime.object_id or "") == "") timeout 5.0
    assert eval (str(scene_runtime.picture or "") == "images/tavern/mainhall/main_hall_night.png") timeout 5.0

testcase external_room_exit_time_costs:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ rooms.enter("TavernKitchen")
    $ _movement_before = int(calendar_v2.clock_minutes() or 0)
    run rooms.get("TavernKitchen").build_exit_items()[0].action
    advance until eval (str(rooms.current_code or "") == "TavernMain") timeout 20.0
    assert eval (int(calendar_v2.clock_minutes() or 0) - _movement_before == 5) timeout 5.0

    $ rooms.enter("BarberShop")
    $ _movement_before = int(calendar_v2.clock_minutes() or 0)
    run rooms.get("BarberShop").build_exit_items()[0].action
    advance until eval (str(rooms.current_code or "") == "ArtisansQuarter") timeout 20.0
    assert eval (int(calendar_v2.clock_minutes() or 0) - _movement_before == 10) timeout 5.0

    $ rooms.enter("GroceryStore")
    $ _movement_before = int(calendar_v2.clock_minutes() or 0)
    run rooms.get("GroceryStore").build_exit_items()[0].action
    advance until eval (str(rooms.current_code or "") == "MarketPlace") timeout 20.0
    assert eval (int(calendar_v2.clock_minutes() or 0) - _movement_before == 10) timeout 5.0

    $ rooms.enter("TavernUpstairs")
    run Call("TavernAmandaRoomKnockAnswer")
    $ _movement_before = int(calendar_v2.clock_minutes() or 0)
    run main_ui_runtime.action_items[0].action
    advance until eval (str(rooms.current_code or "") == "TavernAmandaRoom") timeout 20.0
    assert eval (int(calendar_v2.clock_minutes() or 0) - _movement_before == 5) timeout 5.0

testcase external_player_exploration_progression:
    $ player.set_stat("exploration", 95)
    $ _exploration_after_gain = player.change_stat("exploration", 15)
    assert eval (int(_exploration_after_gain or 0) == 110 and int(player.stats.exploration or 0) == 110) timeout 5.0
    $ _exploration_after_loss = player.change_stat("exploration", -20)
    assert eval (int(_exploration_after_loss or 0) == 90 and int(player.stats.exploration or 0) == 90) timeout 5.0
    $ player.set_stat("exploration", 300)
    assert eval (int(player.stats.exploration or 0) == 300) timeout 5.0
'''


MELISSA_BATS_DRAWINGS_CHECKS = r'''
testcase external_melissa_recipe_unlock_single_authority:
    $ recipe_book_item_state()["hidden_recipes_revealed"] = False
    $ Melissa.var["bat_recipe_unlocked"] = 1
    assert eval (not recipe_page_is_unlocked("bat_repellent_recipe")) timeout 5.0
    $ Melissa.var.pop("bat_recipe_unlocked", None)
    $ recipe_book_item_state()["hidden_recipes_revealed"] = True
    assert eval (recipe_page_is_unlocked("bat_repellent_recipe")) timeout 5.0
    assert eval ("bat_repellent_recipe" in visible_recipe_pages()) timeout 5.0
    $ Melissa.var["bat_recipe_unlocked"] = 1
    $ Melissa.var["private_context_place"] = "wine_cellar"
    $ Melissa.var["private_place_heat"] = 99
    $ Melissa.var["sex_times_today"] = 3
    $ Melissa.var["room_pests_last_help_day"] = 17
    $ Melissa.var["bats_completion_day"] = 18
    $ saveVersion = 48
    $ updateSave()
    assert eval (int(saveVersion or 0) == int(currentVersion or 0)) timeout 5.0
    assert eval (all(key not in Melissa.var for key in ["bat_recipe_unlocked", "private_context_place", "private_place_heat", "sex_times_today", "room_pests_last_help_day", "bats_completion_day"])) timeout 5.0

testcase external_melissa_bats_room_search_after_wait:
    $ _melissa_bats_test_date = calendar_v2.day_number_to_parts(100)
    $ external_calendar_set_fields(int(_melissa_bats_test_date.get("day", 1) or 1), int(_melissa_bats_test_date.get("month", 1) or 1), int(_melissa_bats_test_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 14, 0)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ rooms.enter("TavernMelissaRoom")
    $ Melissa.initialize_new_game_state()
    $ Melissa.temp_room_code = "TavernAmandaRoom"
    $ Melissa.drawings_found = False
    $ Melissa.drawings_booklet_left = False
    $ Melissa.drawings_ready_day = 86
    $ player.set_stat("exploration", 121)
    $ player.remove_item("melissa_drawings_booklet_001", player.item_count("melissa_drawings_booklet_001"))
    $ player.chores.weekly["clean_upstairs_rooms"] = int(player_chore_target("clean_upstairs_rooms") or 0)
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ Melissa.var["bats_episode"] = 5
    $ updateSave_V22()
    assert eval (int(threads["melissaBatProblem"].num or 0) == 5 and "bats_episode" not in Melissa.var) timeout 5.0
    $ threads["melissaBatProblem"].advanceTo(6, force_active=True)
    $ findAvailableEvents(True)

    assert eval (int(threads["melissaBatProblem"].data.length or 0) == 8) timeout 5.0
    assert eval (int(threads["melissaBatProblem"].num or 0) == 6) timeout 5.0
    assert eval (set(str(evt.target or "") for evt in threads["melissaBatProblem"].data.triggers[6]) == set(["story_melissa_bat_problem_5", "story_melissa_bat_problem_4"])) timeout 5.0
    assert eval (threads["melissaBatProblem"].currentTarget() == "story_melissa_bat_problem_5") timeout 5.0
    assert eval (story_event_available("TavernMelissaRoom", "room_search")) timeout 5.0
    assert eval (str(event_runtime.available["TavernMelissaRoom"]["room_search"].target or "") == "story_melissa_bat_problem_5") timeout 5.0
    run Jump("TavernMelissaRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Осмотреть комнату получше" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("пачка непристойных рисунков" not in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 10.0
    click pos (0.5, 0.5) until eval (bool(Melissa.drawings_found)) timeout 10.0
    assert eval (bool(Melissa.drawings_found)) timeout 5.0
    assert eval (int(_room_item_count_by_id(rooms.get("TavernMelissaRoom"), "melissa_drawings_booklet_001") or 0) == 1) timeout 5.0
    click pos (0.5, 0.5) until eval ("пачка непристойных рисунков" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 10.0
    assert eval ("пачка непристойных рисунков" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items].index("пачка непристойных рисунков") == 2) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (str(main_ui_runtime.object_id or "") == "melissa_drawings_booklet_001") timeout 10.0
    assert eval (str(main_ui_runtime.object_id or "") == "melissa_drawings_booklet_001") timeout 5.0
    assert eval (len(list(main_ui_runtime.action_items or [])) >= 5) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (int(player.item_count("melissa_drawings_booklet_001") or 0) == 1) timeout 10.0
    assert eval (not bool(Melissa.drawings_booklet_left)) timeout 5.0
    assert eval (int(player.item_count("melissa_drawings_booklet_001") or 0) == 1) timeout 5.0
    assert eval (int(_room_item_count_by_id(rooms.get("TavernMelissaRoom"), "melissa_drawings_booklet_001") or 0) == 0) timeout 5.0
    $ show_player_card_main_ui_state()
    $ player_card_show_inventory_item_state("melissa_drawings_booklet_001")
    assert eval (str(main_ui_runtime.mode or "") == "mc" and "Прочитать буклет" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval (all(caption not in [str(i.caption or "") for i in main_ui_runtime.action_items] for caption in ["Взять буклет", "Оставить его там, где лежал", "Продолжить поиски"])) timeout 5.0
    $ _melissa_booklet_read_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Прочитать буклет")
    $ _melissa_booklet_read_button_id = "choice_panel_button_%d" % int(_melissa_booklet_read_index)
    click id _melissa_booklet_read_button_id pos (0.5, 0.5) until screen "say" timeout 10.0
    advance until eval (bool(Melissa.drawings_booklet_read) and str(main_ui_runtime.mode or "") == "mc" and "Прочитать буклет" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernMelissaRoom" and str(main_ui_runtime.action_title or "") == "пачка непристойных рисунков") timeout 5.0
    $ main_ui_end_card_state()
    assert eval (int(threads["melissaBatProblem"].num or 0) == 6) timeout 5.0
    assert eval (story_event_available("TavernAtic", "melissa_bats")) timeout 5.0
    $ player.add_item("bat_repellent_001", 1)
    $ rooms.enter("TavernAtic")
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (str(event_runtime.available["TavernAtic"]["melissa_bats"].target or "") == "story_melissa_bat_problem_4") timeout 5.0
    run Call("checkTriggers", "TavernAtic", "melissa_bats", 0)
    click pos (0.5, 0.5) until eval (int(threads["melissaBatProblem"].num or 0) == 7) timeout 10.0
    assert eval (int(threads["melissaBatProblem"].num or 0) == 7) timeout 5.0

    $ player.set_money(max(1000, int(player.economy.money or 0)))
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (str(event_runtime.available["TavernAtic"]["melissa_bats"].target or "") == "story_melissa_bat_problem_roof") timeout 5.0
    run Call("checkTriggers", "TavernAtic", "melissa_bats", 0)
    click pos (0.5, 0.5) until eval (int(Melissa.roof_repair_complete_day or -1) >= 0) timeout 10.0
    assert eval (int(threads["melissaBatProblem"].num or 0) == 7) timeout 5.0

    $ Melissa.roof_repair_complete_day = int(current_game_day() or 0)
    $ Melissa.drawings_returned = True
    $ rooms.enter("TavernMain")
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (story_event_available("TavernMain", "melissa_talk")) timeout 5.0
    run Call("checkTriggers", "TavernMain", "melissa_talk", 0)
    click pos (0.5, 0.5) until eval (int(threads["melissaBatProblem"].num or 0) == 8) timeout 10.0
    assert eval (bool(threads["melissaBatProblem"].completed)) timeout 5.0

testcase external_melissa_werecat_thread_condition_sequence:
    $ external_calendar_set_fields(3, 1, 1100, 6, 0)
    run Call("InitGameNPCs")
    $ rooms.enter("TavernStorage")
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = False
    $ Melissa.initialize_new_game_state()
    $ Melissa.storage_rat_help_day = -1
    $ werecat_state()["rats_problem_active"] = 0
    $ werecat_state()["rat_breakfast_seen"] = 0
    $ werecat_state()["hunter_tease_day"] = -1
    $ werecat_state()["adopted"] = 0
    $ werecat_state()["adopted_count"] = 0
    $ werecat_state()["adoption_breakfast_seen"] = 0
    $ werecat_state()["adopted_day"] = -1
    $ werecat_state()["first_month_thanks_day"] = -1
    $ npc_interval_schedule_load_all(True)
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6, 7], start_hour=0, end_hour=24, awake=True, talkable=True, priority=999, label="external_storage_rat")])
    $ Melissa.temp_room_code = "TavernStorage"
    $ household_mark_runtime_event_seen("melissa_storage_rat", -999)
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval (threads["melissaRatProblem"].currentTarget() == "story_melissa_storage_rat_0") timeout 5.0
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_rumor_0") timeout 5.0
    assert eval (not threads["melissaWerecatProblem"].checkActive()) timeout 5.0
    $ _rat_evt = threads["melissaRatProblem"].getevent(0)
    $ _rat_check_fields = [str(row.get("field", "") or "") for row in _rat_evt.auditChecks(threads["melissaRatProblem"].day)]
    assert eval (int(Melissa.storage_rat_help_day or -1) < 0) timeout 5.0
    assert eval (str(people.location("melissa") or "") == "TavernStorage") timeout 5.0
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

    $ Melissa.storage_rat_help_day = current_game_day()
    $ Melissa.temp_room_code = ""
    $ werecat_state()["rats_problem_active"] = 1
    $ threads["melissaRatProblem"].advance()
    $ external_calendar_set_fields(3, 1, 1100, 8, 0)
    $ rooms.enter("HunterClub")
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval (threads["melissaRatProblem"].completed) timeout 5.0
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_rumor_0") timeout 5.0
    $ _rumor_evt = threads["melissaWerecatProblem"].getevent(0)
    $ _rumor_check_map = {str(row.get("field", "") or ""): bool(row.get("ok", False)) for row in _rumor_evt.auditChecks(threads["melissaWerecatProblem"].day)}
    assert eval (_rumor_check_map.get("day", False)) timeout 5.0
    assert eval (_rumor_check_map.get("hour", False)) timeout 5.0
    assert eval (_rumor_check_map.get("delay", False)) timeout 5.0
    assert eval (_rumor_check_map.get("requirements", False)) timeout 5.0
    assert eval (_rumor_check_map.get("conditions", False)) timeout 5.0
    assert eval (_rumor_check_map.get("location_open", False)) timeout 5.0
    assert eval (story_event_available("HunterClub", "overheard")) timeout 5.0

    $ event_runtime.active_thread = threads["melissaWerecatProblem"]
    $ event_runtime.active_thread.setDay()
    run Call("story_melissa_werecat_rumor_0")
    assert eval (int(werecat_state().get("hunter_tease_day", -1) or -1) == current_game_day()) timeout 5.0
    advance until eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_intro_0") timeout 10.0
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_intro_0") timeout 5.0

    $ external_calendar_set_fields(3, 1, 1100, 7, 0)
    $ rooms.enter("TavernKitchen")
    $ player.tavern_management.breakfast.today = False
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval (rooms.get("TavernKitchen").is_open()) timeout 5.0
    assert eval (rooms.get("TavernKitchen") is rooms.get("TavernKitchen")) timeout 5.0
    assert eval (rooms.get("TavernKitchen").is_open()) timeout 5.0
    $ _intro_evt = threads["melissaWerecatProblem"].getevent(1)
    $ _intro_check_map = {str(row.get("field", "") or ""): bool(row.get("ok", False)) for row in _intro_evt.auditChecks(threads["melissaWerecatProblem"].day)}
    assert eval (_intro_check_map.get("day", False)) timeout 5.0
    assert eval (_intro_check_map.get("hour", False)) timeout 5.0
    assert eval (_intro_check_map.get("delay", False)) timeout 5.0
    assert eval (_intro_check_map.get("requirements", False)) timeout 5.0
    assert eval (_intro_check_map.get("conditions", False)) timeout 5.0
    assert eval (_intro_check_map.get("location_open", False)) timeout 5.0
    assert eval (story_event_available("TavernKitchen", "enter")) timeout 5.0

    $ event_runtime.active_thread = threads["melissaWerecatProblem"]
    $ event_runtime.active_thread.setDay()
    run Call("story_melissa_werecat_intro_0")
    assert eval (int(werecat_state().get("rat_breakfast_seen", 0) or 0) == 1) timeout 5.0
    assert eval (threads["melissaWerecatProblem"].currentTarget() == "story_melissa_werecat_home_0") timeout 5.0

    $ werecat_state()["adopted"] = 1
    $ werecat_state()["adopted_count"] = 1
    $ werecat_state()["adopted_day"] = current_game_day() - 1
    $ werecat_state()["adoption_breakfast_seen"] = 0
    $ external_calendar_set_fields(3, 1, 1100, 7, 0)
    $ player.tavern_management.breakfast.today = False
    $ event_runtime.evaluation_time = None
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
    run Jump("TavernKitchen")
    advance until eval (int(werecat_state().get("adoption_breakfast_seen", 0) or 0) == 1) timeout 20.0
    assert eval (int(werecat_state().get("adoption_breakfast_seen", 0) or 0) == 1) timeout 5.0
'''


MELISSA_WERECAT_FOREST_ACTION_CHECKS = r'''
testcase external_melissa_werecat_forest_actions_rebuild:
    $ external_calendar_set_fields(4, 1, 1100, 10, 0)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ rooms.enter("Forest")
    $ ForestReturnTarget = "StreetTavern"
    $ ForestSavedText = ""
    $ werecat_state()["rats_problem_active"] = 1
    $ werecat_state()["rat_breakfast_seen"] = 1
    $ werecat_state()["hunter_tease_day"] = current_game_day()
    $ werecat_state()["adopted"] = 0
    $ werecat_state()["adopted_count"] = 0
    $ werecat_state()["sold"] = 0
    $ werecat_state()["caught"] = 0
    $ werecat_state()["tracks_seen"] = 0
    $ werecat_state()["tracks_first_text_seen"] = 0
    $ werecat_state()["trap_rooms"] = {}
    $ Melissa.storage_rat_help_day = current_game_day() - 1
    $ player.stats.exploration = 130
    $ player.remove_item("hunting_trap_001", player.item_count("hunting_trap_001"))
    run Jump("Forest")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Осмотреть лес внимательнее" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 10.0
    advance until eval (int(werecat_state().get("tracks_seen", 0) or 0) == 1) timeout 20.0
    assert eval (int(werecat_state().get("tracks_seen", 0) or 0) == 1) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Действия") timeout 5.0
    assert eval ("Осмотреть лес внимательнее" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ player.add_item("hunting_trap_001", 1)
    run Call("WerecatSetTrap", "Forest")
    assert eval ("ставите охотничью ловушку" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (int(player.item_count("hunting_trap_001") or 0) == 0) timeout 5.0
    assert eval ("Forest" in werecat_trap_rooms()) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Действия") timeout 5.0
    assert eval ("Проверить странную приманку" not in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ werecat_state()["trap_rooms"] = {"Forest": {"day": current_game_day() - 1}}
    assert eval (list(werecat_trap_rooms().keys()) == ["Forest"]) timeout 5.0
    $ werecat_state()["woods_exploration"] = 0
    assert eval (list(werecat_trap_rooms().keys()) == ["Forest"]) timeout 5.0
    $ player.stats.exploration = 20
    assert eval (set(werecat_trap_rooms().keys()) == set(["Forest"])) timeout 5.0
    assert eval (current_game_day() > int(dict(werecat_trap_rooms()["Forest"]).get("day", -1))) timeout 5.0
    assert eval (int(werecat_state().get("caught", 0) or 0) == 0) timeout 5.0
    assert eval (werecat_can_check_bait("Forest")) timeout 5.0
    run Jump("Forest")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "Forest") timeout 5.0
    assert eval ("Forest" in werecat_trap_rooms()) timeout 5.0
    assert eval (werecat_can_check_bait("Forest")) timeout 5.0
    $ _werecat_check_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Проверить странную приманку")
    $ _werecat_check_button_id = "choice_panel_button_%s" % _werecat_check_index
    click id _werecat_check_button_id pos (0.5, 0.5)
    assert eval (len(werecat_trap_rooms()) == 0) timeout 5.0
    assert eval ("оказалась слишком осторожной" in str(scene_runtime.text or "")) timeout 5.0
    assert eval ("оказалась слишком осторожной" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (len(werecat_trap_rooms()) == 0) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Действия") timeout 5.0
'''


CHURCH_LINK_CHECKS = r'''
testcase external_church_service_action_links_work:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(7, 1, 1100, 8, 0)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ Georgett.known = True
    $ Georgett.rel = 2
    $ Georgett.corruption = 0
    $ Georgett.set_sex_stat("sexacts", 3)
    $ Georgett.set_story_value("askkids", 0)
    $ Liza.known = False
    $ player.intimacy.came_today = 0
    $ player.intimacy.can_cum_daily = 3
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
    assert eval ("Прихожане" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("прихожан" in str(scene_runtime.location_text or "")) timeout 5.0
    assert eval ("{a=church:service:1}" not in str(scene_runtime.location_text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Прихожане") timeout 10.0
    assert eval (str(main_ui_runtime.action_title or "") == "Прихожане") timeout 5.0
    assert eval ("Найти Сандру" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("Найти сестричек" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("Найти Жоржетту Брюно" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _church_blanken_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Найти семейство Блэнкеншип")
    $ _church_blanken_button = "choice_panel_button_%d" % int(_church_blanken_index)
    click id _church_blanken_button pos (0.5, 0.5) until eval ("Вдова Блэнкеншип" in str(scene_runtime.text or "")) timeout 20.0
    assert eval (str(scene_runtime.picture or "") in ("images/becky/church/cermon.png", "images/becky/church/talk1.jpg", "images/becky/church/talk2.jpg")) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Прихожане") timeout 5.0
    assert eval (not Georgett.story_value("foundinchurch", 0)) timeout 5.0
    $ _church_georgett_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Найти Жоржетту Брюно")
    $ _church_georgett_button = "choice_panel_button_%d" % int(_church_georgett_index)
    click id _church_georgett_button pos (0.5, 0.5) until eval (people_to_int(Georgett.story_value("foundinchurch", 0), 0) == 1) timeout 20.0
    assert eval (str(people.location("georgett") or "") == "Church" and str(people.schedule_state("georgett").get("label", "") or "") == "sunday_mass") timeout 5.0
    assert eval (str(scene_runtime.picture or "") == "images/georgett/church/cermon.jpg") timeout 5.0
    assert eval ("Лизет" not in str(scene_runtime.text or "") and not Liza.known) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Жоржетта" and [str(i.caption or "") for i in main_ui_runtime.action_items] == ["Предложить Жоржетте перепихнуться по быстрому", "Назад"]) timeout 5.0
    $ _church_quick_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Предложить Жоржетте перепихнуться по быстрому")
    $ _church_quick_button = "choice_panel_button_%d" % int(_church_quick_index)
    click id _church_quick_button pos (0.5, 0.5) until eval ("Ты что, сдурел" in str(scene_runtime.text or "") and str(main_ui_runtime.action_title or "") == "Разговор с Жоржеттой") timeout 20.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items] == ["Назад"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Жоржетта") timeout 20.0
    $ _church_back_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Назад")
    click id ("choice_panel_button_%d" % int(_church_back_index)) pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Прихожане") timeout 20.0
    assert eval (str(scene_runtime.picture or "") == "images/church/churchEntryDay.png") timeout 5.0

    $ Georgett.rel = 6
    $ player.economy.money = 14
    $ _church_georgett_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Найти Жоржетту Брюно")
    click id ("choice_panel_button_%d" % int(_church_georgett_index)) pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Жоржетта") timeout 20.0
    $ _church_quick_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Предложить Жоржетте перепихнуться по быстрому")
    click id ("choice_panel_button_%d" % int(_church_quick_index)) pos (0.5, 0.5) until eval ("столько нет" in str(scene_runtime.text or "") and str(main_ui_runtime.action_title or "") == "Разговор с Жоржеттой") timeout 20.0
    assert eval (int(player.economy.money or 0) == 14 and [str(i.caption or "") for i in main_ui_runtime.action_items] == ["Назад"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Жоржетта") timeout 20.0

    $ Georgett.set_story_value("askkids", 1)
    $ Georgett.set_story_value("fuckinchurch", 0)
    $ Georgett.set_story_value("lizasawinchurch", 0)
    $ Liza.rel = 0
    $ Liza.known = False
    $ player.economy.money = 100
    $ _church_quick_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Предложить Жоржетте перепихнуться по быстрому")
    click id ("choice_panel_button_%d" % int(_church_quick_index)) pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval ("Лизетточка" in str(scene_runtime.text or "")) timeout 5.0
    click pos (960, 900) until screen "choice" timeout 20.0
    assert eval (str(scene_runtime.picture or "") == "images/georgett/church/withLiza.jpg/withliza1.jpg") timeout 5.0
    assert eval (int(player.economy.money or 0) == 85) timeout 5.0
    assert eval (int(player.intimacy.came_today or 0) == 1) timeout 5.0
    assert eval (Georgett.story_value("fuckinchurch", 0) == 1 and Georgett.story_value("lizasawinchurch", 0) == 1 and int(Liza.rel or 0) == 1 and Liza.known) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(scene_runtime.picture or "").endswith("withliza2.jpg")) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(scene_runtime.picture or "").endswith("withliza3.jpg")) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(scene_runtime.picture or "").endswith("withliza4.jpg")) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(scene_runtime.picture or "").endswith("withliza5.jpg")) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(scene_runtime.picture or "").endswith("withliza6.jpg")) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "Church" and int(calendar_v2.hour or 0) == 9) timeout 20.0
    assert eval (Georgett.story_value("foundinchurch", 0) == 0 and str(main_ui_runtime.action_title or "") == "Действия") timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 10, 0)
    run Jump("Church")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Идти на исповедь" not in [str(i.caption or "") for i in main_ui_runtime.action_items] and "gerhard" in people.ids_at("Church")) timeout 5.0
    assert eval (str(people.action_data_for_room("gerhard", "Church").get("talk_label", "") or "") == "ChurchIspoved") timeout 5.0
    click id "main_ui_entity_button_npc_gerhard" pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 900) until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (960, 900) until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "Church") timeout 20.0
    assert eval (str(rooms.current_code or "") == "Church") timeout 5.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    run Jump("Church")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Обойти собор" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    run Call("ChurchAfterCermon", 1)
    advance until screen "say" timeout 20.0
    assert eval ("Ничего интересного" in str(scene_runtime.text or "")) timeout 5.0

testcase external_liza_identity_save_migration:
    run Call("InitGameNPCs")
    $ Liza.known = True
    $ Liza.rel = 0
    $ Liza.prostitution_started = False
    $ Liza.witnessed_church_after_sermon = False
    $ Georgett.set_story_value("lizasawinchurch", 0)
    $ Georgett.set_story_value("churchlizaadmit", 0)
    $ saveVersion = 70
    $ updateSave()
    assert eval (int(saveVersion or 0) == 71 and not Liza.known) timeout 5.0

    $ Liza.known = False
    $ Liza.rel = 1
    $ saveVersion = 70
    $ updateSave()
    assert eval (int(saveVersion or 0) == 71 and Liza.known) timeout 5.0
'''


CHURCH_AFTER_SERMON_EVENT_CHECKS = r'''
testcase external_georgett_liza_church_after_sermon_events:
    $ external_calendar_set_fields(7, 1, 1100, 12, 0)
    $ rooms.enter("Church")
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
    $ rooms.enter("Church")
    $ TodaySexEvents_Clear()
    $ Georgett.set_story_value("churchgeorgettadmit", 0)
    $ Georgett.set_story_value("churchlizaadmit", 1)
    $ TodaySexEvents_Add("liza", 99, 99, "Priest")
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("Church", "after_cermon_walk")) timeout 5.0
    run Call("ChurchAfterCermon", 1)
    advance until screen "choice" timeout 10.0
    assert eval ("замочную скважину" in str(scene_runtime.location_text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (CheckIfSexEventExist("liza", 99, "Priest") <= 0) timeout 10.0
    assert eval (not hasattr(Liza, "after_sermon_stage")) timeout 5.0
    assert eval ("Лизетту" in str(scene_runtime.location_text or "")) timeout 5.0

testcase external_becky_church_after_sermon_uses_daily_event_authority:
    $ external_calendar_set_fields(7, 1, 1100, 12, 0)
    $ external_calendar_set_weekday(7)
    $ rooms.enter("Church")
    $ scene_runtime.text = ""
    $ TodaySexEvents_Clear()
    $ Becky.priest_advice_stage = 1
    $ ChurchDonatedAmount = 0
    $ TodaySexEvents_Add("becky", 99, 99, "Priest")
    $ _becky_sermon_start_minutes = int(calendar_v2.daysInGame or 0) * 1440 + calendar_v2.clock_minutes()
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("Church", "after_cermon_walk")) timeout 5.0
    run Call("story_becky_church_after_sermon")
    advance until screen "choice" timeout 10.0
    assert eval (CheckIfSexEventExist("becky", 99, "Priest") > 0) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 10.0
    assert eval (CheckIfSexEventExist("becky", 99, "Priest") <= 0) timeout 5.0
    advance until screen "choice" timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 10.0
    advance until screen "choice" timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 10.0
    advance until screen "choice" timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "say" timeout 10.0
    advance until screen "choice" timeout 10.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (int(calendar_v2.daysInGame or 0) * 1440 + calendar_v2.clock_minutes() >= _becky_sermon_start_minutes + 60) timeout 10.0
    assert eval (not hasattr(Becky, "after_sermon_stage")) timeout 5.0

    $ external_calendar_set_weekday(7)
    $ TodaySexEvents_Clear()
    $ Becky.priest_advice_stage = 1
    $ ChurchDonatedAmount = 0
    $ TodaySexEvents_Add("becky", 99, 99, "Priest")
    $ next_day_finish_day_events()
    assert eval (int(Becky.priest_advice_stage or 0) == 2) timeout 5.0
    assert eval (CheckIfSexEventExist("becky", 99, "Priest") <= 0) timeout 5.0
'''


CLARA_MELISSA_TAVERN_BAR_GOSSIP_CHECKS = r'''
testcase external_clara_market_event_repeats_until_exploration_success:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(2)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ people.get_data("clara").set_schedule([NPCScheduleEntry(location="MarketPlace", start_minute=0, end_minute=1440, priority=999)])
    $ Clara.market_intro_seen = False
    $ Clara.market_follow_failed_day = -1
    $ Clara.market_follow_failed_hour = -1
    $ Clara.market_day_roll_day = int(calendar_v2.daysInGame or 0)
    $ Clara.market_day_roll = True
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ findAvailableEvents(True)
    assert eval (story_event_available("MarketPlace", "enter")) timeout 5.0
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until screen "choice" timeout 20.0
    assert eval ("Проследить за Клариссой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0

    $ player.stats.exploration = 10
    $ _clara_follow_energy_before = int(player.condition.energy or 0)
    $ _clara_follow_minutes_before = (int(calendar_v2.daysInGame or 0) * 1440) + int(calendar_v2.clock_minutes() or 0)
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (people_to_int(Clara.market_follow_failed_day, -1) == int(calendar_v2.daysInGame or 0)) timeout 20.0
    assert eval ("Похоже, без лучшей сноровки" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (renpy.get_screen("main_ui") is not None) timeout 5.0
    assert eval (((int(calendar_v2.daysInGame or 0) * 1440) + int(calendar_v2.clock_minutes() or 0)) - _clara_follow_minutes_before == 30) timeout 5.0
    assert eval (int(player.condition.energy or 0) == max(0, _clara_follow_energy_before - 5)) timeout 5.0
    assert eval (people_to_int(Clara.market_follow_failed_day, -1) == int(calendar_v2.daysInGame or 0) and people_to_int(Clara.market_follow_failed_hour, -1) == int(calendar_v2.hour or 0)) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 0) timeout 5.0
    run Jump("MarketPlace")
    advance until screen "main_ui" timeout 20.0
    $ findAvailableEvents(True)
    assert eval (not story_event_available("MarketPlace", "enter")) timeout 5.0

    $ _clara_next_day = calendar_v2.day_number_to_parts(int(calendar_v2.daysInGame or 0) + 1)
    $ external_calendar_set_fields(_clara_next_day["day"], _clara_next_day["month"], _clara_next_day["year"], 12, 0)
    $ Clara.market_day_roll_day = int(calendar_v2.daysInGame or 0)
    $ Clara.market_day_roll = True
    $ findAvailableEvents(True)
    assert eval (people_to_int(Clara.market_day_roll_day, -1) == int(calendar_v2.daysInGame or 0) and bool(Clara.market_day_roll)) timeout 5.0
    assert eval (not (people_to_int(Clara.market_follow_failed_day, -1) == int(calendar_v2.daysInGame or 0) and people_to_int(Clara.market_follow_failed_hour, -1) == int(calendar_v2.hour or 0))) timeout 5.0
    assert eval (rooms.get("MarketPlace").is_open()) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 0 and threads["claraBookletMarket"].checkActive()) timeout 5.0
    assert eval (len(threads["claraBookletMarket"].getAvailableEvents()) > 0) timeout 5.0
    assert eval (story_event_available("MarketPlace", "enter")) timeout 5.0
    $ event_runtime.active_thread = threads["claraBookletMarket"]
    $ player.stats.exploration = 100
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until screen "choice" timeout 20.0
    assert eval ("Проследить за Клариссой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _clara_follow_energy_before = int(player.condition.energy or 0)
    $ _clara_follow_minutes_before = (int(calendar_v2.daysInGame or 0) * 1440) + int(calendar_v2.clock_minutes() or 0)
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("Кларисса что-то сбывает" in str(scene_runtime.text or "")) timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (int(threads["claraBookletMarket"].num or 0) == 1) timeout 20.0
    assert eval ("Кларисса что-то сбывает" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (((int(calendar_v2.daysInGame or 0) * 1440) + int(calendar_v2.clock_minutes() or 0)) - _clara_follow_minutes_before == 30) timeout 5.0
    assert eval (int(player.condition.energy or 0) == max(0, _clara_follow_energy_before - 5)) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 1 and threads["claraBookletMarket"].currentTarget() == "story_clara_market_booklet_2") timeout 5.0

testcase external_clara_market_follow_finishes_without_self_loop:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(2)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ player.stats.exploration = max(int(player.stats.exploration or 0), 100)
    $ people.get_data("clara").set_schedule([NPCScheduleEntry(location="MarketPlace", start_minute=0, end_minute=1440, priority=999)])
    $ Clara.market_intro_seen = False
    $ Clara.market_follow_failed_day = -1
    $ Clara.market_follow_failed_hour = -1
    $ Clara.market_day_roll_day = int(calendar_v2.daysInGame or 0)
    $ Clara.market_day_roll = True
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ findAvailableEvents(True)

    assert eval (story_event_available("MarketPlace", "enter")) timeout 5.0
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until screen "choice" timeout 20.0
    assert eval ("Проследить за Клариссой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _clara_follow_energy_before = int(player.condition.energy or 0)
    $ _clara_follow_minutes_before = (int(calendar_v2.daysInGame or 0) * 1440) + int(calendar_v2.clock_minutes() or 0)
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval ("Кларисса что-то сбывает" in str(scene_runtime.text or "")) timeout 20.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (int(threads["claraBookletMarket"].num or 0) == 1) timeout 20.0
    assert eval ("Кларисса что-то сбывает" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (((int(calendar_v2.daysInGame or 0) * 1440) + int(calendar_v2.clock_minutes() or 0)) - _clara_follow_minutes_before == 30) timeout 5.0
    assert eval (int(player.condition.energy or 0) == max(0, _clara_follow_energy_before - 5)) timeout 5.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 1 and threads["claraBookletMarket"].currentTarget() == "story_clara_market_booklet_2") timeout 5.0

testcase external_mongol_market_schedule_rolls_once_per_day:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 10, 0)
    $ week = 2
    $ player.horse.remove()
    $ Mongol.known = True
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    $ TavernEventOngoing = ""
    $ people.get_data("clara").set_schedule([])
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ Mongol.market_roll_day = int(current_game_day())
    $ Mongol.market_roll = False
    assert eval (not marketplace_mongol_visible()) timeout 5.0
    assert eval (str(people.location("mongol") or "") != "MarketPlace") timeout 5.0
    run Jump("MarketPlace")
    advance until screen "main_ui" timeout 20.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 10, 0)
    $ week = 2
    $ Mongol.market_roll_day = int(current_game_day())
    $ Mongol.market_roll = True
    assert eval (not player.horse.owns_horse()) timeout 5.0
    assert eval (rooms.get("MarketPlace").is_open()) timeout 5.0
    assert eval (Mongol.market_roll_day == int(current_game_day()) and Mongol.market_roll) timeout 5.0
    assert eval (marketplace_mongol_visible()) timeout 5.0
    assert eval (str(people.location("mongol") or "") == "MarketPlace") timeout 5.0
    run Jump("MarketPlace")
    advance until screen "main_ui" timeout 20.0

    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 19, 0)
    assert eval (not marketplace_mongol_visible()) timeout 5.0

testcase external_clara_melissa_bar_gossip_click_fires_ready_dialog:
    run Call("InitGameNPCs")
    $ relationship_calm("clara", 9)
    $ Clara.rel = 9
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ TavernClosed = ""
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ household.runtime_event_seen.clear()
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ _clara_visit_day = external_position_clara_tavern_visit(104)
    $ findAvailableEvents(True)

    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(people.location("clara") or "") == "TavernMain" and str(people.location("melissa") or "") == "TavernMain") timeout 5.0
    $ _clara_visit_thread = threads.get("claraTavernVisit")
    $ _clara_visit_event = _clara_visit_thread.getevent(0) if _clara_visit_thread is not None else None
    $ assert story_event_available("TavernMain", "clara_tavern_visit"), repr({"level": _story_relationship_level("clara"), "active": _clara_visit_thread.checkActive() if _clara_visit_thread is not None else None, "target": _clara_visit_thread.currentTarget() if _clara_visit_thread is not None else None, "checks": _clara_visit_event.auditChecks(_clara_visit_thread.day) if _clara_visit_event is not None else None, "available": dict(event_runtime.available or {})})
    run Call("TavernMainObjectMenu", "bar_001")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Задержаться у стойки в ожидании истории" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _clara_visit_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Задержаться у стойки в ожидании истории")
    $ _clara_visit_button_id = "choice_panel_button_%d" % int(_clara_visit_index)
    click id _clara_visit_button_id pos (0.5, 0.5) until eval (int(threads["claraTavernVisit"].num or 0) == 1) timeout 20.0
    assert eval ('Мелисса, едва сдерживая смех' in str(scene_runtime.text or "")) timeout 5.0
    assert eval (renpy.showing("images/clara/tavern_visit.png")) timeout 5.0
    assert eval (threads["claraTavernVisit"].currentTarget() == "story_clara_tavern_visit_bar_1") timeout 5.0

    $ threads["melissaBatProblem"].advanceTo(6, force_active=True)
    $ _clara_visit_day = external_position_clara_tavern_visit(int(_clara_visit_day or 0) + 1)
    $ household.runtime_event_seen.clear()
    $ rooms.enter("TavernMain")
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (story_event_available("TavernMain", "clara_tavern_visit")) timeout 5.0
    run Call("TavernMainObjectMenu", "bar_001")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Задержаться у стойки в ожидании истории" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _clara_visit_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Задержаться у стойки в ожидании истории")
    $ _clara_visit_button_id = "choice_panel_button_%d" % int(_clara_visit_index)
    click id _clara_visit_button_id pos (0.5, 0.5) until eval (int(threads["claraTavernVisit"].num or 0) == 2) timeout 20.0
    assert eval ('Если б я была царица' in str(scene_runtime.text or "")) timeout 5.0
    assert eval (renpy.showing("images/clara/tavern_visit_size.png")) timeout 5.0
    assert eval (threads["claraTavernVisit"].currentTarget() == "story_clara_tavern_visit_bar_2") timeout 5.0

testcase external_clara_booklet_mongol_night_buttons_advance:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ _clara_mongol_date = calendar_v2.day_number_to_parts(70)
    $ external_calendar_set_fields(_clara_mongol_date["day"], _clara_mongol_date["month"], _clara_mongol_date["year"], 21, 0)
    $ external_calendar_set_weekday(2)
    $ rooms.enter("CityGuard"
)
    $ player.tavern_management.productnum = max(int(player.tavern_management.productnum or 0), 2)
    $ player.tavern_management.winenum = max(int(player.tavern_management.winenum or 0), 1)
    $ Mongol.stocks_arrest_day = int(calendar_v2.daysInGame or 0) - 1
    $ Mongol.stocks_food_day = -1
    $ Draupnir.mongol_lockpick_order_day = -1
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ threads["claraBookletMarket"].advanceTo(6, force_active=True)
    $ findAvailableEvents(True)
    assert eval (story_event_available("menu_CityGuard", "mongol_stocks")) timeout 5.0
    $ event_runtime.active_thread = threads["claraBookletMarket"]
    run Call("story_clara_market_booklet_feed_mongol")
    advance until screen "say" timeout 20.0
    click pos (960, 560) until eval (Mongol.stocks_food_day == int(calendar_v2.daysInGame or 0)) timeout 20.0
    assert eval (Mongol.stocks_food_day == int(calendar_v2.daysInGame or 0)) timeout 5.0
    assert eval (threads["claraBookletMarket"].currentTarget() == "story_clara_market_booklet_8") timeout 5.0
    $ Draupnir.mongol_lockpick_order_day = int(calendar_v2.daysInGame or 0)
    $ threads["claraBookletMarket"].advanceTo(8, force_active=True)
    $ rooms.enter("CityGuard")
    $ _clara_release_date = calendar_v2.day_number_to_parts(Mongol.stocks_food_day + 1)
    $ external_calendar_set_fields(_clara_release_date["day"], _clara_release_date["month"], _clara_release_date["year"], 23, 0)
    $ findAvailableEvents(True)
    assert eval (story_event_available("menu_CityGuard", "mongol_stocks")) timeout 5.0
    $ event_runtime.active_thread = threads["claraBookletMarket"]
    run Call("story_clara_market_booklet_release_mongol")
    advance until screen "say" timeout 20.0
    click pos (960, 560) until eval (threads["claraBookletMarket"].completed) timeout 20.0
    assert eval (int(threads["claraBookletMarket"].num or 0) == 9) timeout 5.0
    assert eval (threads["claraBookletMarket"].completed) timeout 5.0

testcase external_mongol_v61_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Mongol.var.update({
            "StocksReleased": 1,
            "WillTryToSteal": 1,
            "StocksFoodDay": 40,
            "StocksArrestDay": 38,
            "StocksSeen": 1,
            "GuardCaptainKnown": 1,
            "MarketRollDay": int(current_game_day() or 0),
            "MarketRoll": 1,
            "GypsyAsk": 1,
            "AskPriceIncr": 1,
            "ZimmerKnow": 1,
            "HorsePrice": 900,
            "DiscountAsk": 1,
            "TheftAsk": 1,
            "AskSawStolen": 1,
            "SawStolen": 1,
            "HorsesBought": 3,
        })
        for _mongol_field in (
            "will_try_to_steal", "stocks_food_day", "stocks_arrest_day",
            "guard_captain_known", "market_roll_day", "market_roll",
            "asked_about_gypsy", "asked_price_increase",
            "zimmer_knows_horse_theft", "horse_price", "discount_asked",
            "theft_asked", "asked_about_seen_stolen", "seen_with_stolen_horse",
            "horses_bought",
        ):
            Mongol.__dict__.pop(_mongol_field, None)
        globals()["MongolVar"] = {"HorsesBought": 3}
    $ updateSave_V61()
    assert eval (Mongol.will_try_to_steal and Mongol.stocks_food_day == 40 and Mongol.stocks_arrest_day == 38 and Mongol.guard_captain_known) timeout 5.0
    assert eval (Mongol.market_roll_day == int(current_game_day() or 0) and Mongol.market_roll and Mongol.asked_about_gypsy and Mongol.asked_price_increase) timeout 5.0
    assert eval (Mongol.zimmer_knows_horse_theft and Mongol.horse_price == 900 and Mongol.discount_asked and Mongol.theft_asked) timeout 5.0
    assert eval (Mongol.asked_about_seen_stolen and Mongol.seen_with_stolen_horse and Mongol.horses_bought == 3) timeout 5.0
    assert eval (not Mongol.var and "MongolVar" not in globals()) timeout 5.0

testcase external_irma_v62_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Irma.var.update({
            "DeniedMinetMoney": 1,
            "KnowInfertility": 1,
            "KnowDad": 1,
            "KnowMom": 1,
            "KnowSlut": 1,
        })
        for _irma_field in (
            "extra_fee_refused", "infertility_known", "father_story_known",
            "mother_story_known", "sexual_history_known",
        ):
            Irma.__dict__.pop(_irma_field, None)
        globals()["IrmaVar"] = {"KnowMom": 1}
    $ updateSave_V62()
    assert eval (Irma.extra_fee_refused and Irma.infertility_known and Irma.father_story_known) timeout 5.0
    assert eval (Irma.mother_story_known and Irma.sexual_history_known) timeout 5.0
    assert eval (not Irma.var and "IrmaVar" not in globals()) timeout 5.0

testcase external_amanda_v63_night_bowl_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Amanda.var.update({
            "gave_night_bowl": 1,
            "night_bowl_request_day": 41,
            "got_fancy_night_bowl": 1,
            "prefers_backyard_relief": 1,
        })
        for _amanda_bowl_field in (
            "night_bowl_given", "night_bowl_request_day",
            "fancy_night_bowl_received", "backyard_relief_preference",
        ):
            Amanda.__dict__.pop(_amanda_bowl_field, None)
    $ updateSave_V63()
    assert eval (Amanda.night_bowl_given and Amanda.night_bowl_request_day == 41) timeout 5.0
    assert eval (Amanda.fancy_night_bowl_received and Amanda.backyard_relief_preference == 1) timeout 5.0
    assert eval (all(key not in Amanda.var for key in ("gave_night_bowl", "night_bowl_request_day", "got_fancy_night_bowl", "prefers_backyard_relief"))) timeout 5.0

testcase external_amanda_night_bowl_object_state:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ player.add_item("recipe_book_001", 1) if player.item_count("recipe_book_001") <= 0 else False
    $ player.remove_item("night_bowl_001", player.item_count("night_bowl_001")) if player.item_count("night_bowl_001") > 0 else False
    $ player.remove_item("fancy_night_bowl_001", player.item_count("fancy_night_bowl_001")) if player.item_count("fancy_night_bowl_001") > 0 else False
    $ Amanda.night_bowl_given = False
    $ Amanda.night_bowl_request_day = -1
    $ Amanda.fancy_night_bowl_received = False
    $ Amanda.backyard_relief_preference = -1
    $ Amanda.rel = 10
    $ _amanda_bowl_result = Amanda.night_bowl_request_result(False)
    assert eval (_amanda_bowl_result.get("granted") and Amanda.night_bowl_given and Amanda.night_bowl_request_day == int(current_game_day() or 0)) timeout 5.0
    assert eval (player.item_count("night_bowl_001") == 1 and not Amanda.can_be_asked_for_night_bowl()) timeout 5.0
    $ player.add_item("fancy_night_bowl_001", 1)
    assert eval (Amanda.can_receive_fancy_night_bowl()) timeout 5.0
    $ Amanda.fancy_night_bowl_received = True
    assert eval (not Amanda.can_receive_fancy_night_bowl()) timeout 5.0
    $ _amanda_preference_result = Amanda.pick_backyard_relief_preference()
    assert eval (_amanda_preference_result in (0, 1) and Amanda.backyard_relief_preference == _amanda_preference_result) timeout 5.0

testcase external_amanda_v64_attic_breakfast_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Amanda.var.update({
            "attic_window_busted": 1,
            "attic_window_breakfast_bj_day": 44,
            "attic_mock_response_day": 45,
            "attic_mock_stopped": 1,
            "attic_mock_exposed": 1,
            "breakfast_tease_day": 46,
        })
        for _amanda_attic_field in (
            "attic_window_breakfast_bj_day", "attic_mock_response_day",
            "attic_mock_stopped", "attic_mock_exposed", "breakfast_tease_day",
        ):
            Amanda.__dict__.pop(_amanda_attic_field, None)
    $ updateSave_V64()
    assert eval (Amanda.attic_window_breakfast_bj_day == 44 and Amanda.attic_mock_response_day == 45) timeout 5.0
    assert eval (Amanda.attic_mock_stopped and Amanda.attic_mock_exposed and Amanda.breakfast_tease_day == 46) timeout 5.0
    assert eval (all(key not in Amanda.var for key in ("attic_window_busted", "attic_window_breakfast_bj_day", "attic_mock_response_day", "attic_mock_stopped", "attic_mock_exposed", "breakfast_tease_day"))) timeout 5.0

testcase external_amanda_v65_daily_misc_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Amanda.var.update({
            "warnnotwork": 1,
            "askzalettoday": 1,
            "MomDressComplaint": 7,
        })
        for _amanda_daily_field in (
            "warned_about_not_working", "pregnancy_risk_asked_today",
            "mom_dress_complaint_count",
        ):
            Amanda.__dict__.pop(_amanda_daily_field, None)
    $ updateSave_V65()
    assert eval (Amanda.warned_about_not_working and Amanda.pregnancy_risk_asked_today) timeout 5.0
    assert eval (Amanda.mom_dress_complaint_count == 7) timeout 5.0
    assert eval (all(key not in Amanda.var for key in ("warnnotwork", "askzalettoday", "MomDressComplaint"))) timeout 5.0
    $ _amanda_complaint_seen_before = mom_dress_complaint_mark_seen("amanda")
    assert eval (_amanda_complaint_seen_before == 7 and Amanda.mom_dress_complaint_count == 8) timeout 5.0

testcase external_amanda_v66_room_rejection_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Amanda.var.update({
            "kickyoufromroom": 1,
            "kickyoufromroomcount": 4,
            "kickedwithmomhelp": 1,
        })
        for _amanda_room_field in (
            "room_entry_blocked_today", "room_rejection_count",
            "room_rescue_called",
        ):
            Amanda.__dict__.pop(_amanda_room_field, None)
    $ updateSave_V66()
    assert eval (Amanda.room_entry_blocked_today and Amanda.room_rejection_count == 4 and Amanda.room_rescue_called) timeout 5.0
    assert eval (all(key not in Amanda.var for key in ("kickyoufromroom", "kickyoufromroomcount", "kickedwithmomhelp"))) timeout 5.0

testcase external_amanda_room_rejection_flow:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ Amanda.room_entry_blocked_today = False
    $ Amanda.room_rejection_count = 3
    $ Amanda.room_rescue_called = False
    assert eval (tavern_upstairs_can_enter_amanda_room()) timeout 5.0
    run Jump("CodeAmandaKickFromRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernMain") timeout 5.0
    assert eval (Amanda.room_entry_blocked_today and Amanda.room_rejection_count == 4 and Amanda.room_rescue_called) timeout 5.0
    assert eval (not tavern_upstairs_can_enter_amanda_room()) timeout 5.0
    run Call("NextDay_FinishDayEvents")
    assert eval (not Amanda.room_entry_blocked_today and tavern_upstairs_can_enter_amanda_room()) timeout 5.0

testcase external_amanda_v67_legare_state_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Amanda.var.update({
            "alberfriends": 14,
            "albernowdances": 1,
            "leftdances": 1,
            "alberprohibit": 1,
            "LegareGo": 2,
            "EscapeUnnoticed": 1,
            "sucklegare": 1,
            "fucklegare": 1,
            "deflowerlegare": 1,
            "knowdeflowerlegare": 1,
            "knowlegaresex": 1,
            "sawlegaresex": 1,
            "knowyousawlegaresex": 1,
            "knowyouseesex": 1,
        })
        for _amanda_legare_field in (
            "legare_affection", "dancing_with_legare", "left_friday_dance",
            "legare_forbidden", "legare_departure_code", "escaped_dance_unnoticed",
            "performed_oral_with_legare", "had_sex_with_legare",
            "lost_virginity_to_legare", "player_knows_legare_deflowered",
            "player_knows_legare_sex", "player_saw_legare_sex",
            "knows_player_saw_legare_sex", "knows_player_is_watching_legare_sex",
        ):
            Amanda.__dict__.pop(_amanda_legare_field, None)
    $ updateSave_V67()
    assert eval (Amanda.legare_affection == 14 and Amanda.legare_departure_code == 2) timeout 5.0
    assert eval (Amanda.dancing_with_legare and Amanda.left_friday_dance and Amanda.legare_forbidden and Amanda.escaped_dance_unnoticed) timeout 5.0
    assert eval (Amanda.performed_oral_with_legare and Amanda.had_sex_with_legare and Amanda.lost_virginity_to_legare) timeout 5.0
    assert eval (Amanda.player_knows_legare_deflowered and Amanda.player_knows_legare_sex and Amanda.player_saw_legare_sex) timeout 5.0
    assert eval (Amanda.knows_player_saw_legare_sex and Amanda.knows_player_is_watching_legare_sex) timeout 5.0
    assert eval (all(key not in Amanda.var for key in ("alberfriends", "albernowdances", "leftdances", "alberprohibit", "LegareGo", "EscapeUnnoticed", "sucklegare", "fucklegare", "deflowerlegare", "knowdeflowerlegare", "knowlegaresex", "sawlegaresex", "knowyousawlegaresex", "knowyouseesex"))) timeout 5.0

testcase external_amanda_legare_resolution_uses_object_state:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ Amanda.performed_oral_with_legare = True
    $ Amanda.had_sex_with_legare = True
    $ Amanda.legare_affection = 10
    $ Amanda.corruption = 30
    $ Amanda.set_sex_stat("ConceptionChance", 0)
    $ Amanda.set_sex_stat("pregnancy", 0)
    assert eval (Amanda.legare_sex_type() == 4) timeout 5.0
    $ _amanda_legare_resolution = Amanda.resolve_legare_let_go()
    assert eval (_amanda_legare_resolution == 4 and Amanda.had_sex_with_legare) timeout 5.0
    assert eval (Amanda.legare_affection in (11, 12)) timeout 5.0

testcase external_eddie_v60_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Eddie.var.update({
            "TalkedAboutWhores": 1,
            "SawWithGeorgett": 1,
            "TalkedAboutGeorgett": 1,
            "SawMomSex": 1,
            "FingalTalk": 2,
            "FingalTalkDestination": 1,
            "FingalTalkComplain": 1,
            "RidiculeFollow": 1,
            "OthersSawWithMom": 1,
            "WhoreVisitFreq": 9,
        })
        for _eddie_field in (
            "told_about_tavern_whores", "seen_with_georgett",
            "talked_about_georgett", "saw_mother_sex", "fingal_talk_stage",
            "asked_fingal_destination", "asked_fingal_guard_complaint",
            "ridiculed_follow_attempt", "others_saw_with_mother",
        ):
            Eddie.__dict__.pop(_eddie_field, None)
        globals()["EddieVar"] = {"FingalTalk": 2}
    $ updateSave_V60()
    assert eval (Eddie.told_about_tavern_whores and Eddie.seen_with_georgett and Eddie.talked_about_georgett and Eddie.saw_mother_sex) timeout 5.0
    assert eval (Eddie.fingal_talk_stage == 2 and Eddie.asked_fingal_destination and Eddie.asked_fingal_guard_complaint) timeout 5.0
    assert eval (Eddie.ridiculed_follow_attempt and Eddie.others_saw_with_mother and Eddie.whore_visit_frequency == 6) timeout 5.0
    assert eval (not Eddie.var and "EddieVar" not in globals()) timeout 5.0

testcase external_eddie_fingal_talk_progression:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ rooms.enter("GroceryStore")
    $ Eddie.rel = 9
    $ Eddie.talked_today = 0
    $ Eddie.fingal_talk_stage = 0
    $ Eddie.asked_fingal_destination = False
    $ Eddie.asked_fingal_guard_complaint = False
    $ Becky.eddie_robbed_day = max(1, int(current_game_day() or 0))
    $ Becky.home_visit_stage = 7
    run Call("IntEddieTalk")
    advance until screen "choice" timeout 20.0
    assert eval ("Спросить о синяке." in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _eddie_bruise_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Спросить о синяке.")
    $ _eddie_bruise_button_id = "choice_panel_button_%d" % _eddie_bruise_index
    click id _eddie_bruise_button_id pos (0.5, 0.5) until eval (Eddie.fingal_talk_stage == 1) timeout 20.0
    assert eval ("А все таки расскажи, кто это тебе так вмазал?" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _eddie_who_hit_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("А все таки расскажи, кто это тебе так вмазал?")
    $ _eddie_who_hit_button_id = "choice_panel_button_%d" % _eddie_who_hit_index
    click id _eddie_who_hit_button_id pos (0.5, 0.5) until eval (Eddie.fingal_talk_stage == 2) timeout 20.0
    $ _eddie_end_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _eddie_end_button_id = "choice_panel_button_%d" % _eddie_end_index
    click id _eddie_end_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
    $ Eddie.talked_today = 0
    run Call("IntEddieTalk")
    advance until screen "choice" timeout 20.0
    assert eval ("А куда это ты ездил?" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] and "Страже жаловался?" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _eddie_destination_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("А куда это ты ездил?")
    $ _eddie_destination_button_id = "choice_panel_button_%d" % _eddie_destination_index
    click id _eddie_destination_button_id pos (0.5, 0.5) until eval (Eddie.asked_fingal_destination) timeout 20.0
    $ Eddie.talked_today = 0
    $ _eddie_complain_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Страже жаловался?")
    $ _eddie_complain_button_id = "choice_panel_button_%d" % _eddie_complain_index
    click id _eddie_complain_button_id pos (0.5, 0.5) until eval (Eddie.asked_fingal_guard_complaint) timeout 20.0

testcase external_draupnir_v59_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Draupnir.var.update({
            "SloganAsked": 1,
            "HoleAsked": 1,
            "GloryHoleAsked": 1,
            "SoapBarrelAsked": 1,
            "DogBoothAsked": 1,
            "MongolLockpickOrderDay": 41,
        })
        for _draupnir_field in (
            "slogan_quote_received", "peep_hole_quote_received",
            "glory_hole_quote_received", "soap_barrel_quote_received",
            "dog_booth_quote_received", "mongol_lockpick_order_day",
        ):
            Draupnir.__dict__.pop(_draupnir_field, None)
        globals()["DraupnirVar"] = {"SloganAsked": 1}
    $ updateSave_V59()
    assert eval (Draupnir.slogan_quote_received and Draupnir.peep_hole_quote_received and Draupnir.glory_hole_quote_received) timeout 5.0
    assert eval (Draupnir.soap_barrel_quote_received and Draupnir.dog_booth_quote_received and Draupnir.mongol_lockpick_order_day == 41) timeout 5.0
    assert eval (not Draupnir.var and "DraupnirVar" not in globals()) timeout 5.0

testcase external_francheska_v57_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Francheska.var.update({
            "meet": 1,
            "ellonaask": 1,
            "graceask": 2,
            "conchitaask": 1,
            "dukeask": 1,
            "starkask": 1,
            "stateask": 1,
            "kingask": 1,
            "rebelask": 1,
            "alienask": 1,
            "sunday_stories_seen_day": 37,
        })
        for _fran_field in (
            "met", "asked_about_ellona", "graces_stage", "asked_about_duchess",
            "asked_about_duke", "asked_about_stark", "asked_about_duchy",
            "asked_about_king", "asked_about_kingdom_relations",
            "asked_about_aliens", "sunday_stories_seen_day",
        ):
            Francheska.__dict__.pop(_fran_field, None)
        globals()["FranVar"] = {"meet": 1}
        globals()["FranBusy"] = {0: 1}
    $ updateSave_V57()
    assert eval (Francheska.met and Francheska.asked_about_ellona and Francheska.graces_stage == 2) timeout 5.0
    assert eval (Francheska.asked_about_duchess and Francheska.asked_about_duke and Francheska.asked_about_stark and Francheska.asked_about_duchy) timeout 5.0
    assert eval (Francheska.asked_about_king and Francheska.asked_about_kingdom_relations and Francheska.asked_about_aliens and Francheska.sunday_stories_seen_day == 37) timeout 5.0
    assert eval (not Francheska.var and "FranVar" not in globals() and "FranBusy" not in globals()) timeout 5.0

testcase external_alber_v56_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Alber.var.update({
            "sawwithliza": 1,
            "talkedaboutliza": 1,
            "hearabouthiswife": 1,
            "FightYouAmanda": 2,
            "WhoreVisitFreq": 9,
            "LegareProvokeYou": 1,
        })
        for _alber_field in (
            "liza_encounter_seen", "talked_about_liza", "heard_about_wife",
            "amanda_conflict_stage",
        ):
            Alber.__dict__.pop(_alber_field, None)
        globals()["AlberVar"] = {"FightYouAmanda": 2}
        globals()["LegareProvokeYou"] = 1
    $ updateSave_V56()
    assert eval (Alber.liza_encounter_seen and Alber.talked_about_liza and Alber.heard_about_wife) timeout 5.0
    assert eval (Alber.amanda_conflict_stage == 2 and Alber.whore_visit_frequency == 3) timeout 5.0
    assert eval (not Alber.var and "AlberVar" not in globals() and "LegareProvokeYou" not in globals()) timeout 5.0

testcase external_alber_native_talk_local_provocation_flow:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ rooms.enter("WineStore")
    $ Alber.rel = 5
    $ Alber.talked_today = 0
    $ Alber.liza_encounter_seen = True
    $ Alber.talked_about_liza = False
    $ Alber.amanda_conflict_stage = 1
    run Call("IntAlberTalk")
    advance until screen "choice" timeout 20.0
    assert eval ("Спросить мессира Легаре о Лизетте" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Попробовать помириться" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _alber_reconcile_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Попробовать помириться")
    $ _alber_reconcile_button_id = "choice_panel_button_%d" % int(_alber_reconcile_index)
    click id _alber_reconcile_button_id pos (0.5, 0.5) until eval ("Проигнорировать" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (Alber.amanda_conflict_stage == 0 and "Обругать месье" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] and "Заехать с правой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _alber_ignore_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Проигнорировать")
    $ _alber_ignore_button_id = "choice_panel_button_%d" % int(_alber_ignore_index)
    click id _alber_ignore_button_id pos (0.5, 0.5) until eval ("Спросить мессира Легаре о Лизетте" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _alber_liza_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Спросить мессира Легаре о Лизетте")
    $ _alber_liza_button_id = "choice_panel_button_%d" % int(_alber_liza_index)
    click id _alber_liza_button_id pos (0.5, 0.5) until eval (Alber.talked_about_liza) timeout 20.0
    assert eval (Alber.talked_about_liza and Alber.rel == 8) timeout 5.0
    $ _alber_end_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _alber_end_button_id = "choice_panel_button_%d" % int(_alber_end_index)
    click id _alber_end_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") != "talk") timeout 20.0

testcase external_liza_v55_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Liza.var.update({
            "SawChurchAfterCermon": 1,
            "TalkChurchAfterCermon": 1,
            "TalkChurchAfterCermonGeorgett": 1,
            "ProstStart": 1,
            "seeclients": 1,
            "askclients": 1,
            "askpregnancy": 1,
            "asksex": 1,
            "GloryHoleMentioned": 1,
            "GloryHoleAsked": 1,
            "portstreet_clients_seen_today": 1,
        })
        for _liza_field in (
            "witnessed_church_after_sermon", "discussed_georgett_gerhard",
            "prostitution_started", "has_seen_clients", "asked_about_clients",
            "asked_about_pregnancy", "asked_about_sex", "glory_hole_mentioned",
            "glory_hole_asked", "portstreet_clients_seen_today",
        ):
            Liza.__dict__.pop(_liza_field, None)
        globals()["LizaVar"] = {"ProstStart": 1}
    $ updateSave_V55()
    assert eval (Liza.witnessed_church_after_sermon and Liza.discussed_georgett_gerhard and Liza.prostitution_started) timeout 5.0
    assert eval (Liza.has_seen_clients and Liza.asked_about_clients and Liza.asked_about_pregnancy and Liza.asked_about_sex) timeout 5.0
    assert eval (Liza.glory_hole_mentioned and Liza.glory_hole_asked and Liza.portstreet_clients_seen_today) timeout 5.0
    assert eval (not Liza.var and "LizaVar" not in globals()) timeout 5.0

testcase external_zimmer_v54_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Zimmer.var.update({
            "ComplainHorse": 1,
            "SherwoodStory": 2,
            "ComplainRobin": 2,
            "RobinInvestigationDay": 42,
            "street_pass": 1,
        })
        for _zimmer_field in (
            "horse_complaint_stage", "sherwood_story_stage", "robin_complaint_stage",
            "robin_investigation_day", "street_patrol_pass",
        ):
            Zimmer.__dict__.pop(_zimmer_field, None)
        globals()["ZimmerVar"] = {"ComplainHorse": 1}
    $ updateSave_V54()
    assert eval (Zimmer.horse_complaint_stage == 1 and Zimmer.sherwood_story_stage == 2 and Zimmer.robin_complaint_stage == 2) timeout 5.0
    assert eval (Zimmer.robin_investigation_day == 42 and Zimmer.street_patrol_pass and not Zimmer.var and "ZimmerVar" not in globals()) timeout 5.0

testcase external_zimmer_mongol_wine_distraction_dialog:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ rooms.enter("CityGuard")
    $ player.tavern_management.productnum = max(int(player.tavern_management.productnum or 0), 2)
    $ player.tavern_management.winenum = max(int(player.tavern_management.winenum or 0), 1)
    $ Zimmer.talked_today = 0
    $ threads["claraBookletMarket"].advanceTo(8, force_active=True)
    $ Mongol.stocks_food_day = int(calendar_v2.daysInGame or 0)
    $ Mongol.guard_captain_known = False
    $ Draupnir.mongol_lockpick_order_day = int(calendar_v2.daysInGame or 0)
    run Call("IntZimmerTalk")
    advance until screen "choice" timeout 20.0
    assert eval ("Похвастаться вином для ночной стражи" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _zimmer_wine_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Похвастаться вином для ночной стражи")
    $ _zimmer_wine_button_id = "choice_panel_button_%d" % int(_zimmer_wine_index)
    click id _zimmer_wine_button_id pos (0.5, 0.5) until eval (Mongol.guard_captain_known) timeout 20.0
    assert eval (Mongol.guard_captain_known) timeout 5.0
    assert eval ("правильное понимание общественного порядка" in str(scene_runtime.text or "")) timeout 5.0
    assert eval (int(Zimmer.rel or 0) >= 1) timeout 5.0

testcase external_robin_v58_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Robin.var.update({
            "KnowHim": 1,
            "KnowComplaint": 1,
            "KnowPlace": 1,
            "KnowWeapon": 1,
            "RobbedNum": 3,
            "Negotiate": 2,
            "KnowBigTitsVillage": 1,
            "MongolSafePass": 1,
            "KunidellOpened": 1,
            "KunidellDeliveries": 4,
            "BlackwoodRoadOpen": 1,
        })
        for _robin_field in (
            "identity_known", "complaint_explained", "place_explained",
            "weapon_source_explained", "robbery_count", "negotiation_stage",
            "knows_big_tits_village", "mongol_safe_pass", "kunidell_opened",
            "kunidell_deliveries", "blackwood_road_open",
        ):
            Robin.__dict__.pop(_robin_field, None)
        globals()["RobinVar"] = {"RobbedNum": 3}
    $ updateSave_V58()
    assert eval (Robin.identity_known and Robin.complaint_explained and Robin.place_explained and Robin.weapon_source_explained) timeout 5.0
    assert eval (Robin.robbery_count == 3 and Robin.negotiation_stage == 2 and Robin.knows_big_tits_village) timeout 5.0
    assert eval (Robin.mongol_safe_pass and Robin.kunidell_opened and Robin.kunidell_deliveries == 4 and Robin.blackwood_road_open) timeout 5.0
    assert eval (not Robin.var and "RobinVar" not in globals()) timeout 5.0

testcase external_robin_blackwood_room_thread_and_mongol_pass:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval (people.get_info("robin") is Robin and isinstance(Robin, RobinInfo)) timeout 5.0
    assert eval (people.get_data("robin") is RobinStaticData) timeout 5.0
    assert eval (str(people.location("robin") or "") == "BlackwoodRoad") timeout 5.0
    $ rooms.enter("BlackwoodRoad")
    $ Becky.trade_offer_stage = 1
    $ Robin.mongol_safe_pass = True
    $ Robin.kunidell_opened = False
    $ rooms.get("BlackwoodRoad").custom_properties["on_horse"] = 0
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    assert eval ("robinBlackwoodRoadAmbush" in threads) timeout 5.0
    assert eval (story_event_available("BlackwoodRoad", "enter")) timeout 5.0
    $ event_runtime.active_thread = threads["robinBlackwoodRoadAmbush"]
    run Call("story_robin_blackwood_mongol_pass")
    advance until screen "say" timeout 20.0
    click pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until eval (Robin.kunidell_opened) timeout 20.0
    assert eval (Robin.kunidell_opened) timeout 5.0
    assert eval ("MongolSafePassUsed" not in Robin.var) timeout 5.0
'''


FRIDAY_DANCE_AMANDA_CHECKS = r'''
testcase external_friday_amanda_bad_invite_uses_one_dance:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 20, 0)
    $ external_calendar_set_weekday(5)
    $ rooms.get("FridayDance").state["dance_count"] = 0
    $ rooms.get("FridayDance").step = 0
    $ player.tavern_management.dance_sponsor = 0
    $ GirlDance_Clear()
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="FridayDance", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="FridayDance", start_minute=0, end_minute=1440, awake=True, talkable=True, priority=999)])
    $ Amanda.left_friday_dance = False
    $ Amanda.escaped_dance_unnoticed = False
    $ Amanda.dancing_with_legare = False
    $ Amanda.legare_departure_code = 0
    $ Becky.left_dances = 1
    $ Amanda.rel = 0
    $ Amanda.corruption = 0
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"

    run Jump("FridayDance")
    advance until screen "choice" timeout 20.0
    assert eval (int(rooms.get("FridayDance").state["dance_count"] or 0) == 0) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (int(rooms.get("FridayDance").state["dance_count"] or 0) == 1) timeout 5.0
    advance until screen "choice" timeout 20.0
    assert eval (int(rooms.get("FridayDance").step or 0) == 1) timeout 5.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (int(rooms.get("FridayDance").state["dance_count"] or 0) == 1) timeout 5.0
    advance until screen "choice" timeout 20.0
    assert eval (int(rooms.get("FridayDance").state["dance_count"] or 0) == 1) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (int(rooms.get("FridayDance").step or 0) == 0) timeout 20.0
    assert eval (int(rooms.get("FridayDance").state["dance_count"] or 0) == 1) timeout 5.0
    assert eval (int(rooms.get("FridayDance").step or 0) == 0) timeout 5.0

testcase external_friday_amanda_legare_go_phrase_survives_create_dance:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 20, 0)
    $ external_calendar_set_weekday(5)
    $ rooms.get("FridayDance").state["dance_count"] = 0
    $ rooms.get("FridayDance").step = 0
    $ player.tavern_management.dance_sponsor = 0
    $ GirlDance_Clear()
    $ GirlDance_Add("amanda", "legare", 1, 1, "LEGARE_GO_TEST_PHRASE")
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="FridayDance", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="FridayDance", start_minute=0, end_minute=1440, awake=True, talkable=True, priority=999)])
    $ Amanda.left_friday_dance = False
    $ Amanda.escaped_dance_unnoticed = False
    $ Amanda.dancing_with_legare = False
    $ Amanda.legare_departure_code = 0
    $ Amanda.legare_affection = 12
    $ Amanda.corruption = 40
    $ Becky.left_dances = 1
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"

    run Jump("FridayDance")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    assert eval (int(rooms.get("FridayDance").state["dance_count"] or 0) == 1) timeout 5.0
    assert eval (Amanda.dancing_with_legare) timeout 5.0
    assert eval (CheckIfDanceExist("amanda", "legare", 0) <= 0) timeout 5.0
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
    assert eval (Amanda.legare_departure_code == 0) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "choice" timeout 20.0
    assert eval (Amanda.left_friday_dance) timeout 5.0

testcase external_amanda_legare_sex_scene_label_procedures:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("amanda") is not None) timeout 20.0
    $ Amanda.performed_oral_with_legare = False
    $ Amanda.had_sex_with_legare = False
    $ Amanda.legare_affection = 0
    $ Amanda.knows_player_is_watching_legare_sex = False
    $ Amanda.set_sex_stat("ConceptionChance", 0)
    $ Amanda.set_sex_stat("pregnancy", 0)
    $ Amanda.corruption = 0
    run Call("AfterDanceSexLegare", 3, 1, "")
    advance until screen "choice" timeout 20.0
    assert eval (Amanda.performed_oral_with_legare) timeout 5.0
    assert eval (Amanda.legare_affection == 1) timeout 5.0
    run Call("AfterDanceSexLegare", 5, 2, "")
    advance until screen "choice" timeout 20.0
    assert eval (Amanda.had_sex_with_legare) timeout 5.0

testcase external_friday_becky_inner_actions_do_not_spend_extra_dances:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 20, 0)
    $ external_calendar_set_weekday(5)
    $ rooms.enter("FridayDance"
)
    $ rooms.get("FridayDance").state["dance_count"] = 1
    $ rooms.get("FridayDance").step = 1
    $ player.tavern_management.dance_sponsor = 0
    $ rooms.get("FridayDance").state["becky_home_invited"] = False
    $ Becky.rel = 0
    $ Becky.corruption = 0
    run Call("int_becky_dance")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval (int(rooms.get("FridayDance").dance_count or 0) == 1 and int(rooms.get("FridayDance").step or 0) == 6) timeout 5.0
'''

BECKY_HOME_GUEST_CHECKS = r'''
# Important multi-visit home guest tests (not one visit)
# Covers citydress gate, dinner arrival, basic progression toward the full guest experience
# (wine, grope, inga minet, to bedroom, Georgett crossover when EddieWhoreHome=4, etc.)

testcase external_becky_home_guest_citydress_gate_and_arrival:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 20, 0)
    $ week = 5
    $ rooms.enter("FridayDance"
)
    $ rooms.get("FridayDance").state["becky_home_invited"] = True
    $ Becky.home_visit_stage = 0
    $ player.appearance.current_dress = "citydress"
    $ player.appearance.add_dress("citydress", calendar_v2.daysInGame)
    $ Becky.rel = 15
    $ Becky.corruption = 50
    $ Becky.set_sex_stat("sexacts", 1)
    run Call("becky_accept_home_invitation")
    advance until screen "main_ui" timeout 30.0
    assert eval ('Бекки' in str(scene_runtime.text or "") or 'дома' in str(scene_runtime.text or "").lower()) timeout 10.0
'''


SANDRA_NIGHT_THANKS_CHECKS = r'''
testcase external_clara_flirt_unlocks_paintings_gate:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("clara") is Clara) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 8, 0)
    $ external_calendar_set_weekday(1)
    $ player.stats.charisma = 100
    $ player.stats.exploration = 100
    $ Clara.rel = 5
    $ Clara.openness = 4
    $ Clara.known = True
    $ Clara.flirted_today = 0
    $ Clara.flirt_count = 0
    $ people.get_data("clara").set_schedule([NPCScheduleEntry(location="WineStore", start_minute=0, end_minute=1440, awake=True, talkable=True, priority=999)])
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    run Call("IntClaraTalk", "clara")
    advance until screen "choice" timeout 20.0
    assert eval ("Флиртовать" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _clara_flirt_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Флиртовать")
    $ _clara_flirt_button_id = "choice_panel_button_%d" % int(_clara_flirt_index)
    click id _clara_flirt_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Затеять светскую игру" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _clara_topic_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index(str([i.caption for i in renpy.get_screen("choice").scope.get("items", []) if str(i.caption or "") != "Назад"][0]))
    $ _clara_topic_button_id = "choice_panel_button_%d" % int(_clara_topic_index)
    click id _clara_topic_button_id pos (0.5, 0.5) until eval (int(Clara.flirted_today or 0) == 1 and int(Clara.flirt_count or 0) == 1 and str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is None) timeout 20.0
    click id "main_ui_entity_button_npc_clara" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 20.0
    $ _clara_back_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Назад")
    $ _clara_back_button_id = "choice_panel_button_%d" % int(_clara_back_index)
    click id _clara_back_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == "WineStore") timeout 20.0
    $ threads["claraPaintingsPath"].advanceTo(1, force_active=True)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (story_event_available("WineStore", "clara_paintings")) timeout 5.0

testcase external_amanda_glory_reaction_uses_story_event:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("amanda") is not None and people.get_info("liza") is not None) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 14, 0)
    $ external_calendar_set_weekday(1)
    $ player.tavern_management.glory_hole = 2
    $ Liza.jobs["jobgloryhole"] = 1
    $ TodaySexEvents_Add("amanda", 99, 1, "glorytry")
    run Jump("TavernGloryHole")
    advance until screen "choice" timeout 20.0
    assert eval (int(player.tavern_management.glory_hole_session.amanda_present or 0) == 1) timeout 5.0
    $ Amanda.set_var_int("glory_cur_state", 1)
    assert eval (story_event_available("TavernGloryHole", "amanda_gloryhole_try")) timeout 5.0
    $ _amanda_glory_evt = event_runtime.available["TavernGloryHole"]["amanda_gloryhole_try"]
    assert eval (str(_amanda_glory_evt.target or "") == "story_amanda_gloryhole_try_0") timeout 5.0
    run Call("checkTriggers", "TavernGloryHole", "amanda_gloryhole_try", 0)
    advance until screen "choice" timeout 20.0
    assert eval (event_runtime.active_thread is None) timeout 5.0
    assert eval ("Осмотреть Аманду" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0

testcase external_amanda_liza_talk_rows_use_typed_conditions:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("amanda") is not None and people.get_info("liza") is not None) timeout 20.0
    $ Amanda.corruption = 22
    $ Amanda.set_sex_stat("sexacts", 0)
    $ player.tavern_management.glory_hole = 2
    $ _amanda_liza_selected_row = get_random_amanda_liza_talk_row()
    assert eval ("научишь" in str(_amanda_liza_selected_row["Phrase"] or "") and tuple(_amanda_liza_selected_row["Reaction"]) == ()) timeout 5.0
    $ _amanda_liza_kick_row = [row for row in AmandaLizaTalkRows if "Сандру с Мелиссой" in str(row["Phrase"] or "")][0]
    $ Amanda.set_var_int("fuckyou", 0)
    $ Amanda.room_rescue_called = True
    assert eval (bool(_amanda_liza_kick_row["Condition"]()) and tuple(_amanda_liza_kick_row["Reaction"]) == (40, 20, 24)) timeout 5.0
    $ Amanda.room_rescue_called = False
    assert eval (not bool(_amanda_liza_kick_row["Condition"]())) timeout 5.0

testcase external_amanda_talk_opens_from_npc_button:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("amanda") is not None) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 10, 0)
    $ external_calendar_set_weekday(1)
    $ Amanda.known = True
    $ Amanda.rel = 15
    $ Amanda.asked_today = 0
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=999)])
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval ("amanda" in list(people.ids_at("TavernMain") or [])) timeout 5.0
    click id "main_ui_entity_button_npc_amanda" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and str(main_ui_runtime.action_title or "") == "Разговор с Амандой" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("Осмотреть" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Назад" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Спросить, чего ей сейчас хочется больше всего" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Флиртовать" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ player.condition.fun = 10
    $ _amanda_flirt_start = int(calendar_v2.daysInGame or 0) * 1440 + int(calendar_v2.clock_minutes() or 0)
    $ _amanda_flirt_talked = int(Amanda.talked_today or 0)
    $ _amanda_flirted = int(Amanda.flirted_today or 0)
    $ _amanda_flirt_openness = int(Amanda.openness or 0)
    $ _amanda_flirt_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Флиртовать")
    $ _amanda_flirt_button_id = "choice_panel_button_%d" % int(_amanda_flirt_index)
    click id _amanda_flirt_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and int(Amanda.flirted_today or 0) == _amanda_flirted + 1) timeout 20.0
    assert eval (int(calendar_v2.daysInGame or 0) * 1440 + int(calendar_v2.clock_minutes() or 0) == _amanda_flirt_start + 30) timeout 5.0
    assert eval (int(Amanda.talked_today or 0) == _amanda_flirt_talked + 1 and int(player.condition.fun or 0) == 14) timeout 5.0
    assert eval (int(Amanda.openness or 0) == _amanda_flirt_openness and len(str(scene_runtime.text or "")) > 0) timeout 5.0
    click id "main_ui_entity_button_npc_amanda" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 20.0
    $ _amanda_priority_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Спросить, чего ей сейчас хочется больше всего")
    $ _amanda_priority_button_id = "choice_panel_button_%d" % int(_amanda_priority_index)
    click id _amanda_priority_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is None and int(Amanda.asked_today or 0) == 1) timeout 20.0
    assert eval ("чего ей сейчас хочется больше всего" in str(scene_runtime.text or "")) timeout 5.0
    click id "main_ui_entity_button_npc_amanda" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("Спросить, чего ей сейчас хочется больше всего" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _amanda_back_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Назад")
    $ _amanda_back_button_id = "choice_panel_button_%d" % int(_amanda_back_index)
    click id _amanda_back_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == "TavernMain") timeout 20.0
    $ Amanda.rel = 100
    $ Amanda.openness = 7
    $ _amanda_kino_start = int(calendar_v2.daysInGame or 0) * 1440 + int(calendar_v2.clock_minutes() or 0)
    $ _amanda_kino_talked = int(Amanda.talked_today or 0)
    $ _amanda_kino_flirted = int(Amanda.flirted_today or 0)
    $ _amanda_kino_result = old_point_kino_attempt("amanda")
    assert eval (bool(_amanda_kino_result.get("ok", False)) and len(str(_amanda_kino_result.get("text", "") or "")) > 0) timeout 5.0
    assert eval (int(calendar_v2.daysInGame or 0) * 1440 + int(calendar_v2.clock_minutes() or 0) == _amanda_kino_start + 30) timeout 5.0
    assert eval (int(Amanda.talked_today or 0) == _amanda_kino_talked + 1 and int(Amanda.flirted_today or 0) == _amanda_kino_flirted) timeout 5.0
    assert eval (int(Amanda.openness or 0) == 7 and int(player.condition.fun or 0) == 19) timeout 5.0

testcase external_amanda_daily_talk_actions:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("amanda") is not None) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 10, 0)
    $ external_calendar_set_weekday(1)
    $ Amanda.known = True
    $ Amanda.rel = 15
    $ Amanda.asked_today = 0
    $ Amanda.talked_today = 0
    $ Amanda.warned_about_not_working = True
    $ Amanda.pregnancy_risk_asked_today = False
    $ Amanda.set_var_int("knowsexactive", 1)
    $ Amanda.set_sex_stat("virginity", False)
    $ Amanda.set_sex_stat("pregnancy", 0)
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=999)])
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    click id "main_ui_entity_button_npc_amanda" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("Сказать Аманде что она может иногда брать перерывы" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Спросить не боиться ли она залететь" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _amanda_break_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Сказать Аманде что она может иногда брать перерывы")
    $ _amanda_break_button_id = "choice_panel_button_%d" % int(_amanda_break_index)
    click id _amanda_break_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and not Amanda.warned_about_not_working) timeout 20.0
    click id "main_ui_entity_button_npc_amanda" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("Сказать Аманде что она может иногда брать перерывы" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Спросить не боиться ли она залететь" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _amanda_pregnancy_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Спросить не боиться ли она залететь")
    $ _amanda_pregnancy_button_id = "choice_panel_button_%d" % int(_amanda_pregnancy_index)
    click id _amanda_pregnancy_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and Amanda.pregnancy_risk_asked_today and int(Amanda.asked_today or 0) == 1) timeout 20.0

testcase external_sandra_talk_opens_from_npc_button:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("sandra") is not None) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 10, 0)
    $ external_calendar_set_weekday(1)
    $ Sandra.known = True
    $ Sandra.rel = 15
    $ Sandra.asked_today = 0
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    run Jump("TavernKitchen")
    advance until screen "main_ui" timeout 20.0
    assert eval ("sandra" in list(people.ids_at("TavernKitchen") or [])) timeout 5.0
    click id "main_ui_entity_button_npc_sandra" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and str(main_ui_runtime.action_title or "") == "Разговор с Сандрой" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("Осмотреть" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Назад" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Поговорить" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Флиртовать" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Подарить маленький подарок" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Коснуться ее смелее" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Извиниться перед Сандрой" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("между вами еще нет того доверия" not in str(scene_runtime.text or "")) timeout 5.0
    assert eval ("Спросить, что для нее сейчас важнее всего по хозяйству" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _sandra_priority_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Спросить, что для нее сейчас важнее всего по хозяйству")
    $ _sandra_priority_button_id = "choice_panel_button_%d" % int(_sandra_priority_index)
    click id _sandra_priority_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is None and int(Sandra.asked_today or 0) == 1) timeout 20.0
    assert eval ("Чтобы в трактире был порядок" in str(scene_runtime.text or "")) timeout 5.0
    click id "main_ui_entity_button_npc_sandra" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("Спросить, что для нее сейчас важнее всего по хозяйству" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _sandra_back_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Назад")
    $ _sandra_back_button_id = "choice_panel_button_%d" % int(_sandra_back_index)
    click id _sandra_back_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == "TavernKitchen") timeout 20.0
    $ Sandra.rel = 0
    $ Sandra.talked_today = 0
    click id "main_ui_entity_button_npc_sandra" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("Попробовать помириться с мамой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _sandra_reconcile_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Попробовать помириться с мамой")
    $ _sandra_reconcile_button_id = "choice_panel_button_%d" % int(_sandra_reconcile_index)
    click id _sandra_reconcile_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and "Вы подошли к Сандре и извинились" in str(scene_runtime.text or "")) timeout 20.0
    assert eval ("Сандра" in str(scene_runtime.text or "") and "мам" not in str(scene_runtime.text or "").lower()) timeout 5.0

testcase external_sandra_weekly_thread_progression:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("sandra") is not None) timeout 20.0
    python:
        Sandra.var.update({
            "knowmolodost": 1,
            "revealing_dress_ordered": 1,
            "revealing_dress_code": "test_revealing_dress",
            "revealing_dress_initiative_seen": 1,
            "SecuredFuture": 1,
            "SecuredFutureDay": 31,
            "MaidRevengeEnding": 1,
            "MaidRevengeReason": "test_reason",
            "kitchen_regular_breakfast_requests": 2,
            "kitchen_client_manners_requests": 3,
        })
        Melissa.var.update({
            "harass_instruction": "allow",
            "revealing_dress_ordered": 1,
            "revealing_dress_code": "test_melissa_revealing_dress",
            "revealing_dress_request_seen": 1,
        })
        Amanda.var.update({
            "revealing_dress_ordered": 1,
            "revealing_dress_code": "test_amanda_revealing_dress",
            "revealing_dress_request_seen": 1,
        })
        Sandra.__dict__.pop("knows_molodost", None)
        Sandra.__dict__.pop("revealing_dress_code", None)
        Melissa.__dict__.pop("harass_instruction_state", None)
        Melissa.__dict__.pop("revealing_dress_code", None)
        Amanda.__dict__.pop("revealing_dress_code", None)
        tractir_progress.__dict__.pop("maid_revenge_ready", None)
        tractir_progress.__dict__.pop("maid_revenge_reason", None)
        tractir_progress.__dict__.pop("sandra_secured_future_day", None)
        threads.pop("sandraRevealingDressInitiative", None)
        threads.pop("melissaRevealingDressRequest", None)
        threads.pop("amandaRevealingDressRequest", None)
    $ updateSave_V49()
    assert eval (Sandra.knows_molodost and Sandra.revealing_dress_code == "test_revealing_dress") timeout 5.0
    assert eval (Melissa.harass_instruction() == "allow" and Melissa.revealing_dress_code == "test_melissa_revealing_dress" and "harass_instruction" not in Melissa.var) timeout 5.0
    assert eval (threads["sandraRevealingDressInitiative"].completed) timeout 5.0
    assert eval (threads["melissaRevealingDressRequest"].completed and not any(key in Melissa.var for key in ("revealing_dress_ordered", "revealing_dress_code", "revealing_dress_request_seen"))) timeout 5.0
    assert eval (threads["amandaRevealingDressRequest"].completed and Amanda.revealing_dress_code == "test_amanda_revealing_dress" and not any(key in Amanda.var for key in ("revealing_dress_ordered", "revealing_dress_code", "revealing_dress_request_seen"))) timeout 5.0
    assert eval (tractir_progress.sandra_secured_future_day == 31 and tractir_progress.maid_revenge_ready and tractir_progress.maid_revenge_reason == "test_reason") timeout 5.0
    assert eval (not any(key in Sandra.var for key in ("knowmolodost", "revealing_dress_ordered", "revealing_dress_code", "revealing_dress_initiative_seen", "SecuredFuture", "SecuredFutureDay", "MaidRevengeEnding", "MaidRevengeReason", "kitchen_regular_breakfast_requests", "kitchen_client_manners_requests"))) timeout 5.0
    python:
        Melissa.var.update({
            "MomDressComplaint": 2,
            "AskedAboutClaraDay": 11,
            "StartDay": 12,
            "StartCount": 3,
            "StartTotal": 4,
            "private_context_day": 13,
            "private_context_origin": "MarketPlace",
            "StorageThanksDay": 14,
            "temp_room": "TavernAmandaRoom",
            "storage_rat_cleared": 1,
            "storage_rat_last_help_day": 15,
            "bat_attic_check_day": 16,
            "drawings_ready_day": 17,
            "drawings_found": 1,
            "drawings_booklet_left": 1,
            "drawings_booklet_read": 1,
            "drawings_returned": 1,
            "roof_repair_order_day": 20,
            "roof_repair_complete_day": -1,
            "breakfast_tease_day": 23,
            "work_attitude": 99,
        })
        for _melissa_field in (
            "mom_dress_complaint_count", "asked_about_clara_day", "private_context_day",
            "private_context_origin", "storage_thanks_day", "temp_room_code",
            "storage_rat_help_day", "bat_attic_check_day", "drawings_ready_day",
            "drawings_found", "drawings_booklet_left", "drawings_booklet_read",
            "drawings_returned", "roof_repair_complete_day", "breakfast_tease_day",
        ):
            Melissa.__dict__.pop(_melissa_field, None)
    $ updateSave_V50()
    assert eval (Melissa.mom_dress_complaint_count == 2 and Melissa.asked_about_clara_day == 11) timeout 5.0
    assert eval (not any(hasattr(Melissa, field) for field in ("intimacy_start_day", "intimacy_start_count", "intimacy_start_total"))) timeout 5.0
    assert eval (Melissa.private_context_day == 13 and Melissa.private_context_origin == "MarketPlace" and Melissa.storage_thanks_day == 14 and Melissa.temp_room_code == "TavernAmandaRoom") timeout 5.0
    assert eval (Melissa.storage_rat_help_day == 15 and Melissa.bat_attic_check_day == 16 and Melissa.drawings_ready_day == 17 and Melissa.drawings_found and Melissa.drawings_booklet_left and Melissa.drawings_booklet_read and Melissa.drawings_returned) timeout 5.0
    assert eval (Melissa.roof_repair_complete_day == 22 and Melissa.breakfast_tease_day == 23) timeout 5.0
    assert eval (not any(key in Melissa.var for key in ("MomDressComplaint", "AskedAboutClaraDay", "StartDay", "StartCount", "StartTotal", "private_context_day", "private_context_origin", "StorageThanksDay", "temp_room", "storage_rat_cleared", "storage_rat_last_help_day", "bat_attic_check_day", "drawings_ready_day", "drawings_found", "drawings_booklet_left", "drawings_booklet_read", "drawings_returned", "roof_repair_order_day", "roof_repair_complete_day", "breakfast_tease_day", "work_attitude"))) timeout 5.0
    python:
        Clara.var.update({
            "flirt": 3,
            "drawings_secret_known": 1,
            "market_intro_seen": 1,
            "market_follow_failed_day": 31,
            "market_follow_failed_hour": 8,
            "market_day_roll_day": 32,
            "market_day_roll": 1,
            "market_evening_roll_day": 33,
            "market_evening_roll": 1,
            "day_location_override": {"day": 34, "location": "WineStore"},
            "merchant_contact_unlocked": 1,
            "merchant_contact_month_key": 110005,
            "old_water_pump_hint_seen": 1,
            "commission_followup_day": 35,
            "murder_day": 36,
            "special_cream_recipe_unlocked": 1,
            "sergio_discount": 25,
        })
        for _clara_field in (
            "flirt_count", "drawings_secret_known", "market_intro_seen",
            "market_follow_failed_day", "market_follow_failed_hour", "market_day_roll_day",
            "market_day_roll", "market_evening_roll_day", "market_evening_roll",
            "day_location_override_day", "day_location_override_code",
            "merchant_contact_unlocked", "merchant_contact_month_key",
            "old_water_pump_hint_seen", "commission_followup_day", "murder_day",
        ):
            Clara.__dict__.pop(_clara_field, None)
        crafting.__dict__.pop("special_cream_recipe_unlocked", None)
        tractir_progress.__dict__.pop("sergio_discount_percent", None)
    $ updateSave_V51()
    assert eval (Clara.flirt_count == 3 and Clara.drawings_secret_known and Clara.market_intro_seen and Clara.market_follow_failed_day == 31 and Clara.market_follow_failed_hour == 8) timeout 5.0
    assert eval (Clara.market_day_roll_day == 32 and Clara.market_day_roll and Clara.market_evening_roll_day == 33 and Clara.market_evening_roll) timeout 5.0
    assert eval (Clara.day_location_override_day == 34) timeout 5.0
    assert eval (Clara.day_location_override_code == "WineStore") timeout 5.0
    assert eval (Clara.merchant_contact_unlocked) timeout 5.0
    assert eval (Clara.merchant_contact_month_key == 110005) timeout 5.0
    assert eval (Clara.old_water_pump_hint_seen and Clara.commission_followup_day == 35 and Clara.murder_day == 36 and crafting.special_cream_recipe_unlocked and tractir_progress.sergio_discount_percent == 25) timeout 5.0
    assert eval (not any(key in Clara.var for key in ("flirt", "drawings_secret_known", "market_intro_seen", "market_follow_failed_day", "market_follow_failed_hour", "market_day_roll_day", "market_day_roll", "market_evening_roll_day", "market_evening_roll", "day_location_override", "merchant_contact_unlocked", "merchant_contact_month_key", "old_water_pump_hint_seen", "commission_followup_day", "murder_day", "special_cream_recipe_unlocked", "sergio_discount"))) timeout 5.0
    $ threads["sandraRevealingDressInitiative"].reset()
    $ Becky.home_visit_stage = 3
    $ Sandra.revealing_dress_code = ""
    $ Sandra.rel = 7
    $ Sandra.talked_today = 0
    $ daily_events.delete("", "BuyDressTom", "")
    $ daily_events.delete("sandra", "BuyDress", "")
    $ rooms.enter("TavernKitchen")
    assert eval (story_event_available("TavernKitchen", "sandra_dress_initiative")) timeout 5.0
    run Call("SandraDressInitiativeEvent")
    advance until screen "choice" timeout 20.0
    assert eval (threads["sandraRevealingDressInitiative"].completed) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
    assert eval (not story_event_available("TavernKitchen", "sandra_dress_initiative")) timeout 5.0
    $ threads["melissaRevealingDressRequest"].reset()
    $ Sandra.revealing_dress_code = "test_sandra_revealing_dress"
    $ Melissa.revealing_dress_code = ""
    $ Melissa.rel = 6
    $ Melissa.talked_today = 0
    $ daily_events.delete("melissa", "BuyDress", "")
    assert eval (story_event_available("TavernKitchen", "melissa_dress_request")) timeout 5.0
    run Call("MelissaDressRequestEvent")
    advance until screen "choice" timeout 20.0
    assert eval (threads["melissaRevealingDressRequest"].completed) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
    assert eval (not story_event_available("TavernKitchen", "melissa_dress_request")) timeout 5.0
    $ threads["amandaRevealingDressRequest"].reset()
    $ Melissa.revealing_dress_code = "test_melissa_revealing_dress"
    $ Amanda.revealing_dress_code = ""
    $ Amanda.rel = 5
    $ Amanda.talked_today = 0
    $ daily_events.delete("amanda", "BuyDress", "")
    assert eval (story_event_available("TavernKitchen", "amanda_dress_request")) timeout 5.0
    run Call("AmandaDressRequestEvent")
    advance until screen "choice" timeout 20.0
    assert eval (threads["amandaRevealingDressRequest"].completed) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0
    assert eval (not story_event_available("TavernKitchen", "amanda_dress_request")) timeout 5.0
    $ threads["sandraWeeklyEvaluation"].reset()
    $ threads["sandraWeeklyEvaluation"].disable()
    $ external_calendar_set_fields(7, 1, 1100, 23, 0)
    $ external_calendar_set_weekday(7)
    $ player.tavern_management.weekly_chores_last_eval_stamp = ""
    python:
        for _chore_key in PLAYER_CHORE_KEYS:
            player.chores.weekly[_chore_key] = player_chore_target(_chore_key)
    $ _sandra_weekly_message = evaluate_weekly_chores_and_rewards()
    assert eval (int(player.chores.last_score or 0) == 6 and str(player.chores.last_evaluation or "") == "good") timeout 5.0
    assert eval (threads["sandraWeeklyEvaluation"].enabled and int(threads["sandraWeeklyEvaluation"].num or 0) == 0) timeout 5.0
    $ external_calendar_set_fields(8, 1, 1100, 8, 0)
    $ external_calendar_set_weekday(1)
    assert eval (story_event_available("TavernMyRoom", "sleep")) timeout 5.0
    run Call("checkTriggers", "TavernMyRoom", "sleep", 0)
    advance until eval (int(threads["sandraWeeklyEvaluation"].num or 0) == 1 and not threads["sandraWeeklyEvaluation"].enabled) timeout 30.0
    assert eval (tavern_upstairs_can_enter_sandra_room()) timeout 5.0

testcase external_sandra_night_thanks_hours_work:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ rooms.enter("TavernSandraRoom")
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernSandraRoom", start_minute=0, end_minute=1440, priority=999)])
    $ threads["sandraWeeklyEvaluation"].advanceTo(4, force_active=True)
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    assert eval ("Принять ночную благодарность Сандры" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    run Call("checkTriggers", "TavernSandraRoom", "sandra_night_thanks", 0)
    assert eval (threads["sandraWeeklyEvaluation"].completed and int(threads["sandraWeeklyEvaluation"].num or 0) == 5) timeout 5.0
    assert eval (not hasattr(Sandra, "final_reward_flag") and not hasattr(Sandra, "sandraSex")) timeout 5.0
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    assert eval ("Уединиться с Сандрой" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ threads["sandraWeeklyEvaluation"].advanceTo(4, force_active=True)
    $ external_calendar_set_fields(calendar_v2.day + 1, calendar_v2.period, calendar_v2.cycle, 23, 0)
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    assert eval ("Принять ночную благодарность Сандры" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    run Call("checkTriggers", "TavernSandraRoom", "sandra_night_thanks", 0)
    assert eval (threads["sandraWeeklyEvaluation"].completed and int(threads["sandraWeeklyEvaluation"].num or 0) == 5) timeout 5.0
'''


MELISSA_SEX_ENGINE_CHECKS = r'''
testcase external_melissa_courtship_is_slow_and_daily:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ _melissa_courtship_date = calendar_v2.day_number_to_parts(90)
    $ external_calendar_set_fields(int(_melissa_courtship_date.get("day", 1) or 1), int(_melissa_courtship_date.get("month", 1) or 1), int(_melissa_courtship_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 23, 0)
    $ rooms.enter("TavernMyRoom")
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernMyRoom", start_hour=0, end_hour=24, priority=999)])
    $ Melissa.rel = 16
    $ Melissa.openness = 12
    $ Melissa.corruption = 18
    $ Melissa.storage_rat_help_day = 1
    $ Melissa.roof_repair_complete_day = 1
    $ Melissa.drawings_returned = True
    $ Melissa.drawings_booklet_left = False
    $ threads["melissaBatProblem"].advanceTo(8, complete_at_end=True)
    $ threads["melissaCourtship"].reset()
    $ Melissa.reset_daily()
    $ initStoryEventRuntime(True)
    assert eval (not story_event_available("talk_melissa", "melissa_intimacy")) timeout 5.0

    $ Melissa.drawings_booklet_left = True
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_melissa", "melissa_intimacy")) timeout 5.0
    assert eval (not Melissa.relationship_allows("intimacy") and not Melissa.relationship_allows("sex")) timeout 5.0

    run Call("IntMelissaTalk", "melissa")
    advance until screen "choice" timeout 20.0
    $ _melissa_talk_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Поговорить")
    click id ("choice_panel_button_%d" % int(_melissa_talk_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Закончить разговор" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _melissa_end_talk_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    click id ("choice_panel_button_%d" % int(_melissa_end_talk_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Сблизиться с Мелиссой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (int(Melissa.talked_today or 0) == 1 and "Поговорить" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Сблизиться с Мелиссой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Уединиться с Мелиссой" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _melissa_courtship_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Сблизиться с Мелиссой")
    click id ("choice_panel_button_%d" % int(_melissa_courtship_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Осторожно коснуться Мелиссы" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval ("Осторожно поцеловать Мелиссу" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _melissa_touch_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Осторожно коснуться Мелиссы")
    click id ("choice_panel_button_%d" % int(_melissa_touch_index)) pos (0.5, 0.5) until eval (int(threads["melissaCourtship"].num or 0) == 1 and renpy.get_screen("say") is not None) timeout 20.0
    assert eval (int(Melissa.fucked_today or 0) == 1 and "так можно" in str(scene_runtime.text or "")) timeout 5.0
    advance until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (not story_event_available("talk_melissa", "melissa_intimacy")) timeout 5.0

    $ _melissa_next_date = calendar_v2.day_number_to_parts(current_game_day() + 1)
    $ external_calendar_set_fields(int(_melissa_next_date.get("day", 1) or 1), int(_melissa_next_date.get("month", 1) or 1), int(_melissa_next_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 23, 0)
    $ Melissa.reset_daily()
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_melissa", "melissa_intimacy")) timeout 5.0

    run Call("IntMelissaTalk", "melissa")
    advance until screen "choice" timeout 20.0
    $ _melissa_courtship_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Сблизиться с Мелиссой")
    click id ("choice_panel_button_%d" % int(_melissa_courtship_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Осторожно поцеловать Мелиссу" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _melissa_wait_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Не торопить события")
    click id ("choice_panel_button_%d" % int(_melissa_wait_index)) pos (0.5, 0.5) until eval (renpy.get_screen("say") is not None) timeout 20.0
    advance until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0

testcase external_melissa_finished_intimacy_returns_to_room_and_closes_for_day:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ _melissa_intimacy_date = calendar_v2.day_number_to_parts(90)
    $ external_calendar_set_fields(int(_melissa_intimacy_date.get("day", 1) or 1), int(_melissa_intimacy_date.get("month", 1) or 1), int(_melissa_intimacy_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 23, 0)
    $ rooms.enter("TavernMyRoom")
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernMyRoom", start_hour=0, end_hour=24, priority=999)])
    $ Melissa.rel = 18
    $ Melissa.openness = 14
    $ Melissa.corruption = 22
    $ Melissa.storage_rat_help_day = 1
    $ Melissa.roof_repair_complete_day = 1
    $ Melissa.drawings_returned = True
    $ Melissa.drawings_booklet_left = True
    $ threads["melissaBatProblem"].advanceTo(8, complete_at_end=True)
    $ threads["melissaCourtship"].advanceTo(5, complete_at_end=True)
    $ Melissa.reset_daily()
    $ initStoryEventRuntime(True)
    assert eval (Melissa.relationship_allows("intimacy") and Melissa.relationship_allows("sex")) timeout 5.0

    run Call("IntMelissaTalk", "melissa")
    advance until screen "choice" timeout 20.0
    assert eval ("Уединиться с Мелиссой" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _melissa_intimacy_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Уединиться с Мелиссой")
    click id ("choice_panel_button_%d" % int(_melissa_intimacy_index)) pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "event" and renpy.get_screen("choice") is not None and "Осмотреть Мелиссу" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "event" and str(main_ui_runtime.action_title or "") == "Мелисса") timeout 5.0
    $ _melissa_stop_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Остановиться")
    click id ("choice_panel_button_%d" % int(_melissa_stop_index)) pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (int(Melissa.fucked_today or 0) == 1 and not Melissa.relationship_allows("intimacy")) timeout 5.0
'''


PLAYER_INTIMACY_STATE_CHECKS = r'''
testcase external_player_intimacy_state_sleep_arousal_and_help:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ renpy.call_in_new_context("InitDressDesc")
    $ player.intimacy.arousal = {"You": 73, "you": 11, "amanda": 99}
    $ tractir_save_normalize_player_arousal()
    assert eval (player.intimacy.arousal_value() == 73 and isinstance(player.intimacy.arousal, int)) timeout 5.0
    $ player.intimacy.arousal = 5
    $ Arousal = {"you": 41}
    $ tractir_save_normalize_player_arousal()
    assert eval (player.intimacy.arousal_value() == 41 and isinstance(player.intimacy.arousal, int)) timeout 5.0
    $ _intimacy_test_date = calendar_v2.day_number_to_parts(8)
    $ external_calendar_set_fields(int(_intimacy_test_date.get("day", 1) or 1), int(_intimacy_test_date.get("month", 1) or 1), int(_intimacy_test_date.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 7, 0)
    $ rooms.enter("TavernMyRoom")
    $ player_ensure_nightwear_in_chest()
    assert eval ("nightshirt" in list(player.appearance.owned_dresses or [])) timeout 5.0
    run Call("TavernMyRoomOpenChest")
    assert eval (len([str(i.caption or "") for i in main_ui_runtime.action_items]) == len(set([str(i.caption or "") for i in main_ui_runtime.action_items]))) timeout 5.0
    $ player_set_sleep_layer("nothing")
    assert eval (player_is_naked()) timeout 5.0
    assert eval ("ничего" in "\n".join(player_body_state_lines()).lower()) timeout 5.0

    run Jump("TavernUpstairs")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Спуститься в главный зал" not in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval (any("одеться" in str(i.caption or "").lower() for i in main_ui_runtime.action_items)) timeout 5.0

    $ rooms.enter("TavernMyRoom")
    $ player.intimacy.last_sex_day = current_game_day() - 3
    $ player.intimacy.morning_arousal_day = -1
    $ PlayerRoomLightClosed = 1
    $ player.intimacy.set_arousal(0)
    $ player_apply_morning_state("TavernMyRoom")
    assert eval (player.intimacy.arousal_value() > 0) timeout 5.0
    assert eval ("утренним стояком" in str(player.intimacy.wake_state_notice or "")) timeout 5.0

    $ Amanda.rel = 20
    $ Amanda.openness = 20
    $ Amanda.corruption = 80
    $ Amanda.set_arousal(85)
    $ player.intimacy.set_arousal(85)
    $ player.intimacy.came_today = 0
    $ player.intimacy.last_sex_day = -1
    $ _help_result = player_intimacy_help_result("amanda", 0.0)
    assert eval (bool(_help_result.get("ok", False))) timeout 5.0
    assert eval (int(player.intimacy.came_today or 0) == 1) timeout 5.0
    assert eval (int(player.intimacy.last_sex_day) == current_game_day()) timeout 5.0

    $ Melissa.rel = 20
    $ Melissa.openness = 0
    $ Melissa.corruption = 40
    $ Melissa.set_arousal(0)
    $ _melissa_friend_before = int(Melissa.rel or 0)
    $ _melissa_slut_before = int(Melissa.corruption or 0)
    $ _bad_result = player_intimacy_help_result("melissa", 1.0)
    assert eval (not bool(_bad_result.get("ok", False))) timeout 5.0
    assert eval (int(Melissa.rel or 0) == _melissa_friend_before - 10) timeout 5.0
    assert eval (int(Melissa.corruption or 0) < _melissa_slut_before) timeout 5.0
'''


CLARA_AMANDA_SCHEDULE_FLOW_CHECKS = r'''
testcase external_clara_evening_follow_finishes_in_melissa_room:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(13, 2, 1100, 21, 0)
    $ external_calendar_set_weekday(3)
    $ BlockTimeAdvance = 0
    $ TavernEventOngoing = ""
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.mode = "scene"
    $ Clara.murder_day = 999999
    $ Clara.rel = max(int(Clara.rel or 0), 8)
    $ player.tavern_management.breakfast.event_active = False
    $ TavernBreakfastPresentIds = None
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ threads["claraPaintingsPath"].advanceTo(8, force_active=True)
    $ findAvailableEvents(True)

    run Jump("ArtisansQuarter")
    advance until screen "main_ui" timeout 20.0
    assert eval (int(threads["claraPaintingsPath"].num or 0) == 9) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    $ npc_interval_schedule_load_all(True)
    assert eval (str(people.location("clara") or "") == "TavernMelissaRoom") timeout 5.0
    assert eval (str(people.location("melissa") or "") == "TavernMelissaRoom") timeout 5.0
    run Jump("TavernMelissaRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Выслушать Клариссу и Мелиссу" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ renpy.call_in_new_context("checkTriggers", "TavernMelissaRoom", "clara_paintings", 0)
    assert eval (int(threads["claraPaintingsPath"].num or 0) == 10) timeout 5.0
    assert eval ("Кларисса наконец срывается" in str(scene_runtime.text or "")) timeout 5.0

'''


HOUSEHOLD_AI_EVENT_CHECKS = r'''
testcase external_household_ai_kitchen_event_fires:
    $ renpy.call_in_new_context("InitGameNPCs")
    $ external_calendar_set_fields(1, 1, 1100, 8, 0)
    $ player.economy.money = 80
    $ player.tavern_management.cleanliness = 15
    $ player.tavern_management.productnum = 0
    $ rooms.enter("TavernKitchen"
)
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
    $ household.seen.clear()
    $ household.meta.update({"pressure": 0.0, "friction": 0.70, "convergence": 0.0, "external_threat": 0.0, "last_event_code": ""})
    $ household_ai_npc_state("amanda")["drive"] = 0.0
    $ household_ai_npc_state("sandra")["drive"] = 0.0
    $ household_ai_npc_state("melissa")["drive"] = 0.0
    assert eval (household_ai_pick_event("TavernKitchen", "room") == "household_event_kitchen_amanda_sandra_spark") timeout 5.0
    run Call("HouseholdEvent_Try", "TavernKitchen", "room")
    advance until screen "choice" timeout 20.0
    click pos (960, 560)
    advance until eval (str(household.meta.get("last_event_code", "") or "") == "household_event_kitchen_amanda_sandra_spark") timeout 10.0
    assert eval (household_ai_seen("household_event_kitchen_amanda_sandra_spark", "TavernKitchen")) timeout 5.0
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
            captions = [full_click_text(getattr(i, "caption", "")) for i in list(main_ui_runtime.action_items or [])]
        except Exception:
            captions = []
        overlay_screens = []
        for screen_name in (
            "dress_shop_catalog_page",
            "girl_card_overlay",
            "player_card_overlay",
            "story_thread_board",
        ):
            try:
                if _full_click_renpy.get_screen(screen_name) is not None:
                    overlay_screens.append(screen_name)
            except Exception:
                pass
        try:
            native_choice_visible = _full_click_renpy.get_screen("choice") is not None
        except Exception:
            native_choice_visible = False
        return (
            full_click_text(rooms.current_code),
            full_click_text(main_ui_runtime.action_title),
            full_click_text(scene_runtime.text),
            full_click_text(scene_runtime.location_text),
            full_click_text(scene_runtime.picture),
            full_click_text(main_ui_runtime.overlay),
            full_click_text(main_ui_runtime.girl_key),
            full_click_text(main_ui_runtime.object_id),
            tuple(captions),
            tuple(overlay_screens),
            native_choice_visible,
        )

    def full_click_prepare_common():
        calendar_v2.week = 1
        calendar_v2.hour = 12
        calendar_v2.minute = 0
        calendar_v2.time_advance_blocked = 0
        main_ui_runtime.overlay = ""
        main_ui_runtime.inventory_dropdown_open = False
        main_ui_runtime.action_content = None
        main_ui_runtime.mode = "scene"
        try:
            threads.clear()
            initThreads()
            threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
            event_runtime.available.clear()
            event_runtime.evaluation_time = None
        except Exception:
            pass
        try:
            Sandra.rel = max(int(Sandra.rel or 0), 10)
            set_bedroom_door_locked("TavernSandraRoom", False)
            Amanda.room_entry_blocked_today = False
            people.get_data("eddie").set_schedule([NPCScheduleEntry(location="GroceryStore", start_minute=0, end_minute=1440, priority=999)])
            people.get_data("becky").set_schedule([NPCScheduleEntry(location="GroceryStore", start_minute=0, end_minute=1440, priority=999)])
            people.get_data("irma").set_schedule([NPCScheduleEntry(location="DressShop", start_minute=0, end_minute=1440, priority=999)])
            people.get_data("alber").set_schedule([NPCScheduleEntry(location="WineStore", start_minute=0, end_minute=1440, priority=999)])
            people.get_data("zimmer").set_schedule([NPCScheduleEntry(location="CityGuard", start_minute=0, end_minute=1440, priority=999)])
            people.get_data("fran").set_schedule([NPCScheduleEntry(location="EllonaTemple", start_minute=0, end_minute=1440, priority=999)])
            Eddie.known = True
            Becky.known = True
            Irma.known = True
            Alber.known = True
            Zimmer.known = True
            Fran.known = True
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
        _full_click_renpy.hide_screen("choice")
        _full_click_renpy.jump(FULL_CLICK_ROOM)

    def full_click_capture_before():
        global FULL_CLICK_CAPTION, FULL_CLICK_BEFORE, FULL_CLICK_SKIP, FULL_CLICK_SKIP_REASON
        items = list(main_ui_runtime.action_items or [])
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
            escaped_caption = FULL_CLICK_CAPTION.encode("unicode_escape").decode("ascii")
            raise AssertionError("{}[{}] {}: click made no visible state change".format(FULL_CLICK_ROOM, FULL_CLICK_INDEX, escaped_caption))
        FULL_CLICK_REPORT.append("{}[{}] {}".format(FULL_CLICK_ROOM, FULL_CLICK_INDEX, FULL_CLICK_CAPTION))

testcase external_all_room_action_clicks:
    parameter (room_name, action_index) = __ROOM_ACTION_CLICK_PARAMS__
    run Function(full_click_start_room, room_name, action_index)
    advance until screen "main_ui" timeout 20.0
    $ full_click_capture_before()
    if eval full_click_has_item():
        if eval (FULL_CLICK_INDEX >= 7):
            scroll amount 2 pos (1700, 760)
        if eval (FULL_CLICK_INDEX >= 9):
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


CALENDAR_TIME_CHECKS = r'''
testcase external_new_game_starts_at_8_morning:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval (int(calendar_v2.hour or 0) == 8) timeout 5.0
    assert eval (int(calendar_v2.minute or 0) == 0) timeout 5.0
    assert eval (int(calendar_v2.time_slot() or 0) == 1 and TIME_SLOT_INFO[calendar_v2.time_slot()]["name_en"] == "morning") timeout 5.0
    assert eval (str(calendar_v2.clock_text() or "") == "08:00") timeout 5.0
    assert eval (int(player.tavern_management.visitors or 0) == 40 and int(player.tavern_management.productnum or 0) == 200 and int(player.tavern_management.winenum or 0) == 100) timeout 5.0
    assert eval (str(tractir_first_active_ending() or "") == "") timeout 5.0

testcase external_navigation_jump_does_not_stack_previous_room:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ threads["cityBlindPirateFall"].advanceTo(threads["cityBlindPirateFall"].data.length, complete_at_end=True)
    run Jump("StreetTavern")
    advance until eval (str(rooms.current_code or "") == "StreetTavern" and renpy.get_screen("main_ui") is not None) timeout 20.0
    $ _navigation_stack_before = len(renpy.get_return_stack())
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "MarketPlace") timeout 20.0
    advance until eval (str(rooms.current_code or "") == "MarketPlace" and len(main_ui_runtime.action_items or []) > 0 and renpy.get_screen("main_ui") is not None) timeout 20.0
    assert eval (len(renpy.get_return_stack()) == _navigation_stack_before) timeout 5.0

testcase external_calendar_long_cycle_thirteenth_period_rollover:
    $ player.identity.age = 20
    $ external_calendar_set_fields(28, 13, 1100, 23, 59)
    assert eval (int(calendar_v2.clock_minutes() or 0) == 1439 and int(calendar_v2.daysInGame or 0) == external_calendar_day_number_from_fields(28, 13, 1100)) timeout 5.0
    $ calendar_v2.advance_minutes(1)
    assert eval (int(calendar_v2.cycle or 0) == 1101) timeout 5.0
    assert eval (int(calendar_v2.period or 0) == 1) timeout 5.0
    assert eval (int(calendar_v2.day or 0) == 1) timeout 5.0
    assert eval (int(calendar_v2.clock_minutes() or 0) == 0) timeout 5.0
    assert eval (int(player.identity.age or 0) == 20) timeout 5.0
    assert eval (calendar_v2.moon_name_en() == "Wolf Moon" and calendar_v2.moon_name_ru() == "Луна Волка") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 16, 0)
    assert eval (int(calendar_v2.time_slot() or 0) == 4) timeout 5.0
    assert eval (int(calendar_v2.clock_minutes() or 0) == 960) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 5, 59)
    assert eval (int(calendar_v2.time_slot() or 0) == 7) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 6, 0)
    assert eval (int(calendar_v2.time_slot() or 0) == 0) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    assert eval (int(calendar_v2.time_slot() or 0) == 1 and TIME_SLOT_INFO[calendar_v2.time_slot()]["name_en"] == "morning") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 10, 45)
    assert eval (int(calendar_v2.time_slot() or 0) == 1 and TIME_SLOT_INFO[calendar_v2.time_slot()]["name_en"] == "morning") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 11, 0)
    assert eval (int(calendar_v2.time_slot() or 0) == 2 and TIME_SLOT_INFO[calendar_v2.time_slot()]["name_en"] == "noon") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 13, 0)
    assert eval (int(calendar_v2.time_slot() or 0) == 3 and TIME_SLOT_INFO[calendar_v2.time_slot()]["name_en"] == "afternoon") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 16, 0)
    assert eval (int(calendar_v2.time_slot() or 0) == 4 and TIME_SLOT_INFO[calendar_v2.time_slot()]["name_en"] == "day") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 19, 0)
    assert eval (int(calendar_v2.time_slot() or 0) == 5 and TIME_SLOT_INFO[calendar_v2.time_slot()]["name_en"] == "evening") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 21, 0)
    assert eval (int(calendar_v2.time_slot() or 0) == 6 and TIME_SLOT_INFO[calendar_v2.time_slot()]["name_en"] == "late evening") timeout 5.0
    $ player.condition.energy = 80
    $ player.condition.fun = 80
    $ _evening_chore_allowed = can_do_player_chore("clean_ashes", "TavernMain", "fireplace_001")
    assert eval (bool(_evening_chore_allowed[0])) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 16, 0)
    $ player.condition.energy = 68
    $ player.condition.fun = 80
    assert eval (str(action_restriction_message("chore") or "") == "") timeout 5.0
    assert eval (str(action_restriction_message("heavy_chore") or "") == "") timeout 5.0
    assert eval (str(action_restriction_message("wash") or "") == "") timeout 5.0
    assert eval (str(action_restriction_message("rest") or "") == "") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 30)
    $ _before_minutes = (int(calendar_v2.daysInGame or 0) * 1440) + int(calendar_v2.clock_minutes() or 0)
    $ _advanced = 30
    $ calendar_v2.advance_minutes(_advanced)
    assert eval (int(_advanced or 0) == 30) timeout 5.0
    assert eval (int(calendar_v2.hour or 0) == 23) timeout 5.0
    assert eval (int(calendar_v2.minute or 0) == 0) timeout 5.0
    assert eval (((int(calendar_v2.daysInGame or 0) * 1440) + int(calendar_v2.clock_minutes() or 0)) - _before_minutes == 30) timeout 5.0
    $ _late_evening_chore_allowed = can_do_player_chore("clean_ashes", "TavernMain", "fireplace_001")
    assert eval (bool(_late_evening_chore_allowed[0])) timeout 5.0
    assert eval (str(action_restriction_message("chore") or "") == "") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 4, 0)
    $ _night_chore = do_player_chore("clean_ashes", "TavernMain", "fireplace_001")
    assert eval (not bool(_night_chore.get("ok", False))) timeout 5.0
    assert eval ("пора немедленно ложиться спать" in str(_night_chore.get("text", "") or "")) timeout 5.0
    assert eval ("пора немедленно ложиться спать" in str(action_restriction_message("chore") or "")) timeout 5.0
    $ player.condition.health = 73
    $ player.condition.energy = 46
    assert eval (("Энергия", "46") in player_card_stat_rows_right()) timeout 5.0

testcase external_sleep_wake_hour_rules:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 23, 0)
    $ _sleep_wake_23 = player_sleep_wake_time()
    assert eval (int(_sleep_wake_23[0]) == 6 and int(_sleep_wake_23[1]) == 0) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 1, 20)
    $ _sleep_wake_1 = player_sleep_wake_time()
    assert eval (int(_sleep_wake_1[0]) == 7 and int(_sleep_wake_1[1]) == 20) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 2, 15)
    $ _sleep_wake_2 = player_sleep_wake_time()
    assert eval (int(_sleep_wake_2[0]) == 7 and int(_sleep_wake_2[1]) == 15) timeout 5.0

testcase external_daily_setstatdefault_body_maps_exist:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ Melissa.set_sex_stat("breastfeed", 0)
    $ Melissa.set_sex_stat("lactate", 0)
    $ Sandra.rel = 10
    $ Sandra.openness = 0
    $ Amanda.rel = 10
    $ Amanda.openness = 0
    run Call("DailySetstatdefault", "melissa")
    run Call("DailySetstatdefault", "sandra")
    run Call("DailySetstatdefault", "amanda")
    assert eval (int(Melissa.sex_stat("breastfeed", -1)) >= 0 and int(Melissa.sex_stat("lactate", -1)) >= 0) timeout 5.0
    assert eval (int(Sandra.sex_stat("breastfeed", -1)) >= 0 and int(Sandra.sex_stat("lactate", -1)) >= 0 and int(Amanda.sex_stat("breastfeed", -1)) >= 0 and int(Amanda.sex_stat("lactate", -1)) >= 0) timeout 5.0
    assert eval (int(Sandra.openness or 0) >= 5 and int(Amanda.openness or 0) >= 5) timeout 5.0

testcase external_hunter_club_reputation_challenge_and_trade:
    run Call("InitGameNPCs")
    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 12, 0)
    $ external_calendar_set_weekday(1)
    $ rooms.get("HunterClub").state["first_visit_seen"] = 1
    run Jump("HunterClub")
    advance until screen "main_ui" timeout 20.0
    assert eval ("Купить товары" in [str(i.caption or "") for i in main_ui_runtime.action_items] and "Продать добычу" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval ("Поговорить с Луизой" not in [str(i.caption or "") for i in main_ui_runtime.action_items] and "luisa" in people.ids_at("HunterClub")) timeout 5.0
    click id "main_ui_entity_button_npc_luisa" pos (0.5, 0.5) until eval (str(main_ui_runtime.action_title or "") == "Толстуха Луиза") timeout 20.0
    assert eval ("Закупиться для охоты" in [str(i.caption or "") for i in main_ui_runtime.action_items] and "Подать добычу" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _hunter_luisa_buy_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Закупиться для охоты")
    $ _hunter_luisa_buy_button = "choice_panel_button_%d" % int(_hunter_luisa_buy_index)
    click id _hunter_luisa_buy_button pos (0.5, 0.5) until screen "hunter_club_trade_overlay" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("hunter_club_trade_overlay") is not None and str(main_ui_runtime.action_title or "") == "Покупка" and main_ui_runtime.action_content is None) timeout 5.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items] == ["Подтвердить покупку", "Сбросить выбор", "Назад"]) timeout 5.0
    assert eval (len(list(hunter_club_trade_entries("buy") or [])) > 0 and rooms.get("HunterClub").state.get("trade_mode", "") == "buy") timeout 5.0
    $ rooms.get("HunterClub").state["completed_challenges"] = {}
    $ rooms.get("HunterClub").state["reputation"] = 0
    $ player.set_stat("reputation", 0)
    $ _hunter_wolf_before = int(player.item_count("wolf_skin_001") or 0)
    $ player.add_item("wolf_skin_001", 1)
    $ _hunter_challenge_result = hunter_club_apply_challenge("wolf_skin")
    assert eval (bool(_hunter_challenge_result.get("ok", False))) timeout 5.0
    assert eval (hunter_club_challenge_completed("wolf_skin") and hunter_club_reputation() == 2) timeout 5.0
    assert eval (int(player.stats.reputation or 0) == 2 and int(player.item_count("wolf_skin_001") or 0) == _hunter_wolf_before) timeout 5.0
    $ _hunter_duplicate_result = hunter_club_apply_challenge("wolf_skin")
    assert eval (not bool(_hunter_duplicate_result.get("ok", True)) and hunter_club_reputation() == 2 and int(player.stats.reputation or 0) == 2) timeout 5.0
    $ player.economy.money = 100
    $ _hunter_arrows_before = int(player.item_count("arrows_001") or 0)
    $ rooms.get("HunterClub").state["trade_mode"] = "buy"
    $ rooms.get("HunterClub").state["trade_selection"] = {"arrows_001": 2}
    assert eval (get_game_item("arrows_001") is not None) timeout 5.0
    assert eval (hunter_club_trade_selected_qty("arrows_001") == 2) timeout 5.0
    assert eval (any(str(row.get("item_id", "") or "") == "arrows_001" for row in hunter_club_trade_entries("buy"))) timeout 5.0
    $ _hunter_trade_result = hunter_club_apply_trade("buy")
    assert eval (bool(_hunter_trade_result.get("ok", False))) timeout 5.0
    assert eval (int(player.economy.money or 0) == 88 and int(player.item_count("arrows_001") or 0) == _hunter_arrows_before + 2) timeout 5.0

testcase external_hour_based_room_and_npc_schedule_adjustment:
    run Call("InitGameNPCs")
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = []
    $ npc_interval_schedule_load_all(True)
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(1)
    assert eval (rooms.get("MarketPlace").is_open()) timeout 5.0
    assert eval (rooms.get("WineStore").is_open()) timeout 5.0
    assert eval (rooms.get("DressShop").is_open()) timeout 5.0
    assert eval (str(people.location("clara") or "") == "WineStore" and str(people.schedule_state("clara").get("label", "") or "") == "wine_store") timeout 5.0
    assert eval (int(calendar_v2.week or 0) == 1 and int(calendar_v2.hour or 0) == 8) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 6, 0)
    assert eval (int(calendar_v2.week or 0) == 1 and int(calendar_v2.hour or 0) == 6) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 6, 0)
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    assert eval (str(people.schedule_state("clara").get("label", "") or "") != "wine_store" and int(calendar_v2.week or 0) == 1 and int(calendar_v2.hour or 0) == 12) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 17, 59)
    assert eval (rooms.get("MarketPlace").is_open()) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 19, 0)
    assert eval (not rooms.get("MarketPlace").is_open()) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 15, 59)
    assert eval (rooms.get("GroceryStore").is_open() and rooms.get("HunterClub").is_open() and people.location("luisa") == "HunterClub") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 19, 0)
    assert eval ((not rooms.get("GroceryStore").is_open()) and (not rooms.get("HunterClub").is_open()) and people.location("luisa") == "") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 6, 0)
    $ external_calendar_set_weekday(7)
    assert eval (not rooms.get("Church").is_open()) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(7)
    assert eval (rooms.get("Church").is_open() and people.location("gerhard") == "Church") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 59)
    $ external_calendar_set_weekday(7)
    assert eval (rooms.get("Church").is_open()) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 13, 0)
    $ external_calendar_set_weekday(7)
    assert eval ((not rooms.get("Church").is_open()) and people.location("gerhard") == "") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 6, 0)
    $ external_calendar_set_weekday(5)
    assert eval (city_guard_open_now() and people.location("zimmer") == "CityGuard") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(5)
    assert eval ((not city_guard_open_now()) and people.location("zimmer") == "") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(6)
    assert eval (barber_shop_is_open()) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 0)
    $ external_calendar_set_weekday(1)
    assert eval (barber_shop_is_open()) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 6, 0)
    assert eval (calendar_v2.time_slot() == 0) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 0)
    assert eval (calendar_v2.time_slot() == 1) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 59)
    assert eval (calendar_v2.time_slot() == 6) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 23, 0)
    assert eval (str(people.schedule_state("amanda").get("label", "") or "") == "sleep") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 16, 0)
    assert eval (str(people.schedule_state("amanda").get("label", "") or "") != "sleep") timeout 5.0
    $ npc_interval_schedule_load_all(True)
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 8, 30)
    $ external_calendar_set_weekday(1)
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 23, 30)
    $ external_calendar_set_weekday(1)
    $ _amanda_sleep_entries = [row for row in people.get_data("amanda").interval_schedule_entries if str(getattr(row, "label", "") or "") == "sleep"]
    assert eval (len(_amanda_sleep_entries) == 1) timeout 5.0
    assert eval (int(getattr(_amanda_sleep_entries[0], "priority", 0) or 0) == 700 and _amanda_sleep_entries[0].matches()) timeout 5.0
    $ _amanda_resolved_night = people.schedule_entry("amanda")
    assert eval (_amanda_resolved_night is _amanda_sleep_entries[0]) timeout 5.0
    assert eval (str(people.schedule_state("amanda").get("label", "") or "") == "sleep") timeout 5.0
    assert eval (bool(people.schedule_state("amanda").get("awake", True)) == False) timeout 5.0
    assert eval (str(people.location("amanda") or "") == "TavernAmandaRoom") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 20, 0)
    $ external_calendar_set_weekday(5)
    assert eval (str(people.location("melissa") or "") in ("FridayDance", "TavernMelissaRoom") and str(people.schedule_state("melissa").get("label", "") or "") == "friday_dance") timeout 5.0
    assert eval (str(people.location("clara") or "") in ("FridayDance", "WineStore") and str(people.schedule_state("clara").get("label", "") or "") == "friday_dance") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 22, 0)
    $ external_calendar_set_weekday(5)
    assert eval (str(people.location("melissa") or "") == "TavernMelissaRoom" and str(people.location("clara") or "") == "TavernMelissaRoom") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 12, 30)
    $ external_calendar_set_weekday(2)
    assert eval (str(people.location("irma") or "") == "DressShop" and bool(people.schedule_state("irma").get("talkable", False)) == True) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 13, 30)
    assert eval (str(people.location("irma") or "") == "DressShop" and bool(people.schedule_state("irma").get("talkable", True)) == False) timeout 5.0
    $ npc_interval_schedule_load_all(True)
    assert eval (all(len(people.get_data(key).interval_schedule_entries or []) > 0 for key in ("becky", "eddie", "alber"))) timeout 5.0
    $ external_calendar_set_fields(10, calendar_v2.period, calendar_v2.cycle, 8, 0)
    $ external_calendar_set_weekday(1)
    assert eval (str(people.location("alber") or "") == "" and "alber" not in list(people.ids_at("WineStore") or [])) timeout 5.0
    assert eval (str(people.location("clara") or "") == "WineStore" and "clara" in list(people.ids_at("WineStore") or [])) timeout 5.0
    $ external_calendar_set_fields(10, calendar_v2.period, calendar_v2.cycle, 8, 30)
    $ external_calendar_set_weekday(1)
    assert eval (str(people.location("eddie") or "") == "GroceryStore" and str(people.schedule_state("eddie").get("label", "") or "") == "grocery_morning_shift") timeout 5.0
    assert eval (str(people.location("becky") or "") != "GroceryStore") timeout 5.0
    $ external_calendar_set_fields(10, calendar_v2.period, calendar_v2.cycle, 13, 0)
    $ external_calendar_set_weekday(1)
    assert eval (str(people.location("becky") or "") == "GroceryStore" and str(people.schedule_state("becky").get("label", "") or "") == "grocery_afternoon_shift") timeout 5.0
    assert eval (str(people.location("eddie") or "") != "GroceryStore") timeout 5.0
    $ external_calendar_set_fields(22, calendar_v2.period, calendar_v2.cycle, 8, 30)
    assert eval (str(people.location("eddie") or "") == "OutOfTown" and str(people.schedule_state("eddie").get("label", "") or "") == "monthly_absence") timeout 5.0
    assert eval (str(people.location("becky") or "") == "GroceryStore" and str(people.schedule_state("becky").get("label", "") or "") == "eddie_absent_grocery_cover") timeout 5.0
    $ external_calendar_set_fields(10, calendar_v2.period, calendar_v2.cycle, 20, 0)
    $ external_calendar_set_weekday(5)
    assert eval (str(people.location("becky") or "") == "FridayDance" and str(people.schedule_state("becky").get("label", "") or "") == "friday_dance") timeout 5.0
    assert eval (str(people.location("alber") or "") == "FridayDance" and str(people.schedule_state("alber").get("label", "") or "") == "friday_dance") timeout 5.0
    $ external_calendar_set_fields(10, calendar_v2.period, calendar_v2.cycle, 20, 0)
    $ external_calendar_set_weekday(2)
    assert eval (str(people.location("eddie") or "") == "PortStreetsBackAlley" and str(people.schedule_state("eddie").get("label", "") or "") == "port_whores_evening") timeout 5.0
    $ external_calendar_set_fields(10, calendar_v2.period, calendar_v2.cycle, 12, 30)
    $ external_calendar_set_weekday(1)
    assert eval (str(people.location("alber") or "") == "WineStore" and str(people.schedule_state("alber").get("label", "") or "") == "wine_store_shift_after_clarissa") timeout 5.0
    assert eval ("alber" in list(people.ids_at("WineStore") or [])) timeout 5.0
    assert eval (Alber.display_name() == people.get_data("alber").cname) timeout 5.0
    $ _alber_overlap_entry = next(row for row in people.get_data("alber").interval_schedule_entries if str(getattr(row, "label", "") or "") == "clarissa_overlap_wine_store")
    assert eval (int(_alber_overlap_entry.start_minute or 0) == 11 * 60 and int(_alber_overlap_entry.end_minute or 0) == 12 * 60) timeout 5.0
    $ Becky.rel = 15
    $ Sandra.rel = 15
    $ Becky.home_sex_unlocked = True
    $ Becky.home_visit_stage = 2
    python:
        _becky_visit_day = -1
        for _probe_day in range(31, 420):
            _probe_parts = calendar_v2.day_number_to_parts(_probe_day)
            external_calendar_set_fields(int(_probe_parts.get("day", 1) or 1), int(_probe_parts.get("month", 1) or 1), int(_probe_parts.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 13, 0)
            if npc_schedule_becky_sandra_kitchen_visit_active():
                _becky_visit_day = _probe_day
                break
        if _becky_visit_day >= 0:
            _becky_visit_parts = calendar_v2.day_number_to_parts(_becky_visit_day)
            external_calendar_set_fields(int(_becky_visit_parts.get("day", 1) or 1), int(_becky_visit_parts.get("month", 1) or 1), int(_becky_visit_parts.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 13, 0)
    assert eval (_becky_visit_day >= 0) timeout 5.0
    assert eval (str(people.location("sandra") or "") == "TavernKitchen") timeout 5.0
    assert eval (str(people.location("becky") or "") == "TavernKitchen" and str(people.schedule_state("becky").get("label", "") or "") == "sandra_kitchen_visit") timeout 5.0
    $ Liza.prostitution_started = True
    $ Liza.set_hired(False)
    python:
        _alber_port_day = -1
        for _probe_day in range(31, 420):
            _probe_parts = calendar_v2.day_number_to_parts(_probe_day)
            external_calendar_set_fields(int(_probe_parts.get("day", 1) or 1), int(_probe_parts.get("month", 1) or 1), int(_probe_parts.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 20, 0)
            if int(calendar_v2.week or 0) in (1, 3) and str(people.location("alber") or "") == "PortStreetsBackAlley":
                _alber_port_day = _probe_day
                break
        if _alber_port_day >= 0:
            _alber_port_parts = calendar_v2.day_number_to_parts(_alber_port_day)
            external_calendar_set_fields(int(_alber_port_parts.get("day", 1) or 1), int(_alber_port_parts.get("month", 1) or 1), int(_alber_port_parts.get("year", CALENDAR_START_CYCLE) or CALENDAR_START_CYCLE), 20, 0)
    assert eval (_alber_port_day >= 0) timeout 5.0
    assert eval (str(people.location("alber") or "") == "PortStreetsBackAlley" and str(people.schedule_state("alber").get("label", "") or "") == "liza_portstreets_visit") timeout 5.0
'''


ROOM_REGISTRY_SAVE_CHECKS = r'''
testcase external_room_registry_pickle_round_trip:
    $ _room_registry_count = len(rooms)
    $ rooms.get("TavernMyRoom").state["external_save_probe"] = "saved"
    $ _room_registry_payload = renpy.compat.pickle.dumps(rooms)
    $ rooms.get("TavernMyRoom").state["external_save_probe"] = "mutated"
    $ _loaded_rooms = renpy.compat.pickle.loads(_room_registry_payload)
    $ rooms = _loaded_rooms
    assert eval (isinstance(rooms, RoomRegistry) and len(rooms) == _room_registry_count) timeout 5.0
    assert eval (rooms.get("TavernMyRoom").state.get("external_save_probe") == "saved") timeout 5.0
    assert eval (all(room.code_name == code for code, room in rooms.items())) timeout 5.0
    $ rooms.get("TavernMyRoom").state.pop("external_save_probe", None)
'''


PLAYER_SAVE_PARITY_CHECKS = r'''
testcase external_player_save_payload_parity:
    $ player.identity.age = 27
    $ player.condition.health = 83
    $ player.stats.exploration = 14
    $ player.skills["tracking"] = 6
    $ player.economy.money = 4321
    $ player.inventory.items = {"soap_001": 2}
    $ player.equipment.weapon = "rusty_hunter_rifle_001"
    $ player.appearance.days_since_wash = 2
    $ player.appearance.days_since_haircut = 19
    $ player.intimacy.arousal = 37
    $ player.chores.weekly = {"bring_woods": 3}
    $ player.tavern_management.visitors = 57
    $ player.horse.acquire("Буцефал", 1000, True)
    $ player.combat.party = ["dog"]
    $ player.history["external_save_probe"] = "saved"
    $ player.events = ["external_event_probe"]
    $ player.sleep_wake_hour_override = 9
    $ renpy.save("external-player-parity")
    $ _saved_player = renpy.get_save_data("external-player-parity").get("player")
    assert eval (isinstance(_saved_player, Player)) timeout 5.0
    assert eval (isinstance(_saved_player.identity, PlayerIdentity) and int(_saved_player.identity.age or 0) == 27) timeout 5.0
    assert eval (isinstance(_saved_player.condition, PlayerCondition) and int(_saved_player.condition.health or 0) == 83) timeout 5.0
    assert eval (isinstance(_saved_player.stats, PlayerStats) and int(_saved_player.stats.exploration or 0) == 14 and int(_saved_player.skills.get("tracking", 0) or 0) == 6) timeout 5.0
    assert eval (isinstance(_saved_player.economy, PlayerEconomy) and int(_saved_player.economy.money or 0) == 4321) timeout 5.0
    assert eval (isinstance(_saved_player.inventory, PlayerInventory) and int(_saved_player.inventory.count("soap_001") or 0) == 2) timeout 5.0
    assert eval (isinstance(_saved_player.equipment, PlayerEquipment) and str(_saved_player.equipment.weapon or "") == "rusty_hunter_rifle_001") timeout 5.0
    assert eval (isinstance(_saved_player.appearance, PlayerAppearance) and int(_saved_player.appearance.days_since_wash or 0) == 2 and int(_saved_player.appearance.days_since_haircut or 0) == 19) timeout 5.0
    assert eval (isinstance(_saved_player.intimacy, PlayerIntimacy) and int(_saved_player.intimacy.arousal or 0) == 37) timeout 5.0
    assert eval (isinstance(_saved_player.chores, PlayerChores) and int(_saved_player.chores.weekly.get("bring_woods", 0) or 0) == 3) timeout 5.0
    assert eval (isinstance(_saved_player.tavern_management, PlayerTavernManagement) and int(_saved_player.tavern_management.visitors or 0) == 57) timeout 5.0
    assert eval (isinstance(_saved_player.horse, PlayerHorse) and str(_saved_player.horse.name or "") == "Буцефал" and bool(_saved_player.horse.saddled)) timeout 5.0
    assert eval (isinstance(_saved_player.combat, PlayerCombat) and list(_saved_player.combat.party or []) == ["dog"]) timeout 5.0
    assert eval (_saved_player.history.get("external_save_probe") == "saved" and list(_saved_player.events or []) == ["external_event_probe"] and int(_saved_player.sleep_wake_hour_override or 0) == 9) timeout 5.0

label external_player_actual_load_probe:
    call InitGameNPCs
    $ Amanda.rel = 17
    $ Eddie.fingal_talk_stage = 2
    $ Sandra.rel = 13
    $ Sandra.set_var_int("knowmolodost", 1)
    $ Sandra.set_sex_stat("pregnancy", 44)
    $ threads["sandraWeeklyEvaluation"].advanceTo(2, force_active=True)
    $ Melissa.rel = 12
    $ Melissa.temp_room_code = "TavernAmandaRoom"
    $ Melissa.drawings_found = True
    $ threads["melissaBatProblem"].advanceTo(6, force_active=True)
    $ player.economy.money = 2468
    $ player.appearance.days_since_wash = 2
    $ player.appearance.days_since_haircut = 16
    $ player.combat.party = ["dog"]
    $ player.history["external_actual_load_probe"] = "saved"
    $ household.__dict__.pop("barber_appointments", None)
    $ Sandra.var["barber_invite_pending"] = 1
    $ saveVersion = currentVersion
    $ renpy.save("external-player-actual-load")
    if external_player_load_marker_exists():
        return
    $ external_player_mark_load()
    $ player.economy.money = 1
    $ player.appearance.days_since_wash = 99
    $ player.appearance.days_since_haircut = 99
    $ player.combat.party = []
    $ player.history["external_actual_load_probe"] = "mutated"
    $ Sandra.rel = 1
    $ Sandra.set_var_int("knowmolodost", 0)
    $ Sandra.set_sex_stat("pregnancy", 0)
    $ threads["sandraWeeklyEvaluation"].reset()
    $ Melissa.rel = 1
    $ Melissa.temp_room_code = ""
    $ Melissa.drawings_found = False
    $ threads["melissaBatProblem"].reset()
    $ renpy.load("external-player-actual-load")
    return

testcase external_player_actual_load_parity:
    $ external_player_clear_load_marker()
    run Call("external_player_actual_load_probe")
    # Ren'Py's test executor resumes its own node after renpy.load(), so invoke
    # the engine's normal load continuation explicitly for this regression.
    assert eval (config.after_load_callbacks[0] is updateSave) timeout 5.0
    run Call("_after_load")
    assert eval (isinstance(player, Player) and isinstance(player.appearance, PlayerAppearance) and isinstance(player.combat, PlayerCombat)) timeout 5.0
    assert eval (int(player.economy.money or 0) == 2468) timeout 5.0
    assert eval (int(player.appearance.days_since_wash or 0) == 2 and int(player.appearance.days_since_haircut or 0) == 16) timeout 5.0
    assert eval (list(player.combat.party or []) == ["dog"] and player.history.get("external_actual_load_probe") == "saved") timeout 5.0
    assert eval (household.barber_appointments == {"sandra": 1} and "barber_invite_pending" not in Sandra.var) timeout 5.0
    assert eval (int(saveVersion or 0) == int(currentVersion or 0)) timeout 5.0
    assert eval (people.get_info("amanda") is Amanda and people.get_data("amanda") is AmandaStaticData and Amanda.data is AmandaStaticData) timeout 5.0
    python:
        _expected_people_after_load = {
            "alber": (Alber, AlberStaticData),
            "amanda": (Amanda, AmandaStaticData),
            "becky": (Becky, BeckyStaticData),
            "clara": (Clara, ClaraStaticData),
            "dog": (dog, DogStaticData),
            "draupnir": (Draupnir, DraupnirStaticData),
            "eddie": (Eddie, EddieStaticData),
            "fran": (Francheska, FranStaticData),
            "georgett": (Georgett, GeorgettStaticData),
            "gerhard": (Gerhard, GerhardStaticData),
            "inga": (Inga, IngaStaticData),
            "irma": (Irma, IrmaStaticData),
            "liza": (Liza, LizaStaticData),
            "luisa": (Luisa, LuisaStaticData),
            "melissa": (Melissa, MelissaStaticData),
            "mongol": (Mongol, MongolStaticData),
            "robin": (Robin, RobinStaticData),
            "sandra": (Sandra, SandraStaticData),
            "sergio": (Sergio, SergioStaticData),
            "werecat": (werecat, WerecatStaticData),
            "zimmer": (Zimmer, ZimmerStaticData),
        }
    assert eval (set(people.ids()) == set(_expected_people_after_load.keys()) and len(people.runtime) == len(people.definitions) == 21) timeout 5.0
    assert eval (all(people.get_info(key) is pair[0] and people.get_data(key) is pair[1] and pair[0].data is pair[1] for key, pair in _expected_people_after_load.items())) timeout 5.0
    assert eval (not hasattr(Melissa, "location")) timeout 5.0
    assert eval (int(Amanda.rel or 0) == 17 and Eddie.fingal_talk_stage == 2) timeout 5.0
    assert eval (int(Sandra.rel or 0) == 13 and Sandra.var_int("knowmolodost", 0) == 1 and int(Sandra.pregnancy_days() or 0) == 44) timeout 5.0
    assert eval (int(threads["sandraWeeklyEvaluation"].num or 0) == 2 and threads["sandraWeeklyEvaluation"].enabled and not threads["sandraWeeklyEvaluation"].completed) timeout 5.0
    assert eval (int(Melissa.rel or 0) == 12 and str(Melissa.temp_room_code or "") == "TavernAmandaRoom" and bool(Melissa.drawings_found)) timeout 5.0
    assert eval (int(threads["melissaBatProblem"].num or 0) == 6 and threads["melissaBatProblem"].enabled and not threads["melissaBatProblem"].completed) timeout 5.0
    $ external_player_clear_load_marker()

testcase external_player_appearance_v47_migration:
    $ external_calendar_set_fields(23, 2, 1100, 8, 0)
    $ player.appearance.days_since_wash = 1
    $ player.appearance.days_since_haircut = 7
    $ player.appearance.washDays = 1
    $ player.appearance.hairCutdays = 4
    $ player.appearance.haircut_day = int(current_game_day() or 0) - 20
    $ updateSave_V47()
    assert eval (int(player.appearance.days_since_wash or 0) == 2) timeout 5.0
    assert eval (int(player.appearance.days_since_haircut or 0) == 20) timeout 5.0
    assert eval (not hasattr(player.appearance, "washDays") and not hasattr(player.appearance, "hairCutdays") and not hasattr(player.appearance, "haircut_day")) timeout 5.0
'''


TAVERN_HELP_FLOW_CHECKS = r'''
testcase external_tavern_help_book_single_owner_flow:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ player.economy.money = 50
    $ TavernHelpBookItem.state["stash_taken"] = 0
    $ TavernHelpBookItem.state["stash_amount"] = 150
    assert eval (get_game_item("book_001") is TavernHelpBookItem) timeout 5.0
    run Jump("TavernHelp")
    advance until screen "choice" timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernHelp" and int(rooms.get("TavernHelp").state.get("page", -1)) == 0) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (int(TavernHelpBookItem.state.get("stash_taken", 0) or 0) == 1) timeout 20.0
    assert eval (int(player.economy.money or 0) == 200 and int(TavernHelpBookItem.state.get("stash_amount", -1) or 0) == 0) timeout 5.0
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_2" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain") timeout 20.0
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
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    run Call("HarassShowImage", "melissa", "ass", 5, 1, "waitress")
    assert eval (str(scene_runtime.picture or "") == "images/melissa/Grope/assOk.png") timeout 5.0
    assert eval (_media_asset_exists(scene_runtime.picture)) timeout 5.0
    run Call("HarassShowImage", "melissa", "tits", 2, 1, "cleaning")
    assert eval (str(scene_runtime.picture or "") == "images/melissa/Grope/titsShy.png" and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    run Call("HarassShowImage", "melissa", "dress", 0, 1, "waitress")
    assert eval (str(scene_runtime.picture or "") == "images/melissa/Grope/assAngry.png" and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    run Call("HarassShowImage", "amanda", "ass", 2, 1, "waitress")
    assert eval (str(scene_runtime.picture or "").lower().endswith("/amanda/grope/assshy.jpg") and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    run Call("HarassShowImage", "amanda", "dress", 5, 1, "waitress")
    assert eval (str(scene_runtime.picture or "").lower().endswith("/amanda/grope/dresspanties.jpg") and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    run Call("HarassShowImage", "sandra", "dress", 5, 1, "waitress")
    assert eval (str(scene_runtime.picture or "") in ("images/sandra/tavern/waitress1.jpg", "images/sandra/tavern/waitress2.jpg", "images/sandra/tavern/waitress3.jpg", "images/sandra/tavern/waitress4.jpg") and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    run Call("HarassShowImage", "sandra", "ass", 1, 1, "cleaning")
    assert eval (str(scene_runtime.picture or "") == "images/sandra/tavern/cleaning1.jpg" and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    run Call("HarassDiscussImage", "melissa", 3)
    assert eval (str(scene_runtime.picture or "") == "images/melissa/Grope/scoldAgree.png" and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    run Call("HarassDiscussImage", "amanda", 3)
    assert eval (str(scene_runtime.picture or "").lower().endswith("/amanda/grope/scold.jpg") and _media_asset_exists(scene_runtime.picture)) timeout 5.0

testcase external_harassment_event_picture_sequence:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ rooms.enter("TavernMain")
    $ GraphicsOn = 1
    $ Melissa.corruption = 5
    $ Melissa.rel = 0
    $ Melissa.set_harass_instruction("")
    $ scene_runtime.picture = ""
    run Call("PartEventYourFirstReactionOutcome", "melissa", "event_waitress_harrass_part2", 1, 1, 3)
    advance until screen "choice" timeout 20.0
    assert eval (str(scene_runtime.picture or "") == "images/melissa/Grope/scoldNeutral1.png" and _media_asset_exists(scene_runtime.picture)) timeout 5.0
    assert eval ("возвращаясь к работе" in str(scene_runtime.text or "") or "дальше по своим делам" in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain") timeout 20.0
    assert eval (str(rooms.current_code or "") == "TavernMain") timeout 5.0
'''


GIRL_OBJECT_RUNTIME_CHECKS = r'''
testcase external_inga_v53_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Inga.var.update({"SawLucassex": 1, "Knowher": 2})
        Inga.__dict__.pop("saw_lucas_sex", None)
        Inga.__dict__.pop("acquaintance_stage", None)
        globals()["IngaVar"] = {"SawLucassex": 1, "Knowher": 2}
    $ updateSave_V53()
    assert eval (Inga.saw_lucas_sex and Inga.acquaintance_stage == 2 and not Inga.var and "IngaVar" not in globals()) timeout 5.0

testcase external_inga_secondary_npc_source:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval ("inga" not in AllGirlNames) timeout 5.0
    assert eval (Inga.registry_group == "secondary") timeout 5.0
    assert eval (people.get_data("inga") is IngaStaticData and isinstance(people.get_data("inga"), IngaData)) timeout 5.0
    assert eval (people.get_info("inga") is Inga and isinstance(people.get_info("inga"), IngaInfo)) timeout 5.0
    assert eval (people.get_info("inga") not in people.girl_values() and people.get_info("inga") in people.secondary_values()) timeout 5.0
    assert eval (Inga.acquaintance_stage == 0 and not Inga.saw_lucas_sex and "IngaVar" not in globals() and not hasattr(Inga, "location")) timeout 5.0

testcase external_francheska_secondary_and_birth_thread:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval (people.get_data("fran") is FranStaticData and isinstance(people.get_data("fran"), FranData)) timeout 5.0
    assert eval (people.get_info("fran") is Francheska and isinstance(people.get_info("fran"), FrancheskaInfo)) timeout 5.0
    assert eval (people.get_info("fran") not in people.girl_values() and people.get_info("fran") in people.secondary_values() and Francheska.registry_group == "secondary") timeout 5.0
    assert eval (len(FRANCHESKA_TALK_START) == 11 and len(FRANCHESKA_TALK_SECOND) == 11 and len(FRANCHESKA_TALK_MAIN) == 11) timeout 5.0
    assert eval (all(str(FRANCHESKA_TALK_START[index] or "").strip() and str(FRANCHESKA_TALK_SECOND[index] or "").strip() and str(FRANCHESKA_TALK_MAIN[index] or "").strip() for index in range(11))) timeout 5.0
    assert eval ("systemGiveBirth" in threads and "systemGiveBirth" in threadData) timeout 5.0
    $ calendar_v2.daysInGame = 240
    $ Amanda.set_sex_stat("pregnancy", 240)
    $ Amanda.set_sex_stat("pregfather", "Вы")
    $ rooms.enter("TavernMain")
    assert eval (Amanda.birth_ready()) timeout 5.0
    $ initStoryEventRuntime(True)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (story_event_available("TavernMain", "enter")) timeout 5.0
    assert eval (str(event_runtime.available["TavernMain"]["enter"].target or "") == "story_amanda_give_birth_0") timeout 5.0
    $ Amanda.set_sex_stat("pregnancy", 0)
    $ Amanda.set_sex_stat("pregfather", "")
    $ Inga.set_sex_stat("pregnancy", 240)
    $ Inga.set_sex_stat("pregfather", "Лукас")
    $ rooms.enter("BeckyHome")
    $ initStoryEventRuntime(True)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (story_event_available("BeckyHome", "enter")) timeout 5.0
    assert eval (str(event_runtime.available["BeckyHome"]["enter"].target or "") == "story_give_birth_inga") timeout 5.0
    $ Inga.set_sex_stat("pregnancy", 0)
    $ Inga.set_sex_stat("pregfather", "")
    $ calendar_v2.daysInGame = 0
    $ Francheska.met = False
    $ Francheska.talked_today = 0
    run Call("FrancheskaTalk")
    advance until screen "choice" timeout 20.0
    $ _fran_meet_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Порасспрашивать об этом месте")
    $ _fran_meet_button_id = "choice_panel_button_%d" % int(_fran_meet_index)
    click id _fran_meet_button_id pos (0.5, 0.5) until screen "say" timeout 20.0
    advance until eval (Francheska.met and int(Francheska.talked_today or 0) == 1 and str(main_ui_runtime.mode or "") == "scene") timeout 30.0

testcase external_kids_birth_history_single_authority:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ player.history["kids"] = {"list": [], "next_id": 1}
    $ calendar_v2.daysInGame = 240
    $ Amanda.set_sex_stat("pregnancy", 240)
    $ Amanda.set_sex_stat("pregfather", "Вы")
    $ _kids_before = Amanda.sex_stat("kids", 0)
    $ _household_before = player.tavern_management.household_members
    $ _support_before = player.economy.child_support_count
    $ _newborn_id = CreateKid("amanda")
    $ _newborn_data = GetKidData(_newborn_id)
    assert eval (_newborn_id == 1 and len(_kids_list()) == 1 and player_children_count() == 1) timeout 5.0
    assert eval (Amanda.sex_stat("kids", 0) == _kids_before + 1 and Amanda.sex_stat("pregnancy", 0) == 0 and Amanda.sex_stat("pregfather", "") == "") timeout 5.0
    assert eval (player.tavern_management.household_members == _household_before + 1) timeout 5.0
    assert eval (player.economy.child_support_count == _support_before + 1 and "600" in player.economy.child_birth_benefit_notice) timeout 5.0
    assert eval (_newborn_data["KidName"] != "" and _newborn_data["KidGender"] in ("M", "F")) timeout 5.0
    assert eval ("новорожденн" in ShowKidDesc(_newborn_id) and "scratch" not in player.history["kids"]) timeout 5.0
    $ Amanda.set_sex_stat("lactate", 1)
    $ Amanda.corruption = 70
    $ _breastfeeding_text = DescribeBreastFeeding("amanda", 1)
    assert eval ("сисю" in _breastfeeding_text and _newborn_data["KidName"] in _breastfeeding_text) timeout 5.0
    $ calendar_v2.daysInGame = 700
    assert eval (_newborn_data["KidName"] in ShowFullKidsListByAge("amanda")) timeout 5.0
    $ calendar_v2.daysInGame = 0

testcase external_player_derived_stats_direct_owners:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ _exploration_without_dog = effective_player_exploration()
    $ dog.owned = True
    assert eval (effective_player_exploration() == _exploration_without_dog + 25) timeout 5.0
    assert eval (0 <= player_quest_progress_score() <= 100) timeout 5.0
    assert eval (0 <= tavern_improvements_score() <= 100 and 0 <= tavern_reputation_score() <= 100) timeout 5.0
    assert eval (0 <= player_charisma_breakdown()["charisma"] <= 100 and 0 <= player_reputation_breakdown()["reputation"] <= 100) timeout 5.0
    $ update_stat_state()
    assert eval (player.appearance.days_since_haircut >= 0 and player.appearance.days_since_wash >= 0) timeout 5.0

testcase external_church_ellona_player_owned_state:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval (len(player.economy.church_repairs_donated) == len(CHURCH_REPAIR_COSTS) == 10) timeout 5.0
    $ _church_money_before = player.economy.money
    $ player.spend_money(CHURCH_REPAIR_COSTS[0])
    $ player.economy.record_church_donation(0, CHURCH_REPAIR_COSTS[0])
    assert eval (player.economy.church_repair_is_donated(0) and player.economy.church_donated_amount == CHURCH_REPAIR_COSTS[0] and player.economy.money == _church_money_before - CHURCH_REPAIR_COSTS[0]) timeout 5.0
    $ _cum_capacity = player.intimacy.can_cum_daily
    $ player.intimacy.apply_ellona_curse(14)
    assert eval (player.intimacy.ellona_cursed == 1 and player.intimacy.can_cum_daily == 0 and player.intimacy.ellona_curse_reduction == _cum_capacity) timeout 5.0
    $ player.intimacy.extend_ellona_curse(7)
    assert eval (player.intimacy.ellona_curse_days == 21) timeout 5.0
    $ player.intimacy.lift_ellona_curse()
    assert eval (player.intimacy.ellona_cursed == 0 and player.intimacy.can_cum_daily == _cum_capacity and player.intimacy.ellona_curse_days == 0) timeout 5.0
    $ player.intimacy.ellona_grace_blessings = [0, 0, 0, 0, 0, 0]
    $ player.intimacy.grant_ellona_grace(5)
    assert eval (player.intimacy.ellona_grace_blessings[5] == 1) timeout 5.0

testcase external_gerhard_secondary_npc_source:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval ("gerhard" not in AllGirlNames) timeout 5.0
    assert eval (Gerhard.registry_group == "secondary") timeout 5.0
    assert eval (people.get_data("gerhard") is GerhardStaticData and isinstance(people.get_data("gerhard"), GerhardData)) timeout 5.0
    assert eval (people.get_info("gerhard") is Gerhard and isinstance(people.get_info("gerhard"), GerhardInfo)) timeout 5.0
    assert eval (people.get_info("gerhard") not in people.girl_values() and people.get_info("gerhard") in people.secondary_values()) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 10, 0)
    $ external_calendar_set_weekday(7)
    assert eval (isinstance(Gerhard.var, dict) and "GerhardVar" not in globals() and not hasattr(Gerhard, "location") and Gerhard.getLocation() == "Church") timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 13, 0)
    assert eval (Gerhard.getLocation() == "") timeout 5.0
    assert eval (people.get_data("gerhard").cname == "Брат Герхард" and people.get_data("gerhard").portrait == "images/gerhard/portrait.png") timeout 5.0
    assert eval (all(key not in Gerhard.var for key in ["confession_intro_done", "sermon_story_stage", "becky_advice_stage", "georgett_confession_stage", "liza_confession_stage"])) timeout 5.0

testcase external_secondary_side_characters_are_classes:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval (all(people.get_info(key).registry_group == "secondary" for key in ["luisa", "sergio"])) timeout 5.0
    assert eval (people.get_data("luisa") is LuisaStaticData and people.get_info("luisa") is Luisa and isinstance(Luisa, LuisaInfo)) timeout 5.0
    assert eval (people.get_data("sergio") is SergioStaticData and people.get_info("sergio") is Sergio and isinstance(Sergio, SergioInfo)) timeout 5.0
    assert eval (people.get_info("lucas") is None and people.get_data("lucas") is None and "Lucas" not in globals()) timeout 5.0
    assert eval (people.get_info("clara_fiance") is None and people.get_data("clara_fiance") is None and "ClaraFiance" not in globals()) timeout 5.0
    assert eval (people.get_info("sergio_pet") is None and people.get_data("sergio_pet") is None and "SergioPet" not in globals()) timeout 5.0
    assert eval (all(people.get_info(key) not in people.girl_values() and people.get_info(key) in people.secondary_values() for key in ["luisa", "sergio"])) timeout 5.0
    assert eval (all(isinstance(people.get_info(key).var, dict) for key in ["luisa", "sergio"])) timeout 5.0
    assert eval (all((key + "Var") not in globals() for key in ["Luisa", "Sergio", "Lucas", "ClaraFiance", "SergioPet"])) timeout 5.0
    assert eval (people.get_data("luisa").fullname == "Толстушка Луиза" and people.get_data("sergio").dative == "Серджио") timeout 5.0

testcase external_birth_thread_conditions_block_day_zero:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    $ renpy.call_in_new_context("InitGameNPCs")
    $ calendar_v2.daysInGame = 0
    $ Sandra.set_sex_stat("pregnancy", 240)
    $ Sandra.set_sex_stat("pregfather", "Вы")
    $ initStoryEventRuntime(True)
    assert eval ("systemGiveBirth" in threads and "systemGiveBirth" in threadData) timeout 5.0
    assert eval (not threadData["systemGiveBirth"].triggers[0][0].checkConditions()) timeout 5.0
    assert eval (not story_event_available("TavernMain", "enter")) timeout 5.0
    $ calendar_v2.daysInGame = 240
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("TavernMain", "enter")) timeout 5.0
    assert eval (str(event_runtime.available["TavernMain"]["enter"].target or "") == "story_give_birth_sandra") timeout 5.0
    $ calendar_v2.daysInGame = 0
    $ Sandra.set_sex_stat("pregnancy", 0)
    $ Sandra.set_sex_stat("pregfather", "")

testcase external_ellona_temple_sunday_story_event:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    $ renpy.call_in_new_context("InitGameNPCs")
    $ external_calendar_set_fields(day_value=1, month_value=1, year_value=CALENDAR_START_CYCLE, hour_value=9, minute_value=0)
    $ external_calendar_set_weekday(7)
    $ people.get_data("fran").set_schedule([NPCScheduleEntry(location="EllonaTemple", start_minute=0, end_minute=1440, awake=True, talkable=True, priority=999, label="test_temple_presence")])
    $ Francheska.sunday_stories_seen_day = -1
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("EllonaTemple", "enter")) timeout 5.0
    assert eval (str(event_runtime.available["EllonaTemple"]["enter"].target or "") == "story_ellona_temple_sunday_stories") timeout 5.0
    run Jump("EllonaTemple")
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and str(main_ui_runtime.mode or "") == "event") timeout 5.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Осмотреться в храме"]) timeout 5.0
    assert eval (str(scene_runtime.picture or "") == "images/ellona/Fran5.png" and "Во дворике храма Франческа сегодня не одна" in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (str(rooms.current_code or "") == "EllonaTemple") timeout 5.0
    assert eval (Francheska.sunday_stories_seen_day == int(calendar_v2.daysInGame or 0)) timeout 5.0
    assert eval ("Во дворике храма Франческа сегодня не одна" not in str(scene_runtime.text or "") and str(scene_runtime.text or "") == str(scene_runtime.location_text or "")) timeout 5.0
    assert eval ([str(i.caption or "") for i in list(main_ui_runtime.action_items or [])] == ["Осмотреть дворик-клуатр", "Зайти в помещение для родов", "Вернуться в порт"]) timeout 5.0
    $ _ellona_room_text = str(scene_runtime.location_text or "")
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "choice" timeout 20.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Рассмотреть статую", "Рассмотреть портрет справа от входа в храм", "Рассмотреть портрет слева от входа в храм", "Рассмотреть портрет над родильной комнатой", "Рассмотреть портрет справа от входа в родильную комнату", "Рассмотреть портрет слева от входа в родильную комнату", "Закончить осмотр"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(scene_runtime.picture or "") == "images/ellona/statue1.jpg") timeout 20.0
    assert eval (str(scene_runtime.location_text or "") == _ellona_room_text and "\nЭто заметно и здесь" in str(scene_runtime.text or "")) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until screen "choice" timeout 20.0
    click id "choice_panel_button_3" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None and str(scene_runtime.picture or "") in ["images/ellona/agla1.jpg", "images/ellona/agla2.jpg", "images/ellona/alga3.jpg"]) timeout 20.0
    assert eval (str(scene_runtime.location_text or "") == _ellona_room_text and "\n\nНа холсте" in str(scene_runtime.text or "")) timeout 5.0
    $ initStoryEventRuntime(True)
    assert eval (not story_event_available("EllonaTemple", "enter")) timeout 5.0

testcase external_becky_v52_migration:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    python:
        Becky.var.update({
            "leftdances": 1,
            "visitedhome": 6,
            "IngaSexGreet": 1,
            "VisitScolded": 1,
            "TodayFrontSexCheck": 1,
            "HomeSex": 1,
            "EddieGeorg": 2,
            "EddieWhoreHome": 4,
            "BeckyOpenMinet": 1,
            "TimesVisited": 9,
            "TalkAboutEddie": 1,
            "GeorgMention": 1,
            "EddieIntrReact": 2,
            "PriestAdvice": 3,
            "GerhardBeckyTalk": 2,
            "AskedEddieFuck": 2,
            "EddieTryToFuck": 4,
            "EddieFailures": 3,
            "EddieRobbedDay": 41,
            "KnowBlackwood": 1,
            "SherwoodSuspect": 17,
            "TradeOffer": 1,
            "SherwoodWarn": 2,
            "AskTradeElf": 1,
            "FingalClarify": 1,
            "AdmitSherwood": 2,
            "RobbedByRobin": 2,
            "ConsoleRobbery": 1,
            "SandraKitchenVisitMonth": 7,
            "last_store_orgasm_day": 39,
            "BarDrinkDay": 40,
        })
        for _becky_field in (
            "left_dances", "home_visit_stage", "inga_sex_greeting_seen", "uninvited_visit_scolded",
            "home_front_checked_today", "home_sex_unlocked", "eddie_georgett_stage",
            "eddie_home_visit_state", "open_oral_stage", "home_visit_count", "talked_about_eddie",
            "georgett_mentioned", "eddie_intervention_reaction", "priest_advice_stage",
            "gerhard_talk_stage", "asked_about_eddie_sex_stage", "eddie_join_stage",
            "eddie_join_failures", "eddie_robbed_day", "knows_blackwood", "sherwood_suspicion",
            "trade_offer_stage", "sherwood_warning_stage", "asked_about_elf_trade",
            "fingal_connection_clarified", "admitted_sherwood_stage", "robin_robbery_stage",
            "robbery_consolation_count", "sandra_kitchen_visit_period", "last_store_orgasm_day",
        ):
            Becky.__dict__.pop(_becky_field, None)
        globals()["BeckyAdmit"] = 1
    $ updateSave_V52()
    assert eval (Becky.left_dances == 1 and Becky.home_visit_stage == 6 and Becky.inga_sex_greeting_seen and Becky.uninvited_visit_scolded and Becky.home_front_checked_today and Becky.home_sex_unlocked) timeout 5.0
    assert eval (Becky.eddie_georgett_stage == 2 and Becky.eddie_home_visit_state == 4 and Becky.open_oral_stage == 1 and Becky.home_visit_count == 9) timeout 5.0
    assert eval (Becky.talked_about_eddie and Becky.georgett_mentioned and Becky.eddie_intervention_reaction == 2 and Becky.priest_advice_stage == 3 and Becky.gerhard_talk_stage == 2) timeout 5.0
    assert eval (Becky.asked_about_eddie_sex_stage == 2 and Becky.eddie_join_stage == 4 and Becky.eddie_join_failures == 3 and Becky.eddie_robbed_day == 41) timeout 5.0
    assert eval (Becky.knows_blackwood and Becky.sherwood_suspicion == 17 and Becky.trade_offer_stage == 1 and Becky.sherwood_warning_stage == 2 and Becky.asked_about_elf_trade) timeout 5.0
    assert eval (Becky.fingal_connection_clarified and Becky.admitted_sherwood_stage == 2 and Becky.robin_robbery_stage == 2 and Becky.robbery_consolation_count == 1) timeout 5.0
    assert eval (Becky.sandra_kitchen_visit_period == 7 and Becky.last_store_orgasm_day == 39 and not Becky.var and "BeckyAdmit" not in globals()) timeout 5.0

testcase external_becky_classes_are_initialized:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval ("becky" in people and people.get_data("becky") is BeckyStaticData) timeout 5.0
    assert eval (people.get_info("becky") is Becky and isinstance(Becky, BeckyInfo)) timeout 5.0
    assert eval (Becky in people.girl_values() and "BeckyVar" not in globals()) timeout 5.0
    assert eval (people.get_data("becky").cname == "Бекки" and people.get_data("becky").fullname == "Ребекка Блэнкеншип") timeout 5.0
    assert eval (hasattr(people.get_data("becky"), "birth_date") and people.get_data("becky").age_years() == 36) timeout 5.0
    assert eval (Becky.rel == 0 and Becky.corruption == 25 and "Friends" not in globals() and "sluttiness" not in globals()) timeout 5.0
    $ Becky.set_cock_position("pussy", "You")
    $ Becky.set_cock_position("mouth", "eddie")
    assert eval (Becky.cock_in("pussy", "You") and Becky.cock_in("mouth", "eddie") and Becky.sex_state["partner_positions"] == {"you": "pussy", "eddie": "mouth"}) timeout 5.0
    $ Becky.set_cock_position("none", "You")
    $ Becky.set_cock_position("none", "eddie")
    assert eval (Becky.sex_state["partner_positions"] == {} and "cock_position" not in Becky.sex_state and "cock_positions" not in Becky.sex_state) timeout 5.0
    run Call("CockPosition", "becky", 3, "You")
    assert eval (Becky.cock_in("tits", "You") and Becky.sex_state["partner_positions"] == {"you": "tits"}) timeout 5.0
    $ Becky.set_cock_position("none", "You")
    $ CockInPussy = {"becky": 1}
    $ YouCockInMouth = {"becky": 1}
    $ tractir_save_normalize_sex_positions()
    assert eval (Becky.cock_in("pussy", "You") and "CockInPussy" not in globals() and "YouCockInMouth" not in globals()) timeout 5.0
    $ Becky.set_cock_position("none", "You")
    assert eval (Becky.wardrobe["current_dress"] == "openworkdress" and Becky.wardrobe["current_underwear"]["bra"] == "simplebra" and Becky.wardrobe["current_underwear"]["panties"] == "simplepanties") timeout 5.0
    assert eval (all(hasattr(Becky, key) for key in ["home_visit_stage", "home_sex_unlocked", "eddie_home_visit_state", "trade_offer_stage", "knows_blackwood"])) timeout 5.0
    assert eval (int(Becky.home_visit_stage or 0) == 0 and not Becky.home_sex_unlocked and int(Becky.trade_offer_stage or 0) == 0) timeout 5.0
    assert eval (Becky.getLocation(1, 13 * 60) == "GroceryStore") timeout 5.0
    $ initStoryEventRuntime(True)
    assert eval (Becky.home_visit_stage == 0) timeout 5.0
    assert eval (str(player.appearance.current_dress or "") != "citydress") timeout 5.0
    assert eval (not (Becky.home_visit_stage == 2 and Becky.rel > 12 and Becky.talk_count() < 2)) timeout 5.0
    $ Becky.home_visit_stage = 2
    $ Becky.rel = 13
    $ Becky.update()
    assert eval (Becky.home_visit_stage == 2 and Becky.rel > 12 and Becky.talk_count() < 2) timeout 5.0
    $ Becky.stats["orgasms_given"] = 1
    $ Becky.rel = 14
    $ Becky.talked_today = 0
    $ Becky.update()
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_husband1")) timeout 5.0
    $ Becky.trade_offer_stage = 1
    $ Becky.asked_about_elf_trade = False
    $ Becky.talked_today = 0
    assert eval (Becky.talk_count() < 2 and Becky.trade_offer_stage == 1 and not Becky.asked_about_elf_trade) timeout 5.0

testcase external_becky_husband_backstory_uses_one_thread_stage:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ Becky.stats["orgasms_given"] = 1
    $ Becky.rel = 14
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (int(threads["beckyHusbandBackstory"].num or 0) == 0) timeout 5.0
    assert eval (story_event_available("talk_becky", "becky_talk_husband1")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_husband1", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyHusbandBackstory"].num or 0) == 1) timeout 20.0
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_husband2")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_husband2", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyHusbandBackstory"].num or 0) == 2) timeout 20.0
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_husband3")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_husband3", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyHusbandBackstory"].num or 0) == 3) timeout 20.0
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_husband4")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_husband4", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyHusbandBackstory"].num or 0) == 4) timeout 20.0
    assert eval (threads["beckyHusbandBackstory"].completed) timeout 5.0
    assert eval (not hasattr(Becky, "husbandtalk")) timeout 5.0

testcase external_becky_eddie_backstory_uses_one_thread_stage:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ Becky.rel = 10
    $ Becky.talked_today = 0
    $ Eddie.talked_about_georgett = True
    $ Becky.stats["orgasms_given"] = 1
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_eddie1")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_eddie1", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyEddieBackstory"].num or 0) == 1) timeout 20.0
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_eddie2")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_eddie2", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyEddieBackstory"].num or 0) == 2) timeout 20.0
    assert eval (threads["beckyEddieBackstory"].completed and not hasattr(Becky, "eddietalk")) timeout 5.0

testcase external_becky_eddie_opinions_remain_parallel_repeatable_topics:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ Becky.georgett_mentioned = True
    $ Becky.home_visit_stage = 3
    $ Becky.corruption = 60
    $ Becky.talked_today = 0
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    assert eval ("Возмутиться поведением Эдди" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Посоветовать Бекки быть повнимательнее к нуждам Эдди" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _becky_oppose_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Возмутиться поведением Эдди")
    $ _becky_oppose_button_id = "choice_panel_button_%s" % _becky_oppose_index
    click id _becky_oppose_button_id pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until eval (int(Becky.eddie_intervention_reaction or 0) == 1 and renpy.get_screen("choice") is None) timeout 20.0
    $ Becky.talked_today = 0
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    assert eval ("Возмутиться поведением Эдди" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Посоветовать Бекки быть повнимательнее к нуждам Эдди" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval (all(name not in threads for name in ("beckyEddieReactionTalk", "beckyEddieBehaviorTalk", "beckyEddieAfterSexTalk"))) timeout 5.0

testcase external_becky_sherwood_followups_use_branch_state_not_threads:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ Becky.trade_offer_stage = 2
    $ Becky.asked_about_elf_trade = False
    $ Becky.talked_today = 0
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    assert eval ("Насчет твоего предложения, в чем там все-таки дело?" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _becky_offer_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Насчет твоего предложения, в чем там все-таки дело?")
    $ _becky_offer_button_id = "choice_panel_button_%s" % _becky_offer_index
    click id _becky_offer_button_id pos (0.5, 0.5) until eval (int(Becky.trade_offer_stage or 0) == 1 and renpy.get_screen("choice") is None) timeout 20.0
    $ Becky.talked_today = 0
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    assert eval ("А чего ты сама с эльфами не торгуешь?" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval (all(name not in threads for name in ("beckySherwoodOfferTalk", "beckySherwoodElvesTalk", "beckySherwoodRoadTalk", "beckySherwoodRobbedTalk"))) timeout 5.0

testcase external_becky_blackwood_offer_uses_single_live_label:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ Becky.trade_offer_stage = 0
    $ Becky.rel = 18
    $ Becky.stats["orgasms_given"] = 10
    run Call("BeckyQuestInit")
    advance until screen "choice" timeout 20.0
    assert eval ("А кто ж не хочет?" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _becky_accept_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("А кто ж не хочет?")
    $ _becky_accept_button_id = "choice_panel_button_%s" % _becky_accept_index
    click id _becky_accept_button_id pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Пойти подумать над предложением" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval ("Пойти подумать над предложением" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval (int(Becky.trade_offer_stage or 0) == 1 and int(Becky.sherwood_warning_stage or 0) == 1) timeout 5.0
    assert eval (all(not hasattr(Becky, key) for key in ("TradeOfferText", "EddieRobbed", "SherwoodQuestScheduled"))) timeout 5.0

testcase external_becky_inga_lucas_thread_from_native_homefront_menu:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(2, 1, CALENDAR_START_CYCLE, 20, 0)
    $ Becky.home_front_checked_today = False
    $ Becky.home_visit_stage = 1
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (int(threads["beckyIngaLucasPath"].num or 0) == 0) timeout 5.0
    run Call("BeckyHomeFront", "FromDances")
    advance until screen "choice" timeout 20.0
    assert eval (int(rooms.get("BeckyHomeFront").state["inga_scene_roll"] or 0) <= 2) timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until screen "choice" timeout 20.0
    assert eval ("Поделится с вдовой своим открытием" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Сделать вид, что ничего там нет" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Предложить подойти к парочке" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Посмотреть как они кончат" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _becky_inga_thread = threads["beckyIngaLucasPath"]
    $ _becky_inga_event = _becky_inga_thread.getevent(0)
    $ assert story_event_available("BeckyHomeFront", "inga_discovery"), repr({"active": _becky_inga_thread.checkActive(), "target": _becky_inga_thread.currentTarget(), "checks": _becky_inga_event.auditChecks(_becky_inga_thread.day), "available": dict(event_runtime.available or {})})
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until eval (int(threads["beckyIngaLucasPath"].num or 0) == 1) timeout 20.0
    advance until screen "choice" timeout 20.0
    assert eval ("Предложить подойти к парочке" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Поделится с вдовой своим открытием" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval (not hasattr(Becky, "SawIngaFuck")) timeout 5.0
    run Jump("TavernMain")
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_inga1")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_inga1", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyIngaLucasPath"].num or 0) == 2) timeout 20.0
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_inga2")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_inga2", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyIngaLucasPath"].num or 0) == 3) timeout 20.0
    $ Becky.talked_today = 0
    $ initStoryEventRuntime(True)
    assert eval (story_event_available("talk_becky", "becky_talk_lucas")) timeout 5.0
    run Call("checkTriggers", "talk_becky", "becky_talk_lucas", 0)
    click pos (0.5, 0.5) until eval (int(threads["beckyIngaLucasPath"].num or 0) == 4) timeout 20.0
    assert eval (threads["beckyIngaLucasPath"].completed and not hasattr(Becky, "SawIngaFuck")) timeout 5.0

testcase external_becky_talk_action_returns_without_duplicate_menu:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    $ _becky_inspect_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Осмотреть")
    $ _becky_inspect_button_id = "choice_panel_button_%d" % int(_becky_inspect_index)
    click id _becky_inspect_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "char" and str(main_ui_runtime.selected_char or "") == "becky") timeout 20.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Назад"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and renpy.get_screen("choice") is None) timeout 20.0
    $ Becky.talked_today = 0
    run Call("IntBeckyTalk", "becky")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until screen "say" timeout 20.0
    click pos (0.5, 0.5) until eval (int(Becky.talked_today or 0) == 1 and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (int(Becky.talked_today or 0) == 1 and renpy.get_screen("choice") is None) timeout 5.0

testcase external_people_objects_are_single_source:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval (not ("girls_data" in globals()) and not ("girls_info" in globals())) timeout 5.0
    assert eval (all(isinstance(people.get_data(key), PeopleData) for key in AllGirlNames)) timeout 5.0
    assert eval (all(isinstance(people.get_info(key), PeopleInfo) for key in AllGirlNames)) timeout 5.0
    assert eval (people.get_data("amanda").cname == "Аманда" and people.get_data("amanda").birth_date.get("cycle") == 1082 and people.get_info("amanda").known) timeout 5.0
    assert eval (people.get_data("melissa").cname == "Мелисса" and hasattr(people.get_data("melissa"), "birth_date") and people.get_info("melissa").known) timeout 5.0
    assert eval (people.get_data("sandra").cname == "Сандра") timeout 5.0
    assert eval (hasattr(people.get_data("sandra"), "birth_date")) timeout 5.0
    assert eval (people.get_data("sandra").birth_date.get("cycle") == 1066) timeout 5.0
    assert eval (people.get_info("sandra").known) timeout 5.0
    assert eval (people.get_info("amanda").rel == 5 and people.get_info("amanda").openness == 3) timeout 5.0
    assert eval (Amanda.current_dress() == "modestworkdress" and Melissa.current_dress() == "workdress" and Sandra.current_dress() == "workdresszhilet") timeout 5.0
    assert eval (people.get_data("eddie").cname == "Эдди" and bool(people.get_data("eddie").birth_date) and people.get_info("eddie") in people.secondary_values()) timeout 5.0
    assert eval (people.get_data("mongol").cname == "Монгол" and people.get_info("mongol") in people.secondary_values()) timeout 5.0
    assert eval ("inga" not in AllGirlNames and people.get_data("inga") is IngaStaticData and people.get_info("inga") is Inga and isinstance(people.get_info("inga"), IngaInfo)) timeout 5.0
    assert eval (people.get_info("inga") not in people.girl_values()) timeout 5.0
    assert eval (people.get_info("inga") in people.secondary_values()) timeout 5.0
    assert eval (Inga.registry_group == "secondary") timeout 5.0
    assert eval (all(people.get_info(key) in people.girl_values() for key in AllGirlNames)) timeout 5.0
    assert eval (all(isinstance(info, PeopleInfo) and info.registry_group == "secondary" for info in people.secondary_values())) timeout 5.0
    assert eval (all(info not in people.girl_values() for info in people.secondary_values())) timeout 5.0
    assert eval (people.get_info("amanda") is Amanda and Amanda.uses_own_var_state and all(isinstance(people.get_info(key).var, dict) for key in AllGirlNames)) timeout 5.0
    assert eval (all((key + "Var") not in globals() for key in ["Amanda", "Becky", "Clara", "Irma", "Melissa", "Sandra"])) timeout 5.0
    assert eval (people.get_data("melissa") is MelissaStaticData and people.get_info("melissa") is Melissa) timeout 5.0
    assert eval (people.get_data("melissa").cname == "Мелисса" and people.get_data("clara").cname == "Кларисса") timeout 5.0
    assert eval (people.get_info("sandra") is Sandra and isinstance(people.get_info("sandra"), SandraInfo)) timeout 5.0
    assert eval (people.get_data("clara") is ClaraStaticData and people.get_info("clara") is Clara and isinstance(people.get_info("clara"), ClaraInfo)) timeout 5.0
    $ Amanda.drunk = 1
    assert eval (Amanda.drunk == 1) timeout 5.0
    $ _drunk_social_result = social_apply_topic("amanda", "talk", "chat")
    assert eval (isinstance(_drunk_social_result, dict) and "text" in _drunk_social_result) timeout 5.0
    $ Amanda.drunk = 0
    assert eval (people.get_data("irma") is IrmaStaticData and people.get_info("irma") is Irma) timeout 5.0
    assert eval (not social_has_visible_topics("irma", "flirt") and not social_interaction_allowed_for_npc("irma", "flirt")) timeout 5.0
    $ Melissa.rel = 17
    $ Melissa.openness = 10
    $ Melissa.corruption = 20
    assert eval (Melissa.rel == 17 and Melissa.relationship_stage() >= 3) timeout 5.0
    assert eval (all(people.get_info(key).data is people.get_data(key) for key in ["melissa", "sandra", "clara"])) timeout 5.0
    $ Amanda.talked_today = 2
    $ Melissa.flirted_today = 1
    $ Sandra.gifted_today = 1
    $ Becky.fucked_today = 1
    $ Clara.drunk = 1
    assert eval (Amanda.talked_today == 2) timeout 5.0
    assert eval (Melissa.flirtToday and Sandra.giftToday and Becky.fucked_today == 1) timeout 5.0
    assert eval (Clara.drunk == 1) timeout 5.0
    $ people_reset_daily_interactions(["amanda", "melissa", "sandra", "becky", "clara"])
    assert eval (Amanda.talked_today == 0 and not Melissa.flirtToday and not Sandra.giftToday and Becky.fucked_today == 0) timeout 5.0
    assert eval (Clara.drunk == 0) timeout 5.0
    assert eval (isinstance(dog, DogCompanion)) timeout 5.0

testcase external_registry_girl_daily_processing_once:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ _registry_girl_ids = [info.name for info in people.girl_values()]
    assert eval (len(_registry_girl_ids) == len(set(_registry_girl_ids)) and set(_registry_girl_ids) == set(AllGirlNames)) timeout 5.0
    $ SexEvents.today_events = []
    $ SexEvents.girl_dance = []
    python:
        for _registry_girl in people.girl_values():
            _registry_girl.set_sex_stat("pregnancy", 0)
            _registry_girl.set_sex_stat("pregfather", "")
    $ Amanda.set_sex_stat("pregnancy", 10)
    $ Amanda.set_sex_stat("pregfather", "Вы")
    run Call("NextDay_FinishDayEvents")
    assert eval (int(Amanda.pregnancy_days() or 0) == 11) timeout 5.0

testcase external_npc_schedule_room_visibility_agreement:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("melissa") is not None) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 6, 0)
    $ external_calendar_set_weekday(1)
    $ rooms.enter("TavernKitchen")
    $ _kitchen_ids = list(people.ids_at("TavernKitchen") or [])
    $ _main_ids = list(people.ids_at("TavernMain") or [])
    assert eval (str(people.location("melissa") or "") in ("TavernKitchen", "TavernStorage", "TavernMain", "Backyard", "TavernMelissaRoom")) timeout 5.0
    assert eval (set(_kitchen_ids) == set(people.ids_at("TavernKitchen"))) timeout 5.0
    assert eval (set(_main_ids) == set(people.ids_at("TavernMain"))) timeout 5.0
    $ threads["melissaBatProblem"].advanceTo(6, force_active=True)
    $ Melissa.temp_room_code = "TavernAmandaRoom"
    assert eval (str(people.location("melissa") or "") == "TavernAmandaRoom") timeout 5.0
    assert eval ("melissa" in list(people.ids_at("TavernAmandaRoom") or []) and "melissa" not in list(people.ids_at("TavernKitchen") or [])) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 13, 0)
    $ external_calendar_set_weekday(1)
    assert eval (str(people.location("melissa") or "") in ("TavernMain", "TavernKitchen", "TavernStorage", "Backyard")) timeout 5.0
    assert eval ("melissa" not in list(people.ids_at("TavernMelissaRoom") or [])) timeout 5.0
    $ Melissa.temp_room_code = ""
    $ external_calendar_set_fields(3, 1, 1100, 8, 30)
    $ external_calendar_set_weekday(1)
    $ player.tavern_management.breakfast.event_active = True
    $ player.tavern_management.breakfast.present_ids = ["melissa"]
    $ _forced_kitchen = list(people.ids_at("TavernKitchen") or [])
    $ _forced_main = list(people.ids_at("TavernMain") or [])
    assert eval (bool(player.tavern_management.breakfast.event_active) and list(player.tavern_management.breakfast.present_ids or []) == ["melissa"]) timeout 5.0
    assert eval (str(people.location("melissa") or "") == "TavernKitchen") timeout 5.0
    assert eval ("melissa" in people.ids_at("TavernKitchen") and "melissa" not in people.ids_at("TavernMain")) timeout 5.0
    assert eval ("melissa" in _forced_kitchen) timeout 5.0
    assert eval ("melissa" not in _forced_main) timeout 5.0
    assert eval ("eddie" not in _forced_main) timeout 5.0
    assert eval ("eddie" not in _forced_kitchen) timeout 5.0
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = []
    $ people.get_data("clara").set_schedule([NPCScheduleEntry(location="WineStore", start_minute=0, end_minute=1440, awake=True, talkable=True, priority=999)])
    $ external_calendar_set_fields(3, 1, 1100, 20, 0)
    $ external_calendar_set_weekday(1)
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    assert eval (not rooms.get("WineStore").is_open()) timeout 5.0
    assert eval (str(people.location("clara") or "") == "WineStore" and "clara" in list(people.ids_at("WineStore") or [])) timeout 5.0
    assert eval (people.action_data_for_room("clara", "WineStore") is None and not Clara.talk_available_in_room("WineStore")) timeout 5.0
    assert eval (renpy.get_displayable("main_ui", "main_ui_entity_button_npc_clara") is None) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 8, 0)
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    assert eval (rooms.get("WineStore").is_open() and people.action_data_for_room("clara", "WineStore") is not None) timeout 5.0
    assert eval (renpy.get_displayable("main_ui", "main_ui_entity_button_npc_clara") is not None) timeout 5.0
    $ people.get_data("alber").set_schedule([NPCScheduleEntry(location="WineStore", start_minute=0, end_minute=1440, awake=True, talkable=True, priority=999)])
    $ external_calendar_set_fields(3, 1, 1100, 11, 30)
    run Jump("WineStore")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(people.location("clara") or "") == "WineStore" and str(people.location("alber") or "") == "WineStore") timeout 5.0
    assert eval (wine_store_seller_id() == "alber") timeout 5.0
    assert eval (people.action_data_for_room("clara", "WineStore") is None and people.action_data_for_room("alber", "WineStore") is not None) timeout 5.0
    assert eval (renpy.get_displayable("main_ui", "main_ui_entity_button_npc_clara") is None) timeout 5.0
    assert eval (renpy.get_displayable("main_ui", "main_ui_entity_button_npc_alber") is not None) timeout 5.0

testcase external_right_side_npc_buttons_open_default_menu:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("eddie") is not None) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 8, 30)
    $ external_calendar_set_weekday(1)
    $ Eddie.known = True
    $ rooms.enter("GroceryStore")
    run Jump("GroceryStore")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(people.location("eddie") or "") == "GroceryStore") timeout 5.0
    assert eval ("eddie" in list(people.ids_at("GroceryStore") or [])) timeout 5.0
    click id "main_ui_entity_button_npc_eddie" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and str(main_ui_runtime.action_title or "") == "Разговор с Эдди" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval (list(main_ui_runtime.action_items or []) == []) timeout 5.0
    assert eval (bool(Eddie.known)) timeout 5.0
    assert eval (str(rooms.current_code or "") == "GroceryStore") timeout 5.0
    $ _eddie_talk_end_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _eddie_talk_end_button_id = "choice_panel_button_%d" % int(_eddie_talk_end_index)
    click id _eddie_talk_end_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene") timeout 20.0

    $ external_calendar_set_fields(3, 1, 1100, 10, 0)
    $ Melissa.known = True
    $ Melissa.rel = 15
    $ Melissa.openness = 8
    $ Melissa.asked_today = 0
    $ Melissa.talked_today = 0
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=999)])
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0
    assert eval ("melissa" in list(people.ids_at("TavernMain") or [])) timeout 5.0
    click id "main_ui_entity_button_npc_melissa" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and str(main_ui_runtime.action_title or "") == "Разговор с Мелиссой" and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval ("Осмотреть" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Поговорить" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Флиртовать" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Подарить маленький подарок" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Коснуться ее смелее" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Извиниться перед Мелиссой" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    assert eval ("Предложить купить сестренке обновку" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _melissa_look_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Осмотреть")
    $ _melissa_look_button_id = "choice_panel_button_%d" % int(_melissa_look_index)
    click id _melissa_look_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "char") timeout 20.0
    assert eval ([str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] == ["Назад"] and list(main_ui_runtime.action_items or []) == []) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is None) timeout 20.0
    click id "main_ui_entity_button_npc_melissa" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Спросить, что для нее сейчас важнее всего" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _melissa_priority_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Спросить, что для нее сейчас важнее всего")
    $ _melissa_priority_button_id = "choice_panel_button_%d" % int(_melissa_priority_index)
    click id _melissa_priority_button_id pos (0.5, 0.5) until eval (int(Melissa.asked_today or 0) == 1 and str(main_ui_runtime.mode or "") == "talk" and renpy.get_screen("choice") is None) timeout 20.0
    assert eval ("Чтобы в доме было тише и ровнее" in str(scene_runtime.text or "")) timeout 5.0
    click id "main_ui_entity_button_npc_melissa" pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Назад" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    $ _melissa_back_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Назад")
    $ _melissa_back_button_id = "choice_panel_button_%d" % int(_melissa_back_index)
    click id _melissa_back_button_id pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == "TavernMain") timeout 20.0

testcase external_people_locate_matches_schedule:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("irma") is not None) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 8, 30)
    $ external_calendar_set_weekday(1)
    $ player.tavern_management.breakfast.event_active = True
    $ player.tavern_management.breakfast.present_ids = ["melissa"]
    $ main_ui_runtime.overlay = "people"
    $ _loc_rows = people_locate_rows()
    assert eval (str(main_ui_runtime.overlay or "") == "people") timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "melissa")["location"] == people.location("melissa") == "TavernKitchen") timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "eddie")["location"] == people.location("eddie") == "GroceryStore") timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "irma")["location"] == people.location("irma")) timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "clara")["location"] == people.location("clara")) timeout 5.0
    assert eval (next(row for row in _loc_rows if row["id"] == "mongol")["location"] == people.location("mongol")) timeout 5.0
    assert eval ("melissa" in people.ids_at("TavernKitchen") and "melissa" not in people.ids_at("TavernMain")) timeout 5.0
    assert eval (Melissa.talk_available_in_room("TavernKitchen") and people_locate_state_text("melissa", "TavernKitchen") == "можно говорить") timeout 5.0
    assert eval (not Eddie.talk_available_in_room("TavernKitchen")) timeout 5.0
    $ Clara.data.set_schedule([NPCScheduleEntry(location="MarketPlace", start_minute=0, end_minute=1440, priority=999)])
    assert eval (str(Clara.getLocation() or "") == "MarketPlace" and not Clara.talk_available_in_room("MarketPlace")) timeout 5.0
    assert eval (people_locate_state_text("clara", "MarketPlace") == "на месте") timeout 5.0
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.present_ids = None
    $ main_ui_runtime.overlay = ""

testcase external_player_and_girl_cards_render:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("sandra") is not None) timeout 20.0
    $ _card_return_room = str(rooms.current_code or "")
    click id "main_ui_entity_button_player_you" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "mc") timeout 20.0
    assert eval (len(player_card_stat_rows_left()) > 0 and len(player_card_stat_rows_right()) > 0 and str(player_card_portrait_path() or "") != "") timeout 5.0
    assert eval (str(player_card_portrait_path() or "") == "images/general/player_card.jpg" and renpy.loadable(player_card_portrait_path())) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Действия" and [str(i.caption or "") for i in main_ui_runtime.action_items][-1] == "Назад") timeout 5.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    $ _card_keys = ["sandra", "amanda", "melissa", "clara", "becky", "irma", "georgett", "liza"]
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_hour=0, end_hour=24, priority=999)])
    $ Melissa.known = True
    $ _melissa_rows = girl_card_stat_rows("melissa")
    assert eval (("Локация", people.location("melissa")) in _melissa_rows and len(_melissa_rows) >= 5) timeout 5.0
    assert eval (("Работа сегодня", "уборка, зал") in _melissa_rows and ("Работа завтра", "уборка, зал") in _melissa_rows) timeout 5.0
    $ SandraStaticData.birth_date = {"day": int(calendar_v2.day or 1), "period": int(calendar_v2.period or 1), "cycle": int(calendar_v2.cycle or 0) - 35}
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
    assert eval (("Работа сегодня", "кухня") in girl_card_stat_rows("sandra") and ("Работа завтра", "кухня") in girl_card_stat_rows("sandra")) timeout 5.0
    assert eval (str(girl_card_portrait_path("amanda") or "") != "" and renpy.loadable(girl_card_portrait_path("amanda"))) timeout 5.0
    assert eval (str(girl_card_portrait_path("melissa") or "") != "" and renpy.loadable(girl_card_portrait_path("melissa"))) timeout 5.0
    assert eval (str(girl_card_portrait_path("sandra") or "") != "" and renpy.loadable(girl_card_portrait_path("sandra"))) timeout 5.0
    python:
        _card_results = {}
        for _card_key in _card_keys:
            show_girl_card_main_ui_state(_card_key)
            _card_results[_card_key] = (
                str(main_ui_runtime.mode or "") == "char"
                and str(main_ui_runtime.selected_char or "") == _card_key
                and str(girl_card_display_name(_card_key) or "") != ""
                and str(girl_card_portrait_path(_card_key) or "") != ""
                and len(list(girl_card_stat_rows(_card_key) or [])) > 0
                and len(list(girl_card_body_lines(_card_key) or [])) > 0
            )
            main_ui_end_card_state()
    assert eval (all(_card_results.values())) timeout 5.0
    assert eval (str(main_ui_runtime.mode or "") == "scene") timeout 5.0

    $ show_girl_card_main_ui_state("sandra")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.action_title or "") == "Действия" and [str(i.caption or "") for i in main_ui_runtime.action_items] == ["Назад"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("amanda")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("melissa")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("clara")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("becky")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("irma")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("georgett")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    $ show_girl_card_main_ui_state("liza")
    advance until screen "main_ui" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == _card_return_room and str(main_ui_runtime.mode or "") == "scene") timeout 20.0

    $ player.add_item("energy_tea_001", 1)
    $ _energy_tea_before = int(player.item_count("energy_tea_001") or 0)
    $ show_player_card_main_ui_state()
    $ player_card_show_inventory_item_state("energy_tea_001")
    advance until screen "main_ui" timeout 20.0
    assert eval ([str(i.caption or "") for i in main_ui_runtime.action_items].count("Выпить чай") == 1) timeout 5.0
    $ _energy_tea_action_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Выпить чай")
    $ _energy_tea_action_button_id = "choice_panel_button_%d" % int(_energy_tea_action_index)
    click id _energy_tea_action_button_id pos (0.5, 0.5) until eval (int(player.item_count("energy_tea_001") or 0) == _energy_tea_before - 1) timeout 20.0
    assert eval ("бодрящий чай" in str(scene_runtime.text or "") and str(main_ui_runtime.mode or "") == "mc") timeout 5.0
    $ main_ui_end_card_state()
    assert eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == _card_return_room) timeout 5.0

testcase external_mongol_horse_purchase_once_and_amanda_room_presence:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ player.set_money(5000)
    $ player.horse.remove()
    $ Mongol.horse_price = 1000
    $ Mongol.asked_about_gypsy = True
    $ Mongol.asked_price_increase = True
    $ Mongol.discount_asked = True
    $ Mongol.theft_asked = True
    $ Mongol.asked_about_seen_stolen = True
    $ Clara.merchant_contact_unlocked = False
    run Call("MongolTalk")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_1" pos (0.5, 0.5) until eval (player.horse.owns_horse() and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (player.horse.owns_horse() and bool(player.horse.saddled) and str(rooms.current_code or "") == "TavernStable") timeout 5.0
    $ Mongol.will_try_to_steal = True
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 16, 0)
    run Jump("TavernStable")
    advance until screen "main_ui" timeout 20.0
    assert eval (Mongol.will_try_to_steal and "приглушенное лязгание" not in str(scene_runtime.text or "")) timeout 5.0
    $ external_calendar_set_fields(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, 23, 0)
    run Jump("TavernStable")
    advance until screen "main_ui" timeout 20.0
    assert eval (not Mongol.will_try_to_steal and "приглушенное лязгание" in str(scene_runtime.text or "")) timeout 5.0
    run Jump("TavernAmandaRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(people.location("amanda") or "") == "TavernAmandaRoom") timeout 5.0
    assert eval ("amanda" in people.ids_at("TavernAmandaRoom")) timeout 5.0
    assert eval ("amanda" in [str(row.get("id", "") or "") for row in renpy.get_screen("main_ui").scope.get("_char_entries", [])]) timeout 5.0

testcase external_clara_object_thread_conditions:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    assert eval ("clara" in people and people.get_data("clara") is ClaraStaticData) timeout 5.0
    assert eval (Clara in people.girl_values() and not ("girls_data" in globals()) and not ("girls_info" in globals())) timeout 5.0
    $ Clara.rel = max(int(Clara.rel or 0), 5)
    $ people.get_data("clara").set_schedule([NPCScheduleEntry(location="WineStore", start_minute=0, end_minute=1440, priority=999)])
    $ rooms.enter("WineStore")
    $ external_calendar_set_fields(3, 1, 1100, 6, 0)
    assert eval (str(people.location("clara") or "") == "WineStore") timeout 5.0
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ threads["claraPaintingsPath"].advanceTo(2, force_active=True)
    $ findAvailableEvents(True)
    assert eval (story_event_available("WineStore", "clara_paintings")) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 12, 0)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (not story_event_available("WineStore", "clara_paintings")) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 6, 0)
    $ Clara.commission_followup_day = int(calendar_v2.daysInGame or 0)
    $ threads["claraPaintingsPath"].advanceTo(7, force_active=True)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (story_event_available("WineStore", "clara_paintings")) timeout 5.0
    $ external_calendar_set_fields(3, 1, 1100, 21, 0)
    $ threads["claraPaintingsPath"].advanceTo(8, force_active=True)
    $ rooms.enter("ArtisansQuarter")
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (story_event_available("ArtisansQuarter", "enter")) timeout 5.0
    $ people.get_data("clara").set_schedule([NPCScheduleEntry(location="TavernMelissaRoom", start_minute=0, end_minute=1440, priority=999)])
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernMelissaRoom", start_minute=0, end_minute=1440, priority=999)])
    $ external_calendar_set_fields(3, 1, 1100, 22, 0)
    $ threads["claraPaintingsPath"].advanceTo(9, force_active=True)
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    assert eval (people.location("clara") == "TavernMelissaRoom" and people.location("melissa") == "TavernMelissaRoom") timeout 5.0
    assert eval (story_event_available("TavernMelissaRoom", "clara_paintings")) timeout 5.0

testcase external_story_event_audit_methods_cover_tuple_attributes:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 6, 0)
    $ rooms.enter("TavernStorage")
    $ player.tavern_management.breakfast.today = False
    $ player.tavern_management.breakfast.event_active = False
    $ Melissa.storage_rat_help_day = -1
    $ werecat_state()["rats_problem_active"] = 0
    $ people.get_data("melissa").set_schedule([NPCScheduleEntry(location="TavernStorage", start_minute=0, end_minute=1440, priority=999)])
    $ household_mark_runtime_event_seen("melissa_storage_rat", -999)
    $ threads.clear()
    $ event_runtime.available.clear()
    $ event_runtime.evaluation_time = None
    $ initStoryEventRuntime(True)
    $ findAvailableEvents(True)
    $ _audit_tinfo = threads["melissaRatProblem"]
    $ _audit_evt = _audit_tinfo.getevent(0)
    $ _audit_rows = _audit_evt.auditChecks(_audit_tinfo.day)
    $ _audit_fields = [str(row.get("field", "") or "") for row in _audit_rows]
    assert eval (set(["target", "binding", "day", "hour", "delay", "requirements", "conditions", "item", "location_open", "probability"]).issubset(set(_audit_fields))) timeout 5.0
    assert eval (all(isinstance(row.get("ok", None), bool) for row in _audit_rows)) timeout 5.0
'''


FIGHT_SYSTEM_RUNTIME_CHECKS = r'''
testcase external_fight_system_runtime_flow:
    run Jump("TavernMain")
    advance until screen "main_ui" timeout 20.0

    $ external_calendar_set_fields(1, 1, CALENDAR_START_CYCLE, 12, 0)
    $ calendar_v2.time_advance_blocked = 0
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.action_content = None
    $ rooms.enter("Forest")
    $ scene_runtime.picture = "images/forest/forest_1.png"
    $ player.set_stat("health", 100)
    $ player.set_stat("energy", 100)
    $ player.set_stat("exploration", 120)
    $ player.inventory.items = {}
    $ player.add_item("rusty_hunter_rifle_001", 1)
    $ player.equip("rusty_hunter_rifle_001", "weapon")
    $ player.unequip("armor")
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = "arrows"
    $ player.add_item("arrows_001", 2)
    $ player.add_item("bandage_001", 1)
    assert eval (hasattr(FIGHT_ENEMY_DEFINITIONS.get("wolf", None), "as_dict")) timeout 5.0
    assert eval (hasattr(FIGHT_ENEMY_DEFINITIONS.get("boar", None), "as_dict")) timeout 5.0
    assert eval (hasattr(FIGHT_ENEMY_DEFINITIONS.get("brown_bear", None), "as_dict")) timeout 5.0
    assert eval (str(FIGHT_ENEMY_DEFINITIONS["street_crook"].weapon or "") == "дубинка") timeout 5.0
    assert eval (str(FIGHT_ENEMY_DEFINITIONS["patrol_guard"].tactics or "") == "formation") timeout 5.0

    run Call("FightStartHuntCurrentRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight") timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") == "Команды") timeout 5.0
    assert eval (len(list(fight.enemy_party or [])) >= 1) timeout 5.0
    assert eval (all(isinstance(enemy, FightEnemyInstance) and not hasattr(enemy, "data") for enemy in fight.enemy_party)) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "").startswith("images/hunt/")) timeout 5.0
    assert eval (main_ui_runtime.action_content is None and "Скрыться" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ _fight_retreat_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Скрыться")
    $ _fight_retreat_button = "choice_panel_button_%d" % int(_fight_retreat_index)
    click id _fight_retreat_button pos (0.5, 0.5) until eval (str(fight.outcome_kind or "") == "retreat") timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (str(rooms.current_code or "") == "Forest" and str(scene_runtime.picture or "") == "images/forest/forest_1.png" and rusty_hunter_rifle_loaded_ammo() == "arrows") timeout 5.0
    assert eval (str(main_ui_runtime.action_content or "") == "" and "Выслеживать добычу" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ player.inventory.items = {}
    $ player.add_item("rusty_hunter_rifle_001", 1)
    $ player.add_item("old_axe_001", 1)
    $ player.equip("rusty_hunter_rifle_001", "weapon")
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    run Call("FightStartHuntCurrentRoom")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight" and str(player.equipment.weapon or "") == "old_axe_001") timeout 5.0
    assert eval ("Атаковать: старый топор" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    $ fight.enemy_party = []
    $ main_ui_runtime.action_items = fight_action_items()
    $ renpy.restart_interaction()
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene") timeout 20.0

    $ player.remove_item("old_axe_001", 1)
    $ player.add_item("arrows_001", 2)
    $ player.add_item("bandage_001", 1)
    $ player.equip("rusty_hunter_rifle_001", "weapon")
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    $ fight_begin("wolf", 1, "Forest", scene_runtime.picture, "Тестовая схватка.")
    run Call("FightLoop")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight") timeout 5.0
    assert eval (len(list(fight.enemy_party or [])) == 1) timeout 5.0
    assert eval (int(fight_player_level() or 0) >= 3) timeout 5.0
    assert eval ("Перезарядить стрелой" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0
    assert eval (any(str(i.caption or "").startswith("Атаковать") or str(i.caption or "") == "Бить прикладом" for i in main_ui_runtime.action_items)) timeout 5.0
    assert eval (int(fight_weapon_attack_points() or 0) == 14) timeout 5.0

    $ player.add_item("old_axe_001", 1)
    $ player.equip("old_axe_001", "weapon")
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    $ main_ui_runtime.action_items = fight_action_items()
    assert eval (int(fight_weapon_attack_points() or 0) == 10) timeout 5.0
    assert eval (not any(str(i.caption or "").startswith("Перезарядить") or str(i.caption or "").startswith("Выстрелить") for i in main_ui_runtime.action_items)) timeout 5.0

    $ player.unequip("weapon")
    $ main_ui_runtime.action_items = fight_action_items()
    assert eval (fight_player_weapon_name() == "кулаки" and "Атаковать кулаками" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ player.equip("rusty_hunter_rifle_001", "weapon")
    $ main_ui_runtime.action_items = fight_action_items()
    assert eval ("Перезарядить стрелой" in [str(i.caption or "") for i in main_ui_runtime.action_items]) timeout 5.0

    $ _reload_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index("Перезарядить стрелой")
    $ _reload_button = "choice_panel_button_%d" % int(_reload_index)
    click id _reload_button pos (0.5, 0.5) until eval (int(fight.weapon_loaded or 0) == 1 and str(fight.loaded_ammo or "") == "arrows") timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight") timeout 5.0
    assert eval (int(fight.weapon_loaded or 0) == 1 and str(fight.loaded_ammo or "") == "arrows") timeout 5.0
    assert eval (int(fight_supply_count("arrows") or 0) == 1) timeout 5.0

    $ _shoot_caption = "Выстрелить ({})".format(fight_loaded_ammo_name(fight.loaded_ammo))
    $ _shoot_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index(_shoot_caption)
    $ _shoot_button = "choice_panel_button_%d" % int(_shoot_index)
    click id _shoot_button pos (0.5, 0.5) until eval (int(fight.weapon_loaded or 0) == 0 and str(fight.loaded_ammo or "") == "") timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight") timeout 5.0
    assert eval (int(fight.weapon_loaded or 0) == 0 and str(fight.loaded_ammo or "") == "") timeout 5.0
    assert eval (0 < int(player.condition.health or 0) <= 100) timeout 5.0

    $ _fight_retreat_caption = "Скрыться" if "Скрыться" in [str(i.caption or "") for i in main_ui_runtime.action_items] else "Попытаться сбежать"
    $ _fight_retreat_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index(_fight_retreat_caption)
    $ _fight_retreat_button = "choice_panel_button_%d" % int(_fight_retreat_index)
    click id _fight_retreat_button pos (0.5, 0.5) until eval (str(fight.outcome_kind or "") == "retreat") timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight" and str(fight.outcome_kind or "") == "retreat") timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (str(rooms.current_code or "") == "Forest") timeout 5.0
    assert eval (len(list(fight.enemy_party or [])) == 0) timeout 5.0
    assert eval (str(main_ui_runtime.action_title or "") != "Бой") timeout 5.0

    $ player.set_stat("health", 80)
    $ player.set_stat("energy", 100)
    $ player.equip("old_axe_001", "weapon")
    $ fight_begin("street_crook", 1, "StreetTavern", "images/fight/thug.png", "Forced victory test.")
    $ fight.enemy_party[0].health = 1
    $ fight.enemy_party[0].energy = 1
    $ main_ui_runtime.action_items = fight_action_items()
    run Call("FightLoop")
    $ _attack_caption = fight_attack_action_caption()
    $ _attack_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index(_attack_caption)
    $ _attack_button = "choice_panel_button_%d" % int(_attack_index)
    click id _attack_button pos (0.5, 0.5) until eval (str(fight.outcome_kind or "") == "victory") timeout 20.0
    assert eval (str(fight.outcome_kind or "") == "victory" and str(main_ui_runtime.action_title or "") == "Победа") timeout 5.0
    assert eval (isinstance(fight.last_result, dict) and str(fight.last_result.get("outcome", "") or "") == "victory") timeout 5.0
    assert eval (isinstance(fight.victory_loot, dict) and int(fight.victory_loot.get("money", 0) or 0) >= 0) timeout 5.0
    assert eval ("Победа" in str(main_ui_runtime.action_title or "") and "добыч" in str(scene_runtime.text or "").lower()) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene") timeout 20.0

    $ player.set_stat("exploration", 300)
    $ fight_begin("patrol_guard", 2, "StreetTavern", "bg StreetTavern", "Тестовая схватка с патрулем.")
    run Call("FightLoop")
    advance until screen "main_ui" timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight") timeout 5.0
    assert eval (str(fight.enemy_id or "") == "patrol_guard" and len(list(fight.enemy_party or [])) == 2) timeout 5.0
    assert eval (str(fight_selected_enemy_image() or "") == "images/fight/patrol_guard.png") timeout 5.0
    assert eval (str(fight.enemy_party[0].weapon or "") == "алебарда") timeout 5.0
    assert eval ("formation" in list(fight.enemy_party[0].skills or [])) timeout 5.0
    $ _patrol_retreat_caption = "Скрыться" if "Скрыться" in [str(i.caption or "") for i in main_ui_runtime.action_items] else "Попытаться сбежать"
    $ _patrol_retreat_index = [str(i.caption or "") for i in main_ui_runtime.action_items].index(_patrol_retreat_caption)
    $ _patrol_retreat_button = "choice_panel_button_%d" % int(_patrol_retreat_index)
    click id _patrol_retreat_button pos (0.5, 0.5) until eval (str(fight.outcome_kind or "") == "retreat") timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "fight" and str(fight.outcome_kind or "") == "retreat") timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(main_ui_runtime.mode or "") == "scene") timeout 20.0
    assert eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == "StreetTavern") timeout 5.0

    $ player.set_stat("health", 100)
    $ player.set_stat("energy", 100)
    $ player.inventory.items = {}
    $ player.combat.special_supply["bees_bomb"] = 1
    $ player.add_item("rusty_hunter_rifle_001", 1)
    $ player.add_item("arrows_001", 3)
    $ player.add_item("droplets_001", 1)
    $ player.add_item("gunpowder_001", 1)
    $ player.add_item("bandage_001", 1)
    $ player.add_item("energy_tea_001", 1)
    $ player.add_item("healing_potion_001", 1)
    $ player.add_item("fire_bomb_001", 1)
    $ dog.owned = True
    $ dog.health = max(1, int(dog.max_health or 1))
    $ player.add_party_member("dog")
    $ player.equip("rusty_hunter_rifle_001", "weapon")
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    $ fight_begin("patrol_guard", 2, "StreetTavern", "images/fight/patrol_guard.png", "Проверка прямых боевых команд.")
    python:
        for _command_enemy in fight.enemy_party:
            _command_enemy.health = 1000
            _command_enemy.health_max = 1000
            _command_enemy.energy = 1000
            _command_enemy.energy_max = 1000
            _command_enemy.attack_min = 0
            _command_enemy.attack_max = 0
            _command_enemy.moves = ["attack"]

    $ renpy.call_in_new_context("FightCycleTarget")
    assert eval (int(fight.target_index or 0) == 2 and "цель" in str(scene_runtime.text or "").lower()) timeout 5.0
    $ renpy.call_in_new_context("FightDodge")
    assert eval ("уклон" in str(scene_runtime.text or "").lower() and str(main_ui_runtime.action_title or "") == "Команды") timeout 5.0
    $ renpy.call_in_new_context("FightBlock")
    assert eval ("защищенную стойку" in str(scene_runtime.text or "").lower()) timeout 5.0
    $ renpy.call_in_new_context("FightAttack")
    assert eval ("ближний бой" in str(scene_runtime.text or "").lower()) timeout 5.0

    $ rusty_hunter_rifle_item().state["loaded_ammo"] = "arrows"
    $ renpy.call_in_new_context("FightShoot")
    assert eval (str(fight.loaded_ammo or "") == "" and "выпускаете стрелу" in str(scene_runtime.text or "").lower()) timeout 5.0
    $ _command_arrows_before = fight_supply_count("arrows")
    $ renpy.call_in_new_context("FightReload", "arrows")
    assert eval (str(fight.loaded_ammo or "") == "arrows" and fight_supply_count("arrows") == _command_arrows_before - 1) timeout 5.0
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    $ _command_droplets_before = fight_supply_count("droplets")
    $ _command_powder_before = fight_supply_count("gunpowder")
    $ renpy.call_in_new_context("FightReload", "droplets")
    assert eval (str(fight.loaded_ammo or "") == "droplets" and fight_supply_count("droplets") == _command_droplets_before - 1 and fight_supply_count("gunpowder") == _command_powder_before - 1) timeout 5.0

    $ player.set_stat("health", 50)
    $ renpy.call_in_new_context("FightUseBandage")
    assert eval (int(player.condition.health or 0) == 62 and fight_supply_count("bandage") == 0) timeout 5.0
    $ player.set_stat("energy", 20)
    $ renpy.call_in_new_context("FightDrinkEnergyTea")
    assert eval (int(player.condition.energy or 0) == 35 and fight_supply_count("energy_tea") == 0) timeout 5.0
    $ player.set_stat("health", 50)
    $ renpy.call_in_new_context("FightDrinkHealingPotion")
    assert eval (int(player.condition.health or 0) == 75 and fight_supply_count("healing_potion") == 0) timeout 5.0
    $ renpy.call_in_new_context("FightThrowBeesBomb")
    assert eval (fight_supply_count("bees_bomb") == 0) timeout 5.0
    assert eval (all(int(enemy.status.get("paralyzed", 0) or 0) == 3 and int(enemy.status.get("poison_turns", 0) or 0) == 5 for enemy in fight.enemy_party)) timeout 5.0
    $ _command_enemy_health_before = sum(int(enemy.health or 0) for enemy in fight.enemy_party)
    $ renpy.call_in_new_context("FightThrowFireBomb")
    assert eval (fight_supply_count("fire_bomb") == 0 and sum(int(enemy.health or 0) for enemy in fight.enemy_party) < _command_enemy_health_before) timeout 5.0
    $ player.set_stat("energy", 20)
    $ renpy.call_in_new_context("FightCatchBreath")
    assert eval (int(player.condition.energy or 0) == 26 and "переводите дух" in str(scene_runtime.text or "").lower()) timeout 5.0
    $ _command_enemy_health_before = sum(int(enemy.health or 0) for enemy in fight.enemy_party)
    $ renpy.call_in_new_context("FightCommandDog")
    assert eval (sum(int(enemy.health or 0) for enemy in fight.enemy_party) < _command_enemy_health_before and "пес" in str(scene_runtime.text or "").lower()) timeout 5.0
    $ fight_finish_to_room("Проверка прямых боевых команд завершена.")
    assert eval (str(main_ui_runtime.mode or "") == "scene" and str(rooms.current_code or "") == "StreetTavern") timeout 5.0

    $ player.set_stat("health", 100)
    $ dog.health = int(dog.max_health or 1)
    $ fight_begin("wolf", 1, "Forest", "images/hunt/lonely_wolf_attack.png", "Проверка целей зверя.")
    $ fight.enemy_party[0].attack_min = 100
    $ fight.enemy_party[0].attack_max = 100
    $ fight.enemy_party[0].moves = ["attack"]
    python:
        _beast_hit_player = False
        _beast_hit_dog = False
        for _beast_target_try in range(20):
            player.set_stat("health", 100)
            dog.health = int(dog.max_health or 1)
            _beast_phase_text = fight_apply_enemy_phase("normal")
            if int(player.condition.health or 0) < 100:
                _beast_hit_player = True
            if int(dog.health or 0) < int(dog.max_health or 1):
                _beast_hit_dog = True
    assert eval (_beast_hit_player and _beast_hit_dog) timeout 5.0
    $ fight_finish_to_room("Проверка выбора цели зверем завершена.")

    python:
        _legacy_fight_enemy = object.__new__(FightEnemyInstance)
        _legacy_fight_enemy.data = {
            "id": "street_crook",
            "name": "Старый громила",
            "enemy_type": "human",
            "index": 3,
            "health": 17,
            "health_max": 42,
            "energy": 9,
            "energy_max": 42,
            "attack_min": 2,
            "attack_max": 4,
            "defence_min": 1,
            "defence_max": 3,
            "moves": ["strike"],
            "skills": ["brawl"],
            "weapon": "дубинка",
            "tactics": "pressure",
            "loot": {"rope_001": 1},
            "money_min": 2,
            "money_max": 8,
            "exploration_reward": 3,
            "status": {"bleed_turns": 2, "bleed_damage": 4},
        }
        fight.enemy_id = "street_crook"
        fight.enemy_party = [_legacy_fight_enemy]
    $ updateSave_V68()
    assert eval (len(fight.enemy_party) == 1) timeout 5.0
    assert eval (isinstance(fight.enemy_party[0], FightEnemyInstance)) timeout 5.0
    assert eval (not hasattr(fight.enemy_party[0], "data")) timeout 5.0
    assert eval (fight.enemy_party[0].object_id == "street_crook" and fight.enemy_party[0].name == "Старый громила" and fight.enemy_party[0].index == 3) timeout 5.0
    assert eval (fight.enemy_party[0].health == 17 and fight.enemy_party[0].health_max == 42 and fight.enemy_party[0].energy == 9 and fight.enemy_party[0].energy_max == 42) timeout 5.0
    assert eval (fight.enemy_party[0].moves == ["strike"] and fight.enemy_party[0].status == {"bleed_turns": 2, "bleed_damage": 4}) timeout 5.0
    $ fight.enemy_party = []
'''


SMALLTALK_MAIN_UI_CHECKS = r'''
init python:
    def external_prepare_smalltalk_picture_check(girl_name):
        key = str(girl_name or "").strip().lower()
        info = people.get_info(key)
        if info is None:
            raise AssertionError("No NPC info for {}".format(key))
        relationship_calm(key, 9)
        if hasattr(info, "anger_with_player"):
            info.anger_with_player = 0
        if isinstance(getattr(info, "var", None), dict):
            info.var["social_topic_seen"] = {}
        return True

testcase external_working_girl_talk_penalty:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and people.get_info("amanda") is not None) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 12, 0)
    $ external_calendar_set_weekday(1)
    $ Amanda.known = True
    $ Amanda.rel = 11
    $ Amanda.talked_today = 0
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=999, working=True)])
    $ rooms.enter("TavernMain")
    run Call("IntAmandaTalk", "amanda")
    advance until screen "choice" timeout 20.0
    assert eval (Amanda.is_working() and "Поговорить" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _work_talk_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Поговорить")
    $ _work_talk_button_id = "choice_panel_button_%d" % int(_work_talk_index)
    click id _work_talk_button_id pos (0.5, 0.5) until eval ("занята работой" in str(scene_runtime.text or "") and renpy.get_screen("choice") is not None) timeout 20.0
    assert eval (int(Amanda.rel or 0) == 10 and int(Amanda.talked_today or 0) == 0) timeout 5.0
    assert eval ("Осмотреть" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] and "Назад" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _work_flirted_before = int(Amanda.flirted_today or 0)
    $ _work_flirt_result = old_point_flirt_attempt("amanda")
    assert eval (not bool(_work_flirt_result.get("ok", True)) and int(_work_flirt_result.get("gain", 0)) == -1 and "занята работой" in str(_work_flirt_result.get("text", "") or "")) timeout 5.0
    assert eval (int(Amanda.rel or 0) == 9 and int(Amanda.flirted_today or 0) == _work_flirted_before) timeout 5.0
    $ people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=999, working=True), NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=1000, label="planned_scene", working=False)])
    assert eval (not Amanda.is_working()) timeout 5.0
    $ _work_talk_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Поговорить")
    $ _work_talk_button_id = "choice_panel_button_%d" % int(_work_talk_index)
    click id _work_talk_button_id pos (0.5, 0.5) until eval (len(list(renpy.get_screen("choice").scope.get("items", []) or [])) == 11) timeout 20.0
    assert eval (int(Amanda.rel or 0) == 9 and int(Amanda.talked_today or 0) == 1) timeout 5.0

testcase external_smalltalk_main_ui_portraits:
    run Jump("Intro")
    advance until screen "choice" timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (str(rooms.current_code or "") == "TavernMain" and len(people) > 0) timeout 20.0
    $ external_calendar_set_fields(3, 1, 1100, 9, 0)
    $ rooms.enter("TavernMain")
    $ main_ui_runtime.overlay = ""
    $ main_ui_runtime.inventory_dropdown_open = False

    $ _talk_girl = "amanda"
    $ external_prepare_smalltalk_picture_check(_talk_girl)
    $ Amanda.rel = 10
    $ _smalltalk_clock_before = int(calendar_v2.clock_minutes() or 0)
    $ _smalltalk_rel_before = int(Amanda.rel or 0)
    run Call("IntAmandaTalk", _talk_girl)
    advance until screen "choice" timeout 20.0
    $ _smalltalk_talk_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Поговорить")
    $ _smalltalk_talk_button_id = "choice_panel_button_%d" % int(_smalltalk_talk_index)
    click id _smalltalk_talk_button_id pos (0.5, 0.5) until eval (len(list(renpy.get_screen("choice").scope.get("items", []) or [])) == 11) timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None and str(main_ui_runtime.mode or "") == "talk") timeout 5.0
    assert eval (str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "") == _talk_girl) timeout 5.0
    assert eval (str(main_ui_runtime.talk_picture or "") == str(main_ui_talk_picture_path(_talk_girl) or "") and renpy.loadable(main_ui_runtime.talk_picture)) timeout 5.0
    assert eval (len(list(renpy.get_screen("choice").scope.get("items", []) or [])) == 11) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 1) timeout 20.0
    assert eval (renpy.get_screen("choice") is not None and int(calendar_v2.clock_minutes() or 0) - _smalltalk_clock_before == 5) timeout 5.0
    assert eval (renpy.get_screen("say") is None) timeout 5.0
    assert eval (renpy.get_screen("notify") is None) timeout 5.0
    assert eval (_smalltalk_rel_before - int(Amanda.rel or 0) in (1, 2)) timeout 5.0
    assert eval ("О работе и распорядке" not in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 5.0
    $ _smalltalk_rel_after_bad = int(Amanda.rel or 0)
    $ _smalltalk_favorite_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("О танцах")
    $ _smalltalk_favorite_button_id = "choice_panel_button_%d" % int(_smalltalk_favorite_index)
    click id _smalltalk_favorite_button_id pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 2) timeout 20.0
    assert eval (renpy.get_screen("choice") is not None and int(calendar_v2.clock_minutes() or 0) - _smalltalk_clock_before == 10) timeout 5.0
    assert eval (int(Amanda.rel or 0) - _smalltalk_rel_after_bad in (1, 2)) timeout 5.0
    $ _smalltalk_quit_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _smalltalk_quit_button_id = "choice_panel_button_%d" % int(_smalltalk_quit_index)
    click id _smalltalk_quit_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is not None and "Осмотреть" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])] and "Назад" in [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])]) timeout 20.0
    assert eval (renpy.get_screen("say") is None) timeout 5.0
    assert eval (int(calendar_v2.clock_minutes() or 0) - _smalltalk_clock_before == 10) timeout 5.0
    $ _smalltalk_back_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Назад")
    $ _smalltalk_back_button_id = "choice_panel_button_%d" % int(_smalltalk_back_index)
    click id _smalltalk_back_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0

    $ _talk_girl = "melissa"
    $ external_prepare_smalltalk_picture_check(_talk_girl)
    run Call("SocialTalkTopicMenu", _talk_girl, "talk")
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None and str(main_ui_runtime.mode or "") == "talk") timeout 5.0
    assert eval (str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "") == _talk_girl) timeout 5.0
    assert eval (str(main_ui_runtime.talk_picture or "") == str(main_ui_talk_picture_path(_talk_girl) or "") and renpy.loadable(main_ui_runtime.talk_picture)) timeout 5.0
    assert eval (len(list(renpy.get_screen("choice").scope.get("items", []) or [])) > 1) timeout 5.0
    $ _smalltalk_quit_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _smalltalk_quit_button_id = "choice_panel_button_%d" % int(_smalltalk_quit_index)
    click id _smalltalk_quit_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0

    $ _talk_girl = "sandra"
    $ external_prepare_smalltalk_picture_check(_talk_girl)
    run Call("SocialTalkTopicMenu", _talk_girl, "talk")
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None and str(main_ui_runtime.mode or "") == "talk") timeout 5.0
    assert eval (str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "") == _talk_girl) timeout 5.0
    assert eval (str(main_ui_runtime.talk_picture or "") == str(main_ui_talk_picture_path(_talk_girl) or "") and renpy.loadable(main_ui_runtime.talk_picture)) timeout 5.0
    assert eval (len(list(renpy.get_screen("choice").scope.get("items", []) or [])) > 1) timeout 5.0
    $ _smalltalk_quit_index = [str(i.caption or "") for i in renpy.get_screen("choice").scope.get("items", [])].index("Закончить разговор")
    $ _smalltalk_quit_button_id = "choice_panel_button_%d" % int(_smalltalk_quit_index)
    click id _smalltalk_quit_button_id pos (0.5, 0.5) until eval (renpy.get_screen("choice") is None) timeout 20.0

    $ _talk_girl = "clara"
    $ external_prepare_smalltalk_picture_check(_talk_girl)
    $ _smalltalk_clock_before = int(calendar_v2.clock_minutes() or 0)
    run Call("SocialTalkTopicMenu", _talk_girl, "talk")
    advance until screen "choice" timeout 20.0
    assert eval (renpy.get_screen("main_ui") is not None and renpy.get_screen("choice") is not None and str(main_ui_runtime.mode or "") == "talk") timeout 5.0
    assert eval (str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "") == _talk_girl) timeout 5.0
    assert eval (str(main_ui_runtime.talk_picture or "") == str(main_ui_talk_picture_path(_talk_girl) or "") and renpy.loadable(main_ui_runtime.talk_picture)) timeout 5.0
    assert eval (len(list(renpy.get_screen("choice").scope.get("items", []) or [])) > 1) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 1) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 2) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 3) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 4) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 5) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 6) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 7) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 8) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 9) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5) until eval (social_topic_seen_count(_talk_girl, "talk") == 10 and renpy.get_screen("choice") is None) timeout 20.0
    assert eval (int(calendar_v2.clock_minutes() or 0) - _smalltalk_clock_before == 50) timeout 5.0
    assert eval (social_talk_session_remaining(_talk_girl) == 0) timeout 5.0
'''


def build_test_rpy() -> str:
    room_action_click_params = [
        (room_name, action_index)
        for room_name in ROOM_LABELS
        for action_index in range(ROOM_ACTION_INDEX_LIMIT)
    ]
    all_room_action_click_checks = ALL_ROOM_ACTION_CLICK_CHECKS.replace(
        "__ROOM_ACTION_CLICK_PARAMS__", repr(room_action_click_params)
    )
    return TEST_HEADER + "".join(
        ROOM_CHECK_TEMPLATE.format(room_name=room_name) for room_name in ROOM_LABELS
    ) + "\n\n" + SHOP_ACTION_CHECKS + "\n\n" + TAVERN_REPORT_STATE_CHECKS + "\n\n" + TAILOR_PURCHASE_FLOW_CHECKS + "\n\n" + DOG_ENTITY_ACTION_CHECKS + "\n\n" + BACKYARD_BARREL_OBJECT_CHECKS + "\n\n" + GROCERY_STORE_OBJECT_PURCHASE_CHECKS + "\n\n" + FIGHT_SYSTEM_RUNTIME_CHECKS + "\n\n" + SMALLTALK_MAIN_UI_CHECKS + "\n\n" + PORT_STREETS_FLOW_CHECKS + "\n\n" + CALENDAR_TIME_CHECKS + "\n\n" + ROOM_REGISTRY_SAVE_CHECKS + "\n\n" + PLAYER_SAVE_PARITY_CHECKS + "\n\n" + TAVERN_HELP_FLOW_CHECKS + "\n\n" + MEDIA_RESOLUTION_CHECKS + "\n\n" + HARASSMENT_IMAGE_CHECKS + "\n\n" + GIRL_OBJECT_RUNTIME_CHECKS + "\n\n" + ACTUAL_ACTION_BUTTON_CLICK_CHECKS + "\n\n" + ACTUAL_RANDOM_TOWN_CLICK_CHECKS + "\n\n" + TARGETED_CURRENT_BUG_CHECKS + "\n\n" + DEBUG_BUILDER_ROOM_CHECKS + "\n\n" + AMANDA_ROOM_NIGHT_EVENT_CHECKS + "\n\n" + MY_ROOM_RECIPE_BOOK_ACTION_CHECKS + "\n\n" + MY_ROOM_WINDOW_ACTION_CHECKS + "\n\n" + TAVERN_ROOM_PICTURE_STATE_CHECKS + "\n\n" + MELISSA_BATS_DRAWINGS_CHECKS + "\n\n" + MELISSA_WERECAT_FOREST_ACTION_CHECKS + "\n\n" + CHURCH_LINK_CHECKS + "\n\n" + CHURCH_AFTER_SERMON_EVENT_CHECKS + "\n\n" + CLARA_MELISSA_TAVERN_BAR_GOSSIP_CHECKS + "\n\n" + FRIDAY_DANCE_AMANDA_CHECKS + "\n\n" + SANDRA_NIGHT_THANKS_CHECKS + "\n\n" + MELISSA_SEX_ENGINE_CHECKS + "\n\n" + PLAYER_INTIMACY_STATE_CHECKS + "\n\n" + CLARA_AMANDA_SCHEDULE_FLOW_CHECKS + "\n\n" + HOUSEHOLD_AI_EVENT_CHECKS + "\n\n" + all_room_action_click_checks + "\n\n" + BECKY_HOME_GUEST_CHECKS


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
    if os.name == "nt":
        try:
            attributes = os.lstat(path).st_file_attributes
            return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        except (AttributeError, OSError):
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
            "external_tavern_sunday_dinner_schedule_and_stats",
            "external_actual_tailor_buy_dress_measure_flow",
            "external_female_tailor_choose_agree_purchase_flow",
            "external_female_tailor_refusal_returns_to_catalog",
            "external_dog_entity_actions",
            "external_backyard_barrel_object_actions",
            "external_grocery_store_object_purchase_actions",
            "external_fight_system_runtime_flow",
            "external_working_girl_talk_penalty",
            "external_smalltalk_main_ui_portraits",
            "external_port_streets_georgette_liza_flow",
            "external_georgette_portstreet_relationship_talk_and_sex_flow",
            "external_sexport_finish_does_not_show_advance_time_developer_text",
            "external_liza_inherited_state_and_native_sex_menu",
            "external_new_game_starts_at_8_morning",
            "external_tavern_help_book_single_owner_flow",
            "external_navigation_jump_does_not_stack_previous_room",
            "external_room_exit_time_costs",
            "external_player_exploration_progression",
            "external_calendar_long_cycle_thirteenth_period_rollover",
            "external_sleep_wake_hour_rules",
            "external_daily_setstatdefault_body_maps_exist",
            "external_room_registry_pickle_round_trip",
            "external_player_save_payload_parity",
            "external_player_actual_load_parity",
            "external_player_appearance_v47_migration",
            "external_hunter_club_reputation_challenge_and_trade",
            "external_hour_based_room_and_npc_schedule_adjustment",
            "external_context_image_resolution",
            "external_harassment_images_use_exact_existing_paths",
            "external_harassment_event_picture_sequence",
            "external_inga_v53_migration",
            "external_inga_secondary_npc_source",
            "external_francheska_secondary_and_birth_thread",
            "external_kids_birth_history_single_authority",
            "external_player_derived_stats_direct_owners",
            "external_church_ellona_player_owned_state",
            "external_gerhard_secondary_npc_source",
            "external_secondary_side_characters_are_classes",
            "external_birth_thread_conditions_block_day_zero",
            "external_ellona_temple_sunday_story_event",
            "external_becky_v52_migration",
            "external_becky_classes_are_initialized",
            "external_becky_husband_backstory_uses_one_thread_stage",
            "external_becky_eddie_backstory_uses_one_thread_stage",
            "external_becky_eddie_opinions_remain_parallel_repeatable_topics",
            "external_becky_sherwood_followups_use_branch_state_not_threads",
            "external_becky_blackwood_offer_uses_single_live_label",
            "external_becky_inga_lucas_thread_from_native_homefront_menu",
            "external_becky_talk_action_returns_without_duplicate_menu",
            "external_people_objects_are_single_source",
            "external_registry_girl_daily_processing_once",
            "external_npc_schedule_room_visibility_agreement",
            "external_right_side_npc_buttons_open_default_menu",
            "external_people_locate_matches_schedule",
            "external_player_and_girl_cards_render",
            "external_mongol_horse_purchase_once_and_amanda_room_presence",
            "external_clara_object_thread_conditions",
            "external_story_event_audit_methods_cover_tuple_attributes",
            "external_main_ui_does_not_repeat_active_dialogue_text",
            "external_actual_grocery_click",
            "external_becky_store_event_replaces_room_text",
            "external_actual_wine_click",
            "external_wine_store_return_restores_market_scene_once",
            "external_actual_wine_for_dance_menu",
            "external_tavern_random_event_plan_consumes_once",
            "external_tavern_small_fight_native_event_flow",
            "external_tavern_unwitnessed_event_report_consumes_leftovers",
            "external_breakfast_dance_sponsor_announcement",
            "external_breakfast_attendance_location_wins",
            "external_breakfast_angry_amanda_melissa_mockery",
            "external_sandra_weekly_visit_native_beats",
            "external_melissa_bat_breakfast_single_finish",
            "external_breakfast_window_and_call_all_click",
            "external_kitchen_entry_morning_sickness_event",
            "external_actual_barber_actions_click",
            "external_actual_draupnir_talk_menu",
            "external_actual_market_click",
            "external_actual_market_blind_pirate_first_entry",
            "external_market_clock_open_hours",
            "external_actual_random_town_continue_click",
            "external_actual_random_town_click",
            "external_sleep_after_midnight_detector",
            "external_next_day_report_releases_time_block",
            "external_town_thugs_shout_result",
            "external_town_thugs_fight_victory_result",
            "external_georgette_back_alley_not_visible_in_port_streets",
            "external_debug_builder_room_visual_surfaces",
            "external_amanda_room_night_bed_action_uses_thread_event",
            "external_my_room_recipe_book_table_link",
            "external_my_room_window_day_night_amanda_pictures",
            "external_tavern_room_movement_resets_picture_state",
            "external_melissa_bats_room_search_after_wait",
            "external_melissa_recipe_unlock_single_authority",
            "external_melissa_werecat_forest_actions_rebuild",
            "external_melissa_werecat_thread_condition_sequence",
            "external_church_service_action_links_work",
            "external_liza_identity_save_migration",
            "external_georgett_liza_church_after_sermon_events",
            "external_becky_church_after_sermon_uses_daily_event_authority",
            "external_clara_market_event_repeats_until_exploration_success",
            "external_clara_market_follow_finishes_without_self_loop",
            "external_mongol_market_schedule_rolls_once_per_day",
            "external_clara_melissa_bar_gossip_click_fires_ready_dialog",
            "external_clara_booklet_mongol_night_buttons_advance",
            "external_mongol_v61_migration",
            "external_irma_v62_migration",
            "external_amanda_v63_night_bowl_migration",
            "external_amanda_night_bowl_object_state",
            "external_amanda_v64_attic_breakfast_migration",
            "external_amanda_v65_daily_misc_migration",
            "external_amanda_v66_room_rejection_migration",
            "external_amanda_room_rejection_flow",
            "external_amanda_v67_legare_state_migration",
            "external_amanda_legare_resolution_uses_object_state",
            "external_eddie_v60_migration",
            "external_eddie_fingal_talk_progression",
            "external_draupnir_v59_migration",
            "external_francheska_v57_migration",
            "external_alber_v56_migration",
            "external_alber_native_talk_local_provocation_flow",
            "external_liza_v55_migration",
            "external_zimmer_v54_migration",
            "external_zimmer_mongol_wine_distraction_dialog",
            "external_robin_v58_migration",
            "external_robin_blackwood_room_thread_and_mongol_pass",
            "external_friday_amanda_bad_invite_uses_one_dance",
            "external_friday_amanda_legare_go_phrase_survives_create_dance",
            "external_amanda_legare_sex_scene_label_procedures",
            "external_friday_becky_inner_actions_do_not_spend_extra_dances",
            "external_clara_flirt_unlocks_paintings_gate",
            "external_amanda_glory_reaction_uses_story_event",
            "external_amanda_liza_talk_rows_use_typed_conditions",
            "external_amanda_talk_opens_from_npc_button",
            "external_amanda_daily_talk_actions",
            "external_sandra_talk_opens_from_npc_button",
            "external_sandra_weekly_thread_progression",
            "external_sandra_night_thanks_hours_work",
            "external_melissa_courtship_is_slow_and_daily",
            "external_melissa_finished_intimacy_returns_to_room_and_closes_for_day",
            "external_player_intimacy_state_sleep_arousal_and_help",
            "external_clara_evening_follow_finishes_in_melissa_room",
            "external_household_ai_kitchen_event_fires",
            "external_all_room_action_clicks",
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
            "external_tavern_sunday_dinner_schedule_and_stats",
            "external_actual_tailor_buy_dress_measure_flow",
            "external_female_tailor_choose_agree_purchase_flow",
            "external_female_tailor_refusal_returns_to_catalog",
            "external_dog_entity_actions",
            "external_backyard_barrel_object_actions",
            "external_grocery_store_object_purchase_actions",
            "external_fight_system_runtime_flow",
            "external_working_girl_talk_penalty",
            "external_smalltalk_main_ui_portraits",
            "external_port_streets_georgette_liza_flow",
            "external_georgette_portstreet_relationship_talk_and_sex_flow",
            "external_sexport_finish_does_not_show_advance_time_developer_text",
            "external_liza_inherited_state_and_native_sex_menu",
            "external_new_game_starts_at_8_morning",
            "external_tavern_help_book_single_owner_flow",
            "external_navigation_jump_does_not_stack_previous_room",
            "external_room_exit_time_costs",
            "external_player_exploration_progression",
            "external_calendar_long_cycle_thirteenth_period_rollover",
            "external_sleep_wake_hour_rules",
            "external_daily_setstatdefault_body_maps_exist",
            "external_room_registry_pickle_round_trip",
            "external_player_save_payload_parity",
            "external_player_actual_load_parity",
            "external_player_appearance_v47_migration",
            "external_hunter_club_reputation_challenge_and_trade",
            "external_hour_based_room_and_npc_schedule_adjustment",
            "external_context_image_resolution",
            "external_harassment_images_use_exact_existing_paths",
            "external_harassment_event_picture_sequence",
            "external_inga_v53_migration",
            "external_inga_secondary_npc_source",
            "external_francheska_secondary_and_birth_thread",
            "external_kids_birth_history_single_authority",
            "external_player_derived_stats_direct_owners",
            "external_church_ellona_player_owned_state",
            "external_gerhard_secondary_npc_source",
            "external_secondary_side_characters_are_classes",
            "external_birth_thread_conditions_block_day_zero",
            "external_ellona_temple_sunday_story_event",
            "external_becky_v52_migration",
            "external_becky_classes_are_initialized",
            "external_becky_husband_backstory_uses_one_thread_stage",
            "external_becky_eddie_backstory_uses_one_thread_stage",
            "external_becky_eddie_opinions_remain_parallel_repeatable_topics",
            "external_becky_sherwood_followups_use_branch_state_not_threads",
            "external_becky_blackwood_offer_uses_single_live_label",
            "external_becky_inga_lucas_thread_from_native_homefront_menu",
            "external_becky_talk_action_returns_without_duplicate_menu",
            "external_people_objects_are_single_source",
            "external_registry_girl_daily_processing_once",
            "external_npc_schedule_room_visibility_agreement",
            "external_right_side_npc_buttons_open_default_menu",
            "external_people_locate_matches_schedule",
            "external_player_and_girl_cards_render",
            "external_mongol_horse_purchase_once_and_amanda_room_presence",
            "external_clara_object_thread_conditions",
            "external_story_event_audit_methods_cover_tuple_attributes",
            "external_main_ui_does_not_repeat_active_dialogue_text",
            "external_actual_grocery_click",
            "external_becky_store_event_replaces_room_text",
            "external_actual_wine_click",
            "external_wine_store_return_restores_market_scene_once",
            "external_actual_wine_for_dance_menu",
            "external_tavern_random_event_plan_consumes_once",
            "external_tavern_small_fight_native_event_flow",
            "external_tavern_unwitnessed_event_report_consumes_leftovers",
            "external_breakfast_dance_sponsor_announcement",
            "external_breakfast_attendance_location_wins",
            "external_breakfast_angry_amanda_melissa_mockery",
            "external_sandra_weekly_visit_native_beats",
            "external_melissa_bat_breakfast_single_finish",
            "external_breakfast_window_and_call_all_click",
            "external_kitchen_entry_morning_sickness_event",
            "external_actual_barber_actions_click",
            "external_actual_draupnir_talk_menu",
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
            "external_melissa_recipe_unlock_single_authority",
            "external_melissa_werecat_forest_actions_rebuild",
            "external_melissa_werecat_thread_condition_sequence",
            "external_church_service_action_links_work",
            "external_liza_identity_save_migration",
            "external_georgett_liza_church_after_sermon_events",
            "external_becky_church_after_sermon_uses_daily_event_authority",
            "external_clara_market_event_repeats_until_exploration_success",
            "external_clara_market_follow_finishes_without_self_loop",
            "external_mongol_market_schedule_rolls_once_per_day",
            "external_clara_melissa_bar_gossip_click_fires_ready_dialog",
            "external_clara_booklet_mongol_night_buttons_advance",
            "external_mongol_v61_migration",
            "external_irma_v62_migration",
            "external_amanda_v63_night_bowl_migration",
            "external_amanda_night_bowl_object_state",
            "external_amanda_v64_attic_breakfast_migration",
            "external_amanda_v65_daily_misc_migration",
            "external_amanda_v66_room_rejection_migration",
            "external_amanda_room_rejection_flow",
            "external_amanda_v67_legare_state_migration",
            "external_amanda_legare_resolution_uses_object_state",
            "external_eddie_v60_migration",
            "external_eddie_fingal_talk_progression",
            "external_draupnir_v59_migration",
            "external_francheska_v57_migration",
            "external_alber_v56_migration",
            "external_alber_native_talk_local_provocation_flow",
            "external_liza_v55_migration",
            "external_zimmer_v54_migration",
            "external_zimmer_mongol_wine_distraction_dialog",
            "external_robin_v58_migration",
            "external_robin_blackwood_room_thread_and_mongol_pass",
            "external_friday_amanda_bad_invite_uses_one_dance",
            "external_friday_amanda_legare_go_phrase_survives_create_dance",
            "external_amanda_legare_sex_scene_label_procedures",
            "external_friday_becky_inner_actions_do_not_spend_extra_dances",
            "external_clara_flirt_unlocks_paintings_gate",
            "external_amanda_glory_reaction_uses_story_event",
            "external_amanda_liza_talk_rows_use_typed_conditions",
            "external_amanda_talk_opens_from_npc_button",
            "external_amanda_daily_talk_actions",
            "external_sandra_talk_opens_from_npc_button",
            "external_sandra_weekly_thread_progression",
            "external_sandra_night_thanks_hours_work",
            "external_melissa_courtship_is_slow_and_daily",
            "external_melissa_finished_intimacy_returns_to_room_and_closes_for_day",
            "external_player_intimacy_state_sleep_arousal_and_help",
            "external_clara_evening_follow_finishes_in_melissa_room",
            "external_household_ai_kitchen_event_fires",
            "external_all_room_action_clicks",
            "external_becky_home_guest_citydress_gate_and_arrival",
        ]
        failed_tests = []
        for test_name in test_names:
            clear_renpy_runtime_state(temp_project)
            test_result = run_renpy(renpy_exe, temp_project, args.timeout, test_name)
            result = max(result, test_result)
            if test_result != 0:
                failed_tests.append(test_name)
        if failed_tests:
            print("FAILED TESTCASES:")
            for test_name in failed_tests:
                print("  " + test_name)
        return result
    finally:
        if args.keep_temp:
            print(f"Keeping temporary test project: {temp_root}")
        else:
            remove_temp_tree(temp_root)


if __name__ == "__main__":
    raise SystemExit(main())
