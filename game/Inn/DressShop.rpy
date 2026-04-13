default DressShopCatalogRack = ""
default DressShopCatalogDressCode = ""
default DressShopMaleCatalogItemIds = []
default DressShopFemaleCatalogItemIds = []
default DressShopSavedText = ""

init python:
    def dress_shop_irma_visible():
        return True

    def dress_shop_clara_visible():
        return clara_visible_in_location("DressShop")

    DressShopRoom = Room(
        code_name="DressShop",
        display_name="Лавка портнихи",
        bg_picture="images/irma/Irma_working_portrait.png",
        descriptions=[
            RoomDescription(
                text="Вы зашли в лавку очаровательной Ирмы. Ваш взгляд сразу падает на образцы платьев, костюмов, блузок, камзолов и прочей одежды, висящие вдоль стен - женские вдоль левой и мужские вдоль правой стены. На стеллажах, на полу, на полках лежат в одном хозяйке понятном порядке отрезы разноцветных тканей, рулоны кружев, мотки золоченой тесьмы и прочие полезные в хозяйстве портнихи вещи. В дальнем углу, за обширным столом, сидит сама мисс Фараго и",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в квартал ремесленников", target="ArtisansQuarter"),
        ],
        game_items=[
            "female_samples_001",
            "male_samples_001",
            "worktable_001",
        ],
        npcs=[
            {"npc_id": "irma", "name": "Ирма", "condition": dress_shop_irma_visible, "talk_label": "IntIrmaTalk"},
            {"npc_id": "clara", "name": "Кларисса", "condition": dress_shop_clara_visible, "talk_label": "IntClaraTalk"},
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            time_slots=[0, 1, 2],
            closed_text="В это время лавка закрыта.",
        ),
        custom_properties={
            "shop_feature": "tailor",
            "object_menu_label": "DressShopObjectMenu",
        },
    )

    def dress_shop_get_object(object_id):
        return get_game_object(object_id)

    def dress_shop_sync_catalog_lists():
        male_ids = [
            str(getattr(item, "object_id", "") or "")
            for item in list(dress_shop_rack_items("male"))
            if str(getattr(item, "object_id", "") or "")
        ]
        female_ids = [
            str(getattr(item, "object_id", "") or "")
            for item in list(dress_shop_rack_items("female"))
            if str(getattr(item, "object_id", "") or "")
        ]

        if isinstance(getattr(DressShopRoom, "custom_properties", None), dict):
            DressShopRoom.custom_properties["male_catalog_item_ids"] = list(male_ids)
            DressShopRoom.custom_properties["female_catalog_item_ids"] = list(female_ids)

        return male_ids, female_ids

    def dress_shop_catalog_ids(rack_type):
        if str(rack_type or "") == "female":
            return list(DressShopFemaleCatalogItemIds or [])
        return list(DressShopMaleCatalogItemIds or [])

    def dress_shop_catalog_items(rack_type):
        items = []
        female_rack = str(rack_type or "") == "female"
        for item_id in dress_shop_catalog_ids(rack_type):
            item_obj = dress_shop_get_item(item_id, female_rack)
            if item_obj is not None:
                items.append(item_obj)
        return items

    def dress_shop_catalog_name(dress_code):
        code = str(dress_code or "").strip()
        return str(ShortDressName.get(code, code))

    def dress_shop_catalog_desc(dress_code):
        code = str(dress_code or "").strip()
        return str(FullDressDesc.get(code, code))

    def dress_shop_catalog_price(dress_code):
        code = str(dress_code or "").strip()
        return int(DressCost.get(code, 0) or 0)

    def dress_shop_catalog_owned(dress_code):
        code = str(dress_code or "").strip()
        return code in list(MyDresses)

    def dress_shop_catalog_can_buy_male(dress_code):
        code = str(dress_code or "").strip()
        if not code:
            return False
        if str(DressProduced or "") != "":
            return False
        if dress_shop_catalog_owned(code):
            return False
        return int(money or 0) >= dress_shop_catalog_price(code)

    def dress_shop_catalog_title(rack_type):
        return "Женские образцы" if str(rack_type or "") == "female" else "Мужские костюмы"

    def dress_shop_catalog_picture():
        return "images/rpg_message_bg.png"

    def dress_shop_catalog_intro(rack_type):
        if str(rack_type or "") == "female":
            return "Вы рассматриваете образцы разнообразных платьев, юбок и блузок, развешанных вдоль левой стены."
        return "Вы рассматриваете мужские костюмы и камзолы, развешанные вдоль правой стены."

    def dress_shop_catalog_listing(rack_type):
        lines = [dress_shop_catalog_intro(rack_type), ""]
        for dress_item in dress_shop_catalog_items(rack_type):
            dress_name = str(getattr(dress_item, "name", "") or getattr(dress_item, "object_id", ""))
            dress_price = int(getattr(dress_item, "price", 0) or 0)
            lines.append(dress_name + " - " + str(dress_price) + " мараведи")
        return "\n".join(lines)


label DressShop:
    call EnterLocation("DressShop")
    $ DressShopMaleCatalogItemIds, DressShopFemaleCatalogItemIds = dress_shop_sync_catalog_lists()
    $ CurrentRoom = DressShopRoom
    $ CurLoc = "DressShop"
    $ location = CurLoc
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_object_id = ""
    $ GirlDressBlock = 0

    if not DressShopRoom.is_open(week, time):
        $ MainTxt = DressShopRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        call ShowImageSeq("general", "", "LocArtisansQuarter", 4)
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        jump DressShopView

    $ MainTxt = DressShopRoom.descriptions[0].text
    if str(DressProduced or "") == "":
        $ MainTxt += "\n\nувлеченно кроит какой-то костюм."
    else:
        $ MainTxt += "\n\nсосредоточенно работает над вашим заказом."
    if dress_shop_clara_visible():
        $ MainTxt += "\n\nСегодня здесь крутится и Кларисса Легаре: она перебирает отрезы ткани и вполголоса что-то обсуждает с Ирмой."
    $ CurLocDesc = MainTxt
    $ DressShopSavedText = MainTxt

    call ShowImage("", "", irma_working_picture_path())

    if renpy.has_label("CheckDailyEvent"):
        call CheckDailyEvent("", "BuyDress")

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        jump DressShopView

    call DressShopBuildActions
    jump DressShopView


label DressShopView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump DressShopView


label DressShopBuildActions:
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ DressShopCatalogRack = ""
    $ DressShopCatalogDressCode = ""
    $ current_action_items.append(MenuItem("Женские образцы", [Hide("dress_shop_male_catalog_overlay"), Call("DressShopOpenFemaleCatalog")]))
    $ current_action_items.append(MenuItem("Мужские образцы", [Hide("dress_shop_female_catalog_overlay"), Call("DressShopOpenMaleCatalog")]))
    $ current_action_items.append(MenuItem("Рабочий стол Ирмы", [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Call("DressShopOpenWorktable")]))
    $ current_action_items.append(MenuItem("Карточка Ирмы", [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Call("ShowGirlCard", "irma", "DressShopRestore")]))
    $ current_action_items.append(MenuItem("Поговорить с Ирмой", [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Call("IntIrmaTalk")]))
    python:
        for _room_exit in DressShopRoom.visible_exits():
            current_action_items.append(MenuItem(_room_exit.label, [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Jump(_room_exit.target)]))
    return


label DressShopOpenFemaleCatalog:
    call DressShopOpenCatalog("female")
    return


label DressShopOpenMaleCatalog:
    call DressShopOpenCatalog("male")
    return


label DressShopOpenCatalog(rack_type=""):
    $ DressShopCatalogRack = str(rack_type or "")
    if DressShopCatalogRack not in ("female", "male"):
        call DressShopBuildActions
        return

    $ DressShopMaleCatalogItemIds, DressShopFemaleCatalogItemIds = dress_shop_sync_catalog_lists()
    $ current_action_content = None
    $ DressShopCatalogDressCode = ""
    $ current_action_title = "Действия"
    $ MainTxt = DressShopSavedText
    $ CurLocDesc = MainTxt
    call ShowImage("", "", irma_working_picture_path())
    hide screen girl_card_overlay
    if DressShopCatalogRack == "female":
        show screen dress_shop_female_catalog_overlay
        hide screen dress_shop_male_catalog_overlay
    else:
        show screen dress_shop_male_catalog_overlay
        hide screen dress_shop_female_catalog_overlay
    return


label DressShopOpenWorktable:
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ _worktable = dress_shop_get_object("worktable_001")
    if _worktable is None:
        call DressShopBuildActions
        return

    $ current_action_title = str(_worktable.name or "Рабочий стол Ирмы")
    $ current_action_content = None
    $ MainTxt = str(_worktable.description or "")
    $ CurLocDesc = MainTxt
    call ShowImage("", "", irma_working_picture_path())
    $ current_action_items = []

    python:
        for _room_action in _worktable.visible_actions():
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("DressShopWorktableText", _room_action.action_id)))

    $ current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRestore")))
    return


label DressShopWorktableText(action_id=""):
    $ _worktable = dress_shop_get_object("worktable_001")
    if _worktable is None:
        call DressShopBuildActions
        return

    python:
        _worktable_text = ""
        for _room_action in _worktable.visible_actions():
            if str(getattr(_room_action, "action_id", "") or "") == str(action_id or ""):
                _worktable_text = str(getattr(_room_action, "target", "") or "")
                break
        if _worktable_text:
            MainTxt = _worktable_text
            CurLocDesc = _worktable_text

    call DressShopOpenWorktable
    return


label DressShopCatalogSelect(dress_code=""):
    $ DressShopCatalogDressCode = str(dress_code or "")
    if DressShopCatalogRack not in ("female", "male") or DressShopCatalogDressCode == "":
        call DressShopBuildActions
        return
    call DressShopCatalogShowSelected
    return


label DressShopCatalogShowSelected:
    return


label DressShopBuyMaleItem(dress_code=""):
    $ _dress_code = str(dress_code or "")
    if _dress_code == "":
        call DressShopOpenMaleCatalog
        return
    if not dress_shop_catalog_can_buy_male(_dress_code):
        $ DressShopCatalogRack = "male"
        call DressShopCatalogSelect(_dress_code)
        return

    $ money -= dress_shop_catalog_price(_dress_code)
    if money < 0:
        $ money = 0
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    hide screen main_ui
    call DressTry("You", _dress_code)
    return


label DressShopFemaleBuyInfo(dress_code=""):
    $ DressShopCatalogRack = "female"
    $ DressShopCatalogDressCode = str(dress_code or "")
    if str(DressShopCatalogDressCode or "") == "":
        call DressShopOpenFemaleCatalog
        return
    $ MainTxt = str(FullDressDesc.get(DressShopCatalogDressCode, DressShopCatalogDressCode))
    $ CurLocDesc = MainTxt
    return

label DressShopObjectMenu(object_id=""):
    $ _room_object = dress_shop_get_object(object_id)
    if _room_object is None:
        call DressShopBuildActions
        return
    $ _rack_type = str(getattr(_room_object, "custom_properties", {}).get("rack_type", "") or "")
    if _rack_type in ("female", "male"):
        call DressShopOpenCatalog(_rack_type)
        return

    $ MainTxt = _room_object.description
    $ CurLocDesc = MainTxt
    $ current_action_title = _room_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("DressShopObjectText", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                _room_args = tuple(getattr(_room_action, "args", ()) or ())
                current_action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("DressShopRestore")))
    return


label DressShopObjectText(object_id="", action_id=""):
    python:
        _dress_text = ""
        _dress_name = ""
        _room_object = dress_shop_get_object(object_id)
        if _room_object is not None:
            _dress_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _dress_text = str(_room_action.target or "")
                    break
        if _dress_text:
            MainTxt = _dress_text
            CurLocDesc = _dress_text
            current_action_title = _dress_name or "Действия"
    call DressShopObjectMenu(object_id)
    return


label DressShopItemMenu(parent_object_id="", item_id=""):
    $ _parent_object = dress_shop_get_object(parent_object_id)
    if _parent_object is None:
        call DressShopBuildActions
        return

    $ _female_rack = str(getattr(_parent_object, "custom_properties", {}).get("rack_type", "") or "") == "female"
    $ _dress_item = dress_shop_get_item(item_id, _female_rack)
    if _dress_item is None:
        call DressShopObjectMenu(parent_object_id)
        return

    $ _dress_price = int(getattr(_dress_item, "price", 0) or 0)
    $ MainTxt = str(_dress_item.description or "") + "\n\nЦена: " + str(_dress_price) + " мараведи."
    $ CurLocDesc = MainTxt
    $ current_action_title = _dress_item.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _item_action in _dress_item.visible_actions():
            if _item_action.hook == "text":
                current_action_items.append(MenuItem(_item_action.label, Call("DressShopItemText", parent_object_id, item_id, _item_action.action_id)))
            elif _item_action.hook == "call" and str(_item_action.target or "") != "":
                current_action_items.append(MenuItem(_item_action.label, Call("DressShopItemAction", parent_object_id, item_id, _item_action.action_id)))
            elif _item_action.hook == "jump" and str(_item_action.target or "") != "":
                current_action_items.append(MenuItem(_item_action.label, Jump(_item_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("DressShopObjectMenu", parent_object_id)))
    return


label DressShopItemText(parent_object_id="", item_id="", action_id=""):
    $ _parent_object = dress_shop_get_object(parent_object_id)
    if _parent_object is None:
        call DressShopBuildActions
        return
    $ _female_rack = str(getattr(_parent_object, "custom_properties", {}).get("rack_type", "") or "") == "female"
    $ _dress_item = dress_shop_get_item(item_id, _female_rack)
    if _dress_item is None:
        call DressShopObjectMenu(parent_object_id)
        return

    python:
        _item_text = ""
        for _item_action in _dress_item.visible_actions():
            if getattr(_item_action, "action_id", "") == str(action_id or ""):
                _item_text = str(_item_action.target or "")
                break
        if _item_text:
            MainTxt = _item_text
            CurLocDesc = _item_text
    call DressShopItemMenu(parent_object_id, item_id)
    return


label DressShopItemAction(parent_object_id="", item_id="", action_id=""):
    $ _parent_object = dress_shop_get_object(parent_object_id)
    if _parent_object is None:
        call DressShopBuildActions
        return
    $ _female_rack = str(getattr(_parent_object, "custom_properties", {}).get("rack_type", "") or "") == "female"
    $ _dress_item = dress_shop_get_item(item_id, _female_rack)
    if _dress_item is None:
        call DressShopObjectMenu(parent_object_id)
        return

    python:
        _item_target = ""
        _dress_code = str(getattr(_dress_item, "custom_properties", {}).get("dress_code", "") or "")
        for _item_action in _dress_item.visible_actions():
            if getattr(_item_action, "action_id", "") == str(action_id or ""):
                _item_target = str(_item_action.target or "")
                break

    if _item_target != "":
        call expression _item_target pass (_dress_code,)
    return


label DressShopRestore:
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ MainTxt = DressShopSavedText
    $ CurLocDesc = MainTxt
    $ current_action_content = None
    call ShowImage("", "", irma_working_picture_path())
    call DressShopBuildActions
    return


screen dress_shop_male_catalog_overlay():
    zorder 120

    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add im.Scale("images/rpg_message_bg.png", _left_w, _left_h)

        viewport:
            xpos 28
            ypos 24
            xsize _left_w - 56
            ysize _left_h - 48
            draggable True
            mousewheel True

            vbox:
                spacing 16

                text "МУЖСКИЕ КОСТЮМЫ" size 30 color "#1e130c" xalign 0.5

                for _dress_item in dress_shop_catalog_items("male"):
                    $ _dress_code = str(_dress_item.custom_properties.get("dress_code", "") or "")
                    $ _dress_desc = dress_shop_catalog_desc(_dress_code)
                    $ _dress_price = dress_shop_catalog_price(_dress_code)

                    hbox:
                        spacing 20

                        vbox:
                            xmaximum int((_left_w - 260) * 0.72)
                            spacing 4
                            text str(_dress_item.name or _dress_code) size 24 color "#1e130c"
                            text _dress_desc size 18 color "#2d1d12"

                        vbox:
                            xminimum 170
                            spacing 8
                            text str(_dress_price) + " мараведи" size 20 color "#1e130c" xalign 0.5
                            if dress_shop_catalog_owned(_dress_code):
                                text "Уже куплено" size 18 color "#5a3a24" xalign 0.5
                            else:
                                textbutton "Купить":
                                    text_size 20
                                    sensitive dress_shop_catalog_can_buy_male(_dress_code)
                                    action Call("DressShopBuyMaleItem", _dress_code)

                textbutton "Назад в лавку":
                    text_size 22
                    action Call("DressShopRestore")


screen dress_shop_female_catalog_overlay():
    zorder 120

    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add im.Scale("images/rpg_message_bg.png", _left_w, _left_h)

        viewport:
            xpos 28
            ypos 24
            xsize _left_w - 56
            ysize _left_h - 48
            draggable True
            mousewheel True

            vbox:
                spacing 16

                text "ЖЕНСКИЕ ПЛАТЬЯ" size 30 color "#1e130c" xalign 0.5

                for _dress_item in dress_shop_catalog_items("female"):
                    $ _dress_code = str(_dress_item.custom_properties.get("dress_code", "") or "")
                    $ _dress_desc = dress_shop_catalog_desc(_dress_code)
                    $ _dress_price = dress_shop_catalog_price(_dress_code)

                    hbox:
                        spacing 20

                        vbox:
                            xmaximum int((_left_w - 260) * 0.72)
                            spacing 4
                            text str(_dress_item.name or _dress_code) size 24 color "#1e130c"
                            text _dress_desc size 18 color "#2d1d12"

                        vbox:
                            xminimum 170
                            spacing 8
                            text str(_dress_price) + " мараведи" size 20 color "#1e130c" xalign 0.5
                            textbutton "Подробнее":
                                text_size 20
                                action Call("DressShopFemaleBuyInfo", _dress_code)

                textbutton "Назад в лавку":
                    text_size 22
                    action Call("DressShopRestore")
