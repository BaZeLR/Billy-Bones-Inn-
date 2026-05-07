# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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
default TavernBreakfastPresentIds = None
default TavernBreakfastMelissaAmandaGerhardDay = -1
default TavernBreakfastSharePerks = {}
default TavernBreakfastFoodPerkDay = -1
default TavernBreakfastDrinkPerkDay = -1
default TavernBreakfastLewdSeriesDay = -1
default TavernBreakfastAppearancePerkDay = -1
default TavernBreakfastSweetPerkDay = -1
default TavernBreakfastBlindPirateTeamPledge = 0
default TavernBreakfastMilkTeamTalkDone = 0
default TavernBreakfastAleTeamTalkDone = 0

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
        if str(getLocation("sandra") or "") == "TavernKitchen":
            sandra_scene = tavern_kitchen_random_sandra_scene()
            if sandra_scene:
                return sandra_scene
        if str(getLocation("melissa") or "") == "TavernKitchen":
            if random.randint(1, 4) == 1:
                if renpy.loadable("images/melissa/tavern/basement.png"):
                    return "images/melissa/tavern/basement.png"
                if renpy.loadable("images/tavern/storage/storage_room.png"):
                    return "images/tavern/storage/storage_room.png"
                if renpy.loadable("images/tavern/kitchen/kitchen_room.png"):
                    return "images/tavern/kitchen/kitchen_room.png"
                return resolve_room_background_media(TavernKitchenRoom)
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
            and int(time or 0) in (1, 2)
            and int(hour or 0) >= 12
            and int(hour or 0) < 18
            and int(TavernSundayDinnerLastDay or -1) != int(dayspassed or 0)
        )

    def tavern_breakfast_present_ids():
        present = []
        if bool(TavernBreakfastEventActive) and isinstance(TavernBreakfastPresentIds, list):
            present.extend(list(TavernBreakfastPresentIds or []))
        else:
            present.extend(list(household_breakfast_attendee_ids() or []))

        try:
            present.extend(list(getNPCids("TavernKitchen") or []))
        except Exception:
            pass

        rows = []
        seen = set()
        for npc_id in present:
            key = str(npc_id or "").strip().lower()
            if key not in ("sandra", "melissa", "amanda", "becky"):
                continue
            if key in seen:
                continue
            seen.add(key)
            rows.append(key)
        return rows

    def tavern_breakfast_present_names():
        names = []
        for npc_id in tavern_breakfast_present_ids():
            names.append(_action_display_name(npc_id))
        return names

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

    def tavern_breakfast_morning_issue_girl():
        for npc_id in ("sandra", "melissa", "amanda"):
            if npc_id in list(tavern_breakfast_present_ids() or []):
                continue
            issue_code = str(household_morning_issue_type(npc_id) or "").strip()
            if issue_code not in ("sick", "sleepy"):
                continue
            if len(list(household_room_issue_action_specs(npc_id) or [])) > 0:
                return npc_id
        return ""

    def tavern_breakfast_morning_issue_text(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        issue_code = str(household_morning_issue_type(girl) or "").strip()
        girl_name_text = _action_display_name(girl)
        if issue_code == "sick":
            return "%s не вышла к завтраку. По утренней суете уже понятно: это не просто опоздание, а состояние, с которым надо что-то решать отдельно." % girl_name_text
        if issue_code == "sleepy":
            return "%s так и не появилась за столом. Похоже, она проспала общий подъем, и теперь вам решать, будить ее или оставить последствия Сандре." % girl_name_text
        return "Сейчас за завтраком нет отдельной утренней проблемы, которую надо решать."

    def tavern_breakfast_banter_text():
        present_ids = set(tavern_breakfast_present_ids())
        absent_ids = tavern_breakfast_absent_ids()
        if "amanda" in present_ids and "melissa" in absent_ids:
            if amanda_attic_busted():
                return "Аманда на удивление не торопится цеплять Мелиссу привычной колкостью. Она только косится в сторону лестницы и слишком уж старательно делает вид, будто ее куда больше интересует каша, чем чужая спальня."
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

    def tavern_breakfast_amanda_alt_cure_possible():
        if not amanda_attic_busted():
            return False
        if "amanda" not in list(tavern_breakfast_present_ids() or []):
            return False
        if int(AmandaVar.get("attic_window_breakfast_bj_day", -1) or -1) == int(dayspassed or 0):
            return False
        wetness = max(int(PussyWetStart.get("amanda", 0) or 0), int(Arousal.get("amanda", 0) or 0))
        return wetness >= 25 or int(sluttiness.get("amanda", 0) or 0) >= 28

    def tavern_breakfast_amanda_alt_cure_ready():
        if not tavern_breakfast_amanda_alt_cure_possible():
            return False
        wetness = max(int(PussyWetStart.get("amanda", 0) or 0), int(Arousal.get("amanda", 0) or 0))
        sluttiness_value = int(sluttiness.get("amanda", 0) or 0)
        chance = 15 + max(0, wetness - 25) * 2 + max(0, sluttiness_value - 28)
        if "melissa" in list(tavern_breakfast_present_ids() or []):
            chance += 8
        profile = build_girl_decision_profile("amanda")
        decision_bonus = int(girl_decision_good_probability("amanda", "breakfast_alt_cure", profile) * 35)
        chance += decision_bonus
        if str(profile.get("cycle_phase", "") or "") == "critical":
            chance -= 10
        if float(profile.get("anger", 0.0) or 0.0) > 0.0:
            chance -= 12
        chance = max(15, min(70, int(chance or 0)))
        roll = (int(dayspassed or 0) * 17 + int(week or 0) * 13 + int(hour or 0) * 5 + wetness + sluttiness_value * 3 + int(profile.get("rebel_value", 0) or 0) * 7) % 100
        return roll < chance

    def tavern_breakfast_amanda_attic_mock_ready():
        return (
            amanda_attic_busted()
            and "amanda" in list(tavern_breakfast_present_ids() or [])
            and int(AmandaVar.get("attic_mock_stopped", 0) or 0) == 0
            and int(AmandaVar.get("attic_mock_exposed", 0) or 0) == 0
            and int(AmandaVar.get("attic_mock_response_day", -1) or -1) != int(dayspassed or 0)
        )

    def tavern_breakfast_sweet_or_spiced_served():
        return (
            tavern_kitchen_honey_bonus_active()
            or tavern_kitchen_fertility_bonus_active()
            or int(TavernBreakfastSpicyDrinkDay or -1) == int(dayspassed or 0)
            or int(TavernBreakfastSweetPerkDay or -1) == int(dayspassed or 0)
        )

    def tavern_breakfast_melissa_amanda_gerhard_ready():
        present_ids = list(tavern_breakfast_present_ids() or [])
        return (
            melissa_bats_stage() >= 6
            and melissa_bats_stage() < 8
            and str(MelissaVar.get("temp_room", "") or "") == "TavernAmandaRoom"
            and amanda_attic_busted()
            and "melissa" in present_ids
            and "amanda" in present_ids
            and "sandra" not in present_ids
            and int(TavernBreakfastMelissaAmandaGerhardDay or -1) != int(dayspassed or 0)
            and tavern_breakfast_sweet_or_spiced_served()
        )

    def tavern_breakfast_soap_request_girl():
        for npc_id in list(tavern_breakfast_present_ids() or []):
            if npc_id in ("sandra", "melissa", "amanda") and household_soap_request_ready(npc_id):
                return npc_id
        return ""

    def tavern_breakfast_dress_request_girl():
        present_ids = list(tavern_breakfast_present_ids() or [])
        if "sandra" in present_ids and sandra_revealing_dress_initiative_ready():
            return "sandra"
        if "melissa" in present_ids and melissa_revealing_dress_request_ready():
            return "melissa"
        if "amanda" in present_ids and amanda_revealing_dress_request_ready():
            return "amanda"
        return ""

    def tavern_breakfast_tease_candidate():
        candidates = []
        for npc_id in list(tavern_breakfast_present_ids() or []):
            if npc_id not in ("amanda", "melissa"):
                continue
            state = AmandaVar if npc_id == "amanda" else MelissaVar
            if int(state.get("breakfast_tease_day", -1) or -1) == int(dayspassed or 0):
                continue
            friend_value = int(Friends.get(npc_id, 0) or 0)
            open_value = int(otkroven.get(npc_id, 0) or 0)
            corruption_value = int(sluttiness.get(npc_id, 0) or 0)
            perk_score = tavern_breakfast_player_perk_score(npc_id)
            friend_need = max(4, 6 - perk_score // 5)
            open_need = 0 if perk_score >= 8 else 1
            corruption_need = max(8, 12 - perk_score)
            if friend_value < friend_need or open_value < open_need or corruption_value < corruption_need:
                continue
            tier = 1
            if friend_value >= 8 and open_value >= 4 and corruption_value >= 28:
                tier = 2
            if friend_value >= 11 and open_value >= 7 and corruption_value >= 45:
                tier = 3
            if perk_score >= 8:
                tier = max(tier, 2)
            if perk_score >= 12 and corruption_value >= 20:
                tier = max(tier, 3)
            if perk_score >= 16 and corruption_value >= 30:
                tier = max(tier, 4)
            candidates.append((tier, friend_value + open_value + corruption_value + perk_score * 2, npc_id))
        if len(candidates) <= 0:
            return {"girl": "", "tier": 0}
        candidates.sort(reverse=True)
        return {"girl": str(candidates[0][2] or ""), "tier": int(candidates[0][0] or 0)}

    def tavern_breakfast_tease_ready():
        return str(tavern_breakfast_tease_candidate().get("girl", "") or "") != ""

    def tavern_breakfast_player_perk_score(npc_id=""):
        key = str(npc_id or "").strip().lower()
        if key not in ("sandra", "melissa", "amanda"):
            return 0
        score = 0
        score += min(4, max(0, int(Friends.get(key, 0) or 0) // 4))
        score += min(3, max(0, int(otkroven.get(key, 0) or 0) // 5))
        score += min(3, max(0, int(sluttiness.get(key, 0) or 0) // 20))
        if int(dayspassed or 0) - int(BarberVisitLastDay.get(key, -99) or -99) <= 14:
            score += 2
        dress_top = str(topdress.get(key, "") or topdressdef.get(key, "") or "")
        dress_bottom = str(bottomdress.get(key, "") or bottomdressdef.get(key, "") or "")
        dress_score = max(int(DressPartSlut.get(dress_top, 0) or 0), int(DressPartSlut.get(dress_bottom, 0) or 0))
        if dress_score >= 4:
            score += 2
        elif dress_score >= 3:
            score += 1
        if tavern_kitchen_honey_bonus_active():
            score += 2
        if tavern_kitchen_milk_bonus_active():
            score += 1
        if tavern_kitchen_boar_bonus_active():
            score += 1
        if int(TavernBreakfastSpicyDrinkDay or -1) == int(dayspassed or 0):
            score += 2
        share_perks = TavernBreakfastSharePerks or {}
        if isinstance(share_perks, dict):
            share_data = share_perks.get(key, {})
            if isinstance(share_data, dict) and int(dayspassed or 0) - int(share_data.get("day", -99) or -99) <= 7:
                score += min(3, max(1, int(share_data.get("score", 1) or 1)))
        if int(ClaraVar.get("booklet_market_seen", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1:
            score += 1
        return max(0, int(score or 0))

    def tavern_breakfast_household_perk_score():
        present_ids = [npc_id for npc_id in list(tavern_breakfast_present_ids() or []) if npc_id in ("sandra", "melissa", "amanda")]
        if len(present_ids) <= 0:
            return 0
        return sum([tavern_breakfast_player_perk_score(npc_id) for npc_id in present_ids])

    def tavern_breakfast_relaxed_appearance_lines():
        present_ids = [npc_id for npc_id in list(tavern_breakfast_present_ids() or []) if npc_id in ("sandra", "melissa", "amanda")]
        if len(present_ids) <= 0:
            return []
        total_score = tavern_breakfast_household_perk_score()
        if total_score < 8:
            return []
        relaxed = []
        for npc_id in present_ids:
            score = tavern_breakfast_player_perk_score(npc_id)
            if score >= 10:
                relaxed.append((npc_id, "ночной рубашке"))
            elif score >= 7:
                relaxed.append((npc_id, "домашнем, чуть небрежном виде"))
        if len(relaxed) <= 0:
            return []
        names = ["%s в %s" % (_action_display_name(npc_id), caption) for npc_id, caption in relaxed]
        lines = [
            "За завтраком уже видно, что домочадцы воспринимают вас не просто как хозяина, а как человека, от которого идут реальные удобства: еда, сладости, напитки, обновки, визиты к Серджио и всякие опасно интересные городские истории.",
            "Из-за этого утренний стол стал заметно домашнее. %s приходит к еде без прежней показной собранности, будто в этом доме уже можно не строить из себя приличную статую с первой минуты после сна." % ", ".join(names),
        ]
        if int(ClaraVar.get("booklet_market_seen", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1:
            lines.append("После разговоров о непристойных рисунках и книжечках Клариссы даже обычные шутки за столом цепляют сильнее: все слишком хорошо понимают, какие картинки теперь стоят за невинными словами.")
        share_perks = TavernBreakfastSharePerks or {}
        recent_shared = []
        if isinstance(share_perks, dict):
            for npc_id in present_ids:
                share_data = share_perks.get(npc_id, {})
                if isinstance(share_data, dict) and int(dayspassed or 0) - int(share_data.get("day", -99) or -99) <= 7:
                    recent_shared.append(_action_display_name(npc_id))
        if len(recent_shared) > 0:
            lines.append("Те, с кем вы недавно делились едой, напитками или сладостями, держатся за столом теплее обычного: %s явно помнят, что ваша забота не ограничивается приказами." % ", ".join(recent_shared))
        if tavern_kitchen_honey_bonus_active() or int(TavernBreakfastSpicyDrinkDay or -1) == int(dayspassed or 0):
            lines.append("Сладкое и пряное только подталкивают этот настрой: взгляды задерживаются дольше, а поддевки звучат смелее обычного.")
        return lines

    def tavern_breakfast_core_present_ids():
        rows = []
        for npc_id in list(tavern_breakfast_present_ids() or []):
            key = str(npc_id or "").strip().lower()
            if key in ("sandra", "melissa", "amanda"):
                rows.append(key)
        return rows

    def tavern_breakfast_look_picture(npc_id=""):
        key = str(npc_id or "").strip().lower()
        candidates = {
            "sandra": [
                "images/sandra/tavern/kitchen_sandra_0.jpg",
                "images/sandra/sandra_kitchen.png",
                "images/tavern/kitchen/sandra.png",
                "images/tavern/kitchen/kitchen_sandra_0.jpg",
            ],
            "melissa": [
                "images/melissa/tavern/kitchen_0.png",
                "images/melissa/tavern/kitchen_1.png",
                "images/melissa/tavern/portrait.png",
            ],
            "amanda": [
                "images/amanda/kitchen_help.png",
                "images/amanda/amanda_card.jpg",
                "images/amanda/amanda_portrait.jpg",
            ],
        }.get(key, [])
        for picture_path in candidates:
            if renpy.loadable(picture_path):
                return picture_path
        return tavern_kitchen_breakfast_picture()

    def tavern_breakfast_look_text(npc_id=""):
        key = str(npc_id or "").strip().lower()
        name = _action_display_name(key)
        if key not in list(tavern_breakfast_present_ids() or []):
            return "%s сейчас не сидит за завтраком, так что разглядывать за столом некого." % name
        if key == "sandra":
            return "Вы внимательнее смотрите на Сандру за завтраком. Она держит стол в хозяйском порядке даже тогда, когда молчит: взглядом поправляет ленивых, замечает пустую миску раньше остальных и одним своим присутствием не дает кухне развалиться в балаган."
        if key == "melissa":
            return "Вы присматриваетесь к Мелиссе за завтраком. Если она пришла к столу, значит старается держаться вместе с домом: ест аккуратно, слушает больше, чем говорит, и слишком быстро опускает глаза, когда разговор становится личным."
        if key == "amanda":
            return "Вы смотрите, как Аманда ведет себя за завтраком. Она будто специально занимает чуть больше места за столом, лениво играет ложкой и ловит чужие реакции, проверяя, кто первым сорвется на замечание."
        return "%s сидит за общим столом, и этого уже достаточно, чтобы разговоры и настроение завтрака шли иначе." % name

    def tavern_breakfast_record_group_perk(item_id="", score=1, targets=None):
        global TavernBreakfastSharePerks

        rows = list(targets or tavern_breakfast_core_present_ids() or [])
        if len(rows) <= 0:
            return []
        if not isinstance(TavernBreakfastSharePerks, dict):
            TavernBreakfastSharePerks = {}
        item_key = str(item_id or "").strip()
        perk_score = max(1, int(score or 1))
        for npc_id in rows:
            key = str(npc_id or "").strip().lower()
            if key not in ("sandra", "melissa", "amanda"):
                continue
            existing = TavernBreakfastSharePerks.get(key, {})
            existing_score = int(existing.get("score", 0) or 0) if isinstance(existing, dict) else 0
            TavernBreakfastSharePerks[key] = {
                "day": int(dayspassed or 0),
                "item": item_key,
                "score": max(existing_score, perk_score),
            }
        return rows

    def tavern_breakfast_apply_group_social(targets=None, friend_delta=0, open_delta=0, corruption_delta=0, fun_delta=0):
        global fun

        rows = list(targets or tavern_breakfast_core_present_ids() or [])
        for npc_id in rows:
            if int(friend_delta or 0) != 0:
                Friends[npc_id] = min(20, max(0, int(Friends.get(npc_id, 0) or 0) + int(friend_delta or 0)))
            if int(open_delta or 0) != 0:
                otkroven[npc_id] = min(20, max(0, int(otkroven.get(npc_id, 0) or 0) + int(open_delta or 0)))
            if int(corruption_delta or 0) != 0:
                sluttiness[npc_id] = min(100, max(0, int(sluttiness.get(npc_id, 0) or 0) + int(corruption_delta or 0)))
        if int(fun_delta or 0) != 0:
            fun = _player_clamp(int(fun or 0) + int(fun_delta or 0), 0, 100)
        return rows

    def tavern_breakfast_take_perk_item(preferred_ids=None):
        preferred = list(preferred_ids or [])
        if len(preferred) <= 0:
            return ""
        if isinstance(KitchenWildFoodStock, dict):
            stocked = tavern_kitchen_take_food_from_stock(preferred)
            if str(stocked or "").strip():
                return str(stocked or "").strip()
        for item_id in preferred:
            item_key = str(item_id or "").strip()
            if item_key and int(_player_item_count_by_id(item_key) or 0) > 0:
                if _player_remove_item_by_id(item_key, 1):
                    return item_key
        return ""

    def tavern_breakfast_food_perk_item_available():
        for item_id in ("honey_comb_001", "berries_001", "milk_pitcher_001", "boar_meat_001", "mushroom_001"):
            if tavern_kitchen_food_stock_count(item_id) > 0 or int(_player_item_count_by_id(item_id) or 0) > 0:
                return True
        return False

    def tavern_breakfast_drink_perk_item_available():
        for item_id in ("energy_tea_001", "drink_ale_001", "libido_tincture_001"):
            if int(_player_item_count_by_id(item_id) or 0) > 0:
                return True
        return False

    def tavern_breakfast_lewd_series_available():
        return int(ClaraVar.get("booklet_market_seen", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1

    def tavern_breakfast_appearance_perk_available():
        for npc_id in tavern_breakfast_core_present_ids():
            if int(dayspassed or 0) - int(BarberVisitLastDay.get(npc_id, -99) or -99) <= 14:
                return True
            dress_top = str(topdress.get(npc_id, "") or topdressdef.get(npc_id, "") or "")
            dress_bottom = str(bottomdress.get(npc_id, "") or bottomdressdef.get(npc_id, "") or "")
            if max(int(DressPartSlut.get(dress_top, 0) or 0), int(DressPartSlut.get(dress_bottom, 0) or 0)) >= 3:
                return True
        return False

    def tavern_breakfast_can_offer_perk_menu():
        if len(tavern_breakfast_core_present_ids()) <= 0:
            return False
        day_value = int(dayspassed or 0)
        return (
            (int(TavernBreakfastFoodPerkDay or -1) != day_value and tavern_breakfast_food_perk_item_available())
            or (int(TavernBreakfastDrinkPerkDay or -1) != day_value and tavern_breakfast_drink_perk_item_available())
            or (int(TavernBreakfastLewdSeriesDay or -1) != day_value and tavern_breakfast_lewd_series_available())
        )

    def tavern_breakfast_perk_menu_items():
        items = []
        day_value = int(dayspassed or 0)
        special_milk_ready = False
        special_ale_ready = False
        if int(TavernBreakfastBlindPirateTeamPledge or 0) == 1 and int(TavernBreakfastMilkTeamTalkDone or 0) == 0 and int(TavernBreakfastFoodPerkDay or -1) != day_value:
            if tavern_kitchen_food_stock_count("milk_pitcher_001") > 0 or int(_player_item_count_by_id("milk_pitcher_001") or 0) > 0:
                special_milk_ready = True
                items.append(MenuItem("Поделиться молоком", Call("TavernKitchenBreakfastPerkFood", "milk_pitcher_001")))
        if int(TavernBreakfastBlindPirateTeamPledge or 0) == 1 and int(TavernBreakfastMilkTeamTalkDone or 0) == 1 and int(TavernBreakfastAleTeamTalkDone or 0) == 0 and int(TavernBreakfastDrinkPerkDay or -1) != day_value:
            if int(_player_item_count_by_id("drink_ale_001") or 0) > 0:
                special_ale_ready = True
                items.append(MenuItem("Поделиться элем за команду", Call("TavernKitchenBreakfastPerkDrink", "drink_ale_001")))
        if not special_milk_ready and int(TavernBreakfastFoodPerkDay or -1) != day_value and tavern_breakfast_food_perk_item_available():
            items.append(MenuItem("Поставить на стол лучшие припасы", Jump("TavernKitchenBreakfastPerkFood")))
        if not special_ale_ready and int(TavernBreakfastDrinkPerkDay or -1) != day_value and tavern_breakfast_drink_perk_item_available():
            items.append(MenuItem("Поделиться напитком", Jump("TavernKitchenBreakfastPerkDrink")))
        if int(TavernBreakfastLewdSeriesDay or -1) != day_value and tavern_breakfast_lewd_series_available():
            items.append(MenuItem("Подкинуть тему про новые непристойные листки", Jump("TavernKitchenBreakfastPerkLewdSeries")))
        items.append(MenuItem("Назад к завтраку", Jump("TavernKitchenBreakfastMenu")))
        return items

    def tavern_breakfast_blind_pirate_team_present():
        present_ids = list(tavern_breakfast_present_ids() or [])
        return "sandra" in present_ids and "melissa" in present_ids and "amanda" in present_ids

    def tavern_breakfast_blind_pirate_story_text():
        present_ids = list(tavern_breakfast_present_ids() or [])
        if "sandra" in present_ids and "melissa" in present_ids and "amanda" in present_ids:
            return "\n\n".join([
                "Вы пересказываете за столом, что видели на рынке: бывшего хозяина трактира «Слепой Пират» в клетке, дорогу на галеры герцогини Кончиты и женщин из его дома, которые бежали следом уже без дома, денег и защиты.",
                "На кухне становится тихо. Даже ложки стучат осторожнее: всем понятно, что такая беда начинается не с одной ошибки, а с того дня, когда дом перестает держаться вместе.",
                "Сандра первой мрачно кивает. \"Вот так трактиры и гибнут. Сперва хозяин думает, что как-нибудь выкрутится, потом продукты уходят, люди разбегаются, а под конец уже поздно молиться.\"",
                "Мелисса опускает глаза к миске. \"Значит, если дом провалится, никто нас потом красиво спасать не станет,\" тихо говорит она. \"Просто уведут, продадут или забудут.\"",
                "Именно это молчание Аманда и ломает. Она хмыкает, оглядывает всех и нарочно говорит бодрее: \"Слушайте, я от одной девки слышала про цирюльню Серджио. Там и волосы приводят в порядок, и девок делают такими, что люди в зале смотрят совсем иначе. Он еще, говорят, милый. Может, мессир Стефан будет так добр и когда-нибудь сводит нас туда?\"",
                "Вы смотрите на нее достаточно долго, чтобы шутка перестала быть просто шуткой. \"Если дела пойдут ровно, и вы будете стараться, почему бы и нет. Но сперва дом, работа и порядок. Хорошие вещи будут наградой для тех, кто помогает трактиру не стать вторым «Слепым Пиратом».\"",
                "Аманда только пожимает плечами и улыбается так, будто услышала ровно то, что хотела: не отказ, а условие. Сандра ворчит для порядка, Мелисса уже украдкой смотрит на Аманду с новым любопытством, а завтрак снова начинает шуметь.",
            ])
        lines = [
            "Вы пересказываете за столом, что видели на рынке: бывшего хозяина трактира «Слепой Пират» в клетке, дорогу на галеры герцогини Кончиты и женщин из его дома, которые бежали следом уже без дома, денег и защиты.",
            "Эта история ложится на кухню тяжело. Сегодня она звучит не как слух, а как предупреждение: если дом перестанет держаться вместе, город быстро найдет, как разделить тех, кто останется без защиты.",
        ]
        if "amanda" in present_ids:
            lines.append("Аманда после паузы все равно пытается увести разговор к цирюльне Серджио и женским хитростям, но вы отвечаете ей прямо: хорошие вещи появятся только тогда, когда дом будет работать ровно.")
        return "\n\n".join(lines)

    def tavern_breakfast_blind_pirate_milk_text():
        return "\n\n".join([
            "Вы ставите на стол свежую крынку молока. После разговора о «Слепом Пирате» это выглядит почти вызывающе просто: не обещание богатства, а знак, что сегодня в вашем доме есть чем поделиться.",
            "Аманда первой тянется к кружке и довольно щурится. \"Ох, молоко... свежее и славное. Ах, прямо туда попало, куда надо. Спасибо, мессир Стефан.\"",
            "Мелисса тут же оживляется: \"С медом было бы еще лучше. Я слышала, от молока с медом грудь растет. Аманде как раз надо.\"",
            "Аманда вскидывает подбородок. \"С моей грудью все в порядке.\"",
            "Мелисса невинно хлопает глазами. \"Тогда зачем ты корсет рваными тряпками набиваешь, м-м?\"",
            "Сандра резко ставит кружку на стол. \"Замолчите обе. Вы сейчас мессиру Стефану уши в кашу уроните от стыда.\"",
            "Мелисса только пожимает плечами: \"Мы же все здесь команда, разве нет?\" Аманда сразу кивает: \"Да. Он один из нас. Верно?\"",
            "Сандра вздыхает, но уже мягче. \"Может, и верно. По крайней мере, сегодня у нас есть что поставить на стол. Дай бог, чтобы так и осталось.\"",
            "Вы спокойно отвечаете: \"Я сделаю все, что потребуется, чтобы мы не закончили как «Слепой Пират».\" После этих слов молоко уже не просто угощение, а первый настоящий знак общего дома.",
        ])

    def tavern_breakfast_blind_pirate_ale_text():
        return "\n\n".join([
            "Вы достаете эль и разливаете его малыми кружками, не для пьянства, а за общий стол. После молока, шуток и тяжелой рыночной истории это звучит почти как маленькая клятва.",
            "\"За команду,\" говорите вы. \"За трактир. И за то, чтобы этот дом не пошел вслед за «Слепым Пиратом».\"",
            "Сандра, Мелисса и Аманда переглядываются. На лицах у них нет полного доверия, но уже нет и прежней холодной осторожности.",
            "\"Посмотрим,\" отвечают они почти одновременно.",
            "И в этом коротком ответе слышится не отказ. Скорее испытательный срок: они готовы смотреть, что вы сделаете дальше.",
        ])

    def tavern_breakfast_apply_food_perk(preferred_ids=None):
        global TavernBreakfastFoodPerkDay, TavernBreakfastSweetPerkDay, TavernBreakfastMilkTeamTalkDone

        preferred = preferred_ids or ("honey_comb_001", "berries_001", "milk_pitcher_001", "boar_meat_001", "mushroom_001")
        item_key = tavern_breakfast_take_perk_item(preferred)
        if str(item_key or "").strip() == "":
            return "На кухне не находится ничего достаточно хорошего, чтобы сделать из этого особое утреннее угощение."
        TavernBreakfastFoodPerkDay = int(dayspassed or 0)
        score = 1
        if item_key in ("honey_comb_001", "berries_001", "milk_pitcher_001"):
            TavernBreakfastSweetPerkDay = int(dayspassed or 0)
            score = 3 if item_key == "honey_comb_001" else 2
        if item_key == "boar_meat_001":
            score = 2
        targets = tavern_breakfast_record_group_perk(item_key, score)
        tavern_breakfast_apply_group_social(targets, 1, 0, 1 if item_key in ("honey_comb_001", "boar_meat_001") else 0, 2)
        if item_key == "milk_pitcher_001" and int(TavernBreakfastBlindPirateTeamPledge or 0) == 1 and int(TavernBreakfastMilkTeamTalkDone or 0) == 0 and tavern_breakfast_blind_pirate_team_present():
            TavernBreakfastMilkTeamTalkDone = 1
            return tavern_breakfast_blind_pirate_milk_text()
        item_name = tavern_kitchen_food_item_name(item_key)
        text = "Вы не просто завтракаете, а ставите на стол %s как отдельное угощение для своих. Домочадцы быстро понимают разницу: это уже не казенная миска, а знак, что хорошие припасы идут тем, кто держит дом рядом с вами." % item_name
        if item_key in ("honey_comb_001", "berries_001", "milk_pitcher_001"):
            text += "\n\nСладкое сразу меняет тон завтрака. Девочки отвечают мягче, чаще улыбаются и позволяют себе более ленивые, домашние позы за столом."
        return text

    def tavern_breakfast_apply_drink_perk(preferred_ids=None):
        global TavernBreakfastDrinkPerkDay, TavernBreakfastSpicyDrinkDay, TavernBreakfastAleTeamTalkDone

        item_key = ""
        for candidate in list(preferred_ids or ("energy_tea_001", "drink_ale_001", "libido_tincture_001")):
            if int(_player_item_count_by_id(candidate) or 0) > 0 and _player_remove_item_by_id(candidate, 1):
                item_key = candidate
                break
        if item_key == "":
            return "У вас нет подходящего напитка, чтобы сделать завтрак особенным."
        if item_key == "drink_ale_001":
            _player_add_item_by_id("empty_bottle_001", 1)
            _player_add_item_by_id("cork_001", 1)
        TavernBreakfastDrinkPerkDay = int(dayspassed or 0)
        if item_key == "libido_tincture_001":
            TavernBreakfastSpicyDrinkDay = int(dayspassed or 0)
        score = 3 if item_key == "libido_tincture_001" else 2
        targets = tavern_breakfast_record_group_perk(item_key, score)
        tavern_breakfast_apply_group_social(targets, 1, 1, 1 if item_key in ("drink_ale_001", "libido_tincture_001") else 0, 2)
        if item_key == "energy_tea_001":
            return "Вы делитесь бодрящим чаем со всеми, кто сейчас сидит за столом. Теплая кружка в руках делает утренний разговор ровнее, а девочки заметно легче принимают ваши замечания и распоряжения."
        if item_key == "drink_ale_001":
            if int(TavernBreakfastBlindPirateTeamPledge or 0) == 1 and int(TavernBreakfastMilkTeamTalkDone or 0) == 1 and int(TavernBreakfastAleTeamTalkDone or 0) == 0 and tavern_breakfast_blind_pirate_team_present():
                TavernBreakfastAleTeamTalkDone = 1
                return tavern_breakfast_blind_pirate_ale_text()
            return "Вы делитесь элем за завтраком, разливая его малыми кружками. Это не пьянка, но общий стол сразу становится свободнее: шутки идут смелее, взгляды держатся дольше."
        return "Вы делитесь за завтраком пряной настойкой. Она расходится по кружкам совсем понемногу, зато эффект виден быстро: голоса теплеют, щеки розовеют, а обычные фразы начинают звучать двусмысленно."

    def tavern_breakfast_apply_lewd_series_perk():
        global TavernBreakfastLewdSeriesDay

        if not tavern_breakfast_lewd_series_available():
            return "Пока у вас нет подходящей непристойной истории или серии, которую можно пустить за столом."
        TavernBreakfastLewdSeriesDay = int(dayspassed or 0)
        targets = tavern_breakfast_record_group_perk("lewd_series", 3)
        tavern_breakfast_apply_group_social(targets, 0, 1, 1, 1)
        lines = [
            "Вы как бы между делом подкидываете тему о новых непристойных рисунках и книжечках. Никто не признается, что слушает слишком внимательно, но завтрак сразу сбивается с обычной хозяйственной колеи.",
        ]
        if "sandra" in targets:
            lines.append("Сандра делает строгое лицо, но краснеет слишком быстро, чтобы это выглядело убедительно.")
        if "melissa" in targets:
            lines.append("Мелисса сперва прячет улыбку за кружкой, а потом сама задает вопрос, который звучит куда смелее, чем она рассчитывала.")
        if "amanda" in targets:
            lines.append("Аманда сразу начинает дразнить остальных, будто вся эта тема появилась за столом именно ради нее.")
        return "\n\n".join(lines)

    def tavern_breakfast_apply_appearance_perk():
        global TavernBreakfastAppearancePerkDay

        if not tavern_breakfast_appearance_perk_available():
            return "Сегодня за столом нет ни свежих обновок, ни недавних визитов к Серджио, за которые можно зацепить разговор."
        TavernBreakfastAppearancePerkDay = int(dayspassed or 0)
        targets = tavern_breakfast_record_group_perk("appearance", 2)
        tavern_breakfast_apply_group_social(targets, 1, 1, 0, 1)
        names = ", ".join([_action_display_name(npc_id) for npc_id in targets])
        return "Вы спокойно отмечаете, что %s за завтраком выглядят уже совсем по-домашнему: не как работницы перед хозяином, а как свои люди в доме, где можно выйти к столу без полной брони приличий.\n\nТакой тон им явно нравится. Комплимент не звучит приказом, но закрепляет новую меру доверия: обновки, визиты к Серджио и домашняя небрежность становятся частью общего утреннего порядка." % names

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

    def build_breakfast_text_pages(text="", min_paragraphs=1, max_paragraphs=2, page_limit=650):
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
            candidate_text = "\n\n".join(candidate_parts)
            if current_parts and (len(candidate_parts) > int(max_paragraphs or 2) or (len(candidate_text) > int(page_limit or 650) and len(current_parts) >= int(min_paragraphs or 1))):
                pages.append("\n\n".join(current_parts))
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
        if tavern_breakfast_can_offer_perk_menu():
            items.append(MenuItem("Поделиться едой и напитками", Jump("TavernKitchenBreakfastPerkMenu")))
        for look_girl in tavern_breakfast_core_present_ids():
            items.append(MenuItem("Посмотреть на %s за завтраком" % _action_display_name(look_girl), Call("TavernKitchenBreakfastLookAtGirl", look_girl)))
        if tavern_breakfast_amanda_attic_mock_ready():
            items.append(MenuItem("Ответить Аманде про чердак", Jump("TavernKitchenBreakfastAmandaAtticMock")))
        if tavern_breakfast_melissa_amanda_gerhard_ready():
            items.append(MenuItem("Разобрать спор Мелиссы и Аманды", Jump("TavernKitchenBreakfastMelissaAmandaGerhard")))
        if tavern_breakfast_tease_ready():
            items.append(MenuItem("Заметить провокацию за столом", Jump("TavernKitchenBreakfastTease")))
        if bool(globals().get("AmandaAIIntegrationEnabled", False)) and "amanda_ai_breakfast_intent_code" in globals():
            amanda_intent = amanda_ai_breakfast_intent_code()
            if amanda_intent:
                items.append(MenuItem(amanda_ai_menu_label(amanda_intent), Call("AmandaAIIntentBreakfastEvent", amanda_intent)))
        soap_request_girl = tavern_breakfast_soap_request_girl()
        if soap_request_girl:
            items.append(MenuItem("Выслушать просьбу о мыле", Call("HouseholdSoapRequestEvent", soap_request_girl)))
        dress_request_girl = tavern_breakfast_dress_request_girl()
        if dress_request_girl == "sandra":
            items.append(MenuItem("Поговорить с Сандрой о новом платье", Call("SandraDressInitiativeEvent")))
        elif dress_request_girl == "melissa":
            items.append(MenuItem("Поговорить с Мелиссой о новом платье", Call("MelissaDressRequestEvent")))
        elif dress_request_girl == "amanda":
            items.append(MenuItem("Поговорить с Амандой о новом платье", Call("AmandaDressRequestEvent")))
        if household_barber_request_ready("sandra", "breakfast"):
            items.append(MenuItem("Предложить Сандре сходить к Серджио", Call("HouseholdBarberRequestEvent", "sandra")))
        if household_barber_request_ready("melissa", "breakfast"):
            items.append(MenuItem("Предложить Мелиссе сходить к Серджио", Call("HouseholdBarberRequestEvent", "melissa")))
        if household_barber_request_ready("amanda", "breakfast"):
            items.append(MenuItem("Предложить Аманде сходить к Серджио", Call("HouseholdBarberRequestEvent", "amanda")))
        if int(TavernBreakfastGeorgetteLizaPending or 0) == 1:
            items.append(MenuItem("Объявить о Жоржетте и Лизетте", Jump("TavernKitchenBreakfastAnnounceGeorgetteLiza")))
        issue_girl = tavern_breakfast_morning_issue_girl()
        if str(issue_girl or "").strip():
            items.append(MenuItem("Проверить, почему %s не вышла к завтраку" % _action_display_name(issue_girl), Jump("TavernKitchenBreakfastMorningIssue")))
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
        global MainTxt, CurLocDesc, UI_mode, UI_selected_char
        global current_girl_key, current_object_id, action_menu_specs
        global current_action_title, current_action_content, current_action_items
        text_value = str(panel_text or TavernKitchenSavedText or TavernBreakfastBaseText or MainTxt or "Вы все еще сидите за общим утренним столом.")
        MainTxt = text_value
        CurLocDesc = text_value
        UI_mode = "scene"
        UI_selected_char = ""
        current_girl_key = ""
        current_object_id = ""
        action_menu_specs = []
        current_action_title = "Завтрак"
        current_action_content = None
        current_action_items = list(tavern_breakfast_menu_items() or [])
        try:
            renpy.restart_interaction()
        except Exception:
            pass
        return text_value

    def tavern_breakfast_has_listen_topic():
        return (
            story_event_available("TavernKitchen", "enter")
            or tavern_breakfast_amanda_alt_cure_possible()
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
        global fun
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
        fun = _player_clamp(int(fun or 0) + 2, 0, 100)
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
        rows = []
        for npc_id in ("sandra", "melissa", "amanda"):
            if household_morning_issue_type(npc_id) in ("sick", "sleepy"):
                continue
            rows.append(npc_id)
        if str(getLocation("becky") or "") in ("TavernKitchen", "TavernMain"):
            rows.append("becky")
        return rows

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
        global TavernBreakfastDanceSponsorAnnouncedDay

        lines = []
        present_ids = tavern_breakfast_present_ids()
        lines.extend(list(tavern_breakfast_relaxed_appearance_lines() or []))

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
        if int(DanceSponsor or 0) == 1 and int(TavernBreakfastDanceSponsorAnnouncedDay or -1) != int(dayspassed or 0):
            TavernBreakfastDanceSponsorAnnouncedDay = int(dayspassed or 0)
            lines.append("За завтраком вы объявляете, что трактир уже выставит вино и закуски к пятничным танцам. Сандра довольно кивает: такой взнос сразу делает дом заметнее в городе, а девки начинают переглядываться куда живее обычного.")
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
        return int(BeckyKitchenVisitActive or 0) == 1 and str(getLocation("sandra") or "") == "TavernKitchen" and int(_player_item_count_by_id("energy_tea_001") or 0) > 0

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
        return str(getLocation("sandra") or "") == "TavernKitchen" and tavern_kitchen_food_stock_count() > 0 and int(Friends.get("sandra", 0) or 0) >= 5 and int(AskedToday.get("sandra", 0) or 0) == 0

    def tavern_kitchen_sandra_can_discuss_clients():
        return str(getLocation("sandra") or "") == "TavernKitchen" and tavern_kitchen_food_stock_count() > 0 and int(Friends.get("sandra", 0) or 0) >= 5 and int(AskedToday.get("sandra", 0) or 0) == 0

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
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={"object_menu_label": "TavernKitchenObjectMenu"},
    )

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

        text_parts.append(werecat_visible_text("TavernKitchen"))

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
    call RoomEnterEventGate(CurLoc, False)
    $ current_object_id = ""
    $ current_girl_key = ""
    if TavernBreakfastEventActive:
        if str(TavernKitchenSavedText or "").strip():
            $ MainTxt = str(TavernKitchenSavedText or "")
        else:
            $ MainTxt = "Вы все еще сидите за общим утренним столом."
        $ CurLocDesc = MainTxt
        hide screen main_ui
        jump TavernKitchenBreakfastMenu
    if bool(AmandaAIIntegrationEnabled):
        call AmandaMiniEventTry(CurLoc, "room")
    $ BeckyKitchenVisitActive = 1 if becky_kitchen_visit_active() else 0
    if BeckyKitchenVisitActive:
        $ BeckyVar["SandraKitchenVisitMonth"] = int(month or 0)

    $ _kitchen_wine_event_text = ""
    $ _kitchen_pending_event = tavern_kitchen_pending_mandatory_event_code()
    if str(_kitchen_pending_event or "") == "WineForDance" and not tavern_breakfast_available():
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
        if str(CurEventCode or "") != "WineForDance" or len(list(current_action_items or [])) <= 0:
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
    $ _kitchen_ui_return = None
    while _kitchen_ui_return is None:
        call screen main_ui
        $ _kitchen_ui_return = _return
    jump TavernKitchen


label TavernKitchenBuildActions:
    if TavernBreakfastEventActive:
        return
    $ tavern_kitchen_hearth_wood_stock()
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
    if werecat_is_in_room("TavernKitchen"):
        $ current_action_items.append(MenuItem(werecat_action_caption("TavernKitchen"), Call("IntWerecatTalk", "TavernKitchen")))
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
    $ TavernBreakfastPresentIds = list(household_breakfast_attendee_ids() or [])
    $ BreakfastToday = True
    $ TavernBreakfastLastDay = int(dayspassed or 0)
    $ TavernBreakfastDay = int(dayspassed or 0)
    $ TavernBreakfastEventActive = True
    $ _breakfast_morning_sick_girl = str(tavern_breakfast_morning_sickness_girl() or "")
    $ calendar_advance_minutes(30)
    vscene tavern_kitchen_breakfast_picture()
    if bool(AmandaAIIntegrationEnabled):
        call AmandaMiniEventTry("TavernKitchen", "breakfast")
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
            or tavern_breakfast_can_offer_perk_menu()
            or len(tavern_breakfast_core_present_ids()) > 0
            or tavern_breakfast_amanda_attic_mock_ready()
            or tavern_breakfast_melissa_amanda_gerhard_ready()
            or tavern_breakfast_tease_ready()
            or (
                bool(globals().get("AmandaAIIntegrationEnabled", False))
                and "amanda_ai_breakfast_intent_code" in globals()
                and str(amanda_ai_breakfast_intent_code() or "").strip() != ""
            )
            or str(tavern_breakfast_soap_request_girl() or "").strip() != ""
            or str(tavern_breakfast_dress_request_girl() or "").strip() != ""
            or household_barber_request_ready("sandra", "breakfast")
            or household_barber_request_ready("melissa", "breakfast")
            or household_barber_request_ready("amanda", "breakfast")
            or int(TavernBreakfastGeorgetteLizaPending or 0) == 1
            or str(_breakfast_morning_sick_girl or "").strip() != ""
            or str(tavern_breakfast_morning_issue_girl() or "").strip() != ""
            or str(tavern_breakfast_absent_prompt() or "").strip() != ""
            or ("sandra" in list(tavern_breakfast_present_ids() or []) and tavern_kitchen_sandra_can_discuss_breakfasts())
            or ("sandra" in list(tavern_breakfast_present_ids() or []) and tavern_kitchen_sandra_can_discuss_clients())
            or tavern_breakfast_can_offer_dance_sponsorship()
        ):
            _breakfast_lines.append("За столом уже чувствуется, что утро может вытянуть за собой и разговор, и новости, и чьи-нибудь старые счеты.")
        else:
            _breakfast_lines.append("Ничего особенного за столом пока не происходит: обычное домашнее утро без лишней суеты.")
        MainTxt = "\n\n".join([row for row in _breakfast_lines if str(row or "").strip()])
        CurLocDesc = MainTxt
    if int(DanceSponsor or 0) == 1 and int(TavernBreakfastDanceSponsorAnnouncedDay or -1) != int(dayspassed or 0):
        $ TavernBreakfastDanceSponsorAnnouncedDay = int(dayspassed or 0)
    $ _eat_result = player_eat_meal("утреннюю кашу и свежий хлеб", 16)
    if str(_eat_result.get("text", "") or "").strip():
        $ MainTxt = str(MainTxt or "") + "\n\n" + str(_eat_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
    $ _breakfast_social_ids = tavern_breakfast_apply_social_bonus()
    if len(list(_breakfast_social_ids or [])) > 0:
        $ MainTxt = str(MainTxt or "") + "\n\nСовместный завтрак заметно сближает вас с теми, кто сидит с вами за столом."
        $ CurLocDesc = MainTxt
    if tavern_breakfast_can_give_first_soap_samples():
        $ _soap_intro_text = tavern_breakfast_apply_first_soap_samples()
        if str(_soap_intro_text or "").strip():
            $ MainTxt = str(MainTxt or "") + "\n\n" + str(_soap_intro_text or "")
            $ CurLocDesc = MainTxt
    elif soap_available_piece_count() > 0 and int(TavernBreakfastSoapAnnouncedDay or -1) != int(dayspassed or 0):
        $ TavernBreakfastSoapAnnouncedDay = int(dayspassed or 0)
        $ fun = _player_clamp(int(fun or 0) + 3, 0, 100)
    if len(list(tavern_recent_barber_ids() or [])) > 0:
        $ TavernBreakfastBarberTalkDay = int(dayspassed or 0)
    $ TavernBreakfastBaseText = str(MainTxt or "")
    $ TavernBreakfastBaseShownDay = -1
    $ TavernKitchenSavedText = str(MainTxt or "")
    call stat
    if _breakfast_morning_sick_girl != "":
        hide screen main_ui
        call CheckDailyEvent(_breakfast_morning_sick_girl, "MorningSickness", "TavernKitchen", 0)
    hide screen main_ui
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastMenu:
    if not TavernBreakfastEventActive:
        show screen main_ui
        call TavernKitchenBuildActions
        return
    $ tavern_breakfast_restore_ui_state()
    if int(TavernBreakfastBaseShownDay or -1) != int(dayspassed or 0):
        $ TavernBreakfastBaseShownDay = int(dayspassed or 0)
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
    $ TavernKitchenSavedText = MainTxt
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
    if tavern_breakfast_amanda_alt_cure_ready():
        call TavernKitchenBreakfastAmandaAltCure1
        return
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


label TavernKitchenBreakfastAmandaAltCure1:
    $ AmandaVar["attic_window_breakfast_bj_day"] = int(dayspassed or 0)
    $ Arousal["You"] = max(35, int(Arousal.get("You", 0) or 0))
    $ Arousal["amanda"] = max(30, int(Arousal.get("amanda", 0) or 0))
    $ MainTxt = "За общим столом Аманда сегодня на редкость притихла. Несколько раз она украдкой встречается с вами взглядом, потом криво улыбается и будто невзначай касается вашей ноги под столом. Колкость про Мелиссу так и не срывается с ее языка.\n\nЧерез пару минут ее ступня уже гладит вас куда смелее, а сама она наклоняется ближе и почти беззвучно шепчет, что после той неловкой истории с окном ей почему-то самой теперь труднее делать вид, будто ничего такого в доме не бывает.\n\nПока остальные заняты едой и разговорами, Аманда незаметно скользит ниже под край стола и решает загладить свою дерзость способом куда приятнее обычных извинений."
    $ CurLocDesc = MainTxt
    call IntAmandaSex("amanda", "home", "minet")
    $ MainTxt = "Когда все заканчивается, Аманда так же тихо возвращается на свое место, поправляет волосы и берется за ложку так невинно, будто под столом только что не происходило ничего предосудительного. На вас она смотрит уже без прежней насмешки: скорее с довольным сговором, чем с привычным желанием поддеть."
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastAmandaAtticMock:
    if not tavern_breakfast_amanda_attic_mock_ready():
        jump TavernKitchenBreakfastMenu
    $ AmandaVar["attic_mock_response_day"] = int(dayspassed or 0)
    $ MainTxt = "Стоит за завтраком снова всплыть слову \"чердак\", Аманда тут же цепляет вас взглядом и слишком невинно спрашивает, не собираетесь ли вы опять падать туда, куда приличные люди хотя бы стучатся."
    $ CurLocDesc = MainTxt
    $ _attic_items = [
        MenuItem("Рассказать всем, что вы видели у окна Аманды", Jump("TavernKitchenBreakfastAmandaAtticExpose")),
        MenuItem("Тихо велеть ей прекратить насмешки", Jump("TavernKitchenBreakfastAmandaAtticStop")),
        MenuItem("Не развивать тему", Jump("TavernKitchenBreakfastMenu")),
    ]
    call QueuePagedPanelText(MainTxt, "Ваш ответ", _attic_items, "plain")
    call ReturnToMainUI
    return


label TavernKitchenBreakfastAmandaAtticExpose:
    $ AmandaVar["attic_mock_exposed"] = 1
    $ AmandaVar["attic_mock_stopped"] = 1
    $ sluttiness["amanda"] = min(100, int(sluttiness.get("amanda", 0) or 0) + 1)
    $ otkroven["amanda"] = min(20, int(otkroven.get("amanda", 0) or 0) + 1)
    $ MainTxt = "Вы спокойно отвечаете, что если Аманда так любит шутить про чердак, можно сразу рассказать всем, откуда она сама высматривала тот же двор. За столом становится тише. Аманда краснеет, дергает плечом и больше к этой теме за завтраком не возвращается."
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastMelissaAmandaGerhard:
    if not tavern_breakfast_melissa_amanda_gerhard_ready():
        jump TavernKitchenBreakfastMenu
    $ MainTxt = "Сладкая добавка к утренней еде делает разговор заметно мягче и одновременно опаснее. Сандры за столом нет, и Мелисса, сперва будто бы говоря о комнате, вдруг косится на Аманду.\n\n\"Некоторым, похоже, и шуршания под крышей не нужны, чтобы по ночам не спать,\" замечает она слишком невинно. \"У Аманды в комнате иногда тоже такое возится, будто кто-то сам себе мешает уснуть.\"\n\nАманда тут же вскидывает брови и улыбается так же сладко: \"О! А ты, дорогая, значит, точно знаешь, что это за звуки? Сама тоже так делаешь?\""
    $ CurLocDesc = MainTxt
    $ _melissa_amanda_items = [
        MenuItem("Сказать, что это естественно", Jump("TavernKitchenBreakfastMelissaAmandaGerhardNatural")),
        MenuItem("Не лезть в девичью перепалку", Jump("TavernKitchenBreakfastMenu")),
    ]
    call QueuePagedPanelText(MainTxt, "Спор за завтраком", _melissa_amanda_items, "plain")
    call ReturnToMainUI
    return


label TavernKitchenBreakfastMelissaAmandaGerhardNatural:
    if not tavern_breakfast_melissa_amanda_gerhard_ready():
        jump TavernKitchenBreakfastMenu
    $ TavernBreakfastMelissaAmandaGerhardDay = int(dayspassed or 0)
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
    $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    $ otkroven["melissa"] = min(20, int(otkroven.get("melissa", 0) or 0) + 1)
    $ otkroven["amanda"] = min(20, int(otkroven.get("amanda", 0) or 0) + 1)
    $ MainTxt = "Вы спокойно обрываете перепалку и говорите, что в этом нет ни ведьмовства, ни особой тайны: почти все так делают, просто не все любят, когда их ловят на звуках и намеках.\n\nАманда победно смотрит на Мелиссу: \"Слышала? Все делают. Значит, нечего строить из себя святую кошку у чужой кровати.\" Мелисса краснеет, но не отступает: \"Я не об этом говорила. Если в твоей комнате теперь ночую я, мне тоже надо понимать, что там происходит.\"\n\nСпор быстро возвращается к настоящей причине: Мелиссе все еще некуда нормально спать, чердак над ее комнатой все еще испорчен, а после истории с падением и окном никто уже не может делать вид, будто вопрос решится сам собой.\n\nНа шум в кухню наконец заглядывает Сандра. Аманда и Мелисса наперебой пересказывают ей вашу фразу про то, что все это естественно, и Сандра краснеет так густо, будто ее застали за чем-то куда хуже обычного разговора. Но от темы она не уходит.\n\n\"Ладно,\" выдавливает она, глядя мимо всех сразу. \"Про такое с девками тоже надо говорить прямо, раз уж дом у нас дошел до таких разговоров. И с братом Герхардом насчет комнаты Мелиссы я тоже поговорю. Только без ваших ухмылок, поняли?\""
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastAmandaAtticStop:
    $ AmandaVar["attic_mock_stopped"] = 1
    $ Friends["amanda"] = min(20, int(Friends.get("amanda", 0) or 0) + 1)
    $ MainTxt = "Вы наклоняетесь ближе и коротко говорите Аманде, что эту шутку пора оставить при себе. Она еще секунду держит дерзкий вид, потом опускает глаза к тарелке и тихо фыркает: \"Ладно. Поняла.\" После этого тема чердака за столом глохнет сама собой."
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastTease:
    $ _tease_data = tavern_breakfast_tease_candidate()
    $ _tease_girl = str(_tease_data.get("girl", "") or "")
    $ _tease_tier = int(_tease_data.get("tier", 0) or 0)
    if _tease_girl == "":
        jump TavernKitchenBreakfastMenu
    if _tease_girl == "amanda":
        $ AmandaVar["breakfast_tease_day"] = int(dayspassed or 0)
    else:
        $ MelissaVar["breakfast_tease_day"] = int(dayspassed or 0)
    if _tease_tier >= 4:
        $ MainTxt = "{} приходит к завтраку настолько по-домашнему небрежной, что это уже похоже не на случайность, а на проверку ваших границ. Ночная ткань или плохо запахнутый домашний наряд оставляют слишком много поводов для взгляда, и она прекрасно видит, что вы это заметили.".format(RealName.get(_tease_girl, _tease_girl))
        if int(ClaraVar.get("booklet_market_seen", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1:
            $ MainTxt = str(MainTxt or "") + "\n\nПосле историй о Клариссиных листках эта поза читается еще прямее: как будто кто-то нарочно примеряет на себя одну из тех непристойных сцен, только делает вид, что речь всего лишь о завтраке."
    elif _tease_tier >= 3:
        $ MainTxt = "{} ловит ваш взгляд, чуть меняет позу за столом и дает понять, что сегодня под платьем у нее куда меньше защиты, чем принято показывать за завтраком. Это длится всего миг, но она явно рассчитывала, что вы заметите.".format(RealName.get(_tease_girl, _tease_girl))
    elif _tease_tier >= 2:
        $ MainTxt = "{} будто случайно садится смелее обычного: колено уходит в сторону, юбка натягивается, и вся поза становится скорее вызовом, чем неловкостью.".format(RealName.get(_tease_girl, _tease_girl))
    else:
        $ MainTxt = "{} незаметно приподнимает край юбки ровно настолько, чтобы вы успели заметить белье, а потом с невинным видом возвращается к завтраку.".format(RealName.get(_tease_girl, _tease_girl))
    $ Arousal["You"] = max(0, min(100, int(Arousal.get("You", 0) or 0) + 5 + _tease_tier))
    $ Arousal[_tease_girl] = max(0, min(100, int(Arousal.get(_tease_girl, 0) or 0) + 3 + _tease_tier))
    $ sluttiness[_tease_girl] = min(100, int(sluttiness.get(_tease_girl, 0) or 0) + 1)
    $ CurLocDesc = MainTxt
    call stat
    if int(HadSex.get(_tease_girl, 0) or 0) > 0 or (_tease_girl == "amanda" and (int(AmandaVar.get("suckyou", 0) or 0) == 1 or int(AmandaVar.get("fuckyou", 0) or 0) == 1)) or (_tease_girl == "melissa" and int(MelissaVar.get("sex_engine_unlocked", 0) or 0) == 1):
        $ _tease_items = [
            MenuItem("Намекнуть на склад после завтрака", Call("TavernKitchenBreakfastTeasePrivate", _tease_girl, "storage")),
            MenuItem("Намекнуть на сарай после завтрака", Call("TavernKitchenBreakfastTeasePrivate", _tease_girl, "shed")),
            MenuItem("Сделать вид, что ничего не заметили", Jump("TavernKitchenBreakfastMenu")),
        ]
        call QueuePagedPanelText(MainTxt, "Провокация", _tease_items, "plain")
        call ReturnToMainUI
        return
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastTeasePrivate(girl_name="", place_code="storage"):
    $ _tease_private_girl = str(girl_name or "").strip().lower()
    $ _tease_private_place = "склад" if str(place_code or "") == "storage" else "сарай"
    $ Friends[_tease_private_girl] = min(20, int(Friends.get(_tease_private_girl, 0) or 0) + 1)
    $ otkroven[_tease_private_girl] = min(20, int(otkroven.get(_tease_private_girl, 0) or 0) + 1)
    $ MainTxt = "{} понимает ваш намек про {} без лишних объяснений. Пока за столом еще шумят ложками и спорят о работе, она только коротко улыбается: этот разговор явно можно будет продолжить там, где никто не станет мешать.".format(RealName.get(_tease_private_girl, _tease_private_girl), _tease_private_place)
    $ CurLocDesc = MainTxt
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


label TavernKitchenBreakfastMorningIssue:
    $ _breakfast_issue_girl = str(tavern_breakfast_morning_issue_girl() or "").strip()
    if str(_breakfast_issue_girl or "") == "":
        jump TavernKitchenBreakfastMenu
    $ MainTxt = tavern_breakfast_morning_issue_text(_breakfast_issue_girl)
    $ CurLocDesc = MainTxt
    $ current_action_title = "Утреннее отсутствие"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _issue_action in list(household_room_issue_action_specs(_breakfast_issue_girl) or []):
            current_action_items.append(MenuItem(str(_issue_action.get("label", "") or ""), Call(str(_issue_action.get("target", "") or ""), *tuple(_issue_action.get("args", ()) or ()))))
        current_action_items.append(MenuItem("Оставить это до конца завтрака", Jump("TavernKitchenBreakfastMenu")))
    call QueuePagedPanelText(MainTxt, current_action_title, list(current_action_items or []), "plain")
    call ReturnToMainUI
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


label TavernKitchenBreakfastPerkMenu:
    if not tavern_breakfast_can_offer_perk_menu():
        jump TavernKitchenBreakfastMenu
    $ _perk_text = "Вы решаете, чем именно поделиться за общим столом, чтобы завтрак был не просто обязательной кашей, а живым домашним утром."
    $ tavern_breakfast_restore_ui_state(_perk_text)
    $ _perk_items = list(tavern_breakfast_perk_menu_items() or [])
    call QueuePagedPanelText(_perk_text, "Общий стол", _perk_items, "plain")
    call ReturnToMainUI
    return


label TavernKitchenBreakfastLookAtGirl(girl_name=""):
    $ _breakfast_look_girl = str(girl_name or "").strip().lower()
    if _breakfast_look_girl not in list(tavern_breakfast_present_ids() or []):
        jump TavernKitchenBreakfastMenu
    $ _breakfast_look_picture = tavern_breakfast_look_picture(_breakfast_look_girl)
    if str(_breakfast_look_picture or "").strip():
        vscene _breakfast_look_picture
    $ MainTxt = tavern_breakfast_look_text(_breakfast_look_girl)
    $ CurLocDesc = MainTxt
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastPerkFood(item_id=""):
    $ _breakfast_food_choice = [str(item_id or "").strip()] if str(item_id or "").strip() else None
    $ MainTxt = tavern_breakfast_apply_food_perk(_breakfast_food_choice)
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastPerkDrink(item_id=""):
    $ _breakfast_drink_choice = [str(item_id or "").strip()] if str(item_id or "").strip() else None
    $ MainTxt = tavern_breakfast_apply_drink_perk(_breakfast_drink_choice)
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastPerkLewdSeries:
    $ MainTxt = tavern_breakfast_apply_lewd_series_perk()
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastPerkAppearance:
    $ MainTxt = tavern_breakfast_apply_appearance_perk()
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
    $ TavernBreakfastBlindPirateTeamPledge = 1
    $ AmandaVar["barber_request_interest"] = 1
    $ AmandaVar["beauty_help_terms_accepted"] = 1
    $ AmandaVar["beauty_help_approved_day"] = int(dayspassed or 0)
    $ MainTxt = tavern_breakfast_blind_pirate_story_text()
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
    $ TavernBreakfastPresentIds = None
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
    if str(getLocation("sandra") or "") == "TavernKitchen":
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
        if str(getLocation("sandra") or "") == "TavernKitchen":
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
            _kitchen_label = str(_kitchen_action.label or "")
            if str(getattr(_kitchen_action, "action_id", "") or "") == "make_fire" and _pc_fire_is_active(TavernKitchenHearthObject):
                _kitchen_label = "Подложить дрова"
            if _kitchen_action.hook == "text":
                current_action_items.append(MenuItem(_kitchen_label, Call("TavernKitchenObjectText", object_id, _kitchen_action.action_id)))
            elif _kitchen_action.hook == "call" and str(_kitchen_action.target or "") != "":
                current_action_items.append(MenuItem(_kitchen_label, Call(_kitchen_action.target, *_kitchen_args)))
            elif _kitchen_action.hook == "jump" and str(_kitchen_action.target or "") != "":
                current_action_items.append(MenuItem(_kitchen_label, Jump(_kitchen_action.target)))
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
