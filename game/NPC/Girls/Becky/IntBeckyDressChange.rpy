# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntBeckyDressChange(GirlName="becky", agreed_to_redress=0):
    $ renpy.dynamic("_other_saw", "_dress_flags", "_can_offer_bra_off", "_can_offer_panties_off", "_can_shame", "_can_buy")
    $ _dress_flags = Becky.dress_change_flags(GirlName)
    $ _can_offer_bra_off = bool(_dress_flags.get("can_offer_bra_off", False))
    $ _can_offer_panties_off = bool(_dress_flags.get("can_offer_panties_off", False))
    $ _can_shame = bool(_dress_flags.get("can_shame", False))
    $ _can_buy = bool(_dress_flags.get("can_buy", False))

    if not (_can_offer_bra_off or _can_offer_panties_off or _can_shame or _can_buy):
        return

    menu:
        "Предложить вдове ходить без лифа" if _can_offer_bra_off:
            $ agreed_to_redress = 0
            "\"Бекки, дорогуша, зачем же ты носишь лиф?\" - подкатили вы к миссис Блэнкеншип с нескромным вопросом. \"Твои достоинства столь выдающиеся, что не стоит их скрывать. Наоборот, ими надо гордиться,\" продолжили вы гнуть свою линию."
            if Becky.clothing_slut("top") < 4:
                if Becky.corruption < 35:
                    "\"Да ты что такое удумал, Стефан?!\" ответила вам Ребекка с изумлением. \"Это же неприлично!\""
                else:
                    "\"Ой, спасибо тебе за комплимент,\" ответила вам польщенная вдова. \"Наверное ты прав, без него я буду выглядеть лучше.\""
                    $ agreed_to_redress = 1
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
                    $ agreed_to_redress = 1

            if agreed_to_redress == 1:
                $ Becky.set_default_bra("")
                $ Becky.apply_social_roll(0, 0, 0, 60, 2, 1)

            $ _other_saw = Becky.dress_change_other_saw_text(GirlName, agreed_to_redress)
            if str(_other_saw or "").strip() != "":
                "[_other_saw]"
            $ Becky.finish_talk()
            return

        "Предложить вдове снять панталоны" if _can_offer_panties_off:
            $ agreed_to_redress = 0
            "\"Бекки, милая, а зачем тебе панталончики?\" - задали вы волнующий вас вопрос в лоб, без излишних экивоков. \"Разве не лучше тебе будет без них, ты ведь тогда будешь выглядеть еще сексуальнее?\""
            if Becky.clothing_slut("bottom") < 4:
                if Becky.corruption < 35:
                    "\"Да ты что такое удумал, Стефан?!\" ответила вам Ребекка с изумлением. \"Как тебе такое только в голову могло прийти! Это же неприлично!\""
                else:
                    "\"Ой, ну я даже не знаю, наверное ты прав,\" помялась немного вдова. \"Все равно никто и не увидит.\""
                    $ agreed_to_redress = 1
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
                    $ agreed_to_redress = 1

            if agreed_to_redress == 1:
                $ Becky.set_default_panties("")
                $ Becky.apply_social_roll(0, 0, 0, 60, 2, 1)

            $ _other_saw = Becky.dress_change_other_saw_text(GirlName, agreed_to_redress)
            if str(_other_saw or "").strip() != "":
                "[_other_saw]"
            $ Becky.finish_talk()
            return

        "Постыдить Бекки за то, что ходит без лифчика" if _can_shame:
            $ agreed_to_redress = 0
            "\"Бекки, а ты чего без лифа ходишь?\" - строго спросили вы вдову. \"У тебя и так грудь велика, так ты ее еще наружу выпячиваешь.\""
            if Becky.has_bra() or (not Becky.has_bra() and Becky.corruption >= 45 and procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:166:4") == 1):
                "\"С чего это ты решил что нету, конечно я лиф одеваю,\" Ребекка пресекла ваши разглагольствования на полуслове."
            else:
                "\"Ну да, ты же меня сам просил без него ходить,\" обескураженно ответила вам она.\n\"Мне кажется, все-таки это как-то пошло и безвкусно, может лучше оденешь?\" отчитали вы бесстыдницу."
                if Becky.corruption < 45:
                    "\"Ты прав, я только ради тебя его сняла, но раз ты передумал, то...\" с облегчением в голосе сказала Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ agreed_to_redress = 1
                elif Becky.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:173:5") <= 3:
                    "\"А раньше тебе нравилось...\" обиженно протянула Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ agreed_to_redress = 1
                    $ Becky.apply_social_roll(10, 2, -1, 0, 0, 0)
                else:
                    "\"Что это на тебя нашло, когда это ты таким скромником-то заделался?!\" с удивлением спросила Бекки. \"Знаешь, я подольше тебя живу на свете, так что обойдусь я и без твоих советов, как мне одеваться.\""
                    $ Becky.apply_social_roll(10, 1, -1, 0, 0, 0)

            if agreed_to_redress == 1:
                $ Becky.set_default_bra("simplebra")
                $ Becky.apply_social_roll(0, 0, 0, 30, 1, -1)

            $ Becky.finish_talk()
            return

        "Постыдить Бекки за то, что ходит без панталон" if _can_shame:
            $ agreed_to_redress = 0
            "\"Бекки, а у тебя что, сейчас под юбкой ничего нет, что ли?\" - строго спросили вы вдову."
            if Becky.has_panties() or (not Becky.has_panties() and Becky.corruption >= 45 and procedural_randint(1, 2, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:191:6") == 1):
                "\"Конечно есть, за кого ты меня принимаешь,\" Ребекка пресекла вас на полуслове."
            else:
                "\"Ну да, ты же меня сам просил без ничего ходить,\" обескураженно ответила вам она.\n\"Мне кажется, все-таки это как-то пошло и безвкусно, может лучше оденешь?\" отчитали вы бесстыдницу."
                if Becky.corruption < 45:
                    "\"Ты прав, я только ради тебя без них ходила, но раз ты передумал, то...\" с облегчением в голосе сказала Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ agreed_to_redress = 1
                elif Becky.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Becky/IntBeckyDressChange.rpy:procedural_randint:198:7") <= 3:
                    "\"А раньше тебе нравилось...\" обиженно протянула Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ agreed_to_redress = 1
                    $ Becky.apply_social_roll(10, 2, -1, 0, 0, 0)
                else:
                    "\"Что это на тебя нашло, когда это ты таким скромником-то заделался?!\" с удивлением спросила Бекки. \"Знаешь, я подольше тебя живу на свете, так что обойдусь я и без твоих советов, как мне одеваться.\""
                    $ Becky.apply_social_roll(10, 1, -1, 0, 0, 0)

            if agreed_to_redress == 1:
                $ Becky.set_default_panties("simplepanties")
                $ Becky.apply_social_roll(0, 0, 0, 30, 1, -1)

            $ Becky.finish_talk()
            return

        "Предложить купить вдовушке обновку" if _can_buy:
            "\"Бекки, а давай к портнихе сходим и я тебе чего-нибудь подарю там?\" - обратились вы к вдовушке.\n\"Прямо аттракцион невиданной щедрости!\" засмеялась та. \"Ну давай! Завтра с утра?\"\n\"Да, давай завтра с утра пораньше. У Ирмы Фараго, я буду тебя там ждать, вместе и выберем!\" заверили вы Бекки."
            $ daily_events.add(GirlName, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")
            $ Becky.finish_talk()
            return

        "Назад":
            return

    return
