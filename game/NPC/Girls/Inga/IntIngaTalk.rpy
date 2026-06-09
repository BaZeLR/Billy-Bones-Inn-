# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntIngaTalk(show_menu=True):
    $ Talked.setdefault("inga", 0)
    $ IngaVar.setdefault("Knowher", 0)
    if str(CurLoc or "") == "GroceryStore":
        $ _inga_talk_picture = str(grocery_store_talk_picture("inga") or "").strip()
        if _inga_talk_picture:
            call ShowImage("", "", _inga_talk_picture)

    if not bool(show_menu):
        call GirlsDesc("inga")
        return

    $ main_ui_begin_talk_state("Разговор с Ингенборг", "inga")
    $ current_action_title = "Разговор с Ингенборг"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Осмотреть", Function(main_ui_call_label, "IntIngaTalk", False)),
        MenuItem("Закончить разговор", Function(main_ui_end_talk_state)),
    ]

    return


label int_inga_talk(show_menu=True):
    call IntIngaTalk(show_menu)
    return
