# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntGeorgettDressChange(GirlNameIGT="georgett"):
    python:
        _can_shame = Friends.get(GirlNameIGT, 0) > 8 and Talked.get(GirlNameIGT, 0) < 2
        _can_buy = (
            Friends.get(GirlNameIGT, 0) > 8
            and CheckDailyEventExists("", "BuyDressTom", "") == 0
            and CheckDailyEventExists(GirlNameIGT, "BuyDress", "") == 0
            and Talked.get(GirlNameIGT, 0) < 2
            and week != 6
        )

    if not (_can_shame or _can_buy):
        return

    menu:
        "Постыдить Жоржетту за то, что она ходит без лифчика" if _can_shame:
            "\"Жоржетт, а не стыдно тебе без лифа-то ходить?\" - попробовали пристыдить вы гулящую девку со стажем. \"У тебя же сиськи такие, ну такие, объемные в общем, монументальные, такие что даже вываливаются иногда из декольте. Может лиф-то оденешь?\""
            "\"Ты, парнишка, за меня не беспокойся,\" ответила вам она. \"Нет у меня лифа, не носила я его никогда, и не буду носить. Так вот, от того что не носила, то у меня такие сиськи и выросли, всем девкам в округе на зависть. Это меня мама такому научила,\" добавила она с гордостью."
            $ Talked[GirlNameIGT] = Talked.get(GirlNameIGT, 0) + 1
            return

        "Постыдить Жоржетту за отстутсвие панталон" if _can_shame:
            $ AgreedToRedress = 0
            "\"Жоржетт, у тебя юбочка и до пупа не достает, а ты еще и без панталон ходишь. Как говорится что на прилавке то и в лавке. Людей бы постыдилась! Я понимаю, что в твоем ремесле они скорее мешают, но стыд-то знать надо?\" - попробовали вы пристыдить ее."
            "\"Знаешь, что мой юный работадатель!\" в сердцах ответила вам Жоржетта. \"Не тебе меня учить как трахаться и как клиентов завлекать. Я первый раз свою киску продала, когда ты еще пешком под стол ходил. И, между прочим, помни, что с каждого клиента я тебе три мараведи отстегиваю. Меньше клиентов у меня - меньше денег у тебя!\""
            $ Talked[GirlNameIGT] = Talked.get(GirlNameIGT, 0) + 1
            return

        "Предложить купить Жоржетте обновку" if _can_buy:
            "\"Жоржи, шлюшка ты моя ненаглядная, а хочешь я тебе обновку куплю?\" - в порыве щедрости задали вы вопрос жрице любви."
            "\"За твой счет, тоесть в подарок?\" удивилась та. \"Конечно хочу, что я, дура что ли от подарков отказываться!\""
            "\"Ну тогда завтра, с утра пораньше, дуй к Ирме Фараго, я буду тебя там ждать, вместе и выберем!\" заверили вы девицу."
            $ DailyEventsList_Add(GirlNameIGT, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
            $ Talked[GirlNameIGT] = Talked.get(GirlNameIGT, 0) + 1
            return

        "Назад":
            return

    return
