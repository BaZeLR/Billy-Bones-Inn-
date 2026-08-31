# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    AMANDA_ROOM_SLEEP_PICTURES = {
        1: "images/amanda/Room/amanda_sleeps_1.jpg",
        2: "images/amanda/Room/amanda_sleeps_2.png",
        3: "images/amanda/Room/amanda_sleeps_3.png",
        4: "images/amanda/Room/amanda_sleeps_4.png",
        6: "images/amanda/Room/amanda_sleeps_6.png",
        7: "images/amanda/Room/amanda_sleeps_7.png",
        8: "images/amanda/Room/amanda_sleeps_7.png",
        9: "images/amanda/Room/amanda_sleeps_9.png",
        10: "images/amanda/Room/amanda_sleeps_10.png",
        11: "images/amanda/Room/amanda_sleeps_11.png",
    }

    AMANDA_ROOM_BEDROOM_PICTURES = {
        1: "images/amanda/Room/amanda_bedroom_001.jpeg",
        2: "images/amanda/Room/amanda_bedroom_002.jpeg",
        3: "images/amanda/Room/amanda_bedroom_003.jpeg",
        4: "images/amanda/Room/amanda_bedroom_004.jpeg",
        5: "images/amanda/Room/amanda_bedroom_005.jpeg",
    }

    def tavern_amanda_room_sleep_dress():
        sleep_dress = 0
        if not bool(Amanda.sex_stat("virginity", True)):
            if int(Amanda.corruption or 0) >= 30:
                sleep_dress = 1
            if int(Amanda.corruption or 0) >= 50:
                sleep_dress = 2
        return sleep_dress

    def tavern_amanda_room_sleep_scene():
        return (
            not people.is_awake("amanda")
            or (
                str(household_morning_issue_type("amanda") or "") == "sleepy"
                and int(calendar_v2.hour or 0) < 12
            )
        )

    def tavern_amanda_room_picture(sleep_dress=None):
        dress_state = tavern_amanda_room_sleep_dress() if sleep_dress is None else int(sleep_dress or 0)
        corruption_level = npc_corruption_level("amanda")
        horny_state = int(Amanda.arousal_value() or 0) >= 65
        if tavern_amanda_room_sleep_scene():
            if horny_state:
                sleep_picture_number = 9 + max(0, min(2, dress_state))
            elif dress_state >= 2:
                sleep_picture_number = 8 if corruption_level >= 4 else 7
            elif dress_state == 1:
                sleep_picture_number = 6
            else:
                sleep_picture_number = min(4, corruption_level + 1)
            return AMANDA_ROOM_SLEEP_PICTURES[sleep_picture_number]
        if str(people.location("amanda") or "") != "TavernAmandaRoom":
            return "images/amanda/Room/emptyroom.jpg"
        bedroom_picture_number = min(5, corruption_level + 1 + (1 if horny_state else 0))
        return AMANDA_ROOM_BEDROOM_PICTURES[bedroom_picture_number]

    def tavern_amanda_room_wake_picture(sleep_dress=None):
        dress_state = tavern_amanda_room_sleep_dress() if sleep_dress is None else int(sleep_dress or 0)
        if dress_state >= 2:
            return "images/amanda/Room/wakenaked.jpg"
        return "images/amanda/Room/wakedress.jpg"

    def tavern_amanda_room_issue_text():
        issue_code = str(household_morning_issue_type("amanda") or "").strip()
        if int(calendar_v2.hour or 0) >= 12:
            return ""
        if issue_code == "sick":
            return "Аманда с утра расклеилась и так и осталась у себя в комнате. Похоже, ей бы не помешало лечебное зелье."
        if issue_code == "sleepy":
            if household_morning_issue_indecent("amanda"):
                return "Аманда проспала общий подъем и до сих пор валяется в постели, раскрывшись куда сильнее приличного."
            return "Аманда проспала общий подъем и до сих пор спит у себя в комнате."
        if str(people.location("amanda") or "") != "TavernAmandaRoom":
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
        if not Amanda.attic_busted():
            return ""
        if tavern_amanda_room_sleep_scene() or str(people.location("amanda") or "") != "TavernAmandaRoom":
            return ""
        return "Вы входите в комнату Аманды как раз в тот момент, когда она, едва прикрытая одеялом, сидит на кровати слишком близко к окну. Услышав вас, девушка быстро подбирает ткань к груди, пересаживается глубже на постель и демонстративно отворачивается от окна, будто надеется, что это сразу сделает сцену приличнее."

    def tavern_amanda_room_window_scene_text():
        if not Amanda.attic_busted():
            return "Окно выходит прямо на стену соседнего дома. Вид так себе, зато света днем хватает."
        return "Вы осторожно подходите к окну и сразу понимаете, отчего Аманда так поспешно от него отстранилась. Стоит только выбрать угол между рамой и соседней стеной, как взгляд уходит в тот самый соседний двор.\n\n" + attic_neighbor_sex_scene_text() + " Теперь понятно, что именно отсюда она и высматривала ту же самую похабную сцену, что открывалась вам с чердака."

    def tavern_amanda_morning_window_outcome():
        friend_value = int(Amanda.rel or 0)
        open_value = int(Amanda.openness or 0)
        corruption_value = int(Amanda.corruption or 0)
        decision = girl_decide("amanda", "peek_window_confront")
        reaction = str(decision.get("reaction", "") or "")
        decision_score = girl_decision_reaction_score(reaction)
        if Amanda.var_int("suckyou", 0) == 1 or Amanda.var_int("fuckyou", 0) == 1:
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
        room_ref = room_obj if room_obj is not None else rooms.get("TavernAmandaRoom")
        desc_rows = list(room_ref.visible_descriptions() or [])
        issue_text = tavern_amanda_room_issue_text()
        busted_text = tavern_amanda_room_busted_entry_text()
        parts = []

        if len(desc_rows) > 0:
            parts.append(str(desc_rows[0].text or "").strip())

        if tavern_amanda_room_sleep_scene():
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

        if str(people.location("melissa") or "") == "TavernAmandaRoom":
            parts.append("Похоже, Мелисса пока ночует здесь, у Аманды: у стены лежит ее узел с вещами, а по комнате заметно, что место теперь делят две девушки.")
        parts.append(werecat_visible_text("TavernAmandaRoom"))

        parts = [row for row in parts if str(row or "").strip()]
        return "\n\n".join(parts) if len(parts) > 0 else "Комната Аманды."

    TavernAmandaRoomRoomDefinition = Room(
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
        for room_object in rooms.get("TavernAmandaRoom").visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    def tavern_amanda_room_sleeping_now():
        return (
            str(people.location("amanda") or "") == "TavernAmandaRoom"
            and tavern_amanda_room_sleep_scene()
        )

    def tavern_amanda_current_dress_text():
        wardrobe = getattr(Amanda, "wardrobe", {}) if Amanda is not None else {}
        dress_code = ""
        if isinstance(wardrobe, dict):
            dress_code = str(wardrobe.get("current_dress", "") or "").strip()
        if not dress_code:
            return ""
        dress_name = str(ShortDressName.get(dress_code, dress_code) or dress_code).lower()
        dress_desc = str(FullDressDesc.get(dress_code, "") or "").strip()
        if dress_desc:
            return "На ней %s. %s." % (dress_name, dress_desc)
        return "На ней %s." % dress_name

    def tavern_amanda_room_action_items():
        items = []
        if story_event_available("TavernAmandaRoom", "amanda_morning_window"):
            items.append(MenuItem("Поймать Аманду у окна", Call("checkTriggers", "TavernAmandaRoom", "amanda_morning_window", 0)))
        for issue_action in list(household_room_issue_action_specs("amanda") or []):
            items.append(MenuItem(str(issue_action.get("label", "") or ""), Call(str(issue_action.get("target", "") or ""), *tuple(issue_action.get("args", ()) or ()))))
        if tavern_upstairs_can_clean_rooms():
            items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernAmandaRoom", "", "")))
        items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernAmandaRoom")))
        for room_object in rooms.get("TavernAmandaRoom").visible_game_items():
            items.append(MenuItem(room_object.name, Call("tavern_amanda_room_object_menu", room_object.object_id)))
        items.extend(rooms.get("TavernAmandaRoom").build_exit_items())
        return items

label TavernAmandaRoom:
    $ renpy.dynamic("_room", "_amanda_sleep_dress", "_amanda_room_picture")
    $ _room = rooms.get("TavernAmandaRoom")
    $ rooms.enter("TavernAmandaRoom")
    $ _amanda_sleep_dress = tavern_amanda_room_sleep_dress()
    call RoomEnterEventGate(rooms.current_code, False)
    if story_event_available(rooms.current_code, "melissa_bats"):
        call checkTriggers(rooms.current_code, "melissa_bats", 0)
    $ _amanda_room_picture = tavern_amanda_room_picture(_amanda_sleep_dress)
    $ scene_runtime.picture = _amanda_room_picture or ""
    if str(_amanda_room_picture or "").strip():
        vscene _amanda_room_picture
    $ _room.mark_visited()
    if tavern_amanda_room_sleep_scene():
        call dress_for_night("amanda", _amanda_sleep_dress)
    $ scene_runtime.text = tavern_amanda_room_main_text(_room, _amanda_sleep_dress)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Комната Аманды"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_amanda_room_action_items()
    while True:
        call screen main_ui


label TavernAmandaRoomDoor:
    $ rooms.enter("TavernUpstairs")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ scene_runtime.text = "Вы стоите перед дверью комнаты Аманды."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Дверь Аманды"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [
        MenuItem("Постучать", Call("TavernAmandaRoomKnock")),
        MenuItem("Войти в комнату", Call("TavernAmandaRoomEnterWithoutKnock")),
        MenuItem("Уйти", Jump("TavernUpstairs")),
    ]
    return


label TavernAmandaRoomKnock:
    $ renpy.dynamic("_amanda_knock_roll")
    $ main_ui_runtime.action_title = "Дверь Аманды"
    $ main_ui_runtime.action_content = None
    if str(people.location("amanda") or "") != "TavernAmandaRoom":
        $ scene_runtime.text = "Вы постучали в дверь, но ответа не последовало."
        $ main_ui_runtime.action_items = [MenuItem("Попробовать войти", Call("TavernAmandaRoomEnterWithoutKnock")), MenuItem("Уйти", Jump("TavernUpstairs"))]
    else:
        $ _amanda_knock_roll = procedural_randint(1, 100, key="procedural:Inn/TavernAmandaRoom.rpy:procedural_randint:323:1")
        if _amanda_knock_roll <= 50:
            $ scene_runtime.text = "Вы стучите в дверь. Через несколько секунд Аманда отвечает: \"Войдите.\""
            $ main_ui_runtime.action_items = [MenuItem("Войти", movement_actions("TavernAmandaRoom")), MenuItem("Уйти", Jump("TavernUpstairs"))]
        elif _amanda_knock_roll <= 75:
            $ scene_runtime.text = "Вы стучите в дверь. Из комнаты доносится осторожное: \"Кто там?\""
            $ main_ui_runtime.action_items = [MenuItem("Назваться", Call("TavernAmandaRoomKnockAnswer")), MenuItem("Уйти", Jump("TavernUpstairs"))]
        else:
            $ scene_runtime.text = "Вы постучали в дверь, но ответа не последовало."
            $ main_ui_runtime.action_items = [MenuItem("Попробовать войти", Call("TavernAmandaRoomEnterWithoutKnock")), MenuItem("Уйти", Jump("TavernUpstairs"))]
    $ scene_runtime.location_text = scene_runtime.text
    return


label TavernAmandaRoomKnockAnswer:
    $ scene_runtime.text = "Вы называете себя. За дверью слышится короткая возня, потом Аманда отвечает: \"Хорошо, входите.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Дверь Аманды"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [MenuItem("Войти", movement_actions("TavernAmandaRoom")), MenuItem("Уйти", Jump("TavernUpstairs"))]
    return


label TavernAmandaRoomEnterWithoutKnock:
    $ renpy.dynamic("_amanda_dress_text")
    $ apply_movement_time(5, "TavernAmandaRoom")
    if tavern_amanda_room_sleeping_now():
        $ Amanda.rel = max(0, int(Amanda.rel or 0) - 5)
        $ _amanda_dress_text = tavern_amanda_current_dress_text()
        $ scene_runtime.text = "Вы открываете дверь без стука. Аманда сидит на кровати и торопливо пытается прикрыться, на лице у нее тяжелый румянец.\n\n\"Ох... доброе утро, мессир Стефан. В следующий раз вам стоит постучать,\" выдыхает она, явно сбитая с толку."
        if str(_amanda_dress_text or "").strip():
            $ scene_runtime.text = scene_runtime.text + "\n\n" + _amanda_dress_text
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Комната Аманды"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = [MenuItem("Извиниться", Call("TavernAmandaRoomApologizeForEntry")), MenuItem("Выйти", Jump("TavernUpstairs"))]
        call stat
        return
    jump TavernAmandaRoom


label TavernAmandaRoomApologizeForEntry:
    $ scene_runtime.text = "Вы извиняетесь и отступаете к двери, давая Аманде возможность прийти в себя. Она все еще краснеет, но коротко кивает, принимая извинение."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Дверь Аманды"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [MenuItem("Выйти в коридор", Jump("TavernUpstairs"))]
    return


label tavern_amanda_room_object_menu(object_id=""):
    $ renpy.dynamic("_room_object")
    $ renpy.dynamic("_room_action", "_room_args")
    if str(object_id or "") != "":
        $ main_ui_runtime.object_id = object_id
    $ object_id = main_ui_runtime.object_id
    $ _room_object = tavern_amanda_room_get_object(object_id)
    if _room_object is None:
        $ main_ui_runtime.action_items = tavern_amanda_room_action_items()
        return

    $ main_ui_runtime.object_id = object_id
    $ scene_runtime.text = bedroom_door_object_text(_room_object)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(_room_object.name or "Комната Аманды")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call("tavern_amanda_room_object_text", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                _room_args = tuple(getattr(_room_action, "args", ()) or ())
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "text", tavern_amanda_room_main_text(rooms.get("TavernAmandaRoom"), tavern_amanda_room_sleep_dress())),
            SetField(scene_runtime, "location_text", tavern_amanda_room_main_text(rooms.get("TavernAmandaRoom"), tavern_amanda_room_sleep_dress())),
            SetField(main_ui_runtime, "action_title", "Комната Аманды"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_amanda_room_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label tavern_amanda_room_object_text(object_id="", action_id=""):
    $ renpy.dynamic("_room_action", "_room_name", "_room_object", "_room_text")
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
            scene_runtime.text = _room_text
            scene_runtime.location_text = _room_text
            main_ui_runtime.action_title = _room_name or "Комната Аманды"
    call tavern_amanda_room_object_menu(object_id)
    return


label TavernAmandaRoomWindowLook:
    $ scene_runtime.text = tavern_amanda_room_window_scene_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Окно"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [MenuItem("Назад", Call("tavern_amanda_room_object_menu", "window"))]
    return


label story_amanda_room_morning_window_0:
    $ renpy.dynamic("_amanda_window_outcome", "_amanda_sleep_dress", "_amanda_room_picture")
    $ _amanda_window_outcome = tavern_amanda_morning_window_outcome()
    $ calendar_v2.advance_minutes(20)
    $ household_clear_morning_issue("amanda")
    $ scene_runtime.text = "Аманда не спит. Вы застаете ее у окна ровно в тот момент, когда она резко отдергивает руку от занавески и пытается сделать вид, будто просто смотрела во двор.\n\n\"Ну что, Аманда? Кто у нас теперь извращенец?\" спрашиваете вы.\n\nОна вспыхивает, но не уходит от ответа: \"Ничего не могу поделать... иногда так зудит, что хоть на стену лезь.\" Вы спокойно отвечаете: \"Могу помочь, если хочешь.\""
    if _amanda_window_outcome == "oral":
        $ player.intimacy.set_arousal(max(35, int(player.intimacy.arousal_value() or 0)))
        $ Amanda.set_arousal(max(35, Amanda.arousal_value()))
        $ Amanda.change_social(open_delta=1, corruption_delta=2)
        $ scene_runtime.location_text = scene_runtime.text
        call IntAmandaSex("amanda", "home", "minet")
        $ scene_runtime.text = "После этого Аманда уже не спорит насчет окна. Она только быстро приводит себя в порядок и, все еще краснея, просит не разносить эту сцену по всему дому."
    elif _amanda_window_outcome == "mutual":
        $ player.intimacy.set_arousal(max(30, int(player.intimacy.arousal_value() or 0) + 10))
        $ Amanda.add_arousal(10, 100)
        $ Amanda.change_social(friend_delta=1, open_delta=1, corruption_delta=2)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nАманда долго смотрит на вас, потом сама делает шаг ближе. Дальше все остается на грани игры и взаимной смелости: достаточно, чтобы обоим стало трудно делать вид, будто это обычное утро, но недостаточно, чтобы она потом могла назвать это чем-то большим.\n\nЧерез несколько минут она уже торопливо поправляет платье и шепчет, что на сегодня с нее хватит."
    else:
        $ Amanda.change_social(friend_delta=1)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nАманда кусает губу, но все же качает головой. \"Не сейчас. Увидимся позже, если ты умеешь держать язык за зубами.\" На этом она быстро собирается и делает вид, будто вы разбудили ее самым обычным способом."
    if int(Amanda.attic_window_favor_stage or 0) == 0:
        $ Amanda.attic_window_favor_stage = 1
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    $ _amanda_sleep_dress = tavern_amanda_room_sleep_dress()
    $ _amanda_room_picture = tavern_amanda_room_picture(_amanda_sleep_dress)
    $ scene_runtime.picture = _amanda_room_picture or ""
    $ scene_runtime.text = tavern_amanda_room_main_text(rooms.get("TavernAmandaRoom"), _amanda_sleep_dress)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = tavern_amanda_room_action_items()
    return True


label story_amanda_room_grope_0:
    $ renpy.dynamic("tmpSexType", "_amanda_sleep_dress", "_amanda_wake_picture", "_grope_sleep_dress", "tmpGropeReact", "tmpRand")
    $ _grope_sleep_dress = tavern_amanda_room_sleep_dress()
    $ _amanda_sleep_dress = _grope_sleep_dress
    "\nОтбросив сомнения вы подошли к спящей девушке и поцеловали ее прямо в губы."
    if _grope_sleep_dress == 2:
        "Одной рукой вы начали массировать ее обнаженный клитор, а другой ласкать сисечки."
    elif _grope_sleep_dress == 1:
        "Руками же вы начали массировать ее обнаженные сисечки."
    $ _amanda_wake_picture = tavern_amanda_room_wake_picture(_grope_sleep_dress)
    vscene _amanda_wake_picture
    $ tmpGropeReact = Amanda.sex_offer_reaction()
    $ tmpSexType = 0
    if bool(Amanda.sex_stat("virginity", True)):
        if (Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0)) and Amanda.corruption >= 30:
            $ tmpSexType = 1
        if Amanda.corruption >= 38:
            $ tmpSexType = 1
    else:
        if (Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0)) and Amanda.corruption >= 20:
            $ tmpSexType = 2
        if Amanda.corruption >= 30:
            $ tmpSexType = 2
    
    if tmpGropeReact == 1:
        "Проснувшаяся от вашего поцелуя Аманда не казалась через чур уж обескураженной вашим пылом. Тем не менее она все-таки оттолкнула вас, прошептав: 'Стефан, ты что?'"
        python:
            tmpRand = procedural_randint(1, 3, "amanda_room_grope_soft_refusal_1_%s" % int(current_game_day()))
            if tmpRand == 1:
                renpy.say(None, 'За стенкой Сандра и остальные спят, да и я спать хочу, намаялась за день.')
            elif tmpRand == 2:
                renpy.say(None, 'Ты что это такое удумал?')
            else:
                renpy.say(None, 'Нашел время.')
        python:
            tmpRand = procedural_randint(1, 3, "amanda_room_grope_soft_refusal_2_%s" % int(current_game_day()))
            if tmpRand == 1:
                renpy.say(None, 'Давай, иди к себе, водичкой холодной облейся если невтерпеж.')
            elif tmpRand == 2:
                renpy.say(None, 'Не хочу я сейчас ничего, только спать, к себе иди.')
            else:
                renpy.say(None, 'Если совсем невмоготу, то в узел завяжи себе, а меня сейчас не трогай.')
        "<br>Увидев, что Аманда настроена вежливо, но решительно дать вам отпор, вы не стали шуметь и спорить, а вернулись в зал."
        $ Amanda.room_entry_blocked_today = True
        jump TavernMain
    elif tmpGropeReact == 2:
        "Аманда, почувствовав ваши прикосновения, раскрыла глаза. 'Ага, заявился, подонок,' не очень-то романтично огорошила вас своенравная девица
        ."
        call CodeAmandaListScold
        "Вы открыли рот чтобы оправдаться, но такого шанса вам не дали, не став слушать ваших оправданий Аманда твердо и решительно произнесла: 'Вон отсюда, пока я не закричала.'<br>Вы попробовали еще что-то сказать, но в ответ услышали лишь снова 'Вон!'. Почуствовав твердость в голосе девушки, вы решили попробовать сделать свой заход позже, а пока временно отступить в главный зал.<br>"
        $ Amanda.room_entry_blocked_today = True
        if Amanda.rel > 5:
            $ Amanda.change_social(friend_delta=-1)
        if Amanda.corruption > 30:
            $ Amanda.change_social(corruption_delta=-1)
        if Amanda.rel > 5:
            $ Amanda.change_social(friend_delta=-1)
        jump TavernMain
    elif tmpGropeReact == 3:
        
        "Аманда, почувствовав ваши прикосновения, раскрыла глаза. 'Ага, хозяин, явился не запылился,' легко разобралась она в ситуации. Однако последующая ее речь вас не сильно обрадовала: 'Значит днем, на людях, ты меня ругаешь, шлюхой походя обзываешь, учишь духовности и целомудрию. А ночью приперся в мою комнату? И зачем приперся? Стихи читать или цены на базаре обсудить? Что-то мне подсказывает что нет,' решительно обличила ваши грязные помыслы Аманда."
        call CodeAmandaListScold
        "Крыть ее аргументы вам было нечем, но вы все-таки решили попробовать: 'Амандочка, послушай, все совсем не так, на самом деле....'\n'На самом деле что?' и, воспользовавшись тем, что сразу вы не нашлись с ответом, она продолжила: \n-'Нет, это ты меня послушай! Либо ты сейчас берешь свои слова обратно, либо же ты, такой весь из себя правильный, идешь себе восвояси, будем считать что ты приходил проверять не дует ли из окна.'"
        call CodeAmandaSorryChoices
    elif tmpGropeReact == 4:
        
        "Ваш поцелуй ничуть не обескуражил Аманду. Проснувшись и поняв, что это вы, она не замедлила вернуть вам ваш отнюдь не монашеский поцелуй. И не просто вернуть, а вернуть с душой, чувством и языком."
        call CodeAmandaSexStart
    else:
        call CodeAmandaKickFromRoom
    return
