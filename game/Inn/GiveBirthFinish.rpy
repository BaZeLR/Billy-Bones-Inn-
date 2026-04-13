label GiveBirthFinish:
    if not GirlName:
        return

    $ real_name = RealName.get(GirlName, GirlName)
    $ real_name3 = RealName3.get(GirlName, real_name)

    "Храм огласил детский крик: [real_name] наконец разрешилась от бремени."

    if GirlName == "sandra":
        "Вы вместе с сестрами подошли к ложу посмотреть на новорожденного."
    elif GirlName in ("melissa", "amanda"):
        "Матушка подвинулась, чтобы вы могли рассмотреть младенца."
    elif GirlName == "becky":
        "Вы подошли ближе, пока Эдди стоял рядом с тяжелым выражением лица."
    elif GirlName == "liza":
        "Вы заглянули через плечо довольной Жоржетты."
    elif GirlName == "georgett":
        "Вы осторожно подвинули ахающую Лизетту и посмотрели на ребенка."
    elif GirlName == "inga":
        "Ребенок уже оказался на руках у Бекки, и она гордо показала его вам."

    python:
        try:
            KidID = CreateKid(GirlName)
        except Exception:
            KidID = 0

        try:
            KidDescription = ShowKidDesc(KidID)
        except Exception:
            KidDescription = "новорожденный ребенок"

        store.KidID = KidID
        store.KidDescription = KidDescription

    "Это [KidDescription]."
    "[real_name] что-то прошептала Франческе, и та торжественно нарекла младенца именем перед статуей Эллоны."

    menu:
        "Подождать, пока [real_name3] отдохнет и придет в себя":
            "Через несколько часов [real_name3] оправилась после родов."

            if GirlName == "sandra":
                "Вы с Мелиссой и Амандой проводили маму и младенца домой, в трактир."
            elif GirlName in ("melissa", "amanda"):
                "Вы вместе с мамой помогли [real_name3] добраться до трактира."
            elif GirlName == "becky":
                "Вы вместе с Эдди проводили вдовушку с младенцем до ее дома."
            elif GirlName == "liza":
                "Вы вместе с Жоржеттой помогли Лизетте дойти домой."
            elif GirlName == "georgett":
                "Вы вместе с Лизеттой помогли Жоржетте и ребенку добраться домой."
            elif GirlName == "inga":
                "Бекки поблагодарила вас, и семья Инги отправилась домой."

            "День выдался долгим. Вам хочется только лечь спать."

            menu:
                "Идти спать":
                    call NextDay("TavernMain", 1)
                    return

    return
