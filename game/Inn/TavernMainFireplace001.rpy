# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_main_fireplace_wood_stock():
        loose_wood = _room_item_count_by_id(rooms.get("TavernMain"), "chopped_wood_001")
        if loose_wood > 0:
            while _room_remove_item_by_id(rooms.get("TavernMain"), "chopped_wood_001"):
                _add_object_state_int(TavernMainFireplaceObject, "chopped_wood_stock", 1, 0)
        return _object_state_int(TavernMainFireplaceObject, "chopped_wood_stock", 0)

    def tavern_main_fireplace_drop_wood_visible(_obj=None):
        return player.item_count("chopped_wood_001") > 0

    def tavern_main_fireplace_description():
        fire_active = _pc_fire_is_active(TavernMainFireplaceObject)
        ash_dirty = _object_state_int(TavernMainFireplaceObject, "ash_dirty", 0)
        wood_stock = tavern_main_fireplace_wood_stock()
        if fire_active and ash_dirty > 0:
            description = "В камине горит огонь, и тепла должно хватить еще примерно на {b}%s{/b} ч. Можно подложить дрова, чтобы снова получить полный двенадцатичасовой жар. Внизу уже собирается зола." % str(max(1, int((_pc_fire_remaining_minutes(TavernMainFireplaceObject) + 59) / 60)))
        elif fire_active:
            description = "В камине горит огонь. Тепла должно хватить еще примерно на {b}%s{/b} ч. Можно подложить дрова, чтобы снова получить полный двенадцатичасовой жар." % str(max(1, int((_pc_fire_remaining_minutes(TavernMainFireplaceObject) + 59) / 60)))
        elif ash_dirty > 0:
            description = "Камин остыл, но в нем скопилась зола после прошлой топки."
        else:
            description = "Небольшой камин, который помогает держать главный зал в тепле. Сейчас он не разожжен."
        if wood_stock > 0:
            description += "\n\nРядом с камином сложены колотые дрова: {b}%s{/b} шт." % str(wood_stock)
        carried_wood = int(player.item_count("chopped_wood_001") or 0)
        if carried_wood > 0:
            description += "\nПри себе у вас колотые дрова: {b}%s{/b} шт." % str(carried_wood)
        return description

    TavernMainFireplaceObject = GameObject(
        object_id="fireplace_001",
        name="Камин",
        description="Небольшой камин, который помогает держать главный зал в тепле.",
        picture="images/tavern/mainhall/camin_mainHall.png",
        container=True,
        actions=[
            ObjectAction(
                action_id="make_fire",
                label="Разжечь огонь",
                hook="call",
                target="MakeFire",
                args=("chopped_wood_001", "TavernMain", "", "fireplace_001"),
            ),
            ObjectAction(
                action_id="drop_chopped_wood_fireplace",
                label="Сложить рядом дрова",
                hook="call",
                target="TavernMainFireplaceDepositWood",
                condition=tavern_main_fireplace_drop_wood_visible,
            ),
            ObjectAction(
                action_id="clean_ashes",
                label="Вычистить золу",
                hook="call",
                target="Clean",
                args=("ashes", "TavernMain", "", "fireplace_001"),
            ),
        ],
        state={"fire_started_minute": 0, "fire_until_minute": 0, "fire_adds": 0, "ash_dirty": 0, "chopped_wood_stock": 0},
        carriable=False,
        stackable=False,
    )


label TavernMainFireplaceDepositWood:
    if not player.remove_item("chopped_wood_001", 1):
        $ scene_runtime.text = "У вас больше нет колотых дров."
        $ scene_runtime.location_text = scene_runtime.text
        call TavernMainObjectMenu("fireplace_001")
        return
    $ _add_object_state_int(TavernMainFireplaceObject, "chopped_wood_stock", 1, 0)
    $ scene_runtime.text = "Вы складываете колотые дрова рядом с камином. Теперь у камина лежит {b}%s{/b} шт." % str(tavern_main_fireplace_wood_stock())
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernMainObjectMenu("fireplace_001")
    return
