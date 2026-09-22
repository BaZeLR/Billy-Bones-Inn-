# Draupnir's new renovation catalog. The tavern object owns paid dates;
# rooms and objects only project that state. Existing construction is unchanged.
init -30 python:
    class TavernRenovationDefinition(object):
        def __init__(self, code, title, price, logs, days, description, quest_giver="", is_hidden=True):
            self.code = code
            self.title = title
            self.price = price
            self.logs = logs
            self.days = days
            self.description = description
            self.quest_giver = quest_giver
            self.is_hidden = bool(is_hidden)

        @property
        def quote(self):
            return "%s мараведи, %s бревен, срок — %s дн." % (self.price, self.logs, self.days)

    class TavernInfo(object):
        def __init__(self):
            # One saved completion date per job. Request conversations are deferred.
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
            if project.is_hidden:
                return "Этот заказ пока недоступен."
            if code in self.renovation_due_days:
                return "Эта работа уже выполнена." if self.renovation_complete(code) else "Этот заказ уже выполняется."
            if not rooms.get("StolyarWorkshop").is_open():
                return "Мастерская сейчас закрыта."
            if code == "player_peephole" and not self.renovation_complete("guest_room"):
                return "Сначала нужно закончить ремонт гостевой комнаты."
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
    "backyard": TavernRenovationDefinition("backyard", "Благоустройство двора", 600, 8, 3, "Поправить забор и нужник, осушить дорожки, привести в порядок место для воды и хозяйственных работ.", "melissa"),
    "shed": TavernRenovationDefinition("shed", "Прачечная и купальня в сарае", 900, 12, 4, "Починить сарай и разделить его перегородкой. В одной части устроить прачечную и купальню, в другой — печь с баком горячей воды и раздельное хранение бревен и колотых дров.", "sandra"),
    "guest_room": TavernRenovationDefinition("guest_room", "Ремонт гостевой комнаты", 700, 8, 3, "Привести в порядок стены и пол, поставить добротную кровать, шкаф и стол, повесить занавеси. Гостевая послужит и небольшой гостиной для спокойных бесед. Существующее оборудование комнаты останется на месте.", "clara"),
    "player_peephole": TavernRenovationDefinition("player_peephole", "Потайное окошко из вашей комнаты", 100, 1, 1, "После ремонта гостевой комнаты устроить в вашей комнате маленькое обзорное отверстие с деревянной заслонкой. Старое окошко для наблюдения за посетителями это не заменяет."),
}

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
    TavernMyRoomPeepholeObject = GameObject(
        object_id="myroom_guest_peephole", name="Потайное окошко в гостевую",
        description="Драупнир спрятал в стене маленькое окошко с плотно подогнанной деревянной заслонкой. Оно выходит в гостевую комнату.",
        condition={"rule": "tavern_renovation", "code": "player_peephole"},
        actions=[ObjectAction(action_id="peek_guest_room", label="Посмотреть в гостевую комнату", hook="call", target="TavernMyRoomPeephole")],
    )

label DraupnirRenovations:
    $ main_ui_begin_native_scene_state("Обустройство трактира")
    vscene "images/draupnir/dwarf1.jpg"
    while True:
        menu:
            "Благоустройство двора" if not TAVERN_RENOVATIONS["backyard"].is_hidden:
                call DraupnirRenovationOrder("backyard")
            "Прачечная и купальня в сарае" if not TAVERN_RENOVATIONS["shed"].is_hidden:
                call DraupnirRenovationOrder("shed")
            "Ремонт гостевой комнаты" if not TAVERN_RENOVATIONS["guest_room"].is_hidden:
                call DraupnirRenovationOrder("guest_room")
            "Потайное окошко из вашей комнаты" if not TAVERN_RENOVATIONS["player_peephole"].is_hidden:
                call DraupnirRenovationOrder("player_peephole")
            "Назад":
                $ main_ui_end_native_scene_state()
                return

label DraupnirRenovationOrder(code):
    $ renpy.dynamic("_renovation", "_renovation_error", "_renovation_quote", "_renovation_days")
    $ _renovation = TAVERN_RENOVATIONS[code]
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
                $ tavern.order_renovation(code)
            "Назад":
                pass
    $ main_ui_runtime.action_title = "Обустройство трактира"
    return

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

label TavernMyRoomPeephole:
    $ renpy.dynamic("_peephole_client")
    $ main_ui_begin_native_scene_state(TavernMyRoomPeepholeObject.name)
    $ scene_runtime.picture = tavern_empty_room_picture()
    "Вы осторожно отодвигаете заслонку и смотрите в гостевую комнату, оставаясь у себя."
    menu:
        "Посмотреть внимательнее":
            $ _peephole_client = str(rooms.get("TavernMain").state.get("client_room_girl", "") or "")
            if player.tavern_management.isTavernOpen and _peephole_client and CheckIfSexEventExist(_peephole_client, calendar_v2.time_slot(), "Prostitution") > 0:
                call TavernProstClientsWatch(1, _peephole_client, "TavernMyRoom", calendar_v2.time_slot())
            else:
                "В гостевой сейчас тихо. Через отверстие видны кровать, стол и край занавеси."
                menu:
                    "Закрыть окошко":
                        pass
        "Закрыть окошко":
            pass
    $ main_ui_end_native_scene_state()
    return
