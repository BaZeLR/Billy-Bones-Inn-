# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def city_guard_open_now():
        current_weekday = int(calendar_v2.week or 0)
        if current_weekday == 2:
            return calendar_v2.is_between_clock(11, 0, 12, 59)
        if current_weekday == 5:
            return calendar_v2.is_between_clock(6, 0, 7, 59)
        return False

    def city_guard_closed_now():
        return not city_guard_open_now()

    CityGuardPlacat = {
        1: "Падонак: Помни-\nРубить рыцаря - МАЛО!\nКоли рыцарюгу алебардой в хлебало!",
        2: "Строй, МЛЯ, имеет значение!",
        3: "Даже в самые критические дни я чувствую себя сухо и комфортно в готическом доспехе!",
        4: "Пихота она как дите! Во всем найдет красоту!",
        5: "Пехота:\nПапав во врага окружение-\nЕбошь его гада, на паражение!",
        6: "Пихатинец умелый, сматри чо делать:\nСлабай ударно на всякий пожарный!\nАлибарда, Видро, П..ц",
        7: "Просто мы любим свою работу...",
        8: "Рыцарем быть - галимый ацтой!\nСлужи в пехоте парень простой!!!\nЧем куртуазничать в беленьких латах,\nЕбошь алебардой! будь бразер, солдатом!",
    }

    CityGuardRoomDefinition = Room(
        code_name="CityGuard",
        display_name="Приемная городской стражи",
        bg_picture="images/general/cityguard.jpg",
        descriptions=[
            RoomDescription(
                text="Вы зашли в комнату, где городская стража принимает жалобщиков и записывает в свои ряды новобранцев. Ее стены обвешанны расписными досками, прославляющими оной стражи доблесть и храбрость, а также призывающими вступать в ее ряды. Лавок для посетителей и прочей роскоши не предусмотренно, а на единственном табурете сидит десятник Циммерман.",
                condition=city_guard_open_now,
                priority=200,
            ),
            RoomDescription(
                text="Прием посетителей производится только во вторник днем и в пятницу утром.",
                condition=city_guard_closed_now,
                priority=190,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на рынок", target="MarketPlace", minutes_to_pass=10),
        ],
        game_items=[
            GameObject(
                object_id="placards",
                name="Расписные доски",
                description="На стенах висят расписные доски с призывами и похвальбой городской страже.",
                condition=city_guard_open_now,
                actions=[
                    ObjectAction(
                        action_id="show_placard",
                        label="Посмотреть на доску",
                        hook="call",
                        target="CityGuardShowPlacat",
                    ),
                ],
            ),
        ],
        schedule=RoomSchedule(
            closed_text="Прием посетителей производится только во вторник днем и в пятницу утром.",
            condition=city_guard_open_now,
        ),
    )

    def city_guard_action_items():
        items = []
        if len(rooms.get("CityGuard").visible_objects()) > 0:
            items.append(MenuItem("Расписные доски", Call("CityGuardShowPlacat")))
        if story_event_available("menu_CityGuard", "mongol_stocks"):
            items.append(MenuItem("Осмотреть колодки у караулки", Call("checkTriggers", "menu_CityGuard", "mongol_stocks", 0)))
        elif story_event_available("CityGuard", "enter"):
            items.append(MenuItem("Осмотреть колодки у караулки", Call("checkTriggers", "CityGuard", "enter", 0)))
        items.extend(rooms.get("CityGuard").build_exit_items())
        return items


label CityGuard:
    $ renpy.dynamic("_city_guard_desc_rows")
    $ rooms.enter("CityGuard")
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.object_id = ""
    $ _city_guard_desc_rows = rooms.get("CityGuard").visible_descriptions()
    if len(_city_guard_desc_rows) > 0:
        $ scene_runtime.text = _city_guard_desc_rows[0].text
    else:
        $ scene_runtime.text = "Вы зашли в приемную городской стражи."
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.get("CityGuard").mark_visited()

    call RoomEnterEventGate(rooms.current_code, False)

    if rooms.get("CityGuard").is_open():
        vscene "images/zimmer/portrait1.png"
    else:
        vscene "images/general/cityguard.jpg"

    $ main_ui_runtime.action_items = city_guard_action_items()
    while True:
        call screen main_ui


label CityGuardShowPlacat:
    $ renpy.dynamic("RandVar", "_placard_picture")
    $ RandVar = procedural_randint(1, 8, "city_guard_placard_%s_%s" % (current_game_day(), int(calendar_v2.clock_minutes() or 0)))
    $ scene_runtime.text = CityGuardPlacat[RandVar]
    $ scene_runtime.location_text = scene_runtime.text
    $ _placard_picture = "images/zimmer/soldierplakat/plakat%s.jpg" % RandVar
    vscene _placard_picture
    $ main_ui_runtime.action_title = "Расписные доски"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.action_items.append(MenuItem("Посмотреть на другую доску", Call("CityGuardShowPlacat")))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", [SetField(main_ui_runtime, "action_title", "Действия"), SetField(main_ui_runtime, "action_content", None), SetField(main_ui_runtime, "action_items", city_guard_action_items()), Function(main_ui_restart_interaction)]))
    return
