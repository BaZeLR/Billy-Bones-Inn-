# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def TavernHelpBuildPages():
        book_text = str(TavernMainBookObject.custom_properties.get("help_text", [""])[0] or "")
        paragraphs = [str(part).strip() for part in book_text.split("\n\n") if str(part).strip()]
        pages = []
        current_parts = []
        current_len = 0
        page_limit = 850

        for paragraph in paragraphs:
            paragraph_len = len(paragraph)
            if current_parts and (current_len + paragraph_len) > page_limit:
                pages.append("\n".join(current_parts))
                current_parts = [paragraph]
                current_len = paragraph_len
            else:
                current_parts.append(paragraph)
                current_len += paragraph_len

        if current_parts:
            pages.append("\n".join(current_parts))

        if not pages:
            pages.append("")

        return pages

    TavernHelpRoom = Room(
        code_name="TavernHelp",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Бабслей и Литрбол для чайников",
        bg_picture="bg book",
        descriptions=[],
        exits=[
            RoomExit(label="Оторваться от чтения", target="TavernMain"),
        ],
        game_items=[],
    )

default TavernHelpPage = 0
default CheatMoneyGrab = 0


label TavernHelp:
    $ _book = TavernMainBookObject
    $ _help_text = list(_book.custom_properties.get("help_text", []) or [])
    $ _stash_text = _help_text[1] if len(_help_text) > 1 else ""

    scene black
    show bg book at master

    $ CurrentRoom = TavernHelpRoom
    $ CurLoc = "TavernHelp"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    $ current_action_title = "Бабслей и Литрбол для чайников"
    $ current_action_content = None
    $ current_action_items = []
    $ current_object_id = "book_001"
    $ TavernHelpPage = 0
    call TavernHelpShowPage
    call screen main_ui
    jump TavernHelp


label TavernHelpApply(choice_code=""):
    $ _choice = str(choice_code or "")
    $ _help_pages = TavernHelpBuildPages()
    $ _last_help_page = len(_help_pages) - 1

    if _choice == "next" and TavernHelpPage < _last_help_page:
        $ TavernHelpPage += 1
    elif _choice == "restart" and TavernHelpPage >= _last_help_page:
        $ TavernHelpPage = 0
    elif _choice == "stash_take" and int(CheatMoneyGrab or 0) == 0 and money <= 100:
        call TavernHelpTakeStash
    elif _choice == "stash_wait" and int(CheatMoneyGrab or 0) == 0 and money > 100:
        $ MainTxt = "У вас пока достаточно денег. Заначку можно оставить на действительно черный день."
        $ CurLocDesc = MainTxt
        call TavernHelpShowPage
        call screen main_ui
        jump TavernHelp
    elif _choice == "stash_empty" and int(CheatMoneyGrab or 0) == 1:
        $ MainTxt = "Вы уже забрали деньги из семейной заначки."
        $ CurLocDesc = MainTxt
        call TavernHelpShowPage
        call screen main_ui
        jump TavernHelp
    elif _choice == "leave":
        jump TavernMain

    call TavernHelpShowPage
    call screen main_ui
    jump TavernHelp


label TavernHelpShowPage:
    $ _book = TavernMainBookObject
    $ _help_text = list(_book.custom_properties.get("help_text", []) or [])
    $ _stash_text = _help_text[1] if len(_help_text) > 1 else ""
    $ _help_pages = TavernHelpBuildPages()
    if TavernHelpPage < 0:
        $ TavernHelpPage = 0
    if TavernHelpPage >= len(_help_pages):
        $ TavernHelpPage = len(_help_pages) - 1

    $ CurLocDesc = _help_pages[TavernHelpPage]
    if int(_book.state.get('stash_taken', 0) or 0) == 1 and _stash_text != "" and TavernHelpPage == (len(_help_pages) - 1):
        $ CurLocDesc = CurLocDesc + "\n" + _stash_text
    $ MainTxt = CurLocDesc
    $ current_action_title = "Бабслей и Литрбол для чайников"
    $ current_action_content = None
    $ current_action_items = []
    if TavernHelpPage < (len(_help_pages) - 1):
        $ current_action_items.append(MenuItem("Читать дальше", Call("TavernHelpApply", "next")))
    else:
        $ current_action_items.append(MenuItem("Перечитать сначала", Call("TavernHelpApply", "restart")))
    if int(CheatMoneyGrab or 0) == 0 and money <= 100:
        $ current_action_items.append(MenuItem("Совсем разоряюсь, возьму ка я 150 мараведи из заначки", Call("TavernHelpApply", "stash_take")))
    elif int(CheatMoneyGrab or 0) == 0 and money > 100:
        $ current_action_items.append(MenuItem("Заначку пока лучше поберечь", Call("TavernHelpApply", "stash_wait")))
    elif int(CheatMoneyGrab or 0) == 1:
        $ current_action_items.append(MenuItem("Заначка уже пуста", Call("TavernHelpApply", "stash_empty")))
    $ current_action_items.append(MenuItem("Оторваться от чтения", Call("TavernHelpApply", "leave")))
    return


label TavernHelpTakeStash:
    $ _book = TavernMainBookObject
    if int(CheatMoneyGrab or 0) == 0 and money <= 100:
        $ CheatMoneyGrab = 1
        $ money += 150
        $ _book.state["stash_taken"] = 1
        $ _book.state["stash_amount"] = 0
        call stat
    return
