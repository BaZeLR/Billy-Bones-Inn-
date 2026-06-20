# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Amanda Sex Dance Street scene - converted from QSP to Ren'Py

label AmandaAfterDanceMC:
    $ GirlNameASDS = "amanda"
    $ Amanda.add_var_int("mc_dance_after_seen", 1)
    $ Amanda.set_var_int("mc_dance_last_day", dayspassed)
    $ Amanda.set_var_int("leftdances", 1)
    $ FridayDancesCount = 5
    vscene "images/market/LocFridayDance.jpg"
    "Музыка стихает, но Аманда не сразу отпускает вашу руку. Она смеется тише обычного и сама тянет вас прочь от света факелов."
    "За углом шум площади становится глухим. Аманда останавливается, будто хочет что-то сказать, но вместо слов только смотрит на вас и улыбается."
    menu:
        "Поцеловать ее":
            jump AmandaAfterDanceMCMakeOut
        "Проводить ее домой":
            jump AmandaAfterDanceMCWalkHome
        "Вернуться на площадь":
            jump AmandaAfterDanceMCReturn

label AmandaAfterDanceMCMakeOut:
    $ Amanda.add_var_int("mc_dance_makeout_seen", 1)
    $ Amanda.add_var_int("mc_dance_private_walks", 1)
    call ShowImage("amanda", "dance", "YouKiss")
    "Вы наклоняетесь к ней, и Аманда отвечает сразу, будто ждала именно этого. Поцелуй выходит долгим, неловким и слишком горячим для тесного переулка у рыночной площади."
    "Она прижимается ближе, потом вдруг отстраняется, поправляет платье и смеется, пытаясь скрыть смущение."
    "\"Все, Стефан. Если мы сейчас не остановимся, я потом сама себя не узнаю.\""
    $ Amanda.change_social(friend_delta=2, open_delta=1, corruption_delta=1)
    $ Amanda.change_mana(1, "friday_dance_makeout")
    menu:
        "Остановиться":
            "Вы еще немного стоите рядом в темноте, держась за руки, пока шум праздника окончательно не начинает стихать."
            jump AmandaAfterDanceMCFinish
        "Увести ее глубже в переулок" if int(Amanda.stats.get("sexacts", 0) or 0) > 0 or Amanda.var_int("suckyou", 0) == 1 or Amanda.corruption >= 35:
            $ Amanda.add_var_int("mc_dance_sex_seen", 1)
            $ Amanda.change_mana(1, "friday_dance_after_sex")
            jump AmandaSexDanceStreet

label AmandaAfterDanceMCWalkHome:
    $ Amanda.add_var_int("mc_dance_private_walks", 1)
    call ShowImage("amanda", "dance", "YouInvite1")
    "Вы не торопите ее. Просто идете рядом, пока огни площади остаются позади."
    "Аманда сначала молчит, потом начинает рассказывать о музыке, людях и о том, как странно было весь вечер чувствовать на себе ваш взгляд."
    "У дверей трактира она задерживается на миг и мягко сжимает вашу ладонь."
    "\"Спасибо. Сегодня было хорошо.\""
    $ Amanda.change_social(friend_delta=1, open_delta=1, corruption_delta=1)
    $ Amanda.change_mana(1, "friday_dance_walk_home")
    jump AmandaAfterDanceMCFinish

label AmandaAfterDanceMCReturn:
    call ShowImage("amanda", "dance", "wait1")
    "Вы отступаете, давая ей возможность первой решить, что делать дальше. Аманда смотрит на вас с удивлением, потом кивает."
    "\"Наверное, так и правда лучше. Но танец я запомню.\""
    $ Amanda.change_social(friend_delta=1, corruption_delta=1)
    jump AmandaAfterDanceMCFinish

label AmandaAfterDanceMCFinish:
    $ DanceStep = 0
    $ Amanda.set_var_int("albernowdances", 0)
    "Праздник для вас на сегодня закончился."
    return

label AmandaSexDanceStreet:
    $ GirlNameASDS = "amanda"
    "Продолжая танцевать, вы вдруг прошептали Аманде на ушко: \"Милая, а может прогуляемся немного?\"\n\"А почему бы и нет\", с улыбкой ответила вам она. Взявшись за руки вы пошли в лабиринт улочек и переулков. Увидя скрытую от глаз подворотню, вы, не сговариваясь, устремились туда."

    python:
        tmp_minet_or_full = 0
        if Amanda.stats.get("virginity", True) != True:
            # Not virgin, check conditions
            if Amanda.var_int("fuckyou", 0) and Amanda.corruption >= 35:
                tmp_minet_or_full = 1
            elif Amanda.corruption >= 40:
                tmp_minet_or_full = 1
            else:
                tmp_minet_or_full = 0
    
    if tmp_minet_or_full == 0:
        "Вдруг Аманда сказала: \"Только знаешь, Стефан, а вдруг нас кто здесь застукает? Я стесняюсь. Давай я тебе по быстрому отсосу, пока никто не пришел? Хорошо?\" и с этими словами ваша озорная подруга начала расстегивать ваши штаны.\nРешив, что спор может привлечь ненужное внимание вы не стали вступать с ней в дискуссию и указывать ей на очевидную бездоказательность ее позиции и слабость аргументов."
        call BeginPaidSexModule(GirlNameASDS, "StreetTavern")
        call IntAmandaSex("amanda", "street", "minet")
    else:
        call BeginPaidSexModule(GirlNameASDS, "StreetTavern")
        call IntAmandaSex("amanda", "street")
    
    "Вы находитесь в какой-то подворотне. Рядом с вами Аманда."
    
    if tmp_minet_or_full == 0:
        menu:
            "Закончить и выйти из переулка":
                call FinishPaidSexModule(GirlNameASDS, "StreetTavern")
    
    jump AmandaAfterDanceMCFinish
