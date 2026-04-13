label IntRobinTalk():
    "Что сделать?"  
    while True:
        menu:
            
                "Посмотреть на разбойников":
                    $ renpy.call('clean_screen_overflow')
                    $ RobinTmpDesc = 'Робин Гуд, ' if RobinVar.get('KnowHim', 0) else ''
                    "Мужики в трико, вооруженные как луками, так и самыми разными колюще-режущими предметами. Ими командует [RobinTmpDesc]здоровенный негр с золотой цепью на шее. На голове у него капюшон, частично скрывающий лицо."
                    $ renpy.call('show_image_seq', 'Robin', '', 'portrait', 2)
                    jump IntRobinTalkEnd
                "Да кто вы вообще такие?" if RobinVar.get('KnowHim', 0) == 0:
                    $ renpy.call('clean_screen_overflow')
                    "Йо, чувак, я же все изложил. Мои браза - доведенные до отчаяния лесорубы. А я Робин, Робин из Титли... (full text)"
                    $ RobinVar['KnowHim'] = 1
                    $ RobbersHeadNameTmp = 'Робин Гуд' if RobinVar['KnowHim'] else 'предводитель'
                    jump IntRobinTalkEnd
                "А если вы простые лесорубы, то откуда у вас оружие?" if RobinVar.get('KnowHim', 0) == 1 and RobinVar.get('KnowWeapon', 0) == 0:
                    $ renpy.call('clean_screen_overflow')
                    "Йо , чувак, ты меня прикалываешь. Как откуда? Купили конечно... (full text)"
                    $ RobinVar['KnowWeapon'] = 1
                    jump IntRobinTalkEnd
                "Поинтересоваться что это за место" if RobinVar.get('KnowHim', 0) == 1 and RobinVar.get('KnowPlace', 0) == 0:
                    $ renpy.call('clean_screen_overflow')
                    "Йо, чувак, это же южный, тьфу, шервудский центра..., тьфу лес... (full text)"
                    $ RobinVar['KnowPlace'] = 1
                    jump IntRobinTalkEnd
                "Узнать, в чем состоят их неприятности" if RobinVar.get('KnowHim', 0) == 1 and RobinVar.get('KnowComplaint', 0) == 0:
                    $ renpy.call('clean_screen_overflow')
                    "Хей, мэн! Как это в чем? Ты не видишь?... (full text)"
                    $ RobinVar['KnowComplaint'] = 1
                    jump IntRobinTalkEnd
                "А может, договоримся?" if RobinVar.get('Negotiate', 0) == 0 and RobinVar.get('RobbedNum', 0) > 0:
                    $ renpy.call('clean_screen_overflow')
                    "Ребят, а может договоримся? Я, конечно, на благородные цели всегда пожертвовать готов... (full text)"
                    $ RobinVar['Negotiate'] = RobinVar.get('Negotiate', 0) + 1
                    jump IntRobinTalkEnd
                "А может все таки договоримся?" if RobinVar.get('Negotiate', 0) == 2 and RobinVar.get('RobbedNum', 0) > 0:
                    $ renpy.call('clean_screen_overflow')
                    "А может все таки договоримся?... (full text)"
                    $ RobinVar['Negotiate'] = RobinVar.get('Negotiate', 0) + 1
                    jump IntRobinTalkEnd
                "Уйти":
                    jump IntRobinTalkEnd
label IntRobinTalkEnd:
    return
