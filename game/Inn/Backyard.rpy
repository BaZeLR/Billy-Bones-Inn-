# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def backyard_has_ash_barrel():
        return int(SoapAshBarrelInstalled or 0) == 1

    def backyard_has_dog_booth():
        try:
            ensure_dog_runtime()
            return bool(getattr(dog, "booth_built", False))
        except Exception:
            return False

    def backyard_ash_barrel_ready():
        return backyard_has_ash_barrel() and soap_ash_barrel_is_ready()

    def backyard_ash_barrel_description_text():
        if not backyard_has_ash_barrel():
            return ""
        if backyard_ash_barrel_ready():
            return "У стены стоит поставленная Драупниром зольная бочка. Щелок в ней уже настоялся, и теперь ее можно пустить в дело."
        days_left = max(0, int(SoapAshBarrelReadyDay or 0) - int(dayspassed or 0))
        if days_left <= 0:
            return "У стены стоит поставленная Драупниром зольная бочка. Щелок почти готов, осталось совсем немного подождать."
        return "У стены стоит поставленная Драупниром зольная бочка. Щелок в ней еще настаивается, до готовности остается примерно %s дн." % str(days_left)

    def backyard_dynamic_picture():
        if int(hour or 0) < 12 and int(week or 0) != 7:
            if str(getLocation("melissa") or "") == "Backyard":
                melissa_backyard = [
                    "images/melissa/tavern/backyard_0.png",
                    "images/melissa/tavern/backyard_1.png",
                ]
                melissa_backyard = [row for row in melissa_backyard if renpy.loadable(row)]
                if len(melissa_backyard) > 0:
                    return melissa_backyard[int((dayspassed or 0) + (hour or 0) + (minute or 0)) % len(melissa_backyard)]
            if str(getLocation("amanda") or "") == "Backyard" and renpy.loadable("images/tavern/backyard/backyard_chop_woods.png"):
                return "images/tavern/backyard/backyard_chop_woods.png"
        if backyard_has_ash_barrel() and renpy.loadable("images/tavern/backyard/soap_backyard.png"):
            return "images/tavern/backyard/soap_backyard.png"
        return str(BackyardRoom.bg_picture or "")

    def backyard_base_text():
        return "Вы выходите на задний двор трактира. Здесь грязь, лужи, следы копыт и старые доски под ногами. У стены стоит большая бочка с дождевой водой, рядом темнеет маленькое кострище, на веревке болтается выстиранное белье, а у забора растут кусты и старый дуб. В углу притулился кривой деревянный нужник.\n\nСтарый дуб нависает над частью двора и дает немного тени. Под ногами хлюпает разбитая грязь, в которой отпечатались сапоги, копыта и волочившиеся мешки. Колючие кусты вдоль забора цепляются за одежду и собирают на себя пыль, перья и всякий мелкий сор."

    def backyard_dynamic_text():
        base_text = backyard_base_text()
        if int(hour or 0) < 12 and int(week or 0) != 7:
            names_here = tavern_household_present_names("Backyard")
            if str(names_here or "").strip() and str(names_here or "") != "никто":
                base_text += "\n\nДо полудня во дворе возятся: %s." % str(names_here)
        if backyard_has_dog_booth():
            base_text += "\n\nУ стены возле сарая стоит крепкая собачья будка, которую сколотил Драупнир."
        werecat_text = werecat_visible_text("Backyard")
        if str(werecat_text or "").strip():
            base_text += "\n\n" + str(werecat_text or "").strip()
        ash_barrel_text = backyard_ash_barrel_description_text()
        if ash_barrel_text:
            return base_text + "\n\n" + ash_barrel_text
        return base_text

    BackyardRoom = Room(
        code_name="Backyard",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Задний двор",
        bg_picture="images/tavern/backyard/backyard_1.png",
        descriptions=[
            RoomDescription(
                text=backyard_base_text(),
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на кухню", target="TavernKitchen"),
            RoomExit(label="Идти к сараю", target="Shed"),
            RoomExit(label="Проверить конюшню", target="TavernStable"),
        ],
        game_items=[
            GameObject(
                object_id="backyard_toilet",
                name="Старый деревянный нужник",
                description="Покосившийся деревянный нужник стоит у самого забора. Дверца перекошена, петли скрипят, а внутри пахнет так, как и положено подобному месту.",
                actions=[
                    ObjectAction(action_id="examine_toilet", label="Осмотреть нужник", hook="call", target="BackyardToiletExamine"),
                ],
            ),
            GameObject(
                object_id="backyard_water_barrel",
                name="Бочка с дождевой водой",
                description="Большая бочка под водостоком почти всегда полна дождевой воды. Вода холодная, но для умывания сойдет.",
                actions=[
                    ObjectAction(action_id="wash_barrel", label="Умыться и ополоснуться", hook="call", target="Wash", args=("backyard_water_barrel", "Backyard", "Вы умываетесь и наскоро обмываетесь холодной дождевой водой. Это освежает и помогает привести себя в порядок.", "backyard_water_barrel")),
                    ObjectAction(action_id="examine_barrel", label="Осмотреть бочку", hook="text", target="Обычная большая бочка, куда стекает дождевая вода с крыши трактира."),
                ],
            ),
            GameObject(
                object_id="backyard_firepit",
                name="Кострище",
                description="Небольшое кострище, где можно сжечь мусор или быстро что-нибудь прогреть.",
                actions=[
                    ObjectAction(action_id="examine_firepit", label="Осмотреть кострище", hook="text", target="Здесь жгут мусор, сушат всякую дрянь и иногда разводят маленький огонь для хозяйственных нужд."),
                ],
            ),
            GameObject(
                object_id="backyard_laundry",
                name="Веревка с бельем",
                description="На длинной веревке развешано постиранное белье работников трактира.",
                actions=[
                    ObjectAction(action_id="examine_laundry", label="Осмотреть белье", hook="text", target="Рубахи, тряпки, чулки и прочая мелочь сушатся на ветру."),
                ],
            ),
            GameObject(
                object_id="backyard_ash_barrel",
                name="Зольная бочка",
                description="Деревянная бочка с устроенным для щелока дном. Здесь зола постепенно вымачивается водой, чтобы потом пойти на мыло.",
                picture="images/tavern/backyard/soap_backyard.png",
                actions=[
                    ObjectAction(action_id="inspect_ash_barrel", label="Осмотреть зольную бочку", hook="call", target="BackyardInspectAshBarrel"),
                ],
                condition=backyard_has_ash_barrel,
            ),
            GameObject(
                object_id="backyard_dog_booth",
                name="Собачья будка",
                description="Простая, но крепкая собачья будка, поставленная во дворе специально для вашего пса.",
                actions=[
                    ObjectAction(action_id="inspect_dog_booth", label="Осмотреть будку", hook="call", target="BackyardInspectDogBooth"),
                ],
                condition=backyard_has_dog_booth,
            ),
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "object_menu_label": "BackyardObjectMenu",
        },
    )


default BackyardToiletBusy = 0


label Backyard:
    call EnterLocation("Backyard")
    $ dog_prepare_current_spawn()
    $ CurrentRoom = BackyardRoom
    $ CurLoc = "Backyard"
    $ location = CurLoc
    call RoomEnterEventGate(CurLoc, False)
    $ scene_image = backyard_dynamic_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = backyard_dynamic_text()
    $ CurLocDesc = MainTxt
    $ BackyardSavedText = MainTxt
    $ current_action_title = "Задний двор"
    $ current_action_content = None
    $ current_action_items = []
    call BackyardBuildActions
    $ _backyard_ui_return = None
    while _backyard_ui_return is None:
        call screen main_ui
        $ _backyard_ui_return = _return
    jump Backyard


label BackyardBuildActions:
    $ BackyardSavedText = backyard_dynamic_text()
    $ current_action_title = "Задний двор"
    $ current_action_content = None
    $ current_action_items = []
    if soap_can_cook_at_backyard():
        $ current_action_items.append(MenuItem("Варить хозяйственное мыло", Call("BackyardCookSoap", "soap_recipe")))
    if soap_can_cook_luxury_at_backyard():
        $ current_action_items.append(MenuItem("Варить туалетное мыло с оливковым маслом", Call("BackyardCookSoap", "luxury_soap_recipe")))
    if player_can_train_shooting():
        $ current_action_items.append(MenuItem("Потренироваться в стрельбе", Call("ShootingPracticeMenu", "Backyard")))
    if werecat_is_in_room("Backyard"):
        $ current_action_items.append(MenuItem(werecat_action_caption("Backyard"), Call("IntWerecatTalk", "Backyard")))
    python:
        for _yard_object in BackyardRoom.visible_objects():
            current_action_items.append(MenuItem(_yard_object.name, Call("BackyardObjectMenu", _yard_object.object_id)))
        for _yard_exit in BackyardRoom.visible_exits():
            current_action_items.append(MenuItem(_yard_exit.label, Call("AdvanceMovementTime", _yard_exit.target)))
    return


label BackyardObjectMenu(object_id="", refresh_only=False):
    if str(object_id or "") == "backyard_dog_booth":
        call BackyardInspectDogBooth
        return

    $ _yard_object = None
    python:
        for _room_object in BackyardRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _yard_object = _room_object
                break

    if _yard_object is None:
        call BackyardBuildActions
        return

    $ MainTxt = _yard_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _yard_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _yard_action in _yard_object.visible_actions():
            _yard_args = tuple(getattr(_yard_action, "args", ()) or ())
            if _yard_action.hook == "text":
                current_action_items.append(MenuItem(_yard_action.label, Call("BackyardObjectText", object_id, _yard_action.action_id)))
            elif _yard_action.hook == "call" and str(_yard_action.target or "") != "":
                current_action_items.append(MenuItem(_yard_action.label, Call(_yard_action.target, *_yard_args)))
            elif _yard_action.hook == "jump" and str(_yard_action.target or "") != "":
                current_action_items.append(MenuItem(_yard_action.label, Jump(_yard_action.target)))
    $ current_action_items.append(MenuItem("Назад", Call("BackyardRestore")))
    return


label BackyardObjectText(object_id="", action_id=""):
    python:
        _yard_text = ""
        _yard_name = ""
        for _room_object in BackyardRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _yard_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _yard_text = str(_room_action.target or "")
                    break
            break
        if _yard_text:
            MainTxt = _yard_text
            CurLocDesc = _yard_text
            current_action_title = _yard_name or "Действия"
    call BackyardObjectMenu(object_id)
    $ MainTxt = str(_yard_text or MainTxt or "")
    $ CurLocDesc = MainTxt
    $ current_action_title = str(_yard_name or current_action_title or "Действия")
    return


label BackyardToiletExamine:
    if int(BackyardToiletBusy or 0) == 1:
        $ MainTxt = "Дверца нужника заперта изнутри. Похоже, там сейчас занято."
    else:
        $ MainTxt = "Дверца нужника приоткрыта. Сейчас внутри свободно, хотя заходить туда без нужды желания не возникает."
    $ CurLocDesc = MainTxt
    call BackyardObjectMenu("backyard_toilet")
    return


label BackyardWashAtBarrel:
    call Wash("backyard_water_barrel", "Backyard", "Вы умываетесь у бочки с дождевой водой.", "backyard_water_barrel")
    return


label BackyardRestore:
    $ BackyardSavedText = backyard_dynamic_text()
    $ MainTxt = BackyardSavedText
    $ CurLocDesc = MainTxt
    $ scene_image = backyard_dynamic_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    call BackyardBuildActions
    return


label BackyardInspectAshBarrel:
    $ MainTxt = backyard_ash_barrel_description_text() or "Зольной бочки здесь пока нет."
    $ CurLocDesc = MainTxt
    call BackyardObjectMenu("backyard_ash_barrel")
    return


label BackyardInspectDogBooth:
    if backyard_has_dog_booth():
        call IntDogTalk("Backyard")
        return
    else:
        $ MainTxt = "Собачьей будки здесь пока нет."
    $ CurLocDesc = MainTxt
    call BackyardObjectMenu("backyard_dog_booth")
    return
