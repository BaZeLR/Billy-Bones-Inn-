label ChurchServiceGeorgett:
    show screen main_ui
    $ scene_runtime.text = "В одном из углов собора вы находите вашу ветренную знакомую - Жоржетту Брюно, шлюху из портового квартала. Это молодая белокурая и кареглазая женщина, среднего роста, чуть пухленькая и с большой налитой грудью. В собор она нарядилась чуть скромнее, чем обычно, но не слишком: на ней красное платье до колен и блузка с глубоким декольте, на этот раз хотя бы не прозрачная. Вы замечаете, что прихожане-мужчины обращают на нее гораздо больше внимания, чем на проповедь с амвона."
    if Georgett.story_value("askkids", 0):
        if Liza.rel > 0:
            $ scene_runtime.text = scene_runtime.text + "\n\nРядом с ней вы видите ее старшую дочь Лизетту - молоденькую мулатку, на вид - ровесницу вашей сестры Аманды. Ее волосы забранны в две косички а груди только начали расти. Ее шоколадное тело закрывают юбка и блузка, такие же как у ее мамы."
        else:
            $ scene_runtime.text = scene_runtime.text + "\n\nРядом с ней вы видите молоденькую мулатку, на вид - ровесницу вашей сестры Аманды. Ее волосы забранны в две косички а груди только начали расти. Судя по всему это Лизетта - старшая дочь Жоржетты. Ее шоколадное тело закрывают юбка и блузка, такие же как у ее мамы."
        vscene "images/georgett/church/cermonliza.jpg"
    else:
        vscene "images/georgett/church/cermon.jpg"
    $ scene_runtime.location_text = scene_runtime.text
    $ Georgett.set_story_value("foundinchurch", 1)
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.action_title = "Жоржетта"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    if player.intimacy.can_cum() and people_to_int(Georgett.rel, 0) >= 2 and people_to_int(Georgett.sex_stat("sexacts", 0), 0) >= 3:
        $ main_ui_runtime.action_items.append(MenuItem("Предложить Жоржетте перепихнуться по быстрому", Call("ChurchGeorgettQuickSex")))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", Call("ChurchServiceMenu", True)))
    $ renpy.restart_interaction()
    return


label ChurchGeorgettQuickSex:
    $ renpy.dynamic("_church_georgett_variant", "_church_georgett_picture_prefix")
    show screen main_ui
    if Georgett.story_value("askkids", 0):
        vscene "images/georgett/church/cermonliza.jpg"
    else:
        vscene "images/georgett/church/cermon.jpg"

    $ scene_runtime.text = "В одном из углов собора вы находите вашу ветренную знакомую и шепчете ей на ухо ваше нескромное предложение."
    if Georgett.rel < 6:
        $ scene_runtime.text = scene_runtime.text + "\n\n\"Ты что, сдурел!\" - отвечает вам она. \"Это же собор!\""
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.mode = "scene"
        $ main_ui_runtime.action_title = "Разговор с Жоржеттой"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = [MenuItem("Назад", Call("ChurchServiceGeorgett"))]
        $ renpy.restart_interaction()
        return

    $ scene_runtime.text = scene_runtime.text + "\n\n\"Какой ты пошлый! Поиметь меня прямо на церковной службе!\" - смеется Жоржетта. \"Это обойдется тебе в 15 мараведи!\""
    if int(player.economy.money or 0) < 15:
        $ scene_runtime.text = scene_runtime.text + "\n\n\"Ой, а у меня столько нет\", говорите вы.\n\n\"Ну нет так нет\", следует резонный ответ."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.mode = "scene"
        $ main_ui_runtime.action_title = "Разговор с Жоржеттой"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = [MenuItem("Назад", Call("ChurchServiceGeorgett"))]
        $ renpy.restart_interaction()
        return

    $ _church_georgett_variant = "bench"
    if Georgett.story_value("askkids", 0):
        $ _church_georgett_variant = "withliza"
        if Liza.rel == 0:
            $ scene_runtime.text = scene_runtime.text + "\n\nЖоржетта поворачивается к молоденькой мулатке-шоколадке, стоящей рядом с ней: \"Стефан, познакомься, это моя старшая доченька Лизетта, я тебе про нее рассказывала. Лизетта, познакомься, это дядя Стефан.\""
            $ Liza.add_relation(1)
        if Georgett.story_value("lizasawinchurch", 0):
            $ scene_runtime.text = scene_runtime.text + "\n\n\"Лизетточка, мы сейчас с дядей Стефаном пойдем потрахаемся\", - без тени смущения говорит ваша подруга своей дочке. \"Оставайся здесь, или, если хочешь, можешь посмотреть. Только тихо.\""
        else:
            $ scene_runtime.text = scene_runtime.text + "\n\n\"Лизетточка, мы сейчас с дядей Стефаном отойдем поговорить, а ты нас здесь подожди, хорошо?\" - говорит ваша подруга своей дочке. \"Хорошо, мама.\""
    elif procedural_randint(1, 2, "church_georgett_variant_%s_%s" % (int(current_game_day()), int(player_cum_count()))) == 1:
        $ _church_georgett_variant = "doggy"

    if _church_georgett_variant == "doggy":
        $ scene_runtime.text = scene_runtime.text + "\n\nВы отдаете деньги Жоржетте и она ведет вас к одной из скамей в дальнем темном углу собора. Вы внимательно осматриваетесь и замечаете, что скамья, колонны, сложенная утварь и прочее барахло заслоняют вас от взглядов толпы. Судя по всему к таким же выводам приходит и Жоржетта, так как она решительным движением снимает с себя юбку под которой, как вы и ожидали, ничего не оказалось. А сняв, Жоржетта наклоняется, опираясь о скамью, приглашающе выставив свою киску. Поняв намек, вы, не теряя времени, спускаете штаны и одним движением входите в развратницу."
    else:
        $ scene_runtime.text = scene_runtime.text + "\n\nВы отдаете деньги Жоржетте и она ведет вас к одной из скамей в дальнем темном углу собора. Вы оба садитесь на нее. Видно, что колонны и прислоненная к ним церковная утварь заслоняют вас от взглядов толпы. Жоржетта быстро приспускает ваши штаны, выпуская на волю ваш уже вставший член. Затем она садится вам на колени, ловко заправляя ваш член в себя. Вы с удовлетворением отмечаете, что Жоржетта даже в церкви не изменила своей привычке ходить без нижнего белья. Оперевшись на следующую скамью ваша подружка начинает плавно двигаться, осторожно но уверенно доводя вас обеих до разрядки."

    if Georgett.story_value("askkids", 0):
        $ scene_runtime.text = scene_runtime.text + "\n\nВдруг вы замечаете, как кто-то наблюдает за вами из тени. Вы извещаете об этом свою подругу, та всматривается в тени и вдруг призывно машет рукой. Наблюдателем оказывается Лизетта, она выходит из своего укрытия и садится рядом с вами.\n\n\"Лизетточка, доченька, видишь, мы с дядей Стефаном трахаемся. Если хочешь посмотреть - то смотри. Только тихо\". С этими словами ваша подруга возобновила свои движения. Лизетта же, смотря на вас, медленно возбуждается и начинает ласкать себя через одежду."

    $ scene_runtime.text = scene_runtime.text + "\n\nВы сношаетесь минут десять, когда ваша подружка не выдерживает, и сжав зубы, чтобы не застонать, кончает. Сразу следом за ней кончаете и вы, заполняя ее незащищенную матку своей спермой. Жоржетта встает с вашего члена и протирает лобок подолом платья, вы же быстро натягиваете приспущенные штаны."
    if Georgett.story_value("askkids", 0):
        $ scene_runtime.text = scene_runtime.text + "\n\n\"Мама, он что, в тебя кончил?\" - вдруг раздается голосок. \"Шшш, доченька, ну конечно в меня, я же тебе говорила что ничего в этом страшного нет.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.mode = "event"
    $ main_ui_runtime.action_title = "Событие"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    "[scene_runtime.text]"

    $ player.spend_money(15)
    $ Georgett.set_story_value("fuckinchurch", 1)
    if Georgett.story_value("askkids", 0):
        $ Georgett.set_story_value("lizasawinchurch", 1)
    $ pregnancy_check("georgett", "inside", 1, "Вы")

    if _church_georgett_variant == "doggy":
        $ _church_georgett_picture_prefix = "images/georgett/church/doggy/doggy"
    elif _church_georgett_variant == "withliza":
        $ _church_georgett_picture_prefix = "images/georgett/church/withLiza.jpg/withliza"
    else:
        $ _church_georgett_picture_prefix = "images/georgett/church/bench/bench"

    $ scene_runtime.picture = _church_georgett_picture_prefix + "1.jpg"
    vscene scene_runtime.picture
    menu:
        "Дальше":
            pass
    $ scene_runtime.picture = _church_georgett_picture_prefix + "2.jpg"
    vscene scene_runtime.picture
    menu:
        "Дальше":
            pass
    $ scene_runtime.picture = _church_georgett_picture_prefix + "3.jpg"
    vscene scene_runtime.picture
    menu:
        "Дальше":
            pass
    $ scene_runtime.picture = _church_georgett_picture_prefix + "4.jpg"
    vscene scene_runtime.picture
    menu:
        "Дальше":
            pass
    $ scene_runtime.picture = _church_georgett_picture_prefix + "5.jpg"
    vscene scene_runtime.picture
    menu:
        "Дальше":
            pass
    $ scene_runtime.picture = _church_georgett_picture_prefix + "6.jpg"
    vscene scene_runtime.picture
    menu:
        "Вернуться в собор":
            $ calendar_v2.advance_minutes(60)
            jump Church
