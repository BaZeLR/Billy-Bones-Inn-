# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def ellona_fran_busy_now():
        return FranBusy.get(time, 0) == 1

    def ellona_fran_known_now():
        return FranBusy.get(time, 0) == 0 and FranVar.get("meet", 0)

    def ellona_fran_unknown_now():
        return FranBusy.get(time, 0) == 0 and not FranVar.get("meet", 0)

    def ellona_fran_sleep_note_now():
        return FranBusy.get(time, 0) == 0 and (time == 0 or time == 4)

    def ellona_birth_room_available():
        return FranBusy.get(time, 0) == 0

    def ellona_fran_visible():
        return FranBusy.get(time, 0) == 0

    def ellona_fran_sunday_stories_now():
        return int(week or 0) == 7 and int(time or 0) in (1, 2) and ellona_fran_visible()

    def ellona_fran_sunday_stories_text():
        return (
            "Во дворике храма Франческа сегодня не одна. Вокруг нее устроилась ребятня, и старая жрица, размахивая руками, рассказывает им воскресные легенды об Эллоне, Грациях и давних временах.\n\n"
            "\"...и звали их пионеры... А когда вожатые занимались тем, чем велела им Эллона и Грации, они били в барабаны и трубили в горны...\"\n\n"
            "Вы решили не мешать Франческе."
        )

    EllonaTempleRoom = Room(
        code_name="EllonaTemple",
        group_name=ROOM_GROUP_CITY,
        display_name="Храм Эллоны",
        bg_picture="images/ellona/Fran1.jpg",
        descriptions=[
            RoomDescription(
                text="Вы заходите в небольшой храм, посвященный богини любви и плодородия Эллоне. Службы в данном храме, однако, не проводятся, хотя в нем и есть небольшой алтарь. В нем роженицы, с помощью Эллоны и одной из ее жриц, разрешаются от бремени.\nВ центре дворика-клуатра стоит статуя богини, а стены вокруг него расписанны фресками, изображающих пятерых Граций, старших дочерей Эллоны. Напротив входа расположена дверь, ведущая в помещение для родов.",
                priority=200,
            ),
            RoomDescription(
                text="Сейчас она заперта и оттуда доносятся стоны.",
                condition=ellona_fran_busy_now,
                priority=150,
            ),
            RoomDescription(
                text="В храме присутствует и ваша знакомая жрица Франческа. Несмотря на свои годы, шустрая старушенция выглядит еще вполне бодро.",
                condition=ellona_fran_known_now,
                priority=140,
            ),
            RoomDescription(
                text="В храме присутствует и старая жрица, может когда она и была красивой, но годы давным давно уже взяли свое. Впрочем старушенция выглядит еще вполне бодро.",
                condition=ellona_fran_unknown_now,
                priority=130,
            ),
            RoomDescription(
                text="До вашего прихода она спала на топчанчике, но услышав что кто-то вошел сразу вскочила, видно сон старушки был чуток, а вы его потревожили.",
                condition=ellona_fran_sleep_note_now,
                priority=120,
            ),
        ],
        exits=[
            RoomExit(label="Зайти в помещение для родов", target="EllonaBirthRoom", condition=ellona_birth_room_available),
            RoomExit(label="Вернуться в порт", target="PortStreets"),
        ],
        game_items=[
            GameObject(
                object_id="cloister",
                name="Дворик-клуатр",
                description="Небольшой дворик с изваянием Эллоны и фресками на стенах.",
                actions=[
                    ObjectAction(action_id="inspect_cloister", label="Осмотреть дворик-клуатр", hook="call", target="EllonaTempleMenu"),
                ],
            ),
            "birth_room_door_001",
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "temple_open_always": True,
            "object_menu_label": "ellona_room_object_menu",
            "object_menu_args": ("EllonaTemple",),
        },
    )

    EllonaBirthRoomRoom = Room(
        code_name="EllonaBirthRoom",
        display_name="Родильная зала",
        bg_picture="images/ellona/ante2.jpg",
        descriptions=[
            RoomDescription(
                text="Вы заходите в родильную залу. У стены стоит ложе для рожениц, рядом аккуратно сложены чистые полотенца и подготовлены кувшины с водой. На стенах видны фрески и картины, посвященные дочерям Эллоны.",
                priority=200,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться во дворик храма", target="EllonaTemple"),
        ],
        game_items=[
            GameObject(
                object_id="birth_room_decor",
                name="Убранство родильной комнаты",
                description="Ложе, полотенца, кувшины и картины, приготовленные для принятия родов.",
                actions=[
                    ObjectAction(action_id="inspect_birth_room", label="Осмотреть убранство родильной комнаты", hook="call", target="EllonaBirthRoomMenu"),
                ],
            ),
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "birth_room": True,
            "object_menu_label": "ellona_room_object_menu",
            "object_menu_args": ("EllonaBirthRoom",),
        },
    )

    def ellona_get_room_object(room_obj, object_id):
        object_key = str(object_id or "").strip()
        if object_key == "birth_room_door_001":
            return get_game_object(object_key)
        for room_object in room_obj.visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

default ellona_room_object_menu_room_code = "EllonaTemple"
default ellona_room_object_menu_object_id = ""

label EllonaTemple:
    scene black
    call EnterLocation("EllonaTemple")
    $ CurrentRoom = EllonaTempleRoom
    $ CurLoc = "EllonaTemple"
    $ location = CurLoc
    $ CurrentLoc["fran"] = "EllonaTemple"
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ FranVar["meet"] = int(FranVar.get("meet", 0) or 0)
    $ Talked["fran"] = int(Talked.get("fran", 0) or 0)
    $ FranBusy[0] = int(FranBusy.get(0, 0) or 0)
    $ FranBusy[1] = int(FranBusy.get(1, 0) or 0)
    $ FranBusy[2] = int(FranBusy.get(2, 0) or 0)
    $ FranBusy[3] = int(FranBusy.get(3, 0) or 0)
    $ FranBusy[4] = int(FranBusy.get(4, 0) or 0)
    $ _room = EllonaTempleRoom
    python:
        _room_desc_rows = _room.visible_descriptions()
        _ellona_desc_parts = []
        for _room_desc in _room_desc_rows:
            _ellona_desc_parts.append(str(_room_desc.text or ""))
        CurLocDesc = "\n\n".join([part for part in _ellona_desc_parts if str(part or "").strip()])
        MainTxt = CurLocDesc

    $ _room.mark_visited()

    if ellona_fran_sunday_stories_now():
        $ scene_image = "images/ellona/Fran5.png"
        $ _layout_last_picture = scene_image
        call ShowImage("", "", scene_image)
        $ MainTxt = ellona_fran_sunday_stories_text()
        $ CurLocDesc = MainTxt
        $ current_action_title = "Воскресные истории"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Уйти домой", Jump("StreetTavern"))]
        $ _ellona_stories_ui_return = None
        while _ellona_stories_ui_return is None:
            call screen main_ui
            $ _ellona_stories_ui_return = _return
        jump EllonaTemple

    if FranBusy.get(time, 0) != 0:
        $ scene_image = "images/ellona/afterBirth.png"
        $ _layout_last_picture = scene_image
        call ShowImage("", "", scene_image)
        $ MainTxt = CurLocDesc + "\n\nДверь родильной на миг открывается. Усталая Франческа выходит наружу с тазом испачканных тряпок, не задерживаясь ни на разговоры, ни на объяснения. Затем дверь снова закрывается. Франческа занята, и в родильную сейчас не пройти."
        $ CurLocDesc = MainTxt
    else:
        call ShowImageSeq("ellona", "", "Fran", 4)

    call EllonaBuildActions("EllonaTemple")
    $ _ellona_temple_ui_return = None
    while _ellona_temple_ui_return is None:
        call screen main_ui
        $ _ellona_temple_ui_return = _return
    jump EllonaTemple


label EllonaBirthRoom:
    scene black
    if FranBusy.get(time, 0) != 0:
        jump EllonaTemple
    call EnterLocation("EllonaBirthRoom")
    $ CurrentRoom = EllonaBirthRoomRoom
    $ CurLoc = "EllonaBirthRoom"
    $ location = CurLoc
    $ CurrentLoc["fran"] = "EllonaBirthRoom"
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ FranBusy[0] = int(FranBusy.get(0, 0) or 0)
    $ FranBusy[1] = int(FranBusy.get(1, 0) or 0)
    $ FranBusy[2] = int(FranBusy.get(2, 0) or 0)
    $ FranBusy[3] = int(FranBusy.get(3, 0) or 0)
    $ FranBusy[4] = int(FranBusy.get(4, 0) or 0)
    $ _room = EllonaBirthRoomRoom

    $ CurLocDesc = _room.descriptions[0].text
    $ MainTxt = CurLocDesc
    $ _room.mark_visited()
    if FranBusy.get(time, 0) == 0:
        call ShowImageSeq("ellona", "", "Fran", 4)

    call EllonaBuildActions("EllonaBirthRoom")
    $ _ellona_birth_ui_return = None
    while _ellona_birth_ui_return is None:
        call screen main_ui
        $ _ellona_birth_ui_return = _return
    jump EllonaBirthRoom


label EllonaBuildActions(room_code="EllonaTemple"):
    if str(room_code or "") == "EllonaBirthRoom":
        $ _room = EllonaBirthRoomRoom
    else:
        $ _room = EllonaTempleRoom

    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _room_object in _room.visible_game_items():
            current_action_items.append(MenuItem(_room_object.name, Call("ellona_room_object_menu", room_code, _room_object.object_id)))
        for _room_npc in _room.visible_npcs():
            if isinstance(_room_npc, dict):
                _npc_id = str(_room_npc.get("npc_id", "") or "").strip()
                _npc_name = entity_presented_name("npc", _npc_id, _room_npc)
                current_action_items.append(MenuItem(_npc_name, Call("FrancheskaTalk")))
        for _room_exit in _room.visible_exits():
            current_action_items.append(MenuItem(_room_exit.label, Jump(_room_exit.target)))

    return


label ellona_room_object_menu(room_code="", object_id=""):
    if str(room_code or "") != "":
        $ ellona_room_object_menu_room_code = room_code
    if str(object_id or "") != "":
        $ ellona_room_object_menu_object_id = object_id
    $ room_code = str(ellona_room_object_menu_room_code or "EllonaTemple")
    $ object_id = str(ellona_room_object_menu_object_id or "")
    if object_id == "":
        call EllonaBuildActions(room_code)
        return
    if str(room_code or "") == "EllonaBirthRoom":
        $ _room = EllonaBirthRoomRoom
    else:
        $ _room = EllonaTempleRoom
    $ _room_object = ellona_get_room_object(_room, object_id)
    if _room_object is None:
        call EllonaBuildActions(room_code)
        return

    $ MainTxt = _room_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _room_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("EllonaRoomObjectText", room_code, object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and _room_action.target != "":
                _room_args = tuple(getattr(_room_action, "args", ()) or ())
                current_action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and _room_action.target != "":
                current_action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("EllonaBuildActions", room_code)))
    return


label EllonaRoomObjectText(room_code="", object_id="", action_id=""):
    python:
        _room = EllonaBirthRoomRoom if str(room_code or "") == "EllonaBirthRoom" else EllonaTempleRoom
        _object_text = ""
        _object_name = ""
        for _room_object in _room.visible_game_items():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _object_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _object_text = str(_room_action.target or "")
                    break
            break
        if str(object_id or "") == "birth_room_door_001" and str(action_id or "") == "examine_birth_room_door" and FranBusy.get(time, 0) != 0:
            _object_text = "Дверь родильной закрыта. За ней слышны стоны и короткие распоряжения Франчески: жрица занята родами, и внутрь сейчас не пройти."
        if _object_text:
            MainTxt = _object_text
            CurLocDesc = _object_text
            current_action_title = _object_name or "Действия"

    if str(object_id or "") == "birth_room_door_001" and str(action_id or "") == "examine_birth_room_door" and FranBusy.get(time, 0) != 0:
        call ShowImage("", "", "images/ellona/afterBirth.png")

    call ellona_room_object_menu(room_code, object_id)
    return
