# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# PartEventCustomerHarrassmentReaction location - converted from legacy script
label PartEventCustomerHarrassmentReaction(GirlNamePECHR):
    $ Result = '\n'
    $ _girl_info = getPersonInfo(GirlNamePECHR)
    $ _girl_corruption = int(getattr(_girl_info, "corruption", 0) or 0)
    $ _girl_name = getattr(getattr(_girl_info, "data", None), "fullname", "") or RealName.get(GirlNamePECHR, GirlNamePECHR)
    if GirlRunAway == 0:
        if _girl_corruption >= 50:
            if renpy.random.randint(1,12) == 1:
                $ Result += 'Вашим завсегдатаям очень понравилась такая податливость. '
                $ player.change_tavern_fame(1)
                if _girl_info is not None:
                    $ _girl_info.skills["waitress"] = min(70, int(_girl_info.skills.get("waitress", 0) or 0) + 1)
        else:
            if renpy.random.randint(1,25) == 1:
                $ Result += 'Ваших завсегдатаев устроило такое обслуживание. '
                $ player.change_tavern_fame(1)
                if _girl_info is not None:
                    $ _girl_info.skills["waitress"] = min(70, int(_girl_info.skills.get("waitress", 0) or 0) + 1)
            if renpy.random.randint(1,6) == 1 and _girl_corruption < 7:
                $ Result += '\n' + _girl_name + ' почуствовала себя чуть больше раскрепощенной.'
                if _girl_info is not None:
                    $ _girl_info.change_social(corruption_delta=1)
                    $ _girl_info.change_mana(-1, "harass_customer_pressure")
                    $ _girl_info.change_rebellion(1, "harass_customer_pressure")
    elif GirlRunAway == 1 and GirlSlapped > 0:
        if renpy.random.randint(1,2) == 1:
            $ Result += 'Неудачливому приставале пощечина понравилась мало. Бормоча себе под нос ругательства он в гневе выбежал из трактира. Будьте уверенны, что он не замедлит рассказать о произошедшем своим дружкам, выставя себя в выгодном свете.'
            $ player.change_tavern_fame(-1)
            if _girl_info is not None:
                $ _girl_info.skills["waitress"] = max(20, int(_girl_info.skills.get("waitress", 0) or 0) - 1)
        else:
            $ Result += 'Хотя неудачливый приставала и получил по мордасам, но все-таки он стерпел обиду и спокойно закончил свою трапезу.'
        if renpy.random.randint(1,2) == 1 and _girl_corruption > 0:
            $ Result += '\n' + _girl_name + ', дав отпор охальнику, почуствовала себя более гордой и неприступной.'
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=-1)
                $ _girl_info.change_mana(1, "harass_rejected")
                $ _girl_info.change_rebellion(-1, "harass_rejected")
    elif GirlRunAway == 1 and GirlSlapped == 0:
        if renpy.random.randint(1,8) == 1:
            $ Result += 'Любителя распускать руки отказ, хотя и спокойный, судя по всему задел за живое, ущемив его нежную и ранимую гордость. Бормоча себе под нос ругательства он в гневе выбежал из трактира. Будьте уверенны, что он не замедлит рассказать о произошедшем своим дружкам, выставя себя в выгодном свете.'
            $ player.change_tavern_fame(-1)
            if _girl_info is not None:
                $ _girl_info.skills["waitress"] = max(20, int(_girl_info.skills.get("waitress", 0) or 0) - 1)
        else:
            $ Result += 'Любитель распускать руки воспринял отказ как само собой разумеющееся и вернулся к трапезе.'
        if renpy.random.randint(1,10) == 1 and _girl_corruption > 0:
            $ Result += '\n' + _girl_name + ', дав отпор охальнику, почуствовала себя более гордой и неприступной.'
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=-1)
                $ _girl_info.change_mana(1, "harass_rejected")
                $ _girl_info.change_rebellion(-1, "harass_rejected")
    return Result
