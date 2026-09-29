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

    if Amanda.var_value("legare_choice_outcome", "") == "service" or (Amanda.var_int("legare_choice_start_day", -1) >= 0 and not Amanda.var_value("legare_choice_outcome", "")):
        $ scene_runtime.text = "Лизетта обрывает Аманду: «Аманда, ты что, пиздой думаешь? Мы все говорили: Альбер Легаре — опасный жулик. Мы уже задумали ему отомстить, а ты всё ещё с ним? Конечно, не мне решать — пизда твоя, твоё дело, с кем трахаться. Но предать настоящих друзей ради него? Кем это тебя делает?» Аманда не находит ответа. Заметив вас, она просит пока не вмешиваться: сперва они хотят поговорить с Клариссой и узнать, чего та сама желает."
    else:
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
    $ main_ui_begin_native_scene_state("Поручение Лизетте")
    show screen main_ui
    vscene LizaStaticData.image_path("tavern", "wench_happy")
    $ scene_runtime.text = "«Да он ко мне ещё в „Пирате“ подкатывал, — смеётся Лизетта. — А так чё? Клиент да клиент и жарит неплохо», — отвечает она, кокетливо улыбаясь. «А что?»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Ответить Лизетте":
            pass

    $ scene_runtime.text = "«Хочу дать тебе ответственное поручение как члену нашего хозяйства», — доверительно шепчете вы."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к разговору":
            pass

    # Pauline's assignment is a later step; the old WineStore fight is gated.
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
