# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label story_clara_paintings_melissa_0:
    $ main_ui_begin_native_scene_state("Рисунки Клариссы")
    show screen main_ui
    $ Clara.drawings_secret_known = True
    $ Melissa.drawings_returned = True
    $ Melissa.mark_asked()
    $ Melissa.change_social(friend_delta=2, open_delta=1)
    $ scene_runtime.text = "Вы осторожно спрашиваете Мелиссу о листках, найденных под ее кроватью. Она сначала делает вид, будто не понимает, о чем речь, но быстро сдается и смотрит на дверь, проверяя, не слышит ли вас Аманда.\n\n\"Это не мои рисунки,\" тихо отвечает она. \"Кларисса дала их мне. Иногда она такое рисует... не для всех, не за просто так, и не потому что ей скучно. Но если ты хочешь знать больше, спрашивай не меня. Я и так сказала больше, чем должна была.\"\n\nТеперь ясно, что ниточка ведет к Клариссе и ее странным делам на рынке."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_cellar_1:
    $ main_ui_begin_native_scene_state("Кларисса и Легаре")
    show screen main_ui
    vscene "images/clara/panishment/panishment1.jpg"
    $ scene_runtime.text = "Из дальнего подвала винной лавки доносится резкий голос Легаре. Вы останавливаетесь у стеллажей и слышите, как он отчитывает Клариссу за проваленную затею с Мелиссой и Амандой. Его слова звучат не как отцовская забота, а как холодный расчет человека, который привык распоряжаться чужими слабостями."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene "images/clara/panishment/panishment2.jpg"
    $ scene_runtime.text = "Потом раздается короткий хлопок ладони по ткани, и Кларисса сдавленно выдыхает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene "images/clara/panishment/panishment3.jpg"
    $ scene_runtime.text = "Легаре зло напоминает ей, что уже много раз говорил: в нужный момент благовоспитанные дамы должны выглядеть так, будто лишняя скромность им только мешает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene "images/clara/panishment/panishment4.jpg"
    $ scene_runtime.text = "Вы можете ворваться сейчас, но тогда Легаре точно станет вашим врагом."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene "images/clara/panishment/panishment5.jpg"
    $ scene_runtime.text = "Можно отступить и поговорить с Клариссой позже, когда она сама сможет сказать больше."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Ворваться и поставить Легаре на место":
            call story_clara_paintings_confront_legare

        "Отступить и поддержать Клариссу позже":
            call story_clara_paintings_wait_comfort
    return


label story_clara_paintings_confront_legare:
    show screen main_ui
    $ Alber.amanda_conflict_stage = 1
    $ Amanda.legare_departure_code = max(2, Amanda.legare_departure_code)
    $ Clara.change_social(friend_delta=1)
    $ scene_runtime.text = "Вы выходите из-за стеллажей и прямо говорите Легаре, что его семейные распоряжения перестали быть только семейным делом. Легаре быстро закрывает подвал за спиной Клариссы и встречает вас уже без торговой улыбки.\n\nДрака выходит короткой и злой: несколько ударов, сбитая бутылка, хруст стекла под сапогом. Легаре отступает первым, но по его лицу ясно, что теперь вы для него не помеха, а враг. Перед уходом он почти спокойно бросает, что раз вы вмешиваетесь в его дом, он займется вашим домом куда настойчивее.\n\nПохоже, он ускорит свои попытки добраться до Аманды."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.abort()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_wait_comfort:
    show screen main_ui
    $ scene_runtime.text = "Вы сдерживаете первый порыв и отходите от подвала. Сейчас Кларисса слишком зажата между вами и отцом, а Легаре слишком хорошо умеет превращать чужой протест в свою пользу.\n\nЕсли поговорить с ней позже без свидетелей, можно узнать больше и не закрыть ей путь к откровенности."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_comfort_2:
    $ main_ui_begin_native_scene_state("Разговор с Клариссой")
    show screen main_ui
    $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
    $ Clara.change_social(friend_delta=1)
    $ scene_runtime.text = "Утром Кларисса держится за прилавком слишком ровно. Вы не давите, просто говорите, что слышали достаточно, чтобы понять: она не одна во всем этом.\n\nСначала она отвечает светски и холодно, но потом голос срывается. Она снова говорит о браке, который для нее уже почти решен в столице, и о надежде, что отец еще передумает. Когда вы спрашиваете, не отсюда ли были все странные поручения, поездки и разговоры о лошадях, Кларисса бледнеет и признает: часть этого правда шла по отцовскому расчету.\n\n\"Я сопротивлялась как могла,\" тихо говорит она. \"Я думала, он изменит решение, если увидит, что я полезна не только как товар для чужого договора. Но он не меняется. Он просто называет это заботой.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_second_ask_3:
    $ main_ui_begin_native_scene_state("Разговор с Клариссой")
    show screen main_ui
    $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
    $ Clara.change_social(open_delta=2)
    $ scene_runtime.text = "Когда вы второй раз возвращаетесь к теме рисунков, Кларисса уже не отшучивается. Она признает, что иногда делает портреты для знатных заказчиков, а иногда видит куда больше, чем люди думают.\n\n\"Многие любят, когда их рисуют красивее, смелее или опаснее, чем они есть,\" говорит она. \"А некоторые забывают, что художник сначала смотрит. Я делаю вид, будто вижу только позу и ткань, но на самом деле замечаю взгляды, тайные жесты, встречи за дверью. Оттуда и берутся сюжеты.\"\n\nТеперь между вами появляется другое доверие: не только разговорное, но и телесное. Кларисса уже понимает, что вы знаете ее тайну и не собираетесь использовать ее против нее."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_church_4:
    $ main_ui_begin_native_scene_state("Семья Легаре в церкви")
    show screen main_ui
    $ scene_runtime.text = "У колонны рядом с семьей Легаре сегодня стоит незнакомый молодой дворянин из столицы. Кларисса держится рядом с ним так ровно, что это выглядит почти болезненно. Легаре, напротив, доволен: он представляет гостя как человека из хорошего дома и будущего союзника семьи.\n\nКларисса не произносит слова \"жених\", но оно и так висит между ними. Теперь понятно, что столичная договоренность уже не слух и не отдаленная угроза."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_barber_5:
    $ main_ui_begin_native_scene_state("Жених Клариссы")
    show screen main_ui
    if int(calendar_v2.time_slot() or 0) == 0:
        $ scene_runtime.text = "Утром у цирюльни вы замечаете того самого столичного жениха. Он выходит от Серджио слишком быстро и слишком аккуратно поправляет перчатки, будто не хочет, чтобы его здесь запомнили."
    else:
        $ scene_runtime.text = "Поздно вечером у закрытой цирюльни мелькает знакомая фигура. Столичный жених Клариссы входит через боковую дверь, а Серджио впускает его без лишних слов."
    $ scene_runtime.location_text = scene_runtime.text
    $ event_runtime.active_thread.advance()
    menu:
        "Осторожно заглянуть внутрь" if int(player.stats.exploration or 0) >= 200:
            call story_clara_paintings_barber_peek

        "Промолчать и уйти":
            $ main_ui_end_native_scene_state()
            return
    return


label story_clara_paintings_barber_peek:
    show screen main_ui
    $ scene_runtime.text = "Вы находите узкую щель между ставней и рамой. Внутри Серджио и столичный гость говорят совсем не как мастер и клиент. Слишком много тишины между фразами, слишком много осторожных прикосновений, слишком мало страха быть понятыми друг другом.\n\nДеталей вам хватает, чтобы понять главное: будущий брак Клариссы держится на лжи с обеих сторон. Этот материал может стать для нее оружием, если использовать его осторожно."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_commission_6:
    $ main_ui_begin_native_scene_state("Поручение Клариссы")
    show screen main_ui
    $ Clara.commission_followup_day = int(current_game_day() or 0) + 1
    $ scene_runtime.text = "Когда Кларисса заглядывает в трактир, вы тихо говорите ей, что у вас появился материал, который стоит зарисовать. Она сперва настораживается, но, услышав про столичного жениха и цирюльню, становится совершенно серьезной.\n\n\"Не здесь,\" отвечает она. \"Завтра утром зайди в лавку. Если это правда, мне нужно понять, как показать это так, чтобы не выглядеть просто мстительной дурой.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_commission_followup_7:
    $ main_ui_begin_native_scene_state("Поручение Клариссы")
    show screen main_ui
    $ scene_runtime.text = "Утром в винной лавке Кларисса сразу понимает, зачем вы пришли. Вы пересказываете ей все без лишних украшений. Она не перебивает, только сжимает пальцы на краю стойки.\n\n\"Вечером,\" решает она наконец. \"Если я увижу сама, я смогу нарисовать не слух, а правду. И тогда отецу будет куда сложнее продать меня за красивую столичную легенду.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_evening_peek_8:
    $ main_ui_begin_native_scene_state("Кларисса у цирюльни")
    show screen main_ui
    $ Clara.murder_day = int(current_game_day() or 0) + 1
    $ scene_runtime.text = "Вечером вы с Клариссой держитесь в тени напротив цирюльни. Когда боковая дверь снова открывается, она успевает увидеть достаточно: столичного жениха, Серджио, их осторожные жесты и ту особую близость, которую нельзя объяснить случайным визитом.\n\nКларисса сперва каменеет, потом почти злится на себя за облегчение. \"Значит, он тоже живет не той жизнью, которую ему продают,\" шепчет она. \"А меня собирались сделать ширмой для чужих приличий.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_confession_9:
    $ main_ui_begin_native_scene_state("Признание Клариссы")
    show screen main_ui
    $ Clara.change_social(friend_delta=2)
    $ Melissa.change_social(friend_delta=1)
    $ scene_runtime.text = "В комнате Мелиссы Кларисса наконец срывается. Она говорит быстро, будто боится остановиться: про отцовские расчеты, про рисунки, про то, как пыталась использовать чужие тайны, чтобы получить хоть немного свободы.\n\nМелисса слушает мрачно, но не перебивает. Когда Кларисса доходит до того, что использовала доверие подруг, она уже почти плачет.\n\n\"Простите,\" говорит она вам обоим. \"Я предала хороших друзей, потому что решила, будто если сама стану хитрее, меня перестанут продавать как вещь. Но от этого я только стала похожа на тех, от кого хотела сбежать.\"\n\nПосле этого в комнате становится тяжелее, но честнее. Теперь Кларисса больше не прячется за одной только игрой."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_murder_10:
    $ main_ui_begin_native_scene_state("Смерть жениха Клариссы")
    show screen main_ui
    $ scene_runtime.text = "У караулки шумно: стражники переговариваются вполголоса, а десятник Циммерман выглядит куда серьезнее обычного. Столичный жених Клариссы найден мертвым.\n\nЦиммерман не спешит называть виновного. Вместо этого он бросает вам странную загадку: \"Кто режет ближе всех, но держит лезвие чистым? Кто слышит тайны, но продает только видимость порядка? Ответишь верно - помогу тебе разобраться и сам.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ event_runtime.active_thread.advance()
    menu:
        "Ответить: цирюльник держит лезвие, но не обязательно вину":
            call story_clara_paintings_solve_murder

        "Промолчать и уйти":
            $ main_ui_end_native_scene_state()
            return
    return


label story_clara_paintings_solve_murder:
    show screen main_ui
    $ crafting.special_cream_recipe_unlocked = True
    $ tractir_progress.sergio_discount_percent = 25
    $ player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 3
    $ Clara.change_social(friend_delta=2)
    $ scene_runtime.text = "Вы отвечаете, что Серджио слишком очевиден как человек с лезвием, а значит, слишком удобен как подозреваемый. Настоящий ответ прячется не в бритве, а в том, кому выгодно было убрать жениха именно сейчас.\n\nЦиммерман долго смотрит на вас, потом коротко кивает. Серджио отпускают из-под подозрения, а город начинает судачить, что хозяин \"Дикого Жеребца\" умеет видеть дальше прямой улики.\n\nПозже Серджио передает вам рецепт особой смягчающей мази и обещает обслуживать вас и ваших работниц со скидкой в четверть цены. Рецепт теперь можно найти в книге рецептов, если открыть список доступных приготовлений."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ main_ui_end_native_scene_state()
    return
