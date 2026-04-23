label GirlSuggestDressFunc(GirlName="", DressToBuy="", ShowOffLevel=-1, DressBuyIsRelative=-1):
    if str(GirlName or "") == "" or str(DressToBuy or "") == "":
        return

    $ _gds_ensure_stats(GirlName)
    $ _gds_ensure_stats("irma")

    if ShowOffLevel < 0:
        $ ShowOffLevel = _gds_showoff_level(GirlName)
    if DressBuyIsRelative < 0:
        $ DressBuyIsRelative = _gds_relative_type(GirlName)

    $ _rn = _gds_name("RealName", GirlName)
    $ _rn2 = _gds_name("RealName2", GirlName)
    $ _rn3 = _gds_name("RealName3", GirlName)

    $ GirlDressBlock = 1

    menu:
        "Подождать, пока Ирма снимет мерку":
            'Что ж, мерка так мерка. [_rn] взяла образец и пошла за занавеску, Ирма поспешила за ней с полным набором булавок, мелков и мерных веревочек.'
            call GirlDressBuyWaitPay(GirlName, DressToBuy)

        "Пройти вместе с девушками за занавеску":
            call CleanScreenOverflow(5)
            '[_rn] взяла образец и пошла за занавеску. Ирма собрала свои булавки, мелки, мерные веревочки и поспешила за ней. Вы, в свою очередь, подумали, что сидеть в одиночестве будет скучновато, и решили присоединиться к их компании.'
            'По хозяйски отодвинув ширмочку, вы увидели Ирму с булавками в зубах и веревкой в руках, а напротив нее стояла уже начавшая раздеваться [_rn].'
            if str(_gds_get_dict("bra").get(GirlName, "") or "") != "":
                'Шнуровка верха платья уже была распущена, открыв вам ее груди, прикрытые, впрочем, лифом.'
            else:
                'Шнуровка верха платья уже была распущена, открыв вам ее голые груди с торчащими от холода сосочками.'

            if ShowOffLevel >= 2:
                '"Так-так-так, Стефанчик, посмотреть, значит, хочешь. Какой ты любопытный!" сказала [_rn], но не сделала ни малейшей попытки вас вытурить.'
                call GirlDressBuyShowInside(GirlName, DressToBuy, ShowOffLevel, DressBuyIsRelative)
            else:
                'Ваше бесцеремонное вторжение немедленно получило достойный отпор: [_rn] взвизгнула, попыталась одной рукой прикрыться, а другой вытолкать вас взашей.'

                menu:
                    "Попросить разрешить вам остаться":
                        '"Эй, ну чего ты? Жалко тебе что ли, если я посмотрю? Я же тебе покупаю это платье, должен же я посмотреть за что я плачу!"'
                        if ShowOffLevel <= 0:
                            '[_rn] была ошарашена таким заявлением: "Ах, вот ты что удумал? Значит я тебе за это поганое платье представление должна устраивать?"'
                            if DressBuyIsRelative == 1:
                                '"А ты не забыл, с кем так разговариваешь? Нет? Вот и рожай таких!"'
                            elif DressBuyIsRelative == 2:
                                '"Так ты со мной поступаешь? Подонок!"'
                            else:
                                '"Так получается? Знаешь что, ищи себе других, а я не такая!"'
                            '"Да пошел ты!" И с этими словами [_rn] одним движением застегнула платье и была такова.'
                            call SlutFriendsIncrease(GirlName, 6, 1, -3, 20, 1, -3)
                            jump ArtisansQuarter
                        else:
                            '"Ой, ну ладно," глупо засмеялась [_rn]. "От меня не убудет, коли тебе покажу. А платьичко новенькое такое хорошенькое. Смотри, если хочешь!"'
                            call GirlDressBuyShowInside(GirlName, DressToBuy, ShowOffLevel, DressBuyIsRelative)

                    "Покаяться и заплатить":
                        '"Ой, прости меня," быстро нашлись вы. "Я думал, что вы уже закончили, вот и заглянул."'
                        if ShowOffLevel <= 0:
                            '"Впредь думай, куда лезешь!" крикнула вам вслед [_rn].'
                        else:
                            '"Ах, уходишь... Ну ладно," немного разочарованно промолвила [_rn].'
                        call SlutFriendsIncrease(GirlName, 6, 1, -1, 25, 1, -1)
                        call GirlDressBuyWaitPay(GirlName, DressToBuy)

        "Предложить снять мерку прямо на месте":
            call GirlDressBuyShowOutside(GirlName, DressToBuy, ShowOffLevel, DressBuyIsRelative)

    return


label GirlDressBuyPay(GirlName="", DressToBuy=""):
    if str(GirlName or "") == "" or str(DressToBuy or "") == "":
        jump ArtisansQuarter

    $ _gds_apply_purchase(GirlName, DressToBuy, set_produced=True)
    jump ArtisansQuarter


label GirlDressBuyPregRemark(GirlName=""):
    if str(GirlName or "") == "":
        return

    if int(_gds_get_dict("pregnancy").get(GirlName, 0) or 0) > 120:
        'Ирма обратила внимание на то, что клиентка находится в положении. "От мужа или нагуляла?" спросила она у покрасневшей [_gds_name("RealName2", GirlName)].'
        '"То беда небольшая, у всех моих платьев талия шнуровкой меняется. Сейчас чуть распустим, потом затянем."'
        $ IrmaVar = _gds_get_dict("IrmaVar")
        $ IrmaVar["KnowInfertility"] = max(int(IrmaVar.get("KnowInfertility", 0) or 0), 1)

    return


label GirlDressBuyWaitPay(GirlName="", DressToBuy=""):
    if str(GirlName or "") == "" or str(DressToBuy or "") == "":
        return

    $ _rn = _gds_name("RealName", GirlName)
    $ _rn2 = _gds_name("RealName2", GirlName)

    'Минут пять-десять вы терпеливо слушали ойканье, хихиканье и прочие звуки, доносящиеся из-за ширмочки. Но вот наконец [_rn] выпорхнула обратно, сказав: "Стефанчик, ты просто прелесть! Ирмочка говорит, что мое платье будет готово уже завтра. Я так рада!"'
    'К вашему разочарованию, благодарность [_rn2] этими словами и ограничилась, по крайней мере на данный момент: довольная девица быстрым и легким шагом направилась к выходу, оставив вас расплачиваться.'
    'Ничего не поделаешь, вы отдали портнихе требуемые [_gds_dress_cost(DressToBuy)] мараведи и тоже поплелись на улицу.'

    call SlutFriendsIncrease(GirlName, 20, 1, 1, 0, 0, 0)
    call GirlDressBuyPay(GirlName, DressToBuy)
    return


label GirlDressBuyShowInside(GirlName="", DressToBuy="", ShowOffLevel=0, DressBuyIsRelative=0):
    if str(GirlName or "") == "" or str(DressToBuy or "") == "":
        return

    $ _rn = _gds_name("RealName", GirlName)
    $ _rn2 = _gds_name("RealName2", GirlName)

    if DressBuyIsRelative == 1:
        '"А тебе не стыдно так на меня пялиться?" продолжила она, чуть помедлив. "Совсем нет, Сандра, я просто восхищаюсь, какая ты у меня красивая," ловко парировали вы.'
    elif DressBuyIsRelative == 2:
        if GirlName == "amanda":
            '"А это ничего, что я Аманда?" как бы невзначай спросила она.'
        else:
            '"А это ничего, что я Мелисса?" как бы невзначай спросила она.'
        '"Конечно ничего, что же плохого в том, чтобы такой красавицей восхититься?"'

    'С помощью загадочно улыбающейся Ирмы, платье было наконец снято.'

    if str(_gds_get_dict("panties").get(GirlName, "") or "") == "":
        'Панталончиков под ним не оказалось.'
        if (int(_gds_get_dict("sluttiness").get(GirlName, 0) or 0) > 49 and int(_gds_get_dict("HadSex").get(GirlName, 0) or 0) > 0) or int(_gds_get_dict("sluttiness").get(GirlName, 0) or 0) > 62:
            'Впрочем, [_rn] ничуть не смутилась от такой мелочи. Она поймала ваш похотливый взгляд, улыбнулась и сказала: "Что, нравится? Смотри!"'
            if DressBuyIsRelative == 1:
                '"Вот оттуда ты и появился!" добавила разбитная Сандра.'
        else:
            'Стеснительная [_rn] попробовала было прикрыться, но Ирма попросила ее вытянуть руки для мерки и ей пришлось открыть свою щелочку вашим любопытным взорам.'

    call GirlDressBuyPregRemark(GirlName)

    menu:
        "Продолжить смотреть":
            'Вы продолжили лицезреть Ирму, снимающую мерку с [_rn2]. Впрочем, увлекательное зрелище снятия мерки вам быстро приелось. На вас же девушки внимания особо не обращали: мысли [_rn2], судя по всему, были всецело заняты новым платьем, а Ирма была слишком сосредоточена на работе. Вскоре они закончили и [_rn] оделась. Получив от портнихи заверение в том, что платье будет готово уже к завтрашнему утру, счастливая [_rn], весело насвистывая, удалилась, оставив вас расплачиваться. С трудом расставшись с кровно заработанными монетками вы удалились в расстроенных чувствах. Впрочем, расставание с мараведи всегда давалось вам тяжело.'
            call SlutFriendsIncrease(GirlName, 15, 2, 1, 45, 2, 1)
            call GirlDressBuyPay(GirlName, DressToBuy)

        "Подрочить на зрелище" if _gds_player_hadsex() > 5 and _gds_player_cum_today() < _gds_player_cum_cap():
            'Зрелище вас немало возбудило, и вы недолго думая достали из широких штанов свое сокровище.'
            if ShowOffLevel < 3:
                if DressBuyIsRelative == 1:
                    '"Да ты что, Стефан, совсем с глузду съехал?!" закричала с негодованием [_rn].'
                elif DressBuyIsRelative == 2:
                    '"Да ты охренел, Стефан, дрочить прямо на меня?!" пристыдила вас [_rn].'
                else:
                    '"Ах, вот зачем ты меня сюда привел! Чтобы я тебе представление устроила?" возмутилась [_rn].'
                '"Ноги моей здесь не будет!" и с этими словами она быстро накинула на себя платье и вылетела из примерочной.'
                call SlutFriendsIncrease(GirlName, 4, 1, -2, 20, 1, -3)
                jump ArtisansQuarter
            else:
                if int(_gds_get_dict("Friends").get("irma", 0) or 0) < 4:
                    '"Знаете что, молодой человек, вы мне своими глупостями мешаете нормально работать. Посидите пока снаружи," сказала вам Ирма.'
                    menu:
                        "Пойти и подождать":
                            'Делать нечего, вы покинули примерочную и стали ждать.'
                            call GirlDressBuyWaitPay(GirlName, DressToBuy)

                        "Предложить на чай 10 мараведи" if int(getattr(store, "money", 0) or 0) >= 10:
                            '"Слушай, зачем сразу уходить? Может мои скромные чаевые компенсируют неудобства," сказали вы и протянули Ирме 10 мараведи.'
                            $ money -= 10
                            call SlutFriendsIncrease("irma", 5, 2, 1, 0, 0, 0)
                            call GirlDressBuyJerkoff(GirlName, DressToBuy, DressBuyIsRelative)
                else:
                    'Решив, что молчание - знак согласия, вы начали наяривать своего друга, похотливо рассматривая [_rn2].'
                    call GirlDressBuyJerkoff(GirlName, DressToBuy, DressBuyIsRelative)

    return


label GirlDressBuyJerkoff(GirlName="", DressToBuy="", DressBuyIsRelative=0):
    if str(GirlName or "") == "" or str(DressToBuy or "") == "":
        return

    $ _rn = _gds_name("RealName", GirlName)
    $ _rn2 = _gds_name("RealName2", GirlName)

    call SlutFriendsIncrease("irma", 10, 1, 1, 50, 2, 1)
    call SlutFriendsIncrease(GirlName, 16, 1, 1, 60, 1, 1)

    if DressBuyIsRelative == 1:
        '"Значит Сандра у тебя еще не стара, раз у тебя на меня встал! Ну и шалопай же ты!" прокомментировала ваши действия [_rn].'
    elif DressBuyIsRelative == 2:
        '"Ох, и не стыдно, что у тебя на меня встал колом!" с напускной скромностью заметила [_rn].'
    else:
        '"Вижу-вижу, как я тебе нравлюсь! Не стесняйся, представляй что ты там хотел со мной сделать," засмеялась [_rn].'

    if renpy.has_label("IrmaShortStories"):
        call IrmaShortStories((DressBuyIsRelative, 0))

    menu:
        "Продолжить свое грязное занятие":
            'Вы продолжали наяривать свой член все то время, пока Ирма снимала мерку. Но все хорошее быстро заканчивается: Ирма закончила свои измерения, а вы... просто кончили.'

            if int(_gds_get_dict("HadSex").get(GirlName, 0) or 0) > 0 and renpy.random.randint(1, 2) == 1:
                'В последний момент [_rn] быстро наклонилась и обхватила губами головку вашего члена. Вы разрядились ей прямо в ротик.'
                call PregnancyCheck(GirlName, "mouth", 1, "Вы")
                call SlutFriendsIncrease(GirlName, 15, 2, 1, 50, 1, 1)
            elif int(_gds_get_dict("Friends").get("irma", 0) or 0) > 5 and renpy.random.randint(1, 2) == 1:
                'Ирма, хоть и была поглощена работой, успела в последний момент взять ваш член в рот, и ваше семя отправилось ей в желудок.'
                call PregnancyCheck("irma", "mouth", 1, "Вы")
                call SlutFriendsIncrease("irma", 8, 2, 1, 50, 1, 1)
            else:
                'Основной поток приземлился на лице [_rn2], немного попало на Ирму. Однако драму предотвратила обходительная Ирма, немедленно доставшая полотенце и воду.'
                call PregnancyCheck(GirlName, "face", 1, "Вы")
                $ _gds_get_dict("CumFaceYou")[GirlName] = 0
                call SlutFriendsIncrease(GirlName, 6, 2, -1, 45, 1, 1)

            'Получив заверения Ирмы что платье будет готово к завтрашнему утру, вы отправились восвояси.'
            call GirlDressBuyPay(GirlName, DressToBuy)

    return


label GirlDressBuyShowOutside(GirlName="", DressToBuy="", ShowOffLevel=0, DressBuyIsRelative=0):
    if str(GirlName or "") == "" or str(DressToBuy or "") == "":
        return

    $ _rn = _gds_name("RealName", GirlName)

    '"Примерить прямо на месте? А почему бы и нет," с готовностью отозвалась [_rn].'
    if DressBuyIsRelative == 1:
        '"Правда, Стефан?"'
    elif DressBuyIsRelative == 2:
        '"А Стефану моему только того и надо!"'
    else:
        '"Тем более что Стефан так просит, а ведь он платит!"'

    '"Желание клиента для меня закон," отозвалась Ирма. Приободренная этими словами, [_rn] начала распускать шнуровку на платье.'

    if str(_gds_get_dict("bra").get(GirlName, "") or "") == "" and str(_gds_get_dict("panties").get(GirlName, "") or "") == "":
        'Вскоре она осталась чем мать родила.'
    elif str(_gds_get_dict("panties").get(GirlName, "") or "") == "":
        'Вскоре она осталась выше пояса в одном лифчике.'
    elif str(_gds_get_dict("bra").get(GirlName, "") or "") == "":
        'Вскоре она осталась в одних панталончиках.'
    else:
        'Вскоре она осталась в нижнем белье.'

    call GirlDressBuyPregRemark(GirlName)

    $ RandVar = renpy.random.randint(1, 5)
    if RandVar <= 3:
        'Ваше внимание привлек шум за окном: похоже, зрители у примерки все же нашлись.'
        call SlutFriendsIncrease(GirlName, 0, 1, 0, 57, 1, 1)

    if RandVar == 1:
        'Какой-то пацаненок заглянул в окно и так и остался стоять с открытым от удивления ртом.'
    elif RandVar == 2:
        'Какой-то мужичок, по виду грузчик, стоял у окна и с интересом наблюдал за открывшимся зрелищем.'
    elif RandVar == 3:
        'Две монашки заглянули в окно, покачали головами и быстро удалились.'

    'Все хорошее имеет тенденцию быстро кончаться, закончилась и примерка. Бросив вам пару многозначительных взглядов, [_rn] оделась и отправилась восвояси, оставив вас расплачиваться.'
    'Волевым усилием вы одержали победу над страшным зеленым болотным зверем и отдали портнихе требуемые [_gds_dress_cost(DressToBuy)] мараведи.'

    call SlutFriendsIncrease(GirlName, 15, 1, 1, 60, 1, 2)
    call SlutFriendsIncrease("irma", 10, 1, 1, 45, 1, 1)
    call GirlDressBuyPay(GirlName, DressToBuy)
    return
