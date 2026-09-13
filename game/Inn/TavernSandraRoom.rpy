# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
define TAVERN_TEAM_PREMIUM_REWARDS = {
    25: (1, 0),
    50: (2, 0),
    100: (3, 1),
    200: (4, 1),
    500: (5, 2),
}

define TAVERN_TEAM_PREMIUM_JOB_SKILLS = (
    ("jobkitchen", "cooking"),
    ("jobcleaning", "cleaning"),
    ("jobwaitress", "waitress"),
)

init 6 python:
    def tavern_premium_reaction_picture(girl_name):
        girl_key = str(girl_name or "").strip().lower()
        if girl_key == "liza":
            picture_path = str(LizaStaticData.image_path("tavern", "wench_happy") or "")
            if picture_path and renpy.loadable(picture_path):
                return picture_path
        return str(girl_card_portrait_path(girl_key) or "")

    def tavern_premium_reaction_text(girl_name, corruption_value=0):
        girl_key = str(girl_name or "").strip().lower()
        corruption = int(corruption_value or 0)
        if girl_key == "sandra":
            if corruption < 15:
                return "Сандра дважды пересчитывает премию и строго кивает. \"Вот это хозяйский поступок. Спасибо, Стефан. Когда труд замечают, и спрашивать с людей можно по совести.\""
            if corruption < 35:
                return "Сандра прячет редкую улыбку, крепко сжимает ваше предплечье и благодарит уже без обычной хозяйской сухости. Перед тем как отойти, она на миг прижимается плечом теснее, чем требовала бы простая благодарность."
            if corruption < 60:
                return "Сандра подходит вплотную, поправляет вам ворот и неожиданно целует в щеку. Ее грудь на мгновение прижимается к вам, а тихое \"спасибо, хозяин\" звучит гораздо теплее любого делового отчета."
            return "Сандра без стеснения обнимает вас, медленно прижимаясь всем телом. \"Щедрого хозяина надо благодарить так, чтобы он это запомнил,\" шепчет она на ухо, прежде чем с довольной улыбкой отойти."
        if girl_key == "melissa":
            if corruption < 15:
                return "Мелисса сначала решает, что ослышалась, потом крепко зажимает премию в ладони и тихо благодарит. Ее смущенная улыбка говорит яснее слов: такого признания своего труда она не ожидала."
            if corruption < 35:
                return "Мелисса радостно обнимает вас, а поняв, насколько тесно прижалась, вспыхивает и отскакивает. \"Это за премию, не воображай лишнего,\" предупреждает она, хотя улыбку спрятать уже не может."
            if corruption < 60:
                return "Мелисса обвивает руками вашу шею и оставляет быстрый поцелуй у самого уголка губ. Отстраняясь, она проводит ладонью по вашей груди и шепчет, что хорошего хозяина иногда хочется награждать особенно старательно."
            return "Мелисса смеется, на несколько мгновений устраивается у вас на колене и прячет премию за вырезом платья. \"Теперь попробуй забрать обратно,\" поддразнивает она, медленно поднимаясь и позволяя вашему взгляду задержаться."
        if girl_key == "amanda":
            if corruption < 15:
                return "Аманда восторженно вскрикивает, бросается вам на шею и едва не опрокидывает лавку. Получив премию, она обещает отработать каждую монету."
            if corruption < 35:
                return "Аманда звонко целует вас в щеку и с озорной улыбкой прячет монеты за пазуху. \"За хорошую работу — хорошая премия. А за очень хорошую благодарность что полагается?\" — спрашивает она и сама же убегает от ответа."
            if corruption < 60:
                return "Аманда неожиданно целует вас уже в губы, а отступая, нарочно проводит бедром по вашей ноге. \"Это только официальное спасибо,\" заявляет она с совершенно неофициальной улыбкой."
            return "Аманда усаживается к вам на колено, пересчитывает деньги прямо перед вашим лицом и шепчет на ухо такую непристойную версию благодарности, что сама начинает хихикать. Поднявшись, она еще раз дразняще прижимается бедрами."
        if girl_key == "liza":
            if corruption < 15:
                return "Лизетта принимает премию с изящным поклоном и благодарит так серьезно, будто вы вручаете ей награду перед всем городом. Только лукавый блеск в глазах выдает, насколько она довольна."
            if corruption < 35:
                return "Лизетта целует кончики пальцев и переносит поцелуй на вашу щеку. \"За щедрость надо платить хорошим настроением,\" говорит она и демонстративно поправляет вырез рабочего платья."
            if corruption < 60:
                return "Лизетта прижимается грудью к вашей руке и медленно целует вас в губы. \"Вот теперь девушки точно поймут, за какого хозяина стоит стараться,\" шепчет она, не спеша отстраняться."
            return "Лизетта садится рядом так тесно, что ее бедро оказывается поверх вашего, и с улыбкой вкладывает одну монету вам за ворот. \"На счастье, хозяин. Остальное я сохраню для нарядов, которые помогут заработать следующую премию.\""
        if girl_key == "georgett":
            if corruption < 15:
                return "Жоржетта удивленно вскидывает брови, затем благодарит вас с непривычной искренностью. Для женщины, привыкшей заранее договариваться о каждой монете, такая премия оказывается настоящим сюрпризом."
            if corruption < 35:
                return "Жоржетта весело целует вас в щеку и обещает, что клиенты сегодня увидят самую приветливую улыбку во всем городе. На прощание она легонько щиплет вас за бок — уже как знакомого, а не нанимателя."
            if corruption < 60:
                return "Жоржетта обнимает вас и медленно проводит ладонью по груди. \"Умный хозяин знает, что довольная работница особенно убедительна,\" мурлычет она, оставляя долгий поцелуй у вашего уха."
            return "Жоржетта прижимается бедрами, целует вас в губы и шепчет, что премия — отличный повод весь день вспоминать о щедром хозяине. Ее ладонь скользит почти неприлично низко, прежде чем она смеясь отступает."
        name = str(people_display_name(girl_key) or girl_key)
        if corruption < 35:
            return "%s принимает премию с искренней благодарностью и обещает, что на этой неделе команда постарается не хуже прежнего." % name
        return "%s благодарит вас теплым объятием и неожиданно смелым поцелуем, превращая деловую раздачу денег в куда более личный момент." % name

    def tavern_upstairs_can_enter_sandra_room():
        return int(Sandra.rel or 0) >= 10 or int(threads["sandraWeeklyEvaluation"].num or 0) > 0

    def tavern_sandra_room_door_locked():
        return bedroom_door_locked("TavernSandraRoom")

    def tavern_sandra_room_picture():
        slot = int(calendar_v2.time_slot())
        if slot >= 4:
            for picture_path in (
                "images/sandra/sleeps .png",
                "images/sandra/player_room_sandra_0.jpg",
                "images/sandra/talk_0.png",
            ):
                if renpy.loadable(picture_path):
                    return picture_path
        if slot == 0:
            for picture_path in (
                "images/sandra/player_room_sandra_0.jpg",
                "images/sandra/talk_0.png",
            ):
                if renpy.loadable(picture_path):
                    return picture_path
        if str(people.location("sandra") or "") == "TavernSandraRoom":
            for picture_path in (
                "images/sandra/talk_0.png",
                "images/sandra/player_room_sandra_0.jpg",
            ):
                if renpy.loadable(picture_path):
                    return picture_path
        return str(rooms.get("TavernSandraRoom").bg_picture or "") or None

    def tavern_sandra_ledger_picture():
        for picture_path in (
            "images/sandra/sandra_room_booking.png",
            "images/sandra/talk_0.png",
            "images/sandra/player_room_sandra_0.jpg",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def tavern_sandra_room_text():
        text = str(rooms.get("TavernSandraRoom").descriptions[0].text or "")
        issue_notice = str(household_room_issue_notice_text("sandra") or "").strip()
        if issue_notice:
            text += "\n\n" + issue_notice
        return werecat_append_visible_text(text, "TavernSandraRoom")

    def tavern_sandra_room_get_object(object_id):
        object_key = str(object_id or "").strip()
        for room_object in rooms.get("TavernSandraRoom").visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    def tavern_sandra_room_action_items():
        items = []
        for issue_action in list(household_room_issue_action_specs("sandra") or []):
            items.append(MenuItem(str(issue_action.get("label", "") or ""), Call(str(issue_action.get("target", "") or ""), *tuple(issue_action.get("args", ()) or ()))))
        if str(people.location("sandra") or "") == "TavernSandraRoom" and people.can_talk("sandra") and int(Sandra.rel or 0) >= 5 and int(Sandra.asked_today or 0) == 0:
            items.append(MenuItem("Сесть с Сандрой над трактирной книгой", Call("TavernSandraLedgerScene")))
        items.extend(story_event_action_items("TavernSandraRoom"))
        if Sandra.relationship_allows("intimacy") and str(people.location("sandra") or "") == "TavernSandraRoom":
            items.append(MenuItem("Заняться сексом с Сандрой", Call("HouseholdSexEngine", "sandra", "TavernSandraRoom", "sex")))
            if player.intimacy.can_cum():
                items.append(MenuItem("Попросить Сандру помочь рукой", Call("HouseholdSexEngine", "sandra", "TavernSandraRoom", "handjob")))
                items.append(MenuItem("Попросить Сандру сделать минет", Call("HouseholdSexEngine", "sandra", "TavernSandraRoom", "blowjob")))
        if tavern_upstairs_can_clean_rooms():
            items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernSandraRoom", "", "")))
        items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernSandraRoom")))
        for room_object in rooms.get("TavernSandraRoom").visible_game_items():
            items.append(MenuItem(room_object.name, Call("TavernSandraRoomObjectMenu", room_object.object_id)))
        for room_exit in rooms.get("TavernSandraRoom").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target)))
        return items

    TavernSandraRoomRoomDefinition = Room(
        code_name="TavernSandraRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Комната Сандры",
        bg_picture="images/tavern/secondfloor/sandra_room.png",
        descriptions=[
            RoomDescription(
                text="Вы осторожно заглядываете в комнату Сандры. Здесь все прибрано куда аккуратнее, чем в остальных комнатах: кровать застелена, вещи уложены, а у стены стоит небольшой ларь.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в коридор", target="TavernUpstairs"),
        ],
        game_items=[
            bedroom_door_object("sandra_room_door_001", "TavernSandraRoom", "Сандры"),
        ],
        custom_properties={
            "object_menu_label": "TavernSandraRoomObjectMenu",
        },
    )


label TavernSandraRoom:
    if tavern_sandra_room_door_locked():
        $ rooms.enter("TavernUpstairs")
        $ scene_runtime.picture = ""
        $ scene_runtime.text = "Дверь в комнату Сандры заперта. Пока она не начала вам по-настоящему доверять, лезть туда рано."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Наверху"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = tavern_upstairs_action_items()
        while True:
            call screen main_ui
    $ rooms.enter("TavernSandraRoom")
    $ scene_runtime.picture = tavern_sandra_room_picture()
    if scene_runtime.picture:
        vscene scene_runtime.picture
    $ scene_runtime.text = tavern_sandra_room_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Комната Сандры"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    while True:
        call screen main_ui


label TavernSandraRoomObjectMenu(object_id=""):
    $ renpy.dynamic("_room_object")
    $ renpy.dynamic("_room_action", "_room_args")
    $ _room_object = tavern_sandra_room_get_object(object_id)
    if _room_object is None:
        $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
        return

    $ main_ui_runtime.object_id = object_id
    $ scene_runtime.text = bedroom_door_object_text(_room_object)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(_room_object.name or "Комната Сандры")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _room_action in _room_object.visible_actions():
            if _room_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call("TavernSandraRoomObjectText", object_id, _room_action.action_id)))
            elif _room_action.hook == "call" and str(_room_action.target or "") != "":
                _room_args = tuple(getattr(_room_action, "args", ()) or ())
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "picture", tavern_sandra_room_picture() or rooms.get("TavernSandraRoom").bg_picture or None),
            SetField(scene_runtime, "text", tavern_sandra_room_text()),
            SetField(scene_runtime, "location_text", tavern_sandra_room_text()),
            SetField(main_ui_runtime, "action_title", "Комната Сандры"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_sandra_room_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label TavernSandraRoomObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_room_action", "_room_name", "_room_object", "_room_text")
    python:
        _room_text = ""
        _room_name = ""
        _room_object = tavern_sandra_room_get_object(object_id)
        if _room_object is not None:
            _room_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _room_text = str(_room_action.target or "")
                    break
        if _room_text:
            scene_runtime.text = _room_text
            scene_runtime.location_text = _room_text
            main_ui_runtime.action_title = _room_name or "Комната Сандры"
    return


label TavernSandraLedgerScene:
    $ renpy.dynamic("_sandra_ledger_picture", "_ledger_stories", "_ledger_idx", "_premium_eval_stamp", "_premium_workers", "_premium_worker_ids", "_premium_worker_count", "_premium_total_25", "_premium_total_50", "_premium_total_100", "_premium_total_200", "_premium_total_500", "_premium_amount", "_premium_decision", "_premium_total", "_premium_mana_gain", "_premium_skill_gain", "_premium_team_names", "_premium_info", "_premium_job_key", "_premium_skill_key", "_premium_skill_before", "_premium_skill_after", "_premium_candidate", "_premium_index", "_premium_person", "_premium_person_info", "_premium_person_corruption", "_premium_picture", "_premium_text")
    $ Sandra.mark_asked()
    $ Sandra.mark_talked()
    $ Sandra.change_social(friend_delta=1, open_delta=1)
    $ player.change_stat("fun", 1)
    $ calendar_v2.advance_minutes(30)
    $ main_ui_runtime.action_items = tavern_sandra_room_action_items()
    $ main_ui_begin_native_scene_state("Трактирные книги")
    show screen main_ui
    $ _sandra_ledger_picture = str(tavern_sandra_ledger_picture() or "")
    if _sandra_ledger_picture != "":
        $ scene_runtime.picture = _sandra_ledger_picture
        vscene _sandra_ledger_picture
    python:
        _ledger_stories = [
            "Вы с Сандрой усаживаетесь над трактирной книгой и какое-то время вместе сводите расходы, припасы и долги по мелочам. Постепенно сухие цифры переходят в разговор, и Сандра неожиданно вспоминает, как еще совсем молодой девчонкой училась считать закупки не по записям, а по памяти, потому что старшие все равно не доверяли ей книги. \"Ошибешься раз-другой, зато потом уже не забываешь,\" замечает она с сухой усмешкой.",
            "Вы раскладываете на кровати трактирные записи, и Сандра быстро втягивается в подсчеты так, словно всегда только этим и занималась. Когда дело доходит до старых долгов и привычек постоянных гостей, она вдруг рассказывает пару историй о тех временах, когда в доме все держалось не на деньгах, а на умении помнить, кто сколько наобещал и кто потом непременно попытается прикинуться забывчивым.",
            "Пока вы вместе перебираете счета и прикидываете, на чем трактир теряет больше всего, Сандра неожиданно начинает рассказывать о себе куда больше обычного. О том, как рано привыкла считать не только деньги, но и силы людей вокруг; кто вынослив, кто ленив, кто сорвется, а кто вытянет весь день на одной злости. В ее голосе почти нет жалобы, только старая привычка держать дом на своих плечах и заранее думать за всех остальных.",
        ]
        _ledger_idx = int(calendar_v2.daysInGame + calendar_v2.hour + int(Sandra.rel or 0)) % len(_ledger_stories)
        scene_runtime.text = _ledger_stories[_ledger_idx]
        scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass

    python:
        _premium_eval_stamp = str(player.tavern_management.weekly_chores_last_eval_stamp or "")
        _premium_workers = [
            (girl_id, info)
            for girl_id, info in people.girl_items()
            if info.is_tavern_worker()
        ]
        _premium_worker_ids = set([girl_id for girl_id, info in _premium_workers])
        _premium_worker_count = len(_premium_workers)
        _premium_total_25 = 25 * _premium_worker_count
        _premium_total_50 = 50 * _premium_worker_count
        _premium_total_100 = 100 * _premium_worker_count
        _premium_total_200 = 200 * _premium_worker_count
        _premium_total_500 = 500 * _premium_worker_count
        _premium_amount = 0
        _premium_decision = ""

    if _premium_eval_stamp != "" and str(player.tavern_management.team_premium_last_eval_stamp or "") != _premium_eval_stamp and _premium_worker_count > 0:
        $ _premium_team_names = ", ".join([people_display_name(girl_id) for girl_id, info in _premium_workers])
        $ scene_runtime.text = "Закончив со счетами, вы с Сандрой переходите к премиям за прошедшую неделю. Сейчас в трактирной команде: %s. Сумма ниже указана для каждого работника, а рядом — общий расход." % _premium_team_names
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Выдать по 25 мараведи — всего [_premium_total_25]" if int(player.economy.money or 0) >= _premium_total_25:
                $ _premium_amount = 25
                $ _premium_decision = "paid"

            "Выдать по 50 мараведи — всего [_premium_total_50]" if int(player.economy.money or 0) >= _premium_total_50:
                $ _premium_amount = 50
                $ _premium_decision = "paid"

            "Выдать по 100 мараведи — всего [_premium_total_100]" if int(player.economy.money or 0) >= _premium_total_100:
                $ _premium_amount = 100
                $ _premium_decision = "paid"

            "Выдать по 200 мараведи — всего [_premium_total_200]" if int(player.economy.money or 0) >= _premium_total_200:
                $ _premium_amount = 200
                $ _premium_decision = "paid"

            "Выдать по 500 мараведи — всего [_premium_total_500]" if int(player.economy.money or 0) >= _premium_total_500:
                $ _premium_amount = 500
                $ _premium_decision = "paid"

            "На этой неделе оставить команду без премии":
                $ _premium_decision = "declined"

            "Вернуться к решению позже":
                $ _premium_decision = "deferred"

        if _premium_decision == "declined":
            $ player.tavern_management.team_premium_last_eval_stamp = _premium_eval_stamp
            $ scene_runtime.text = "Вы решаете, что на этой неделе общей премии не будет. Сандра заносит решение в трактирную книгу и закрывает страницу с расчетами."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Закончить подсчеты":
                    pass

        elif _premium_decision == "paid":
            $ _premium_total = _premium_amount * _premium_worker_count
            $ _premium_mana_gain, _premium_skill_gain = TAVERN_TEAM_PREMIUM_REWARDS[_premium_amount]
            $ player.spend_money(_premium_total)
            $ player.tavern_management.team_premium_last_eval_stamp = _premium_eval_stamp
            python:
                for _premium_candidate, _premium_info in _premium_workers:
                    _premium_info.change_social(friend_delta=1)
                    _premium_info.reward_need_fulfilled(_premium_mana_gain, "team_premium")
                    if _premium_skill_gain > 0:
                        for _premium_job_key, _premium_skill_key in TAVERN_TEAM_PREMIUM_JOB_SKILLS:
                            if int(_premium_info.job_value(_premium_job_key, 0) or 0) <= 0:
                                continue
                            _premium_skill_before = _premium_info.skill_value(_premium_skill_key, 0)
                            _premium_skill_after = _premium_info.change_skill(_premium_skill_key, _premium_skill_gain)
                            if _premium_skill_after > _premium_skill_before:
                                _premium_info.record_skill_gain(_premium_skill_key, _premium_skill_after - _premium_skill_before)
            $ player.change_stat("fun", 3)
            $ _premium_person = ""
            $ scene_runtime.text = "Вы и Сандра приглашаете работников и раздаете премии: по %d мараведи каждому, всего %d. Деньги сразу поднимают настроение команды, а ваше признание их труда — желание работать лучше и держаться за трактир." % (_premium_amount, _premium_total)
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Раздать премии":
                    pass
            $ _premium_index = 0
            while _premium_index < len(_premium_workers):
                $ _premium_candidate, _premium_info = _premium_workers[_premium_index]
                $ _premium_picture = tavern_premium_reaction_picture(_premium_candidate)
                if _premium_picture:
                    vscene _premium_picture
                $ scene_runtime.text = tavern_premium_reaction_text(_premium_candidate, _premium_info.corruption)
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Продолжить":
                        $ _premium_index += 1

            menu:
                "Выделить еще одну личную премию" if int(player.economy.money or 0) >= _premium_amount:
                    menu:
                        "Дополнительно наградить Сандру — [_premium_amount] мараведи" if "sandra" in _premium_worker_ids:
                            $ _premium_person = "sandra"

                        "Дополнительно наградить Мелиссу — [_premium_amount] мараведи" if "melissa" in _premium_worker_ids:
                            $ _premium_person = "melissa"

                        "Дополнительно наградить Аманду — [_premium_amount] мараведи" if "amanda" in _premium_worker_ids:
                            $ _premium_person = "amanda"

                        "Дополнительно наградить Лизетту — [_premium_amount] мараведи" if "liza" in _premium_worker_ids:
                            $ _premium_person = "liza"

                        "Дополнительно наградить Жоржетту — [_premium_amount] мараведи" if "georgett" in _premium_worker_ids:
                            $ _premium_person = "georgett"

                        "Никого дополнительно не награждать":
                            pass

                "Закончить разговор о премиях":
                    pass

            if _premium_person != "":
                $ _premium_person_info = people.get_info(_premium_person)
                $ _premium_person_corruption = int(_premium_person_info.corruption or 0)
                $ player.spend_money(_premium_amount)
                $ _premium_person_info.change_social(friend_delta=1, corruption_delta=1)
                $ _premium_person_info.reward_need_fulfilled(max(2, _premium_mana_gain), "personal_premium")
                $ _premium_picture = tavern_premium_reaction_picture(_premium_person)
                if str(_premium_picture or "").strip():
                    vscene _premium_picture
                $ _premium_text = tavern_premium_reaction_text(_premium_person, _premium_person_corruption)
                $ scene_runtime.text = _premium_text
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Продолжить":
                        pass

    $ main_ui_end_native_scene_state()
    return
