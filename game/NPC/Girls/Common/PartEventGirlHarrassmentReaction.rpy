# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# PartEventGirlHarrassmentReaction location - converted from legacy script
label PartEventGirlHarrassmentReaction(GirlNamePEGHR, JobTypePEGHR, EyewitnessPEGHR=0):
    $ Result = ""
    $ GirlRunAway = 0
    $ GirlSlapped = 0
    $ _girl_info = getPersonInfo(GirlNamePEGHR)
    $ _girl_slut = int(getattr(_girl_info, "corruption", 0) or 0)
    $ _girl_friend = int(getattr(_girl_info, "rel", 0) or 0)
    $ _girl_name = RealName.get(GirlNamePEGHR, GirlNamePEGHR)
    $ _girl_name2 = RealName2.get(GirlNamePEGHR, GirlNamePEGHR)
    $ _girl_name3 = RealName3.get(GirlNamePEGHR, GirlNamePEGHR)
    $ _harass_instruction = _girl_info.harass_instruction() if _girl_info is not None else ""
    if YourReaction1 == 3:
        if JobTypePEGHR == 'cleaning':
            $ Result = 'Оттолкнув похотливые ручонки, вы отчитали охальника, указав ему, что уборщицы у вас предназначены для уборки, а не для развлечений тех охламонов, которые не умеют держать свои руки при себе.'
        else:
            $ Result = 'Оттолкнув похотливые ручонки, вы отчитали охальника, указав ему, что у вас официанток не лапают.'
        $ GirlRunAway = 1
        if _girl_slut <= 10:
            $ Result += f'\nА пунцовая как рак {_girl_name} не замедлила влепить ему смачную пощечину, от всех щедрот. '
            $ GirlSlapped = 1
            if _girl_friend < 5 and renpy.random.randint(1,2) == 1:
                $ Result += f'\nА потом, когда вы отошли в сторону, {_girl_name} поблагодарила вас за помощь.'
                $ _girl_info.change_social(friend_delta=1)
                $ _girl_info.change_mana(1, "harass_player_help")
                $ _girl_info.change_rebellion(-1, "harass_player_help")
        elif _girl_slut >= 60:
            $ Result += f'\nНо {_girl_name} вдруг неожиданно оборвала вас, сказав: "Стефан, душка, зачем же ты ругаешь такого приятного господина? Я совсем не в обиде!" - с этими словами ветреная {_girl_name} страстно, с язычком, поцеловала своего мнимого обидчика и пошла дальше по своим делам, призывно виляя бедрами. Вы остались стоять в оторопении.'
            $ GirlRunAway = 2
            if _girl_friend > 0 and renpy.random.randint(1,3) == 1:
                $ Result += f'\nПохоже, что ваша реакция не очень-то понравилась {_girl_name3}.'
                $ _girl_info.change_social(friend_delta=-1)
                $ _girl_info.change_mana(-1, "harass_blocked_wanted_attention")
                $ _girl_info.change_rebellion(1, "harass_blocked_wanted_attention")
        elif _girl_slut >= 30:
            $ Result += f'\nНо у вас осталось чувство, что {_girl_name} была вовсе не против, чтобы к ней приставали, и что ваше вмешательство было лишним.'
        else:
            $ Result += f'\nВо время всей этой лекции {_girl_name} стояла за вашей спиной и обиженно смотрела на незадачливого любителя распустить руки.'
            if _girl_friend < 5 and renpy.random.randint(1,5) == 1:
                $ Result += f'\nА потом, когда вы отошли в сторону, {_girl_name} поблагодарила вас за помощь.'
                $ _girl_info.change_social(friend_delta=1)
                $ _girl_info.change_mana(1, "harass_player_help")
                $ _girl_info.change_rebellion(-1, "harass_player_help")
        call HarassShowImage(GirlNamePEGHR, "tits", 0, EyewitnessPEGHR, JobTypePEGHR)
    elif YourReaction1 == 2:
        if (_harass_instruction == 'notallow' and _girl_slut < 30) or (_harass_instruction == '' and _girl_slut < 18):
            $ Result += f'{_girl_name} с трудом вырвалась из цепких объятий'
            $ GirlRunAway = 1
            if _girl_slut <= 10:
                $ Result += '. A вырвавшись, залепила охальнику звонкую пощечину и пошла по своим делам.'
                $ GirlSlapped = 1
            else:
                $ Result += ' и вернулась к работе.'
        elif (_harass_instruction == 'notallow' and _girl_slut < 45) or (_harass_instruction == '' and _girl_slut < 30):
            $ Result += f'{_girl_name} сделала слабую попытку вырваться, оглянулась, увидела что вы на нее с интересом смотрите, и решила что будь что будет.'
        elif strcomp(_harass_instruction, '^allow'):
            if _girl_slut < 18 and renpy.random.randint(1, 1 + max((15 - _girl_slut) // 6, 1)) == 1:
                $ Result += f'На личике {_girl_name2} отразилась гримаска страха. Казалось, что она сейчас вырвется и убежит. {_girl_name} обернулась, как бы ища совета или поддержки. И встретилась с вашим взглядом. Вы поняли, что увидя вас она вспомнила ваш совет. Хотя и с трудом, но все-таки {_girl_name} смогла перебороть себя и убегать не стала. '
            elif _girl_slut < 18:
                $ Result += f'На личике {_girl_name2} отразилась гримаска страха. Она посмотрела на вас но, судя по ее дальнейшим дествиям, либо не вспомнила что вы ей говорили, либо решила все равно поступить по своему. С визгом {_girl_name} вырвалась '
                if renpy.random.randint(1,5) == 1:
                    $ Result += '. A вырвавшись, залепила охальнику звонкую пощечину и припустила прочь.'
                    $ GirlSlapped = 1
                else:
                    $ Result += ' и вернулась к работе.'
                $ GirlRunAway = 1
            elif _girl_slut > 45:
                $ Result += f'{_girl_name} восприняла приставания не просто как должное, а с удовольствием и энтузиазмом, не сделав ни малейшей попытки вырваться.'
            else:
                $ Result += f'{_girl_name} сначала дернулась от неожиданности, но в целом реагировала спокойно. Работа уборщицей в вашем трактире приучила ее мириться с такими вещами.'
    else:
        if (_harass_instruction == 'notallow' and _girl_slut < 45) or (_harass_instruction == '' and _girl_slut < 30):
            $ Result += f'{_girl_name} с трудом вырвалась из цепких объятий'
            $ GirlRunAway = 1
            if _girl_slut <= 10:
                $ Result += '. A вырвавшись, залепила охальнику звонкую пощечину и пошла по своим делам.'
                $ GirlSlapped = 1
            else:
                $ Result += ' и вернулась к работе.'
        elif strcomp(_harass_instruction, '^allow'):
            if _girl_slut < 18 and renpy.random.randint(1, 1 + max((18 - _girl_slut) // 4, 1)) == 1:
                $ Result += f'На личике {_girl_name2} отразилась гримаска страха. Казалось, что она сейчас вырвется и убежит. Но все-таки {_girl_name} вспомнила ваш совет и с трудом смогла перебороть себя, не став убегать. '
            elif _girl_slut < 18:
                $ Result += f'На личике {_girl_name2} отразилась гримаска страха. Она и не вспомнила про ваши слова, немедленно вырвавшись из лап охальника с громким визгом. A вырвавшись,'
                if renpy.random.randint(1,5) == 1:
                    $ Result += ' залепила охальнику звонкую пощечину и припустила прочь.'
                    $ GirlSlapped = 1
                else:
                    $ Result += ' вернулась к работе.'
                $ GirlRunAway = 1
            elif _girl_slut > 45:
                $ Result += f'{_girl_name} восприняла приставания не просто как должное, а с удовольствием и энтузиазмом, не сделав ни малейшей попытки вырваться.'
            else:
                if JobTypePEGHR == 'cleaning':
                    $ Result += f'{_girl_name} сначала дернулась от неожиданности, но в целом реагировала спокойно. Работа уборщицей в вашем трактире приучила ее мириться с такими вещами.'
                else:
                    $ Result += f'{_girl_name} сначала дернулась от неожиданности, но в целом реагировала спокойно. Хорошая официантка на такое внимание не обращает.'
    return Result
# ...existing code...
