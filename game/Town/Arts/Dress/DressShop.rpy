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

    def dress_shop_populate_rack_contents():
        male_items = list(dress_shop_rack_items("male"))
        female_items = list(dress_shop_rack_items("female"))

        male_rack = dress_shop_get_object("male_samples_001")
        if male_rack is not None:
            male_rack.contents = list(male_items)
        female_rack = dress_shop_get_object("female_samples_001")
        if female_rack is not None:
            female_rack.contents = list(female_items)

        return True

    def dress_shop_catalog_items(rack_type):
        rack_id = "female_samples_001" if str(rack_type or "") == "female" else "male_samples_001"
        rack_obj = dress_shop_get_object(rack_id)
        if rack_obj is None:
            return []
        return list(rack_obj.visible_contents())

    def dress_shop_catalog_action_items(rack_type):
        rack_key = str(rack_type or "").strip().lower()
        items = []
        for dress_item in dress_shop_catalog_items(rack_key):
            dress_code = str(dress_item.custom_properties.get("dress_code", "") or "")
            dress_name = str(dress_item.name or dress_code)
            dress_price = int(getattr(dress_item, "price", 0) or 0)
            if rack_key == "male":
                if dress_shop_item_owned(dress_item):
                    caption = "%s — уже куплено" % dress_name
                    action = NullAction()
                else:
                    caption = "%s — %s мараведи" % (dress_name, dress_price)
                    action = Call("DressShopBuyMaleItem", dress_code)
            else:
                caption = "%s — подробнее" % dress_name
                action = Call("DressShopFemaleBuyInfo", dress_code)
            items.append(MenuItem(caption, action))
        items.append(MenuItem("Назад в лавку", [
            SetField(main_ui_runtime, "object_id", ""),
            SetField(main_ui_runtime, "action_title", "Действия"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", dress_shop_room_action_items()),
            Function(main_ui_restart_interaction),
        ]))
        return items

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

label DressShop:
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

    $ scene_runtime.text = "\n\n".join([row.text for row in rooms.get("DressShop").visible_descriptions()])
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

    $ dress_shop_populate_rack_contents()
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_title = "Женские платья" if _rack_type == "female" else "Мужские костюмы"
    $ main_ui_runtime.object_id = "female_samples_001" if _rack_type == "female" else "male_samples_001"
    $ _rack_object = dress_shop_get_object(main_ui_runtime.object_id)
    $ scene_runtime.text = str(getattr(_rack_object, "description", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = dress_shop_catalog_action_items(_rack_type)
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
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_title = "Мужские костюмы"
        $ main_ui_runtime.object_id = "male_samples_001"
        $ main_ui_runtime.action_items = dress_shop_catalog_action_items("male")
        return

    $ main_ui_runtime.object_id = ""
    call DressTry("You", _dress_code)
    return


label DressShopFemaleBuyInfo(dress_code=""):
    $ renpy.dynamic("_dress_code", "_dress_item")
    $ _dress_code = str(dress_code or "")
    if _dress_code == "":
        call DressShopOpenCatalog("female")
        return
    $ _dress_item = get_game_item("dress_" + _dress_code)
    $ scene_runtime.text = str(getattr(_dress_item, "description", _dress_code) or _dress_code)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = dress_shop_catalog_action_items("female")
    return

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

    $ main_ui_runtime.action_items.append(MenuItem("Назад", [SetField(main_ui_runtime, "action_title", "Действия"), SetField(main_ui_runtime, "object_id", ""), SetField(main_ui_runtime, "action_content", None), SetField(main_ui_runtime, "action_items", dress_shop_room_action_items()), Function(main_ui_restart_interaction)]))
    return
