default HorseSaddled = 0
default HorsePurchasePrice = 0

init python:
    def tavern_stable_horse_present(_obj=None):
        return MyStallion != ""

    def tavern_stable_no_horse(_obj=None):
        return MyStallion == ""

    def tavern_stable_can_saddle(_obj=None):
        return MyStallion != "" and int(HorseSaddled or 0) == 0

    def tavern_stable_can_unsaddle(_obj=None):
        return MyStallion != "" and int(HorseSaddled or 0) == 1

    def tavern_stable_can_start_becky_trade(_obj=None):
        return int(BeckyVar.get('TradeOffer', 0) or 0) == 1 and int(time or 0) == 0 and int(week or 0) != 7

    def tavern_stable_can_ride_to_kunidell(_obj=None):
        return tavern_stable_can_start_becky_trade() and MyStallion != "" and int(money or 0) >= 200

    def tavern_stable_can_walk_to_kunidell(_obj=None):
        return tavern_stable_can_start_becky_trade() and int(BeckyVar.get('SherwoodSuspect', 0) or 0) >= 5

    TavernStableRoom = Room(
        code_name="TavernStable",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Конюшня",
        bg_picture="bg stable",
        descriptions=[
            RoomDescription(
                text="Вы находитесь в конюшне, пристроенной к вашему трактиру. С обеих сторон от выхода на улицу располагаются денники для лошадей, по три с каждой стороны. За ними стоит большая кадка с водой и расположены вешалки для конской сбруи. Сверху, почти на всем протяжении конюшни, тянется навес для хранения сена. В углу стоит лестница.\n\nЭту конюшню выстроил прежний владелец трактира - большой оптимист. В его мечтах в трактир валом валили богатые и знатные господа: дворяне и купцы. Приезжать они конечно, должны были верхом. Реальность же оказалась куда прозаичней - контингент завсегдатаев 'Дикого Жеребца' состоял из людей попроще и являлся на пьянку пешком. За все время, что вы были владельцем этого заведения, хоть бы один человек приехал бы сюда на лошади!",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Идти обратно в главный зал", target="TavernMain"),
            RoomExit(label="Выйти на задний двор", target="Backyard"),
        ],
        game_items=[
            GameObject(
                object_id="horse",
                name="Конь",
                description="Ваш жеребец, если он сейчас стоит в конюшне.",
                actions=[
                    ObjectAction(
                        action_id="examine_horse",
                        label="Осмотреть коня",
                        hook="call",
                        target="TavernStableHorseExamine",
                        condition=tavern_stable_horse_present,
                    ),
                ],
                condition=tavern_stable_horse_present,
            ),
            GameObject(
                object_id="empty_stalls",
                name="Пустые денники",
                description="Большая часть денников пустует.",
                actions=[
                    ObjectAction(
                        action_id="examine_empty_stalls",
                        label="Осмотреть денники",
                        hook="text",
                        target="Пустые денники лишь подчеркивают, насколько редко сюда вообще кто-то заезжает верхом.",
                    ),
                ],
                condition=tavern_stable_no_horse,
            ),
            GameObject(
                object_id="tack",
                name="Конская сбруя",
                description="На стенах висят ремни, уздечки и прочая сбруя.",
                actions=[
                    ObjectAction(
                        action_id="examine_tack",
                        label="Осмотреть сбрую",
                        hook="text",
                        target="Старые, но еще годные ремни и прочая конская сбруя, оставшаяся в хозяйстве трактира.",
                    ),
                    ObjectAction(
                        action_id="saddle_horse",
                        label="Оседлать коня",
                        hook="call",
                        target="TavernStableSaddleHorse",
                        condition=tavern_stable_can_saddle,
                    ),
                    ObjectAction(
                        action_id="unsaddle_horse",
                        label="Снять седло",
                        hook="call",
                        target="TavernStableUnsaddleHorse",
                        condition=tavern_stable_can_unsaddle,
                    ),
                ],
            ),
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "has_horse_character": True,
        },
    )

    def tavern_stable_get_object(object_id):
        object_key = str(object_id or "").strip()
        for room_object in TavernStableRoom.visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    def tavern_stable_scene_text():
        desc_parts = []
        rows = TavernStableRoom.visible_descriptions()
        if len(rows) > 0:
            desc_parts.append(str(rows[0].text or ""))

        if MyStallion != "":
            desc_parts.append("Сейчас в конюшне есть только один конь - %s. Хоть и не дикий, но все-таки жеребец." % str(MyStallion))
            if int(HorseSaddled or 0) == 1:
                desc_parts.append("Конь уже оседлан и сбруя подогнана.")
            else:
                desc_parts.append("Седло и сбруя висят рядом, коня можно оседлать перед дорогой.")
        else:
            desc_parts.append("Несмотря на название вашего заведения, ни жеребцов, ни кобыл, в конюшне нет. Здесь вообще никого, кроме вас, нет.")

        if int(MongolVar.get('WillTryToSteal', 0) or 0) and int(time or 0) == 4:
            desc_parts.append("Вдруг со стороны ворот послышалось приглушенное лязгание, как будто кто-то незаметно пытался открыть замок. Вы повернулись на звук, нечаянно задев висящую на столбе на счастье подкову. Та звякнула. Со улицы раздались быстрые удаляющиеся шаги. Вы осторожно выглянули, но никого там не обнаружили. Присмотревшись, вы нашли на мостовой оброненный кусок парусины.\nСтранно, что бы это могло значить?")

        return "\n\n".join([part for part in desc_parts if str(part or "").strip()])

label TavernStable:
    call EnterLocation("TavernStable")
    $ _room = TavernStableRoom
    $ CurrentRoom = _room
    $ CurLoc = "TavernStable"
    $ location = CurLoc
    $ scene_image = _room.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MongolVar['WillTryToSteal'] = int(MongolVar.get('WillTryToSteal', 0) or 0)
    $ BeckyVar['TradeOffer'] = int(BeckyVar.get('TradeOffer', 0) or 0)
    $ BeckyVar['SherwoodSuspect'] = int(BeckyVar.get('SherwoodSuspect', 0) or 0)
    if MyStallion != "":
        call ShowImage("", "", "images/tavern/backyard/stables/stablehorse.jpg")
    else:
        call ShowImage("", "", "images/tavern/backyard/stables/stableempty.jpg")
    $ MainTxt = tavern_stable_scene_text()
    $ CurLocDesc = MainTxt
    $ _room.mark_visited()

    if MongolVar.get('WillTryToSteal', 0) and time == 4:
        $ MongolVar['WillTryToSteal'] = 0
    call TavernStableBuildActions
    jump TavernStableView


label TavernStableBuildActions:
    $ current_action_title = "Конюшня"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _room_object in TavernStableRoom.visible_game_items():
            current_action_items.append(MenuItem(_room_object.name, Call("tavern_stable_object_menu", _room_object.object_id)))
        if tavern_stable_can_ride_to_kunidell():
            current_action_items.append(MenuItem("Купить провизию для эльфов у Бекки и отправится в Куниделл верхом", Call("TavernStableRideToKunidell")))
        if tavern_stable_can_walk_to_kunidell():
            current_action_items.append(MenuItem("Пойти в Куниделл пешком и налегке", Call("TavernStableWalkToKunidell")))
        for _room_exit in TavernStableRoom.visible_exits():
            current_action_items.append(MenuItem(_room_exit.label, Call("AdvanceMovementTime", _room_exit.target)))
    return


label TavernStableView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernStableView


label tavern_stable_object_menu(object_id=""):
    if str(object_id or "") != "":
        $ tavern_stable_object_menu_id = object_id
    $ object_id = tavern_stable_object_menu_id
    $ _room_object = tavern_stable_get_object(object_id)
    if _room_object is None:
        call TavernStableRestore
        return

    $ current_object_id = object_id
    $ MainTxt = str(_room_object.description or "")
    $ CurLocDesc = MainTxt
    $ current_action_title = str(_room_object.name or "Конюшня")
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("tavern_stable_object_text", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Call(_room_action.target)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        current_action_items.append(MenuItem("Назад", Call("TavernStableRestore")))
    return


label tavern_stable_object_text(object_id="", action_id=""):
    python:
        _room_text = ""
        _room_name = ""
        _room_object = tavern_stable_get_object(object_id)
        if _room_object is not None:
            _room_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _room_text = str(_room_action.target or "")
                    break
        if _room_text:
            MainTxt = _room_text
            CurLocDesc = _room_text
            current_action_title = _room_name or "Конюшня"
    call tavern_stable_object_menu(object_id)
    return


label TavernStableRestore:
    $ MainTxt = tavern_stable_scene_text()
    $ CurLocDesc = MainTxt
    call TavernStableBuildActions
    return


label TavernStableHorseExamine:
    if int(HorseSaddled or 0) == 1:
        $ MainTxt = "Вы подходите к %s и внимательно его осматриваете. Конь выглядит вполне бодрым и уже стоит под седлом." % str(MyStallion)
    else:
        $ MainTxt = "Вы подходите к %s и внимательно его осматриваете. Конь выглядит вполне бодрым." % str(MyStallion)
    $ CurLocDesc = MainTxt
    return


label TavernStableSaddleHorse:
    if MyStallion == "":
        call TavernStableRestore
        return
    $ HorseSaddled = 1
    $ MainTxt = "Вы подтягиваете подпругу, проверяете ремни и оседлываете [MyStallion]."
    $ CurLocDesc = MainTxt
    call tavern_stable_object_menu("tack")
    return


label TavernStableUnsaddleHorse:
    if MyStallion == "":
        call TavernStableRestore
        return
    $ HorseSaddled = 0
    $ MainTxt = "Вы снимаете с [MyStallion] седло и аккуратно развешиваете сбрую на стене."
    $ CurLocDesc = MainTxt
    call tavern_stable_object_menu("tack")
    return


label TavernStableRideToKunidell:
    if not tavern_stable_can_ride_to_kunidell():
        call TavernStableRestore
        return
    "С утра пораньше вы, 200 мараведи и [MyStallion] отправились к Бекки. Навьючив мешки с овощами на бедную лошадь, вы отправились в путь."
    $ money -= 200
    call ShowImageSeq("general", "", "vorota", 2)
    call SherwoodTravel(1)
    return


label TavernStableWalkToKunidell:
    if not tavern_stable_can_walk_to_kunidell():
        call TavernStableRestore
        return
    "Что-то все это предложение Бекки выглядит подозрительно. Решив все как следует выяснить, вы направились в путь пешком."
    call ShowImageSeq("general", "", "vorota", 2)
    call SherwoodTravel(0)
    return
