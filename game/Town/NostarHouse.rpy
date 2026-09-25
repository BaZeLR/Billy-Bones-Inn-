init python:
    def nostar_house_has_sofa():
        return not Sofa.installed

    def nostar_house_sofa_gone():
        return bool(Sofa.installed)

    def nostar_house_picture():
        return "images/nostar/drawing_room_without_sofa.png" if Sofa.installed else "images/nostar/drawing_room.png"

    NostarHouseRoomDefinition = Room(
        code_name="NostarHouse",
        group_name=ROOM_GROUP_CITY,
        display_name="Дом леди Ностар Линк",
        bg_picture="images/nostar/drawing_room.png",
        descriptions=[
            RoomDescription(
                text="Большая гостиная леди Ностар отделана с изысканной небрежностью. Между окнами и камином стоит старинный бордовый диван с резными лапами. На боковом столике пустует золочёная клетка Розарио; хозяйка то и дело бросает на неё взгляд.",
                condition=nostar_house_has_sofa,
                priority=100,
            ),
            RoomDescription(
                text="В гостиной леди Ностар осталось пустое место между окнами и камином: диван уже отправлен в трактир. На боковом столике всё ещё стоит золочёная клетка Розарио.",
                condition=nostar_house_sofa_gone,
                priority=100,
            ),
        ],
        exits=[RoomExit(label="Выйти в квартал знати", target="NobilityQuarters", minutes_to_pass=5)],
        schedule=RoomSchedule(
            start="09:00",
            end="20:59",
            closed_text="Привратник объясняет, что леди Ностар сейчас никого не принимает.",
        ),
    )


label NostarHouse:
    $ rooms.enter("NostarHouse")
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    $ main_ui_runtime.action_title = rooms.current.display_name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    if rooms.current.is_open():
        vscene nostar_house_picture()
        $ scene_runtime.text = rooms.current.visible_descriptions()[0].text
    else:
        vscene "images/nostar/nobility_quarters.png"
        $ scene_runtime.text = rooms.current.schedule.closed_text
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.current.mark_visited()
    call RoomEnterEventGate(rooms.current_code, False)
    if rooms.current.is_open() and str(people.location("nostar") or "") == "NostarHouse":
        $ main_ui_runtime.action_items = [MenuItem("Поговорить с леди Ностар Линк", Call("IntNostarTalk"))] + rooms.current.build_exit_items()
    else:
        $ main_ui_runtime.action_items = rooms.current.build_exit_items()
    while True:
        call screen main_ui
