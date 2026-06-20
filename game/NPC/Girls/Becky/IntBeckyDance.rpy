# ================================================================================
# Becky Dance Interaction Menu (Friday dance event).
# Label owns the dance scene, choices, state changes, and the home invitation branch.
# ================================================================================

label story_becky_friday_dance_mc_0:
    vscene "images/market/LocFridayDance.jpg"
    $ Becky.var["danceinvitehome"] = 0
    $ FridayDancesCount += 1
    "Вы прошлись по площади, ища вдовушку Блэнкеншип, и нашли ее болтающей с другими торговками."
    call ShowImage("becky", "dance", "wait")
    $ DanceStep = 1
    call int_becky_dance
    return

label int_becky_dance():
    $ GirlNameIBD = "becky"
    $ DanceMaxIBD = 6
    $ scene_image = "images/becky/dance/waiting_0.png"
    $ _layout_last_picture = scene_image
    vscene scene_image

    while True:
        if DanceStep == 0:
            return

        menu:
            "Осмотреть" if DanceStep < 10:
                call GirlsDesc(GirlNameIBD)

            "Поболтать" if DanceStep == 1:
                "Вы подошли к веселой вдовушке и начали сыпать шутками и прибаутками, веселя ее. За разговором незаметно пролетело время."
                if Becky.rel >= 7:
                    "Вы подумали, что зря тратите время. Ничего нового вы не узнали, а Бекки и так знает, что вы шутник хоть куда."
                elif procedural_randint(1, 3, "becky_dance_talk_%s" % int(dayspassed or 0)) == 1:
                    $ Becky.add_relation(1, cap=100)
                    "Вы очень развеселили Бекки своими шутками!"
                $ DanceStep = DanceMaxIBD

            "Пригласить потанцевать" if DanceStep == 1:
                "Вы подошли к вдове Блэнкеншип и пригласили ее потанцевать."
                $ HandsDance = ""
                $ KissDance = 0
                $ TitsDance = 0
                if Becky.rel >= 7 and Becky.corruption > 18:
                    $ scene_image = "images/becky/dance/waiting_0.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "Она с радостью согласилась, вы взяли ее под руку и вскоре вы закружились в танце."
                elif Becky.rel >= 5 and Becky.corruption >= 8:
                    $ scene_image = "images/becky/dance/waiting_0.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "Она сказала: \"Стефан, Стефан, неужели ты действительно хочешь танцевать с такой практически старухой как я? Я же даже постарше вашей Сандры буду. Ну ладно, если ты так настаиваешь,\" - и она взяла вашу руку. Вскоре вы закружились в танце."
                else:
                    $ scene_image = "images/becky/dance/butt_angy.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефан, если ты хочешь танцевать со старой тетей, то пригласи свою бабушку Сандру, если хочешь!\" - ответила вам вдова. Расстроенный отказом, вы отправились восвояси."
                    $ DanceStep = DanceMaxIBD
                $ DanceStep += 1
                if DanceStep == DanceMaxIBD:
                    "Танец закончился и вы вернулись к колоннаде."

            "Продолжить танцевать" if DanceStep >= 2 and DanceStep < DanceMaxIBD:
                $ _dance_pic = procedural_randint(1, 5, "becky_dance_continue_%s_%s" % (int(dayspassed or 0), DanceStep))
                if _dance_pic == 1:
                    $ scene_image = "images/becky/dance/you_dance_1.png"
                elif _dance_pic == 2:
                    $ scene_image = "images/becky/dance/you_dance_2.png"
                elif _dance_pic == 3:
                    $ scene_image = "images/becky/dance/you_dance_3.png"
                elif _dance_pic == 4:
                    $ scene_image = "images/becky/dance/you_dance_4.png"
                else:
                    $ scene_image = "images/becky/dance/you_dance_5.png"
                $ _layout_last_picture = scene_image
                vscene scene_image
                "Вы продолжили кружиться в танце с Бекки."
                if HandsDance == "waist":
                    "Ваши руки нежно обнимают талию вдовушки."
                if HandsDance == "ass":
                    "Ваши руки покоятся на все еще упругой попке вдовы."
                if HandsDance == "ass2":
                    "Ваши руки нежно сжимают попу Бекки через платье."
                if KissDance == 1:
                    "Вы нежно целуете Бекки во время танца."
                if KissDance == 2:
                    "Вы страстно, переплетаясь языками, целуете Бекки, прилагая все усилия, чтобы не сбиться с ритма."
                if TitsDance > 0:
                    "Бекки трется своей огромной грудью о вас, потихоньку возбуждаясь."
                $ DanceStep += 1
                call BeckyInviteHome("becky")
                if DanceStep == DanceMaxIBD:
                    "Танец закончился и вы вернулись к колоннаде."

            "Положить руки на талию" if DanceStep >= 2 and DanceStep < DanceMaxIBD and HandsDance != "waist":
                "Вы положили руки на талию Бекки."
                if Becky.rel >= 7 and Becky.corruption > 10:
                    $ scene_image = "images/becky/dance/you_dance_1.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "Она нежно улыбнулась и придвинулась к вам поближе, продолжая танец."
                    $ Becky.apply_social_roll(8, 5, 1, 14, 5, 1)
                    $ HandsDance = "waist"
                elif Becky.rel >= 5 and Becky.corruption >= 6:
                    $ scene_image = "images/becky/dance/you_dance_2.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "Вдова удивленно приподняла бровь, но возражать не стала."
                    $ Becky.apply_social_roll(8, 5, 1, 14, 5, 1)
                    $ HandsDance = "waist"
                else:
                    $ scene_image = "images/becky/dance/butt_angy.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефан, негодник, что это ты такое делаешь?\" - спросила Бекки. \"Я согласилась просто танцевать с тобой, а ты нарушил наш уговор.\" Вы попробовали объяснить, что так обычно танцуют, но обнаружили, что разговариваете с пустотой: Бекки ушла."
                    $ DanceStep = DanceMaxIBD
                    $ Becky.apply_social_roll(2, 2, -1, 0, 0, 0)
                    $ HandsDance = ""
                $ DanceStep += 1
                call BeckyInviteHome("becky")
                if DanceStep == DanceMaxIBD:
                    "Танец закончился и вы вернулись к колоннаде."

            "Положить руки на попу" if DanceStep >= 2 and DanceStep < DanceMaxIBD and HandsDance == "waist":
                "Вы опустили руки с талии на попу Бекки."
                if Becky.rel >= 7 and Becky.corruption > 18:
                    $ scene_image = "images/becky/dance/you_dance_5.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "Бекки улыбнулась и придвинулась к вам поближе, продолжая танец."
                    $ Becky.apply_social_roll(9, 3, 1, 18, 3, 1)
                    $ HandsDance = "ass"
                elif Becky.rel >= 6 and Becky.corruption >= 12:
                    $ scene_image = "images/becky/dance/you_dance_4.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефан, негодник, что ты делаешь?!\" - прошептала Бекки, улыбаясь. \"Впрочем, продолжай,\" - добавила она."
                    $ Becky.apply_social_roll(9, 3, 1, 18, 3, 1)
                    $ HandsDance = "ass"
                elif Becky.rel >= 5 and Becky.corruption >= 9:
                    $ scene_image = "images/becky/dance/butt_angy.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефан, ай-ай-ай!\" - сказала вдовушка и передвинула ваши руки с попы на талию."
                    $ Becky.apply_social_roll(9, 4, 1, 14, 4, 1)
                    $ HandsDance = "waist"
                else:
                    $ scene_image = "images/becky/dance/butt_angy.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефан, негодник, что это ты такое делаешь?\" - спросила Бекки. \"Я тебе в матери гожусь, а ты что себе позволяешь?!\" Вы попробовали объяснить, что вы так случайно поступили, но обнаружили, что разговариваете с пустотой: Бекки ушла."
                    $ DanceStep = DanceMaxIBD
                    $ Becky.apply_social_roll(0, 1, -1, 0, 1, -1)
                    $ HandsDance = ""
                $ DanceStep += 1
                call BeckyInviteHome("becky")
                if DanceStep == DanceMaxIBD:
                    "Танец закончился и вы вернулись к колоннаде."

            "Сжать попу вдовы" if DanceStep >= 2 and DanceStep < DanceMaxIBD and HandsDance == "ass":
                "Ваши беспокойные ручки начали гладить и сжимать попку вдовушки."
                if Becky.rel >= 10 and Becky.corruption > 20:
                    $ scene_image = "images/becky/dance/you_dance_7.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "Бекки это пришлось по вкусу, она улыбнулась и прижалась вплотную к вам, начав приятно тереться своими дыньками о вашу грудь."
                    $ Becky.apply_social_roll(11, 4, 1, 22, 3, 1)
                    $ HandsDance = "ass2"
                    $ TitsDance = 1
                elif Becky.rel >= 8 and Becky.corruption >= 16:
                    $ scene_image = "images/becky/dance/you_dance_4.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефанчик, ах наглец, ах шалун!\" - прошептала Бекки с напускным гневом, но не сделала ничего, чтобы остановить вас."
                    $ Becky.apply_social_roll(11, 4, 1, 22, 3, 1)
                    $ HandsDance = "ass2"
                elif Becky.rel >= 7 and Becky.corruption >= 13:
                    $ scene_image = "images/becky/dance/butt_angy.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефан, ай-ай-ай!\" - сказала вдовушка и передвинула ваши руки с попы на талию."
                    $ Becky.apply_social_roll(9, 4, 1, 16, 4, 1)
                    $ HandsDance = "waist"
                else:
                    $ scene_image = "images/becky/dance/butt_angy.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефан, негодник, что это ты такое делаешь?\" - спросила Бекки. \"Я тебе в матери гожусь, а ты что себе позволяешь?!\" Вы попробовали объяснить, что вы так случайно поступили, но обнаружили, что разговариваете с пустотой: Бекки ушла."
                    $ DanceStep = DanceMaxIBD
                    $ Becky.apply_social_roll(0, 1, -1, 0, 1, -1)
                    $ HandsDance = ""
                $ DanceStep += 1
                call BeckyInviteHome("becky")
                if DanceStep == DanceMaxIBD:
                    "Танец закончился и вы вернулись к колоннаде."

            "Поцеловать Бекки" if DanceStep >= 2 and DanceStep < DanceMaxIBD and KissDance == 0:
                "Продолжая танцевать, вы вдруг наклонились к вдове Блэнкеншип и впились в ее губы своими."
                if Becky.rel >= 10 and Becky.corruption > 21:
                    $ scene_image = "images/becky/dance/french_kiss_1.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "Опытная вдовушка с готовностью и умением ответила на ваш поцелуй, страстно переплетаясь с вами языками."
                    $ scene_image = "images/becky/dance/french_kiss_2.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    $ Becky.apply_social_roll(11, 4, 1, 24, 3, 1)
                    $ KissDance = 2
                elif Becky.rel >= 8 and Becky.corruption >= 16:
                    $ scene_image = "images/becky/dance/french_kiss_1.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "Преодолев секундное замешательство, Бекки откликнулась на ваш поцелуй, хотя и, как вам показалось, была несколько шокирована вашей прямотой."
                    $ Becky.apply_social_roll(11, 4, 1, 24, 3, 1)
                    $ KissDance = 1
                elif Becky.rel >= 7 and Becky.corruption >= 13:
                    $ scene_image = "images/becky/dance/butt_angy.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефанчик, шалунишка, я же тебе в матери гожусь, а ты целоваться. И не стыдно?\" - прошептала Бекки и отстранилась от вас."
                    $ Becky.apply_social_roll(9, 6, 1, 16, 6, 1)
                    $ KissDance = 0
                else:
                    $ scene_image = "images/becky/dance/butt_angy.png"
                    $ _layout_last_picture = scene_image
                    vscene scene_image
                    "\"Стефан, негодник, что это ты такое делаешь?\" - спросила Бекки. \"Я тебе в матери гожусь, а ты что себе позволяешь?!\" Вы не нашлись с подходящим объяснением, да, впрочем, это было и неважно: Бекки ушла."
                    $ DanceStep = DanceMaxIBD
                    $ Becky.apply_social_roll(0, 1, -1, 0, 1, -1)
                    $ KissDance = 0
                $ DanceStep += 1
                call BeckyInviteHome("becky")
                if DanceStep == DanceMaxIBD:
                    "Танец закончился и вы вернулись к колоннаде."

            "Принять предложение вдовы" if Becky.var.get("danceinvitehome", 0):
                call becky_accept_home_invitation
                return

            "Отойти" if DanceStep >= DanceMaxIBD or DanceStep == 1:
                $ CounterToClean = MaxCounterToClean
                "Вы решили отойти от Бекки и вернуться к колоннаде."
                $ DanceStep = 0
                return

    return


label becky_accept_home_invitation:
    $ Becky.var["danceinvitehome"] = 1
    $ FridayDancesCount = 5
    call BeckyHomeFront("FromDances")
    return
