# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label GiveBirthStep2(girl_name="", daddy_suspect_1="", daddy_suspect_2="", give_birth_timer=0):
    if not girl_name:
        return

    $ renpy.dynamic("real_name", "real_name2")
    $ real_name = people_display_name(girl_name)
    $ real_name2 = people_name(girl_name, 'genitive')

    while True:
        call ShowImage("", "", "images/ellona/ante2.jpg")

        "Вы находитесь в храме, посвященном богине любви и плодородия Эллоне, в комнате для родов."
        "На ложе, широко раздвинув ноги, лежит голая рожающая [real_name]."

        if give_birth_timer == 0:
            "Вокруг нее хлопочет жрица Эллоны Франческа."
        elif give_birth_timer == 1:
            "Она глубоко и размеренно дышит и, повинуясь командам Франчески, тужится, пытаясь разрешиться от бремени."
        elif give_birth_timer == 2:
            "Ее старания не остались безрезультатными, из нее уже показалась макушка младенца. Франческа успокаивающе держит ее за плечи, побуждая продолжать свои усилия."
        elif give_birth_timer == 3:
            "Голова ребенка уже почти полностью вышла наружу. Франческа готовится подхватить его. Сейчас все закончится. Или начнется."

        if girl_name == "sandra":
            "Рядом стоят, готовые помочь, Мелисса и Аманда. Скоро у них, да и у вас, появится еще один малыш."
        elif girl_name in ("melissa", "amanda"):
            "Рядом стоит Сандра, ждущая скорого появления на свет племянника. Или племянницы."
        elif girl_name == "becky":
            "Рядом стоит дружище Эдди. Непонятно, рад он или нет скорому появлению братика или сестрички."
            if daddy_suspect_1 == "эдди" or daddy_suspect_2 == "эдди":
                "А может, вовсе даже сыночка или дочурки."
        elif girl_name == "liza":
            "Рядом стоит Жоржетта, подбадривая Лизетту."
        elif girl_name == "georgett":
            "Рядом стоит Лизетта. Ведет молоденькая шлюшка себя спокойно, судя по всему ее мама и раньше рожала братиков-сестричек в ее присутствии."
        elif girl_name == "inga":
            "Обеспокоенная Бекки стоит рядом и готова помочь, если что, любимой дочурке."

        "Вы, тем временем, можете подождать, рассмотреть украшающие храм статуи и росписи или помолиться за благополучные роды у небольшого алтаря. Впрочем, жрецы и жрицы всегда говорят, что молитва без небольшого, хотя бы в 10 мараведи, пожертвования неискренна и боги ее не услышат."

        menu:
            "Подождать":
                $ give_birth_timer += 1
                if give_birth_timer > 3:
                    call GiveBirthFinish(girl_name)
                    return

            "Рассмотреть статуи и росписи":
                call EllonaTempleMenu

            "Помолиться за благополучные роды":
                call EllonaBirthPrayMenu(girl_name)
                $ give_birth_timer += int(_return or 0)

    return
