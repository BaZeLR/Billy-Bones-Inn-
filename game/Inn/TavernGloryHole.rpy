# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_glory_hole_available():
        return int(player.tavern_management.glory_hole or 0) == 2

    def tavern_glory_hole_workers():
        return girls_by_job("jobgloryhole", "TavernGloryHole")

    def tavern_glory_hole_worker():
        workers = tavern_glory_hole_workers()
        booked_workers = [
            girl_key for girl_key in workers
            if SexEvents.today_index(girl_key, calendar_v2.time_slot(), "Glory") > 0
        ]
        candidates = booked_workers or workers
        if not candidates:
            return ""
        return str(procedural_choice(candidates, key="tavern_glory_worker_%s_%s" % (current_game_day(), calendar_v2.clock_minutes())) or "")

    def tavern_glory_hole_working_now():
        return player.tavern_management.isTavernOpen and tavern_glory_hole_worker() != ""

    def tavern_glory_hole_waiting_text(girl_name=""):
        girl_key = str(girl_name or tavern_glory_hole_worker() or "")
        if girl_key == "":
            return ""
        info = people.get_info(girl_key)
        text = people_display_name(girl_key) + " сидит за ширмой на скамеечке в ожидании клиентов. Подол юбки задран до пояса, полностью открывая киску. Панталончиков прелестница либо не носит, либо сняла как лишнее препятствие."
        if info is not None and info.pregnancy_days() > 120:
            text += " Над задранным подолом из под расстегнутой блузки виднеется беременное пузико " + people_name(girl_key, "genitive") + "."
        return text

    TavernGloryHoleRoomDefinition = Room(
        code_name="TavernGloryHole",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Глорихол",
        bg_picture="images/gloryhole/glory1.jpg",
        descriptions=[
            RoomDescription(
                text="За ширмой в дальнем углу трактира устроена отдельная тесная комнатка с глорихолом. Клиент не видит девушку по ту сторону, девушка не видит клиента, а вы знаете, где здесь потайной проход и как проверить, что происходит.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в главный зал", target="TavernMain"),
        ],
        action_menus=[
            RoomAction(action_id="check_glory_hole", label="Проверить, что происходит", hook="call", target="TavernGloryHoleCheck"),
        ],
        game_items=[],
        custom_properties={},
    )

label TavernGloryHole:
    if not tavern_glory_hole_available():
        "Отдельная комната пока недоступна. Сначала закажите и оплатите постройку."
        jump TavernMain
    $ renpy.dynamic("_tgh_room", "_tgh_desc_parts", "_tgh_desc", "_tgh_worker", "_tgh_workers")
    scene black
    $ rooms.enter("TavernGloryHole")
    $ _tgh_room = rooms.current
    $ scene_runtime.picture = _tgh_room.bg_picture or None
    $ _tgh_desc_parts = [str(_tgh_desc.text or "") for _tgh_desc in _tgh_room.visible_descriptions()]
    $ _tgh_workers = tavern_glory_hole_workers()
    if tavern_glory_hole_working_now():
        python:
            for _tgh_worker in _tgh_workers:
                _tgh_desc_parts.append(tavern_glory_hole_waiting_text(_tgh_worker))
    $ scene_runtime.location_text = "\n\n".join([part for part in _tgh_desc_parts if str(part or "").strip()])
    $ scene_runtime.text = scene_runtime.location_text
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = _tgh_room.build_action_items() + _tgh_room.build_exit_items()
    $ _tgh_room.mark_visited()
    while True:
        call screen main_ui


label TavernGloryHoleCheck:
    if not tavern_glory_hole_available():
        return
    $ main_ui_begin_native_scene_state("Глорихол")
    show screen main_ui
    python hide:
        session = player.tavern_management.glory_hole_session
        session.reset()
        session.girl_name = tavern_glory_hole_worker()
        player.tavern_management.glory_hole_look = 0

        _time_now = calendar_v2.time_slot()
        if tavern_glory_hole_working_now() and session.girl_name != "":
            session.works = 1

        if GetSexEventFromTable("amanda", 99, "glorytry") > 0:
            session.amanda_present = 1
            Amanda.set_var_int("glorytried", 1)

        if session.works:
            _tgh_info = people.get_info(session.girl_name)
            _worker_corruption = int(_tgh_info.corruption or 0) if _tgh_info is not None and hasattr(_tgh_info, "corruption") else 0
            session.roll_inside(_worker_corruption)

            _real_name = people_display_name(session.girl_name)
            _tgh_pregnancy_days = _tgh_info.pregnancy_days() if _tgh_info is not None else 0

            _real_name2 = people_name(session.girl_name, 'genitive')
            player.tavern_management.glory_hole_session.girl_line0 = tavern_glory_hole_waiting_text(session.girl_name)

            player.tavern_management.glory_hole_session.girl_line1 = _real_name + " обрадованно посмотрела на появившийся в отверстии член, наклонилась к нему, и начала облизывать и обсасывать головку члена, не забывая ласкать себя свободной рукой."

            if player.tavern_management.glory_hole_session.inside or player.tavern_management.glory_hole_session.inside_once:
                player.tavern_management.glory_hole_session.girl_line2 = "Вы не в силах поверить своим глазам: пососав некоторое время член, " + _real_name + " выпускает его изо рта, разворачивается, встает раком и насаживается на член прямо своей похотливой киской. И начинает страстно трахать мужика, лица которого она даже не видела!"
                if _tgh_pregnancy_days > 120:
                    player.tavern_management.glory_hole_session.girl_line2 += " Беременность ей в этом ничуть не мешает и не смущает!"
                if player.tavern_management.glory_hole_session.inside:
                    player.tavern_management.glory_hole_session.girl_line3 = "Без всяких мыслей о возможных последствиях, " + _real_name + " продолжает трахать член незнакомца, пока тот не разряжается ей прямо внутрь. Вслед за этим кончает и " + _real_name + ". Развернувшись, она тщательно облизывает обмякший член от остатков спермы и возвращается на свою скамеечку, довольно улыбаясь."
                else:
                    player.tavern_management.glory_hole_session.girl_line3 = "Все-таки благоразумие берет верх над страстью: чувствуя, что клиент уже близок к оргазму, " + _real_name + " соскальзывает с его члена, вызывая вздох разочарования с другой стороны ширмы, и берет член обратно в свой ротик, доводя наконец его до разрядки. С трудом проглатив потоки семени, " + _real_name + " слизывает остатки спермы с члена и возвращается на свою скамеечку, довольно улыбаясь."
            else:
                player.tavern_management.glory_hole_session.girl_line2 = "Не в силах оторваться, вы смотрите на то как член входит в ротик " + _real_name2 + ". Она распаляется все больше и больше, и вот уже заглатывает член почти по самые яйца. Одновременно она иступленно ласкает себя, доводя до уже такого близкого оргазма."
                player.tavern_management.glory_hole_session.girl_line3 = "Продолжая сосать член как огромный леденец и натирать в тоже время себе киску " + _real_name + " наконец кончает. Вскоре, прямо ей в ротик кончает и клиент. С трудом " + _real_name + " проглатывает поток семени, потом слизывает остатки с члена и возвращается на свою скамеечку, довольно улыбаясь."

            if _tgh_pregnancy_days > 120:
                player.tavern_management.glory_hole_session.girl_line3 += " и поглаживая свой беременный животик."
            else:
                player.tavern_management.glory_hole_session.girl_line3 += "."

            if CheckIfSexEventExist(player.tavern_management.glory_hole_session.girl_name, _time_now) > 0 and procedural_randint(1, 2, key="procedural:Inn/TavernGloryHole.rpy:sex_event") == 1 and player.tavern_management.glory_hole_session.amanda_present == 0:
                player.tavern_management.glory_hole_look = GetSexEventFromTable(player.tavern_management.glory_hole_session.girl_name, _time_now)

                if player.tavern_management.glory_hole_look == 1:
                    player.tavern_management.glory_hole_session.client_line1 = "За занавеской вы увидели мастера Драупнира. Видимо низкая цена все-таки привлекла экономного гнома. Расстегнув штаны на помочах, мастер Драупнир извлек свой инструмент. Оный инструмент был как сам гном - очень толстый, но не очень длиный. Встав, в силу невысокого роста, на приступочку, мастер Драупнир направил свой агрегат в дырку."
                    player.tavern_management.glory_hole_session.client_line2 = "Мастер Драупнир наслаждается происходящим, беря максимум удовольствия за свои деньги. Пока кто-то обрабатывает член через дырку, гном блаженно улыбается."
                    player.tavern_management.glory_hole_session.client_line3 = "Гном вдруг замер, и судя, по всему кончил. Ну а затем он застегнул штаны и отправился восвояси."
                    pregnancy_check(player.tavern_management.glory_hole_session.girl_name, "inside" if player.tavern_management.glory_hole_session.inside else "mouth", 1, "Мастер Драупнир")
                elif player.tavern_management.glory_hole_look == 2:
                    player.tavern_management.glory_hole_session.client_line1 = "За занавеской вы увидели своего старого знакомца - рыжего Эдди. Немного нервничая, Эдди смело расстегивает штаны и сует свое достоинство прямо в дырку."
                    player.tavern_management.glory_hole_session.client_line2 = "Эдди кайфует, пока с той стороны ему делают отсос а может и кое-чего покруче."
                    player.tavern_management.glory_hole_session.client_line3 = "Эдди кончил и, застегнув штаны, отправился восвояси."
                    pregnancy_check(player.tavern_management.glory_hole_session.girl_name, "inside" if player.tavern_management.glory_hole_session.inside else "mouth", 1, "Эдди")
                elif player.tavern_management.glory_hole_look == 3:
                    player.tavern_management.glory_hole_session.client_line1 = "За занавеской вы увидели месье Легаре. Женатый, но похотливый винторговец в который уже раз решил обратиться к продажной любви. Приспустив штаны он сунул свой длинный и тонкий член прямо в дырку."
                    player.tavern_management.glory_hole_session.client_line2 = "Месье Легаре слегка поставнывает, пока кто-то с той стороны занимается его сокровищем."
                    player.tavern_management.glory_hole_session.client_line3 = "Месье Легаре извергся и, подтянув штаны, вернулся в главную залу."
                    pregnancy_check(player.tavern_management.glory_hole_session.girl_name, "inside" if player.tavern_management.glory_hole_session.inside else "mouth", 1, "Месье Легаре")
                elif player.tavern_management.glory_hole_look == 4:
                    player.tavern_management.glory_hole_session.client_line1 = "За занавеской вы увидели достойного отца Герхарда. Осенив глорихол знаком Ильматера, он приподнял сутану и, ничтоже сумняшись, сунул своего грешника прямо в дырку."
                    player.tavern_management.glory_hole_session.client_line2 = "Отец Герхард бормочет толи благословения, толи молитвы, пока с той стороны кто-то, несомненно с благославения Ильматера, пытается уложить его вставшего грешника."
                    player.tavern_management.glory_hole_session.client_line3 = "Отец Герхард закончил, благословил свою невидимую прихожанку, опустил сутану и отправился дальше нести слово великого Ильматера."
                    pregnancy_check(player.tavern_management.glory_hole_session.girl_name, "inside" if player.tavern_management.glory_hole_session.inside else "mouth", 1, "Отец Герхард")
                elif 5 <= player.tavern_management.glory_hole_look <= 7:
                    player.tavern_management.glory_hole_session.client_line1 = "За занавеской полупьяный морской волк сунул своего волчонка прямо в дырку."
                    player.tavern_management.glory_hole_session.client_line2 = "Моряк наслаждается процессом, не обращая внимание на окружающее."
                    player.tavern_management.glory_hole_session.client_line3 = "Морячок кончил, и пошел восвояси, может к себе на корабль, а может гулять дальше."
                    pregnancy_check(player.tavern_management.glory_hole_session.girl_name, "inside" if player.tavern_management.glory_hole_session.inside else "mouth", 1, "", 1, "Неизвестный моряк")
                elif 8 <= player.tavern_management.glory_hole_look <= 10:
                    player.tavern_management.glory_hole_session.client_line1 = "За занавеской городской стражник расстегнул форменные штаны и сунул свой член прямо в дырку."
                    player.tavern_management.glory_hole_session.client_line2 = "Страж порядка громко стонет от наслаждения."
                    player.tavern_management.glory_hole_session.client_line3 = "Слуга закона кончил, и пошел обратно на улицы, ловить воров и грабителей."
                    pregnancy_check(player.tavern_management.glory_hole_session.girl_name, "inside" if player.tavern_management.glory_hole_session.inside else "mouth", 1, "", 1, "Неизвестный стражник")
                else:
                    player.tavern_management.glory_hole_session.client_line1 = "За занавеской совсем молоденький пацан, ужасно краснея и нервничая, извлек свой невеликих размеров член и, закатив глаза в предвкушении, сунул его в дырку."
                    player.tavern_management.glory_hole_session.client_line2 = "Лицо пацаненка выражает всю гамму чувств - наслаждение, вострог, радость от расставания с девственностью. Надолго его, судя по всему, не хватит."
                    player.tavern_management.glory_hole_session.client_line3 = "Так и есть: всего через минуту мальчишка кончил и, довольный, убежал, даже забыв застегнуть до конца ширинку."
                    pregnancy_check(player.tavern_management.glory_hole_session.girl_name, "inside" if player.tavern_management.glory_hole_session.inside else "mouth", 1, "", 1, "Неизвестный горожанин")
        else:
            player.tavern_management.glory_hole_session.girl_line0 = "За ширмой оказалось пусто! Может еще рано, а может быть здесь никто не работает."

    "Вы находитесь в дальнем углу вашего трактира, где, за загородкой сделан глорихол. Посетители, чтобы попасть сюда, должны заплатить 6 мараведи, но к вам, согласно договору, это не относится - под внимательными взглядами ваших матери и сестер вы гордо вошли подошли к глорихолу не платя - это ваше право."
    "Что вы собираетесь делать?"

    if renpy.has_label("ShowImage"):
        call ShowImage("gloryhole", "", "glory1")
    jump TavernGloryHole_menu

    label TavernGloryHole_menu:
        menu:
            "Смотреть на клиента" if player.tavern_management.glory_hole_look > 0 and player.tavern_management.glory_hole_session.current_step <= 3 and player.tavern_management.glory_hole_session.menu_blocked == 0:
                if player.tavern_management.glory_hole_session.current_step == 0:
                    "Вспомнив про сделанную мастеровитым гномом возможность обзора, вы решили посмотреть на происходящее инкогнито."
                else:
                    "Вы продолжаете обозревать происходящее внимательным взглядом."

                if player.tavern_management.glory_hole_session.current_step == 0:
                    "[player.tavern_management.glory_hole_session.client_line1]"
                elif player.tavern_management.glory_hole_session.current_step == 1:
                    "[player.tavern_management.glory_hole_session.client_line2]"
                else:
                    "[player.tavern_management.glory_hole_session.client_line3]"

                $ player.tavern_management.glory_hole_session.current_step += 1
                if player.tavern_management.glory_hole_session.current_step >= 3:
                    $ player.tavern_management.glory_hole_session.current_step = 0
                    $ player.tavern_management.glory_hole_look = 0

                if renpy.has_label("ShowImage"):
                    call ShowImage("gloryhole", "", "gloryclient")
                jump TavernGloryHole_menu

            "Смотреть на девочку" if player.tavern_management.glory_hole_session.cock_inserted == 0 and player.tavern_management.glory_hole_session.menu_blocked == 0:
                
                if player.tavern_management.glory_hole_session.current_step == 0 or player.tavern_management.glory_hole_look == 0:
                    "Вы решили аккуратно заглянуть за ширмочку и посмотреть на девочку за работой."
                else:
                    "Вы продолжаете дальше смотреть, как работает очаровательная [people_display_name(player.tavern_management.glory_hole_session.girl_name)]."

                if player.tavern_management.glory_hole_look == 0:
                    "[player.tavern_management.glory_hole_session.girl_line0]"
                elif player.tavern_management.glory_hole_session.current_step == 0:
                    "[player.tavern_management.glory_hole_session.girl_line1]"
                elif player.tavern_management.glory_hole_session.current_step == 1:
                    "[player.tavern_management.glory_hole_session.girl_line2]"
                else:
                    "[player.tavern_management.glory_hole_session.girl_line3]"

                if player.tavern_management.glory_hole_look:
                    $ player.tavern_management.glory_hole_session.current_step += 1
                    if player.tavern_management.glory_hole_session.current_step >= 3:
                        $ player.tavern_management.glory_hole_session.current_step = 0
                        $ player.tavern_management.glory_hole_look = 0

                if player.tavern_management.glory_hole_session.amanda_present == 1:
                    $ player.tavern_management.glory_hole_session.menu_blocked = 1
                    $ Amanda.set_var_int("glory_cur_state", 1)
                    $ Amanda.set_var_int("glorysdiscover", 1)
                    "Ваша реакция?"
                    if renpy.has_label("ShowImage"):
                        call ShowImage("amanda", "gloryfirst", "ambush")

                if player.tavern_management.glory_hole_session.girl_name == "georgett" and player.tavern_management.glory_hole_session.works:
                    if renpy.has_label("ShowImageSeq"):
                        call ShowImageSeq("georgett", "glory", "glory", 2)
                elif player.tavern_management.glory_hole_session.works == 0:
                    if renpy.has_label("ShowImage"):
                        call ShowImage("gloryhole", "", "glory1")
                jump TavernGloryHole_menu

            "Вставить член" if player.tavern_management.glory_hole_session.cock_inserted == 0 and player.tavern_management.glory_hole_look == 0 and player.intimacy.came_today < player.intimacy.can_cum_daily and player.tavern_management.glory_hole_session.current_step == 0 and player.tavern_management.glory_hole_session.menu_blocked == 0:
                
                python hide:
                    session = player.tavern_management.glory_hole_session
                    worker_info = people.get_info(session.girl_name)
                    worker_corruption = int(worker_info.corruption or 0) if worker_info is not None and hasattr(worker_info, "corruption") else 0
                    session.roll_inside(worker_corruption)
                $ player.tavern_management.glory_hole_session.cock_inserted = 1
                "Вы немного поласкали своего друга, приводя его в боевое состояние, и решительно вставили его в столь привлекательную дырку."
                "[player.tavern_management.glory_hole_session.player_line1]"
                if player.tavern_management.glory_hole_session.works:
                    $ player.tavern_management.glory_hole_session.current_step += 1
                if renpy.has_label("ShowImage"):
                    call ShowImage("gloryhole", "", "gloryyou")
                jump TavernGloryHole_menu

            "Наслаждаться процессом" if player.tavern_management.glory_hole_session.cock_inserted == 1 and player.tavern_management.glory_hole_look == 0 and player.intimacy.came_today < player.intimacy.can_cum_daily and player.tavern_management.glory_hole_session.current_step == 1 and player.tavern_management.glory_hole_session.menu_blocked == 0:
                
                "[player.tavern_management.glory_hole_session.player_line2]"
                if player.tavern_management.glory_hole_session.works:
                    $ player.tavern_management.glory_hole_session.current_step += 1
                if renpy.has_label("ShowImage"):
                    call ShowImage("gloryhole", "", "gloryyou")
                jump TavernGloryHole_menu

            "Кончить" if player.tavern_management.glory_hole_session.cock_inserted == 1 and player.tavern_management.glory_hole_look == 0 and player.intimacy.came_today < player.intimacy.can_cum_daily and player.tavern_management.glory_hole_session.current_step == 2 and player.tavern_management.glory_hole_session.menu_blocked == 0:
                
                "[player.tavern_management.glory_hole_session.player_line3]"
                if player.tavern_management.glory_hole_session.works:
                    $ player.tavern_management.glory_hole_session.current_step += 1

                if player.tavern_management.glory_hole_session.amanda_present == 1:
                    $ player.tavern_management.glory_hole_session.menu_blocked = 1
                    "Ваша реакция?"
                    python:
                        Amanda.pregnancy_check("mouthface", 1, "Вы")
                    $ Amanda.set_var_int("glorysuck", 1)
                    $ Amanda.set_var_int("glory_cur_state", 4)
                else:
                    python:
                        pregnancy_check(
                            player.tavern_management.glory_hole_session.girl_name,
                            "inside" if player.tavern_management.glory_hole_session.inside else "mouth",
                            1,
                            "Вы",
                        )

                $ player.tavern_management.glory_hole_session.cock_inserted = 0
                jump TavernGloryHole_menu

            "Что-то не то, проверить кто у глорихола" if player.tavern_management.glory_hole_session.amanda_present == 1 and player.tavern_management.glory_hole_session.menu_blocked == 0 and player.tavern_management.glory_hole_session.cock_inserted == 1:
                
                "[player.tavern_management.glory_hole_session.girl_line1]"
                $ Amanda.set_var_int("glory_cur_state", 2)
                $ player.tavern_management.glory_hole_session.menu_blocked = 1
                "Ваша реакция?"
                if renpy.has_label("ShowImage"):
                    call ShowImage("amanda", "gloryfirst", "ambush")
                jump TavernGloryHole_menu

            "Ваша реакция" if player.tavern_management.glory_hole_session.menu_blocked == 1:
                call checkTriggers("TavernGloryHole", "amanda_gloryhole_try", 0)

            "Вернуться в комнату":
                $ main_ui_end_native_scene_state()
                return
