# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default ChurchAfterCermon = {}
default PriestIncestAgree = 0
default ChurchPurityLastDay = -1
default ChurchPurityReport = {}

init python:
    import random

    def church_pick_picture(candidates=None):
        loadable = [str(row or "").strip() for row in list(candidates or []) if str(row or "").strip() != "" and renpy.loadable(str(row or "").strip())]
        return random.choice(loadable) if len(loadable) > 0 else ""

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

    def church_closed_description_visible():
        return week != 7 or time > 2

    def church_service_description_visible():
        return week == 7 and time <= 2

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
        try:
            source_keys = list(sluttiness.keys())
        except Exception:
            source_keys = []

        for raw_key in source_keys:
            key = str(raw_key or "").strip()
            if key == "" or key.lower() == "you":
                continue
            if _church_to_int(sluttiness.get(key, 0), 0) <= 0:
                continue
            try:
                if _church_to_int(age_girls.get(key, 0), 0) < 18:
                    continue
            except Exception:
                continue
            keys.append(key)
        return sorted(keys)

    def church_apply_sunday_purity():
        global ChurchPurityLastDay, ChurchPurityReport

        if _church_to_int(week, 0) != 7 or _church_to_int(time, 0) > 2:
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
            before_value = _church_to_int(sluttiness.get(key, 0), 0)
            base_percent = random.randint(20, 60)
            openness_value = _church_to_int(otkroven.get(key, 0), 0)
            friend_value = _church_to_int(Friends.get(key, 0), 0)
            relation_resistance = min(16, max(0, openness_value // 2) + max(0, friend_value // 3))
            effective_percent = max(20, min(60, base_percent - player_resistance - relation_resistance))
            reduction = max(1, int(round(float(before_value) * float(effective_percent) / 100.0)))
            after_value = max(0, before_value - reduction)
            sluttiness[key] = after_value
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
            name = str(RealName.get(key, key) or key)
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

    ChurchRoom = Room(
        code_name="Church",
        group_name=ROOM_GROUP_CITY,
        display_name="Собор Ильматера",
        bg_picture="images/general/LocChurchClosed1.jpg",
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
        schedule=RoomSchedule(
            weekdays=[7],
            time_slots=[0, 1, 2],
            closed_text="Перед вами возвышается величественное здание городского собора, посвященного великому богу Ильматеру. Величественными башенками, шпилями, колоннами собор устремляется вверх, в небо. По воскресным утрам здесь собирается почти весь город. Однако сейчас собор закрыт.",
        ),
        custom_properties={"service_location": True},
    )


label Church:
    scene black
    call EnterLocation("Church")
    $ CurrentRoom = ChurchRoom
    $ CurLoc = "Church"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ GeorgettVar["foundinchurch"] = 0
    $ church_apply_sunday_purity()
    call ChurchRestore
    call screen main_ui
    jump Church


label ChurchRestore:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    if week != 7 or time > 2:
        $ MainTxt = ChurchRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        call ShowImageSeq("general", "", "LocChurchClosed", 2)
        $ current_action_items.append(MenuItem("Вернуться к трактиру", Jump("StreetTavern")))
        return

    if time == 0:
        $ MainTxt = "Вы пришли в великий городской собор Ильматера на воскресную службу.\n\nКажется, здесь собралось полгорода. Отец Герхард, жрец Ильматера, ведет службу. Ее вы видели и слышали уже сотни раз. Ваш взор обегает собор и {a=call:ChurchServiceMenu}{color=#245b2b}прихожан{/color}{/a}."
        $ CurLocDesc = MainTxt
        call ShowImage("gerhard", "", "gerhard")
    elif time == 1:
        $ MainTxt = "Служба закончилась, люди понемногу начали расходиться. Вы можете или пойти домой или пойти к отцу Герхарду на исповедь."
        if BeckyVar.get("GerhardBeckyTalk", 0) > 0:
            $ MainTxt = MainTxt + "\nНа небольшом столике в углу лежит {a=call:ShowChurchDraupnirList}{color=#245b2b}листок{/color}{/a}, на котором что-то накорябанно."
        $ CurLocDesc = MainTxt
        call ShowImage("general", "", "LocChurchIspoved1")
    else:
        $ MainTxt = "Почти все прихожане уже разошлись, однако собор еще открыт. Вы можете его обойти и посмотреть нет ли чего интересного."
        $ CurLocDesc = MainTxt
        call ShowImage("general", "", "LocChurchIspoved2")

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n" + navigation_only_message() + "\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt

    call ChurchBuildActions
    return


label ChurchBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []

    if week != 7 or time > 2:
        $ current_action_items.append(MenuItem("Вернуться к трактиру", Jump("StreetTavern")))
        return

    if time == 0:
        pass
    elif time == 1:
        if BeckyVar.get("PriestAdvice", 0) > 0 and BeckyVar.get("GerhardBeckyTalk", 0) < 2:
            $ current_action_items.append(MenuItem("Обсудить сомнения Бекки со святым отцом", Call("becky_church_talk")))
        $ current_action_items.append(MenuItem("Идти на исповедь", Call("ChurchIspoved", 1)))
    else:
        $ current_action_items.append(MenuItem("Обойти собор", Call("ChurchAfterCermon", 1)))

    $ current_action_items.append(MenuItem("Вернуться к трактиру", Jump("StreetTavern")))
    return


label ChurchServiceMenu:
    $ current_action_title = "Прихожане"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Найти Сандру", Call("ChurchServiceMother")))
    $ current_action_items.append(MenuItem("Найти сестричек", Call("ChurchServiceSisters")))
    $ current_action_items.append(MenuItem("Найти семейство Легаре", Call("ChurchServiceLegare")))
    $ current_action_items.append(MenuItem("Найти семейство Блэнкеншип", Call("ChurchServiceBlanken")))
    if Friends.get("georgett", 0) >= 2:
        $ current_action_items.append(MenuItem("Найти Жоржетту Брюно", Call("ChurchServiceGeorgett")))
    if cametoday < cancumdaily and Friends.get("georgett", 0) >= 2 and HadSex.get("georgett", 0) >= 3 and GeorgettVar.get("foundinchurch", 0):
        $ current_action_items.append(MenuItem("Предложить Жоржетте перепихнуться по быстрому", Call("church_georgett_sex")))
    $ current_action_items.append(MenuItem("Вернуться к службе", Call("ChurchRestore")))
    $ renpy.restart_interaction()
    return


label ChurchServiceMother:
    $ MainTxt = "Сандра,одетая , в своё строгое платье внимательно слушает службу."
    $ CurLocDesc = MainTxt
    $ _church_picture = church_sandra_picture()
    if str(_church_picture or "").strip():
        call ShowImage("", "", _church_picture)
    else:
        call ShowImage("sandra", "church", "cermon")
    call ChurchServiceMenu
    return


label ChurchServiceSisters:
    $ MainTxt = "Мелисса и Аманда тихо щебечут между собой, уделяя происходящему куда меньше внимания, чем хотелось бы святому отцу."
    $ CurLocDesc = MainTxt
    $ _church_picture = church_sisters_picture()
    if str(_church_picture or "").strip():
        call ShowImage("", "", _church_picture)
    else:
        call ShowImage("amanda", "church", "cermon")
    call ChurchServiceMenu
    return


label ChurchServiceLegare:
    if clara_paintings_church_fiance_ready():
        call preEvent("claraPaintingsPath")
        call story_clara_paintings_church_4
        return
    $ MainTxt = "Мессир Легаре в черном камзоле стоит около одной из колонн и внимательно слушает службу. Рядом с ним стоит его жена Элоиза, маленькая шатенка средних лет, а за ними все их дети - Кларисса, Жерар, Жан-Жак, Полина и малыш Реми."
    $ CurLocDesc = MainTxt
    call ShowImageSeq("alber", "church", "cermon", 2)
    call ChurchServiceMenu
    return


label ChurchServiceBlanken:
    $ MainTxt = "Вдова Блэнкеншип, высокая рыжая женщина с полной грудью, чуть младше сорока лет. Она на первый взгляд слушает отца Герхарда, но если присмотреться, то видно, что ее мысли витают где-то далеко. Рядом с ней стоит Эдди, ее рыжий управляющий лавкой и ваш ровесник. Поблизости ее дети - Ингенборг, Ивар, Эмма и Лаура."
    $ CurLocDesc = MainTxt
    $ _church_picture = church_blanken_picture()
    if str(_church_picture or "").strip():
        call ShowImage("", "", _church_picture)
    else:
        call ShowImage("becky", "church", "cermon")
    call ChurchServiceMenu
    return


label ChurchServiceGeorgett:
    $ MainTxt = "В одном из углов собора вы находите вашу ветренную знакомую - Жоржетту Брюно, шлюху из портового квартала. Это молодая белокурая и кареглазая женщина, среднего роста, чуть пухленькая и с большой налитой грудью. В собор она нарядилась чуть скромнее, чем обычно, но не слишком: на ней красное платье до колен и блузка с глубоким декольте, на этот раз хотя бы не прозрачная. Вы замечаете, что прихожане-мужчины обращают на нее гораздо больше внимания, чем на проповедь с амвона."
    if GeorgettVar.get("askkids", 0):
        if Friends.get("liza", 0) > 0:
            $ MainTxt = MainTxt + "\n\nРядом с ней вы видите ее старшую дочь Лизетту - молоденькую мулатку, на вид - ровесницу Аманды. Ее волосы забранны в две косички а груди только начали расти. Ее шоколадное тело закрывают юбка и блузка, такие же как у ее мамы."
        else:
            $ MainTxt = MainTxt + "\n\nРядом с ней вы видите молоденькую мулатку, на вид - ровесницу Аманды. Ее волосы забранны в две косички а груди только начали расти. Судя по всему это Лизетта - старшая дочь Жоржетты. Ее шоколадное тело закрывают юбка и блузка, такие же как у ее мамы."
        call ShowImage("georgett", "church", "cermonliza")
    else:
        call ShowImage("georgett", "church", "cermon")
    $ CurLocDesc = MainTxt
    $ GeorgettVar["foundinchurch"] = 1
    call ChurchServiceMenu
    return


label becky_church_talk:
    if BeckyVar.get("GerhardBeckyTalk", 0) == 0:
        $ MainTxt = "После службы вы подошли к отцу Герхарду: \"Падре, одна из ваших прихожанок, торговка с рынка, может обратиться к вам за советом. Снедает ее мысль о том, большой ли грех то, что она собирается совершить. Не могли ли бы вы сказать ей, что то невеликое дело?\""
    else:
        $ MainTxt = "После службы вы подошли к отцу Герхарду: \"Падре, та прихожанка о которой я вас спрашивал, ну та торговка с рынка, она к вам за советом случаем не подходила? И что же вы ей посоветовали?\""

    if BeckyVar.get("PriestAdvice", 0) == 3:
        $ MainTxt = MainTxt + "\n\n\"Поговорил я с ней, сын мой,\" сказал вам святой отец улыбаясь. \"Прав ты был, что ее тревожило - то невеликое прегрешение. Мудр ты, сын мой, не по годам. Да и щедр преизрядно и к церкви нашей с должным пиететом относишься.\"\n\nИ, осенив вас знаком Ильматера, отец Герхард вернулся к своим делам."
    elif BeckyVar.get("GerhardBeckyTalk", 0) == 0:
        $ MainTxt = MainTxt + "\n\n\"Да как ты смеешь, молокосос, указывать мне, настоятелю этого храма, как с моей паствой общаться?!\" справедливо возмутился почтенный жрец.\n\n\"Я выслушиваю своих прихожанок дольше, чем ты прожил на свете, и уж способен сам решить, велик грех или мал, без чьих-то советов.\"\n\nРасстроены отказом, вы уже собрались было уйти, как отец Герхард промолвил в пустоту, ни к кому конкретно не обращаясь:\n\n\"Эх, что за народ нынче пошел, никакого уважения к церкви. Собор-то наш поистрепался слегка, так я и попросил мастера Драупнира чтоб он, значит, ремонт-то небольшой сделал. Раньше-то что, любой бы за честь великую счел бы, что ему доверили храм великого Ильматера ремонтировать. А сейчас? Драупнир, шельмец, такой счет выставил, как будто он десять новых соборов построил. А народишко-то измельчал, жертвуют неохотно. Так этот счет и лежит неоплаченный, вон там,\" жрец махнул рукой куда-то в сторону.\n\nПрисмотревшись, вы заметили в указанном направлении какой-то листок."
    else:
        $ MainTxt = MainTxt + "\n\n\"Да как ты смеешь, молодой человек, на тайну исповеди посягать?! Я по твоему кто, настоятель этого великого храма или сплетник с базарной площади?\" разгневался достопочтенный.\n\nПолучив такую отповедь вы уже собрались было отправиться восвояси, как отец Герхард заметил:\n\n\"Эх, что за люди нынче? Раньше к падре с благовением обращались. А сейчас? Одному тайну исповеди раскрой, а этот шельмец, Драупнир, все деньги требует по счету. А откуда же я их возьму, коли никто не жертвует?\""

    $ CurLocDesc = MainTxt
    call ShowImage("general", "", "LocChurchIspoved1")
    $ BeckyVar["GerhardBeckyTalk"] = 2
    call ChurchBuildActions
    return


label church_georgett_sex:
    hide screen main_ui
    "В одном из углов собора вы находите вашу ветренную знакомую и шепчете ей на ухо ваше нескромное предложение."

    if Friends.get("georgett", 0) < 6:
        "«Ты что, сдурел!» - отвечает вам она. «Это же собор!»"
        call ChurchRestore
        return

    "«Какой ты пошлый! Поиметь меня прямо на церковной службе!» - смеется Жоржетта. «Это обойдется тебе в 15 мараведи!»"

    if int(money or 0) < 15:
        "«Ой, а у меня столько нет», говорите вы."
        "«Ну нет так нет», следует резонный ответ."
        call ChurchRestore
        return

    python:
        import random as _random
        _TmpChurchGeorgSex = "bench"
        if int(GeorgettVar.get("askkids", 0) or 0) == 0 and _random.randint(1, 2) == 1:
            _TmpChurchGeorgSex = "doggy"
        if int(GeorgettVar.get("askkids", 0) or 0) != 0:
            _TmpChurchGeorgSex = "withliza"
        renpy.store.TmpChurchGeorgSex = _TmpChurchGeorgSex

    if GeorgettVar.get("askkids", 0):
        if Friends.get("liza", 0) == 0:
            "Жоржетта поворачивается к молоденькой мулатке-шоколадке, стоящей рядом с ней: «Стефан, познакомься, это моя старшая доченька Лизетта, я тебе про нее рассказывала. Лизетта, познакомься, это дядя Стефан.»"
            $ Friends["liza"] = 1
        if GeorgettVar.get("lizasawinchurch", 0):
            "«Лизетточка, мы сейчас с дядей Стефаном пойдем потрахаемся», - без тени смущения говорит ваша подруга своей дочке. «Оставайся здесь, или, если хочешь, можешь посмотреть. Только тихо.»"
        else:
            "«Лизетточка, мы сейчас с дядей Стефаном отойдем поговорить, а ты нас здесь подожди, хорошо?» - говорит ваша подруга своей дочке. «Хорошо, мама.»"

    if str(TmpChurchGeorgSex or "") == "doggy":
        "Вы отдаете деньги Жоржетте и она ведет вас к одной из скамей в дальнем темном углу собора. Вы внимательно осматриваетесь и замечаете, что скамья, колонны, сложенная утварь и прочее барахло заслоняют вас от взглядов толпы. Судя по всему к таким же выводам приходит и Жоржетта, так как она решительным движением снимает с себя юбку под которой, как вы и ожидали, ничего не оказалось. А сняв, Жоржетта наклоняется, опираясь о скамью, приглашающе выставив свою киску. Поняв намек, вы, не теряя времени, спускаете штаны и одним движением входите в развратницу."
    else:
        "Вы отдаете деньги Жоржетте и она ведет вас к одной из скамей в дальнем темном углу собора. Вы оба садитесь на нее. Видно, что колонны и прислоненная к ним церковная утварь заслоняют вас от взглядов толпы. Жоржетта быстро приспускает ваши штаны, выпуская на волю ваш уже вставший член. Затем она садится вам на колени, ловко заправляя ваш член в себя. Вы с удовлетворением отмечаете, что Жоржетта даже в церкви не изменила своей привычке ходить без нижнего белья. Оперевшись на следующую скамью ваша подружка начинает плавно двигаться, осторожно но уверенно доводя вас обеих до разрядки."

    if GeorgettVar.get("askkids", 0):
        "Вдруг вы замечаете, как кто-то наблюдает за вами из тени. Вы извещаете об этом свою подругу, та всматривается в тени и вдруг призывно машет рукой. Наблюдателем оказывается Лизетта, она выходит из своего укрытия и садится рядом с вами."
        "«Лизетточка, доченька, видишь, мы с дядей Стефаном трахаемся. Если хочешь посмотреть - то смотри. Только тихо». С этими словами ваша подруга возобновила свои движения. Лизетта же, смотря на вас, медленно возбуждается и начинает ласкать себя через одежду."
        $ GeorgettVar["lizasawinchurch"] = 1

    "Вы сношаетесь минут десять, когда ваша подружка не выдерживает, и сжав зубы, чтобы не застонать, кончает. Сразу следом за ней кончаете и вы, заполняя ее незащищенную матку своей спермой. Жоржетта встает с вашего члена и протирает лобок подолом платья, вы же быстро натягиваете приспущенные штаны."

    if GeorgettVar.get("askkids", 0):
        "«Мама, он что, в тебя кончил?» - вдруг раздается голосок. «Шшш, доченька, ну конечно в меня, я же тебе говорила что ничего в этом страшного нет.»"

    $ money -= 15
    $ GeorgettVar["fuckinchurch"] = 1
    $ PregnancyCheck("georgett", "inside", 1, "Вы")
    call ShowImageSeq("georgett", "church", TmpChurchGeorgSex, 6)
    call AdvanceTime("Church")
    return
