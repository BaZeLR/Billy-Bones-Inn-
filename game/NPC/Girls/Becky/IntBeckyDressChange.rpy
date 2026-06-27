# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def dress_change_sync_layers(girl_name=""):
        girl = str(girl_name or "").strip()
        if girl == "":
            return
        topdress.setdefault(girl, "")
        bottomdress.setdefault(girl, "")
        bra.setdefault(girl, "")
        panties.setdefault(girl, "")
        legs.setdefault(girl, "")
        shoes.setdefault(girl, "")
        topdressdef.setdefault(girl, topdress.get(girl, ""))
        bottomdressdef.setdefault(girl, bottomdress.get(girl, ""))
        bradef.setdefault(girl, bra.get(girl, ""))
        pantiesdef.setdefault(girl, panties.get(girl, ""))
        legsdef.setdefault(girl, legs.get(girl, ""))
        shoesdef.setdefault(girl, shoes.get(girl, ""))
        topdress[girl] = topdressdef.get(girl, "")
        bottomdress[girl] = bottomdressdef.get(girl, "")
        bra[girl] = bradef.get(girl, "")
        panties[girl] = pantiesdef.get(girl, "")
        legs[girl] = legsdef.get(girl, "")
        shoes[girl] = shoesdef.get(girl, "")
        topraised[girl] = 0
        bottomraised[girl] = 0

    def becky_dress_change_flags(girl_name="becky"):
        girl_key = str(girl_name or "becky")
        can_offer_bra_off = (
            Becky.stats.get("orgasms_given", 0) >= 2
            and Becky.rel > 8
            and Becky.has_bra()
            and Becky.talk_count() < 2
        )
        can_offer_panties_off = (
            Becky.stats.get("orgasms_given", 0) >= 2
            and Becky.rel > 8
            and Becky.has_panties()
            and Becky.talk_count() < 2
        )
        can_shame = (
            Becky.stats.get("orgasms_given", 0) >= 2
            and Becky.rel > 8
            and Becky.talk_count() < 2
        )
        can_buy = (
            Becky.rel > 8
            and CheckDailyEventExists("", "BuyDressTom", "") == 0
            and CheckDailyEventExists(girl_key, "BuyDress", "") == 0
            and Becky.talk_count() < 2
            and week != 6
        )
        return {
            "can_offer_bra_off": bool(can_offer_bra_off),
            "can_offer_panties_off": bool(can_offer_panties_off),
            "can_shame": bool(can_shame),
            "can_buy": bool(can_buy),
        }

    def becky_dress_change_has_options(girl_name="becky"):
        flags = becky_dress_change_flags(girl_name)
        return any(bool(value) for value in flags.values())

    def becky_dress_change_other_saw_text(girl_name="becky", agreed_to_redress=0):
        girl = str(girl_name or "becky")
        if int(agreed_to_redress or 0) != 1 or Becky.corruption < 45:
            return ""
        randvar = procedural_randint(1, 6, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:71:1")
        if randvar == 1:
            text = "Какой-то мужик, зашедший за чем-то в лавку, наблюдал за этой сценкой с отвалившей челюстью. Бекки подмигнула ему и стала перекладывать овощи на прилавке как ни в чем не бывало."
        elif randvar == 2:
            text = "Глаза у какой-то девицы, заглянувшей в лавку за покупками, расширились от такого зрелища, но под конец она с одобрением кивнула вдове."
        elif randvar == 3:
            text = 'Какая-то мать семейства, заглянувшая в лавку миссис Блэнкеншип за зеленью, назидательно сказала своим двум дочкам, указывая на Бекки: "Вот видите как нужно парней привлекать, а вы все \'это платье слишком смелое\' и прочую чушь, так у меня в девках и проходите, коли за ум не возьметесь."'
        else:
            text = ""
        if randvar <= 3:
            Becky.apply_social_roll(0, 0, 0, 60, 2, 1)
        return text


label IntBeckyDressChange(GirlName="becky"):
    $ _dress_flags = becky_dress_change_flags(GirlName)
    $ _can_offer_bra_off = bool(_dress_flags.get("can_offer_bra_off", False))
    $ _can_offer_panties_off = bool(_dress_flags.get("can_offer_panties_off", False))
    $ _can_shame = bool(_dress_flags.get("can_shame", False))
    $ _can_buy = bool(_dress_flags.get("can_buy", False))

    if not (_can_offer_bra_off or _can_offer_panties_off or _can_shame or _can_buy):
        return

    menu:
        "Предложить вдове ходить без лифа" if _can_offer_bra_off:
            $ AgreedToRedress = 0
            "\"Бекки, дорогуша, зачем же ты носишь лиф?\" - подкатили вы к миссис Блэнкеншип с нескромным вопросом. \"Твои достоинства столь выдающиеся, что не стоит их скрывать. Наоборот, ими надо гордиться,\" продолжили вы гнуть свою линию."
            if DressPartSlut.get(topdress.get(GirlName, ""), 0) < 4:
                if Becky.corruption < 35:
                    "\"Да ты что такое удумал, Стефан?!\" ответила вам Ребекка с изумлением. \"Это же неприлично!\""
                else:
                    "\"Ой, спасибо тебе за комплимент,\" ответила вам польщенная вдова. \"Наверное ты прав, без него я буду выглядеть лучше.\""
                    $ AgreedToRedress = 1
                    if Becky.corruption < 45:
                        if procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:106:2") == 1:
                            "Убедившись что вы одни, Бекки растегнула платье, сняла лиф и одела платье уже на голые груди."
                        else:
                            "Бекки подождала, пока из лавки выйдут посетители, затем растегнула платье, сняла лиф и одела платье уже на голые груди."
                    else:
                        "Не позаботившись проверить есть ли кто еще в лавке, Бекки растегнула платье, сняла лиф и одела платье уже на голые груди."
                    "\"Ну как я тебе,\" кокетливо поинтересовалась она.\n\"Бесподобно!\""
            else:
                if Becky.corruption < 50:
                    "\"Ну нет, я так не могу,\" заныла Ребекка в ответ на ваше предложение. \"У меня и так декольте смотри какое?\"\nВы посмотрели в декольте вдовы и увиденное вам понравилось. Однако выразить свое восхищение вы не успели, так как Ребекка продолжила: \"Без лифа у меня сосочки будут выпирать, а если я повернусь резко, то грудь вообще может вылететь. Нет, нет и нет.\""
                else:
                    "\"Какой ты затейник, Стефан,\" заулыбалась Ребекка. \"Ты же знаешь, у меня декольте глубокое, если резко повернусь, то грудь из платья может вылететь, ты этого что ли хочешь? Ведь все будут на меня тогда смотреть и...\"\n\"Восхищаться,\" быстро добавили вы. Продолжая улыбаться, Бекки растегнула платье, медленно сняла лиф, давая возможность вам еще раз полюбоваться ее здоровенными шарами, и одела платье обратно на голое тело."
                    $ AgreedToRedress = 1

            if AgreedToRedress == 1:
                $ Becky.set_default_bra("")
                $ Becky.apply_social_roll(0, 0, 0, 60, 2, 1)

            $ _other_saw = becky_dress_change_other_saw_text(GirlName, AgreedToRedress)
            if str(_other_saw or "").strip() != "":
                "[_other_saw]"
            $ Becky.finish_talk()
            return

        "Предложить вдове снять панталоны" if _can_offer_panties_off:
            $ AgreedToRedress = 0
            "\"Бекки, милая, а зачем тебе панталончики?\" - задали вы волнующий вас вопрос в лоб, без излишних экивоков. \"Разве не лучше тебе будет без них, ты ведь тогда будешь выглядеть еще сексуальнее?\""
            if DressPartSlut.get(bottomdress.get(GirlName, ""), 0) < 4:
                if Becky.corruption < 35:
                    "\"Да ты что такое удумал, Стефан?!\" ответила вам Ребекка с изумлением. \"Как тебе такое только в голову могло прийти! Это же неприлично!\""
                else:
                    "\"Ой, ну я даже не знаю, наверное ты прав,\" помялась немного вдова. \"Все равно никто и не увидит.\""
                    $ AgreedToRedress = 1
                    if Becky.corruption < 45:
                        if procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:140:3") == 1:
                            "Оглянувшись по сторонам и убедившись что вы одни, Бекки залезла себе под подол и сняла столь досаждавшую вам деталь одежды."
                        else:
                            "Бекки подождала, пока из лавки выйдут посетители, затем залезла себе под подол и сняла столь досаждавшую вам деталь одежды."
                    else:
                        "Не позаботившись проверить есть ли кто еще в лавке, Бекки залезла себе под подол и сняла столь досаждавшую вам деталь одежды."
            else:
                if Becky.corruption < 50:
                    "\"Да ты что, смеешься?!\" возмутилась Ребекка в ответ на ваше предложение. \"Тебе мало того, что у меня и так платье короткое, ты хочешь теперь чтобы я всем встречным и поперечным киску свою демонстрировала? Знаешь что, поищи кого-нибудь другого для этого.\""
                else:
                    "\"Ну ты и пошляк, Стефан,\" заулыбалась Ребекка. \"Ты хочешь чтобы я гуляла в коротком платье на голое тело. А если ветер или там наклонюсь я или присяду, то каждый бы смог в этом убедиться.\"\n\"И восхититься!\" куртуазно вставили вы.\n\"Ты знаешь, а меня это заводит,\" отнюдь не целомудренно сказала вдова.\nПриподняв платье, Бекки медленно стянула с себя панталоны, покрутила их и с многозначительной улыбкой куда-то убрала."
                    $ AgreedToRedress = 1

            if AgreedToRedress == 1:
                $ Becky.set_default_panties("")
                $ Becky.apply_social_roll(0, 0, 0, 60, 2, 1)

            $ _other_saw = becky_dress_change_other_saw_text(GirlName, AgreedToRedress)
            if str(_other_saw or "").strip() != "":
                "[_other_saw]"
            $ Becky.finish_talk()
            return

        "Постыдить Бекки за то, что ходит без лифчика" if _can_shame:
            $ AgreedToRedress = 0
            "\"Бекки, а ты чего без лифа ходишь?\" - строго спросили вы вдову. \"У тебя и так грудь велика, так ты ее еще наружу выпячиваешь.\""
            if Becky.has_bra() or (not Becky.has_bra() and Becky.corruption >= 45 and procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:166:4") == 1):
                "\"С чего это ты решил что нету, конечно я лиф одеваю,\" Ребекка пресекла ваши разглагольствования на полуслове."
            else:
                "\"Ну да, ты же меня сам просил без него ходить,\" обескураженно ответила вам она.\n\"Мне кажется, все-таки это как-то пошло и безвкусно, может лучше оденешь?\" отчитали вы бесстыдницу."
                if Becky.corruption < 45:
                    "\"Ты прав, я только ради тебя его сняла, но раз ты передумал, то...\" с облегчением в голосе сказала Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ AgreedToRedress = 1
                elif Becky.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:173:5") <= 3:
                    "\"А раньше тебе нравилось...\" обиженно протянула Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ AgreedToRedress = 1
                    $ Becky.apply_social_roll(10, 2, -1, 0, 0, 0)
                else:
                    "\"Что это на тебя нашло, когда это ты таким скромником-то заделался?!\" с удивлением спросила Бекки. \"Знаешь, я подольше тебя живу на свете, так что обойдусь я и без твоих советов, как мне одеваться.\""
                    $ Becky.apply_social_roll(10, 1, -1, 0, 0, 0)

            if AgreedToRedress == 1:
                $ Becky.set_default_bra("simplebra")
                $ Becky.apply_social_roll(0, 0, 0, 30, 1, -1)

            $ Becky.finish_talk()
            return

        "Постыдить Бекки за то, что ходит без панталон" if _can_shame:
            $ AgreedToRedress = 0
            "\"Бекки, а у тебя что, сейчас под юбкой ничего нет, что ли?\" - строго спросили вы вдову."
            if Becky.has_panties() or (not Becky.has_panties() and Becky.corruption >= 45 and procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:191:6") == 1):
                "\"Конечно есть, за кого ты меня принимаешь,\" Ребекка пресекла вас на полуслове."
            else:
                "\"Ну да, ты же меня сам просил без ничего ходить,\" обескураженно ответила вам она.\n\"Мне кажется, все-таки это как-то пошло и безвкусно, может лучше оденешь?\" отчитали вы бесстыдницу."
                if Becky.corruption < 45:
                    "\"Ты прав, я только ради тебя без них ходила, но раз ты передумал, то...\" с облегчением в голосе сказала Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ AgreedToRedress = 1
                elif Becky.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:198:7") <= 3:
                    "\"А раньше тебе нравилось...\" обиженно протянула Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ AgreedToRedress = 1
                    $ Becky.apply_social_roll(10, 2, -1, 0, 0, 0)
                else:
                    "\"Что это на тебя нашло, когда это ты таким скромником-то заделался?!\" с удивлением спросила Бекки. \"Знаешь, я подольше тебя живу на свете, так что обойдусь я и без твоих советов, как мне одеваться.\""
                    $ Becky.apply_social_roll(10, 1, -1, 0, 0, 0)

            if AgreedToRedress == 1:
                $ Becky.set_default_panties("simplepanties")
                $ Becky.apply_social_roll(0, 0, 0, 30, 1, -1)

            $ Becky.finish_talk()
            return

        "Предложить купить вдовушке обновку" if _can_buy:
            "\"Бекки, а давай к портнихе сходим и я тебе чего-нибудь подарю там?\" - обратились вы к вдовушке.\n\"Прямо аттракцион невиданной щедрости!\" засмеялась та. \"Ну давай! Завтра с утра?\"\n\"Да, давай завтра с утра пораньше. У Ирмы Фараго, я буду тебя там ждать, вместе и выберем!\" заверили вы Бекки."
            $ DailyEventsList_Add(GirlName, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
            $ Becky.finish_talk()
            return

        "Назад":
            return

    return
