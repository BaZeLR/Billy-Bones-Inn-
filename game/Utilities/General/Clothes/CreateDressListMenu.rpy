# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label CreateDressListMenu:
    return


label MaleDressShop:
label male_dress_shop:
    $ _md_items = []
    python:
        for _code in list(_gds_get_list("MaleDressCodes")):
            _code_s = str(_code or "").strip()
            if not _code_s:
                continue
            _name = str(_gds_get_dict("ShortDressName").get(_code_s, _code_s)).lower()
            _md_items.append(MenuItem("Осмотреть " + _name, Return(_code_s)))
        _md_items.append(MenuItem("Назад", Return("back")))
    call screen choice(_md_items, "Что посмотреть среди мужской одежды?")
    $ _md_choice = _return

    if _md_choice == "back" or str(_md_choice or "") == "":
        return

    $ _desc = str(_gds_get_dict("FullDressDesc").get(_md_choice, ""))
    $ _cost = _gds_dress_cost(_md_choice)
    '[_desc], обойдется он вам в [_cost] мараведи.'
    if player_state().appearance.has_dress(str(_md_choice)):
        'Впрочем, этот костюм у вас уже есть.'
    jump male_dress_shop


label FemaleDressShop:
label female_dress_shop:
    $ _fd_items = []
    python:
        for _code in list(_gds_get_list("FemaleDressCodes")):
            _code_s = str(_code or "").strip()
            if not _code_s or _code_s == "nightshirt":
                continue
            _name = str(_gds_get_dict("ShortDressName").get(_code_s, _code_s)).lower()
            _fd_items.append(MenuItem("Осмотреть " + _name, Return(_code_s)))
        _fd_items.append(MenuItem("Назад", Return("back")))
    call screen choice(_fd_items, "Что посмотреть среди женской одежды?")
    $ _fd_choice = _return

    if _fd_choice == "back" or str(_fd_choice or "") == "":
        return

    $ _desc = str(_gds_get_dict("FullDressDesc").get(_fd_choice, ""))
    $ _cost = _gds_dress_cost(_fd_choice)
    '[_desc], обойдется оно вам в [_cost] мараведи.'
    jump female_dress_shop
