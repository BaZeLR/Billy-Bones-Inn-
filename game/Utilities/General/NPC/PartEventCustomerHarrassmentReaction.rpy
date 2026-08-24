# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# PartEventCustomerHarrassmentReaction location - converted from legacy script
label PartEventCustomerHarrassmentReaction(GirlNamePECHR, girl_run_away=0, girl_slapped=0, result="", _girl_info=None, _girl_corruption=0, _girl_name=""):
    $ result = '\n'
    $ _girl_info = people.get_info(GirlNamePECHR)
    $ _girl_corruption = int(getattr(_girl_info, "corruption", 0) or 0)
    $ _girl_name = people_display_name(GirlNamePECHR)
    if girl_run_away == 0:
        if _girl_corruption >= 50:
            if procedural_randint(1,12, key="procedural:Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy:procedural_randint:12:1") == 1:
                $ result += 'Вашим завсегдатаям очень понравилась такая податливость. '
                $ player.change_tavern_fame(1)
                if _girl_info is not None:
                    $ _girl_info.skills["waitress"] = min(70, int(_girl_info.skills.get("waitress", 0) or 0) + 1)
        else:
            if procedural_randint(1,25, key="procedural:Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy:procedural_randint:18:2") == 1:
                $ result += 'Ваших завсегдатаев устроило такое обслуживание. '
                $ player.change_tavern_fame(1)
                if _girl_info is not None:
                    $ _girl_info.skills["waitress"] = min(70, int(_girl_info.skills.get("waitress", 0) or 0) + 1)
            if procedural_randint(1,6, key="procedural:Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy:procedural_randint:23:3") == 1 and _girl_corruption < 7:
                $ result += '\n' + _girl_name + ' почуствовала себя чуть больше раскрепощенной.'
                if _girl_info is not None:
                    $ _girl_info.change_social(corruption_delta=1)
                    $ _girl_info.change_mana(-1, "harass_customer_pressure")
                    $ _girl_info.change_rebellion(1, "harass_customer_pressure")
    elif girl_run_away == 1 and girl_slapped > 0:
        if procedural_randint(1,2, key="procedural:Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy:procedural_randint:30:4") == 1:
            $ result += 'Неудачливому приставале пощечина понравилась мало. Бормоча себе под нос ругательства он в гневе выбежал из трактира. Будьте уверенны, что он не замедлит рассказать о произошедшем своим дружкам, выставя себя в выгодном свете.'
            $ player.change_tavern_fame(-1)
            if _girl_info is not None:
                $ _girl_info.skills["waitress"] = max(20, int(_girl_info.skills.get("waitress", 0) or 0) - 1)
        else:
            $ result += 'Хотя неудачливый приставала и получил по мордасам, но все-таки он стерпел обиду и спокойно закончил свою трапезу.'
        if procedural_randint(1,2, key="procedural:Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy:procedural_randint:37:5") == 1 and _girl_corruption > 0:
            $ result += '\n' + _girl_name + ', дав отпор охальнику, почуствовала себя более гордой и неприступной.'
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=-1)
                $ _girl_info.change_mana(1, "harass_rejected")
                $ _girl_info.change_rebellion(-1, "harass_rejected")
    elif girl_run_away == 1 and girl_slapped == 0:
        if procedural_randint(1,8, key="procedural:Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy:procedural_randint:44:6") == 1:
            $ result += 'Любителя распускать руки отказ, хотя и спокойный, судя по всему задел за живое, ущемив его нежную и ранимую гордость. Бормоча себе под нос ругательства он в гневе выбежал из трактира. Будьте уверенны, что он не замедлит рассказать о произошедшем своим дружкам, выставя себя в выгодном свете.'
            $ player.change_tavern_fame(-1)
            if _girl_info is not None:
                $ _girl_info.skills["waitress"] = max(20, int(_girl_info.skills.get("waitress", 0) or 0) - 1)
        else:
            $ result += 'Любитель распускать руки воспринял отказ как само собой разумеющееся и вернулся к трапезе.'
        if procedural_randint(1,10, key="procedural:Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy:procedural_randint:51:7") == 1 and _girl_corruption > 0:
            $ result += '\n' + _girl_name + ', дав отпор охальнику, почуствовала себя более гордой и неприступной.'
            if _girl_info is not None:
                $ _girl_info.change_social(corruption_delta=-1)
                $ _girl_info.change_mana(1, "harass_rejected")
                $ _girl_info.change_rebellion(-1, "harass_rejected")
    return result
