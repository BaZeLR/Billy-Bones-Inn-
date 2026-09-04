# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# BeckyHomeFront.rpy
# Converted from legacy script. All features, menus, and event logic preserved.
# Dev notes and comments included for maintainability and future extension.

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
            return procedural_choice(loadable, key="procedural:Town/BeckyHomeFront.rpy:procedural_choice:35:1")
        return "images/becky/Home/house2.jpg"

    def becky_homefront_normal_desc():
        return rooms.get("BeckyHomeFront").state["arrival_mode"] != "FromDances"

    def becky_homefront_dance_desc():
        return rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances"

    def becky_homefront_guest_exit():
        return rooms.get("BeckyHomeFront").state["arrival_mode"] == "guest"

    BeckyHomeFrontRoomDefinition = Room(
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
        game_items=[],
        custom_properties={
            "house_front": True,
        },
        state={
            "arrival_mode": "",
            "inga_scene_roll": 1,
        },
    )

    def show_inga_front_fuck_image(type, with_becky):
        # type: 1=minet, 2=fuck, 3=minet cum
        # with_becky: 1=alone, 2=with Becky
        if type == 1:
            if with_becky == 2:
                show_image_seq("inga", "streetsex", "minetshow", 6)
            else:
                show_image_seq("inga", "streetsex", "minet", 5)
        elif type == 2:
            if with_becky == 2:
                if Inga.pregnancy_days() >= 120:
                    show_image("inga", "streetsex", "pregfuckshow")
                else:
                    show_image_seq("inga", "streetsex", "fuckshow", 3)
            else:
                if Inga.pregnancy_days() >= 120:
                    show_image("inga", "streetsex", "pregfuckyou")
                else:
                    show_image_seq("inga", "streetsex", "fuckyou", 5)
        else:
            if with_becky == 2:
                show_image_seq("inga", "streetsex", "cumfaceshow", 3)
            else:
                show_image("inga", "streetsex", "cumface")

# First-time dance arrival is the opening event of Becky's home thread.
label story_becky_home_arrival_0:
    "[rooms.get('BeckyHomeFront').descriptions[1].text]"
    call ShowImage("", "", becky_homefront_withbecky_picture())
    $ event_runtime.active_thread.advance()
    return


# --- MAIN LOCATION LABEL ---
label BeckyHomeFront(arrive_mode=""):
    $ renpy.dynamic("_becky_front_room")
    python:
        _becky_front_room = rooms.get("BeckyHomeFront")
        rooms.enter("BeckyHomeFront")
    $ rooms.get("BeckyHomeFront").state["arrival_mode"] = str(arrive_mode or "")
    $ rooms.get("BeckyHomeFront").state["inga_scene_roll"] = procedural_randint(1, 4, key="procedural:Town/BeckyHomeFront.rpy:entry_roll")
    if Becky.home_front_checked_today and rooms.get("BeckyHomeFront").state["inga_scene_roll"] <= 2:
        $ rooms.get("BeckyHomeFront").state["inga_scene_roll"] = 3
    $ Becky.home_front_checked_today = True
    if rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 1:
        $ pregnancy_check("inga", "mouthface", 1, "Лукас")
    elif rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 2:
        $ pregnancy_check("inga", "inside", 1, "Лукас")

    if rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances":
        if story_event_available("BeckyHomeFront", "enter"):
            call checkTriggers("BeckyHomeFront", "enter", 0)
        else:
            "[_becky_front_room.descriptions[1].text]"
            call ShowImage("", "", becky_homefront_withbecky_picture())
    else:
        "[_becky_front_room.descriptions[0].text]"
        call ShowImage("", "", becky_homefront_house_picture())
    $ _becky_front_room.mark_visited()

    if rooms.get("BeckyHomeFront").state["inga_scene_roll"] <= 3:
        "Вдруг какое-то движение в темном углу за крыльцом привлекло ваше внимание."
        "Что делать?"
    menu:
        "Зайти в дом":
            call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
            return

        "Вернуться к трактиру" if rooms.get("BeckyHomeFront").state["arrival_mode"] == "guest":
            jump StreetTavern

        "Осторожно заглянуть за угол" if rooms.get("BeckyHomeFront").state["inga_scene_roll"] <= 3:
            call becky_homefront_peek
            return

# --- SUBLABELS FOR MENU OPTIONS ---
label becky_homefront_peek:
    if rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 1:
        if not Inga.saw_lucas_sex:
            "Ваше любопытство оказалось вознагражденным интересной сценой: "
        else:
            "Вы увидели уже знакомую картину: "
        "в углу за крыльцом стоял, прислонившись к стене, "
        if Inga.acquaintance_stage == 0:
            "какой-то молодой парень. "
        else:
            "Лукас, ухажер Ингенборг. "
        "На его лице застыла блаженная гримаса..."
        if Inga.acquaintance_stage == 0:
            "рыжей девахи, стояла перед ним на коленях и увлеченно у него отсасывала. "
        else:
            "Ингенборг, старшей дочки вдовы, стояла перед ним на коленях и увлеченно у него отсасывала. "
        $ show_inga_front_fuck_image(1, 1)
        $ Inga.saw_lucas_sex = True
        $ Inga.acquaintance_stage = max(Inga.acquaintance_stage, 1)
    elif rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 2:
        if not Inga.saw_lucas_sex:
            "Ваше любопытство оказалось вознагражденным интересной сценой: "
        else:
            "Вы увидели уже знакомую картину: "
        "в углу за крыльцом самозабвенно сношалась парочка. "
        if Inga.acquaintance_stage == 0:
            "Молодой парень "
        else:
            "Лукас, ухажер Ингенборг "
        "прижал к стене свою подружку, "
        if Inga.acquaintance_stage == 0:
            "какую-то рыжую деваху"
        else:
            "старшую дочку вдовушки, милашку Ингенборг"
        if Inga.pregnancy_days() >= 120:
            ", и, не смотря на то, что девица явно в положении, жарит ее раком, задрав той юбку."
        else:
            ", завернул ей юбку, спустил панталончики, приподнял и насадил на свой член."
        $ show_inga_front_fuck_image(2, 1)
        $ Inga.saw_lucas_sex = True
        $ Inga.acquaintance_stage = max(Inga.acquaintance_stage, 1)
    else:
        "Наверное, показалось: вы заглянули за крыльцо, но там никого не было."
        call ShowImage("", "", becky_homefront_house_picture())

    if rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances" and rooms.get("BeckyHomeFront").state["inga_scene_roll"] <= 2:
        "Ваши наблюдения заинтересовали Бекки, которая решила проверить, на что это вы там смотрите."

    if rooms.get("BeckyHomeFront").state["inga_scene_roll"] > 2:
        menu:
            "Зайти в дом":
                call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
                return

            "Вернуться к трактиру" if rooms.get("BeckyHomeFront").state["arrival_mode"] == "guest":
                jump StreetTavern

    elif rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances":
        menu:
            "Зайти в дом":
                call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
                return

            "Поделится с вдовой своим открытием":
                if story_event_available("BeckyHomeFront", "inga_discovery"):
                    call checkTriggers("BeckyHomeFront", "inga_discovery", 0)
                else:
                    call becky_homefront_share_with_becky
                return

            "Сделать вид, что ничего там нет":
                call becky_homefront_ignore
                return

    elif rooms.get("BeckyHomeFront").state["arrival_mode"] == "":
        menu:
            "Зайти в дом":
                call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
                return

            "Подойти к парочке":
                call becky_homefront_approach
                return

    else:
        menu:
            "Зайти в дом":
                call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
                return

            "Вернуться к трактиру" if rooms.get("BeckyHomeFront").state["arrival_mode"] == "guest":
                jump StreetTavern
    return

label becky_homefront_share_with_becky:
    $ renpy.dynamic("_becky_inga_thread", "_becky_inga_first_discovery")
    $ _becky_inga_thread = threads.get("beckyIngaLucasPath", None)
    $ _becky_inga_first_discovery = _becky_inga_thread is not None and int(_becky_inga_thread.num or 0) == 0
    "\"Бекки, смотри\", подозвали вы вдовушку, указав ей на сношающуюся парочку. Бекки подошла к вам и осторожно выглянула из-за угла."
    if _becky_inga_first_discovery:
        "\"Так это ж Ингенборг, дочка моя, с Лукасом, ухажером своим. Очень милый мальчик, он на ней даже жениться собирается. До дома не дотерпели, эх молодость-молодость!\""
    else:
        "\"Эх доченька бедная моя, тебе же наверное неудобно то, на камне. Ну да дело молодое!\""
    "- сказала Бекки, увидев парочку."
    if int(threads["beckyDinner"].num or 0) < 2:
        "\"Но ведь это значит, что дома скорее всего никого нет, так что пошли скорее внутрь, пока они нас не засекли!\" - добавила она."
    $ show_inga_front_fuck_image(rooms.get("BeckyHomeFront").state["inga_scene_roll"], 2)
    $ Inga.acquaintance_stage = max(Inga.acquaintance_stage, 1)
    $ Inga.saw_lucas_sex = True
    if _becky_inga_first_discovery and event_runtime.active_thread is _becky_inga_thread:
        $ _becky_inga_thread.advance()

    menu:
        "Зайти в дом":
            call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
            return

        "Предложить подойти к парочке":
            call becky_homefront_suggest_approach
            return
    return

label becky_homefront_ignore:
    "Вы вернулись к вдове Блэнкеншип: \"А, кошка пробежала, ерунда\", сказали вы ей."
    if int(threads["beckyDinner"].num or 0) < 2:
        "\"А, ну тогда пошли скорее в дом, пока дети мои не вернулись,\" ответила вам Бекки, \"а то увидят, смеяться будут, мол мамке уже [people_age('becky', 36)] лет, а она все с парнями гуляет.\""
    else:
        "\"А, ну тогда пошли скорее в дом, я уже и стол накрыла,\" ответила вам Бекки."

    menu:
        "Зайти в дом":
            call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
            return
    return

label becky_homefront_suggest_approach:
    if int(threads["beckyDinner"].num or 0) < 2:
        "Вы обернулись к вдове Блэнкеншип: \"Может подойдем к ним?\" спросили вы ее."
        "\"Да ты что, ведь тогда дочка меня с тобой увидит, вдруг смеяться будет, мол мамке уже [people_age('becky', 36)] лет, а она все с парнями гуляет. Пошли лучше скорее в дом, пока они тут заняты.\""
        "И с этими словами она настойчиво потянула вас в сторону двери."
    else:
        "\"Бекки, отчего бы тебе не поприветствовать дочу?\" - осведомились вы, и, преодолев слабое сопротивление вдовицы, подошли к влюбленной парочке."
        "\"Привет, детки,\" сказала им Бекки."
        "\"Инга, Лукас, привет, как дела?\" - вежливо осведомились вы."
        if Inga.pregnancy_days() >= 120:
            "\"Пока не родила!\" пошутил в ответ он, погладив округлившийся живот своей любовницы."
        else:
            "\"О, привет Стефан, здравствуйте миссис Блэнкеншип,\" - отозвался Лукас."
        if rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 1:
            "Ингенборг же ничего не ответила, но отнюдь не из-за недостатка вежливости, а оттого, что ее ротик был занят внушительным органом ее жениха. Увидев вас со своей мамой она слегка покраснела, помахала вам рукой в знак приветствия, но члена изо рта не выпустила."
        else:
            "Инга же обладала меньшей выдержкой чем ее хахаль и густо покраснела, увидев мать. Впрочем, недостаточно густо, чтобы перестать. \"Мам, ах, привет, ах, Стефанчик, ах, и тебе приветик,\" - вымолвила Блэнкеншип-младшая."
        $ Becky.apply_social_roll(0, 0, 0, 45, 3, 1)
        $ Inga.apply_social_chance(0, 0, 0, 45, 3, 1, "becky_homefront_suggest")

    if int(threads["beckyDinner"].num or 0) < 2:
        menu:
            "Зайти в дом":
                call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
                return
    else:
        menu:
            "Зайти в дом":
                call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
                return

            "Посмотреть как они кончат":
                call becky_homefront_watch_cum
                return
    return

label becky_homefront_watch_cum:
    if rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances":
        "Вы вместе с Бекки с интересом продолжили наблюдать за совокупляющейся парочкой. Вдову такое зрелище, судя по всему, завело, и ее рука автоматически стала потирать промежность через платье, а на лице застыла улыбка."
        "Любовников же такое внимание возбудило, судя по всему, еще пуще."
    else:
        "Вы с интересом продолжили наблюдать за совокупляющейся парочкой. Любовников ваше внимание завело, судя по всему, еще больше."
    if rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 1:
        "Косясь на вас, Ингенборг старательно продолжала работать ротиком над членом Лукаса и вскоре ее труды оказались вознаграждены: с блаженным вздохом парнишка кончил ей прямо в ротик."
        "Ей такой исход был явно не в первой, так как она проглотила все не поморщившись, облизала пухленькие губки и встала с колен."
        $ show_inga_front_fuck_image(3, 2 if rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances" else 1)
    else:
        "Посматривая время от времени на вас, парочка стремительно приближалась к оргазму. И вот Лукас стал заполнять пещерку Инги своим семенем, а вслед за ним, мелко затрясшись, стала кончать и его партнерша."
        "Обмякший член Лукаса вывалился из влагалища Ингенборг, а та сразу же натянула панталончики, не давая сперме вытечь и запачкать платье."
        $ show_inga_front_fuck_image(2, 2 if rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances" else 1)
    if rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances":
        "\"Мам, Стефан, мы закончили, пойдем теперь в дом,\" как ни в чем не бывало предложила вам Инга."
        $ Becky.apply_social_roll(0, 0, 0, 45, 3, 1)
    else:
        "\"Стефан, увидимся дома, нам надо еще кое что забрать,\" сказал вам Лукас, заправляя член обратно в штаны. И с этими словами парочка удалилась."
    if procedural_randint(1,2, key="procedural:Town/BeckyHomeFront.rpy:procedural_randint:326:2") == 1 and rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 2 and not Becky.inga_sex_greeting_seen and rooms.get("BeckyHomeFront").state["arrival_mode"] == "FromDances":
        "\"Лукас, Ингочка, а что ж вы на улице, вам же небось неудобно?\" - резонно осведомилась у парочки Бекки."
        "\"Я же вам сказала, что можете у нас дома, не стесняйтесь.\""
        "\"Ой мам, ну ты сказанула. Лукас и стыд - вещи мало совместимые. Где он меня только не сношал. Это-то его и заводит, говорит что в одном месте скучно. Правда, милый?\""
        "\"Да, миссис Блэнкеншип,\" согласился Лукас, \"Инга все правильно говорит.\""
        "\"Ну, навязывать свой дом не буду,\" пошла на попятную Бекки, \"только смотрите, не простудитесь,\" заботливо поспешила добавить она."
        $ Becky.inga_sex_greeting_seen = True
    $ Inga.apply_social_chance(0, 0, 0, 45, 3, 1, "becky_homefront_watch")

    menu:
        "Зайти в дом":
            call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
            return
    return

label becky_homefront_approach:
    if Inga.acquaintance_stage < 2:
        "Вы решили нарушить уединение парочки. Подойдя к любовникам решительным шагом, вы нахально осведомились: \"А что это вы тут делаете, а?\""
        "\"Как что делаем, разве не видно?\" удивился парень. \"Я трахаю свою подружку.\""
        "\"Резонно, можно было бы и не спрашивать,\" подумали вы про себя, но набравшись наглости, вслух произнесли: \"Ну тогда я следующий!\""
        "Однако на ваш заход вы получили обескураживающий ответ: \"Ну, хотя я парней обычно не трахаю, для тебя могу сделать исключение.\""
        "\"Нет, нет, что вы, не надо исключений, будьте верны своим принципам,\" тут же нашлись вы."
        "И тут вы поняли, что разговариваете с пустотой: парень решил сосредоточиться на своей партнерше, а не на дискуссии с вами."
    elif int(threads["beckyDinner"].num or 0) < 2:
        "Вы решили нарушить уединение парочки. Подойдя к Лукасу с Ингой решительным шагом, вы нахально осведомились: \"А что это вы тут делаете, а?\""
        "\"О, привет Стефан,\" - ответил Лукас вам как ни в чем не бывало. \"А сам-то что думаешь, что мы тут делаем?\" - задал он риторический вопрос."
        if rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 1:
            "Ингенборг же в силу того, что ее ротик был занят внушительным органом ее жениха ничего вам не ответила, только помахнула вам рукой в знак приветствия, не выпуская члена изо рта."
        else:
            "Инга же обладала меньшей выдержкой чем ее хахаль и густо покраснела, увидев что вы их застали в момент секса."
        "\"Стефан, я тут как видишь несколько занят, если ты хочешь о чем-то поговорить, то давай я кончу и в доме поболтаем, лады?\" - добавил ваш знакомец."
    else:
        "Вы решили поприветствовать ваших знакомых. Подойдя к ним, вы вежливо их поприветствовали: \"Инга, Лукас, привет, как дела?\""
        if Inga.pregnancy_days() >= 120:
            "\"Пока не родила!\" пошутил в ответ Лукас, погладив округлившийся живот своей любовницы."
        else:
            "\"О, привет Стефан,\" - отозвался Лукас."
        if rooms.get("BeckyHomeFront").state["inga_scene_roll"] == 1:
            "Ингенборг же ничего не ответила, но отнюдь не из-за недостатка вежливости, а оттого, что ее ротик был занят внушительным органом ее жениха. Увидев вас она слегка покраснела, помахала рукой в знак приветствия, но члена изо рта не выпустила."
        else:
            "При этом он ни на секунду не замедлил темпа, продолжая сношать Ингенборг. Та обернулась к вам и вежливо, хотя и несколько запыхавшись, поприветствовала вас: \"Стефанчик, ах, приветик, ах!\""
    $ Inga.apply_social_chance(0, 0, 0, 45, 3, 1, "becky_homefront_approach")

    if Inga.acquaintance_stage >= 2 and int(threads["beckyDinner"].num or 0) >= 2:
        menu:
            "Зайти в дом":
                call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
                return

            "Посмотреть как они кончат":
                call becky_homefront_watch_cum
                return
    else:
        menu:
            "Зайти в дом":
                call BeckyHome(rooms.get("BeckyHomeFront").state["arrival_mode"])
                return
    return

# --- END OF LOCATION ---
