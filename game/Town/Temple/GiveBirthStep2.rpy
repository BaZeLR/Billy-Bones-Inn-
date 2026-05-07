# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label GiveBirthStep2:
    if not GirlName:
        return

    $ real_name = RealName.get(GirlName, GirlName)
    $ real_name2 = RealName2.get(GirlName, real_name)
    call ShowImage("", "", "images/ellona/ante2.jpg")

    "Вы находитесь в храме, посвященном богине любви и плодородия Эллоне, в комнате для родов."
    "На ложе, широко раздвинув ноги, лежит голая рожающая [real_name]."

    if GiveBirthTimer == 0:
        "Вокруг нее хлопочет жрица Эллоны Франческа."
    elif GiveBirthTimer == 1:
        "Она глубоко и размеренно дышит и, повинуясь командам Франчески, тужится, пытаясь разрешиться от бремени."
    elif GiveBirthTimer == 2:
        "Ее старания не остались безрезультатными, из нее уже показалась макушка младенца. Франческа успокаивающе держит ее за плечи, побуждая продолжать свои усилия."
    elif GiveBirthTimer == 3:
        "Голова ребенка уже почти полностью вышла наружу. Франческа готовится подхватить его. Сейчас все закончится. Или начнется."

    if GirlName == "sandra":
        "Рядом стоят, готовые помочь, Мелисса и Аманда. Скоро у них, да и у вас, появится еще один малыш."
    elif GirlName in ("melissa", "amanda"):
        "Рядом стоит Сандра, ждущая скорого появления на свет племянника. Или племянницы."
    elif GirlName == "becky":
        "Рядом стоит дружище Эдди. Непонятно, рад он или нет скорому появлению братика или сестрички."
        if DaddySuspect1 == "эдди" or DaddySuspect2 == "эдди":
            "А может, вовсе даже сыночка или дочурки."
    elif GirlName == "liza":
        "Рядом стоит Жоржетта, подбадривая Лизетту."
    elif GirlName == "georgett":
        "Рядом стоит Лизетта. Ведет молоденькая шлюшка себя спокойно, судя по всему ее мама и раньше рожала братиков-сестричек в ее присутствии."
    elif GirlName == "inga":
        "Обеспокоенная Бекки стоит рядом и готова помочь, если что, любимой дочурке."

    "Вы, тем временем, можете подождать, рассмотреть украшающие храм статуи и росписи или помолиться за благополучные роды у небольшого алтаря. Впрочем, жрецы и жрицы всегда говорят, что молитва без небольшого, хотя бы в 10 мараведи, пожертвования неискренна и боги ее не услышат."

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
