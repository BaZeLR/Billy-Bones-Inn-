# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label GiveBirthFinish(girl_name=""):
    if not girl_name:
        return

    $ renpy.dynamic("real_name", "real_name3", "kid_id", "kid_description", "newborn", "kid_name", "kid_gender", "_sandra_newborn_relation", "_mother_newborn_relation", "_liza_newborn_relation", "_georgett_newborn_relation", "_becky_newborn_relation")
    $ real_name = people_display_name(girl_name)
    $ real_name3 = people_name(girl_name, 'dative')
    call ShowImage("", "", "images/ellona/afterBirth.png")

    "Вдруг храм огласил пронзительный детский крик: [real_name] наконец-то разрешилась от бремени."

    if girl_name == "sandra":
        "Не обращая внимания на охи и ахи Мелиссы с Амандой, вы подбежали к ложу, чтобы посмотреть на новорожденного."
    elif girl_name in ("melissa", "amanda"):
        "Как только вы подскочили к ложу [real_name3], Сандра подвинулась чуть в сторону, давая вам возможность без помех осмотреть младенца."
    elif girl_name == "becky":
        "Не обращая внимания на Эдди, стоящего с перекошенным от увиденного лицом, вы подошли к ложу, чтобы рассмотреть ребенка вдовушки поподробнее."
    elif girl_name == "liza":
        "Заглянув через плечо довольной Жоржетты, вы смогли рассмотреть новорожденного."
    elif girl_name == "georgett":
        "Подвинув немножко ахающую Лизетту, вы смогли рассмотреть новорожденного."
    elif girl_name == "inga":
        "Ребенок уже очутился на руках у Бекки. Перехватив ваш заинтересованный взгляд, довольная бабушка гордо показала вам прибавку в своем семействе."

    $ kid_id = CreateKid(girl_name)
    $ kid_description = ShowKidDesc(kid_id)
    $ newborn = GetKidData(kid_id)
    $ kid_name = newborn["KidName"]
    $ kid_gender = newborn["KidGender"]
    $ _sandra_newborn_relation = "новоприобретенным братиком" if kid_gender == "M" else "новоприобретенной сестричкой"
    $ _mother_newborn_relation = "сыночку" if kid_gender == "M" else "дочурке"
    $ _liza_newborn_relation = "нагулянным мальчиком" if kid_gender == "M" else "нагулянной девочкой"
    $ _georgett_newborn_relation = "новому братику" if kid_gender == "M" else "новой сестричке"
    $ _becky_newborn_relation = "внучком" if kid_gender == "M" else "внучкой"

    "Это [kid_description]."
    'Тут [real_name] приподнялась с ложа и что-то прошептала на ухо Франческе. Та выслушала ее, кивнула и, подняв младенца перед статуей Эллоны, провозгласила: "Перед лицом Великой Богини Любви, Урожая и Плодородия, нарекаю тебя [kid_name]! Возблагодари же Эллону за свое появление в этом мире, [("юный" if kid_gender == "M" else "юная")] [kid_name]!"'
    if kid_gender == "M":
        "[kid_name] ответил возмущенным писком."
    else:
        "[kid_name] ответила возмущенным писком."

    menu:
        "Подождать, пока [real_name3] отдохнет и придет в себя":
            "Франческа продолжила хлопотать над роженицей и младенцем. Через несколько часов [real_name3] оправилась от родов, отдохнула и смогла встать."

            if girl_name == "sandra":
                "Вместе с Мелиссой и Амандой вы проводили Сандру с [_sandra_newborn_relation] домой, в трактир."
            elif girl_name in ("melissa", "amanda"):
                "Вместе с Сандрой вы помогли [real_name3] и ее [_mother_newborn_relation] добраться до трактира."
            elif girl_name == "becky":
                "Вместе с Эдди вы проводили вдовушку с младенцем до ее лавки."
            elif girl_name == "liza":
                "Вместе с Жоржеттой вы помогли Лизетте вместе с ее [_liza_newborn_relation] добраться до дому."
            elif girl_name == "georgett":
                "Вместе с Лизеттой вы помогли ее [_georgett_newborn_relation] добраться до дому. Ну и Жоржетту, само собой, не забыли."
            elif girl_name == "inga":
                "Бекки поблагодарила вас за поддержку и попрощалась. Бабушка с дочкой и [_becky_newborn_relation] направились к себе домой, а вы к себе, в трактир."

            "День выдался насыщенным и долгим. Вам уже ничего не хочется делать, кроме как завалиться на кровать и продрыхнуть до утра."

            menu:
                "Идти спать":
                    call NextDay("TavernMain", 1)
                    return

    return
