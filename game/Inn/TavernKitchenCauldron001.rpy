# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_kitchen_cauldron_description():
        if _pc_hot_water_is_ready(TavernKitchenCauldronObject):
            return "В котле есть горячая вода. Ее должно хватить до следующего дня."
        if _pc_fire_is_active(TavernKitchenHearthObject):
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
        state={"boiledWaterToday": 0, "hot_water_until_minute": 0},
        carriable=False,
        stackable=False,
        custom_properties={"object_menu_label": "TavernKitchenCauldronMenu"},
    )


label TavernKitchenCauldronMenu(object_id="cauldron_001"):
    $ renpy.dynamic("_cauldron_action", "_cauldron_args", "_cauldron_label")
    $ main_ui_runtime.object_id = "cauldron_001"
    $ main_ui_runtime.action_title = str(TavernKitchenCauldronObject.name or "Котел")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    if str(TavernKitchenCauldronObject.picture or "").strip() and renpy.loadable(str(TavernKitchenCauldronObject.picture or "").strip()):
        $ scene_runtime.picture = str(TavernKitchenCauldronObject.picture or "").strip()
    $ scene_runtime.text = tavern_kitchen_cauldron_description()
    $ scene_runtime.location_text = scene_runtime.text
    python:
        for _cauldron_action in TavernKitchenCauldronObject.visible_actions():
            _cauldron_args = tuple(getattr(_cauldron_action, "args", ()) or ())
            _cauldron_label = str(_cauldron_action.label or "")
            if _cauldron_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_cauldron_label, Call("TavernKitchenCauldronText", _cauldron_action.action_id)))
            elif _cauldron_action.hook == "call" and str(_cauldron_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_cauldron_label, Call(_cauldron_action.target, *_cauldron_args)))
            elif _cauldron_action.hook == "jump" and str(_cauldron_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_cauldron_label, Jump(_cauldron_action.target)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "picture", tavern_kitchen_picture() or rooms.get("TavernKitchen").bg_picture or None),
            SetField(scene_runtime, "text", tavern_kitchen_saved_text()),
            SetField(scene_runtime, "location_text", tavern_kitchen_saved_text()),
            SetField(main_ui_runtime, "action_title", "Кухня"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_kitchen_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label TavernKitchenCauldronText(action_id=""):
    $ renpy.dynamic("_cauldron_action", "_cauldron_text")
    python:
        _cauldron_text = ""
        for _cauldron_action in TavernKitchenCauldronObject.visible_actions():
            if getattr(_cauldron_action, "action_id", "") == str(action_id or ""):
                _cauldron_text = str(_cauldron_action.target or "")
                break
        if _cauldron_text:
            scene_runtime.text = _cauldron_text
            scene_runtime.location_text = _cauldron_text
            main_ui_runtime.action_title = str(TavernKitchenCauldronObject.name or "Котел")
    call TavernKitchenCauldronMenu
    return
