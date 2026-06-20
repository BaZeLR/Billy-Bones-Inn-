# ================================================================================
# Becky home/front story events.
# Event labels own scene text, menus, state mutation, time, and story flow.
# Rooms only provide the trigger location.
# ================================================================================

label story_becky_home_front_inga_0:
    show screen main_ui
    $ Becky.ensure_story_defaults()
    $ Becky.var["HomeFrontCheckedDay"] = int(dayspassed or 0)
    $ RandIngaFuck = procedural_randint(1, 4, "becky_home_front_%s" % int(dayspassed or 0))
    if Becky.var.get("TodayFrontSexCheck", 0) == 1 and RandIngaFuck <= 2:
        $ RandIngaFuck = 3
    $ Becky.var["TodayFrontSexCheck"] = 1
    $ ViewIngaSex = 0
    $ IngaVar.setdefault("SawLucassex", 0)
    $ IngaVar.setdefault("Knowher", 0)
    $ pregnancy.setdefault("inga", 0)
    if RandIngaFuck == 1:
        $ PregnancyCheck("inga", "mouthface", 1, "Лукас")
    elif RandIngaFuck == 2:
        $ PregnancyCheck("inga", "inside", 1, "Лукас")

    if ArriveMode == "FromDances":
        $ scene_image = "images/becky/Home/withbecky.jpg"
        $ _layout_last_picture = scene_image
        vscene scene_image
        "По дороге к дому Бекки вы продолжаете страстно целоваться с податливой вдовушкой. Дом и лавка вдовы Блэнкеншип стоят как раз у площади, где проходили танцы, и вот вы уже у черного хода."
    else:
        $ scene_image = "images/becky/Home/house2.jpg"
        $ _layout_last_picture = scene_image
        vscene scene_image
        "Вы стоите в темном закоулке неподалеку от рыночной площади. Перед вами ступени, ведущие к черному ходу в дом Ребекки Блэнкеншип."

    if RandIngaFuck <= 3:
        "Вдруг какое-то движение в темном углу за крыльцом привлекло ваше внимание."

    menu:
        "Зайти в дом":
            call BeckyHome(ArriveMode)
            return True

        "Вернуться к трактиру" if ArriveMode == "guest":
            jump StreetTavern

        "Осторожно заглянуть за угол" if ViewIngaSex == 0:
            jump story_becky_home_front_peek_0

        "Сделать вид, что ничего там нет":
            $ ViewIngaSex = 10
            "Вы решаете не задерживаться у темного угла."
            return True


label story_becky_home_front_peek_0:
    show screen main_ui
    if RandIngaFuck == 1:
        if IngaVar["SawLucassex"] == 0:
            "Ваше любопытство оказалось вознагражденным интересной сценой:"
        else:
            "Вы увидели уже знакомую картину:"
        if IngaVar["Knowher"] == 0:
            "В углу за крыльцом стоял, прислонившись к стене, какой-то молодой парень. На его лице застыла блаженная гримаса."
            "Причина его счастья была очевидна: рыжая деваха стояла перед ним на коленях и увлеченно у него отсасывала."
        else:
            "В углу за крыльцом стоял, прислонившись к стене, Лукас, ухажер Ингенборг. На его лице застыла блаженная гримаса."
            "Причина его счастья была очевидна: Ингенборг, старшая дочка вдовы, стояла перед ним на коленях и увлеченно у него отсасывала."
        $ scene_image = "images/inga/StreetSex/minet1.jpg"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ ViewIngaSex = 1
        $ IngaVar["SawLucassex"] = 1
        $ IngaVar["Knowher"] = max(1, IngaVar["Knowher"])
    elif RandIngaFuck == 2:
        if IngaVar["SawLucassex"] == 0:
            "Ваше любопытство оказалось вознагражденным интересной сценой:"
        else:
            "Вы увидели уже знакомую картину:"
        if IngaVar["Knowher"] == 0:
            "В углу за крыльцом самозабвенно сношалась парочка. Молодой парень прижал к стене свою подружку, какую-то рыжую деваху."
        else:
            "В углу за крыльцом самозабвенно сношалась парочка. Лукас, ухажер Ингенборг, прижал к стене свою подружку, старшую дочку вдовушки."
        if pregnancy["inga"] >= 120:
            "Несмотря на то, что девица явно в положении, парень жарил ее раком, задрав той юбку."
        else:
            "Он завернул ей юбку, спустил панталончики, приподнял и насадил на свой член."
        $ scene_image = "images/inga/StreetSex/pregfuckyou.jpg" if pregnancy["inga"] >= 120 else "images/inga/StreetSex/fuckyou1.jpg"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ ViewIngaSex = 1
        $ IngaVar["SawLucassex"] = 1
        $ IngaVar["Knowher"] = max(1, IngaVar["Knowher"])
    else:
        "Наверное, показалось: вы заглянули за крыльцо, но там никого не было."
        $ scene_image = "images/becky/Home/house2.jpg"
        $ _layout_last_picture = scene_image
        vscene scene_image
        $ ViewIngaSex = 10
        return True
    if ArriveMode == "FromDances" and RandIngaFuck <= 2:
        "Ваши наблюдения заинтересовали Бекки, которая решила проверить, на что это вы там смотрите."

    menu:
        "Поделиться с вдовой своим открытием" if ArriveMode == "FromDances":
            jump story_becky_home_front_share_0

        "Сделать вид, что ничего там нет" if ArriveMode == "FromDances":
            jump story_becky_home_front_ignore_0

        "Предложить подойти к парочке" if ArriveMode == "FromDances":
            jump story_becky_home_front_suggest_approach_0

        "Подойти к парочке" if ArriveMode != "FromDances":
            jump story_becky_home_front_approach_0

        "Зайти в дом":
            call BeckyHome(ArriveMode)
            return True


label story_becky_home_front_share_0:
    show screen main_ui
    "\"Бекки, смотри\", - подозвали вы вдовушку, указав ей на парочку. Бекки подошла к вам и осторожно выглянула из-за угла."
    if Becky.var.get("SawIngaFuck", 0) == 0:
        "\"Так это ж Ингенборг, дочка моя, с Лукасом, ухажером своим. Очень милый мальчик, он на ней даже жениться собирается. До дома не дотерпели, эх молодость-молодость!\""
    else:
        "\"Эх доченька бедная моя, тебе же наверное неудобно-то на камне. Ну да дело молодое!\""
    if Becky.var.get("visitedhome", 0) < 5:
        "\"Но ведь это значит, что дома скорее всего никого нет, так что пошли скорее внутрь, пока они нас не засекли!\""
    if RandIngaFuck == 1:
        $ scene_image = "images/inga/StreetSex/minetshow1.jpg"
    elif pregnancy["inga"] >= 120:
        $ scene_image = "images/inga/StreetSex/pregfuckshow.jpg"
    else:
        $ scene_image = "images/inga/StreetSex/fuckshow1.jpg"
    $ _layout_last_picture = scene_image
    vscene scene_image
    $ Becky.var["SawIngaFuck"] = max(int(Becky.var.get("SawIngaFuck", 0) or 0), 1)
    $ IngaVar["Knowher"] = max(1, IngaVar["Knowher"])
    $ IngaVar["SawLucassex"] = 1
    $ ViewIngaSex = 2
    menu:
        "Предложить подойти к парочке":
            jump story_becky_home_front_suggest_approach_0

        "Зайти в дом":
            call BeckyHome(ArriveMode)
            return True


label story_becky_home_front_ignore_0:
    show screen main_ui
    "Вы вернулись к вдове Блэнкеншип: \"А, кошка пробежала, ерунда\", - сказали вы ей."
    if Becky.var.get("visitedhome", 0) < 5:
        "\"А, ну тогда пошли скорее в дом, пока дети мои не вернулись,\" - ответила вам Бекки."
        "\"А то увидят, смеяться будут, мол мамке уже [age_girls.get('becky', 36)] лет, а она все с парнями гуляет.\""
    else:
        "\"А, ну тогда пошли скорее в дом, я уже и стол накрыла,\" - ответила вам Бекки."
    $ ViewIngaSex = 10
    menu:
        "Зайти в дом":
            call BeckyHome(ArriveMode)
            return True


label story_becky_home_front_suggest_approach_0:
    show screen main_ui
    if Becky.var.get("visitedhome", 0) < 5:
        "Вы обернулись к вдове Блэнкеншип: \"Может подойдем к ним?\""
        "\"Да ты что, ведь тогда дочка меня с тобой увидит, вдруг смеяться будет, мол мамке уже [age_girls.get('becky', 36)] лет, а она все с парнями гуляет. Пошли лучше скорее в дом, пока они тут заняты.\""
        "И с этими словами она настойчиво потянула вас в сторону двери."
        $ ViewIngaSex = 10
        menu:
            "Зайти в дом":
                call BeckyHome(ArriveMode)
                return True
    else:
        "\"Бекки, отчего бы тебе не поприветствовать дочу?\" - осведомились вы, и, преодолев слабое сопротивление вдовицы, подошли к влюбленной парочке."
        "\"Привет, детки,\" - сказала им Бекки."
        "\"Инга, Лукас, привет, как дела?\" - вежливо осведомились вы."
        if pregnancy["inga"] >= 120:
            "\"Пока не родила!\" - пошутил в ответ Лукас, погладив округлившийся живот своей любовницы."
        else:
            "\"О, привет Стефан, здравствуйте миссис Блэнкеншип,\" - отозвался Лукас."
        if RandIngaFuck == 1:
            "Ингенборг же ничего не ответила, но отнюдь не из-за недостатка вежливости: ее ротик был занят внушительным органом жениха. Увидев вас со своей мамой, она слегка покраснела, помахала вам рукой, но члена изо рта не выпустила."
        else:
            "При этом Лукас ни на секунду не замедлил темпа, продолжая сношать Ингенборг. Та смутилась и зарделась, увидев мать, но явно недостаточно, чтобы перестать."
            "\"Мам, ах, привет, ах, Стефанчик, ах, и тебе приветик,\" - вымолвила Блэнкеншип-младшая."
        $ ViewIngaSex = 3
        $ Becky.apply_social_roll(0, 0, 0, 45, 3, 1)
        call SlutFriendsIncrease("inga", 0, 0, 0, 45, 3, 1)
        menu:
            "Посмотреть как они кончат":
                jump story_becky_home_front_watch_0

            "Зайти в дом":
                call BeckyHome(ArriveMode)
                return True


label story_becky_home_front_watch_0:
    show screen main_ui
    if ArriveMode == "FromDances":
        "Вы вместе с Бекки с интересом продолжили наблюдать за совокупляющейся парочкой. Вдову такое зрелище, судя по всему, завело, и ее рука автоматически стала потирать промежность через платье, а на лице застыла улыбка."
        "Любовников же такое внимание возбудило, судя по всему, еще пуще."
    else:
        "Вы с интересом продолжили наблюдать за совокупляющейся парочкой. Любовников ваше внимание, судя по всему, завело еще больше."

    if RandIngaFuck == 1:
        "Косясь на вас, Ингенборг старательно продолжала работать ротиком над членом Лукаса и вскоре ее труды оказались вознаграждены: с блаженным вздохом парнишка кончил ей прямо в ротик."
        "Ей такой исход был явно не в первой: она проглотила все не поморщившись, облизала пухленькие губки и встала с колен."
        $ scene_image = "images/inga/StreetSex/cumfaceshow1.jpg" if ArriveMode == "FromDances" else "images/inga/StreetSex/cumface.jpg"
    else:
        "Посматривая время от времени на вас, парочка стремительно приближалась к оргазму. И вот Лукас стал заполнять пещерку Инги своим семенем, а вслед за ним, мелко затрясшись, стала кончать и его партнерша."
        "Обмякший член Лукаса вывалился из влагалища Ингенборг, а та сразу же натянула панталончики, не давая сперме вытечь и запачкать платье."
        if pregnancy["inga"] >= 120:
            $ scene_image = "images/inga/StreetSex/pregfuckshow.jpg" if ArriveMode == "FromDances" else "images/inga/StreetSex/pregfuckyou.jpg"
        else:
            $ scene_image = "images/inga/StreetSex/fuckshow1.jpg" if ArriveMode == "FromDances" else "images/inga/StreetSex/fuckyou1.jpg"
    $ _layout_last_picture = scene_image
    vscene scene_image

    if ArriveMode == "FromDances":
        "\"Мам, Стефан, мы закончили, пойдем теперь в дом,\" - как ни в чем не бывало предложила вам Инга."
        $ Becky.apply_social_roll(0, 0, 0, 45, 3, 1)
    else:
        "\"Стефан, увидимся дома, нам надо еще кое-что забрать,\" - сказал вам Лукас, заправляя член обратно в штаны. И с этими словами парочка удалилась."

    if procedural_randint(1, 2, "becky_home_front_inga_greet_%s" % int(dayspassed or 0)) == 1 and RandIngaFuck == 2 and Becky.var.get("IngaSexGreet", 0) == 0 and ArriveMode == "FromDances":
        "\"Лукас, Ингочка, а что ж вы на улице, вам же небось неудобно?\" - резонно осведомилась у парочки Бекки."
        "\"Я же вам сказала, что можете у нас дома, не стесняйтесь.\""
        "\"Ой мам, ну ты сказанула. Лукас и стыд - вещи мало совместимые. Где он меня только не сношал. Это-то его и заводит, говорит что в одном месте скучно. Правда, милый?\""
        "\"Да, миссис Блэнкеншип,\" - согласился Лукас, \"Инга все правильно говорит.\""
        "\"Ну, навязывать свой дом не буду,\" - пошла на попятную Бекки, \"только смотрите, не простудитесь,\" - заботливо поспешила добавить она."
        $ Becky.var["IngaSexGreet"] = 1

    call SlutFriendsIncrease("inga", 0, 0, 0, 45, 3, 1)
    $ ViewIngaSex = 10
    menu:
        "Зайти в дом" if ArriveMode == "FromDances":
            call BeckyHome(ArriveMode)
            return True

        "Вернуться":
            return True


label story_becky_home_front_approach_0:
    show screen main_ui
    if IngaVar["Knowher"] < 2:
        "Вы решили нарушить уединение парочки. Подойдя к любовникам решительным шагом, вы нахально осведомились: \"А что это вы тут делаете, а?\""
        "\"Как что делаем, разве не видно?\" - удивился парень. \"Я трахаю свою подружку.\""
        "\"Резонно, можно было бы и не спрашивать,\" - подумали вы, но, набравшись наглости, вслух произнесли: \"Ну тогда я следующий!\""
        "Однако на ваш заход вы получили обескураживающий ответ: \"Ну, хотя я парней обычно не трахаю, для тебя могу сделать исключение.\""
        "\"Нет, нет, что вы, не надо исключений, будьте верны своим принципам,\" - тут же нашлись вы. Парень решил сосредоточиться на своей партнерше, а не на дискуссии с вами."
        $ ViewIngaSex = 10
    elif Becky.var.get("visitedhome", 0) < 5:
        "Вы решили нарушить уединение парочки. Подойдя к Лукасу с Ингой решительным шагом, вы нахально осведомились: \"А что это вы тут делаете, а?\""
        "\"О, привет Стефан,\" - ответил Лукас вам как ни в чем не бывало. \"А сам-то что думаешь, что мы тут делаем?\""
        if RandIngaFuck == 1:
            "Ингенборг же ничего вам не ответила: ее ротик был занят внушительным органом жениха. Она только помахала вам рукой, не выпуская члена изо рта."
        else:
            "Инга обладала меньшей выдержкой, чем ее хахаль, и густо покраснела, увидев, что вы их засекли в момент секса."
        "\"Стефан, я тут как видишь несколько занят, если ты хочешь о чем-то поговорить, то давай я кончу и в доме поболтаем, лады?\" - добавил ваш знакомец."
        $ ViewIngaSex = 10
    else:
        "Вы решили поприветствовать ваших знакомых. Подойдя к ним, вы вежливо сказали: \"Инга, Лукас, привет, как дела?\""
        if pregnancy["inga"] >= 120:
            "\"Пока не родила!\" - пошутил в ответ Лукас, погладив округлившийся живот своей любовницы."
        else:
            "\"О, привет Стефан,\" - отозвался Лукас."
        if RandIngaFuck == 1:
            "Ингенборг ничего не ответила, но отнюдь не из-за недостатка вежливости: ее ротик был занят внушительным органом жениха. Увидев вас, она слегка покраснела и помахала рукой, не выпуская члена изо рта."
        else:
            "Лукас ни на секунду не замедлил темпа, продолжая сношать Ингенборг. Та обернулась к вам и вежливо, хотя и несколько запыхавшись, поприветствовала вас: \"Стефанчик, ах, приветик, ах!\""
        $ ViewIngaSex = 3
    call SlutFriendsIncrease("inga", 0, 0, 0, 45, 3, 1)
    menu:
        "Посмотреть как они кончат" if ViewIngaSex == 3:
            jump story_becky_home_front_watch_0

        "Вернуться":
            return True


label story_becky_home_visit_0:
    show screen main_ui
    $ Becky.ensure_story_defaults()
    $ Becky.var["HomeEnterCheckedDay"] = int(dayspassed or 0)
    $ BeckyAdmit = 0
    $ GirlName = "becky"
    $ IngaVar.setdefault("Knowher", 0)
    $ pregnancy.setdefault("inga", 0)
    $ Arousal.setdefault(GirlName, 0)
    $ PussyWetStart.setdefault(GirlName, Arousal.get(GirlName, 0))
    $ scene_image = "images/becky/Home/withbecky.jpg"
    $ _layout_last_picture = scene_image
    vscene scene_image

    "Вы постучали в дверь и через несколько секунд она распахнулась. За ней стояла Ребекка Блэнкеншип."
    if Becky.var.get("visitedhome", 0) < 3:
        if Becky.var.get("VisitScolded", 0) == 0:
            "Она не очень-то была рада вашему визиту: \"Стефан, зачем ты пришел?! Мы же договаривались! Надеюсь, тебя никто не видел?\""
            "\"Никто,\" - сказали вы, глядя на вдову своими честными глазами. \"Но я просто хотел...\""
            "Бекки, однако, ваше желание мало интересовало. Она резко прервала вас: \"Не приходи больше, что люди подумают. Все, пока.\""
            "И дверь перед вашим носом захлопнулась."
            $ Becky.var["VisitScolded"] = 1
            $ Becky.apply_social_roll(8, 3, -1, 35, 3, -1)
        else:
            "Увидев вас, она рассердилась не на шутку: \"Стефан, тебе что, все нужно по двадцать раз повторять?! Не приходи пока ко мне домой.\""
            "\"Но я,\" - начали оправдываться вы, но поняли, что разговариваете с закрытой дубовой дверью."
            "Изнутри послышался звук запираемого засова. Похоже, сейчас вам здесь не очень-то рады."
            $ Becky.apply_social_roll(8, 1, -1, 35, 1, -1)
        menu:
            "В печали вернуться к трактиру":
                jump StreetTavern
    elif player_state().appearance.current_dress != "citydress":
        "Она тщательно осмотрела вас и строго сказала: \"Стефан, я же тебе говорила, ты должен быть одет скромно, но прилично. А ты в чем пришел? Беги переодевайся!\""
        "С этими словами она захлопнула дверь перед вашим носом. Отчего-то вы почувствовали себя нашкодничавшим школьником."
        menu:
            "Вернуться к трактиру переодеться":
                jump StreetTavern
    else:
        "Она тщательно осмотрела вас и сказала: \"Что же ты встал на пороге, проходи скорей!\""
        "Вы не замедлили воспользоваться приглашением и прошли в дом, прямо к накрытому столу. К вашей скромной трапезе из шести блюд присоединился и Эдди."
        "Не успели вы приступить к поглощению пищи, как услышали, как хлопнула входная дверь."
        $ BeckyAdmit = 1

    if BeckyAdmit == 1:
        $ Becky.var["TimesVisited"] = int(Becky.var.get("TimesVisited", 0) or 0) + 1
        if IngaVar["Knowher"] >= 2:
            "Вскоре к вам за столом присоединились Ингенборг, старшая дочка соломенной вдовушки, вместе с ее хахалем Лукасом."
        elif IngaVar["Knowher"] == 1:
            "На пороге показалась уже виденная вами парочка - Лукас и Ингенборг."
            "Бекки повернулась к вам: \"Стефан, позволь мне представить тебе мою старшую дочку Ингенборг и ее жениха Лукаса. Лукас, Инга, это Стефан, мой важный клиент и оптовый покупатель.\""
            "Вы пожали руку Лукасу, поцеловали в щечку Ингу и уселись за стол."
            $ IngaVar["Knowher"] = 2
        else:
            "На пороге показалось двое - высокая рыжеволосая девушка, похожая на хозяйку дома, в сопровождении парня чуть постарше ее."
            "Бекки повернулась к вам: \"Стефан, позволь мне представить тебе мою старшую дочку Ингенборг и ее жениха Лукаса. Лукас, Инга, это Стефан, мой важный клиент и оптовый покупатель.\""
            "Вы пожали руку Лукасу, поцеловали в щечку Ингу и уселись за стол."
            $ IngaVar["Knowher"] = 2
        $ scene_image = "images/becky/dinner/DinnerInga.jpg"
        $ _layout_last_picture = scene_image
        vscene scene_image
        if procedural_randint(1, 5, "becky_home_dinner_inga_%s" % int(dayspassed or 0)) == 1:
            "Вы присмотрелись к Инге и заметили, что перед ужином времени она не теряла: на ее рыжей шевелюре были видны следы спермы."
        if pregnancy.get("inga", 0) >= 120:
            "Одного взгляда на круглый живот Инги было достаточно, чтобы понять, что она ведет активную половую жизнь."
        call IntBeckyGuest
        "Итак, вы сидите за столом в гостях у вдовы Блэнкеншип и наслаждаетесь аппетитной домашней кухней."
    return True


label story_becky_home_from_dances_0:
    show screen main_ui
    $ GirlName = "becky"
    $ scene_image = "images/becky/sex/inroom1.jpg"
    $ _layout_last_picture = scene_image
    vscene scene_image
    "Заведя вас к себе в дом, Бекки тихо и осторожно повела вас по коридору к себе в спальню."
    "Вдоль стен стояло несколько массивных сундуков, скамья, пара стульев. А весь центр комнаты занимала большая кровать."
    "Вы и миссис Блэнкеншип находитесь в ее спальне."
    $ Arousal.setdefault(GirlName, 0)
    $ PussyWetStart.setdefault(GirlName, Arousal.get(GirlName, 0))
    $ Arousal[GirlName] = PussyWetStart[GirlName]
    $ ArriveMode = ""
    call cock_position(GirlName, 0)
    call check_visibility(GirlName)
    call IntBeckySex(GirlName)
    return True


label story_becky_home_from_dinner_0:
    show screen main_ui
    $ GirlName = "becky"
    $ scene_image = "images/becky/sex/inroom1.jpg"
    $ _layout_last_picture = scene_image
    vscene scene_image
    "Вы зашли вслед за Бекки в ее спальню. Вдоль стен стояло несколько массивных сундуков, скамья, пара стульев. А весь центр комнаты занимала большая кровать."
    if Becky.var.get("EddieTryToFuck", 0) == 1 and Becky.var.get("visitedhome", 0) < 7:
        call BeckyEddieJoinFirst
    else:
        if Becky.var.get("visitedhome", 0) < 7:
            "Дав вам зайти, вдова закрыла дверь на ключ и обернулась к вам: \"Если детишки мои развлекаются, то почему в конце концов я не могу себе такого позволить? Иди же ко мне!\""
        else:
            "Вдова не позаботилась не то, что запереть дверь на ключ, но и даже полностью закрыть ее, и не теряя времени потащила вас к кровати."
        "Вы и миссис Блэнкеншип находитесь в ее спальне."
    $ Arousal.setdefault(GirlName, 0)
    $ PussyWetStart.setdefault(GirlName, Arousal.get(GirlName, 0))
    $ Arousal[GirlName] = PussyWetStart[GirlName]
    $ ArriveMode = ""
    call cock_position(GirlName, 0)
    call check_visibility(GirlName)
    call IntBeckySex(GirlName)
    return True


label story_becky_home_svalnyi_greh_0:
    show screen main_ui
    $ GirlName = "becky"
    $ scene_image = "images/becky/sex/inroom1.jpg"
    $ _layout_last_picture = scene_image
    vscene scene_image
    $ GrupenSex["eddie"] = 1
    call IntEddieBeckySex
    "Весь центр комнаты занимает большая кровать, а вдоль стен стоит несколько массивных сундуков, скамья, пара стульев."
    "Вы и миссис Блэнкеншип находитесь в ее спальне. Вместе с вами находится Эдди, сын Бекки и управляющий лавкой. Им движут к матери отнюдь не сыновьи чувства."
    $ Arousal.setdefault(GirlName, 0)
    $ PussyWetStart.setdefault(GirlName, Arousal.get(GirlName, 0))
    $ Arousal[GirlName] = PussyWetStart[GirlName]
    $ ArriveMode = ""
    call cock_position(GirlName, 0)
    call check_visibility(GirlName)
    call IntBeckySex(GirlName)
    return True
