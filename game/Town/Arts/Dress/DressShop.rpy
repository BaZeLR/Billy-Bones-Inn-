# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default dress_shop = DressShopRuntimeState()

init python:
    class DressShopRuntimeState(object):
        def __init__(self):
            self.produced = ""
            self.buyer = ""
            self.measure_stage = 0
            self.sex_step = 0
            self.girl_dress_block = 0

    def dress_shop_irma_working_idle():
        return str(dress_shop.produced or "") == ""

    def dress_shop_irma_working_order():
        return str(dress_shop.produced or "") != ""

    def dress_shop_clara_present():
        return str(people.location("clara") or "") == "DressShop"

    def dress_shop_room_text():
        return "\n\n".join(
            row.text for row in rooms.get("DressShop").visible_descriptions()
        )

    DressShopRoomDefinition = Room(
        code_name="DressShop",
        group_name=ROOM_GROUP_CITY,
        display_name="Лавка портнихи",
        bg_picture="images/irma/portraits/portrait3.png",
        descriptions=[
            RoomDescription(
                text="Вы зашли в лавку очаровательной Ирмы. Ваш взгляд сразу падает на образцы платьев, костюмов, блузок, камзолов и прочей одежды, висящие вдоль стен - женские вдоль левой и мужские вдоль правой стены. На стеллажах, на полу, на полках лежат в одном хозяйке понятном порядке отрезы разноцветных тканей, рулоны кружев, мотки золоченой тесьмы и прочие полезные в хозяйстве портнихи вещи. В дальнем углу, за обширным столом, сидит сама мисс Фараго и",
                priority=100,
            ),
            RoomDescription(
                text="увлеченно кроит какой-то костюм.",
                condition=dress_shop_irma_working_idle,
                priority=90,
            ),
            RoomDescription(
                text="сосредоточенно работает над вашим заказом.",
                condition=dress_shop_irma_working_order,
                priority=90,
            ),
            RoomDescription(
                text="Сегодня здесь крутится и Кларисса Легаре: она перебирает отрезы ткани и вполголоса что-то обсуждает с Ирмой.",
                condition=dress_shop_clara_present,
                priority=80,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в квартал ремесленников", target="ArtisansQuarter", minutes_to_pass=10),
        ],
        game_items=[
            "female_samples_001",
            "male_samples_001",
            "worktable_001",
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            closed_text="В это время лавка закрыта.",
            start="06:00",
            end="17:59",
        ),
        custom_properties={
            "shop_feature": "tailor",
            "object_menu_label": "DressShopObjectMenu",
        },
    )
    def dress_shop_get_object(object_id):
        return get_game_object(object_id)

    def dress_shop_catalog_items(rack_type):
        return list(dress_shop_rack_items(rack_type))

    def dress_shop_room_action_items():
        return rooms.get("DressShop").build_object_items() + rooms.get("DressShop").build_exit_items()

    def dress_shop_buy_male_item(dress_code):
        code = str(dress_code or "").strip()
        if not code:
            return "invalid"
        if str(dress_shop.produced or "") != "":
            return "busy"
        item_obj = get_game_item("dress_" + code)
        if item_obj is None:
            return "invalid"
        if player.appearance.has_dress(code) and not dress_shop_item_depreciated(item_obj):
            return "owned"
        price = int(getattr(item_obj, "price", 0) or 0)
        if int(player.economy.money or 0) < price:
            return "no_money"
        player.spend_money(price)
        return "success"


init -5:
    style dress_shop_catalog_button is button:
        background Solid("#3d2919")
        hover_background Solid("#5a3a24")
        insensitive_background Solid("#8a7963")
        padding (14, 6)

    style dress_shop_catalog_button_text is button_text:
        size 18
        color "#f5ead3"
        hover_color "#ffffff"
        insensitive_color "#d2c5b0"


screen dress_shop_catalog_page(rack_type="male", girl_name=""):
    zorder 120
    default catalog_page = 0

    $ _rack_type = "female" if str(rack_type or "").strip().lower() == "female" else "male"
    $ _girl_name = str(girl_name or "").strip()
    $ _catalog_items = list(dress_shop_catalog_items(_rack_type) or [])
    $ _page_size = 3
    $ _page_count = max(1, (len(_catalog_items) + _page_size - 1) // _page_size)
    $ _current_page = max(0, min(int(catalog_page or 0), _page_count - 1))
    $ _page_start = _current_page * _page_size
    $ _page_items = _catalog_items[_page_start:_page_start + _page_size]
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24
    $ _catalog_title = "ЖЕНСКИЕ ПЛАТЬЯ" if _rack_type == "female" else "МУЖСКИЕ КОСТЮМЫ"
    if _rack_type == "female" and _girl_name:
        $ _catalog_intro = "Выберите одежду, которую хотите предложить %s." % people_name(_girl_name, "dative")
    else:
        $ _catalog_intro = "Образцы женской одежды с левой стены лавки." if _rack_type == "female" else "Костюмы и камзолы с правой стены лавки."

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add Transform("images/rpg_message_bg.png", fit="cover")

        vbox:
            xpos 28
            ypos 22
            xsize _left_w - 56
            ysize _left_h - 44
            spacing 10

            text _catalog_title size 30 color "#1e130c" xalign 0.5
            text _catalog_intro size 17 color "#5a3a24" xalign 0.5

            for _dress_item in _page_items:
                $ _dress_code = dress_shop_item_code(_dress_item)
                $ _dress_name = str(getattr(_dress_item, "name", "") or _dress_code)
                $ _dress_desc = str(getattr(_dress_item, "description", "") or "")
                $ _dress_price = int(getattr(_dress_item, "price", 0) or 0)

                frame:
                    xfill True
                    yminimum 168
                    padding (14, 10)
                    background Solid("#f5ead3d9")

                    hbox:
                        xfill True
                        spacing 18

                        vbox:
                            xmaximum _left_w - 320
                            spacing 5
                            text _dress_name size 23 color "#1e130c"
                            text _dress_desc size 16 color "#2d1d12"

                        vbox:
                            xminimum 205
                            spacing 8
                            text "[_dress_price] мараведи" size 20 color "#1e130c" xalign 0.5

                            if _rack_type == "male":
                                if dress_shop_item_owned(_dress_item):
                                    text "Уже куплено" size 17 color "#5a3a24" xalign 0.5
                                elif str(dress_shop.produced or "") != "":
                                    text "Ирма занята заказом" size 17 color "#5a3a24" xalign 0.5
                                else:
                                    textbutton "Купить":
                                        id "dress_shop_catalog_buy_" + _dress_code
                                        alt "dress_shop_catalog_buy_" + _dress_code
                                        style "dress_shop_catalog_button"
                                        text_style "dress_shop_catalog_button_text"
                                        xalign 0.5
                                        sensitive dress_shop_can_buy_item(_dress_item)
                                        action Call("DressShopBuyMaleItem", _dress_code)
                            else:
                                $ _girl_has_dress = bool(_girl_name) and _gds_has_dress_for_girl(_girl_name, _dress_code)
                                $ _female_can_offer = bool(_girl_name) and not _girl_has_dress and str(dress_shop.produced or "") == "" and int(dress_shop.girl_dress_block or 0) == 0 and _dress_price <= int(player.economy.money or 0)

                                textbutton "Выбрать":
                                    id "dress_shop_catalog_offer_" + _dress_code
                                    alt "dress_shop_catalog_offer_" + _dress_code
                                    style "dress_shop_catalog_button"
                                    text_style "dress_shop_catalog_button_text"
                                    xalign 0.5
                                    sensitive _female_can_offer
                                    action ([Hide("dress_shop_catalog_page"), Call("GirlDressSuggest", _girl_name, _dress_code)] if _girl_name else NullAction())

                                if not _girl_name:
                                    text "Выбор доступен при совместном визите" size 15 color "#5a3a24" xalign 0.5 text_align 0.5
                                elif _girl_has_dress:
                                    text "Уже куплено" size 15 color "#5a3a24" xalign 0.5
                                elif str(dress_shop.produced or "") != "":
                                    text "Ирма занята заказом" size 15 color "#5a3a24" xalign 0.5
                                elif int(dress_shop.girl_dress_block or 0) != 0:
                                    text "Выбор закрыт" size 15 color "#5a3a24" xalign 0.5
                                elif _dress_price > int(player.economy.money or 0):
                                    text "Не хватает денег" size 15 color "#5a3a24" xalign 0.5

            null yfill True

            hbox:
                xalign 0.5
                spacing 18

                textbutton "<":
                    id "dress_shop_catalog_previous"
                    alt "dress_shop_catalog_previous"
                    style "dress_shop_catalog_button"
                    text_style "dress_shop_catalog_button_text"
                    sensitive _current_page > 0
                    action SetScreenVariable("catalog_page", _current_page - 1)

                text "Страница [_current_page + 1] из [_page_count]" size 19 color "#1e130c" yalign 0.5

                textbutton ">":
                    id "dress_shop_catalog_next"
                    alt "dress_shop_catalog_next"
                    style "dress_shop_catalog_button"
                    text_style "dress_shop_catalog_button_text"
                    sensitive _current_page + 1 < _page_count
                    action SetScreenVariable("catalog_page", _current_page + 1)

label DressShop:
    hide screen dress_shop_catalog_page
    show screen main_ui
    $ rooms.enter("DressShop")
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.object_id = ""
    $ dress_shop.girl_dress_block = 0
    call RoomEnterEventGate(rooms.current_code, False)

    if not rooms.get("DressShop").is_open():
        $ scene_runtime.text = rooms.get("DressShop").schedule.closed_text
        $ scene_runtime.location_text = scene_runtime.text
        $ scene_runtime.picture = ""
        $ main_ui_runtime.action_items = rooms.get("DressShop").build_exit_items()
        while True:
            call screen main_ui

    $ scene_runtime.text = dress_shop_room_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ scene_runtime.picture = ""

    if renpy.has_label("check_daily_event") and int(calendar_v2.hour or 0) < 12:
        call check_daily_event("", "BuyDress", "DressShop", 0)

    $ main_ui_runtime.action_items = rooms.get("DressShop").build_object_items() + rooms.get("DressShop").build_exit_items()
    while True:
        call screen main_ui


label DressShopOpenCatalog(rack_type=""):
    $ renpy.dynamic("_rack_type", "_rack_object")
    $ _rack_type = str(rack_type or "")
    if _rack_type not in ("female", "male"):
        return

    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_title = "Женские платья" if _rack_type == "female" else "Мужские костюмы"
    $ main_ui_runtime.object_id = "female_samples_001" if _rack_type == "female" else "male_samples_001"
    $ _rack_object = dress_shop_get_object(main_ui_runtime.object_id)
    $ scene_runtime.text = str(getattr(_rack_object, "description", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = [
        MenuItem("Назад", [
            Hide("dress_shop_catalog_page"),
            SetField(main_ui_runtime, "object_id", ""),
            SetField(main_ui_runtime, "action_title", "Действия"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", dress_shop_room_action_items()),
            SetField(scene_runtime, "picture", ""),
            SetField(scene_runtime, "text", dress_shop_room_text()),
            SetField(scene_runtime, "location_text", dress_shop_room_text()),
            Function(main_ui_restart_interaction),
        ]),
    ]
    show screen dress_shop_catalog_page(rack_type=_rack_type)
    return


label DressShopBuyMaleItem(dress_code=""):
    $ renpy.dynamic("_dress_code", "_buy_result")
    $ _dress_code = str(dress_code or "")
    $ _buy_result = dress_shop_buy_male_item(_dress_code)
    if _buy_result != "success":
        if _buy_result == "busy":
            $ scene_runtime.text = "Ирма сейчас уже работает над вашим заказом."
        elif _buy_result == "owned":
            $ scene_runtime.text = "Этот костюм уже лежит среди вашей одежды."
        elif _buy_result == "no_money":
            $ scene_runtime.text = "У вас не хватает денег на этот костюм."
        else:
            $ scene_runtime.text = "Вы не выбрали костюм."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Мужские костюмы"
        $ main_ui_runtime.object_id = "male_samples_001"
        show screen dress_shop_catalog_page(rack_type="male")
        return

    hide screen dress_shop_catalog_page
    $ main_ui_runtime.object_id = ""
    call DressTry("You", _dress_code)
    jump ArtisansQuarter

label DressShopObjectMenu(object_id=""):
    $ renpy.dynamic("_room_object")
    $ renpy.dynamic("_menu_item", "_room_action")
    $ _room_object = dress_shop_get_object(object_id)
    if _room_object is None:
        return

    $ scene_runtime.text = _room_object.description
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = _room_object.name
    $ main_ui_runtime.object_id = object_id
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []

    python:
        for _room_action in _room_object.visible_actions():
            _menu_item = room_action_menu_item(_room_action)
            if _menu_item is not None:
                main_ui_runtime.action_items.append(_menu_item)

    $ main_ui_runtime.action_items.append(MenuItem("Назад", [SetField(scene_runtime, "picture", ""), SetField(scene_runtime, "text", dress_shop_room_text()), SetField(scene_runtime, "location_text", dress_shop_room_text()), SetField(main_ui_runtime, "action_title", "Действия"), SetField(main_ui_runtime, "object_id", ""), SetField(main_ui_runtime, "action_content", None), SetField(main_ui_runtime, "action_items", dress_shop_room_action_items()), Function(main_ui_restart_interaction)]))
    return
