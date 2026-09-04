# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ChurchAfterCermon(entry_arg=0):
    $ renpy.dynamic("_church_after_event")
    if int(entry_arg or 0) != 1:
        return

    $ main_ui_begin_native_scene_state("Обход собора")
    $ scene_runtime.text = "Вы решили пройтись по опустевшему собору. Вы обошли огромное здание по периметру, заглянули в несколько коридоров и залов, затем прошли через галлерею с кабинками для исповеди."
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/church/confessionEntry.png"
    $ findAvailableEvents(True)
    $ _church_after_event = dict(event_runtime.available.get("Church", {}) or {}).get("after_cermon_walk", None)
    if _church_after_event is not None:
        $ main_ui_end_native_scene_state()
    call checkTriggers("Church", "after_cermon_walk", 0)
    if _church_after_event is not None:
        return

    $ scene_runtime.text = scene_runtime.text + "\n\nНичего интересного вы не нашли."
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Назад":
            pass
    $ main_ui_end_native_scene_state()
    return
