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
        "В том, что уединились с Жоржеттой во время службы" if int(Georgett.sex_stat("sexacts", 0) or 0) > 0 and Georgett.story_value("church_bench_seen", 0):
            $ scene_runtime.text = "Вы рассказали отцу Герхарду, что во время службы уединились с Жоржеттой в темном углу собора. Священник подробно расспросил вас об обстоятельствах, затем строго напомнил, что в храме следует думать о молитве, а не о плотских желаниях."
            $ Georgett.set_story_value("churchgeorgettadmit", 1)
        "В том, что рискнули с Жоржеттой прямо во время службы" if int(Georgett.sex_stat("sexacts", 0) or 0) > 0 and Georgett.story_value("church_doggy_seen", 0):
            $ scene_runtime.text = "Вы признались, что рискнули с Жоржеттой прямо во время службы, почти не скрываясь. Отец Герхард долго молчал, потом сказал, что честное покаяние лучше утаивания."
            $ Georgett.set_story_value("churchgeorgettadmit", 1)
        "В том, что Лизетта видела вас с Жоржеттой во время службы" if int(Georgett.sex_stat("sexacts", 0) or 0) > 0 and Georgett.story_value("church_liza_seen", 0):
            $ scene_runtime.text = "Вы добавили, что Лизетта видела вас с Жоржеттой во время службы. Отец Герхард стал расспрашивать уже не о вас, а о том, как на это смотрели мать и дочь, после чего отпустил вас с необычайно задумчивым видом."
            $ Georgett.set_story_value("churchlizaadmit", 1)
        "Передумать":
            return

    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/gerhard/gerhardispoved.jpg"
    "[scene_runtime.text]"
    $ calendar_v2.advance_minutes(60)
    return
