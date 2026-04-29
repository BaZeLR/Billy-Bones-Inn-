# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default ClaraPaintingsThreadDoc = "Clara paintings / Legare pressure / fiance investigation thread"

init -1 python:
    def clara_paintings_flag(name, default=0):
        try:
            return int(ClaraVar.get(str(name or ""), default) or default)
        except Exception:
            return default

    def clara_paintings_set(name, value=1):
        ClaraVar[str(name or "")] = value

    def clara_paintings_melissa_question_ready():
        return (
            int(MelissaVar.get("drawings_found", 0) or 0) == 1
            and clara_paintings_flag("paintings_melissa_asked", 0) == 0
        )

    def clara_paintings_cellar_ready():
        return (
            clara_paintings_flag("paintings_melissa_asked", 0) == 1
            and clara_paintings_flag("cellar_seen", 0) == 0
            and int(ClaraVar.get("flirt", 0) or 0) > 0
            and str(_story_current_location() or "") == "WineStore"
            and int(time or 0) in (1, 2)
        )

    def clara_paintings_comfort_ready():
        return (
            clara_paintings_flag("comfort_pending", 0) == 1
            and clara_paintings_flag("comfort_done", 0) == 0
            and str(getLocation("clara") or "") == "WineStore"
            and int(time or 0) == 0
        )

    def clara_paintings_second_ask_ready():
        return (
            clara_paintings_flag("second_ask_unlocked", 0) == 1
            and clara_paintings_flag("source_known", 0) == 0
        )

    def clara_paintings_church_fiance_ready():
        return (
            clara_paintings_flag("source_known", 0) == 1
            and clara_paintings_flag("fiance_church_seen", 0) == 0
            and int(week or 0) == 7
            and int(time or 0) <= 2
        )

    def clara_paintings_barber_fiance_ready():
        if clara_paintings_flag("fiance_church_seen", 0) != 1:
            return False
        if clara_paintings_flag("fiance_barber_seen", 0) == 1:
            return False
        if str(_story_current_location() or "") != "BarberShop":
            return False
        if int(time or 0) == 0:
            return True
        if int(time or 0) >= 4:
            today = int(dayspassed or 0)
            if clara_paintings_flag("fiance_barber_night_roll_day", -1) != today:
                ClaraVar["fiance_barber_night_roll_day"] = today
                try:
                    ClaraVar["fiance_barber_night_roll"] = 1 if renpy.random.randint(1, 3) == 1 else 0
                except Exception:
                    ClaraVar["fiance_barber_night_roll"] = 1
            try:
                return clara_paintings_flag("fiance_barber_night_roll", 0) == 1
            except Exception:
                return True
        return False

    def clara_paintings_commission_ready():
        return (
            clara_paintings_flag("fiance_barber_seen", 0) == 1
            and clara_paintings_flag("commission_started", 0) == 0
            and str(getLocation("clara") or "") == "TavernMain"
        )

    def clara_paintings_commission_followup_ready():
        return (
            clara_paintings_flag("commission_started", 0) == 1
            and clara_paintings_flag("commission_followup_done", 0) == 0
            and int(dayspassed or 0) >= clara_paintings_flag("commission_followup_day", 999999)
            and str(getLocation("clara") or "") == "WineStore"
            and int(time or 0) == 0
        )

    def clara_paintings_evening_peek_ready():
        return (
            clara_paintings_flag("commission_followup_done", 0) == 1
            and clara_paintings_flag("peek_done", 0) == 0
            and str(getLocation("clara") or "") == "WineStore"
            and int(time or 0) == 3
        )

    def clara_paintings_confession_ready():
        return (
            clara_paintings_flag("peek_done", 0) == 1
            and clara_paintings_flag("confession_done", 0) == 0
            and str(getLocation("clara") or "") == "TavernMelissaRoom"
            and str(getLocation("melissa") or "") == "TavernMelissaRoom"
        )

    def clara_paintings_murder_ready():
        return (
            clara_paintings_flag("confession_done", 0) == 1
            and clara_paintings_flag("murder_seen", 0) == 0
            and int(dayspassed or 0) >= clara_paintings_flag("murder_day", 999999)
            and str(_story_current_location() or "") == "CityGuard"
        )

    def clara_paintings_special_cream_recipe_unlocked():
        return clara_paintings_flag("special_cream_recipe_unlocked", 0) == 1

    def clara_paintings_tavern_caption():
        if clara_paintings_commission_ready():
            return "Сказать Клариссе, что у вас есть материал для рисунка"
        return "Поговорить с Клариссой о рисунках"

    def clara_paintings_wine_caption():
        if clara_paintings_cellar_ready():
            return "Спуститься на шум в подвале"
        if clara_paintings_comfort_ready():
            return "Поддержать Клариссу после разговора с отцом"
        if clara_paintings_commission_followup_ready():
            return "Обсудить с Клариссой материал для рисунка"
        if clara_paintings_evening_peek_ready():
            return "Проверить лавку вместе с Клариссой вечером"
        return "Поговорить о рисунках"


label story_clara_paintings_melissa_0:
    call preEvent("claraPaintingsPath")
    $ ClaraVar["paintings_melissa_asked"] = 1
    $ ClaraVar["drawings_secret_known"] = 1
    $ MelissaVar["drawings_returned"] = 1
    $ AskedToday["melissa"] = int(AskedToday.get("melissa", 0) or 0) + 1
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 2)
    $ otkroven["melissa"] = min(20, int(otkroven.get("melissa", 0) or 0) + 1)
    $ MainTxt = "Вы осторожно спрашиваете Мелиссу о листках, найденных под ее кроватью. Она сначала делает вид, будто не понимает, о чем речь, но быстро сдается и смотрит на дверь, проверяя, не слышит ли вас Аманда.\n\n\"Это не мои рисунки,\" тихо отвечает она. \"Кларисса дала их мне. Иногда она такое рисует... не для всех, не за просто так, и не потому что ей скучно. Но если ты хочешь знать больше, спрашивай не меня. Я и так сказала больше, чем должна была.\"\n\nТеперь ясно, что ниточка ведет к Клариссе и ее странным делам на рынке."
    $ CurLocDesc = MainTxt
    python:
        try:
            evalTime = None
            findAvailableEvents(True)
        except Exception:
            pass
    $ story_thread_advance_current()
    call IntMelissaTalkRefresh("melissa")
    return


label story_clara_paintings_cellar_1:
    $ ClaraVar["cellar_seen"] = 1
    $ ClaraVar["cellar_spanking_discovered"] = 1
    $ MainTxt = "Из дальнего подвала винной лавки доносится резкий голос Легаре. Вы останавливаетесь у стеллажей и слышите, как он отчитывает Клариссу за проваленную затею с Мелиссой и Амандой. Его слова звучат не как отцовская забота, а как холодный расчет человека, который привык распоряжаться чужими слабостями.\n\nПотом раздается короткий хлопок ладони по ткани, и Кларисса сдавленно выдыхает. Легаре зло напоминает ей, что уже много раз говорил: в нужный момент благовоспитанные дамы должны выглядеть так, будто лишняя скромность им только мешает.\n\nВы можете ворваться сейчас, но тогда Легаре точно станет вашим врагом. Можно отступить и поговорить с Клариссой позже, когда она сама сможет сказать больше."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Винный подвал"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Ворваться и поставить Легаре на место", Call("story_clara_paintings_confront_legare")),
        MenuItem("Отступить и поддержать Клариссу позже", Call("story_clara_paintings_wait_comfort")),
    ]
    return


label story_clara_paintings_confront_legare:
    $ ClaraVar["cellar_confronted"] = 1
    $ AlberVar["FightYouAmanda"] = 1
    $ AlberVar["clara_paintings_enemy"] = 1
    $ AmandaVar["LegareGo"] = max(2, int(AmandaVar.get("LegareGo", 0) or 0))
    $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + 1)
    $ MainTxt = "Вы выходите из-за стеллажей и прямо говорите Легаре, что его семейные распоряжения перестали быть только семейным делом. Легаре быстро закрывает подвал за спиной Клариссы и встречает вас уже без торговой улыбки.\n\nДрака выходит короткой и злой: несколько ударов, сбитая бутылка, хруст стекла под сапогом. Легаре отступает первым, но по его лицу ясно, что теперь вы для него не помеха, а враг. Перед уходом он почти спокойно бросает, что раз вы вмешиваетесь в его дом, он займется вашим домом куда настойчивее.\n\nПохоже, он ускорит свои попытки добраться до Аманды."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Винный подвал"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в лавку", Jump("WineStore"))]
    python:
        try:
            thread.abort()
            globals()["evalTime"] = None
            findAvailableEvents(True)
        except Exception:
            pass
    return


label story_clara_paintings_wait_comfort:
    $ ClaraVar["comfort_pending"] = 1
    $ MainTxt = "Вы сдерживаете первый порыв и отходите от подвала. Сейчас Кларисса слишком зажата между вами и отцом, а Легаре слишком хорошо умеет превращать чужой протест в свою пользу.\n\nЕсли поговорить с ней позже без свидетелей, можно узнать больше и не закрыть ей путь к откровенности."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Винная лавка"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Уйти", Jump("WineStore"))]
    $ story_thread_advance_current()
    return


label story_clara_paintings_comfort_2:
    call preEvent("claraPaintingsPath")
    $ ClaraVar["comfort_done"] = 1
    $ ClaraVar["second_ask_unlocked"] = 1
    $ ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 2)
    $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + 1)
    $ MainTxt = "Утром Кларисса держится за прилавком слишком ровно. Вы не давите, просто говорите, что слышали достаточно, чтобы понять: она не одна во всем этом.\n\nСначала она отвечает светски и холодно, но потом голос срывается. Она снова говорит о браке, который для нее уже почти решен в столице, и о надежде, что отец еще передумает. Когда вы спрашиваете, не отсюда ли были все странные поручения, поездки и разговоры о лошадях, Кларисса бледнеет и признает: часть этого правда шла по отцовскому расчету.\n\n\"Я сопротивлялась как могла,\" тихо говорит она. \"Я думала, он изменит решение, если увидит, что я полезна не только как товар для чужого договора. Но он не меняется. Он просто называет это заботой.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Кларисса"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Дать ей прийти в себя", Call("IntClaraTalkRefresh", "clara"))]
    $ story_thread_advance_current()
    return


label story_clara_paintings_second_ask_3:
    call preEvent("claraPaintingsPath")
    $ ClaraVar["source_known"] = 1
    $ ClaraVar["sex_engine_unlocked"] = 1
    $ ClaraVar["necking_unlocked"] = 1
    $ ClaraVar["petting_unlocked"] = 1
    $ ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 2)
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + 2)
    $ MainTxt = "Когда вы второй раз возвращаетесь к теме рисунков, Кларисса уже не отшучивается. Она признает, что иногда делает портреты для знатных заказчиков, а иногда видит куда больше, чем люди думают.\n\n\"Многие любят, когда их рисуют красивее, смелее или опаснее, чем они есть,\" говорит она. \"А некоторые забывают, что художник сначала смотрит. Я делаю вид, будто вижу только позу и ткань, но на самом деле замечаю взгляды, тайные жесты, встречи за дверью. Оттуда и берутся сюжеты.\"\n\nТеперь между вами появляется другое доверие: не только разговорное, но и телесное. Кларисса уже понимает, что вы знаете ее тайну и не собираетесь использовать ее против нее."
    $ CurLocDesc = MainTxt
    $ story_thread_advance_current()
    call IntClaraTalkRefresh("clara")
    return


label story_clara_paintings_church_4:
    call preEvent("claraPaintingsPath")
    $ ClaraVar["fiance_church_seen"] = 1
    $ ClaraVar["fiance_seen_day"] = int(dayspassed or 0)
    $ MainTxt = "У колонны рядом с семьей Легаре сегодня стоит незнакомый молодой дворянин из столицы. Кларисса держится рядом с ним так ровно, что это выглядит почти болезненно. Легаре, напротив, доволен: он представляет гостя как человека из хорошего дома и будущего союзника семьи.\n\nКларисса не произносит слова \"жених\", но оно и так висит между ними. Теперь понятно, что столичная договоренность уже не слух и не отдаленная угроза."
    $ CurLocDesc = MainTxt
    $ story_thread_advance_current()
    call ChurchServiceMenu
    return


label story_clara_paintings_barber_5:
    $ ClaraVar["fiance_barber_seen"] = 1
    if int(time or 0) == 0:
        $ MainTxt = "Утром у цирюльни вы замечаете того самого столичного жениха. Он выходит от Серджио слишком быстро и слишком аккуратно поправляет перчатки, будто не хочет, чтобы его здесь запомнили."
        $ current_action_items = [MenuItem("Запомнить это", Jump("ArtisansQuarter"))]
    else:
        $ MainTxt = "Поздно вечером у закрытой цирюльни мелькает знакомая фигура. Столичный жених Клариссы входит через боковую дверь, а Серджио впускает его без лишних слов."
        $ current_action_items = [MenuItem("Уйти, пока вас не заметили", Jump("ArtisansQuarter"))]
        if int(exploration or 0) >= 200:
            $ current_action_items.insert(0, MenuItem("Осторожно заглянуть внутрь", Call("story_clara_paintings_barber_peek")))
    $ CurLocDesc = MainTxt
    $ current_action_title = "Цирюльня"
    $ current_action_content = None
    $ story_thread_advance_current()
    return


label story_clara_paintings_barber_peek:
    $ ClaraVar["fiance_barber_secret_seen"] = 1
    $ MainTxt = "Вы находите узкую щель между ставней и рамой. Внутри Серджио и столичный гость говорят совсем не как мастер и клиент. Слишком много тишины между фразами, слишком много осторожных прикосновений, слишком мало страха быть понятыми друг другом.\n\nДеталей вам хватает, чтобы понять главное: будущий брак Клариссы держится на лжи с обеих сторон. Этот материал может стать для нее оружием, если использовать его осторожно."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Цирюльня"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отойти от окна", Jump("ArtisansQuarter"))]
    return


label story_clara_paintings_commission_6:
    $ ClaraVar["commission_started"] = 1
    $ ClaraVar["commission_followup_day"] = int(dayspassed or 0) + 1
    $ MainTxt = "Когда Кларисса заглядывает в трактир, вы тихо говорите ей, что у вас появился материал, который стоит зарисовать. Она сперва настораживается, но, услышав про столичного жениха и цирюльню, становится совершенно серьезной.\n\n\"Не здесь,\" отвечает она. \"Завтра утром зайди в лавку. Если это правда, мне нужно понять, как показать это так, чтобы не выглядеть просто мстительной дурой.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Кларисса"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Кивнуть и не продолжать при людях", Call("TavernMainRestore"))]
    $ story_thread_advance_current()
    return


label story_clara_paintings_commission_followup_7:
    $ ClaraVar["commission_followup_done"] = 1
    $ MainTxt = "Утром в винной лавке Кларисса сразу понимает, зачем вы пришли. Вы пересказываете ей все без лишних украшений. Она не перебивает, только сжимает пальцы на краю стойки.\n\n\"Вечером,\" решает она наконец. \"Если я увижу сама, я смогу нарисовать не слух, а правду. И тогда отецу будет куда сложнее продать меня за красивую столичную легенду.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Кларисса"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Договориться на вечер", Jump("WineStore"))]
    $ story_thread_advance_current()
    return


label story_clara_paintings_evening_peek_8:
    $ ClaraVar["peek_done"] = 1
    $ ClaraVar["murder_day"] = int(dayspassed or 0) + 1
    $ MainTxt = "Вечером вы с Клариссой держитесь в тени напротив цирюльни. Когда боковая дверь снова открывается, она успевает увидеть достаточно: столичного жениха, Серджио, их осторожные жесты и ту особую близость, которую нельзя объяснить случайным визитом.\n\nКларисса сперва каменеет, потом почти злится на себя за облегчение. \"Значит, он тоже живет не той жизнью, которую ему продают,\" шепчет она. \"А меня собирались сделать ширмой для чужих приличий.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Вечерняя слежка"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отвести Клариссу к Мелиссе", Jump("TavernMelissaRoom"))]
    $ story_thread_advance_current()
    return


label story_clara_paintings_confession_9:
    $ ClaraVar["confession_done"] = 1
    $ ClaraVar["drawings_betrayal_confessed"] = 1
    $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + 2)
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
    $ MainTxt = "В комнате Мелиссы Кларисса наконец срывается. Она говорит быстро, будто боится остановиться: про отцовские расчеты, про рисунки, про то, как пыталась использовать чужие тайны, чтобы получить хоть немного свободы.\n\nМелисса слушает мрачно, но не перебивает. Когда Кларисса доходит до того, что использовала доверие подруг, она уже почти плачет.\n\n\"Простите,\" говорит она вам обоим. \"Я предала хороших друзей, потому что решила, будто если сама стану хитрее, меня перестанут продавать как вещь. Но от этого я только стала похожа на тех, от кого хотела сбежать.\"\n\nПосле этого в комнате становится тяжелее, но честнее. Теперь Кларисса больше не прячется за одной только игрой."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Оставить девушек поговорить", Call("TavernMelissaRoomRestore"))]
    $ story_thread_advance_current()
    return


label story_clara_paintings_murder_10:
    $ ClaraVar["murder_seen"] = 1
    $ MainTxt = "У караулки шумно: стражники переговариваются вполголоса, а десятник Циммерман выглядит куда серьезнее обычного. Столичный жених Клариссы найден мертвым.\n\nЦиммерман не спешит называть виновного. Вместо этого он бросает вам странную загадку: \"Кто режет ближе всех, но держит лезвие чистым? Кто слышит тайны, но продает только видимость порядка? Ответишь верно - помогу тебе разобраться и сам.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Расследование"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Ответить: цирюльник держит лезвие, но не обязательно вину", Call("story_clara_paintings_solve_murder")),
        MenuItem("Промолчать и уйти", Call("CityGuardRestore")),
    ]
    $ story_thread_advance_current()
    return


label story_clara_paintings_solve_murder:
    $ ClaraVar["murder_solved"] = 1
    $ ClaraVar["special_cream_recipe_unlocked"] = 1
    $ ClaraVar["sergio_discount"] = 25
    $ ZimmerVar["ClaraFianceCaseSolved"] = 1
    $ tavernfame = int(tavernfame or 0) + 3
    $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + 2)
    $ MainTxt = "Вы отвечаете, что Серджио слишком очевиден как человек с лезвием, а значит, слишком удобен как подозреваемый. Настоящий ответ прячется не в бритве, а в том, кому выгодно было убрать жениха именно сейчас.\n\nЦиммерман долго смотрит на вас, потом коротко кивает. Серджио отпускают из-под подозрения, а город начинает судачить, что хозяин \"Дикого Жеребца\" умеет видеть дальше прямой улики.\n\nПозже Серджио передает вам рецепт особой смягчающей мази и обещает обслуживать вас и ваших работниц со скидкой в четверть цены. Рецепт теперь можно найти в книге рецептов, если открыть список доступных приготовлений."
    $ CurLocDesc = MainTxt
    $ ClaraVar["anal_unlocked"] = 1
    $ ClaraVar["virginity_choice_unlocked"] = 1
    $ current_action_title = "Расследование"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться к городу", Call("CityGuardRestore"))]
    return
