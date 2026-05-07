# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntGeorgettAfterCermon:
    $ ChurchAfterCermon["georgett"] = 0
    return


label AfterCermonGeorgett:
    $ GirlNameAC = "georgett"
    $ current_action_title = "Замочная скважина"
    $ current_action_content = None
    $ current_action_items = []

    if ChurchAfterCermon.get(GirlNameAC, 0) == 0:
        $ GetSexEventFromTable(GirlNameAC, 99, "Priest")
        call PregnancyCheck(GirlNameAC, "inside", 1, "Отец Герхард")
        $ MainTxt = "Посмотрев в замочную скважину вы увидели Жоржетту и отца Герхарда."
        if GeorgettVar.get("SawChurchAfterCermon", 0) == 0:
            $ MainTxt = MainTxt + "\n\n\"Дочь моя, скрыла ты от меня что совокуплялась в этом храме. Но служителю Ильматера все ведомо\" - говорит отец Герхард, кладя руку на обнаженное колено Жоржетты.\n\"Ох, падре, постеснялась я признаться в таком непотребстве\" - отвечает Жоржетта, слегка раздвигая ноги."
        else:
            $ MainTxt = MainTxt + "\n\n\"Дочь моя, ты опять грешила. Расскажи мне все без утайки, не можешь же расскать - продемонстрируй\" - говорит отец Герхард, кладя руку на обнаженное колено Жоржетты.\n\"Ох, падре, грешила я, сходилась со многими, даже в храме этом\" - отвечает Жоржетта, слегка раздвигая ноги и приподнимая выше подол платья."
        $ CurLocDesc = MainTxt
        call ShowImage("georgett", "ispoved", "ispoved1")
        $ ChurchAfterCermon[GirlNameAC] = 1
        $ current_action_items.append(MenuItem("Посмотреть еще", Call("AfterCermonGeorgett")))
        $ renpy.restart_interaction()
        return

    if ChurchAfterCermon.get(GirlNameAC, 0) == 1:
        $ MainTxt = "Вы продолжаете наблюдать за Жоржеттой и отцом Герхардом через замочную скважину."
        if GeorgettVar.get("SawChurchAfterCermon", 0) == 0:
            $ MainTxt = MainTxt + "\n\n\"Не печалься, дочь моя, могу я отпустить тебе этот грех, как и грех лжи. Но сначала расскажи подробно, как ты согрешила. Вот член, подобный тому, с коим ты грешила. Если трогала его рукой, то покажи как.\" - говорит отец Герхард, приподнимая сутану. Под ней обнаруживается уже поднявшийся член жреца.\n\"Да, падре, трогала я член, вот так\" - говорит Жоржетта и начинает подрачивать член отца Герхарда своими ловкими пальчиками."
        else:
            $ MainTxt = MainTxt + "\n\n\"Не печалься, дочь моя, а рассказывай подробно. Вот член, подобный тем, с коими ты грешила. Покажи, что ты с ним делала.\" - говорит отец Герхард, приподнимая сутану. Под ней обнаруживается уже поднявшийся член жреца.\n\"Падре, трогала я член, вот так\" - говорит Жоржетта и начинает подрачивать член отца Герхарда своими ловкими пальчиками.\n\"А еще я в рот их брала, вот так\" - добавляет Жоржетта, становясь на колени и начиная делать минет отцу Герхарду своим искусным ротиком."
        $ CurLocDesc = MainTxt
        call ShowImageSeq("georgett", "ispoved", "ispovedstep2_", 2)
        $ ChurchAfterCermon[GirlNameAC] = 2
        $ current_action_items.append(MenuItem("Смотреть дальше", Call("AfterCermonGeorgett")))
        $ renpy.restart_interaction()
        return

    if ChurchAfterCermon.get(GirlNameAC, 0) == 2:
        $ MainTxt = "Вы продолжаете наблюдать за Жоржеттой и отцом Герхардом через замочную скважину."
        if GeorgettVar.get("SawChurchAfterCermon", 0) == 0:
            $ MainTxt = MainTxt + "\n\n\"А что ты потом делала? Панталончики сняла наверное?\"\n\"Нет, падре, не ношу я панталончиков, вот, смотрите.\" - говорит Жоржетта и задирает подол платья, демонстрируя жрецу свою киску."
        else:
            $ MainTxt = MainTxt + "\n\n\"И ты наверное опять без панталончиков, негодница?\"\n\"Да, падре, вот, смотрите.\" - говорит Жоржетта и задирает подол платья, демонстрируя жрецу свою киску."
        if CumInsideYou.get(GirlNameAC, 0) or CumInsideOthers.get(GirlNameAC, 0):
            $ MainTxt = MainTxt + "\n\nОтец Герхард немедленно замечает свежие следы спермы на бедрах и лобке девушки. \"Ух, негодница, уже потрахалась с утра пораньше.\" - говорит он. Вам кажется, что в его голосе вы слышите одобрение."
        $ MainTxt = MainTxt + "\n\n\"Ну, показывай, как грешила.\"\nЖоржетта встает, перекидывает ногу через сидящего отца Герхарда и садится своей девочкой прямо на его вздыбленный член. \"Вот так я грешила, падре!\""
        $ CurLocDesc = MainTxt
        $ GeorgettVar["SawChurchAfterCermon"] = 1
        call ShowImage("georgett", "ispoved", "ispovedstep3")
        $ ChurchAfterCermon[GirlNameAC] = 3
        $ current_action_items.append(MenuItem("Смотреть не отрываясь", Call("AfterCermonGeorgett")))
        $ renpy.restart_interaction()
        return

    $ MainTxt = "Вы продолжаете наблюдать за Жоржеттой и отцом Герхардом через замочную скважину.\n\nЖоржетта скачет на члене отца Герхарда, а тот уже успел расстегнуть ее блузку и теперь мнет ее полные груди. Жоржетта впивается в отца Герхарда страстным поцелуем, не прекращая скачки.\n\nВскоре парочка достигает оргазма практически одновременно, Жоржетта издает протяжный стон, содрогаясь всем телом, а жрец заполняет ее своим семенем."
    if GeorgettVar.get("TalkChurchAfterCermonLiza", 0):
        $ MainTxt = MainTxt + "\n\n\"А ты ведь и доченьку мою потрахиваешь\" - говорит Жоржетта. \"И кто лучше: я или она?\"\n\"Обе вы прекрасны\", не растерявшись, говорит жрец. \"Все важны Ильматеру, все ему любы. А значит и мне любы одинаково, как его слуге."
        if kids.get("liza", 0) == 0:
            $ MainTxt = MainTxt + "\n\n\"Ловко вывернулся,\" смеется Жоржетта. \"Доча-то моя шустрая глядишь такими темпами меня бабушкой скоро сделает, а мне ведь и тридцать еше не скоро стукнет."
        else:
            $ MainTxt = MainTxt + "\n\n\"Ловко вывернулся,\" смеется Жоржетта. \"Доча-то моя шустрая, меня ведь уже бабушкой сделала, а мне ведь и тридцати нет."
    $ MainTxt = MainTxt + "\n\n\"Заполнило тебя семя слуги Ильматера в храме его. Это отпускает все грехи твои и благославляет тебя, дочь моя\" - благочестиво говорит отец Герхард Жоржетте, даже не подумав прикрыть свой обмякший член сутаной. \"Теперь иди, а если еще нагрешишь - приходи и покайся мне.\"\n\"Спасибо, отец Герхард\" - говорит Жоржетта и начинает приводить себя в порядок."
    $ CurLocDesc = MainTxt
    call ShowImage("georgett", "ispoved", "ispovedstep4")
    $ ChurchAfterCermon[GirlNameAC] = 4
    $ current_action_items.append(MenuItem("Вернуться", Function(main_ui_call_label, "AdvanceTimeAndRestore", "ChurchRestore")))
    $ renpy.restart_interaction()
    return
