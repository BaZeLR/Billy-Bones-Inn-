# The stove owns its saved fuel/fire/ash state and its native object menu.
# Chore consequences remain in the shared PlayerChoresSystem procedures.
init python:
    def tavern_guest_room_stove_available():
        return tavern.renovation_complete("guest_room") or Sofa.installed

default TavernGuestRoomStoveObject = GameObject(
    object_id="guest_room_stove_001",
    name="Каменная печь",
    description="Небольшая каменная печь обогревает гостевую. Перед ней оставлено место для дивана.",
    condition=tavern_guest_room_stove_available,
    state={"fire_started_minute": 0, "fire_until_minute": 0, "fire_adds": 0, "ash_dirty": 0, "chopped_wood_stock": 0},
    custom_properties={"object_menu_label": "TavernGuestRoomStoveMenu"},
)

label TavernGuestRoomStoveMenu(object_id="guest_room_stove_001"):
    $ renpy.dynamic("_guest_stove_fire_caption")
    if not tavern_guest_room_stove_available():
        return
    $ main_ui_begin_native_scene_state(TavernGuestRoomStoveObject.name)
    show screen main_ui
    while True:
        vscene tavern_empty_room_picture()
        if _pc_fire_is_active(TavernGuestRoomStoveObject):
            $ scene_runtime.text = "В каменной печи горит огонь. Тепла хватит еще примерно на %s ч." % max(1, (_pc_fire_remaining_minutes(TavernGuestRoomStoveObject) + 59) // 60)
        else:
            $ scene_runtime.text = "Каменная печь холодная. Чтобы разжечь ее, нужны колотые дрова."
        if _object_state_int(TavernGuestRoomStoveObject, "ash_dirty", 0) > 0:
            $ scene_runtime.text += " Внизу скопилась зола; ее можно вычистить."
        $ _guest_stove_fire_caption = "Подложить дрова" if _pc_fire_is_active(TavernGuestRoomStoveObject) else "Разжечь огонь"
        menu:
            "[_guest_stove_fire_caption]":
                call MakeFire("chopped_wood_001", "TavernEmptyRoom", "", "guest_room_stove_001")
                vscene tavern_empty_room_picture()
                menu:
                    "Продолжить":
                        pass
            "Вычистить золу" if _object_state_int(TavernGuestRoomStoveObject, "ash_dirty", 0) > 0:
                call Clean("ashes", "TavernEmptyRoom", "", "guest_room_stove_001")
                vscene tavern_empty_room_picture()
                menu:
                    "Продолжить":
                        pass
            "Назад":
                $ main_ui_end_native_scene_state()
                $ scene_runtime.picture = tavern_empty_room_picture()
                $ scene_runtime.text = tavern_empty_room_description()
                $ scene_runtime.location_text = scene_runtime.text
                $ main_ui_runtime.action_title = rooms.get("TavernEmptyRoom").display_name
                $ main_ui_runtime.object_id = ""
                return
