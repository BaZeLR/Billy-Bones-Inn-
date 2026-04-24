init python:
    def street_tavern_sign_broken():
        return SloganFixed == 0

    def street_tavern_sign_repairing():
        return SloganFixed == 1

    def street_tavern_sign_fixed():
        return SloganFixed > 1

    def street_tavern_draupnir_donkey_visible():
        return TavernGloryHole == 1

    StreetTavernRoom = Room(
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
        for room_object in StreetTavernRoom.visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

label StreetTavern:
    scene black
    show bg StreetTavern at master
    call EnterLocation("StreetTavern")
    $ dog_prepare_current_spawn()
    $ CurrentRoom = StreetTavernRoom
    $ CurLoc = "StreetTavern"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    $ current_action_title = "Куда идти"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""

    call ShowImageSeq("general", "", "LocStreetTavern", 2)
    python:
        try:
            _street_tavern_event_check_block = _args[0]
        except Exception:
            _street_tavern_event_check_block = ""

    if _street_tavern_event_check_block != "EventCheckBlock":
        call CheckDailyEvent("", "_story_enter", CurLoc, time)

    python:
        _street_desc_rows = StreetTavernRoom.visible_descriptions()
        _street_desc_parts = []
        for _desc_row in _street_desc_rows:
            _street_desc_parts.append(str(_desc_row.text or ""))
        CurLocDesc = "\n\n".join([part for part in _street_desc_parts if str(part or "").strip()])
        if dog_is_here("StreetTavern"):
            CurLocDesc += "\n\nНеподалеку от входа крутится бродячий пес, время от времени принюхиваясь к прохожим."
        MainTxt = CurLocDesc
        if dog_is_here("StreetTavern"):
            current_action_items.append(MenuItem(dog_room_action_caption("StreetTavern"), Call("IntDogTalk", "StreetTavern")))
        for _street_exit in StreetTavernRoom.visible_exits():
            current_action_items.append(MenuItem(_street_exit.label, Jump(_street_exit.target)))
    $ StreetTavernRoom.mark_visited()

    show screen main_ui
    $ renpy.pause(hard=True)
    return


label street_tavern_menu:
    $ _street_room = StreetTavernRoom
    python:
        _street_choices = []
        for _street_object in _street_room.visible_game_items():
            _street_choices.append((_street_object.name, ("object", _street_object.object_id)))
        for _street_exit in _street_room.visible_exits():
            _street_choices.append((_street_exit.label, ("jump", _street_exit.target)))
        _street_pick = renpy.display_menu(_street_choices)

    if isinstance(_street_pick, tuple) and len(_street_pick) >= 2:
        if _street_pick[0] == "object":
            call street_tavern_object_menu(_street_pick[1])
            jump street_tavern_menu
        if _street_pick[0] == "jump":
            jump expression _street_pick[1]
    return


label street_tavern_object_menu(object_id=""):
    if str(object_id or "") != "":
        $ street_tavern_object_menu_id = object_id
    $ object_id = street_tavern_object_menu_id
    $ _street_object = street_tavern_get_object(object_id)
    if _street_object is None:
        jump street_tavern_menu

    "[_street_object.description]"

    python:
        _street_object_choices = []
        for _street_action in _street_object.visible_actions():
            _street_object_choices.append((_street_action.label, ("action", _street_action.action_id)))
        _street_object_choices.append(("Назад", "__back__"))
        _street_object_pick = renpy.display_menu(_street_object_choices)
        _selected_street_action = None
        if isinstance(_street_object_pick, tuple) and len(_street_object_pick) >= 2:
            for _street_action in _street_object.visible_actions():
                if getattr(_street_action, "action_id", "") == _street_object_pick[1]:
                    _selected_street_action = _street_action
                    break

    if _street_object_pick == "__back__":
        jump street_tavern_menu

    if _selected_street_action is not None:
        if _selected_street_action.hook == "text":
            "[_selected_street_action.target]"
            $ street_tavern_object_menu_id = object_id
            jump street_tavern_object_menu
        if _selected_street_action.hook == "call" and _selected_street_action.target != "":
            call expression _selected_street_action.target
            $ street_tavern_object_menu_id = object_id
            jump street_tavern_object_menu
        if _selected_street_action.hook == "jump" and _selected_street_action.target != "":
            jump expression _selected_street_action.target

    $ street_tavern_object_menu_id = object_id
    jump street_tavern_object_menu


label StreetTavernExamineSignboard:
    if SloganFixed == 0:
        "Вывеска выглядит старой и выцветшей. Она уже давно просится в руки хорошего мастера."
    elif SloganFixed == 1:
        "Мастер Драупнир как раз приводит вывеску в порядок. Лучше не мешать ему за работой."
    else:
        "Теперь вывеска действительно выглядит так, словно достойна хорошего трактира."
    return


