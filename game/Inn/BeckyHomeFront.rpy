# BeckyHomeFront.rpy
# Converted from legacy script. All features, menus, and event logic preserved.
# Dev notes and comments included for maintainability and future extension.

# --- GLOBAL DEFAULTS ---
default ViewIngaSex = 0
default ArriveMode = ""
default RandIngaFuck = 1
default _becky_home_front_resume = False
default IngaVar = {"SawLucassex": 0, "Knowher": 0}

init python:
    def becky_homefront_withbecky_picture():
        candidates = [
            "images/becky/Home/withbecky.jpg",
            "images/becky/home/withbecky.jpg",
        ]
        for candidate in candidates:
            if renpy.loadable(candidate):
                return candidate
        return "images/becky/Home/withbecky.jpg"

    def becky_homefront_house_picture():
        candidates = [
            "images/becky/Home/house1.jpg",
            "images/becky/Home/house2.jpg",
            "images/becky/home/house1.jpg",
            "images/becky/home/house2.jpg",
        ]
        loadable = [row for row in candidates if renpy.loadable(row)]
        if len(loadable) > 0:
            return renpy.random.choice(loadable)
        return "images/becky/Home/house2.jpg"

    def becky_homefront_normal_desc():
        return ArriveMode != "FromDances"

    def becky_homefront_dance_desc():
        return ArriveMode == "FromDances"

    def becky_homefront_guest_exit():
        return ArriveMode == "guest"

    def becky_homefront_peek_available():
        return ViewIngaSex == 0

    def becky_homefront_becky_visible():
        return ArriveMode == "FromDances"

    def becky_homefront_inga_visible():
        return ViewIngaSex > 0

    def becky_homefront_lucas_visible():
        return ViewIngaSex > 0

    BeckyHomeFrontRoom = Room(
        code_name="BeckyHomeFront",
        group_name=ROOM_GROUP_CITY,
        display_name="Черный ход дома Бекки",
        bg_picture="images/becky/Home/house2.jpg",
        descriptions=[
            RoomDescription(
                text="Вы стоите в темном закоулке неподалеку от рыночной площади. Перед вами поднимаются ступени, ведущие к черному ходу в дом Ребекки Блэнкеншип.",
                condition=becky_homefront_normal_desc,
                priority=200,
            ),
            RoomDescription(
                text="По дороге к дому Бекки вы продолжаете страстно целоваться с податливой вдовушкой. Впрочем, дорога ваша была недолгой - ведь дом и лавка вдовы Блэнкеншип стояли как раз на площади, где проходили танцы, надо было всего лишь зайти за угол, дабы войти туда через черный ход. И вот, буквально через несколько минут, вы вдвоем уже стоите перед дверью в дом Блэнкеншип со стороны боковой улочки.",
                condition=becky_homefront_dance_desc,
                priority=210,
            ),
        ],
        exits=[
            RoomExit(label="Зайти в дом", target="BeckyHome"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern", condition=becky_homefront_guest_exit),
        ],
        game_items=[
            GameObject(
                object_id="back_door",
                name="Черный ход",
                description="Неприметная дверь со стороны боковой улочки ведет прямо в дом Бекки.",
                actions=[
                    ObjectAction(action_id="enter_house", label="Зайти в дом", hook="call", target="BeckyHome"),
                ],
            ),
            GameObject(
                object_id="dark_corner",
                name="Темный угол за крыльцом",
                description="За крыльцом есть темный угол, где вполне может происходить что-нибудь интересное.",
                actions=[
                    ObjectAction(action_id="peek_corner", label="Осторожно заглянуть за угол", hook="call", target="becky_homefront_peek", condition=becky_homefront_peek_available),
                ],
            ),
        ],
        npcs=[
            {"npc_id": "becky", "name": "Бекки", "condition": becky_homefront_becky_visible, "talk_label": "IntBeckyTalk"},
            {"npc_id": "inga", "name": "Ингенборг", "condition": becky_homefront_inga_visible, "talk_label": "IntIngaTalk"},
            {"npc_id": "lucas", "name": "Лукас", "condition": becky_homefront_lucas_visible},
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "house_front": True,
        },
    )

    def show_inga_front_fuck_image(type, with_becky):
        # type: 1=minet, 2=fuck, 3=minet cum
        # with_becky: 1=alone, 2=with Becky
        if type == 1:
            if with_becky == 2:
                ShowImageSeq("inga", "streetsex", "minetshow", 6)
            else:
                ShowImageSeq("inga", "streetsex", "minet", 5)
        elif type == 2:
            if with_becky == 2:
                if pregnancy["inga"] >= 120:
                    ShowImage("inga", "streetsex", "pregfuckshow")
                else:
                    ShowImageSeq("inga", "streetsex", "fuckshow", 3)
            else:
                if pregnancy["inga"] >= 120:
                    ShowImage("inga", "streetsex", "pregfuckyou")
                else:
                    ShowImageSeq("inga", "streetsex", "fuckyou", 5)
        else:
            if with_becky == 2:
                ShowImageSeq("inga", "streetsex", "cumfaceshow", 3)
            else:
                ShowImage("inga", "streetsex", "cumface")

# --- MAIN LOCATION LABEL ---
label BeckyHomeFront(arrive_mode=""):
    call EnterLocation("BeckyHomeFront")
    python:
        BeckyVar.setdefault("visitedhome", 0)
        BeckyVar.setdefault("TodayFrontSexCheck", 0)
        BeckyVar.setdefault("SawIngaFuck", 0)
        BeckyVar.setdefault("IngaSexGreet", 0)
        IngaVar.setdefault("SawLucassex", 0)
        IngaVar.setdefault("Knowher", 0)
        pregnancy.setdefault("inga", 0)
        _becky_front_room = BeckyHomeFrontRoom

    python:
        _resume_mode = bool(_becky_home_front_resume)
        _becky_home_front_resume = False

    if not _resume_mode:
        $ ArriveMode = arrive_mode
        $ ViewIngaSex = 0
        $ RandIngaFuck = renpy.random.randint(1,4)
        if BeckyVar["TodayFrontSexCheck"] == 1 and RandIngaFuck <= 2:
            $ RandIngaFuck = 3
        $ BeckyVar["TodayFrontSexCheck"] = 1
        if RandIngaFuck == 1:
            $ PregnancyCheck("inga", "mouthface", 1, "Лукас")
        elif RandIngaFuck == 2:
            $ PregnancyCheck("inga", "inside", 1, "Лукас")

    if ArriveMode == "FromDances":
        if BeckyVar["visitedhome"] == 0:
            $ BeckyVar["visitedhome"] = 1
        "[_becky_front_room.descriptions[1].text]"
        call ShowImage("", "", becky_homefront_withbecky_picture())
    else:
        "[_becky_front_room.descriptions[0].text]"
        call ShowImage("", "", becky_homefront_house_picture())
    $ _becky_front_room.mark_visited()

    if navigation_only_mode_enabled():
        "[navigation_only_message()]"
        "[navigation_only_time_note()]"
        menu:
            "Зайти в дом":
                call BeckyHome(ArriveMode)
                return
            "Вернуться к трактиру":
                jump StreetTavern
        return

    if RandIngaFuck <= 3:
        "Вдруг какое-то движение в темном углу за крыльцом привлекло ваше внимание."
        "Что делать?"
    menu:
        
            "Зайти в дом":
                call BeckyHome(ArriveMode)
                return
                
            "Вернуться к трактиру" if ArriveMode == "guest":
                jump StreetTavern
                
            "Осторожно заглянуть за угол" if ViewIngaSex == 0:
                call becky_homefront_peek
                jump BeckyHomeFrontMenu
                
            "Поделиться с вдовой своим открытием" if (ViewIngaSex == 1 and ArriveMode == "FromDances"):
                call becky_homefront_share_with_becky
                jump BeckyHomeFrontMenu
                
            "Сделать вид, что ничего там нет" if (ViewIngaSex == 1 and ArriveMode == "FromDances"):
                call becky_homefront_ignore
                jump BeckyHomeFrontMenu
                
            "Предложить подойти к парочке" if (ViewIngaSex == 1 and ArriveMode == "FromDances"):
                call becky_homefront_suggest_approach
                jump BeckyHomeFrontMenu
                
            "Посмотреть как они кончат" if (ViewIngaSex == 2 and ArriveMode == "FromDances"):
                call becky_homefront_watch_cum
                jump BeckyHomeFrontMenu
                
            "Подойти к парочке" if (ViewIngaSex == 1 and ArriveMode == ""):
                call becky_homefront_approach
                jump BeckyHomeFrontMenu

label BeckyHomeFrontMenu:
    # Return to main menu after sub-actions
    $ _becky_home_front_resume = True
    jump BeckyHomeFront

# --- SUBLABELS FOR MENU OPTIONS ---
label becky_homefront_peek:
    if RandIngaFuck == 1:
        if IngaVar["SawLucassex"] == 0:
            "Ваше любопытство оказалось вознагражденным интересной сценой: "
        else:
            "Вы увидели уже знакомую картину: "
        "в углу за крыльцом стоял, прислонившись к стене, "
        if IngaVar["Knowher"] == 0:
            "какой-то молодой парень. "
        else:
            "Лукас, ухажер Ингенборг. "
        "На его лице застыла блаженная гримаса..."
        if IngaVar["Knowher"] == 0:
            "рыжей девахи, стояла перед ним на коленях и увлеченно у него отсасывала. "
        else:
            "Ингенборг, старшей дочки вдовы, стояла перед ним на коленях и увлеченно у него отсасывала. "
        $ show_inga_front_fuck_image(1, 1)
        $ ViewIngaSex += 1
        $ IngaVar["SawLucassex"] = 1
        $ IngaVar["Knowher"] = max(1, IngaVar["Knowher"])
    elif RandIngaFuck == 2:
        if IngaVar["SawLucassex"] == 0:
            "Ваше любопытство оказалось вознагражденным интересной сценой: "
        else:
            "Вы увидели уже знакомую картину: "
        "в углу за крыльцом самозабвенно сношалась парочка. "
        if IngaVar["Knowher"] == 0:
            "Молодой парень "
        else:
            "Лукас, ухажер Ингенборг "
        "прижал к стене свою подружку, "
        if IngaVar["Knowher"] == 0:
            "какую-то рыжую деваху"
        else:
            "старшую дочку вдовушки, милашку Ингенборг"
        if pregnancy["inga"] >= 120:
            ", и, не смотря на то, что девица явно в положении, жарит ее раком, задрав той юбку."
        else:
            ", завернул ей юбку, спустил панталончики, приподнял и насадил на свой член."
        $ show_inga_front_fuck_image(2, 1)
        $ ViewIngaSex += 1
        $ IngaVar["SawLucassex"] = 1
        $ IngaVar["Knowher"] = max(1, IngaVar["Knowher"])
    else:
        "Наверное, показалось: вы заглянули за крыльцо, но там никого не было."
        call ShowImage("", "", becky_homefront_house_picture())
        $ ViewIngaSex = 10
    if ArriveMode == "FromDances" and RandIngaFuck <= 2:
        "Ваши наблюдения заинтересовали Бекки, которая решила проверить, на что это вы там смотрите."
    return

label becky_homefront_share_with_becky:
    "\"Бекки, смотри\", подозвали вы вдовушку, указав ей на сношающуюся парочку. Бекки подошла к вам и осторожно выглянула из-за угла."
    if BeckyVar["SawIngaFuck"] == 0:
        "\"Так это ж Ингенборг, дочка моя, с Лукасом, ухажером своим. Очень милый мальчик, он на ней даже жениться собирается. До дома не дотерпели, эх молодость-молодость!\""
    else:
        "\"Эх доченька бедная моя, тебе же наверное неудобно то, на камне. Ну да дело молодое!\""
    "- сказала Бекки, увидев парочку."
    if BeckyVar["visitedhome"] < 5:
        "\"Но ведь это значит, что дома скорее всего никого нет, так что пошли скорее внутрь, пока они нас не засекли!\" - добавила она."
    $ show_inga_front_fuck_image(RandIngaFuck, 2)
    $ BeckyVar["SawIngaFuck"] = 1
    $ IngaVar["Knowher"] = max(1, IngaVar["Knowher"])
    $ IngaVar["SawLucassex"] = 1
    $ ViewIngaSex += 1
    return

label becky_homefront_ignore:
    "Вы вернулись к вдове Блэнкеншип: \"А, кошка пробежала, ерунда\", сказали вы ей."
    if BeckyVar["visitedhome"] < 5:
        "\"А, ну тогда пошли скорее в дом, пока дети мои не вернулись,\" ответила вам Бекки, \"а то увидят, смеяться будут, мол мамке уже [age_girls.get('becky', 36)] лет, а она все с парнями гуляет.\""
    else:
        "\"А, ну тогда пошли скорее в дом, я уже и стол накрыла,\" ответила вам Бекки."
    $ ViewIngaSex = 10
    return

label becky_homefront_suggest_approach:
    if BeckyVar["visitedhome"] < 5:
        "Вы обернулись к вдове Блэнкеншип: \"Может подойдем к ним?\" спросили вы ее."
        "\"Да ты что, ведь тогда дочка меня с тобой увидит, вдруг смеяться будет, мол мамке уже [age_girls.get('becky', 36)] лет, а она все с парнями гуляет. Пошли лучше скорее в дом, пока они тут заняты.\""
        "И с этими словами она настойчиво потянула вас в сторону двери."
        $ ViewIngaSex = 10
    else:
        "\"Бекки, отчего бы тебе не поприветствовать дочу?\" - осведомились вы, и, преодолев слабое сопротивление вдовицы, подошли к влюбленной парочке."
        "\"Привет, детки,\" сказала им Бекки."
        "\"Инга, Лукас, привет, как дела?\" - вежливо осведомились вы."
        if pregnancy["inga"] >= 120:
            "\"Пока не родила!\" пошутил в ответ он, погладив округлившийся живот своей любовницы."
        else:
            "\"О, привет Стефан, здравствуйте миссис Блэнкеншип,\" - отозвался Лукас."
        if RandIngaFuck == 1:
            "Ингенборг же ничего не ответила, но отнюдь не из-за недостатка вежливости, а оттого, что ее ротик был занят внушительным органом ее жениха. Увидев вас со своей мамой она слегка покраснела, помахала вам рукой в знак приветствия, но члена изо рта не выпустила."
        else:
            "Инга же обладала меньшей выдержкой чем ее хахаль и густо покраснела, увидев мать. Впрочем, недостаточно густо, чтобы перестать. \"Мам, ах, привет, ах, Стефанчик, ах, и тебе приветик,\" - вымолвила Блэнкеншип-младшая."
        $ ViewIngaSex += 1
        call SlutFriendsIncrease("becky", 0, 0, 0, 45, 3, 1)
        call SlutFriendsIncrease("inga", 0, 0, 0, 45, 3, 1)
    return

label becky_homefront_watch_cum:
    if ArriveMode == "FromDances":
        "Вы вместе с Бекки с интересом продолжили наблюдать за совокупляющейся парочкой. Вдову такое зрелище, судя по всему, завело, и ее рука автоматически стала потирать промежность через платье, а на лице застыла улыбка."
        "Любовников же такое внимание возбудило, судя по всему, еще пуще."
    else:
        "Вы с интересом продолжили наблюдать за совокупляющейся парочкой. Любовников ваше внимание завело, судя по всему, еще больше."
    if RandIngaFuck == 1:
        "Косясь на вас, Ингенборг старательно продолжала работать ротиком над членом Лукаса и вскоре ее труды оказались вознаграждены: с блаженным вздохом парнишка кончил ей прямо в ротик."
        "Ей такой исход был явно не в первой, так как она проглотила все не поморщившись, облизала пухленькие губки и встала с колен."
        $ show_inga_front_fuck_image(3, 2 if ArriveMode == "FromDances" else 1)
    else:
        "Посматривая время от времени на вас, парочка стремительно приближалась к оргазму. И вот Лукас стал заполнять пещерку Инги своим семенем, а вслед за ним, мелко затрясшись, стала кончать и его партнерша."
        "Обмякший член Лукаса вывалился из влагалища Ингенборг, а та сразу же натянула панталончики, не давая сперме вытечь и запачкать платье."
        $ show_inga_front_fuck_image(2, 2 if ArriveMode == "FromDances" else 1)
    if ArriveMode == "FromDances":
        "\"Мам, Стефан, мы закончили, пойдем теперь в дом,\" как ни в чем не бывало предложила вам Инга."
        call SlutFriendsIncrease("becky", 0, 0, 0, 45, 3, 1)
    else:
        "\"Стефан, увидимся дома, нам надо еще кое что забрать,\" сказал вам Лукас, заправляя член обратно в штаны. И с этими словами парочка удалилась."
    if renpy.random.randint(1,2) == 1 and RandIngaFuck == 2 and BeckyVar["IngaSexGreet"] == 0 and ArriveMode == "FromDances":
        "\"Лукас, Ингочка, а что ж вы на улице, вам же небось неудобно?\" - резонно осведомилась у парочки Бекки."
        "\"Я же вам сказала, что можете у нас дома, не стесняйтесь.\""
        "\"Ой мам, ну ты сказанула. Лукас и стыд - вещи мало совместимые. Где он меня только не сношал. Это-то его и заводит, говорит что в одном месте скучно. Правда, милый?\""
        "\"Да, миссис Блэнкеншип,\" согласился Лукас, \"Инга все правильно говорит.\""
        "\"Ну, навязывать свой дом не буду,\" пошла на попятную Бекки, \"только смотрите, не простудитесь,\" заботливо поспешила добавить она."
        $ BeckyVar["IngaSexGreet"] = 1
    call SlutFriendsIncrease("inga", 0, 0, 0, 45, 3, 1)
    $ ViewIngaSex += 1
    return

label becky_homefront_approach:
    if IngaVar["Knowher"] < 2:
        "Вы решили нарушить уединение парочки. Подойдя к любовникам решительным шагом, вы нахально осведомились: \"А что это вы тут делаете, а?\""
        "\"Как что делаем, разве не видно?\" удивился парень. \"Я трахаю свою подружку.\""
        "\"Резонно, можно было бы и не спрашивать,\" подумали вы про себя, но набравшись наглости, вслух произнесли: \"Ну тогда я следующий!\""
        "Однако на ваш заход вы получили обескураживающий ответ: \"Ну, хотя я парней обычно не трахаю, для тебя могу сделать исключение.\""
        "\"Нет, нет, что вы, не надо исключений, будьте верны своим принципам,\" тут же нашлись вы."
        "И тут вы поняли, что разговариваете с пустотой: парень решил сосредоточиться на своей партнерше, а не на дискуссии с вами."
        $ ViewIngaSex = 10
    elif BeckyVar["visitedhome"] < 5:
        "Вы решили нарушить уединение парочки. Подойдя к Лукасу с Ингой решительным шагом, вы нахально осведомились: \"А что это вы тут делаете, а?\""
        "\"О, привет Стефан,\" - ответил Лукас вам как ни в чем не бывало. \"А сам-то что думаешь, что мы тут делаем?\" - задал он риторический вопрос."
        if RandIngaFuck == 1:
            "Ингенборг же в силу того, что ее ротик был занят внушительным органом ее жениха ничего вам не ответила, только помахнула вам рукой в знак приветствия, не выпуская члена изо рта."
        else:
            "Инга же обладала меньшей выдержкой чем ее хахаль и густо покраснела, увидев что вы их застали в момент секса."
        "\"Стефан, я тут как видишь несколько занят, если ты хочешь о чем-то поговорить, то давай я кончу и в доме поболтаем, лады?\" - добавил ваш знакомец."
        $ ViewIngaSex = 10
    else:
        "Вы решили поприветствовать ваших знакомых. Подойдя к ним, вы вежливо их поприветствовали: \"Инга, Лукас, привет, как дела?\""
        if pregnancy["inga"] >= 120:
            "\"Пока не родила!\" пошутил в ответ Лукас, погладив округлившийся живот своей любовницы."
        else:
            "\"О, привет Стефан,\" - отозвался Лукас."
        if RandIngaFuck == 1:
            "Ингенборг же ничего не ответила, но отнюдь не из-за недостатка вежливости, а оттого, что ее ротик был занят внушительным органом ее жениха. Увидев вас она слегка покраснела, помахала рукой в знак приветствия, но члена изо рта не выпустила."
        else:
            "При этом он ни на секунду не замедлил темпа, продолжая сношать Ингенборг. Та обернулась к вам и вежливо, хотя и несколько запыхавшись, поприветствовала вас: \"Стефанчик, ах, приветик, ах!\""
        $ ViewIngaSex = 3
    call SlutFriendsIncrease("inga", 0, 0, 0, 45, 3, 1)
    return

# --- END OF LOCATION ---
# All logic, menus, and event outcomes are now modular and maintainable.
# Further refinement and integration with the event system is possible as needed.

