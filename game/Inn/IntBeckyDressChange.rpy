init python:
    def becky_dress_change_flags(girl_name="becky"):
        girl_key = str(girl_name or "becky")
        can_offer_bra_off = (
            GiveOrgasms.get(girl_key, 0) >= 2
            and Friends.get(girl_key, 0) > 8
            and bra.get(girl_key, "") != ""
            and Talked.get(girl_key, 0) < 2
        )
        can_offer_panties_off = (
            GiveOrgasms.get(girl_key, 0) >= 2
            and Friends.get(girl_key, 0) > 8
            and panties.get(girl_key, "") != ""
            and Talked.get(girl_key, 0) < 2
        )
        can_shame = (
            GiveOrgasms.get(girl_key, 0) >= 2
            and Friends.get(girl_key, 0) > 8
            and Talked.get(girl_key, 0) < 2
        )
        can_buy = (
            Friends.get(girl_key, 0) > 8
            and CheckDailyEventExists("", "BuyDressTom", "") == 0
            and CheckDailyEventExists(girl_key, "BuyDress", "") == 0
            and Talked.get(girl_key, 0) < 2
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


label IntBeckyDressChange(GirlName="becky"):
    python:
        def _call_slut_friends_increase(*args):
            if renpy.has_label("SlutFriendsIncrease"):
                renpy.call("SlutFriendsIncrease", *args)
            elif renpy.has_label("slut_friends_increase"):
                renpy.call("slut_friends_increase", *args)

        def _call_dress_up(girl_name):
            if renpy.has_label("DressUp"):
                renpy.call("DressUp", girl_name)
            elif renpy.has_label("dress_up"):
                renpy.call("dress_up", girl_name)

        def _say(text):
            renpy.say(None, text)

        def OtherSawBeckyCode(AgreedToRedress):
            if AgreedToRedress == 1 and sluttiness.get(GirlName, 0) >= 45:
                RandVar = renpy.random.randint(1, 6)
                if RandVar == 1:
                    _say("Какой-то мужик, зашедший за чем-то в лавку, наблюдал за этой сценкой с отвалившей челюстью. Бекки подмигнула ему и стала перекладывать овощи на прилавке как ни в чем не бывало.")
                elif RandVar == 2:
                    _say("Глаза у какой-то девицы, заглянувшей в лавку за покупками, расширились от такого зрелища, но под конец она с одобрением кивнула вдове.")
                elif RandVar == 3:
                    _say("Какая-то мать семейства, заглянувшая в лавку миссис Блэнкеншип за зеленью, назидательно сказала своим двум дочкам, указывая на Бекки: \"Вот видите как нужно парней привлекать, а вы все 'это платье слишком смелое мама' и прочую чушь, так у меня в девках и проходите, коли за ум не возьметесь.\"")

                if RandVar <= 3:
                    _call_slut_friends_increase("becky", 0, 0, 0, 60, 2, 1)

        _dress_flags = becky_dress_change_flags(GirlName)
        _can_offer_bra_off = bool(_dress_flags.get("can_offer_bra_off", False))
        _can_offer_panties_off = bool(_dress_flags.get("can_offer_panties_off", False))
        _can_shame = bool(_dress_flags.get("can_shame", False))
        _can_buy = bool(_dress_flags.get("can_buy", False))

    if not (_can_offer_bra_off or _can_offer_panties_off or _can_shame or _can_buy):
        return

    menu:
        "Предложить вдове ходить без лифа" if _can_offer_bra_off:
            $ AgreedToRedress = 0
            "\"Бекки, дорогуша, зачем же ты носишь лиф?\" - подкатили вы к миссис Блэнкеншип с нескромным вопросом. \"Твои достоинства столь выдающиеся, что не стоит их скрывать. Наоборот, ими надо гордиться,\" продолжили вы гнуть свою линию."
            if DressPartSlut.get(topdress.get(GirlName, ""), 0) < 4:
                if sluttiness.get(GirlName, 0) < 35:
                    "\"Да ты что такое удумал, Стефан?!\" ответила вам Ребекка с изумлением. \"Это же неприлично!\""
                else:
                    "\"Ой, спасибо тебе за комплимент,\" ответила вам польщенная вдова. \"Наверное ты прав, без него я буду выглядеть лучше.\""
                    $ AgreedToRedress = 1
                    if sluttiness.get(GirlName, 0) < 45:
                        if renpy.random.randint(1, 2) == 1:
                            "Убедившись что вы одни, Бекки растегнула платье, сняла лиф и одела платье уже на голые груди."
                        else:
                            "Бекки подождала, пока из лавки выйдут посетители, затем растегнула платье, сняла лиф и одела платье уже на голые груди."
                    else:
                        "Не позаботившись проверить есть ли кто еще в лавке, Бекки растегнула платье, сняла лиф и одела платье уже на голые груди."
                    "\"Ну как я тебе,\" кокетливо поинтересовалась она.\n\"Бесподобно!\""
            else:
                if sluttiness.get(GirlName, 0) < 50:
                    "\"Ну нет, я так не могу,\" заныла Ребекка в ответ на ваше предложение. \"У меня и так декольте смотри какое?\"\nВы посмотрели в декольте вдовы и увиденное вам понравилось. Однако выразить свое восхищение вы не успели, так как Ребекка продолжила: \"Без лифа у меня сосочки будут выпирать, а если я повернусь резко, то грудь вообще может вылететь. Нет, нет и нет.\""
                else:
                    "\"Какой ты затейник, Стефан,\" заулыбалась Ребекка. \"Ты же знаешь, у меня декольте глубокое, если резко повернусь, то грудь из платья может вылететь, ты этого что ли хочешь? Ведь все будут на меня тогда смотреть и...\"\n\"Восхищаться,\" быстро добавили вы. Продолжая улыбаться, Бекки растегнула платье, медленно сняла лиф, давая возможность вам еще раз полюбоваться ее здоровенными шарами, и одела платье обратно на голое тело."
                    $ AgreedToRedress = 1

            if AgreedToRedress == 1:
                $ bradef[GirlName] = ""
                python:
                    _call_slut_friends_increase("becky", 0, 0, 0, 60, 2, 1)
                    _call_dress_up(GirlName)

            python:
                OtherSawBeckyCode(AgreedToRedress)
            $ Talked[GirlName] = Talked.get(GirlName, 0) + 1
            return

        "Предложить вдове снять панталоны" if _can_offer_panties_off:
            $ AgreedToRedress = 0
            "\"Бекки, милая, а зачем тебе панталончики?\" - задали вы волнующий вас вопрос в лоб, без излишних экивоков. \"Разве не лучше тебе будет без них, ты ведь тогда будешь выглядеть еще сексуальнее?\""
            if DressPartSlut.get(bottomdress.get(GirlName, ""), 0) < 4:
                if sluttiness.get(GirlName, 0) < 35:
                    "\"Да ты что такое удумал, Стефан?!\" ответила вам Ребекка с изумлением. \"Как тебе такое только в голову могло прийти! Это же неприлично!\""
                else:
                    "\"Ой, ну я даже не знаю, наверное ты прав,\" помялась немного вдова. \"Все равно никто и не увидит.\""
                    $ AgreedToRedress = 1
                    if sluttiness.get(GirlName, 0) < 45:
                        if renpy.random.randint(1, 2) == 1:
                            "Оглянувшись по сторонам и убедившись что вы одни, Бекки залезла себе под подол и сняла столь досаждавшую вам деталь одежды."
                        else:
                            "Бекки подождала, пока из лавки выйдут посетители, затем залезла себе под подол и сняла столь досаждавшую вам деталь одежды."
                    else:
                        "Не позаботившись проверить есть ли кто еще в лавке, Бекки залезла себе под подол и сняла столь досаждавшую вам деталь одежды."
            else:
                if sluttiness.get(GirlName, 0) < 50:
                    "\"Да ты что, смеешься?!\" возмутилась Ребекка в ответ на ваше предложение. \"Тебе мало того, что у меня и так платье короткое, ты хочешь теперь чтобы я всем встречным и поперечным киску свою демонстрировала? Знаешь что, поищи кого-нибудь другого для этого.\""
                else:
                    "\"Ну ты и пошляк, Стефан,\" заулыбалась Ребекка. \"Ты хочешь чтобы я гуляла в коротком платье на голое тело. А если ветер или там наклонюсь я или присяду, то каждый бы смог в этом убедиться.\"\n\"И восхититься!\" куртуазно вставили вы.\n\"Ты знаешь, а меня это заводит,\" отнюдь не целомудренно сказала вдова.\nПриподняв платье, Бекки медленно стянула с себя панталоны, покрутила их и с многозначительной улыбкой куда-то убрала."
                    $ AgreedToRedress = 1

            if AgreedToRedress == 1:
                $ pantiesdef[GirlName] = ""
                python:
                    _call_slut_friends_increase("becky", 0, 0, 0, 60, 2, 1)
                    _call_dress_up(GirlName)

            python:
                OtherSawBeckyCode(AgreedToRedress)
            $ Talked[GirlName] = Talked.get(GirlName, 0) + 1
            return

        "Постыдить Бекки за то, что ходит без лифчика" if _can_shame:
            $ AgreedToRedress = 0
            "\"Бекки, а ты чего без лифа ходишь?\" - строго спросили вы вдову. \"У тебя и так грудь велика, так ты ее еще наружу выпячиваешь.\""
            if bra.get(GirlName, "") != "" or (bra.get(GirlName, "") == "" and sluttiness.get(GirlName, 0) >= 45 and renpy.random.randint(1, 2) == 1):
                "\"С чего это ты решил что нету, конечно я лиф одеваю,\" Ребекка пресекла ваши разглагольствования на полуслове."
            else:
                "\"Ну да, ты же меня сам просил без него ходить,\" обескураженно ответила вам она.\n\"Мне кажется, все-таки это как-то пошло и безвкусно, может лучше оденешь?\" отчитали вы бесстыдницу."
                if sluttiness.get(GirlName, 0) < 45:
                    "\"Ты прав, я только ради тебя его сняла, но раз ты передумал, то...\" с облегчением в голосе сказала Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ AgreedToRedress = 1
                elif sluttiness.get(GirlName, 0) < 60 and renpy.random.randint(1, 4) <= 3:
                    "\"А раньше тебе нравилось...\" обиженно протянула Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ AgreedToRedress = 1
                    python:
                        _call_slut_friends_increase("becky", 10, 2, -1, 0, 0, 0)
                else:
                    "\"Что это на тебя нашло, когда это ты таким скромником-то заделался?!\" с удивлением спросила Бекки. \"Знаешь, я подольше тебя живу на свете, так что обойдусь я и без твоих советов, как мне одеваться.\""
                    python:
                        _call_slut_friends_increase("becky", 10, 1, -1, 0, 0, 0)

            if AgreedToRedress == 1:
                $ bradef[GirlName] = "simplebra"
                python:
                    _call_slut_friends_increase("becky", 0, 0, 0, 30, 1, -1)
                    _call_dress_up(GirlName)

            $ Talked[GirlName] = Talked.get(GirlName, 0) + 1
            return

        "Постыдить Бекки за то, что ходит без панталон" if _can_shame:
            $ AgreedToRedress = 0
            "\"Бекки, а у тебя что, сейчас под юбкой ничего нет, что ли?\" - строго спросили вы вдову."
            if panties.get(GirlName, "") != "" or (panties.get(GirlName, "") == "" and sluttiness.get(GirlName, 0) >= 45 and renpy.random.randint(1, 2) == 1):
                "\"Конечно есть, за кого ты меня принимаешь,\" Ребекка пресекла вас на полуслове."
            else:
                "\"Ну да, ты же меня сам просил без ничего ходить,\" обескураженно ответила вам она.\n\"Мне кажется, все-таки это как-то пошло и безвкусно, может лучше оденешь?\" отчитали вы бесстыдницу."
                if sluttiness.get(GirlName, 0) < 45:
                    "\"Ты прав, я только ради тебя без них ходила, но раз ты передумал, то...\" с облегчением в голосе сказала Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ AgreedToRedress = 1
                elif sluttiness.get(GirlName, 0) < 60 and renpy.random.randint(1, 4) <= 3:
                    "\"А раньше тебе нравилось...\" обиженно протянула Бекки, \"хорошо, одену как только доберусь до комода.\""
                    $ AgreedToRedress = 1
                    python:
                        _call_slut_friends_increase("becky", 10, 2, -1, 0, 0, 0)
                else:
                    "\"Что это на тебя нашло, когда это ты таким скромником-то заделался?!\" с удивлением спросила Бекки. \"Знаешь, я подольше тебя живу на свете, так что обойдусь я и без твоих советов, как мне одеваться.\""
                    python:
                        _call_slut_friends_increase("becky", 10, 1, -1, 0, 0, 0)

            if AgreedToRedress == 1:
                $ pantiesdef[GirlName] = "simplepanties"
                python:
                    _call_slut_friends_increase("becky", 0, 0, 0, 30, 1, -1)
                    _call_dress_up(GirlName)

            $ Talked[GirlName] = Talked.get(GirlName, 0) + 1
            return

        "Предложить купить вдовушке обновку" if _can_buy:
            "\"Бекки, а давай к портнихе сходим и я тебе чего-нибудь подарю там?\" - обратились вы к вдовушке.\n\"Прямо аттракцион невиданной щедрости!\" засмеялась та. \"Ну давай! Завтра с утра?\"\n\"Да, давай завтра с утра пораньше. У Ирмы Фараго, я буду тебя там ждать, вместе и выберем!\" заверили вы Бекки."
            $ DailyEventsList_Add(GirlName, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
            $ Talked[GirlName] = Talked.get(GirlName, 0) + 1
            return

        "Назад":
            return

    return
