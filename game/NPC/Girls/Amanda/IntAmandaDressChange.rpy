# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label int_amanda_dress_change(GirlNameIAT="amanda"):
    $ renpy.dynamic("_can_offer_bra", "_can_offer_panties", "_can_shame", "_can_buy")
    $ main_ui_runtime.action_title = "Переодеть Аманду"
    $ main_ui_runtime.action_content = None
    $ _can_offer_bra = Amanda.rel > 8 and int(Amanda.sex_stat("orgasms_given", 0) or 0) >= 2 and str(Amanda.current_underwear("bra", "") or "") != "" and (Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0)) and Amanda.talked_today < 2
    $ _can_offer_panties = Amanda.rel > 8 and int(Amanda.sex_stat("orgasms_given", 0) or 0) >= 2 and str(Amanda.current_underwear("panties", "") or "") != "" and (Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0)) and Amanda.talked_today < 2
    $ _can_shame = Amanda.rel > 8 and int(Amanda.sex_stat("orgasms_given", 0) or 0) >= 2 and Amanda.talked_today < 2
    $ _can_buy = Amanda.rel > 8 and daily_events.exists("", "BuyDressTom") == 0 and daily_events.exists(GirlNameIAT, "BuyDress") == 0 and Amanda.talked_today < 2 and int(calendar_v2.week or 0) != 6
    menu:
        "Предложить Аманде ходить без лифчика" if _can_offer_bra:
            call IntAmandaDressChangeOfferBra(GirlNameIAT)
            return
        "Предложить Аманде снять панталоны" if _can_offer_panties:
            call IntAmandaDressChangeOfferPanties(GirlNameIAT)
            return
        "Постыдить Аманду за то, что ходит без лифчика" if _can_shame:
            call IntAmandaDressChangeShameBra(GirlNameIAT)
            return
        "Постыдить Аманду за отстутсвие панталон" if _can_shame:
            call IntAmandaDressChangeShamePanties(GirlNameIAT)
            return
        "Предложить купить Аманде обновку" if _can_buy:
            call IntAmandaDressChangeBuyDress(GirlNameIAT)
            return
        "Назад":
            return
    return


label IntAmandaDressChangeOfferBra(GirlNameIAT="amanda", agreed_to_redress=0):
        $ renpy.dynamic("_other_saw")
        $ agreed_to_redress = 0
        $ scene_runtime.text = '"Амандочка, милашка, а зачем же ты ходишь в лифчике?" - неожиданно спросили вы Аманду. "Ведь если начистоту, то он тебе пока не нужен, более того, он скрывает твою хоть и небольшую, но красивую и упругую грудь. Если ты будешь ходить без него, то платье лучше подчеркнет все ее изумительные изгибы если оно будет надето на голое тело," начали вы вешать ей лапшу на уши.'
        if DressPartSlut.get(DressTopPart.get(Amanda.current_dress(), ""), 0) < 4:
            if Amanda.corruption < 35:
                $ scene_runtime.text += '\n\n"Да ты что, Стефан?!" рассердилась Аманда. "Ты мне без лифчика предлагаешь ходить, чтобы полтрактира на мои сиськи пялилось? Ты что?!"'
            else:
                $ scene_runtime.text += '\n\n"Ну не знаю," ответила вам Аманда с сомнением. "Но раз ты так говоришь, то попробую без него походить."'
                $ agreed_to_redress = 1
                if Amanda.corruption < 50:
                    if procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:91:4") == 1:
                        $ scene_runtime.text += '\n\nАманда забежала на кухню, убедилась что там никого нет, и сноровисто избавилась от лифа, одев платье уже на голые груди.'
                    else:
                        $ scene_runtime.text += '\n\nАманда и вы спрятались за стойкой, где вас не было видно из зала. Вы запустили руки под платье Аманды, расстегивая многочисленные завязки и крючочки. Минута работы - и трофей уже в ваших руках. Правда ненадолго, девушка тут же забрала его обратно и спрятала.'
                else:
                    $ scene_runtime.text += '\n\nАманда лишь слегка отвернулась от зала и быстро распахнула блузку. За ней пришел черед и лифчика. На несколько секунд мелькнули ее маленькие грудки с торчащими сосочками, а затем она застегнула платье, пряча свои два сокровища.'
                $ scene_runtime.text += '\n\n"Ну как я тебе," смущенно поинтересовалась она.\n"Гораздо лучше!" честно ответили вы.'
        else:
            if Amanda.corruption < 50:
                $ scene_runtime.text += '\n\n"Да ты что?" удивилась Аманда вашему предложению. "Только парень мог такое предложить. Ты же видишь, что у меня глубокое декольте. Я подкладываю в лиф вату, чтобы моя грудь казалась больше. А если я его уберу, то моя грудь будет во-первых смотреться чуть меньше, а во вторых, и это самое главное, любой кто мне туда заглянет увидет мои груди вплоть до сосков, ведь платье-то чуть больше чем надо. Сам видишь, твоя идея не сработает."'
            else:
                $ scene_runtime.text += '\n\n"Хм, Стефан," удивилась Аманда. "Ты действительно так думаешь? Не помню, говорила я тебе или нет, у меня платье чуть больше чем мой размер, а декольте глубокое. Так любой сможет заглянуть и увидеть даже соски."\n"Так в этом и вся идея!" не растерялись вы. "Могут увидеть, так ты еще соблазнительней покажешься, разве нет?'
                if str(people.location("liza") or "") == "TavernMain":
                    $ scene_runtime.text += ' Ты ведь хочешь чтобы тебя хотели, вон на Лизетту посмотри, она ничего не носит!'
                $ scene_runtime.text += '"\n"Ну, наверное ты прав," после небольшого колебания согласилась с вами Аманда, "помоги тогда."\nВы не замедлили оказать ей помощь, запустив руки под платье, расстегнув и затем вытащив лиф. Лишь потом вы поняли что даже и не попробовали отойти куда в сторонку.'
                $ agreed_to_redress = 1
        if agreed_to_redress == 1:
            $ Amanda.set_current_underwear("bra", "")
            $ Amanda.apply_social_chance(0, 0, 0, 60, 2, 1, "dress_change_bra")
        $ _other_saw = Amanda.dress_change_other_saw_text(GirlNameIAT, agreed_to_redress)
        if str(_other_saw or "").strip() != "":
            $ scene_runtime.text += "\n\n" + str(_other_saw)
        $ Amanda.mark_talked()
        $ scene_runtime.location_text = scene_runtime.text
        return

label IntAmandaDressChangeOfferPanties(GirlNameIAT="amanda", agreed_to_redress=0):
        $ renpy.dynamic("tmpLizaComandoBonus", "_other_saw")
        $ agreed_to_redress = 0
        $ tmpLizaComandoBonus = 0
        $ scene_runtime.text = '"Аманда, а чего ты в панталонах-то ходишь?" - поинтересовались вы как бы между делом у Аманды. "Они только тебя стесняют, без них ты и работу будешь сноровистей выполнять, да и сама себя будешь ощущать сексуальнее.'
        if str(people.location("liza") or "") == "TavernMain":
            $ scene_runtime.text += ' Разве ты не знаешь, что Лизетта, твоя лучшая подруга, без них ходит?" добавили вы для пущей убедительности. '
            if Liza.current_underwear("panties", "") == "":
                $ scene_runtime.text += '\n\n"И то правда," задумчиво сказала Аманда.'
                $ tmpLizaComandoBonus = min(10, Amanda.var_int("lizafriends", 0) // 2)
            else:
                $ scene_runtime.text += '\n\n"Лишь бы чего ляпнуть," укоризнено сказала вам Аманда, "я прекрасно знаю что это не так."'
                $ tmpLizaComandoBonus = -min(10, Amanda.var_int("lizafriends", 0) // 4)
        else:
            $ scene_runtime.text += '"'
        if DressPartSlut.get(DressBottomPart.get(Amanda.current_dress(), ""), 0) < 4:
            if Amanda.corruption + tmpLizaComandoBonus < 42:
                $ scene_runtime.text += '\n\n"Как тебе такое только в голову могло прийти! Мол сноровистей я буду работать. Я же каждую минуту буду думать, как бы мне кто под юбку не заглянул! Какая уж тут работа!"'
            else:
                $ scene_runtime.text += '\n\n"Ну, может оно и так," сказала Аманда. "Ведь никто ничего не увидит, значит все в порядке. Может и буду я шустрей работать. Надо попробовать."'
                $ agreed_to_redress = 1
                if Amanda.corruption < 50:
                    if procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:138:5") == 1:
                        $ scene_runtime.text += '\n\nАманда забежала на кухню, убедилась что там никого нет, и быстро стянула с себя панталончики.'
                    else:
                        $ scene_runtime.text += '\n\nАманда зашла за стойку, убедилась что по меньшей мере ее нижней половины не видно из зала, и стянула с себя эту деталь своего туалета. Впрочем вам она ее не отдала, а куда-то спрятала.'
                else:
                    $ scene_runtime.text += '\n\nНе особо-то скрываясь, Аманда слегка присела, сунула руку себе под подол, и стянула с себя панталончики, даже не проверив, не следит ли за ней кто из посетителей.'
        else:
            if Amanda.corruption + tmpLizaComandoBonus < 55:
                $ scene_runtime.text += '\n\n"Да ты издеваешься, Стефан?!," возмутилась Аманда в ответ на ваше предложение. "Ты мое платье видел? Если не видел, то вот, посмотри! Оно же попу едва закрывает! Если я наклонюсь, то всем посетителям свою девочку покажу. Какое уж тут, прости Ильматер, обслуживание, если все меня будут лапать. А лапать будут, ты сам наших посетителей знаешь!" '
            else:
                $ scene_runtime.text += '\n\n"Эх, Стефан," пошло улыбнулась Аманда. "Ты ведь прекрасно знаешь, что в таком коротком платьичке, да без панталончиков, каждый мою писю увидит. А ведь нагибаться придется, там со стола вытри, здесь кружки поставь. Это ты называешь лучшим обслуживанием?"\n"Именно это, ты все отлично поняла," не смутились вы.\n"Ой, уговорил, языкастый, попробуем!" с готовностью отозвалась Аманда.\nДаже не попытавшись уйти за стойку или еще куда, Аманда сунула руки под короткую юбочку и стянула с себя панталончики, показав на секунду свою щелку.'
                $ agreed_to_redress = 1
        if agreed_to_redress == 1:
            $ Amanda.set_current_underwear("panties", "")
            $ Amanda.apply_social_chance(0, 0, 0, 60, 2, 1, "dress_change_panties")
        $ _other_saw = Amanda.dress_change_other_saw_text(GirlNameIAT, agreed_to_redress)
        if str(_other_saw or "").strip() != "":
            $ scene_runtime.text += "\n\n" + str(_other_saw)
        $ Amanda.mark_talked()
        $ scene_runtime.location_text = scene_runtime.text
        return

label IntAmandaDressChangeShameBra(GirlNameIAT="amanda", agreed_to_redress=0):
        $ agreed_to_redress = 0
        $ scene_runtime.text = '"Аманда, а не стыдно тебе без лифа ходить?" - пристыдили вы Аманду. "Половина посетителей на тебя пялится!"'
        if str(Amanda.current_underwear("bra", "") or "") != "" or (str(Amanda.current_underwear("bra", "") or "") == "" and Amanda.corruption >= 50 and procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:164:6") == 1):
            $ scene_runtime.text += '\n\n"А с чего это ты решил что нету? Как это ты проверил? Во сне меня что ли без лифа представил?" пресекла ваши поучения Аманда. '
        else:
            $ scene_runtime.text += '\n\n"Ну да, ты же меня сам так надоумил," обескураженно ответила вам она.\n"Сказал что мол изгибы мои изумительные так лучше будут подчеркнуты, помнишь?"\n"Не помню!" Отрезали вы. "А если и сказал, то уже сожалею, погорячился я, как-то уж слишком пошло ты без него выглядишь."'
            if Amanda.corruption < 45:
                $ scene_runtime.text += '\n\n"Ну, коль ты теперь по-другому заговорил, то пойду и одену его обратно. Я себя и правда как-то неловко чувствовала."'
                $ agreed_to_redress = 1
            elif Amanda.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:171:7") <= 3:
                $ scene_runtime.text += '\n\n"Так вроде тебе нравилось, а сейчас ты вон как заговорил, "Не помнит" видите ли..." надулась Аманда, "хорошо, ладно, пойду наверх одену его."'
                $ agreed_to_redress = 1
                $ Amanda.apply_social_chance(7, 2, -1, 0, 0, 0, "dress_shame_bra")
            else:
                $ scene_runtime.text += '\n\n"Ай-яй, Стефан, значит ты у нас теперь скромник?!" засмеялась Аманда. "Ну а я, представь себе, нет! И я теперь уже взрослая и могу сама выбирать как мне одеваться! Так то!"'
                $ Amanda.apply_social_chance(7, 1, -1, 0, 0, 0, "dress_shame_bra")
        if agreed_to_redress == 1:
            $ Amanda.set_current_underwear("bra", "simplebra")
            $ Amanda.apply_social_chance(0, 0, 0, 30, 1, -1, "dress_shame_bra")
        $ Amanda.mark_talked()
        $ scene_runtime.location_text = scene_runtime.text
        return

label IntAmandaDressChangeShamePanties(GirlNameIAT="amanda", agreed_to_redress=0):
        $ agreed_to_redress = 0
        $ scene_runtime.text = '"Аманда, мне показалось что у тебя под юбкой ничего нет?" - пожурили вы Аманду. "И не стыдно?"'
        if str(Amanda.current_underwear("panties", "") or "") != "" or (str(Amanda.current_underwear("panties", "") or "") == "" and Amanda.corruption >= 45 and procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:189:8") == 1):
            $ scene_runtime.text += '\n\n"Ага, тебе показалось. А когда кажется, надо знак Ильматера вокруг себя очерчить, морок-то и пройдет," и Аманда убежала дальше.'
        else:
            $ scene_runtime.text += '\n\n"Так ты ж сам сказал, что мол без них работать мне удобнее будет, если мол движения не скованны."\n"Ага, удобнее, я же вижу как все посетители, когда ты им голой мандой светишь, руки распускать начинают. Какое уж тут удобнее. Не стыдно? Одела бы ты панталоны обратно, не позорила наше заведение!" отчитали вы бесстыдницу.'
            if Amanda.corruption < 45:
                $ scene_runtime.text += '\n\n"Ну, коль ты теперь по-другому заговорил, то пойду и одену их обратно. Я себя и правда как-то слишком неуютно чувствовала, все время юбку проверяла, не задралась ли."'
                $ agreed_to_redress = 1
            elif Amanda.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/IntAmandaDressChange.rpy:procedural_randint:196:9") <= 3:
                $ scene_runtime.text += '\n\n"Ага, сначала сам подначил, а теперь стыдит. Да ты издеваешься надо мной, а я, то дура, поверила." надулась Аманда, "ну ладно, пойду наверх одену."'
                $ agreed_to_redress = 1
                $ Amanda.apply_social_chance(7, 1, -1, 0, 0, 0, "dress_shame_panties")
            else:
                $ scene_runtime.text += '\n\n"Ага, позорила, уж кто бы говорил" засмеялась Аманда. "А чаевые, между прочим, так гораздо лучше дают! И вообще, я теперь уже взрослая и могу сама выбирать как мне одеваться! И ты мне в этом - не указ!"'
                $ Amanda.apply_social_chance(7, 1, -1, 0, 0, 0, "dress_shame_panties")
        if agreed_to_redress == 1:
            $ Amanda.set_current_underwear("panties", "simplepanties")
            $ Amanda.apply_social_chance(0, 0, 0, 30, 1, -1, "dress_shame_panties")
        $ Amanda.mark_talked()
        $ scene_runtime.location_text = scene_runtime.text
        return

label IntAmandaDressChangeBuyDress(GirlNameIAT="amanda"):
        $ scene_runtime.text = '"Амандочка, а хочешь я тебе обновку куплю?" - задали вы Аманде вопрос, хотя уже заранее знали на него ответ.\n"Конечно хочу!" Аманда даже подпрыгнула от радости и еле удержалась, чтобы не захлопать в ладоши.\n"Ну тогда завтра, с утра пораньше, дуй к Ирме Фараго, я буду тебя там ждать, вместе и выберем!" заверили вы Аманду.'
        $ daily_events.add(GirlNameIAT, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")
        $ Amanda.mark_talked()
        $ scene_runtime.location_text = scene_runtime.text
        return

