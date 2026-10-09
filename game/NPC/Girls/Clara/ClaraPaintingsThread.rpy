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
    vscene "images/clara/punishment/punishment1.jpg"
    $ scene_runtime.text = "Из  подвала винной лавки доносится резкий голос Легаре. Вы останавливаетесь у стеллажей и слышите, как он отчитывает Клариссу за проваленную затею с Мелиссой и Амандой. Его слова звучат не как отцовская забота, а как холодный расчет человека, который привык распоряжаться чужими слабостями."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene "images/clara/punishment/punishment2.jpg"
    $ scene_runtime.text = "Потом раздается короткий хлопок ладони по ткани, и Кларисса сдавленно выдыхает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene "images/clara/punishment/punishment3.jpg"
    $ scene_runtime.text = "Легаре зло напоминает ей, что уже много раз говорил: в нужный момент благовоспитанные дамы должны выглядеть так, будто лишняя скромность им только мешает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene "images/clara/punishment/punishment4.jpg"
    $ scene_runtime.text = "Вы можете ворваться сейчас, но тогда Легаре точно станет вашим врагом."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene "images/clara/punishment/punishment5.jpg"
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


label story_clara_paintings_legare_secret_date_7:
    $ main_ui_begin_native_scene_state("Тайный визит Легаре к Серджио")
    show screen main_ui
    $ scene_runtime.text = "Поздним вечером вы замечаете, как Альбер Легаре оглядывает пустую улицу и стучит в боковую дверь цирюльни. Серджио выглядывает наружу, узнаёт его и сразу впускает внутрь. Через минуту у соседней стены появляется Кларисса. Она знаком показывает вам молчать и припадает к щели между ставнями."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Заглянуть вместе с Клариссой":
            $ calendar_v2.advance_minutes(15)
            if int(player.stats.exploration or 0) < 200:
                $ scene_runtime.text = "Вы обходите цирюльню, но сегодня ставни закрыты слишком плотно. Кларисса сердито качает головой и уходит. Придётся вернуться в другой вечер и выбрать место получше."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Продолжить":
                        pass
                $ main_ui_end_native_scene_state()
                return True

            vscene "images/barber shop/alber_sergio_secret_date_underwear.png"
            $ scene_runtime.text = "Через щель видно, как Серджио держит камзол Легаре, пока тот, оставшись в одной рубашке и нижних штанах, усаживается возле ширмы. Обычным бритьём здесь и не пахнет. Серджио кладёт ладонь ему на плечо; Альбер перехватывает его руку и тянет к себе. Вскоре оба исчезают за ширмой, откуда доносятся скрип кушетки, приглушённые стоны и довольный смех."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Не отводить взгляда":
                    pass

            vscene "images/clara/secret_date/clarissa_watches_window.png"
            $ scene_runtime.text = "Кларисса прижимается к ставне ещё ближе. В полоске света белеет её серебристая прядь; она смотрит на отчима и Серджио, будто наконец увидела объяснение слишком многим его тайным отлучкам."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Посмотреть на Клариссу":
                    pass

            vscene "images/clara/secret_date/clarissa_laughing_closeup.png"
            $ scene_runtime.text = "За ширмой Серджио насмешливо спрашивает, надолго ли сегодня задержался почтенный семьянин. Кларисса зажимает рот ладонью, но плечи всё равно начинают дрожать от беззвучного смеха."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Не выдавать её":
                    pass

            vscene "images/clara/secret_date/clarissa_blushing_closeup.png"
            $ scene_runtime.text = "Она замечает ваш взгляд и вспыхивает до самых ушей. «Только не смейте сейчас задавать вопросы, — шепчет Кларисса. — Я ещё не решила, смеяться мне или провалиться сквозь землю»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Отойти от окна вместе":
                    pass
            $ event_runtime.active_thread.advance()
            $ main_ui_end_native_scene_state()
            return True

        "Не вмешиваться и уйти":
            $ calendar_v2.advance_minutes(15)
            $ main_ui_end_native_scene_state()
            return True


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

            $ scene_runtime.text = "Через щель между ставней и рамой вы видите, как Серджио целует жениха Клариссы. Тот отвечает на поцелуй и увлекает цирюльника за ширму. Вскоре оттуда доносятся частый скрип кушетки, сбившееся дыхание, приглушённые мужские стоны и короткие смешки.\n\nСерджио шепчет: «Тише, Джеймс, нас услышат». Жених тихо смеётся: «Тогда не заставляй меня просить ещё»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Не отводить взгляда":
                    pass

            vscene "images/barber shop/leonard_sergio_secret_date.png"
            $ scene_runtime.text = "Наконец ширма отодвигается. Джеймс выходит в распахнутой рубашке, белых нижних штанах и чулках; его камзол и верхние штаны лежат на кресле. Он просовывает ногу в штанину, пока Серджио держит его чёрный камзол и придерживает за плечо. Оба раскраснелись и то и дело давятся довольным смехом.\n\nСерджио: «Ты опять обещал, что только на минуту».\n\nДжеймс: «И ты опять первым снял с меня штаны».\n\nСерджио хихикает: «Зато теперь застегну их сам», — поправляет ему воротник и быстро целует на прощание. Теперь вы точно знаете: будущий брак Клариссы держится на лжи, которую можно обратить в её защиту."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Запомнить увиденное":
                    pass

            vscene "images/clara/secret_date/clarissa_watches_window.png"
            $ scene_runtime.text = "Вы уже собираетесь отойти, когда у соседней щели между ставнями замечаете серебристую прядь. Закутавшись в тёмный плащ, Кларисса тоже приникла к окну. Она не сводит глаз с жениха и Серджио и, судя по выражению лица, увидела достаточно."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Проследить за её реакцией":
                    pass

            vscene "images/clara/secret_date/clarissa_laughing_closeup.png"
            $ scene_runtime.text = "Когда Джеймс напоминает Серджио, кто первым снял с него штаны, Кларисса зажимает рот ладонью. Её плечи начинают дрожать: она изо всех сил старается не рассмеяться вслух и не выдать вас обоих."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Не выдавать её":
                    pass

            vscene "images/clara/secret_date/clarissa_blushing_closeup.png"
            $ scene_runtime.text = "Кларисса поворачивает голову и встречается с вами взглядом. Смех обрывается, щёки вспыхивают.\n\nКларисса шепчет: «Ни слова. Ни ему, ни Серджио. Я хотела узнать, за кого меня собираются выдать... Теперь узнала даже больше, чем собиралась»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Отойти от окна вместе":
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

    vscene "images/Alber/james_leonard_found.jpg"
    $ scene_runtime.text = "«Утром его обнаружила прислуга: лежал бездыханный, без панталон, а в заднице — огромная деревяшка. Теперь стража трясёт всех, кто с ним встречался. До Клариссы и Серджио добрались первыми»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    vscene rooms.get("HunterClub").bg_picture
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


label story_clara_paintings_legare_warning_11:
    $ main_ui_begin_native_scene_state("Разговор с Легаре")
    show screen main_ui
    vscene wine_store_scene_picture()
    $ scene_runtime.text = "В винном погребке за прилавком стоит Легаре. Вы без приветствия спрашиваете, что он сделал для освобождения Клариссы. Затем требуете оставить в покое и её, и Аманду: никаких тайных поручений, угроз и попыток заманить девушку после танцев."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Потребовать ответа":
            pass

    $ Alber.add_relation(-4)
    $ Alber.amanda_conflict_stage = 2
    $ scene_runtime.text = "Легаре медленно выходит из-за прилавка и указывает тростью на дверь. «Вы пришли в мой дом учить меня обращаться с моей семьёй и с девкой из вашего трактира? Вон. Кларисса сама выбрала позор, а до Аманды вам ещё придётся дорасти». Он распахивает дверь и обещает, что следующая встреча будет короче."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Выйти из погребка":
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
    $ story_event_mark_fired_today(event_runtime.active_thread.getevent(13))
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


label story_clara_paintings_dance_exposure_15:
    $ renpy.dynamic("_clara_dance_fight_outcome")
    $ main_ui_begin_native_scene_state("Разоблачение Легаре")
    show screen main_ui
    vscene "images/market/LocFridayDance.jpg"
    $ scene_runtime.text = "Вы подходите к танцующей паре и громко спрашиваете Легаре, рассказал ли он Аманде о своих вечерних визитах к Серджио. Музыка вокруг ещё играет, но ближайшие танцующие уже прислушиваются."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Рассказать всё при Аманде":
            pass

    $ scene_runtime.text = "Вы говорите прямо: сначала через щель в ставнях видели самого Легаре полураздетым с Серджио, а в другой вечер — Серджио с Джеймсом Леонардом, женихом Клариссы. Теперь понятны и их тайные встречи, и бешенство Легаре после ареста."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Посмотреть на реакцию Аманды":
            pass

    vscene AmandaStaticData.image_path("tavern", "angry")
    $ scene_runtime.text = "Аманда сперва прыскает со смеху, потом отдёргивает руку от Легаре. «Так это ты с Серджио? И жених Клариссы тоже с ним? Как ты вообще мог совать свой член в чужую задницу, а потом строить из себя важного господина? Извращенец! Мудак!» Она объявляет, что больше никуда с ним не пойдёт."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Встать между ними":
            pass

    $ Amanda.legare_affection = 0
    $ Amanda.legare_forbidden = True
    $ Amanda.dancing_with_legare = False
    $ Amanda.left_friday_dance = True
    $ Amanda.legare_departure_code = 0
    $ GirlDance_DeleteGirl("amanda")
    $ Alber.amanda_conflict_stage = 1
    $ fight_begin("legare", 1, "FridayDance", "images/Alber/fight/streetdraw.jpg", "Легаре бросается на вас прежде, чем Аманда успевает отойти. Он уже не пытается сохранить достоинство: трость летит вам в голову, и толпа расступается вокруг драки.")
    call FightLoop
    $ _clara_dance_fight_outcome = str(fight.last_result.get("outcome", "") or "")
    if _clara_dance_fight_outcome == "victory":
        $ Alber.add_relation(-5)
        $ scene_runtime.text = "Вы выбиваете трость из руки Легаре и заставляете его отступить. Аманда смеётся ему в лицо, подхватывает юбку и уходит с площади одна."
    elif _clara_dance_fight_outcome == "defeat":
        $ Alber.add_relation(-3)
        $ scene_runtime.text = "Легаре сбивает вас на мостовую, но победой насладиться не успевает: Аманда при всех называет его лживым старым извращенцем и уходит одна. За ним она больше не следует."
    else:
        $ Alber.add_relation(-4)
        $ scene_runtime.text = "Стражники и танцующие растаскивают вас прежде, чем драка заканчивается. Аманда отталкивает Легаре и уходит одна, оставив его посреди шепчущейся толпы."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к танцам":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_amanda_punishment_16:
    $ main_ui_begin_native_scene_state("Разговор Сандры с Амандой")
    show screen main_ui
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "За завтраком Сандра уже знает о драке на площади. Она выслушивает рассказ Аманды до конца, затем велит ей встать из-за стола. «Над Легаре можешь смеяться сколько хочешь. Но тайком путаться с ним после всех предупреждений и доводить дело до уличной драки — за это ответишь дома»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Не вмешиваться в решение Сандры":
            pass

    $ scene_runtime.text = "Сандра уводит Аманду в её комнату. Вскоре за дверью слышны свист розги, возмущённые вскрики и спор о том, кто имел право распоряжаться её личной жизнью. Вернувшись, Аманда садится осторожно, но повторяет, что к Легаре больше не пойдёт — не из-за наказания, а потому что теперь знает, кем он оказался."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить завтрак":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_winery_rescue_17:
    $ main_ui_begin_native_scene_state("Забрать Клариссу у Легаре")
    show screen main_ui
    vscene "images/clara/punishment/punishment1.jpg"
    $ scene_runtime.text = "При следующем визите в погребок из подвала доносится голос Легаре. Он обвиняет Клариссу в том, что она опозорила семью, позволила арестовать себя и Серджио, помогла разоблачить жениха и настроила против него Аманду. Кларисса отвечает, что ложь разрушил он сам."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Спуститься к подвалу":
            pass

    vscene "images/clara/punishment/punishment2.jpg"
    $ scene_runtime.text = "Легаре приказывает Клариссе наклониться над столом и задирает её платье. Она пытается выпрямиться, но он удерживает её за талию и объявляет, что сегодня выбьет из неё непокорность."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Подойти ближе":
            pass

    vscene "images/clara/punishment/punishment3.jpg"
    $ scene_runtime.text = "Первый тяжёлый удар розгой оставляет на ягодицах красные полосы. Кларисса стискивает зубы и повторяет, что всё равно не откажется от своих слов."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Не уходить":
            pass

    vscene "images/clara/punishment/punishment4.jpg"
    $ scene_runtime.text = "Легаре продолжает порку, пока Кларисса уже не может скрывать боль. Затем отбрасывает розги, расстёгивает штаны и насилует её сзади, называя это последним уроком послушания. Кларисса требует остановиться, но он не слушает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Остановить Легаре":
            pass

    vscene "images/clara/punishment/punishment5.jpg"
    $ scene_runtime.text = "Вы оттаскиваете Легаре и заслоняете Клариссу. Он тянется к трости, но, увидев вашу готовность драться и услышав шаги наверху, отступает. «Забирай её, — выплёвывает он. — Но в мой дом больше не возвращайтесь». На этот раз драки не происходит."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Увести Клариссу":
            pass

    vscene "images/clara/tavern_visit.png"
    $ scene_runtime.text = "Вы приводите Клариссу в трактир вместе с её небольшим узлом вещей. Сандра без расспросов освобождает место в комнате Мелиссы. Кларисса принимает защиту и остаётся членом команды «Дикого жеребца». К Легаре она больше не вернётся."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Принять Клариссу в команду":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_confession_14:
    $ main_ui_begin_native_scene_state("Признание Клариссы")
    show screen main_ui
    vscene "images/clara/melissa_talk.png"
    $ scene_runtime.text = "Поздним вечером Мелисса понимающе оставляет вас вдвоём, а Кларисса сама запирает за ней дверь. Она не прячет взгляд и не мнётся: после наказания Легаре у неё осталось болезненное повреждение, которое так и не прошло. Серджио уверял, что помочь может только особая мазь — и Кларисса хочет, чтобы нанесли её именно вы."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    $ scene_runtime.text = "Кларисса подходит почти вплотную и говорит без тени прежней робости: «Не путайте осторожность с целомудрием. Я взрослая женщина и умею говорить, чего хочу. Вы коснётесь меня только по моей просьбе и остановитесь, если я скажу “стоп”. А если мне станет приятно, я не собираюсь притворяться, будто это не так. Договорились?»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Принять условия Клариссы и обещать принести мазь":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_paintings_ointment_15:
    $ main_ui_begin_native_scene_state("Лечение Клариссы")
    show screen main_ui
    vscene tavern_melissa_room_picture()
    $ scene_runtime.text = "Вы показываете Клариссе приготовленную мазь. Она проверяет засов, пробует каплю на запястье и удовлетворённо кивает. «Напоминаю: это происходит потому, что я сама вас попросила. Скажу “стоп” — вы сразу уберёте руку». Вы соглашаетесь, и только тогда она ставит баночку возле кровати."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Нанести мазь по просьбе Клариссы":
            $ player.remove_item("special_cream_001", 1)
            $ Clara.set_sex_stat("beauty", min(100, int(Clara.sex_stat("beauty", 0) or 0) + 2))
            $ Clara.add_arousal(8)
            $ scene_runtime.text = "Кларисса медленно поднимает юбку, спускает бельё до колен и ложится поперёк кровати. Она сама разводит ягодицы и, оглянувшись через плечо, велит начинать. Вы согреваете мазь между пальцами и осторожно проводите по её воспалённому анусу. Первый вдох выходит резким, но Кларисса тут же направляет вашу руку: «По кругу. Медленнее... да, именно там».\n\nБоль постепенно отпускает, и её тело отвечает уже иначе. Кларисса начинает подаваться бёдрами навстречу каждому движению, а свободной рукой ласкает набухший клитор. Заметив ваше возбуждение, она усмехается: «Смотреть можно. Остальное — только когда я попрошу». Вы замираете, когда её дыхание сбивается; она ясно просит продолжать и сама прижимает ваш палец к чувствительному колечку. Через несколько движений Кларисса глухо стонет, кончая под собственной ладонью, и лишь потом позволяет вам убрать руку.\n\nОна не спешит прикрываться, спокойно вытирает остатки мази и объявляет цену за своё доверие: «Теперь займитесь трактиром. Закажите у Драупнира потайное окошко в стене гостевой комнаты и доведите глорихол до полностью рабочего состояния. Когда оба улучшения будут готовы, найдите Хордуса Папируса на дневном рынке и купите у него старинный диван. Я знаю, что именно он вам покажет. И не пытайтесь заменить хоть один пункт красивыми обещаниями»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Согласиться выполнить все условия Клариссы":
                    pass
            $ event_runtime.active_thread.complete()
            $ main_ui_end_native_scene_state()
            return True

        "Убрать мазь и вернуться позже":
            $ main_ui_end_native_scene_state()
            return True
