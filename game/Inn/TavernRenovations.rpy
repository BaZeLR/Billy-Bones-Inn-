# Tavern owns construction; the thread records which follow-up scenes were played.
init -30 python:
    class TavernRenovationDefinition(object):
        def __init__(self, code, title, price, logs, days, description, quest_giver, room, payment_text="Драупнир принимает оплату и отмечает, сколько брёвен заберёт из сарая. Заказ принят."):
            self.code = code
            self.title = title
            self.price = price
            self.logs = logs
            self.days = days
            self.description = description
            self.quest_giver = quest_giver
            self.room = room
            self.payment_text = payment_text

        @property
        def order_visible(self):
            return tavern.renovations[self.code].status in ("accepted", "building", "completed")

        @property
        def quote(self):
            return "%s мараведи, %s бревен, срок — %s дн." % (self.price, self.logs, self.days)

    class TavernRenovation(object):
        def __init__(self, code):
            self.code = code
            self.status = "unrequested"
            self.requester = ""
            self.requested_day = -1
            self.started_day = -1
            self.due_day = -1
            self.completed_day = -1
            self.paid_maravedies = 0
            self.used_logs = 0

        def request(self, requester):
            if self.status == "unrequested":
                self.status = "requested"
                self.requester = requester
                self.requested_day = int(calendar_v2.daysInGame)

        def accept(self):
            if self.status == "requested":
                self.status = "accepted"

    class TavernInfo(object):
        def __init__(self):
            self.renovations = {code: TavernRenovation(code) for code in TAVERN_RENOVATIONS}

        def renovation_complete(self, code):
            return self.renovations[code].status == "completed"

        @property
        def active_renovation(self):
            return next((job for job in self.renovations.values() if job.status == "building"), None)

        @property
        def renovation_work_description(self):
            job = self.active_renovation
            if job is None:
                return ""
            return "Драупнир работает над заказом: %s. До окончания осталось дней: %s." % (TAVERN_RENOVATIONS[job.code].title, self.renovation_days_left(job.code))

        def renovation_days_left(self, code):
            job = self.renovations[code]
            return max(0, job.due_day - int(calendar_v2.daysInGame)) if job.status == "building" else 0

        def renovation_order_error(self, code):
            project = TAVERN_RENOVATIONS[code]
            job = self.renovations[code]
            if job.status in ("building", "completed"):
                return "Эта работа уже выполнена." if self.renovation_complete(code) else "Этот заказ уже выполняется."
            if job.status != "accepted":
                return "Сначала нужно принять просьбу об этом улучшении."
            if self.active_renovation is not None:
                return "Драупнир сначала должен закончить текущий заказ."
            if not rooms.get("StolyarWorkshop").is_open():
                return "Мастерская сейчас закрыта."
            if player.economy.money < project.price:
                return "Не хватает мараведи."
            if _room_item_count_by_id(rooms.get("Shed"), "lumber_001") < project.logs:
                return "Не хватает бревен в сарае. Колотые дрова для строительства не годятся."
            return ""

        def order_renovation(self, code):
            if self.renovation_order_error(code):
                return False
            project = TAVERN_RENOVATIONS[code]
            if not player.spend_money(project.price):
                return False
            for _ in range(project.logs):
                _room_remove_item_by_id(rooms.get("Shed"), "lumber_001")
            job = self.renovations[code]
            job.status = "building"
            job.started_day = int(calendar_v2.daysInGame)
            job.due_day = job.started_day + project.days
            job.paid_maravedies = project.price
            job.used_logs = project.logs
            return True

        def finish_due_renovations(self):
            today = int(calendar_v2.daysInGame)
            for job in self.renovations.values():
                if job.status != "building" or today < job.due_day:
                    continue
                job.status = "completed"
                job.completed_day = today
                for girl_id, info in people.girl_items():
                    if info.is_tavern_worker():
                        info.reward_need_fulfilled(1, "renovation_" + job.code)
                if job.requester != "player":
                    people.get_info(job.requester).reward_need_fulfilled(2, "renovation_" + job.code)

default tavern = TavernInfo()

define TAVERN_RENOVATIONS = {
    "sign": TavernRenovationDefinition("sign", "Ремонт вывески", 200, 0, 1, "Починить обветшавшую вывеску трактира.", "player", "StreetTavern", "Скрепя сердце вы отсчитали 200 мараведи мастеру Драупниру. Собрав свои инструменты работящий гном направил свои стопы к вашему трактиру."),
    "peephole": TavernRenovationDefinition("peephole", "Потайное окошко", 100, 0, 1, "Устроить в комнате хозяина потайное окошко для наблюдения за гостевой. Работа будет готова на следующий день.", "player", "TavernMyRoom", "Скрепя сердце вы отсчитали 100 мараведи мастеру Драупниру. Взяв с собой дрель, стамески, пилу и еще пару инструментов, работящий гном отправился к вашему трактиру. Потайное окошко будет готово на следующий день."),
    "glory_hole": TavernRenovationDefinition("glory_hole", "Глорихол", 700, 0, 1, "Устроить отдельную комнату с ширмой и занавесями.", "georgett", "TavernMain", "Жестоко задавив в себе жабу пока она еще была в состоянии головастика, вы отсчитали 700 мараведи мастеру Драупниру. Загрузив ослика досками, собрав в ящичек разнообразные инструменты, а в специальный мешок ткани для занавески, трудолюбивый гном потопал к вашему трактиру."),
    "roof": TavernRenovationDefinition("roof", "Починка крыши", 2000, 0, 2, "Заменить гнилые доски и заделать щели после изгнания летучих мышей.", "melissa", "TavernAtic", "Вы договариваетесь о починке старой крыши и отдаете за работу две тысячи монет. Теперь остается только дождаться, пока Драупнир перетянет гнилые доски, забьет щели и приведет верх трактира в порядок. Он обещает управиться за пару дней."),
    "backyard": TavernRenovationDefinition("backyard", "Благоустройство двора", 600, 8, 3, "Поправить забор и нужник, осушить дорожки, привести в порядок место для воды и хозяйственных работ.", "melissa", "Backyard"),
    "shed": TavernRenovationDefinition("shed", "Прачечная и купальня в сарае", 900, 12, 4, "Починить сарай и разделить его перегородкой. В одной части устроить прачечную и купальню, в другой — печь с баком горячей воды и раздельное хранение бревен и колотых дров.", "sandra", "Shed"),
    "guest_room": TavernRenovationDefinition("guest_room", "Ремонт гостевой комнаты", 700, 8, 3, "Привести в порядок стены и пол, поставить добротную кровать, шкаф и стол, повесить занавеси. Гостевая послужит и небольшой гостиной для спокойных бесед. Существующее оборудование комнаты останется на месте.", "clara", "TavernEmptyRoom"),
}

define tavernRenovationThreadList = [
    UThreadData(0, "tavern", "Renovations", None, [
        ([("story_tavern_renovation_request", None, None, None, 1, None,
         ["#people.location('%s') == rooms.current_code" % project.quest_giver,
          "#rooms.current.group_name == ROOM_GROUP_TAVERN",
          "#tavern.renovations['%s'].status in ('unrequested', 'requested')" % project.code]
         + (["#Clara.tavern_resident()"] if project.quest_giver == "clara" else []),
         None, "talk_" + project.quest_giver, "renovation", 60, True)] if project.code in ("backyard", "shed", "guest_room") else []) + [
        ("DraupnirRenovationOrder", None, None, None, 1, None,
         ["#tavern.renovations['%s'].status == 'accepted'" % project.code],
         None, "talk_draupnir", "renovation_" + project.code, 60, True),
        ("story_tavern_renovation_complete", None, None, None, 1, None,
         ["#tavern.renovation_complete('%s')" % project.code],
         None, project.room, "enter", 5),
        ] for project in TAVERN_RENOVATIONS.values()
    ], highlight=True, threaded=True)
]

init 5 python:
    ShedRuinedStoveObject = GameObject(
        object_id="shed_ruined_stove", name="Каморка со старой печью",
        description="В глубине сарая есть тесная каморка с наполовину развалившейся печью. В ее давно остывшем нутре может спрятаться взрослый человек.",
        picture="images/tavern/backyard/shed/ruined_stove_chamber.png",
        condition={"rule": "tavern_renovation", "code": "shed", "completed": False},
        actions=[ObjectAction(action_id="inspect_ruined_stove", label="Осмотреть каморку и печь", hook="call", target="ShedRuinedStove")],
    )
    ShedWashTubObject = GameObject(
        object_id="shed_wash_tub", name="Купель",
        description="Деревянная купель стоит отдельно от стирального корыта. Чистые полотенца лежат на полке; горячую воду приносят из соседнего хозяйственного помещения.",
        picture="images/tavern/backyard/shed/washroom.png",
        condition={"rule": "tavern_renovation", "code": "shed"},
        actions=[ObjectAction(action_id="use_shed_wash_tub", label="Вымыться", hook="call", target="ShedWashroomBath")],
    )
    ShedHotWaterStoveObject = GameObject(
        object_id="shed_hot_water_stove", name="Печь с водяным баком",
        description="Новая печь греет большой металлический бак. Бревна и колотые дрова сложены отдельно, на безопасном расстоянии от топки; запас топлива по-прежнему общий для хозяйства.",
        picture="images/tavern/backyard/shed/renovated.png",
        condition={"rule": "tavern_renovation", "code": "shed"},
        actions=[ObjectAction(action_id="inspect_shed_stove", label="Печь и запас дров", hook="call", target="ShedHotWaterStove")],
    )

# Each request resolves its own item, never aborting unrelated improvements.
label story_tavern_renovation_request:
    $ renpy.dynamic("_renovation")
    $ _renovation = next(project for project in TAVERN_RENOVATIONS.values() if project.code in ("backyard", "shed", "guest_room") and "talk_" + project.quest_giver == evt.location)
    $ tavern.renovations[_renovation.code].request(_renovation.quest_giver)
    $ main_ui_begin_native_scene_state(_renovation.title)
    show screen main_ui
    if _renovation.code == "shed":
        vscene "images/sandra/portrait2.jpg"
        "— Хозяин, нам нужна настоящая купальня, — говорит Сандра. — В сарае можно отделить комнату для стирки и мытья. Печь с баком горячей воды и дрова останутся за перегородкой: чистое бельё не должно лежать возле золы. Поговорите с Драупниром."
    elif _renovation.code == "backyard":
        vscene "images/melissa/melissa_portrait_0.jpg"
        "— Хотите знать, чего мне не хватает? Удобства в собственном доме, — отвечает Мелисса. — Во дворе грязь, дорожки разбиты, нужник пора чинить. Если Драупнир приведёт всё в порядок, нам и воду носить, и работать будет легче."
    else:
        vscene "images/clara/portrait.png"
        "— Раз уж я теперь живу здесь, скажу прямо: гостевую нужно привести в порядок, — заявляет Кларисса. — Кровать, шкаф, стол, занавеси — и получится приличная гостиная. Можно будет принимать гостей и беседовать, а не стоять посреди голых стен. Закажите ремонт Драупниру."
    menu:
        "Хорошо, закажу работу у Драупнира":
            $ event_runtime.active_thread.enable()
            $ tavern.renovations[_renovation.code].accept()
            "Вы соглашаетесь обсудить заказ с Драупниром. Деньги и строительные брёвна понадобятся при оплате работы."
        "Обсудим это позже":
            "Вы пока не даёте обещаний. К разговору можно будет вернуться позже."
        "Отказаться от этого улучшения":
            $ tavern.renovations[_renovation.code].status = "declined"
            $ event_runtime.active_thread.seen(list(TAVERN_RENOVATIONS).index(_renovation.code))
            "Вы решаете отказаться от этой затеи. Заказ мастеру передан не будет."
    menu:
        "Вернуться к разговору":
            pass
    $ main_ui_end_native_scene_state()
    return True

label DraupnirRenovations:
    $ main_ui_begin_native_scene_state("Обустройство трактира")
    vscene "images/draupnir/dwarf1.jpg"
    while True:
        menu:
            "Ремонт вывески" if TAVERN_RENOVATIONS["sign"].order_visible:
                call DraupnirRenovationOrder("sign")
            "Потайное окошко" if TAVERN_RENOVATIONS["peephole"].order_visible:
                call DraupnirRenovationOrder("peephole")
            "Глорихол" if TAVERN_RENOVATIONS["glory_hole"].order_visible:
                call DraupnirRenovationOrder("glory_hole")
            "Починка крыши" if TAVERN_RENOVATIONS["roof"].order_visible:
                call DraupnirRenovationOrder("roof")
            "Благоустройство двора" if TAVERN_RENOVATIONS["backyard"].order_visible:
                call DraupnirRenovationOrder("backyard")
            "Прачечная и купальня в сарае" if TAVERN_RENOVATIONS["shed"].order_visible:
                call DraupnirRenovationOrder("shed")
            "Ремонт гостевой комнаты" if TAVERN_RENOVATIONS["guest_room"].order_visible:
                call DraupnirRenovationOrder("guest_room")
            "Назад":
                $ main_ui_end_native_scene_state()
                return

label DraupnirRenovationOrder(code=None):
    $ renpy.dynamic("_renovation", "_renovation_error", "_renovation_quote", "_renovation_days")
    $ _renovation = TAVERN_RENOVATIONS[code if code is not None else evt.action[len("renovation_"):]]
    $ code = _renovation.code
    $ main_ui_begin_native_scene_state(_renovation.title)
    show screen main_ui
    vscene "images/draupnir/dwarf1.jpg"
    $ _renovation_quote = _renovation.description + "\n\n" + _renovation.quote
    "[_renovation_quote]"
    if tavern.renovations[code].status in ("building", "completed"):
        if tavern.renovation_complete(code):
            "Эта работа уже закончена."
        else:
            $ _renovation_days = tavern.renovation_days_left(code)
            "Заказ уже в работе. До окончания осталось дней: [_renovation_days]."
        menu:
            "Назад":
                pass
    else:
        $ _renovation_error = tavern.renovation_order_error(code)
        if _renovation_error:
            "[_renovation_error]"
        menu:
            "Заказать работу" if not _renovation_error:
                if tavern.order_renovation(code):
                    $ threads["tavernRenovations"].enable()
                    "[_renovation.payment_text]"
                    menu:
                        "Продолжить":
                            pass
            "Назад":
                pass
    $ main_ui_end_native_scene_state()
    return


# A completed building is inspected once; room entry only triggers this event.
label story_tavern_renovation_complete:
    $ renpy.dynamic("_renovation", "_renovation_picture")
    $ _renovation = next(project for project in TAVERN_RENOVATIONS.values() if project.room == evt.location)
    $ main_ui_begin_native_scene_state(_renovation.title)
    show screen main_ui
    if _renovation.code == "shed":
        $ _renovation_picture = shed_picture()
        vscene _renovation_picture
        "Драупнир закончил работу. Печь с баком и поленница остались в хозяйственной половине; за отдельной дверью теперь чистая прачечная с купальней."
    elif _renovation.code == "backyard":
        vscene "images/tavern/backyard/backyard_renewal.png"
        "Двор приведён в порядок: дорожки осушены, забор и нужник починены. Воду и хозяйственные припасы теперь можно носить без прежних неудобств."
    elif _renovation.code == "guest_room":
        vscene tavern_empty_room_picture()
        "Вместо пустой комнаты вас встречает уютная гостиная: добротная кровать, шкаф, стол и занавеси. Теперь здесь можно спокойно принять гостей."
    else:
        $ _renovation_picture = rooms.current.bg_picture
        vscene _renovation_picture
        if _renovation.code == "peephole":
            "Потайное окошко готово. Теперь из своей комнаты вы можете незаметно наблюдать за происходящим в гостевой."
        elif _renovation.code == "roof":
            "Драупнир заменил гнилые доски и заделал щели. Крыша над комнатой Мелиссы починена; теперь можно сообщить ей об этом."
        elif _renovation.code == "sign":
            "Вывеска починена. Теперь посетители снова смогут как следует разглядеть название вашего трактира."
        else:
            "Драупнир закончил работу: отдельная комната с ширмой и занавесями готова принимать посетителей."
    if _renovation.quest_giver != "player":
        "В трактире рады законченной работе. Особенно довольна та, кто просила об этом улучшении."
    menu:
        "Осмотреть готовую работу":
            $ event_runtime.active_thread.seen(list(TAVERN_RENOVATIONS).index(_renovation.code))
    $ main_ui_end_native_scene_state()
    return True

label ShedRuinedStove:
    $ main_ui_begin_native_scene_state(ShedRuinedStoveObject.name)
    if 6 <= int(calendar_v2.hour) < 20:
        vscene "images/tavern/backyard/shed/ruined_stove_chamber.png"
    else:
        vscene "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
    "За покосившейся перегородкой прячется каморка. Старая печь наполовину осыпалась, но под уцелевшим сводом осталось просторное темное нутро. Здесь давно не топили; если пригнуться, взрослый мужчина вполне поместится внутри."
    menu:
        "Заглянуть внутрь":
            "В глубине лежат только холодная зола и кирпичная крошка. Пока здесь никто не прячется. Топить такую печь нельзя — сначала ее нужно переложить."
            menu:
                "Назад":
                    pass
        "Назад":
            pass
    $ main_ui_end_native_scene_state()
    return

label ShedWashroomBath(object_id="shed_wash_tub"):
    $ main_ui_begin_native_scene_state(ShedWashTubObject.name)
    $ scene_runtime.picture = shed_washroom_picture()
    "В отдельной купальне можно спокойно вымыться. Корыто для белья стоит в стороне, на полке сложены чистые полотенца."
    menu:
        "Вымыться — 15 минут":
            $ player.appearance.wash()
            $ calendar_v2.advance_minutes(15)
            "Вы смываете с себя дорожную пыль и вытираетесь чистым полотенцем."
            menu:
                "Назад":
                    pass
        "Назад":
            pass
    $ main_ui_end_native_scene_state()
    return

label ShedHotWaterStove:
    $ main_ui_begin_native_scene_state(ShedHotWaterStoveObject.name)
    $ scene_runtime.picture = shed_picture()
    "На месте развалившейся печи теперь стоит крепко сложенная новая, с баком для горячей воды. В этом помещении есть два сухих места хранения: одно для целых бревен, другое для колотых дров. Дверь в перегородке ведет в отдельную прачечную с купальней."
    menu:
        "Назад":
            pass
    $ main_ui_end_native_scene_state()
    return
