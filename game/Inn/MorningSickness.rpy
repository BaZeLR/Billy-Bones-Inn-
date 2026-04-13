label MorningSickness(girl_name):
    python:
        import random
        CumInsideLastDays = cuminside.get(girl_name, 0)
        
        if pregnancy.get(girl_name, 0) > 14:
            Zaderzhka = pregnancy[girl_name] - 14
        elif pregnancy.get(girl_name, 0) > 0:
            Zaderzhka = 0
        else:
            Zaderzhka = 0
            if random.randint(1,3) == 1:
                Zaderzhka = random.randint(1,20)
                
        ZaletOpinion = 0
        if kids.get(girl_name, 0) > 0:
            if CumInsideLastDays > 2 + random.randint(1,8):
                if Zaderzhka == 0:
                    ZaletOpinion = 1
                elif Zaderzhka >= 3 + random.randint(1,5):
                    ZaletOpinion = 3
                else:
                    ZaletOpinion = 2
            elif CumInsideLastDays == 0:
                if Zaderzhka == 0:
                    ZaletOpinion = 0
                else:
                    ZaletOpinion = 1
            else:
                if Zaderzhka == 0:
                    ZaletOpinion = 0
                elif Zaderzhka >= 10 + random.randint(1,8):
                    ZaletOpinion = 3
                elif Zaderzhka >= 8:
                    ZaletOpinion = 2
                else:
                    ZaletOpinion = 1
        else:
            if CumInsideLastDays > 6 + random.randint(3,12):
                if Zaderzhka < 5:
                    ZaletOpinion = 0
                elif Zaderzhka >= 10 + random.randint(2,10):
                    ZaletOpinion = 2
                else:
                    ZaletOpinion = 1
            elif cuminside.get(girl_name, 0) == 0:
                ZaletOpinion = 0
            elif CumInsideLastDays == 0:
                if Zaderzhka < 7:
                    ZaletOpinion = 0
                else:
                    ZaletOpinion = 1
            else:
                if Zaderzhka >= 10 + random.randint(2,10):
                    ZaletOpinion = 1
                else:
                    ZaletOpinion = 0
    
    # Access RealName safely with a default
    $ girl_display_name = RealName.get(girl_name, girl_name)
    "Вы мирно шли по своим делам, когда вдруг вам навстречу, зажав рот руками, пробежала бледная [girl_display_name]. Даже не заметив вас, она ломанулась куда-то дальше, скорее всего на свежий воздух."
    
    call girls_desc(girl_name)
    
    "Что делать?"
    
    menu:
        "Проверить, что это с ней":
            $ girl_display_name = RealName.get(girl_name, girl_name)
            "Немного обеспокоившись, вы последовали за ней. Далеко ходить не пришлось: как только [girl_display_name] выскочила за порог, ее тут же стошнило в ближайшую канаву. Вытерев рот платком она пошла обратно и тут увидела вас. 'Стефан, ты чего это за мной следишь?' возмутилась она. 'Любопытство сгубило кошку, знаешь такое? Ты бы еще в уборной дырку бы проковырял! Не видишь что ли, подташнивает меня слегка.'"
            call morning_sickness_step2(girl_name, ZaletOpinion, Zaderzhka, CumInsideLastDays)
            return
            
        "Бросилась - значит надо ей":
            $ girl_display_name = RealName.get(girl_name, girl_name)
            "Всего через несколько минут [girl_display_name] вернулась. Здоровый оттенок лица вернулся к ней, хотя некоторая бледность сохраялась. 'Чего-й то, Стефанчик, меня стошнило слегка,' поделилась она с вами."
            call morning_sickness_step2(girl_name, ZaletOpinion, Zaderzhka, CumInsideLastDays)
            return

label morning_sickness_step2(girl_name, ZaletOpinion, Zaderzhka, CumInsideLastDays):
    python:
        # Process the morning sickness scenario based on parameters
        girl_display_name = RealName.get(girl_name, girl_name)
    
    "Что сказать?"
    
    menu:
        "Может, беременна?":
            python:
                # Logic for pregnancy suspicion based on ZaletOpinion
                if ZaletOpinion == 0:
                    response = f"'Да что ты, Стефан!' смеется {girl_display_name}. 'Откуда мне быть беременной? Просто желудок барахлит немного.'"
                elif ZaletOpinion == 1:
                    response = f"'{girl_display_name} задумчиво смотрит на вас. 'А знаешь... может и правда. Надо будет внимательнее за собой понаблюдать.'"
                elif ZaletOpinion == 2:
                    response = f"'{girl_display_name} бледнеет еще больше. 'Боже мой... а ведь и правда может быть. Уже довольно давно у меня... того... не было.'"
                else:  # ZaletOpinion == 3
                    response = f"'{girl_display_name} опускает глаза. 'Я... я сама об этом думала. Скорее всего так и есть. Что же теперь делать?'"
                renpy.say(None, response)
            return
            
        "Наверное просто съела что-то не то":
            python:
                # Logic for food poisoning excuse
                response = f"'Да, наверное ты прав,' соглашается {girl_display_name}. 'Вчера ела что-то странное на рынке. Надо быть осторожнее с едой.'"
                renpy.say(None, response)
            return
    
    return
