# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ChurchIspoved(entry_arg=0):
    if int(entry_arg or 0) != 1:
        jump Church

    $ MainTxt = "Вы зашли в маленькую кабинку для исповеди. С другой стороны ее прозвучал вопрос: \"Грешил ли ты, сын мой?\"\n\nВы решили покаяться {a=church:confession_menu:1}{color=#245b2b}в...{/color}{/a}"
    $ CurLocDesc = MainTxt
    vscene "images/gerhard/gerhardispoved.jpg"
    $ current_action_title = "Исповедь"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в собор", [SetVariable("LastAdvancedMinutes", 60), Function(calendar_v2.sync_state), Function(calendar_v2.advance_minutes, 60), Function(npc_schedule_sync_all), Jump("Church")])]
    $ renpy.restart_interaction()
    return


label ChurchIspovedMenu:
    $ current_action_title = "В чем покаяться?"
    $ current_action_content = None
    $ current_action_items = []

    $ current_action_items.append(MenuItem("В разных пустяках", Call("ChurchIspovedChoice", "small")))
    if Georgett.had_sex_count() > 0:
        $ current_action_items.append(MenuItem("В том, что совокуплялись с Жоржеттой", Call("ChurchIspovedChoice", "georgett")))
    if Georgett.had_sex_count() > 0 and Georgett.story_value("church_bench_seen", 0):
        $ current_action_items.append(MenuItem("В том, что уединились с Жоржеттой во время службы", Call("ChurchIspovedChoice", "church_bench")))
    if Georgett.had_sex_count() > 0 and Georgett.story_value("church_doggy_seen", 0):
        $ current_action_items.append(MenuItem("В том, что рискнули с Жоржеттой прямо во время службы", Call("ChurchIspovedChoice", "church_doggy")))
    if Georgett.had_sex_count() > 0 and Georgett.story_value("church_liza_seen", 0):
        $ current_action_items.append(MenuItem("В том, что Лизетта видела вас с Жоржеттой во время службы", Call("ChurchIspovedChoice", "church_liza")))
    $ current_action_items.append(MenuItem("Назад", Call("ChurchIspoved", 1)))
    $ renpy.restart_interaction()
    return


label ChurchIspovedChoice(choice_code=""):
    if str(choice_code or "") == "small":
        $ MainTxt = "Вы покаялись в том, что ругались и пару раз обсчитали пьяных в своем трактире на один-два мараведи.\n\n\"Это небольшой грех сын мой и я его тебе отпускаю\" - прозвучал ответ."
    elif str(choice_code or "") == "georgett":
        $ MainTxt = "Вы покаялись в том, что сношались с проституткой Жоржеттой. Отец Герхард вас подробно распросил обо всех обстоятельствах и как именно и сколько раз вы имели дело с Жоржеттой. Потом он сказал:\n\n\"Великий бог Ильматер завещал нам плодиться и размножаться. Коль обе стороны желают соития, то не грех это сын мой!\""
        $ Georgett.set_story_value("georgettadmit", 1)
    elif str(choice_code or "") == "church_bench":
        $ MainTxt = "Вы рассказали отцу Герхарду, что во время службы уединились с Жоржеттой в темном углу собора. Священник подробно расспросил вас об обстоятельствах, затем строго напомнил, что в храме следует думать о молитве, а не о плотских желаниях."
        $ Georgett.set_story_value("churchgeorgettadmit", 1)
    elif str(choice_code or "") == "church_doggy":
        $ MainTxt = "Вы признались, что рискнули с Жоржеттой прямо во время службы, почти не скрываясь. Отец Герхард долго молчал, потом сказал, что честное покаяние лучше утаивания."
        $ Georgett.set_story_value("churchgeorgettadmit", 1)
    else:
        $ MainTxt = "Вы добавили, что Лизетта видела вас с Жоржеттой во время службы. Отец Герхард стал расспрашивать уже не о вас, а о том, как на это смотрели мать и дочь, после чего отпустил вас с необычайно задумчивым видом."
        $ Georgett.set_story_value("churchlizaadmit", 1)

    $ CurLocDesc = MainTxt
    vscene "images/gerhard/gerhardispoved.jpg"
    $ current_action_title = "Исповедь"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в собор", [SetVariable("LastAdvancedMinutes", 60), Function(calendar_v2.sync_state), Function(calendar_v2.advance_minutes, 60), Function(npc_schedule_sync_all), Jump("Church")])]
    $ renpy.restart_interaction()
    return
