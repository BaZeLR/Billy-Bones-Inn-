#!/usr/bin/env python3
"""Verify the scoped Sandra menu and Clara/Pauline handover in a copied game."""

import external_tavern_renovations_test as isolated


TEST_RPY = r'''
init python:
    def external_handover_choices():
        choice = renpy.get_screen("choice")
        return [str(item.caption or "") for item in choice.scope.get("items", [])] if choice else []

    def external_handover_button(caption):
        return "choice_panel_button_%d" % external_handover_choices().index(caption)

    def external_handover_prepare():
        for thread in threads.values():
            thread.abort()
        threads["claraPaintingsPath"].advanceTo(0)
        threads["claraMongolAccusation"].advanceTo(0)
        daily_events.rows = []
        calendar_v2.week = 2
        calendar_v2.hour = 9
        calendar_v2.minute = 0
        player.tavern_management.breakfast.today = True
        player.tavern_management.breakfast.event_active = False
        main_ui_runtime.clear_contexts()
        main_ui_runtime.mode = "scene"
        main_ui_runtime.overlay = ""
        Clara.jobs.clear()

testsuite global:
    teardown:
        exit

testcase external_clara_pauline_handover_room_and_talk:
    parameter route = ["paintings", "accusation"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_handover_prepare()
    assert eval (people.get_info("pauline") is Pauline and not Clara.is_tavern_worker()) timeout 5.0
    assert eval (people.location("pauline") == "") timeout 5.0
    python:
        if route == "paintings":
            threads["claraPaintingsPath"].advanceTo(14)
        else:
            threads["claraMongolAccusation"].advanceTo(4, complete_at_end=True)
        Pauline.known = False
        Pauline.rel = 7
    run Jump("WineStore")
    advance until eval (rooms.current_code == "WineStore" and main_ui_runtime.action_title == "Действия") timeout 20.0
    assert eval (Clara.is_tavern_worker() and "clara" in _tavern_team_keys() and "clara" in household.resident_ids()) timeout 5.0
    assert eval (Clara.tavern_job_available("jobkitchentomorrow") and Clara.tavern_job_available("jobcleaningtomorrow") and Clara.tavern_job_available("jobwaitresstomorrow")) timeout 5.0
    assert eval (people.location("clara") != "WineStore" and "pauline" in people.ids_at("WineStore")) timeout 5.0
    assert eval (wine_store_seller_id() == "pauline" and wine_store_seller_name() == "Полина") timeout 5.0
    assert eval ("За прилавком вместо неё Полина" in scene_runtime.text and people.action_data_for_room("pauline", "WineStore")["talk_label"] == "IntPaulineTalk") timeout 5.0
    $ _handover_origin = main_ui_context_snapshot()
    run Call("IntPaulineTalk")
    advance until screen "choice" timeout 20.0
    assert eval (Pauline.known and external_handover_choices() == ["Назад"] and "Меня зовут Полина" in scene_runtime.text) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_handover_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _handover_origin and Pauline.rel == 7) timeout 5.0
    run Call("IntPaulineTalk")
    advance until screen "choice" timeout 20.0
    assert eval ("Здравствуйте, Стефан" in scene_runtime.text and "Меня зовут" not in scene_runtime.text) timeout 5.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_handover_choices()) timeout 20.0
    assert eval (main_ui_context_snapshot() == _handover_origin and Pauline.rel == 7) timeout 5.0

testcase external_pauline_follows_actual_room_hours:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_handover_prepare()
    $ threads["claraPaintingsPath"].advanceTo(14)
    python:
        for weekday, hour, minute in [(1, 5, 59), (1, 6, 0), (2, 16, 59), (2, 17, 1), (5, 14, 59), (5, 15, 1), (7, 9, 0)]:
            calendar_v2.week, calendar_v2.hour, calendar_v2.minute = weekday, hour, minute
            opened = rooms.get("WineStore").is_open()
            assert (people.location("pauline") == "WineStore") == opened
            assert (people.action_data_for_room("pauline", "WineStore") is not None) == opened
        assert Pauline.job_value("jobWhoreAvail", 0) == 0
        assert not Pauline.is_tavern_worker()

testcase external_pauline_save_registration_preserves_state:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_handover_prepare()
    python:
        Pauline.rel = 8
        Pauline.known = True
        Pauline.set_var_int("test_story_progress", 3)
        _handover_pauline = Pauline
        _handover_wardrobe = Pauline.wardrobe
        people.runtime.pop("pauline")
        people.definitions.pop("pauline")
        updateSave_V98()
        assert people.get_info("pauline") is _handover_pauline
        assert Pauline.wardrobe is _handover_wardrobe
        assert Pauline.rel == 8 and Pauline.known and Pauline.var_int("test_story_progress") == 3
        people.repair()
        npc_schedule_after_load()
        assert people.get_info("pauline") is _handover_pauline
        assert Pauline.rel == 8 and Pauline.known and Pauline.var_int("test_story_progress") == 3
    $ renpy.save("external-pauline-serialization", include_screenshot=False)
    assert eval (renpy.can_load("external-pauline-serialization")) timeout 5.0

testcase external_sandra_single_entry_preserves_inner_menu:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_handover_prepare()
    $ rooms.enter("TavernSandraRoom")
    $ people.get_data("sandra").set_schedule([NPCScheduleEntry(location="TavernSandraRoom", start_hour=0, end_hour=24, priority=999)])
    $ threads["sandraWeeklyEvaluation"].advanceTo(5, complete_at_end=True)
    $ Sandra.fucked_today = 0
    $ player.intimacy.came_today = 0
    $ Sandra.asked_today = 1
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    assert eval ([item.caption for item in main_ui_runtime.action_items if "Санд" in item.caption] == ["Заняться сексом с Сандрой"]) timeout 5.0
    run Call("IntSandraTalk")
    advance until screen "choice" timeout 20.0
    assert eval (external_handover_choices().count("Заняться сексом с Сандрой") == 1) timeout 5.0
    assert eval ("Попросить Сандру помочь рукой" not in external_handover_choices() and "Попросить Сандру сделать минет" not in external_handover_choices()) timeout 5.0
    click id (external_handover_button("Заняться сексом с Сандрой")) pos (0.5, 0.5)
    advance until eval ("Остановиться" in external_handover_choices()) timeout 20.0
    assert eval ("Попросить помочь рукой" in external_handover_choices() and "Попросить сделать минет" in external_handover_choices()) timeout 5.0
    click id (external_handover_button("Остановиться")) pos (0.5, 0.5)
    advance until eval (external_handover_choices() == ["Закончить близость"]) timeout 20.0
    click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_handover_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernSandraRoom" and main_ui_runtime.scene_origin is None) timeout 5.0
'''


if __name__ == "__main__":
    isolated.TEST_RPY = TEST_RPY
    raise SystemExit(isolated.main())
