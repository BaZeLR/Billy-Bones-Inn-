# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntMelissaDressChange(GirlNameIMT="melissa"):
    call IntMelissaDressChangeRefresh(GirlNameIMT)
    return


label IntMelissaDressChangeRefresh(GirlNameIMT="melissa"):
    $ current_action_title = "Переодеть Мелиссу"
    $ current_action_content = None
    $ current_action_items = []
    $ _can_buy = int(Melissa.rel or 0) > 8 and CheckDailyEventExists("", "BuyDressTom", "") == 0 and CheckDailyEventExists(GirlNameIMT, "BuyDress", "") == 0 and int(Melissa.talked_today or 0) < 2 and week != 6

    if _can_buy:
        $ current_action_items.append(MenuItem("Предложить купить Мелиссе обновку", Call("IntMelissaDressChangeApply", GirlNameIMT, "buy_dress")))
    $ current_action_items.append(MenuItem("Назад", Call("IntMelissaTalkRefresh", GirlNameIMT)))
    return


label IntMelissaDressChangeApply(GirlNameIMT="melissa", choice_code=""):
    if str(choice_code or "") == "buy_dress":
        $ MainTxt = "\"Мелисса, у тебя наверное мало нарядов? Давай я тебе еще один куплю?\" - спросили вы.\n\"Да, мало, а ты откуда знаешь?\" удивилась та вашей осведомленности. \"Впрочем, девушке всегда мало. Раз ты предложил, то давай завтра с утра к Ирме пойдем? Ну и да, спасибо, Стефан.\"\n\"Да, давай, чего откладывать? Значит завтра с утра пораньше в мастерской Ирмы Фараго. Буду ждать.\""
        $ CurLocDesc = MainTxt
        $ DailyEventsList_Add(GirlNameIMT, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
        $ Melissa.mark_talked()
        call IntMelissaTalkRefresh(GirlNameIMT)
        return
    return


label int_melissa_dress_change():
    call IntMelissaDressChange("melissa")
    return
