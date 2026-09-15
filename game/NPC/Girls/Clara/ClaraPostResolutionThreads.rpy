# ================================================================================
# Clarissa's post-resolution authored events.
# The Clara-owned threads are registered in StoryEventRuntime.rpy. These labels
# own scene flow and native menus; rooms retain navigation and object ownership.
# ================================================================================

label story_clara_legare_revenge_amanda_tells_liza_0:
    $ main_ui_begin_native_scene_state("Аманда рассказывает Лизетте")
    show screen main_ui
    vscene "images/Liza/lizaNew/liza_amanda_work_talk.png"
    $ scene_runtime.text = "В главной зале Аманда отводит Лизетту в сторону и пересказывает всё, что успела узнать о Легаре: предупреждение Клариссы, его угрозы и то, как он пытался использовать девушек трактира в своих планах. В этот раз в её голосе нет обычного легкомыслия."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "Лизетта сперва сердито отвечает, что давно знала Легаре как опасного человека, но не представляла всей истории. Затем обе замечают вас. Аманда просит пока не вмешиваться: они хотят сначала поговорить с Клариссой и понять, чего та сама желает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Дать им закончить разговор":
            pass

    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ main_ui_end_native_scene_state()
    return True


label story_clara_legare_revenge_request_1:
    $ main_ui_begin_native_scene_state("Просьба Аманды и Лизетты")
    show screen main_ui
    vscene "images/amanda/liazaamandatalk.webp"
    $ scene_runtime.text = "Аманда и Лизетта подходят к вам вместе. После разговора с Клариссой обе уверены: Легаре снова попытается запугать её, если решит, что она осталась без защиты. Девушки не просят расправы исподтишка — они хотят, чтобы вы встали рядом с Клариссой, когда тот явится, и не позволили ему снова диктовать ей свою волю."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Выслушать их":
            pass

    $ scene_runtime.text = "«Он привык, что все отступают, стоит ему повысить голос», — говорит Лизетта. Аманда упрямо добавляет: «Так пусть на этот раз увидит, что Кларисса не одна». Вы обещаете разобраться с Легаре открыто, если он вновь тронет её."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пообещать защитить Клариссу":
            pass

    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ main_ui_end_native_scene_state()
    return True


label story_clara_legare_revenge_fight_2:
    $ renpy.dynamic("_clara_revenge_outcome")
    $ main_ui_begin_native_scene_state("Последняя угроза Легаре")
    show screen main_ui
    vscene "images/clara/panishment/panishment1.jpg"
    $ scene_runtime.text = "Из подвала винной лавки снова доносится голос Легаре. Он загнал Клариссу между столом и стеллажами и требует отказаться от защиты трактира. Но теперь Кларисса не склоняет голову: она прямо говорит, что больше не принадлежит ни его дому, ни его планам. Легаре делает шаг к ней — и вы выходите из-за бочек."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Встать между Клариссой и Легаре":
            pass

    $ fight_begin("legare", 1, "WineStore", "images/Alber/fight/streetdraw.jpg", "Легаре перехватывает трость и бросается на вас. На этот раз спор закончится только тогда, когда он поймёт, что Клариссу больше нельзя запугать.")
    call FightLoop
    $ _clara_revenge_outcome = str(fight.last_result.get("outcome", "") or "")

    if _clara_revenge_outcome == "victory":
        $ Alber.add_relation(-5)
        $ Clara.change_social(friend_delta=3, open_delta=1)
        $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
        $ Amanda.change_social(friend_delta=1)
        $ Liza.change_social(friend_delta=1)
        $ scene_runtime.text = "Легаре отступает, роняя трость среди разбитых бутылок. Кларисса сама открывает дверь подвала и велит ему больше не приближаться к ней без приглашения. Аманда и Лизетта ждали неподалёку; увидев Клариссу рядом с вами, они понимают, что просьба выполнена. Теперь решение принадлежит Клариссе, а не её бывшему хозяину."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Уйти вместе с Клариссой":
                pass
        $ event_runtime.active_thread.advance()
    else:
        $ Alber.add_relation(-2)
        $ scene_runtime.text = "В тесном подвале Легаре удаётся вынудить вас отступить. Кларисса вырывается следом и требует не продолжать драку сейчас. Его власть уже не вернулась, но окончательно поставить точку не удалось. Придётся прийти подготовленным в другой день."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Вернуться за Легаре в другой день":
                pass

    $ event_runtime.evaluation_time = None
    $ main_ui_end_native_scene_state()
    return True


label story_clara_tavern_education_cards_0:
    $ main_ui_begin_native_scene_state("Урок карт Клариссы")
    show screen main_ui
    vscene "images/clara/wineSellar_clara_talk_6.png"
    $ scene_runtime.text = "Кларисса собирает женщин трактира в дальнем подвале винной лавки, где никто не мешает занятию. На стол ложатся колода, несколько монет и пустые кружки. Она объясняет не только правила игры, но и то, как по ставкам, паузам и взглядам понять характер гостя."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить урок":
            pass

    $ scene_runtime.text = "Сандра быстро замечает попытки жульничать, Лизетта без труда отвлекает соперниц разговором, а Аманда с Мелиссой несколько раз выдают свои карты лицом. К концу занятия каждая уже умеет поддержать игру за столом и вовремя остановить спор, прежде чем он испортит вечер в трактире."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить занятие":
            pass

    $ Clara.change_social(friend_delta=1)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ main_ui_end_native_scene_state()
    return True


label story_clara_tavern_education_manners_1:
    $ main_ui_begin_native_scene_state("Урок хороших манер")
    show screen main_ui
    vscene "images/clara/tavern_visit.png"
    $ scene_runtime.text = "На следующем занятии Кларисса становится у стойки и показывает, как встречать состоятельного гостя без раболепия: кому предложить лучший стол, когда принести вино и как пресечь слишком вольные руки одной вежливой фразой. Сандра тут же превращает советы в понятные правила работы."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Попросить продолжить":
            pass

    $ scene_runtime.text = "Аманда упражняется в поклонах, Мелисса учится принимать сложный заказ без суеты, а Лизетта и Жоржетта добавляют к уроку собственные приёмы общения с требовательными гостями. Уже через несколько дней по городу расходится слух, что в «Диком Жеребце» умеют достойно принять не только грузчиков и матросов."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Поблагодарить Клариссу":
            pass

    python:
        for _clara_student in (Sandra, Amanda, Melissa, Liza, Georgett):
            _clara_student.skills["waitress"] = min(100, int(_clara_student.skills.get("waitress", 0) or 0) + 5)
    $ Melissa.change_social(friend_delta=1, open_delta=1)
    $ Clara.change_social(friend_delta=2, open_delta=1)
    $ player.tavern_management.visitors = max(0, int(player.tavern_management.visitors or 0) + 5)
    $ player.change_tavern_fame(3)
    $ calendar_v2.advance_minutes(60)
    call stat
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ main_ui_end_native_scene_state()
    return True
