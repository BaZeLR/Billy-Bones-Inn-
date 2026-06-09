# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

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


label IntSandraOfferBuyDress(GirlNameIST="sandra"):
    $ GirlNameIST = str(GirlNameIST or "sandra")
    $ current_action_title = "Одежда Сандры"
    $ current_action_content = None

    if not sandra_dress_change_can_buy(GirlNameIST):
        $ MainTxt = "Сандра сейчас не готова обсуждать покупку нового наряда."
        $ CurLocDesc = MainTxt
        $ current_action_items = [
            MenuItem("Вернуться к разговору", Function(main_ui_call_label, "IntSandraTalk", GirlNameIST)),
            MenuItem("Закончить разговор", Function(main_ui_end_talk_state)),
        ]
        return

    $ MainTxt = "\"Сандра, дорогая, я хочу тебе что-нибудь подарить! Ты у меня такая замечательная! Давай я тебе какой-нибудь наряд подарю! Хочешь?\" - порадовали вы Сандру.\n\n\"Какой ты у меня хороший, Стефан! Не могу на тебя нарадоваться!\" засмеялась Сандра. \"Конечно хочу!\"\n\n\"Ну давай тогда завтра, с утра пораньше, встретимся у Ирмы Фараго, я буду тебя там ждать, вместе и выберем!\" заверили вы ее."
    $ DailyEventsList_Add(GirlNameIST, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
    $ Talked[GirlNameIST] = int(Talked.get(GirlNameIST, 0) or 0) + 1
    $ CurLocDesc = MainTxt
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Function(main_ui_call_label, "IntSandraTalk", GirlNameIST)),
        MenuItem("Закончить разговор", Function(main_ui_end_talk_state)),
    ]
    return
