label IntIngaTalk(show_menu=False):
    $ Talked.setdefault("inga", 0)
    $ IngaVar.setdefault("Knowher", 0)

    if not bool(show_menu):
        call CleanScreenOverflow(3)
        call GirlsDesc("inga")
        return

    label inga_talk_menu:
        "Что сделать с Ингенборг?"
        menu:
            "Осмотреть":
                call CleanScreenOverflow(3)
                call GirlsDesc("inga")
                jump inga_talk_menu

            "Закончить разговор":
                return

    return


label int_inga_talk(show_menu=False):
    call IntIngaTalk(show_menu)
    return
