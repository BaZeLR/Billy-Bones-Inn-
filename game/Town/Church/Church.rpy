default ChurchAfterCermon = {}
default PriestIncestAgree = 0
default ChurchPurityLastDay = -1
default ChurchPurityReport = {}    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n" + navigation_only_message() + "\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n" + navigation_only_message() + "\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
default ChurchAfterCermon = {}
default PriestIncestAgree = 0
default ChurchPurityLastDay = -1
default ChurchPurityReport = {}    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n" + navigation_only_message() + "\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n" + navigation_only_message() + "\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
default ChurchAfterCermon = {}
default PriestIncestAgree = 0
default ChurchPurityLastDay = -1
default ChurchPurityReport = {}    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n" + navigation_only_message() + "\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n" + navigation_only_message() + "\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init python:
    def church_call_label(label_name="", *label_args):
        label = str(label_name or "").strip()
        if label == "" or not renpy.has_label(label):
            return
        return renpy.call_in_new_context(label, *tuple(label_args or ()))

    def church_hyperlink_handler(value=""):
        parts = [str(row or "").strip() for row in str(value or "").split(":")]
        action_key = parts[0] if len(parts) > 0 else ""
        action_arg = parts[1] if len(parts) > 1 else ""
        if action_key == "service":
            return church_call_label("ChurchServiceMenu", action_arg != "0")
        if action_key == "confession":
            return church_call_label("ChurchIspoved", 1)
        if action_key == "confession_menu":
            return church_call_label("ChurchIspovedMenu")
        if action_key == "confession_menu":
            return church_call_label("ChurchIspovedMenu")
        if action_key == "after_cermon":
            return church_call_label("ChurchAfterCermon", 1)
        if action_key == "draupnir":
            return church_call_label("ShowChurchDraupnirList")
        if action_key == "after_becky":
            return church_call_label("AfterCermonBecky")

    config.hyperlink_handlers["church"] = church_hyperlink_handler

    def church_call_label(label_name="", *label_args):
        label = str(label_name or "").strip()
        if label == "" or not renpy.has_label(label):
            return
        return renpy.call_in_new_context(label, *tuple(label_args or ()))

    def church_hyperlink_handler(value=""):
        parts = [str(row or "").strip() for row in str(value or "").split(":")]
        action_key = parts[0] if len(parts) > 0 else ""
        action_arg = parts[1] if len(parts) > 1 else ""
        if action_key == "service":
            return church_call_label("ChurchServiceMenu", action_arg != "0")
        if action_key == "confession":
            return church_call_label("ChurchIspoved", 1)
        if action_key == "confession_menu":
            return church_call_label("ChurchIspovedMenu")
        if action_key == "confession_menu":
            return church_call_label("ChurchIspovedMenu")
        if action_key == "after_cermon":
            return church_call_label("ChurchAfterCermon", 1)
        if action_key == "draupnir":
            return church_call_label("ShowChurchDraupnirList")
        if action_key == "after_becky":
            return church_call_label("AfterCermonBecky")

    config.hyperlink_handlers["church"] = church_hyperlink_handler

    def church_call_label(label_name="", *label_args):
        label = str(label_name or "").strip()
        if label == "" or not renpy.has_label(label):
            return
        return renpy.call_in_new_context(label, *tuple(label_args or ()))

    def church_hyperlink_handler(value=""):
        parts = [str(row or "").strip() for row in str(value or "").split(":")]
        action_key = parts[0] if len(parts) > 0 else ""
        action_arg = parts[1] if len(parts) > 1 else ""
        if action_key == "service":
            return church_call_label("ChurchServiceMenu", action_arg != "0")
        if action_key == "confession":
            return church_call_label("ChurchIspoved", 1)
        if action_key == "confession_menu":
            return church_call_label("ChurchIspovedMenu")
        if action_key == "confession_menu":
            return church_call_label("ChurchIspovedMenu")
        if action_key == "after_cermon":
            return church_call_label("ChurchAfterCermon", 1)
        if action_key == "draupnir":
            return church_call_label("ShowChurchDraupnirList")
        if action_key == "after_becky":
            return church_call_label("AfterCermonBecky")

    config.hyperlink_handlers["church"] = church_hyperlink_handler

    def church_pick_picture(candidates=None):
        loadable = [str(row or "").strip() for row in list(candidates or []) if str(row or "").strip() != "" and renpy.loadable(str(row or "").strip())]
        if len(loadable) <= 0:
            return ""
        return loadable[procedural_randint(0, len(loadable) - 1, "church_pick_picture_%s" % people_to_int(dayspassed, 0))]

    def church_sandra_picture():
        return church_pick_picture([
            "images/sandra/church/church_sandra_0.jpg",
            "images/sandra/church/cermon.jpg",
        ])

    def church_sisters_picture():
        return church_pick_picture([
            "images/melissa/church/sisters.png",
            "images/amanda/church/amanda_church.png",
            "images/amanda/church/cermon.jpg",
        ])

    def church_blanken_picture():
        return church_pick_picture([
            "images/becky/church/cermon.jpg",
            "images/becky/church/talk1.jpg",
            "images/becky/church/talk2.jpg",
        ])

    def church_hour_now():
        try:
            return int(calendar_v2.hour or 0) % 24
        except Exception:
            return 0

    def church_hour_between(start_hour=0, end_hour=23):
        hour_value = church_hour_now()
        start_value = int(start_hour or 0) % 24
        end_value = int(end_hour or 0) % 24
        if start_value <= end_value:
            return start_value <= hour_value < end_value
        return hour_value >= start_value or hour_value < end_value

    def church_open_hours_visible():
        return week == 7 and church_hour_between(8, 13)

    def church_closed_description_visible():
        return not church_open_hours_visible()

    def church_service_description_visible():
        return church_open_hours_visible()

    def church_closed_time_visible():
        return not church_open_hours_visible()

    def church_service_action_visible():
        return week == 7 and church_hour_between(8, 10)

    def church_confession_action_visible():
        return week == 7 and church_hour_between(10, 11)

    def church_after_cermon_action_visible():
        return week == 7 and church_hour_between(11, 13)

    def church_becky_priest_talk_visible():
        return (
            church_confession_action_visible()
            and Becky.var.get("PriestAdvice", 0) > 0
            and Becky.var.get("GerhardBeckyTalk", 0) < 2
        )

    def church_draupnir_note_visible():
        return church_confession_action_visible() and Becky.var.get("GerhardBeckyTalk", 0) > 0

    def _church_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def church_purity_player_pressure_resistance():
        try:
            update_stat_state()
        except Exception:
            pass

        fight_value = 1
        try:
            if isinstance(FightLevel, dict):
                fight_value = _church_to_int(FightLevel.get("you", 1), 1)
        except Exception:
            fight_value = 1

        resistance = 0
        resistance += min(10, max(0, _church_to_int(charisma, 0) // 10))
        resistance += min(8, max(0, _church_to_int(notoriety, 0) // 12))
        resistance += min(8, max(0, _church_to_int(exploration, 0) // 12))
        resistance += min(6, max(0, fight_value - 1))
        return min(24, resistance)

    def church_purity_girl_keys():
        keys = []
        for raw_key in list(peopleInfo.keys() if isinstance(peopleInfo, dict) else []):
            key = str(raw_key or "").strip().lower()
            if key == "" or key == "you":
                continue
            info = getPersonInfo(key)
            if info is None or not hasattr(info, "corruption"):
                continue
            if _church_to_int(getattr(info, "corruption", 0), 0) <= 0:
                continue
            keys.append(key)
        return sorted(keys)

    def church_apply_sunday_purity():
        global ChurchPurityLastDay, ChurchPurityReport

        if not church_open_hours_visible():
            return {}

        today = _church_to_int(dayspassed, 0)
        if _church_to_int(ChurchPurityLastDay, -1) == today:
            if isinstance(ChurchPurityReport, dict):
                return dict(ChurchPurityReport)
            return {}

        ChurchPurityLastDay = today
        report = {}
        player_resistance = church_purity_player_pressure_resistance()

        for key in church_purity_girl_keys():
            info = getPersonInfo(key)
            if info is None:
                continue
            before_value = _church_to_int(getattr(info, "corruption", 0), 0)
            base_percent = procedural_randint(20, 60, "church_purity_%s_%s" % (key, today))
            openness_value = _church_to_int(getattr(info, "openness", 0), 0)
            friend_value = _church_to_int(getattr(info, "rel", 0), 0)
            relation_resistance = min(16, max(0, openness_value // 2) + max(0, friend_value // 3))
            effective_percent = max(20, min(60, base_percent - player_resistance - relation_resistance))
            reduction = max(1, int(round(float(before_value) * float(effective_percent) / 100.0)))
            after_value = max(0, before_value - reduction)
            info.corruption = after_value
            report[key] = {
                "before": before_value,
                "after": after_value,
                "base_percent": base_percent,
                "effective_percent": effective_percent,
                "reduction": before_value - after_value,
            }

        ChurchPurityReport = report
        if len(report) > 0:
            try:
                renpy.notify("Воскресная служба охладила пыл прихожанок.")
            except Exception:
                pass
        return dict(report)

    def church_purity_report_text():
        if not isinstance(ChurchPurityReport, dict) or len(ChurchPurityReport) <= 0:
            return ""
        if _church_to_int(ChurchPurityLastDay, -1) != _church_to_int(dayspassed, 0):
            return ""

        changed = []
        for key in sorted(list(ChurchPurityReport.keys())):
            row = dict(ChurchPurityReport.get(key, {}) or {})
            before_value = _church_to_int(row.get("before", 0), 0)
            after_value = _church_to_int(row.get("after", 0), 0)
            if before_value <= after_value:
                continue
            info = getPersonInfo(key)
            if info is not None and hasattr(info, "display_name"):
                name = str(info.display_name() or key)
            elif info is not None and hasattr(info, "data"):
                name = str(getattr(info.data, "fullname", key) or key)
            else:
                name = str(key or "")
            reduction = max(0, before_value - after_value)
            if reduction >= 18 or after_value <= before_value // 2:
                change_text = "заметно строже держит себя после службы"
            elif reduction >= 8:
                change_text = "держится сдержаннее после службы"
            else:
                change_text = "слегка одумалась после службы"
            changed.append("%s %s" % (name, change_text))

        if len(changed) <= 0:
            return ""
        return "Воскресная служба укрепила нравственный настрой прихожанок. " + "; ".join(changed) + "."

    def church_service_attendees_text():
        lines = [
            "Вы осматриваете собор во время воскресной службы.",
            "Отец Герхард ведет мессу, а в нефе и у колонн стоят знакомые семьи, городские торговцы, ремесленники и простые прихожане.",
        ]
        present = list(getNPCids("Church") or [])
        if len(present) > 0:
            names = []
            for npc_id in present:
                key = str(npc_id or "").strip()
                if key == "":
                    continue
                names.append(str(RealName.get(key, _action_display_name(key)) or _action_display_name(key)))
            if len(names) > 0:
                lines.append("Среди тех, кого вы можете узнать: " + ", ".join(names) + ".")
        lines.append("Если хотите присмотреться внимательнее, выберите кого искать среди прихожан.")
        purity_text = church_purity_report_text()
        if str(purity_text or "").strip():
            lines.append(str(purity_text or ""))
        return "\n\n".join(lines)

    ChurchRoom = Room(
        code_name="Church",
        group_name=ROOM_GROUP_CITY,
        display_name="Собор Ильматера",
        bg_picture="images/church/locChurchClosed_day.png",
        descriptions=[
            RoomDescription(
                text="Перед вами возвышается величественное здание городского собора, посвященного великому богу Ильматеру. Величественными башенками, шпилями, колоннами собор устремляется вверх, в небо. По воскресным утрам здесь собирается почти весь город. Однако сейчас собор закрыт.",
                condition=church_closed_description_visible,
                priority=300,
            ),
            RoomDescription(
                text="Вы пришли в великий городской собор Ильматера на воскресную службу.",
                condition=church_service_description_visible,
                priority=290,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        action_menus=[
            RoomAction(action_id="service_attendees", label="Прихожане", hook="ui_call", target="ChurchServiceMenu", args=(True,), condition=church_service_action_visible),
            RoomAction(action_id="becky_priest_talk", label="Обсудить сомнения Бекки со святым отцом", hook="ui_call", target="becky_church_talk", condition=church_becky_priest_talk_visible),
            RoomAction(action_id="confession", label="Идти на исповедь", hook="ui_call", target="ChurchIspoved", args=(1,), condition=church_confession_action_visible),
            RoomAction(action_id="draupnir_note", label="Посмотреть листок Драупнира", hook="ui_call", target="ShowChurchDraupnirList", condition=church_draupnir_note_visible),
            RoomAction(action_id="after_cermon_walk", label="Обойти собор", hook="ui_call", target="ChurchAfterCermon", args=(1,), condition=church_after_cermon_action_visible),
        ],
        schedule=RoomSchedule(
            weekdays=[7],
            start="08:00",
            end="12:59",
            closed_text="Перед вами возвышается величественное здание городского собора, посвященного великому богу Ильматеру. Величественными башенками, шпилями, колоннами собор устремляется вверх, в небо. По воскресным утрам здесь собирается почти весь город. Однако сейчас собор закрыт.",
        ),
        custom_properties={"service_location": True},
    )


label Church:
    scene black
    $ CurrentRoom = ChurchRoom
    $ CurLoc = "Church"
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ church_apply_sunday_purity()

    if not ChurchRoom.is_open():
        $ MainTxt = ChurchRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        vscene "images/church/locChurchClosed_day.png"
    else:
        if church_service_action_visible():
            $ MainTxt = "Вы пришли в великий городской собор Ильматера на воскресную службу.\n\nКажется, здесь собралось полгорода. Отец Герхард, жрец Ильматера, ведет службу. Ее вы видели и слышали уже сотни раз. Ваш взор обегает собор и прихожан."
            $ CurLocDesc = MainTxt
            vscene "images/church/churchEntryDay.png"
        elif church_confession_action_visible():
            $ MainTxt = "Служба закончилась, люди понемногу начали расходиться. Вы можете или пойти домой или пойти к отцу Герхарду на исповедь."
            if Becky.var.get("GerhardBeckyTalk", 0) > 0:
                $ MainTxt = MainTxt + "\nНа небольшом столике в углу лежит листок, на котором что-то накорябанно."
            $ CurLocDesc = MainTxt
            vscene "images/church/confessionEntry.png"
        else:
            $ MainTxt = "Почти все прихожане уже разошлись, однако собор еще открыт. Вы можете его обойти и посмотреть нет ли чего интересного."
            $ CurLocDesc = MainTxt
            vscene "images/church/confessionEntry.png"

    python:
        if ChurchRoom.is_open():
            for _church_action in ChurchRoom.visible_actions():
                _church_menu_item = room_action_menu_item(_church_action)
                if _church_menu_item is not None:
                    current_action_items.append(_church_menu_item)
        for _church_exit in ChurchRoom.visible_exits():
            current_action_items.append(MenuItem(_church_exit.label, Call("MoveToRoom", _church_exit.target, getattr(_church_exit, "minutes_to_pass", 5))))

    while True:
        call screen main_ui


label ChurchServiceMenu(show_attendees=True):
    if show_attendees:
        $ MainTxt = church_service_attendees_text()
        $ CurLocDesc = MainTxt
    $ current_action_title = "Прихожане"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Найти Сандру", Function(main_ui_call_label, "ChurchServiceMother")))
    $ current_action_items.append(MenuItem("Найти сестричек", Function(main_ui_call_label, "ChurchServiceSisters")))
    $ current_action_items.append(MenuItem("Найти семейство Легаре", Function(main_ui_call_label, "ChurchServiceLegare")))
    $ current_action_items.append(MenuItem("Найти семейство Блэнкеншип", Function(main_ui_call_label, "ChurchServiceBlanken")))
    if (bool(Georgett.known) or people_to_int(Georgett.rel, 0) > 0) and people_to_int(Georgett.rel, 0) >= 2:
        $ current_action_items.append(MenuItem("Найти Жоржетту Брюно", Function(main_ui_call_label, "ChurchServiceGeorgett")))
    $ current_action_items.append(MenuItem("Вернуться к службе", Jump("Church")))
    $ renpy.restart_interaction()
    return


label ChurchServiceMother:
    $ MainTxt = "Сандра, одетая в своё строгое платье, внимательно слушает службу."
    $ CurLocDesc = MainTxt
    $ _church_picture = church_sandra_picture()
    if str(_church_picture or "").strip():
        call ShowImage("", "", _church_picture)
    else:
        call ShowImage("sandra", "church", "cermon")
    call ChurchServiceMenu(False)
    return


label ChurchServiceSisters:
    $ MainTxt = "Мелисса и Аманда тихо щебечут между собой, уделяя происходящему куда меньше внимания, чем хотелось бы святому отцу."
    $ CurLocDesc = MainTxt
    $ _church_picture = church_sisters_picture()
    if str(_church_picture or "").strip():
        call ShowImage("", "", _church_picture)
    else:
        call ShowImage("amanda", "church", "cermon")
    call ChurchServiceMenu(False)
    return


label ChurchServiceLegare:
    if story_event_available("Church", "clara_paintings"):
        call checkTriggers("Church", "clara_paintings", 0)
        return
    $ MainTxt = "Мессир Легаре в черном камзоле стоит около одной из колонн и внимательно слушает службу. Рядом с ним стоит его жена Элоиза, маленькая шатенка средних лет, а за ними все их дети - Кларисса, Жерар, Жан-Жак, Полина и малыш Реми."
    $ CurLocDesc = MainTxt
    call ShowImageSeq("alber", "church", "cermon", 2)
    call ChurchServiceMenu(False)
    return


label ChurchServiceBlanken:
    $ MainTxt = "Вдова Блэнкеншип, высокая рыжая женщина с полной грудью, чуть младше сорока лет. Она на первый взгляд слушает отца Герхарда, но если присмотреться, то видно, что ее мысли витают где-то далеко. Рядом с ней стоит Эдди, ее рыжий управляющий лавкой и ваш ровесник. Поблизости ее дети - Ингенборг, Ивар, Эмма и Лаура."
    $ CurLocDesc = MainTxt
    $ _church_picture = church_blacken_picture()
    if str(_church_picture or "").strip():
        call ShowImage("", "", _church_picture)
    else:
        call ShowImage("becky", "church", "cermon")
    call ChurchServiceMenu(False)
    return


label becky_church_talk:
    if Becky.var.get("GerhardBeckyTalk", 0) == 0:
        $ MainTxt = "После службы вы подошли к отцу Герхарду: \"Падре, одна из ваших прихожанок, торговка с рынка, может обратиться к вам за советом. Снедает ее мысль о том, большой ли грех то, что она собирается совершить. Не могли ли бы вы сказать ей, что то невеликое дело?\""
    else:
        $ MainTxt = "После службы вы подошли к отцу Герхарду: \"Падре, та прихожанка о которой я вас спрашивал, ну та торговка с рынка, она к вам за советом случаем не подходила? И что же вы ей посоветовали?\""

    if Becky.var.get("PriestAdvice", 0) == 3:
        $ MainTxt = MainTxt + "\n\n\"Поговорил я с ней, сын мой,\" сказал вам святой отец улыбаясь. \"Прав ты был, что ее тревожило - то невеликое прегрешение. Мудр ты, сын мой, не по годам. Да и щедр преизрядно и к церкви нашей с должным пиететом относишься.\"\n\nИ, осенив вас знаком Ильматера, отец Герхард вернулся к своим делам."
    elif Becky.var.get("GerhardBeckyTalk", 0) == 0:
        $ MainTxt = MainTxt + "\n\n\"Да как ты смеешь, молокосос, указывать мне, настоятелю этого храма, как с моей паствой общаться?!\" справедливо возмутился почтенный жрец.\n\n\"Я выслушиваю своих прихожанок дольше, чем ты прожил на свете, и уж способен сам решить, велик грех или мал, без чьих-то советов.\"\n\nРасстроены отказом, вы уже собрались было уйти, как отец Герхард промолвил в пустоту, ни к кому конкретно не обращаясь:\n\n\"Эх, что за народ нынче пошел, никакого уважения к церкви. Собор-то наш поистрепался слегка, так я и попросил мастера Драупнира чтоб он, значит, ремонт-то небольшой сделал. Раньше-то что, любой бы за честь великую счел бы, что ему доверили храм великого Ильматера ремонтировать. А сейчас? Драупнир, шельмец, такой счет выставил, как будто он десять новых соборов построил. А народишко-то измельчал, жертвуют неохотно. Так этот счет и лежит неоплаченный, вон там,\" жрец махнул рукой куда-то в сторону.\n\nПрисмотревшись, вы заметили в указанном направлении какой-то листок."
    else:
        $ MainTxt = MainTxt + "\n\n\"Да как ты смеешь, молодой человек, на тайну исповеди посягать?! Я по твоему кто, настоятель этого великого храма или сплетник с базарной площади?\" разгневался достопочтенный.\n\nПолучив такую отповедь вы уже собрались было отправиться восвояси, как отец Герхард заметил:\n\n\"Эх, что за люди нынче? Раньше к падре с благовением обращались. А сейчас? Одному тайну исповеди раскрой, а этот шельмец, Драупнир, все деньги требует по счету. А откуда же я их возьму, коли никто не жертвует?\""

    $ CurLocDesc = MainTxt
    vscene "images/church/confessionEntry.png"
    $ Becky.var["GerhardBeckyTalk"] = 2
    jump Church
