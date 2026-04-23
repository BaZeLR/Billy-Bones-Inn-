label IntIngaTalk(show_menu=True):
    $ Talked.setdefault("inga", 0)
    $ IngaVar.setdefault("Knowher", 0)

    if not bool(show_menu):
        call CleanScreenOverflow(3)
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
