# ================================================================================
# Irma tailor interaction/event scenes.
# ================================================================================

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
        MenuItem("Назад в лавку", Call("DressShopRoomActions")),
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
        MenuItem("Назад в лавку", Call("DressShopRoomActions")),
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
    $ current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRoomActions")))
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
        MenuItem("Назад в лавку", Call("DressShopRoomActions")),
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
    $ current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRoomActions")))
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
    $ current_action_items.append(MenuItem("Назад в лавку", Call("DressShopRoomActions")))
    return
