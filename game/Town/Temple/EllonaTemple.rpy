# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
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
                condition=francheska_busy_now,
                priority=150,
            ),
            RoomDescription(
                text="В храме присутствует и ваша знакомая жрица Франческа. Несмотря на свои годы, шустрая старушенция выглядит еще вполне бодро.",
                condition=francheska_known_now,
                priority=140,
            ),
            RoomDescription(
                text="В храме присутствует и старая жрица, может когда она и была красивой, но годы давным давно уже взяли свое. Впрочем старушенция выглядит еще вполне бодро.",
                condition=francheska_unknown_now,
                priority=130,
            ),
            RoomDescription(
                text="До вашего прихода она спала на топчанчике, но услышав что кто-то вошел сразу вскочила, видно сон старушки был чуток, а вы его потревожили.",
                condition=francheska_sleep_note_now,
                priority=120,
            ),
        ],
        exits=[
            RoomExit(label="Зайти в помещение для родов", target="EllonaBirthRoom", condition=francheska_birth_room_available),
            RoomExit(label="Вернуться в порт", target="PortStreets"),
        ],
        game_items=[
            "birth_room_door_001",
        ],
        action_menus=[
            RoomAction(action_id="inspect_cloister", label="Осмотреть дворик-клуатр", hook="call", target="EllonaTempleMenu"),
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="00:00", end="23:59"),
        custom_properties={
            "temple_open_always": True,
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
        ],
        action_menus=[
            RoomAction(action_id="inspect_birth_room", label="Осмотреть убранство родильной комнаты", hook="call", target="EllonaBirthRoomMenu"),
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="00:00", end="23:59"),
        custom_properties={
            "birth_room": True,
        },
    )

label EllonaTemple:
    scene black
    $ CurrentRoom = EllonaTempleRoom
    $ CurLoc = "EllonaTemple"
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ _room = EllonaTempleRoom
    python:
        _room_desc_rows = _room.visible_descriptions()
        _ellona_desc_parts = []
        for _room_desc in _room_desc_rows:
            _ellona_desc_parts.append(str(_room_desc.text or ""))
        CurLocDesc = "\n\n".join([part for part in _ellona_desc_parts if str(part or "").strip()])
        MainTxt = CurLocDesc

    $ _room.mark_visited()

    call RoomEnterEventGate(CurLoc, False)

    if Francheska.busy_now():
        $ scene_image = "images/ellona/afterBirth.png"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ MainTxt = CurLocDesc + "\n\nДверь родильной на миг открывается. Усталая Франческа выходит наружу с тазом испачканных тряпок, не задерживаясь ни на разговоры, ни на объяснения. Затем дверь снова закрывается. Франческа занята, и в родильную сейчас не пройти."
        $ CurLocDesc = MainTxt
    else:
        call ShowImageSeq("ellona", "", "Fran", 4)

    $ current_action_items = CurrentRoom.build_action_items() + CurrentRoom.build_exit_items()
    while True:
        call screen main_ui


label EllonaBirthRoom:
    scene black
    if Francheska.busy_now():
        jump EllonaTemple
    $ CurrentRoom = EllonaBirthRoomRoom
    $ CurLoc = "EllonaBirthRoom"
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ _room = EllonaBirthRoomRoom

    $ CurLocDesc = _room.descriptions[0].text
    $ MainTxt = CurLocDesc
    $ _room.mark_visited()
    if Francheska.visible_now():
        call ShowImageSeq("ellona", "", "Fran", 4)

    $ current_action_items = CurrentRoom.build_action_items() + CurrentRoom.build_exit_items()
    while True:
        call screen main_ui
