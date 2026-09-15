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
    $ renpy.dynamic("_legare_fight_outcome")
    show screen main_ui
    $ Alber.amanda_conflict_stage = 1
    $ Amanda.legare_departure_code = max(2, Amanda.legare_departure_code)
    $ fight_begin("legare", 1, "WineStore", "images/Alber/fight/streetdraw.jpg", "Вы выходите из-за стеллажей и прямо говорите Легаре, что его семейные распоряжения перестали быть только семейным делом. Он закрывает подвал за спиной Клариссы, перехватывает трость и встречает вас уже без торговой улыбки.")
    call FightLoop
    $ _legare_fight_outcome = str(fight.last_result.get("outcome", "") or "")
    if _legare_fight_outcome == "victory":
        $ Alber.add_relation(-5)
        $ Clara.change_social(friend_delta=2, open_delta=1)
        $ scene_runtime.text = "Легаре первым отступает среди разбитых бутылок. Кларисса успевает подобрать платье и смотрит на вас уже не как на случайного покупателя. Перед уходом ее отец обещает, что теперь займется вашим домом куда настойчивее. Похоже, он ускорит попытки добраться до Аманды."
    elif _legare_fight_outcome == "defeat":
        $ Alber.add_relation(-3)
        $ Clara.change_social(friend_delta=1)
        $ scene_runtime.text = "Легаре сбивает вас на каменный пол и велит больше не вмешиваться в дела его семьи. Но Кларисса успевает выскользнуть из подвала, а сам факт вашего вмешательства она не забудет. Вражда с Легаре теперь стала открытой."
    else:
        $ Alber.add_relation(-2)
        $ Clara.change_social(friend_delta=1)
        $ scene_runtime.text = "Вы отступаете из тесного подвала прежде, чем Легаре успевает загнать вас между бочками. Кларисса остается позади, но теперь знает, что вы были готовы вмешаться. Легаре же больше не считает вас просто назойливым трактирщиком."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ event_runtime.active_thread.advance()
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


label story_clara_paintings_first_ask_3:
    $ main_ui_begin_native_scene_state("Рисунки Клариссы")
    show screen main_ui
    $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
    $ Clara.change_social(friend_delta=1, open_delta=1)
    $ scene_runtime.text = "Вы впервые спрашиваете Клариссу прямо о ее рисунках. Девушка мгновенно понимает, какие именно листки вы имеете в виду, но отвечает осторожно.\n\n\"Я рисую то, о чем приличные люди предпочитают только шептаться,\" признается она. \"Иногда это фантазия, иногда увиденная сцена, а иногда заказ. Но имена я тебе пока не назову. Если хочешь услышать больше, сначала докажи, что умеешь хранить чужие тайны.\"\n\nКларисса не отрицает ни рисунков, ни их продажи, однако за разговором явно скрывается история, которую она пока не готова открыть."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Не давить и вернуться к разговору позже":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_second_ask_4:
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


label story_clara_paintings_legare_5:
    $ main_ui_begin_native_scene_state("Кларисса и Легаре")
    show screen main_ui
    vscene "images/clara/wineSellar_clara_talk_5.png"
    $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
    $ Clara.change_social(open_delta=2)
    $ scene_runtime.text = "После второго разговора о рисунках Кларисса уже не может спрятаться за светскими шутками. Вы спрашиваете, почему среди ее самых откровенных сюжетов снова и снова появляется Легаре. Девушка долго молчит, затем запирает дверь в дальнюю кладовую.\n\nОна признается, что отношения с Легаре давно переступили границу между властным опекуном и приемной дочерью. Он пользовался ее зависимостью и ее страхом перед навязанным браком; Кларисса то подчинялась, то пыталась обратить эту связь в средство получить свободу. Именно поэтому в рисунках так много стыда, злости и попыток взять происходящее под собственный контроль."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Спросить, почему она называет его приемным отцом":
            pass
    $ scene_runtime.text = "Кларисса отвечает, что Альбер Легаре не ее настоящий отец. Ее мать Элоиза уже растила маленькую дочь, когда вышла за него замуж; кто был биологическим отцом, она сама, вероятно, не знает. Легаре дал Клариссе свое имя, вырастил ее в своем доме и привык считать ее частью собственной собственности.\n\nТеперь вы понимаете, почему Кларисса одновременно боится его, зависит от него и так яростно ищет тайную жизнь вне семьи."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пообещать не выдавать ее признание":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_church_6:
    $ main_ui_begin_native_scene_state("Семья Легаре в церкви")
    show screen main_ui
    vscene "images/Alber/church/cermon_fiance_clara.png"
    $ scene_runtime.text = "У колонны рядом с семьёй Легаре сегодня стоит незнакомый молодой дворянин из столицы. Он держится уверенно, словно место рядом с Клариссой уже принадлежит ему, а сама девушка отвечает на его любезности с болезненно ровной улыбкой."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    vscene "images/Alber/church/cermon_fiance1_clara.png"
    $ scene_runtime.text = "Легаре представляет гостя как человека из хорошего дома и будущего союзника семьи. Кларисса не произносит слова «жених», но по её взгляду становится ясно: столичный брак уже не слух и не далёкая угроза."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к прихожанам":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_clara_paintings_secret_date_7:
    $ main_ui_begin_native_scene_state("Тайный визит к Серджио")
    show screen main_ui
    $ scene_runtime.text = "Уже после закрытия цирюльни вы замечаете знакомого столичного дворянина. Оглядевшись, жених Клариссы стучит в боковую дверь. Серджио впускает его без единого вопроса, и за ними сразу щёлкает засов."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Осторожно заглянуть внутрь":
            $ calendar_v2.advance_minutes(15)
            if int(player.stats.exploration or 0) < 200:
                $ scene_runtime.text = "Вы обходите цирюльню, но не находите места, откуда можно было бы что-нибудь рассмотреть, не выдав себя. Сегодня придётся уйти ни с чем и попробовать в другой вечер."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Продолжить":
                        pass
                $ main_ui_end_native_scene_state()
                return True

            $ scene_runtime.text = "Через щель между ставней и рамой вы видите, что Серджио и столичный гость говорят совсем не как мастер и клиент. Осторожные прикосновения быстро становятся откровенными. Теперь вы точно знаете: будущий брак Клариссы держится на лжи, которую можно обратить в её защиту."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Продолжить":
                    pass
            $ event_runtime.active_thread.advance()
            $ main_ui_end_native_scene_state()
            return True

        "Не вмешиваться и уйти":
            $ calendar_v2.advance_minutes(15)
            $ main_ui_end_native_scene_state()
            return True


label story_clara_paintings_barber_closed_8:
    $ main_ui_begin_native_scene_state("Закрытая цирюльня")
    show screen main_ui
    vscene "images/general/closedVenue default.png"
    $ scene_runtime.text = "Вы приходите к цирюльне в часы, когда Серджио обычно принимает посетителей, но ставни закрыты, вывеска снята, а дверь заперта. Изнутри не доносится ни голоса, ни звона инструментов. Соседние торговцы только переглядываются и старательно делают вид, что ничего не знают."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться в квартал ремесленников":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_luisa_report_9:
    $ main_ui_begin_native_scene_state("Новости о Клариссе и Серджио")
    show screen main_ui
    vscene rooms.get("HunterClub").bg_picture
    $ scene_runtime.text = "Луиза наклоняется через прилавок и понижает голос: «Слыхал про Клариссу Легаре и цирюльника? Обоих взяли. Богатого Джеймса Леонарда, её столичного жениха, нашли мёртвым у него дома»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "«Утром его обнаружила прислуга: лежал бездыханный, без панталон, а в заднице — огромная деревяшка. Теперь стража трясёт всех, кто с ним встречался. До Клариссы и Серджио добрались первыми»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "MC: И что теперь будет?\n\nЛуиза: А что теперь? Зная Циммера, он отправит обоих на герцогские галеры, а то и хуже — продаст оркам в рабство."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "Хм, интересно. Пожалуй, стоит навестить Циммера, узнать подробности и, может быть, попытаться защитить Клариссу, как я и обещал."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к разговору с Луизой":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_zimmer_needs_wine_10:
    $ main_ui_begin_native_scene_state("Дело Клариссы и Серджио")
    show screen main_ui
    vscene "images/zimmer/talk.png"
    $ scene_runtime.text = "MC: Я хочу поговорить о Клариссе Легаре и Серджио.\n\nЦиммерман: «Таки хотите вмешаться в дело об убийстве богатого человека? Разговор долгий, молодой человек, а от долгих разговоров у моих людей пересыхает горло. Принесите ещё один бочонок вина — тогда и посмотрим, что можно сделать»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к разговору":
            pass
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_zimmer_wine_10:
    $ main_ui_begin_native_scene_state("Дело Клариссы и Серджио")
    show screen main_ui
    vscene "images/zimmer/talk.png"
    $ scene_runtime.text = "MC: Я принёс ещё один бочонок вина. Теперь мы можем поговорить о Клариссе и Серджио?\n\nЦиммерман: «Вот теперь разговор становится обстоятельным. Та бочка для ночной стражи была за другое дело; эта — за время, которое я потрачу на ваше»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Передать бочонок и продолжить":
            $ player.tavern_management.winenum -= 1
            $ event_runtime.active_thread.advance()
            $ main_ui_end_native_scene_state()
            jump story_clara_paintings_zimmer_puzzle_11

        "Оставить вино при себе и вернуться позже":
            $ main_ui_end_native_scene_state()
            return True


label story_clara_paintings_zimmer_puzzle_11:
    $ renpy.dynamic("_clara_case_answer")
    $ story_event_mark_fired_today(event_runtime.active_thread.getevent(11))
    $ main_ui_begin_native_scene_state("Показания по делу Джеймса Леонарда")
    show screen main_ui
    vscene "images/zimmer/talk.png"
    $ scene_runtime.text = "MC: Кларисса и Серджио могли скрывать свои отношения, но это ещё не делает их убийцами. Я обещал Клариссе защиту и хочу услышать, на чём держится обвинение.\n\nЦиммерман: «Таки защиту обещали? Хорошо. Тогда слушайте показания и скажите мне, кто из свидетелей врёт. Если увидите то, что проглядели мои люди, я пересмотрю дело»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Выслушать показания":
            pass

    $ scene_runtime.text = "Богатого Джеймса Леонарда убили в воскресенье днём. В доме были горничная, повар, дворецкий, садовник и жена.\n\n— Горничная: накрывала на стол.\n— Повар: готовил завтрак.\n— Дворецкий: полировал серебро и посуду.\n— Садовник: сажал семена томатов.\n— Жена: читала книгу.\n\nКто это сделал?"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Горничная":
            $ _clara_case_answer = "maid"
        "Повар":
            $ _clara_case_answer = "cook"
        "Дворецкий":
            $ _clara_case_answer = "butler"
        "Садовник":
            $ _clara_case_answer = "gardener"
        "Жена":
            $ _clara_case_answer = "wife"
        "Вернуться к вопросу позже":
            $ _clara_case_answer = "later"

    if _clara_case_answer == "later":
        $ main_ui_end_native_scene_state()
        return False

    if _clara_case_answer == "cook":
        vscene "images/zimmer/thank.png"
        $ scene_runtime.text = "MC: Повар. Леонарда убили в воскресенье днём, а повар утверждает, что готовил завтрак. После полудня завтрак уже не готовят.\n\nЦиммерман некоторое время молчит, затем усмехается: «Таки верно. Показание слишком старательное и совершенно не подходит ко времени смерти. Я прикажу допросить повара заново, а Клариссу и Серджио выпустить»."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Продолжить":
                pass
        $ event_runtime.active_thread.advance()
        $ main_ui_end_native_scene_state()
        return True

    $ scene_runtime.text = "Циммерман качает головой: «Нет, молодой человек. В этом показании нет противоречия со временем убийства. Подумайте ещё и приходите в другой приёмный час»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться в караулку":
            pass
    $ Zimmer.mark_talked(max(0, 2 - int(Zimmer.talked_today or 0)))
    $ main_ui_end_native_scene_state()
    return False


label story_clara_paintings_sergio_followup_12:
    $ main_ui_begin_native_scene_state("Благодарность Серджио")
    show screen main_ui
    vscene barber_shop_picture_path()
    $ scene_runtime.text = "Серджио встречает вас без привычной салонной улыбки. «Мне сказали, кто заметил ложь в показаниях. Без вас нас с Клариссой уже везли бы на галеры»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "«Если после всего этого понадобится средство от трещин, ушибов и самых деликатных повреждений, запишите рецепт. А в моей цирюльне отныне платите на четверть меньше»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Записать рецепт и вернуться к разговору":
            pass
    $ crafting.special_cream_recipe_unlocked = True
    $ tractir_progress.sergio_discount_percent = max(25, int(tractir_progress.sergio_discount_percent or 0))
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_tavern_arrival_13:
    $ main_ui_begin_native_scene_state("Кларисса просит защиты")
    show screen main_ui
    vscene "images/clara/tavern_visit.png"
    $ scene_runtime.text = "Вечером Кларисса появляется в общем зале с небольшим узлом вещей. Вся прежняя уверенность исчезает, когда она просит выполнить обещание и позволить ей остаться под вашей защитой."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "Кларисса: «К Легаре я не вернусь. После ареста в городе мне тоже небезопасно. Если вы не передумали, разрешите пожить здесь. Я могу делить комнату с Мелиссой и помогать трактиру»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Позволить Клариссе поселиться у Мелиссы":
            $ event_runtime.active_thread.advance()
            $ main_ui_end_native_scene_state()
            return True

        "Попросить её вернуться к разговору позже":
            $ main_ui_end_native_scene_state()
            return True


label story_clara_paintings_confession_14:
    $ main_ui_begin_native_scene_state("Признание Клариссы")
    show screen main_ui
    vscene "images/clara/melissa_talk.png"
    $ scene_runtime.text = "Поздним вечером Кларисса просит поговорить без посторонних. После истории с женихом она всё ещё испытывает боль и наконец признаётся, что унижения и насилие оставили повреждение, которое само не проходит."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "Кларисса: «Серджио говорил о специальной мази. Мне стыдно просить, но если вы сумеете её приготовить, я позволю вам помочь. Только без шуток и без спешки»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Обещать принести мазь":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_ointment_15:
    $ main_ui_begin_native_scene_state("Лечение Клариссы")
    show screen main_ui
    vscene tavern_melissa_room_picture()
    $ scene_runtime.text = "Вы показываете Клариссе приготовленную мазь. Она убеждается, что дверь закрыта, и ещё раз просит действовать осторожно."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Помочь Клариссе":
            $ player.remove_item("special_cream_001", 1)
            $ scene_runtime.text = "Когда всё закончено, Кларисса с заметным облегчением приводит одежду в порядок. «Спасибо. Теперь я хотя бы не буду вспоминать о нём при каждом движении. Если когда-нибудь между нами случится что-то ещё, это будет потому, что я сама так решила»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Продолжить":
                    pass
            $ event_runtime.active_thread.complete()
            $ main_ui_end_native_scene_state()
            return True

        "Убрать мазь и вернуться позже":
            $ main_ui_end_native_scene_state()
            return True
