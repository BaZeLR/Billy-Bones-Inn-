# PartEventCustomerHarrassmentReaction location - converted from legacy script
label PartEventCustomerHarrassmentReaction(GirlNamePECHR):
    $ Result = '\n'
    if GirlRunAway == 0:
        if sluttiness.get(GirlNamePECHR, 0) >= 50:
            if renpy.random.randint(1,12) == 1:
                $ Result += 'Вашим завсегдатаям очень понравилась такая податливость. '
                $ tavernfame += 1
                $ waitress_val = waitress.get(GirlNamePECHR, 0)
                if waitress_val < 70:
                    $ waitress[GirlNamePECHR] = waitress_val + 1
        else:
            if renpy.random.randint(1,25) == 1:
                $ Result += 'Ваших завсегдатаев устроило такое обслуживание. '
                $ tavernfame += 1
                $ waitress_val = waitress.get(GirlNamePECHR, 0)
                if waitress_val < 70:
                    $ waitress[GirlNamePECHR] = waitress_val + 1
            if renpy.random.randint(1,6) == 1 and sluttiness.get(GirlNamePECHR, 0) < 7:
                $ Result += '\n' + RealName.get(GirlNamePECHR, GirlNamePECHR) + ' почуствовала себя чуть больше раскрепощенной.'
                $ sluttiness[GirlNamePECHR] = sluttiness.get(GirlNamePECHR, 0) + 1
    elif GirlRunAway == 1 and GirlSlapped > 0:
        if renpy.random.randint(1,2) == 1:
            $ Result += 'Неудачливому приставале пощечина понравилась мало. Бормоча себе под нос ругательства он в гневе выбежал из трактира. Будьте уверенны, что он не замедлит рассказать о произошедшем своим дружкам, выставя себя в выгодном свете.'
            $ tavernfame -= 1
            $ waitress_val = waitress.get(GirlNamePECHR, 0)
            if waitress_val >= 20:
                $ waitress[GirlNamePECHR] = waitress_val - 1
        else:
            $ Result += 'Хотя неудачливый приставала и получил по мордасам, но все-таки он стерпел обиду и спокойно закончил свою трапезу.'
        $ slut_val = sluttiness.get(GirlNamePECHR, 0)
        if renpy.random.randint(1,2) == 1 and slut_val > 0:
            $ Result += '\n' + RealName.get(GirlNamePECHR, GirlNamePECHR) + ', дав отпор охальнику, почуствовала себя более гордой и неприступной.'
            $ sluttiness[GirlNamePECHR] = slut_val - 1
    elif GirlRunAway == 1 and GirlSlapped == 0:
        if renpy.random.randint(1,8) == 1:
            $ Result += 'Любителя распускать руки отказ, хотя и спокойный, судя по всему задел за живое, ущемив его нежную и ранимую гордость. Бормоча себе под нос ругательства он в гневе выбежал из трактира. Будьте уверенны, что он не замедлит рассказать о произошедшем своим дружкам, выставя себя в выгодном свете.'
            $ tavernfame -= 1
            $ waitress_val = waitress.get(GirlNamePECHR, 0)
            if waitress_val >= 20:
                $ waitress[GirlNamePECHR] = waitress_val - 1
        else:
            $ Result += 'Любитель распускать руки воспринял отказ как само собой разумеющееся и вернулся к трапезе.'
        $ slut_val = sluttiness.get(GirlNamePECHR, 0)
        if renpy.random.randint(1,10) == 1 and slut_val > 0:
            $ Result += '\n' + RealName.get(GirlNamePECHR, GirlNamePECHR) + ', дав отпор охальнику, почуствовала себя более гордой и неприступной.'
            $ sluttiness[GirlNamePECHR] = slut_val - 1
    return Result
