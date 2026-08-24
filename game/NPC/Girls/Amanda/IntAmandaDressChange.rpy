            global player.economy.tavern_fame            global player.economy.tavern_fame    return            global player.economy.tavern_fame            global player.economy.tavern_fame    return            global player.economy.tavern_fame            global player.economy.tavern_fame    return# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def amanda_dress_change_has_options(girl_name="amanda"):
        if Amanda.talked_today >= 2:
            return False
        if Amanda.rel > 8 and int(Amanda.sex_stat("orgasms_given", 0) or 0) >= 2:
            return True
        if Amanda.rel > 8 and CheckDailyEventExists("", "BuyDressTom") == 0 and CheckDailyEventExists("amanda", "BuyDress") == 0 and week != 6:
            return True
        return False

    def amanda_dress_change_other_saw_text(girl_name="amanda", agreed_to_redress=0):
        girl = str(girl_name or "amanda")
        if int(agreed_to_redress or 0) != 1 or Amanda.corruption < 50:
            return ""
        randvar = procedural_randint(1, 9, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:18:1")
        if str(getLocation("liza") or "") != "TavernMain" and randvar == 4:
            randvar = procedural_randint(5, 7, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:20:2")
        if str(getLocation("georgett") or "") != "TavernMain" and randvar == 3:
            randvar = procedural_randint(5, 7, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:22:3")
        if randvar == 1:
            if Sandra.corruption >= 35:
                text = 'Обернувшись, вы вдруг встретились взглядом с Сандрой, наблюдающей за этой сценкой. Но она всего лишь усмехнулась, покачала головой и пошла по своим делам.'
            else:
                text = 'Обернувшись, вы вдруг встретились взглядом с Сандрой, наблюдающей за этой сценкой. И увиденное ей явно не понравилось. Она подскочила и сердито заорала: "Значит Аманда становится шлюхой? Раздеваться при всех, ни стыда, ни совести!"\n"Сандра, успокойся," заступились вы за Аманду. У нее там просто что-то кололо, да так больно, что она и не сообразила где она."\nХоть и малоправдоподобная, но все-таки отмазка смутила Сандру и вы смогли заболтать тему.'
        elif randvar == 2:
            if Melissa.corruption >= 35:
                text = 'Вы окинули взглядом трактир и увидели пораженную Мелиссу, заметившую Амандин стриптиз. Но увиденное ее совсем не шокировало, она понимающе улыбнулась Аманде и пошла дальше по своим делам.'
            else:
                text = 'Вы окинули взглядом трактир и увидели пораженную Мелиссу, заметившую Амандин стриптиз. И этот стриптиз ее явно шокировал. Она подбежала к вам и воскликнула: "Аманда, ты что, совсем стыд потеряла?"\n"Знаешь что, то что ты старше, не дает тебе права кричать на меня," отвергла критику Аманда, и не слушая возмущенные писки Мелиссы, пошла как ни в чем ни бывало.'
        elif randvar == 3:
            text = 'Вы заметили, что за вами с улыбкой наблюдала Жоржетта и кивнули ей в ответ. А она тогда одобрительно подняла большой палец вверх.'
        elif randvar == 4:
            text = 'Вы заметили, что за подругой наблюдала Лизетта, одобрительно кивая.'
        elif randvar == 5:
            text = 'Из-за ближайшего стола послышался одобрительный свист, посетителям Амандин стриптиз пришелся по душе.'
        elif randvar == 6:
            text = 'Когда Аманда пошла в зал, то сразу пара посетителей, наверное заметивших ее стриптиз, ущипнули девчонку за мягкое место. Она довольно взвизгнула и побежала дальше.'
        elif randvar == 7:
            text = 'Один из посетителей наблюдал за этой сценкой с отвалившей челюстью. Аманда весело подмигнула ему и пошла к стойке.'
        else:
            text = ""
        if randvar <= 2:
            Amanda.apply_social_chance(0, 0, 0, 60, 2, 1, "dress_change_seen")
        if randvar >= 5 and randvar <= 7:
            Amanda.apply_social_chance(0, 0, 0, 60, 1, 1, "dress_change_seen")
            player.economy.tavern_fame = int(player.economy.tavern_fame or 0) + 1
        return text


label int_amanda_dress_change(GirlNameIAT="amanda"):
    while True:
        $ current_action_title = "Переодеть Аманду"
        $ current_action_content = None
        $ _can_offer_bra = Amanda.rel > 8 and int(Amanda.sex_stat("orgasms_given", 0) or 0) >= 2 and str(Amanda.current_underwear("bra", "") or "") != "" and (Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0)) and Amanda.talked_today < 2
        $ _can_offer_panties = Amanda.rel > 8 and int(Amanda.sex_stat("orgasms_given", 0) or 0) >= 2 and str(Amanda.current_underwear("panties", "") or "") != "" and (Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0)) and Amanda.talked_today < 2
        $ _can_shame = Amanda.rel > 8 and int(Amanda.sex_stat("orgasms_given", 0) or 0) >= 2 and Amanda.talked_today < 2
        $ _can_buy = Amanda.rel > 8 and CheckDailyEventExists("", "BuyDressTom") == 0 and CheckDailyEventExists(GirlNameIAT, "BuyDress") == 0 and Amanda.talked_today < 2 and week != 6
        menu:
            "Предложить Аманде ходить без лифчика" if _can_offer_bra:
                call IntAmandaDressChangeApply(GirlNameIAT, "offer_bra")
            "Предложить Аманде снять панталоны" if _can_offer_panties:
                call IntAmandaDressChangeApply(GirlNameIAT, "offer_panties")
            "Постыдить Аманду за то, что ходит без лифчика" if _can_shame:
                call IntAmandaDressChangeApply(GirlNameIAT, "shame_bra")
            "Постыдить Аманду за отстутсвие панталон" if _can_shame:
                call IntAmandaDressChangeApply(GirlNameIAT, "shame_panties")
            "Предложить купить Аманде обновку" if _can_buy:
                call IntAmandaDressChangeApply(GirlNameIAT, "buy_dress")
            "Назад":
                return
    return


label IntAmandaDressChangeApply(GirlNameIAT="amanda", choice_code=""):
    $ AgreedToRedress = 0
    $ tmpLizaComandoBonus = 0

    if str(choice_code or "") == "offer_bra":
        $ MainTxt = '"Амандочка, милашка, а зачем же ты ходишь в лифчике?" - неожиданно спросили вы Аманду. "Ведь если начистоту, то он тебе пока не нужен, более того, он скрывает твою хоть и небольшую, но красивую и упругую грудь. Если ты будешь ходить без него, то платье лучше подчеркнет все ее изумительные изгибы если оно будет надето на голое тело," начали вы вешать ей лапшу на уши.'
        if DressPartSlut.get(DressTopPart.get(Amanda.current_dress(), ""), 0) < 4:
            if Amanda.corruption < 35:
                $ MainTxt += '\n\n"Да ты что, Стефан?!" рассердилась Аманда. "Ты мне без лифчика предлагаешь ходить, чтобы полтрактира на мои сиськи пялилось? Ты что?!"'
            else:
                $ MainTxt += '\n\n"Ну не знаю," ответила вам Аманда с сомнением. "Но раз ты так говоришь, то попробую без него походить."'
                $ AgreedToRedress = 1
                if Amanda.corruption < 50:
                    if procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:91:4") == 1:
                        $ MainTxt += '\n\nАманда забежала на кухню, убедилась что там никого нет, и сноровисто избавилась от лифа, одев платье уже на голые груди.'
                    else:
                        $ MainTxt += '\n\nАманда и вы спрятались за стойкой, где вас не было видно из зала. Вы запустили руки под платье Аманды, расстегивая многочисленные завязки и крючочки. Минута работы - и трофей уже в ваших руках. Правда ненадолго, девушка тут же забрала его обратно и спрятала.'
                else:
                    $ MainTxt += '\n\nАманда лишь слегка отвернулась от зала и быстро распахнула блузку. За ней пришел черед и лифчика. На несколько секунд мелькнули ее маленькие грудки с торчащими сосочками, а затем она застегнула платье, пряча свои два сокровища.'
                $ MainTxt += '\n\n"Ну как я тебе," смущенно поинтересовалась она.\n"Гораздо лучше!" честно ответили вы.'
        else:
            if Amanda.corruption < 50:
                $ MainTxt += '\n\n"Да ты что?" удивилась Аманда вашему предложению. "Только парень мог такое предложить. Ты же видишь, что у меня глубокое декольте. Я подкладываю в лиф вату, чтобы моя грудь казалась больше. А если я его уберу, то моя грудь будет во-первых смотреться чуть меньше, а во вторых, и это самое главное, любой кто мне туда заглянет увидет мои груди вплоть до сосков, ведь платье-то чуть больше чем надо. Сам видишь, твоя идея не сработает."'
            else:
                $ MainTxt += '\n\n"Хм, Стефан," удивилась Аманда. "Ты действительно так думаешь? Не помню, говорила я тебе или нет, у меня платье чуть больше чем мой размер, а декольте глубокое. Так любой сможет заглянуть и увидеть даже соски."\n"Так в этом и вся идея!" не растерялись вы. "Могут увидеть, так ты еще соблазнительней покажешься, разве нет?'
                if str(getLocation("liza") or "") == "TavernMain":
                    $ MainTxt += ' Ты ведь хочешь чтобы тебя хотели, вон на Лизетту посмотри, она ничего не носит!'
                $ MainTxt += '"\n"Ну, наверное ты прав," после небольшого колебания согласилась с вами Аманда, "помоги тогда."\nВы не замедлили оказать ей помощь, запустив руки под платье, расстегнув и затем вытащив лиф. Лишь потом вы поняли что даже и не попробовали отойти куда в сторонку.'
                $ AgreedToRedress = 1
        if AgreedToRedress == 1:
            $ Amanda.set_current_underwear("bra", "")
            $ Amanda.publish_wardrobe_state()
            $ Amanda.apply_social_chance(0, 0, 0, 60, 2, 1, "dress_change_bra")
            $ Amanda.publish_wardrobe_state()
        $ _other_saw = amanda_dress_change_other_saw_text(GirlNameIAT, AgreedToRedress)
        if str(_other_saw or "").strip() != "":
            $ MainTxt += "\n\n" + str(_other_saw)
        $ Amanda.mark_talked()
        $ CurLocDesc = MainTxt
        return

    if str(choice_code or "") == "offer_panties":
        $ MainTxt = '"Аманда, а чего ты в панталонах-то ходишь?" - поинтересовались вы как бы между делом у Аманды. "Они только тебя стесняют, без них ты и работу будешь сноровистей выполнять, да и сама себя будешь ощущать сексуальнее.'
        if str(getLocation("liza") or "") == "TavernMain":
            $ MainTxt += ' Разве ты не знаешь, что Лизетта, твоя лучшая подруга, без них ходит?" добавили вы для пущей убедительности. '
            if Liza.current_underwear("panties", "") == "":
                $ MainTxt += '\n\n"И то правда," задумчиво сказала Аманда.'
                $ tmpLizaComandoBonus = min(10, Amanda.var_int("lizafriends", 0) // 2)
            else:
                $ MainTxt += '\n\n"Лишь бы чего ляпнуть," укоризнено сказала вам Аманда, "я прекрасно знаю что это не так."'
                $ tmpLizaComandoBonus = -min(10, Amanda.var_int("lizafriends", 0) // 4)
        else:
            $ MainTxt += '"'
        if DressPartSlut.get(DressBottomPart.get(Amanda.current_dress(), ""), 0) < 4:
            if Amanda.corruption + tmpLizaComandoBonus < 42:
                $ MainTxt += '\n\n"Как тебе такое только в голову могло прийти! Мол сноровистей я буду работать. Я же каждую минуту буду думать, как бы мне кто под юбку не заглянул! Какая уж тут работа!"'
            else:
                $ MainTxt += '\n\n"Ну, может оно и так," сказала Аманда. "Ведь никто ничего не увидит, значит все в порядке. Может и буду я шустрей работать. Надо попробовать."'
                $ AgreedToRedress = 1
                if Amanda.corruption < 50:
                    if procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:138:5") == 1:
                        $ MainTxt += '\n\nАманда забежала на кухню, убедилась что там никого нет, и быстро стянула с себя панталончики.'
                    else:
                        $ MainTxt += '\n\nАманда зашла за стойку, убедилась что по меньшей мере ее нижней половины не видно из зала, и стянула с себя эту деталь своего туалета. Впрочем вам она ее не отдала, а куда-то спрятала.'
                else:
                    $ MainTxt += '\n\nНе особо-то скрываясь, Аманда слегка присела, сунула руку себе под подол, и стянула с себя панталончики, даже не проверив, не следит ли за ней кто из посетителей.'
        else:
            if Amanda.corruption + tmpLizaComandoBonus < 55:
                $ MainTxt += '\n\n"Да ты издеваешься, Стефан?!," возмутилась Аманда в ответ на ваше предложение. "Ты мое платье видел? Если не видел, то вот, посмотри! Оно же попу едва закрывает! Если я наклонюсь, то всем посетителям свою девочку покажу. Какое уж тут, прости Ильматер, обслуживание, если все меня будут лапать. А лапать будут, ты сам наших посетителей знаешь!" '
            else:
                $ MainTxt += '\n\n"Эх, Стефан," пошло улыбнулась Аманда. "Ты ведь прекрасно знаешь, что в таком коротком платьичке, да без панталончиков, каждый мою писю увидит. А ведь нагибаться придется, там со стола вытри, здесь кружки поставь. Это ты называешь лучшим обслуживанием?"\n"Именно это, ты все отлично поняла," не смутились вы.\n"Ой, уговорил, языкастый, попробуем!" с готовностью отозвалась Аманда.\nДаже не попытавшись уйти за стойку или еще куда, Аманда сунула руки под короткую юбочку и стянула с себя панталончики, показав на секунду свою щелку.'
                $ AgreedToRedress = 1
        if AgreedToRedress == 1:
            $ Amanda.set_current_underwear("panties", "")
            $ Amanda.publish_wardrobe_state()
            $ Amanda.apply_social_chance(0, 0, 0, 60, 2, 1, "dress_change_panties")
            $ Amanda.publish_wardrobe_state()
        $ _other_saw = amanda_dress_change_other_saw_text(GirlNameIAT, AgreedToRedress)
        if str(_other_saw or "").strip() != "":
            $ MainTxt += "\n\n" + str(_other_saw)
        $ Amanda.mark_talked()
        $ CurLocDesc = MainTxt
        return

    if str(choice_code or "") == "shame_bra":
        $ MainTxt = '"Аманда, а не стыдно тебе без лифа ходить?" - пристыдили вы Аманду. "Половина посетителей на тебя пялится!"'
        if str(Amanda.current_underwear("bra", "") or "") != "" or (str(Amanda.current_underwear("bra", "") or "") == "" and Amanda.corruption >= 50 and procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:164:6") == 1):
            $ MainTxt += '\n\n"А с чего это ты решил что нету? Как это ты проверил? Во сне меня что ли без лифа представил?" пресекла ваши поучения Аманда. '
        else:
            $ MainTxt += '\n\n"Ну да, ты же меня сам так надоумил," обескураженно ответила вам она.\n"Сказал что мол изгибы мои изумительные так лучше будут подчеркнуты, помнишь?"\n"Не помню!" Отрезали вы. "А если и сказал, то уже сожалею, погорячился я, как-то уж слишком пошло ты без него выглядишь."'
            if Amanda.corruption < 45:
                $ MainTxt += '\n\n"Ну, коль ты теперь по-другому заговорил, то пойду и одену его обратно. Я себя и правда как-то неловко чувствовала."'
                $ AgreedToRedress = 1
            elif Amanda.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:171:7") <= 3:
                $ MainTxt += '\n\n"Так вроде тебе нравилось, а сейчас ты вон как заговорил, "Не помнит" видите ли..." надулась Аманда, "хорошо, ладно, пойду наверх одену его."'
                $ AgreedToRedress = 1
                $ Amanda.apply_social_chance(7, 2, -1, 0, 0, 0, "dress_shame_bra")
            else:
                $ MainTxt += '\n\n"Ай-яй, Стефан, значит ты у нас теперь скромник?!" засмеялась Аманда. "Ну а я, представь себе, нет! И я теперь уже взрослая и могу сама выбирать как мне одеваться! Так то!"'
                $ Amanda.apply_social_chance(7, 1, -1, 0, 0, 0, "dress_shame_bra")
        if AgreedToRedress == 1:
            $ Amanda.set_current_underwear("bra", "simplebra")
            $ Amanda.publish_wardrobe_state()
            $ Amanda.apply_social_chance(0, 0, 0, 30, 1, -1, "dress_shame_bra")
            $ Amanda.publish_wardrobe_state()
        $ Amanda.mark_talked()
        $ CurLocDesc = MainTxt
        return

    if str(choice_code or "") == "shame_panties":
        $ MainTxt = '"Аманда, мне показалось что у тебя под юбкой ничего нет?" - пожурили вы Аманду. "И не стыдно?"'
        if str(Amanda.current_underwear("panties", "") or "") != "" or (str(Amanda.current_underwear("panties", "") or "") == "" and Amanda.corruption >= 45 and procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:189:8") == 1):
            $ MainTxt += '\n\n"Ага, тебе показалось. А когда кажется, надо знак Ильматера вокруг себя очерчить, морок-то и пройдет," и Аманда убежала дальше.'
        else:
            $ MainTxt += '\n\n"Так ты ж сам сказал, что мол без них работать мне удобнее будет, если мол движения не скованны."\n"Ага, удобнее, я же вижу как все посетители, когда ты им голой мандой светишь, руки распускать начинают. Какое уж тут удобнее. Не стыдно? Одела бы ты панталоны обратно, не позорила наше заведение!" отчитали вы бесстыдницу.'
            if Amanda.corruption < 45:
                $ MainTxt += '\n\n"Ну, коль ты теперь по-другому заговорил, то пойду и одену их обратно. Я себя и правда как-то слишком неуютно чувствовала, все время юбку проверяла, не задралась ли."'
                $ AgreedToRedress = 1
            elif Amanda.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:196:9") <= 3:
                $ MainTxt += '\n\n"Ага, сначала сам подначил, а теперь стыдит. Да ты издеваешься надо мной, а я, то дура, поверила." надулась Аманда, "ну ладно, пойду наверх одену."'
                $ AgreedToRedress = 1
                $ Amanda.apply_social_chance(7, 1, -1, 0, 0, 0, "dress_shame_panties")
            else:
                $ MainTxt += '\n\n"Ага, позорила, уж кто бы говорил" засмеялась Аманда. "А чаевые, между прочим, так гораздо лучше дают! И вообще, я теперь уже взрослая и могу сама выбирать как мне одеваться! И ты мне в этом - не указ!"'
                $ Amanda.apply_social_chance(7, 1, -1, 0, 0, 0, "dress_shame_panties")
        if AgreedToRedress == 1:
            $ Amanda.set_current_underwear("panties", "simplepanties")
            $ Amanda.publish_wardrobe_state()
            $ Amanda.apply_social_chance(0, 0, 0, 30, 1, -1, "dress_shame_panties")
            $ Amanda.publish_wardrobe_state()
        $ Amanda.mark_talked()
        $ CurLocDesc = MainTxt
        return

    if str(choice_code or "") == "buy_dress":
        $ MainTxt = '"Амандочка, а хочешь я тебе обновку куплю?" - задали вы Аманде вопрос, хотя уже заранее знали на него ответ.\n"Конечно хочу!" Аманда даже подпрыгнула от радости и еле удержалась, чтобы не захлопать в ладоши.\n"Ну тогда завтра, с утра пораньше, дуй к Ирме Фараго, я буду тебя там ждать, вместе и выберем!" заверили вы Аманду.'
        $ DailyEventsList_Add(GirlNameIAT, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
        $ Amanda.mark_talked()
        $ CurLocDesc = MainTxt
        return

