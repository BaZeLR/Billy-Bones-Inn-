# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntAlberTalk:
    $ LegareProvokeYou = 0
    if str(CurLoc or "") == "WineStore":
        $ _alber_talk_picture = str(alber_random_portrait() or "").strip()
        if _alber_talk_picture:
            call ShowImage("", "", _alber_talk_picture)
    $ main_ui_begin_talk_state("Разговор с Альбером", "alber")
    $ current_action_title = "Разговор с Альбером"
    $ current_action_content = None
    $ MainTxt = "Альбер Легаре вопросительно смотрит на вас, ожидая продолжения разговора."
    $ CurLocDesc = MainTxt
    call IntAlberTalkRefresh
    return


label IntAlberTalkRefresh:
    $ main_ui_begin_talk_state("Разговор с Альбером", "alber")
    $ current_action_title = "Разговор с Альбером"
    $ current_action_content = None
    $ current_action_items = []

    if Talked.get("Alber", 0) <= 2 and LegareProvokeYou == 0:
        $ current_action_items.append(MenuItem("Поболтать со мессиром Легаре о разной всячине.", Function(main_ui_call_label, "IntAlberTalkApply", "smalltalk")))

    if Friends.get("Alber", 0) >= 6 and Talked.get("Alber", 0) <= 2 and LegareProvokeYou == 0:
        $ current_action_items.append(MenuItem("Поболтать с мессиром Легаре о более личных вещах", Function(main_ui_call_label, "IntAlberTalkApply", "personal")))

    if Friends.get("Alber", 0) >= 5 and AlberVar.get("sawwithliza", 0) and Talked.get("Alber", 0) <= 2 and LegareProvokeYou == 0:
        $ current_action_items.append(MenuItem("Спросить мессира Легаре о Лизетте", Function(main_ui_call_label, "IntAlberTalkApply", "lizett")))

    if AlberVar.get("FightYouAmanda", 0) > 0 and Talked.get("Alber", 0) <= 2 and LegareProvokeYou == 0:
        $ current_action_items.append(MenuItem("Попробовать помириться", Function(main_ui_call_label, "IntAlberTalkApply", "reconcile")))

    if LegareProvokeYou != 0:
        $ current_action_items.append(MenuItem("Проигнорировать", Function(main_ui_call_label, "IntAlberTalkApply", "ignore")))
        $ current_action_items.append(MenuItem("Обругать месье", Function(main_ui_call_label, "IntAlberTalkApply", "insult")))
        $ current_action_items.append(MenuItem("Заехать с правой", Function(main_ui_call_label, "IntAlberTalkApply", "punch")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntAlberTalkApply(choice_code=""):
    if str(choice_code or "") == "smalltalk":
        $ MainTxt = "Вы некоторое время болтаете со Альбером Легаре о несущественных вещах."
        if Talked.get("Alber", 0) <= 2 and renpy.random.randint(1, 2) == 1 and Friends.get("Alber", 0) < 5:
            $ MainTxt += "\n\nВы немного сдружились с мессиром Легаре."
            $ Friends["Alber"] = Friends.get("Alber", 0) + 1
        elif Talked.get("Alber", 0) > 2:
            $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
        $ Talked["Alber"] = Talked.get("Alber", 0) + 1
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "personal":
        $ MainTxt = "Вы некоторое время болтаете с Альбером о его жизни, отношениях с семьей и прочем."
        if Talked.get("Alber", 0) <= 2 and renpy.random.randint(1, 2) == 1 and Friends.get("Alber", 0) <= 10:
            $ MainTxt += "\n\nВы немного сдружились с мессиром Легаре."
            $ Friends["Alber"] = Friends.get("Alber", 0) + 1
        elif Talked.get("Alber", 0) > 2:
            $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
        $ Talked["Alber"] = Talked.get("Alber", 0) + 1
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "lizett":
        if AlberVar.get("talkedaboutliza", 0) == 0:
            $ MainTxt = "Набравшись смелости, вы говорите Альберу что видели как у него отсасывала Лизетта. Виноторговец сначала смущается, но потом говорит вам, что его жена постоянно занята по хозяйству и он не видит ничего плохого чтобы воспользоваться страстными губками похотливой мулатки. \"Кстати\", добавлят он: \"господин Стефан, вы, как владелец трактира, можете позвать этих двух достойных дам работать у вас. Вам будет доход, посетителей будет больше и нам,страждующим, хе-хе, будет поудобнее чем на улице\"."
            $ Friends["Alber"] = Friends.get("Alber", 0) + 1
            $ AlberVar["talkedaboutliza"] = 1
        else:
            $ MainTxt = "Вы некоторое время болтаете с Альбером о жарких губках Лизетты. Он замечает вам, что хотя Лизетта не столь опытна как ее мать, он обычно предпочитает ее, а почему - сам не знает."
        $ Talked["Alber"] = Talked.get("Alber", 0) + 1
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "\"Эй, Альбер, чего ты так надулся?\" примирительно сказали вы. \"Ну увидел я тебя с Амандой, ну вспылил. Ну подрались мы малость, бывает. Все, проехали. \" и вы протянули месье свою руку. Тот немного поколебался, но все-таки ее пожал. \"Ладно, проехали\" согласился он.\n\nВы развернулись, чтобы уйти, но услышали, как месье пробормотал сквозь зубы:"
        if AmandaVar.get("fucklegare", 0) != 0:
            $ MainTxt += "\n\n\"А все таки я ее отымел.\""
        elif AmandaVar.get("sucklegare", 0) != 0:
            $ MainTxt += "\n\n\"И все таки я ее отымею, раз она у меня уже отсосала.\""
        else:
            $ MainTxt += "\n\n\"И все таки я ее отымею.\""
        $ Talked["Alber"] = Talked.get("Alber", 0) + 1
        $ Friends["Alber"] = min(10, Friends.get("Alber", 0) + 2)
        $ AlberVar["FightYouAmanda"] = 0
        $ LegareProvokeYou = 1
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "ignore":
        $ LegareProvokeYou = 0
        $ MainTxt = "\"Да не мое это дело, Аманда уже достаточно взрослая,\" подумали вы."
        $ CurLocDesc = MainTxt
        call IntAlberTalkRefresh
        return

    if str(choice_code or "") == "insult":
        $ MainTxt = "\"Ах ты ублюдок,\" завелись вы от слов Легаре. \"На девочек молоденьких тебя, значит потянуло. Я тебе, дрищу расфранченному, яйца пообрываю и в глотку твою поганую затолкаю. Отымеет он ее, сволочь. Фантазер хренов, ебарь-неудачник блин нашелся.\"\n\nВыразив таким образом обуревавшие вас чувства невозмутимому Легаре, вы отправились восвояси. Похоже что попытка помириться не задалась."
        $ LegareProvokeYou = 0
        $ AlberVar["FightYouAmanda"] = 2
        $ Friends["Alber"] = max(1, Friends.get("Alber", 0) - 2)
        $ CurLocDesc = MainTxt
        jump MarketPlace

    if str(choice_code or "") == "punch":
        $ _int_alber_randvar = FightResult(FightLevel.get("you", 1), FightLevel.get("legare", 1), 0)
        $ MainTxt = "Слова Альбера привели вас в бешенство. Так что вы, без особых прелюдий, развернулись и врезали месье по наглой морде."
        if _int_alber_randvar == 1:
            $ MainTxt += "\n\nНаваляв от души любителю девочек, вы напоследок еще раз стукнули его мордой лица о прилавок и довольно удалились восвояси."
            call ShowImageSeq("alber", "fight", "housewon", 4)
        else:
            $ MainTxt += "\n\nНо торгаш знал о вашей несдержанности и был готов. Отбив ваш удар, он перехватил вашу руку и, дернув, развернул вас. Не успели вы сообразить что к чему, как смачным пинком виноторговец выкинул вас из своей лавки и захлопнул за вами дверь."
            call ShowImageSeq("alber", "fight", "houselost", 3)
        $ LegareProvokeYou = 0
        $ AlberVar["FightYouAmanda"] = 1
        $ Friends["Alber"] = max(0, Friends.get("Alber", 0) - 2)
        $ CurLocDesc = MainTxt
        jump MarketPlace

    jump WineStore
    return
