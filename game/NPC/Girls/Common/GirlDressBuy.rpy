# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def girl_dress_buy_actions(girl_name):
        options = [
            MenuItem("Осмотреть портниху", Call("GirlsDesc", "irma")),
            MenuItem("Посмотреть во что одета " + str(_gds_name("RealName", girl_name)), Call("GirlsDesc", girl_name)),
        ]

        for dress_code in list(_gds_get_list("FemaleDressCodes")):
            code = str(dress_code or "").strip()
            if not code or code == "nightshirt":
                continue
            cost = _gds_dress_cost(code)
            has_dress = _gds_has_dress_for_girl(girl_name, code)
            if int(getattr(store, "money", 0) or 0) >= cost and (not has_dress) and str(getattr(store, "DressProduced", "") or "") == "" and int(getattr(store, "GirlDressBlock", 0) or 0) == 0:
                caption = "Заказать " + str(_gds_get_dict("ShortDressName").get(code, code)).lower()
                options.append(MenuItem(caption, Call("GirlDressSuggest", girl_name, code)))

        options.append(MenuItem("Уйти из лавки", Call("GirlDressBuyLeave", girl_name)))
        return options


label GirlDressBuy(GirlName="", CurLocArg=""):
    if str(GirlName or "") == "":
        python:
            _girl_dress_buy_args = _args if isinstance(_args, (list, tuple)) else ()
            if len(_girl_dress_buy_args) > 0:
                GirlName = str(_girl_dress_buy_args[0] or "")
    if str(GirlName or "") == "":
        return

    $ _gds_ensure_stats(GirlName)
    $ _gds_ensure_stats("irma")

    $ DressObman = _gds_get_dict("DressObman")
    $ DressObman[GirlName] = 0
    $ GirlDressesBought = 0
    $ GirlDressBlock = 0

    if renpy.has_label("delete_daily_event"):
        call delete_daily_event(GirlName, "DressNoShow", "")

    $ _rn = _gds_name("RealName", GirlName)
    $ _rn3 = _gds_name("RealName3", GirlName)

    call GirlDressBuyRefresh(GirlName)
    call screen main_ui
    jump GirlDressBuy


label GirlDressBuyRefresh(GirlName=""):
    hide screen dress_shop_male_catalog_overlay
    hide screen dress_shop_female_catalog_overlay
    hide screen girl_card_overlay
    $ UI_mode = "scene"
    $ CurLoc = "GirlDressBuy"
    $ location = CurLoc
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ MainTxt = "Вы зашли в лавку очаровательной Ирмы. Там вас уже ожидала [_gds_name('RealName', GirlName)]. Она обрадованно улыбнулась, увидев вас, и сразу же вернулась к рассматриванию образцов разнообразных платьев, юбок и блузок, развешанных вдоль левой стены. Вы тоже можете на них поглазеть. Ну а если вы наконец определились с выбором, то можете предложить [_gds_name('RealName3', GirlName)] примерить и заказать одно из платьев."
    $ CurLocDesc = MainTxt
    call ShowImage("", "", irma_working_picture_path())
    $ current_action_items = girl_dress_buy_actions(GirlName)
    return


label GirlDressBuyLeave(GirlName=""):
    $ _rn = _gds_name("RealName", GirlName)
    if int(GirlDressesBought or 0) <= 0:
        $ MainTxt = "Осмотрев предлагаемый товар и обратив особое внимание на цены, вы буркнули: \"Покупать нечего, зайдем в другой раз!\" и бодро направились к выходу.\n\n[_rn] ваше мнение, судя по всему, не разделяла и попыталась вас остановить: \"Стефан, давай еще посмотрим, ты же обещал мне что-нибудь купить!\""
        $ CurLocDesc = MainTxt
        $ GirlDressBlock = 1
        $ current_action_title = "Ответить"
        $ current_action_content = None
        $ current_action_items = [
            MenuItem("Ну мало ли что на ком и где я обещал!", Call("GirlDressBuyRefuse", GirlName)),
            MenuItem("Ну если ты так считаешь...", Call("GirlDressBuyContinue", GirlName)),
        ]
        return

    $ MainTxt = "\"Ну, хорошенького понемножку,\" сказали вы и пошли к выходу. [_rn] же осталась в магазине, пощебетать еще немножко, всего полчасика или часик, с Ирмой о купленной обновке."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Выйти из лавки", Jump("ArtisansQuarter"))]
    return


label GirlDressBuyRefuse(GirlName=""):
    "\"Я же сказал, смотреть здесь не на что, покупать нечего, цены запре.., да не в ценах дело, просто выбор убогий!\" назидательно сказали вы и вышли на улицу."
    call SlutFriendsIncrease("irma", 0, 2, -1, 0, 0, 0)
    call SlutFriendsIncrease(GirlName, 5, 1, -1, 0, 0, 0)
    jump ArtisansQuarter


label GirlDressBuyContinue(GirlName=""):
    "Вы решили не обманывать надежды и вернулись к осмотру одеяний."
    $ GirlDressBlock = 0
    call GirlDressBuyRefresh(GirlName)
    return
