# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ChurchAfterCermon(entry_arg=0):
    if int(entry_arg or 0) != 1:
        jump Church

    $ MainTxt = "Вы решили пройтись по опустевшему собору. Вы обошли огромное здание по периметру, заглянули в несколько коридоров и залов, затем прошли через галлерею с кабинками для исповеди."
    $ CurLocDesc = MainTxt
    vscene "images/church/confessionEntry.png"
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items.append(MenuItem("Вернуться в собор", Jump("Church")))
        return

    call checkTriggers("Church", "after_cermon_walk", 0)
    if _return:
        return

    if int(BeckyVar.get("PriestAdvice", 0) or 0) > 0:
        call IntBeckyAfterCermon
        $ MainTxt = MainTxt + "\n\nВы заметили, как миссис Блэнкеншип направилась было к кабинке для исповеди, но отец Герхард взял ее за руку и повел к неприметной двери, которую он отпер висящим у него на поясе ключом. Как только вдова проследовала за ним, дверь захлопнулась и послышался стук задвигаемого засова. Хотя вы можете попробовать {a=church:after_becky:1}{color=#245b2b}посмотреть{/color}{/a}, что там происходит через замочную скважину."
        $ CurLocDesc = MainTxt
        $ current_action_items.append(MenuItem("Посмотреть", Function(main_ui_call_label, "AfterCermonBecky")))
    else:
        $ MainTxt = MainTxt + "\n\nНичего интересного вы не нашли."
        $ CurLocDesc = MainTxt

    if BeckyVar.get("PriestAdvice", 0) == 0 or BeckyVar.get("PriestAdvice", 0) > 2:
        $ current_action_items.append(MenuItem("Вернуться в собор", Jump("Church")))
    $ renpy.restart_interaction()
    return
