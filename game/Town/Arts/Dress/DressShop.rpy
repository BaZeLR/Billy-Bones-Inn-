    hide screen girl_card_overlay    hide screen girl_card_overlay        hide screen girl_card_overlay    hide screen girl_card_overlay    hide screen girl_card_overlay    hide screen girl_card_overlay        hide screen girl_card_overlay    hide screen girl_card_overlay    hide screen girl_card_overlay    hide screen girl_card_overlay        hide screen girl_card_overlay    hide screen girl_card_overlay# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default DressProduced = ""
default DressBuyer = ""
default IrmaMeasureShopStage = 0
default IrmaSexShopStep = 0

init python:
    def dress_shop_irma_working_idle():
        return str(DressProduced or "") == ""

    def dress_shop_irma_working_order():
        return str(DressProduced or "") != ""

    def dress_shop_clara_present():
        return str(getLocation("clara") or "") == "DressShop"

    DressShopRoom = Room(
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



default dress_shop = DressShopRuntimeState()



default dress_shop = DressShopRuntimeState()

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

    def dress_shop_buy_male_item(dress_code):
        global money
        global money
        global money
        code = str(dress_code or "").strip()
        if not code:
            return "invalid"
        if str(DressProduced or "") != "":
            return "busy"
        item_obj = get_game_item("dress_" + code)
        if item_obj is None:
            return "invalid"
        if player.appearance.has_dress(code) and not dress_shop_item_depreciated(item_obj):
            return "owned"
        price = int(getattr(item_obj, "price", 0) or 0)
        if int(money or 0) < price:
            return "no_money"
        money = max(0, int(money or 0) - price)
        return "success"

label DressShop:
    $ CurrentRoom = DressShopRoom
    $ CurLoc = "DressShop"
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_object_id = ""
    $ GirlDressBlock = 0
    call RoomEnterEventGate(CurLoc, False)

    if not DressShopRoom.is_open():
        $ MainTxt = DressShopRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ scene_image = build_media_ref("general", "", "LocArtisansQuarter" + str(procedural_randint(1, 4, key="procedural:Town/Arts/Dress/DressShop.rpy:procedural_randint:120:1")))
        $ _layout_last_picture = ""
        $ current_action_items = DressShopRoom.build_exit_items()
        while True:
            call screen main_ui

    $ MainTxt = "\n\n".join([row.text for row in DressShopRoom.visible_descriptions()])
    $ CurLocDesc = MainTxt
    $ scene_image = CurrentRoom.bg_picture
    $ _layout_last_picture = ""

    if renpy.has_label("CheckDailyEvent") and int(calendar_v2.hour or 0) < 12:
        call check_daily_event("", "BuyDress", "DressShop", 0)

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = DressShopRoom.build_exit_items()
    else:
        if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = DressShopRoom.build_exit_items()
    else:
        if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = DressShopRoom.build_exit_items()
    else:
        $ current_action_items = DressShopRoom.build_object_items() + DressShopRoom.build_exit_items()
    while True:
        call screen main_ui


label DressShopOpenCatalog(rack_type=""):
    $ _rack_type = str(rack_type or "")
    if _rack_type not in ("female", "male"):
        if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = DressShopRoom.build_exit_items()
        $ _dress_ui_return = None
        while _dress_ui_return is None:
            call screen main_ui
            $ _dress_ui_return = _return
        jump DressShop

    call DressShopRoomActions
        call DressShopRoomActions
        if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = DressShopRoom.build_exit_items()
        $ _dress_ui_return = None
        while _dress_ui_return is None:
            call screen main_ui
            $ _dress_ui_return = _return
        jump DressShop

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = DressShopRoom.build_exit_items()
        $ _dress_ui_return = None
        while _dress_ui_return is None:
            call screen main_ui
            $ _dress_ui_return = _return
        jump DressShop

    call DressShopRoomActions
        return

    $ dress_shop_populate_rack_contents()
    $ current_action_content = None
    $ current_action_title = "Действия"
    $ current_object_id = "female_samples_001" if _rack_type == "female" else "male_samples_001"
    $ _rack_object = dress_shop_get_object(current_object_id)
    $ MainTxt = str(getattr(_rack_object, "description", "") or "")
    $ CurLocDesc = MainTxt
    if _rack_type == "female":
        show screen dress_shop_female_catalog_overlay
        hide screen dress_shop_male_catalog_overlay
    else:
        show screen dress_shop_male_catalog_overlay
        hide screen dress_shop_female_catalog_overlay
    return


label DressShopBuyMaleItem(dress_code=""):
    $ _dress_code = str(dress_code or "")
    $ _buy_result = dress_shop_buy_male_item(_dress_code)
    if _buy_result != "success":
        if _buy_result == "busy":
            $ MainTxt = "Ирма сейчас уже работает над вашим заказом."
        elif _buy_result == "owned":
            $ MainTxt = "Этот костюм уже лежит среди вашей одежды."
        elif _buy_result == "no_money":
            $ MainTxt = "У вас не хватает денег на этот костюм."
        else:
            $ MainTxt = "Вы не выбрали костюм."
        $ CurLocDesc = MainTxt
        $ current_action_content = None
        $ current_action_title = "Действия"
        $ current_object_id = "male_samples_001"
        hide screen dress_shop_female_catalog_overlay
        show screen dress_shop_male_catalog_overlay
        return

    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    $ current_object_id = ""
    call DressTry("You", _dress_code)
    return


label DressShopFemaleBuyInfo(dress_code=""):
    $ _dress_code = str(dress_code or "")
    if _dress_code == "":
        call DressShopOpenCatalog("female")
        return
    $ _dress_item = get_game_item("dress_" + _dress_code)
    $ MainTxt = str(getattr(_dress_item, "description", _dress_code) or _dress_code)
    $ CurLocDesc = MainTxt
    return

label DressShopObjectMenu(object_id=""):
    $ _room_object = dress_shop_get_object(object_id)
    if _room_object is None:
        call DressShopRoomActions
        return

    $ MainTxt = _room_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _room_object.name
    $ current_object_id = object_id
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _room_action in _room_object.visible_actions():
            _menu_item = room_action_menu_item(_room_action)
            if _menu_item is not None:
                current_action_items.append(_menu_item)

    $ current_action_items.append(MenuItem("Назад", Call("DressShopRoomActions")))
    return
