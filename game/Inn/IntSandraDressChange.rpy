init python:
    def sandra_dress_change_can_buy(girl_name="sandra"):
        girl = str(girl_name or "sandra")
        return (
            Friends.get(girl, 0) > 8
            and CheckDailyEventExists("", "BuyDressTom", "") == 0
            and CheckDailyEventExists(girl, "BuyDress", "") == 0
            and Talked.get(girl, 0) < 2
            and week != 6
        )


label IntSandraDressChange(GirlNameIST="sandra"):
    $ current_action_title = "Одежда Сандры"
    $ current_action_content = None
    call IntSandraDressChangeRefresh(GirlNameIST)
    return


label IntSandraDressChangeRefresh(GirlNameIST="sandra"):
    $ current_action_title = "Одежда Сандры"
    $ current_action_content = None
    $ current_action_items = []

    if sandra_dress_change_can_buy(GirlNameIST):
        $ current_action_items.append(MenuItem("Предложить купить мамуле обновку", Call("IntSandraDressChangeApply", GirlNameIST, "buy_dress")))

    $ current_action_items.append(MenuItem("Назад", Call("IntSandraTalkRefresh", GirlNameIST)))
    return


label IntSandraDressChangeApply(GirlNameIST="sandra", choice_code=""):
    if str(choice_code or "") != "buy_dress":
        call IntSandraDressChangeRefresh(GirlNameIST)
        return

    if not sandra_dress_change_can_buy(GirlNameIST):
        call IntSandraTalkRefresh(GirlNameIST)
        return

    $ MainTxt = "\"Мамочка, дорогая, я хочу тебе что нибудь подарить! Ты у меня такая замечательная! Давай я тебе какой-нибудь наряд подарю! Хочешь?\" - порадовали вы маму.\n\"Какой ты у меня хороший сыночек! Не могу на тебя нарадоваться!\" засмеялась мама. \"Конечно хочу!\"\n\"Ну давай тогда завтра, с утра пораньше, встретимся у Ирмы Фараго, я буду тебя там ждать, вместе и выберем!\" заверили вы маму."
    $ DailyEventsList_Add(GirlNameIST, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
    $ Talked[GirlNameIST] = Talked.get(GirlNameIST, 0) + 1
    $ CurLocDesc = MainTxt
    call IntSandraTalkRefresh(GirlNameIST)
    return


label int_sandra_dress_change():
    call IntSandraDressChange("sandra")
    return
