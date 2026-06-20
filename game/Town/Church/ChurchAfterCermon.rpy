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

    $ MainTxt = MainTxt + "\n\nНичего интересного вы не нашли."
    $ CurLocDesc = MainTxt
    $ current_action_items.append(MenuItem("Вернуться в собор", Jump("Church")))
    $ renpy.restart_interaction()
    return
