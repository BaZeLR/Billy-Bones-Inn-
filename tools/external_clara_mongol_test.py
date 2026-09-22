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

label external_clara_actual_load_probe(saved_stage):
    $ external_clara_prepare()
    $ saveVersion = currentVersion
    $ threads["claraMongolAccusation"].advanceTo(saved_stage, complete_at_end=True)
    $ Clara.trust = 7
    $ player.economy.money = 1234
    $ renpy.save("external-clara-reload", include_screenshot=False)
    if __import__("os").path.exists(config.basedir + "/clara-load.marker"):
        return
    python hide:
        with open(config.basedir + "/clara-load.marker", "w") as marker:
            marker.write("loaded")
    $ initThreads()
    $ threads["claraMongolAccusation"].reset()
    $ Clara.trust = 0
    $ player.economy.money = 1
    $ renpy.load("external-clara-reload")
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
        Clara.set_day_location_override("WineStore")
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

testcase external_clara_zimmer_accusation_choices:
    parameter decision = ["report", "protect", "postpone"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_prepare()
    python:
        threads["claraBookletMarket"].advanceTo(3)
        threads["claraMongolAccusation"].advanceTo(0, force_active=True)
        Clara.trust = 3
        player.horse.stolen_days = 0
        Zimmer.horse_complaint_stage = 0
        Zimmer.talked_today = 2
        Mongol.stocks_arrest_day = -1
        calendar_v2.week = 2
        calendar_v2.hour = 16
        rooms.enter("CityGuard")
        assert people.location("zimmer") == "CityGuard"
        assert story_event_available("talk_zimmer", "clara_mongol_accusation")
    run Call("IntZimmerTalk")
    advance until eval ("Решить, назвать ли сообщницу Монгола" in external_clara_choices()) timeout 20.0
    click id (external_clara_button("Решить, назвать ли")) pos (0.5, 0.5)
    advance until eval ("Назвать Клариссу сообщницей Монгола" in external_clara_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and not main_ui_runtime.action_items) timeout 5.0
    assert eval (scene_runtime.text == scene_runtime.location_text) timeout 5.0
    if eval (decision == "report"):
        click id "choice_panel_button_0" pos (0.5, 0.5)
    elif eval (decision == "protect"):
        click id "choice_panel_button_1" pos (0.5, 0.5)
    else:
        click id "choice_panel_button_2" pos (0.5, 0.5)
    if eval (decision != "postpone"):
        advance until eval ("Вернуться к разговору" in external_clara_choices()) timeout 20.0
        click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Закончить разговор" in external_clara_choices()) timeout 20.0
    python:
        case = threads["claraMongolAccusation"]
        assert rooms.current_code == "CityGuard" and main_ui_runtime.mode == "talk"
        assert case.num == (1 if decision == "report" else 0)
        assert case.aborted == (decision == "protect")
        assert Clara.trust == (4 if decision == "protect" else 3)
        assert Clara.mongol_case_detained() == (decision == "report")
        assert threads["claraBookletMarket"].num == (4 if decision == "report" else 3)
        assert not threads["claraBookletMarket"].done[3]
        assert Mongol.stocks_arrest_day == -1
        assert threads["claraPaintingsPath"].num == 1
        assert story_event_available("talk_zimmer", "clara_mongol_accusation") == (decision == "postpone")
        if decision == "report":
            assert people.location("clara") == ""
            restored = __import__("pickle").loads(__import__("pickle").dumps(case))
            threads["claraMongolAccusation"] = restored
            initThreads()
            assert Clara.mongol_case_detained()
            assert people.location("clara") == ""
            renpy.save("external-clara-custody", include_screenshot=False)
            assert renpy.can_load("external-clara-custody")
    click id (external_clara_button("Закончить разговор")) pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0

testcase external_clara_custody_food_escape_arrival:
    parameter free_clara = [True, False]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_prepare()
    python:
        threads["claraMongolAccusation"].advanceTo(1, force_active=True)
        threads["claraBookletMarket"].advanceTo(8, force_active=True)
        Draupnir.mongol_lockpick_order_day = 98
        Mongol.stocks_food_day = 99
        Mongol.stocks_fate = ""
        player.tavern_management.productnum = 10
        player.tavern_management.winenum = 5
        calendar_v2.hour = 21
        rooms.enter("CityGuard")
        assert story_event_available("menu_CityGuard", "clara_custody")
        assert any(item.caption == "Навестить задержанную Клариссу" for item in city_guard_action_items())
        origin = main_ui_context_snapshot()
    run Call("checkTriggers", "menu_CityGuard", "clara_custody", 0)
    advance until eval ("Передать Клариссе еду из трактира" in external_clara_choices()) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Уйти от караулки" in external_clara_choices()) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == origin) timeout 5.0
    assert eval (threads["claraMongolAccusation"].num == 2 and Clara.mongol_case_detained()) timeout 5.0
    assert eval (player.tavern_management.productnum == 9) timeout 5.0
    run Call("checkTriggers", "menu_CityGuard", "clara_custody", 0)
    advance until screen "choice" timeout 20.0
    assert eval (external_clara_choices() == ["Уйти и вернуться позже"]) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0
    assert eval (player.tavern_management.productnum == 9) timeout 5.0
    run Call("checkTriggers", "menu_CityGuard", "mongol_stocks", 0)
    advance until eval ("Послать стражникам вино и угощение, а затем освободить Монгола" in external_clara_choices()) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval ("Освободить Клариссу вместе с Монголом" in external_clara_choices()) timeout 20.0
    if eval (free_clara):
        click id "choice_panel_button_0" pos (0.5, 0.5)
        advance until eval ("Покинуть караулку" in external_clara_choices()) timeout 20.0
        click id "choice_panel_button_0" pos (0.5, 0.5)
    else:
        click id "choice_panel_button_1" pos (0.5, 0.5)
    advance until eval (not external_clara_choices()) timeout 20.0
    python:
        assert Mongol.stocks_fate == "released" and Robin.mongol_safe_pass
        assert threads["claraBookletMarket"].num == 9
        assert player.tavern_management.productnum == 8
        assert player.tavern_management.winenum == 4
        assert Clara.mongol_case_detained() == (not free_clara)
        assert threads["claraMongolAccusation"].num == (3 if free_clara else 2)
        assert not threads["claraMongolAccusation"].completed
        assert not Clara.tavern_resident()
    if eval (free_clara):
        $ rooms.enter("TavernMain")
        assert eval (story_event_available("TavernMain", "enter")) timeout 5.0
        run Call("checkTriggers", "TavernMain", "enter", 0)
        advance until eval ("Выслушать Клариссу" in external_clara_choices()) timeout 20.0
        click id "choice_panel_button_0" pos (0.5, 0.5)
        advance until eval ("Поселить у Мелиссы и поручить уборку со следующего дня" in external_clara_choices()) timeout 20.0
        click id "choice_panel_button_0" pos (0.5, 0.5)
        advance until eval (not external_clara_choices()) timeout 20.0
        python:
            assert threads["claraMongolAccusation"].completed
            assert Clara.tavern_resident()
            assert household.resident_ids().count("clara") == 1
            assert Clara.is_tavern_worker()
            assert Clara.job_value("jobcleaning", 0) == 0
            assert Clara.job_value("jobcleaningtomorrow", 0) == 1
            assert Clara.tavern_job_available("jobkitchentomorrow")
            assert Clara.job_value("jobHallAvail", 0) == 0
            calendar_v2.week = 2
            calendar_v2.hour = 9
            assert people.location("clara") == "TavernMelissaRoom", people.location("clara")
            Clara.apply_tavern_job_plan()
            assert Clara.job_value("jobcleaning", 0) == 1
            while calendar_v2.day in HordusStaticData.monthly_visit_days():
                calendar_v2.day += 1
            calendar_v2.hour = 16
            assert people.location("clara") == "TavernMain", people.location("clara")

testcase external_clara_custody_actual_save_load:
    parameter saved_stage = [1, 4]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    python:
        if __import__("os").path.exists(config.basedir + "/clara-load.marker"):
            __import__("os").remove(config.basedir + "/clara-load.marker")
    run Call("external_clara_actual_load_probe", saved_stage)
    # Ren'Py's test executor owns the pending node; run the normal continuation.
    run Call("_after_load")
    assert eval (Clara.trust == 7 and player.economy.money == 1234) timeout 5.0
    assert eval (threads["claraMongolAccusation"].num == max(0, saved_stage)) timeout 5.0
    assert eval (Clara.mongol_case_detained() == (saved_stage == 1)) timeout 5.0
    assert eval (Clara.tavern_resident() == (saved_stage == 4)) timeout 5.0

testcase external_clara_missing_thread_load_initialization:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    python:
        # Run the saved-state upgrade and after_load initializers together,
        # before the test executor renders a screen with a partial old schema.
        saveVersion = currentVersion
        original_trust = Clara.trust
        original_money = player.economy.money
        threads.pop("claraMongolAccusation")
        updateSave()
        npc_schedule_after_load()
        initStoryEventRuntime(True)
        assert threads["claraMongolAccusation"].num == 0
        assert not Clara.mongol_case_detained()
        assert Clara.trust == original_trust and player.economy.money == original_money

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
