default ClaraPaintingsThreadDoc = "Clara paintings / Legare pressure / fiance investigation thread"
    $ Clara.var["trust"] = int(Clara.trust or 0)    $ Clara.var["trust"] = int(Clara.trust or 0)    $ Clara.current_location = "TavernMelissaRoom"
    $ Melissa.current_location = "TavernMelissaRoom"
    $ Melissa.location = "TavernMelissaRoom"default ClaraPaintingsThreadDoc = "Clara paintings / Legare pressure / fiance investigation thread"
    $ Clara.var["trust"] = int(Clara.trust or 0)    $ Clara.var["trust"] = int(Clara.trust or 0)    $ Clara.current_location = "TavernMelissaRoom"
    $ Melissa.current_location = "TavernMelissaRoom"
    $ Melissa.location = "TavernMelissaRoom"default ClaraPaintingsThreadDoc = "Clara paintings / Legare pressure / fiance investigation thread"
    $ Clara.var["trust"] = int(Clara.trust or 0)    $ Clara.var["trust"] = int(Clara.trust or 0)    $ Clara.current_location = "TavernMelissaRoom"
    $ Melissa.current_location = "TavernMelissaRoom"
    $ Melissa.location = "TavernMelissaRoom"# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -1 python:
    def clara_paintings_special_cream_recipe_unlocked():
        $ current_action_title = "Расследование"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться к городу", Jump("CityGuard"))]
    $ current_action_title = "Расследование"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться к городу", Jump("CityGuard"))]
    $ current_action_title = "Расследование"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться к городу", Jump("CityGuard"))]
    return int(Clara.var.get("special_cream_recipe_unlocked", 0) or 0) == 1


label story_clara_paintings_melissa_0:
    $ Clara.var["paintings_melissa_asked"] = 1
    $ Clara.var["drawings_secret_known"] = 1
    $ Melissa.var["drawings_returned"] = 1
    $ Melissa.mark_asked()
    $ Melissa.change_social(friend_delta=2, open_delta=1)
    $ MainTxt = "Вы осторожно спрашиваете Мелиссу о листках, найденных под ее кроватью. Она сначала делает вид, будто не понимает, о чем речь, но быстро сдается и смотрит на дверь, проверяя, не слышит ли вас Аманда.\n\n\"Это не мои рисунки,\" тихо отвечает она. \"Кларисса дала их мне. Иногда она такое рисует... не для всех, не за просто так, и не потому что ей скучно. Но если ты хочешь знать больше, спрашивай не меня. Я и так сказала больше, чем должна была.\"\n\nТеперь ясно, что ниточка ведет к Клариссе и ее странным делам на рынке."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Оставить девушек поговорить", Jump("TavernMelissaRoom"))]
    if thread is not None:
        $ thread.advance()
    $ current_action_title = "Цирюльня"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отойти от окна", Jump("ArtisansQuarter"))]
    $ current_action_title = "Цирюльня"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отойти от окна", Jump("ArtisansQuarter"))]
    $ current_action_title = "Цирюльня"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отойти от окна", Jump("ArtisansQuarter"))]
    return


label story_clara_paintings_cellar_1:
    show screen main_ui
    $ Clara.var["cellar_seen"] = 1
    $ Clara.var["cellar_spanking_discovered"] = 1
    $ Clara.var["cellar_seen"] = 1
    $ Clara.var["cellar_spanking_discovered"] = 1
    $ Clara.var["cellar_seen"] = 1
    $ Clara.var["cellar_spanking_discovered"] = 1
    $ Clara.var["cellar_seen"] = 1
    $ Clara.var["cellar_spanking_discovered"] = 1
    $ MainTxt = "Из дальнего подвала винной лавки доносится резкий голос Легаре. Вы останавливаетесь у стеллажей и слышите, как он отчитывает Клариссу за проваленную затею с Мелиссой и Амандой. Его слова звучат не как отцовская забота, а как холодный расчет человека, который привык распоряжаться чужими слабостями.\n\nПотом раздается короткий хлопок ладони по ткани, и Кларисса сдавленно выдыхает. Легаре зло напоминает ей, что уже много раз говорил: в нужный момент благовоспитанные дамы должны выглядеть так, будто лишняя скромность им только мешает.\n\nВы можете ворваться сейчас, но тогда Легаре точно станет вашим врагом. Можно отступить и поговорить с Клариссой позже, когда она сама сможет сказать больше."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Винный подвал"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Ворваться и поставить Легаре на место", Call("story_clara_paintings_confront_legare")),
        MenuItem("Отступить и поддержать Клариссу позже", Call("story_clara_paintings_wait_comfort")),
    ]
    call IntClaraTalkMenu("clara")
    menu:
        "Дать ей прийти в себя":
            call IntClaraTalkMenu("clara")
    call IntClaraTalkMenu("clara")
    menu:
        "Дать ей прийти в себя":
            call IntClaraTalkMenu("clara")
    call IntClaraTalkMenu("clara")
    menu:
        "Дать ей прийти в себя":
            call IntClaraTalkMenu("clara")
    return


label story_clara_paintings_confront_legare:
    show screen main_ui
    $ Clara.var["cellar_confronted"] = 1
    $ Clara.var["cellar_confronted"] = 1
    $ Clara.var["cellar_confronted"] = 1
    $ Clara.var["cellar_confronted"] = 1
    $ Alber.set_var_int("FightYouAmanda", 1)
    $ Alber.set_var_int("clara_paintings_enemy", 1)
    $ Amanda.set_var_int("LegareGo", max(2, Amanda.var_int("LegareGo", 0)))
    $ Clara.change_social(friend_delta=1)
    $ MainTxt = "Вы выходите из-за стеллажей и прямо говорите Легаре, что его семейные распоряжения перестали быть только семейным делом. Легаре быстро закрывает подвал за спиной Клариссы и встречает вас уже без торговой улыбки.\n\nДрака выходит короткой и злой: несколько ударов, сбитая бутылка, хруст стекла под сапогом. Легаре отступает первым, но по его лицу ясно, что теперь вы для него не помеха, а враг. Перед уходом он почти спокойно бросает, что раз вы вмешиваетесь в его дом, он займется вашим домом куда настойчивее.\n\nПохоже, он ускорит свои попытки добраться до Аманды."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Винный подвал"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в лавку", Jump("WineStore"))]
    $ current_action_title = "Винный подвал"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в лавку", Jump("WineStore"))]
    $ current_action_title = "Винный подвал"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в лавку", Jump("WineStore"))]
    python:
        try:
            thread.abort()
            findAvailableEvents(False)
        except Exception:
            pass
    return


label story_clara_paintings_wait_comfort:
    $ Clara.var["comfort_pending"] = 1
    $ MainTxt = "Вы сдерживаете первый порыв и отходите от подвала. Сейчас Кларисса слишком зажата между вами и отцом, а Легаре слишком хорошо умеет превращать чужой протест в свою пользу.\n\nЕсли поговорить с ней позже без свидетелей, можно узнать больше и не закрыть ей путь к откровенности."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Кларисса"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Договориться на вечер", Jump("WineStore"))]
    if thread is not None:
        $ thread.advance()
    return


label story_clara_paintings_comfort_2:
    $ Clara.var["comfort_done"] = 1
    $ Clara.var["second_ask_unlocked"] = 1
    $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
    $ Clara.change_social(friend_delta=1)
    $ MainTxt = "Утром Кларисса держится за прилавком слишком ровно. Вы не давите, просто говорите, что слышали достаточно, чтобы понять: она не одна во всем этом.\n\nСначала она отвечает светски и холодно, но потом голос срывается. Она снова говорит о браке, который для нее уже почти решен в столице, и о надежде, что отец еще передумает. Когда вы спрашиваете, не отсюда ли были все странные поручения, поездки и разговоры о лошадях, Кларисса бледнеет и признает: часть этого правда шла по отцовскому расчету.\n\n\"Я сопротивлялась как могла,\" тихо говорит она. \"Я думала, он изменит решение, если увидит, что я полезна не только как товар для чужого договора. Но он не меняется. Он просто называет это заботой.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Кларисса"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Кивнуть и не продолжать при людях", Jump("TavernMain"))]
    if thread is not None:
        $ thread.advance()
    return


label story_clara_paintings_second_ask_3:
    $ Clara.var["source_known"] = 1
    $ Clara.var["sex_engine_unlocked"] = 1
    $ Clara.var["necking_unlocked"] = 1
    $ Clara.var["petting_unlocked"] = 1
    $ Clara.var["source_known"] = 1
    $ Clara.var["sex_engine_unlocked"] = 1
    $ Clara.var["necking_unlocked"] = 1
    $ Clara.var["petting_unlocked"] = 1
    $ Clara.var["source_known"] = 1
    $ Clara.var["sex_engine_unlocked"] = 1
    $ Clara.var["necking_unlocked"] = 1
    $ Clara.var["petting_unlocked"] = 1
    $ Clara.var["source_known"] = 1
    $ Clara.var["sex_engine_unlocked"] = 1
    $ Clara.var["necking_unlocked"] = 1
    $ Clara.var["petting_unlocked"] = 1
    $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
    $ Clara.change_social(open_delta=2)
    $ MainTxt = "Когда вы второй раз возвращаетесь к теме рисунков, Кларисса уже не отшучивается. Она признает, что иногда делает портреты для знатных заказчиков, а иногда видит куда больше, чем люди думают.\n\n\"Многие любят, когда их рисуют красивее, смелее или опаснее, чем они есть,\" говорит она. \"А некоторые забывают, что художник сначала смотрит. Я делаю вид, будто вижу только позу и ткань, но на самом деле замечаю взгляды, тайные жесты, встречи за дверью. Оттуда и берутся сюжеты.\"\n\nТеперь между вами появляется другое доверие: не только разговорное, но и телесное. Кларисса уже понимает, что вы знаете ее тайну и не собираетесь использовать ее против нее."
    $ CurLocDesc = MainTxt
    if thread is not None:
        $ thread.advance()
    call ChurchServiceMenu
    return


label story_clara_paintings_church_4:
    $ Clara.var["fiance_church_seen"] = 1
    $ Clara.var["fiance_seen_day"] = int(calendar_v2.daysInGame or 0)
    $ Clara.var["fiance_church_seen"] = 1
    $ Clara.var["fiance_seen_day"] = int(calendar_v2.daysInGame or 0)
    $ Clara.var["fiance_church_seen"] = 1
    $ Clara.var["fiance_seen_day"] = int(calendar_v2.daysInGame or 0)
    $ Clara.var["fiance_church_seen"] = 1
    $ Clara.var["fiance_seen_day"] = int(current_game_day() or 0)
    $ MainTxt = "У колонны рядом с семьей Легаре сегодня стоит незнакомый молодой дворянин из столицы. Кларисса держится рядом с ним так ровно, что это выглядит почти болезненно. Легаре, напротив, доволен: он представляет гостя как человека из хорошего дома и будущего союзника семьи.\n\nКларисса не произносит слова \"жених\", но оно и так висит между ними. Теперь понятно, что столичная договоренность уже не слух и не отдаленная угроза."
    $ CurLocDesc = MainTxt
    if thread is not None:
        $ thread.advance()
    call IntClaraTalkMenu("clara")
    return


label story_clara_paintings_barber_5:
    $ Clara.var["fiance_barber_seen"] = 1
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
    if thread is not None:
        $ thread.advance()
    return


label story_clara_paintings_barber_peek:
    show screen main_ui
    $ Clara.var["fiance_barber_secret_seen"] = 1
    $ Clara.var["fiance_barber_secret_seen"] = 1
    $ Clara.var["fiance_barber_secret_seen"] = 1
    $ Clara.var["fiance_barber_secret_seen"] = 1
    $ MainTxt = "Вы находите узкую щель между ставней и рамой. Внутри Серджио и столичный гость говорят совсем не как мастер и клиент. Слишком много тишины между фразами, слишком много осторожных прикосновений, слишком мало страха быть понятыми друг другом.\n\nДеталей вам хватает, чтобы понять главное: будущий брак Клариссы держится на лжи с обеих сторон. Этот материал может стать для нее оружием, если использовать его осторожно."
    $ CurLocDesc = MainTxt
    menu:
        "Отойти от окна":
            jump ArtisansQuarter


label story_clara_paintings_commission_6:
    $ Clara.var["commission_started"] = 1
    $ Clara.var["commission_followup_day"] = int(current_game_day() or 0) + 1
    $ MainTxt = "Когда Кларисса заглядывает в трактир, вы тихо говорите ей, что у вас появился материал, который стоит зарисовать. Она сперва настораживается, но, услышав про столичного жениха и цирюльню, становится совершенно серьезной.\n\n\"Не здесь,\" отвечает она. \"Завтра утром зайди в лавку. Если это правда, мне нужно понять, как показать это так, чтобы не выглядеть просто мстительной дурой.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Кларисса"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Дать ей прийти в себя", Call("IntClaraTalkMenu", "clara"))]
    if thread is not None:
        $ thread.advance()
    return


label story_clara_paintings_commission_followup_7:
    $ Clara.var["commission_followup_done"] = 1
    $ MainTxt = "Утром в винной лавке Кларисса сразу понимает, зачем вы пришли. Вы пересказываете ей все без лишних украшений. Она не перебивает, только сжимает пальцы на краю стойки.\n\n\"Вечером,\" решает она наконец. \"Если я увижу сама, я смогу нарисовать не слух, а правду. И тогда отецу будет куда сложнее продать меня за красивую столичную легенду.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Винная лавка"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Уйти", Jump("WineStore"))]
    if thread is not None:
        $ thread.advance()
    return


label story_clara_paintings_evening_peek_8:
    $ Clara.var["peek_done"] = 1
    $ Clara.var["murder_day"] = int(current_game_day() or 0) + 1
    $ MainTxt = "Вечером вы с Клариссой держитесь в тени напротив цирюльни. Когда боковая дверь снова открывается, она успевает увидеть достаточно: столичного жениха, Серджио, их осторожные жесты и ту особую близость, которую нельзя объяснить случайным визитом.\n\nКларисса сперва каменеет, потом почти злится на себя за облегчение. \"Значит, он тоже живет не той жизнью, которую ему продают,\" шепчет она. \"А меня собирались сделать ширмой для чужих приличий.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Вечерняя слежка"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отвести Клариссу к Мелиссе", Jump("TavernMelissaRoom"))]
    if thread is not None:
        $ thread.advance()
    return


label story_clara_paintings_confession_9:
    $ Clara.var["confession_done"] = 1
    $ Clara.var["drawings_betrayal_confessed"] = 1
    $ Clara.change_social(friend_delta=2)
    $ Melissa.change_social(friend_delta=1)
    $ MainTxt = "В комнате Мелиссы Кларисса наконец срывается. Она говорит быстро, будто боится остановиться: про отцовские расчеты, про рисунки, про то, как пыталась использовать чужие тайны, чтобы получить хоть немного свободы.\n\nМелисса слушает мрачно, но не перебивает. Когда Кларисса доходит до того, что использовала доверие подруг, она уже почти плачет.\n\n\"Простите,\" говорит она вам обоим. \"Я предала хороших друзей, потому что решила, будто если сама стану хитрее, меня перестанут продавать как вещь. Но от этого я только стала похожа на тех, от кого хотела сбежать.\"\n\nПосле этого в комнате становится тяжелее, но честнее. Теперь Кларисса больше не прячется за одной только игрой."
    $ CurLocDesc = MainTxt
    python:
        try:
            findAvailableEvents(False)
        except Exception:
            pass
    if thread is not None:
        $ thread.advance()
    call IntMelissaTalkRefresh("melissa")
    return


label story_clara_paintings_murder_10:
    $ Clara.var["murder_seen"] = 1
    $ MainTxt = "У караулки шумно: стражники переговариваются вполголоса, а десятник Циммерман выглядит куда серьезнее обычного. Столичный жених Клариссы найден мертвым.\n\nЦиммерман не спешит называть виновного. Вместо этого он бросает вам странную загадку: \"Кто режет ближе всех, но держит лезвие чистым? Кто слышит тайны, но продает только видимость порядка? Ответишь верно - помогу тебе разобраться и сам.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Расследование"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Ответить: цирюльник держит лезвие, но не обязательно вину", Call("story_clara_paintings_solve_murder")),
        MenuItem("Промолчать и уйти", Jump("CityGuard")),
    ]
    if thread is not None:
        $ thread.advance()
    return


label story_clara_paintings_solve_murder:
    show screen main_ui
    $ Clara.var["murder_solved"] = 1
    $ Clara.var["murder_solved"] = 1
    $ Clara.var["murder_solved"] = 1
    $ Clara.var["murder_solved"] = 1
    $ Clara.var["special_cream_recipe_unlocked"] = 1
    $ Clara.var["sergio_discount"] = 25
    $ Zimmer.var["ClaraFianceCaseSolved"] = 1
    $ tavernfame = int(tavernfame or 0) + 3
    $ Clara.change_social(friend_delta=2)
    $ MainTxt = "Вы отвечаете, что Серджио слишком очевиден как человек с лезвием, а значит, слишком удобен как подозреваемый. Настоящий ответ прячется не в бритве, а в том, кому выгодно было убрать жениха именно сейчас.\n\nЦиммерман долго смотрит на вас, потом коротко кивает. Серджио отпускают из-под подозрения, а город начинает судачить, что хозяин \"Дикого Жеребца\" умеет видеть дальше прямой улики.\n\nПозже Серджио передает вам рецепт особой смягчающей мази и обещает обслуживать вас и ваших работниц со скидкой в четверть цены. Рецепт теперь можно найти в книге рецептов, если открыть список доступных приготовлений."
    $ CurLocDesc = MainTxt
    $ Clara.var["anal_unlocked"] = 1
    $ Clara.var["virginity_choice_unlocked"] = 1
    menu:
        "Вернуться к городу":
            jump CityGuard
