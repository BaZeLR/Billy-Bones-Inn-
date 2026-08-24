init python:
    def tavern_help_pages():
        book_text = str(TavernHelpBookItem.custom_properties.get("help_text", [""])[0] or "")
        paragraphs = [str(part).strip() for part in book_text.split("\n\n") if str(part).strip()]
        pages = []
        current_parts = []
        current_len = 0
        for paragraph in paragraphs:
            if current_parts and current_len + len(paragraph) > 850:
                pages.append("\n\n".join(current_parts))
                current_parts = [paragraph]
                current_len = len(paragraph)
            else:
                current_parts.append(paragraph)
                current_len += len(paragraph)
        if current_parts:
            pages.append("\n\n".join(current_parts))
        return pages or [""]

    TavernHelpRoomDefinition = Room(
        code_name="TavernHelp",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Бабслей и Литрбол для чайников",
        bg_picture="bg book",
        descriptions=[],
        exits=[RoomExit(label="Оторваться от чтения", target="TavernMain")],
        game_items=[],
        state={"page": 0},
    )


label TavernHelp:
    scene black
    show bg book at master
    $ rooms.enter("TavernHelp")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ main_ui_runtime.object_id = "book_001"
    $ rooms.get("TavernHelp").state["page"] = 0
    show screen main_ui
    jump TavernHelpReadPage


label TavernHelpReadPage:
    $ renpy.dynamic("_book", "_help_text", "_stash_text", "_help_pages", "_help_page")
    $ _book = TavernHelpBookItem
    $ _help_text = list(_book.custom_properties.get("help_text", []) or [])
    $ _stash_text = _help_text[1] if len(_help_text) > 1 else ""
    $ _help_pages = tavern_help_pages()
    $ _help_page = max(0, min(int(rooms.get("TavernHelp").state.get("page", 0) or 0), len(_help_pages) - 1))
    $ rooms.get("TavernHelp").state["page"] = _help_page
    $ scene_runtime.text = _help_pages[_help_page]
    if int(_book.state.get("stash_taken", 0) or 0) == 1 and _stash_text and _help_page == len(_help_pages) - 1:
        $ scene_runtime.text += "\n\n" + _stash_text
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Читать дальше" if _help_page < len(_help_pages) - 1:
            $ rooms.get("TavernHelp").state["page"] = _help_page + 1
            jump TavernHelpReadPage

        "Перечитать сначала" if _help_page >= len(_help_pages) - 1:
            $ rooms.get("TavernHelp").state["page"] = 0
            jump TavernHelpReadPage

        "Совсем разоряюсь, возьму 150 мараведи из заначки" if int(_book.state.get("stash_taken", 0) or 0) == 0 and player.economy.money <= 100:
            $ player.add_money(150)
            $ _book.state["stash_taken"] = 1
            $ _book.state["stash_amount"] = 0
            call stat
            $ scene_runtime.text = _stash_text
            $ scene_runtime.location_text = scene_runtime.text
            jump TavernHelpReadPage

        "Заначку пока лучше поберечь" if int(_book.state.get("stash_taken", 0) or 0) == 0 and player.economy.money > 100:
            $ scene_runtime.text = "У вас пока достаточно денег. Заначку можно оставить на действительно черный день."
            $ scene_runtime.location_text = scene_runtime.text
            jump TavernHelpReadPage

        "Заначка уже пуста" if int(_book.state.get("stash_taken", 0) or 0) == 1:
            $ scene_runtime.text = "Вы уже забрали деньги из семейной заначки."
            $ scene_runtime.location_text = scene_runtime.text
            jump TavernHelpReadPage

        "Оторваться от чтения":
            jump TavernMain
