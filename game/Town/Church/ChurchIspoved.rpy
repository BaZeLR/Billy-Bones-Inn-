# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ChurchIspoved(entry_arg=0):
    if int(entry_arg or 0) != 1:
        jump Church

    $ MainTxt = "Вы зашли в маленькую кабинку для исповеди. С другой стороны ее прозвучал вопрос: \"Грешил ли ты, сын мой?\"\n\nВы решили покаяться {a=church:confession_menu:1}{color=#245b2b}в...{/color}{/a}"
    $ CurLocDesc = MainTxt
    call ShowImage("gerhard", "", "gerhardispoved")
    $ current_action_title = "Исповедь"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в собор", Function(main_ui_call_label, "ChurchReturnAfterConfession"))]
    $ renpy.restart_interaction()
    return


label ChurchIspovedMenu:
    $ current_action_title = "В чем покаяться?"
    $ current_action_content = None
    $ current_action_items = []

    $ current_action_items.append(MenuItem("В разных пустяках", Function(main_ui_call_label, "ChurchIspovedChoice", "small")))
    if HadSex.get("georgett", 0) > 0:
        $ current_action_items.append(MenuItem("В том, что совокуплялись с Жоржеттой", Function(main_ui_call_label, "ChurchIspovedChoice", "georgett")))
    if HadSex.get("georgett", 0) > 0 and GeorgettVar.get("fuckinchurch", 0) and GeorgettVar.get("georgettadmit", 0) == 1:
        $ current_action_items.append(MenuItem("В том, что совокуплялись с Жоржеттой прямо во время службы", Function(main_ui_call_label, "ChurchIspovedChoice", "church")))
    if HadSex.get("georgett", 0) > 0 and GeorgettVar.get("fuckinchurch", 0) and GeorgettVar.get("lizasawinchurch", 0) and GeorgettVar.get("churchgeorgettadmit", 0):
        $ current_action_items.append(MenuItem("В том, что совокуплялись с Жоржеттой прямо во время службы на глазах у ее дочки", Function(main_ui_call_label, "ChurchIspovedChoice", "church_liza")))
    $ current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, "ChurchIspoved", 1)))
    $ renpy.restart_interaction()
    return


label ChurchIspovedChoice(choice_code=""):
    if str(choice_code or "") == "small":
        $ MainTxt = "Вы покаялись в том, что ругались и пару раз обсчитали пьяных в своем трактире на один-два мараведи.\n\n\"Это небольшой грех сын мой и я его тебе отпускаю\" - прозвучал ответ."
    elif str(choice_code or "") == "georgett":
        $ MainTxt = "Вы покаялись в том, что сношались с проституткой Жоржеттой. Отец Герхард вас подробно распросил обо всех обстоятельствах и как именно и сколько раз вы имели дело с Жоржеттой. Потом он сказал:\n\n\"Великий бог Ильматер завещал нам плодиться и размножаться. Коль обе стороны желают соития, то не грех это сын мой!\""
        $ GeorgettVar["georgettadmit"] = 1
    elif str(choice_code or "") == "church":
        $ MainTxt = "Вы покаялись в том, что трахнули Жоржетту в соборе прямо во время службы. Отец Герхард вас подробно распросил обо всех обстоятельствах, о том, как вам удалось остаться незамеченными и как все прошло. Потом он сказал:\n\n\"Великий бог Ильматер завещал нам плодиться и размножаться. Конечно нужно это делать вне храма, а в храме смиренно слушать службу. А ты, сын мой, не утерпел. Грех это, но не великий. Коль покаялся ты в нем и рассказал все честно, без утайки, то отпускаю я его тебе!\""
        $ GeorgettVar["churchgeorgettadmit"] = 1
    else:
        $ MainTxt = "Вы сказали что вы рассказали не все. Пока вы имели Жоржетту, за вами наблюдала, лаская себя, ее дочка Лизетта. Отец Герхард заметно оживился и стал расспрашивать вас о подробностях, как Лизетта вела себя, что сказала на это ей мать, и прочем. Потом он сказал:\n\n\"Великий бог Ильматер завещал родителям передавать все свои знания и умения детям. Так что отдельного греха в том нет, разве что, как я уже говорил тебе, в храме нужно смиренно слушать службу. Но тот грех я тебе уже отпустил, так что иди с миром\""
        $ GeorgettVar["churchlizaadmit"] = 1

    $ CurLocDesc = MainTxt
    call ShowImage("gerhard", "", "gerhardispoved")
    $ current_action_title = "Исповедь"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в собор", Function(main_ui_call_label, "ChurchReturnAfterConfession"))]
    $ renpy.restart_interaction()
    return


label ChurchReturnAfterConfession:
    call AdvanceTimeAndRestore("ChurchRestore")
    $ renpy.restart_interaction()
    return
