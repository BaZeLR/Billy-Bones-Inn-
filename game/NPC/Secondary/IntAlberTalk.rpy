# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntAlberTalk:
    $ Alber.set_var_int("LegareProvokeYou", 0)
    if str(CurLoc or "") == "WineStore":
        $ _alber_talk_picture = str(alber_random_portrait() or "").strip()
        if _alber_talk_picture:
            vscene _alber_talk_picture
    $ main_ui_begin_talk_state("Разговор с Альбером", "alber")
    $ current_action_title = "Разговор с Альбером"
    $ current_action_content = None
    $ MainTxt = "Альбер Легаре вопросительно смотрит на вас, ожидая продолжения разговора."
    $ CurLocDesc = MainTxt
    call IntAlberTalkRefresh
    return


label IntAlberTalkRefresh:
    $ _alber_talked = Alber.talk_count()
    $ _alber_rel = people_to_int(Alber.rel, 0)
    $ _legare_provoke = Alber.var_int("LegareProvokeYou", 0)
    $ main_ui_begin_talk_state("Разговор с Альбером", "alber")
    $ current_action_title = "Разговор с Альбером"
    $ current_action_content = None
    $ current_action_items = []

    if _alber_talked <= 2 and _legare_provoke == 0:
        $ current_action_items.append(MenuItem("Поболтать со мессиром Легаре о разной всячине.", Call("IntAlberTalkApply", "smalltalk")))

    if _alber_rel >= 6 and _alber_talked <= 2 and _legare_provoke == 0:
        $ current_action_items.append(MenuItem("Поболтать с мессиром Легаре о более личных вещах", Call("IntAlberTalkApply", "personal")))

    if _alber_rel >= 5 and Alber.var_int("sawwithliza", 0) and _alber_talked <= 2 and _legare_provoke == 0:
        $ current_action_items.append(MenuItem("Спросить мессира Легаре о Лизетте", Call("IntAlberTalkApply", "lizett")))

    if Alber.var_int("FightYouAmanda", 0) > 0 and _alber_talked <= 2 and _legare_provoke == 0:
        $ current_action_items.append(MenuItem("Попробовать помириться", Call("IntAlberTalkApply", "reconcile")))

    if _legare_provoke != 0:
        $ current_action_items.append(MenuItem("Проигнорировать", Call("IntAlberTalkApply", "ignore")))
        $ current_action_items.append(MenuItem("Обругать месье", Call("IntAlberTalkApply", "insult")))
        $ current_action_items.append(MenuItem("Заехать с правой", Call("IntAlberTalkApply", "punch")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntAlberTalkApply(choice_code=""):
    $ _alber_talked = Alber.talk_count()
    if str(choice_code or "") == "smalltalk":
        $ MainTxt = "Вы некоторое время болтаете со Альбером Легаре о несущественных вещах."
        if _alber_talked <= 2 and procedural_randint(1, 2, "alber_smalltalk_%s_%s" % (dayspassed, _alber_talked)) == 1 and people_to_int(Alber.rel, 0) < 5:
            $ MainTxt += "\n\nВы немного сдружились с мессиром Легаре."
            $ Alber.add_relation(1)
        elif _alber_talked > 2:
            $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
        $ Alber.finish_talk()
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "personal":
        $ MainTxt = "Вы некоторое время болтаете с Альбером о его жизни, отношениях с семьей и прочем."
        if _alber_talked <= 2 and procedural_randint(1, 2, "alber_personal_%s_%s" % (dayspassed, _alber_talked)) == 1 and people_to_int(Alber.rel, 0) <= 10:
            $ MainTxt += "\n\nВы немного сдружились с мессиром Легаре."
            $ Alber.add_relation(1)
        elif _alber_talked > 2:
            $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
        $ Alber.finish_talk()
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "lizett":
        if Alber.var_int("talkedaboutliza", 0) == 0:
            $ MainTxt = "Набравшись смелости, вы говорите Альберу что видели как у него отсасывала Лизетта. Виноторговец сначала смущается, но потом говорит вам, что его жена постоянно занята по хозяйству и он не видит ничего плохого чтобы воспользоваться страстными губками похотливой мулатки. \"Кстати\", добавлят он: \"господин Стефан, вы, как владелец трактира, можете позвать этих двух достойных дам работать у вас. Вам будет доход, посетителей будет больше и нам,страждующим, хе-хе, будет поудобнее чем на улице\"."
            $ Alber.add_relation(1)
            $ Alber.set_var_int("talkedaboutliza", 1)
        else:
            $ MainTxt = "Вы некоторое время болтаете с Альбером о жарких губках Лизетты. Он замечает вам, что хотя Лизетта не столь опытна как ее мать, он обычно предпочитает ее, а почему - сам не знает."
        $ Alber.finish_talk()
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "\"Эй, Альбер, чего ты так надулся?\" примирительно сказали вы. \"Ну увидел я тебя с Амандой, ну вспылил. Ну подрались мы малость, бывает. Все, проехали. \" и вы протянули месье свою руку. Тот немного поколебался, но все-таки ее пожал. \"Ладно, проехали\" согласился он.\n\nВы развернулись, чтобы уйти, но услышали, как месье пробормотал сквозь зубы:"
        if Amanda.var_int("fucklegare", 0) != 0:
            $ MainTxt += "\n\n\"А все таки я ее отымел.\""
        elif Amanda.var_int("sucklegare", 0) != 0:
            $ MainTxt += "\n\n\"И все таки я ее отымею, раз она у меня уже отсосала.\""
        else:
            $ MainTxt += "\n\n\"И все таки я ее отымею.\""
        $ Alber.finish_talk()
        $ Alber.add_relation(2, 10)
        $ Alber.set_var_int("FightYouAmanda", 0)
        $ Alber.set_var_int("LegareProvokeYou", 1)
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "ignore":
        $ Alber.set_var_int("LegareProvokeYou", 0)
        $ MainTxt = "\"Да не мое это дело, Аманда уже достаточно взрослая,\" подумали вы."
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "insult":
        $ MainTxt = "\"Ах ты ублюдок,\" завелись вы от слов Легаре. \"На девочек молоденьких тебя, значит потянуло. Я тебе, дрищу расфранченному, яйца пообрываю и в глотку твою поганую затолкаю. Отымеет он ее, сволочь. Фантазер хренов, ебарь-неудачник блин нашелся.\"\n\nВыразив таким образом обуревавшие вас чувства невозмутимому Легаре, вы отправились восвояси. Похоже что попытка помириться не задалась."
        $ Alber.set_var_int("LegareProvokeYou", 0)
        $ Alber.set_var_int("FightYouAmanda", 2)
        $ Alber.rel = max(1, people_to_int(Alber.rel, 0) - 2)
        $ Alber.relationship = Alber.rel
        $ CurLocDesc = MainTxt
        jump MarketPlace

    if str(choice_code or "") == "punch":
        $ _int_alber_fight_level = player_state(False).combat.fight_level
        $ _int_alber_randvar = FightResult(_int_alber_fight_level.get("you", 1), _int_alber_fight_level.get("legare", 1), 0)
        $ MainTxt = "Слова Альбера привели вас в бешенство. Так что вы, без особых прелюдий, развернулись и врезали месье по наглой морде."
        if _int_alber_randvar == 1:
            $ MainTxt += "\n\nНаваляв от души любителю девочек, вы напоследок еще раз стукнули его мордой лица о прилавок и довольно удалились восвояси."
            call ShowImageSeq("alber", "fight", "housewon", 4)
        else:
            $ MainTxt += "\n\nНо торгаш знал о вашей несдержанности и был готов. Отбив ваш удар, он перехватил вашу руку и, дернув, развернул вас. Не успели вы сообразить что к чему, как смачным пинком виноторговец выкинул вас из своей лавки и захлопнул за вами дверь."
            call ShowImageSeq("alber", "fight", "houselost", 3)
        $ Alber.set_var_int("LegareProvokeYou", 0)
        $ Alber.set_var_int("FightYouAmanda", 1)
        $ Alber.add_relation(-2)
        $ CurLocDesc = MainTxt
        jump MarketPlace

    jump WineStore
    return
