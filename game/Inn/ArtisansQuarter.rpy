init python:
    ArtisansQuarterRoom = Room(
        code_name="ArtisansQuarter",
        display_name="Квартал ремесленников",
        bg_picture="bg ArtisansQuarter",
        descriptions=[
            RoomDescription(
                text="Вы находитесь в квартале ремесленников, на улице Плотников. Тщательно замощенные камнем мостовые, нарядно раскрашенные вывески, ладно построенные дома выдают богатство этого квартала. Здесь располагаются разнообразные лавки и мастерские. Для вас непосредственный интерес представляют мастерская столяра Драупнира и лавка модистки, портнихи, швеи и просто мастерицы на все руки Ирмы Фараго. Дальше улица Плотников ведет к богатым кварталам городского нобилитета.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Идти в мастерскую столяра Драупнира", target="StolyarWorkshop"),
            RoomExit(label="Идти в лавку портнихи Фараго", target="DressShop"),
            RoomExit(label="Зайти в цирюльню Серджио Пета", target="BarberShop"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[
            GameObject(
                object_id="workshops",
                name="Мастерские",
                description="Вдоль улицы тянутся ремесленные лавки и мастерские, каждая со своей вывеской и запахом работы.",
                actions=[
                    ObjectAction(
                        action_id="examine_workshops",
                        label="Осмотреть мастерские",
                        hook="text",
                        target="На этой улице трудятся хорошие мастера. Тут можно найти и столяра Драупнира, и лавку Ирмы Фараго, и цирюльню болтливого Серджио Пета.",
                    ),
                ],
            ),
            GameObject(
                object_id="farago_shop_sign",
                name="Вывеска Фараго",
                description="Яркая вывеска лавки Ирмы сразу бросается в глаза.",
                actions=[
                    ObjectAction(
                        action_id="examine_farago_sign",
                        label="Осмотреть вывеску",
                        hook="text",
                        target="Вывеска обещает, что здесь сошьют все: от простого платья до наряда для важного господина.",
                    ),
                ],
            ),
        ],
        npcs=[],
    )


label ArtisansQuarter:
    call EnterLocation("ArtisansQuarter")
    $ dog_prepare_current_spawn()
    $ CurrentRoom = ArtisansQuarterRoom
    $ CurLoc = "ArtisansQuarter"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_object_id = ""
    $ GirlDressBlock = 0
    $ _artisans_desc_rows = CurrentRoom.visible_descriptions()
    if len(_artisans_desc_rows) > 0:
        $ MainTxt = _artisans_desc_rows[0].text
    else:
        $ MainTxt = "Вы находитесь в квартале ремесленников."
    $ MainTxt += "\n\nМежду портновской лавкой и мастерской столяра примостилась цирюльня Серджио Пета: оттуда тянет мылом, горячими полотенцами и нескончаемыми городскими сплетнями."
    if dog_is_here("ArtisansQuarter"):
        $ MainTxt += "\n\nУ края мостовой крутится бродячий пес, заглядывающий в мастерские в поисках чего-нибудь съестного."
    $ CurLocDesc = MainTxt
    $ ArtisansQuarterSavedText = MainTxt
    $ CurrentRoom.mark_visited()

    call ShowImageSeq("general", "", "LocArtisansQuarter", 4)

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться к трактиру", Jump("StreetTavern"))]
        jump ArtisansQuarterView

    call ArtisansQuarterBuildActions
    jump ArtisansQuarterView


label ArtisansQuarterView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump ArtisansQuarterView


label ArtisansQuarterBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    python:
        if dog_is_here("ArtisansQuarter"):
            current_action_items.append(MenuItem(dog_room_action_caption("ArtisansQuarter"), Call("IntDogTalk", "ArtisansQuarter")))
        for _artisans_object in ArtisansQuarterRoom.visible_objects():
            current_action_items.append(MenuItem(_artisans_object.name, Call("ArtisansQuarterObjectMenu", _artisans_object.object_id)))
        for _artisans_exit in ArtisansQuarterRoom.visible_exits():
            current_action_items.append(MenuItem(_artisans_exit.label, Jump(_artisans_exit.target)))
    return


label ArtisansQuarterObjectMenu(object_id=""):
    $ _artisans_object = None
    python:
        for _room_object in ArtisansQuarterRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _artisans_object = _room_object
                break

    if _artisans_object is None:
        call ArtisansQuarterBuildActions
        return

    $ MainTxt = _artisans_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _artisans_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _artisans_action in _artisans_object.visible_actions():
            _artisans_args = tuple(getattr(_artisans_action, "args", ()) or ())
            if _artisans_action.hook == "text":
                current_action_items.append(MenuItem(_artisans_action.label, Call("ArtisansQuarterObjectText", object_id, _artisans_action.action_id)))
            elif _artisans_action.hook == "call" and str(_artisans_action.target or "") != "":
                current_action_items.append(MenuItem(_artisans_action.label, Call(_artisans_action.target, *_artisans_args)))
            elif _artisans_action.hook == "jump" and str(_artisans_action.target or "") != "":
                current_action_items.append(MenuItem(_artisans_action.label, Jump(_artisans_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("ArtisansQuarterRestore")))
    return


label ArtisansQuarterObjectText(object_id="", action_id=""):
    python:
        _artisans_text = ""
        _artisans_name = ""
        for _room_object in ArtisansQuarterRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _artisans_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _artisans_text = str(_room_action.target or "")
                    break
            break
        if _artisans_text:
            MainTxt = _artisans_text
            CurLocDesc = _artisans_text
            current_action_title = _artisans_name or "Действия"
    call ArtisansQuarterObjectMenu(object_id)
    return


label ArtisansQuarterRestore:
    $ MainTxt = ArtisansQuarterSavedText
    $ CurLocDesc = MainTxt
    call ShowImageSeq("general", "", "LocArtisansQuarter", 4)
    call ArtisansQuarterBuildActions
    return
