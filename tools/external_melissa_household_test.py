#!/usr/bin/env python3
"""Test the existing Melissa kitchen count, using copied scripts/temp saves."""

import external_tavern_renovations_test as isolated


def read_until_choice(prefix):
    # Ren'Py 8.5.2 testcases support if/until, not while blocks. Expand a bounded
    # series of real clicks; once the target choice is reached, later steps skip.
    # Wait for a new menu's items, not the outgoing choice screen still on screen.
    step = '''    if eval (not any(caption.startswith(%r) for caption in external_melissa_choices())):
        $ _melissa_read.append(scene_runtime.text)
        $ _melissa_previous_items = renpy.get_screen("choice").scope["items"]
        assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == []) timeout 5.0
        click id "choice_panel_button_0" pos (0.5, 0.5)
        pause 0.1
        advance until eval (renpy.get_screen("choice") is not None and renpy.get_screen("choice").scope["items"] is not _melissa_previous_items) timeout 20.0
''' % prefix
    return step * 10 + '    assert eval (any(caption.startswith(%r) for caption in external_melissa_choices())) timeout 5.0\n' % prefix


TEST_RPY = r'''
init python:
    def external_melissa_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_melissa_button(prefix):
        index = next(index for index, caption in enumerate(external_melissa_choices()) if caption.startswith(prefix))
        return "choice_panel_button_%d" % index

    def external_melissa_prepare():
        for thread in threads.values():
            thread.abort()
        event_runtime.available.clear()
        event_runtime.fired_keys_today = []
        event_runtime.evaluation_time = None
        tractir_progress.activated_achievements.discard("melissa_full_storeroom")
        tractir_progress.achieved.discard("melissa_full_storeroom")
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        player.tavern_management.cleanliness = 100
        tavern.renovations = {key: TavernRenovation(key) for key in TAVERN_RENOVATIONS}
        tavern_storage_supplies_stock().clear()
        tavern_storage_supplies_effects().clear()
        household.seen.clear()
        household.meta["friction"] = 0
        household.morning_state.clear()
        player.set_money(5000)
        player.tavern_management.productnum = 0
        player.tavern_management.winenum = 0
        player.chores.weekly["clean_upstairs_rooms"] = 0
        Melissa.comfort_cleaning_score = 0
        Melissa.comfort_interaction_score = 0
        Melissa.household_satisfaction = 0
        Melissa.rel = 15
        Melissa.trust = 5
        Melissa.corruption = 3
        Melissa.energy = 100
        Melissa.set_arousal(0)
        Melissa.asked_today = 0
        Melissa.talked_today = 0
        Melissa.temp_room_code = ""
        calendar_v2.daysInGame = 30
        calendar_v2.week = 2
        calendar_v2.hour = 9
        calendar_v2.minute = 0
        for person_id in ("melissa", "sandra"):
            people.get_data(person_id).set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
        people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernMain", start_minute=0, end_minute=1440, priority=999)])
        rooms.enter("TavernKitchen")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_items = []
        scene_runtime.picture = "images/tavern/kitchen/kitchen_room.png"
        scene_runtime.text = "EXTERNAL_MELISSA_ROOM_ORIGIN"
        scene_runtime.location_text = scene_runtime.text
        renpy.show_screen("main_ui")

testsuite global:
    before testcase:
        run Jump("dev_after_report_checkpoint")
        advance until screen "main_ui" timeout 25.0
        $ external_melissa_prepare()
    teardown:
        exit

testcase external_melissa_stock_purchase_only_satisfaction:
    parameter shop = ["GroceryStore", "WineStore"]
    run Call(shop + "BuyStockMenu")
    advance until eval (main_ui_runtime.action_title in ("Покупка провизии", "Покупка вина")) timeout 20.0
    run (next(item.action for item in main_ui_runtime.action_items if item.caption.startswith("Купить один")))
    advance until eval (Melissa.household_satisfaction == 2) timeout 20.0
    python:
        assert Melissa.trust == 5 and Melissa.comfort_interaction_score == 0 and Melissa.rel == 15
        assert player.economy.money == 5000 - (6 if shop == "GroceryStore" else 14)
        assert "melissa_full_storeroom" not in tractir_progress.activated_achievements
    run Call(shop + "BuyStockApply", 0, 0, 0)
    advance until eval ("решили пока ничего" in scene_runtime.text) timeout 20.0
    assert eval (Melissa.household_satisfaction == 2) timeout 5.0

testcase external_melissa_kitchen_choices:
    parameter case = [(5, False, "Пообещать", 0), (100, False, "Пообещать", 1), (100, True, "Пообещать", 2), (100, "bear", "Пообещать", 2), (100, True, "Сказать", -1)]
    python:
        food, forest, reply, delta = case
        player.tavern_management.productnum = food
        if forest == "bear":
            tavern_storage_supplies_effects()["bear_days"] = 14
        elif forest:
            tavern_storage_supplies_stock()["berries_001"] = 3
        _melissa_origin = main_ui_context_snapshot()
        _melissa_read = []
    run Call("HouseholdEvent_Try", "TavernKitchen", "room")
    advance until screen "choice" timeout 20.0
{READ_TO_ACTIONS}
    python:
        assert any(("Провизии осталось мало" if food < 100 else "С провизией сейчас порядок") in text for text in _melissa_read)
        assert not any("EXTERNAL_MELISSA_ROOM_ORIGIN" in text for text in _melissa_read)
        assert external_melissa_choices() == ["Пообещать разобраться с припасами", "Сказать, чтобы справлялась с тем, что есть", "Спросить, что ей нужнее всего"]
    if eval (forest == "bear"):
        pause 0.2
        $ renpy.screenshot(config.basedir + "/melissa-kitchen-count.png")
    click id (external_melissa_button(reply)) pos (0.5, 0.5)
    advance until eval ("Закончить разговор" in external_melissa_choices()) timeout 20.0
    assert eval (Melissa.trust == 5 + delta and Melissa.comfort_interaction_score == delta and Melissa.rel == 15) timeout 5.0
    click id (external_melissa_button("Закончить")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene") timeout 20.0
    assert eval (main_ui_context_snapshot() == _melissa_origin) timeout 5.0
    assert eval (household_ai_pick_event("TavernKitchen", "room") != "household_event_kitchen_melissa_practical_complaint") timeout 5.0

testcase external_melissa_needs_only_unfinished:
    parameter completed = [False, True]
    python:
        player.tavern_management.productnum = 101
        werecat_state()["rats_problem_active"] = 0 if completed else 1
        threads["melissaBatProblem"].num = 7 if completed else 0
        if completed:
            for code in ("roof", "backyard", "shed"):
                tavern.renovations[code].status = "completed"
            player.chores.weekly["clean_upstairs_rooms"] = 1
        _melissa_read = []
    run Call("HouseholdEvent_Try", "TavernKitchen", "room")
    advance until screen "choice" timeout 20.0
{READ_TO_ACTIONS}
    click id (external_melissa_button("Спросить, что")) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
{READ_TO_FINISH}
    $ _melissa_read.append(scene_runtime.text)
    python:
        read_text = "\n".join(_melissa_read)
        for marker in ("Избавь нас от крыс", "ремонт моей комнаты", "порядок двор", "нужник нужно", "На этой неделе", "Прачечная"):
            assert (marker in read_text) != completed, (marker, read_text)
        assert ("все сделано" in read_text) == completed
        assert all(job.status != "accepted" for job in tavern.renovations.values())

testcase external_melissa_needs_leads_to_renovation_event:
    $ threads["tavernRenovations"] = UThreadInfo(threadData["tavernRenovations"])
    $ _melissa_read = []
    $ _kitchen_origin = main_ui_context_snapshot()
    run Call("HouseholdEvent_Try", "TavernKitchen", "room")
    advance until screen "choice" timeout 20.0
{READ_TO_ACTIONS}
    click id (external_melissa_button("Спросить, что")) pos (0.5, 0.5)
    advance until screen "choice" timeout 20.0
{READ_TO_FINISH}
    click id (external_melissa_button("Закончить")) pos (0.5, 0.5)
    advance until eval ("Хорошо, закажу работу у Драупнира" in external_melissa_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and main_ui_runtime.action_items == [])
    click id (external_melissa_button("Хорошо, закажу")) pos (0.5, 0.5)
    advance until eval ("Вернуться к разговору" in external_melissa_choices()) timeout 20.0
    click id (external_melissa_button("Вернуться к разговору")) pos (0.5, 0.5)
    advance until eval (not external_melissa_choices()) timeout 20.0
    assert eval (tavern.renovations["backyard"].status == "accepted")
    assert eval (main_ui_context_snapshot() == _kitchen_origin)

testcase external_melissa_reward_by_current_state:
    parameter state = [(4, 30, 80, 100, "сдержанно благодарит"), (15, 3, 80, 100, "быстро целует"), (15, 20, 0, 100, "запишем в долг"), (15, 20, 80, 100, "особая благодарность"), (15, 20, 80, 20, "Сегодня сил совсем мало")]
    python:
        Melissa.rel, Melissa.corruption, arousal, Melissa.energy, expected = state
        Melissa.set_arousal(arousal)
        player.tavern_management.productnum = 101
        player.tavern_management.winenum = 500
        _melissa_read = []
    run Call("HouseholdEvent_Try", "TavernKitchen", "room")
    advance until screen "choice" timeout 20.0
{READ_TO_ACTIONS}
    python:
        assert expected in "\n".join(_melissa_read), _melissa_read
        assert "melissa_full_storeroom" in tractir_progress.achieved
        assert "melissaStoreroomMilestone" not in threads
    click id (external_melissa_button("Пообещать")) pos (0.5, 0.5)
    advance until eval ("Закончить разговор" in external_melissa_choices()) timeout 20.0
    click id (external_melissa_button("Закончить")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene") timeout 20.0
    $ household.seen.clear()
    $ _melissa_read = []
    run Call("HouseholdEvent_Try", "TavernKitchen", "room")
    advance until screen "choice" timeout 20.0
{READ_TO_ACTIONS}
    assert eval ("Вот теперь действительно полная кладовая" not in "\n".join(_melissa_read)) timeout 5.0

testcase external_melissa_no_reward_in_talk_or_purchase:
    python:
        player.tavern_management.productnum = 101
        player.tavern_management.winenum = 500
        Melissa.record_stock_growth()
        assert "melissa_full_storeroom" not in tractir_progress.activated_achievements
        assert not story_event_available("talk_melissa", "storeroom_thanks")
    run Call("IntMelissaTalk")
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "talk" and "Осмотреть" in external_melissa_choices()) timeout 5.0

testcase external_melissa_count_follows_played_argument:
    python:
        people.get_data("amanda").set_schedule([NPCScheduleEntry(location="TavernKitchen", start_minute=0, end_minute=1440, priority=999)])
        household.meta["friction"] = 0.8
        assert household_ai_pick_event("TavernKitchen", "room") == "household_event_kitchen_amanda_sandra_spark"
        household_ai_mark_seen("household_event_kitchen_amanda_sandra_spark", "TavernKitchen")
        assert household_ai_pick_event("TavernKitchen", "room") == "household_event_kitchen_melissa_practical_complaint"
        household_ai_mark_seen("household_event_kitchen_melissa_practical_complaint", "TavernKitchen")
        assert household_ai_pick_event("TavernKitchen", "room") == "household_event_breakfast_squirrel_mockery"

testcase external_melissa_count_threshold:
    parameter stock = [(100, 500, False), (101, 499, False), (101, 500, True)]
    python:
        player.tavern_management.productnum, player.tavern_management.winenum, expected = stock
        _melissa_read = []
    run Call("HouseholdEvent_Try", "TavernKitchen", "room")
    advance until screen "choice" timeout 20.0
{READ_TO_ACTIONS}
    assert eval (("melissa_full_storeroom" in tractir_progress.achieved) == expected) timeout 5.0

testcase external_melissa_save_migration:
    parameter played = [False, True]
    python:
        # Same saved ThreadInfo schema; migration reads only completion state.
        old = LThreadInfo(threadData["melissaBatProblem"])
        old.completed = played
        threads["melissaStoreroomMilestone"] = old
        tractir_progress.activated_achievements.add("melissa_full_storeroom")
        tractir_progress.achieved.add("melissa_full_storeroom")
        del Melissa.comfort_interaction_score
        Melissa.household_satisfaction = 8
        Melissa.comfort_cleaning_score = -2
        before_inventory = dict(player.inventory.items)
        updateSave_V95()
        assert "melissaStoreroomMilestone" not in threads
        assert ("melissa_full_storeroom" in tractir_progress.achieved) == played
        assert Melissa.comfort_interaction_score == 0
        assert Melissa.household_satisfaction == 8 and Melissa.comfort_cleaning_score == -2
        Melissa.comfort_interaction_score = 3
        updateSave_V95()
        assert Melissa.comfort_interaction_score == 3
        assert player.inventory.items == before_inventory
        restored = __import__("pickle").loads(__import__("pickle").dumps(Melissa))
        assert restored.comfort_interaction_score == 3
        renpy.save("external-melissa-kitchen", include_screenshot=False)
        assert renpy.can_load("external-melissa-kitchen")
'''.replace("{READ_TO_ACTIONS}", read_until_choice("Пообещать")).replace("{READ_TO_FINISH}", read_until_choice("Закончить"))


if __name__ == "__main__":
    isolated.TEST_RPY = TEST_RPY
    raise SystemExit(isolated.main())
