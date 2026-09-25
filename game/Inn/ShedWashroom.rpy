init -30 python:
    def tavern_bathday_ready():
        return tavern.renovation_complete("shed") and _pc_hot_water_is_ready(ShedHotWaterStoveObject)

init 6 python:
    def tavern_bathday_breakfast_request_ready():
        return (
            tavern.renovation_complete("shed")
            and int(calendar_v2.week or 0) in (3, 6)
            and 9 <= int(calendar_v2.hour or 0) <= 11
            and "sandra" in list(player.tavern_management.breakfast.present_ids or [])
        )

    def tavern_bathday_pictures():
        folder = "images/tavern/backyard/shed/bathDay/"
        pictures = sorted(path for path in renpy.list_files() if path.startswith(folder) and path.lower().endswith((".jpg", ".png", ".webp")))
        chosen = []
        for index in range(min(3, len(pictures))):
            roll = procedural_randint(0, len(pictures) - 1, "tavern_bathday_%s_%s" % (current_game_day(), index))
            chosen.append(pictures.pop(roll))
        return chosen

    ShedWashroomDefinition = Room(
        code_name="ShedWashroom",
        display_name="Прачечная и купальня",
        group_name=ROOM_GROUP_TAVERN,
        bg_picture="images/tavern/backyard/shed/washroom.png",
        descriptions=[RoomDescription(
            text="Это отдельная комната в отремонтированном сарае. Здесь стоят купель, корыто для стирки и скамья; на полках сложены полотенца и белье. Плотная дверь отделяет прачечную от соседнего помещения с печью и запасом дров.",
            priority=100,
        )],
        exits=[RoomExit(label="Вернуться к печи и поленнице", target="Shed", minutes_to_pass=1)],
        game_items=["shed_wash_tub"],
        custom_properties={"object_menu_label": "ShedWashroomBath"},
    )

    def shed_washroom_picture():
        if 6 <= int(calendar_v2.hour) < 20:
            return "images/tavern/backyard/shed/washroom.png"
        return "images/tavern/backyard/shed/washroom_night.png"

label ShedWashroom:
    if not tavern.renovation_complete("shed"):
        jump Shed
    $ rooms.enter("ShedWashroom")
    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.picture = shed_washroom_picture()
    $ scene_runtime.text = rooms.current.visible_descriptions()[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.current.mark_visited()
    $ main_ui_runtime.action_title = "Прачечная и купальня"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    while True:
        call screen main_ui


label story_tavern_bathday:
    $ renpy.dynamic("_bathday_pictures", "_bathday_index")
    $ _bathday_pictures = tavern_bathday_pictures()
    if len(_bathday_pictures) < 3 or not _pc_hot_water_is_ready(ShedHotWaterStoveObject):
        return False
    $ main_ui_begin_native_scene_state("Банный день")
    show screen main_ui
    "Вы заходите в купальню. Сандра, Мелисса и Аманда уже собрались у наполненной горячей водой купели; рабочий день наконец можно оставить за дверью."
    $ _bathday_index = 0
    while _bathday_index < len(_bathday_pictures):
        vscene _bathday_pictures[_bathday_index]
        "Плеск воды и негромкий смех наполняют купальню. Девушки отдыхают, приводят себя в порядок и оживленно переговариваются."
        menu:
            "Продолжить":
                $ _bathday_index += 1
    python:
        for _bathday_girl in (Sandra, Melissa, Amanda):
            _bathday_girl.set_sex_stat("beauty", min(100, int(_bathday_girl.sex_stat("beauty", 0) or 0) + 10))
            _bathday_girl.bathday_day = current_game_day()
    $ _set_object_state_int(ShedHotWaterStoveObject, "hot_water_until_minute", 0)
    "После купания все трое выглядят отдохнувшими и ухоженными. Горячая вода в баке закончилась."
    menu:
        "Вернуться в купальню":
            pass
    $ main_ui_end_native_scene_state()
    return True
