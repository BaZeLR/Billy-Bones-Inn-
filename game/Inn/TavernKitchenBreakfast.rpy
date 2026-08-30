# ================================================================================
# Breakfast and Sunday meal flow for TavernKitchen.
# Room entry, objects, navigation, and ordinary kitchen NPC actions stay in TavernKitchen.rpy.
# ================================================================================

init python:
    import renpy.exports as renpy

    AMANDA_BREAKFAST_TEASE_PICTURES = {
        1: "images/amanda/breakfastTease/breakfastTease1.jpg",
        2: "images/amanda/breakfastTease/breakfastTease2.jpg",
        3: "images/amanda/breakfastTease/breakfastTease3.jpg",
        4: "images/amanda/breakfastTease/breakfastTease4.jpg",
        5: "images/amanda/breakfastTease/breakfastTease5.jpg",
        6: "images/amanda/breakfastTease/breakfastTease6.jpg",
    }
    MELISSA_BREAKFAST_TEASE_PICTURES = {
        1: "images/breakfast/melissa_breakfast/melissa_breakfast_0.jpg",
        2: "images/breakfast/melissa_breakfast/melissa_breakfast_1.jpg",
        3: "images/breakfast/melissa_breakfast/melissa_breakfast_2.jpg",
        4: "images/breakfast/melissa_breakfast/melissa_breakfast_3.jpg",
    }
    BREAKFAST_GIRLS_TEASE_PICTURE = "images/breakfast/tavent_girls.jpg"

    def tavern_breakfast_available():
        return int(calendar_v2.hour or 0) < 12 and not bool(player.tavern_management.breakfast.today)

    def tavern_sunday_dinner_available():
        return (
            all(
                str(people.schedule_state(npc_id).get("label", "") or "") == "sunday_dinner"
                and str(people.schedule_state(npc_id).get("location", "") or "") == "TavernKitchen"
                for npc_id in ("sandra", "melissa", "amanda")
            )
            and int(player.tavern_management.breakfast.sunday_dinner_last_day or -1) != current_game_day()
        )

    def npc_schedule_becky_sandra_kitchen_visit_active():
        if int(Becky.sandra_kitchen_visit_period or 0) == int(calendar_v2.period or 0):
            return False
        if int(Becky.home_visit_stage or 0) < 2:
            return False
        return int(calendar_v2.hour or 0) >= 12 and int(calendar_v2.hour or 0) < 18

    def tavern_breakfast_present_ids():
        present = []
        if bool(player.tavern_management.breakfast.event_active) and player.tavern_management.breakfast.present_ids is not None:
            present.extend(list(player.tavern_management.breakfast.present_ids or []))
        else:
            present.extend(list(household_breakfast_attendee_ids() or []))

        try:
            present.extend(list(people.ids_at("TavernKitchen") or []))
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
            if Amanda.attic_busted():
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
        if not Amanda.attic_busted():
            return False
        if "amanda" not in list(tavern_breakfast_present_ids() or []):
            return False
        if Amanda.attic_window_breakfast_bj_day == current_game_day():
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
        roll = (current_game_day() * 17 + int(calendar_v2.week or 0) * 13 + int(calendar_v2.hour or 0) * 5 + wetness + sluttiness_value * 3 + int(profile.get("rebel_value", 0) or 0) * 7) % 100
        return roll < chance

    def tavern_breakfast_amanda_attic_mock_ready():
        return (
            Amanda.attic_busted()
            and "amanda" in list(tavern_breakfast_present_ids() or [])
            and not Amanda.attic_mock_stopped
            and not Amanda.attic_mock_exposed
            and Amanda.attic_mock_response_day != current_game_day()
        )

    def tavern_breakfast_sweet_or_spiced_served():
        return (
            tavern_kitchen_honey_bonus_active()
            or tavern_kitchen_fertility_bonus_active()
            or int(player.tavern_management.breakfast.spicy_drink_day or -1) == current_game_day()
            or int(player.tavern_management.breakfast.sweet_perk_day or -1) == current_game_day()
        )

    def tavern_breakfast_melissa_amanda_gerhard_ready():
        present_ids = list(tavern_breakfast_present_ids() or [])
        return (
            (int(threads["melissaBatProblem"].num or 0) >= 3 or int(werecat_state().get("rats_problem_active", 0) or 0) == 1)
            and int(threads["melissaBatProblem"].num or 0) < 8
            and "melissa" in present_ids
            and "amanda" in present_ids
            and "sandra" in present_ids
            and int(player.tavern_management.breakfast.melissa_amanda_gerhard_day or -1) != current_game_day()
        )

    def tavern_breakfast_soap_request_girl():
        for npc_id in list(tavern_breakfast_present_ids() or []):
            if npc_id in ("sandra", "melissa", "amanda") and household_soap_request_ready(npc_id):
                return npc_id
        return ""

    def tavern_breakfast_dress_request_girl():
        present_ids = list(tavern_breakfast_present_ids() or [])
        if "sandra" in present_ids and story_event_available("TavernKitchen", "sandra_dress_initiative"):
            return "sandra"
        if "melissa" in present_ids and story_event_available("TavernKitchen", "melissa_dress_request"):
            return "melissa"
        if "amanda" in present_ids and story_event_available("TavernKitchen", "amanda_dress_request"):
            return "amanda"
        return ""

    def tavern_breakfast_tease_candidate():
        candidates = []
        for npc_id in list(tavern_breakfast_present_ids() or []):
            if npc_id not in ("amanda", "melissa"):
                continue
            info = people.get_info(npc_id)
            last_tease_day = Amanda.breakfast_tease_day if npc_id == "amanda" else people_to_int(Melissa.breakfast_tease_day, -1)
            if last_tease_day == current_game_day():
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
        info = people.get_info(key)
        if info is None:
            return 0
        if info is None:
            return 0
        score = 0
        score += min(4, max(0, int(getattr(info, "rel", 0) or 0) // 4))
        score += min(3, max(0, int(getattr(info, "openness", 0) or 0) // 5))
        score += min(3, max(0, int(getattr(info, "corruption", 0) or 0) // 20))
        if current_game_day() - int(household.barber_visit_last_day.get(key, -99) or -99) <= 14:
            score += 2
        dress_score = max(info.clothing_slut("top"), info.clothing_slut("bottom"))
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
        if int(player.tavern_management.breakfast.spicy_drink_day or -1) == current_game_day():
            score += 2
        share_perks = player.tavern_management.breakfast_share_perks
        if isinstance(share_perks, dict):
            share_data = share_perks.get(key, {})
            if isinstance(share_data, dict) and current_game_day() - int(share_data.get("day", -99) or -99) <= 7:
                score += min(3, max(1, int(share_data.get("score", 1) or 1)))
        if int(threads["claraBookletMarket"].num or 0) >= 1 or bool(Clara.drawings_secret_known):
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
        if int(threads["claraBookletMarket"].num or 0) >= 1 or bool(Clara.drawings_secret_known):
            lines.append("После разговоров о непристойных рисунках и книжечках Клариссы даже обычные шутки за столом цепляют сильнее: все слишком хорошо понимают, какие картинки теперь стоят за невинными словами.")
        share_perks = player.tavern_management.breakfast_share_perks
        recent_shared = []
        if isinstance(share_perks, dict):
            for npc_id in present_ids:
                share_data = share_perks.get(npc_id, {})
                if isinstance(share_data, dict) and current_game_day() - int(share_data.get("day", -99) or -99) <= 7:
                    recent_shared.append(_action_display_name(npc_id))
        if len(recent_shared) > 0:
            lines.append("Те, с кем вы недавно делились едой, напитками или сладостями, держатся за столом теплее обычного: %s явно помнят, что ваша забота не ограничивается приказами." % ", ".join(recent_shared))
        if tavern_kitchen_honey_bonus_active() or int(player.tavern_management.breakfast.spicy_drink_day or -1) == current_game_day():
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
        if key == "amanda":
            return AMANDA_BREAKFAST_TEASE_PICTURES[1]
        if key == "melissa":
            return MELISSA_BREAKFAST_TEASE_PICTURES[1]
        candidates = {
            "sandra": [
                "images/sandra/tavern/kitchen_sandra_0.jpg",
                "images/sandra/tavern/kitchen_sandra_1.jpg",
                "images/sandra/tavern/kitchen_sandra_2.jpg",
                "images/sandra/tavern/kitchen_sandra_3.jpg",
                "images/sandra/tavern/kitchen_sandra_4.jpg",
                "images/sandra/sandra_kitchen.png",
                "images/tavern/kitchen/sandra.png",
                "images/kitchen/kitchen_sandra_0.jpg",
                "images/kitchen/kitchen_sandra_1.jpg",
                "images/kitchen/kitchen_sandra_2.jpg",
                "images/kitchen/kitchen_sandra_3.jpg",
                "images/kitchen/kitchen_sandra_4.jpg",
                "images/tavern/kitchen/kitchen_sandra_0.jpg",
                "images/tavern/kitchen/kitchen_sandra_1.jpg",
                "images/tavern/kitchen/kitchen_sandra_2.jpg",
                "images/tavern/kitchen/kitchen_sandra_3.jpg",
                "images/tavern/kitchen/kitchen_sandra_4.jpg",
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

        rows = list(targets or tavern_breakfast_core_present_ids() or [])
        if len(rows) <= 0:
            return []
        share_perks = player.tavern_management.breakfast_share_perks
        item_key = str(item_id or "").strip()
        perk_score = max(1, int(score or 1))
        for npc_id in rows:
            key = str(npc_id or "").strip().lower()
            if key not in ("sandra", "melissa", "amanda"):
                continue
            existing = share_perks.get(key, {})
            existing_score = int(existing.get("score", 0) or 0) if isinstance(existing, dict) else 0
            share_perks[key] = {
                "day": current_game_day(),
                "item": item_key,
                "score": max(existing_score, perk_score),
            }
        return rows

    def tavern_breakfast_apply_group_social(targets=None, friend_delta=0, open_delta=0, corruption_delta=0, fun_delta=0):
        rows = list(targets or tavern_breakfast_core_present_ids() or [])
        for npc_id in rows:
            info = people.get_info(npc_id)
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
            if item_key and int(player.item_count(item_key) or 0) > 0:
                if player.remove_item(item_key, 1):
                    return item_key
        return ""

    def tavern_breakfast_food_perk_item_available():
        for item_id in ("honey_comb_001", "berries_001", "milk_pitcher_001", "boar_meat_001", "mushroom_001"):
            if tavern_kitchen_food_stock_count(item_id) > 0 or int(player.item_count(item_id) or 0) > 0:
                return True
        return False

    def tavern_breakfast_drink_perk_item_available():
        for item_id in ("energy_tea_001", "drink_ale_001", "libido_tincture_001"):
            if int(player.item_count(item_id) or 0) > 0:
                return True
        return False

    def tavern_breakfast_lewd_series_available():
        return int(threads["claraBookletMarket"].num or 0) >= 1 or bool(Clara.drawings_secret_known)

    def tavern_breakfast_appearance_perk_available():
        for npc_id in tavern_breakfast_core_present_ids():
            if current_game_day() - int(household.barber_visit_last_day.get(npc_id, -99) or -99) <= 14:
                return True
            info = people.get_info(npc_id)
            if max(info.clothing_slut("top"), info.clothing_slut("bottom")) >= 3:
                return True
        return False

    def tavern_breakfast_can_offer_perk_menu():
        if len(tavern_breakfast_core_present_ids()) <= 0:
            return False
        day_value = current_game_day()
        return (
            (int(player.tavern_management.breakfast.food_perk_day or -1) != day_value and tavern_breakfast_food_perk_item_available())
            or (int(player.tavern_management.breakfast.drink_perk_day or -1) != day_value and tavern_breakfast_drink_perk_item_available())
            or (int(player.tavern_management.breakfast.lewd_series_day or -1) != day_value and tavern_breakfast_lewd_series_available())
        )

    def tavern_breakfast_perk_menu_items():
        items = []
        day_value = current_game_day()
        special_milk_ready = False
        special_ale_ready = False
        if int(player.tavern_management.breakfast.blind_pirate_team_pledge or 0) == 1 and int(player.tavern_management.breakfast.milk_team_talk_done or 0) == 0 and int(player.tavern_management.breakfast.food_perk_day or -1) != day_value:
            if tavern_kitchen_food_stock_count("milk_pitcher_001") > 0 or int(player.item_count("milk_pitcher_001") or 0) > 0:
                special_milk_ready = True
                items.append(MenuItem("Поделиться молоком", Call("TavernKitchenBreakfastPerkFood", "milk_pitcher_001")))
        if int(player.tavern_management.breakfast.blind_pirate_team_pledge or 0) == 1 and int(player.tavern_management.breakfast.milk_team_talk_done or 0) == 1 and int(player.tavern_management.breakfast.ale_team_talk_done or 0) == 0 and int(player.tavern_management.breakfast.drink_perk_day or -1) != day_value:
            if int(player.item_count("drink_ale_001") or 0) > 0:
                special_ale_ready = True
                items.append(MenuItem("Поделиться элем за команду", Call("TavernKitchenBreakfastPerkDrink", "drink_ale_001")))
        if not special_milk_ready and int(player.tavern_management.breakfast.food_perk_day or -1) != day_value and tavern_breakfast_food_perk_item_available():
            items.append(MenuItem("Поставить на стол лучшие припасы", Jump("TavernKitchenBreakfastPerkFood")))
        if not special_ale_ready and int(player.tavern_management.breakfast.drink_perk_day or -1) != day_value and tavern_breakfast_drink_perk_item_available():
            items.append(MenuItem("Поделиться напитком", Jump("TavernKitchenBreakfastPerkDrink")))
        if int(player.tavern_management.breakfast.lewd_series_day or -1) != day_value and tavern_breakfast_lewd_series_available():
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

        preferred = preferred_ids or ("honey_comb_001", "berries_001", "milk_pitcher_001", "boar_meat_001", "mushroom_001")
        item_key = tavern_breakfast_take_perk_item(preferred)
        if str(item_key or "").strip() == "":
            return "На кухне не находится ничего достаточно хорошего, чтобы сделать из этого особое утреннее угощение."
        player.tavern_management.breakfast.food_perk_day = current_game_day()
        score = 1
        if item_key in ("honey_comb_001", "berries_001", "milk_pitcher_001"):
            player.tavern_management.breakfast.sweet_perk_day = current_game_day()
            score = 3 if item_key == "honey_comb_001" else 2
        if item_key == "boar_meat_001":
            score = 2
        targets = tavern_breakfast_record_group_perk(item_key, score)
        tavern_breakfast_apply_group_social(targets, 1, 0, 1 if item_key in ("honey_comb_001", "boar_meat_001") else 0, 2)
        if item_key == "milk_pitcher_001" and int(player.tavern_management.breakfast.blind_pirate_team_pledge or 0) == 1 and int(player.tavern_management.breakfast.milk_team_talk_done or 0) == 0 and tavern_breakfast_blind_pirate_team_present():
            player.tavern_management.breakfast.milk_team_talk_done = 1
            return tavern_breakfast_blind_pirate_milk_text()
        item_name = tavern_kitchen_food_item_name(item_key)
        text = "Вы не просто завтракаете, а ставите на стол %s как отдельное угощение для своих. Домочадцы быстро понимают разницу: это уже не казенная миска, а знак, что хорошие припасы идут тем, кто держит дом рядом с вами." % item_name
        if item_key in ("honey_comb_001", "berries_001", "milk_pitcher_001"):
            text += "\n\nСладкое сразу меняет тон завтрака. Девочки отвечают мягче, чаще улыбаются и позволяют себе более ленивые, домашние позы за столом."
        return text

    def tavern_breakfast_apply_drink_perk(preferred_ids=None):

        item_key = ""
        for candidate in list(preferred_ids or ("energy_tea_001", "drink_ale_001", "libido_tincture_001")):
            if int(player.item_count(candidate) or 0) > 0 and player.remove_item(candidate, 1):
                item_key = candidate
                break
        if item_key == "":
            return "У вас нет подходящего напитка, чтобы сделать завтрак особенным."
        if item_key == "drink_ale_001":
            player.add_item("empty_bottle_001", 1)
            player.add_item("cork_001", 1)
        player.tavern_management.breakfast.drink_perk_day = current_game_day()
        if item_key == "libido_tincture_001":
            player.tavern_management.breakfast.spicy_drink_day = current_game_day()
        score = 3 if item_key == "libido_tincture_001" else 2
        targets = tavern_breakfast_record_group_perk(item_key, score)
        tavern_breakfast_apply_group_social(targets, 1, 1, 1 if item_key in ("drink_ale_001", "libido_tincture_001") else 0, 2)
        if item_key == "energy_tea_001":
            return "Вы делитесь бодрящим чаем со всеми, кто сейчас сидит за столом. Теплая кружка в руках делает утренний разговор ровнее, а девочки заметно легче принимают ваши замечания и распоряжения."
        if item_key == "drink_ale_001":
            if int(player.tavern_management.breakfast.blind_pirate_team_pledge or 0) == 1 and int(player.tavern_management.breakfast.milk_team_talk_done or 0) == 1 and int(player.tavern_management.breakfast.ale_team_talk_done or 0) == 0 and tavern_breakfast_blind_pirate_team_present():
                player.tavern_management.breakfast.ale_team_talk_done = 1
                return tavern_breakfast_blind_pirate_ale_text()
            return "Вы делитесь элем за завтраком, разливая его малыми кружками. Это не пьянка, но общий стол сразу становится свободнее: шутки идут смелее, взгляды держатся дольше."
        return "Вы делитесь за завтраком пряной настойкой. Она расходится по кружкам совсем понемногу, зато эффект виден быстро: голоса теплеют, щеки розовеют, а обычные фразы начинают звучать двусмысленно."

    def tavern_breakfast_apply_lewd_series_perk():

        if not tavern_breakfast_lewd_series_available():
            return "Пока у вас нет подходящей непристойной истории или серии, которую можно пустить за столом."
        player.tavern_management.breakfast.lewd_series_day = current_game_day()
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

        if not tavern_breakfast_appearance_perk_available():
            return "Сегодня за столом нет ни свежих обновок, ни недавних визитов к Серджио, за которые можно зацепить разговор."
        player.tavern_management.breakfast.appearance_perk_day = current_game_day()
        targets = tavern_breakfast_record_group_perk("appearance", 2)
        tavern_breakfast_apply_group_social(targets, 1, 1, 0, 1)
        names = ", ".join([_action_display_name(npc_id) for npc_id in targets])
        return "Вы спокойно отмечаете, что %s за завтраком выглядят уже совсем по-домашнему: не как работницы перед хозяином, а как свои люди в доме, где можно выйти к столу без полной брони приличий.\n\nТакой тон им явно нравится. Комплимент не звучит приказом, но закрепляет новую меру доверия: обновки, визиты к Серджио и домашняя небрежность становятся частью общего утреннего порядка." % names

    def tavern_breakfast_market_story_text():
        if int(calendar_v2.week or 0) == 3:
            return "Вы пересказываете утренние рыночные слухи и напоминаете, что к пятничным танцам город уже начинает шевелиться заранее. За столом сразу прикидывают, кого это приведет вечером в трактир."
        if int(calendar_v2.week or 0) == 7:
            return "Вы делитесь тем, что слышали утром в городе перед воскресной службой. Домочадцы слушают внимательнее обычного: в такой день слухи расходятся особенно быстро."
        return "Вы коротко рассказываете, что успели заметить и услышать в городе. Для домашнего стола это почти такой же важный утренний ритуал, как сама каша."

    def tavern_breakfast_motivation_text():
        if "sandra" in tavern_breakfast_present_ids():
            return "Вы напоминаете, что день надо вытянуть ровно и без лишней ругани. Сандра сперва хмыкает, но потом одобрительно кивает: тон задан правильно, и остальные тоже собираются заметно бодрее."
        return "Вы находите пару крепких слов перед началом дня. Даже если никто не спешит это признавать вслух, общий стол после такого расходится собраннее."

    def tavern_breakfast_restore_ui_state(panel_text=""):
        text_value = str(panel_text or tavern_kitchen_saved_text() or player.tavern_management.breakfast.base_text or scene_runtime.text or "Вы все еще сидите за общим утренним столом.")
        scene_runtime.text = text_value
        scene_runtime.location_text = text_value
        main_ui_runtime.mode = "scene"
        main_ui_runtime.selected_char = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.object_id = ""
        main_ui_runtime.action_title = "Завтрак"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []
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
        return int(threads["cityBlindPirateFall"].num or 0) == 1

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
            not crafting.soap_sample_intro_done
            and soap_available_piece_count() >= 3
            and required_ids.issubset(present_ids)
        )

    def tavern_breakfast_apply_first_soap_samples():

        if not tavern_breakfast_can_give_first_soap_samples():
            return ""
        player.remove_item("soap_001", 3)
        for npc_id in ("sandra", "melissa", "amanda"):
            crafting.soap_sample_given[npc_id] = 1
            crafting.soap_requests[npc_id] = 1
            info = people.get_info(npc_id)
            if info is not None:
                info.change_social(friend_delta=1)
        crafting.soap_sample_intro_done = True
        player.tavern_management.breakfast.soap_announced_day = current_game_day()
        player.change_stat("fun", 3)
        return "За завтраком вы объявляете, что партия мыла наконец вылежалась, и тут же раздаете по куску Сандре, Мелиссе и Аманде на пробу. Дом сразу оживляется: всем любопытно, как поведет себя новое %s мыло, когда его наконец пустят в ход." % soap_last_batch_label()

    def tavern_breakfast_can_serve_spicy_tincture():
        return (
            int(player.item_count("libido_tincture_001") or 0) > 0
            and len(list(tavern_breakfast_present_ids() or [])) >= 2
            and int(player.tavern_management.breakfast.spicy_drink_day or -1) != current_game_day()
        )

    def tavern_sunday_dinner_can_serve_spicy_tincture(present_ids=None):
        dinner_ids = list(tavern_sunday_dinner_present_ids() if present_ids is None else present_ids)
        return (
            int(player.item_count("libido_tincture_001") or 0) > 0
            and len(dinner_ids) >= 2
            and int(player.tavern_management.breakfast.sunday_dinner_spicy_drink_day or -1) != current_game_day()
        )

    def tavern_kitchen_spicy_tincture_apply(present_ids=None):
        rows = list(present_ids or [])
        if len(rows) <= 0:
            return ""
        player.remove_item("libido_tincture_001", 1)
        for npc_id in rows:
            info = people.get_info(npc_id)
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
            "images/kitchen/kitchen_breakfast.jpg",
            "images/tavern/kitchen/kitchen_breakfast.jpg",
            "images/breakfast/tavern_girls_impregnat.jpg",
            "images/breakfast/tavern_girls_impregnat_1.jpg",
            "images/breakfast/amanda_b.png",
        ]
        for candidate in candidates:
            if renpy.loadable(candidate):
                return candidate
        return tavern_kitchen_event_picture("kitchen_breakfast")

    def tavern_breakfast_tease_picture(girl_name="", tier=0):
        key = str(girl_name or "").strip().lower()
        if key == "amanda":
            tease_tier = max(1, min(4, int(tier or 0)))
            horny_state = int(Amanda.arousal_value() or 0) >= 65
            if tease_tier >= 4:
                picture_number = 6 if horny_state else 5
            elif tease_tier >= 3:
                picture_number = 4 if horny_state else 3
            else:
                picture_number = tease_tier
            return AMANDA_BREAKFAST_TEASE_PICTURES[picture_number]
        if key == "melissa":
            tease_tier = max(1, min(4, int(tier or 0)))
            return MELISSA_BREAKFAST_TEASE_PICTURES[tease_tier]
        return tavern_kitchen_breakfast_picture()

    def tavern_kitchen_sunday_dinner_picture():
        return tavern_kitchen_event_picture("kitchen_sundaydinnerAll_0")

    def tavern_sunday_dinner_present_ids():
        kitchen_ids = set(people.ids_at("TavernKitchen") or [])
        rows = []
        for npc_id in ("sandra", "melissa", "amanda"):
            if npc_id not in kitchen_ids:
                continue
            if household_morning_issue_type(npc_id) in ("sick", "sleepy"):
                continue
            rows.append(npc_id)
        if "becky" in kitchen_ids:
            rows.append("becky")
        return rows

    def tavern_sunday_dinner_present_names():
        names = []
        for npc_id in tavern_sunday_dinner_present_ids():
            names.append(_action_display_name(npc_id))
        return names

    def tavern_recent_barber_ids():
        rows = []
        for npc_id in ("sandra", "melissa", "amanda"):
            if current_game_day() - int(household.barber_visit_last_day.get(npc_id, -99) or -99) <= 14:
                rows.append(npc_id)
        return rows

    def tavern_barber_breakfast_lines():
        recent_ids = [npc_id for npc_id in tavern_recent_barber_ids() if npc_id in list(tavern_breakfast_present_ids() or [])]
        if len(recent_ids) <= 0 or int(player.tavern_management.breakfast.barber_talk_day or -1) == current_game_day():
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
        if len(recent_ids) <= 0 or int(player.tavern_management.breakfast.sunday_dinner_barber_talk_day or -1) == current_game_day():
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
        lines.extend(list(tavern_breakfast_relaxed_appearance_lines() or []))
        rat_problem = int(werecat_state().get("rats_problem_active", 0) or 0) == 1 or int(next_day_runtime.current_day.get("rat_food_loss", 0) or 0) > 0
        bats_stage = int(threads["melissaBatProblem"].num or 0)

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
            if threads["melissaBatProblem"].num >= 6 and "amanda" in present_ids:
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
        if int(calendar_v2.week or 0) == 3 and "sandra" in present_ids:
            lines.append("За завтраком Сандра напоминает, что к середине недели надо бы пополнить запасы вина и хорошей еды, иначе в трактире скоро станет совсем уныло.")
        if tavern_breakfast_can_offer_dance_sponsorship() and "sandra" in present_ids:
            lines.append("Сандра заодно осторожно спрашивает, не хотите ли вы и в этом году скинуться на пятничные танцы от лица трактира.")
        if int(player.tavern_management.dance_sponsor or 0) == 1 and int(player.tavern_management.breakfast.dance_sponsor_announced_day or -1) != current_game_day():
            player.tavern_management.breakfast.dance_sponsor_announced_day = current_game_day()
            lines.append("За завтраком вы объявляете, что трактир уже выставит вино и закуски к пятничным танцам. Сандра довольно кивает: такой взнос сразу делает дом заметнее в городе, а девки начинают переглядываться куда живее обычного.")
        if soap_available_piece_count() > 0 and int(player.tavern_management.breakfast.soap_announced_day or -1) != current_game_day():
            if not crafting.soap_sample_intro_done:
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
            info = people.get_info(npc_id)
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

    def tavern_sunday_dinner_apply_social_bonus(present_ids=None):
        present_ids = list(tavern_sunday_dinner_present_ids() if present_ids is None else present_ids)
        for npc_id in present_ids:
            info = people.get_info(npc_id)
            if info is not None:
                info.change_social(friend_delta=1)
        return present_ids



label TavernKitchenBreakfast:
    $ renpy.dynamic("_breakfast_morning_sick_girl", "_eat_result", "_breakfast_social_ids", "_soap_intro_text", "_breakfast_lines", "_breakfast_line_index")
    if not tavern_breakfast_available():
        $ scene_runtime.text = "Сегодня вы уже завтракали."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
        return
    $ player.tavern_management.breakfast.present_ids = list(household_breakfast_attendee_ids() or [])
    $ player.tavern_management.breakfast.today = True
    $ player.tavern_management.breakfast.last_day = current_game_day()
    $ player.tavern_management.breakfast.day = current_game_day()
    $ player.tavern_management.breakfast.event_active = True
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
            or int(player.tavern_management.breakfast.georgett_liza_pending or 0) == 1
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
        _breakfast_lines = [str(row or "").strip() for row in _breakfast_lines if str(row or "").strip()]
    if int(player.tavern_management.dance_sponsor or 0) == 1 and int(player.tavern_management.breakfast.dance_sponsor_announced_day or -1) != current_game_day():
        $ player.tavern_management.breakfast.dance_sponsor_announced_day = current_game_day()
    $ _eat_result = player_eat_meal("утреннюю кашу и свежий хлеб", 16)
    if str(_eat_result.get("text", "") or "").strip():
        $ _breakfast_lines.append(str(_eat_result.get("text", "") or "").strip())
    $ _breakfast_social_ids = tavern_breakfast_apply_social_bonus()
    if len(list(_breakfast_social_ids or [])) > 0:
        $ _breakfast_lines.append("Совместный завтрак заметно сближает вас с теми, кто сидит с вами за столом.")
    if tavern_breakfast_can_give_first_soap_samples():
        $ _soap_intro_text = tavern_breakfast_apply_first_soap_samples()
        if str(_soap_intro_text or "").strip():
            $ _breakfast_lines.append(str(_soap_intro_text or "").strip())
    elif soap_available_piece_count() > 0 and int(player.tavern_management.breakfast.soap_announced_day or -1) != current_game_day():
        $ player.tavern_management.breakfast.soap_announced_day = current_game_day()
        $ player.change_stat("fun", 3)
    if len(list(tavern_recent_barber_ids() or [])) > 0:
        $ player.tavern_management.breakfast.barber_talk_day = current_game_day()
    call stat
    if _breakfast_morning_sick_girl != "":
        call check_daily_event(_breakfast_morning_sick_girl, "MorningSickness", "TavernKitchen", 0)
    $ _breakfast_line_index = 0
    while _breakfast_line_index < len(_breakfast_lines):
        $ scene_runtime.text = _breakfast_lines[_breakfast_line_index]
        $ scene_runtime.location_text = scene_runtime.text
        $ tavern_kitchen_set_saved_text(scene_runtime.text)
        menu:
            "Продолжить":
                $ _breakfast_line_index += 1
    $ player.tavern_management.breakfast.base_text = str(scene_runtime.text or "")
    $ player.tavern_management.breakfast.base_shown_day = -1
    call TavernKitchenBreakfastMenu
    return


label TavernKitchenBreakfastMenu:
    $ renpy.dynamic("_breakfast_soap_girl", "_breakfast_dress_girl", "_breakfast_issue_girl", "_breakfast_issue_name")
    if not player.tavern_management.breakfast.event_active:
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
        return
    while True:
        $ _breakfast_soap_girl = str(tavern_breakfast_soap_request_girl() or "")
        $ _breakfast_dress_girl = str(tavern_breakfast_dress_request_girl() or "")
        $ _breakfast_issue_girl = str(tavern_breakfast_morning_issue_girl() or "")
        $ _breakfast_issue_name = _action_display_name(_breakfast_issue_girl)
        menu:
            "Послушать разговор за столом" if tavern_breakfast_can_listen() and int(player.tavern_management.breakfast.listen_day or -1) != current_game_day():
                call TavernKitchenBreakfastHearDialogue

            "Рассказать, что вы видели на рынке" if tavern_breakfast_has_market_topic() and int(player.tavern_management.breakfast.market_talk_day or -1) != current_game_day():
                call TavernKitchenBreakfastMarketTalk

            "Сказать пару слов перед работой" if tavern_breakfast_can_make_speech() and int(player.tavern_management.breakfast.motivation_day or -1) != current_game_day():
                call TavernKitchenBreakfastMotivation

            "Поделиться едой и напитками" if tavern_breakfast_can_offer_perk_menu():
                call TavernKitchenBreakfastPerkMenu

            "Посмотреть на Сандру за завтраком" if "sandra" in tavern_breakfast_core_present_ids():
                call TavernKitchenBreakfastLookAtGirl("sandra")

            "Посмотреть на Мелиссу за завтраком" if "melissa" in tavern_breakfast_core_present_ids():
                call TavernKitchenBreakfastLookAtGirl("melissa")

            "Посмотреть на Аманду за завтраком" if "amanda" in tavern_breakfast_core_present_ids():
                call TavernKitchenBreakfastLookAtGirl("amanda")

            "Ответить Аманде про чердак" if tavern_breakfast_amanda_attic_mock_ready():
                call TavernKitchenBreakfastAmandaAtticMock

            "Разобрать спор Мелиссы и Аманды" if tavern_breakfast_melissa_amanda_gerhard_ready():
                call TavernKitchenBreakfastMelissaAmandaGerhard

            "Заметить провокацию за столом" if tavern_breakfast_tease_ready():
                call TavernKitchenBreakfastTease

            "Выслушать просьбу о мыле" if _breakfast_soap_girl != "":
                call HouseholdSoapRequestEvent(_breakfast_soap_girl)

            "Поговорить с Сандрой о новом платье" if _breakfast_dress_girl == "sandra":
                call SandraDressInitiativeEvent

            "Поговорить с Мелиссой о новом платье" if _breakfast_dress_girl == "melissa":
                call MelissaDressRequestEvent

            "Поговорить с Амандой о новом платье" if _breakfast_dress_girl == "amanda":
                call AmandaDressRequestEvent

            "Предложить Сандре сходить к Серджио" if household_barber_request_ready("sandra", "breakfast"):
                call HouseholdBarberRequestEvent("sandra")

            "Предложить Мелиссе сходить к Серджио" if household_barber_request_ready("melissa", "breakfast"):
                call HouseholdBarberRequestEvent("melissa")

            "Предложить Аманде сходить к Серджио" if household_barber_request_ready("amanda", "breakfast"):
                call HouseholdBarberRequestEvent("amanda")

            "Объявить о Жоржетте и Лизетте" if int(player.tavern_management.breakfast.georgett_liza_pending or 0) == 1:
                call TavernKitchenBreakfastAnnounceGeorgetteLiza

            "Проверить, почему [_breakfast_issue_name] не вышла к завтраку" if _breakfast_issue_girl != "":
                call TavernKitchenBreakfastMorningIssue

            "Поговорить об отсутствующих" if str(tavern_breakfast_absent_prompt() or "").strip() and int(player.tavern_management.breakfast.absent_talk_day or -1) != current_game_day():
                call TavernKitchenBreakfastTalkAbsent

            "Попросить Сандру почаще собирать всех на общий завтрак" if "sandra" in list(tavern_breakfast_present_ids() or []) and tavern_kitchen_sandra_can_discuss_breakfasts():
                call TavernKitchenAskSandraBreakfasts

            "Попросить Сандру мягче настроить домочадцев к гостям" if "sandra" in list(tavern_breakfast_present_ids() or []) and tavern_kitchen_sandra_can_discuss_clients():
                call TavernKitchenAskSandraClients

            "Обсудить пятничные танцы" if tavern_breakfast_can_offer_dance_sponsorship():
                call TavernKitchenBreakfastDanceMenu

            "Закончить завтрак":
                call TavernKitchenFinishBreakfastEvent
                return


label TavernKitchenBreakfastShowText(text=""):
    $ scene_runtime.text = str(text or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ tavern_kitchen_set_saved_text(scene_runtime.text)
    "[scene_runtime.text]"
    return


label TavernKitchenBreakfastHearDialogue:
    $ renpy.dynamic("_banter_text", "_talk_arousal", "_talk_result")
    $ player.tavern_management.breakfast.listen_day = current_game_day()
    if tavern_breakfast_amanda_alt_cure_ready():
        call TavernKitchenBreakfastAmandaAltCure1
        return
    $ _talk_result = tavern_breakfast_talk_result()
    $ _banter_text = str(_talk_result.get("text", "") or "")
    $ _talk_arousal = int(_talk_result.get("arousal_gain", 0) or 0)
    if str(_banter_text or "").strip():
        $ scene_runtime.text = str(_banter_text or "")
    else:
        $ scene_runtime.text = "За столом на миг воцаряется обычная утренняя болтовня без чего-то особенно примечательного."
    if int(_talk_arousal or 0) > 0:
        $ player_apply_arousal_trigger("breakfast_talk", int(_talk_arousal or 0))
        $ scene_runtime.text = str(scene_runtime.text or "") + "\nЭтот разговор слишком легко цепляет и вас самих: утреннее возбуждение только сильнее мешает делать вид, будто вы слушаете все это совсем спокойно."
    $ scene_runtime.location_text = scene_runtime.text
    if int(_talk_arousal or 0) > 0:
        call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastAmandaAltCure1:
    $ Amanda.attic_window_breakfast_bj_day = current_game_day()
    if int(Amanda.attic_window_favor_stage or 0) in (1, 2):
        $ Amanda.attic_window_favor_stage = 3
    $ player_apply_arousal_trigger("breakfast_amanda_alt_cure", max(0, 35 - int(player.intimacy.arousal_value() or 0)))
    $ Amanda.set_arousal(max(30, int(Amanda.arousal_value() or 0)))
    $ scene_runtime.text = "За общим столом Аманда сегодня на редкость притихла. Несколько раз она украдкой встречается с вами взглядом, потом криво улыбается и будто невзначай касается вашей ноги под столом. Колкость про Мелиссу так и не срывается с ее языка.\n\nЧерез пару минут ее ступня уже гладит вас куда смелее, а сама она наклоняется ближе и почти беззвучно шепчет, что после той неловкой истории с окном ей почему-то самой теперь труднее делать вид, будто ничего такого в доме не бывает.\n\nПока остальные заняты едой и разговорами, Аманда незаметно скользит ниже под край стола и решает загладить свою дерзость способом куда приятнее обычных извинений."
    $ scene_runtime.location_text = scene_runtime.text
    call IntAmandaSex("amanda", "home", "minet")
    $ scene_runtime.text = "Когда все заканчивается, Аманда так же тихо возвращается на свое место, поправляет волосы и берется за ложку так невинно, будто под столом только что не происходило ничего предосудительного. На вас она смотрит уже без прежней насмешки: скорее с довольным сговором, чем с привычным желанием поддеть."
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastAmandaAtticMock:
    if not tavern_breakfast_amanda_attic_mock_ready():
        return
    $ Amanda.attic_mock_response_day = current_game_day()
    $ scene_runtime.text = "Стоит за завтраком снова всплыть слову \"чердак\", Аманда тут же цепляет вас взглядом и слишком невинно спрашивает, не собираетесь ли вы опять падать туда, куда приличные люди хотя бы стучатся."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Рассказать всем, что вы видели у окна Аманды":
            jump TavernKitchenBreakfastAmandaAtticExpose

        "Тихо велеть ей прекратить насмешки":
            jump TavernKitchenBreakfastAmandaAtticStop

        "Не развивать тему":
            return
    return


label TavernKitchenBreakfastAmandaAtticExpose:
    $ Amanda.attic_mock_exposed = True
    $ Amanda.attic_mock_stopped = True
    $ Amanda.change_social(open_delta=1, corruption_delta=1)
    $ scene_runtime.text = "Вы спокойно отвечаете, что если Аманда так любит шутить про чердак, можно сразу рассказать всем, откуда она сама высматривала тот же двор. За столом становится тише. Аманда краснеет, дергает плечом и больше к этой теме за завтраком не возвращается."
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastMelissaAmandaGerhard:
    if not tavern_breakfast_melissa_amanda_gerhard_ready():
        return
    vscene BREAKFAST_GIRLS_TEASE_PICTURE
    $ scene_runtime.text = "Завтрак еще не успевает толком начаться, как Сандра снова заводит про кладовую.\n\n\"Крысы лезут к мешкам, будто им там ярмарку открыли,\" ворчит она. \"Еще пара таких ночей, и мы будем кормить не гостей, а хвостатую сволочь.\"\n\nМелисса тут же подхватывает, злая и невыспавшаяся: \"Крысы снизу, летучие мыши сверху, по крыше шуршит, по стенам скребет. Я ночью уже не знаю, то ли одеялом накрываться, то ли метлой отбиваться.\"\n\nАманда усмехается в миску. \"Так заведите кошечку. Только не простую. Клариссу, например. Пусть эта благородная киска в кладовой помурлычет, может, крысы от стыда сами уйдут.\"\n\nМелисса фыркает слишком громко, а Аманда смотрит на нее так, будто специально ждет грязной догадки. Сандра тут же хлопает ладонью по столу.\n\n\"Хватит мне ваших кошечек, кисок и ночных воздыханий,\" срезает она. \"Пальцы из пизд вынули обе и слушайте старших. Самоуспокоение закончится тем, что брат Герхард устроит вам дьявольское покаяние, а этого в доме никто не хочет. Крысы, мыши и чердак — вот о чем речь, а не о ваших мокрых фантазиях.\""
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Сказать, что сначала надо решить крыс и чердак":
            jump TavernKitchenBreakfastMelissaAmandaGerhardNatural

        "Не лезть в девичью перепалку":
            return
    return


label TavernKitchenBreakfastMelissaAmandaGerhardNatural:
    if not tavern_breakfast_melissa_amanda_gerhard_ready():
        return
    $ player.tavern_management.breakfast.melissa_amanda_gerhard_day = current_game_day()
    $ Melissa.change_social(friend_delta=1, open_delta=1)
    $ Amanda.change_social(friend_delta=1, open_delta=1)
    $ scene_runtime.text = "Вы обрываете спор и говорите, что сначала надо разобраться с настоящей грязью: крысы в кладовой, летучие мыши под крышей, щели на чердаке. Остальное за столом можно оставить для тех часов, когда дом не трещит по углам.\n\nСандра хмуро кивает. \"Вот это дело. Сначала хозяйство, потом девичьи смешки. Мелисса, хватит ныть — покажешь, где сильнее всего шуршит. Аманда, хватит мяукать про Клариссу — пойдешь помогать, если надо будет таскать тряпки и доски.\"\n\nАманда закатывает глаза, но спорить уже не решается. Мелисса бурчит себе под нос, зато видно: ей стало легче от того, что проблему наконец назвали вслух, а не превратили в очередную кухонную шутку.\n\nСандра под конец все равно добавляет, не удержавшись: \"И чтоб я ночью не слышала, как кто-то вместо сна себя утешает. Я вам не монастырь держу, но если брат Герхард услышит такие стоны, дьявола он будет искать не на чердаке.\""
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastAmandaAtticStop:
    $ Amanda.attic_mock_stopped = True
    $ Amanda.change_social(friend_delta=1)
    $ scene_runtime.text = "Вы наклоняетесь ближе и коротко говорите Аманде, что эту шутку пора оставить при себе. Она еще секунду держит дерзкий вид, потом опускает глаза к тарелке и тихо фыркает: \"Ладно. Поняла.\" После этого тема чердака за столом глохнет сама собой."
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastTease:
    $ renpy.dynamic("_tease_private_unlocked", "_tease_data", "_tease_girl", "_tease_tier", "_breakfast_tease_picture", "_tease_info")
    $ _tease_data = tavern_breakfast_tease_candidate()
    $ _tease_girl = str(_tease_data.get("girl", "") or "")
    $ _tease_tier = int(_tease_data.get("tier", 0) or 0)
    if _tease_girl == "":
        return
    if _tease_girl == "amanda":
        $ Amanda.breakfast_tease_day = current_game_day()
    else:
        $ Melissa.breakfast_tease_day = current_game_day()
    $ _breakfast_tease_picture = tavern_breakfast_tease_picture(_tease_girl, _tease_tier)
    if str(_breakfast_tease_picture or "").strip():
        vscene _breakfast_tease_picture
    if _tease_tier >= 4:
        $ scene_runtime.text = "{} приходит к завтраку настолько по-домашнему небрежной, что это уже похоже не на случайность, а на проверку ваших границ. Ночная ткань или плохо запахнутый домашний наряд оставляют слишком много поводов для взгляда, и она прекрасно видит, что вы это заметили.".format(people_display_name(_tease_girl))
        if int(threads["claraBookletMarket"].num or 0) >= 1 or bool(Clara.drawings_secret_known):
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nПосле историй о Клариссиных листках эта поза читается еще прямее: как будто кто-то нарочно примеряет на себя одну из тех непристойных сцен, только делает вид, что речь всего лишь о завтраке."
    elif _tease_tier >= 3:
        $ scene_runtime.text = "{} ловит ваш взгляд, чуть меняет позу за столом и дает понять, что сегодня под платьем у нее куда меньше защиты, чем принято показывать за завтраком. Это длится всего миг, но она явно рассчитывала, что вы заметите.".format(people_display_name(_tease_girl))
    elif _tease_tier >= 2:
        $ scene_runtime.text = "{} будто случайно садится смелее обычного: колено уходит в сторону, юбка натягивается, и вся поза становится скорее вызовом, чем неловкостью.".format(people_display_name(_tease_girl))
    else:
        $ scene_runtime.text = "{} незаметно приподнимает край юбки ровно настолько, чтобы вы успели заметить белье, а потом с невинным видом возвращается к завтраку.".format(people_display_name(_tease_girl))
    $ player_apply_arousal_trigger("breakfast_tease", 5 + _tease_tier)
    $ _tease_info = people.get_info(_tease_girl)
    if _tease_info is not None:
        $ _tease_info.add_arousal(3 + _tease_tier)
        $ _tease_info.change_social(corruption_delta=1)
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    $ _tease_private_unlocked = bool(_tease_info is not None and people_to_int(_tease_info.sex_stat("sexacts", 0), 0) > 0)
    if _tease_girl == "amanda":
        $ _tease_private_unlocked = _tease_private_unlocked or Amanda.var_int("suckyou", 0) == 1 or Amanda.var_int("fuckyou", 0) == 1
    elif _tease_girl == "melissa":
        $ _tease_private_unlocked = _tease_private_unlocked or threads["melissaBatProblem"].num >= 8
    if _tease_private_unlocked:
        "[scene_runtime.text]"
        menu:
            "Намекнуть на склад после завтрака":
                call TavernKitchenBreakfastTeasePrivate(_tease_girl, "storage")

            "Намекнуть на сарай после завтрака":
                call TavernKitchenBreakfastTeasePrivate(_tease_girl, "shed")

            "Сделать вид, что ничего не заметили":
                return
        return
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastTeasePrivate(girl_name="", place_code="storage"):
    $ renpy.dynamic("_tease_private_girl", "_tease_private_place", "_tease_private_info")
    $ _tease_private_girl = str(girl_name or "").strip().lower()
    $ _tease_private_place = "склад" if str(place_code or "") == "storage" else "сарай"
    $ _tease_private_info = people.get_info(_tease_private_girl)
    if _tease_private_info is not None:
        $ _tease_private_info.change_social(friend_delta=1, open_delta=1)
    $ scene_runtime.text = "{} понимает ваш намек про {} без лишних объяснений. Пока за столом еще шумят ложками и спорят о работе, она только коротко улыбается: этот разговор явно можно будет продолжить там, где никто не станет мешать.".format(people_display_name(_tease_private_girl), _tease_private_place)
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastTalkAbsent:
    $ renpy.dynamic("_absence_prompt")
    $ player.tavern_management.breakfast.absent_talk_day = current_game_day()
    $ _absence_prompt = tavern_breakfast_absent_prompt()
    if str(_absence_prompt or "").strip():
        $ scene_runtime.text = str(_absence_prompt or "") + "\n" + tavern_breakfast_absent_talk_text()
    else:
        $ scene_runtime.text = tavern_breakfast_absent_talk_text()
    $ scene_runtime.location_text = scene_runtime.text
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastMorningIssue:
    $ renpy.dynamic("_breakfast_issue_girl", "_breakfast_issue_code", "_breakfast_issue_name")
    $ _breakfast_issue_girl = str(tavern_breakfast_morning_issue_girl() or "").strip()
    if str(_breakfast_issue_girl or "") == "":
        return
    $ scene_runtime.text = tavern_breakfast_morning_issue_text(_breakfast_issue_girl)
    $ scene_runtime.location_text = scene_runtime.text
    $ _breakfast_issue_code = str(household_morning_issue_type(_breakfast_issue_girl) or "").strip()
    $ _breakfast_issue_name = _action_display_name(_breakfast_issue_girl)
    "[scene_runtime.text]"
    menu:
        "Проверить, не притворяется ли Аманда" if _breakfast_issue_girl == "amanda" and _breakfast_issue_code == "sick":
            call HouseholdAmandaFakeSicknessWake

        "Принести [_breakfast_issue_name] лечебное зелье" if _breakfast_issue_code == "sick" and int(player.item_count("healing_potion_001") or 0) > 0:
            call HouseholdMorningIssueCure(_breakfast_issue_girl)

        "Согреть [_breakfast_issue_name] пряной настойкой" if _breakfast_issue_code == "sick" and household_warm_drink_ready(_breakfast_issue_girl):
            call HouseholdMorningIssueWarmDrink(_breakfast_issue_girl)

        "Разбудить [_breakfast_issue_name]" if _breakfast_issue_code == "sleepy":
            call HouseholdWakeSleepyGirl(_breakfast_issue_girl)

        "Оставить это до конца завтрака":
            return
    return


label TavernKitchenBreakfastMarketTalk:
    $ player.tavern_management.breakfast.market_talk_day = current_game_day()
    if int(threads["cityBlindPirateFall"].num or 0) == 1:
        call TavernKitchenBreakfastBlindPirateStory
        return
    $ scene_runtime.text = tavern_breakfast_market_story_text()
    $ scene_runtime.location_text = scene_runtime.text
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastMotivation:
    $ player.tavern_management.breakfast.motivation_day = current_game_day()
    $ scene_runtime.text = tavern_breakfast_motivation_text()
    $ player.change_stat("fun", 1)
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastPerkMenu:
    $ renpy.dynamic("_perk_text", "_perk_day", "_special_milk_ready", "_special_ale_ready")
    if not tavern_breakfast_can_offer_perk_menu():
        return
    $ _perk_text = "Вы решаете, чем именно поделиться за общим столом, чтобы завтрак был не просто обязательной кашей, а живым домашним утром."
    $ tavern_breakfast_restore_ui_state(_perk_text)
    $ _perk_day = int(calendar_v2.daysInGame or 0)
    $ _special_milk_ready = int(player.tavern_management.breakfast.blind_pirate_team_pledge or 0) == 1 and int(player.tavern_management.breakfast.milk_team_talk_done or 0) == 0 and int(player.tavern_management.breakfast.food_perk_day or -1) != _perk_day and (tavern_kitchen_food_stock_count("milk_pitcher_001") > 0 or int(player.item_count("milk_pitcher_001") or 0) > 0)
    $ _special_ale_ready = int(player.tavern_management.breakfast.blind_pirate_team_pledge or 0) == 1 and int(player.tavern_management.breakfast.milk_team_talk_done or 0) == 1 and int(player.tavern_management.breakfast.ale_team_talk_done or 0) == 0 and int(player.tavern_management.breakfast.drink_perk_day or -1) != _perk_day and int(player.item_count("drink_ale_001") or 0) > 0
    "[_perk_text]"
    menu:
        "Поделиться молоком" if _special_milk_ready:
            call TavernKitchenBreakfastPerkFood("milk_pitcher_001")

        "Поделиться элем за команду" if _special_ale_ready:
            call TavernKitchenBreakfastPerkDrink("drink_ale_001")

        "Поставить на стол лучшие припасы" if not _special_milk_ready and int(player.tavern_management.breakfast.food_perk_day or -1) != _perk_day and tavern_breakfast_food_perk_item_available():
            call TavernKitchenBreakfastPerkFood

        "Поделиться напитком" if not _special_ale_ready and int(player.tavern_management.breakfast.drink_perk_day or -1) != _perk_day and tavern_breakfast_drink_perk_item_available():
            call TavernKitchenBreakfastPerkDrink

        "Подкинуть тему про новые непристойные листки" if int(player.tavern_management.breakfast.lewd_series_day or -1) != _perk_day and tavern_breakfast_lewd_series_available():
            call TavernKitchenBreakfastPerkLewdSeries

        "Назад к завтраку":
            return
    return


label TavernKitchenBreakfastLookAtGirl(girl_name=""):
    $ renpy.dynamic("_breakfast_look_girl", "_breakfast_look_picture")
    $ _breakfast_look_girl = str(girl_name or "").strip().lower()
    if _breakfast_look_girl not in list(tavern_breakfast_present_ids() or []):
        return
    $ _breakfast_look_picture = tavern_breakfast_look_picture(_breakfast_look_girl)
    if str(_breakfast_look_picture or "").strip():
        vscene _breakfast_look_picture
    $ scene_runtime.text = tavern_breakfast_look_text(_breakfast_look_girl)
    $ scene_runtime.location_text = scene_runtime.text
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastPerkFood(item_id=""):
    $ renpy.dynamic("_breakfast_food_choice")
    $ _breakfast_food_choice = [str(item_id or "").strip()] if str(item_id or "").strip() else None
    $ scene_runtime.text = tavern_breakfast_apply_food_perk(_breakfast_food_choice)
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastPerkDrink(item_id=""):
    $ renpy.dynamic("_breakfast_drink_choice")
    $ _breakfast_drink_choice = [str(item_id or "").strip()] if str(item_id or "").strip() else None
    $ scene_runtime.text = tavern_breakfast_apply_drink_perk(_breakfast_drink_choice)
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastPerkLewdSeries:
    $ scene_runtime.text = tavern_breakfast_apply_lewd_series_perk()
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastPerkAppearance:
    $ scene_runtime.text = tavern_breakfast_apply_appearance_perk()
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastServeSpicyDrink:
    if not tavern_breakfast_can_serve_spicy_tincture():
        return
    $ player.tavern_management.breakfast.spicy_drink_day = current_game_day()
    $ scene_runtime.text = tavern_kitchen_spicy_tincture_apply(tavern_breakfast_present_ids())
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastBlindPirateStory:
    $ player.tavern_management.breakfast.blind_pirate_team_pledge = 1
    $ scene_runtime.text = tavern_breakfast_blind_pirate_story_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ player.change_stat("fun", 5)
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    $ threads["cityBlindPirateFall"].advance()
    return


label TavernKitchenBreakfastAnnounceGeorgetteLiza:
    $ player.tavern_management.breakfast.georgett_liza_pending = 0
    $ scene_runtime.text = "Вы даете за столом договорить всем до конца, а затем коротко объявляете, что Жоржетта с Лизеттой отныне будут жить и работать у вас в трактире.\n\nКогда по кухне проходит первый тяжелый шум, вы тут же пресекаете его и холодно напоминаете, чем закончилась судьба «Слепого Пирата». Если кому-то из присутствующих хочется проверить, не ждет ли ее галера, долговая яма или продажа в блудный дом, вы не станете никого удерживать. Но пока дом держится на вас, порядок здесь решаете вы.\n\nПосле этих слов разговор за столом резко остывает."
    if "sandra" in list(tavern_breakfast_present_ids() or []):
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nСандра первая берет себя в руки. Она явно недовольна, но вместо скандала только сухо замечает, что тогда новых баб надо сразу встраивать в хозяйственный распорядок и следить, чтобы они не развалили дом изнутри."
    if "melissa" in list(tavern_breakfast_present_ids() or []):
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nМелисса заметно бледнеет от вашей жесткости, но спорить не решается. По ее лицу видно, что она поняла сказанное слишком хорошо и теперь старается только не выдать своего страха лишним словом."
    if "amanda" in list(tavern_breakfast_present_ids() or []):
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nАманда сперва открывает рот для колкости, но, встретившись с вашим взглядом, только отводит глаза и начинает нервно вертеть ложку в пальцах."
    if "becky" in list(tavern_breakfast_present_ids() or []):
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nБекки хмуро косится на остальных и, похоже, предпочитает не подливать масла в огонь: вдова слишком хорошо знает, как быстро в городе рушатся дома, где хозяин теряет хватку."
    $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nЖоржетта держится с показным достоинством, а Лизетта жмется к матери чуть ближе обычного. Вы же на этом обрываете завтрак и даете понять, что разговор окончен."
    $ scene_runtime.location_text = scene_runtime.text
    $ player.change_stat("rebellion", -1)
    $ Sandra.change_rebellion(-1, "breakfast_georgette_liza_order")
    $ Melissa.change_rebellion(-1, "breakfast_georgette_liza_order")
    $ Amanda.change_rebellion(-1, "breakfast_georgette_liza_order")
    $ player.change_stat("fun", 1)
    call stat
    call TavernKitchenBreakfastShowText(scene_runtime.text)
    return


label TavernKitchenBreakfastDanceMenu:
    $ renpy.dynamic("_dance_text")
    $ _dance_text = "За столом приходится быстро решить, готовы ли вы вложиться в пятничные танцы вином и закуской или пока отступите."
    $ tavern_breakfast_restore_ui_state(_dance_text)
    "[_dance_text]"
    menu:
        "Отправить вино и начать готовить закуску" if wine_for_dance_can_sponsor():
            call WineForDanceOutcome(1)

        "Посокрушаться о нехватке запасов" if not wine_for_dance_can_sponsor():
            call WineForDanceOutcome(2)

        "Отказаться":
            call WineForDanceOutcome(3)

        "Назад к завтраку":
            return
    return


label TavernKitchenFinishBreakfastEvent:
    $ renpy.dynamic("_kitchen_scene")
    $ player.tavern_management.breakfast.event_active = False
    $ player.tavern_management.breakfast.base_text = ""
    $ player.tavern_management.breakfast.base_shown_day = -1
    $ player.tavern_management.breakfast.present_ids = None
    $ _kitchen_scene = tavern_kitchen_picture() or getattr(rooms.current, "bg_picture", "") or ""
    if str(_kitchen_scene or "").strip():
        vscene _kitchen_scene
    $ scene_runtime.text = build_kitchen_description()
    $ scene_runtime.location_text = scene_runtime.text
    $ tavern_kitchen_set_saved_text(scene_runtime.text)
    $ main_ui_runtime.action_title = "Кухня"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    show screen main_ui
    return


label TavernKitchenSundayDinnerMenu:
    if not tavern_sunday_dinner_available():
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
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
            $ main_ui_runtime.action_items = tavern_kitchen_action_items()
            return


label TavernKitchenSundayDinner(serve_spicy=0):
    $ renpy.dynamic("_eat_result", "_sunday_present_ids", "_sunday_social_ids", "_sunday_lines")
    if not tavern_sunday_dinner_available():
        $ scene_runtime.text = "Сегодня вы уже сидели за воскресным обедом."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = tavern_kitchen_action_items()
        return
    $ _sunday_present_ids = list(tavern_sunday_dinner_present_ids() or [])
    $ player.tavern_management.breakfast.sunday_dinner_last_day = current_game_day()
    vscene tavern_kitchen_sunday_dinner_picture()
    python:
        _sunday_lines = [
            "К полудню кухня собирает всех на более основательную воскресную трапезу.",
            "За столом сидят: " + (", ".join(tavern_sunday_dinner_present_names()) if len(tavern_sunday_dinner_present_names()) > 0 else "пока что только вы сами") + ".",
            "На некоторое время трактирная суета отступает, и весь дом живет одним общим столом.",
        ]
        _sunday_lines.extend(tavern_sunday_dinner_dialogue_lines())
        scene_runtime.text = "\n\n".join([row for row in _sunday_lines if str(row or "").strip()])
        scene_runtime.location_text = scene_runtime.text
    $ _eat_result = player_eat_meal("воскресный обед для всей челяди", 22, 45)
    if str(_eat_result.get("text", "") or "").strip():
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n" + str(_eat_result.get("text", "") or "")
        $ scene_runtime.location_text = scene_runtime.text
    $ _sunday_social_ids = tavern_sunday_dinner_apply_social_bonus(_sunday_present_ids)
    if len(list(tavern_recent_barber_ids() or [])) > 0:
        $ player.tavern_management.breakfast.sunday_dinner_barber_talk_day = current_game_day()
    if len(list(_sunday_social_ids or [])) > 0:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\nСпокойный воскресный стол немного сближает вас с теми, кто сейчас обедает вместе с вами."
        $ scene_runtime.location_text = scene_runtime.text
    if int(serve_spicy or 0) == 1 and tavern_sunday_dinner_can_serve_spicy_tincture(_sunday_present_ids):
        $ player.tavern_management.breakfast.sunday_dinner_spicy_drink_day = current_game_day()
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n" + tavern_kitchen_spicy_tincture_apply(_sunday_present_ids)
        $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    call stat
    $ main_ui_runtime.action_items = tavern_kitchen_action_items()
    show screen main_ui
    return
