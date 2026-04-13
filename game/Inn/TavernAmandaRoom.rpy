init python:
    def tavern_amanda_room_picture():
        if household_morning_issue_type("amanda") == "sleepy" and int(hour or 0) < 12:
            return "images/amanda/Room/amanda_sleeps_3.png"
        if int(time or 0) >= 4:
            return "images/amanda/Room/amanda_sleeps_3.png"
        return "bg amanda_room"

    def tavern_amanda_room_amanda_visible():
        if int(time or 0) >= 4:
            return True
        try:
            return _tavern_is_in_room("amanda", "TavernAmandaRoom")
        except Exception:
            return False

    TavernAmandaRoomRoom = Room(
        code_name="TavernAmandaRoom",
        display_name="Комната Аманды",
        bg_picture="bg amanda_room",
        descriptions=[
            RoomDescription(
                text="Тихо и осторожно вы открыли дверь в комнату младшей сестры.",
                priority=200,
            ),
            RoomDescription(
                text="Обстановка у комнаты вполне скромная, кровать и несколько ларей с вещами. Окно выходит на стену соседнего дома.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в коридор", target="TavernUpstairs"),
        ],
        game_items=[
            "bed_002",
            "night_bowl_001",
            GameObject(
                object_id="chests",
                name="Лари с вещами",
                description="Несколько ларей, где Аманда хранит одежду и всякие мелочи.",
                actions=[
                    ObjectAction(
                        action_id="examine_chests",
                        label="Осмотреть лари",
                        hook="text",
                        target="Несколько простых ларей с одеждой и личными вещами Аманды. Рыться в них без спроса было бы уже слишком.",
                    ),
                ],
            ),
            GameObject(
                object_id="window",
                name="Окно",
                description="Небольшое окно, выходящее на стену соседнего дома.",
                actions=[
                    ObjectAction(
                        action_id="examine_window",
                        label="Осмотреть окно",
                        hook="text",
                        target="Окно выходит прямо на стену соседнего дома. Вид так себе, зато света днем хватает.",
                    ),
                ],
            ),
        ],
        npcs=[
            {"npc_id": "amanda", "name": "Аманда", "condition": tavern_amanda_room_amanda_visible, "talk_label": "IntAmandaTalk", "auto_card": True},
        ],
        custom_properties={
            "object_menu_label": "tavern_amanda_room_object_menu",
        },
    )

    def tavern_amanda_room_get_object(object_id):
        object_key = str(object_id or "").strip()
        if object_key == "bed_002":
            return get_game_object(object_key)
        for room_object in TavernAmandaRoomRoom.visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

label TavernAmandaRoom:
    hide screen main_ui
    scene black
    call EnterLocation("TavernAmandaRoom")
    $ _room = TavernAmandaRoomRoom
    $ CurrentRoom = _room
    $ CurrentRoom.npcs = TavernAmandaRoomRoom.npcs
    $ CurLoc = "TavernAmandaRoom"
    $ location = CurLoc
    $ scene_image = tavern_amanda_room_picture() or _room.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
        if str(scene_image).startswith("bg "):
            show expression scene_image at master
    $ _room_desc_rows = _room.visible_descriptions()
    if len(_room_desc_rows) > 0:
        "[_room_desc_rows[0].text]"
    if time < 4 and household_morning_issue_type("amanda") == "":
        "Как вы и ожидали, ее самой там не оказалось."
    if len(_room_desc_rows) > 1:
        "[_room_desc_rows[1].text]"
    if household_morning_issue_type("amanda") == "sick":
        "Похоже, Аманда сегодня расклеилась и осталась в комнате. По ее виду ясно, что без лечебного зелья ей быстро не подняться."
    elif household_morning_issue_type("amanda") == "sleepy" and time < 4:
        if household_morning_issue_indecent("amanda"):
            "Аманда до сих пор сладко спит у себя в кровати, совсем не чувствуя, что уже давно пора вставать. Во сне она раскрылась куда сильнее приличного и теперь выглядит куда менее невинно, чем сама хотела бы казаться днем."
        else:
            "Аманда до сих пор спит у себя в кровати, завернувшись в одеяло и явно проспав общий подъем."
    $ _room.mark_visited()

    if time >= 4:
        call AmandaAtHomeCode
        $ tmpSleepDress = 0
        if virginity['amanda'] == 0:
            if sluttiness['amanda'] >= 30:
                $ tmpSleepDress = 1
            if sluttiness['amanda'] >= 50:
                $ tmpSleepDress = 2
        python:
            import random
            if random.randint(1,3) <= 2:
                renpy.say(None, "Аманда сладко спит у себя в кровати под покрывалом. Пока вы смотрели, сестренка повернулась во сне, частично раскрывшись.")
            else:
                renpy.say(None, "Аманда сладко спит у себя в кровати, скинув во сне покрывало.")
        if tmpSleepDress == 2:
            "Оба-на! Ваше сестренка, оказывается, предпочитает спать голенькой. И во сне теребить себя там, внизу, видно сон уж очень приятный."
            call ShowImage("amanda", "room", "amandanaked")
        elif tmpSleepDress == 1:
            "Вы увидели, что спит она в одних панталончиках, ее маленькие острые грудки задорно обнаженны."
        else:
            "Вы увидели, что она одета в длинную ночную рубашку до пят."
        call DressForNight("amanda", tmpSleepDress)
    else:
        call ShowImage("amanda", "room", "emptyroom")
    if time >= 4:
        if tmpSleepDress == 2:
            $ MainTxt = "Оба-на! Ваше сестренка, оказывается, предпочитает спать голенькой. И во сне теребить себя там, внизу, видно сон уж очень приятный."
        elif tmpSleepDress == 1:
            $ MainTxt = "Вы увидели, что спит она в одних панталончиках, ее маленькие острые грудки задорно обнаженны."
        else:
            $ MainTxt = "Вы увидели, что она одета в длинную ночную рубашку до пят."
    elif household_morning_issue_type("amanda") == "sleepy":
        if household_morning_issue_indecent("amanda"):
            $ MainTxt = "Аманда проспала общий подъем и до сих пор валяется в постели, раскрывшись куда сильнее приличного."
        else:
            $ MainTxt = "Аманда проспала общий подъем и до сих пор спит у себя в комнате."
    elif household_morning_issue_type("amanda") == "sick":
        $ MainTxt = "Аманда с утра расклеилась и так и осталась у себя в комнате. Похоже, ей бы не помешало лечебное зелье."
    elif len(_room_desc_rows) > 1:
        $ MainTxt = _room_desc_rows[1].text
    elif len(_room_desc_rows) > 0:
        $ MainTxt = _room_desc_rows[0].text
    else:
        $ MainTxt = "Комната Аманды."
    $ CurLocDesc = MainTxt
    call TavernAmandaRoomBuildActions
    jump TavernAmandaRoomView


label TavernAmandaRoomBuildActions:
    $ current_action_title = "Комната Аманды"
    $ current_action_content = None
    $ current_action_items = []
    if household_morning_issue_type("amanda") == "sick" and int(_player_item_count_by_id("healing_potion_001") or 0) > 0:
        $ current_action_items.append(MenuItem("Принести Аманде лечебное зелье", Call("HouseholdMorningIssueCure", "amanda")))
    elif household_morning_issue_type("amanda") == "sleepy":
        $ current_action_items.append(MenuItem("Разбудить Аманду", Call("HouseholdWakeSleepyGirl", "amanda")))
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernAmandaRoom", "", "")))
    $ current_action_items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernAmandaRoom", "TavernAmandaRoomBuildActions")))
    python:
        for _room_object in TavernAmandaRoomRoom.visible_game_items():
            current_action_items.append(MenuItem(_room_object.name, Call("tavern_amanda_room_object_menu", _room_object.object_id)))
        for _room_exit in TavernAmandaRoomRoom.visible_exits():
            current_action_items.append(MenuItem(_room_exit.label, Call("AdvanceMovementTime", _room_exit.target)))
    return


label TavernAmandaRoomView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernAmandaRoomView


label tavern_amanda_room_object_menu(object_id=""):
    if str(object_id or "") != "":
        $ tavern_amanda_room_object_menu_id = object_id
    $ object_id = tavern_amanda_room_object_menu_id
    $ _room_object = tavern_amanda_room_get_object(object_id)
    if _room_object is None:
        call TavernAmandaRoomBuildActions
        return

    $ current_object_id = object_id
    $ MainTxt = str(_room_object.description or "")
    $ CurLocDesc = MainTxt
    $ current_action_title = str(_room_object.name or "Комната Аманды")
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("tavern_amanda_room_object_text", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                _room_args = tuple(getattr(_room_action, "args", ()) or ())
                current_action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        current_action_items.append(MenuItem("Назад", Call("TavernAmandaRoomRestore")))
    return


label tavern_amanda_room_object_text(object_id="", action_id=""):
    python:
        _room_text = ""
        _room_name = ""
        _room_object = tavern_amanda_room_get_object(object_id)
        if _room_object is not None:
            _room_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _room_text = str(_room_action.target or "")
                    break
        if _room_text:
            MainTxt = _room_text
            CurLocDesc = _room_text
            current_action_title = _room_name or "Комната Аманды"
    call tavern_amanda_room_object_menu(object_id)
    return


label TavernAmandaRoomRestore:
    $ _room_desc_rows = TavernAmandaRoomRoom.visible_descriptions()
    if len(_room_desc_rows) > 1 and time < 4:
        $ MainTxt = _room_desc_rows[1].text
    elif len(_room_desc_rows) > 0:
        $ MainTxt = _room_desc_rows[0].text
    else:
        $ MainTxt = "Комната Аманды."
    $ CurLocDesc = MainTxt
    call TavernAmandaRoomBuildActions
    return


label TavernAmandaRoomGropeAction:
    "\nОтбросив сомнения вы подошли к спящей девушке и поцеловали ее прямо в губы."
    if tmpSleepDress == 2:
        "Одной рукой вы начали массировать ее обнаженный клитор, а другой ласкать сисечки."
    elif tmpSleepDress == 1:
        "Руками же вы начали массировать ее обнаженные сисечки."
    if tmpSleepDress >= 2:
        call ShowImage("amanda", "room", "wakenaked")
    else:
        call ShowImage("amanda", "room", "wakedress")
    $ tmpGropeReact = AmandaSexOfferReaction()
    $ tmpSexType = 0
    if virginity['amanda']:
        if (AmandaVar['suckyou'] or AmandaVar['fuckyou']) and sluttiness['amanda'] >= 30:
            $ tmpSexType = 1
        if sluttiness['amanda'] >= 38:
            $ tmpSexType = 1
    else:
        if (AmandaVar['suckyou'] or AmandaVar['fuckyou']) and sluttiness['amanda'] >= 20:
            $ tmpSexType = 2
        if sluttiness['amanda'] >= 30:
            $ tmpSexType = 2
    call AddCleanScreen
    if tmpGropeReact == 1:
        "Проснувшаяся от вашего поцелуя Аманда не казалась через чур уж обескураженной вашим пылом. Тем не менее она все-таки оттолкнула вас, прошептав: 'Стефан, ты что?'"
        python:
            tmpRand = random.randint(1,3)
            if tmpRand == 1:
                renpy.say(None, 'За стенкой мама, сестра спят, да и я спать хочу, намаялась за день.')
            elif tmpRand == 2:
                renpy.say(None, 'Ты что это такое удумал?')
            else:
                renpy.say(None, 'Нашел время.')
        python:
            tmpRand = random.randint(1,3)
            if tmpRand == 1:
                renpy.say(None, 'Давай, иди к себе, водичкой холодной облейся если невтерпеж.')
            elif tmpRand == 2:
                renpy.say(None, 'Не хочу я сейчас ничего, только спать, к себе иди.')
            else:
                renpy.say(None, 'Если совсем невмоготу, то в узел завяжи себе, а меня сейчас не трогай.')
        "<br>Увидев, что сестра настроена вежливо, но решительно дать вам отпор, вы не стали шуметь и спорить, а вернулись в зал."
        $ AmandaVar['kickyoufromroom'] = 1
        jump TavernMain
    elif tmpGropeReact == 2:
        "Аманда, почувствовав ваши прикосновения, раскрыла глаза. 'Ага, заявился, подонок,' не очень-то романтично огорошила вас сестренка."
        call CodeAmandaListScold
        "<br>Вы открыли рот чтобы оправдаться, но такого шанса вам не дали, не став слушать ваших оправданий Аманда твердо и решительно произнесла: 'Вон отсюда, пока я не закричала.'<br>Вы попробовали еще что-то сказать, но в ответ услышали лишь снова 'Вон!'. Почуствовав твердость в голосе девушки, вы решили попробовать сделать свой заход позже, а пока временно отступить в главный зал.<br>"
        $ AmandaVar['kickyoufromroom'] = 1
        call SlutFriendsIncrease('amanda', 5, 1, -1, 30, 1, -1)
        call SlutFriendsIncrease('amanda', 5, 1, -1, 0, 0, 0)
        jump TavernMain
    elif tmpGropeReact == 3:
        call CleanScreenOverflow
        "Аманда, почувствовав ваши прикосновения, раскрыла глаза. 'Ага, братик, явился не запылился,' легко разобралась она в ситуации. Однако последующая ее речь вас не сильно обрадовала: 'Значит днем, на людях, ты меня ругаешь, шлюхой походя обзываешь, учишь духовности и целомудрию. А ночью приперся в мою комнату? И зачем приперся? Стихи читать или цены на базаре обсудить? Что-то мне подсказывает что нет,' решительно обличила ваши грязные помыслы Аманда."
        call CodeAmandaListScold
        "<br>Крыть ее аргументы вам было нечем, но вы все-таки решили попробовать: 'Амандочка, послушай, все совсем не так, на самом деле....'\n'На самом деле что?' и, воспользовавшись тем, что сразу вы не нашлись с ответом, она продолжила: <br>'Нет, это ты меня послушай! Либо ты сейчас берешь свои слова обратно, либо же ты, такой весь из себя правильный, идешь себе восвояси, будем считать что ты приходил проверять не дует ли из окна.'"
        call CodeAmandaSorryChoices
    elif tmpGropeReact == 4:
        call CleanScreenOverflow
        "Ваш поцелуй ничуть не обескуражил Аманду. Проснувшись и поняв что это вы, она не замедлила вернуть вам ваш отнюдь не братский поцелуй. И не просто вернуть, а вернуть с душой, чувством и языком."
        call CodeAmandaSexStart
    else:
        call CodeAmandaKickFromRoom
    return
