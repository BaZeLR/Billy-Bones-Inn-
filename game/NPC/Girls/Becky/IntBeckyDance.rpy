# ================================================================================
# Becky Dance Interaction Menu (Friday dance event).
# Label owns the dance scene, choices, state changes, and the home invitation branch.
# ================================================================================

label story_becky_friday_dance_mc_0:
    $ main_ui_begin_native_scene_state("Танец с Бекки")
    $ scene_runtime.text = ""
    $ scene_runtime.location_text = ""
    vscene "images/market/LocFridayDance.jpg"
    $ rooms.get("FridayDance").becky_home_invited = False
    $ rooms.get("FridayDance").dance_count += 1
    "Вы прошлись по площади, ища вдовушку Блэнкеншип, и нашли ее болтающей с другими торговками."
    call ShowImage("becky", "dance", "waiting_0")
    $ rooms.get("FridayDance").step = 1
    call int_becky_dance
    $ main_ui_end_native_scene_state()
    return

label int_becky_dance():
    $ renpy.dynamic("GirlNameIBD")
    $ GirlNameIBD = "becky"
    $ rooms.get("FridayDance").max_step = 6
    $ scene_runtime.picture = "images/becky/dance/waiting_0.png"
    vscene scene_runtime.picture

    while True:
        if rooms.get("FridayDance").step == 0:
            return

        menu:
            "Осмотреть" if rooms.get("FridayDance").step < 10:
                call GirlsDesc(GirlNameIBD)

            "Поболтать" if rooms.get("FridayDance").step == 1:
                $ scene_runtime.picture = "images/becky/dance/you_talk_1.png"
                vscene scene_runtime.picture
                "Вы подошли к веселой вдовушке и начали сыпать шутками и прибаутками, веселя ее. За разговором незаметно пролетело время."
                if Becky.rel >= 7:
                    "Вы подумали, что зря тратите время. Ничего нового вы не узнали, а Бекки и так знает, что вы шутник хоть куда."
                elif procedural_randint(1, 3, "becky_dance_talk_%s_%s" % (int(current_game_day() or 0), rooms.get("FridayDance").dance_count)) == 1:
                    $ Becky.add_relation(1, cap=100)
                    "Вы очень развеселили Бекки своими шутками!"
                $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step

            "Пригласить потанцевать" if rooms.get("FridayDance").step == 1:
                "Вы подошли к вдове Блэнкеншип и пригласили ее потанцевать."
                $ rooms.get("FridayDance").hands = ""
                $ rooms.get("FridayDance").kiss = 0
                $ rooms.get("FridayDance").tits = 0
                if Becky.rel >= 7 and Becky.corruption > 18:
                    $ scene_runtime.picture = "images/becky/dance/you_dance_2.png"
                    vscene scene_runtime.picture
                    "Она с радостью согласилась, вы взяли ее под руку и вскоре вы закружились в танце."
                elif Becky.rel >= 5 and Becky.corruption >= 8:
                    $ scene_runtime.picture = "images/becky/dance/you_dance_2.png"
                    vscene scene_runtime.picture
                    "Она сказала: \"Стефан, Стефан, неужели ты действительно хочешь танцевать с такой практически старухой как я? Я же даже постарше вашей Сандры буду. Ну ладно, если ты так настаиваешь,\" - и она взяла вашу руку. Вскоре вы закружились в танце."
                else:
                    $ scene_runtime.picture = "images/becky/dance/waiting_0.png"
                    vscene scene_runtime.picture
                    "\"Стефан, если ты хочешь танцевать со старой тетей, то пригласи свою бабушку Сандру, если хочешь!\" - ответила вам вдова. Расстроенный отказом, вы отправились восвояси."
                    $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                $ rooms.get("FridayDance").step += 1
                if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                    "Танец закончился и вы вернулись к колоннаде."

            "Продолжить танцевать" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step:
                if rooms.get("FridayDance").kiss == 2:
                    $ scene_runtime.picture = "images/becky/dance/french_kiss_2.png"
                elif rooms.get("FridayDance").kiss == 1:
                    $ scene_runtime.picture = "images/becky/dance/you_dance_7.png"
                elif rooms.get("FridayDance").hands == "ass2":
                    $ scene_runtime.picture = "images/becky/dance/you dance_6.png"
                elif rooms.get("FridayDance").hands == "ass":
                    $ scene_runtime.picture = "images/becky/dance/you_dance_5.png"
                elif rooms.get("FridayDance").hands == "waist":
                    $ scene_runtime.picture = "images/becky/dance/you_dance_4.png"
                else:
                    $ scene_runtime.picture = "images/becky/dance/you dance_3.png"
                vscene scene_runtime.picture
                "Вы продолжили кружиться в танце с Бекки."
                if rooms.get("FridayDance").hands == "waist":
                    "Ваши руки нежно обнимают талию вдовушки."
                if rooms.get("FridayDance").hands == "ass":
                    "Ваши руки покоятся на все еще упругой попке вдовы."
                if rooms.get("FridayDance").hands == "ass2":
                    "Ваши руки нежно сжимают попу Бекки через платье."
                if rooms.get("FridayDance").kiss == 1:
                    "Вы нежно целуете Бекки во время танца."
                if rooms.get("FridayDance").kiss == 2:
                    "Вы страстно, переплетаясь языками, целуете Бекки, прилагая все усилия, чтобы не сбиться с ритма."
                if rooms.get("FridayDance").tits > 0:
                    "Бекки трется своей огромной грудью о вас, потихоньку возбуждаясь."
                $ rooms.get("FridayDance").step += 1
                call BeckyInviteHome("becky")
                if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                    "Танец закончился и вы вернулись к колоннаде."

            "Положить руки на талию" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and rooms.get("FridayDance").hands != "waist":
                "Вы положили руки на талию Бекки."
                if Becky.rel >= 7 and Becky.corruption > 10:
                    $ scene_runtime.picture = "images/becky/dance/you_dance_4.png"
                    vscene scene_runtime.picture
                    "Она нежно улыбнулась и придвинулась к вам поближе, продолжая танец."
                    $ Becky.apply_social_roll(8, 5, 1, 14, 5, 1)
                    $ rooms.get("FridayDance").hands = "waist"
                elif Becky.rel >= 5 and Becky.corruption >= 6:
                    $ scene_runtime.picture = "images/becky/dance/you_dance_3.png"
                    vscene scene_runtime.picture
                    "Вдова удивленно приподняла бровь, но возражать не стала."
                    $ Becky.apply_social_roll(8, 5, 1, 14, 5, 1)
                    $ rooms.get("FridayDance").hands = "waist"
                else:
                    $ scene_runtime.picture = "images/becky/dance/butt_angy.png"
                    vscene scene_runtime.picture
                    "\"Стефан, негодник, что это ты такое делаешь?\" - спросила Бекки. \"Я согласилась просто танцевать с тобой, а ты нарушил наш уговор.\" Вы попробовали объяснить, что так обычно танцуют, но обнаружили, что разговариваете с пустотой: Бекки ушла."
                    $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                    $ Becky.apply_social_roll(2, 2, -1, 0, 0, 0)
                    $ rooms.get("FridayDance").hands = ""
                $ rooms.get("FridayDance").step += 1
                call BeckyInviteHome("becky")
                if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                    "Танец закончился и вы вернулись к колоннаде."

            "Положить руки на попу" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and rooms.get("FridayDance").hands == "waist":
                "Вы опустили руки с талии на попу Бекки."
                if Becky.rel >= 7 and Becky.corruption > 18:
                    $ scene_runtime.picture = "images/becky/dance/you_dance_5.png"
                    vscene scene_runtime.picture
                    "Бекки улыбнулась и придвинулась к вам поближе, продолжая танец."
                    $ Becky.apply_social_roll(9, 3, 1, 18, 3, 1)
                    $ rooms.get("FridayDance").hands = "ass"
                elif Becky.rel >= 6 and Becky.corruption >= 12:
                    $ scene_runtime.picture = "images/becky/dance/you_dance_5.png"
                    vscene scene_runtime.picture
                    "\"Стефан, негодник, что ты делаешь?!\" - прошептала Бекки, улыбаясь. \"Впрочем, продолжай,\" - добавила она."
                    $ Becky.apply_social_roll(9, 3, 1, 18, 3, 1)
                    $ rooms.get("FridayDance").hands = "ass"
                elif Becky.rel >= 5 and Becky.corruption >= 9:
                    $ scene_runtime.picture = "images/becky/dance/butt_angy.png"
                    vscene scene_runtime.picture
                    "\"Стефан, ай-ай-ай!\" - сказала вдовушка и передвинула ваши руки с попы на талию."
                    $ Becky.apply_social_roll(9, 4, 1, 14, 4, 1)
                    $ rooms.get("FridayDance").hands = "waist"
                else:
                    $ scene_runtime.picture = "images/becky/dance/butt_angy.png"
                    vscene scene_runtime.picture
                    "\"Стефан, негодник, что это ты такое делаешь?\" - спросила Бекки. \"Я тебе в матери гожусь, а ты что себе позволяешь?!\" Вы попробовали объяснить, что вы так случайно поступили, но обнаружили, что разговариваете с пустотой: Бекки ушла."
                    $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                    $ Becky.apply_social_roll(0, 1, -1, 0, 1, -1)
                    $ rooms.get("FridayDance").hands = ""
                $ rooms.get("FridayDance").step += 1
                call BeckyInviteHome("becky")
                if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                    "Танец закончился и вы вернулись к колоннаде."

            "Сжать попу вдовы" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and rooms.get("FridayDance").hands == "ass":
                "Ваши беспокойные ручки начали гладить и сжимать попку вдовушки."
                if Becky.rel >= 10 and Becky.corruption > 20:
                    $ scene_runtime.picture = "images/becky/dance/you dance_6.png"
                    vscene scene_runtime.picture
                    "Бекки это пришлось по вкусу, она улыбнулась и прижалась вплотную к вам, начав приятно тереться своими дыньками о вашу грудь."
                    $ Becky.apply_social_roll(11, 4, 1, 22, 3, 1)
                    $ rooms.get("FridayDance").hands = "ass2"
                    $ rooms.get("FridayDance").tits = 1
                elif Becky.rel >= 8 and Becky.corruption >= 16:
                    $ scene_runtime.picture = "images/becky/dance/you dance_6.png"
                    vscene scene_runtime.picture
                    "\"Стефанчик, ах наглец, ах шалун!\" - прошептала Бекки с напускным гневом, но не сделала ничего, чтобы остановить вас."
                    $ Becky.apply_social_roll(11, 4, 1, 22, 3, 1)
                    $ rooms.get("FridayDance").hands = "ass2"
                elif Becky.rel >= 7 and Becky.corruption >= 13:
                    $ scene_runtime.picture = "images/becky/dance/butt_angy.png"
                    vscene scene_runtime.picture
                    "\"Стефан, ай-ай-ай!\" - сказала вдовушка и передвинула ваши руки с попы на талию."
                    $ Becky.apply_social_roll(9, 4, 1, 16, 4, 1)
                    $ rooms.get("FridayDance").hands = "waist"
                else:
                    $ scene_runtime.picture = "images/becky/dance/butt_angy.png"
                    vscene scene_runtime.picture
                    "\"Стефан, негодник, что это ты такое делаешь?\" - спросила Бекки. \"Я тебе в матери гожусь, а ты что себе позволяешь?!\" Вы попробовали объяснить, что вы так случайно поступили, но обнаружили, что разговариваете с пустотой: Бекки ушла."
                    $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                    $ Becky.apply_social_roll(0, 1, -1, 0, 1, -1)
                    $ rooms.get("FridayDance").hands = ""
                $ rooms.get("FridayDance").step += 1
                call BeckyInviteHome("becky")
                if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                    "Танец закончился и вы вернулись к колоннаде."

            "Поцеловать Бекки" if rooms.get("FridayDance").step >= 2 and rooms.get("FridayDance").step < rooms.get("FridayDance").max_step and rooms.get("FridayDance").kiss == 0:
                "Продолжая танцевать, вы вдруг наклонились к вдове Блэнкеншип и впились в ее губы своими."
                if Becky.rel >= 10 and Becky.corruption > 21:
                    $ scene_runtime.picture = "images/becky/dance/french_kiss_1.png"
                    vscene scene_runtime.picture
                    "Опытная вдовушка с готовностью и умением ответила на ваш поцелуй, страстно переплетаясь с вами языками."
                    $ scene_runtime.picture = "images/becky/dance/french_kiss_2.png"
                    vscene scene_runtime.picture
                    $ Becky.apply_social_roll(11, 4, 1, 24, 3, 1)
                    $ rooms.get("FridayDance").kiss = 2
                elif Becky.rel >= 8 and Becky.corruption >= 16:
                    $ scene_runtime.picture = "images/becky/dance/you_dance_7.png"
                    vscene scene_runtime.picture
                    "Преодолев секундное замешательство, Бекки откликнулась на ваш поцелуй, хотя и, как вам показалось, была несколько шокирована вашей прямотой."
                    $ Becky.apply_social_roll(11, 4, 1, 24, 3, 1)
                    $ rooms.get("FridayDance").kiss = 1
                elif Becky.rel >= 7 and Becky.corruption >= 13:
                    $ scene_runtime.picture = "images/becky/dance/butt_angy.png"
                    vscene scene_runtime.picture
                    "\"Стефанчик, шалунишка, я же тебе в матери гожусь, а ты целоваться. И не стыдно?\" - прошептала Бекки и отстранилась от вас."
                    $ Becky.apply_social_roll(9, 6, 1, 16, 6, 1)
                    $ rooms.get("FridayDance").kiss = 0
                else:
                    $ scene_runtime.picture = "images/becky/dance/butt_angy.png"
                    vscene scene_runtime.picture
                    "\"Стефан, негодник, что это ты такое делаешь?\" - спросила Бекки. \"Я тебе в матери гожусь, а ты что себе позволяешь?!\" Вы не нашлись с подходящим объяснением, да, впрочем, это было и неважно: Бекки ушла."
                    $ rooms.get("FridayDance").step = rooms.get("FridayDance").max_step
                    $ Becky.apply_social_roll(0, 1, -1, 0, 1, -1)
                    $ rooms.get("FridayDance").kiss = 0
                $ rooms.get("FridayDance").step += 1
                call BeckyInviteHome("becky")
                if rooms.get("FridayDance").step == rooms.get("FridayDance").max_step:
                    "Танец закончился и вы вернулись к колоннаде."

            "Принять предложение вдовы" if rooms.get("FridayDance").becky_home_invited:
                $ main_ui_end_native_scene_state()
                call becky_accept_home_invitation
                return

            "Отойти" if rooms.get("FridayDance").step >= rooms.get("FridayDance").max_step or rooms.get("FridayDance").step == 1:
                "Вы решили отойти от Бекки и вернуться к колоннаде."
                $ rooms.get("FridayDance").step = 0
                return

    return


label becky_accept_home_invitation:
    $ rooms.get("FridayDance").becky_home_invited = True
    $ rooms.get("FridayDance").dance_count = 5
    call BeckyHomeFront("FromDances")
    return
