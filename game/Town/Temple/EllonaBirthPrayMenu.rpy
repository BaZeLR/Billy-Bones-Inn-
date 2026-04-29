# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# EllonaBirthPrayMenu location - converted from legacy script
label EllonaBirthPrayMenu:
    # Menu for praying to Ellona and the Graces during childbirth
    menu ellona_birth_pray:
        "Помолиться Эллоне" if money >= 10:
            $ money -= 10
            $ GraceBlessing[args[0]] = 1
            call SlutFriendsIncrease(GirlName, 20, 1, 1, 65, 1, 1)
            "\nОткуда-то издалека вы услышали удивленный возглас [RealName2[GirlName]]: 'Боль ушла!'\nЗатем зазвучал радостный голос Франчески: 'Богиня услышала наши молитвы!'"
            if args[0] == 0 and SumArray(GraceBlessing) >= 6 and (BlessedByEllona == 0 or CursedByEllona == 1):
                if CursedByEllona == 1:
                    "\nТут Эллона посмотрела на вас внимательней: 'Вижу мои дочурки наказали тебя. Они молоды и скоры на суждения. Ты ж я вижу чтишь меня, поэтому я тебя прощаю! Будь осторожнее в следующий раз.'\nВы почувствовали как чьи-то незримые пальчики умело начали массировать ваш член и мошонку. Под их прикосновениями он моментально восстал, оттопырив штаны. \nВ ушах у вас зазвенел серебристый смех: 'Теперь ты можешь опять облагодетельствовать свой игрущкой добрых девиц. Ступай!'\n\nВаша мужская сила вернулась к вам! "
                    $ CursedByEllona = 0
                    $ cancumdaily += CursedByEllonaReduce
                    $ CursedByEllonaDays = 0
                    $ CursedByEllonaReduce = 0
                else:
                    "\nТут Эллона посмотрела на вас с интересом: 'Вижу ты чтишь меня и моих дочерей. Такой благочестивый юноша достоин награды.' \nВы внезапно ощутили как ваш член очутился в чьем-то жарком ротике. Удивленно вы посмотрели вниз, но ваши штаны остались на вас и застегнутыми. Тем не менее вы ощущали, как кто-то вам делает минет, причем с просто потрясающей страстью и сноровкой. Долго продержаться вы не могли и не продержались, разрядившись густым потоком семени. Несмотря на то, что вы продолжали оставаться полностью одетым, кто-то невидимый с готовностью проглотил все, что вы накончали и даже облизал головку.\nЧудеса, однако, на это не закончились. Ваш опавший боец вдруг вновь воспрянул духом и стал подниматься. Незримая Эллона шепнула вам: 'Теперь ты отмечен моим благословением. Те, у кого отсосала богиня,  помнят об этом до конца своих дней. И до конца своих дней они несут мой дар!'\n\nЗА ВАШЕ БЛАГОЧЕСТИЕ ЭЛЛОНА ВОЗНАГРАДИЛА ВАС СВОИМ БЛАГОСЛОВЕНИЕМ: БОЖЕСТВЕННЫМ МИНЕТОМ. ТЕПЕРЬ ВЫ МОЖЕТЕ ЕЖЕДНЕВНО КОНЧАТЬ НА ОДИН РАЗ БОЛЬШЕ."
                    $ BlessedByEllona = 1
                    $ cancumdaily += 1
                    call PregnancyCheck('ellona', 'mouth', 1, 'Вы')
            else:
                "А вы сами почувствовали как вас наполняет неуловимое чувство благости и духовности."
            call stat
            $ GiveBirthTimer += 2
            call GiveBirthStep2
        "Помолиться Антее" if money >= 10:
            $ money -= 10
            if GirlName == 'liza' or GirlName == 'melissa' or GirlName == 'amanda':
                "Молодая и красивая девица нагуляла себе ребеночка? Такие девицы мне по нраву. Пусть боль уляжется."
                $ GraceBlessing[1] = 1
                call SlutFriendsIncrease(GirlName, 20, 1, 1, 65, 1, 1)
                call stat
                $ GiveBirthTimer += 2
                call GiveBirthStep2
            else:
                "Зачем ты побеспокоил меня зря, ничтожество?! Разве есть здесь молодуха, нуждающаяся в моей помощи?"
                call stat
                $ GiveBirthTimer += 2
                call GiveBirthStep2
        "Помолиться Фаене" if money >= 10:
            $ money -= 10
            if GirlName == 'liza' or GirlName == 'georgett':
                "Шлюха нагуляла пузо от клиента? Как же не помочь товарке по ремеслу? Пусть боль уляжется."
                $ GraceBlessing[2] = 1
                call SlutFriendsIncrease(GirlName, 20, 1, 1, 65, 1, 1)
                call stat
                $ GiveBirthTimer += 2
                call GiveBirthStep2
            else:
                "Зачем ты побеспокоил меня зря, ничтожество?! Я не вижу здесь шлюхи, которой бы потребовалась моя помощь!"
                call stat
                $ GiveBirthTimer += 2
                call GiveBirthStep2
        "Помолиться Аглае" if money >= 10:
            $ money -= 10
            "[RealName[GirlName]] рожает? Конечно я помогу, беременность священна! Пусть боль уляжется."
            $ GraceBlessing[3] = 1
            call SlutFriendsIncrease(GirlName, 20, 1, 1, 65, 1, 1)
            call stat
            $ GiveBirthTimer += 2
            call GiveBirthStep2
        "Помолиться Пасифее" if money >= 10:
            $ money -= 10
            if GirlName == 'inga':
                "Жених обрюхатил невесту не дожидаясь свадьбы? Благословенны те свадьбы и те пары, где невеста приходит в церковь на последних месяцах, или вовсе с толпой карапузов! Пусть боль уляжется."
                $ GraceBlessing[4] = 1
                call SlutFriendsIncrease(GirlName, 20, 1, 1, 65, 1, 1)
                call stat
                $ GiveBirthTimer += 2
                call GiveBirthStep2
            else:
                "Как ты посмел оторвать меня от любимого мужа и семьи, червь?! Я не вижу здесь ни страстной жены, ни влюбленной невесты!"
                call stat
                $ GiveBirthTimer += 2
                call GiveBirthStep2
        "Помолиться Талии" if money >= 10:
            $ money -= 10
            if sluttiness[GirlName] >= 60:
                "Я вижу здесь страстную женщину которую ее страсть ввела в положение. Да пребудет с ней мое благословение! Пусть боль уляжется."
                $ GraceBlessing[5] = 1
                call SlutFriendsIncrease(GirlName, 20, 1, 1, 65, 1, 1)
                call stat
                $ GiveBirthTimer += 2
                call GiveBirthStep2
            else:
                "Жалкий смертный, как ты посмел оторвать меня от моих игрушек?! Я не вижу здесь ни одной настоящей женщины, которой хотелось бы помочь, я вижу лишь одних стеснительных клуш, что краснеют при слове хуй!"
                call stat
                $ GiveBirthTimer += 2
                call GiveBirthStep2
    return
