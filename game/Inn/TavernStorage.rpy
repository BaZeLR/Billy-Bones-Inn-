# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    import renpy.exports as renpy

    TavernStorageSuppliesObject = GameObject(
        object_id="tavern_storage_supplies_001",
        name="Кладовые припасы",
        description="Полки и ящики с провизией, которую вы приносите для кухонного хозяйства.",
        state={
            "stock": {},
            "effects": {},
        },
        carriable=False,
        stackable=False,
    )

    def tavern_storage_supplies_stock():
        if not isinstance(TavernStorageSuppliesObject.state.get("stock", None), dict):
            TavernStorageSuppliesObject.state["stock"] = {}
        return TavernStorageSuppliesObject.state["stock"]

    def tavern_storage_supplies_effects():
        if not isinstance(TavernStorageSuppliesObject.state.get("effects", None), dict):
            TavernStorageSuppliesObject.state["effects"] = {}
        return TavernStorageSuppliesObject.state["effects"]

    def tavern_storage_picture():
        if int(calendar_v2.hour or 0) < 12 and int(calendar_v2.week or 0) != 7:
            if str(people.location("amanda") or "") == "TavernStorage" and renpy.loadable("images/amanda/tavern/amanda_storage.png"):
                return "images/amanda/tavern/amanda_storage.png"
            if str(people.location("melissa") or "") == "TavernStorage":
                melissa_basement = MelissaStaticData.image_path("tavern", "basement")
                if melissa_basement:
                    return melissa_basement
                if renpy.loadable("images/tavern/storage/storage_room.png"):
                    return "images/tavern/storage/storage_room.png"
        return str(rooms.get("TavernStorage").bg_picture or "")

    def tavern_storage_text():
        text_parts = [str(rooms.get("TavernStorage").descriptions[0].text or "").strip()]
        if tavern_kitchen_food_stock_count() > 0:
            text_parts.append("На полках отложены принесенные вами припасы для кухни: %s." % tavern_kitchen_food_stock_summary())
        if int(calendar_v2.hour or 0) < 12 and int(calendar_v2.week or 0) != 7:
            names_here = tavern_household_present_names("TavernStorage")
            if str(names_here or "").strip() and str(names_here or "") != "никто":
                text_parts.append("До полудня в кладовой возятся: %s." % str(names_here))
        text_parts.append(werecat_visible_text("TavernStorage"))
        return "\n\n".join([row for row in text_parts if str(row or "").strip()])

    TavernStorageRoomDefinition = Room(
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
        game_items=[
            TavernStorageSuppliesObject,
        ],
        custom_properties={},
    )


label TavernStorage:
    $ renpy.dynamic("_storage_exit", "_storage_items")
    $ rooms.enter("TavernStorage")
    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.picture = tavern_storage_picture() or rooms.get("TavernStorage").bg_picture or None
    $ scene_runtime.text = tavern_storage_text()
    $ scene_runtime.location_text = scene_runtime.text
    python:
        _storage_items = []
        for _storage_exit in rooms.get("TavernStorage").visible_exits():
            _storage_items.append(MenuItem(_storage_exit.label, movement_actions(_storage_exit.target)))
    $ main_ui_runtime.action_title = "Кладовая"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = _storage_items
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.girl_key = ""
    while True:
        call screen main_ui


