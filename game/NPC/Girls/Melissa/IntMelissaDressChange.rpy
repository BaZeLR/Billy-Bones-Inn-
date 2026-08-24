label IntMelissaDressChange(GirlNameIMT="melissa"):
    $ scene_runtime.text = "\"Мелисса, у тебя наверное мало нарядов? Давай я тебе еще один куплю?\" - спросили вы сестру.\n\n\"Да, мало, а ты откуда знаешь?\" удивилась та вашей осведомленности. \"Впрочем, девушке всегда мало. Раз ты предложил, то давай завтра с утра к Ирме пойдем? Ну и да, спасибо, братик.\"\n\n\"Да, давай, чего откладывать? Значит завтра с утра пораньше в мастерской Ирмы Фараго. Буду ждать.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ daily_events.add(GirlNameIMT, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")
    $ Melissa.mark_talked()
    return
