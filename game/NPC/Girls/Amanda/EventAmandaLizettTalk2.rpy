# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label EventAmandaLizettTalk2(eyewitness=0, result="", _amanda_liza_row=None, _amanda_liza_reaction_values=(), _amanda_liza_definite_accept=0, _amanda_liza_friend_limit=0, _amanda_liza_slut_limit=0, _amanda_liza_friend_value=0, _amanda_liza_believe_friend=0):
    $ _amanda_liza_row = get_random_amanda_liza_talk_row()
    if _amanda_liza_row:
        $ result = str(_amanda_liza_row["Phrase"] or "").replace("<br><br>", "\n\n").replace("<br>", "\n").replace("<<Amanda.data.age_years()>>", str(Amanda.data.age_years()))
        $ _amanda_liza_reaction_values = tuple(_amanda_liza_row.get("Reaction", ()))
        if _amanda_liza_reaction_values:
            $ _amanda_liza_definite_accept = int(_amanda_liza_reaction_values[0] or 0)
            $ _amanda_liza_friend_limit = int(_amanda_liza_reaction_values[1] or 0)
            $ _amanda_liza_slut_limit = int(_amanda_liza_reaction_values[2] or 0)
            $ _amanda_liza_friend_value = Amanda.var_int("lizafriends", 0)
            $ _amanda_liza_believe_friend = 0
            if _amanda_liza_friend_value > 0:
                if procedural_randint(1, max(2, int(_amanda_liza_friend_limit / _amanda_liza_friend_value)), key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy:procedural_randint:17:1") == 1:
                    $ _amanda_liza_believe_friend = 1
            if Amanda.corruption >= _amanda_liza_definite_accept or procedural_randint(1, 5, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy:procedural_randint:19:2") <= 3 or _amanda_liza_believe_friend:
                $ result += "\n%s внимательно слушает свою собеседницу, впитывая информацию." % people_display_name("amanda")
                if _amanda_liza_friend_value < _amanda_liza_friend_limit and procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy:procedural_randint:21:3") == 1:
                    $ Amanda.add_var_int("lizafriends", 1)
                    $ result += "\nПохоже, %s и %s сдружились еще больше!" % (people_display_name("amanda"), people_display_name("liza"))
                if Amanda.corruption < _amanda_liza_slut_limit and procedural_randint(1, 2, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy:procedural_randint:24:4") == 1:
                    $ Amanda.change_social(corruption_delta=1)
                    $ result += "\nВам показалось, что после этого разговора %s почуствовала себя чуть больше раскрепощенной." % people_display_name("amanda")
            else:
                $ result += '\n"Да врешь ты все!" воскликнула %s и пошла по своим делам, даже не удосужившись попрощаться.' % people_display_name("amanda")
                if _amanda_liza_friend_value > (_amanda_liza_friend_limit / 4) and procedural_randint(1, 5, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy:procedural_randint:29:5") == 1:
                    $ Amanda.add_var_int("lizafriends", -1)
                    $ result += "\nПохоже, %s и %s малость поссорились!" % (people_display_name("amanda"), people_display_name("liza"))
                if Amanda.corruption > (_amanda_liza_slut_limit / 4) and Amanda.corruption > (_amanda_liza_slut_limit + 15) and procedural_randint(1, 5, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy:procedural_randint:32:6") == 1:
                    $ Amanda.change_social(corruption_delta=-1)
                    $ result += "\nВам показалось, что после этого разговора %s почуствовала себя более гордой и неприступной." % people_display_name("amanda")
    else:
        $ result = ""

    if eyewitness > 0:
        $ result += "\n\nПосле разговора Аманда с Лизеттой разошлись. Намеренны ли вы что-то сказать проходящей мимо Аманде?"
        "[result]"
        menu:
            "Строго наругать Аманду за то, та болтает с Лизеттой" if Amanda.var_int("prohibitliza", 0) > 0:
                $ Amanda.set_var_int("prohibitliza", 2)
                "Вы поймали проходящую мимо Аманду и строго ее отчитали за то, что она болтала с Лизеттой несмотря на запрет. Аманда расплакалась и убежала в слезах."
                $ Amanda.apply_social_chance(3, 1, -1, 0, 0, 0, "liza_talk_scold")
            "Сказать Аманде, чтобы не болтала с Лизеттой" if Amanda.var_int("prohibitliza", 0) == 0:
                $ Amanda.set_var_int("prohibitliza", 1)
                "Вы поймали проходящую мимо Аманду и сказали ей, чтобы она не болтала с Лизеттой, так как та распущенная девчонка и хорошему не научит. Аманда выслушала вас и пообещала с Лизеттой не говорить."
            "Сказать Аманде, что вы погорячились, когда запретили ей говорить с Лизеттой" if Amanda.var_int("prohibitliza", 0) > 0:
                $ Amanda.set_var_int("prohibitliza", 0)
                "Вы поймали проходящую мимо Аманду и сказали ей, что погорячились, вы не хотите на нее давить и она имеет полное право говорить с кем хочет. Аманда поблагодарила вас за доверие и пошла по своим делам."
                if Amanda.rel < 5 and procedural_randint(1, 4, key="procedural:NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy:procedural_randint:67:7") == 1:
                    "Ей очень понравилось, что вы ей так доверяете."
                    $ Amanda.apply_social_chance(6, 1, 1, 0, 0, 0, "liza_talk_trust")
            "Вернуться к своим делам":
                pass
        return ""

    return result
