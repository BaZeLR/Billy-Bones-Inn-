# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntIngaTalk(show_menu=True):
    if not bool(show_menu):
        if str(rooms.current_code or "") == "GroceryStore":
            vscene "images/inga/StreetSex/minet1.jpg"
        call GirlsDesc("inga")
        return

    $ Inga.mark_known()
    $ main_ui_begin_talk_state("Разговор с Ингенборг", "inga")
    if str(rooms.current_code or "") == "GroceryStore":
        vscene "images/inga/StreetSex/minet1.jpg"
    menu:
        "Осмотреть":
            call GirlsDesc("inga")
        "Закончить разговор":
            pass
    $ main_ui_end_talk_state()
    return
