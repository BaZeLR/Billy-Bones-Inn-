# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_amanda_room_sleep_dress():
        sleep_dress = 0
        if int(virginity.get("amanda", 1) or 1) == 0:
            if int(sluttiness.get("amanda", 0) or 0) >= 30:
                sleep_dress = 1
            if int(sluttiness.get("amanda", 0) or 0) >= 50:
                sleep_dress = 2
        return sleep_dress

    def tavern_amanda_room_pick_picture(candidates, fallback=""):
        for candidate in list(candidates or []):
            candidate_ref = str(candidate or "").strip()
            if candidate_ref and renpy.loadable(candidate_ref):
                return candidate_ref
        return str(fallback or "")

    def tavern_amanda_room_picture(sleep_dress=None):
        dress_state = tavern_amanda_room_sleep_dress() if sleep_dress is None else int(sleep_dress or 0)
        room_issue = str(household_morning_issue_type("amanda") or "")
        is_sleep_scene = int(time or 0) >= 4 or (room_issue == "sleepy" and int(hour or 0) < 12)
        if is_sleep_scene:
            if dress_state >= 2:
                return tavern_amanda_room_pick_picture([
                    "images/amanda/Room/amandanaked.jpg",
                    "images/amanda/Room/amanda_sleeps_11.png",
                    "images/amanda/Room/amanda_sleeps_10.png",
                ], "images/amanda/Room/amandanaked.jpg")
            if dress_state == 1:
                return tavern_amanda_room_pick_picture([
                    "images/amanda/Room/amanda_sleeps_10.png",
                    "images/amanda/Room/amanda_sleep_6.png",
                    "images/amanda/Room/amandaInbed_004.jpeg",
                    "images/amanda/Room/amanda_sleeps_9.png",
                ], "images/amanda/Room/amanda_sleeps_10.png")
            return tavern_amanda_room_pick_picture([
                "images/amanda/Room/amanda_sleeps_3.png",
                "images/amanda/Room/amanda_sleeps_4.png",
                "images/amanda/Room/amanda_sleeps_1.jpg",
                "images/amanda/Room/amanda_bedroom_003.jpeg",
            ], "bg amanda_room")
        if str(getLocation("amanda") or "") != "TavernAmandaRoom":
            return tavern_amanda_room_pick_picture([
                "images/amanda/Room/emptyroom.jpg",
            ], "bg amanda_room")
        if amanda_attic_busted():
            return tavern_amanda_room_pick_picture([
                "images/amanda/Room/amanda_sleeps_10.png",
                "images/amanda/Room/amandaInbed_004.jpeg",
                "images/amanda/Room/amanda_sleeps_9.png",
                "images/amanda/Room/amanda_bedroom_003.jpeg",
            ], "bg amanda_room")
        return tavern_amanda_room_pick_picture([
            "images/amanda/Room/amanda_bedroom_003.jpeg",
            "images/amanda/Room/amanda_bedroom_002.jpeg",
            "images/amanda/Room/amanda_bedroom.jpeg",
        ], "bg amanda_room")

    def tavern_amanda_room_issue_text():
        issue_code = str(household_morning_issue_type("amanda") or "").strip()
        if int(time or 0) >= 4:
            return ""
        if issue_code == "sick":
            return "Аманда с утра расклеилась и так и осталась у себя в комнате. Похоже, ей бы не помешало лечебное зелье."
        if issue_code == "sleepy":
            if household_morning_issue_indecent("amanda"):
                return "Аманда проспала общий подъем и до сих пор валяется в постели, раскрывшись куда сильнее приличного."
            return "Аманда проспала общий подъем и до сих пор спит у себя в комнате."
        if str(getLocation("amanda") or "") != "TavernAmandaRoom":
            return "Как вы и ожидали, ее самой там не оказалось."
        return ""

    def tavern_amanda_room_sleep_text(sleep_dress=0):
        dress_state = int(sleep_dress or 0)
        if dress_state >= 2:
            return "Аманда спит голой и, похоже, даже во сне не оставляет себя совсем уж без ласки."
        if dress_state == 1:
            return "Аманда спит в одних панталончиках, и ее маленькая грудь остается совсем открытой."
        return "Аманда спит в длинной ночной рубашке до пят."

    def tavern_amanda_room_busted_entry_text():
        if not amanda_attic_busted():
            return ""
        if int(time or 0) >= 4 or str(getLocation("amanda") or "") != "TavernAmandaRoom":
            return ""
        return "Вы входите в комнату Аманды как раз в тот момент, когда она, едва прикрытая одеялом, сидит на кровати слишком близко к окну. Услышав вас, девушка быстро подбирает ткань к груди, пересаживается глубже на постель и демонстративно отворачивается от окна, будто надеется, что это сразу сделает сцену приличнее."

    def tavern_amanda_room_window_scene_text():
        if not amanda_attic_busted():
            return "Окно выходит прямо на стену соседнего дома. Вид так себе, зато света днем хватает."
        return "Вы осторожно подходите к окну и сразу понимаете, отчего Аманда так поспешно от него отстранилась. Стоит только выбрать угол между рамой и соседней стеной, как взгляд уходит в тот самый соседний двор.\n\n" + attic_neighbor_sex_scene_text() + " Теперь понятно, что именно отсюда она и высматривала ту же самую похабную сцену, что открывалась вам с чердака."

    def tavern_amanda_morning_window_episode_ready():
        return (
            amanda_attic_busted()
            and str(household_morning_issue_type("amanda") or "") == "sleepy"
            and int(time or 0) == 0
            and int(hour or 0) < 12
            and int(AmandaVar.get("attic_window_morning_day", -1) or -1) != int(dayspassed or 0)
        )

    def tavern_amanda_morning_window_outcome():
        friend_value = int(Friends.get("amanda", 0) or 0)
        open_value = int(otkroven.get("amanda", 0) or 0)
        corruption_value = int(sluttiness.get("amanda", 0) or 0)
        decision = girl_decide("amanda", "peek_window_confront")
        reaction = str(decision.get("reaction", "") or "")
        decision_score = girl_decision_reaction_score(reaction)
        if int(AmandaVar.get("suckyou", 0) or 0) == 1 or int(AmandaVar.get("fuckyou", 0) or 0) == 1:
            return "oral" if decision_score >= 0 else "mutual"
        if decision_score > 0:
            if friend_value >= 10 and open_value >= 6 and corruption_value >= 28:
                return "oral"
            return "mutual"
        if decision_score < 0:
            return "later"
        if friend_value >= 12 and open_value >= 8 and corruption_value >= 35:
            return "oral"
        if friend_value >= 8 and open_value >= 5 and corruption_value >= 20:
            return "mutual"
        return "later"

    def tavern_amanda_room_main_text(room_obj=None, sleep_dress=0):
        room_ref = room_obj if room_obj is not None else TavernAmandaRoomRoom
        desc_rows = list(room_ref.visible_descriptions() or [])
        issue_text = tavern_amanda_room_issue_text()
        busted_text = tavern_amanda_room_busted_entry_text()
        parts = []

        if len(desc_rows) > 0:
            parts.append(str(desc_rows[0].text or "").strip())

        if int(time or 0) >= 4:
            parts.append(tavern_amanda_room_sleep_text(sleep_dress))
        elif str(issue_text or "").strip():
            parts.append(str(issue_text or "").strip())
            if len(desc_rows) > 1:
                parts.append(str(desc_rows[1].text or "").strip())
        elif str(busted_text or "").strip():
            parts.append(str(busted_text or "").strip())
            if len(desc_rows) > 1:
                parts.append(str(desc_rows[1].text or "").strip())
        elif len(desc_rows) > 1:
            parts.append(str(desc_rows[1].text or "").strip())

        try:
            melissa_sync_room_problem_state()
        except Exception:
            pass
        if str(getLocation("melissa") or "") == "TavernAmandaRoom":
            parts.append("Похоже, Мелисса пока ночует здесь, у Аманды: у стены лежит ее узел с вещами, а по комнате заметно, что место теперь делят две девушки.")
        parts.append(werecat_visible_text("TavernAmandaRoom"))

        parts = [row for row in parts if str(row or "").strip()]
        return "\n\n".join(parts) if len(parts) > 0 else "Комната Аманды."

    def tavern_amanda_room_locked_for_melissa_booklet():
        try:
            melissa_sync_room_problem_state()
        except Exception:
            pass
        return (
            int(time or 0) >= 4
            and str(MelissaVar.get("temp_room", "") or "") == "TavernAmandaRoom"
            and int(MelissaVar.get("drawings_found", 0) or 0) == 0
            and melissa_bats_stage() >= 6
            and melissa_bats_stage() < 8
        )

    TavernAmandaRoomRoom = Room(
        code_name="TavernAmandaRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Комната Аманды",
        bg_picture="bg amanda_room",
        descriptions=[
            RoomDescription(
                text="Тихо и осторожно вы открыли дверь в комнату Аманды, одну из комнат девушек трактира.",
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
            bedroom_door_object("amanda_room_door_001", "TavernAmandaRoom", "Аманды"),
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
                        hook="call",
                        target="TavernAmandaRoomWindowLook",
                    ),
                ],
            ),
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
    call EnterLocation("TavernAmandaRoom")
    $ _room = TavernAmandaRoomRoom
    $ CurrentRoom = _room
    $ CurLoc = "TavernAmandaRoom"
    $ location = CurLoc
    $ tmpSleepDress = tavern_amanda_room_sleep_dress()
    if tavern_amanda_room_locked_for_melissa_booklet():
        $ _amanda_room_picture = tavern_amanda_room_picture(tmpSleepDress)
        $ scene_image = _amanda_room_picture or None
        if str(_amanda_room_picture or "").strip():
            $ _layout_last_picture = _amanda_room_picture
            call ShowImage("", "", _amanda_room_picture)
        $ MainTxt = "Дверь закрыта изнутри. За ней слышны приглушенные голоса, шорох и короткий смешок."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Комната Аманды"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться в коридор", Call("AdvanceMovementTime", "TavernUpstairs"))]
        $ _amanda_locked_ui_return = None
        while _amanda_locked_ui_return is None:
            call screen main_ui
            $ _amanda_locked_ui_return = _return
        jump TavernAmandaRoom
    call CheckDailyEvent("", "_story_enter", CurLoc, time)
    if story_event_available(CurLoc, "melissa_bats"):
        call checkTriggers(CurLoc, "melissa_bats", 0)
    $ _amanda_room_picture = tavern_amanda_room_picture(tmpSleepDress)
    $ scene_image = _amanda_room_picture or None
    $ _layout_last_picture = _amanda_room_picture or ""
    if str(_amanda_room_picture or "").strip():
        call ShowImage("", "", _amanda_room_picture)
    $ _room.mark_visited()
    if int(time or 0) >= 4:
        call AmandaAtHomeCode
        call DressForNight("amanda", tmpSleepDress)
    $ MainTxt = tavern_amanda_room_main_text(_room, tmpSleepDress)
    $ CurLocDesc = MainTxt
    call TavernAmandaRoomBuildActions
    $ _amanda_room_ui_return = None
    while _amanda_room_ui_return is None:
        call screen main_ui
        $ _amanda_room_ui_return = _return
    jump TavernAmandaRoom


label TavernAmandaRoomBuildActions:
    $ current_action_title = "Комната Аманды"
    $ current_action_content = None
    $ current_action_items = []
    if tavern_amanda_morning_window_episode_ready():
        $ current_action_items.append(MenuItem("Поймать Аманду у окна", Call("TavernAmandaRoomMorningWindowEpisode")))
    python:
        for _issue_action in list(household_room_issue_action_specs("amanda") or []):
            current_action_items.append(MenuItem(str(_issue_action.get("label", "") or ""), Call(str(_issue_action.get("target", "") or ""), *tuple(_issue_action.get("args", ()) or ()))))
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernAmandaRoom", "", "")))
    $ current_action_items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernAmandaRoom", "TavernAmandaRoomBuildActions")))
    if story_event_available("TavernAmandaRoom", "melissa_bats"):
        $ current_action_items.append(MenuItem(melissa_bat_drawings_event_caption(), Call("checkTriggers", "TavernAmandaRoom", "melissa_bats", 0)))
    if werecat_is_in_room("TavernAmandaRoom"):
        $ current_action_items.append(MenuItem(werecat_action_caption("TavernAmandaRoom"), Call("IntWerecatTalk", "TavernAmandaRoom")))
    python:
        for _room_object in TavernAmandaRoomRoom.visible_game_items():
            current_action_items.append(MenuItem(_room_object.name, Call("tavern_amanda_room_object_menu", _room_object.object_id)))
        for _room_exit in TavernAmandaRoomRoom.visible_exits():
            current_action_items.append(MenuItem(_room_exit.label, Call("AdvanceMovementTime", _room_exit.target)))
    return


label tavern_amanda_room_object_menu(object_id="", refresh_only=False):
    if str(object_id or "") != "":
        $ tavern_amanda_room_object_menu_id = object_id
    $ object_id = tavern_amanda_room_object_menu_id
    $ _room_object = tavern_amanda_room_get_object(object_id)
    if _room_object is None:
        call TavernAmandaRoomBuildActions
        return

    $ current_object_id = object_id
    $ MainTxt = bedroom_door_object_text(_room_object)
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


label TavernAmandaRoomWindowLook:
    $ MainTxt = tavern_amanda_room_window_scene_text()
    $ CurLocDesc = MainTxt
    $ current_action_title = "Окно"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Назад", Call("tavern_amanda_room_object_menu", "window"))]
    return


label TavernAmandaRoomMorningWindowEpisode:
    if not tavern_amanda_morning_window_episode_ready():
        call TavernAmandaRoomRestore
        return
    $ AmandaVar["attic_window_morning_day"] = int(dayspassed or 0)
    $ _amanda_window_outcome = tavern_amanda_morning_window_outcome()
    $ calendar_advance_minutes(20)
    $ household_clear_morning_issue("amanda")
    $ CurrentLoc["amanda"] = "TavernAmandaRoom"
    $ MainTxt = "Аманда не спит. Вы застаете ее у окна ровно в тот момент, когда она резко отдергивает руку от занавески и пытается сделать вид, будто просто смотрела во двор.\n\n\"Ну что, Аманда? Кто у нас теперь извращенец?\" спрашиваете вы.\n\nОна вспыхивает, но не уходит от ответа: \"Ничего не могу поделать... иногда так зудит, что хоть на стену лезь.\" Вы спокойно отвечаете: \"Могу помочь, если хочешь.\""
    if _amanda_window_outcome == "oral":
        $ Arousal["You"] = max(35, int(Arousal.get("You", 0) or 0))
        $ Arousal["amanda"] = max(35, int(Arousal.get("amanda", 0) or 0))
        $ sluttiness["amanda"] = min(100, int(sluttiness.get("amanda", 0) or 0) + 2)
        $ otkroven["amanda"] = min(20, int(otkroven.get("amanda", 0) or 0) + 1)
        $ CurLocDesc = MainTxt
        call IntAmandaSex("amanda", "home", "minet")
        $ MainTxt = "После этого Аманда уже не спорит насчет окна. Она только быстро приводит себя в порядок и, все еще краснея, просит не разносить эту сцену по всему дому."
    elif _amanda_window_outcome == "mutual":
        $ Arousal["You"] = max(30, int(Arousal.get("You", 0) or 0) + 10)
        $ Arousal["amanda"] = max(30, int(Arousal.get("amanda", 0) or 0) + 10)
        $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
        $ otkroven["amanda"] = min(20, int(otkroven.get("amanda", 0) or 0) + 1)
        $ sluttiness["amanda"] = min(100, int(sluttiness.get("amanda", 0) or 0) + 2)
        $ MainTxt = str(MainTxt or "") + "\n\nАманда долго смотрит на вас, потом сама делает шаг ближе. Дальше все остается на грани игры и взаимной смелости: достаточно, чтобы обоим стало трудно делать вид, будто это обычное утро, но недостаточно, чтобы она потом могла назвать это чем-то большим.\n\nЧерез несколько минут она уже торопливо поправляет платье и шепчет, что на сегодня с нее хватит."
    else:
        $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
        $ MainTxt = str(MainTxt or "") + "\n\nАманда кусает губу, но все же качает головой. \"Не сейчас. Увидимся позже, если ты умеешь держать язык за зубами.\" На этом она быстро собирается и делает вид, будто вы разбудили ее самым обычным способом."
    $ CurLocDesc = MainTxt
    call stat
    call TavernAmandaRoomRestore
    return


label TavernAmandaRoomRestore:
    $ _amanda_room_picture = tavern_amanda_room_picture(tmpSleepDress if int(time or 0) >= 4 else None)
    $ scene_image = _amanda_room_picture or None
    $ _layout_last_picture = _amanda_room_picture or ""
    $ MainTxt = tavern_amanda_room_main_text(TavernAmandaRoomRoom, tmpSleepDress if int(time or 0) >= 4 else 0)
    $ CurLocDesc = MainTxt
    call TavernAmandaRoomBuildActions
    return


label TavernAmandaRoomGropeAction:
    hide screen main_ui
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
                renpy.say(None, 'За стенкой Сандра и остальные спят, да и я спать хочу, намаялась за день.')
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
        "<br>Увидев, что Аманда настроена вежливо, но решительно дать вам отпор, вы не стали шуметь и спорить, а вернулись в зал."
        $ AmandaVar['kickyoufromroom'] = 1
        jump TavernMain
    elif tmpGropeReact == 2:
        "Аманда, почувствовав ваши прикосновения, раскрыла глаза. 'Ага, заявился, подонок,' не очень-то романтично огорошила вас своенравная девица
        ."
        call CodeAmandaListScold
        "Вы открыли рот чтобы оправдаться, но такого шанса вам не дали, не став слушать ваших оправданий Аманда твердо и решительно произнесла: 'Вон отсюда, пока я не закричала.'<br>Вы попробовали еще что-то сказать, но в ответ услышали лишь снова 'Вон!'. Почуствовав твердость в голосе девушки, вы решили попробовать сделать свой заход позже, а пока временно отступить в главный зал.<br>"
        $ AmandaVar['kickyoufromroom'] = 1
        call SlutFriendsIncrease('amanda', 5, 1, -1, 30, 1, -1)
        call SlutFriendsIncrease('amanda', 5, 1, -1, 0, 0, 0)
        jump TavernMain
    elif tmpGropeReact == 3:
        call CleanScreenOverflow
        "Аманда, почувствовав ваши прикосновения, раскрыла глаза. 'Ага, хозяин, явился не запылился,' легко разобралась она в ситуации. Однако последующая ее речь вас не сильно обрадовала: 'Значит днем, на людях, ты меня ругаешь, шлюхой походя обзываешь, учишь духовности и целомудрию. А ночью приперся в мою комнату? И зачем приперся? Стихи читать или цены на базаре обсудить? Что-то мне подсказывает что нет,' решительно обличила ваши грязные помыслы Аманда."
        call CodeAmandaListScold
        "Крыть ее аргументы вам было нечем, но вы все-таки решили попробовать: 'Амандочка, послушай, все совсем не так, на самом деле....'\n'На самом деле что?' и, воспользовавшись тем, что сразу вы не нашлись с ответом, она продолжила: \n-'Нет, это ты меня послушай! Либо ты сейчас берешь свои слова обратно, либо же ты, такой весь из себя правильный, идешь себе восвояси, будем считать что ты приходил проверять не дует ли из окна.'"
        call CodeAmandaSorryChoices
    elif tmpGropeReact == 4:
        call CleanScreenOverflow
        "Ваш поцелуй ничуть не обескуражил Аманду. Проснувшись и поняв, что это вы, она не замедлила вернуть вам ваш отнюдь не монашеский поцелуй. И не просто вернуть, а вернуть с душой, чувством и языком."
        call CodeAmandaSexStart
    else:
        call CodeAmandaKickFromRoom
    return
