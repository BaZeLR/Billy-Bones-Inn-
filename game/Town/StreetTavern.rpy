# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def street_tavern_sign_broken():
        return player.tavern_management.slogan_state == 0

    def street_tavern_sign_repairing():
        return player.tavern_management.slogan_state == 1

    def street_tavern_sign_fixed():
        return player.tavern_management.slogan_state > 1

    def street_tavern_draupnir_donkey_visible():
        return player.tavern_management.glory_hole == 1

    def street_tavern_exit_minutes(target_room=""):
        target_key = str(target_room or "").strip()
        if target_key == "TavernMain":
            return 5
        if target_key == "Church":
            return 5
        if target_key == "PortStreets":
            return 10
        return navigation_group_travel_minutes()

    StreetTavernRoomDefinition = Room(
        code_name="StreetTavern",
        group_name=ROOM_GROUP_CITY,
        display_name="Улица Мясников",
        bg_picture="bg StreetTavern",
        descriptions=[
            RoomDescription(
                text="Вы стоите на улице мясников, около вашего трактира 'Дикий жеребец'.",
                priority=100,
            ),
            RoomDescription(
                text="Вход в ваш трактир украшает простая вывеска в виде взвившегося на дыбы коня. Вывеска изрядно выцвела и потрескалась.",
                condition=street_tavern_sign_broken,
                priority=90,
            ),
            RoomDescription(
                text="Над вашей покосившейся вывеской в поте гномьего лица своего работает мастер Драупнир. Он сосредоточенно строгает, обтесывает, пилит и красит. Отвлекать его сейчас было бы неразумно.",
                condition=street_tavern_sign_repairing,
                priority=90,
            ),
            RoomDescription(
                text="Вход в ваш трактир украшает роскошная вывеска в виде взвившегося на дыбы могучего коня. Вывеска изящно сделана, красиво и цветасто покрашенна, а также тщательно отполированна. Она выгодно отличает ваш трактир от конкурентов.",
                condition=street_tavern_sign_fixed,
                priority=90,
            ),
            RoomDescription(
                text="У входа в трактир стоит ослик мастера Драупнира. Сам хозяин, судя по всему, внутри.",
                condition=street_tavern_draupnir_donkey_visible,
                priority=80,
            ),
            RoomDescription(
                text="Сама же улица ничем не примечательна. От нее вы можете идти в переулки идущие по направлению к порту, на рынок, к городским воротам, в церковь или в квартал ремесленников.",
                priority=70,
            ),
        ],
        exits=[
            RoomExit(label="Зайти в трактир", target="TavernMain"),
            RoomExit(label="Идти на рынок", target="MarketPlace"),
            RoomExit(label="Идти к порту", target="PortStreets"),
            RoomExit(label="Идти к церкви", target="Church"),
            RoomExit(label="Идти в квартал ремесленников", target="ArtisansQuarter"),
        ],
        game_items=[
            GameObject(
                object_id="signboard",
                name="Вывеска трактира",
                description="Над входом висит вывеска вашего трактира.",
                actions=[
                    ObjectAction(
                        action_id="examine_signboard",
                        label="Осмотреть вывеску",
                        hook="call",
                        target="StreetTavernExamineSignboard",
                    ),
                ],
            ),
            GameObject(
                object_id="street_view",
                name="Улица",
                description="Обычная городская улица, откуда можно пройти в несколько важных частей города.",
                actions=[
                    ObjectAction(
                        action_id="examine_street",
                        label="Осмотреть улицу",
                        hook="text",
                        target="Отсюда удобно идти к рынку, порту, церкви и в квартал ремесленников.",
                    ),
                ],
            ),
        ],
    )

    def street_tavern_get_object(object_id):
        object_key = str(object_id or "").strip()
        for room_object in rooms.get("StreetTavern").visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    def street_tavern_action_items():
        items = []
        for room_object in rooms.get("StreetTavern").visible_game_items():
            items.append(MenuItem(room_object.name, Call("StreetTavernObjectMenu", room_object.object_id)))
        for room_exit in rooms.get("StreetTavern").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target, street_tavern_exit_minutes(room_exit.target))))
        return items

    def street_tavern_location_text():
        parts = [
            str(row.text or "")
            for row in rooms.get("StreetTavern").visible_descriptions()
            if str(row.text or "").strip()
        ]
        if dog.is_stray_here("StreetTavern"):
            parts.append("Неподалеку от входа крутится бродячий пес, время от времени принюхиваясь к прохожим.")
        return "\n\n".join(parts)

label StreetTavern:
    $ renpy.dynamic("_street_tavern_event_check_block")
    scene black
    show bg StreetTavern at master
    $ rooms.enter("StreetTavern")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ main_ui_runtime.action_title = "Куда идти"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""

    call ShowImageSeq("general", "", "LocStreetTavern", 2)
    python:
        try:
            _street_tavern_event_check_block = _args[0]
        except Exception:
            _street_tavern_event_check_block = ""

    if _street_tavern_event_check_block != "EventCheckBlock":
        call RoomEnterEventGate(rooms.current_code, False)

    $ scene_runtime.text = street_tavern_location_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = street_tavern_action_items()
    $ rooms.get("StreetTavern").mark_visited()

    while True:
        call screen main_ui


label StreetTavernObjectMenu(object_id=""):
    $ renpy.dynamic("_street_object")
    $ renpy.dynamic("_street_action", "_street_menu_item")
    $ _street_object = street_tavern_get_object(object_id)
    if _street_object is None:
        $ main_ui_runtime.action_title = "Куда идти"
        $ main_ui_runtime.action_items = street_tavern_action_items()
        return
    $ scene_runtime.text = str(_street_object.description or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(_street_object.name or "Объект")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _street_action in _street_object.visible_actions():
            _street_menu_item = room_action_menu_item(_street_action)
            if _street_menu_item is not None:
                main_ui_runtime.action_items.append(_street_menu_item)
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "text", street_tavern_location_text()),
            SetField(scene_runtime, "location_text", street_tavern_location_text()),
            SetField(main_ui_runtime, "action_title", "Куда идти"),
            SetField(main_ui_runtime, "action_items", street_tavern_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label StreetTavernExamineSignboard:
    if player.tavern_management.slogan_state == 0:
        "Вывеска выглядит старой и выцветшей. Она уже давно просится в руки хорошего мастера."
    elif player.tavern_management.slogan_state == 1:
        "Мастер Драупнир как раз приводит вывеску в порядок. Лучше не мешать ему за работой."
    else:
        "Теперь вывеска действительно выглядит так, словно достойна хорошего трактира."
    return


