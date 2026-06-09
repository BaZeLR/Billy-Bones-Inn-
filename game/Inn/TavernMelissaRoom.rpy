# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_melissa_room_clara_scene_paths():
        return [
            picture_path
            for picture_path in (
                "images/clara/melissa Pillow fight.png",
                "images/clara/melissa_doodleTimes.png",
                "images/clara/melissa_doodles.png",
            )
            if renpy.loadable(picture_path)
        ]

    def tavern_melissa_room_clara_visit_active():
        return str(getLocation("clara") or "") == "TavernMelissaRoom" and Melissa.bats_stage() >= 8

    def tavern_melissa_room_locked_from_inside():
        if not tavern_melissa_room_clara_visit_active():
            return False
        try:
            if story_event_available("TavernMelissaRoom", "clara_paintings"):
                return False
        except Exception:
            pass
        return True

    def tavern_melissa_room_register_clara_visit():
        if not tavern_melissa_room_clara_visit_active():
            return
        if int(ClaraVar.get("tavern_melissa_visit_day", -1) or -1) == int(dayspassed or 0):
            return
        ClaraVar["tavern_melissa_visit_day"] = int(dayspassed or 0)
        ClaraVar["tavern_melissa_visit_count"] = int(ClaraVar.get("tavern_melissa_visit_count", 0) or 0) + 1

    def tavern_melissa_room_clara_visit_index():
        scene_count = len(tavern_melissa_room_clara_scene_paths())
        if scene_count <= 0:
            return 0
        visit_count = max(1, int(ClaraVar.get("tavern_melissa_visit_count", 0) or 0))
        return (visit_count - 1) % scene_count

    def tavern_melissa_room_clara_visit_picture():
        scene_paths = tavern_melissa_room_clara_scene_paths()
        if len(scene_paths) <= 0:
            return ""
        return scene_paths[tavern_melissa_room_clara_visit_index()]

    def tavern_melissa_room_clara_visit_text():
        scene_index = tavern_melissa_room_clara_visit_index()
        if scene_index == 0:
            return "Вы заглядываете в комнату и тут же понимаете, что пришли не вовремя: Кларисса с Мелиссой уже устроили на кровати полушутливую драку подушками, а по полу летят перья и обрывки смеха. Обе резко замирают, увидев вас в дверях, и Мелисса первой просит вас не торчать у порога."
        if scene_index == 1:
            return "Сегодня девушки сидят совсем близко друг к другу на кровати и, склонившись над коленями, возятся с листками и угольком. Кларисса что-то быстро дорисовывает, а Мелисса смеется шепотом и тут же прикрывает рисунки ладонью, заметив вас."
        return "Кларисса с Мелиссой так увлечены своими непристойными каракулями и перешептыванием, что сперва даже не сразу замечают вас. Когда же замечают, обе смотрят одинаково красноречиво: вам здесь сейчас делать нечего."

    def tavern_melissa_room_sleep_picture():
        picture_cycle = [
            "images/melissa/tavern/melissa_sleeps_0.jpg",
            "images/melissa/tavern/melissa_sleeps_1.png",
            "images/melissa/tavern/melissa_sleeps_2.png",
            "images/melissa/tavern/melissa_sleeps_3.png",
            "images/melissa/tavern/melissa_sleeps_4.png",
            "images/melissa/tavern/melissa_sleeps.png",
        ]
        picture_cycle = [row for row in picture_cycle if renpy.loadable(row)]
        if len(picture_cycle) > 0:
            return picture_cycle[int(dayspassed or 0) % len(picture_cycle)]
        return ""

    def tavern_melissa_room_can_show_sleeping():
        try:
            Melissa.sync_room_problem_state()
        except Exception:
            pass
        temp_room = str(Melissa.var.get("temp_room", "") or "").strip()
        if temp_room and Melissa.bats_stage() < 8:
            return False
        if str(getLocation("melissa") or "") != "TavernMelissaRoom":
            return False
        return int(time or 0) >= 4 or (household_morning_issue_type("melissa") == "sleepy" and int(hour or 0) < 12)

    def tavern_melissa_room_picture():
        clara_picture = tavern_melissa_room_clara_visit_picture() if tavern_melissa_room_clara_visit_active() else ""
        if str(clara_picture or "").strip():
            return clara_picture
        if tavern_melissa_room_can_show_sleeping():
            sleep_picture = tavern_melissa_room_sleep_picture()
            if str(sleep_picture or "").strip():
                return sleep_picture
        return "images/tavern/secondfloor/girls_room_day.png"

    def tavern_melissa_room_get_object(object_id):
        object_key = str(object_id or "").strip()
        for room_object in TavernMelissaRoomRoom.visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    def tavern_melissa_room_call_label(label_name="", *label_args):
        label = str(label_name or "").strip()
        if label == "" or not renpy.has_label(label):
            return
        return renpy.call_in_new_context(label, *tuple(label_args or ()))

    def tavern_melissa_room_object_hyperlink_handler(value=""):
        object_key = str(value or "").strip()
        if object_key == "":
            return
        return tavern_melissa_room_call_label("TavernMelissaRoomObjectMenu", object_key)

    config.hyperlink_handlers["melissa_room_object"] = tavern_melissa_room_object_hyperlink_handler

    TavernMelissaRoomRoom = Room(
        code_name="TavernMelissaRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Комната Мелиссы",
        bg_picture="images/melissa/tavern/melissa_portrait.png",
        descriptions=[
            RoomDescription(
                text="Вы заглядываете в комнату Мелиссы. Обстановка небогатая: кровать, ларь, табурет и несколько аккуратно сложенных вещей.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в коридор", target="TavernUpstairs"),
        ],
        game_items=[
            bedroom_door_object("melissa_room_door_001", "TavernMelissaRoom", "Мелиссы"),
            "melissa_drawings_booklet_001",
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "object_menu_label": "TavernMelissaRoomObjectMenu",
        },
    )


label TavernMelissaRoom:
    call EnterLocation("TavernMelissaRoom")
    $ CurrentRoom = TavernMelissaRoomRoom
    $ CurLoc = "TavernMelissaRoom"
    $ location = CurLoc
    $ tavern_melissa_room_register_clara_visit()
    $ scene_image = tavern_melissa_room_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
        call ShowImage("", "", scene_image)
    if tavern_melissa_room_locked_from_inside():
        $ MainTxt = "Дверь закрыта изнутри. За ней слышны приглушенные голоса, шорох и короткий смешок."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Комната Мелиссы"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться в коридор", Call("AdvanceMovementTime", "TavernUpstairs"))]
        $ _melissa_locked_ui_return = None
        while _melissa_locked_ui_return is None:
            call screen main_ui
            $ _melissa_locked_ui_return = _return
        jump TavernMelissaRoom
    call RoomEnterEventGate(CurLoc, False)
    $ MainTxt = TavernMelissaRoomRoom.descriptions[0].text
    $ _melissa_room_notice = household_room_issue_notice_text("melissa")
    if str(_melissa_room_notice or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_melissa_room_notice or "")
    $ _melissa_temp_room_notice = melissa_temp_room_text()
    if str(_melissa_temp_room_notice or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_melissa_temp_room_notice or "")
    $ MainTxt = werecat_append_visible_text(MainTxt, "TavernMelissaRoom")
    $ CurLocDesc = MainTxt
    call TavernMelissaRoomBuildActions
    if tavern_melissa_room_pests_event_ready():
        call MelissaRoomPestsEvent
    $ _melissa_room_ui_return = None
    while _melissa_room_ui_return is None:
        call screen main_ui
        $ _melissa_room_ui_return = _return
    jump TavernMelissaRoom


label TavernMelissaRoomBuildActions:
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = []
    if tavern_melissa_room_locked_from_inside():
        $ current_action_items = [MenuItem("Вернуться в коридор", Call("AdvanceMovementTime", "TavernUpstairs"))]
        return
    python:
        for _issue_action in list(household_room_issue_action_specs("melissa") or []):
            current_action_items.append(MenuItem(str(_issue_action.get("label", "") or ""), Call(str(_issue_action.get("target", "") or ""), *tuple(_issue_action.get("args", ()) or ()))))
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernMelissaRoom", "", "")))
    $ current_action_items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernMelissaRoom", "TavernMelissaRoomBuildActions")))
    if story_event_available("TavernMelissaRoom", "clara_paintings"):
        $ current_action_items.append(MenuItem("Выслушать Клариссу и Мелиссу", Call("checkTriggers", "TavernMelissaRoom", "clara_paintings", 0)))
    python:
        for _room_object in TavernMelissaRoomRoom.visible_game_items():
            current_action_items.append(MenuItem(_room_object.name, Call("TavernMelissaRoomObjectMenu", _room_object.object_id)))
    python:
        for _exit in TavernMelissaRoomRoom.visible_exits():
            current_action_items.append(MenuItem(_exit.label, Call("AdvanceMovementTime", _exit.target)))
    return


label TavernMelissaRoomObjectMenu(object_id="", preserve_text=False):
    $ _room_object = tavern_melissa_room_get_object(object_id)
    if _room_object is None:
        call TavernMelissaRoomBuildActions
        return

    $ current_object_id = object_id
    if not bool(preserve_text):
        $ MainTxt = bedroom_door_object_text(_room_object)
        $ CurLocDesc = MainTxt
    $ current_action_title = str(_room_object.name or "Комната Мелиссы")
    $ current_action_content = None
    $ current_action_items = []
    python:
        _melissa_room_has_take_action = False
        for _room_action in _room_object.visible_actions():
            _room_args = tuple(getattr(_room_action, "args", ()) or ())
            if str(getattr(_room_action, "target", "") or "") == "Take":
                _melissa_room_has_take_action = True
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("TavernMelissaRoomObjectText", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        if bool(getattr(_room_object, "carriable", False)) and not _melissa_room_has_take_action:
            current_action_items.append(MenuItem("Взять", Call("Take", object_id, "TavernMelissaRoom", "", object_id)))
        current_action_items.append(MenuItem("Назад", Call("TavernMelissaRoomRestore")))
    return


label TavernMelissaRoomObjectText(object_id="", action_id=""):
    python:
        _room_text = ""
        _room_name = ""
        _room_object = tavern_melissa_room_get_object(object_id)
        if _room_object is not None:
            _room_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _room_text = str(_room_action.target or "")
                    break
        if _room_text:
            MainTxt = _room_text
            CurLocDesc = _room_text
            current_action_title = _room_name or "Комната Мелиссы"
    call TavernMelissaRoomObjectMenu(object_id)
    return


label TavernMelissaRoomRestore:
    $ scene_image = tavern_melissa_room_picture() or TavernMelissaRoomRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
        call ShowImage("", "", scene_image)
    $ MainTxt = TavernMelissaRoomRoom.descriptions[0].text
    $ _melissa_room_notice = household_room_issue_notice_text("melissa")
    if str(_melissa_room_notice or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_melissa_room_notice or "")
    $ _melissa_temp_room_notice = melissa_temp_room_text()
    if str(_melissa_temp_room_notice or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_melissa_temp_room_notice or "")
    $ MainTxt = werecat_append_visible_text(MainTxt, "TavernMelissaRoom")
    $ CurLocDesc = MainTxt
    call TavernMelissaRoomBuildActions
    return


