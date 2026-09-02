# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init python:
    def sandra_dress_change_can_buy(girl_name="sandra"):
        return (
            int(Sandra.rel or 0) > 8
            and daily_events.exists("", "BuyDressTom", "") == 0
            and daily_events.exists("sandra", "BuyDress", "") == 0
            and int(Sandra.talked_today or 0) < 2
            and int(calendar_v2.week or 0) != 6
        )


label IntSandraOfferBuyDress(GirlNameIST="sandra"):
    $ GirlNameIST = str(GirlNameIST or "sandra")
    $ main_ui_runtime.action_title = "Одежда Сандры"
    $ main_ui_runtime.action_content = None

    if not sandra_dress_change_can_buy(GirlNameIST):
        $ scene_runtime.text = "Сандра сейчас не готова обсуждать покупку нового наряда."
        $ scene_runtime.location_text = scene_runtime.text
        return

    $ scene_runtime.text = "\"Сандра, дорогая, я хочу тебе что-нибудь подарить! Ты у меня такая замечательная! Давай я тебе какой-нибудь наряд подарю! Хочешь?\" - порадовали вы Сандру.\n\n\"Какой ты внимательный, Стефан! Не могу на тебя нарадоваться!\" засмеялась Сандра. \"Конечно хочу!\"\n\n\"Ну давай тогда завтра, с утра пораньше, встретимся у Ирмы Фараго, я буду тебя там ждать, вместе и выберем!\" заверили вы Сандру."
    $ daily_events.add(GirlNameIST, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")
    $ Sandra.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return
