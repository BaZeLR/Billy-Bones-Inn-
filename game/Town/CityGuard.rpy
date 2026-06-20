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

    CityGuardRoom = Room(
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
            RoomExit(label="Вернуться на рынок", target="MarketPlace"),
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


label CityGuard:
    call EnterLocation("CityGuard")
    $ CurrentRoom = CityGuardRoom
    $ CurLoc = "CityGuard"
    $ location = CurLoc
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_object_id = ""
    $ _city_guard_desc_rows = CityGuardRoom.visible_descriptions()
    if len(_city_guard_desc_rows) > 0:
        $ MainTxt = _city_guard_desc_rows[0].text
    else:
        $ MainTxt = "Вы зашли в приемную городской стражи."
    $ CurLocDesc = MainTxt
    $ CityGuardRoom.mark_visited()

    call RoomEnterEventGate(CurLoc, False)

    if CityGuardRoom.is_open(week, time):
        vscene "images/zimmer/Portrait1.jpg"
    else:
        vscene "images/general/cityguard.jpg"

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться на рынок", Jump("MarketPlace"))]
        call screen main_ui
        jump CityGuard

    call CityGuardBuildActions
    call screen main_ui
    jump CityGuard


label CityGuardBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    if len(CityGuardRoom.visible_objects()) > 0:
        $ current_action_items.append(MenuItem("Расписные доски", Call("CityGuardShowPlacat")))

    if CityGuardRoom.is_open(week, time):
        $ current_action_items.append(MenuItem("Десятник Циммерман", Call("IntZimmerTalk")))
    if story_event_available("CityGuard", "enter"):
        $ current_action_items.append(MenuItem("Осмотреть колодки у караулки", Call("checkTriggers", "CityGuard", "enter", 0)))

    $ current_action_items.append(MenuItem("Вернуться на рынок", Jump("MarketPlace")))
    return


label CityGuardShowPlacat:
    $ RandVar = procedural_randint(1, 8, "city_guard_placard_%s_%s" % (dayspassed, int(clock_minutes or 0)))
    $ MainTxt = CityGuardPlacat[RandVar]
    $ CurLocDesc = MainTxt
    vscene "images/general/soldierplakat/plakat[RandVar].jpg"
    $ current_action_title = "Расписные доски"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Посмотреть на другую доску", Call("CityGuardShowPlacat")))
    $ current_action_items.append(MenuItem("Назад", Jump("CityGuard")))
    return
