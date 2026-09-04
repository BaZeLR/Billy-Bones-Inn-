# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_stable_horse_present(_obj=None):
        return player.horse.owns_horse()

    def tavern_stable_no_horse(_obj=None):
        return not player.horse.owns_horse()

    def tavern_stable_can_saddle(_obj=None):
        return player.horse.owns_horse() and not player.horse.saddled

    def tavern_stable_can_unsaddle(_obj=None):
        return player.horse.owns_horse() and player.horse.saddled

    def tavern_stable_can_start_becky_trade(_obj=None):
        hour_now = int(calendar_v2.hour or 0) % 24
        return int(Becky.trade_offer_stage or 0) == 1 and int(calendar_v2.week or 0) != 7 and 6 <= hour_now < 12

    def tavern_stable_can_ride_to_kunidell(_obj=None):
        return tavern_stable_can_start_becky_trade() and player.horse.owns_horse() and int(player.economy.money or 0) >= 200

    def tavern_stable_can_walk_to_kunidell(_obj=None):
        return tavern_stable_can_start_becky_trade() and int(Becky.sherwood_suspicion or 0) >= 5

    def tavern_stable_picture():
        hour_now = int(calendar_v2.hour or 0) % 24
        is_day = 6 <= hour_now < 20
        if player.horse.owns_horse():
            if is_day:
                return "images/tavern/backyard/stables/horse-day.png"
            return "images/tavern/backyard/stables/stablehorse_night.png"
        if is_day:
            return "images/tavern/backyard/stables/stable_empty_day.png"
        return "images/tavern/backyard/stables/stable_empy _night.png"

    TavernStableRoomDefinition = Room(
        code_name="TavernStable",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Конюшня",
        bg_picture="images/tavern/backyard/stables/stable_empty_day.png",
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
        custom_properties={
            "has_horse_character": True,
        },
    )

    def tavern_stable_get_object(object_id):
        object_key = str(object_id or "").strip()
        for room_object in rooms.get("TavernStable").visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    def tavern_stable_action_items():
        items = []
        for room_object in rooms.get("TavernStable").visible_game_items():
            items.append(MenuItem(room_object.name, Call("tavern_stable_object_menu", room_object.object_id)))
        if tavern_stable_can_ride_to_kunidell():
            items.append(MenuItem("Купить провизию для эльфов у Бекки и отправится в Куниделл верхом", Call("TavernStableRideToKunidell")))
        if tavern_stable_can_walk_to_kunidell():
            items.append(MenuItem("Пойти в Куниделл пешком и налегке", Call("TavernStableWalkToKunidell")))
        for room_exit in rooms.get("TavernStable").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target)))
        return items

    def tavern_stable_scene_text():
        desc_parts = []
        rows = rooms.get("TavernStable").visible_descriptions()
        if len(rows) > 0:
            desc_parts.append(str(rows[0].text or ""))

        if player.horse.owns_horse():
            desc_parts.append("Сейчас в конюшне есть только один конь - %s. Хоть и не дикий, но все-таки жеребец." % str(player.horse.name))
            if player.horse.saddled:
                desc_parts.append("Конь уже оседлан и сбруя подогнана.")
            else:
                desc_parts.append("Седло и сбруя висят рядом, коня можно оседлать перед дорогой.")
        else:
            desc_parts.append("Несмотря на название вашего заведения, ни жеребцов, ни кобыл, в конюшне нет. Здесь вообще никого, кроме вас, нет.")

        if Mongol.will_try_to_steal and calendar_v2.is_between_clock(23, 0, 5, 59):
            desc_parts.append("Вдруг со стороны ворот послышалось приглушенное лязгание, как будто кто-то незаметно пытался открыть замок. Вы повернулись на звук, нечаянно задев висящую на столбе на счастье подкову. Та звякнула. Со улицы раздались быстрые удаляющиеся шаги. Вы осторожно выглянули, но никого там не обнаружили. Присмотревшись, вы нашли на мостовой оброненный кусок парусины.\nСтранно, что бы это могло значить?")

        return "\n\n".join([part for part in desc_parts if str(part or "").strip()])

label TavernStable:
    $ renpy.dynamic("_room")
    $ _room = rooms.get("TavernStable")
    $ rooms.enter("TavernStable")
    $ scene_runtime.picture = tavern_stable_picture() or _room.bg_picture or None
    $ Mongol.ensure_story_defaults()
    $ scene_runtime.text = tavern_stable_scene_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ _room.mark_visited()

    if Mongol.will_try_to_steal and calendar_v2.is_between_clock(23, 0, 5, 59):
        $ Mongol.will_try_to_steal = False
    $ main_ui_runtime.action_title = "Конюшня"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_stable_action_items()
    while True:
        call screen main_ui


label tavern_stable_object_menu(object_id=""):
    $ renpy.dynamic("_room_object")
    $ renpy.dynamic("_room_action")
    if str(object_id or "") != "":
        $ main_ui_runtime.object_id = object_id
    $ object_id = main_ui_runtime.object_id
    $ _room_object = tavern_stable_get_object(object_id)
    if _room_object is None:
        $ scene_runtime.text = tavern_stable_scene_text()
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_stable_action_items()
        return

    $ main_ui_runtime.object_id = object_id
    $ scene_runtime.text = str(_room_object.description or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(_room_object.name or "Конюшня")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call("tavern_stable_object_text", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call(_room_action.target)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "picture", tavern_stable_picture() or rooms.get("TavernStable").bg_picture or None),
            SetField(scene_runtime, "text", tavern_stable_scene_text()),
            SetField(scene_runtime, "location_text", tavern_stable_scene_text()),
            SetField(main_ui_runtime, "action_title", "Конюшня"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_stable_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label tavern_stable_object_text(object_id="", action_id=""):
    $ renpy.dynamic("_room_action", "_room_name", "_room_object", "_room_text")
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
            scene_runtime.text = _room_text
            scene_runtime.location_text = _room_text
            main_ui_runtime.action_title = _room_name or "Конюшня"
    call tavern_stable_object_menu(object_id)
    return


label TavernStableHorseExamine:
    if player.horse.saddled:
        $ scene_runtime.text = "Вы подходите к %s и внимательно его осматриваете. Конь выглядит вполне бодрым и уже стоит под седлом." % str(player.horse.name)
    else:
        $ scene_runtime.text = "Вы подходите к %s и внимательно его осматриваете. Конь выглядит вполне бодрым." % str(player.horse.name)
    $ scene_runtime.location_text = scene_runtime.text
    return


label TavernStableSaddleHorse:
    if not player.horse.owns_horse():
        $ scene_runtime.text = tavern_stable_scene_text()
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_stable_action_items()
        return
    $ player.horse.saddled = True
    $ scene_runtime.text = "Вы подтягиваете подпругу, проверяете ремни и оседлываете %s." % player.horse.name
    $ scene_runtime.location_text = scene_runtime.text
    call tavern_stable_object_menu("tack")
    return


label TavernStableUnsaddleHorse:
    if not player.horse.owns_horse():
        $ scene_runtime.text = tavern_stable_scene_text()
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_stable_action_items()
        return
    $ player.horse.saddled = False
    $ scene_runtime.text = "Вы снимаете с %s седло и аккуратно развешиваете сбрую на стене." % player.horse.name
    $ scene_runtime.location_text = scene_runtime.text
    call tavern_stable_object_menu("tack")
    return


label TavernStableRideToKunidell:
    if not tavern_stable_can_ride_to_kunidell():
        $ scene_runtime.text = tavern_stable_scene_text()
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_stable_action_items()
        return
    $ scene_runtime.text = "С утра пораньше вы, 200 мараведи и %s отправились к Бекки. Навьючив мешки с овощами на бедную лошадь, вы отправились в путь." % player.horse.name
    $ scene_runtime.location_text = scene_runtime.text
    $ player.spend_money(200)
    call ShowImageSeq("general", "", "vorota", 2)
    $ rooms.get("BlackwoodRoad").custom_properties["on_horse"] = 1
    jump BlackwoodRoad


label TavernStableWalkToKunidell:
    if not tavern_stable_can_walk_to_kunidell():
        $ scene_runtime.text = tavern_stable_scene_text()
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_stable_action_items()
        return
    "Что-то все это предложение Бекки выглядит подозрительно. Решив все как следует выяснить, вы направились в путь пешком."
    call ShowImageSeq("general", "", "vorota", 2)
    $ rooms.get("BlackwoodRoad").custom_properties["on_horse"] = 0
    jump BlackwoodRoad
