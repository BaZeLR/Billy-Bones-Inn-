# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def dress_no_show_relation_type(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "sandra":
            return 1
        if girl in ("melissa", "amanda"):
            return 2
        return 0

    def dress_no_show_open_picture(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "amanda":
            ShowImage(girl, "tavern", "angry")
        elif girl == "becky":
            ShowImage(girl, "portraits", "portrait1")
        elif girl == "sandra":
            ShowImage(girl, "tavern", "cleaning1")
        elif girl == "melissa":
            ShowImage(girl, "tavern", "angry")
        elif girl == "georgett":
            ShowImage(girl, "portraits", "portrait3")

    def dress_no_show_title_address(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "sandra":
            return "Сандра"
        if girl == "amanda":
            return "Аманда"
        if girl == "melissa":
            return "Мелисса"
        return "дорогуша"

    def dress_no_show_soft_address(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "sandra":
            return "Сандра"
        if girl == "amanda":
            return "Аманда"
        if girl == "melissa":
            return "Мелисса"
        return "котеночек"


label DressNoShow(girl_name_dns):
    $ _dns_girl = str(girl_name_dns or "").strip().lower()
    if _dns_girl == "":
        return

    $ _dress_no_show_restore_ui = True if (CurrentRoom is not None or str(CurLoc or "") != "") else False
    $ DressBuyIsRelative = dress_no_show_relation_type(_dns_girl)
    $ _dns_real_name = RealName.get(_dns_girl, _dns_girl)
    $ _dns_real_name3 = RealName3.get(_dns_girl, _dns_real_name)
    $ dress_no_show_open_picture(_dns_girl)

    '"Ага!" воскликнула [_dns_real_name], едва завидев вас. "Явился значит! Мы где договаривались встретиться? Я тебя ждала, как дура, битый час под дверью, а ты шлялся незнамо где! Ну и нафига было предлагать мне обновку купить если ты даже зад свой от кровати не способен вовремя оторвать!'
    if DressBuyIsRelative == 1:
        extend ' Решил, значится, поиздеваться над Сандрой! Ну и характер же у тебя!"'
    elif DressBuyIsRelative == 2:
        extend ' Значит ты считаешь, что можешь глумиться надо мной как тебе угодно! Ну знаешь, Стефан!"'
    else:
        extend ' Связалась я с тобой, на свою голову! Думала ты и правда мне подарочек хочешь сделать, а ты, оказывается, только издевался!"'

    menu:
        "Что хочу, то и ворочу":
            '"Знаешь, что, [dress_no_show_title_address(_dns_girl)]?! Я своему слову хозяин. Захотел - позвал, захотел передумал! Я тебе подарок собирался купить, а не ты мне! Так что не надо мне тут ля-ля-тополя разводить. Не будешь тут мне надоедать, может опять передумаю и все-таки куплю тебе чего." гордо сказали вы. При этом вам почему-то пришло на ум странное слово ББПЕ. На секунду удивившись причудам памяти, вы продолжили гордиться твердостью занятой вами позиции.'
            '"Ты, ты, ты..." с трудом выдавила [_dns_real_name], пораженная вашим разумным, логичным и исполненным собственного достоинства ответом.'
            '"Ну и козел же ты!" продолжила она, подтверждая лишний раз ту простую истину, что женщинам недоступна логика, и отвернулась. Похоже, разговор с вами закончился.'
            $ slut_friends_increase(_dns_girl, 1, 1, -4, 0, 0, 0)
            jump DressNoShow_End

        "Извиниться":
            '"Ой, ты знаешь, [dress_no_show_soft_address(_dns_girl)], я забегался по делам и опоздал."'
            '"По каким-таким делам ты с утра пораньше бегал?" недоуменно ответила [_dns_real_name].'
            '"Да, надо было там сделать кое-что." туманно объяснили вы. "Прости, я виноват. Не дуйся."'
            if week != 6:
                '"Ну ладно, раз так, то давай будем считать, что мы перенесли наш поход на завтра," неожиданно ответила вам [_dns_real_name].'
            else:
                '"Ну ладно, раз так, то давай будем считать, что мы перенесли наш поход на понедельник," неожиданно ответила вам [_dns_real_name].'
            '"Ну давай," промямлили вы, будучи застигнутым врасплох таким оборотом дел.'
            '"Вот и ладушки, утром, как всегда!" сказала повеселевшая [_dns_real_name] и убежала.'
            $ DailyEventsList_Add(_dns_girl, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
            jump DressNoShow_End

        "Платить, но не каяться" if money > 50:
            '"Ой, ты знаешь, [dress_no_show_soft_address(_dns_girl)], я забегался по делам и опоздал, но не унывай, вот, деньги, которые я отложил для нашего похода за покупками."'
            'И с этими словами вы решительно вложили в руку [_dns_real_name3] 50 мараведи.'
            '"Зашиваюсь я с делами совсем, так что давай ты купишь себе что-нибудь сама, а я побежал. Хорошо?"'
            '"Ну ладно." [_dns_real_name] слегка повеселела.'
            $ slut_friends_increase(_dns_girl, 20, 2, 1, 0, 0, 0)
            $ money -= 50
            call stat
            jump DressNoShow_End


label DressNoShow_End:
    if _dress_no_show_restore_ui:
        show screen main_ui
    "Вот и поболтали."
    return
