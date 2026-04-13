label GiveBirthStep2:
    if not GirlName:
        return

    $ real_name = RealName.get(GirlName, GirlName)

    "Вы находитесь в храме Эллоны, в комнате для родов."
    "На ложе, широко раздвинув ноги, лежит рожающая [real_name]."

    if GiveBirthTimer == 0:
        "Вокруг нее хлопочет жрица Эллоны Франческа."
    elif GiveBirthTimer == 1:
        "Она глубоко дышит и, по команде Франчески, тужится."
    elif GiveBirthTimer == 2:
        "Уже показалась макушка младенца."
    elif GiveBirthTimer == 3:
        "Голова ребенка почти вышла. Осталось совсем немного."

    if GirlName == "sandra":
        "Рядом стоят Мелисса и Аманда."
    elif GirlName in ("melissa", "amanda"):
        "Рядом стоит ваша матушка."
    elif GirlName == "becky":
        "Рядом стоит Эдди."
        if DaddySuspect1 == "эдди" or DaddySuspect2 == "эдди":
            "Похоже, он догадывается, что может быть отцом ребенка."
    elif GirlName == "liza":
        "Рядом стоит Жоржетта, подбадривая дочь."
    elif GirlName == "georgett":
        "Рядом стоит Лизетта."
    elif GirlName == "inga":
        "Рядом стоит обеспокоенная Бекки."

    menu:
        "Подождать":
            $ GiveBirthTimer += 1
            if GiveBirthTimer > 3:
                call GiveBirthFinish
                return
            jump GiveBirthStep2

        "Рассмотреть статуи и росписи":
            call EllonaTempleMenu
            jump GiveBirthStep2

        "Помолиться за благополучные роды":
            call EllonaBirthPrayMenu
            jump GiveBirthStep2

    return
