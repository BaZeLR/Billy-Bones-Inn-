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
        if int(hour or 0) < 12 and int(week or 0) != 7:
            if str(getLocation("amanda") or "") == "TavernStorage" and renpy.loadable("images/amanda/tavern/amanda_storage.png"):
                return "images/amanda/tavern/amanda_storage.png"
            if str(getLocation("melissa") or "") == "TavernStorage":
                melissa_basement = Melissa.image_path("tavern", "basement")
                if melissa_basement:
                    return melissa_basement
                if renpy.loadable("images/tavern/storage/storage_room.png"):
                    return "images/tavern/storage/storage_room.png"
        return str(TavernStorageRoom.bg_picture or "")

    def tavern_storage_text():
        text_parts = [str(TavernStorageRoom.descriptions[0].text or "").strip()]
        if tavern_kitchen_food_stock_count() > 0:
            text_parts.append("На полках отложены принесенные вами припасы для кухни: %s." % tavern_kitchen_food_stock_summary())
        if int(hour or 0) < 12 and int(week or 0) != 7:
            names_here = tavern_household_present_names("TavernStorage")
            if str(names_here or "").strip() and str(names_here or "") != "никто":
                text_parts.append("До полудня в кладовой возятся: %s." % str(names_here))
        text_parts.append(werecat_visible_text("TavernStorage"))
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
            RoomExit(label="Вернуться на кухню", target="TavernKitchen", minutes_to_pass=10),
        ],
        game_items=[
            TavernStorageSuppliesObject,
        ],
        custom_properties={},
    )


label TavernStorage:
    $ CurLoc = "TavernStorage"
    $ _storage_room = get_registered_room(CurLoc) or TavernStorageRoom
    call RoomEnterEventGate(CurLoc, False)
    $ scene_image = tavern_storage_picture() or _storage_room.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = tavern_storage_text()
    $ CurLocDesc = MainTxt
    $ _storage_menu = _storage_room.build_menu_sections()
    $ current_action_title = "Кладовая"
    $ current_action_content = None
    $ current_action_items = _storage_menu["movement"] + _storage_menu["actions"]
    $ UI_mode = "scene"
    $ UI_selected_char = ""
    $ current_girl_key = ""
    call screen main_ui
    jump TavernStorage


