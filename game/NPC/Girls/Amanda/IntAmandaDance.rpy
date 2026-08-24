# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Amanda Dance Interaction Menu (Friday Dance Event)
# Converted from legacy script. Handles all Amanda dance menu options and outcomes.
# To be called from FridayDance or related event chains.

label story_amanda_friday_dance_mc_0:
    vscene "images/market/LocFridayDance.jpg"
    $ Amanda.dancing_with_legare = False
    $ rooms.get("FridayDance").dance_count += 1
    "Вы прошлись по площади, ища Аманду, и нашли ее скромно стоящей около одной из колонн."
    call ShowImage("amanda", "dance", "wait" + str(procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/IntAmandaDance.rpy:procedural_randint:14:1")))
    $ rooms.get("FridayDance").step = 1
    call IntAmandaDance
    return

label story_amanda_friday_dance_legare_0:
    vscene "images/market/LocFridayDance.jpg"
    $ GetDanceFromTable("amanda", "legare", rooms.get("FridayDance").dance_count)
    $ Amanda.dancing_with_legare = True
    call EventAmandaLegareCreateDance
    $ rooms.get("FridayDance").dance_count += 1
    if Amanda.escaped_dance_unnoticed:
        "Вы попробовали найти Аманду, но к своему удивлению не смогли этого сделать. На площади ее не было. Вокруг площади тоже. Может она отправилась домой, а может ее этот хрен Легаре за собой уволок, а может еще что стряслось, но так или иначе вы упустили Аманду."
        $ Amanda.left_friday_dance = True
        call FridayDanceCounterShow
        return
    "Вы прошлись по площади, ища Аманду, и обнаружили ее c мессиром Легаре."
    call ShowImage("amanda", "dance", "legare_step_0")
    $ rooms.get("FridayDance").step = 1
    call IntAmandaDance
    return

label IntAmandaDance():
    $ renpy.dynamic("GirlNameIAD", "_favor_result", "tmpGropeReact", "dance_message", "_amanda_legare_dance_advance", "legare_go_message")
    $ GirlNameIAD = 'amanda'
    $ rooms.get("FridayDance").max_step = 6
    $ Amanda.ensure_story_defaults()
    
    menu amanda_dance_menu:
        "Осмотреть" if rooms.get("FridayDance").step < 10:
            call GirlsDesc("amanda")
            jump IntAmandaDance
        "Поболтать" if rooms.get("FridayDance").step == 1 and not Amanda.dancing_with_legare:
            "Вы подошли к Аманде и начали с ней весело болтать о разной ерунде. За разговором незаметно пролетело время."
            if Amanda.rel >= 7:
                "Вы подумали что зря вы стали болтать с Амандой о ерунде. Ничего нового вы не узнали, а доверяет вам она и без пустого трепа."
            else:
                if procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/IntAmandaDance.rpy:procedural_randint:50:2") == 1:
                    $ Amanda.change_social(friend_delta=1)
                    "Кажется, Аманда стала еще больше восхищаться вами!"
            call ShowImage(GirlNameIAD, "dance", "you_invite_1.png")
            $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
            jump IntAmandaDance
        "Попросить об одолжении" if rooms.get("FridayDance").step == 1 and not Amanda.dancing_with_legare and Amanda.can_be_asked_for_night_bowl_favor():
            "Пока музыка еще не стихла, вы наклоняетесь к Аманде поближе и тихо просите ее об одолжении. Объясняете, что для хозяйственного дела вам очень пригодилась бы ее ночная миска, а взамен обещаете потом купить новую, красивее прежней."
            $ _favor_result = Amanda.night_bowl_request_result(True)
            if bool(_favor_result.get("granted", False)):
                "Подвыпившая Аманда сначала хихикает над странной просьбой, потом шепчет, что вы и впрямь умеете выбирать момент. Немного поколебавшись, она соглашается и обещает потом тихонько передать вам миску."
            else:
                "\"Нет уж, Стефан. Даже с вином в голове я не настолько безумна,\" шепчет Аманда и, смущенно улыбаясь, отмахивается от вашей просьбы."
            jump IntAmandaDance
        "Пригласить потанцевать" if rooms.get("FridayDance").step == 1 and not Amanda.dancing_with_legare:
            "Вы подошли к Аманде и пригласили ее потанцевать."
            $ rooms.get("FridayDance").hands = ''
            $ rooms.get("FridayDance").kiss = 0
            $ rooms.get("FridayDance").tits = 0
            if Amanda.rel >= 8 and Amanda.corruption > 15:
                "Она с радостью согласилась, вы взяли ее под руку и вскоре вы закружились в танце."
                call ShowImage(GirlNameIAD, "dance", "you_invites.png")
            elif Amanda.rel >= 5 and Amanda.corruption >= 5:
                "Она с сомнением сказала: 'Ты же Стефан, зачем это мне с тобой танцевать?', но все таки взяла вашу руку и вскоре вы закружились в танце."
                call ShowImage(GirlNameIAD, "dance", "you_invite_1.png")
            else:
                '"Ты что, Стефан, сдурел?!" ответила вам Аманда. Расстроенный отказом, вы отправились восвояси.'
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                call ShowImage(GirlNameIAD, "dance", "you_invite_1.png")
            $ rooms.get("FridayDance").step += 1
            if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Продолжить танцевать" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and not Amanda.dancing_with_legare:
            "Вы продолжили кружится в танце с Амандой."
            if rooms.get("FridayDance").hands == 'waist':
                "Ваши руки нежно обнимают талию Аманды."
            if rooms.get("FridayDance").hands == 'ass':
                "Ваши руки покоятся на попе Аманды."
            if rooms.get("FridayDance").hands == 'ass2':
                "Ваши руки нежно сжимают упругую попку Аманды через тонкую ткань ее платья."
            if rooms.get("FridayDance").kiss == 1:
                "Вы нежно целуете Аманду во время танца."
            if rooms.get("FridayDance").kiss == 2:
                "Вы страстно, переплетаясь языками, целуете Аманду, прилагая все усилия чтобы не сбиться с ритма."
            if rooms.get("FridayDance").tits > 0:
                "Аманда трется своими грудками о вашу грудь, потихоньку возбуждаясь."
            $ rooms.get("FridayDance").step += 1
            if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Положить руки на талию" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and not Amanda.dancing_with_legare and rooms.get("FridayDance").hands != 'waist':
            "Вы положили руки на талию Аманды."
            if Amanda.rel >= 6 and Amanda.corruption > 10:
                "Она улыбнулась и придвинулась к вам поближе, продолжая танец."
                $ Amanda.apply_social_chance(8, 5, 1, 14, 5, 1, "friday_dance_waist")
                $ rooms.get("FridayDance").hands = 'waist'
                call ShowImage(GirlNameIAD, "dance", "you_3.png")
            elif Amanda.rel >= 5 and Amanda.corruption >= 6:
                "Аманда поморщилась, но возражать не стала."
                $ Amanda.apply_social_chance(8, 5, 1, 14, 5, 1, "friday_dance_waist")
                $ rooms.get("FridayDance").hands = 'waist'
                call ShowImage(GirlNameIAD, "dance", "you_worry.png")
            else:
                '"Стефан, что ты такое делаешь?!" закричала Аманда. Вы попробовали объяснить, что так обычно танцуют, но обнаружили что разговариваете с пустотой, Аманда ушла.'
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                $ Amanda.apply_social_chance(2, 2, -1, 0, 0, 0, "friday_dance_waist_reject")
                $ rooms.get("FridayDance").hands = ''
                call ShowImage(GirlNameIAD, "dance", "you_nolike_1.png")
            $ rooms.get("FridayDance").step += 1
            if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Положить руки на попу" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and not Amanda.dancing_with_legare and rooms.get("FridayDance").hands == 'waist':
            if rooms.get("FridayDance").hands == 'waist':
                "Вы опустили руки с талии на попу Аманды."
            else:
                "Вы положили руки на попу Аманды."
            if Amanda.rel >= 7 and Amanda.corruption > 18:
                "Аманда улыбнулась и придвинулась к вам поближе, продолжая танец."
                $ Amanda.apply_social_chance(9, 3, 1, 18, 3, 1, "friday_dance_ass")
                $ rooms.get("FridayDance").hands = 'ass'
                call ShowImage(GirlNameIAD, "dance", "you_3.png")
            elif Amanda.rel >= 6 and Amanda.corruption >= 12:
                '"Стефан, что ты делаешь?!" прошептала Аманда. Впрочем танцевать она не перестала и рук ваших не убрала.'
                $ Amanda.apply_social_chance(9, 3, 1, 18, 3, 1, "friday_dance_ass")
                $ rooms.get("FridayDance").hands = 'ass'
                call ShowImage(GirlNameIAD, "dance", "you_2.png")
            elif Amanda.rel >= 5 and Amanda.corruption >= 9:
                '"Стефан, что ты делаешь?!" прошептала Аманда и передвинула ваши руки с попы на талию.'
                $ Amanda.apply_social_chance(9, 4, 1, 14, 4, 1, "friday_dance_ass_worry")
                $ rooms.get("FridayDance").hands = 'waist'
                call ShowImage(GirlNameIAD, "dance", "you_worry.png")
            else:
                '"Стефан, что ты такое делаешь?!" закричала Аманда, с размаху дала вам смачную пощечину, развернулась и ушла, оставив вас в одиночестве.'
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                $ Amanda.apply_social_chance(0, 1, -1, 0, 1, -1, "friday_dance_ass_reject")
                $ rooms.get("FridayDance").hands = ''
                call ShowImage(GirlNameIAD, "dance", "you_nolike_1.png")
            $ rooms.get("FridayDance").step += 1
            if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Сжать попу Аманды" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and not Amanda.dancing_with_legare and rooms.get("FridayDance").hands == 'ass':
            "Ваши беспокойные ручки начали гладить и сжимать попку Аманды."
            if Amanda.rel >= 10 and Amanda.corruption > 20:
                "Аманда улыбнулась и прижалась вплотную к вам, начав тереться своими сисечками о вашу грудь."
                $ Amanda.apply_social_chance(11, 4, 1, 22, 3, 1, "friday_dance_grope")
                $ rooms.get("FridayDance").hands = 'ass2'
                $ rooms.get("FridayDance").tits = 1
                call ShowImage(GirlNameIAD, "dance", "you_3.png")
            elif Amanda.rel >= 8 and Amanda.corruption >= 16:
                '"Стефанчик, что ты делаешь?! Мы же все-таки не на виду у всех" прошептала Аманда, но не сделала ничего, чтобы остановить вас.'
                $ Amanda.apply_social_chance(11, 4, 1, 22, 3, 1, "friday_dance_grope")
                $ rooms.get("FridayDance").hands = 'ass2'
                call ShowImage(GirlNameIAD, "dance", "you_2.png")
            elif Amanda.rel >= 7 and Amanda.corruption >= 13:
                '"Стефан, что ты делаешь?!" прошептала Аманда и передвинула ваши руки с попы на талию.'
                $ Amanda.apply_social_chance(9, 4, 1, 16, 4, 1, "friday_dance_grope_worry")
                $ rooms.get("FridayDance").hands = 'waist'
                call ShowImage(GirlNameIAD, "dance", "you_worry.png")
            else:
                '"Стефан, что ты такое делаешь?!" закричала Аманда, с размаху дала вам смачную пощечину, развернулась и ушла, оставив вас в одиночестве.'
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                $ Amanda.apply_social_chance(0, 1, -1, 0, 1, -1, "friday_dance_grope_reject")
                $ rooms.get("FridayDance").hands = ''
                call ShowImage(GirlNameIAD, "dance", "you_nolike_1.png")
            $ rooms.get("FridayDance").step += 1
            if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Поцеловать Аманду" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and not Amanda.dancing_with_legare and rooms.get("FridayDance").kiss == 0:
            "Продолжая танцевать, вы вдруг наклонились к Аманде и впились в ее губы своими."
            if Amanda.rel >= 10 and Amanda.corruption > 21:
                "Аманда с готовностью ответила на ваш поцелуй, страстно переплетаясь с вами языками."
                $ Amanda.apply_social_chance(11, 4, 1, 24, 3, 1, "friday_dance_kiss")
                $ rooms.get("FridayDance").kiss = 2
                call ShowImage(GirlNameIAD, "dance", "you_kiss.png")
            elif Amanda.rel >= 8 and Amanda.corruption >= 16:
                "Преодолев секундное замешательство, Аманда откликнулась на ваш поцелуй, хотя и без особого энтузиазма."
                $ Amanda.apply_social_chance(11, 4, 1, 24, 3, 1, "friday_dance_kiss")
                $ rooms.get("FridayDance").kiss = 1
                call ShowImage(GirlNameIAD, "dance", "you_kiss.png")
            elif Amanda.rel >= 7 and Amanda.corruption >= 13:
                '"Стефанчик, что ты делаешь?!" прошептала Аманда и отстранилась от вас.'
                $ Amanda.apply_social_chance(9, 6, 1, 16, 6, 1, "friday_dance_kiss_worry")
                $ rooms.get("FridayDance").kiss = 0
                call ShowImage(GirlNameIAD, "dance", "you_worry.png")
            else:
                '"Стефан, что ты такое делаешь?!" закричала Аманда, с размаху дала вам смачную пощечину, развернулась и ушла, оставив вас в одиночестве.'
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                $ Amanda.apply_social_chance(0, 1, -1, 0, 1, -1, "friday_dance_kiss_reject")
                $ rooms.get("FridayDance").kiss = 0
                call ShowImage(GirlNameIAD, "dance", "you_nolike_1.png")
            $ rooms.get("FridayDance").step += 1
            if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                "Танец закончился и вы вернулись к колоннаде."
            jump IntAmandaDance
        "Предложить Аманде прогулятся" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and not Amanda.dancing_with_legare and Amanda.sex_stat("sexacts", 0) > 0 and (rooms.get("FridayDance").hands.startswith('ass') or rooms.get("FridayDance").kiss > 0):
            $ tmpGropeReact = Amanda.sex_offer_reaction()
            if tmpGropeReact == 2:
                "Продолжая танцевать, вы вдруг прошептали Аманде на ушко: 'Милая, а может прогуляемся немного?'"
                '"Ага, значит то ты меня ругаешь, шлюхой обзываешь, учишь скромности и всякому возвышенному да? Ф как танцы - так все мигом забыл и мало что за задницу лапаешь, так еще и в подворотню тащищь?" обругала ваше двуличие Аманда.{p}"Знаешь что, иди себе сам в свою подворотню и сам с собою там что хочешь то и делай. Впрочем, ты только одного и хочешь. А я пока пойду!" гневно сказала Аманда, слово с делом у нее не разошлись и она развернулась и ушла, оставив вас в одиночестве.'
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                $ Amanda.apply_social_chance(0, 3, -1, 0, 3, -1, "friday_dance_walk_reject")
                call ShowImage(GirlNameIAD, "dance", "you_nolike_1.png")
            elif tmpGropeReact >= 3:
                $ Amanda.left_friday_dance = True
                $ GirlDance_DeleteGirl('amanda')
                $ rooms.get("FridayDance").dance_count = 5
                call ShowImage(GirlNameIAD, "dance", "you_invites.png")
                jump AmandaAfterDanceMC
            else:
                "Продолжая танцевать, вы вдруг прошептали Аманде на ушко: 'Милая, а может прогуляемся немного?'"
                '"Стефан, ты что, предлагаешь мне пойти с тобой в какую-то подворотню? Мне?!" гневно сказала Аманда, развернулась и ушла, оставив вас в одиночестве.'
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                $ Amanda.apply_social_chance(0, 1, -1, 0, 1, -1, "friday_dance_walk_reject")
                call ShowImage(GirlNameIAD, "dance", "you_nolike_1.png")
            jump IntAmandaDance
            
        "Наблюдать за Амандой и мессиром Легаре" if rooms.get("FridayDance").step >= 1 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step + 2 and Amanda.dancing_with_legare:
            if rooms.get("FridayDance").step == 1:
                "Вы посмотрели на Аманду и мессира Легаре."
            
            # Safe way to show dialogue based on dance step
            $ dance_message = ""
            $ _amanda_legare_dance_advance = Amanda.legare_dance_advance_level()
            if rooms.get("FridayDance").step - 1 <= _amanda_legare_dance_advance:
                $ dance_message = SexEvents.dance_watch_line[rooms.get("FridayDance").step]
            elif _amanda_legare_dance_advance == 0:
                $ dance_message = SexEvents.dance_watch_line[1]
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step + 1
            else:
                $ dance_message = SexEvents.dance_watch_line[0]
            
            "[dance_message]"
            call ShowImage("amanda", "dance", "legare_step_" + str(min(rooms.get("FridayDance").step, 3)) + ".png")
            
            if rooms.get("FridayDance").step == 6 and Amanda.legare_departure_code == 1:
                $ legare_go_message = str(SexEvents.dance_watch_line.get(6, "") or "")
                if legare_go_message != "" and dance_message != legare_go_message:
                    "[legare_go_message]"
                $ Amanda.legare_departure_code = 0
                call LegareAmandaGoMenu
            $ rooms.get("FridayDance").step += 1
                
            if rooms.get("FridayDance").step >= rooms.get("FridayDance").max_step + 2:
                "Музыка доиграла и Аманда с мессиром Легаре разошлись."
            jump IntAmandaDance
            
        "Вмешаться и разогнать их" if rooms.get("FridayDance").step >= 1 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step + 2 and Amanda.dancing_with_legare:
            "Нежелая больше смотреть на это непотребство вы решительно подошли к парочке и заявили:\n'Мессир! Что вы себе позволяете?! У вас же есть дети старше Аманды, да и вы женаты! А ты что возомнила?! Разве ты не видишь, что он ей по возрасту годится в опекуны! А ну, кыш отседа и чтобы больше я такого не видел!'"
            
            if Amanda.legare_forbidden:
                "\"Да и вообще, я тебе ведь уже запрещал с ним танцевать, а ты опять за старое! Или ты оглохла или память потеряла?\" продолжаете орать вы."
                
            "Нахмурившись от выволочки, что вы ему учинили, мессир Легаре мрачно удалился."
            $ Alber.add_relation(-4)
            
            if Amanda.legare_affection >= 7:
                "\"Как ты смеешь лезть в мою личную жизнь, Стефан?! Я уже взрослая и могу сама решать! А Альбер мне очень-очень нравится, ну и что что он женат!\" закричала Аманда и убежала рыдая."
                $ Amanda.legare_affection += 3
                $ Amanda.apply_social_chance(3, 1, -5, 0, 0, 0, "friday_dance_intervene")
            else:
                "\"Хорошо,\" только и сказала Аманда. Но вам показалось что под внешней покорностью девчонка затаила обиду."
                $ Amanda.legare_affection -= 1
                $ Amanda.apply_social_chance(3, 1, -2, 15, 1, -4, "friday_dance_intervene")
            $ Amanda.legare_forbidden = True
            $ Amanda.left_friday_dance = True
            $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step + 2
            $ Amanda.dancing_with_legare = False
            $ GirlDance_DeleteGirl('amanda')
            jump IntAmandaDance
        "Отойти" if rooms.get("FridayDance").step >= rooms.get("FridayDance").max_step or Amanda.dancing_with_legare or rooms.get("FridayDance").step == 1:
            $ rooms.get("FridayDance").step = 0
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
