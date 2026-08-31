# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def girl_dress_buy_actions(girl_name):
        options = [
            MenuItem("Осмотреть портниху", Call("GirlsDesc", "irma")),
            MenuItem("Посмотреть во что одета " + str(people_display_name(girl_name)), Call("GirlsDesc", girl_name)),
        ]

        options.append(MenuItem("Уйти из лавки", Call("GirlDressBuyLeave", girl_name)))
        return options


label GirlDressBuy(GirlName="", CurLocArg=""):
    $ renpy.dynamic("_girl_dress_buy_args", "_rn", "_rn3")
    if str(GirlName or "") == "":
        python:
            _girl_dress_buy_args = _args if isinstance(_args, (list, tuple)) else ()
            if len(_girl_dress_buy_args) > 0:
                GirlName = str(_girl_dress_buy_args[0] or "")
    if str(GirlName or "") == "":
        return

    hide screen dress_shop_catalog_page
    $ _gds_ensure_stats(GirlName)
    $ _gds_ensure_stats("irma")

    $ player.appearance.girl_dresses_bought = 0
    $ dress_shop.girl_dress_block = 0

    $ daily_events.delete(GirlName, "DressNoShow", "")

    $ _rn = people_display_name(GirlName)
    $ _rn3 = people_name(GirlName, 'dative')

    $ scene_runtime.text = "Вы зашли в лавку очаровательной Ирмы. Там вас уже ожидала %s. Она обрадованно улыбнулась, увидев вас, и сразу же вернулась к рассматриванию образцов разнообразных платьев, юбок и блузок, развешанных вдоль левой стены. Вы тоже можете на них поглазеть. Ну а если вы наконец определились с выбором, то можете предложить %s примерить и заказать одно из платьев." % (people_display_name(GirlName), people_name(GirlName, 'dative'))
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    call ShowImage("", "", irma_working_picture_path())
    $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
    show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
    while True:
        call screen main_ui


label GirlDressBuyLeave(GirlName=""):
    $ renpy.dynamic("_rn")
    hide screen dress_shop_catalog_page
    $ _rn = people_display_name(GirlName)
    if int(player.appearance.girl_dresses_bought or 0) <= 0:
        $ scene_runtime.text = "Осмотрев предлагаемый товар и обратив особое внимание на цены, вы буркнули: \"Покупать нечего, зайдем в другой раз!\" и бодро направились к выходу.\n\n%s ваше мнение, судя по всему, не разделяла и попыталась вас остановить: \"Стефан, давай еще посмотрим, ты же обещал мне что-нибудь купить!\"" % str(_rn)
        $ scene_runtime.location_text = scene_runtime.text
        $ dress_shop.girl_dress_block = 1
        $ main_ui_runtime.action_title = "Ответить"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = [
            MenuItem("Ну мало ли что на ком и где я обещал!", Call("GirlDressBuyRefuse", GirlName)),
            MenuItem("Ну если ты так считаешь...", Call("GirlDressBuyContinue", GirlName)),
        ]
        return

    $ scene_runtime.text = "\"Ну, хорошенького понемножку,\" сказали вы и пошли к выходу. %s же осталась в магазине, пощебетать еще немножко, всего полчасика или часик, с Ирмой о купленной обновке." % str(_rn)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [MenuItem("Выйти из лавки", Jump("ArtisansQuarter"))]
    return


label GirlDressBuyRefuse(GirlName=""):
    hide screen dress_shop_catalog_page
    $ household_cancel_outfit_request(GirlName)
    "\"Я же сказал, смотреть здесь не на что, покупать нечего, цены запре.., да не в ценах дело, просто выбор убогий!\" назидательно сказали вы и вышли на улицу."
    call SlutFriendsIncrease("irma", 0, 2, -1, 0, 0, 0)
    call SlutFriendsIncrease(GirlName, 5, 1, -1, 0, 0, 0)
    jump ArtisansQuarter


label GirlDressBuyContinue(GirlName=""):
    "Вы решили не обманывать надежды и вернулись к осмотру одеяний."
    $ dress_shop.girl_dress_block = 0
    $ main_ui_runtime.action_items = girl_dress_buy_actions(GirlName)
    show screen dress_shop_catalog_page(rack_type="female", girl_name=GirlName)
    return
