init 6 python:
    import renpy.exports as renpy

    def tavern_storage_picture():
        if int(hour or 0) < 12 and int(week or 0) != 7:
            if str(getLocation("amanda") or "") == "TavernStorage" and renpy.loadable("images/amanda/tavern/amanda_storage.png"):
                return "images/amanda/tavern/amanda_storage.png"
            if str(getLocation("melissa") or "") == "TavernStorage":
                if renpy.loadable("images/melissa/tavern/basement.png"):
                    return "images/melissa/tavern/basement.png"
                if renpy.loadable("images/amanda/melissa_in storage.mp4"):
                    return "images/amanda/melissa_in storage.mp4"
        return str(TavernStorageRoom.bg_picture or "")

    def tavern_storage_text():
        text_parts = [str(TavernStorageRoom.descriptions[0].text or "").strip()]
        if int(hour or 0) < 12 and int(week or 0) != 7:
            names_here = tavern_household_present_names("TavernStorage")
            if str(names_here or "").strip() and str(names_here or "") != "никто":
                text_parts.append("До полудня в кладовой возятся: %s." % str(names_here))
        return "\n\n".join([row for row in text_parts if str(row or "").strip()])

    TavernStorageRoom = Room(
        code_name="TavernStorage",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Кладовая",
        bg_picture="bg StolyarWorkshop",
        descriptions=[
            RoomDescription(
                text="Вы заходите в кладовую при кухне. На полках и в ящиках хранится провизия, посуда и всякая хозяйственная мелочь.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на кухню", target="TavernKitchen"),
        ],
        game_items=[],
        npcs=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={},
    )


label TavernStorage:
    call EnterLocation("TavernStorage")
    $ CurrentRoom = TavernStorageRoom
    $ CurLoc = "TavernStorage"
    $ location = CurLoc
    call CheckDailyEvent("", "_story_enter", CurLoc, time)
    $ scene_image = tavern_storage_picture() or TavernStorageRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = tavern_storage_text()
    $ CurLocDesc = MainTxt
    $ current_action_title = "Кладовая"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _storage_exit in TavernStorageRoom.visible_exits():
            current_action_items.append(MenuItem(_storage_exit.label, Call("AdvanceMovementTime", _storage_exit.target)))
    jump TavernStorageView


label TavernStorageView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernStorageView
