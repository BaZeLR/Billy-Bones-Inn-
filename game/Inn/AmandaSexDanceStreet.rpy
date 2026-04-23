# Amanda Sex Dance Street scene - converted from QSP to Ren'Py

label AmandaSexDanceStreet:
    $ GirlNameASDS = "amanda"
    "Продолжая танцевать, вы вдруг прошептали Аманде на ушко: \"Милая, а может прогуляемся немного?\"\n\"А почему бы и нет\", с улыбкой ответила вам она. Взявшись за руки вы пошли в лабиринт улочек и переулков. Увидя скрытую от глаз подворотню, вы, не сговариваясь, устремились туда."

    python:
        tmp_minet_or_full = 0
        if virginity.get('amanda', 1) != 1:
            # Not virgin, check conditions
            if AmandaVar.get('fuckyou', 0) and sluttiness.get('amanda', 0) >= 35:
                tmp_minet_or_full = 1
            elif sluttiness.get('amanda', 0) >= 40:
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
    
    return
