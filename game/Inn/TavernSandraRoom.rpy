# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_upstairs_can_enter_sandra_room():
        return int(Sandra.rel or 0) >= 10 or int(threads["sandraWeeklyEvaluation"].num or 0) > 0

    def tavern_sandra_room_door_locked():
        return bedroom_door_locked("TavernSandraRoom")

    def tavern_sandra_room_picture():
        slot = int(calendar_v2.time_slot())
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
        if str(people.location("sandra") or "") == "TavernSandraRoom":
            for picture_path in (
                "images/sandra/talk_0.png",
                "images/sandra/player_room_sandra_0.jpg",
            ):
                if renpy.loadable(picture_path):
                    return picture_path
        return str(rooms.get("TavernSandraRoom").bg_picture or "") or None

    def tavern_sandra_ledger_picture():
        for picture_path in (
            "images/sandra/sandra_room_booking.png",
            "images/sandra/talk_0.png",
            "images/sandra/player_room_sandra_0.jpg",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def tavern_sandra_room_text():
        text = str(rooms.get("TavernSandraRoom").descriptions[0].text or "")
        issue_notice = str(household_room_issue_notice_text("sandra") or "").strip()
        if issue_notice:
            text += "\n\n" + issue_notice
        return werecat_append_visible_text(text, "TavernSandraRoom")

    def tavern_sandra_room_get_object(object_id):
        object_key = str(object_id or "").strip()
        for room_object in rooms.get("TavernSandraRoom").visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    def tavern_sandra_room_action_items():
        items = []
        for issue_action in list(household_room_issue_action_specs("sandra") or []):
            items.append(MenuItem(str(issue_action.get("label", "") or ""), Call(str(issue_action.get("target", "") or ""), *tuple(issue_action.get("args", ()) or ()))))
        if str(people.location("sandra") or "") == "TavernSandraRoom" and people.can_talk("sandra") and int(Sandra.rel or 0) >= 5 and int(Sandra.asked_today or 0) == 0:
            items.append(MenuItem("Сесть с Сандрой над трактирной книгой", Call("TavernSandraLedgerScene")))
        items.extend(story_event_action_items("TavernSandraRoom"))
        if threads["sandraWeeklyEvaluation"].completed:
            items.append(MenuItem("Уединиться с Сандрой", Call("HouseholdSexEngine", "sandra", "TavernSandraRoom")))
        if tavern_upstairs_can_clean_rooms():
            items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernSandraRoom", "", "")))
        items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernSandraRoom")))
        for room_object in rooms.get("TavernSandraRoom").visible_game_items():
            items.append(MenuItem(room_object.name, Call("TavernSandraRoomObjectMenu", room_object.object_id)))
        for room_exit in rooms.get("TavernSandraRoom").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target)))
        return items

    TavernSandraRoomRoomDefinition = Room(
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
        custom_properties={
            "object_menu_label": "TavernSandraRoomObjectMenu",
        },
    )


label TavernSandraRoom:
    if tavern_sandra_room_door_locked():
        $ rooms.enter("TavernUpstairs")
        $ scene_runtime.picture = ""
        $ scene_runtime.text = "Дверь в комнату Сандры заперта. Пока она не начала вам по-настоящему доверять, лезть туда рано."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Наверху"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = tavern_upstairs_action_items()
        while True:
            call screen main_ui
    $ rooms.enter("TavernSandraRoom")
    $ scene_runtime.picture = tavern_sandra_room_picture()
    if scene_runtime.picture:
        vscene scene_runtime.picture
    $ scene_runtime.text = tavern_sandra_room_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Комната Сандры"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    while True:
        call screen main_ui


label TavernSandraRoomObjectMenu(object_id=""):
    $ renpy.dynamic("_room_object")
    $ renpy.dynamic("_room_action", "_room_args")
    $ _room_object = tavern_sandra_room_get_object(object_id)
    if _room_object is None:
        $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
        return

    $ main_ui_runtime.object_id = object_id
    $ scene_runtime.text = bedroom_door_object_text(_room_object)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(_room_object.name or "Комната Сандры")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call("TavernSandraRoomObjectText", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                _room_args = tuple(getattr(_room_action, "args", ()) or ())
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "text", tavern_sandra_room_text()),
            SetField(scene_runtime, "location_text", tavern_sandra_room_text()),
            SetField(main_ui_runtime, "action_title", "Комната Сандры"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_sandra_room_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label TavernSandraRoomObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_room_action", "_room_name", "_room_object", "_room_text")
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
            scene_runtime.text = _room_text
            scene_runtime.location_text = _room_text
            main_ui_runtime.action_title = _room_name or "Комната Сандры"
    return


label TavernSandraLedgerScene:
    $ renpy.dynamic("_sandra_ledger_picture", "_ledger_stories", "_ledger_idx")
    $ Sandra.mark_asked()
    $ Sandra.mark_talked()
    $ Sandra.change_social(friend_delta=1, open_delta=1)
    $ player.change_stat("fun", 1)
    $ calendar_v2.advance_minutes(30)
    $ _sandra_ledger_picture = str(tavern_sandra_ledger_picture() or "")
    if _sandra_ledger_picture != "":
        $ scene_runtime.picture = _sandra_ledger_picture
        vscene _sandra_ledger_picture
    python:
        _ledger_stories = [
            "Вы с Сандрой усаживаетесь над трактирной книгой и какое-то время вместе сводите расходы, припасы и долги по мелочам. Постепенно сухие цифры переходят в разговор, и Сандра неожиданно вспоминает, как еще совсем молодой девчонкой училась считать закупки не по записям, а по памяти, потому что старшие все равно не доверяли ей книги. \"Ошибешься раз-другой, зато потом уже не забываешь,\" замечает она с сухой усмешкой.",
            "Вы раскладываете на кровати трактирные записи, и Сандра быстро втягивается в подсчеты так, словно всегда только этим и занималась. Когда дело доходит до старых долгов и привычек постоянных гостей, она вдруг рассказывает пару историй о тех временах, когда в доме все держалось не на деньгах, а на умении помнить, кто сколько наобещал и кто потом непременно попытается прикинуться забывчивым.",
            "Пока вы вместе перебираете счета и прикидываете, на чем трактир теряет больше всего, Сандра неожиданно начинает рассказывать о себе куда больше обычного. О том, как рано привыкла считать не только деньги, но и силы людей вокруг; кто вынослив, кто ленив, кто сорвется, а кто вытянет весь день на одной злости. В ее голосе почти нет жалобы, только старая привычка держать дом на своих плечах и заранее думать за всех остальных.",
        ]
        _ledger_idx = int(calendar_v2.daysInGame + calendar_v2.hour + int(Sandra.rel or 0)) % len(_ledger_stories)
        scene_runtime.text = _ledger_stories[_ledger_idx]
        scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    return
