label MomDressComplaint(girl_name):
    python:
        GirlSillyName = 'Амандочк' if girl_name == 'amanda' else 'Меллисочк'
        girl_var_name = "{}Var".format(girl_name)
        girl_var = getattr(renpy.store, girl_var_name, None)
        if not isinstance(girl_var, dict):
            girl_var = {}
            setattr(renpy.store, girl_var_name, girl_var)
        TalkedBeforeTmp = girl_var.get('MomDressComplaint', 0)
        girl_var['MomDressComplaint'] = TalkedBeforeTmp + 1
        KidsOrPregTmp = 0
        if pregnancy.get(girl_name, 0) > 150:
            KidsOrPregTmp = 1
        if kids.get(girl_name, 0) > 0:
            KidsOrPregTmp = 2
    if sluttiness.get('sandra', 0) < 50:
        "Вы мирно и спокойно шли по своим делам, когда вас вдруг остановила ваша матушка: 'Стефан, мне надо с тобой поговорить.'... (full text and menu as in original)"
        # ... Implement all menu options and logic as in the original, using Ren'Py menus and python blocks ...
        # For each branch, use call statements for 'slut_friends_increase', 'girls_desc', etc.
        # Use Ren'Py's random and variable handling for all conditions
    else:
        "Вы шли себе по своим делам, и пересеклись с вашей матушкой. ... (full text and menu as in original)"
        # ... Implement all menu options and logic as in the original, using Ren'Py menus and python blocks ...
    return
