# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_kitchen_cauldron_description():
        tavern_kitchen_sync_hearth_state()
        if _pc_hot_water_is_ready(TavernKitchenCauldronObject):
            return "В котле есть горячая вода. Ее должно хватить до следующего дня."
        if _object_state_int(TavernKitchenCauldronObject, "canBoilWater", 0) > 0:
            return "Большой котел для кипячения воды. Огонь в очаге горит, воду можно вскипятить."
        return "Большой котел для кипячения воды. Сейчас в нем нет горячей воды."

    TavernKitchenCauldronObject = GameObject(
        object_id="cauldron_001",
        name="Котел",
        description="Большой котел для кипячения воды.",
        picture="images/tavern/kitchen/kitchen_stove.png",
        container=False,
        actions=[
            ObjectAction(
                action_id="boil_water",
                label="Вскипятить воду",
                hook="call",
                target="BoilWater",
                args=("cauldron_001", "TavernKitchen", "", "cauldron_001"),
            ),
        ],
        state={"canBoilWater": 0, "boiledWaterToday": 0, "hot_water_until_minute": 0, "hot_water_units": 0},
        carriable=False,
        stackable=False,
        custom_properties={"object_menu_label": "TavernKitchenCauldronMenu"},
    )


label TavernKitchenCauldronMenu(object_id="cauldron_001", refresh_only=False):
    $ tavern_kitchen_sync_hearth_state()
    $ current_object_id = "cauldron_001"
    $ current_action_title = str(TavernKitchenCauldronObject.name or "Котел")
    $ current_action_content = None
    $ current_action_items = []
    if str(TavernKitchenCauldronObject.picture or "").strip() and renpy.loadable(str(TavernKitchenCauldronObject.picture or "").strip()):
        $ _layout_last_picture = str(TavernKitchenCauldronObject.picture or "").strip()
    $ MainTxt = tavern_kitchen_cauldron_description()
    $ CurLocDesc = MainTxt
    python:
        for _cauldron_action in TavernKitchenCauldronObject.visible_actions():
            _cauldron_args = tuple(getattr(_cauldron_action, "args", ()) or ())
            _cauldron_label = str(_cauldron_action.label or "")
            if _cauldron_action.hook == "text":
                current_action_items.append(MenuItem(_cauldron_label, Call("TavernKitchenCauldronText", _cauldron_action.action_id)))
            elif _cauldron_action.hook == "call" and str(_cauldron_action.target or "") != "":
                current_action_items.append(MenuItem(_cauldron_label, Call(_cauldron_action.target, *_cauldron_args)))
            elif _cauldron_action.hook == "jump" and str(_cauldron_action.target or "") != "":
                current_action_items.append(MenuItem(_cauldron_label, Jump(_cauldron_action.target)))
        current_action_items.append(MenuItem("Назад", Jump("TavernKitchen")))
    return


label TavernKitchenCauldronText(action_id=""):
    python:
        _cauldron_text = ""
        for _cauldron_action in TavernKitchenCauldronObject.visible_actions():
            if getattr(_cauldron_action, "action_id", "") == str(action_id or ""):
                _cauldron_text = str(_cauldron_action.target or "")
                break
        if _cauldron_text:
            MainTxt = _cauldron_text
            CurLocDesc = _cauldron_text
            current_action_title = str(TavernKitchenCauldronObject.name or "Котел")
    call TavernKitchenCauldronMenu
    return
