# ================================================================================
# Breakfast and Sunday meal flow for TavernKitchen.
# Room entry, objects, navigation, and ordinary kitchen NPC actions stay in TavernKitchen.rpy.
# ================================================================================

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

init python:
    import random
    import re
    import renpy.exports as renpy

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

    def becky_kitchen_visit_active():
        if int(Becky.var.get("SandraKitchenVisitMonth", 0) or 0) == int(month or 0):
            return False
        if int(Becky.var.get("visitedhome", 0) or 0) < 2:
            return False
        if str(getLocation("sandra") or "") != "TavernKitchen":
            return False
        return int(hour or 0) >= 12 and int(hour or 0) < 18

    def tavern_breakfast_present_ids():
        present = []
        if bool(TavernBreakfastEventActive) and TavernBreakfastPresentIds is not None:
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
        if int(Amanda.var.get("attic_window_breakfast_bj_day", -1) or -1) == int(dayspassed or 0):
            return False
        wetness = max(int(Amanda.stats.get("PussyWetStart", 0) or 0), int(Amanda.arousal_value() or 0))
        return wetness >= 25 or int(Amanda.corruption or 0) >= 28

    def tavern_breakfast_amanda_alt_cure_ready():
        if not tavern_breakfast_amanda_alt_cure_possible():
            return False
        wetness = max(int(Amanda.stats.get("PussyWetStart", 0) or 0), int(Amanda.arousal_value() or 0))
        sluttiness_value = int(Amanda.corruption or 0)
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
            and int(Amanda.var.get("attic_mock_stopped", 0) or 0) == 0
            and int(Amanda.var.get("attic_mock_exposed", 0) or 0) == 0
            and int(Amanda.var.get("attic_mock_response_day", -1) or -1) != int(dayspassed or 0)
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
            (int(Melissa.bats_stage() or 0) >= 3 or int(werecat_state().get("rats_problem_active", 0) or 0) == 1)
            and int(Melissa.bats_stage() or 0) < 8
            and "melissa" in present_ids
            and "amanda" in present_ids
            and "sandra" in present_ids
            and int(TavernBreakfastMelissaAmandaGerhardDay or -1) != int(dayspassed or 0)
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
            info = getPersonInfo(npc_id)
            state = Amanda.var if npc_id == "amanda" else Melissa.var
            if int(state.get("breakfast_tease_day", -1) or -1) == int(dayspassed or 0):
                continue
            friend_value = int(getattr(info, "rel", 0) or 0)
            open_value = int(getattr(info, "openness", 0) or 0)
            corruption_value = int(getattr(info, "corruption", 0) or 0)
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
        info = getPersonInfo(key)
        score = 0
        score += min(4, max(0, int(getattr(info, "rel", 0) or 0) // 4))
        score += min(3, max(0, int(getattr(info, "openness", 0) or 0) // 5))
        score += min(3, max(0, int(getattr(info, "corruption", 0) or 0) // 20))
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
        if int(Clara.var.get("booklet_market_seen", 0) or 0) == 1 or int(Clara.var.get("drawings_secret_known", 0) or 0) == 1:
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
        if int(Clara.var.get("booklet_market_seen", 0) or 0) == 1 or int(Clara.var.get("drawings_secret_known", 0) or 0) == 1:
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
            "melissa": Melissa.image_sequence("kitchen", "breakfast"),
            "amanda": [
                "images/breakfast/amanda_breakfast/amanda_tease_1.jpg",
                "images/breakfast/amanda_breakfast/amanda_tease.jpg",
                "images/breakfast/amanda_b.png",
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
            return "Вы присматриваетесь к Мелиссе за завтраком. Она сидит ровно, ест аккуратно, но под глазами у нее усталость: ночные шорохи, крысы и летучие мыши сделали ее злой еще до первой ложки."
        if key == "amanda":
            return "Вы смотрите, как Аманда ведет себя за завтраком. Она играет ложкой, чуть наглее обычного садится за столом и ловит чужие взгляды, будто проверяет, кто первым полезет с замечанием."
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
        rows = list(targets or tavern_breakfast_core_present_ids() or [])
        for npc_id in rows:
            info = getPersonInfo(npc_id)
            if info is not None:
                info.change_social(friend_delta=friend_delta, open_delta=open_delta, corruption_delta=corruption_delta)
        if int(fun_delta or 0) != 0:
            player.change_stat("fun", int(fun_delta or 0))
        return rows

    def tavern_breakfast_take_perk_item(preferred_ids=None):
        preferred = list(preferred_ids or [])
        if len(preferred) <= 0:
            return ""
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
        return int(Clara.var.get("booklet_market_seen", 0) or 0) == 1 or int(Clara.var.get("drawings_secret_known", 0) or 0) == 1

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
            return "Вы садитесь за кухонный стол. Сандра ставит кашу, хлеб и горячую кружку без всяких церемоний: ешь, пока теплое, потом всем по делам."
        if len(present_ids) > 0:
            return "Сандра к столу не вышла, и завтрак выходит кривоватый: хлеб, вчерашняя каша и что-то горячее из котла, лишь бы брюхо не урчало."
        return "Сандра к столу не вышла, так что вы сами шарите по кухне и перебиваетесь тем, что попалось под руку."

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
        global SoapRequestQueue

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
            info = getPersonInfo(npc_id)
            if info is not None:
                info.change_social(friend_delta=1)
        HouseholdSoapSampleIntroDone = 1
        TavernBreakfastSoapAnnouncedDay = int(dayspassed or 0)
        player.change_stat("fun", 3)
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
            info = getPersonInfo(npc_id)
            if info is not None:
                open_delta = 1 if npc_id in ("sandra", "melissa", "amanda", "becky") else 0
                corruption_delta = 1 if npc_id in ("sandra", "melissa", "amanda") else 0
                info.change_social(friend_delta=1, open_delta=open_delta, corruption_delta=corruption_delta)
        player.change_stat("fun", 2)
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
        candidates = [
            "images/tavern/kitchen/kitchen_breakfast.jpg",
            "images/kitchen/kitchen_breakfast.jpg",
            "images/breakfast/tavent_girls.jpg",
            "images/breakfast/amanda_b.png",
        ]
        for candidate in candidates:
            if renpy.loadable(candidate):
                return candidate
        return tavern_kitchen_event_picture("kitchen_breakfast")

    def tavern_breakfast_tease_picture(girl_name="", tier=0):
        key = str(girl_name or "").strip().lower()
        if key == "amanda":
            candidates = [
                "images/breakfast/amanda_breakfast/amanda_tease_5.jpg",
                "images/breakfast/amanda_breakfast/amanda_tease_4.jpg",
                "images/breakfast/amanda_breakfast/amanda_tease_3.jpg",
                "images/breakfast/amanda_breakfast/amanda_tease_2.jpg",
                "images/breakfast/amanda_breakfast/amanda_tease_1.jpg",
                "images/breakfast/amanda_breakfast/amanda_tease.jpg",
            ]
        elif key == "melissa":
            candidates = [
                "images/breakfast/melissa_breakfast/melissa breakfast_2.jpg",
                "images/breakfast/melissa_breakfast/melissa breakfast.jpg",
                "images/breakfast/melissa_breakfast/melissa_breakfast_1.jpg",
                "images/breakfast/melissa_breakfast/melissa_breakfast.jpg",
            ]
        else:
            candidates = [
                "images/breakfast/tavern_girls_impregnat.jpg",
                "images/breakfast/tavern_girls_impregnat_1.jpg",
                "images/breakfast/tavent_girls.jpg",
            ]
        for candidate in candidates:
            if renpy.loadable(candidate):
                return candidate
        return tavern_kitchen_breakfast_picture()

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
        rat_problem = int(werecat_state().get("rats_problem_active", 0) or 0) == 1 or int(CurDay.get("rat_food_loss", 0) or 0) > 0
        bats_stage = int(Melissa.bats_stage() or 0)

        if "sandra" in present_ids:
            lines.append("Сандра ставит миски так, будто гвозди забивает. \"Жуйте быстрее. Крысы сами из кладовой не уйдут, пол сам себя не вымоет, а гости с пустыми кружками ждать не любят.\"")
            lines.append("Она ворчит, что трактир держится не на красивых речах, а на том, кто утром поднял задницу раньше прочих.")
            if rat_problem:
                lines.append("\"И еще раз говорю: у нас крысиная беда,\" бросает Сандра. \"Если эти твари опять доберутся до мешков, я кому-нибудь этой кашей прямо в уши налью.\"")
        if "melissa" in present_ids:
            lines.append("Мелисса ест аккуратно, но язык у нее сегодня острый: успевает буркнуть и про пол, и про грязные кружки, и про то, кто опять ночью топал по коридору.")
            if bats_stage < 8:
                if bats_stage >= 4:
                    lines.append("Мелисса трет глаза и зло тычет ложкой в кашу. \"Опять всю ночь под крышей шуршало. То крысы внизу, то летучие мыши наверху. У нас дом или проклятый курятник?\"")
                elif bats_stage >= 3:
                    lines.append("Мелисса жалуется, что ночью над ее комнатой снова возились под балками, а из щелей тянуло сыростью. По виду ясно: спала она мало и ругаться готова с первого слова.")
                else:
                    lines.append("Мелисса мрачно говорит, что под потолком шуршало до рассвета. \"Если это мыши, пусть подавятся. Если летучие мыши, пусть провалятся в ад.\"")
                if "sandra" in present_ids:
                    lines.append("Сандра коротко отвечает, что с чердаком надо кончать: сначала выгнать крылатую дрянь, потом заделать щели, а не чесать языком за кашей.")
            if int(Melissa.var.get("bats_episode", 0) or 0) >= 6 and "amanda" in present_ids:
                lines.append("Стоит за столом всплыть слову \"чердак\", как Аманда многозначительно тянет: \"Главное, Стефан, теперь не падать сверху в чужие комнаты без стука.\" Мелисса тут же фыркает, но уголки ее губ все равно дрожат.")
        if "amanda" in present_ids:
            lines.append("Аманда ест быстро, но все равно успевает строить рожи и цеплять всех подряд, будто завтрак без подколок ей в горло не лезет.")
            lines.append("\"Крысы?\" Аманда пожимает плечом. \"Нужна кошечка. Только не простая. Есть одна такая, благородная, коготки чистые, носик вверх... Может, Клариссу в кладовую запереть?\"")
            if rat_problem and "sandra" in present_ids:
                lines.append("Сандра смотрит на нее так, что Аманда сразу утыкается в миску. \"Еще раз про чужих кошечек за столом мяукнешь, сама полезешь к крысам с веником.\"")
        if "sandra" in present_ids and "melissa" in present_ids and "amanda" in present_ids and (rat_problem or bats_stage >= 3):
            lines.append("Когда разговор снова съезжает на ночные шорохи и девичьи комнаты, Аманда хихикает слишком грязно, а Мелисса краснеет не вовремя. Сандра хлопает ладонью по столу: \"Пальцы из кисок вынули обе. Самоуспокоение закончится тем, что брат Герхард устроит вам дьявольское покаяние, а этого в доме никто не хочет.\"")
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
            info = getPersonInfo(npc_id)
            if info is not None:
                info.change_social(friend_delta=1)
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
            info = getPersonInfo(npc_id)
            if info is not None:
                info.change_social(friend_delta=1)
        return present_ids



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
    $ calendar_v2.advance_minutes(30)
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
            or tavern_breakfast_can_offer_perk_menu()
            or len(tavern_breakfast_core_present_ids()) > 0
            or tavern_breakfast_amanda_attic_mock_ready()
            or tavern_breakfast_melissa_amanda_gerhard_ready()
            or tavern_breakfast_tease_ready()
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
        $ player.change_stat("fun", 3)
    if len(list(tavern_recent_barber_ids() or [])) > 0:
        $ TavernBreakfastBarberTalkDay = int(dayspassed or 0)
    $ TavernBreakfastBaseText = str(MainTxt or "")
    $ TavernBreakfastBaseShownDay = -1
    $ TavernKitchenSavedText = str(MainTxt or "")
    call stat
    if _breakfast_morning_sick_girl != "":
        call CheckDailyEvent(_breakfast_morning_sick_girl, "MorningSickness", "TavernKitchen", 0)
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
        $ player_apply_arousal_trigger("breakfast_talk", int(_talk_arousal or 0))
        $ MainTxt = str(MainTxt or "") + "\nЭтот разговор слишком легко цепляет и вас самих: утреннее возбуждение только сильнее мешает делать вид, будто вы слушаете все это совсем спокойно."
    $ CurLocDesc = MainTxt
    if int(_talk_arousal or 0) > 0:
        call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastAmandaAltCure1:
    $ Amanda.set_var_int("attic_window_breakfast_bj_day", int(dayspassed or 0))
    $ player_apply_arousal_trigger("breakfast_amanda_alt_cure", max(0, 35 - int(player_state(False).intimacy.arousal_value("You") or 0)))
    $ Amanda.set_arousal(max(30, int(Amanda.arousal_value() or 0)))
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
    $ Amanda.set_var_int("attic_mock_response_day", int(dayspassed or 0))
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
    $ Amanda.set_var_int("attic_mock_exposed", 1)
    $ Amanda.set_var_int("attic_mock_stopped", 1)
    $ Amanda.change_social(open_delta=1, corruption_delta=1)
    $ MainTxt = "Вы спокойно отвечаете, что если Аманда так любит шутить про чердак, можно сразу рассказать всем, откуда она сама высматривала тот же двор. За столом становится тише. Аманда краснеет, дергает плечом и больше к этой теме за завтраком не возвращается."
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastMelissaAmandaGerhard:
    if not tavern_breakfast_melissa_amanda_gerhard_ready():
        jump TavernKitchenBreakfastMenu
    $ MainTxt = "Завтрак еще не успевает толком начаться, как Сандра снова заводит про кладовую.\n\n\"Крысы лезут к мешкам, будто им там ярмарку открыли,\" ворчит она. \"Еще пара таких ночей, и мы будем кормить не гостей, а хвостатую сволочь.\"\n\nМелисса тут же подхватывает, злая и невыспавшаяся: \"Крысы снизу, летучие мыши сверху, по крыше шуршит, по стенам скребет. Я ночью уже не знаю, то ли одеялом накрываться, то ли метлой отбиваться.\"\n\nАманда усмехается в миску. \"Так заведите кошечку. Только не простую. Клариссу, например. Пусть эта благородная киска в кладовой помурлычет, может, крысы от стыда сами уйдут.\"\n\nМелисса фыркает слишком громко, а Аманда смотрит на нее так, будто специально ждет грязной догадки. Сандра тут же хлопает ладонью по столу.\n\n\"Хватит мне ваших кошечек, кисок и ночных воздыханий,\" срезает она. \"Пальцы из пизд вынули обе и слушайте старших. Самоуспокоение закончится тем, что брат Герхард устроит вам дьявольское покаяние, а этого в доме никто не хочет. Крысы, мыши и чердак — вот о чем речь, а не о ваших мокрых фантазиях.\""
    $ CurLocDesc = MainTxt
    $ _melissa_amanda_items = [
        MenuItem("Сказать, что сначала надо решить крыс и чердак", Jump("TavernKitchenBreakfastMelissaAmandaGerhardNatural")),
        MenuItem("Не лезть в девичью перепалку", Jump("TavernKitchenBreakfastMenu")),
    ]
    call QueuePagedPanelText(MainTxt, "Спор за завтраком", _melissa_amanda_items, "plain")
    call ReturnToMainUI
    return


label TavernKitchenBreakfastMelissaAmandaGerhardNatural:
    if not tavern_breakfast_melissa_amanda_gerhard_ready():
        jump TavernKitchenBreakfastMenu
    $ TavernBreakfastMelissaAmandaGerhardDay = int(dayspassed or 0)
    $ Melissa.change_social(friend_delta=1, open_delta=1)
    $ Amanda.change_social(friend_delta=1, open_delta=1)
    $ MainTxt = "Вы обрываете спор и говорите, что сначала надо разобраться с настоящей грязью: крысы в кладовой, летучие мыши под крышей, щели на чердаке. Остальное за столом можно оставить для тех часов, когда дом не трещит по углам.\n\nСандра хмуро кивает. \"Вот это дело. Сначала хозяйство, потом девичьи смешки. Мелисса, хватит ныть — покажешь, где сильнее всего шуршит. Аманда, хватит мяукать про Клариссу — пойдешь помогать, если надо будет таскать тряпки и доски.\"\n\nАманда закатывает глаза, но спорить уже не решается. Мелисса бурчит себе под нос, зато видно: ей стало легче от того, что проблему наконец назвали вслух, а не превратили в очередную кухонную шутку.\n\nСандра под конец все равно добавляет, не удержавшись: \"И чтоб я ночью не слышала, как кто-то вместо сна себя утешает. Я вам не монастырь держу, но если брат Герхард услышит такие стоны, дьявола он будет искать не на чердаке.\""
    $ CurLocDesc = MainTxt
    call stat
    call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
    return


label TavernKitchenBreakfastAmandaAtticStop:
    $ Amanda.set_var_int("attic_mock_stopped", 1)
    $ Amanda.change_social(friend_delta=1)
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
        $ Amanda.set_var_int("breakfast_tease_day", int(dayspassed or 0))
    else:
        $ Melissa.var["breakfast_tease_day"] = int(dayspassed or 0)
    $ _breakfast_tease_picture = tavern_breakfast_tease_picture(_tease_girl, _tease_tier)
    if str(_breakfast_tease_picture or "").strip():
        vscene _breakfast_tease_picture
    if _tease_tier >= 4:
        $ MainTxt = "{} приходит к завтраку настолько по-домашнему небрежной, что это уже похоже не на случайность, а на проверку ваших границ. Ночная ткань или плохо запахнутый домашний наряд оставляют слишком много поводов для взгляда, и она прекрасно видит, что вы это заметили.".format(RealName.get(_tease_girl, _tease_girl))
        if int(Clara.var.get("booklet_market_seen", 0) or 0) == 1 or int(Clara.var.get("drawings_secret_known", 0) or 0) == 1:
            $ MainTxt = str(MainTxt or "") + "\n\nПосле историй о Клариссиных листках эта поза читается еще прямее: как будто кто-то нарочно примеряет на себя одну из тех непристойных сцен, только делает вид, что речь всего лишь о завтраке."
    elif _tease_tier >= 3:
        $ MainTxt = "{} ловит ваш взгляд, чуть меняет позу за столом и дает понять, что сегодня под платьем у нее куда меньше защиты, чем принято показывать за завтраком. Это длится всего миг, но она явно рассчитывала, что вы заметите.".format(RealName.get(_tease_girl, _tease_girl))
    elif _tease_tier >= 2:
        $ MainTxt = "{} будто случайно садится смелее обычного: колено уходит в сторону, юбка натягивается, и вся поза становится скорее вызовом, чем неловкостью.".format(RealName.get(_tease_girl, _tease_girl))
    else:
        $ MainTxt = "{} незаметно приподнимает край юбки ровно настолько, чтобы вы успели заметить белье, а потом с невинным видом возвращается к завтраку.".format(RealName.get(_tease_girl, _tease_girl))
    $ player_apply_arousal_trigger("breakfast_tease", 5 + _tease_tier)
    $ _tease_info = getPersonInfo(_tease_girl)
    if _tease_info is not None:
        $ _tease_info.add_arousal(3 + _tease_tier)
        $ _tease_info.change_social(corruption_delta=1)
    $ CurLocDesc = MainTxt
    call stat
    $ _tease_private_unlocked = bool(_tease_info is not None and people_to_int(_tease_info.sex_stat("sexacts", 0), 0) > 0)
    if _tease_girl == "amanda":
        $ _tease_private_unlocked = _tease_private_unlocked or Amanda.var_int("suckyou", 0) == 1 or Amanda.var_int("fuckyou", 0) == 1
    elif _tease_girl == "melissa":
        $ _tease_private_unlocked = _tease_private_unlocked or people_to_int(Melissa.var.get("sex_engine_unlocked", 0), 0) == 1
    if _tease_private_unlocked:
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
    $ _tease_private_info = getPersonInfo(_tease_private_girl)
    if _tease_private_info is not None:
        $ _tease_private_info.change_social(friend_delta=1, open_delta=1)
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
    $ player.change_stat("fun", 1)
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
    $ Amanda.set_var_int("barber_request_interest", 1)
    $ Amanda.set_var_int("beauty_help_terms_accepted", 1)
    $ Amanda.set_var_int("beauty_help_approved_day", int(dayspassed or 0))
    $ MainTxt = tavern_breakfast_blind_pirate_story_text()
    $ CurLocDesc = MainTxt
    $ player.change_stat("fun", 5)
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
    $ player.change_stat("rebellion", -1)
    $ Sandra.change_rebellion(-1, "breakfast_georgette_liza_order")
    $ Melissa.change_rebellion(-1, "breakfast_georgette_liza_order")
    $ Amanda.change_rebellion(-1, "breakfast_georgette_liza_order")
    $ player.change_stat("fun", 1)
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
    $ TavernSundayDinnerLastDay = int(dayspassed or 0)
    $ calendar_v2.advance_minutes(45)
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
