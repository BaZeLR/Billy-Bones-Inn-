# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ChurchIspoved(entry_arg=0):
    if int(entry_arg or 0) != 1:
        return

    $ scene_runtime.text = "Вы зашли в маленькую кабинку для исповеди. С другой стороны ее прозвучал вопрос: \"Грешил ли ты, сын мой?\""
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/church/confessionEntry.png"
    show screen main_ui
    "[scene_runtime.text]"
    menu:
        "В разных пустяках":
            $ scene_runtime.text = "Вы покаялись в том, что ругались и пару раз обсчитали пьяных в своем трактире на один-два мараведи.\n\n\"Это небольшой грех сын мой и я его тебе отпускаю\" - прозвучал ответ."
        "В том, что совокуплялись с Жоржеттой" if int(Georgett.sex_stat("sexacts", 0) or 0) > 0:
            $ scene_runtime.text = "Вы покаялись в том, что сношались с проституткой Жоржеттой. Отец Герхард вас подробно распросил обо всех обстоятельствах и как именно и сколько раз вы имели дело с Жоржеттой. Потом он сказал:\n\n\"Великий бог Ильматер завещал нам плодиться и размножаться. Коль обе стороны желают соития, то не грех это сын мой!\""
            $ Georgett.set_story_value("georgettadmit", 1)
        "В том, что совокуплялись с Жоржеттой прямо во время службы" if int(Georgett.sex_stat("sexacts", 0) or 0) > 0 and Georgett.story_value("fuckinchurch", 0) and Georgett.story_value("georgettadmit", 0):
            $ scene_runtime.text = "Вы покаялись в том, что трахнули Жоржетту в соборе прямо во время службы. Отец Герхард вас подробно распросил обо всех обстоятельствах, о том, как вам удалось остаться незамеченными и как все прошло. Потом он сказал:\n\n\"Великий бог Ильматер завещал нам плодиться и размножаться. Конечно нужно это делать вне храма, а в храме смиренно слушать службу. А ты, сын мой, не утерпел. Грех это, но не великий. Коль покаялся ты в нем и рассказал все честно, без утайки, то отпускаю я его тебе!\""
            $ Georgett.set_story_value("churchgeorgettadmit", 1)
        "В том, что совокуплялись с Жоржеттой прямо во время службы на глазах у ее дочки" if int(Georgett.sex_stat("sexacts", 0) or 0) > 0 and Georgett.story_value("fuckinchurch", 0) and Georgett.story_value("lizasawinchurch", 0) and Georgett.story_value("churchgeorgettadmit", 0):
            $ scene_runtime.text = "Вы сказали что вы рассказали не все. Пока вы имели Жоржетту, за вами наблюдала, лаская себя, ее дочка Лизетта. Отец Герхард заметно оживился и стал расспрашивать вас о подробностях, как Лизетта вела себя, что сказала на это ей мать, и прочем. Потом он сказал:\n\n\"Великий бог Ильматер завещал родителям передавать все свои знания и умения детям. Так что отдельного греха в том нет, разве что, как я уже говорил тебе, в храме нужно смиренно слушать службу. Но тот грех я тебе уже отпустил, так что иди с миром\""
            $ Georgett.set_story_value("churchlizaadmit", 1)

    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/gerhard/gerhardispoved.jpg"
    "[scene_runtime.text]"
    menu:
        "Вернуться в собор":
            $ calendar_v2.advance_minutes(60)
            jump Church
