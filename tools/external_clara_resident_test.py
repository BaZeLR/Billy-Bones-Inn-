#!/usr/bin/env python3
"""Native resident scenes plus renovation regressions, in an isolated copy."""
import external_tavern_renovations_test as copied


TEST_RPY = r'''
init python:
    def external_clara_resident_prepare():
        external_renovation_prepare("guest_room")
        threads["tavernRenovations"].abort()
        threads["claraResidentLife"] = createThread(threadData["claraResidentLife"])
        Clara.jobs.clear()
        Clara.day_location_override_day = -1
        Clara.day_location_override_code = ""
        Clara.rel = 20
        Clara.corruption = 30
        Clara.flirted_today = 0
        Clara.anger_with_player = 0
        Clara.rebellion = 0
        Clara.mana = 40
        player.stats.charisma = 80
        player.stats.exploration = 80
        household.barber_appointments.clear()
        for person in ("sandra", "melissa", "amanda"):
            household.morning_state[_household_morning_state_key(person)] = {"issue": "", "resolved": 1, "indecent": 0}
        tavern.renovations["peephole"].status = "completed"
        calendar_v2.hour = 10
        rooms.enter("TavernMyRoom")
        findAvailableEvents(True)

    def external_clara_resident_text_count():
        from renpy.text.text import Text
        from renpy.test.testfocus import focus_from_displayable
        rows, seen = [], set()
        def collect(displayable):
            if id(displayable) in seen or not isinstance(displayable, Text):
                return
            seen.add(id(displayable))
            if focus_from_displayable(displayable) is not None:
                rows.append("".join(part for part in displayable.text if isinstance(part, str)))
        for name in ("main_ui", "choice", "say"):
            screen = renpy.get_screen(name)
            if screen is not None:
                screen.visit_all(collect)
        return sum(row.count(scene_runtime.text) for row in rows) if scene_runtime.text else 0

testcase external_clara_drawing_room_entry:
    parameter option = ["Спросить о рисунках", "Попробовать поцеловать её", "Оставить её рисовать"]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_resident_prepare()
    $ before_rel = Clara.rel
    assert eval (Clara.drawing_now() and people.location("clara") == "TavernMyRoom")
    assert eval (Clara.interrupt_work() == "" and Clara.rel == before_rel)
    run Jump("TavernMyRoom")
    advance until screen "choice" timeout 20.0
    assert eval (main_ui_runtime.mode == "event" and not main_ui_runtime.action_items)
    assert eval (scene_runtime.picture == player_room_image_path("room"))
    pause 0.1
    assert eval (external_clara_resident_text_count() == 1)
    click id (external_renovation_button(option)) pos (0.5, 0.5)
    if eval (option != "Оставить её рисовать"):
        advance until eval ("Не мешать работе" in external_renovation_choices() or "Дать ей закончить" in external_renovation_choices()) timeout 20.0
        assert eval (scene_runtime.picture == ClaraStaticData.portrait)
        click id "choice_panel_button_0" pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (rooms.current_code == "TavernMyRoom" and main_ui_runtime.scene_origin is None)
    assert eval (scene_runtime.picture == tavern_my_room_scene_state()[0])
    assert eval (not story_event_available("TavernMyRoom", "enter"))
    assert eval (story_event_available("talk_clara", "drawing"))
    assert eval (Clara.rel == before_rel)

testcase external_clara_busy_flirt_returns_to_talk:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_resident_prepare()
    run Call("IntClaraTalk")
    advance until eval ("Флиртовать" in external_renovation_choices()) timeout 20.0
    $ before_rel = Clara.rel
    $ before_flirts = Clara.flirted_today
    click id (external_renovation_button("Флиртовать")) pos (0.5, 0.5)
    advance until eval ("Попробовать поцеловать её" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Попробовать поцеловать её")) pos (0.5, 0.5)
    advance until eval ("Дать ей закончить" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Дать ей закончить")) pos (0.5, 0.5)
    advance until eval ("Флиртовать" in external_renovation_choices()) timeout 20.0
    assert eval (main_ui_runtime.mode == "talk" and rooms.current_code == "TavernMyRoom")
    assert eval (Clara.rel == before_rel and Clara.flirted_today == before_flirts)
    click id (external_renovation_button("Назад")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0

testcase external_clara_breakfast_banter_return_and_daily_limit:
    parameter encourage = [False, True]
    parameter joke = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_resident_prepare()
    $ calendar_v2.hour = 8
    $ rooms.enter("TavernKitchen")
    python:
        for sample_day in range(30, 300):
            calendar_v2.daysInGame = sample_day
            if procedural_randint(0, 10, "clara_breakfast_banter") == joke:
                break
        else:
            raise AssertionError("No actual calendar seed found for breakfast anecdote %s" % joke)
    assert eval (household_breakfast_attendee_ids().count("clara") == 1)
    $ player.tavern_management.breakfast.event_active = True
    $ player.tavern_management.breakfast.present_ids = household_breakfast_attendee_ids()
    $ before_stats = {key: (people.get_info(key).mana, people.get_info(key).corruption) for key in tavern_breakfast_present_ids()}
    $ before_context = main_ui_context_snapshot()
    assert eval (story_event_available("TavernKitchen", "breakfast"))
    run Call("checkTriggers", "TavernKitchen", "breakfast", 0)
    advance until eval ("Слушать дальше" in external_renovation_choices()) timeout 20.0
    assert eval (_clara_breakfast_joke == joke)
    assert eval (["маскарад", "три пальца", "прачку", "запасную", "воз с сеном", "десять девственниц", "свою тоже", "Николас", "двенадцатью спицами", "черти", "рукоблудием"][joke] in scene_runtime.text)
    assert eval (main_ui_runtime.mode == "event" and not main_ui_runtime.action_items)
    pause 0.1
    assert eval (external_clara_resident_text_count() == 1)
    click id (external_renovation_button("Слушать дальше")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Поддержать её настроение" in external_renovation_choices()) timeout 20.0
    if eval (encourage):
        click id (external_renovation_button("Поддержать её настроение")) pos (0.5, 0.5)
        advance until eval (len(external_renovation_choices()) == 1) timeout 20.0
    click id (external_renovation_button("Вернуться к завтраку")) pos (0.5, 0.5)
    advance until eval (not external_renovation_choices()) timeout 20.0
    assert eval (player.tavern_management.breakfast.event_active and rooms.current_code == "TavernKitchen")
    assert eval (main_ui_context_snapshot() == before_context)
    assert eval (not story_event_available("TavernKitchen", "breakfast"))
    python:
        for key, (mana, corruption) in before_stats.items():
            assert people.get_info(key).mana == min(100, mana + int(encourage))
            assert people.get_info(key).corruption == corruption
    run Call("TavernKitchenBreakfastMenu")
    advance until screen "choice" timeout 20.0
    assert eval (player.tavern_management.breakfast.event_active)

testcase external_clara_resident_meals_and_absence:
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_resident_prepare()
    $ calendar_v2.week = 7
    $ calendar_v2.hour = 13
    assert eval (people.location("clara") == "TavernKitchen")
    assert eval (tavern_sunday_dinner_present_ids().count("clara") == 1)
    assert eval (tavern_kitchen_sunday_dinner_picture() == "images/kitchen/renewed/sunday_clarissa.png")
    assert eval (tavern_sunday_lake_walk_candidate(["clara"]) == "clara")
    $ calendar_v2.hour = 8
    $ threads["claraMongolAccusation"].done[0] = True
    $ threads["claraMongolAccusation"].done[2] = False
    assert eval ("clara" not in household_breakfast_attendee_ids())
    assert eval (people.location("clara") == "")
    $ threads["claraMongolAccusation"].done[0] = False
    $ threads["claraPaintingsPath"].num = 0
    $ threads["claraPaintingsPath"].completed = False
    assert eval (not Clara.tavern_resident())
    assert eval ("clara" not in household_breakfast_attendee_ids())

testcase external_clara_sunday_dinner_story:
    parameter homewear = [False, True]
    run Jump("dev_after_report_checkpoint")
    advance until screen "main_ui" timeout 25.0
    $ external_clara_resident_prepare()
    $ calendar_v2.daysInGame = 35 if homewear else 30
    $ calendar_v2.week = 7
    $ calendar_v2.hour = 13
    $ rooms.enter("TavernKitchen")
    assert eval (tavern_sunday_dinner_available())
    assert eval (tavern_kitchen_sunday_dinner_picture() == "images/kitchen/renewed/sunday_clarissa.png")
    run Call("TavernKitchenSundayDinner", 0)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Послушать историю Клариссы" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Послушать историю Клариссы")) pos (0.5, 0.5)
    advance until eval ("Слушать дальше" in external_renovation_choices()) timeout 20.0
    assert eval (scene_runtime.picture == "images/kitchen/renewed/clarissa_story_homewear.png" if homewear else scene_runtime.picture == "images/kitchen/renewed/clarissa_story_cozy.png")
    assert eval ("Кларисса устраивается рядом с Мелиссой" in scene_runtime.text)
    click id (external_renovation_button("Слушать дальше")) pos (0.5, 0.5)
    advance until eval ("Вернуться к обеду" in external_renovation_choices()) timeout 20.0
    click id (external_renovation_button("Вернуться к обеду")) pos (0.5, 0.5)
    advance until eval ("Закончить воскресный обед" in external_renovation_choices()) timeout 20.0
    assert eval (scene_runtime.picture == ("images/kitchen/renewed/sunday_clarissa_homewear.png" if homewear else "images/kitchen/renewed/sunday_clarissa.png"))
    assert eval ("Послушать историю Клариссы" not in external_renovation_choices())
    click id (external_renovation_button("Закончить воскресный обед")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices() or "Сегодня остаться в трактире" in external_renovation_choices()) timeout 20.0
    if eval ("Продолжить" in external_renovation_choices()):
        click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Продолжить" in external_renovation_choices() or "Сегодня остаться в трактире" in external_renovation_choices() or main_ui_runtime.scene_origin is None) timeout 20.0
    if eval ("Продолжить" in external_renovation_choices()):
        click id (external_renovation_button("Продолжить")) pos (0.5, 0.5)
    advance until eval ("Сегодня остаться в трактире" in external_renovation_choices() or main_ui_runtime.scene_origin is None) timeout 20.0
    if eval ("Сегодня остаться в трактире" in external_renovation_choices()):
        click id (external_renovation_button("Сегодня остаться в трактире")) pos (0.5, 0.5)
    advance until eval (main_ui_runtime.scene_origin is None) timeout 20.0
    assert eval (Clara.current_dress() == "greenworkdress")
'''


if __name__ == "__main__":
    copied.TEST_RPY += TEST_RPY
    raise SystemExit(copied.main())
