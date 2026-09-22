#!/usr/bin/env python3
"""Play Clara's market -> denial -> delayed arrest with isolated Ren'Py saves."""

import external_tavern_renovations_test as isolated


TEST_RPY = r'''
init python:
    def external_clara_choices():
        screen = renpy.get_screen("choice")
        return [str(item.caption) for item in screen.scope.get("items", [])] if screen else []

    def external_clara_button(prefix):
        return "choice_panel_button_%d" % next(i for i, text in enumerate(external_clara_choices()) if text.startswith(prefix))

    def external_clara_prepare():
        for thread in threads.values():
            thread.abort()
        threads["claraBookletMarket"].advanceTo(1, force_active=True)
        threads["claraPaintingsPath"].advanceTo(1, force_active=True)
        threads["claraPaintingsPath"].abort()
        player.horse.theft_attempted = True
        player.stats.exploration = 100
        Clara.rel = 10
        calendar_v2.daysInGame = 100
        calendar_v2.day = 10
        calendar_v2.week = 1
        calendar_v2.hour = 19
        calendar_v2.minute = 0
        Clara.market_evening_roll_day = 100
        Clara.market_evening_roll = True
        Clara.day_location_override_day = -1
        daily_events.rows = []
        event_runtime.fired_keys_today = []
        event_runtime.fired_day = -1
        event_runtime.evaluation_time = None
        rooms.enter("MarketPlace")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.action_items = []
        scene_runtime.picture = MARKETPLACE_CLOSED_PICTURE
        scene_runtime.text = "EXTERNAL_CLOSED_MARKET"
        scene_runtime.location_text = scene_runtime.text
        findAvailableEvents(True)

label external_clara_resolve_day:
    $ renpy.dynamic("CurDay", "TotalDay")
    $ next_day_runtime.current_day = {}
    $ CurDay = next_day_runtime.current_day
    $ TotalDay = dict.fromkeys(("whorerevenue", "gloryholerevenue", "loyalty", "revenue", "dineout", "fixedcost", "KidsMoney", "visitors", "wine", "products", "HorseFood", "HorseStolen", "fameaten", "rat_food_loss", "happy"), 0)
    call NextDay_TavernDaily
    return

testsuite global:
    teardown:
        exit

testcase external_clara_mongol_missing_prerequisite:
    parameter missing = ["theft", "drawings", "skill", "open_market", "friday", "sunday", "roll"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_prepare()
    python:
        if missing == "theft":
            player.horse.theft_attempted = False
            daily_events.add("", "TavernStable", 7, "=", 1, 0, "StableHorseTheft", "TavernStableHorseTheftAttempt", "none")
        elif missing == "drawings":
            threads["claraPaintingsPath"].advanceTo(0)
            Melissa.drawings_found = True
            Clara.drawings_secret_known = True
        elif missing == "skill":
            player.stats.exploration = 99
        elif missing == "open_market":
            calendar_v2.hour = 18
            calendar_v2.minute = 59
        elif missing == "friday":
            calendar_v2.week = 5
        elif missing == "sunday":
            calendar_v2.week = 7
        elif missing == "roll":
            Clara.market_evening_roll = False
        assert not story_event_available("MarketPlace", "enter")
        threads["claraBookletMarket"].advanceTo(2)
        assert not story_event_available("MarketPlace", "enter")

testcase external_clara_market_denial_arrest_sequence:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_prepare()
    assert eval (story_event_available("MarketPlace", "enter")) timeout 5.0
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until eval ("Тихо проследить за Клариссой" in external_clara_choices()) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Запомнить услышанное и уйти" in external_clara_choices()) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0
    assert eval (threads["claraBookletMarket"].num == 3) timeout 5.0
    assert eval (not story_event_available("HunterClub", "overheard")) timeout 5.0
    python:
        threads["claraForestSofa"].advanceTo(0, force_active=True)
        threads["claraForestSofa"].metconds = False
        assert threads["claraForestSofa"].checkActive()
        threads["claraForestSofa"].abort()
        calendar_v2.daysInGame = 101
        calendar_v2.hour = 9
        calendar_v2.minute = 0
        rooms.enter("WineStore")
        people.get_data("clara").set_schedule([NPCScheduleEntry(location="WineStore", start_minute=0, end_minute=1440, priority=999)])
        assert people.location("clara") == "WineStore"
        assert story_event_available("WineStore", "clara_mongol")
    run Call("IntClaraTalk", "clara")
    advance until screen "choice" timeout 20.0
    click id (external_clara_button("Спросить о ночном")) pos (0.5, 0.5)
    advance until eval ("Выслушать ответ" in external_clara_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == []) timeout 5.0
    pause 0.2
    $ renpy.screenshot(config.basedir + "/clara-wine-denial.png")
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Не выдавать, сколько вы услышали" in external_clara_choices()) timeout 20.0
    assert eval ("бочек" in scene_runtime.text) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Вернуться к разговору" in external_clara_choices()) timeout 20.0
    assert eval ("лжет" in scene_runtime.text) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Назад" in external_clara_choices()) timeout 20.0
    assert eval (threads["claraBookletMarket"].num == 4 and main_ui_runtime.mode == "talk" and rooms.current_code == "WineStore") timeout 5.0
    assert eval (not any("ночном разговоре" in text for text in external_clara_choices())) timeout 5.0
    click id (external_clara_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0
    python:
        rooms.enter("HunterClub")
        calendar_v2.daysInGame = 107
        assert not story_event_available("HunterClub", "overheard")
        calendar_v2.daysInGame = 108
        assert story_event_available("HunterClub", "overheard")
    run Call("checkTriggers", "HunterClub", "overheard", 0)
    advance until eval ("Запомнить слух" in external_clara_choices()) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0
    assert eval (threads["claraBookletMarket"].num == 5 and Mongol.stocks_arrest_day == 108) timeout 5.0

testcase external_clara_witnessed_theft_survives_save:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_prepare()
    python:
        player.horse.theft_attempted = False
        player.horse.acquire("EXTERNAL_HORSE", 1000)
        calendar_v2.hour = 23
        rooms.enter("TavernStable")
        daily_events.add("", "TavernStable", 7, "=", 1, 0, "StableHorseTheft", "TavernStableHorseTheftAttempt", "none")
    run Call("check_daily_event", "", "StableHorseTheft", "TavernStable", 7)
    advance until screen "choice" timeout 20.0
    assert eval (player.horse.theft_attempted and player.horse.owns_horse()) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0
    python:
        assert daily_events.exists("", "StableHorseTheft") == 0
        player.horse.remove()
        player.horse.acquire("EXTERNAL_SECOND_HORSE", 500)
        assert player.horse.theft_attempted
        renpy.save("external-clara-attempt", include_screenshot=False)
        assert renpy.can_load("external-clara-attempt")
        restored = __import__("pickle").loads(__import__("pickle").dumps(player.horse))
        assert restored.theft_attempted and restored.name == "EXTERNAL_SECOND_HORSE"

testcase external_clara_overnight_theft_records_attempt:
    parameter outcome = ["stolen", "no_horse", "dog"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_prepare()
    python:
        player.horse.theft_attempted = False
        player.horse.remove()
        player.horse.stolen_days = 0
        if outcome != "no_horse":
            player.horse.acquire("EXTERNAL_HORSE", 1000)
        dog.owned = outcome == "dog"
        dog.loyalty = 10
        if outcome == "dog":
            while procedural_randint(1, 100, "dog_catch_horse_%s" % int(current_game_day())) > 70:
                calendar_v2.daysInGame += 1
        calendar_v2.hour = 6
        daily_events.add("", "TavernStable", 7, "=", 1, 0, "StableHorseTheft", "TavernStableHorseTheftAttempt", "none")
    run Call("external_clara_resolve_day")
    pause 0.1
    assert eval (player.horse.theft_attempted == (outcome != "no_horse")) timeout 5.0
    assert eval (daily_events.exists("", "StableHorseTheft") == 0) timeout 5.0
    assert eval (player.horse.stolen_days == (14 if outcome == "stolen" else 0)) timeout 5.0
    assert eval (player.horse.owns_horse() == (outcome == "dog")) timeout 5.0

testcase external_clara_moon_sabbath_returns_to_market:
    parameter follow = [True, False]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_prepare()
    python:
        threads["claraBookletMarket"].abort()
        threads["claraForestSofa"].advanceTo(3, force_active=True)
        threads["claraMoonSabbath"].forceEnable()
        Clara.wardrobe.add_owned("thiefdress")
        clothes_before = (dict(Clara.wardrobe.current_layers), dict(Clara.wardrobe.raised_layers), Clara.wardrobe.context, Clara.wardrobe.day_dress)
        calendar_v2.day = 20
        calendar_v2.week = 6
        origin = main_ui_context_snapshot()
        assert story_event_available("MarketPlace", "enter")
    run Call("checkTriggers", "MarketPlace", "enter", 0)
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [] and scene_runtime.picture == "images/clara/market_night.png") timeout 5.0
    assert eval (Clara.wardrobe.current_dress() == "thiefdress") timeout 5.0
    if eval (follow):
        click id "choice_panel_button_0" pos (0.5, 0.5)
        advance until eval ("Посмотреть, зачем она пришла" in external_clara_choices()) timeout 20.0
        assert eval (scene_runtime.picture == "images/forest/hidden_path.png") timeout 5.0
        click id "choice_panel_button_0" pos (0.5, 0.5)
        advance until eval ("Продолжить наблюдение из укрытия" in external_clara_choices()) timeout 20.0
        assert eval ("рисует" in scene_runtime.text) timeout 5.0
        click id "choice_panel_button_0" pos (0.5, 0.5)
        advance until eval ("Вернуться на рынок" in external_clara_choices()) timeout 20.0
        assert eval (calendar_v2.moon_name_ru() in scene_runtime.text) timeout 5.0
        click id "choice_panel_button_0" pos (0.5, 0.5)
    else:
        click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == origin and rooms.current_code == "MarketPlace") timeout 5.0
    assert eval ((dict(Clara.wardrobe.current_layers), dict(Clara.wardrobe.raised_layers), Clara.wardrobe.context, Clara.wardrobe.day_dress) == clothes_before) timeout 5.0
    assert eval (calendar_v2.hour == (20 if follow else 19)) timeout 5.0
    assert eval (threads["claraForestSofa"].num == 3 and not story_event_available("MarketPlace", "enter")) timeout 5.0
    python:
        calendar_v2.daysInGame += 28
        calendar_v2.period += 1
        assert story_event_available("MarketPlace", "enter")

testcase external_clara_migration_preserves_later_story:
    parameter old_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_prepare()
    python:
        booklet = threads["claraBookletMarket"]
        booklet.advanceTo(old_num)
        booklet.completed = old_num == 9
        booklet.aborted = old_num == 2
        booklet.day = 88
        del player.horse.theft_attempted
        player.horse.stolen_days = 0
        player.horse.stolen_purchase_price = 1000
        inventory_before = dict(player.inventory.items)
        updateSave_V96()
        assert booklet.num == (old_num + 1 if old_num >= 4 else old_num)
        assert booklet.completed == (old_num == 9)
        assert booklet.aborted == (old_num == 2)
        assert booklet.day == 88
        assert player.horse.theft_attempted
        assert dict(player.inventory.items) == inventory_before
'''


if __name__ == "__main__":
    isolated.TEST_RPY = TEST_RPY
    raise SystemExit(isolated.main())
