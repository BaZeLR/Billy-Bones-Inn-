# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def becky_home_detail_picture(image_name=""):
        image_key = str(image_name or "").strip()
        if image_key == "":
            return ""
        candidates = [
            "images/becky/Home/{}.jpg".format(image_key),
            "images/becky/home/{}.jpg".format(image_key),
        ]
        for candidate in candidates:
            if renpy.loadable(candidate):
                return candidate
        return candidates[0]

label IntBeckyGuest:
    $ dinnertime = 0
    $ dinnerbecky = 0
    $ dinnerbeckyorgasm = 0
    $ dinneringaminet = 0
    $ georgedinnersex = 0
    $ GirlName = "becky"

    label int_becky_guest_menu:
        $ _has_actions = (
            (dinnertime <= 5)
            or (dinnertime == 0 and winenum >= 30 and productnum >= 30 and IngaVar.get("Knowher", 0) >= 2)
            or (dinnertime <= 5 and georgedinnersex == 0)
            or (dinnertime <= 5 and dinnerbeckyorgasm == 0 and georgedinnersex == 0)
            or (dinnertime == 6 and georgedinnersex == 0)
            or (dinnertime == 6 and georgedinnersex == 0 and BeckyVar.get("visitedhome", 0) >= 7)
            or (dinnertime > 5 and georgedinnersex == 0)
        )
        if not _has_actions:
            return

        menu:
            "Осмотреть Ребекку" if dinnertime <= 5:
                call GirlsDesc("becky")
                jump int_becky_guest_menu

            "Осмотреть Ингенборг" if dinnertime <= 5:
                call IntIngaTalk(False)
                jump int_becky_guest_menu

            "Выставить на стол вино и еду из вашего трактира" if (dinnertime == 0 and winenum >= 30 and productnum >= 30 and IngaVar.get("Knowher", 0) >= 2):
                "Вы решили принести кувшин красного вина и закуски из запасов трактира. Вино явно пришлось по вкусу присутствующим."
                if pregnancy.get("becky", 0) <= 30:
                    "Вместе с остальными накатила и Бекки, ее лицо сразу раскраснелось."
                    call GetGirlDrunk("becky")
                else:
                    "Бекки от вина воздержалась, лишь слегка пригубив бокал."
                if pregnancy.get("inga", 0) <= 30:
                    "Ингенборг, игнорируя укоризненный взгляд мамы, тоже выпила."
                    call GetGirlDrunk("inga")
                else:
                    "Инга отодвинула стакан, сказав что ей и так весело."
                call SlutFriendsIncrease("becky", 11, 1, 2, 0, 0, 0)
                $ winenum -= 5
                $ productnum -= 5
                $ dinnertime += 1
                call stat
                call ShowImage("becky", "dinner", "tabledrink")
                jump int_becky_guest_menu

            "Кушать" if (dinnertime <= 5 and georgedinnersex == 0):
                
                if dinnerbecky > 0:
                    $ dinnerbecky = 0
                    "Вытянув руку из-под стола, вы решили вернуться к еде."
                $ r1 = renpy.random.randint(1, 4)
                $ r2 = renpy.random.randint(1, 4)
                if r1 == 1:
                    "Вы напряженно работаете ложкой, а то что выпадает, подбираете пальцами."
                elif r2 == 1:
                    "Оглянувшись и удостоверившись что на вас никто не смотрит, вы незаметно вытерли руки о край скатерти."
                else:
                    "Вы как можно энергичнее работаете челюстями."

                if BeckyVar.get("visitedhome", 0) == 4 and renpy.random.randint(1, 7) == 1:
                    "Вдруг Ребекка заговорила с Ингой и Лукасом о том, что им не стоит стесняться ее. Парочка быстро унеслась на второй этаж."
                    $ BeckyVar["visitedhome"] = 5

                if BeckyVar.get("visitedhome", 0) >= 5 and dinneringaminet == 0 and dinnertime <= 2 and renpy.random.randint(1, 6) == 1:
                    "Неожиданно вы услышали звон ножа по полу. Инга полезла под стол искать его."
                    $ dinneringaminet += 1

                if dinneringaminet > 0 and dinneringaminet <= 3:
                    "Вы обратили внимание, что Инга как полезла под стол, так оттуда и не вылезла. Лукас сидит с блаженной улыбкой."
                    if renpy.random.randint(1, 5) == 1:
                        "Бекки заглянула под стол, улыбнулась и продолжила трапезу."
                    if renpy.random.randint(1, 5) == 1:
                        "Эдди уронил салфетку, полез за ней и вылез с сальным блеском в глазах."
                        $ EddieVar["SawMomSex"] = max(EddieVar.get("SawMomSex", 0), 1)
                    $ dinneringaminet += 1

                if dinneringaminet == 4:
                    "Инга наконец вылезла из-под стола. На уголках губ у нее что-то поблескивало."
                    call SlutFriendsIncrease("inga", 0, 1, 0, 40, 2, 1)
                    call PregnancyCheck("inga", "mouth", 1, "Лукас")
                    $ dinneringaminet += 1

                if BeckyVar.get("EddieWhoreHome", 0) == 4 and dinnertime == 5:
                    call GeorgettBeckyVisit

                $ dinnertime += 1
                call ShowImage("becky", "dinner", "DinnerStart")
                jump int_becky_guest_menu

            "Полапать под столом Бекки" if (dinnertime <= 5 and dinnerbeckyorgasm == 0 and georgedinnersex == 0):
                if dinnerbecky == 0:
                    "Как можно более незаметно вы запустили руку под стол и положили ее на колено Бекки."
                elif dinnerbecky == 1:
                    "Ваша шаловливая рука задирает подол вдовушки все выше."
                    if panties.get("becky", "") != "":
                        "Путь в сладкую пещерку преграждала ткань, и вам пришлось ласкать ее через нее."
                    else:
                        "Под юбкой ничего не оказалось, и ваши пальцы сразу нашли цель."
                    "Щеки Бекки залились румянцем, но она лишь чуть шире расставила ноги."
                    call ShowImage("becky", "dinner", "grope")
                else:
                    $ dinnerbeckyorgasm = 0
                    "Вы продолжаете ласкать вдовушку прямо под семейным столом."
                    if (dinnerbecky >= 3 or (panties.get("becky", "") == "" and dinnerbecky > 2)) and renpy.random.randint(1, 3) == 1:
                        $ dinnerbeckyorgasm = 1
                    if dinnerbeckyorgasm == 1:
                        "По телу Бекки пробежала дрожь оргазма. Она крепко сжала вашу руку ногами."
                        $ GiveOrgasms["becky"] = GiveOrgasms.get("becky", 0) + 1
                        call SlutFriendsIncrease("becky", 16, 1, 1, 40, 2, 1)
                        $ BeckyVar["visitedhome"] = max(BeckyVar.get("visitedhome", 0), 4)
                        if renpy.random.randint(1, 4) == 1:
                            "Ваши игры не остались незамеченными: Эдди нырнул под стол и все понял."
                            call ShowImage("becky", "dinner", "gropeeddie")
                            $ EddieVar["SawMomSex"] = max(EddieVar.get("SawMomSex", 0), 1)
                            if renpy.random.randint(1, 2) == 3 and BeckyVar.get("EddieGeorg", 0) == 0:
                                "Как-то Эдди пошловато смотрит на хозяйку лавки, надо будет рассказать это Жоржи."
                        elif renpy.random.randint(1, 4) == 1:
                            "Это заметила Инга, понимающе усмехнулась и потянулась рукой под стол к Лукасу."
                            call ShowImage("becky", "dinner", "grope")

                if dinnertime == 5 and dinnerbeckyorgasm == 0:
                    "К вашему сожалению, Эдди, Инга и Лукас уже доели и начали собирать тарелки. Пришлось закончить игру."

                if BeckyVar.get("EddieWhoreHome", 0) == 4 and dinnertime == 5:
                    call GeorgettBeckyVisit

                $ dinnerbecky += 1
                $ dinnertime += 1
                if Drunk.get("becky", 0) == 1:
                    $ _dinner_picture = "drink" + str(renpy.random.randint(1, 3))
                    call ShowImage("becky", "dinner", _dinner_picture)
                else:
                    call ShowImage("becky", "dinner", "eat")
                jump int_becky_guest_menu

            "Взять Бекки под руку и идти наверх в спальню" if (dinnertime == 6 and georgedinnersex == 0):
                $ dinnertime += 1
                if BeckyVar.get("visitedhome", 0) < 4:
                    "Вы попытались повести Бекки наверх, но она отвесила вам пинок под столом и мягко выпроводила."
                    call SlutFriendsIncrease("becky", 8, 3, -1, 35, 3, -1)
                    call ShowImage("", "", becky_home_detail_picture("door"))
                    jump int_becky_guest_menu
                elif BeckyVar.get("visitedhome", 0) <= 6 and BeckyVar.get("visitedhome", 0) >= 4:
                    if BeckyVar.get("visitedhome", 0) >= 5 and (sluttiness.get("becky", 0) + renpy.random.randint(1, 5) + dinnerbeckyorgasm * 5 >= 48 or BeckyVar.get("HomeSex", 0) == 1):
                        call SlutFriendsIncrease("becky", 18, 2, 1, 50, 2, 1)
                        "Вы взяли Бекки за руку и повели наверх. Она решительно последовала за вами."
                        if BeckyVar.get("EddieTryToFuck", 0) == 4:
                            "Эдди дернулся было следом, но Бекки остановила его взглядом."
                        else:
                            "Эдди проводил вас затуманившимся взглядом, а Инга с Лукасом — понимающим."
                        if BeckyVar.get("EddieWhoreHome", 0) == 4:
                            "Жоржетта весело подмигнула вам."
                        $ BeckyVar["HomeSex"] = 1
                        $ _kids_watch = renpy.random.randint(1, 8)
                        call BeckyGuestKidsWatchStepsCode(_kids_watch)
                        if _kids_watch > 3 and renpy.random.randint(1, 2) == 1 and BeckyVar.get("EddieGeorg", 0) == 0:
                            "Хм, Эдди слишком уж возбужден вашим походом в спальню. Надо это обсудить с Жоржи."
                        call BeckyHome("FromDinner")
                        return
                    else:
                        "Вы потянули Бекки к лестнице, но она смущенно покачала головой и высвободила руку."
                        call ShowImage("", "", becky_home_detail_picture("door"))
                        jump int_becky_guest_menu
                else:
                    "Вы привычно взяли вдову за руку и повели к лестнице."
                    if (EddieVar.get("RidiculeFollow", 0) > 0 and renpy.random.randint(1, 10) == 1) or (EddieVar.get("RidiculeFollow", 0) == 0 and renpy.random.randint(1, 2) == 1):
                        "Эдди попытался присоединиться, но вы жестко осадили его при всех."
                        if renpy.random.randint(1, 3) == 1:
                            "Эдди чуть не разрыдался и выбежал из комнаты."
                            call SlutFriendsIncrease("eddie", 5, 1, -1, 0, 0, 0)
                        else:
                            "Эдди закусил губу и плюхнулся обратно на стул."
                            call SlutFriendsIncrease("eddie", 5, 2, -1, 0, 0, 0)
                        "Лукас и Инга заулыбались."
                        if BeckyVar.get("EddieWhoreHome", 0) == 4:
                            "Жоржетта и вовсе расхохоталась."
                            call SlutFriendsIncrease("eddie", 5, 2, -1, 0, 0, 0)
                        $ EddieVar["RidiculeFollow"] = 1
                    else:
                        "Эдди огорчился, что его не взяли, но последовать не попытался."
                        call SlutFriendsIncrease("eddie", 5, 5, -1, 0, 0, 0)
                    "Вы поднялись со вдовой наверх, в ее уютную спальню."
                    $ _kids_watch = renpy.random.randint(1, 8)
                    call BeckyGuestKidsWatchStepsCode(_kids_watch)
                    $ _becky_ladder_picture = becky_home_detail_picture("ladder" + str(renpy.random.randint(1, 2)))
                    call ShowImage("", "", _becky_ladder_picture)
                    call BeckyHome("FromDinner")
                    return

            "Идти в спальню вместе с Бекки и Эдди" if (dinnertime == 6 and georgedinnersex == 0 and BeckyVar.get("visitedhome", 0) >= 7):
                $ dinnertime += 1
                "После ужина вы взяли Бекки за руку и повели к лестнице. Она прошептала: \"А Эдди?\""
                $ _becky_ladder_picture = becky_home_detail_picture("ladder" + str(renpy.random.randint(1, 2)))
                call ShowImage("", "", _becky_ladder_picture)
                if sluttiness.get(GirlName, 0) >= 60:
                    "Вы махнули Эдди рукой, и он сразу подскочил следом."
                    if EddieVar.get("OthersSawWithMom", 0) > 0:
                        "Ингенборг проводила вас понимающим взглядом, а Лукас уже полез к ней под подол."
                        call SlutFriendsIncrease("inga", 0, 0, 0, 45, 2, 1)
                    else:
                        "Инга смотрела на Эдди с открытым ртом. Лукас быстро сориентировался и начал задирать ей юбку."
                        $ EddieVar["OthersSawWithMom"] = 1
                        call SlutFriendsIncrease("inga", 0, 0, 0, 45, 2, 1)
                else:
                    "Вы хотели позвать его явно, но Бекки одернула вас: \"Ну не так явно же!\" Вы незаметно кивнули Эдди."
                if BeckyVar.get("EddieWhoreHome", 0) == 4:
                    "Жоржетта показала Эдди поднятые вверх большие пальцы."
                $ _kids_watch = renpy.random.randint(1, 8)
                call BeckyGuestKidsWatchStepsCode(_kids_watch)
                if sluttiness.get(GirlName, 0) >= 60:
                    "Втроем вы ввалились в спальню миссис Блэнкеншип."
                else:
                    "Вы с Бекки поднялись в спальню и начали целоваться, не закрыв дверь. Вскоре к вам присоединился уже раздетый Эдди."
                call BeckyHome("SvalnyiGreh")
                return

            "Попрощаться и идти домой" if (dinnertime > 5 and georgedinnersex == 0):
                "Вы вежливо попрощались с семейством Блэнкеншип и направились на улицу."
                $ calendar_advance_slots(1)
                jump MarketPlace
                return

label BeckyGuestKidsWatchStepsCode(kids_watch=0):
    if kids_watch <= 3:
        "Поднимаясь вслед за вдовой по лестнице, вы заметили что из-за угла за вами кто-то подсматривает."
        if kids_watch == 1:
            "Это был Ивар, младший сын вдовы. Встретившись с вами взглядом он усмехнулся и сделал пошлый жест."
        elif kids_watch == 2:
            "Это была юная Эмма, средняя дочка Бекки. На ее лице застыло мечтательное выражение."
        else:
            "Это была Эмма с маленькой Лаурой, младшей дочкой Бекки. Лаура была явно удивлена происходящим, но Эмма наклонилась к ней и прошептала что-то такое, отчего глазенки Лауры расширились, а щеки стали пунцовыми."
    return
