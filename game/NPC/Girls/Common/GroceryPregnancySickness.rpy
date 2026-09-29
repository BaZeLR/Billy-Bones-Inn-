init python:
    def grocery_pregnancy_sickness_girl(room_code=""):
        current_room = str(room_code or rooms.current_code or "").strip()
        if current_room != "GroceryStore" or not rooms.get("GroceryStore").is_open():
            return ""
        current_slot = calendar_v2.time_slot()
        for girl_key in ("becky", "inga"):
            girl_info = people.get_info(girl_key)
            if (girl_info is not None
                    and str(people.location(girl_key) or "") == current_room
                    and 0 < girl_info.pregnancy_days() < 80
                    and daily_events.exists(girl_key, "GroceryPregnancySickness", current_room, current_slot)):
                return girl_key
        return ""


label GroceryPregnancySickness(girl_name):
    $ renpy.dynamic("_grocery_sick_name", "_grocery_sick_picture")
    $ _grocery_sick_name = people_display_name(girl_name)
    $ _grocery_sick_picture = grocery_store_grocer_picture(girl_name)
    $ main_ui_begin_native_scene_state("Недомогание в лавке")
    show screen main_ui
    if _grocery_sick_picture:
        vscene _grocery_sick_picture
    else:
        vscene rooms.get("GroceryStore").bg_picture
    $ scene_runtime.text = "Вы едва переступаете порог лавки, как [_grocery_sick_name] поспешно отставляет товар и скрывается за дверью во двор. Через мгновение она возвращается, бледная, придерживаясь за косяк."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Предложить ей воды":
            $ scene_runtime.text = "Вы подаёте ей кружку воды. [_grocery_sick_name] делает несколько осторожных глотков и благодарно кивает. «То подташнивает, то отпускает. Сейчас пройдёт», — говорит она, присаживаясь на минуту."
        "Дать ей передохнуть":
            $ scene_runtime.text = "Вы молча ждёте у прилавка. [_grocery_sick_name] переводит дух, умывает лицо и возвращается к вам. «Прости, Стефан. Что-то опять мутит», — говорит она."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к покупкам":
            $ main_ui_end_native_scene_state()
            return True
