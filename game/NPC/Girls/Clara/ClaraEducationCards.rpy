# The existing education thread owns progress. These are alternative events
# within its first step, not additional cursors or parallel completion flags.
# A two-number list is a RANGE in Event.checkDay. Ren'Py's store range produces
# a list, so use the builtin range to select only Monday and Saturday.
define claraEducationCardsEvent = Event((
    "story_clara_tavern_education_cards_0",
    builtins.range(1, 7, 5), (20, 23), None,
    1, None,
    ["#not Clara.mongol_case_detained()", "#not Clara.fiance_case_detained()",
     "#not Clara.sex_busy()", "#not Melissa.sex_busy()", "#not Amanda.sex_busy()"],
    None, "MarketPlace", "enter", 0, True,
), "claraTavernEducation", True)

define claraEducationWhispersEvent = Event((
    "story_clara_education_whispers",
    claraEducationCardsEvent.day, (19, 19), None,
    1, None, claraEducationCardsEvent.condStr,
    None, "TavernMain", "enter", 0,
), "claraTavernEducation", True)

define claraEducationAbsenceEvent = Event((
    "story_clara_education_absence",
    claraEducationCardsEvent.day, claraEducationCardsEvent.hour, None,
    1, None, claraEducationCardsEvent.condStr,
    None, "TavernMain", "enter", 0,
), "claraTavernEducation", True)

init 10 python:
    def clara_education_cards_pending():
        lesson = threads["claraTavernEducation"]
        return lesson.num == 0 and lesson.checkActive() and claraEducationCardsEvent.checkConditions()

    # Schedule projections use the event's actual weekdays/hours and existing
    # thread state. No temporary-location flags, saved callbacks or daily reset.
    for _education_event, _education_location in (
        (claraEducationWhispersEvent, "TavernMain"),
        (claraEducationCardsEvent, "WineStoreBasement"),
    ):
        for _education_data in (ClaraStaticData, MelissaStaticData, AmandaStaticData):
            _education_data.add_schedule_entry(NPCScheduleEntry(
                location=_education_location,
                weekdays=list(_education_event.day),
                start_hour=_education_event.hour[0],
                end_hour=_education_event.hour[1] + 1,
                awake=True,
                talkable=False,
                # This planned outing overrides the 23:00 bedtime (900/910),
                # but not the higher-priority health schedule (950).
                priority=925,
                label="clara_card_lesson",
                condition=clara_education_cards_pending,
            ))


# An optional clue, once per eligible evening. It does not consume the lesson.
label story_clara_education_whispers:
    $ main_ui_begin_native_scene_state("Шёпот в углу")
    show screen main_ui
    vscene rooms.get("TavernMain").bg_picture
    $ scene_runtime.text = "В дальнем углу зала Кларисса, Мелисса и Аманда о чём-то шепчутся. Кларисса прячет в ладони колоду карт; Аманда бросает на вас озорной взгляд, и все трое едва сдерживают смешки. Заметив, что вы смотрите в их сторону, девушки разом принимают самый невинный вид."
    menu:
        "Заняться своими делами":
            pass
    $ main_ui_end_native_scene_state()
    return True


label story_clara_education_absence:
    $ main_ui_begin_native_scene_state("Куда подевались девушки?")
    show screen main_ui
    vscene rooms.get("TavernMain").bg_picture
    $ scene_runtime.text = "Вечер в трактире ещё не закончился, а Клариссы, Мелиссы и Аманды нигде в зале не видно. Похоже, на сегодня у них были свои планы."
    if story_event_fired_today(claraEducationWhispersEvent):
        $ scene_runtime.text += " Вы вспоминаете их заговорщический шёпот и смешки."
    menu:
        "Продолжить вечер":
            pass
    $ main_ui_end_native_scene_state()
    return True


# Observer event: MC remains outside on the Market. Each picture/paragraph has
# an explicit native choice. Leaving does not complete the lesson or strand MC.
label story_clara_tavern_education_cards_0:
    $ main_ui_begin_native_scene_state("Свет за винной лавкой")
    show screen main_ui
    vscene MARKETPLACE_CLOSED_PICTURE
    $ scene_runtime.text = "Рынок опустел. Ставни лавок закрыты, последние торговцы давно разошлись. Но возле винного погребка вы замечаете что-то странное: из-за угла ложится на мостовую узкая полоска света, и оттуда доносится приглушённый смех."
    menu:
        "Пойти проверить":
            pass
        "Не вмешиваться":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/general/closedVenue default.png"
    $ scene_runtime.text = "Дверь винной лавки закрыта. За ставнями темно, однако свет идёт не из торгового зала, а откуда-то ниже. За углом, со стороны подвала, вновь слышатся голоса."
    menu:
        "Обойти лавку":
            pass
        "Вернуться на рынок":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/basement_window_night.png"
    $ scene_runtime.text = "Позади лавки, почти у самой земли, находится небольшое подвальное окно. Створка приоткрыта, и свет свечей падает на камни. Вы узнаёте голоса Клариссы, Мелиссы и Аманды. Отсюда можно заглянуть внутрь, не входя в закрытую лавку."
    menu:
        "Заглянуть в окно":
            pass
        "Вернуться на рынок":
            $ main_ui_end_native_scene_state()
            return True

    $ main_ui_runtime.action_title = "Урок карт Клариссы"
    vscene "images/clara/education/cardplay0.jpg"
    $ scene_runtime.text = "За столом между винными бочками сидят Кларисса, Мелисса и Аманда. Кларисса раздаёт карты: «Для начала запомните: смотреть надо не только в свою руку. Соперница иногда расскажет вам всё одним выражением лица». Вы остаётесь у окна."
    menu:
        "Продолжить наблюдать":
            pass
        "Уйти":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/cardplay1.jpg"
    $ scene_runtime.text = "«А если у меня совсем плохие карты?» — спрашивает Аманда. «Тогда особенно не надо объявлять об этом на весь подвал», — отвечает Кларисса. Мелисса прыскает, а Аманда торопливо прячет улыбку за веером карт."
    menu:
        "Продолжить наблюдать":
            pass
        "Уйти":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/cardplay2.jpg"
    $ scene_runtime.text = "Мелисса прищуривается: «Ты объяснила правила не все сразу». Кларисса кладёт ладонь на колоду: «Правила для всех одинаковые. Спрашивать можно сколько угодно — только до того, как сделала ход». «Вот ведь учительница!» — смеётся Аманда."
    menu:
        "Продолжить наблюдать":
            pass
        "Уйти":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/cardplay3.jpg"
    $ scene_runtime.text = "«Не торопись, Аманда. Она нарочно тебя подзадоривает», — предупреждает Мелисса. «А ты нарочно мне мешаешь!» Кларисса тихо смеётся: «Вот теперь вы начинаете понимать: за столом играют и картами, и словами»."
    menu:
        "Продолжить наблюдать":
            pass
        "Уйти":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/cardplay4.jpg"
    $ scene_runtime.text = "Карты ложатся на стол. На мгновение в подвале становится тихо, а затем Аманда возмущённо вскрикивает: «Да откуда у тебя опять такая рука?» «Из той же колоды, что и у тебя», — невозмутимо отвечает Кларисса. Мелисса хохочет так, что ей приходится придержать кружку."
    menu:
        "Продолжить наблюдать":
            pass
        "Уйти":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/cardplay5.jpg"
    $ scene_runtime.text = "«Следующая сдача моя», — объявляет Мелисса и забирает колоду. Аманда немедленно придвигается: «А я прослежу, чтобы всё было честно». Кларисса разводит руками: «Прошу. Но на этот раз не показывайте друг другу карты, когда спорите»."
    menu:
        "Продолжить наблюдать":
            pass
        "Уйти":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/cardplay6.jpg"
    $ scene_runtime.text = "Аманда долго смотрит на Клариссу и вдруг довольно кивает: «Ты улыбаешься, когда блефуешь». «Правда?» Кларисса улыбается ещё шире. Мелисса качает головой: «Вот теперь она будет улыбаться всё время, а ты опять ничего не поймёшь»."
    menu:
        "Продолжить наблюдать":
            pass
        "Уйти":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/cardplay7.jpg"
    $ scene_runtime.text = "Новая сдача оборачивается таким спором, что Кларисса стучит костяшками пальцев по столу: «По очереди! Сначала ход Мелиссы». «Слышала? Я ещё могу выиграть!» — торжествует та. Аманда отвечает смешком: «Сначала выиграй, потом хвастайся»."
    menu:
        "Продолжить наблюдать":
            pass
        "Уйти":
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/education/cardplay8.jpg"
    $ scene_runtime.text = "Кларисса собирает карты: «На сегодня хватит. Главное вы поняли: следите за игрой и не выдавайте себя раньше времени». «А реванш?» — разом спрашивают Аманда и Мелисса, после чего снова смеются. Вы тихо отступаете от окна, оставляя их заканчивать вечер."
    menu:
        "Закончить наблюдение и вернуться на рынок":
            pass
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ main_ui_end_native_scene_state()
    return True
