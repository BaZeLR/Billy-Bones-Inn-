label IntLizaTalk(girl_name_ilt="liza", girl_loc_ilt=""):
    python:
        GirlNameILT = girl_name_ilt or "liza"
        if str(girl_loc_ilt or ""):
            GirlLocILT = str(girl_loc_ilt or "")
        elif CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "TavernMain":
            GirlLocILT = "tavern"
        elif CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "PortStreets":
            GirlLocILT = "street"
        elif str(CurLoc or "") == "TavernMain":
            GirlLocILT = "tavern"
        else:
            GirlLocILT = "street"

        if GirlNameILT not in Talked:
            Talked[GirlNameILT] = 0
        if GirlNameILT not in Friends:
            Friends[GirlNameILT] = 0
        if GirlNameILT not in LickPussy:
            LickPussy[GirlNameILT] = 0
        if GirlNameILT not in GiveOrgasms:
            GiveOrgasms[GirlNameILT] = 0
        if GirlNameILT not in pregnancy:
            pregnancy[GirlNameILT] = 0
        if GirlNameILT not in kids:
            kids[GirlNameILT] = 0
        if GirlNameILT not in jobWhoreAvail:
            jobWhoreAvail[GirlNameILT] = 0
        if GirlNameILT not in sluttiness:
            sluttiness[GirlNameILT] = 0
        if GirlNameILT not in panties:
            panties[GirlNameILT] = ""
        if GirlNameILT not in CumInsideYou:
            CumInsideYou[GirlNameILT] = 0
        if GirlNameILT not in CumInsideOthers:
            CumInsideOthers[GirlNameILT] = 0

        if "seeclients" not in LizaVar:
            LizaVar["seeclients"] = 0
        if "askclients" not in LizaVar:
            LizaVar["askclients"] = 0
        if "asksex" not in LizaVar:
            LizaVar["asksex"] = 0
        if "askpregnancy" not in LizaVar:
            LizaVar["askpregnancy"] = 0
        if "SawChurchAfterCermon" not in LizaVar:
            LizaVar["SawChurchAfterCermon"] = 0
        if "TalkChurchAfterCermonGeorgett" not in LizaVar:
            LizaVar["TalkChurchAfterCermonGeorgett"] = 0
        if "GloryHoleMentioned" not in LizaVar:
            LizaVar["GloryHoleMentioned"] = 0
        if "GloryHoleAsked" not in LizaVar:
            LizaVar["GloryHoleAsked"] = 0
        if "SawChurchAfterCermon" not in GeorgettVar:
            GeorgettVar["SawChurchAfterCermon"] = 0

    label liza_talk_menu:
        "Что спросить у Лизетты?"

        menu:
            "Осмотреть":
                call ShowGirlCard(GirlNameILT)
                jump liza_talk_menu

            "Болтать":
                "Вы некоторое время болтаете с Лизеттой о разных вещах."
                python:
                    if Talked.get(GirlNameILT, 0) <= 2 and renpy.random.randint(1, 2) == 1:
                        girl_friends = Friends.get(GirlNameILT, 0)
                        lick_pussy_count = LickPussy.get(GirlNameILT, 0)
                        give_orgasms_count = GiveOrgasms.get(GirlNameILT, 0)

                        if (
                            girl_friends < 3
                            or (lick_pussy_count >= 7 and girl_friends < 4)
                            or (
                                give_orgasms_count >= 3
                                and lick_pussy_count >= 7
                                and girl_friends < 5
                            )
                        ):
                            renpy.say(None, "Вы чуть лучше узнали Лизетту.")
                            Friends[GirlNameILT] = girl_friends + 1
                        elif girl_friends < 5:
                            renpy.say(None, "Из уклончивых ответов девушки вы поняли, что она вам еще мало доверяет. Может, если бы вы узнали ее получше или доставили ей приятное, она бы с вами поделилась еще чем-то.")

                    if Talked.get(GirlNameILT, 0) > 2:
                        renpy.say(None, "Ничего нового из разговора вы не узнали.")

                    Talked[GirlNameILT] = Talked.get(GirlNameILT, 0) + 1
                jump liza_talk_menu

            "Спросить о клиентах" if (LizaVar.get("seeclients", 0) and Talked.get(GirlNameILT, 0) < 2 and Friends.get(GirlNameILT, 0) >= 5):
                "«За вечер меня хотят обычно три-четыре дяденьки. С некоторыми очень хорошо бывает, пока он закончит успеваешь сама спустить, а порой и несколько раз. А некоторые дяденьки так быстро заканчивают, что только начинаешь входить в охотку, а он уже все.» - говорит Лизетта, автоматически поглаживая промежность сквозь юбку."

                python:
                    if sluttiness.get(GirlNameILT, 0) < 50 and pregnancy.get(GirlNameILT, 0) < 120:
                        renpy.say(None, "«Только вот как не прошу я их чтобы внутрь не спускали, а они почти все либо делают вид что не слышат, либо отвечают, что платят деньги и спускают куда хотят. И в моей бедной киске теперь постоянно сперма хлюпает. А я не хочу залететь!» - добавляет Лизетта.")

                    if pregnancy.get(GirlNameILT, 0) >= 120:
                        renpy.say(None, "«Только вот как не просила я дяденек не спускать в меня, никто меня не слушал и теперь я залетела» - грустно добавляет Лизетта, проводя рукой по своему округлившимуся животику.")

                    if LizaVar.get("askclients", 0) == 0:
                        renpy.say(None, "Вас немного возбудил рассказ Лизетты.")
                        LizaVar["askclients"] = 1
                        Friends[GirlNameILT] = Friends.get(GirlNameILT, 0) + 1

                    Talked[GirlNameILT] = Talked.get(GirlNameILT, 0) + 1
                jump liza_talk_menu

            "Спросить о сексе" if (LizaVar.get("askclients", 0) and Talked.get(GirlNameILT, 0) < 2 and Friends.get(GirlNameILT, 0) >= 5):
                "«Ох, нравится мне трахаться! Маменька рассказывала как это хорошо, да и сама я за маменькой подсматривала, и за бабушкой, и за тетями моими и за дядями. Так что как мальчишки соседские начали мне под юбку лезть, то я сразу ножки и раздвинула. И не пожалела. А сейчас, как с мамочкой работать вместе начала, сладко мне каждый день бывает!» - говорит Лизетта."
                python:
                    if LizaVar.get("asksex", 0) == 0:
                        renpy.say(None, "Вас немного возбудил рассказ Лизетты.")
                        LizaVar["asksex"] = 1
                        Friends[GirlNameILT] = Friends.get(GirlNameILT, 0) + 1
                    Talked[GirlNameILT] = Talked.get(GirlNameILT, 0) + 1
                jump liza_talk_menu

            "Спросить о беременности" if (LizaVar.get("askclients", 0) and Talked.get(GirlNameILT, 0) < 2 and Friends.get(GirlNameILT, 0) >= 5):
                python:
                    if sluttiness.get(GirlNameILT, 0) < 50 and pregnancy.get(GirlNameILT, 0) < 120 and kids.get(GirlNameILT, 0) > 0:
                        renpy.say(None, "«Эх, как я не прошу дяденек чтобы в серединку мне не спускали, а они все равно! Все время во мне семя чье-то! Ребеночка мне уже заделали, скоро такими темпами еще будет!» - говорит Лизетта.")
                    elif sluttiness.get(GirlNameILT, 0) < 50 and pregnancy.get(GirlNameILT, 0) < 120:
                        renpy.say(None, "«Эх, как я не прошу дяденек чтобы в серединку мне не спускали, а они все равно! Все время во мне семя чье-то! Мамочка говорит что я ее скоро бабушкой сделаю, а я не хочу, я еще слишком молодая!» - говорит Лизетта.")
                    elif pregnancy.get(GirlNameILT, 0) >= 120:
                        renpy.say(None, "«Эх, баловалась я, баловалась вот и добаловалось - залетела. Столько меня имели, что теперь и предположить от кого - сложно.» - говорит Лизетта, проводя рукой по своему округлившимуся животику.")
                    else:
                        renpy.say(None, "«Маменька говорит, что любишь гулять - непременно пузо нагуляешь. А я гулять люблю, без чьего-нибудь колышка у себя в серединке и дня прожить трудно. Так что чему быть - того не миновать» - философски замечает Лизетта.")

                    if LizaVar.get("askpregnancy", 0) == 0:
                        renpy.say(None, "Вас немного возбудил рассказ Лизетты.")
                        LizaVar["askpregnancy"] = 1
                        Friends[GirlNameILT] = Friends.get(GirlNameILT, 0) + 1

                    Talked[GirlNameILT] = Talked.get(GirlNameILT, 0) + 1
                jump liza_talk_menu

            "Рассказать про ее мать и отца Герхарда" if (GeorgettVar.get("SawChurchAfterCermon", 0) and Talked.get(GirlNameILT, 0) < 2 and Friends.get(GirlNameILT, 0) >= 5 and LizaVar.get("TalkChurchAfterCermonGeorgett", 0) == 0):
                "Вы рассказываете Лизетте что вы видели как отец Герхард трахал ее мамочку после воскресной службы."
                "«Ух мама, и ты тоже с падре перепихнулась! Но я-то помоложе буду, я докажу отцу Герхарду что я лучшая любовница и больше достойна благословления Ильматера!» - отвечает Лизетта."
                python:
                    if LizaVar.get("TalkChurchAfterCermonGeorgett", 0) == 0:
                        renpy.say(None, "Вас немного возбудил рассказ Лизетты.")
                        LizaVar["TalkChurchAfterCermonGeorgett"] = 1
                        Friends[GirlNameILT] = Friends.get(GirlNameILT, 0) + 1
                    Talked[GirlNameILT] = Talked.get(GirlNameILT, 0) + 1
                jump liza_talk_menu

            "Спросить как работается у вас в трактире" if (jobWhoreAvail.get(GirlNameILT, 0) and Talked.get(GirlNameILT, 0) < 2):
                "Вы спрашиваете Лизетту как ей работается у вас в трактире."
                python:
                    if TavernGloryHole == 2:
                        renpy.say(None, "«Ой, - отвечает она, - здесь так здорово! Мне все нравится. А теперь еще и этот, холгло.., тьфу, в смысле глорихол есть! Все круто, куда круче чем на улице!»")
                    elif LizaVar.get("GloryHoleAsked", 0) == 1:
                        renpy.say(None, "«Ой, - отвечает она, - здесь так здорово! Мне все нравится!»")
                    else:
                        renpy.say(None, "«Ой, - отвечает она, - здесь так здорово! Мне все нравится. Правда мама говорила, что когда она подрабатывала в Пьяном Пирате, там была какая-то штука, не помню как называется. Холглор или еще как-то так. А у вас ее нет.»")
                    LizaVar["GloryHoleMentioned"] = 1
                    Talked[GirlNameILT] = Talked.get(GirlNameILT, 0) + 1
                jump liza_talk_menu

            "Спросить о таинственном \"Холглоре\" в \"Пьяном Пирате\"" if (jobWhoreAvail.get(GirlNameILT, 0) and LizaVar.get("GloryHoleAsked", 0) == 0 and LizaVar.get("GloryHoleMentioned", 0) == 1 and Talked.get(GirlNameILT, 0) < 2):
                "Вы просите Лизетту рассказать вам больше."
                "«Мама говорила что это такая ширмочка с дыркой, в которую дяденьки суют свои штуки, - рассказывает вам девчонка. - А мама с другой стороны их отсасывает. Ну или, если в охотку, писечкой насаживается. И никто никого не видит!»"
                $ LizaVar["GloryHoleAsked"] = 1
                $ Talked[GirlNameILT] = Talked.get(GirlNameILT, 0) + 1
                jump liza_talk_menu

            "Снять" if ((money >= 8 or (money >= 4 and GirlLocILT == "tavern")) and cametoday < cancumdaily):
                if GirlLocILT == "tavern":
                    $ money -= 4
                    call SexProstTavern(1, "liza")
                else:
                    $ money -= 8
                    call SexPort(1, "liza")
                return

            "Лапать":
                python:
                    if Friends.get(GirlNameILT, 0) >= 5:
                        renpy.say(None, f"Вы начали гладить маленькие сисечки {RealName2.get(GirlNameILT, GirlNameILT)} через тонкую ткань ее блузки.")

                        if panties.get(GirlNameILT, ""):
                            renpy.say(None, "Вы сунули руку под платьичко вашей подружки и начали натирать ее киску сквозь панталончики.")
                        else:
                            renpy.say(None, "Вы сунули руку под короткое платьичко вашей любовницы и стали наминать ее юную вульвочку.")

                        if not panties.get(GirlNameILT, ""):
                            if CumInsideYou.get(GirlNameILT, 0) > 0:
                                renpy.say(None, f"Вы почуствовали свою сперму в пещерке {RealName2.get(GirlNameILT, GirlNameILT)}.")
                            elif CumInsideOthers.get(GirlNameILT, 0) > 0:
                                renpy.say(None, f"Ваши пальцы заскользили по пещерке {RealName2.get(GirlNameILT, GirlNameILT)}, похоже кто-то уже кончил в нее.")
                    else:
                        renpy.say(None, f"«Эй, дяденка, не так быстро!» останавливает вас {RealName.get(GirlNameILT, GirlNameILT)}. «Мамочка говорит, что ты сначала заплатить должен, а потом уже лапать!»")
                call ShowCurrentSex(GirlNameILT)
                jump liza_talk_menu

            "Поинтересоваться, знает ли она кто ей ребенка заделал" if (Talked.get(GirlNameILT, 0) < 2 and Friends.get(GirlNameILT, 0) >= 8 and pregnancy.get(GirlNameILT, 0) >= 120):
                $ _dad_phrase = DaddyAskBuildPhrase(GirlNameILT)
                if _dad_phrase != "":
                    "[_dad_phrase]"
                $ Talked[GirlNameILT] = Talked.get(GirlNameILT, 0) + 1
                jump liza_talk_menu

            "Обсудить одежду" if GirlLocILT == "tavern":
                call IntLizaDressChange(GirlNameILT)
                jump liza_talk_menu

            "Уйти":
                if GirlLocILT == "tavern":
                    jump TavernMain
                jump PortStreets

    return
