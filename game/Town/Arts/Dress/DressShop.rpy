# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default DressShopCatalogRack = ""
default DressShopCatalogDressCode = ""
default DressShopMaleCatalogItemIds = []
default DressShopFemaleCatalogItemIds = []
default DressShopSavedText = ""
default IrmaMeasureShopStage = 0
default IrmaSexShopStep = 0

init python:
    DressShopRoom = Room(
        code_name="DressShop",
        group_name=ROOM_GROUP_CITY,
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
    call RoomEnterEventGate(CurLoc, False)

    if not DressShopRoom.is_open(week, time):
        $ MainTxt = DressShopRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        $ _layout_last_picture = build_media_ref("general", "", "LocArtisansQuarter" + str(renpy.random.randint(1, 4)))
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _dress_ui_return = None
        while _dress_ui_return is None:
            call screen main_ui
            $ _dress_ui_return = _return
        jump DressShop

    $ MainTxt = DressShopRoom.descriptions[0].text
    if str(DressProduced or "") == "":
        $ MainTxt += "\n\nувлеченно кроит какой-то костюм."
    else:
        $ MainTxt += "\n\nсосредоточенно работает над вашим заказом."
    if str(getLocation("clara") or "") == "DressShop":
        $ MainTxt += "\n\nСегодня здесь крутится и Кларисса Легаре: она перебирает отрезы ткани и вполголоса что-то обсуждает с Ирмой."
    $ CurLocDesc = MainTxt
    $ DressShopSavedText = MainTxt

    $ _layout_last_picture = irma_working_picture_path()

    if renpy.has_label("CheckDailyEvent"):
        call CheckDailyEvent("", "BuyDress")

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _dress_ui_return = None
        while _dress_ui_return is None:
            call screen main_ui
            $ _dress_ui_return = _return
        jump DressShop

    call DressShopBuildActions
    $ _dress_ui_return = None
    while _dress_ui_return is None:
        call screen main_ui
        $ _dress_ui_return = _return
    jump DressShop


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
    $ current_action_items.append(MenuItem("Примерочная Ирмы", [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Call("IrmaMeasureRoomMenu")]))
    $ current_action_items.append(MenuItem("Флиртовать с Ирмой", [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Call("IrmaShopFlirtScene")]))
    if str(getLocation("clara") or "") == "DressShop":
        $ current_action_items.append(MenuItem("Примерка Клариссы", [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Call("IrmaClaraFittingScene", 0)]))
    if str(DressProduced or "") != "":
        $ current_action_items.append(MenuItem("Спросить, когда будет готово", [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Call("DressShopAskReady")]))
    python:
        for _room_exit in DressShopRoom.visible_exits():
            current_action_items.append(MenuItem(_room_exit.label, [Hide("dress_shop_male_catalog_overlay"), Hide("dress_shop_female_catalog_overlay"), Jump(_room_exit.target)]))
    return


label DressShopAskReady:
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    "Вы осведомились у Ирмы, скоро ли будет готов ваш заказ."
    "Она подняла на вас удивленный взгляд и ответила, что, как она и говорила, закончит работу она к завтрашнему утру."
    call DressShopRestore
    return


label IrmaShopFlirtScene:
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ MainTxt = "Ирма отрывается от работы, одаривает вас внимательным взглядом и поправляет сантиметровую ленту на шее. Разговор быстро уходит от ткани, выкроек и ниток к намекам, в которых портниха чувствует себя не менее уверенно, чем за рабочим столом."
    $ CurLocDesc = MainTxt
    $ _layout_last_picture = irma_flirting_picture_path()
    $ current_action_title = "Ирма"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Поговорить с Ирмой", Call("IntIrmaTalk")),
        MenuItem("Примерочная Ирмы", Call("IrmaMeasureRoomMenu")),
        MenuItem("Назад в лавку", Call("DressShopRestore")),
    ]
    return


label IrmaMeasureRoomMenu:
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ IrmaMeasureShopStage = 0
    $ MainTxt = "За ширмой стоит узкая скамья, большое зеркало и манекен с наколотыми булавками лентами. Ирма держит мерную ленту наготове и предлагает выбрать, насколько тщательно снимать мерки."
    $ CurLocDesc = MainTxt
    $ _layout_last_picture = irma_measure_picture_path(0)
    $ current_action_title = "Примерочная Ирмы"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Обычные мерки", Call("IrmaMeasureRoomStage", 0)),
        MenuItem("Мерки в белье", Call("IrmaMeasureRoomStage", 1)),
        MenuItem("Белье и размышления", Call("IrmaMeasureRoomStage", 2)),
        MenuItem("Войти без одежды", Call("IrmaMeasureRoomStage", 3)),
        MenuItem("Назад в лавку", Call("DressShopRestore")),
    ]
    return


label IrmaMeasureRoomStage(stage=0):
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ IrmaMeasureShopStage = max(0, min(int(stage or 0), 3))
    $ _layout_last_picture = irma_measure_picture_path(IrmaMeasureShopStage)
    if IrmaMeasureShopStage == 0:
        $ MainTxt = "Ирма снимает обычные мерки быстро и профессионально: плечи, грудь, талия, длина рукавов. Ее пальцы едва касаются ткани, но ни одно движение не выглядит случайным."
    elif IrmaMeasureShopStage == 1:
        $ MainTxt = "Ирма просит убрать лишнюю одежду, чтобы посадка была точнее. В примерочной становится тише; слышно только, как скользит сантиметровая лента и как портниха негромко отмечает размеры."
    elif IrmaMeasureShopStage == 2:
        $ MainTxt = "Вы остаетесь в белье и стараетесь держаться спокойно, пока Ирма задумчиво сверяет мерки. Она смотрит то на ленту, то на зеркало, будто уже видит готовую вещь на теле."
    else:
        $ MainTxt = "В примерочную входят уже без лишней одежды. Ирма снимает последнюю, самую смелую мерку, задерживает взгляд и оставляет за вами выбор: закончить сцену сейчас или перейти к более смелому продолжению."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Примерочная Ирмы"
    $ current_action_content = None
    $ current_action_items = []
    if IrmaMeasureShopStage < 3:
        $ current_action_items.append(MenuItem("Следующая стадия", Call("IrmaMeasureRoomStage", IrmaMeasureShopStage + 1)))
    else:
        $ current_action_items.append(MenuItem("Продолжить за ширмой", Call("IrmaSexSequence", 0)))
    $ current_action_items.append(MenuItem("Выбрать другую стадию", Call("IrmaMeasureRoomMenu")))
    $ current_action_items.append(MenuItem("Закончить примерку", Call("IrmaMeasureEndScene")))
    $ current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRestore")))
    return


label IrmaMeasureEndScene:
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ MainTxt = "Ирма собирает ленты и булавки, снова превращаясь в деловую хозяйку лавки. Но на прощание она задерживает улыбку чуть дольше, чем требуется для простой вежливости."
    $ CurLocDesc = MainTxt
    $ _layout_last_picture = irma_shop_end_picture_path()
    $ current_action_title = "Ирма"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Поговорить с Ирмой", Call("IntIrmaTalk")),
        MenuItem("Примерочная Ирмы", Call("IrmaMeasureRoomMenu")),
        MenuItem("Назад в лавку", Call("DressShopRestore")),
    ]
    return


label IrmaSexSequence(step=0):
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ IrmaSexShopStep = int(step or 0)
    $ _layout_last_picture = irma_sex_picture_path(IrmaSexShopStep)
    if IrmaSexShopStep <= 0:
        $ MainTxt = "За ширмой Ирма уже не прячет интереса. Сцена начинается с осторожного, но явного приглашения продолжить примерку иначе."
    elif IrmaSexShopStep == 1:
        $ MainTxt = "Ирма подходит ближе, все еще сохраняя вид портнихи, которая просто проверяет посадку ткани."
    elif IrmaSexShopStep == 2:
        $ MainTxt = "Пауза тянется дольше обычного, и ее рабочая строгость постепенно сменяется откровенным любопытством."
    elif IrmaSexShopStep == 3:
        $ MainTxt = "Примерочная окончательно становится местом для игры, а не только для заказа одежды."
    elif IrmaSexShopStep == 4:
        $ MainTxt = "Ирма уверенно ведет сцену дальше, будто заранее знала, чем закончится такая примерка."
    elif IrmaSexShopStep == 5:
        $ MainTxt = "Все лишние слова уже сказаны; остается только следовать ритму, который задает портниха."
    elif IrmaSexShopStep == 6:
        $ MainTxt = "Сцена подходит к кульминации, и Ирма больше не пытается выглядеть равнодушной."
    elif IrmaSexShopStep == 8:
        $ MainTxt = "После горячего продолжения Ирма приводит себя в порядок и проверяет, не осталось ли следов на ткани."
    else:
        $ MainTxt = "Ирма возвращается к работе, но теперь примерочная кажется куда менее невинным местом, чем несколько минут назад."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ирма за ширмой"
    $ current_action_content = None
    $ current_action_items = []
    if IrmaSexShopStep == 0:
        $ current_action_items.append(MenuItem("Продолжить", Call("IrmaSexSequence", 1)))
    elif IrmaSexShopStep == 1:
        $ current_action_items.append(MenuItem("Продолжить", Call("IrmaSexSequence", 2)))
    elif IrmaSexShopStep == 2:
        $ current_action_items.append(MenuItem("Продолжить", Call("IrmaSexSequence", 3)))
    elif IrmaSexShopStep == 3:
        $ current_action_items.append(MenuItem("Продолжить", Call("IrmaSexSequence", 4)))
    elif IrmaSexShopStep == 4:
        $ current_action_items.append(MenuItem("Продолжить", Call("IrmaSexSequence", 5)))
    elif IrmaSexShopStep == 5:
        $ current_action_items.append(MenuItem("Продолжить", Call("IrmaSexSequence", 6)))
    elif IrmaSexShopStep == 6:
        $ current_action_items.append(MenuItem("Продолжить", Call("IrmaSexSequence", 8)))
    elif IrmaSexShopStep == 8:
        $ current_action_items.append(MenuItem("Завершить", Call("IrmaSexSequence", 9)))
    else:
        $ current_action_items.append(MenuItem("Закончить сцену", Call("IrmaMeasureEndScene")))
    $ current_action_items.append(MenuItem("Вернуться к примерке", Call("IrmaMeasureRoomMenu")))
    $ current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRestore")))
    return


label IrmaClaraFittingScene(stage=0):
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ _clara_fit_stage = max(0, min(int(stage or 0), 3))
    $ _layout_last_picture = irma_clara_fitting_picture_path(_clara_fit_stage)
    if str(getLocation("clara") or "") != "DressShop":
        $ MainTxt = "Клариссы сейчас нет в лавке, так что примерочная занята только тканями, манекенами и Ирмиными выкройками."
    elif _clara_fit_stage == 0:
        $ MainTxt = "Кларисса стоит у зеркала, пока Ирма прикладывает к ней тонкую ткань будущего белья и оценивает посадку."
    elif _clara_fit_stage == 1:
        $ MainTxt = "Ирма поправляет ленты и мерки, а Кларисса вполголоса спорит о том, насколько смело должна выглядеть новая вещь."
    elif _clara_fit_stage == 2:
        $ MainTxt = "Примерка превращается в оживленный разговор: Кларисса спрашивает совета, Ирма отвечает профессионально, но с заметной улыбкой."
    else:
        $ MainTxt = "Кларисса наконец соглашается с выбором Ирмы. Обе женщины выглядят довольными результатом, хотя разговор явно можно продолжить позже."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Примерка Клариссы"
    $ current_action_content = None
    $ current_action_items = []
    if str(getLocation("clara") or "") == "DressShop" and _clara_fit_stage < 3:
        $ current_action_items.append(MenuItem("Продолжить примерку", Call("IrmaClaraFittingScene", _clara_fit_stage + 1)))
    $ current_action_items.append(MenuItem("Поговорить с Ирмой", Call("IntIrmaTalk")))
    $ current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRestore")))
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
    $ _layout_last_picture = irma_working_picture_path()
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
    $ _layout_last_picture = irma_working_picture_path()
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
        current_action_title = str(_worktable.name or "Рабочий стол Ирмы")
        current_action_content = None
        _layout_last_picture = irma_working_picture_path()
        current_action_items = []
        for _room_action in _worktable.visible_actions():
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("DressShopWorktableText", _room_action.action_id)))
        current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRestore")))
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
        current_action_content = None
        current_action_items = []
        if _room_object is not None:
            for _room_action in _room_object.visible_actions():
                if _room_action.hook == "text":
                    current_action_items.append(MenuItem(_room_action.label, Call("DressShopObjectText", object_id, _room_action.action_id)))
                elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                    _room_args = tuple(getattr(_room_action, "args", ()) or ())
                    current_action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
                elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                    current_action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        current_action_items.append(MenuItem("Назад", Call("DressShopRestore")))
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
        current_action_title = _dress_item.name
        current_action_content = None
        current_action_items = []
        for _item_action in _dress_item.visible_actions():
            if _item_action.hook == "text":
                current_action_items.append(MenuItem(_item_action.label, Call("DressShopItemText", parent_object_id, item_id, _item_action.action_id)))
            elif _item_action.hook == "call" and str(_item_action.target or "") != "":
                current_action_items.append(MenuItem(_item_action.label, Call("DressShopItemAction", parent_object_id, item_id, _item_action.action_id)))
            elif _item_action.hook == "jump" and str(_item_action.target or "") != "":
                current_action_items.append(MenuItem(_item_action.label, Jump(_item_action.target)))
        current_action_items.append(MenuItem("Назад", Call("DressShopObjectMenu", parent_object_id)))
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
    $ _layout_last_picture = irma_working_picture_path()
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
