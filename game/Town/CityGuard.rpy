# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default CityGuardSavedText = ""

init python:
    def city_guard_open_now():
        return (week == 2 and time == 2) or (week == 5 and time == 0)

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
    $ CityGuardSavedText = MainTxt
    $ CityGuardRoom.mark_visited()

    if int(MongolVar.get("StocksArrestDay", -1) or -1) >= 0 and int(MongolVar.get("StocksSeen", 0) or 0) == 0:
        call story_clara_market_booklet_city_guard_direct
    else:
        call RoomEnterEventGate(CurLoc, False)

    if CityGuardRoom.is_open(week, time):
        call ShowImage("Zimmer", "", "Portrait1")
    else:
        call ShowImage("general", "", "cityguard")

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

    python:
        for _guard_object in CityGuardRoom.visible_objects():
            current_action_items.append(MenuItem(_guard_object.name, Call("CityGuardObjectMenu", _guard_object.object_id)))

    if CityGuardRoom.is_open(week, time):
        $ current_action_items.append(MenuItem("Десятник Циммерман", Call("IntZimmerTalk")))
    if (not CityGuardRoom.is_open(week, time)) and int(MongolVar.get("StocksArrestDay", -1) or -1) >= 0 and int(MongolVar.get("StocksSeen", 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Подойти к колодкам у караулки", Call("story_clara_market_booklet_city_guard_direct")))
    if int(MongolVar.get("StocksSeen", 0) or 0) == 1 and int(MongolVar.get("StocksFoodDay", -1) or -1) < 0 and int(time or 0) >= 4 and int(productnum or 0) > 0:
        $ current_action_items.append(MenuItem("Передать Монголу еду из трактира", Call("story_clara_market_booklet_feed_mongol_direct")))
    if int(DraupnirVar.get("MongolLockpickOrderDay", -1) or -1) >= 0 and int(MongolVar.get("StocksReleased", 0) or 0) == 0 and int(time or 0) >= 4 and int(dayspassed or 0) > int(MongolVar.get("StocksFoodDay", -1) or -1) and int(productnum or 0) > 0 and int(winenum or 0) > 0:
        $ current_action_items.append(MenuItem("Послать стражникам вино и угощение, а затем освободить Монгола", Call("story_clara_market_booklet_release_mongol_direct")))

    $ current_action_items.append(MenuItem("Вернуться на рынок", Jump("MarketPlace")))
    return


label CityGuardObjectMenu(object_id=""):
    $ _city_guard_object = None
    python:
        for _room_object in CityGuardRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _city_guard_object = _room_object
                break

    if _city_guard_object is None:
        call CityGuardBuildActions
        return

    $ MainTxt = _city_guard_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _city_guard_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _guard_action in _city_guard_object.visible_actions():
            if _guard_action.hook == "text":
                current_action_items.append(MenuItem(_guard_action.label, Call("CityGuardObjectText", object_id, _guard_action.action_id)))
            elif _guard_action.hook == "call" and str(_guard_action.target or "") != "":
                _guard_args = tuple(getattr(_guard_action, "args", ()) or ())
                current_action_items.append(MenuItem(_guard_action.label, Call(_guard_action.target, *_guard_args)))
            elif _guard_action.hook == "jump" and str(_guard_action.target or "") != "":
                current_action_items.append(MenuItem(_guard_action.label, Jump(_guard_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("CityGuardRestore")))
    return


label CityGuardObjectText(object_id="", action_id=""):
    python:
        _guard_text = ""
        _guard_name = ""
        for _room_object in CityGuardRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _guard_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _guard_text = str(_room_action.target or "")
                    break
            break
        if _guard_text:
            MainTxt = _guard_text
            CurLocDesc = _guard_text
            current_action_title = _guard_name or "Действия"
    call CityGuardObjectMenu(object_id)
    return


label CityGuardShowPlacat:
    $ RandVar = renpy.random.randint(1, 8)
    $ MainTxt = CityGuardPlacat[RandVar]
    $ CurLocDesc = MainTxt
    call ShowImage("general", "soldierplakat", "plakat" + str(RandVar))
    $ current_action_title = "Расписные доски"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Посмотреть на другую доску", Call("CityGuardShowPlacat")))
    $ current_action_items.append(MenuItem("Назад", Call("CityGuardRestore")))
    return


label CityGuardRestore:
    $ MainTxt = CityGuardSavedText
    $ CurLocDesc = MainTxt
    if CityGuardRoom.is_open(week, time):
        call ShowImage("Zimmer", "", "Portrait1")
    else:
        call ShowImage("general", "", "cityguard")
    call CityGuardBuildActions
    return
