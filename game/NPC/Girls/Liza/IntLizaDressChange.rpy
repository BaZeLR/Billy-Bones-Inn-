# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntLizaDressChange(GirlNameILT="liza", agreed_to_redress=0):
    $ renpy.dynamic("_other_saw")
    $ renpy.dynamic("_can_remove_panties", "_can_shame", "_can_buy")
    python:
        _can_remove_panties = Liza.rel > 8 and Liza.current_underwear("panties", "") != "" and Liza.talk_count() < 2
        _can_shame = Liza.rel > 8 and Liza.talk_count() < 2
        _can_buy = Liza.rel > 8 and daily_events.exists("", "BuyDressTom", "") == 0 and daily_events.exists(GirlNameILT, "BuyDress", "") == 0 and Liza.talk_count() < 2 and int(calendar_v2.week or 0) != 6

    if not (_can_remove_panties or _can_shame or _can_buy):
        return

    menu:
        "Предложить Лизетте снять панталоны" if _can_remove_panties:
            $ agreed_to_redress = 0
            "\"Лизетта, а чего ты в панталонах-то ходишь?\" - поинтересовались вы у вашей юной работницы. \"Мамка-то твоя без них ходит, бери с нее пример! Они тебе только в обузу, снимать, одевать по многу раз за день...\""

            if Liza.clothing_slut("bottom") < 4:
                if Liza.corruption < 40:
                    "\"Спасибочки конечно за заботу, но руки у меня не отсохнут их снимать-надевать. Чай не слабосильная,\" отбрила вас Лизетта."
                else:
                    "\"А и то верно, да и мамочка несколько раз мне уже говорила, что можно и без них, \" согласила с вами Лизетта. \"Ладно, попробую.\""
                    $ agreed_to_redress = 1
                    if Liza.corruption < 50:
                        if procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaDressChange.rpy:procedural_randint:63:2") == 1:
                            "Лизетта зашла в комнатку, где они с мамой обычно обслуживали посетителей, и сноровисто стянула с себя панталончики."
                        else:
                            "Лизетта скромно спряталась за стойкой и быстро избавилась от мешающего ей нижнего белья."
                    else:
                        "Решив, что лучшая демонстрация - лучшая реклама ее услуг, Лизетта в тот же момент стянула с себя панталоны не прячась и не пугаясь возможных зрителей."
            else:
                if Liza.corruption < 50:
                    "\"Стефанчик, да ты прикалываешься?\" недоверчиво сказала Лизетта, услышав ваше предложение. \"У меня же платьичко смотри, какое короткое. Если я без панталон буду, то я мою щелку всем и каждому покажу, это все равно как голой на улицу выйти. Это моя мамка может, а у меня духу на такое не хватит.\""
                else:
                    "\"Ха, Стефан,\" засмеялась Лизетта. \"Ты хочешь чтобы я, в таком коротком платьичке, ничего под ним не носила? И всем свою щелочку светила?\"\n\"Именно!\" согласились вы. \"Так ты всем покажешь, чего ты предлагаешь, глядишь, и клиентов у тебя прибавится. Ну и ветерок тебе нижние губки-то пощекочет, мокренькой будешь,  значит приятнее тебе клиентов принимать будет. Сплошной выигрыш, не веришь мне - у мамы спроси!\"\n\"А чего ее справшивать, она мне давно тоже самое советовала,\" и Лизетта в тот же момент стянула с себя панталоны не прячась и не пугаясь возможных зрителей."
                    $ agreed_to_redress = 1

            if agreed_to_redress == 1:
                $ Liza.set_current_underwear("panties", "")
                $ Liza.apply_social_chance(0, 0, 0, 60, 2, 1, "dress_change_panties")

            $ _other_saw = Liza.dress_change_other_saw_text(agreed_to_redress)
            if str(_other_saw or "").strip() != "":
                "[_other_saw]"
            $ Liza.finish_talk()
            return

        "Постыдить Лизетту за то, что ходит без лифчика" if _can_shame:
            $ agreed_to_redress = 0
            "\"Лизетта, а не стыдно тебе без лифа ходить?\" - попробовали пристыдить вы юную шлюху. Однако это был дохлый номер: \"Не, не стыдно,\" спокойно ответила вам она. \"Нет у меня лифа, у мамы нету и она всегда меня учила, что от него сиськи плохо растут. А ей это бабуся рассказала. Так что не надо мне тут мораль читать.\""
            $ Liza.finish_talk()
            return

        "Постыдить Лизетту за отстутсвие панталон" if _can_shame:
            $ agreed_to_redress = 0
            "\"Лизетта, а чего это ты без панталон ходишь? Я понимаю, что в твоем ремесле они скорее мешают, но стыд-то знать надо?\" - раскритиковали вы юную давалку."
            if Liza.current_underwear("panties", "") != "" or (Liza.current_underwear("panties", "") == "" and Liza.corruption >= 45 and procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaDressChange.rpy:procedural_randint:96:3") == 1):
                "\"А может они у меня есть? Ты точно все проверил? Вот сними меня и посмотри, а пока верь мне на слово, что они у меня есть!\" отбрехалась от вас Лизетта."
            else:
                "\"Ну нет и нет, что ты шум поднимаешь? Мне так удобнее работается, сам же говорил!\n\"Может и удобнее, только все-таки это приличное заведение, так что одень как ты их, подруга, обратно!\" отчитали вы бесстыдницу."
                if Liza.corruption < 45:
                    "\"Ну, ладно, ладно, не ругайся. Приличное значит приличное, сейчас одену.\""
                    $ agreed_to_redress = 1
                elif Liza.corruption < 60 and procedural_randint(1, 4, key="procedural:NPC/Girls/Liza/IntLizaDressChange.rpy:procedural_randint:103:4") <= 3:
                    "\"Ага, то сам говорил, посмотри на маму, посмотри на маму, так тебе удобнее мол будет, а теперь стыдит. Приличное у него видите ли заведение. Ладно, не плачь, ща пойду наверх одену.\""
                    $ agreed_to_redress = 1
                    $ Liza.apply_social_chance(7, 1, -1, 0, 0, 0, "dress_change_shame")
                else:
                    "\"А ты вот мамашке моей эту байку расскажи! То-то она в коротюлечком платье без них шляется. Не, ей ты ни слова не сказал, только ко мне придираешься.\" отбрила вас Лизетта. \"А мне, между прочим, так клиентов больше набегает. Так что не учи меня, дяденька.\""
                    $ Liza.apply_social_chance(7, 1, -1, 0, 0, 0, "dress_change_shame")

            if agreed_to_redress == 1:
                $ Liza.set_current_underwear("panties", "simplepanties")
                $ Liza.apply_social_chance(0, 0, 0, 30, 1, -1, "dress_change_panties")

            $ Liza.finish_talk()
            return

        "Предложить купить Лизетте обновку" if _can_buy:
            "\"Лизка, красотулька моя, а хочешь я тебе тряпку новую подарю?\" - порадовали вы юную давалку.\n\"Подаришь?\" обрадовалась та. \"Конечно хочу, Стефанчик, миленький!\" От избытка чувств она даже чмокнула вас в губы.\n\"Ну тогда завтра, с утра пораньше, беги к Ирме Фараго, я буду тебя там ждать, вместе и выберем!\" заверили вы шалаву."
            $ daily_events.add(GirlNameILT, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")
            $ Liza.finish_talk()
            return

        "Назад":
            return

    return
