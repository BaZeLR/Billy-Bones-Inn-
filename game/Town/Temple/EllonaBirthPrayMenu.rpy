# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label EllonaBirthPrayMenu(girl_name=""):
    menu ellona_birth_pray:
        "Помолиться Эллоне" if player.economy.money >= 10:
            $ player.spend_money(10)
            $ player.intimacy.grant_ellona_grace(0)
            call SlutFriendsIncrease(girl_name, 20, 1, 1, 65, 1, 1)
            "\nОткуда-то издалека вы услышали удивленный возглас [people_name(girl_name, 'genitive')]: 'Боль ушла!'\nЗатем зазвучал радостный голос Франчески: 'Богиня услышала наши молитвы!'"
            if sum(player.intimacy.ellona_grace_blessings) >= 6 and (not player.intimacy.ellona_blessed or player.intimacy.ellona_cursed):
                if player.intimacy.ellona_cursed:
                    "\nТут Эллона посмотрела на вас внимательней: 'Вижу мои дочурки наказали тебя. Они молоды и скоры на суждения. Ты ж я вижу чтишь меня, поэтому я тебя прощаю! Будь осторожнее в следующий раз.'\nВы почувствовали как чьи-то незримые пальчики умело начали массировать ваш член и мошонку. Под их прикосновениями он моментально восстал, оттопырив штаны. \nВ ушах у вас зазвенел серебристый смех: 'Теперь ты можешь опять облагодетельствовать свой игрущкой добрых девиц. Ступай!'\n\nВаша мужская сила вернулась к вам! "
                    $ player.intimacy.lift_ellona_curse()
                else:
                    "\nТут Эллона посмотрела на вас с интересом: 'Вижу ты чтишь меня и моих дочерей. Такой благочестивый юноша достоин награды.' \nВы внезапно ощутили как ваш член очутился в чьем-то жарком ротике. Удивленно вы посмотрели вниз, но ваши штаны остались на вас и застегнутыми. Тем не менее вы ощущали, как кто-то вам делает минет, причем с просто потрясающей страстью и сноровкой. Долго продержаться вы не могли и не продержались, разрядившись густым потоком семени. Несмотря на то, что вы продолжали оставаться полностью одетым, кто-то невидимый с готовностью проглотил все, что вы накончали и даже облизал головку.\nЧудеса, однако, на это не закончились. Ваш опавший боец вдруг вновь воспрянул духом и стал подниматься. Незримая Эллона шепнула вам: 'Теперь ты отмечен моим благословением. Те, у кого отсосала богиня,  помнят об этом до конца своих дней. И до конца своих дней они несут мой дар!'\n\nЗА ВАШЕ БЛАГОЧЕСТИЕ ЭЛЛОНА ВОЗНАГРАДИЛА ВАС СВОИМ БЛАГОСЛОВЕНИЕМ: БОЖЕСТВЕННЫМ МИНЕТОМ. ТЕПЕРЬ ВЫ МОЖЕТЕ ЕЖЕДНЕВНО КОНЧАТЬ НА ОДИН РАЗ БОЛЬШЕ."
                    $ player.intimacy.grant_ellona_blessing()
                    call PregnancyCheck('ellona', 'mouth', 1, 'Вы')
            else:
                "А вы сами почувствовали как вас наполняет неуловимое чувство благости и духовности."
            call stat
        "Помолиться Антее" if player.economy.money >= 10:
            $ player.spend_money(10)
            if girl_name == 'liza' or girl_name == 'melissa' or girl_name == 'amanda':
                "Молодая и красивая девица нагуляла себе ребеночка? Такие девицы мне по нраву. Пусть боль уляжется."
                $ player.intimacy.grant_ellona_grace(1)
                call SlutFriendsIncrease(girl_name, 20, 1, 1, 65, 1, 1)
                call stat
            else:
                "Зачем ты побеспокоил меня зря, ничтожество?! Разве есть здесь молодуха, нуждающаяся в моей помощи?"
                call EllonaBirthPrayerFailure
                call stat
        "Помолиться Фаене" if player.economy.money >= 10:
            $ player.spend_money(10)
            if girl_name == 'liza' or girl_name == 'georgett':
                "Шлюха нагуляла пузо от клиента? Как же не помочь товарке по ремеслу? Пусть боль уляжется."
                $ player.intimacy.grant_ellona_grace(2)
                call SlutFriendsIncrease(girl_name, 20, 1, 1, 65, 1, 1)
                call stat
            else:
                "Зачем ты побеспокоил меня зря, ничтожество?! Я не вижу здесь шлюхи, которой бы потребовалась моя помощь!"
                call EllonaBirthPrayerFailure
                call stat
        "Помолиться Аглае" if player.economy.money >= 10:
            $ player.spend_money(10)
            "[people_display_name(girl_name)] рожает? Конечно я помогу, беременность священна! Пусть боль уляжется."
            $ player.intimacy.grant_ellona_grace(3)
            call SlutFriendsIncrease(girl_name, 20, 1, 1, 65, 1, 1)
            call stat
        "Помолиться Пасифее" if player.economy.money >= 10:
            $ player.spend_money(10)
            if girl_name == 'inga':
                "Жених обрюхатил невесту не дожидаясь свадьбы? Благословенны те свадьбы и те пары, где невеста приходит в церковь на последних месяцах, или вовсе с толпой карапузов! Пусть боль уляжется."
                $ player.intimacy.grant_ellona_grace(4)
                call SlutFriendsIncrease(girl_name, 20, 1, 1, 65, 1, 1)
                call stat
            else:
                "Как ты посмел оторвать меня от любимого мужа и семьи, червь?! Я не вижу здесь ни страстной жены, ни влюбленной невесты!"
                call EllonaBirthPrayerFailure
                call stat
        "Помолиться Талии" if player.economy.money >= 10:
            $ player.spend_money(10)
            if people.get_info(girl_name).corruption >= 60:
                "Я вижу здесь страстную женщину которую ее страсть ввела в положение. Да пребудет с ней мое благословение! Пусть боль уляжется."
                $ player.intimacy.grant_ellona_grace(5)
                call SlutFriendsIncrease(girl_name, 20, 1, 1, 65, 1, 1)
                call stat
            else:
                "Жалкий смертный, как ты посмел оторвать меня от моих игрушек?! Я не вижу здесь ни одной настоящей женщины, которой хотелось бы помочь, я вижу лишь одних стеснительных клуш, что краснеют при слове хуй!"
                call EllonaBirthPrayerFailure
                call stat
    return 2


label EllonaBirthPrayerFailure:
    if player.intimacy.ellona_cursed:
        '"Вижу, что ты уже наказан, смертный, за свою дерзость и непочтительность. И все равно ты решился на новую дерзость. Помучайся еще недельку, коли первый урок не пошел тебе впрок," продолжал греметь у вас в ушах рассерженный голос.'
        $ player.intimacy.extend_ellona_curse(7)
    elif procedural_randint(1, 3, "ellona_bad_prayer_%s" % current_game_day()) == 1:
        '"Как ты посмел потревожить меня, могущественную Грацию, без серьезного повода?! Отберу-ка я у тебя твою игрушку, что между ног болтается — на пару недель. Тебе это будет уроком богобоязненности и почтения."'
        "Видение начало затуманиваться, а вы с ужасом ощутили, что теперь ваш член не подымут ласки и сотни красавиц."
        $ player.intimacy.apply_ellona_curse(14)
    else:
        '"Надо бы мне было тебя примерно наказать, смертный, чтобы ты знал, как тревожить меня зазря. Но на этот раз я тебя прощу. А в следующий раз думай, прежде чем звать меня без причины!"'
        "Видение начало затуманиваться."
    return
