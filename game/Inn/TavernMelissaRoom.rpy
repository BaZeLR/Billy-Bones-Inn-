init 6 python:
    def tavern_melissa_room_picture():
        if household_morning_issue_type("melissa") == "sleepy" and int(hour or 0) < 12:
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
        if int(time or 0) >= 4:
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
        return "images/tavern/secondfloor/girls_room_day.png"

    def tavern_melissa_room_visible():
        return _tavern_is_in_room("melissa", "TavernMelissaRoom")

    TavernMelissaRoomRoom = Room(
        code_name="TavernMelissaRoom",
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
        game_items=[],
        npcs=[
            {"npc_id": "melissa", "name": "Мелисса", "condition": tavern_melissa_room_visible, "talk_label": "IntMelissaTalk", "auto_card": True},
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={},
    )


label TavernMelissaRoom:
    call EnterLocation("TavernMelissaRoom")
    $ CurrentRoom = TavernMelissaRoomRoom
    $ CurLoc = "TavernMelissaRoom"
    $ location = CurLoc
    $ scene_image = tavern_melissa_room_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = TavernMelissaRoomRoom.descriptions[0].text
    $ _melissa_room_notice = household_room_issue_notice_text("melissa")
    if str(_melissa_room_notice or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_melissa_room_notice or "")
    $ CurLocDesc = MainTxt
    call TavernMelissaRoomBuildActions
    if tavern_melissa_room_pests_event_ready():
        call MelissaRoomPestsEvent
    jump TavernMelissaRoomView


label TavernMelissaRoomBuildActions:
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = []
    if household_morning_issue_type("melissa") == "sick" and int(_player_item_count_by_id("healing_potion_001") or 0) > 0:
        $ current_action_items.append(MenuItem("Принести Мелиссе лечебное зелье", Call("HouseholdMorningIssueCure", "melissa")))
    elif household_morning_issue_type("melissa") == "sleepy":
        $ current_action_items.append(MenuItem("Разбудить Мелиссу", Call("HouseholdWakeSleepyGirl", "melissa")))
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernMelissaRoom", "", "")))
    $ current_action_items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernMelissaRoom", "TavernMelissaRoomBuildActions")))
    python:
        for _exit in TavernMelissaRoomRoom.visible_exits():
            current_action_items.append(MenuItem(_exit.label, Call("AdvanceMovementTime", _exit.target)))
    return


label TavernMelissaRoomView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernMelissaRoomView
