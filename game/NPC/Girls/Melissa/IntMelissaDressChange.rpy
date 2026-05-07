# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntMelissaDressChange(GirlNameIMT="melissa"):
    python:
        _can_buy = (
            Friends.get(GirlNameIMT, 0) > 8
            and CheckDailyEventExists("", "BuyDressTom", "") == 0
            and CheckDailyEventExists(GirlNameIMT, "BuyDress", "") == 0
            and Talked.get(GirlNameIMT, 0) < 2
            and week != 6
        )

    if not _can_buy:
        return

    menu:
        "Предложить купить Мелиссе обновку" if _can_buy:
            "\"Мелисса, у тебя наверное мало нарядов? Давай я тебе еще один куплю?\" - спросили вы.\n\"Да, мало, а ты откуда знаешь?\" удивилась та вашей осведомленности. \"Впрочем, девушке всегда мало. Раз ты предложил, то давай завтра с утра к Ирме пойдем? Ну и да, спасибо, Стефан.\"\n\"Да, давай, чего откладывать? Значит завтра с утра пораньше в мастерской Ирмы Фараго. Буду ждать.\""
            $ DailyEventsList_Add(GirlNameIMT, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
            $ Talked[GirlNameIMT] = Talked.get(GirlNameIMT, 0) + 1
            return

        "Назад":
            return

    return

label int_melissa_dress_change():
    call IntMelissaDressChange("melissa")
    return
