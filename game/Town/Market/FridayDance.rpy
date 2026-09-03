# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Event Location: FridayDance (Market Square Friday Night Event)
# Converted from legacy script. Handles chained events and dynamic menu logic.
# To be called from the main event dispatcher or location system.

init 6 python:
    class FridayDanceRoom(Room):
        def __init__(self, *args, **kwargs):
            super(FridayDanceRoom, self).__init__(*args, **kwargs)
            self.state.setdefault("dance_count", 0)
            self.state.setdefault("becky_home_invited", False)
            self.state.setdefault("step", 0)
            self.state.setdefault("hands", "")
            self.state.setdefault("kiss", 0)
            self.state.setdefault("tits", 0)
            self.state.setdefault("max_step", 6)

        @property
        def dance_count(self):
            return int(self.state.get("dance_count", 0) or 0)

        @dance_count.setter
        def dance_count(self, value):
            self.state["dance_count"] = max(0, int(value or 0))

        @property
        def becky_home_invited(self):
            return bool(self.state.get("becky_home_invited", False))

        @becky_home_invited.setter
        def becky_home_invited(self, value):
            self.state["becky_home_invited"] = bool(value)

        @property
        def step(self):
            return int(self.state.get("step", 0) or 0)

        @step.setter
        def step(self, value):
            self.state["step"] = max(0, int(value or 0))

        @property
        def hands(self):
            return str(self.state.get("hands", "") or "")

        @hands.setter
        def hands(self, value):
            self.state["hands"] = str(value or "")

        @property
        def kiss(self):
            return int(self.state.get("kiss", 0) or 0)

        @kiss.setter
        def kiss(self, value):
            self.state["kiss"] = max(0, int(value or 0))

        @property
        def tits(self):
            return int(self.state.get("tits", 0) or 0)

        @tits.setter
        def tits(self, value):
            self.state["tits"] = max(0, int(value or 0))

        @property
        def max_step(self):
            return max(1, int(self.state.get("max_step", 6) or 6))

        @max_step.setter
        def max_step(self, value):
            self.state["max_step"] = max(1, int(value or 6))

        def market_entry_is_active(self):
            return self.is_open() and self.dance_count < 5

    FridayDanceRoomDefinition = FridayDanceRoom(
        code_name="FridayDance",
        display_name="Пятничные танцы",
        bg_picture="images/market/LocFridayDance.jpg",
        schedule=RoomSchedule(weekdays=[5], start="18:00", end="21:59"),
        state={},
        group_name="city",
    )

label FridayDance(add_dance_phrase_tmp=""):
    $ renpy.dynamic("rand_friday_dance", "result", "_friday_dance_finish_minute", "_friday_dance_minutes_remaining")
    $ rooms.enter("FridayDance")

    if not rooms.get("FridayDance").is_open():
        jump StreetTavern

    $ rooms.get("FridayDance").step = 0
    call checkTriggers("FridayDance", "enter", 0)

    while True:
        $ rooms.get("FridayDance").step = 0

        if rooms.get("FridayDance").dance_count < 5:
            call ShowImage("", "", "images/market/LocFridayDance.jpg")
            "Вы находитесь на рыночной площади. Сейчас вечер пятницы и площадь расчищена от лотков и палаток, которые занимают ее в обычное время. На стенах домов, на колоннах, в общем всюду, висят факелы освещающие праздник хоть и тусклым и колеблющимся, но светом. А народу, похоже, собралось больше чем днем. Кажется полгорода пришло сюда послушать музыку, которую играет маленький оркестр, стоящий на возвышении в центре площади. Ну и конечно потанцевать, куда же без этого. "
            call FridayDanceCounterShow
            if player.tavern_management.dance_sponsor == 1:
                "В северо-восточном углу площади, под навесом с изображением вставшего на дыбы жеребца, такого же как на вывеске вашего трактира, раздают вино и закуску. Бесплатная выпивка приманивает толпы народа, которые, после посещения вашего ларька, отправляются праздновать дальше уже под шофе, что придает веселью дополнительный колорит."
                python hide:
                    for girl_name in AllGirlNames:
                        get_girl_drunk(girl_name)
            "Вы видите всех своих знакомых. Что вы собираетесь делать?"
            menu friday_dance_menu:
                "Понаблюдать за танцующими" if rooms.get("FridayDance").dance_count < 5 and rooms.get("FridayDance").step == 0:
                    $ rand_friday_dance = procedural_randint(1, 8, key="procedural:Town/Market/FridayDance.rpy:procedural_randint:52:1")
                    if rand_friday_dance == 1:
                        $ result = "Вы замечаете как молодая пара, танцуя, сливается в страстном поцелуе."
                    elif rand_friday_dance == 2:
                        $ result = "Вы смотрите на танцующие парочки. Ваше внимание привлекает одна пара: парень потихоньку перемещает руку с талии на задницу девушки, она же в ответ прижимается к нему еще теснее."
                    elif rand_friday_dance == 3 and player.tavern_management.dance_sponsor == 1:
                        $ result = "Ваша внимание привлекает одна пара: такое впечатление что они забыли о том, что находятся не наедине. Парень во время танца мнет ягодицы своей партнерши, а та, в свою очередь трется о него своей полной грудью. Вы присмотрелись внимательней, и заметили, что раскрасневшаяся шалунья пытается незаметно тереть бугор на оттопыренных штанах парня. Во время очередного круга парень впивается в губы девушки и она ему страстно отвечает."
                    elif rand_friday_dance == 4 and player.tavern_management.dance_sponsor == 1:
                        $ result = "Вы замечаете ушлого парня, который танцует сразу с двумя девицами, по всей видимости сестрами. И позволяет себе много вольностей, то как бы нечаяно заденет за грудь, то потискает попу через юбку, то чмокнет в губы. Сестрицам такой подход по видимому нравятся, они весело смеются и обнимают своего ухажера."
                    else:
                        $ result = "Вы наблюдаете за тем, как народ весело отплясывает под разухабистые мелодии."
                    call ShowImage("", "", "images/market/LocFridayDance.jpg")
                    $ rooms.get("FridayDance").dance_count += 1
                    "[result]"
                    call FridayDanceCounterShow
                "Найти Аманду" if story_event_available("FridayDance", "amanda_dance_legare") or story_event_available("FridayDance", "amanda_dance_mc"):
                    if CheckIfDanceExist('amanda', 'legare', rooms.get("FridayDance").dance_count) > 0:
                        call checkTriggers("FridayDance", "amanda_dance_legare", 0)
                    else:
                        call checkTriggers("FridayDance", "amanda_dance_mc", 0)
                "Найти Бекки Блэнкеншип" if story_event_available("FridayDance", "becky_dance_mc"):
                    call checkTriggers("FridayDance", "becky_dance_mc", 0)
                "Заметить Мелиссу и Клариссу среди танцующих" if rooms.get("FridayDance").dance_count < 5 and rooms.get("FridayDance").step == 0 and Clara.visible_at_friday_dance() and str(people.location("melissa") or "") == "FridayDance":
                    $ rooms.get("FridayDance").dance_count += 1
                    if Clara.can_start_social_events():
                        $ result = "Среди танцующих вы замечаете Мелиссу и Клариссу. Девушки смеются, кружатся под музыку и явно чувствуют себя на празднике совершенно свободно. Кларисса, заметив ваш взгляд, на миг улыбается вам поверх плеча подруги."
                    else:
                        $ result = "Среди танцующих вы замечаете Мелиссу и Клариссу. Девушки весело кружатся под музыку и о чем-то шепчутся между собой, а вы пока лишь наблюдаете за ними со стороны."
                    "[result]"
                    call FridayDanceCounterShow
        else:
            $ _friday_dance_finish_minute = rooms.get("FridayDance").schedule._clock_value(rooms.get("FridayDance").schedule.end, 21 * 60 + 59) + 1
            $ _friday_dance_minutes_remaining = max(0, _friday_dance_finish_minute - int(calendar_v2.clock_minutes() or 0))
            call AdvanceTimeOnly(_friday_dance_minutes_remaining)
            jump MarketPlace

    return

label CheckIfAmandaGoneDance:
    if int(rooms.get("FridayDance").dance_count or 0) <= 0:
        return
    if GetDanceJustLeft("amanda", "legare", rooms.get("FridayDance").dance_count) > 0 or Amanda.legare_departure_code == 1:
        $ Amanda.legare_departure_code = 0
        if procedural_randint(1, 2, key="procedural:Town/Market/FridayDance.rpy:procedural_randint:107:2") == 1:
            $ Amanda.left_friday_dance = True
            "Неожиданно вы заметили, что Аманда торопиться куда-то прочь под ручку с мессиром Легаре."
            call LegareAmandaGoMenu
        else:
            $ Amanda.resolve_legare_let_go()
            $ Amanda.escaped_dance_unnoticed = True
    return


label FridayDanceCounterShow:
    if rooms.get("FridayDance").dance_count < 5:
        "Осталось еще [5-rooms.get('FridayDance').dance_count] танцев, до того как все разойдутся."
    else:
        "Праздник закончился и народ расходится."
    call CheckIfAmandaGoneDance
    return

