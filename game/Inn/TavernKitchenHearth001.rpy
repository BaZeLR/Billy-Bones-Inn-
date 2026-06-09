# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_kitchen_hearth_wood_stock():
        loose_wood = _room_item_count_by_id(TavernKitchenRoom, "chopped_wood_001")
        if loose_wood > 0:
            while _room_remove_item_by_id(TavernKitchenRoom, "chopped_wood_001"):
                _add_object_state_int(TavernKitchenHearthObject, "chopped_wood_stock", 1, 0)
        return _object_state_int(TavernKitchenHearthObject, "chopped_wood_stock", 0)

    def tavern_kitchen_hearth_drop_wood_visible(_obj=None):
        return _player_has_item_by_id("chopped_wood_001")

    def tavern_kitchen_hearth_description():
        fire_active = _pc_fire_is_active(TavernKitchenHearthObject)
        ash_dirty = _object_state_int(TavernKitchenHearthObject, "ash_dirty", 0)
        wood_stock = tavern_kitchen_hearth_wood_stock()
        if fire_active and ash_dirty > 0:
            description = "В очаге горит огонь, и жара должно хватить еще примерно на {b}%s{/b} ч. Можно подложить дрова, чтобы снова получить полный двенадцатичасовой жар. Внизу уже собирается зола." % str(max(1, int((_pc_fire_remaining_minutes(TavernKitchenHearthObject) + 59) / 60)))
        elif fire_active:
            description = "В очаге горит огонь. Жара должно хватить еще примерно на {b}%s{/b} ч. Можно подложить дрова, чтобы снова получить полный двенадцатичасовой жар." % str(max(1, int((_pc_fire_remaining_minutes(TavernKitchenHearthObject) + 59) / 60)))
        elif ash_dirty > 0:
            description = "Очаг остыл, но в нем скопилась зола после прошлой топки."
        else:
            description = "Большой очаг, на котором готовят пищу. Сейчас он не разожжен."
        if wood_stock > 0:
            description += "\n\nРядом с очагом сложены колотые дрова: {b}%s{/b} шт." % str(wood_stock)
        carried_wood = int(_player_item_count_by_id("chopped_wood_001") or 0)
        if carried_wood > 0:
            description += "\nПри себе у вас колотые дрова: {b}%s{/b} шт." % str(carried_wood)
        return description

    TavernKitchenHearthObject = GameObject(
        object_id="hearth_001",
        name="Очаг",
        description="Большой очаг, на котором готовят пищу.",
        picture="images/tavern/kitchen/kitchen_stove.png",
        container=True,
        actions=[
            ObjectAction(
                action_id="make_fire",
                label="Разжечь огонь",
                hook="call",
                target="MakeFire",
                args=("chopped_wood_001", "TavernKitchen", "", "hearth_001"),
            ),
            ObjectAction(
                action_id="drop_chopped_wood_hearth",
                label="Сложить рядом дрова",
                hook="call",
                target="TavernKitchenHearthDepositWood",
                condition=tavern_kitchen_hearth_drop_wood_visible,
            ),
            ObjectAction(
                action_id="clean_ashes",
                label="Вычистить золу",
                hook="call",
                target="Clean",
                args=("ashes", "TavernKitchen", "", "hearth_001"),
            ),
        ],
        state={"fire_started_minute": 0, "fire_until_minute": 0, "fire_units": 0, "fire_adds": 0, "ash_dirty": 0, "chopped_wood_stock": 0},
        carriable=False,
        stackable=False,
    )


label TavernKitchenHearthDepositWood:
    if not _player_remove_item_by_id("chopped_wood_001", 1):
        $ MainTxt = "У вас больше нет колотых дров."
        $ CurLocDesc = MainTxt
        call TavernKitchenObjectMenu("hearth_001")
        return
    $ _add_object_state_int(TavernKitchenHearthObject, "chopped_wood_stock", 1, 0)
    $ MainTxt = "Вы складываете колотые дрова рядом с очагом. Теперь у очага лежит {b}%s{/b} шт." % str(tavern_kitchen_hearth_wood_stock())
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenObjectMenu("hearth_001")
    return
