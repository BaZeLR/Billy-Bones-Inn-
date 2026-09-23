# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_empty_room_picture(view="lounge"):
        if tavern.renovation_complete("guest_room") or Sofa.installed:
            furniture = "sofa" if Sofa.installed else "lounge"
            lighting = "day" if 6 <= int(calendar_v2.hour or 0) < 18 else "night"
            fire = "lit" if _pc_fire_is_active(TavernGuestRoomStoveObject) else "cold"
            return "images/tavern/guest_room/%s_%s_%s.png" % (furniture, lighting, fire)
        if view == "bedroom":
            return "images/amanda/Room/emptyroom.jpg"
        return rooms.get("TavernEmptyRoom").bg_picture

    def tavern_empty_room_description():
        if tavern.renovation_complete("guest_room"):
            text = "Гостевая комната отремонтирована: добротная кровать с занавесями, шкаф и стол превращают ее в уютную небольшую гостиную. Здесь удобно принять гостей и спокойно побеседовать."
        else:
            text = rooms.get("TavernEmptyRoom").descriptions[0].text
        if Sofa.installed:
            text += "\n\nУ каменной печи стоит старинный диван Хордуса: бордовый бархат, резное дерево и ножки в виде звериных лап. Иногда его резные ножки сами собой переступают по полу, а из обивки доносится приглушенное ворчание."
        if tavern_guest_room_stove_available():
            text += "\n\nВ печи горит огонь." if _pc_fire_is_active(TavernGuestRoomStoveObject) else "\n\nКаменная печь сейчас холодная."
        if tavern_glory_hole_available():
            text += " Рядом с печью есть дверь в комнатку с глорихолом."
        if tavern.renovation_days_left("guest_room"):
            text += "\n\nДо окончания ремонта осталось дней: %s." % tavern.renovation_days_left("guest_room")
        return text

    def tavern_empty_room_peephole_visible():
        return tavern.renovation_complete('peephole')

    def tavern_empty_room_peephole_has_client():
        if not player.tavern_management.isTavernOpen or not tavern.renovation_complete('peephole'):
            return False
        girl_name = str(rooms.get("TavernMain").state.get("client_room_girl", "") or "")
        if girl_name == "georgett":
            return 13 <= int(calendar_v2.hour or 0) <= 15 and Georgett.can_work_tavern() and CheckIfSexEventExist("georgett", 3, "Prostitution") > 0
        return story_event_available("TavernEmptyRoom", "tavern_client_room")

    def tavern_empty_room_peephole_no_client():
        return tavern.renovation_complete('peephole') and not tavern_empty_room_peephole_has_client()

    TavernEmptyRoomPeepholeObject = GameObject(
        object_id="tavern_empty_room_peephole",
        name="Потайное окошко",
        description="В стене вашей комнаты спрятано потайное окошко, за которое вы заплатили Драупниру. Отсюда можно наблюдать за происходящим в гостевой.",
        picture="images/amanda/Room/emptyroom.jpg",
        condition=tavern_empty_room_peephole_visible,
        actions=[
            ObjectAction(
                action_id="peek_client_room",
                label="Подглядеть в комнату",
                hook="call",
                target="TavernEmptyRoomPeekClient",
                condition=tavern_empty_room_peephole_has_client,
            ),
            ObjectAction(
                action_id="peek_empty_client_room",
                label="Проверить окошко",
                hook="call",
                target="TavernEmptyRoomPeekEmpty",
                condition=tavern_empty_room_peephole_no_client,
            ),
        ],
        custom_properties={},
    )

    def tavern_empty_room_action_items():
        items = rooms.get("TavernEmptyRoom").build_object_items()
        if tavern_upstairs_can_clean_rooms():
            items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernEmptyRoom", "", "")))
        items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernEmptyRoom")))
        for room_exit in rooms.get("TavernEmptyRoom").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target)))
        return items

    TavernEmptyRoomRoomDefinition = Room(
        code_name="TavernEmptyRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Гостевая комната",
        bg_picture="bg amanda_room",
        descriptions=[
            RoomDescription(
                text="Вы открываете гостевую комнату. Здесь пока почти ничего нет: голая кровать, голые стены и пыль в углах. Сейчас комната никем не занята.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Пройти к глорихолу", target="TavernGloryHole", condition={"rule": "tavern_renovation", "code": "glory_hole"}),
            RoomExit(label="Вернуться в коридор", target="TavernUpstairs"),
        ],
        game_items=["guest_room_stove_001"],
        custom_properties={},
    )

image guest_room_peek = Composite(
    (1536, 1024),
    (0, 0), Transform(DynamicImage("[tavern_empty_room_picture('bedroom')]"), xysize=(1536, 1024)),
    (0, 0), "images/tavern/guest_room/peephole_frame.png",
)


label TavernEmptyRoom:
    $ rooms.enter("TavernEmptyRoom")
    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.picture = tavern_empty_room_picture()
    $ scene_runtime.text = tavern_empty_room_description()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = rooms.get("TavernEmptyRoom").display_name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_empty_room_action_items()
    while True:
        call screen main_ui




label TavernEmptyRoomPeekClient:
    if not tavern_empty_room_peephole_has_client():
        call TavernEmptyRoomPeekEmpty
        return
    if str(rooms.get("TavernMain").state.get("client_room_girl", "") or "") == "georgett":
        call TavernProstClients("georgett")
    else:
        call checkTriggers("TavernEmptyRoom", "tavern_client_room", 0)
    return


label TavernEmptyRoomPeekEmpty:
    $ main_ui_begin_native_scene_state("Потайное окошко")
    show screen main_ui
    vscene "guest_room_peek"
    "Вы осторожно проверяете потайное окошко из своей комнаты, но в гостевой сейчас никого нет. Остается только вернуться позже."
    menu:
        "Закрыть окошко":
            pass
    $ main_ui_end_native_scene_state()
    return
