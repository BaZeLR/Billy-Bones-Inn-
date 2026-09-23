# Threads own requests and outcomes; the tavern owns construction dates.
init -30 python:
    class TavernRenovationDefinition(object):
        def __init__(self, code, title, price, logs, days, description, quest_giver, room):
            self.code = code
            self.title = title
            self.price = price
            self.logs = logs
            self.days = days
            self.description = description
            self.quest_giver = quest_giver
            self.room = room

        @property
        def thread_name(self):
            return self.quest_giver + "TavernRenovation"

        @property
        def order_visible(self):
            thread = threads[self.thread_name]
            return thread.num > 0 and not thread.aborted

        @property
        def quote(self):
            return "%s мараведи, %s бревен, срок — %s дн." % (self.price, self.logs, self.days)

    class TavernInfo(object):
        def __init__(self):
            # Physical construction dates, not a second quest-progress store.
            self.renovation_due_days = {}

        def renovation_complete(self, code, day=None):
            due = int(self.renovation_due_days.get(code, -1))
            today = int(calendar_v2.daysInGame if day is None else day)
            return due >= 0 and today >= due

        def renovation_days_left(self, code):
            due = int(self.renovation_due_days.get(code, -1))
            return max(0, due - int(calendar_v2.daysInGame)) if due >= 0 else 0

        def renovation_order_error(self, code):
            project = TAVERN_RENOVATIONS[code]
            if code in self.renovation_due_days:
                return "Эта работа уже выполнена." if self.renovation_complete(code) else "Этот заказ уже выполняется."
            thread = threads[project.thread_name]
            if not thread.checkActive() or thread.num != 1:
                return "Сначала нужно принять просьбу об этом улучшении."
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
            player.spend_money(project.price)
            for _ in range(project.logs):
                _room_remove_item_by_id(rooms.get("Shed"), "lumber_001")
            self.renovation_due_days[code] = int(calendar_v2.daysInGame) + project.days
            return True

default tavern = TavernInfo()

define TAVERN_RENOVATIONS = {
    "backyard": TavernRenovationDefinition("backyard", "Благоустройство двора", 600, 8, 3, "Поправить забор и нужник, осушить дорожки, привести в порядок место для воды и хозяйственных работ.", "melissa", "Backyard"),
    "shed": TavernRenovationDefinition("shed", "Прачечная и купальня в сарае", 900, 12, 4, "Починить сарай и разделить его перегородкой. В одной части устроить прачечную и купальню, в другой — печь с баком горячей воды и раздельное хранение бревен и колотых дров.", "sandra", "Shed"),
    "guest_room": TavernRenovationDefinition("guest_room", "Ремонт гостевой комнаты", 700, 8, 3, "Привести в порядок стены и пол, поставить добротную кровать, шкаф и стол, повесить занавеси. Гостевая послужит и небольшой гостиной для спокойных бесед. Существующее оборудование комнаты останется на месте.", "clara", "TavernEmptyRoom"),
}

define tavernRenovationThreadList = [
    LThreadData(0, project.quest_giver, "TavernRenovation", None, [
        ("story_tavern_renovation_request", None, None, None, 1, None,
         ["#people.location('%s') == rooms.current_code" % project.quest_giver,
          "#rooms.current.group_name == ROOM_GROUP_TAVERN"]
         + (["#Clara.tavern_resident()"] if project.quest_giver == "clara" else []),
         None, "talk_" + project.quest_giver, "renovation", 60),
        ("DraupnirRenovationOrder", None, None, None, 1, None, None,
         None, "talk_draupnir", "renovation_" + project.code, 60, True),
        ("story_tavern_renovation_complete", None, None, None, 1, None,
         ["#tavern.renovation_complete('%s')" % project.code],
         None, project.room, "enter", 5),
    ], highlight=True, threaded=True)
    for project in TAVERN_RENOVATIONS.values()
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

# Accept advances to the order; postpone repeats later; refusal aborts the quest.
label story_tavern_renovation_request:
    $ renpy.dynamic("_renovation")
    $ _renovation = next(project for project in TAVERN_RENOVATIONS.values() if project.thread_name == event_runtime.active_thread.data.name)
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
            $ event_runtime.active_thread.advance()
            "Вы соглашаетесь обсудить заказ с Драупниром. Деньги и строительные брёвна понадобятся при оплате работы."
        "Обсудим это позже":
            "Вы пока не даёте обещаний. К разговору можно будет вернуться позже."
        "Отказаться от этого улучшения":
            $ event_runtime.active_thread.abort()
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
            "Благоустройство двора" if TAVERN_RENOVATIONS["backyard"].order_visible:
                if story_event_available("talk_draupnir", "renovation_backyard"):
                    call checkTriggers("talk_draupnir", "renovation_backyard", 0)
                else:
                    call DraupnirRenovationOrder("backyard")
            "Прачечная и купальня в сарае" if TAVERN_RENOVATIONS["shed"].order_visible:
                if story_event_available("talk_draupnir", "renovation_shed"):
                    call checkTriggers("talk_draupnir", "renovation_shed", 0)
                else:
                    call DraupnirRenovationOrder("shed")
            "Ремонт гостевой комнаты" if TAVERN_RENOVATIONS["guest_room"].order_visible:
                if story_event_available("talk_draupnir", "renovation_guest_room"):
                    call checkTriggers("talk_draupnir", "renovation_guest_room", 0)
                else:
                    call DraupnirRenovationOrder("guest_room")
            "Назад":
                $ main_ui_end_native_scene_state()
                return

label DraupnirRenovationOrder(code=None):
    $ renpy.dynamic("_renovation", "_renovation_error", "_renovation_quote", "_renovation_days")
    $ _renovation = TAVERN_RENOVATIONS[code] if code is not None else next(project for project in TAVERN_RENOVATIONS.values() if project.thread_name == event_runtime.active_thread.data.name)
    $ code = _renovation.code
    $ main_ui_runtime.action_title = _renovation.title
    $ _renovation_quote = _renovation.description + "\n\n" + _renovation.quote
    "[_renovation_quote]"
    if code in tavern.renovation_due_days:
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
                    $ threads[_renovation.thread_name].advance()
                    "Драупнир принимает оплату и отмечает, сколько брёвен заберёт из сарая. Заказ принят."
                    menu:
                        "Продолжить":
                            pass
            "Назад":
                pass
    $ main_ui_runtime.action_title = "Обустройство трактира"
    return


# A completed building is inspected once; room entry only triggers this event.
label story_tavern_renovation_complete:
    $ renpy.dynamic("_renovation", "_renovation_picture")
    $ _renovation = next(project for project in TAVERN_RENOVATIONS.values() if project.thread_name == event_runtime.active_thread.data.name)
    $ main_ui_begin_native_scene_state(_renovation.title)
    show screen main_ui
    if _renovation.code == "shed":
        $ _renovation_picture = shed_picture()
        vscene _renovation_picture
        "Драупнир закончил работу. Печь с баком и поленница остались в хозяйственной половине; за отдельной дверью теперь чистая прачечная с купальней."
    elif _renovation.code == "backyard":
        vscene "images/tavern/backyard/backyard_renewal.png"
        "Двор приведён в порядок: дорожки осушены, забор и нужник починены. Воду и хозяйственные припасы теперь можно носить без прежних неудобств."
    else:
        vscene "images/amanda/Room/emptyroom.jpg"
        "Вместо пустой комнаты вас встречает уютная гостиная: добротная кровать, шкаф, стол и занавеси. Теперь здесь можно спокойно принять гостей."
    menu:
        "Осмотреть готовую работу":
            if _renovation.code == "shed":
                $ rooms.get("ShedWashroom").is_hidden = False
            $ event_runtime.active_thread.complete()
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
