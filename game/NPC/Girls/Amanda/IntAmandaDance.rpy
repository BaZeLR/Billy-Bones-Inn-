# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Amanda Dance Interaction Menu (Friday Dance Event)
# Converted from legacy script. Handles all Amanda dance menu options and outcomes.
# To be called from FridayDance or related event chains.

label story_amanda_friday_dance_mc_0:
    vscene "images/market/LocFridayDance.jpg"
    $ Amanda.set_var_int("albernowdances", 0)
    $ Amanda.set_var_int("legare_dance_pending", 0)
    $ FridayDanceRoom.state["dance_count"] += 1
    "Вы прошлись по площади, ища Аманду, и нашли ее скромно стоящей около одной из колонн."
    call ShowImage("amanda", "dance", "wait" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDance.rpy:procedural_randint:14:1")))
    $ DanceStep = 1
    call IntAmandaDance
    return

label story_amanda_friday_dance_legare_0:
    vscene "images/market/LocFridayDance.jpg"
    $ Amanda.set_var_int("albernowdances", 1)
    $ Amanda.set_var_int("legare_dance_pending", 0)
    call EventAmandaLegareCreateDance
    $ FridayDanceRoom.state["dance_count"] += 1
    if Amanda.var_int("EscapeUnnoticed", 0) == 1:
        "Вы попробовали найти Аманду, но к своему удивлению не смогли этого сделать. На площади ее не было. Вокруг площади тоже. Может она отправилась домой, а может ее этот хрен Легаре за собой уволок, а может еще что стряслось, но так или иначе вы упустили Аманду."
        $ Amanda.set_var_int("leftdances", 1)
        call FridayDanceCounterShow
        return
    "Вы прошлись по площади, ища Аманду, и обнаружили ее c мессиром Легаре."
    call ShowImage("amanda", "dance", "legare_step_0")
    $ DanceStep = 1
    call IntAmandaDance
    return

label IntAmandaDance():
    $ GirlNameIAD = 'amanda'
    $ DanceMaxIAD = 6
    $ Amanda.ensure_story_defaults()
    
    menu amanda_dance_menu:
        "Осмотреть" if DanceStep < 10:
            call GirlsDesc("amanda")
            jump IntAmandaDance
        "Поболтать" if DanceStep == 1 and Amanda.var_int("albernowdances", 0) == 0:
            "Вы подошли к Аманде и начали с ней весело болтать о разной ерунде. За разговором незаметно пролетело время."
            if Amanda.rel >= 7:
                "Вы подумали что зря вы стали болтать с Амандой о ерунде. Ничего нового вы не узнали, а доверяет вам она и без пустого трепа."
            else:
                if procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/IntAmandaDance.rpy:procedural_randint:50:2") == 1:
                    $ Amanda.change_social(friend_delta=1)
                    "Кажется, Аманда стала еще больше восхищаться вами!"
            call ShowImage(GirlNameIAD, "dance", "YouInvite1")
            $ DanceStep = DanceMaxIAD
            jump IntAmandaDance
        "Попросить об одолжении" if DanceStep == 1 and Amanda.var_int("albernowdances", 0) == 0 and amanda_can_be_asked_for_night_bowl_favor():
            "Пока музыка еще не стихла, вы наклоняетесь к Аманде поближе и тихо просите ее об одолжении. Объясняете, что для хозяйственного дела вам очень пригодилась бы ее ночная миска, а взамен обещаете потом купить новую, красивее прежней."
            $ _favor_result = amanda_night_bowl_request_result(True)
            if bool(_favor_result.get("granted", False)):
                "Подвыпившая Аманда сначала хихикает над странной просьбой, потом шепчет, что вы и впрямь умеете выбирать момент. Немного поколебавшись, она соглашается и обещает потом тихонько передать вам миску."
            else:
                "\"Нет уж, Стефан. Даже с вином в голове я не настолько безумна,\" шепчет Аманда и, смущенно улыбаясь, отмахивается от вашей просьбы."
            jump IntAmandaDance
        "Пригласить потанцевать" if DanceStep == 1 and Amanda.var_int("albernowdances", 0) == 0:
            "Вы подошли к Аманде и пригласили ее потанцевать."
            $ HandsDance = ''
            $ KissDance = 0
            $ TitsDance = 0
            if Amanda.rel >= 8 and Amanda.corruption > 15:
                "Она с радостью согласилась, вы взяли ее под руку и вскоре вы закружились в танце."
                call ShowImage(GirlNameIAD, "dance", "YouInvite2")
            elif Amanda.rel >= 5 and Amanda.corruption >= 5:
                "Она с сомнением сказала: 'Ты же Стефан, зачем это мне с тобой танцевать?', но все таки взяла вашу руку и вскоре вы закружились в танце."
                call ShowImage(GirlNameIAD, "dance", "YouInvite1")
            else:
                '"Ты что, Стефан, сдурел?!" ответила вам Аманда. Расстроенный отказом, вы отправились восвояси.'
                $ DanceStep = DanceMaxIAD
                call ShowImage(GirlNameIAD, "dance", "YouInvite1")
            $ DanceStep += 1
            if DanceStep == DanceMaxIAD:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Продолжить танцевать" if DanceStep >= 2 and DanceStep < DanceMaxIAD and Amanda.var_int("albernowdances", 0) == 0:
            "Вы продолжили кружится в танце с Амандой."
            if HandsDance == 'waist':
                "Ваши руки нежно обнимают талию Аманды."
            if HandsDance == 'ass':
                "Ваши руки покоятся на попе Аманды."
            if HandsDance == 'ass2':
                "Ваши руки нежно сжимают упругую попку Аманды через тонкую ткань ее платья."
            if KissDance == 1:
                "Вы нежно целуете Аманду во время танца."
            if KissDance == 2:
                "Вы страстно, переплетаясь языками, целуете Аманду, прилагая все усилия чтобы не сбиться с ритма."
            if TitsDance > 0:
                "Аманда трется своими грудками о вашу грудь, потихоньку возбуждаясь."
            $ DanceStep += 1
            if DanceStep == DanceMaxIAD:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Положить руки на талию" if DanceStep >= 2 and DanceStep < DanceMaxIAD and Amanda.var_int("albernowdances", 0) == 0 and HandsDance != 'waist':
            "Вы положили руки на талию Аманды."
            if Amanda.rel >= 6 and Amanda.corruption > 10:
                "Она улыбнулась и придвинулась к вам поближе, продолжая танец."
                $ Amanda.apply_social_chance(8, 5, 1, 14, 5, 1, "friday_dance_waist")
                $ HandsDance = 'waist'
                call ShowImage(GirlNameIAD, "dance", "YouClose")
            elif Amanda.rel >= 5 and Amanda.corruption >= 6:
                "Аманда поморщилась, но возражать не стала."
                $ Amanda.apply_social_chance(8, 5, 1, 14, 5, 1, "friday_dance_waist")
                $ HandsDance = 'waist'
                call ShowImage(GirlNameIAD, "dance", "YouDanceWorry")
            else:
                '"Стефан, что ты такое делаешь?!" закричала Аманда. Вы попробовали объяснить, что так обычно танцуют, но обнаружили что разговариваете с пустотой, Аманда ушла.'
                $ DanceStep = DanceMaxIAD
                $ Amanda.apply_social_chance(2, 2, -1, 0, 0, 0, "friday_dance_waist_reject")
                $ HandsDance = ''
                call ShowImage(GirlNameIAD, "dance", "YouDanceAngry")
            $ DanceStep += 1
            if DanceStep == DanceMaxIAD:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Положить руки на попу" if DanceStep >= 2 and DanceStep < DanceMaxIAD and Amanda.var_int("albernowdances", 0) == 0 and HandsDance == 'waist':
            if HandsDance == 'waist':
                "Вы опустили руки с талии на попу Аманды."
            else:
                "Вы положили руки на попу Аманды."
            if Amanda.rel >= 7 and Amanda.corruption > 18:
                "Аманда улыбнулась и придвинулась к вам поближе, продолжая танец."
                $ Amanda.apply_social_chance(9, 3, 1, 18, 3, 1, "friday_dance_ass")
                $ HandsDance = 'ass'
                call ShowImage(GirlNameIAD, "dance", "YouClose")
            elif Amanda.rel >= 6 and Amanda.corruption >= 12:
                '"Стефан, что ты делаешь?!" прошептала Аманда. Впрочем танцевать она не перестала и рук ваших не убрала.'
                $ Amanda.apply_social_chance(9, 3, 1, 18, 3, 1, "friday_dance_ass")
                $ HandsDance = 'ass'
                call ShowImage(GirlNameIAD, "dance", "YouDance")
            elif Amanda.rel >= 5 and Amanda.corruption >= 9:
                '"Стефан, что ты делаешь?!" прошептала Аманда и передвинула ваши руки с попы на талию.'
                $ Amanda.apply_social_chance(9, 4, 1, 14, 4, 1, "friday_dance_ass_worry")
                $ HandsDance = 'waist'
                call ShowImage(GirlNameIAD, "dance", "YouDanceWorry")
            else:
                '"Стефан, что ты такое делаешь?!" закричала Аманда, с размаху дала вам смачную пощечину, развернулась и ушла, оставив вас в одиночестве.'
                $ DanceStep = DanceMaxIAD
                $ Amanda.apply_social_chance(0, 1, -1, 0, 1, -1, "friday_dance_ass_reject")
                $ HandsDance = ''
                call ShowImage(GirlNameIAD, "dance", "YouDanceAngry")
            $ DanceStep += 1
            if DanceStep == DanceMaxIAD:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Сжать попу Аманды" if DanceStep >= 2 and DanceStep < DanceMaxIAD and Amanda.var_int("albernowdances", 0) == 0 and HandsDance == 'ass':
            "Ваши беспокойные ручки начали гладить и сжимать попку Аманды."
            if Amanda.rel >= 10 and Amanda.corruption > 20:
                "Аманда улыбнулась и прижалась вплотную к вам, начав тереться своими сисечками о вашу грудь."
                $ Amanda.apply_social_chance(11, 4, 1, 22, 3, 1, "friday_dance_grope")
                $ HandsDance = 'ass2'
                $ TitsDance = 1
                call ShowImage(GirlNameIAD, "dance", "YouClose")
            elif Amanda.rel >= 8 and Amanda.corruption >= 16:
                '"Стефанчик, что ты делаешь?! Мы же все-таки не на виду у всех" прошептала Аманда, но не сделала ничего, чтобы остановить вас.'
                $ Amanda.apply_social_chance(11, 4, 1, 22, 3, 1, "friday_dance_grope")
                $ HandsDance = 'ass2'
                call ShowImage(GirlNameIAD, "dance", "YouDance")
            elif Amanda.rel >= 7 and Amanda.corruption >= 13:
                '"Стефан, что ты делаешь?!" прошептала Аманда и передвинула ваши руки с попы на талию.'
                $ Amanda.apply_social_chance(9, 4, 1, 16, 4, 1, "friday_dance_grope_worry")
                $ HandsDance = 'waist'
                call ShowImage(GirlNameIAD, "dance", "YouDanceWorry")
            else:
                '"Стефан, что ты такое делаешь?!" закричала Аманда, с размаху дала вам смачную пощечину, развернулась и ушла, оставив вас в одиночестве.'
                $ DanceStep = DanceMaxIAD
                $ Amanda.apply_social_chance(0, 1, -1, 0, 1, -1, "friday_dance_grope_reject")
                $ HandsDance = ''
                call ShowImage(GirlNameIAD, "dance", "YouDanceAngry")
            $ DanceStep += 1
            if DanceStep == DanceMaxIAD:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Поцеловать Аманду" if DanceStep >= 2 and DanceStep < DanceMaxIAD and Amanda.var_int("albernowdances", 0) == 0 and KissDance == 0:
            "Продолжая танцевать, вы вдруг наклонились к Аманде и впились в ее губы своими."
            if Amanda.rel >= 10 and Amanda.corruption > 21:
                "Аманда с готовностью ответила на ваш поцелуй, страстно переплетаясь с вами языками."
                $ Amanda.apply_social_chance(11, 4, 1, 24, 3, 1, "friday_dance_kiss")
                $ KissDance = 2
                call ShowImage(GirlNameIAD, "dance", "YouKiss")
            elif Amanda.rel >= 8 and Amanda.corruption >= 16:
                "Преодолев секундное замешательство, Аманда откликнулась на ваш поцелуй, хотя и без особого энтузиазма."
                $ Amanda.apply_social_chance(11, 4, 1, 24, 3, 1, "friday_dance_kiss")
                $ KissDance = 1
                call ShowImage(GirlNameIAD, "dance", "YouKiss")
            elif Amanda.rel >= 7 and Amanda.corruption >= 13:
                '"Стефанчик, что ты делаешь?!" прошептала Аманда и отстранилась от вас.'
                $ Amanda.apply_social_chance(9, 6, 1, 16, 6, 1, "friday_dance_kiss_worry")
                $ KissDance = 0
                call ShowImage(GirlNameIAD, "dance", "YouDanceWorry")
            else:
                '"Стефан, что ты такое делаешь?!" закричала Аманда, с размаху дала вам смачную пощечину, развернулась и ушла, оставив вас в одиночестве.'
                $ DanceStep = DanceMaxIAD
                $ Amanda.apply_social_chance(0, 1, -1, 0, 1, -1, "friday_dance_kiss_reject")
                $ KissDance = 0
                call ShowImage(GirlNameIAD, "dance", "YouDanceAngry")
            $ DanceStep += 1
            if DanceStep == DanceMaxIAD:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Предложить Аманде прогулятся" if DanceStep >= 2 and DanceStep < DanceMaxIAD and Amanda.var_int("albernowdances", 0) == 0 and Amanda.sex_stat("sexacts", 0) > 0 and (HandsDance.startswith('ass') or KissDance > 0):
            $ tmpGropeReact = Amanda.sex_offer_reaction()
            if tmpGropeReact == 2:
                "Продолжая танцевать, вы вдруг прошептали Аманде на ушко: 'Милая, а может прогуляемся немного?'"
                '"Ага, значит то ты меня ругаешь, шлюхой обзываешь, учишь скромности и всякому возвышенному да? Ф как танцы - так все мигом забыл и мало что за задницу лапаешь, так еще и в подворотню тащищь?" обругала ваше двуличие Аманда.{p}"Знаешь что, иди себе сам в свою подворотню и сам с собою там что хочешь то и делай. Впрочем, ты только одного и хочешь. А я пока пойду!" гневно сказала Аманда, слово с делом у нее не разошлись и она развернулась и ушла, оставив вас в одиночестве.'
                $ DanceStep = DanceMaxIAD
                $ Amanda.apply_social_chance(0, 3, -1, 0, 3, -1, "friday_dance_walk_reject")
                call ShowImage(GirlNameIAD, "dance", "YouDanceAngry")
            elif tmpGropeReact >= 3:
                $ Amanda.set_var_int("leftdances", 1)
                $ GirlDance_DeleteGirl('amanda')
                $ FridayDanceRoom.state["dance_count"] = 5
                call ShowImage(GirlNameIAD, "dance", "YouInvite2")
                jump AmandaAfterDanceMC
            else:
                "Продолжая танцевать, вы вдруг прошептали Аманде на ушко: 'Милая, а может прогуляемся немного?'"
                '"Стефан, ты что, предлагаешь мне пойти с тобой в какую-то подворотню? Мне?!" гневно сказала Аманда, развернулась и ушла, оставив вас в одиночестве.'
                $ DanceStep = DanceMaxIAD
                $ Amanda.apply_social_chance(0, 1, -1, 0, 1, -1, "friday_dance_walk_reject")
                call ShowImage(GirlNameIAD, "dance", "YouDanceAngry")
            jump IntAmandaDance
            
        "Наблюдать за Амандой и мессиром Легаре" if DanceStep >= 1 and DanceStep < DanceMaxIAD + 2 and Amanda.var_int("albernowdances", 0) == 1:
            if DanceStep == 1:
                "Вы посмотрели на Аманду и мессира Легаре."
            
            # Safe way to show dialogue based on dance step
            $ dance_message = ""
            if DanceStep - 1 <= Amanda.var_int("alberdanceadvance", 0):
                $ dance_message = SexEvents.dance_watch_line[DanceStep]
            elif Amanda.var_int("alberdanceadvance", 0) == 0:
                $ dance_message = SexEvents.dance_watch_line[1]
                $ DanceStep = DanceMaxIAD + 1
            else:
                $ dance_message = SexEvents.dance_watch_line[0]
            
            "[dance_message]"
            call ShowImage("amanda", "dance", "alberdanceStep" + str(min(DanceStep, 3)))
            
            if DanceStep == 6 and Amanda.var_int("LegareGo", 0) == 1:
                $ legare_go_message = str(SexEvents.dance_watch_line.get(6, "") or "")
                if legare_go_message != "" and dance_message != legare_go_message:
                    "[legare_go_message]"
                $ Amanda.set_var_int("LegareGo", 0)
                call LegareAmandaGoMenu
            $ DanceStep += 1
                
            if DanceStep >= DanceMaxIAD + 2:
                "Музыка доиграла и Аманда с мессиром Легаре разошлись."
            jump IntAmandaDance
            
        "Вмешаться и разогнать их" if DanceStep >= 1 and DanceStep < DanceMaxIAD + 2 and Amanda.var_int("albernowdances", 0) == 1:
            "Нежелая больше смотреть на это непотребство вы решительно подошли к парочке и заявили:\n'Мессир! Что вы себе позволяете?! У вас же есть дети старше Аманды, да и вы женаты! А ты что возомнила?! Разве ты не видишь, что он ей по возрасту годится в опекуны! А ну, кыш отседа и чтобы больше я такого не видел!'"
            
            if Amanda.var_int("alberprohibit", 0) == 1:
                "\"Да и вообще, я тебе ведь уже запрещал с ним танцевать, а ты опять за старое! Или ты оглохла или память потеряла?\" продолжаете орать вы."
                
            "Нахмурившись от выволочки, что вы ему учинили, мессир Легаре мрачно удалился."
            $ Alber.add_relation(-4)
            
            if Amanda.var_int("alberfriends", 0) >= 7:
                "\"Как ты смеешь лезть в мою личную жизнь, Стефан?! Я уже взрослая и могу сама решать! А Альбер мне очень-очень нравится, ну и что что он женат!\" закричала Аманда и убежала рыдая."
                $ Amanda.set_var_int("alberfriends", Amanda.var_int("alberfriends", 0) + 3)
                $ Amanda.apply_social_chance(3, 1, -5, 0, 0, 0, "friday_dance_intervene")
            else:
                "\"Хорошо,\" только и сказала Аманда. Но вам показалось что под внешней покорностью девчонка затаила обиду."
                $ Amanda.set_var_int("alberfriends", Amanda.var_int("alberfriends", 0) - 1)
                $ Amanda.apply_social_chance(3, 1, -2, 15, 1, -4, "friday_dance_intervene")
            $ Amanda.set_var_int("alberprohibit", 1)
            $ Amanda.set_var_int("leftdances", 1)
            $ DanceStep = DanceMaxIAD + 2
            $ Amanda.set_var_int("albernowdances", 0)
            $ GirlDance_DeleteGirl('amanda')
            jump IntAmandaDance
        "Отойти" if DanceStep >= DanceMaxIAD or Amanda.var_int("albernowdances", 0) == 1 or DanceStep == 1:
            $ DanceStep = 0
            call ShowImage(GirlNameIAD, "dance", "wait" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDance.rpy:procedural_randint:284:3")))
            return
    return

# # Helper labels for menu actions
# label girls_desc(girl):
#     # ...show girl description...
#     return

#     # ...logic for increasing slut friends...
#     return

# label clean_screen_overflow():
#     # ...logic for cleaning screen overflow...
#     return

# label amanda_sex_dance_street():
#     # ...Amanda sex dance street event...
#     return
