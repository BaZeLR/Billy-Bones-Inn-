default fire_state = 0
default hot_water_state = 0

default TavernKitchenNoticeText = ""
default TavernKitchenNoticePending = False
default TavernKitchenSavedText = ""
default BeckyKitchenVisitActive = 0
default BreakfastToday = False
default TavernBreakfastLastDay = -1
default TavernBreakfastDay = -1
default TavernBreakfastBaseText = ""
default TavernBreakfastSoapAnnouncedDay = -1
default TavernBreakfastBarberTalkDay = -1
default TavernBreakfastListenDay = -1
default TavernBreakfastMarketTalkDay = -1
default TavernBreakfastMotivationDay = -1
default TavernBreakfastAbsentTalkDay = -1
default TavernBreakfastBaseShownDay = -1
default TavernBreakfastEventActive = False
default TavernSundayDinnerLastDay = -1
default TavernSundayDinnerBarberTalkDay = -1
default TavernBreakfastSpicyDrinkDay = -1
default TavernSundayDinnerSpicyDrinkDay = -1
default KitchenWildFoodStock = {}
default KitchenFoodEffects = {}
default TavernBreakfastGeorgetteLizaPending = 0
default TavernBreakfastTextPages = []
default TavernBreakfastTextPageIndex = 0
default TavernBreakfastTextReturnLabel = ""

init 4 python:
    def tavern_kitchen_has_worker(worker_name):
        return int(jobkitchen.get(worker_name, 0))

init python:
    import random
    import re
    import renpy.exports as renpy

    def tavern_kitchen_random_sandra_scene():
        candidates = []
        for picture_index in range(5):
            picture_path = "images/tavern/kitchen/kitchen_sandra_%s.jpg" % picture_index
            if renpy.loadable(picture_path):
                candidates.append(picture_path)
        if len(candidates) == 0:
            return ""
        return random.choice(candidates)

    def tavern_kitchen_picture():
        if _kitchen_worker_is_present("sandra"):
            sandra_scene = tavern_kitchen_random_sandra_scene()
            if sandra_scene:
                return sandra_scene
        if _kitchen_worker_is_present("melissa"):
            if random.randint(1, 4) == 1:
                if renpy.loadable("images/melissa/tavern/basement.png"):
                    return "images/melissa/tavern/basement.png"
                return "images/amanda/melissa_in storage.mp4"
            melissa_kitchen = [
                "images/melissa/tavern/melissa_kitchen_0.png",
                "images/melissa/tavern/melissa_kitchen_1.png",
            ]
            melissa_kitchen = [row for row in melissa_kitchen if renpy.loadable(row)]
            if len(melissa_kitchen) > 0:
                return melissa_kitchen[random.randint(0, len(melissa_kitchen) - 1)]
        return resolve_room_background_media(TavernKitchenRoom)

    def tavern_kitchen_pending_mandatory_event_code():
        mandatory_count = int(EventsCount.get(10, 0) or 0)
        if mandatory_count <= 0:
            return ""
        event_idx = mandatory_count - 1
        return str(NewEvents.get("10_" + str(event_idx), "") or "")

    def tavern_kitchen_wine_donation_picture():
        sandra_scene = tavern_kitchen_random_sandra_scene()
        if sandra_scene:
            return sandra_scene
        fallback_candidates = [
            "images/sandra/tavern/kitchen_sandra_0.jpg",
            "images/sandra/tavern/kitchen_sandra_1.jpg",
            "images/sandra/tavern/kitchen_sandra_2.jpg",
            "images/sandra/tavern/kitchen_sandra_3.jpg",
            "images/sandra/tavern/kitchen_sandra_4.jpg",
            "images/sandra/sandra_kitchen.png",
        ]
        for picture_path in fallback_candidates:
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def tavern_breakfast_available():
        return int(hour or 0) < 12 and not bool(BreakfastToday)

    def tavern_sunday_dinner_available():
        return (
            int(week or 0) == 7
            and int(hour or 0) >= 12
            and int(hour or 0) < 17
            and int(TavernSundayDinnerLastDay or -1) != int(dayspassed or 0)
        )

    def tavern_breakfast_present_ids():
        return list(household_breakfast_attendee_ids() or [])

    def tavern_breakfast_present_names():
        names = []
        for npc_id in tavern_breakfast_present_ids():
            names.append(_action_display_name(npc_id))
        return names

    def tavern_breakfast_present_entries():
        entries = []
        for npc_key in tavern_breakfast_present_ids():
            if str(npc_key or "") == "becky":
                entries.append({
                    "npc_id": "becky",
                    "name": "Бекки",
                    "talk_label": "IntBeckyTalk",
                    "auto_card": True,
                    "condition": kitchen_becky_visit_visible,
                })
            else:
                entries.append({
                    "npc_id": npc_key,
                    "name": _kitchen_display_name(npc_key),
                    "talk_label": _kitchen_talk_label(npc_key),
                    "auto_card": True,
                })
        return entries

    def tavern_breakfast_absent_ids():
        present_ids = set(tavern_breakfast_present_ids())
        return [npc_id for npc_id in ("sandra", "melissa", "amanda") if npc_id not in present_ids]

    def tavern_breakfast_absent_prompt():
        absent_ids = tavern_breakfast_absent_ids()
        if len(absent_ids) <= 0:
            return ""
        absent_names = [_action_display_name(npc_id) for npc_id in absent_ids]
        return "За столом быстро замечают, что не хватает: %s." % ", ".join(absent_names)

    def tavern_breakfast_absent_talk_text():
        absent_ids = tavern_breakfast_absent_ids()
        if len(absent_ids) <= 0:
            return "Сегодня за столом и так собрались все, кого вообще можно было вытащить к утренней каше."

        lines = []
        for npc_id in absent_ids:
            npc_name = _action_display_name(npc_id)
            issue_code = household_morning_issue_type(npc_id)
            if npc_id == "amanda":
                if issue_code == "sleepy":
                    lines.append("Аманда, конечно, опять не явилась. Мелисса сухо замечает, что та любит строить из себя бедную замученную девочку ровно до тех пор, пока кто-то другой делает за нее утреннюю работу.")
                elif issue_code == "sick":
                    lines.append("Разговор быстро сворачивает на Аманду: Сандра хмуро признает, что девчонку с утра совсем скрутило, так что не до каши ей сейчас.")
                else:
                    lines.append("За столом быстро проходятся по Аманде: то ли заспалась, то ли опять решила, что дом как-нибудь проживет и без нее.")
            elif npc_id == "melissa":
                if issue_code == "sleepy":
                    lines.append("Про Мелиссу сразу вспоминают, что она опять, видно, не выспалась. Сандра бурчит, что под такой крышей и мертвый будет вертеться до рассвета.")
                elif issue_code == "sick":
                    lines.append("О Мелиссе говорят уже спокойнее: видно, что девушка с утра совсем расклеилась, и даже Сандра не пытается тащить ее к столу силой.")
                else:
                    lines.append("Кто-то замечает, что Мелисса опять держится в стороне. За столом сходятся на том, что с ней сперва надо поговорить по-человечески, а уже потом ждать обычной утренней болтовни.")
            elif npc_id == "sandra":
                if issue_code == "sleepy":
                    lines.append("Отсутствие Сандры за столом чувствуется сильнее всего. Даже шутки звучат тише: без нее кухня сразу кажется каким-то временным лагерем, а не домом.")
                elif issue_code == "sick":
                    lines.append("О Сандре говорят с заметной тревогой. Если уж она не пришла к столу, значит дело и правда серьезное.")
                else:
                    lines.append("За столом быстро понимают, что без Сандры вся утренняя собранность держится на честном слове. Даже те, кто ворчит на нее каждый день, это признают.")
            else:
                lines.append("Разговор ненадолго переходит на %s, которой сегодня нет за столом." % npc_name)
        return "\n\n".join(lines)

    def tavern_breakfast_banter_text():
        present_ids = set(tavern_breakfast_present_ids())
        absent_ids = tavern_breakfast_absent_ids()
        if "amanda" in present_ids and "melissa" in absent_ids:
            return "Аманда фыркает: \"Вот же соня. Опять дрыхнет у себя, а я потом за двоих носись.\""
        if "melissa" in present_ids and "amanda" in absent_ids:
            return "Мелисса тихо замечает: \"Аманда опять решила, что работа сама себя сделает. Любит она проспать самый удобный час.\""
        if "sandra" in present_ids and len(absent_ids) > 0:
            return "Сандра с явным раздражением отодвигает кружку. \"Еще немного, и начну наказывать этих ленивых задниц. Дом держится не на капризах.\""
        if "becky" in present_ids:
            return "Бекки весело подбрасывает еще сплетен к столу, будто ради этого и пришла ни свет ни заря."
        return "За столом идут обычные для большого дома утренние шпильки, ворчание и короткие замечания о том, кто что опять успел или не успел."

    def tavern_breakfast_talk_result():
        present_ids = [npc_id for npc_id in list(tavern_breakfast_present_ids() or []) if npc_id in ("amanda", "melissa", "sandra", "becky")]
        if len(present_ids) <= 0:
            return {"text": tavern_breakfast_banter_text(), "arousal_gain": 0}

        candidates = []
        for npc_id in present_ids:
            profile = npc_relationship_level(npc_id)
            friend_level = int(profile.get("friend_level", 0) or 0)
            corruption_level = int(profile.get("corruption_level", 0) or 0)
            if friend_level >= 2 and corruption_level >= 2:
                tier = 2 if (friend_level >= 3 and corruption_level >= 3) else 1
                candidates.append((tier, friend_level + corruption_level, npc_id))

        if len(candidates) <= 0:
            return {"text": tavern_breakfast_banter_text(), "arousal_gain": 0}

        candidates.sort(reverse=True)
        talk_tier = int(candidates[0][0] or 0)
        talk_npc = str(candidates[0][2] or "")
        recent_barber_ids = set(tavern_recent_barber_ids() or [])
        lines = []
        arousal_gain = 0

        if talk_npc == "amanda":
            if talk_tier >= 2:
                lines.append("Аманда быстро переводит утреннюю болтовню на совсем уж двусмысленный лад и почти без стеснения начинает рассуждать о том, как мужчины замечают гладкую кожу под юбкой еще раньше, чем успевают увидеть что-то по-настоящему запретное.")
                lines.append("Даже те, кто сперва собирался отшутиться, уже слушают ее слишком внимательно: разговор выходит куда откровеннее обычного.")
                arousal_gain = 7
            else:
                lines.append("Аманда с лукавой улыбкой принимается рассуждать, как у девушки меняется походка, когда на ней хорошее белье, чистая кожа и чуть больше уверенности в себе.")
                arousal_gain = 3
        elif talk_npc == "melissa":
            if talk_tier >= 2:
                lines.append("Мелисса сперва говорит тихо, будто сама удивляется собственной смелости, но затем уже без особых околичностей признает, что после разговоров о чулках, гладкой коже и том, как это ощущается под ладонью, такие темы перестают быть просто шуткой.")
                lines.append("От ее почти спокойной откровенности утренний стол делается только опаснее.")
                arousal_gain = 6
            else:
                lines.append("Мелисса, заметно смущаясь, все же признает, что ухоженная женщина и сама двигается иначе: будто знает, что ее будут рассматривать внимательнее обычного.")
                arousal_gain = 2
        elif talk_npc == "sandra":
            if talk_tier >= 2:
                lines.append("Сандра без лишней деликатности замечает, что тонкие чулки, хорошее белье и гладкая кожа под платьем действуют на мужчин вполне предсказуемо, и притворяться тут особенно нечего.")
                lines.append("Сухой хозяйский тон делает эти слова только откровеннее.")
                arousal_gain = 5
            else:
                lines.append("Сандра сухо замечает, что ухоженный вид, хорошее белье и уверенная подача в трактире работают не хуже хорошего вина: люди и смотрят дольше, и платят охотнее.")
                arousal_gain = 2
        elif talk_npc == "becky":
            if talk_tier >= 2:
                lines.append("Бекки, как самая опытная в подобных темах, почти смеясь, пересказывает, как быстро разговоры о новых панталонах, бритье и \"гладкости под юбкой\" перестают быть разговорами и превращаются в вполне понятные приглашения.")
                lines.append("После такой прямоты вам уже трудно сохранять совсем невозмутимый вид.")
                arousal_gain = 7
            else:
                lines.append("Бекки с понимающей усмешкой подбрасывает пару двусмысленных замечаний о том, как меняется женская походка, когда та знает, что под юбкой у нее все именно так, как надо.")
                arousal_gain = 3

        if len(lines) <= 0:
            return {"text": tavern_breakfast_banter_text(), "arousal_gain": 0}

        if len(recent_barber_ids.intersection(set(present_ids))) > 0:
            if talk_tier >= 2:
                lines.append("Разговор почти сразу съезжает на советы Серджио: на белье, чулки, запах мыла и на то, что после таких мелочей женщины начинают куда смелее обсуждать даже совсем интимные подробности.")
                arousal_gain += 2
            else:
                lines.append("Кто-то невзначай вспоминает и советы Серджио, так что разговор сам собой уходит к уходу за собой, белью и всем тем мелочам, которые женщины обычно обсуждают только между своими.")
                arousal_gain += 1

        return {
            "text": "\n\n".join([row for row in lines if str(row or "").strip()]),
            "arousal_gain": max(0, min(10, int(arousal_gain or 0))),
            "tier": talk_tier,
            "speaker": talk_npc,
        }

    def tavern_breakfast_market_story_text():
        if int(week or 0) == 3:
            return "Вы пересказываете утренние рыночные слухи и напоминаете, что к пятничным танцам город уже начинает шевелиться заранее. За столом сразу прикидывают, кого это приведет вечером в трактир."
        if int(week or 0) == 7:
            return "Вы делитесь тем, что слышали утром в городе перед воскресной службой. Домочадцы слушают внимательнее обычного: в такой день слухи расходятся особенно быстро."
        return "Вы коротко рассказываете, что успели заметить и услышать в городе. Для домашнего стола это почти такой же важный утренний ритуал, как сама каша."

    def tavern_breakfast_motivation_text():
        if "sandra" in tavern_breakfast_present_ids():
            return "Вы напоминаете, что день надо вытянуть ровно и без лишней ругани. Сандра сперва хмыкает, но потом одобрительно кивает: тон задан правильно, и остальные тоже собираются заметно бодрее."
        return "Вы находите пару крепких слов перед началом дня. Даже если никто не спешит это признавать вслух, общий стол после такого расходится собраннее."

    def build_breakfast_text_pages(text="", min_paragraphs=2, max_paragraphs=3, page_limit=900):
        normalized = str(text or "").replace("\r\n", "\n").strip()
        if not normalized:
            return [""]

        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", normalized) if part.strip()]
        if len(paragraphs) <= 1:
            return [normalized]

        pages = []
        current_parts = []
        for paragraph in paragraphs:
            candidate_parts = list(current_parts) + [paragraph]
            candidate_text = "\n".join(candidate_parts)
            if current_parts and (len(candidate_parts) > int(max_paragraphs or 3) or (len(candidate_text) > int(page_limit or 900) and len(current_parts) >= int(min_paragraphs or 2))):
                pages.append("\n".join(current_parts))
                current_parts = [paragraph]
            else:
                current_parts = candidate_parts

        if len(current_parts) > 0:
            pages.append("\n\n".join(current_parts))

        return pages or [normalized]

    def tavern_breakfast_menu_items():
        items = []
        if tavern_breakfast_can_listen() and int(TavernBreakfastListenDay or -1) != int(dayspassed or 0):
            items.append(MenuItem("Послушать разговор за столом", Jump("TavernKitchenBreakfastHearDialogue")))
        if tavern_breakfast_has_market_topic() and int(TavernBreakfastMarketTalkDay or -1) != int(dayspassed or 0):
            items.append(MenuItem("Рассказать, что вы видели на рынке", Jump("TavernKitchenBreakfastMarketTalk")))
        if tavern_breakfast_can_make_speech() and int(TavernBreakfastMotivationDay or -1) != int(dayspassed or 0):
            items.append(MenuItem("Сказать пару слов перед работой", Jump("TavernKitchenBreakfastMotivation")))
        if tavern_breakfast_can_serve_spicy_tincture():
            items.append(MenuItem("Подать к столу пряную настойку", Jump("TavernKitchenBreakfastServeSpicyDrink")))
        if household_barber_request_ready("sandra", "breakfast"):
            items.append(MenuItem("Предложить Сандре сходить к Серджио", Call("HouseholdBarberRequestEvent", "sandra")))
        if household_barber_request_ready("melissa", "breakfast"):
            items.append(MenuItem("Предложить Мелиссе сходить к Серджио", Call("HouseholdBarberRequestEvent", "melissa")))
        if household_barber_request_ready("amanda", "breakfast"):
            items.append(MenuItem("Предложить Аманде сходить к Серджио", Call("HouseholdBarberRequestEvent", "amanda")))
        if int(TavernBreakfastGeorgetteLizaPending or 0) == 1:
            items.append(MenuItem("Объявить о Жоржетте и Лизетте", Jump("TavernKitchenBreakfastAnnounceGeorgetteLiza")))
        if str(tavern_breakfast_absent_prompt() or "").strip() and int(TavernBreakfastAbsentTalkDay or -1) != int(dayspassed or 0):
            items.append(MenuItem("Поговорить об отсутствующих", Jump("TavernKitchenBreakfastTalkAbsent")))
        if "sandra" in list(tavern_breakfast_present_ids() or []) and tavern_kitchen_sandra_can_discuss_breakfasts():
            items.append(MenuItem("Попросить Сандру почаще собирать всех на общий завтрак", Jump("TavernKitchenAskSandraBreakfasts")))
        if "sandra" in list(tavern_breakfast_present_ids() or []) and tavern_kitchen_sandra_can_discuss_clients():
            items.append(MenuItem("Попросить Сандру мягче настроить домочадцев к гостям", Jump("TavernKitchenAskSandraClients")))
        if tavern_breakfast_can_offer_dance_sponsorship():
            items.append(MenuItem("Обсудить пятничные танцы", Jump("TavernKitchenBreakfastDanceMenu")))
        items.append(MenuItem("Закончить завтрак", Jump("TavernKitchenFinishBreakfastEvent")))
        return items

    def tavern_breakfast_restore_ui_state(panel_text=""):
        text_value = str(panel_text or TavernBreakfastBaseText or TavernKitchenSavedText or MainTxt or "Вы все еще сидите за общим утренним столом.")
        renpy.store.MainTxt = text_value
        renpy.store.CurLocDesc = text_value
        renpy.store.current_action_title = "Завтрак"
        renpy.store.current_action_content = None
        renpy.store.current_action_items = list(tavern_breakfast_menu_items() or [])
        try:
            renpy.restart_interaction()
        except Exception:
            pass
        return text_value

    def tavern_breakfast_has_listen_topic():
        return (
            werecat_rat_breakfast_ready()
            or melissa_bat_breakfast_ready()
            or werecat_month_thanks_ready()
        )

    def tavern_breakfast_has_market_topic():
        return int(BlindPirateBreakfastPending or 0) == 1

    def tavern_breakfast_can_listen():
        return tavern_breakfast_has_listen_topic() or len(list(tavern_breakfast_present_ids() or [])) >= 2

    def tavern_breakfast_can_make_speech():
        return len(list(tavern_breakfast_present_ids() or [])) >= 2

    def tavern_breakfast_intro_line():
        present_ids = list(tavern_breakfast_present_ids() or [])
        if "sandra" in present_ids:
            return "Вы садитесь на кухне и завтракаете горячей кашей, свежим хлебом и чем-то согревающим."
        if len(present_ids) > 0:
            return "Сандра к столу не вышла, так что завтрак сегодня собирают на скорую руку из того, что уже было на кухне: хлеба, вчерашней каши и чего-нибудь горячего из котла."
        return "Сандра к столу не вышла, так что вы перебиваетесь на кухне тем, что удается наскоро собрать самому."

    def tavern_breakfast_barber_request_ids():
        rows = []
        for npc_id in list(tavern_breakfast_present_ids() or []):
            if household_barber_request_ready(npc_id, "breakfast"):
                rows.append(npc_id)
        return rows

    def tavern_breakfast_can_give_first_soap_samples():
        required_ids = set(("sandra", "melissa", "amanda"))
        present_ids = set(tavern_breakfast_present_ids() or [])
        return (
            int(HouseholdSoapSampleIntroDone or 0) == 0
            and soap_available_piece_count() >= 3
            and required_ids.issubset(present_ids)
        )

    def tavern_breakfast_apply_first_soap_samples():
        global HouseholdSoapSampleIntroDone, HouseholdSoapSampleGiven, TavernBreakfastSoapAnnouncedDay
        global fun, SoapRequestQueue

        if not tavern_breakfast_can_give_first_soap_samples():
            return ""
        _player_remove_item_by_id("soap_001", 3)
        if not isinstance(HouseholdSoapSampleGiven, dict):
            HouseholdSoapSampleGiven = {}
        if not isinstance(SoapRequestQueue, dict):
            SoapRequestQueue = {}
        for npc_id in ("sandra", "melissa", "amanda"):
            HouseholdSoapSampleGiven[npc_id] = 1
            SoapRequestQueue[npc_id] = 1
            Friends[npc_id] = min(20, int(Friends.get(npc_id, 0) or 0) + 1)
        HouseholdSoapSampleIntroDone = 1
        TavernBreakfastSoapAnnouncedDay = int(dayspassed or 0)
        fun = _player_clamp(int(fun or 0) + 3, 0, 100)
        return "За завтраком вы объявляете, что партия мыла наконец вылежалась, и тут же раздаете по куску Сандре, Мелиссе и Аманде на пробу. Дом сразу оживляется: всем любопытно, как поведет себя новое %s мыло, когда его наконец пустят в ход." % soap_last_batch_label()

    def tavern_breakfast_can_serve_spicy_tincture():
        return (
            int(_player_item_count_by_id("libido_tincture_001") or 0) > 0
            and len(list(tavern_breakfast_present_ids() or [])) >= 2
            and int(TavernBreakfastSpicyDrinkDay or -1) != int(dayspassed or 0)
        )

    def tavern_sunday_dinner_can_serve_spicy_tincture():
        return (
            int(_player_item_count_by_id("libido_tincture_001") or 0) > 0
            and len(list(tavern_sunday_dinner_present_ids() or [])) >= 2
            and int(TavernSundayDinnerSpicyDrinkDay or -1) != int(dayspassed or 0)
        )

    def tavern_kitchen_spicy_tincture_apply(present_ids=None):
        rows = list(present_ids or [])
        if len(rows) <= 0:
            return ""
        _player_remove_item_by_id("libido_tincture_001", 1)
        for npc_id in rows:
            Friends[npc_id] = min(20, int(Friends.get(npc_id, 0) or 0) + 1)
            if npc_id in ("sandra", "melissa", "amanda", "becky"):
                otkroven[npc_id] = min(20, int(otkroven.get(npc_id, 0) or 0) + 1)
            if npc_id in ("sandra", "melissa", "amanda"):
                sluttiness[npc_id] = min(100, int(sluttiness.get(npc_id, 0) or 0) + 1)
        globals()["fun"] = _player_clamp(int(fun or 0) + 2, 0, 100)
        lines = [
            "Вы подаете к столу пряную настойку с медовой сладостью. По комнате сразу идет теплый, терпкий запах, и общий разговор делается заметно живее.",
        ]
        if "becky" in rows:
            lines.append("Бекки первой усмехается и замечает, что после такой добавки даже самые приличные разговоры обычно быстро становятся куда смелее.")
        if "sandra" in rows:
            lines.append("Сандра сперва ворчит для порядка, но потом признает, что такая кружка к столу иной раз полезнее кислых рож.")
        return "\n\n".join(lines)

    def tavern_kitchen_event_picture(base_name=""):
        stem = str(base_name or "").strip()
        if stem == "":
            return ""
        candidates = (
            "images/kitchen/%s.jpg" % stem,
            "images/tavern/kitchen/%s.jpg" % stem,
            "images/kitchen/%s.png" % stem,
            "images/tavern/kitchen/%s.png" % stem,
        )
        for candidate in candidates:
            try:
                if renpy.loadable(candidate):
                    return candidate
            except Exception:
                pass
        return candidates[0]

    def tavern_kitchen_breakfast_picture():
        return tavern_kitchen_event_picture("kitchen_breakfast")

    def tavern_kitchen_sunday_dinner_picture():
        return tavern_kitchen_event_picture("kitchen_sundaydinnerAll_0")

    def tavern_sunday_dinner_present_ids():
        return list(household_breakfast_attendee_ids() or [])

    def tavern_sunday_dinner_present_names():
        names = []
        for npc_id in tavern_sunday_dinner_present_ids():
            names.append(_action_display_name(npc_id))
        return names

    def tavern_recent_barber_ids():
        if not isinstance(BarberVisitLastDay, dict):
            return []
        rows = []
        for npc_id in ("sandra", "melissa", "amanda"):
            if int(BarberVisitLastDay.get(npc_id, -99) or -99) < 0:
                continue
            if int(dayspassed or 0) - int(BarberVisitLastDay.get(npc_id, -99) or -99) <= 14:
                rows.append(npc_id)
        return rows

    def tavern_barber_breakfast_lines():
        recent_ids = [npc_id for npc_id in tavern_recent_barber_ids() if npc_id in list(tavern_breakfast_present_ids() or [])]
        if len(recent_ids) <= 0 or int(TavernBreakfastBarberTalkDay or -1) == int(dayspassed or 0):
            return []
        names = [_action_display_name(npc_id) for npc_id in recent_ids]
        lines = [
            "За столом быстро всплывает вчерашний разговор Серджио о женских хитростях: о хорошем мыле, о том, как важны чистота, чулки и нижнее белье, и о том, что даже простая стрижка меняет, как женщина держится в доме.",
        ]
        if "amanda" in recent_ids:
            lines.append("Аманда оживленно спрашивает, какие панталоны считаются самыми соблазнительными и правда ли, что после хорошей стрижки и бритья мужчинам будто сносит голову быстрее.")
        if "melissa" in recent_ids:
            lines.append("Мелисса сначала смущается, но потом все же признает, что после визита к Серджио начала иначе смотреть и на белье, и на уход за собой: \"Когда сама себе кажешься аккуратнее, и двигаешься почему-то увереннее.\"")
        if "sandra" in recent_ids:
            lines.append("Сандра сухо подводит итог, что ухоженный вид в трактире тоже работает на дом: \"Если девки выглядят лучше, и людям приятнее смотреть, и дурные разговоры как-то сами делаются мягче.\"")
        if len(names) > 0:
            lines.append("Похоже, после цирюльни тема ухода за собой еще пару недель будет возвращаться и к завтракам, и к вечерним разговорам.")
        return lines

    def tavern_barber_sunday_dinner_lines():
        recent_ids = [npc_id for npc_id in tavern_recent_barber_ids() if npc_id in list(tavern_sunday_dinner_present_ids() or [])]
        if len(recent_ids) <= 0 or int(TavernSundayDinnerBarberTalkDay or -1) == int(dayspassed or 0):
            return []
        lines = [
            "За воскресным столом разговор неожиданно съезжает на то, чему Серджио успел научить про уход за собой: от хорошего мыла и ароматных вод до того, как женщины выбирают белье, чулки и бритье без лишних глаз.",
        ]
        if "becky" in list(tavern_sunday_dinner_present_ids() or []):
            lines.append("Бекки только посмеивается и подтверждает, что такие темы в женских разговорах всплывают куда чаще, чем мужчины думают.")
        return lines

    def tavern_breakfast_dialogue_lines():
        lines = []
        present_ids = tavern_breakfast_present_ids()

        if "sandra" in present_ids:
            lines.append("Сандра привычно командует утренней возней и следит, чтобы никто не сидел без дела.")
            lines.append("Сандра ворчит, что хороший дом держится на привычке вставать вовремя, а не на пустых обещаниях сделать все потом.")
        if "melissa" in present_ids:
            lines.append("Мелисса за завтраком становится разговорчивее обычного и успевает вставить пару тихих замечаний почти в любой разговор.")
            lines.append("Мелисса негромко замечает, что утро в трактире ей нравится куда больше шумного вечера: в такие часы дом еще живет скорее общим хозяйством, чем трактирной суетой.")
            if int(MelissaVar.get("bats_episode", 0) or 0) < 8:
                if int(MelissaVar.get("bats_episode", 0) or 0) >= 4:
                    lines.append("Мелисса устало признается, что после ночи под шуршащей крышей опять почти не выспалась. Теперь, когда источник на чердаке уже найден, она только спрашивает, когда вы наконец выкурите эту дрянь и заделаете щели.")
                elif int(MelissaVar.get("bats_episode", 0) or 0) >= 3:
                    lines.append("Мелисса жалуется, что ночью над ее комнатой опять кто-то возился под крышей, а из найденных щелей тянет сыростью. По ее виду ясно: выспаться ей толком снова не удалось.")
                else:
                    lines.append("Мелисса мрачно признается, что снова не выспалась: под потолком шуршало, а по балкам будто кто-то бегал почти до рассвета.")
                if "sandra" in present_ids:
                    lines.append("Сандра сразу обещает поговорить с Герхардом о крыше и велит вам не тянуть с чердаком: сначала найти источник шума, потом уже решать, чем выкуривать эту дрянь и чем заделывать щели.")
            if int(MelissaVar.get("bats_episode", 0) or 0) >= 6 and "amanda" in present_ids:
                lines.append("Стоит за столом всплыть слову \"чердак\", как Аманда многозначительно тянет: \"Главное, Стефан, теперь не падать сверху в чужие комнаты без стука.\" Мелисса тут же фыркает, но уголки ее губ все равно дрожат.")
        if "amanda" in present_ids:
            lines.append("Аманда клюет завтрак быстрее всех и все время норовит отвлечься на болтовню.")
            lines.append("Аманда с набитым ртом уверяет, что если кормить ее так каждое утро, то она готова даже меньше жаловаться на работу.")
        if "becky" in present_ids:
            lines.append("Бекки охотно подхватывает кухонные сплетни и сразу оживляет стол.")
            lines.append("Бекки усмехается, что именно за такими утренними столами и решается, кто в доме на самом деле всем заправляет.")
        if int(week or 0) == 3 and "sandra" in present_ids:
            lines.append("За завтраком Сандра напоминает, что к середине недели надо бы пополнить запасы вина и хорошей еды, иначе в трактире скоро станет совсем уныло.")
        if tavern_breakfast_can_offer_dance_sponsorship() and "sandra" in present_ids:
            lines.append("Сандра заодно осторожно спрашивает, не хотите ли вы и в этом году скинуться на пятничные танцы от лица трактира.")
        if soap_available_piece_count() > 0 and int(TavernBreakfastSoapAnnouncedDay or -1) != int(dayspassed or 0):
            if int(HouseholdSoapSampleIntroDone or 0) == 0:
                lines.append("За столом вы объявляете, что новая партия %s мыла наконец вылежалась и уже готова. Домашние заметно оживляются от этой новости." % soap_last_batch_label())
            else:
                lines.append("За столом вы напоминаете, что у вас снова есть %s мыло. После прошлой пробы за такой новостью следят уже куда внимательнее." % soap_last_batch_label())
            if "sandra" in present_ids:
                lines.append("Сандра сразу замечает, что в доме наконец будет пахнуть по-человечески, а не только кухней, дымом и работой.")
            if "melissa" in present_ids:
                lines.append("Мелисса тихо радуется, что теперь можно будет без стыда пускать приличных гостей в комнаты наверху.")
            if "amanda" in present_ids:
                lines.append("Аманда смеется, что теперь у нее есть шанс пахнуть не только тестом, дымом и беготней по залу.")
        lines.extend(list(tavern_barber_breakfast_lines() or []))
        lines.extend(list(household_breakfast_absence_lines() or []))
        return lines

    def tavern_breakfast_apply_social_bonus():
        present_ids = tavern_breakfast_present_ids()
        for npc_id in present_ids:
            Friends[npc_id] = min(20, int(Friends.get(npc_id, 0) or 0) + 1)
        return present_ids

    def tavern_sunday_dinner_dialogue_lines():
        lines = []
        present_ids = tavern_sunday_dinner_present_ids()

        if "sandra" in present_ids:
            lines.append("Сандра сегодня не гонит никого в работу и даже позволяет столу идти своим чередом дольше обычного.")
        if "melissa" in present_ids:
            lines.append("Мелисса на воскресном обеде заметно спокойнее и охотнее поддерживает общий разговор, чем в будние дни.")
        if "amanda" in present_ids:
            lines.append("Аманда оживляется сильнее всех: без обычной трактирной беготни она болтает за двоих и успевает сунуть нос в каждый разговор.")
        if "becky" in present_ids:
            lines.append("Бекки охотно поддерживает застольную болтовню и быстро превращает обед в сборник городских новостей.")
        if "sandra" in present_ids:
            try:
                _tavern_rep = int(tavern_reputation_score() or 0)
            except Exception:
                _tavern_rep = 50
            if _tavern_rep >= 70:
                lines.append("Сандра за ужином подводит итог недели заметно мягче обычного: трактир держится крепко, гости идут охотнее, а значит можно думать не только о выживании, но и о мелких приятностях для дома.")
            elif _tavern_rep <= 40:
                lines.append("Сандра напоминает за столом без особой деликатности, что неделя вышла слабой. Пока трактир не начнет приносить больше пользы, о лишних тратах и домашних поблажках лучше не мечтать.")
            else:
                lines.append("Сандра спокойно замечает, что неделя закрылась без позора, но и без особого размаха. Дом держится ровно, а значит хорошие привычки и аккуратная работа по-прежнему важнее красивых обещаний.")
        lines.extend(list(tavern_barber_sunday_dinner_lines() or []))
        return lines

    def tavern_sunday_dinner_apply_social_bonus():
        present_ids = tavern_sunday_dinner_present_ids()
        for npc_id in present_ids:
            Friends[npc_id] = min(20, int(Friends.get(npc_id, 0) or 0) + 1)
        return present_ids

    def tavern_kitchen_can_share_tea_with_sandra_and_becky():
        return int(BeckyKitchenVisitActive or 0) == 1 and _kitchen_worker_is_present("sandra") and int(_player_item_count_by_id("energy_tea_001") or 0) > 0

    def tavern_kitchen_depositable_food_ids():
        return ("berries_001", "mushroom_001", "honey_comb_001", "boar_meat_001", "milk_pitcher_001")

    def tavern_kitchen_food_stock_count(item_id=""):
        item_key = str(item_id or "").strip()
        stock = KitchenWildFoodStock if isinstance(KitchenWildFoodStock, dict) else {}
        if item_key == "":
            return sum(max(0, int(row or 0)) for row in list(stock.values()))
        return max(0, int(stock.get(item_key, 0) or 0))

    def tavern_kitchen_food_stock_summary():
        parts = []
        for item_id in tavern_kitchen_depositable_food_ids():
            item_count = tavern_kitchen_food_stock_count(item_id)
            if item_count <= 0:
                continue
            item_obj = get_game_item(item_id)
            item_name = str(getattr(item_obj, "name", item_id) or item_id)
            parts.append("%s x%s" % (item_name, item_count))
        return ", ".join(parts)

    def tavern_kitchen_has_depositable_food():
        for item_id in tavern_kitchen_depositable_food_ids():
            if int(_player_item_count_by_id(item_id) or 0) > 0:
                return True
        return False

    def tavern_kitchen_deposit_entries():
        entries = []
        for item_id in tavern_kitchen_depositable_food_ids():
            item_count = int(_player_item_count_by_id(item_id) or 0)
            if item_count <= 0:
                continue
            item_obj = get_game_item(item_id)
            item_name = str(getattr(item_obj, "name", item_id) or item_id)
            entries.append({
                "item_id": item_id,
                "count": item_count,
                "caption": "Отдать на кухню %s x%s" % (item_name, item_count),
            })
        return entries

    def tavern_kitchen_deposit_food(item_id=""):
        global KitchenWildFoodStock

        item_key = str(item_id or "").strip()
        if item_key == "":
            return 0
        item_count = int(_player_item_count_by_id(item_key) or 0)
        if item_count <= 0:
            return 0
        removed = _player_remove_item_by_id(item_key, item_count)
        if not removed:
            return 0
        if not isinstance(KitchenWildFoodStock, dict):
            KitchenWildFoodStock = {}
        KitchenWildFoodStock[item_key] = max(0, int(KitchenWildFoodStock.get(item_key, 0) or 0)) + item_count
        tavern_kitchen_apply_deposit_effect(item_key, item_count)
        return item_count

    def tavern_kitchen_take_food_from_stock(preferred_ids=None):
        preferred = list(preferred_ids or [])
        if len(preferred) <= 0:
            preferred = list(tavern_kitchen_depositable_food_ids())
        if not isinstance(KitchenWildFoodStock, dict):
            return ""
        for item_id in preferred:
            item_key = str(item_id or "").strip()
            if tavern_kitchen_food_stock_count(item_key) <= 0:
                continue
            KitchenWildFoodStock[item_key] = max(0, int(KitchenWildFoodStock.get(item_key, 0) or 0) - 1)
            if int(KitchenWildFoodStock.get(item_key, 0) or 0) <= 0:
                KitchenWildFoodStock.pop(item_key, None)
            return item_key
        return ""

    def tavern_kitchen_food_item_name(item_id=""):
        item_obj = get_game_item(str(item_id or "").strip())
        if item_obj is None:
            return str(item_id or "").strip()
        return str(getattr(item_obj, "name", item_id) or item_id)

    def tavern_kitchen_food_effect_days(effect_key=""):
        global KitchenFoodEffects

        if not isinstance(KitchenFoodEffects, dict):
            KitchenFoodEffects = {}
        return max(0, int(KitchenFoodEffects.get(str(effect_key or ""), 0) or 0))

    def tavern_kitchen_add_food_effect(effect_key="", days_value=1):
        global KitchenFoodEffects

        key = str(effect_key or "").strip()
        if key == "":
            return 0
        if not isinstance(KitchenFoodEffects, dict):
            KitchenFoodEffects = {}
        KitchenFoodEffects[key] = max(0, int(KitchenFoodEffects.get(key, 0) or 0)) + max(1, int(days_value or 1))
        return int(KitchenFoodEffects.get(key, 0) or 0)

    def tavern_kitchen_deposit_effect_text(item_id=""):
        item_key = str(item_id or "").strip()
        if item_key == "honey_comb_001":
            return "Мед сразу откладывают для сладких добавок к завтракам и напиткам. Такие угощения заметно теплят настроение в доме и делают разговоры смелее."
        if item_key == "boar_meat_001":
            return "Кабанье мясо идет в общий котел: сытная еда экономит основные припасы, но гостям под нее обычно требуется чуть больше вина."
        if item_key == "milk_pitcher_001":
            return "Свежее молоко сразу убирают в прохладу: с медом оно отлично пойдет и в кашу, и в сладкие утренние блюда."
        if item_key in ("berries_001", "mushroom_001"):
            return "Эти припасы не будут лежать мертвым грузом: их понемногу пустят в еду день за днем."
        return ""

    def tavern_kitchen_apply_deposit_effect(item_id="", item_count=0):
        item_key = str(item_id or "").strip()
        units = max(0, int(item_count or 0))
        if units <= 0:
            return ""
        if item_key == "honey_comb_001":
            tavern_kitchen_add_food_effect("honey_days", min(3, max(1, units)))
            for npc_id in ("sandra", "melissa", "amanda"):
                sluttiness[npc_id] = min(100, int(sluttiness.get(npc_id, 0) or 0) + 2)
            return "honey"
        if item_key == "boar_meat_001":
            tavern_kitchen_add_food_effect("boar_days", min(3, max(1, units)))
            for npc_id in ("sandra", "melissa", "amanda"):
                sluttiness[npc_id] = min(100, int(sluttiness.get(npc_id, 0) or 0) + 1)
            return "boar"
        if item_key == "milk_pitcher_001":
            tavern_kitchen_add_food_effect("milk_days", min(3, max(1, units)))
            return "milk"
        return ""

    def tavern_kitchen_consume_stock_units(units=0, preferred_ids=None):
        global KitchenWildFoodStock

        target = max(0, int(units or 0))
        if target <= 0 or not isinstance(KitchenWildFoodStock, dict):
            return 0
        preferred = list(preferred_ids or ("boar_meat_001", "honey_comb_001", "berries_001", "mushroom_001", "milk_pitcher_001"))
        consumed = 0
        for item_id in preferred:
            item_key = str(item_id or "").strip()
            while consumed < target and tavern_kitchen_food_stock_count(item_key) > 0:
                KitchenWildFoodStock[item_key] = max(0, int(KitchenWildFoodStock.get(item_key, 0) or 0) - 1)
                consumed += 1
                if int(KitchenWildFoodStock.get(item_key, 0) or 0) <= 0:
                    KitchenWildFoodStock.pop(item_key, None)
            if consumed >= target:
                break
        return consumed

    def tavern_kitchen_boar_bonus_active():
        return tavern_kitchen_food_effect_days("boar_days") > 0

    def tavern_kitchen_honey_bonus_active():
        return tavern_kitchen_food_effect_days("honey_days") > 0

    def tavern_kitchen_milk_bonus_active():
        return tavern_kitchen_food_effect_days("milk_days") > 0

    def tavern_kitchen_fertility_bonus_active():
        return tavern_kitchen_honey_bonus_active() and tavern_kitchen_milk_bonus_active()

    def tavern_kitchen_daily_product_savings(base_products=0):
        base = max(0, int(base_products or 0))
        if base <= 0 or tavern_kitchen_food_stock_count() <= 0:
            return 0
        savings_percent = 20
        if tavern_kitchen_boar_bonus_active():
            savings_percent += 10
        target_units = max(1, (base * savings_percent + 99) // 100)
        return tavern_kitchen_consume_stock_units(min(target_units, tavern_kitchen_food_stock_count()))

    def tavern_kitchen_apply_daily_food_effects():
        global KitchenFoodEffects

        if not isinstance(KitchenFoodEffects, dict):
            KitchenFoodEffects = {}
        lines = []
        if tavern_kitchen_honey_bonus_active():
            for npc_id in ("sandra", "melissa", "amanda"):
                sluttiness[npc_id] = min(100, int(sluttiness.get(npc_id, 0) or 0) + 1)
            try:
                add_sex_event = TodaySexEvents_Add
            except Exception:
                add_sex_event = None
            if callable(add_sex_event) and random.randint(1, 3) == 1:
                add_sex_event(random.choice(["sandra", "melissa", "amanda"]), 99, 99, "KitchenHoneyMood")
            lines.append("Медовые угощения за день заметно смягчили настроение в доме.")
        if tavern_kitchen_fertility_bonus_active():
            lines.append("Молоко с медом делает общую еду мягче, сытнее и будто бы здоровее: в доме даже начинают шутить, что от такой кухни женщин тянет к детям быстрее обычного.")
        if tavern_kitchen_boar_bonus_active():
            lines.append("Кабанье мясо сделало кухню сытнее: припасов ушло меньше, зато вина гости просили охотнее.")
        for effect_key in list(KitchenFoodEffects.keys()):
            KitchenFoodEffects[effect_key] = max(0, int(KitchenFoodEffects.get(effect_key, 0) or 0) - 1)
            if int(KitchenFoodEffects.get(effect_key, 0) or 0) <= 0:
                KitchenFoodEffects.pop(effect_key, None)
        return lines

    def tavern_kitchen_sandra_can_discuss_breakfasts():
        return _kitchen_worker_is_present("sandra") and tavern_kitchen_food_stock_count() > 0 and int(Friends.get("sandra", 0) or 0) >= 5 and int(AskedToday.get("sandra", 0) or 0) == 0

    def tavern_kitchen_sandra_can_discuss_clients():
        return _kitchen_worker_is_present("sandra") and tavern_kitchen_food_stock_count() > 0 and int(Friends.get("sandra", 0) or 0) >= 5 and int(AskedToday.get("sandra", 0) or 0) == 0

    TavernKitchenRoom = Room(
        code_name="TavernKitchen",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Кухня",
        bg_picture="bg TavernKitchen",
        descriptions=[
            RoomDescription(
                text="Вы заходите в кухню трактира. Здесь пахнет едой и дымом от очага.",
                first_time=True,
                priority=200,
            ),
            RoomDescription(
                text="Кухня оборудована очагом (hearth), котлом для кипячения воды (cauldron) и другими предметами.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в зал", target="TavernMain"),
            RoomExit(label="Идти в склад", target="TavernStorage"),
            RoomExit(label="Выйти на задний двор", target="Backyard"),
        ],
        game_items=[
            "hearth_001",
            "cauldron_001",
        ],
        npcs=[],  # Filled dynamically from jobkitchen
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={"object_menu_label": "TavernKitchenObjectMenu"},
    )

    def _kitchen_has_job(npc_id):
        mapping = jobkitchen if isinstance(jobkitchen, dict) else {}
        return int(mapping.get(npc_id, 0) or 0) != 0

    def _kitchen_worker_is_present(npc_id):
        return _kitchen_has_job(npc_id) and _tavern_is_in_room(npc_id, "TavernKitchen")

    def _kitchen_display_name(npc_id):
        try:
            return _tavern_name(npc_id)
        except Exception:
            return str(npc_id).capitalize()

    def _kitchen_talk_label(npc_id):
        label = "Int" + str(npc_id).capitalize() + "Talk"
        if renpy.has_label(label):
            return label
        return ""

    def kitchen_becky_visit_visible():
        return int(BeckyKitchenVisitActive or 0) == 1

    def build_kitchen_npc_entries():
        if bool(TavernBreakfastEventActive):
            return tavern_breakfast_present_entries()
        entries = []
        for npc_key in ("sandra", "melissa", "amanda"):
            if not npc_key:
                continue
            if _tavern_is_in_room(npc_key, "TavernKitchen"):
                entries.append({
                    "npc_id": npc_key,
                    "name": _kitchen_display_name(npc_key),
                    "talk_label": _kitchen_talk_label(npc_key),
                    "auto_card": True,
                })
        _werecat_entry = werecat_npc_entry("TavernKitchen")
        if isinstance(_werecat_entry, dict):
            entries.append(dict(_werecat_entry))
        if int(BeckyKitchenVisitActive or 0) == 1:
            entries.append({
                "npc_id": "becky",
                "name": "Бекки",
                "talk_label": "IntBeckyTalk",
                "auto_card": True,
                "condition": kitchen_becky_visit_visible,
            })
        return entries

    def build_kitchen_description(include_notice=True, intro_text=""):
        room_obj = CurrentRoom if CurrentRoom is not None else TavernKitchenRoom
        room_item_ids = [get_object_id(row) for row in list(getattr(room_obj, "game_items", []) or [])]
        text_parts = []

        intro_value = str(intro_text or "").strip()
        if intro_value:
            text_parts.append(intro_value)

        if include_notice and bool(TavernKitchenNoticePending) and str(TavernKitchenNoticeText or "").strip():
            text_parts.append(str(TavernKitchenNoticeText or "").strip())

        # Dynamic crew from original NamesList
        kitchen_crew = NamesList("jobkitchen", "TavernKitchen")
        crew_names = str(kitchen_crew or "никто")
        if int(hour or 0) < 12:
            text_parts.append("До полудня кухня живет скорее ритмом большого двора, чем трактирной службой. Здесь собирают завтрак, ставят воду, проверяют припасы и только готовятся к дневной работе.")
            text_parts.append("На кухне с утра возятся: " + str(tavern_household_present_names("TavernKitchen") or "никто") + ".")
            if int(week or 0) == 7:
                text_parts.append("После службы здесь наверняка соберутся и на более основательную воскресную трапезу, но пока речь идет только о спокойном утреннем сборе.")
        else:
            text_parts.append("На кухне работают: " + crew_names + ".")
        if int(BeckyKitchenVisitActive or 0) == 1:
            text_parts.append("Сегодня сюда заглянула Бекки Блэнкеншип. Она что-то негромко обсуждает с Сандрой у разделочного стола.")
        if int(week or 0) == 7 and int(time or 0) == 1:
            text_parts.append("Судя по запахам и приготовленным блюдам, Сандра решила устроить для всей трактирной челяди воскресный обед поосновательнее обычного.")
        if tavern_kitchen_food_stock_count() > 0:
            text_parts.append("На кухне уже отложены принесенные вами припасы: %s." % tavern_kitchen_food_stock_summary())

        hearth_count = len([row for row in room_item_ids if row == "hearth_001"])
        if hearth_count > 0:
            text_parts.append("Очаг готов к использованию.")

        cauldron_count = len([row for row in room_item_ids if row == "cauldron_001"])
        if cauldron_count > 0:
            text_parts.append("Котел для кипячения воды на месте.")

        return "\n".join([row for row in text_parts if str(row or "").strip()])

    ##    room_obj = CurrentRoom if CurrentRoom is not None else TavernKitchenRoom
    #   items = []
    #    seen_object_ids = set()

        # Dynamic NPCs from kitchen list
    #    kitchen_crew = NamesList("jobkitchen") or []
    #    for worker in kitchen_crew:
    #        items.append(MenuItem(worker, Call("Int" + worker.capitalize() + "Talk")))  # Talk to crew

    #   for row in list(getattr(room_obj, "game_items", []) or []):
    #        object_id = get_object_id(row)
    #        if not object_id or object_id in seen_object_ids:
    #            continue
    #        seen_object_ids.add(object_id)
    #        game_item = get_game_item(object_id, room_obj)
    #        if game_item is None:
    #            continue
    #        for item_action in game_item.visible_actions():
    #            action_args = tuple(getattr(item_action, "args", ()) or ())
    #            if item_action.hook == "call" and str(item_action.target or "") != "":
    #                items.append(MenuItem(item_action.label, Call(item_action.target, *action_args)))
    #            elif item_action.hook == "jump" and str(item_action.target or "") != "":
    #                items.append(MenuItem(item_action.label, Jump(item_action.target)))
    ##                items.append(MenuItem(item_action.label, Call("Examine", object_id, "TavernKitchen", item_action.target, object_id)))

    #    items.append(MenuItem("Вернуться в зал", Jump("TavernMain")))
    #    items.append(MenuItem("Идти в склад", Jump("TavernStorage")))
    #    items.append(MenuItem("Выйти на задний двор", Jump("Backyard")))
    #    return items


label TavernKitchen:
    call EnterLocation("TavernKitchen")
    $ CurrentRoom = TavernKitchenRoom
    $ CurLoc = "TavernKitchen"
    $ location = CurLoc
    $ tavern_kitchen_hearth_wood_stock()
    $ scene_image = tavern_kitchen_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    call CheckDailyEvent("", "_story_enter", CurLoc, time)
    $ current_object_id = ""
    $ current_girl_key = ""
    if TavernBreakfastEventActive:
        if str(TavernKitchenSavedText or "").strip():
            $ MainTxt = str(TavernKitchenSavedText or "")
        else:
            $ MainTxt = "Вы все еще сидите за общим утренним столом."
        $ CurLocDesc = MainTxt
        $ TavernKitchenRoom.npcs = tavern_breakfast_present_entries()
        $ CurrentRoom.npcs = TavernKitchenRoom.npcs
        hide screen main_ui
        jump TavernKitchenBreakfastMenu
    $ BeckyKitchenVisitActive = 1 if becky_kitchen_visit_active() else 0
    if BeckyKitchenVisitActive:
        $ BeckyVar["SandraKitchenVisitMonth"] = int(month or 0)

    $ TavernKitchenRoom.npcs = build_kitchen_npc_entries()
    $ CurrentRoom.npcs = TavernKitchenRoom.npcs

    $ _kitchen_wine_event_text = ""
    $ _kitchen_pending_event = tavern_kitchen_pending_mandatory_event_code()
    if str(_kitchen_pending_event or "") == "WineForDance" and _tavern_is_in_room("sandra", "TavernKitchen") and not tavern_breakfast_available():
        $ _kitchen_event_picture = tavern_kitchen_wine_donation_picture()
        if str(_kitchen_event_picture or "").strip():
            $ scene_image = _kitchen_event_picture
            $ _layout_last_picture = _kitchen_event_picture
        call DisplayTavernEventShort(time, 1)
        $ _kitchen_wine_event_text = str(_return or "")

    if str(_kitchen_wine_event_text or "").strip():
        $ MainTxt = _kitchen_wine_event_text
        $ CurLocDesc = MainTxt
        $ TavernKitchenSavedText = MainTxt
        $ current_action_content = None
        call TavernKitchenBuildActions
    else:
        $ MainTxt = build_kitchen_description()
        $ CurLocDesc = MainTxt
        $ TavernKitchenSavedText = MainTxt
        call TavernKitchenBuildActions
        if sandra_revealing_dress_initiative_ready():
            call SandraDressInitiativeEvent
        else:
            python:
                _kitchen_request_type, _kitchen_request_girl = household_pending_request_girl("TavernKitchen")
            if str(_kitchen_request_type or "") == "soap":
                call HouseholdSoapRequestEvent(_kitchen_request_girl)
    $ TavernKitchenNoticePending = False
    jump TavernKitchenView


label TavernKitchenView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernKitchenView


label TavernKitchenBuildActions:
    if TavernBreakfastEventActive:
        return
    $ tavern_kitchen_hearth_wood_stock()
    $ TavernKitchenRoom.npcs = build_kitchen_npc_entries()
    $ CurrentRoom.npcs = TavernKitchenRoom.npcs
    $ current_action_title = "Кухня"
    $ current_action_content = None
    $ room_menu = CurrentRoom.build_menu_sections()
    $ current_action_items = room_menu["movement"] + room_menu["actions"]
    if tavern_breakfast_available():
        $ current_action_items.append(MenuItem("Позавтракать", Call("TavernKitchenBreakfast")))
    elif tavern_sunday_dinner_available():
        if tavern_sunday_dinner_can_serve_spicy_tincture():
            $ current_action_items.append(MenuItem("Сесть за воскресный обед", Call("TavernKitchenSundayDinnerMenu")))
        else:
            $ current_action_items.append(MenuItem("Сесть за воскресный обед", Call("TavernKitchenSundayDinner")))
    else:
        $ current_action_items.append(MenuItem("Перекусить", Call("Eat", "горячую еду с кухни", 18, "Вы перекусываете на кухне горячей едой и немного приходите в себя.", "TavernKitchen", "")))
    if tavern_kitchen_has_depositable_food():
        $ current_action_items.append(MenuItem("Отдать на кухню лесную добычу и припасы", Call("TavernKitchenDepositMenu")))
    if tavern_kitchen_can_share_tea_with_sandra_and_becky():
        $ current_action_items.append(MenuItem("Угостить Сандру и Бекки чаем", Call("TavernKitchenShareTeaWithSandraAndBecky")))
    if tavern_kitchen_sandra_can_discuss_breakfasts():
        $ current_action_items.append(MenuItem("Попросить Сандру почаще собирать всех на общий завтрак", Call("TavernKitchenAskSandraBreakfasts")))
    if tavern_kitchen_sandra_can_discuss_clients():
        $ current_action_items.append(MenuItem("Попросить Сандру мягче настроить домочадцев к гостям", Call("TavernKitchenAskSandraClients")))
    python:
        try:
            renpy.restart_interaction()
        except Exception:
            pass
    return


label TavernKitchenBreakfast:
    if not tavern_breakfast_available():
        $ MainTxt = "Сегодня вы уже завтракали."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ BreakfastToday = True
    $ TavernBreakfastLastDay = int(dayspassed or 0)
    $ TavernBreakfastDay = int(dayspassed or 0)
    $ calendar_advance_minutes(30)
    vscene tavern_kitchen_breakfast_picture()
    python:
        _breakfast_lines = [
            tavern_breakfast_intro_line(),
            "За столом собираются: " + (", ".join(tavern_breakfast_present_names()) if len(tavern_breakfast_present_names()) > 0 else "пока что только вы сами") + ".",
        ]
        _breakfast_lines.extend(tavern_breakfast_dialogue_lines())
        if (
            tavern_breakfast_can_listen()
            or tavern_breakfast_has_market_topic()
            or tavern_breakfast_can_make_speech()
            or tavern_breakfast_can_serve_spicy_tincture()
            or household_barber_request_ready("sandra", "breakfast")
            or household_barber_request_ready("melissa", "breakfast")
            or household_barber_request_ready("amanda", "breakfast")
            or int(TavernBreakfastGeorgetteLizaPending or 0) == 1
            or str(tavern_breakfast_absent_prompt() or "").strip() != ""
            or ("sandra" in list(tavern_breakfast_present_ids() or []) and tavern_kitchen_sandra_can_discuss_breakfasts())
            or ("sandra" in list(tavern_breakfast_present_ids() or []) and tavern_kitchen_sandra_can_discuss_clients())
            or tavern_breakfast_can_offer_dance_sponsorship()
        ):
            _breakfast_lines.append("За столом уже чувствуется, что утро может вытянуть за собой и разговор, и новости, и чьи-нибудь старые счеты.")
        else:
            _breakfast_lines.append("Ничего особенного за столом пока не происходит: обычное домашнее утро без лишней суеты.")
        MainTxt = "\n".join([row for row in _breakfast_lines if str(row or "").strip()])
        CurLocDesc = MainTxt
    $ _eat_result = player_eat_meal("утреннюю кашу и свежий хлеб", 16)
    if str(_eat_result.get("text", "") or "").strip():
        $ MainTxt = str(MainTxt or "") + "\n" + str(_eat_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
    $ _breakfast_social_ids = tavern_breakfast_apply_social_bonus()
    if len(list(_breakfast_social_ids or [])) > 0:
        $ MainTxt = str(MainTxt or "") + "\nСовместный завтрак заметно сближает вас с теми, кто сидит с вами за столом."
        $ CurLocDesc = MainTxt
    if tavern_breakfast_can_give_first_soap_samples():
        $ _soap_intro_text = tavern_breakfast_apply_first_soap_samples()
        if str(_soap_intro_text or "").strip():
            $ MainTxt = str(MainTxt or "") + "\n" + str(_soap_intro_text or "")
            $ CurLocDesc = MainTxt
    elif soap_available_piece_count() > 0 and int(TavernBreakfastSoapAnnouncedDay or -1) != int(dayspassed or 0):
        $ TavernBreakfastSoapAnnouncedDay = int(dayspassed or 0)
        $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    if len(list(tavern_recent_barber_ids() or [])) > 0:
        $ TavernBreakfastBarberTalkDay = int(dayspassed or 0)
    $ TavernBreakfastBaseText = str(MainTxt or "")
    $ TavernBreakfastBaseShownDay = -1
    $ TavernKitchenSavedText = str(MainTxt or "")
    $ TavernBreakfastEventActive = True
    call stat
    $ TavernKitchenRoom.npcs = tavern_breakfast_present_entries()
    $ CurrentRoom.npcs = TavernKitchenRoom.npcs
    hide screen main_ui
    call TavernKitchenBreakfastMenu
    return


label TavernKitchenBreakfastMenu:
    if not TavernBreakfastEventActive:
        show screen main_ui
        call TavernKitchenBuildActions
        return
    $ _breakfast_menu_text = tavern_breakfast_restore_ui_state()
    if int(TavernBreakfastBaseShownDay or -1) != int(dayspassed or 0):
        $ TavernBreakfastBaseShownDay = int(dayspassed or 0)
        call QueuePagedPanelText(str(_breakfast_menu_text or ""), current_action_title, list(current_action_items or []), "plain")
    call ReturnToMainUI
    return


label TavernKitchenBreakfastShowText(text="", return_label="TavernKitchenBreakfastMenu"):
    $ TavernBreakfastTextPages = build_breakfast_text_pages(text)
    $ TavernBreakfastTextPageIndex = 0
    $ TavernBreakfastTextReturnLabel = str(return_label or "TavernKitchenBreakfastMenu")
    $ current_action_title = "Завтрак"
    $ current_action_content = None
    $ current_action_items = list(tavern_breakfast_menu_items() or [])
    $ MainTxt = str(text or "")
    $ CurLocDesc = MainTxt
    call QueuePagedPanelText(str(text or ""), current_action_title, list(current_action_items or []), "plain")
    call ReturnToMainUI
    return


label TavernKitchenBreakfastTextPage:
    $ _breakfast_pages = list(TavernBreakfastTextPages or [""])
    if len(_breakfast_pages) <= 0:
        $ _breakfast_pages = [""]
    if int(TavernBreakfastTextPageIndex or 0) < 0:
        $ TavernBreakfastTextPageIndex = 0
    if int(TavernBreakfastTextPageIndex or 0) >= len(_breakfast_pages):
        $ TavernBreakfastTextPageIndex = len(_breakfast_pages) - 1
    $ MainTxt = str(_breakfast_pages[int(TavernBreakfastTextPageIndex or 0)] or "")
    $ CurLocDesc = MainTxt
    $ TavernKitchenSavedText = MainTxt
    "[MainTxt]"
    if int(TavernBreakfastTextPageIndex or 0) < (len(_breakfast_pages) - 1):
        menu:
            "Продолжить":
                $ TavernBreakfastTextPageIndex = int(TavernBreakfastTextPageIndex or 0) + 1
                jump TavernKitchenBreakfastTextPage
    jump expression TavernBreakfastTextReturnLabel


label TavernKitchenBreakfastHearDialogue:
    $ TavernBreakfastListenDay = int(dayspassed or 0)
    $ _talk_result = tavern_breakfast_talk_result()
    $ _banter_text = str(_talk_result.get("text", "") or "")
    $ _talk_arousal = int(_talk_result.get("arousal_gain", 0) or 0)
    if str(_banter_text or "").strip():
        $ MainTxt = str(_banter_text or "")
    else:
        $ MainTxt = "За столом на миг воцаряется обычная утренняя болтовня без чего-то особенно примечательного."
    if int(_talk_arousal or 0) > 0:
        $ Arousal["You"] = max(0, min(100, int(Arousal.get("You", 0) or 0) + int(_talk_arousal or 0)))
        $ MainTxt = str(MainTxt or "") + "\nЭтот разговор слишком легко цепляет и вас самих: утреннее возбуждение только сильнее мешает делать вид, будто вы слушаете все это совсем спокойно."
    $ CurLocDesc = MainTxt
    if int(_talk_arousal or 0) > 0:
        call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastTalkAbsent:
    $ TavernBreakfastAbsentTalkDay = int(dayspassed or 0)
    $ _absence_prompt = tavern_breakfast_absent_prompt()
    if str(_absence_prompt or "").strip():
        $ MainTxt = str(_absence_prompt or "") + "\n" + tavern_breakfast_absent_talk_text()
    else:
        $ MainTxt = tavern_breakfast_absent_talk_text()
    $ CurLocDesc = MainTxt
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastMarketTalk:
    $ TavernBreakfastMarketTalkDay = int(dayspassed or 0)
    if int(BlindPirateBreakfastPending or 0) == 1:
        call TavernKitchenBreakfastBlindPirateStory
        return
    $ MainTxt = tavern_breakfast_market_story_text()
    $ CurLocDesc = MainTxt
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastMotivation:
    $ TavernBreakfastMotivationDay = int(dayspassed or 0)
    $ MainTxt = tavern_breakfast_motivation_text()
    $ fun = _player_clamp(int(fun or 0) + 1, 0, 100)
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastServeSpicyDrink:
    if not tavern_breakfast_can_serve_spicy_tincture():
        jump TavernKitchenBreakfastMenu
    $ TavernBreakfastSpicyDrinkDay = int(dayspassed or 0)
    $ MainTxt = tavern_kitchen_spicy_tincture_apply(tavern_breakfast_present_ids())
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastBlindPirateStory:
    $ BlindPirateBreakfastPending = 0
    $ MainTxt = "Вы пересказываете за столом, как на рынке в клетке везли бывшего хозяина трактира «Слепой Пират» на галеры герцогини Кончиты, а следом за телегой, захлебываясь слезами, бежали женщины из его дома."
    if "sandra" in list(tavern_breakfast_present_ids() or []):
        $ MainTxt = str(MainTxt or "") + "\nСандра сразу мрачнеет. \"Трактир валится не за один день,\" тихо говорит она. \"Сперва уходит запас, потом честь, потом люди, а под конец уже и стены некому удержать.\""
    if "melissa" in list(tavern_breakfast_present_ids() or []):
        $ MainTxt = str(MainTxt or "") + "\nМелисса заметно притихает и только спрашивает, неужели у того дома и правда не осталось никого, кто успел бы удержать все от такой пропасти."
    if "amanda" in list(tavern_breakfast_present_ids() or []):
        $ MainTxt = str(MainTxt or "") + "\nДаже Аманда не спешит шутить. Она лишь морщится и бормочет, что от таких историй сразу как-то зябко, будто беда и сама уже стоит у дверей."
    if "becky" in list(tavern_breakfast_present_ids() or []):
        $ MainTxt = str(MainTxt or "") + "\nБекки тяжело вздыхает и признает, что вдовьи и долговые истории в этом городе всегда заканчиваются одинаково скверно, если рядом не находится кто-то достаточно упрямый, чтобы удержать дом на плаву."
    $ CurLocDesc = MainTxt
    $ fun = _player_clamp(int(fun or 0) + 5, 0, 100)
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastAnnounceGeorgetteLiza:
    $ TavernBreakfastGeorgetteLizaPending = 0
    $ MainTxt = "Вы даете за столом договорить всем до конца, а затем коротко объявляете, что Жоржетта с Лизеттой отныне будут жить и работать у вас в трактире.\n\nКогда по кухне проходит первый тяжелый шум, вы тут же пресекаете его и холодно напоминаете, чем закончилась судьба «Слепого Пирата». Если кому-то из присутствующих хочется проверить, не ждет ли ее галера, долговая яма или продажа в блудный дом, вы не станете никого удерживать. Но пока дом держится на вас, порядок здесь решаете вы.\n\nПосле этих слов разговор за столом резко остывает."
    if "sandra" in list(tavern_breakfast_present_ids() or []):
        $ MainTxt = str(MainTxt or "") + "\n\nСандра первая берет себя в руки. Она явно недовольна, но вместо скандала только сухо замечает, что тогда новых баб надо сразу встраивать в хозяйственный распорядок и следить, чтобы они не развалили дом изнутри."
    if "melissa" in list(tavern_breakfast_present_ids() or []):
        $ MainTxt = str(MainTxt or "") + "\n\nМелисса заметно бледнеет от вашей жесткости, но спорить не решается. По ее лицу видно, что она поняла сказанное слишком хорошо и теперь старается только не выдать своего страха лишним словом."
    if "amanda" in list(tavern_breakfast_present_ids() or []):
        $ MainTxt = str(MainTxt or "") + "\n\nАманда сперва открывает рот для колкости, но, встретившись с вашим взглядом, только отводит глаза и начинает нервно вертеть ложку в пальцах."
    if "becky" in list(tavern_breakfast_present_ids() or []):
        $ MainTxt = str(MainTxt or "") + "\n\nБекки хмуро косится на остальных и, похоже, предпочитает не подливать масла в огонь: вдова слишком хорошо знает, как быстро в городе рушатся дома, где хозяин теряет хватку."
    $ MainTxt = str(MainTxt or "") + "\n\nЖоржетта держится с показным достоинством, а Лизетта жмется к матери чуть ближе обычного. Вы же на этом обрываете завтрак и даете понять, что разговор окончен."
    $ CurLocDesc = MainTxt
    $ rebellion = max(0, int(rebellion or 0) - 1)
    $ neshlush["sandra"] = max(0, int(neshlush.get("sandra", 0) or 0) - 1)
    $ neshlush["melissa"] = max(0, int(neshlush.get("melissa", 0) or 0) - 1)
    $ neshlush["amanda"] = max(0, int(neshlush.get("amanda", 0) or 0) - 1)
    $ fun = _player_clamp(int(fun or 0) + 1, 0, 100)
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastDanceMenu:
    $ _dance_text = "За столом приходится быстро решить, готовы ли вы вложиться в пятничные танцы вином и закуской или пока отступите."
    $ tavern_breakfast_restore_ui_state(_dance_text)
    $ _dance_items = []
    if wine_for_dance_can_sponsor():
        $ _dance_items.append(MenuItem("Отправить вино и начать готовить закуску", Call("EventWineForDanceApply", 1)))
    else:
        $ _dance_items.append(MenuItem("Посокрушаться о нехватке запасов", Call("EventWineForDanceApply", 2)))
    $ _dance_items.append(MenuItem("Отказаться", Call("EventWineForDanceApply", 3)))
    $ _dance_items.append(MenuItem("Назад к завтраку", Jump("TavernKitchenBreakfastMenu")))
    call QueuePagedPanelText(_dance_text, "Решение о танцах", _dance_items, "plain")
    call ReturnToMainUI
    return


label TavernKitchenRefreshBreakfastEvent:
    call TavernKitchenBreakfastMenu
    return


label TavernKitchenFinishBreakfastEvent:
    $ TavernBreakfastEventActive = False
    $ TavernBreakfastBaseText = ""
    $ TavernBreakfastBaseShownDay = -1
    $ _kitchen_scene = tavern_kitchen_picture() or getattr(CurrentRoom, "bg_picture", "") or ""
    if str(_kitchen_scene or "").strip():
        vscene _kitchen_scene
    $ MainTxt = build_kitchen_description()
    $ CurLocDesc = MainTxt
    $ TavernKitchenSavedText = MainTxt
    call TavernKitchenBuildActions
    show screen main_ui
    return


label TavernKitchenSundayDinnerMenu:
    if not tavern_sunday_dinner_available():
        call TavernKitchenBuildActions
        return
    if not tavern_sunday_dinner_can_serve_spicy_tincture():
        call TavernKitchenSundayDinner
        return
    hide screen main_ui
    menu:
        "Воскресный обед"
        "Сесть за воскресный обед":
            call TavernKitchenSundayDinner(0)
            return
        "Сесть за воскресный обед и подать пряную настойку":
            call TavernKitchenSundayDinner(1)
            return
        "Назад":
            show screen main_ui
            call TavernKitchenBuildActions
            return


label TavernKitchenSundayDinner(serve_spicy=0):
    if not tavern_sunday_dinner_available():
        $ MainTxt = "Сегодня вы уже сидели за воскресным обедом."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    hide screen main_ui
    $ TavernSundayDinnerLastDay = int(dayspassed or 0)
    $ calendar_advance_minutes(45)
    vscene tavern_kitchen_sunday_dinner_picture()
    python:
        _sunday_lines = [
            "К полудню кухня собирает всех на более основательную воскресную трапезу.",
            "За столом сидят: " + (", ".join(tavern_sunday_dinner_present_names()) if len(tavern_sunday_dinner_present_names()) > 0 else "пока что только вы сами") + ".",
            "На некоторое время трактирная суета отступает, и весь дом живет одним общим столом.",
        ]
        _sunday_lines.extend(tavern_sunday_dinner_dialogue_lines())
        MainTxt = "\n\n".join([row for row in _sunday_lines if str(row or "").strip()])
        CurLocDesc = MainTxt
    $ _eat_result = player_eat_meal("воскресный обед для всей челяди", 22)
    if str(_eat_result.get("text", "") or "").strip():
        $ MainTxt = str(MainTxt or "") + "\n" + str(_eat_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
    $ _sunday_social_ids = tavern_sunday_dinner_apply_social_bonus()
    if len(list(tavern_recent_barber_ids() or [])) > 0:
        $ TavernSundayDinnerBarberTalkDay = int(dayspassed or 0)
    if len(list(_sunday_social_ids or [])) > 0:
        $ MainTxt = str(MainTxt or "") + "\nСпокойный воскресный стол немного сближает вас с теми, кто сейчас обедает вместе с вами."
        $ CurLocDesc = MainTxt
    if int(serve_spicy or 0) == 1 and tavern_sunday_dinner_can_serve_spicy_tincture():
        $ TavernSundayDinnerSpicyDrinkDay = int(dayspassed or 0)
        $ MainTxt = str(MainTxt or "") + "\n" + tavern_kitchen_spicy_tincture_apply(tavern_sunday_dinner_present_ids())
        $ CurLocDesc = MainTxt
    "[MainTxt]"
    call stat
    call TavernKitchenBuildActions
    show screen main_ui
    return


label TavernKitchenShareTeaWithSandraAndBecky:
    if not tavern_kitchen_can_share_tea_with_sandra_and_becky():
        $ MainTxt = "Сейчас для этого не время."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ _player_remove_item_by_id("energy_tea_001", 1)
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ Friends["becky"] = min(20, int(Friends.get("becky", 0) or 0) + 1)
    $ fun = _player_clamp(int(fun or 0) + 1, 0, 100)
    if _kitchen_worker_is_present("sandra"):
        $ _tea_scene = tavern_kitchen_random_sandra_scene()
        if str(_tea_scene or "").strip():
            $ _layout_last_picture = _tea_scene
    $ MainTxt = "Вы завариваете бодрящий чай и угощаете им Сандру с Бекки. Разговор за столом быстро теплеет: Сандра благодарит вас за внимание к хозяйству, а Бекки охотно подхватывает кухонные сплетни и делится парой полезных замечаний о трактирных делах."
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBuildActions
    return


label TavernKitchenDepositMenu:
    $ current_action_title = "Кухонные припасы"
    $ current_action_content = None
    $ current_action_items = []
    $ MainTxt = "Вы прикидываете, что из лесной добычи и запасов можно сразу оставить на кухне для общего хозяйства."
    if tavern_kitchen_food_stock_count() > 0:
        $ MainTxt = str(MainTxt or "") + "\nСейчас у Сандры уже лежат: %s." % tavern_kitchen_food_stock_summary()
    $ CurLocDesc = MainTxt
    python:
        for _deposit_row in tavern_kitchen_deposit_entries():
            current_action_items.append(MenuItem(str(_deposit_row.get("caption", "") or ""), Call("TavernKitchenDepositApply", str(_deposit_row.get("item_id", "") or ""))))
        if len(list(current_action_items or [])) <= 0:
            MainTxt = "Сейчас у вас при себе нет ничего подходящего для кухонных запасов."
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Call("TavernKitchenBuildActions")))
    return


label TavernKitchenDepositApply(item_id=""):
    $ _kitchen_item_id = str(item_id or "").strip()
    $ _kitchen_item_name = tavern_kitchen_food_item_name(_kitchen_item_id)
    $ _kitchen_deposited = tavern_kitchen_deposit_food(_kitchen_item_id)
    if int(_kitchen_deposited or 0) <= 0:
        $ MainTxt = "Нечего отдавать."
    else:
        $ MainTxt = "Вы оставляете на кухне %s x%s." % (_kitchen_item_name, _kitchen_deposited)
        if _kitchen_worker_is_present("sandra"):
            $ MainTxt = str(MainTxt or "") + "\nСандра деловито осматривает припасы, одобрительно кивает и сразу начинает прикидывать, как лучше пустить их в дело."
        $ _kitchen_deposit_effect_text = tavern_kitchen_deposit_effect_text(_kitchen_item_id)
        if str(_kitchen_deposit_effect_text or "").strip():
            $ MainTxt = str(MainTxt or "") + "\n" + str(_kitchen_deposit_effect_text or "")
    if tavern_kitchen_food_stock_count() > 0:
        $ MainTxt = str(MainTxt or "") + "\nТеперь в кухонных запасах лежат: %s." % tavern_kitchen_food_stock_summary()
    $ CurLocDesc = MainTxt
    call TavernKitchenBuildActions
    return


label TavernKitchenAskSandraBreakfasts:
    if not tavern_kitchen_sandra_can_discuss_breakfasts():
        $ MainTxt = "Сейчас не лучший момент для такого разговора."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ _kitchen_used_item = tavern_kitchen_take_food_from_stock(["boar_meat_001", "honey_comb_001", "berries_001", "mushroom_001"])
    $ AskedToday["sandra"] = int(AskedToday.get("sandra", 0) or 0) + 1
    $ Talked["sandra"] = int(Talked.get("sandra", 0) or 0) + 1
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
    $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    $ fun = _player_clamp(int(fun or 0) + 2, 0, 100)
    $ MainTxt = "Вы просите Сандру почаще собирать домочадцев за общий утренний стол и не давать всем разбредаться без толку. Сандра выслушивает вас без лишних слов, потом переводит взгляд на оставленные припасы и кивает.\n\n\"Ладно. Если уж на кухне есть из чего готовить, я поговорю с девочками. Общий завтрак дому не повредит, а там и работа ровнее пойдет,\" решает она."
    if str(_kitchen_used_item or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\nДля ближайшего такого стола Сандра сразу откладывает %s." % tavern_kitchen_food_item_name(_kitchen_used_item)
    $ CurLocDesc = MainTxt
    $ TavernKitchenSavedText = MainTxt
    if TavernBreakfastEventActive:
        jump TavernKitchenBreakfastMenu
    else:
        call TavernKitchenBuildActions
    return


label TavernKitchenAskSandraClients:
    if not tavern_kitchen_sandra_can_discuss_clients():
        $ MainTxt = "Сейчас не лучший момент для такого разговора."
        $ CurLocDesc = MainTxt
        call TavernKitchenBuildActions
        return
    $ _kitchen_used_item = tavern_kitchen_take_food_from_stock(["berries_001", "honey_comb_001", "boar_meat_001", "mushroom_001"])
    $ AskedToday["sandra"] = int(AskedToday.get("sandra", 0) or 0) + 1
    $ Talked["sandra"] = int(Talked.get("sandra", 0) or 0) + 1
    $ Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 1)
    $ tavernfame = int(tavernfame or 0) + 1
    $ MainTxt = "Вы просите Сандру поговорить с домочадцами и держаться с гостями немного мягче обычного. Сандра щурится, явно взвешивая сказанное, а потом нехотя соглашается.\n\n\"Если уж хочешь, чтобы в трактире было больше довольных рож, я скажу девочкам не срываться на людях почем зря. Но и ты смотри, чтобы работа не шла через пень-колоду,\" бурчит она."
    if str(_kitchen_used_item or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\nЗаодно Сандра решает пустить %s на что-нибудь поприятнее для посетителей." % tavern_kitchen_food_item_name(_kitchen_used_item)
    $ CurLocDesc = MainTxt
    $ TavernKitchenSavedText = MainTxt
    if TavernBreakfastEventActive:
        jump TavernKitchenBreakfastMenu
    else:
        call TavernKitchenBuildActions
    return


label TavernKitchenObjectMenu(object_id="", refresh_only=False):
    $ tavern_kitchen_hearth_wood_stock()
    if str(object_id or "") != "":
        $ current_object_id = object_id
    $ object_id = current_object_id
    $ _kitchen_object = None
    python:
        for _room_object in CurrentRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _kitchen_object = _room_object
                break

    if _kitchen_object is None:
        call TavernKitchenBuildActions
        return

    $ current_action_title = str(_kitchen_object.name or "Действия")
    $ current_action_content = None
    $ current_action_items = []
    if str(getattr(_kitchen_object, "picture", "") or "").strip() and renpy.loadable(str(getattr(_kitchen_object, "picture", "") or "").strip()):
        $ _layout_last_picture = str(getattr(_kitchen_object, "picture", "") or "").strip()
    if str(object_id or "") == "hearth_001":
        $ MainTxt = tavern_kitchen_hearth_description()
    elif str(object_id or "") == "cauldron_001":
        $ MainTxt = tavern_kitchen_cauldron_description()
    else:
        $ MainTxt = str(_kitchen_object.description or "")
    $ CurLocDesc = MainTxt

    python:
        for _kitchen_action in _kitchen_object.visible_actions():
            _kitchen_args = tuple(getattr(_kitchen_action, "args", ()) or ())
            if _kitchen_action.hook == "text":
                current_action_items.append(MenuItem(_kitchen_action.label, Call("TavernKitchenObjectText", object_id, _kitchen_action.action_id)))
            elif _kitchen_action.hook == "call" and str(_kitchen_action.target or "") != "":
                current_action_items.append(MenuItem(_kitchen_action.label, Call(_kitchen_action.target, *_kitchen_args)))
            elif _kitchen_action.hook == "jump" and str(_kitchen_action.target or "") != "":
                current_action_items.append(MenuItem(_kitchen_action.label, Jump(_kitchen_action.target)))
        current_action_items.append(MenuItem("Назад", Call("TavernKitchenRestore")))
    return


label TavernKitchenObjectText(object_id="", action_id=""):
    python:
        _kitchen_text = ""
        _kitchen_name = ""
        for _room_object in CurrentRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _kitchen_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _kitchen_text = str(_room_action.target or "")
                    break
            break
        if _kitchen_text:
            MainTxt = _kitchen_text
            CurLocDesc = _kitchen_text
            current_action_title = _kitchen_name or "Действия"
    call TavernKitchenObjectMenu(object_id)
    return


label TavernKitchenRestore:
    $ MainTxt = str(TavernKitchenSavedText or build_kitchen_description())
    $ CurLocDesc = MainTxt
    call TavernKitchenBuildActions
    return
