# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.exports as renpy

    def _household_seen_key(event_code="", day_marker=None):
        return "%s:%s" % (str(event_code or ""), current_game_day() if day_marker is None else int(day_marker or 0))

    def household_runtime_event_seen_today(event_code="", day_marker=None):
        return int(household.runtime_event_seen.get(_household_seen_key(event_code, day_marker), 0) or 0) == 1

    def household_mark_runtime_event_seen(event_code="", day_marker=None):
        household.runtime_event_seen[_household_seen_key(event_code, day_marker)] = 1
        return 1

    def _household_insight_topics(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "melissa":
            return [
                {
                    "min_friend": 8,
                    "label": "Спросить Мелиссу о слухах в трактире",
                    "text": "Вы просите Мелиссу рассказать, что она успела заметить и услышать в трактире. Она понижает голос и спокойно отвечает, что больше всего правды всплывает не в криках, а в полушепоте: у стойки, на лестнице и у дверей комнат. \"Если хочешь понимать, что у людей на уме, слушай не тех, кто шумит, а тех, кто думает, что их никто не слышит,\" замечает она.",
                },
                {
                    "min_friend": 10,
                    "label": "Спросить Мелиссу о полезных хозяйственных хитростях",
                    "text": "Мелисса неожиданно делится вполне практичной хитростью: сухой мох в хозяйстве ценится куда выше сырого. \"Высушишь как следует, истолчешь, и уже можно думать не только о растопке. А если еще есть тряпье, из полос ткани и сухого мха выходят неплохие перевязки. Пять хороших полос ткани и вовсе можно пустить на крепкую веревку,\" объясняет она.",
                },
                {
                    "min_friend": 12,
                    "label": "Спросить Мелиссу о том, что ее по-настоящему тревожит",
                    "text": "После недолгой паузы Мелисса признается, что ее сильнее всего изматывает не сама работа, а ощущение, будто в доме никогда не бывает по-настоящему тихо. \"Когда в кладовой крысы, под потолком шуршат мыши, а по коридору кто-то топает среди ночи, начинаешь злиться не на людей, а на весь дом сразу. Если в доме спокойно, и мне легче дышится,\" говорит она уже без привычной резкости.",
                },
                {
                    "min_friend": 15,
                    "label": "Спросить Мелиссу о самых неловких разговорах и желаниях",
                    "text": "Мелисса сначала смотрит на вас испытующе, но все же решается говорить откровеннее. Она признается, что в большом доме люди очень быстро начинают слышать больше, чем им положено: ночные шаги, тихие стоны, чужие шепоты и разговоры о том, кто к кому тянется. \"Иногда это просто слухи. А иногда по таким мелочам заранее понимаешь, где скоро начнется новая история,\" произносит она и чуть заметно отводит взгляд.",
                },
            ]
        if girl == "sandra":
            return [
                {
                    "min_friend": 8,
                    "label": "Спросить Сандру о припасах и кухонных хитростях",
                    "text": "Сандра сразу уходит в хозяйственные подробности. Она напоминает, что ягоды, грибы, мед и мясо лучше не таскать без толку по карманам, а сразу нести на кухню. \"Из таких вещей потом и завтрак выходит, и похлебка, и нормальный стол для всей челяди. Если дом сытый, всем проще и работать, и не грызться друг с другом,\" говорит она.",
                },
                {
                    "min_friend": 10,
                    "label": "Спросить Сандру о мыле и полезных заготовках",
                    "text": "Сандра охотно возвращается к мыловарению и объясняет, что хорошее домашнее мыло любит терпение. \"Лаванда и роза для такого дела самое оно. Только не думай, что сварил и сразу пользуйся: мылу надо вылежаться как следует. Зато потом и людям приятно, и в доме будто чище дышится,\" деловито замечает она.",
                },
                {
                    "min_friend": 12,
                    "label": "Спросить Сандру о старых местных историях",
                    "text": "Сандра, понизив голос, говорит, что в округе полно мест, о которых лучше знать заранее, чем натыкаться на них случайно. По ее словам, люди годами передают друг другу полузабытые рассказы про запертые комнаты, тайные проходы и странные углы, куда никто не ходит без причины. \"Легенды легендами, а лишняя осторожность еще никому не вредила,\" подводит она итог.",
                },
                {
                    "min_friend": 15,
                    "label": "Спросить Сандру о людях, вине и танцах",
                    "text": "Сандра признается, что лучше всего характер людей виден в те вечера, когда всем становится чуть веселее обычного. За столом, после хорошей еды, кружки вина или перед самыми танцами многие начинают говорить свободнее и смотреть друг на друга уже не так, как днем. \"Кто чего стоит, проще всего понять не в работе, а когда людям кажется, что за ними никто особенно не следит,\" сухо замечает она.",
                },
            ]
        if girl == "amanda":
            return [
                {
                    "min_friend": 8,
                    "label": "Спросить Аманду о сплетнях и городских слухах",
                    "text": "Аманда оживляется почти сразу и начинает пересказывать, как быстро по городу расходятся слухи о клиентах, танцах и чужих романах. По ее словам, на рынке и в трактире люди сами выкладывают половину нужной правды, если дать им возможность почувствовать себя интересными. \"Хочешь знать, кто с кем водится, просто слушай, кто о ком слишком часто вспоминает,\" весело советует она.",
                },
                {
                    "min_friend": 10,
                    "label": "Спросить Аманду о тайных местах и прогулках",
                    "text": "Аманда, чуть понизив голос, рассказывает, что за лесом люди знают не только обычные тропы, но и места, куда забредают затем, чтобы их не тревожили. Она вспоминает старую водокачку, беседку и другие укромные уголки, где можно и поболтать, и спрятаться от лишних глаз. \"Если кто-то хочет секретов, он почти всегда идет не по дороге, а чуть в сторону,\" говорит она с понимающей улыбкой.",
                },
                {
                    "min_friend": 12,
                    "label": "Спросить Аманду о том, как люди флиртуют и чего хотят",
                    "text": "Аманда без особого смущения рассуждает о том, что люди очень редко говорят прямо, чего им хочется. Кто-то начинает чаще вертеться у стойки, кто-то ищет повод задержаться после разговора, а кто-то вдруг становится слишком щедрым на подарки и угощение. \"Если смотреть внимательно, почти любой флирт видно заранее. Особенно когда человек уверен, что отлично все скрывает,\" смеется она.",
                },
                {
                    "min_friend": 15,
                    "label": "Спросить Аманду о желаниях, платьях и смелых решениях",
                    "text": "Аманда неожиданно серьезнеет и говорит, что в доме многое меняется, когда кто-то один перестает стесняться чуть больше обычного. Новое платье, смелый танец, лишняя кружка или даже просто более дерзкий взгляд быстро подталкивают остальных попробовать то же самое. \"Стоит одной решиться, и всем остальным уже легче признаться, чего им самим давно хотелось,\" тихо замечает она.",
                },
            ]
        return []

    def household_special_talk_available(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        topics = list(_household_insight_topics(girl))
        if len(topics) <= 0:
            return False
        girl_info = people.get_info(girl)
        friend_value = int(getattr(girl_info, "rel", 0) or 0) if girl_info is not None else 0
        for topic in topics:
            if friend_value >= int(topic.get("min_friend", 0) or 0):
                return True
        return False

    def household_special_talk_entry(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        girl_info = people.get_info(girl)
        friend_value = int(getattr(girl_info, "rel", 0) or 0) if girl_info is not None else 0
        topics = [topic for topic in _household_insight_topics(girl) if friend_value >= int(topic.get("min_friend", 0) or 0)]
        if len(topics) <= 0:
            return None
        topic_index = int(getattr(girl_info, "var", {}).get("household_insight_index", 0) or 0) % len(topics)
        return dict(topics[topic_index])

    def household_advance_special_talk(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        girl_info = people.get_info(girl)
        if girl_info is None:
            return 0
        girl_info.var["household_insight_index"] = int(girl_info.var.get("household_insight_index", 0) or 0) + 1
        return int(girl_info.var["household_insight_index"] or 0)

    def melissa_storage_thanks_available():
        return (
            str(rooms.current_code or "") == "TavernStorage"
            and people_to_int(Melissa.storage_rat_help_day, -1) >= 0
            and people_to_int(Melissa.storage_thanks_day, -1) != current_game_day()
        )

    def melissa_room_problem_available():
        stage = threads["melissaBatProblem"].num
        temp_room = str(Melissa.temp_room_code or "").strip()
        return (
            str(rooms.current_code or "") == "TavernMelissaRoom"
            and (int(calendar_v2.hour or 0) >= 16 or int(calendar_v2.hour or 0) <= 5)
            and people_to_int(Melissa.storage_rat_help_day, -1) >= 0
            and stage == 3
            and temp_room == ""
        )

    def melissa_temp_room_text():
        temp_room = str(Melissa.temp_room_code or "")
        repair_day = people_to_int(Melissa.roof_repair_complete_day, -1)
        waiting_for_repair = repair_day >= 0
        if temp_room == "" or threads["melissaBatProblem"].num >= 8:
            return ""
        if temp_room == "TavernMyRoom":
            if waiting_for_repair:
                return "Из-за летучих мышей и щелей под крышей Мелисса пока держит часть вещей у вас и временно ночует в вашей комнате, пока не закончится заказанная починка крыши."
            return "Из-за летучих мышей и паутины Мелисса пока держит часть вещей у вас и готова временно ночевать в вашей комнате, пока вы не решите проблему."
        if temp_room == "TavernAmandaRoom":
            if waiting_for_repair:
                return "Из-за летучих мышей и щелей под крышей Мелисса пока ночует у Аманды и ждет, пока закончится заказанная починка крыши."
            return "Из-за летучих мышей и паутины Мелисса пока собирается ночевать у Аманды, пока вы не решите проблему."
        if temp_room == "TavernEmptyRoom":
            if waiting_for_repair:
                return "Из-за летучих мышей и щелей под крышей Мелисса пока перебралась в пустую комнату и ждет, пока закончится заказанная починка крыши."
            return "Из-за летучих мышей и паутины Мелисса пока присматривается к пустующей комнате, пока вы не решите проблему."
        return ""

    def household_dress_revealing_score(dress_code=""):
        dress_name = str(dress_code or "").strip()
        if dress_name == "":
            return 0
        top_part = str((DressTopPart or {}).get(dress_name, "") or "")
        bottom_part = str((DressBottomPart or {}).get(dress_name, "") or "")
        top_score = int((DressPartSlut or {}).get(top_part, 0) or 0)
        bottom_score = int((DressPartSlut or {}).get(bottom_part, 0) or 0)
        return max(top_score, bottom_score)

    def household_is_revealing_dress(dress_code=""):
        return household_dress_revealing_score(dress_code) >= 3

    def household_mark_revealing_dress_order(girl_name="", dress_code=""):
        girl = str(girl_name or "").strip().lower()
        dress_name = str(dress_code or "").strip()
        if girl == "" or dress_name == "" or not household_is_revealing_dress(dress_name):
            return 0

        if girl == "sandra":
            Sandra.revealing_dress_code = dress_name
        elif girl == "melissa":
            Melissa.revealing_dress_code = dress_name
        elif girl == "amanda":
            Amanda.revealing_dress_code = dress_name
        else:
            return 0
        return 1

    def household_soap_request_ready(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "":
            return False
        if int(crafting.soap_requests.get(girl, 0) or 0) <= 0:
            return False
        girl_info = people.get_info(girl)
        if girl_info is not None and int(girl_info.talked_today or 0) != 0:
            return False
        if soap_total_piece_count() > 0:
            return False
        last_day = int(getattr(girl_info, "var", {}).get("soap_request_last_day", -14) or -14)
        return current_game_day() - last_day >= 5

    def household_warm_drink_ready(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "":
            return False
        if household_morning_issue_type(girl) != "sick":
            return False
        if int(player.item_count("libido_tincture_001") or 0) <= 0:
            return False
        girl_info = people.get_info(girl)
        if girl_info is not None and int(girl_info.talked_today or 0) != 0:
            return False
        return current_game_day() - int(household.warm_drink_last_day.get(girl, -7) or -7) >= 1

    def household_room_issue_action_specs(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        issue_code = str(household_morning_issue_type(girl) or "").strip()
        rows = []
        if girl == "":
            return rows
        if issue_code == "sick":
            if girl == "amanda":
                rows.append({
                    "label": "Проверить, не притворяется ли Аманда",
                    "target": "HouseholdAmandaFakeSicknessWake",
                    "args": (),
                })
            if int(player.item_count("healing_potion_001") or 0) > 0:
                rows.append({
                    "label": "Принести %s лечебное зелье" % _action_display_name(girl),
                    "target": "HouseholdMorningIssueCure",
                    "args": (girl,),
                })
            if household_warm_drink_ready(girl):
                rows.append({
                    "label": "Согреть %s пряной настойкой" % _action_display_name(girl),
                    "target": "HouseholdMorningIssueWarmDrink",
                    "args": (girl,),
                })
            return rows
        if issue_code == "sleepy":
            rows.append({
                "label": "Разбудить %s" % _action_display_name(girl),
                "target": "HouseholdWakeSleepyGirl",
                "args": (girl,),
            })
        return rows

    def household_barber_request_ready(girl_name="", request_context=""):
        girl = str(girl_name or "").strip().lower()
        context_key = str(request_context or "").strip().lower()
        if girl == "":
            return False
        if context_key != "breakfast":
            return False
        if girl not in list(tavern_breakfast_present_ids() or []):
            return False
        girl_info = people.get_info(girl)
        if girl_info is not None and int(girl_info.talked_today or 0) != 0:
            return False
        if int(household.barber_appointments.get(girl, 0) or 0) == 1:
            return False
        if current_game_day() - int(household.barber_visit_last_day.get(girl, -14) or -14) < 14:
            return False
        if current_game_day() - int(household.barber_request_last_day.get(girl, -14) or -14) < 14:
            return False
        friend_thresholds = {"sandra": 7, "melissa": 6, "amanda": 5}
        openness_thresholds = {"sandra": 2, "melissa": 2, "amanda": 1}
        girl_info = people.get_info(girl)
        if girl_info is None:
            return False
        if int(girl_info.rel or 0) < int(friend_thresholds.get(girl, 99) or 99):
            return False
        return int(girl_info.openness or 0) >= int(openness_thresholds.get(girl, 99) or 99)

    def household_pending_request_girl(current_room=""):
        room_code = str(current_room or rooms.current_code or "").strip()
        room_girls = []
        if room_code == "TavernMain":
            room_girls = [girl for girl in ("amanda", "melissa", "sandra") if str(people.location(girl) or "") == "TavernMain"]
        elif room_code == "TavernKitchen":
            room_girls = [girl for girl in ("amanda", "melissa", "sandra") if str(people.location(girl) or "") == "TavernKitchen"]
        for girl in room_girls:
            if household_soap_request_ready(girl):
                return ("soap", girl)
        return ("", "")

    def melissa_clara_overhear_ready():
        return (
            str(rooms.current_code or "") == "TavernMain"
            and str(people.location("melissa") or "") == "TavernMain"
            and str(people.location("clara") or "") == "TavernMain"
            and 11 <= int(calendar_v2.hour or 0) <= 12
            and not household_runtime_event_seen_today("melissa_clara_overhear")
        )

    def melissa_clara_overhear_variant():
        return int(current_game_day() + int(calendar_v2.week or 0) + int(calendar_v2.hour or 0)) % 2

    def tavern_storage_rat_event_ready():
        return (
            str(rooms.current_code or "") == "TavernStorage"
            and 6 <= int(calendar_v2.hour or 0) <= 7
            and int(calendar_v2.week or 0) != 7
            and str(people.location("melissa") or "") == "TavernStorage"
            and people_to_int(Melissa.storage_rat_help_day, -1) < 0
            and not household_runtime_event_seen_today("melissa_storage_rat")
        )

    def melissa_night_wake_event_ready(return_location=""):
        return (
            str(return_location or "") == "TavernMyRoom"
            and current_game_day() >= 21
            and not household_runtime_event_seen_today("melissa_night_wake")
            and procedural_randint(1, 4, "melissa_night_wake_%s" % current_game_day()) == 1
        )

label HouseholdSoapRequestEvent(girl_name=""):
    $ renpy.dynamic("_soap_girl", "_soap_info", "_soap_preferred", "_soap_last_label")
    $ _soap_girl = str(girl_name or "").strip().lower()
    if _soap_girl == "":
        if player.tavern_management.breakfast.event_active:
            $ tavern_kitchen_set_saved_text(scene_runtime.text)
            call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    $ household.soap_request_last_day[_soap_girl] = current_game_day()
    $ _soap_info = people.get_info(_soap_girl)
    if _soap_info is not None:
        $ _soap_info.mark_talked(1)
    $ _soap_preferred = household_soap_preferred_aroma_text(_soap_girl)
    $ _soap_last_label = soap_last_batch_label()
    if _soap_girl == "sandra":
        $ scene_runtime.text = "Сандра перехватывает вас на минуту и, чуть понизив голос, признает, что хорошее мыло в доме уже распробовали все. \"Если опять надумаешь варить, отложи мне кусок получше. Мне бы что-нибудь %s. После того %s и на кухне приятнее, и самой будто легче дышится,\" говорит она без обычной суровости." % (_soap_preferred, _soap_last_label)
    elif _soap_girl == "melissa":
        $ scene_runtime.text = "Мелисса, чуть смутившись, спрашивает, не найдется ли у вас еще хорошего мыла. \"После того куска я как-то совсем отвыкла от обычной серой дряни. Если снова сваришь, мне бы %s мыло... вроде того %s. Отложи мне один, ладно?\"" % (_soap_preferred, _soap_last_label)
    else:
        $ scene_runtime.text = "Аманда быстро переходит на заговорщический тон: \"Стефан, если у тебя опять будет %s мыло, не забудь про меня. После того %s и волосы лучше лежат, и сама чувствуешь себя совсем по-другому.\"" % (_soap_preferred, _soap_last_label)
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Сразу отдать роскошное мыло" if int(player.item_count("luxury_soap_001") or 0) > 0:
            call HouseholdSoapRequestGiveNow(_soap_girl, "luxury_soap_001")

        "Сразу отдать обычное мыло" if int(player.item_count("soap_001") or 0) > 0:
            call HouseholdSoapRequestGiveNow(_soap_girl, "soap_001")

        "Пообещать достать мыло позже":
            $ scene_runtime.text = "Вы обещаете, что не забудете о просьбе. Похоже, это заметно поднимает ей настроение."
            if _soap_info is not None:
                $ _soap_info.change_social(friend_delta=1)
            $ scene_runtime.location_text = scene_runtime.text
            if player.tavern_management.breakfast.event_active:
                call TavernKitchenBreakfastShowText(scene_runtime.text)

        "Отмахнуться пока что":
            $ scene_runtime.text = "Вы отвечаете, что пока вам не до мыла. Просьбу принимают без скандала, но без особой радости."
            $ scene_runtime.location_text = scene_runtime.text
            if player.tavern_management.breakfast.event_active:
                call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label HouseholdSoapRequestGiveNow(girl_name="", item_id="soap_001"):
    $ renpy.dynamic("_soap_girl", "_soap_item", "_soap_effect")
    $ _soap_girl = str(girl_name or "").strip().lower()
    $ _soap_item = str(item_id or "soap_001").strip()
    if int(player.item_count(_soap_item) or 0) <= 0:
        $ scene_runtime.text = "У вас этого больше нет."
        $ scene_runtime.location_text = scene_runtime.text
        if player.tavern_management.breakfast.event_active:
            $ tavern_kitchen_set_saved_text(scene_runtime.text)
            call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    $ player.remove_item(_soap_item, 1)
    $ _soap_effect = player_apply_item_social_effects(_soap_girl, _soap_item, True)
    $ scene_runtime.text = "{} принимает подарок сразу, не скрывая удовольствия. {}".format(str(people_display_name(_soap_girl) or _soap_girl), str(_soap_effect.get("text", "") or "").strip())
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    if player.tavern_management.breakfast.event_active:
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label HouseholdBarberRequestEvent(girl_name=""):
    $ renpy.dynamic("_barber_girl", "_barber_info")
    $ _barber_girl = str(girl_name or "").strip().lower()
    if _barber_girl == "":
        if player.tavern_management.breakfast.event_active:
            $ tavern_kitchen_set_saved_text(scene_runtime.text)
            call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    $ household.barber_request_last_day[_barber_girl] = current_game_day()
    $ _barber_info = people.get_info(_barber_girl)
    if _barber_info is not None:
        $ _barber_info.mark_talked(1)
    if _barber_girl == "sandra":
        $ scene_runtime.text = "За завтраком вы сами поднимаете разговор о Серджио и предлагаете Сандре сходить к цирюльнику. Она сперва щурится с привычным недоверием, а потом все же кивает: \"Если уж ты решил тянуть трактир вверх, дом тоже должен выглядеть аккуратнее. И да, для трактира это тоже не пустяк: ухоженная хозяйка кухни дому только на пользу.\""
    elif _barber_girl == "melissa":
        $ scene_runtime.text = "За завтраком вы осторожно предлагаете Мелиссе сходить к Серджио. Она заметно смущается, но не отказывается: \"После хорошей стрижки и всех его притираний, наверное, даже чувствуешь себя иначе. И если я буду выглядеть аккуратнее, то и в зале, и по дому держаться проще.\""
    else:
        $ scene_runtime.text = "За завтраком вы предлагаете Аманде заглянуть к Серджио. Она оживляется почти сразу: \"Это было бы отлично! Он не только стрижет, он еще знает кучу смешных историй про чулки, нижнее белье и всякие женские хитрости. После такого и в трактире выглядеть веселее, и гостей держать на себе проще.\""
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Пообещать визит к Серджио":
            if _barber_info is not None:
                $ household.barber_appointments[_barber_girl] = 1
                $ _barber_info.change_social(friend_delta=1)
            $ scene_runtime.text = "Вы обещаете, что при первом удобном открытом дне Серджио отведете ее к цирюльнику. Просьбу явно услышали с удовольствием."

        "Сказать, что пока не до этого":
            $ scene_runtime.text = "Вы отвечаете, что пока у трактира и без того хватает расходов. На этом разговор сворачивается."
    $ scene_runtime.location_text = scene_runtime.text
    if player.tavern_management.breakfast.event_active:
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label SandraDressInitiativeEvent:
    $ renpy.dynamic("_sandra_scene")
    $ threads["sandraRevealingDressInitiative"].complete()
    $ _sandra_scene = tavern_kitchen_random_sandra_scene() if renpy.has_label("TavernKitchen") else ""
    if str(_sandra_scene or "").strip():
        $ scene_runtime.picture = _sandra_scene
    $ scene_runtime.text = "Сандра, улучив минуту без лишних ушей, задерживает вас у стола и вдруг говорит куда мягче обычного.\n\n\"Слушай, Стефан... после всех этих разговоров о Бекки я тут подумала. Если уж вдова может себе позволить иногда выглядеть поинтереснее, то, может, и мне пора перестать рядиться только в самое практичное. Не в девках ведь дело, а в том, чтобы и на меня иной раз посмотрели как на женщину. Если надумаешь, подбери мне у Ирмы что-нибудь посмелее обычного.\""
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Пообещать подобрать Сандре более смелый наряд":
            $ daily_events.add("sandra", "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")
            $ Sandra.change_social(friend_delta=1)
            $ scene_runtime.text = "Вы киваете Сандре и обещаете, что в ближайшее время заглянете с ней к Ирме и подберете что-нибудь заметно смелее ее обычных платьев. Сандра делает вид, что это пустяк, но по довольной полуулыбке видно: такой ответ ей пришелся по душе."

        "Сказать, что пока не время":
            $ scene_runtime.text = "Вы отвечаете Сандре, что с этим пока лучше не торопиться. Она только фыркает, возвращается к кастрюлям и делает вид, что разговор ничего для нее не значил."
    $ scene_runtime.location_text = scene_runtime.text
    if player.tavern_management.breakfast.event_active:
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label MelissaDressRequestEvent:
    $ renpy.dynamic("_melissa_dress_picture")
    $ threads["melissaRevealingDressRequest"].complete()
    $ _melissa_dress_picture = MelissaStaticData.image_path("portrait", "default")
    if str(_melissa_dress_picture or "").strip():
        $ scene_runtime.picture = _melissa_dress_picture
    $ scene_runtime.text = "Мелисса, дождавшись пока вокруг станет потише, смущенно признается: \"Я видела, какой наряд ты выбрал для Сандры. Если уж ей можно что-то посмелее, может и мне когда-нибудь подберешь платье не только для работы, но и чтобы самой себе нравиться?\"\n\nСказав это, она тут же опускает глаза, но по голосу слышно, что мысль ей давно не дает покоя."
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Согласиться подобрать Мелиссе похожий наряд":
            $ daily_events.add("melissa", "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")
            $ Melissa.change_social(friend_delta=1)
            $ scene_runtime.text = "Вы обещаете Мелиссе, что не забудете о ее просьбе и подберете у Ирмы что-нибудь похожее, но по ее характеру. Мелисса заметно оживляется и тихо благодарит вас."

        "Посоветовать ей пока не спешить":
            $ scene_runtime.text = "Вы мягко советуете Мелиссе пока не спешить с такими обновками. Девушка кивает, хотя по голосу слышно, что надеялась на другой ответ."
    $ scene_runtime.location_text = scene_runtime.text
    if player.tavern_management.breakfast.event_active:
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label AmandaDressRequestEvent:
    $ threads["amandaRevealingDressRequest"].complete()
    if renpy.loadable("images/amanda/amanda_portrate.jpg"):
        $ scene_runtime.picture = "images/amanda/amanda_portrate.jpg"
    $ scene_runtime.text = "Аманда сама подскакивает к вам, едва улучив момент. \"Стефан, это нечестно! У Сандры теперь наряд посмелее, Мелиссе ты тоже обещаешь что-то красивое, а я что, хуже? Мне тоже хочется платье, чтобы ахнули, а не только подносы таскать!\"\n\nПохоже, увиденное окончательно раззадорило ее самолюбие."
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Пообещать подобрать Аманде такой же смелый наряд":
            $ daily_events.add("amanda", "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")
            $ Amanda.change_social(friend_delta=1)
            $ scene_runtime.text = "Вы соглашаетесь, что раз уж в доме одна за другой появляются новые наряды, то и Аманду обделять не стоит. Услышав это, девушка сияет так, будто обновка уже висит у нее в шкафу."

        "Сказать, что пока хватит и чужих обновок":
            $ scene_runtime.text = "Вы осаживаете Аманду и говорите, что пока хватит и тех обновок, что уже обсуждаются в доме. Аманда недовольно надувает губы, но спорить не продолжает."
    $ scene_runtime.location_text = scene_runtime.text
    if player.tavern_management.breakfast.event_active:
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernStorageRatEvent:
    $ renpy.dynamic("_melissa_rat_picture")
    $ household_mark_runtime_event_seen("melissa_storage_rat")
    $ _melissa_rat_picture = MelissaStaticData.image_path("tavern", "rat")
    if str(_melissa_rat_picture or "").strip():
        $ scene_runtime.picture = _melissa_rat_picture
    $ scene_runtime.text = "В кладовой вас встречает раздраженная Мелисса: у мешков с крупой шуршит крупная крыса, а девушка уже стоит наготове с метлой в руках. \"Опять эта тварь сюда лазит,\" шепчет она. \"Если ее сейчас не прогнать, потом весь угол придется перебирать заново.\""
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Прибить крысу":
            $ Melissa.storage_rat_help_day = current_game_day()
            $ werecat_state()["rat_carcass_cached"] = 1
            $ werecat_state()["rats_problem_active"] = 1
            $ werecat_state()["rat_food_loss_next_day"] = current_game_day() + 7
            $ Melissa.skills["cleaning"] = min(100, int(Melissa.skills.get("cleaning", 0) or 0) + 1)
            $ Melissa.change_social(friend_delta=1)
            $ story_thread_advance_current()
            $ scene_runtime.text = "Вы быстро расправляетесь с крысой, и Мелисса заметно расслабляется. \"Вот теперь другое дело,\" тихо говорит она, уже без прежнего раздражения. На всякий случай вы решаете не выбрасывать тушку сразу: такая приманка еще может сгодиться, если в лесу и правда водится тот необычный кошачий охотник, о котором судачат по трактирам."

        "Оставить все как есть":
            $ scene_runtime.text = "Вы решаете не возиться с крысой прямо сейчас. Мелисса поджимает губы и берется переставлять мешки подальше от шороха, явно недовольная тем, что проблему придется терпеть еще какое-то время."
    $ scene_runtime.location_text = scene_runtime.text
    return


label HouseholdMorningIssueCure(girl_name=""):
    $ renpy.dynamic("_issue_girl", "_issue_info")
    $ _issue_girl = str(girl_name or "").strip().lower()
    if household_morning_issue_type(_issue_girl) != "sick":
        if player.tavern_management.breakfast.event_active:
            $ tavern_kitchen_set_saved_text(scene_runtime.text)
            call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    if int(player.item_count("healing_potion_001") or 0) <= 0:
        $ scene_runtime.text = "Без лечебного зелья тут пока не обойтись."
        $ scene_runtime.location_text = scene_runtime.text
        if player.tavern_management.breakfast.event_active:
            $ tavern_kitchen_set_saved_text(scene_runtime.text)
            call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    $ player.remove_item("healing_potion_001", 1)
    $ household_clear_morning_issue(_issue_girl)
    if _issue_girl == "amanda":
        $ Amanda.change_social(friend_delta=1, open_delta=1)
    elif _issue_girl == "melissa":
        $ Melissa.change_social(friend_delta=1, open_delta=1)
    else:
        $ _issue_info = people.get_info(_issue_girl)
        if _issue_info is not None:
            $ _issue_info.change_social(friend_delta=1, open_delta=1)
    $ scene_runtime.text = "%s с благодарностью принимает лечебное зелье. Через несколько минут ей заметно легчает, и она уже выглядит так, будто сможет вернуться к обычным делам." % _action_display_name(_issue_girl)
    $ scene_runtime.location_text = scene_runtime.text
    if player.tavern_management.breakfast.event_active:
        $ tavern_kitchen_set_saved_text(scene_runtime.text)
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return
label HouseholdMorningIssueWarmDrink(girl_name=""):
    $ renpy.dynamic("_issue_girl", "_issue_info")
    $ _issue_girl = str(girl_name or "").strip().lower()
    if not household_warm_drink_ready(_issue_girl):
        if player.tavern_management.breakfast.event_active:
            $ tavern_kitchen_set_saved_text(scene_runtime.text)
            call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    $ player.remove_item("libido_tincture_001", 1)
    $ household.warm_drink_last_day[_issue_girl] = current_game_day()
    $ _issue_info = people.get_info(_issue_girl)
    if _issue_info is not None:
        $ _issue_info.mark_talked(1)
    if _issue_girl == "amanda":
        $ Amanda.change_social(friend_delta=1, open_delta=1, corruption_delta=1)
    elif _issue_girl == "melissa":
        $ Melissa.change_social(friend_delta=1, open_delta=1, corruption_delta=1)
    else:
        if _issue_info is not None:
            $ _issue_info.change_social(friend_delta=1, open_delta=1, corruption_delta=1)
    if _issue_girl == "sandra":
        $ scene_runtime.text = "Сандра сначала кривится на саму идею пряной настойки с утра, но все же делает несколько осторожных глотков. Напиток быстро разгоняет холод по телу, и хозяйка уже не так сурово ворчит, признавая, что от такого внимания ей и правда легче."
    elif _issue_girl == "melissa":
        $ scene_runtime.text = "Мелисса принимает пряную настойку обеими руками и пьет медленно, будто растягивает не столько тепло, сколько саму вашу заботу. Через несколько минут она выглядит живее, хотя и признает, что ей все равно лучше отлежаться еще немного."
    else:
        $ scene_runtime.text = "Аманда с готовностью хватается за пряную настойку и почти сразу оживляется. \"Ну вот, совсем другое дело,\" заявляет она, явно наслаждаясь не только теплом в груди, но и самим поводом получить от вас чуть больше внимания."
    $ scene_runtime.location_text = scene_runtime.text
    if player.tavern_management.breakfast.event_active:
        $ tavern_kitchen_set_saved_text(scene_runtime.text)
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return
label HouseholdAmandaFakeSicknessWake:
    if household_morning_issue_type("amanda") != "sick":
        if player.tavern_management.breakfast.event_active:
            $ tavern_kitchen_set_saved_text(scene_runtime.text)
            call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    $ calendar_v2.advance_minutes(15)
    if int(Amanda.rel or 0) >= 6 or int(Amanda.talked_today or 0) >= 2:
        $ household_clear_morning_issue("amanda")
        $ scene_runtime.text = "Вы не спорите у двери, а спокойно садитесь рядом и просите Аманду хотя бы раз сказать честно, плохо ей или просто не хочется вставать. Она сперва обиженно сопит, потом все же сдается: \"Ладно... больше лени, чем болезни.\" Через несколько минут она уже нехотя натягивает платье и обещает выйти к общему столу."
        $ Amanda.change_social(friend_delta=1, open_delta=1)
    else:
        $ household_clear_morning_issue("amanda")
        $ scene_runtime.text = "Вы резко пресекаете Амандину \"болезнь\" и велите ей подниматься. Она фыркает, жалуется на жестокость и нарочно долго возится с одеждой, но все же встает. Похоже, сегодня это было скорее представление, чем настоящая слабость."
        $ Amanda.change_social(friend_delta=-1)
    $ scene_runtime.location_text = scene_runtime.text
    if player.tavern_management.breakfast.event_active:
        $ tavern_kitchen_set_saved_text(scene_runtime.text)
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return
label HouseholdWakeSleepyGirl(girl_name=""):
    $ renpy.dynamic("_wake_girl", "_wake_indecent", "_wake_bulge", "_wake_info")
    $ _wake_girl = str(girl_name or "").strip().lower()
    if household_morning_issue_type(_wake_girl) != "sleepy":
        if player.tavern_management.breakfast.event_active:
            $ tavern_kitchen_set_saved_text(scene_runtime.text)
            call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    $ _wake_indecent = household_morning_issue_indecent(_wake_girl)
    $ _wake_bulge = 1 if _wake_indecent and player_has_visible_morning_bulge() else 0
    $ calendar_v2.advance_minutes(20)
    $ household_clear_morning_issue(_wake_girl)
    if _wake_girl == "amanda":
        $ Amanda.change_social(friend_delta=1)
    elif _wake_girl == "melissa":
        $ Melissa.change_social(friend_delta=1)
    else:
        $ _wake_info = people.get_info(_wake_girl)
        if _wake_info is not None:
            $ _wake_info.change_social(friend_delta=1)
    if _wake_girl == "sandra":
        $ scene_runtime.text = "Вы осторожно будите Сандру. Та сначала недовольно морщится, потом резко собирается, будто сама сердится не на вас, а на то, что дала себе лишнюю слабину."
        if _wake_indecent:
            $ scene_runtime.text = str(scene_runtime.text or "") + "\nПока Сандра поднималась, вы невольно успели заметить, что рубаха на ней сбилась куда выше приличного. Поймав ваш взгляд, она без лишней суеты поправляет ткань, но в ее лице на миг мелькает совсем не хозяйская, а женская неловкость."
            $ Sandra.change_social(corruption_delta=1)
        if _wake_bulge:
            if int(Sandra.rel or 0) >= 10 or int(Sandra.corruption or 0) >= 20:
                $ scene_runtime.text = str(scene_runtime.text or "") + "\nСандра успевает заметить и вашу слишком уж явную выпуклость под одеждой. Вместо скандала она только сухо хмыкает: \"Вот и думай после этого, кто тут проспал по-настоящему.\""
                $ Sandra.change_social(open_delta=1)
            else:
                $ scene_runtime.text = str(scene_runtime.text or "") + "\nКогда Сандра замечает, что у вас под одеждой все слишком уж на виду, она мгновенно щурится и велит вам сперва привести себя в порядок, а уже потом лезть кого-то будить."
    elif _wake_girl == "melissa":
        $ scene_runtime.text = "Вы будите Мелиссу тихо, но настойчиво. Она вздрагивает, садится на кровати и явно с трудом возвращается в явь, потом понимает, который час, и недовольно выдыхает себе под нос."
        if _wake_indecent:
            $ scene_runtime.text = str(scene_runtime.text or "") + "\nВо сне одеяло успело сползти, и вам открывается куда больше, чем Мелисса обычно позволяет увидеть днем. Осознав это, она быстро оправляется, но вместо злости в ее лице остается скорее смущенное раздражение."
            $ Melissa.change_social(corruption_delta=1)
        if _wake_bulge:
            if int(Melissa.rel or 0) >= 10 or int(Melissa.corruption or 0) >= 18:
                $ scene_runtime.text = str(scene_runtime.text or "") + "\nМелисса замечает вашу выпуклость под штанами, замолкает на полуслове и опускает взгляд. Потом, уже тише, чем прежде, бросает: \"Ну... в следующий раз хоть стучи чуть дольше.\""
                $ Melissa.change_social(open_delta=1)
            else:
                $ scene_runtime.text = str(scene_runtime.text or "") + "\nКогда Мелисса замечает, что вы явились будить ее в слишком уж красноречивом состоянии, она вспыхивает и немедленно отворачивается, явно желая закончить разговор как можно быстрее."
    else:
        $ scene_runtime.text = "Вы будите Аманду, и та сперва лишь что-то недовольно бурчит в подушку. Но стоит ей понять, что утренний стол уже давно собирается без нее, как она мигом оживает и принимается оправдываться."
        if _wake_indecent:
            $ scene_runtime.text = str(scene_runtime.text or "") + "\nВо сне Аманда успела раскрыться куда сильнее приличного, и вам открывается достаточно, чтобы понять: спать скромницей она умеет не всегда. Поняв по вашему лицу, что вы успели увидеть лишнее, она сперва краснеет, а потом упрямо делает вид, будто это пустяк."
            $ Amanda.change_social(corruption_delta=1)
        if _wake_bulge:
            if int(Amanda.rel or 0) >= 10 or int(Amanda.corruption or 0) >= 30:
                $ scene_runtime.text = str(scene_runtime.text or "") + "\nАманда быстро замечает и вашу предательскую выпуклость. Вместо того чтобы смутиться, она хихикает, бросает на вас хитрый взгляд и только потом начинает поспешно поправлять одежду."
                $ Amanda.change_social(corruption_delta=1)
            else:
                $ scene_runtime.text = str(scene_runtime.text or "") + "\nСтоит Аманде заметить ваш слишком уж выразительный стояк, как она фыркает, закатывает глаза и тут же прикрывается одеялом уже куда тщательнее."
    $ scene_runtime.location_text = scene_runtime.text
    if player.tavern_management.breakfast.event_active:
        $ tavern_kitchen_set_saved_text(scene_runtime.text)
        call TavernKitchenBreakfastShowText(scene_runtime.text)
    return
label MelissaNightWakeEvent:
    $ household_mark_runtime_event_seen("melissa_night_wake")
    $ scene_runtime.text = "Вы уже почти проваливаетесь в сон, когда в дверь осторожно, но настойчиво стучат. На пороге оказывается встревоженная Мелисса: то ли в ее комнате снова шуршит какая-то дрянь под потолком, то ли из темного угла опять выскочила крыса. Одной ей туда возвращаться совсем не хочется."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Ночная просьба Мелиссы"
    menu:
        "Спокойно пойти с ней и помочь":
            $ calendar_v2.advance_minutes(20)
            $ Melissa.change_social(friend_delta=1)
            $ scene_runtime.text = "Вы поднимаетесь вместе с Мелиссой, быстро прогоняете ночную дрянь из ее комнаты и помогаете ей успокоиться. На прощание она благодарит вас уже куда мягче обычного: видно, что такая помощь ей важна."

        "Успокоить, прижать к себе и потом помочь":
            $ calendar_v2.advance_minutes(30)
            $ Melissa.change_social(friend_delta=1, open_delta=1, corruption_delta=2)
            $ player.change_stat("fun", 3)
            $ scene_runtime.text = "Вы сначала притягиваете Мелиссу к себе и даете ей выдохнуть в тишине, а уже потом идете разбираться с шорохами. Когда все заканчивается, она еще ненадолго остается рядом, благодарит вас шепотом и уходит заметно теплее и смелее, чем пришла."

        "Проворчать и отправить ее обратно":
            $ Melissa.change_social(friend_delta=-1)
            $ scene_runtime.text = "Вы бурчите, что ночью вам не до таких хлопот, и отправляете Мелиссу разбираться самой. Она ничего не отвечает, но по ее лицу видно, что такой ответ ей очень не по душе."
    $ scene_runtime.location_text = scene_runtime.text
    return
