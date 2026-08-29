# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init python:
    def church_pick_picture(candidates=None):
        loadable = [str(row or "").strip() for row in list(candidates or []) if str(row or "").strip() != "" and renpy.loadable(str(row or "").strip())]
        if len(loadable) <= 0:
            return ""
        return loadable[procedural_randint(0, len(loadable) - 1, "church_pick_picture_%s" % int(current_game_day()))]

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

    def church_minutes_now():
        return (int(calendar_v2.hour or 0) % 24) * 60 + (int(calendar_v2.minute or 0) % 60)

    def church_minutes_between(start_minute=0, end_minute=1439):
        return int(start_minute or 0) <= church_minutes_now() <= int(end_minute or 1439)

    def church_closed_picture():
        if church_minutes_between(6 * 60, 17 * 60 + 59):
            return "images/church/locChurchClosed_day.png"
        return "images/church/locChurchClosed_night.png"

    def church_open_hours_visible():
        return int(calendar_v2.week or 0) == 7 and church_minutes_between(8 * 60, 12 * 60 + 59)

    def church_closed_description_visible():
        return not church_open_hours_visible()

    def church_service_description_visible():
        return church_open_hours_visible()

    def church_closed_time_visible():
        return not church_open_hours_visible()

    def church_service_action_visible():
        return int(calendar_v2.week or 0) == 7 and church_minutes_between(8 * 60, 9 * 60 + 29)

    def church_confession_action_visible():
        return int(calendar_v2.week or 0) == 7 and church_minutes_between(9 * 60 + 30, 10 * 60 + 59)

    def church_after_cermon_action_visible():
        return int(calendar_v2.week or 0) == 7 and church_minutes_between(11 * 60, 12 * 60 + 59)

    def church_becky_priest_talk_visible():
        return (
            church_confession_action_visible()
            and Becky.priest_advice_stage > 0
            and Becky.gerhard_talk_stage < 2
        )

    def church_draupnir_note_visible():
        return church_confession_action_visible() and Becky.gerhard_talk_stage > 0

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

        fight_value = fight_player_level()

        resistance = 0
        resistance += min(10, max(0, _church_to_int(player_charisma_breakdown().get("charisma", 0), 0) // 10))
        resistance += min(8, max(0, _church_to_int(player.stats.notoriety, 0) // 12))
        resistance += min(8, max(0, _church_to_int(player.stats.exploration, 0) // 12))
        resistance += min(6, max(0, fight_value - 1))
        return min(24, resistance)

    def church_purity_girl_keys():
        keys = []
        for raw_key in people.ids():
            key = str(raw_key or "").strip().lower()
            if key == "" or key == "you":
                continue
            info = people.get_info(key)
            if info is None or not hasattr(info, "corruption"):
                continue
            if _church_to_int(getattr(info, "corruption", 0), 0) <= 0:
                continue
            keys.append(key)
        return sorted(keys)

    def church_apply_sunday_purity():
        if not church_open_hours_visible():
            return {}

        today = int(current_game_day())
        if _church_to_int(rooms.get("Church").state.get("purity_last_day", -1), -1) == today:
            return dict(rooms.get("Church").state.get("purity_report", {}) or {})

        rooms.get("Church").state["purity_last_day"] = today
        report = {}
        player_resistance = church_purity_player_pressure_resistance()

        for key in church_purity_girl_keys():
            info = people.get_info(key)
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

        rooms.get("Church").state["purity_report"] = dict(report)
        if len(report) > 0:
            renpy.notify("Воскресная служба охладила пыл прихожанок.")
        return dict(report)

    def church_purity_report_text():
        report = dict(rooms.get("Church").state.get("purity_report", {}) or {})
        if len(report) <= 0:
            return ""
        if _church_to_int(rooms.get("Church").state.get("purity_last_day", -1), -1) != int(current_game_day()):
            return ""

        changed = []
        for key in sorted(list(report.keys())):
            row = dict(report.get(key, {}) or {})
            before_value = _church_to_int(row.get("before", 0), 0)
            after_value = _church_to_int(row.get("after", 0), 0)
            if before_value <= after_value:
                continue
            info = people.get_info(key)
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
        present = list(people.ids_at("Church") or [])
        if len(present) > 0:
            names = []
            for npc_id in present:
                key = str(npc_id or "").strip()
                if key == "":
                    continue
                names.append(str(people_display_name(key) or _action_display_name(key)))
            if len(names) > 0:
                lines.append("Среди тех, кого вы можете узнать: " + ", ".join(names) + ".")
        lines.append("Если хотите присмотреться внимательнее, выберите кого искать среди прихожан.")
        purity_text = church_purity_report_text()
        if str(purity_text or "").strip():
            lines.append(str(purity_text or ""))
        return "\n\n".join(lines)

    ChurchRoomDefinition = Room(
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
            RoomAction(action_id="draupnir_note", label="Посмотреть листок Драупнира", hook="ui_call", target="ShowChurchDraupnirList", condition=church_draupnir_note_visible),
            RoomAction(action_id="after_cermon_walk", label="Обойти собор", hook="ui_call", target="ChurchAfterCermon", args=(1,), condition=church_after_cermon_action_visible),
        ],
        schedule=RoomSchedule(
            weekdays=[7],
            start="08:00",
            end="12:59",
            closed_text="Перед вами возвышается величественное здание городского собора, посвященного великому богу Ильматеру. Величественными башенками, шпилями, колоннами собор устремляется вверх, в небо. По воскресным утрам здесь собирается почти весь город. Однако сейчас собор закрыт.",
        ),
        state={"purity_last_day": -1, "purity_report": {}},
        custom_properties={"service_location": True},
    )


label Church:
    $ renpy.dynamic("_church_action", "_church_exit", "_church_menu_item")
    scene black
    $ rooms.enter("Church")
    $ Georgett.set_story_value("foundinchurch", 0)
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    $ church_apply_sunday_purity()

    if not rooms.get("Church").is_open():
        $ scene_runtime.text = rooms.get("Church").schedule.closed_text
        $ scene_runtime.location_text = scene_runtime.text
        vscene church_closed_picture()
    else:
        if church_service_action_visible():
            $ scene_runtime.text = "Вы пришли в великий городской собор Ильматера на воскресную службу.\n\nКажется, здесь собралось полгорода. Отец Герхард, жрец Ильматера, ведет службу. Ее вы видели и слышали уже сотни раз. Ваш взор обегает собор и прихожан."
            $ scene_runtime.location_text = scene_runtime.text
            vscene "images/church/churchEntryDay.png"
        elif church_confession_action_visible():
            $ scene_runtime.text = "Служба закончилась, люди понемногу начали расходиться. Вы можете или пойти домой или пойти к отцу Герхарду на исповедь."
            if Becky.gerhard_talk_stage > 0:
                $ scene_runtime.text = scene_runtime.text + "\nНа небольшом столике в углу лежит листок, на котором что-то накорябанно."
            $ scene_runtime.location_text = scene_runtime.text
            vscene "images/church/confessionEntry.png"
        else:
            $ scene_runtime.text = "Почти все прихожане уже разошлись, однако собор еще открыт. Вы можете его обойти и посмотреть нет ли чего интересного."
            $ scene_runtime.location_text = scene_runtime.text
            vscene "images/church/confessionEntry.png"

    python:
        if rooms.get("Church").is_open():
            for _church_action in rooms.get("Church").visible_actions():
                _church_menu_item = room_action_menu_item(_church_action)
                if _church_menu_item is not None:
                    main_ui_runtime.action_items.append(_church_menu_item)
        for _church_exit in rooms.get("Church").visible_exits():
            main_ui_runtime.action_items.append(MenuItem(_church_exit.label, movement_actions(_church_exit.target, getattr(_church_exit, "minutes_to_pass", 5))))

    while True:
        call screen main_ui


label ChurchServiceMenu(show_attendees=True):
    if show_attendees:
        $ scene_runtime.text = church_service_attendees_text()
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Прихожане"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.action_items.append(MenuItem("Найти Сандру", Call("ChurchServiceMother")))
    $ main_ui_runtime.action_items.append(MenuItem("Найти сестричек", Call("ChurchServiceSisters")))
    $ main_ui_runtime.action_items.append(MenuItem("Найти семейство Легаре", Call("ChurchServiceLegare")))
    $ main_ui_runtime.action_items.append(MenuItem("Найти семейство Блэнкеншип", Call("ChurchServiceBlanken")))
    if people_to_int(Georgett.rel, 0) >= 2:
        $ main_ui_runtime.action_items.append(MenuItem("Найти Жоржетту Брюно", Call("ChurchServiceGeorgett")))
    if player.intimacy.can_cum() and people_to_int(Georgett.rel, 0) >= 2 and people_to_int(Georgett.sex_stat("sexacts", 0), 0) >= 3 and people_to_int(Georgett.story_value("foundinchurch", 0), 0) > 0:
        $ main_ui_runtime.action_items.append(MenuItem("Предложить Жоржетте перепихнуться по быстрому", Call("ChurchGeorgettQuickSex")))
    $ main_ui_runtime.action_items.append(MenuItem("Вернуться к службе", Jump("Church")))
    $ renpy.restart_interaction()
    return


label ChurchServiceMother:
    $ renpy.dynamic("_church_picture")
    $ scene_runtime.text = "Сандра, одетая в своё строгое платье, внимательно слушает службу."
    $ scene_runtime.location_text = scene_runtime.text
    $ _church_picture = church_sandra_picture()
    if str(_church_picture or "").strip():
        call ShowImage("", "", _church_picture)
    else:
        call ShowImage("sandra", "church", "cermon")
    call ChurchServiceMenu(False)
    return


label ChurchServiceSisters:
    $ renpy.dynamic("_church_picture")
    $ scene_runtime.text = "Мелисса и Аманда тихо щебечут между собой, уделяя происходящему куда меньше внимания, чем хотелось бы святому отцу."
    $ scene_runtime.location_text = scene_runtime.text
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
    $ scene_runtime.text = "Мессир Легаре в черном камзоле стоит около одной из колонн и внимательно слушает службу. Рядом с ним стоит его жена Элоиза, маленькая шатенка средних лет, а за ними все их дети - Кларисса, Жерар, Жан-Жак, Полина и малыш Реми."
    $ scene_runtime.location_text = scene_runtime.text
    call ShowImageSeq("alber", "church", "cermon", 2)
    call ChurchServiceMenu(False)
    return


label ChurchServiceBlanken:
    $ renpy.dynamic("_church_picture")
    $ scene_runtime.text = "Вдова Блэнкеншип, высокая рыжая женщина с полной грудью, чуть младше сорока лет. Она на первый взгляд слушает отца Герхарда, но если присмотреться, то видно, что ее мысли витают где-то далеко. Рядом с ней стоит Эдди, ее рыжий управляющий лавкой и ваш ровесник. Поблизости ее дети - Ингенборг, Ивар, Эмма и Лаура."
    $ scene_runtime.location_text = scene_runtime.text
    $ _church_picture = church_blanken_picture()
    if str(_church_picture or "").strip():
        call ShowImage("", "", _church_picture)
    else:
        call ShowImage("becky", "church", "cermon")
    call ChurchServiceMenu(False)
    return


label becky_church_talk:
    if Becky.gerhard_talk_stage == 0:
        $ scene_runtime.text = "После службы вы подошли к отцу Герхарду: \"Падре, одна из ваших прихожанок, торговка с рынка, может обратиться к вам за советом. Снедает ее мысль о том, большой ли грех то, что она собирается совершить. Не могли ли бы вы сказать ей, что то невеликое дело?\""
    else:
        $ scene_runtime.text = "После службы вы подошли к отцу Герхарду: \"Падре, та прихожанка о которой я вас спрашивал, ну та торговка с рынка, она к вам за советом случаем не подходила? И что же вы ей посоветовали?\""

    if Becky.priest_advice_stage == 3:
        $ scene_runtime.text = scene_runtime.text + "\n\n\"Поговорил я с ней, сын мой,\" сказал вам святой отец улыбаясь. \"Прав ты был, что ее тревожило - то невеликое прегрешение. Мудр ты, сын мой, не по годам. Да и щедр преизрядно и к церкви нашей с должным пиететом относишься.\"\n\nИ, осенив вас знаком Ильматера, отец Герхард вернулся к своим делам."
    elif Becky.gerhard_talk_stage == 0:
        $ scene_runtime.text = scene_runtime.text + "\n\n\"Да как ты смеешь, молокосос, указывать мне, настоятелю этого храма, как с моей паствой общаться?!\" справедливо возмутился почтенный жрец.\n\n\"Я выслушиваю своих прихожанок дольше, чем ты прожил на свете, и уж способен сам решить, велик грех или мал, без чьих-то советов.\"\n\nРасстроены отказом, вы уже собрались было уйти, как отец Герхард промолвил в пустоту, ни к кому конкретно не обращаясь:\n\n\"Эх, что за народ нынче пошел, никакого уважения к церкви. Собор-то наш поистрепался слегка, так я и попросил мастера Драупнира чтоб он, значит, ремонт-то небольшой сделал. Раньше-то что, любой бы за честь великую счел бы, что ему доверили храм великого Ильматера ремонтировать. А сейчас? Драупнир, шельмец, такой счет выставил, как будто он десять новых соборов построил. А народишко-то измельчал, жертвуют неохотно. Так этот счет и лежит неоплаченный, вон там,\" жрец махнул рукой куда-то в сторону.\n\nПрисмотревшись, вы заметили в указанном направлении какой-то листок."
    else:
        $ scene_runtime.text = scene_runtime.text + "\n\n\"Да как ты смеешь, молодой человек, на тайну исповеди посягать?! Я по твоему кто, настоятель этого великого храма или сплетник с базарной площади?\" разгневался достопочтенный.\n\nПолучив такую отповедь вы уже собрались было отправиться восвояси, как отец Герхард заметил:\n\n\"Эх, что за люди нынче? Раньше к падре с благовением обращались. А сейчас? Одному тайну исповеди раскрой, а этот шельмец, Драупнир, все деньги требует по счету. А откуда же я их возьму, коли никто не жертвует?\""

    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/gerhard/talkTogerhardt.png"
    $ Becky.gerhard_talk_stage = 2
    return
