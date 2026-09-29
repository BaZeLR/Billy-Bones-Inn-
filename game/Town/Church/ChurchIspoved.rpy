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
    menu:
        "В разных пустяках":
            $ scene_runtime.text = "Вы покаялись в том, что ругались и пару раз обсчитали пьяных в своем трактире на один-два мараведи.\n\n\"Это небольшой грех сын мой и я его тебе отпускаю\" - прозвучал ответ."
        "В том, что совокуплялись с Жоржеттой" if story_event_available("Church", "georgett_regular_confession"):
            call checkTriggers("Church", "georgett_regular_confession", 0)
        "В том, что совокуплялись с Жоржеттой прямо во время службы" if story_event_available("Church", "georgett_service_confession"):
            call checkTriggers("Church", "georgett_service_confession", 0)
        "В том, что совокуплялись с Жоржеттой прямо во время службы на глазах у ее дочки" if int(Georgett.sex_stat("sexacts", 0) or 0) > 0 and Georgett.story_value("fuckinchurch", 0) and Georgett.story_value("lizasawinchurch", 0) and Georgett.story_value("churchgeorgettadmit", 0) and not Georgett.story_value("churchlizaadmit", 0):
            $ scene_runtime.text = "Вы сказали что вы рассказали не все. Пока вы имели Жоржетту, за вами наблюдала, лаская себя, ее дочка Лизетта. Отец Герхард заметно оживился и стал расспрашивать вас о подробностях, как Лизетта вела себя, что сказала на это ей мать, и прочем. Потом он сказал:\n\n\"Великий бог Ильматер завещал родителям передавать все свои знания и умения детям. Так что отдельного греха в том нет, разве что, как я уже говорил тебе, в храме нужно смиренно слушать службу. Но тот грех я тебе уже отпустил, так что иди с миром\""
            $ Georgett.set_story_value("churchlizaadmit", 1)
        "Рассказать, что вы видели Бекки после службы" if any(threads["beckyGerhardAdvice"].done) and not Gerhard.var_value("becky_church_reported", False):
            $ scene_runtime.text = "Вы тихо назвали имя Бекки и рассказали, что видели за запертой дверью после службы. Герхард умолк. Когда он ответил, в его голосе уже не было прежней надменности: \"Я услышал тебя, сын мой. Говори, если тебя тревожит что-то еще.\""
            $ Gerhard.set_var("becky_church_reported", True)
        "Спросить Герхарда о Франческе" if Gerhard.confession_points() >= 5 and not Gerhard.var_value("franchesca_topic_heard", False):
            call story_gerhard_franchesca_topic
        "Спросить о знатных дамах города" if Gerhard.confession_points() >= 5 and not Gerhard.var_value("town_ladies_topic_heard", False):
            call story_gerhard_town_ladies_topic

    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/gerhard/gerhardispoved.jpg"
    menu:
        "Вернуться в собор":
            $ calendar_v2.advance_minutes(60)
            jump Church


label story_georgett_church_confession_regular:
    $ scene_runtime.text = "Вы покаялись в том, что сношались с проституткой Жоржеттой. Отец Герхард вас подробно распросил обо всех обстоятельствах и как именно и сколько раз вы имели дело с Жоржеттой. Потом он сказал:\n\n\"Великий бог Ильматер завещал нам плодиться и размножаться. Коль обе стороны желают соития, то не грех это сын мой!\""
    $ Georgett.set_story_value("georgettadmit", 1)
    if event_runtime.active_thread is threads.get("georgettChurch") and not event_runtime.active_thread.done[2]:
        $ event_runtime.active_thread.seen(2)
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
    return


label story_georgett_church_confession_service:
    $ scene_runtime.text = "Вы покаялись в том, что трахнули Жоржетту в соборе прямо во время службы. Отец Герхард вас подробно распросил обо всех обстоятельствах, о том, как вам удалось остаться незамеченными и как все прошло. Потом он сказал:\n\n\"Великий бог Ильматер завещал нам плодиться и размножаться. Конечно нужно это делать вне храма, а в храме смиренно слушать службу. А ты, сын мой, не утерпел. Грех это, но не великий. Коль покаялся ты в нем и рассказал все честно, без утайки, то отпускаю я его тебе!\""
    $ Georgett.set_story_value("churchgeorgettadmit", 1)
    if event_runtime.active_thread is threads.get("georgettChurch") and not event_runtime.active_thread.done[3]:
        $ event_runtime.active_thread.seen(3)
        $ event_runtime.evaluation_time = None
        $ findAvailableEvents(True)
    return


label story_gerhard_franchesca_topic:
    $ scene_runtime.text = "Вы спросили Герхарда о Франческе. За перегородкой скрипнула скамья. \"Она служит Эллоне, сын мой, и знает, чего люди желают, прежде чем они сами в том признаются. Мы знакомы давно. Но не принимай ее помощь за бескорыстную: в этом городе у каждого жреца свой расчет.\" Больше он пока не сказал."
    $ Gerhard.set_var("franchesca_topic_heard", True)
    return


label story_gerhard_town_ladies_topic:
    $ scene_runtime.text = "Вы спросили, почему Франческа так часто бывает в домах городских дам. \"Они думают, что устраивают судьбу своих подопечных,\" ответил Герхард. \"Иные даже не ведают, чьему делу помогают. Присмотрись к тем, кого отправляют из этих домов в храм, и поймешь больше, чем из моих слов.\""
    $ Gerhard.set_var("town_ladies_topic_heard", True)
    return
