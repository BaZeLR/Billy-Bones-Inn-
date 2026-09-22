#!/usr/bin/env python3
"""Run Melissa household integration cases using the isolated renovation runner.

Only copied scripts and temporary saves are modified. The runner's existing
--compile-lint and --keep-temp options also apply to this fixture.
"""

import external_tavern_renovations_test as isolated


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
        threads["melissaStoreroomMilestone"].reset()
        event_runtime.available.clear()
        event_runtime.fired_keys_today = []
        event_runtime.evaluation_time = None
        tractir_progress.activated_achievements.discard("melissa_full_storeroom")
        tractir_progress.achieved.discard("melissa_full_storeroom")
        player.tavern_management.breakfast.event_active = False
        player.tavern_management.breakfast.present_ids = None
        tavern.renovation_due_days = {}
        player.set_money(5000)
        player.tavern_management.productnum = 0
        player.tavern_management.winenum = 0
        Melissa.comfort_cleaning_score = 0
        Melissa.household_satisfaction = 0
        Melissa.rel = 15
        Melissa.asked_today = 0
        Melissa.talked_today = 0
        calendar_v2.daysInGame = 30
        calendar_v2.week = 2
        calendar_v2.hour = 9
        calendar_v2.minute = 0
        rooms.enter("TavernStorage")
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_items = []
        scene_runtime.picture = "images/tavern/storage/storage_room.png"
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

testcase external_melissa_stock_purchase:
    parameter shop = ["GroceryStore", "WineStore"]
    run Call(shop + "BuyStockMenu")
    advance until eval (main_ui_runtime.action_title in ("Покупка провизии", "Покупка вина")) timeout 20.0
    run (next(item.action for item in main_ui_runtime.action_items if item.caption.startswith("Купить один")))
    advance until eval (Melissa.household_satisfaction == 2) timeout 20.0
    python:
        assert player.tavern_management.productnum == (10 if shop == "GroceryStore" else 0)
        assert player.tavern_management.winenum == (10 if shop == "WineStore" else 0)
        assert player.economy.money == 5000 - (6 if shop == "GroceryStore" else 14)
        assert Melissa.rel == 15
        assert "melissa_full_storeroom" not in tractir_progress.activated_achievements
    run Call(shop + "BuyStockApply", 0, 0, 0)
    advance until eval ("решили пока ничего" in scene_runtime.text) timeout 20.0
    assert eval (Melissa.household_satisfaction == 2) timeout 5.0
    $ player.set_money(0)
    run Call(shop + "BuyStockMenu")
    advance until eval (main_ui_runtime.action_title in ("Покупка провизии", "Покупка вина")) timeout 20.0
    assert eval (not any(item.caption.startswith("Купить") for item in main_ui_runtime.action_items)) timeout 5.0

testcase external_melissa_food_deposit:
    python:
        player.inventory.items["honey_comb_001"] = 3
        before_stock = tavern_kitchen_food_stock_count("honey_comb_001")
        assert tavern_kitchen_deposit_food("honey_comb_001", 2) == 2
        assert tavern_kitchen_food_stock_count("honey_comb_001") == before_stock + 2
        assert player.item_count("honey_comb_001") == 1
        assert Melissa.household_satisfaction == 2
        assert tavern_kitchen_deposit_food("honey_comb_001", 1) == 1
        assert Melissa.household_satisfaction == 4
        assert tavern_kitchen_deposit_food("honey_comb_001", 1) == 0
        assert tavern_kitchen_deposit_food("nonexistent_item", 1) == 0
        assert Melissa.household_satisfaction == 4
        assert Melissa.rel == 15

testcase external_melissa_threshold_and_event_scope:
    parameter stock = [(100, 500, False), (101, 499, False), (101, 500, True)]
    python:
        food, wine, expected = stock
        player.tavern_management.productnum = food
        player.tavern_management.winenum = wine
        Melissa.record_stock_growth()
        assert story_event_available("talk_melissa", "storeroom_thanks") == expected
        assert Melissa.household_satisfaction == 2
        assert all(project.is_hidden for project in TAVERN_RENOVATIONS.values())
        assert rooms.get("ShedWashroom").is_hidden

testcase external_melissa_priorities_return_to_talk:
    $ _melissa_room_origin = main_ui_context_snapshot()
    run Call("IntMelissaTalk")
    advance until screen "choice" timeout 20.0
    click id (external_melissa_button("Спросить, что для нее")) pos (0.5, 0.5)
    advance until eval ("Выслушать" in external_melissa_choices()) timeout 20.0
    python:
        assert main_ui_runtime.mode == "event"
        assert main_ui_runtime.action_items == []
        assert "EXTERNAL_MELISSA_ROOM_ORIGIN" not in scene_runtime.text
        assert scene_runtime.picture == "images/melissa/tavern/portrait.png"
    click id (external_melissa_button("Выслушать")) pos (0.5, 0.5)
    advance until eval ("Спросить о домашнем уюте" in external_melissa_choices()) timeout 20.0
    click id (external_melissa_button("Спросить о домашнем уюте")) pos (0.5, 0.5)
    advance until eval ("Посмотреть, что уже сделано" in external_melissa_choices()) timeout 20.0
    click id (external_melissa_button("Посмотреть, что уже сделано")) pos (0.5, 0.5)
    advance until eval ("Вернуться к разговору" in external_melissa_choices()) timeout 20.0
    assert eval ("Комфорт Мелиссы:" in scene_runtime.text and "Удовлетворенность хозяйством: 0" in scene_runtime.text) timeout 5.0
    click id (external_melissa_button("Вернуться к разговору")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "talk" and "Осмотреть" in external_melissa_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernStorage" and main_ui_runtime.scene_origin is None) timeout 5.0
    click id (external_melissa_button("Назад")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene") timeout 20.0
    assert eval (main_ui_context_snapshot() == _melissa_room_origin) timeout 5.0

testcase external_melissa_milestone_reward_once:
    parameter response = ["Улыбнуться", "Поблагодарить"]
    python:
        _melissa_room_origin = main_ui_context_snapshot()
        player.tavern_management.productnum = 101
        player.tavern_management.winenum = 500
        Melissa.record_stock_growth()
        # The earned scene remains pending even after normal stock consumption.
        player.tavern_management.productnum = 90
        player.tavern_management.winenum = 490
    run Call("IntMelissaTalk")
    advance until eval ("Продолжить" in external_melissa_choices()) timeout 20.0
    python:
        assert main_ui_runtime.mode == "event"
        assert main_ui_runtime.action_items == []
        assert "EXTERNAL_MELISSA_ROOM_ORIGIN" not in scene_runtime.text
        assert scene_runtime.picture == "images/melissa/happy.png"
        assert not threads["melissaStoreroomMilestone"].completed
    click id (external_melissa_button("Продолжить")) pos (0.5, 0.5)
    advance until eval (any(caption.startswith(response) for caption in external_melissa_choices())) timeout 20.0
    click id (external_melissa_button(response)) pos (0.5, 0.5)
    advance until eval ("Вернуться к разговору" in external_melissa_choices()) timeout 20.0
    click id (external_melissa_button("Вернуться к разговору")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "talk" and "Осмотреть" in external_melissa_choices()) timeout 20.0
    python:
        assert threads["melissaStoreroomMilestone"].completed
        assert threads["melissaStoreroomMilestone"].num == 1
        assert not story_event_available("talk_melissa", "storeroom_thanks")
        assert Melissa.household_satisfaction == 2
        assert Melissa.rel == 15
    click id (external_melissa_button("Назад")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.mode == "scene") timeout 20.0
    assert eval (main_ui_context_snapshot() == _melissa_room_origin) timeout 5.0
    run Call("IntMelissaTalk")
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "talk" and "Продолжить" not in external_melissa_choices()) timeout 5.0

testcase external_melissa_save_migration:
    python:
        del Melissa.comfort_cleaning_score
        del Melissa.household_satisfaction
        before_inventory = dict(player.inventory.items)
        before_threads = {name: (thread.num, thread.completed, thread.aborted) for name, thread in threads.items()}
        updateSave_V94()
        assert Melissa.comfort_cleaning_score == 0
        assert Melissa.household_satisfaction == 0
        Melissa.comfort_cleaning_score = -2
        Melissa.household_satisfaction = 8
        updateSave_V94()
        assert Melissa.comfort_cleaning_score == -2
        assert Melissa.household_satisfaction == 8
        assert player.inventory.items == before_inventory
        assert {name: (thread.num, thread.completed, thread.aborted) for name, thread in threads.items()} == before_threads
        import pickle
        restored = pickle.loads(pickle.dumps(Melissa))
        assert restored.comfort_cleaning_score == -2
        assert restored.household_satisfaction == 8
        assert restored.rel == Melissa.rel
        renpy.save("external-melissa-household", include_screenshot=False)
        assert renpy.can_load("external-melissa-household")
'''


if __name__ == "__main__":
    isolated.TEST_RPY = TEST_RPY
    raise SystemExit(isolated.main())
