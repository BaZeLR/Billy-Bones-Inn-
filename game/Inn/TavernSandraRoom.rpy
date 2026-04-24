init 6 python:
    def tavern_upstairs_can_enter_sandra_room():
        return int(Friends.get("sandra", 0) or 0) >= 10 or int(SandraVar.get("RoomUnlocked", 0) or 0) == 1

    def tavern_sandra_room_door_locked():
        return bedroom_door_locked("TavernSandraRoom")

    def tavern_sandra_room_picture():
        slot = int(time or 0)
        if slot >= 4:
            for picture_path in (
                "images/sandra/sleeps .png",
                "images/sandra/player_room_sandra_0.jpg",
                "images/sandra/talk_0.png",
            ):
                if renpy.loadable(picture_path):
                    return picture_path
        if slot == 0:
            for picture_path in (
                "images/sandra/player_room_sandra_0.jpg",
                "images/sandra/talk_0.png",
            ):
                if renpy.loadable(picture_path):
                    return picture_path
        if str(getLocation("sandra") or "") == "TavernSandraRoom":
            for picture_path in (
                "images/sandra/talk_0.png",
                "images/sandra/player_room_sandra_0.jpg",
            ):
                if renpy.loadable(picture_path):
                    return picture_path
        return str(TavernSandraRoomRoom.bg_picture or "") or None

    def tavern_sandra_ledger_picture():
        for picture_path in (
            "images/sandra/sandra_room_booking.png",
            "images/sandra/talk_0.png",
            "images/sandra/player_room_sandra_0.jpg",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def tavern_sandra_room_get_object(object_id):
        object_key = str(object_id or "").strip()
        for room_object in TavernSandraRoomRoom.visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    TavernSandraRoomRoom = Room(
        code_name="TavernSandraRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Комната Сандры",
        bg_picture="images/tavern/secondfloor/sandra_room.png",
        descriptions=[
            RoomDescription(
                text="Вы осторожно заглядываете в комнату Сандры. Здесь все прибрано куда аккуратнее, чем в остальных комнатах: кровать застелена, вещи уложены, а у стены стоит небольшой ларь.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в коридор", target="TavernUpstairs"),
        ],
        game_items=[
            bedroom_door_object("sandra_room_door_001", "TavernSandraRoom", "Сандры"),
        ],
        npcs=[
            {"npc_id": "sandra", "name": "Сандра", "talk_label": "IntSandraTalk", "auto_card": True},
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "object_menu_label": "TavernSandraRoomObjectMenu",
        },
    )


label TavernSandraRoom:
    if tavern_sandra_room_door_locked():
        call EnterLocation("TavernUpstairs")
        $ CurrentRoom = TavernUpstairsRoom
        $ CurLoc = "TavernUpstairs"
        $ location = CurLoc
        $ _layout_last_picture = ""
        $ MainTxt = "Дверь в комнату Сандры заперта. Пока она не начала вам по-настоящему доверять, лезть туда рано."
        $ CurLocDesc = MainTxt
        call TavernUpstairsBuildActions
        jump TavernUpstairsView
    call EnterLocation("TavernSandraRoom")
    $ CurrentRoom = TavernSandraRoomRoom
    $ CurLoc = "TavernSandraRoom"
    $ location = CurLoc
    $ scene_image = tavern_sandra_room_picture()
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = TavernSandraRoomRoom.descriptions[0].text
    $ _sandra_room_notice = household_room_issue_notice_text("sandra")
    if str(_sandra_room_notice or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_sandra_room_notice or "")
    $ CurLocDesc = MainTxt
    call TavernSandraRoomBuildActions
    jump TavernSandraRoomView


label TavernSandraRoomBuildActions:
    $ current_action_title = "Комната Сандры"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _issue_action in list(household_room_issue_action_specs("sandra") or []):
            current_action_items.append(MenuItem(str(_issue_action.get("label", "") or ""), Call(str(_issue_action.get("target", "") or ""), *tuple(_issue_action.get("args", ()) or ()))))
    if str(getLocation("sandra") or "") == "TavernSandraRoom" and int(Friends.get("sandra", 0) or 0) >= 5 and int(AskedToday.get("sandra", 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Сесть с Сандрой над трактирной книгой", Call("TavernSandraLedgerScene")))
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernSandraRoom", "", "")))
    $ current_action_items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernSandraRoom", "TavernSandraRoomBuildActions")))
    python:
        for _room_object in TavernSandraRoomRoom.visible_game_items():
            current_action_items.append(MenuItem(_room_object.name, Call("TavernSandraRoomObjectMenu", _room_object.object_id)))
    python:
        for _exit in TavernSandraRoomRoom.visible_exits():
            current_action_items.append(MenuItem(_exit.label, Call("AdvanceMovementTime", _exit.target)))
    return


label TavernSandraRoomObjectMenu(object_id=""):
    $ _room_object = tavern_sandra_room_get_object(object_id)
    if _room_object is None:
        call TavernSandraRoomBuildActions
        return

    $ current_object_id = object_id
    $ MainTxt = bedroom_door_object_text(_room_object)
    $ CurLocDesc = MainTxt
    $ current_action_title = str(_room_object.name or "Комната Сандры")
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("TavernSandraRoomObjectText", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                _room_args = tuple(getattr(_room_action, "args", ()) or ())
                current_action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        current_action_items.append(MenuItem("Назад", Call("TavernSandraRoomRestore")))
    return


label TavernSandraRoomObjectText(object_id="", action_id=""):
    python:
        _room_text = ""
        _room_name = ""
        _room_object = tavern_sandra_room_get_object(object_id)
        if _room_object is not None:
            _room_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _room_text = str(_room_action.target or "")
                    break
        if _room_text:
            MainTxt = _room_text
            CurLocDesc = _room_text
            current_action_title = _room_name or "Комната Сандры"
    call TavernSandraRoomObjectMenu(object_id)
    return


label TavernSandraRoomRestore:
    $ scene_image = tavern_sandra_room_picture()
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = TavernSandraRoomRoom.descriptions[0].text
    $ _sandra_room_notice = household_room_issue_notice_text("sandra")
    if str(_sandra_room_notice or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_sandra_room_notice or "")
    $ CurLocDesc = MainTxt
    call TavernSandraRoomBuildActions
    return


label TavernSandraRoomView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernSandraRoomView


label TavernSandraLedgerScene:
    $ AskedToday["sandra"] = int(AskedToday.get("sandra", 0) or 0) + 1
    $ Talked["sandra"] = int(Talked.get("sandra", 0) or 0) + 1
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ otkroven["sandra"] = min(20, int(otkroven.get("sandra", 0) or 0) + 1)
    $ fun = _player_clamp(int(fun or 0) + 1, 0, 100)
    $ calendar_advance_minutes(30)
    $ _sandra_ledger_picture = str(tavern_sandra_ledger_picture() or "")
    if _sandra_ledger_picture != "":
        $ scene_image = _sandra_ledger_picture
        $ _layout_last_picture = _sandra_ledger_picture
        call ShowImage("", "", _sandra_ledger_picture)
    python:
        _ledger_stories = [
            "Вы с Сандрой усаживаетесь над трактирной книгой и какое-то время вместе сводите расходы, припасы и долги по мелочам. Постепенно сухие цифры переходят в разговор, и Сандра неожиданно вспоминает, как еще совсем молодой девчонкой училась считать закупки не по записям, а по памяти, потому что старшие все равно не доверяли ей книги. \"Ошибешься раз-другой, зато потом уже не забываешь,\" замечает она с сухой усмешкой.",
            "Вы раскладываете на кровати трактирные записи, и Сандра быстро втягивается в подсчеты так, словно всегда только этим и занималась. Когда дело доходит до старых долгов и привычек постоянных гостей, она вдруг рассказывает пару историй о тех временах, когда в доме все держалось не на деньгах, а на умении помнить, кто сколько наобещал и кто потом непременно попытается прикинуться забывчивым.",
            "Пока вы вместе перебираете счета и прикидываете, на чем трактир теряет больше всего, Сандра неожиданно начинает рассказывать о себе куда больше обычного. О том, как рано привыкла считать не только деньги, но и силы людей вокруг; кто вынослив, кто ленив, кто сорвется, а кто вытянет весь день на одной злости. В ее голосе почти нет жалобы, только старая привычка держать дом на своих плечах и заранее думать за всех остальных.",
        ]
        _ledger_idx = int((dayspassed or 0) + (hour or 0) + int(Friends.get("sandra", 0) or 0)) % len(_ledger_stories)
        MainTxt = _ledger_stories[_ledger_idx]
        CurLocDesc = MainTxt
    call TavernSandraRoomBuildActions
    return
