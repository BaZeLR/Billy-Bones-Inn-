# PortStreets location - converted from legacy script
default PortStreetsBottleSpawnDay = -1
default PortStreetsBottlePresent = 0

init python:
    import random

    def port_streets_georgett_can_talk():
        return georgett_can_talk == 1

    def port_streets_liza_can_talk():
        return liza_can_talk == 1

    def port_streets_georgett_known():
        return int(Friends.get("georgett", 0) or 0) > 0

    def port_streets_prepare_bottle_spawn():
        current_day = int(dayspassed or 0)
        if int(PortStreetsBottleSpawnDay or -1) == current_day:
            return
        globals()["PortStreetsBottleSpawnDay"] = current_day
        globals()["PortStreetsBottlePresent"] = 1 if random.randint(1, 3) == 1 else 0

    def port_streets_empty_bottle_visible():
        return int(PortStreetsBottlePresent or 0) == 1

    PortStreetsRoom = Room(
        code_name="PortStreets",
        display_name="Портовые переулки",
        bg_picture="images/georgett/Port/port1.jpg",
        descriptions=[
            RoomDescription(
                text="Вы находитесь в лабиринте узких улочек и переулков, ведущих к порту.\nГде-то здесь расположен храм богини Эллоны.",
                priority=200,
            ),
        ],
        exits=[
            RoomExit(label="Идти в храм Эллоны", target="EllonaTemple"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[
            GameObject(
                object_id="port_lanes",
                name="Портовые переулки",
                description="Узкие переулки, ведущие к порту и скрывающие немало темных уголков.",
                actions=[
                    ObjectAction(
                        action_id="examine_port_lanes",
                        label="Осмотреть переулки",
                        hook="text",
                        target="Тесные и запутанные переулки выглядят именно так, как и должно выглядеть место рядом с портом: темновато, шумно и не слишком безопасно.",
                    ),
                ],
            ),
            GameObject(
                object_id="temple_route",
                name="Дорога к храму Эллоны",
                description="Где-то здесь между домами расположен небольшой храм Эллоны.",
                actions=[
                    ObjectAction(
                        action_id="go_temple",
                        label="Идти в храм Эллоны",
                        hook="jump",
                        target="EllonaTemple",
                    ),
                ],
            ),
            GameObject(
                object_id="port_empty_bottle",
                name="Пустая бутылка",
                description="Возле стены валяется пустая бутылка, будто ее недавно бросили мимо груды мусора.",
                actions=[
                    ObjectAction(
                        action_id="take_empty_bottle",
                        label="Подобрать бутылку",
                        hook="call",
                        target="PortStreetsTakeEmptyBottle",
                    ),
                    ObjectAction(
                        action_id="examine_empty_bottle",
                        label="Осмотреть бутылку",
                        hook="text",
                        target="Обычная пустая стеклянная бутылка. Если ее отмыть, она еще вполне пригодится в хозяйстве.",
                    ),
                ],
                condition=port_streets_empty_bottle_visible,
            ),
        ],
        npcs=[
            {"npc_id": "georgett", "name": "Жоржетта", "condition": port_streets_georgett_can_talk, "talk_label": "IntGeorgettTalk", "auto_card": 0, "known_condition": port_streets_georgett_known, "unknown_name": "Молодая женщина", "hide_examine_until_known": True},
            {"npc_id": "liza", "name": "Лизетта", "condition": port_streets_liza_can_talk, "talk_label": "IntLizaTalk", "auto_card": 0},
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6, 7],
            time_slots=[0, 1, 2, 3, 4],
        ),
        custom_properties={
            "street_prostitution_location": True,
        },
    )

label PortStreets:
    scene black
    call EnterLocation("PortStreets")
    $ dog_prepare_current_spawn()
    $ port_streets_prepare_bottle_spawn()
    $ CurrentRoom = PortStreetsRoom
    $ CurLoc = "PortStreets"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ georgett_can_talk = 0
    $ liza_can_talk = 0

    if navigation_only_mode_enabled():
        python:
            _port_nav_parts = [
                PortStreetsRoom.descriptions[0].text,
                navigation_only_message(),
                navigation_only_time_note(),
            ]
            CurLocDesc = "\n\n".join([part for part in _port_nav_parts if str(part or "").strip()])
            MainTxt = CurLocDesc
            current_action_items = []
            for _port_exit in PortStreetsRoom.visible_exits():
                current_action_items.append(MenuItem(_port_exit.label, Jump(_port_exit.target)))
        jump PortStreetsView

    $ GirlNamePS1 = "georgett"
    $ GirlNamePS2 = "liza"
    $ _port_street_clients_target = ""
    $ _port_street_clients_girl = ""

    # Main street logic (TXT-authoritative conditions/visibility)
    if CurrentLoc.get(GirlNamePS1, "") == CurLoc and time == 3 and week != 5 and not (GeorgettVar.get("TalkChurchAfterCermonLiza", 0) != 0 and LizaVar.get("ProstStart", 0) == 0):
        if Friends.get(GirlNamePS1, 0) == 0:
            $ CurLocDesc = "На углу стоит {b}молодая женщина{/b}, не очень высокого роста, чуть пухленькая и с большой налитой грудью, одетая в прозрачную блузку и короткую юбку. Она белокура и кареглаза. Ее внешность и повадки не дают никаких сомнений в том, что она выбрала себе путь отнюдь не монашки."
            if pregnancy.get(GirlNamePS1, 0) >= 210:
                $ CurLocDesc += "\n\nОна беременна и находится на позднем сроке. Ее живот красноречиво об этом свидетельствует."
            if pregnancy.get(GirlNamePS1, 0) < 210 and pregnancy.get(GirlNamePS1, 0) >= 150:
                $ CurLocDesc += "\n\nСредних размеров беременный животик сексуально напоминает о ее бурной личной жизни."
            if pregnancy.get(GirlNamePS1, 0) > 120 and pregnancy.get(GirlNamePS1, 0) < 150:
                $ CurLocDesc += "\n\nВидно что она нагуляла себе животик, но он еще не очень заметен."
            $ MainTxt = CurLocDesc
            call ShowImage("georgett", "port", "wait")
            $ georgett_can_talk = 1
            $ liza_can_talk = 0
        else:
            if time == 3:
                call AddOthersSperm(GirlNamePS1, 6)

            if LizaVar.get("ProstStart", 0):
                if time == 3:
                    call AddOthersSperm(GirlNamePS2, 8)
                $ randvarPS = renpy.random.randint(1, 5)
                if randvarPS == 1 and CheckIfSexEventExist(GirlNamePS1, time) > 0:
                    $ CurLocDesc = "На углу стоит юная Лизетта и ждет клиентов. А вот ее мамаша клиента уже похоже нашла."
                    $ MainTxt = CurLocDesc
                    $ georgett_can_talk = 0
                    $ liza_can_talk = 1
                    $ _port_street_clients_target = "Пойти проверить подворотню"
                    $ _port_street_clients_girl = "georgett"
                elif randvarPS == 2 and CheckIfSexEventExist(GirlNamePS1, time) > 0:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} и ждет клиентов. А вот ее старшую дочку, судя по всему, уже кто-то снял."
                    $ MainTxt = CurLocDesc
                    call ShowImage("georgett", "port", "lizaminet")
                    $ georgett_can_talk = 1
                    $ liza_can_talk = 0
                    $ _port_street_clients_target = "Пойти проверить подворотню"
                    $ _port_street_clients_girl = "liza"
                else:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} со своей дочкой Лизеттой и ждут клиентов."
                    $ MainTxt = CurLocDesc
                    $ georgett_can_talk = 1
                    $ liza_can_talk = 1
            else:
                if renpy.random.randint(1, 3) == 1:
                    $ CurLocDesc = "Почему-то Жоржетты сейчас нет на ее обычном месте. Где же она может быть?"
                    $ MainTxt = CurLocDesc
                    $ georgett_can_talk = 0
                    $ liza_can_talk = 0
                    if HadSex.get(GirlNamePS1, 0) > 0:
                        $ _port_street_clients_target = "Пойти проверить подворотню"
                        $ _port_street_clients_girl = "georgett"
                else:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} и ждет клиентов."
                    $ MainTxt = CurLocDesc
                    call ShowImage("georgett", "port", "wait")
                    $ georgett_can_talk = 1
                    $ liza_can_talk = 0
    else:
        call ShowImageSeq("georgett", "port", "port", 3)
        $ georgett_can_talk = 0
        $ liza_can_talk = 0
        $ CurLocDesc = PortStreetsRoom.descriptions[0].text
        $ MainTxt = CurLocDesc

    if dog_is_here("PortStreets"):
        $ MainTxt += "\n\nВ тени стены крутится бродячий пес, настороженно поглядывающий на прохожих."
        $ CurLocDesc = MainTxt

    call PortStreetsBuildActions
    $ PortStreetsRoom.mark_visited()
    jump PortStreetsView


label PortStreetsView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump PortStreetsView


label PortStreetsBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    if georgett_can_talk:
        if int(Friends.get("georgett", 0) or 0) <= 0:
            $ current_action_items.append(MenuItem("Заговорить с ней", Jump("IntGeorgettTalk")))
        else:
            $ current_action_items.append(MenuItem("Жоржетта", Jump("IntGeorgettTalk")))
    if liza_can_talk:
        $ current_action_items.append(MenuItem("Лизетта", Jump("IntLizaTalk")))
    if dog_is_here("PortStreets"):
        $ current_action_items.append(MenuItem(dog_room_action_caption("PortStreets"), Call("IntDogTalk", "PortStreets")))

    python:
        for _port_object in PortStreetsRoom.visible_objects():
            current_action_items.append(MenuItem(_port_object.name, Call("PortStreetsObjectMenu", _port_object.object_id)))

    if _port_street_clients_target != "" and _port_street_clients_girl != "":
        $ current_action_items.append(MenuItem(_port_street_clients_target, Call("StreetClients", 1, _port_street_clients_girl, time)))

    python:
        for _port_exit in PortStreetsRoom.visible_exits():
            current_action_items.append(MenuItem(_port_exit.label, Jump(_port_exit.target)))

    return


label PortStreetsObjectMenu(object_id=""):
    $ _port_object = None
    python:
        for _room_object in PortStreetsRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _port_object = _room_object
                break

    if _port_object is None:
        call PortStreetsBuildActions
        return

    $ current_action_title = _port_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _port_action in _port_object.visible_actions():
            if _port_action.hook == "text":
                current_action_items.append(MenuItem(_port_action.label, Call("PortStreetsObjectText", object_id, _port_action.action_id)))
            elif _port_action.hook == "call" and str(_port_action.target or "") != "":
                _port_args = tuple(getattr(_port_action, "args", ()) or ())
                current_action_items.append(MenuItem(_port_action.label, Call(_port_action.target, *_port_args)))
            elif _port_action.hook == "jump" and str(_port_action.target or "") != "":
                current_action_items.append(MenuItem(_port_action.label, Jump(_port_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("PortStreetsBuildActions")))
    return


label PortStreetsObjectText(object_id="", action_id=""):
    python:
        _port_text = ""
        for _room_object in PortStreetsRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _port_text = str(_room_action.target or "")
                    break
            break
        if _port_text:
            MainTxt = _port_text
            CurLocDesc = _port_text
    call PortStreetsObjectMenu(object_id)
    return


label PortStreetsTakeEmptyBottle:
    if int(PortStreetsBottlePresent or 0) != 1:
        call PortStreetsBuildActions
        return
    $ PortStreetsBottlePresent = 0
    $ _player_add_item_by_id("empty_bottle_001", 1)
    $ MainTxt = "Вы подбираете пустую бутылку. Стекло цело, и если ее как следует отмыть, она еще пригодится."
    $ CurLocDesc = MainTxt
    call PortStreetsBuildActions
    return
