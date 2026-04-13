init 6 python:
    def tavern_upstairs_can_enter_sandra_room():
        return int(Friends.get("sandra", 0) or 0) >= 10 or int(SandraVar.get("RoomUnlocked", 0) or 0) == 1

    def tavern_sandra_room_visible():
        return _tavern_is_in_room("sandra", "TavernSandraRoom")

    TavernSandraRoomRoom = Room(
        code_name="TavernSandraRoom",
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
        game_items=[],
        npcs=[
            {"npc_id": "sandra", "name": "Сандра", "condition": tavern_sandra_room_visible, "talk_label": "IntSandraTalk", "auto_card": True},
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={},
    )


label TavernSandraRoom:
    if not tavern_upstairs_can_enter_sandra_room():
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
    $ scene_image = CurrentRoom.bg_picture or None
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
    if household_morning_issue_type("sandra") == "sick" and int(_player_item_count_by_id("healing_potion_001") or 0) > 0:
        $ current_action_items.append(MenuItem("Принести Сандре лечебное зелье", Call("HouseholdMorningIssueCure", "sandra")))
    elif household_morning_issue_type("sandra") == "sleepy":
        $ current_action_items.append(MenuItem("Разбудить Сандру", Call("HouseholdWakeSleepyGirl", "sandra")))
    if _tavern_is_in_room("sandra", "TavernSandraRoom") and int(Friends.get("sandra", 0) or 0) >= 5 and int(AskedToday.get("sandra", 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Сесть с Сандрой над трактирной книгой", Call("TavernSandraLedgerScene")))
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernSandraRoom", "", "")))
    $ current_action_items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernSandraRoom", "TavernSandraRoomBuildActions")))
    python:
        for _exit in TavernSandraRoomRoom.visible_exits():
            current_action_items.append(MenuItem(_exit.label, Call("AdvanceMovementTime", _exit.target)))
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
