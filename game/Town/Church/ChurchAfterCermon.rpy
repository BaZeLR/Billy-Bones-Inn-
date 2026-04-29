# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def church_aftercermon_seen_total():
        try:
            state = ChurchAfterCermon if isinstance(ChurchAfterCermon, dict) else {}
        except Exception:
            state = {}
        total = 0
        for _value in list(state.values()):
            try:
                total += int(_value or 0)
            except Exception:
                pass
        return total

    def church_aftercermon_pick_scene_code():
        available = []

        if int(BeckyVar.get("PriestAdvice", 0) or 0) in (1, 2):
            return "becky"

        if church_aftercermon_seen_total() == 0:
            if int(GeorgettVar.get("churchgeorgettadmit", 0) or 0) > 0:
                available.append("georgett")
            if int(GeorgettVar.get("churchlizaadmit", 0) or 0) > 0:
                available.append("liza")

        if int(BeckyVar.get("PriestAdvice", 0) or 0) > 0:
            available.append("becky")

        if not available:
            return ""
        if len(available) == 1:
            return str(available[0] or "")
        return str(renpy.random.choice(available) or "")


label ChurchAfterCermon(entry_arg=0):
    if int(entry_arg or 0) != 1:
        jump Church

    $ MainTxt = "Вы решили пройтись по опустевшему собору. Вы обошли огромное здание по периметру, заглянули в несколько коридоров и залов, затем прошли через галлерею с кабинками для исповеди."
    $ CurLocDesc = MainTxt
    call ShowImage("general", "", "LocChurchIspoved2")
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items.append(MenuItem("Вернуться в собор", Call("ChurchRestore")))
        return

    python:
        _church_scene_code = str(church_aftercermon_pick_scene_code() or "")

    if _church_scene_code == "georgett":
        call IntGeorgettAfterCermon
        $ MainTxt = MainTxt + "\n\nЗа кабинками для исповеди вы заметили неприметную дверь, ведущую внутрь храма. Из-за нее слышаться приглушенные голоса. Вы замечаете большую замочную скважину, через которую вы можете {a=call:AfterCermonGeorgett}{color=#245b2b}посмотреть{/color}{/a}, что там происходит."
        $ CurLocDesc = MainTxt
        $ current_action_items.append(MenuItem("Посмотреть", Call("AfterCermonGeorgett")))
    elif _church_scene_code == "liza":
        call IntLizettAfterCermon
        $ MainTxt = MainTxt + "\n\nЗа кабинками для исповеди вы заметили неприметную дверь, ведущую внутрь храма. Из-за нее слышаться приглушенные голоса. Вы замечаете большую замочную скважину, через которую вы можете {a=call:AfterCermonLizett}{color=#245b2b}посмотреть{/color}{/a}, что там происходит."
        $ CurLocDesc = MainTxt
        $ current_action_items.append(MenuItem("Посмотреть", Call("AfterCermonLizett")))
    elif _church_scene_code == "becky":
        call IntBeckyAfterCermon
        $ MainTxt = MainTxt + "\n\nВы заметили, как миссис Блэнкеншип направилась было к кабинке для исповеди, но отец Герхард взял ее за руку и повел к неприметной двери, которую он отпер висящим у него на поясе ключом. Как только вдова проследовала за ним, дверь захлопнулась и послышался стук задвигаемого засова. Хотя вы можете попробовать {a=call:AfterCermonBecky}{color=#245b2b}посмотреть{/color}{/a}, что там происходит через замочную скважину."
        $ CurLocDesc = MainTxt
        $ current_action_items.append(MenuItem("Посмотреть", Call("AfterCermonBecky")))
    else:
        $ MainTxt = MainTxt + "\n\nНичего интересного вы не нашли."
        $ CurLocDesc = MainTxt

    if BeckyVar.get("PriestAdvice", 0) == 0 or BeckyVar.get("PriestAdvice", 0) > 2:
        $ current_action_items.append(MenuItem("Вернуться в собор", Call("ChurchRestore")))
    $ renpy.restart_interaction()
    return
