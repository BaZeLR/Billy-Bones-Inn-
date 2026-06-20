# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default AmandaIntentMemory = {}
default AmandaIntentSeen = {}
default AmandaIntentLastState = {}
default AmandaDailyWorkReports = {}
default AmandaPreferenceKnown = {}
default AmandaPreferenceWeights = {}
default AmandaNeedBlocked = {}
default AmandaIntentRoomPresence = {}
default AmandaIntentLastText = ""
default AmandaMiniEventSeen = {}
default AmandaMiniEventMemory = {}
default AmandaMiniEventLastState = {}
default AmandaMiniEventLastCode = ""
default AmandaMiniEventLastLocation = ""
default AmandaMiniEventQueued = {}
default BadLandlordScore = 0
default TavernUncleTruthStage = 0
default AmandaAIIntegrationEnabled = True

init 5 python:
    import importlib.util
    import os
    import renpy.store as store

    AmandaIntentModel = None
    AmandaIntentLoadError = ""

    def amanda_ai_load_model():
        path = os.path.join(renpy.config.gamedir, "Utilities", "General", "NPC", "AmandaIntent_ren.py")
        spec = importlib.util.spec_from_file_location("tractir_amanda_intent_model", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    try:
        AmandaIntentModel = amanda_ai_load_model()
    except Exception as _amanda_ai_error:
        AmandaIntentModel = None
        AmandaIntentLoadError = str(_amanda_ai_error)

    def amanda_ai_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return int(default or 0)

    def amanda_ai_clamp(value, low=0, high=100):
        return max(int(low), min(int(high), amanda_ai_int(value, low)))

    def amanda_ai_available():
        return AmandaIntentModel is not None

    def amanda_ai_day_key(day_value=None):
        return str(amanda_ai_int(dayspassed if day_value is None else day_value, 0))

    def amanda_ai_seen_key(intent_code="", location_code=""):
        return "%s|%s|%s" % (amanda_ai_day_key(), str(location_code or ""), str(intent_code or ""))

    def amanda_ai_seen_today(intent_code="", location_code=""):
        return int(AmandaIntentSeen.get(amanda_ai_seen_key(intent_code, location_code), 0) or 0) == 1

    def amanda_ai_mark_seen(intent_code="", location_code=""):
        AmandaIntentSeen[amanda_ai_seen_key(intent_code, location_code)] = 1

    def amanda_ai_cycle_offset():
        try:
            row = DateOfBirth.get("amanda", {}) or {}
            return amanda_ai_int(row.get("day", 7), 7)
        except Exception:
            return 7

    def amanda_ai_cycle_state():
        if amanda_ai_available() and hasattr(AmandaIntentModel, "amanda_cycle_state"):
            return AmandaIntentModel.amanda_cycle_state(amanda_ai_int(dayspassed, 0), amanda_ai_cycle_offset())
        return {"day": 0, "phase": "steady", "desire": 0.10, "rest": 0.20, "safety": 0.45, "fertility": 0.45}

    def amanda_ai_body_state_bonus():
        cycle = amanda_ai_cycle_state()
        phase = str(cycle.get("phase", "steady") or "steady")
        wet_bonus = 0
        arousal_bonus = 0
        need_bandage = 0
        tags = []

        if phase == "critical":
            need_bandage = 1
            tags.append("critical")
        elif phase == "fertile":
            wet_bonus += 12
            arousal_bonus += 8
            tags.append("fertile")
        elif phase == "restless":
            wet_bonus += 6
            arousal_bonus += 5
            tags.append("restless")

        try:
            if tavern_kitchen_fertility_bonus_active():
                wet_bonus += 8
                arousal_bonus += 6
                tags.append("honey_milk")
            else:
                if tavern_kitchen_honey_bonus_active():
                    wet_bonus += 3
                    arousal_bonus += 2
                    tags.append("honey")
                if tavern_kitchen_milk_bonus_active():
                    wet_bonus += 2
                    arousal_bonus += 1
                    tags.append("milk")
        except Exception:
            pass

        try:
            if int(TavernBreakfastSpicyDrinkDay or -1) == int(dayspassed or 0):
                wet_bonus += 18
                arousal_bonus += 15
                tags.append("spiced")
        except Exception:
            pass

        return {
            "phase": phase,
            "cycle_day": amanda_ai_int(cycle.get("day", 0), 0),
            "wet_bonus": max(0, int(wet_bonus or 0)),
            "arousal_bonus": max(0, int(arousal_bonus or 0)),
            "need_bandage": int(need_bandage or 0),
            "tags": tags,
        }

    def amanda_ai_body_state_stamp(state=None):
        row = dict(state or amanda_ai_body_state_bonus())
        return "%s:%s:%s:%s:%s" % (
            amanda_ai_int(dayspassed, 0),
            str(row.get("phase", "steady") or "steady"),
            amanda_ai_int(row.get("wet_bonus", 0), 0),
            amanda_ai_int(row.get("arousal_bonus", 0), 0),
            ",".join(list(row.get("tags", []) or [])),
        )

    def amanda_ai_apply_visible_body_state():
        state = amanda_ai_body_state_bonus()
        stamp = amanda_ai_body_state_stamp(state)
        if str(AmandaVar.get("body_state_stamp", "") or "") == stamp:
            return state
        AmandaVar["body_state_stamp"] = stamp
        AmandaVar["cycle_phase"] = str(state.get("phase", "steady") or "steady")
        AmandaVar["cycle_day"] = amanda_ai_int(state.get("cycle_day", 0), 0)
        AmandaVar["needs_bandage"] = amanda_ai_int(state.get("need_bandage", 0), 0)
        if amanda_ai_int(state.get("wet_bonus", 0), 0) > 0:
            PussyWetStart["amanda"] = min(100, max(0, amanda_ai_int(PussyWetStart.get("amanda", 0), 0) + amanda_ai_int(state.get("wet_bonus", 0), 0)))
        if amanda_ai_int(state.get("arousal_bonus", 0), 0) > 0:
            Arousal["amanda"] = min(100, max(0, amanda_ai_int(Arousal.get("amanda", 0), 0) + amanda_ai_int(state.get("arousal_bonus", 0), 0)))
        return state

    def amanda_ai_body_state_line():
        state = amanda_ai_apply_visible_body_state()
        phase = str(state.get("phase", "steady") or "steady")
        wet_value = max(amanda_ai_int(PussyWetStart.get("amanda", 0), 0), amanda_ai_int(Arousal.get("amanda", 0), 0))
        tags = list(state.get("tags", []) or [])
        lines = []
        if phase == "critical":
            lines.append("У Аманды сегодня критические дни. Она бледнее обычного, старается не двигаться резко и прямо нуждается в чистых тряпках или бинтах; если заставить ее бегать как обычно, она будет злее, слабее и менее послушной.")
        elif phase == "fertile":
            if wet_value >= 35:
                lines.append("Аманда сейчас в плодной части цикла и уже заметно мокрая. Она сжимает бедра, ерзает, слишком быстро краснеет от прямого взгляда и хуже прячет возбуждение, когда разговор касается тела, наград или ночных визитов.")
            else:
                lines.append("Аманда в плодной части цикла. Ее тело быстрее откликается на запахи, взгляды и обещания; она еще держит себя в руках, но возбуждается легче обычного.")
        elif phase == "restless":
            lines.append("Аманда сегодня заведена и беспокойна. Она чаще трогает платье, хуже сидит смирно и явно ищет повод, чтобы кто-нибудь заметил ее как девушку, а не как работницу.")
        if "honey_milk" in tags:
            lines.append("Молоко с медом усиливает жар: грудь и низ живота у нее реагируют быстрее, трусики становятся влажнее, а обычная болтовня за столом легче превращается в провокацию.")
        elif "honey" in tags:
            lines.append("Мед делает ее мягче и смелее: Аманда лениво улыбается, дольше держит взгляд и охотнее играет на грани приличия.")
        elif "milk" in tags:
            lines.append("После молока она теплеет и расслабляется; забота телом доходит до нее быстрее, чем строгие слова.")
        if "spiced" in tags:
            lines.append("Пряная настойка бьет прямо по похоти: у Аманды теплеют щеки, дыхание сбивается, между ног становится мокро, и ей уже трудно изображать, будто это просто хороший завтрак.")
        return "\n\n".join(lines)

    def amanda_ai_assigned(job_map, job_name):
        try:
            return str(job_map.get("amanda", "") or "").strip().lower() == str(job_name or "").strip().lower()
        except Exception:
            return False

    def amanda_ai_job_result(skill_value=0, assigned=False, day_value=0, salt=1):
        if not assigned:
            return "none"
        skill = amanda_ai_int(skill_value, 0)
        drift = ((amanda_ai_int(day_value, 0) + 3) * int(salt or 1)) % 23
        score = skill + drift - 8
        if score >= 34:
            return "good"
        if score <= 10:
            return "bad"
        return "ordinary"

    def amanda_ai_work_report(day_value=None):
        key = amanda_ai_day_key(day_value)
        if key in AmandaDailyWorkReports:
            return dict(AmandaDailyWorkReports.get(key, {}) or {})
        day_number = amanda_ai_int(dayspassed if day_value is None else day_value, 0)
        cleaning_result = amanda_ai_job_result(cleaning.get("amanda", 0), amanda_ai_assigned(jobcleaning, "amanda"), day_number, 5)
        waitress_result = amanda_ai_job_result(waitress.get("amanda", 0), amanda_ai_assigned(jobwaitress, "amanda"), day_number, 7)
        cooking_result = amanda_ai_job_result(cooking.get("amanda", 0), amanda_ai_assigned(jobkitchen, "amanda"), day_number, 11)
        bad_count = len([row for row in (cleaning_result, waitress_result, cooking_result) if row == "bad"])
        good_count = len([row for row in (cleaning_result, waitress_result, cooking_result) if row == "good"])
        report = {
            "cleaning": cleaning_result,
            "waitress": waitress_result,
            "cooking": cooking_result,
            "complaints": bad_count,
            "rude_clients": 1 if waitress_result == "bad" else 0,
            "tips": max(0, good_count * 3 + (2 if waitress_result == "good" else 0)),
        }
        AmandaDailyWorkReports[key] = report
        return dict(report)

    def amanda_ai_recent_barber_done():
        try:
            return int(BarberVisitLastDay.get("amanda", -99) or -99) >= 0
        except Exception:
            return False

    def amanda_ai_dress_reward_done():
        return (
            int(AmandaVar.get("revealing_dress_ordered", 0) or 0) > 0
            or int(AmandaVar.get("dress_request_satisfied", 0) or 0) > 0
        )

    def amanda_ai_beauty_help_satisfied():
        barber_done = amanda_ai_recent_barber_done()
        soap_done = int(AmandaVar.get("soap_sample_received", 0) or 0) > 0 or int(AmandaVar.get("soap_used", 0) or 0) > 0
        return barber_done and (soap_done or amanda_ai_dress_reward_done())

    def amanda_ai_beauty_missing_lines():
        lines = []
        if not amanda_ai_recent_barber_done():
            lines.append("Серджио")
        if int(AmandaVar.get("soap_sample_received", 0) or 0) <= 0 and int(AmandaVar.get("soap_used", 0) or 0) <= 0:
            lines.append("хорошего мыла")
        if not amanda_ai_dress_reward_done():
            lines.append("платья или примерки у Ирмы")
        return lines

    def amanda_ai_barber_result_line():
        if not amanda_ai_recent_barber_done():
            return ""
        return "После Серджио Аманда выглядит заметно иначе: волосы аккуратно уложены, кожа пахнет душистой водой, ноги под чулками кажутся гладкими, а движения стали увереннее. Она уже получила этот уход и больше не должна просить о том же самом."

    def amanda_ai_clothing_line(location_code="", intent_code=""):
        loc = str(location_code or CurLoc or "")
        intent = str(intent_code or "")
        top = str(topdress.get("amanda", "") or "")
        bottom = str(bottomdress.get("amanda", "") or "")
        if loc == "TavernMyRoom" and (amanda_ai_int(hour, 0) >= 20 or amanda_ai_int(time, 0) >= 3):
            return "На ней ночная сорочка, не рабочее платье; поэтому вся ее игра строится на тонкой ткани, распущенных волосах и том, как она держит подол, а не на задирании дневной юбки."
        if loc == "TavernKitchen" or int(jobkitchen.get("amanda", 0) or 0) != 0:
            return "На Аманде рабочее кухонное платье: ткань пахнет жаром, мукой и дымом, так что ее просьбы сейчас звучат как часть утренней домашней суеты, а не как ночная игра."
        if int(jobwaitress.get("amanda", 0) or 0) != 0:
            return "На ней платье для зала, чуть аккуратнее обычного: она явно помнит, что чаевые зависят от того, как гости смотрят на нее."
        if int(jobcleaning.get("amanda", 0) or 0) != 0:
            return "На ней простое рабочее платье для уборки; если она играет вниманием, то делает это грязными руками и упрямым взглядом, а не нарядной позой."
        if top or bottom:
            return "Одежда на Аманде сейчас не нейтральна: она поправляет ткань так, будто проверяет, заметите ли вы ее вид."
        return ""

    def amanda_ai_appearance_context():
        hygiene = 0.15
        skin = 0.10
        scent = 0.10
        hair = 0.10
        grooming = 0.05
        dress = 0.15
        manners = 0.10
        clara_training = 0.0
        if int(AmandaVar.get("soap_sample_received", 0) or 0) > 0 or int(AmandaVar.get("soap_used", 0) or 0) > 0:
            hygiene += 0.35
            scent += 0.25
            skin += 0.20
        if int(AmandaVar.get("barber_visit_day", -1) or -1) >= 0 or int(AmandaVar.get("barber_treatment", 0) or 0) > 0:
            hair += 0.35
            grooming += 0.35
        if int(AmandaVar.get("revealing_dress_ordered", 0) or 0) > 0 or int(AmandaVar.get("dress_request_satisfied", 0) or 0) > 0:
            dress += 0.35
        if int(Clara.var.get("paintings_confession", 0) or 0) > 0 or int(Clara.var.get("courtesan_lessons", 0) or 0) > 0:
            manners += 0.30
            clara_training += 0.35
        return {
            "hygiene": min(1.0, hygiene),
            "skin": min(1.0, skin),
            "scent": min(1.0, scent),
            "hair": min(1.0, hair),
            "body_grooming": min(1.0, grooming),
            "dress": min(1.0, dress),
            "manners": min(1.0, manners),
            "clara_training": min(1.0, clara_training),
        }

    def amanda_ai_witnesses(location_code=""):
        loc = str(location_code or "")
        if loc == "TavernKitchen" and bool(TavernBreakfastEventActive):
            return [row for row in list(tavern_breakfast_present_ids() or []) if str(row or "") != "amanda"]
        return [row for row in list(getNPCids(loc) or []) if str(row or "") != "amanda"]

    def amanda_ai_context(location_code="", mode="room"):
        loc = str(location_code or CurLoc or "")
        body_state = amanda_ai_apply_visible_body_state()
        friend_value = amanda_ai_int(Friends.get("amanda", 0), 0)
        open_value = amanda_ai_int(otkroven.get("amanda", 0), 0)
        slut_value = amanda_ai_int(sluttiness.get("amanda", 0), 0)
        wet_value = amanda_ai_int(PussyWetStart.get("amanda", 0), 0)
        blocked = amanda_ai_int(AmandaNeedBlocked.get("amanda", 0), 0)
        return {
            "location": loc,
            "mode": str(mode or "room"),
            "day": amanda_ai_int(dayspassed, 0),
            "hour": amanda_ai_int(hour, amanda_ai_int(time, 0) * 6),
            "cycle_offset": amanda_ai_cycle_offset(),
            "witnesses": amanda_ai_witnesses(loc),
            "friend": friend_value,
            "openness": open_value,
            "sexual_openness": slut_value,
            "arousal": amanda_ai_int(Arousal.get("amanda", 0), 0),
            "wetness": wet_value,
            "anger": relationship_anger("amanda"),
            "rebel": amanda_ai_int(neshlush.get("amanda", 0), 0),
            "pregnancy": amanda_ai_int(pregnancy.get("amanda", 0), 0),
            "amanda_var": dict(AmandaVar or {}),
            "daily_work_report": amanda_ai_work_report(),
            "appearance": amanda_ai_appearance_context(),
            "beauty_help_satisfied": 1 if amanda_ai_beauty_help_satisfied() else 0,
            "preference_known": dict(AmandaPreferenceKnown or {}),
            "preference_weights": dict(AmandaPreferenceWeights or {}),
            "money_pressure": 1.0 if int(money or 0) < 250 else (0.55 if int(money or 0) < 900 else 0.25),
            "household_order": 0.65 if int(taverncleanliness or 0) >= 35 else 0.35,
            "attention_gap": min(1.0, (0.7 if int(TalkedToday.get("amanda", 0) or 0) <= 0 else 0.2) + (0.15 if "spiced" in list(body_state.get("tags", []) or []) else 0.0)),
            "jealousy": min(1.0, float(amanda_ai_int(AmandaVar.get("jealousy", 0), 0)) / 10.0),
            "player_blocked_recent_need": blocked,
            "melissa_friend": amanda_ai_int(Friends.get("melissa", 0), 0),
            "household_pressure": amanda_ai_household_value("pressure", 0.0),
            "household_friction": amanda_ai_household_value("friction", 0.0),
            "household_convergence": amanda_ai_household_value("convergence", 0.0),
            "external_threat": amanda_ai_household_value("external_threat", 0.0),
            "amanda_drive": amanda_ai_household_npc_value("amanda", "drive", 0.0),
            "sandra_drive": amanda_ai_household_npc_value("sandra", "drive", 0.0),
            "melissa_drive": amanda_ai_household_npc_value("melissa", "drive", 0.0),
            "assigned_work": amanda_ai_assigned_work_name(),
            "cloth_access": amanda_ai_float_access("cloth_supply", 0.0),
            "food_security": amanda_ai_food_security(),
        }

    def amanda_ai_choose(location_code="", mode="room", threshold=0.35):
        if not amanda_ai_available():
            return {}
        state = AmandaIntentModel.amanda_choose_intent(amanda_ai_context(location_code, mode), AmandaIntentMemory, threshold)
        AmandaIntentLastState.clear()
        AmandaIntentLastState.update(state)
        return state

    def amanda_ai_chosen_intent(location_code="", mode="room", threshold=0.35):
        state = amanda_ai_choose(location_code, mode, threshold)
        chosen = state.get("chosen", None) if isinstance(state, dict) else None
        if not chosen:
            return ""
        return str(chosen.get("intent", "") or "")

    def amanda_ai_breakfast_intent_code():
        if not amanda_ai_available():
            return ""
        if not bool(TavernBreakfastEventActive):
            return ""
        if "amanda" not in list(tavern_breakfast_present_ids() or []):
            return ""
        intent = amanda_ai_chosen_intent("TavernKitchen", "breakfast", 0.38)
        if intent not in ("ask_player_money", "ask_player_beauty_help", "ask_player_reward_for_work", "ask_legare_help", "obey_and_work", "avoid_work"):
            return ""
        if intent == "ask_player_beauty_help" and amanda_ai_beauty_help_satisfied():
            return ""
        if intent == "ask_player_reward_for_work" and int(AmandaVar.get("work_reward_day", -1) or -1) == amanda_ai_int(dayspassed, 0):
            return ""
        if amanda_ai_seen_today(intent, "TavernKitchen"):
            return ""
        return intent

    def amanda_ai_my_room_private_unlocked():
        breakfast_terms = (
            int(AmandaVar.get("beauty_help_terms_accepted", 0) or 0) == 1
            and int(TavernBreakfastBlindPirateTeamPledge or 0) == 1
        )
        established = (
            int(AmandaVar.get("night_tease_seen", 0) or 0) == 1
            or int(AmandaVar.get("first_night_tease_hooked", 0) or 0) == 1
            or int(AmandaVar.get("suckyou", 0) or 0) == 1
            or int(AmandaVar.get("fuckyou", 0) or 0) == 1
            or int(AmandaVar.get("knowsexactive", 0) or 0) == 1
            or int(HadSex.get("amanda", 0) or 0) > 0
        )
        return breakfast_terms or established

    def amanda_ai_room_schedule_active():
        row = dict(AmandaIntentRoomPresence or {})
        return (
            int(row.get("day", -1) or -1) == amanda_ai_int(dayspassed, 0)
            and str(row.get("location", "") or "").strip() != ""
        )

    def amanda_ai_room_presence_intent(location_code=""):
        loc = str(location_code or CurLoc or "").strip()
        row = dict(AmandaIntentRoomPresence or {})
        if not amanda_ai_room_schedule_active():
            return ""
        if loc and str(row.get("location", "") or "").strip() != loc:
            return ""
        return str(row.get("intent", "") or "")

    def amanda_ai_place_in_room(location_code="", intent_code=""):
        loc = str(location_code or "").strip()
        if loc == "":
            return
        AmandaIntentRoomPresence.clear()
        AmandaIntentRoomPresence.update({
            "day": amanda_ai_int(dayspassed, 0),
            "week": amanda_ai_int(week, 0),
            "slot": amanda_ai_int(time, 0),
            "location": loc,
            "intent": str(intent_code or ""),
        })
        try:
            rows = []
            for entry in list(npc_schedule_list("amanda") or []):
                if str(getattr(entry, "label", "") or "") != "amanda_ai_room_presence":
                    rows.append(entry)
            rows.append(NPCScheduleEntry(
                location=loc,
                weekdays=[amanda_ai_int(week, 0)],
                time_slots=[amanda_ai_int(time, 0)],
                awake=True,
                talkable=True,
                condition=amanda_ai_room_schedule_active,
                priority=950,
                label="amanda_ai_room_presence",
            ))
            npc_schedule_set("amanda", rows)
        except Exception:
            pass
        CurrentLoc["amanda"] = loc

    def amanda_ai_clear_room_presence(location_code=""):
        loc = str(location_code or "").strip()
        row = dict(AmandaIntentRoomPresence or {})
        if loc and str(row.get("location", "") or "").strip() != loc:
            return
        AmandaIntentRoomPresence.clear()
        try:
            rows = []
            for entry in list(npc_schedule_list("amanda") or []):
                if str(getattr(entry, "label", "") or "") != "amanda_ai_room_presence":
                    rows.append(entry)
            npc_schedule_set("amanda", rows)
            _amanda_ai_restore_loc = str(npc_schedule_location("amanda") or "")
            if _amanda_ai_restore_loc and _amanda_ai_restore_loc != loc:
                CurrentLoc["amanda"] = _amanda_ai_restore_loc
            elif loc and str(CurrentLoc.get("amanda", "") or "") == loc:
                CurrentLoc["amanda"] = "TavernAmandaRoom"
        except Exception:
            if loc and str(CurrentLoc.get("amanda", "") or "") == loc:
                CurrentLoc["amanda"] = "TavernAmandaRoom"

    def amanda_ai_room_intent_code(location_code="", allow_arrival=False):
        loc = str(location_code or CurLoc or "")
        presence_intent = amanda_ai_room_presence_intent(loc)
        if presence_intent:
            return presence_intent
        if not amanda_ai_available():
            return ""
        intent = amanda_ai_chosen_intent(loc, "room", 0.42)
        if intent not in ("private_tease_player", "visit_player_room", "seek_private_satisfaction", "expect_spanking", "ask_player_money", "ask_player_beauty_help", "ask_player_reward_for_work", "ask_melissa_loan_or_favor", "ask_legare_help"):
            return ""
        if loc == "TavernMyRoom" and intent in ("private_tease_player", "visit_player_room"):
            if not amanda_ai_my_room_private_unlocked():
                return ""
        if loc != "TavernMyRoom" and intent == "visit_player_room":
            return ""
        if amanda_ai_seen_today(intent, loc):
            return ""
        if "amanda" not in list(getNPCids(loc) or []):
            if bool(allow_arrival) and loc == "TavernMyRoom" and intent in ("private_tease_player", "visit_player_room", "seek_private_satisfaction", "expect_spanking"):
                amanda_ai_place_in_room(loc, intent)
            if "amanda" not in list(getNPCids(loc) or []):
                return ""
        return intent

    def amanda_ai_menu_label(intent_code=""):
        labels = {
            "ask_player_money": "Аманда просит денег",
            "ask_player_beauty_help": "Аманда просит помочь с красотой",
            "ask_player_reward_for_work": "Аманда ждет похвалы за работу",
            "ask_melissa_loan_or_favor": "Аманда шепчется о займе у Мелиссы",
            "ask_legare_help": "Аманда думает о помощи Легара",
            "private_tease_player": "Спросить Аманду, что она здесь делает",
            "visit_player_room": "Спросить Аманду, что она здесь делает",
            "seek_private_satisfaction": "Спросить Аманду, что с ней",
            "expect_spanking": "Аманда ждет наказания",
            "obey_and_work": "Потребовать улучшить работу",
            "avoid_work": "Аманда пытается уйти от работы",
        }
        return labels.get(str(intent_code or ""), "Аманда хочет поговорить")

    def amanda_ai_status_line():
        state = AmandaIntentLastState if isinstance(AmandaIntentLastState, dict) else {}
        profile = state.get("profile", {}) if isinstance(state, dict) else {}
        needs = state.get("needs", {}) if isinstance(state, dict) else {}
        if not amanda_ai_available() or not isinstance(profile, dict) or not isinstance(needs, dict):
            return ""
        visible = AmandaIntentModel.amanda_visible_status(profile, needs)
        labels = list(visible.get("labels", []) or [])
        body_line = amanda_ai_body_state_line()
        if body_line:
            return body_line
        if "worked_well" in labels:
            return "Сегодня Аманда держится увереннее: она явно помнит, что справилась с делом."
        if "work_trouble" in labels:
            return "Аманда старается выглядеть невинно, но по ее лицу видно: с работой опять вышло не гладко."
        if "wants_attention_to_appearance" in labels:
            missing = amanda_ai_beauty_missing_lines()
            if len(missing) > 0:
                return "Аманда то и дело поправляет волосы и платье, словно ждет, заметите ли вы, чего ей еще не хватает: " + ", ".join(missing) + "."
            return amanda_ai_barber_result_line()
        if "restless" in labels:
            return "Аманда сегодня заведена: взгляд задерживается дольше обычного, а улыбка становится слишком личной."
        if "money_pressure" in labels:
            return "Аманда осторожно считает в уме будущие расходы и ищет момент, чтобы попросить у вас поддержку."
        return ""

    def amanda_ai_private_setup_text(intent_code="", location_code=""):
        intent = str(intent_code or "")
        loc = str(location_code or CurLoc or "")
        hour_value = amanda_ai_int(hour, 0)
        slot_value = amanda_ai_int(time, 0)
        is_late = hour_value >= 20 or slot_value >= 3

        if loc == "TavernMyRoom" and intent in ("visit_player_room", "private_tease_player"):
            if is_late and int(AmandaVar.get("night_tease_seen", 0) or 0) == 0 and int(AmandaVar.get("beauty_help_terms_accepted", 0) or 0) == 1:
                return (
                    "Вы возвращаетесь к себе поздно и уже готовитесь ко сну: скинуть одежду, умыться, погасить свет и наконец лечь. "
                    "Дверь едва слышно скрипит. В комнату входит Аманда в длинной ночной сорочке, босая, с распущенными волосами и слишком спокойным лицом для девки, которая будто бы просто желает доброй ночи.\n\n"
                    "\"Мессир Стефан... доброй ночи,\" говорит она и закрывает дверь за собой.\n\n"
                    "Она развязывает верхний шнурок сорочки. Ткань сползает с плеча, открывая маленькую голую грудь и твердый сосок. Аманда не прикрывается. Наоборот, смотрит прямо на вас, потом медленно поднимает подол. "
                    "Под сорочкой на ней нет панталон; между бедер видно розовую влажную щель. Она держит подол всего несколько ударов сердца, достаточно долго, чтобы вы увидели, что это не случайность, и достаточно коротко, чтобы не считать это обещанием.\n\n"
                    "\"Вот,\" тихо говорит она, отпуская ткань. \"Теперь точно доброй ночи.\""
                )
            if not amanda_ai_my_room_private_unlocked():
                return ""
            if is_late:
                return (
                    "Вы возвращаетесь к себе и уже собираетесь ложиться. Аманда появляется в дверях в ночной сорочке и не спешит уходить: держит взгляд на вашей постели, потом на вас, потом нарочно поправляет ткань на груди так, что сосок на миг проступает под тонким полотном.\n\n"
                    "\"Я только доброй ночи пожелать,\" говорит она, но стоит слишком близко и явно хочет проверить, разрешите ли вы ей продолжить эту игру."
                )
            return (
                "Аманда появляется в вашей комнате без свидетелей и сразу дает понять, что пришла не за пустым разговором. Она подходит ближе, чуть задирает край юбки большим пальцем и смотрит, заметили ли вы эту маленькую наглость."
            )

        if loc == "TavernStorage" and intent in ("private_tease_player", "seek_private_satisfaction"):
            return (
                "В кладовой тесно и тихо. Аманда входит следом, делает вид, что ищет какую-то мелочь, но быстро забывает о полках и мешках. "
                "Она становится так близко, что бедро касается вашего бедра, и нарочно тянет ткань платья на груди, показывая, что хочет внимания без свидетелей."
            )

        if loc == "TavernAmandaRoom" and intent in ("private_tease_player", "seek_private_satisfaction"):
            return (
                "В своей комнате Аманда держится смелее. Здесь ее постель, ее запах и ее беспорядок; она садится на край кровати, разводит колени чуть шире приличного и смотрит, пришли вы командовать, заботиться или смотреть на нее как на девушку."
            )

        return ""

    def amanda_ai_satisfaction_label(intent_code=""):
        labels = {
            "ask_player_money": "Дать ей немного личных денег",
            "ask_player_beauty_help": "Пообещать мыло, платье или Серджио",
            "ask_player_reward_for_work": "Наградить за сегодняшнюю работу",
            "ask_melissa_loan_or_favor": "Самому закрыть ее нужду",
            "ask_legare_help": "Дать домашнюю альтернативу Легару",
            "private_tease_player": "Ответить на ее игру",
            "visit_player_room": "Принять ее визит",
            "seek_private_satisfaction": "Оставить ее одну",
            "expect_spanking": "Наказать ее",
            "obey_and_work": "Похвалить ее старание",
            "avoid_work": "Дать ей передышку",
        }
        return labels.get(str(intent_code or ""), "Удовлетворить просьбу")

    def amanda_ai_approval_label(intent_code=""):
        labels = {
            "ask_player_money": "Дать меньше, чем она просит",
            "ask_player_beauty_help": "Пообещать часть помощи",
            "ask_player_reward_for_work": "Похвалить без награды",
            "ask_melissa_loan_or_favor": "Перехватить разговор с Мелиссой",
            "ask_legare_help": "Отвлечь ее от Легара",
            "private_tease_player": "Ответить сдержанно",
            "visit_player_room": "Принять доброй ночью",
            "seek_private_satisfaction": "Сделать вид, что не заметили",
            "expect_spanking": "Пригрозить и отпустить",
            "obey_and_work": "Похвалить кратко",
            "avoid_work": "Разрешить короткий отдых",
        }
        return labels.get(str(intent_code or ""), "Ответить сдержанно")

    def amanda_ai_reason_refusal_label(intent_code=""):
        labels = {
            "ask_player_money": "Отказать в деньгах",
            "ask_player_beauty_help": "Отказать в помощи",
            "ask_player_reward_for_work": "Отказать в награде",
            "ask_melissa_loan_or_favor": "Отказать в займе",
            "ask_legare_help": "Отказать в Легаре",
            "private_tease_player": "Остановить игру",
            "visit_player_room": "Отправить спать мягко",
            "seek_private_satisfaction": "Сделать вид, что не заметили",
            "expect_spanking": "Отпустить без наказания",
            "obey_and_work": "Не хвалить",
            "avoid_work": "Не отпускать с работы",
        }
        return labels.get(str(intent_code or ""), "Отказать")

    def amanda_ai_hard_refusal_label(intent_code=""):
        labels = {
            "ask_player_money": "Резко отказать в деньгах",
            "ask_player_beauty_help": "Резко отказать в красоте",
            "ask_player_reward_for_work": "Срезать ее ожидания",
            "ask_melissa_loan_or_favor": "Запретить без объяснений",
            "ask_legare_help": "Запретить Легара жестко",
            "private_tease_player": "Оборвать игру",
            "visit_player_room": "Выгнать из комнаты",
            "seek_private_satisfaction": "Пригрозить наказанием",
            "expect_spanking": "Выгнать без разговоров",
            "obey_and_work": "Приказать работать",
            "avoid_work": "Заставить работать",
        }
        return labels.get(str(intent_code or ""), "Просто отказать")

    def amanda_ai_terms_text(intent_code="", response_code="approve"):
        return ""

    def amanda_ai_intro_text(intent_code="", location_code=""):
        intent = str(intent_code or "")
        status = amanda_ai_status_line()
        report = amanda_ai_work_report()
        clothing = amanda_ai_clothing_line(location_code, intent)
        barber_line = amanda_ai_barber_result_line()
        missing_beauty = amanda_ai_beauty_missing_lines()
        private_setup = amanda_ai_private_setup_text(intent, location_code)
        texts = {
            "ask_player_money": "Аманда ловит ваш взгляд и просит немного денег. Не в виде каприза: ей хочется иметь свои монеты, чтобы не унижаться перед каждым мелким желанием.",
            "ask_player_beauty_help": "Аманда говорит тише обычного. Она не просит все сразу: ей нужно то, чего еще нет. Сейчас это: %s." % (", ".join(missing_beauty) if len(missing_beauty) > 0 else "ничего срочного"),
            "ask_player_reward_for_work": "Аманда напоминает, что сегодня не пряталась от обязанностей. В ее голосе слышно желание получить не только монеты, но и ваше одобрение.",
            "ask_melissa_loan_or_favor": "Вы замечаете, как Аманда ищет Мелиссу глазами. Если вы не поможете, она почти наверняка попробует выпросить монеты или услугу у нее, а потом отдавать долг по-своему.",
            "ask_legare_help": "Аманда осторожно произносит имя Легара. Она не говорит прямо, чего хочет от него, но дает понять: если в доме ей закрывают дорогу к красивым вещам и деньгам, она найдет другой путь.",
            "private_tease_player": private_setup or "Вы спрашиваете, что Аманда здесь делает. Она не отвечает сразу: подходит ближе, проверяет взглядом дверь и только потом показывает, что пришла не за поручением.",
            "visit_player_room": private_setup or "Аманда приходит к вам сама и не прячется за пустой болтовней. Она стоит слишком близко, дает вам увидеть голую кожу у ворота сорочки и ждет, решите ли вы принять ее визит как женский вызов, а не как хозяйственную просьбу.",
            "seek_private_satisfaction": private_setup or "Аманда ищет уединения потому, что тело уже мешает ей думать спокойно. Она сжимает бедра, злится на собственную мокрую пизду и почти готова спрятаться где-нибудь, чтобы довести себя пальцами до облегчения без чужих советов.",
            "expect_spanking": "Аманда держится рядом слишком тихо. Она видит, что хозяин злой, и ждет наказания: плечи напряжены, взгляд косится на вашу руку, а упрямство в лице спорит со страхом.",
            "obey_and_work": "Вы останавливаете Аманду и прямо спрашиваете, почему работа сделана плохо. Она сперва пытается улыбнуться, но по вашему тону понимает: сейчас разговор не о внимании, а о навыке и порядке.",
            "avoid_work": "Аманда жалуется на усталость и пытается отлынить от работы. Она делает это мягко, но проверяет, можно ли получить поблажку без расплаты.",
        }
        details = []
        if report.get("cleaning", "none") != "none":
            details.append("уборка: %s" % str(report.get("cleaning")))
        if report.get("waitress", "none") != "none":
            details.append("зал: %s" % str(report.get("waitress")))
        if report.get("cooking", "none") != "none":
            details.append("кухня: %s" % str(report.get("cooking")))
        base = texts.get(intent, "Аманда явно чего-то хочет и ждет вашей реакции.")
        if barber_line and intent in ("ask_player_reward_for_work", "private_tease_player", "visit_player_room", "ask_player_beauty_help"):
            base = base + "\n\n" + barber_line
        if clothing:
            base = base + "\n\n" + clothing
        if status:
            base = base + "\n\n" + status
        if len(details) > 0:
            base = base + "\n\nРабочий след на сегодня: " + ", ".join(details) + "."
        return base

    def amanda_ai_response_text(intent_code="", response_code="approve"):
        intent = str(intent_code or "")
        response = str(response_code or "approve")
        first_night_tease = (
            intent in ("visit_player_room", "private_tease_player")
            and int(AmandaVar.get("night_tease_scene_active", 0) or 0) == 1
        )
        terms = amanda_ai_terms_text(intent, response)
        response_titles = {
            "satisfy": "Вы даете ей то, что она просит",
            "approve": "Вы отвечаете сдержанно",
            "refuse_reason": "Вы отказываете спокойно",
            "refuse": "Вы отказываете резко",
        }
        title = response_titles.get(response, "Вы отвечаете Аманде")
        if response in ("satisfy", "approve"):
            endings = {
                "ask_player_money": "Аманда прячет улыбку и сразу считает, на что хватит монет.",
                "ask_player_beauty_help": "Аманда оживляется и начинает перечислять, что ей нужнее: мыло, волосы, платье или Серджио.",
                "ask_player_reward_for_work": "Аманда выпрямляется и держится заметно довольнее, чем минуту назад.",
                "ask_melissa_loan_or_favor": "Аманда бросает короткий взгляд на Мелиссу и отступает от этой идеи.",
                "ask_legare_help": "Аманда перестает произносить имя Легара, но взгляд у нее остается расчетливым.",
                "private_tease_player": "Аманда довольна тем, что ее заметили. Она отступает медленно, оставляя в воздухе обещание следующего раза.",
                "visit_player_room": "Аманда остается еще на несколько фраз, потом уходит сама, довольно улыбаясь.",
                "seek_private_satisfaction": "Аманда быстро исчезает из виду и потом возвращается тише обычного.",
                "expect_spanking": "Вы наказываете ее. Аманда дергается от первого удара, потом стискивает зубы и держится до конца. После этого она отвечает тише и смотрит внимательнее.",
                "obey_and_work": "Аманда кивает и берется за дело охотнее.",
                "avoid_work": "Аманда получает передышку и тут же старается выглядеть слабее, чем есть.",
            }
            if first_night_tease:
                if response == "satisfy":
                    endings["visit_player_room"] = "Вы не торопитесь давать ей то, за чем она пришла.\n\n\"Сначала докажи, что умеешь просить лучше,\" говорите вы. \"Хочешь награды - учись убеждать, а не требовать.\"\n\nАманда краснеет, но не уходит. Она подходит ближе, берет вашу руку и сама кладет ее на грудь через тонкую ткань сорочки. Пальцы у нее дрожат, зато взгляд становится упрямым и голодным.\n\n\"Тогда смотрите,\" шепчет она. \"Я буду учиться быстро.\"\n\nОна ведет вашу ладонь ниже, дает почувствовать жар тела и только потом отступает, оставляя обещание вместо полного ответа. \"Доброй ночи, мессир Стефан.\" Аманда уходит довольная тем, что смогла вас задержать."
                    endings["private_tease_player"] = "Вы отвечаете на ее игру прямо, но не даете ей победить слишком легко.\n\n\"Мало просто показать тело,\" говорите вы. \"Если хочешь что-то получить, сначала стань искуснее. Убеди меня.\"\n\nАманда подходит вплотную, медленно раскрывает ворот сорочки и дает рассмотреть себя без притворной случайности. Она задерживает вашу руку у своей груди, прикусывает губу и отступает с довольной улыбкой.\n\n\"Не все сразу,\" шепчет она. \"Но теперь вы точно будете думать, чему меня учить.\""
                else:
                    endings["visit_player_room"] = "Вы принимаете ее доброй ночью без продолжения. Аманда задерживается у двери, проверяет вашу реакцию и уходит не сразу.\n\n\"Ладно,\" говорит она, поправляя сорочку. \"Значит, просто доброй ночи.\""
                    endings["private_tease_player"] = "Вы отвечаете сдержанно. Аманда замечает это, усмехается и нарочно тянет паузу дольше обычного.\n\n\"Вот так,\" говорит она. \"Чтобы вы знали, чего пока не получили.\""
        elif response == "refuse_reason":
            endings = {
                "ask_player_money": "Аманда обижается и убирает руки от кармана вашего камзола.",
                "ask_player_beauty_help": "Аманда хмурится и начинает смотреть в сторону, будто уже считает другие способы получить желаемое.",
                "ask_player_reward_for_work": "Аманда не получает награду и сразу теряет часть показного усердия.",
                "ask_melissa_loan_or_favor": "Аманда молчит, но взгляд на Мелиссу становится осторожнее.",
                "ask_legare_help": "Аманда замолкает на имени Легара, но явно не выбрасывает его из головы.",
                "private_tease_player": "Вы останавливаете игру. Аманда краснеет от досады и делает вид, будто ничего особенного не было.",
                "visit_player_room": "Вы отправляете ее обратно спокойно. Аманда уходит злая и смущенная, но без открытого скандала.",
                "seek_private_satisfaction": "Вы делаете вид, что поняли только половину. Аманда пользуется этим и быстро исчезает.",
                "expect_spanking": "Вы только грозите наказанием. Аманда опускает глаза, но по губам видно: она ожидала большего.",
                "obey_and_work": "Аманда не получает похвалы и тут же становится суше в ответах.",
                "avoid_work": "Аманда вздыхает и возвращается к делу без прежней улыбки.",
            }
            if first_night_tease:
                endings["visit_player_room"] = "Вы отправляете ее спать и не даете превратить визит в награду.\n\n\"Сначала научись делать это лучше,\" говорите вы. \"Красивой просьбе нужна практика. Требования оставь за дверью.\"\n\nАманда стоит у двери еще секунду, будто проверяет, не передумаете ли вы, потом зло затягивает шнурок сорочки.\n\n\"Доброй ночи так доброй ночи,\" бросает она и уходит."
                endings["private_tease_player"] = "Вы останавливаете игру.\n\n\"Не требуй того, что еще не умеешь брать красиво,\" говорите вы. \"Сначала навыки. Потом просьбы.\"\n\nАманда сердито опускает подол и поправляет ворот сорочки. Отказ ей неприятен, и она уходит без улыбки."
        else:
            endings = {
                "ask_player_money": "Аманда закрывается мгновенно. Она слышит не отказ, а унижение, и начинает искать обходные пути.",
                "ask_player_beauty_help": "Ее желание стать красивее превращается в злость. Если вы не дадите путь, она найдет чужой.",
                "ask_player_reward_for_work": "Аманда отворачивается. В следующий раз она будет считать, что стараться для вас глупо.",
                "ask_melissa_loan_or_favor": "Вы обрываете разговор, и Аманда запоминает: лучше скрывать такие дела.",
                "ask_legare_help": "Резкий запрет только подкармливает упрямство. Имя Легара после этого звучит в ее голове еще громче.",
                "private_tease_player": "Аманда отступает с холодной улыбкой. Игра не исчезла, но теперь в ней больше злости.",
                "visit_player_room": "Она уходит быстро, и дверь закрывается слишком тихо. Это не конец желания, а начало обиды.",
                "seek_private_satisfaction": "Злость смешивается с испугом. В следующий раз она будет осторожнее и скрытнее.",
                "expect_spanking": "Вы выгоняете ее без разговора. Аманда уходит быстро, но злость на лице остается.",
                "obey_and_work": "Аманда воспринимает это как придирку и отвечает коротко.",
                "avoid_work": "Вы давите жестко. Работу она, может, и сделает, но упрямства станет больше.",
            }
            if first_night_tease:
                endings["visit_player_room"] = "Вы обрываете ее резко. Аманда сразу закрывает грудь и дергает сорочку вниз. Улыбка исчезает быстрее, чем желание.\n\nПеред уходом она тихо бросает: \"Понятно. Значит, хозяин сегодня злой.\" Дверь закрывается мягко."
                endings["private_tease_player"] = "Вы давите на нее слишком грубо, и игра тут же становится злой. Аманда отступает, прижимая ткань к бедрам, и смотрит уже не игриво, а настороженно."
        result_text = title + "."
        if str(terms or "").strip():
            result_text += "\n\n" + str(terms or "")
        result_text += "\n\n" + endings.get(intent, "Аманда запоминает вашу реакцию и меняет свое поведение.")
        return result_text

    def amanda_ai_feedback_outcome(response_code="approve"):
        response = str(response_code or "approve")
        if response == "satisfy":
            return "rewarded"
        if response == "approve":
            return "approved"
        if response == "refuse_reason":
            return "refused_with_reason"
        if response == "refuse":
            return "refused_badly"
        return "neutral"

    def amanda_ai_adjust_dict_value(target, key, delta, low=0, high=100):
        target[key] = amanda_ai_clamp(amanda_ai_int(target.get(key, 0), 0) + amanda_ai_int(delta, 0), low, high)

    def amanda_ai_apply_response(intent_code="", response_code="approve", public=False):
        global BadLandlordScore, TavernUncleTruthStage

        intent = str(intent_code or "")
        response = str(response_code or "approve")
        first_night_tease = (
            intent in ("visit_player_room", "private_tease_player")
            and int(AmandaVar.get("night_tease_scene_active", 0) or 0) == 1
        )
        outcome = amanda_ai_feedback_outcome(response)
        updated_memory = AmandaIntentModel.amanda_apply_feedback(AmandaIntentMemory, intent, outcome, amanda_ai_int(dayspassed, 0), bool(public)) if amanda_ai_available() else dict(AmandaIntentMemory or {})
        AmandaIntentMemory.clear()
        AmandaIntentMemory.update(updated_memory)

        if response in ("satisfy", "approve"):
            amanda_ai_adjust_dict_value(Friends, "amanda", 1, -100, 100)
            amanda_ai_adjust_dict_value(otkroven, "amanda", 1 if response == "satisfy" else 0, 0, 100)
            AmandaNeedBlocked["amanda"] = 0
            relationship_calm("amanda", 1)
        elif response == "refuse_reason":
            AmandaNeedBlocked["amanda"] = 1
            amanda_ai_adjust_dict_value(neshlush, "amanda", -1, 0, 100)
        else:
            AmandaNeedBlocked["amanda"] = 1
            amanda_ai_adjust_dict_value(neshlush, "amanda", 1, 0, 100)
            relationship_set_anger("amanda", 1, 1, "amanda_ai_refusal")

        if intent in ("private_tease_player", "visit_player_room", "seek_private_satisfaction"):
            if response in ("satisfy", "approve"):
                amanda_ai_adjust_dict_value(Arousal, "amanda", 8 if response == "satisfy" else 4, 0, 100)
                amanda_ai_adjust_dict_value(PussyWetStart, "amanda", 6 if response == "satisfy" else 3, 0, 100)
                AmandaPreferenceKnown["teasing"] = 1
                AmandaPreferenceKnown["watching"] = 1
                AmandaPreferenceWeights["teasing"] = amanda_ai_int(AmandaPreferenceWeights.get("teasing", 2), 2) + 1
            elif response == "refuse":
                amanda_ai_adjust_dict_value(Arousal, "amanda", -5, 0, 100)

        if intent == "ask_player_beauty_help" and response in ("satisfy", "approve"):
            AmandaVar["barber_request_interest"] = 1
            AmandaVar["beauty_help_approved_day"] = amanda_ai_int(dayspassed, 0)
            AmandaVar["beauty_help_terms_accepted"] = 1
        if intent == "ask_player_money" and response in ("satisfy", "approve"):
            AmandaVar["money_terms_accepted"] = 1
        if intent == "ask_player_money" and response == "satisfy":
            spend = min(max(5, amanda_ai_int(money, 0) // 50), amanda_ai_int(money, 0))
            store.money = max(0, amanda_ai_int(money, 0) - spend)
            AmandaVar["personal_money"] = amanda_ai_int(AmandaVar.get("personal_money", 0), 0) + spend
        if intent == "ask_player_reward_for_work" and response in ("satisfy", "approve"):
            AmandaVar["work_reward_day"] = amanda_ai_int(dayspassed, 0)
            AmandaVar["work_reward_terms_accepted"] = 1
        if intent in ("private_tease_player", "visit_player_room") and response in ("satisfy", "approve", "refuse_reason"):
            AmandaVar["private_attention_terms_day"] = amanda_ai_int(dayspassed, 0)
        if first_night_tease:
            AmandaVar["night_tease_resolved"] = 1
            AmandaVar["barber_terms_understood"] = 1
            TavernUncleTruthStage = max(amanda_ai_int(TavernUncleTruthStage, 0), 1)
            if response in ("satisfy", "approve"):
                AmandaVar["first_night_tease_hooked"] = 1
                AmandaPreferenceKnown["teasing"] = 1
                AmandaPreferenceWeights["teasing"] = amanda_ai_int(AmandaPreferenceWeights.get("teasing", 2), 2) + 1
            elif response == "refuse_reason":
                AmandaVar["player_not_uncle_hint"] = 1
            else:
                AmandaVar["player_like_uncle_warning"] = amanda_ai_int(AmandaVar.get("player_like_uncle_warning", 0), 0) + 1
                BadLandlordScore = max(0, amanda_ai_int(BadLandlordScore, 0) + 1)
        if intent == "ask_legare_help":
            if response == "refuse":
                AmandaVar["alberfriends"] = amanda_ai_int(AmandaVar.get("alberfriends", 0), 0) + 1
            elif response in ("satisfy", "approve", "refuse_reason"):
                AmandaVar["alberprohibit"] = 1
        if intent == "obey_and_work" and response in ("satisfy", "approve"):
            amanda_ai_adjust_dict_value(neshlush, "amanda", -1, 0, 100)
            amanda_ai_adjust_dict_value(cleaning, "amanda", 1, 0, 100)
        if intent == "avoid_work" and response == "refuse":
            amanda_ai_adjust_dict_value(neshlush, "amanda", 1, 0, 100)

        try:
            renpy.notify(amanda_ai_notify_text(intent, response))
        except Exception:
            pass

    def amanda_ai_notify_text(intent_code="", response_code="approve"):
        response = str(response_code or "approve")
        if response in ("satisfy", "approve"):
            return "Аманда запомнила вашу поддержку."
        if response == "refuse_reason":
            return "Аманда недовольна."
        return "Аманда запомнила резкий отказ."

    def amanda_ai_choice_items(intent_code="", context_code="room", location_code=""):
        items = [
            MenuItem(amanda_ai_satisfaction_label(intent_code), Call("AmandaAIIntentApply", intent_code, "satisfy", context_code, location_code)),
            MenuItem(amanda_ai_approval_label(intent_code), Call("AmandaAIIntentApply", intent_code, "approve", context_code, location_code)),
            MenuItem(amanda_ai_reason_refusal_label(intent_code), Call("AmandaAIIntentApply", intent_code, "refuse_reason", context_code, location_code)),
            MenuItem(amanda_ai_hard_refusal_label(intent_code), Call("AmandaAIIntentApply", intent_code, "refuse", context_code, location_code)),
        ]
        if str(intent_code or "") in ("private_tease_player", "visit_player_room", "seek_private_satisfaction") and player_can_ask_intimacy_help("amanda"):
            items.insert(1, MenuItem("Попросить Аманду помочь вам", Call("PlayerIntimacyHelpAsk", "amanda", "TavernMyRoomRestore" if str(location_code or CurLoc or "") == "TavernMyRoom" else "AmandaAIIntentReturn")))
        items.append(MenuItem("Назад", Call("AmandaAIIntentReturn", context_code, location_code)))
        return items


    # -------------------------------------------------------------------------
    # Household + Amanda mini-event layer.
    # This shares HouseholdAI_ren state and feeds AmandaIntent_ren mini-events.
    # -------------------------------------------------------------------------

    def amanda_ai_float(value, default=0.0):
        try:
            return float(value)
        except Exception:
            return float(default or 0.0)

    def amanda_ai_float_clamp(value, low=0.0, high=1.0):
        return max(float(low), min(float(high), amanda_ai_float(value, low)))

    def amanda_ai_household_value(key_name="", default=0.0):
        try:
            row = getattr(store, "HouseholdAIState", {}) or {}
            if isinstance(row, dict):
                return amanda_ai_float_clamp(row.get(str(key_name or ""), default), 0.0, 1.0)
        except Exception:
            pass
        return amanda_ai_float_clamp(default, 0.0, 1.0)

    def amanda_ai_household_npc_value(npc_id="amanda", key_name="drive", default=0.0):
        try:
            rows = getattr(store, "HouseholdNPCState", {}) or {}
            row = rows.get(str(npc_id or ""), {}) if isinstance(rows, dict) else {}
            if isinstance(row, dict):
                return amanda_ai_float_clamp(row.get(str(key_name or ""), default), 0.0, 1.0)
        except Exception:
            pass
        return amanda_ai_float_clamp(default, 0.0, 1.0)

    def amanda_ai_float_access(var_name="", default=0.0):
        try:
            value = getattr(store, str(var_name or ""), default)
            return amanda_ai_float_clamp(float(value or 0) / 10.0, 0.0, 1.0)
        except Exception:
            return amanda_ai_float_clamp(default, 0.0, 1.0)

    def amanda_ai_food_security():
        try:
            value = getattr(store, "food_stock", 10)
            return amanda_ai_float_clamp(float(value or 0) / 10.0, 0.0, 1.0)
        except Exception:
            return 0.5

    def amanda_ai_assigned_work_name():
        try:
            if amanda_ai_assigned(jobkitchen, "amanda"):
                return "kitchen"
            if amanda_ai_assigned(jobwaitress, "amanda"):
                return "waitress"
            if amanda_ai_assigned(jobcleaning, "amanda"):
                return "cleaning"
        except Exception:
            pass
        return "none"

    def amanda_ai_mini_event_key(event_code="", location_code=""):
        return "%s|%s|%s|%s" % (
            amanda_ai_day_key(),
            amanda_ai_int(time, 0),
            str(location_code or CurLoc or ""),
            str(event_code or ""),
        )

    def amanda_ai_mini_event_seen(event_code="", location_code=""):
        return amanda_ai_int(AmandaMiniEventSeen.get(amanda_ai_mini_event_key(event_code, location_code), 0), 0) == 1

    def amanda_ai_mark_mini_event_seen(event_code="", location_code=""):
        key = amanda_ai_mini_event_key(event_code, location_code)
        AmandaMiniEventSeen[key] = 1
        store.AmandaMiniEventLastCode = str(event_code or "")
        row = dict(AmandaMiniEventMemory.get(str(event_code or ""), {}) or {})
        row["last_day"] = amanda_ai_int(dayspassed, 0)
        row["recent_count"] = amanda_ai_int(row.get("recent_count", 0), 0) + 1
        AmandaMiniEventMemory[str(event_code or "")] = row

    def amanda_ai_mini_event_label(event_code=""):
        labels = {
            "amanda_morning_hover": "AmandaMiniEvent_MorningHover",
            "amanda_sits_on_leg": "AmandaMiniEvent_SitsOnLeg",
            "amanda_bed_edge_talk": "AmandaMiniEvent_BedEdgeTalk",
            "amanda_storm_fear": "AmandaMiniEvent_StormFear",
            "amanda_kitchen_jealousy": "AmandaMiniEvent_KitchenJealousy",
            "amanda_new_dress_pressure": "AmandaMiniEvent_NewDressPressure",
            "amanda_eavesdrop_caught": "AmandaMiniEvent_EavesdropCaught",
            "amanda_hunting_interest": "AmandaMiniEvent_HuntingInterest",
            "amanda_breakfast_mockery": "AmandaMiniEvent_BreakfastMockery",
            "amanda_late_night_window": "AmandaMiniEvent_LateNightWindow",
            "amanda_asks_work_direction": "AmandaMiniEvent_AsksWorkDirection",
            "amanda_poverty_complaint": "AmandaMiniEvent_PovertyComplaint",
        }
        return labels.get(str(event_code or ""), "")

    def amanda_ai_mini_event_picture(event_code="", location_code=""):
        loc = str(location_code or CurLoc or "")
        event = str(event_code or "")
        kitchen_picture = "images/amanda/kitchen_help.png"
        if loc == "TavernKitchen" and renpy.loadable(kitchen_picture):
            return kitchen_picture
        if event in ("amanda_kitchen_jealousy", "amanda_breakfast_mockery") and renpy.loadable(kitchen_picture):
            return kitchen_picture
        room_pictures = {
            "TavernMyRoom": [
                "images/amanda/mc_room_exposure.png",
                "images/tavern/myroom/player_table.png",
            ],
            "TavernAmandaRoom": [
                "images/amanda/Room/amanda_bedroom_003.jpeg",
                "images/amanda/Room/amanda_bedroom_002.jpeg",
                "images/amanda/Room/amanda_bedroom.jpeg",
            ],
            "TavernStorage": [
                "images/amanda/tavern/amanda_storage.png",
                "images/tavern/storage/storage_room.png",
            ],
            "TavernMain": [
                "images/amanda/mock_talk.png",
            ],
        }
        for candidate in list(room_pictures.get(loc, []) or []):
            if renpy.loadable(candidate):
                return candidate
        try:
            last_picture = str(getattr(store, "_layout_last_picture", "") or "")
            if last_picture and renpy.loadable(last_picture):
                return last_picture
        except Exception:
            pass
        return ""

    def amanda_ai_choose_mini_event(location_code="", mode="room", threshold=0.30):
        if not amanda_ai_available() or not hasattr(AmandaIntentModel, "amanda_choose_mini_event"):
            return {}
        ctx = amanda_ai_context(location_code, mode)
        state = AmandaIntentModel.amanda_choose_mini_event(ctx, AmandaMiniEventMemory, threshold)
        AmandaMiniEventLastState.clear()
        AmandaMiniEventLastState.update(state)
        return state

    def amanda_ai_mini_event_code(location_code="", mode="room", threshold=0.30):
        loc = str(location_code or CurLoc or "")
        if "amanda" not in list(getNPCids(loc) or []):
            return ""
        state = amanda_ai_choose_mini_event(loc, mode, threshold)
        chosen = state.get("chosen", None) if isinstance(state, dict) else None
        if not chosen:
            return ""
        code = str(chosen.get("event", "") or "")
        if code == "" or amanda_ai_mini_event_seen(code, loc):
            return ""
        return code

    def amanda_ai_mini_event_ready(location_code="", mode="room"):
        if not bool(AmandaAIIntegrationEnabled):
            return False
        loc = str(location_code or CurLoc or "")
        mode_key = str(mode or "room")
        code = amanda_ai_mini_event_code(loc, mode_key)
        if code == "":
            return False
        AmandaMiniEventQueued[loc + ":" + mode_key] = code
        return True

    def amanda_ai_mini_event_pop(location_code="", mode="room"):
        loc = str(location_code or CurLoc or "")
        mode_key = str(mode or "room")
        key = loc + ":" + mode_key
        code = str(AmandaMiniEventQueued.pop(key, "") or "")
        if code == "":
            code = amanda_ai_mini_event_code(loc, mode_key)
        return code

label AmandaAIIntentBreakfastEvent(intent_code=""):
    $ _amanda_ai_intent = str(intent_code or amanda_ai_breakfast_intent_code() or "")
    if _amanda_ai_intent == "":
        call TavernKitchenBreakfastMenu
        return
    $ amanda_ai_mark_seen(_amanda_ai_intent, "TavernKitchen")
    $ MainTxt = amanda_ai_intro_text(_amanda_ai_intent, "TavernKitchen")
    $ CurLocDesc = MainTxt
    $ current_action_title = amanda_ai_menu_label(_amanda_ai_intent)
    $ current_action_content = None
    $ current_action_items = amanda_ai_choice_items(_amanda_ai_intent, "breakfast", "TavernKitchen")
    call QueuePagedPanelText(MainTxt, current_action_title, list(current_action_items or []), "plain")
    call ReturnToMainUI
    return

label AmandaAIIntentRoomEvent(location_code="", intent_code=""):
    $ _amanda_ai_location = str(location_code or CurLoc or "")
    if "amanda" not in list(getNPCids(_amanda_ai_location) or []):
        call AmandaAIIntentReturn("room", _amanda_ai_location)
        return
    $ _amanda_ai_intent = str(intent_code or amanda_ai_room_intent_code(_amanda_ai_location) or "")
    if _amanda_ai_intent == "":
        call AmandaAIIntentReturn("room", _amanda_ai_location)
        return
    $ amanda_ai_mark_seen(_amanda_ai_intent, _amanda_ai_location)
    if _amanda_ai_location == "TavernMyRoom" and _amanda_ai_intent in ("visit_player_room", "private_tease_player") and int(AmandaVar.get("night_tease_seen", 0) or 0) == 0 and int(AmandaVar.get("beauty_help_terms_accepted", 0) or 0) == 1:
        $ AmandaVar["night_tease_seen"] = 1
        $ AmandaVar["night_tease_scene_active"] = 1
    else:
        $ AmandaVar["night_tease_scene_active"] = 0
    $ MainTxt = amanda_ai_intro_text(_amanda_ai_intent, _amanda_ai_location)
    $ CurLocDesc = MainTxt
    $ current_action_title = amanda_ai_menu_label(_amanda_ai_intent)
    $ current_action_content = None
    $ current_action_items = amanda_ai_choice_items(_amanda_ai_intent, "room", _amanda_ai_location)
    call QueuePagedPanelText(MainTxt, current_action_title, list(current_action_items or []), "plain")
    call ReturnToMainUI
    return

label AmandaAIIntentApply(intent_code="", response_code="approve", context_code="room", location_code=""):
    $ _amanda_ai_public = str(context_code or "") == "breakfast"
    $ amanda_ai_apply_response(intent_code, response_code, _amanda_ai_public)
    if str(context_code or "") == "room" and str(location_code or CurLoc or "") == "TavernMyRoom" and str(intent_code or "") in ("private_tease_player", "visit_player_room", "seek_private_satisfaction", "expect_spanking"):
        $ amanda_ai_clear_room_presence("TavernMyRoom")
    $ MainTxt = amanda_ai_response_text(intent_code, response_code)
    $ CurLocDesc = MainTxt
    call stat
    $ current_action_title = amanda_ai_menu_label(intent_code)
    $ current_action_content = None
    $ current_action_items = [MenuItem("Продолжить", Call("AmandaAIIntentReturn", context_code, location_code))]
    call QueuePagedPanelText(MainTxt, current_action_title, list(current_action_items or []), "plain")
    call ReturnToMainUI
    return

label AmandaAIIntentReturn(context_code="room", location_code=""):
    $ AmandaVar["night_tease_scene_active"] = 0
    if str(context_code or "") == "breakfast":
        call TavernKitchenBreakfastShowText(TavernKitchenSavedText, "TavernKitchenBreakfastMenu")
        return
    if str(location_code or CurLoc or "") == "TavernAmandaRoom":
        call TavernAmandaRoomRestore
        return
    if str(location_code or CurLoc or "") == "TavernMyRoom":
        call TavernMyRoomRestore
        return
    if str(location_code or CurLoc or "") == "TavernStorage":
        jump TavernStorage
    call ReturnToMainUI
    return


# -----------------------------------------------------------------------------
# Mini-event entry point. If no mini-event is available, it returns cleanly.
# -----------------------------------------------------------------------------
label AmandaMiniEventTry(location_code="", mode="room"):
    $ _amanda_mini_location = str(location_code or CurLoc or "")
    $ _amanda_mini_event = amanda_ai_mini_event_pop(_amanda_mini_location, mode)
    if _amanda_mini_event == "":
        return
    $ amanda_ai_mark_mini_event_seen(_amanda_mini_event, _amanda_mini_location)
    $ AmandaMiniEventLastLocation = _amanda_mini_location
    $ _amanda_mini_label = amanda_ai_mini_event_label(_amanda_mini_event)
    $ _amanda_mini_picture = amanda_ai_mini_event_picture(_amanda_mini_event, _amanda_mini_location)
    if str(_amanda_mini_picture or "").strip():
        call ShowImage("", "", _amanda_mini_picture)
    if _amanda_mini_label != "":
        call expression _amanda_mini_label
    return


label AmandaMiniEventEntry(location_code="", mode="room"):
    $ _amanda_mini_entry_location = str(location_code or CurLoc or "")
    $ _amanda_mini_entry_mode = str(mode or "room")
    call checkTriggers(_amanda_mini_entry_location, "amanda_ai_%s_mini" % _amanda_mini_entry_mode, 0)
    if _return:
        return True
    return False


label story_amanda_ai_room_mini_0:
    call AmandaMiniEventTry(CurLoc, "room")
    return True


label story_amanda_ai_breakfast_mini_0:
    call AmandaMiniEventTry("TavernKitchen", "breakfast")
    return True


# =============================================================================
# Amanda Mini Events
# Integrated event labels for AmandaAI_Bridge.rpy.
# =============================================================================

label AmandaMiniEvent_MorningHover:

    "Аманда появляется еще до того, как утро окончательно собирается в обычный трактирный шум."

    "Она делает вид, что расставляет кружки, но каждый раз оказывается к вам ближе, чем требует работа."

    "Аманда: Поздно проснулся."

    "Говорит она это почти как обвинение, только взгляд на вашем лице задерживается слишком долго."

    if amanda_ai_assigned_work_name() != "none":
        "Аманда: Ну? Мне сперва работать, или самой угадывать, что ты опять забыл сказать?"

    menu:
        "Спросить, чего она на самом деле хочет":
            "Аманда: Смотря что предлагаешь. Внимание дешево стоит. А нормальная помощь - нет."
            $ AmandaVar["attention_hint_day"] = dayspassed
            $ household_ai_reduce_drive("amanda", 0.10)

        "Отправить ее к работе":
            "Аманда уходит с таким показным послушанием, что это почти звучит как насмешка."
            $ household_ai_raise_friction(0.04)

        "Велеть говорить прямо":
            "Аманда: Прямо? Ладно. Я хочу, чтобы в этом доме перестали считать каждую мелкую удобную вещь королевской роскошью."
            $ AmandaVar["plain_complaint_day"] = dayspassed

    return


label AmandaMiniEvent_SitsOnLeg:

    "Аманда подходит, пока вы сидите за столом."

    "Не спрашивая разрешения, она боком устраивается у вас на колене: достаточно легко, чтобы притвориться шуткой, и достаточно смело, чтобы шутка стала опасной."

    "Аманда: Не двигайся. Я думаю."

    "Она поправляет юбку, но следит не за тканью, а за вашей реакцией."

    menu:
        "Позволить ей остаться":
            "Аманда на несколько вдохов расслабляется, довольная тем, что вы позволили, и раздраженная тем, что не стали просить большего."
            $ AmandaPreferenceKnown["teasing"] = 1
            $ AmandaPreferenceWeights["teasing"] = amanda_ai_int(AmandaPreferenceWeights.get("teasing", 2), 2) + 1
            $ household_ai_reduce_drive("amanda", 0.12)

        "Убрать ее с колен":
            "Аманда демонстративно поднимается."
            "Аманда: Безнадежно."
            $ household_ai_raise_friction(0.05)
            $ AmandaNeedBlocked["amanda"] = 1

        "Предупредить, чтобы не играла во время работы":
            "Аманда: Тогда перестань делать работу такой скучной."
            $ neshlush["amanda"] = amanda_ai_clamp(amanda_ai_int(neshlush.get("amanda", 0), 0) + 1, 0, 100)

    return


label AmandaMiniEvent_BedEdgeTalk:

    "Вы возвращаетесь поздно."

    "Аманда уже сидит на краю вашей кровати, сложив руки на коленях так, будто имеет на это полное право."

    "Аманда: В твоей комнате теплее, чем в моей."

    "Она говорит это тихо и отворачивается раньше, чем фраза успевает стать просьбой."

    menu:
        "Спросить, зачем она пришла":
            "Аманда: Может, хотела проверить, один ли ты. Может, замерзла. Выбери тот ответ, от которого лучше себя поведешь."
            $ AmandaVar["private_attention_terms_day"] = dayspassed

        "Сесть рядом":
            "Аманда не отодвигается. Для этого мгновения такого разрешения достаточно, хотя обещанием на потом оно не становится."
            $ Friends["amanda"] = amanda_ai_int(Friends.get("amanda", 0), 0) + 1
            $ household_ai_reduce_drive("amanda", 0.10)

        "Сказать ей спать в своей комнате":
            "Аманда щурится: ее задевает не холод, а то, как легко ее прогнали."
            "Аманда: Ладно. Тогда мерзни один."
            $ household_ai_raise_friction(0.05)
            $ AmandaNeedBlocked["amanda"] = 1

    return


label AmandaMiniEvent_StormFear:

    "Гром тяжело прокатывается над крышей трактира."

    "Через несколько минут в дверях появляется Аманда."

    "Аманда: Крыша звучит так, будто собирается провалиться."

    "Она явно пришла не только затем, чтобы сообщить о погоде."

    menu:
        "Позволить ей остаться, пока гроза не утихнет":
            "Аманда придвигается ближе к огню и делает вид, что ей ничуть не легче."
            $ Friends["amanda"] = amanda_ai_int(Friends.get("amanda", 0), 0) + 1
            $ household_ai_reduce_drive("amanda", 0.14)

        "Дать ей одеяло":
            "Она принимает его с подозрительно мягким видом."
            "Аманда: Не гордись так. Это всего лишь одеяло."
            $ AmandaVar["storm_blanket_day"] = dayspassed

        "Сказать, что от грозы она не умрет":
            "Аманда: Как всегда, умеешь утешить."
            $ household_ai_raise_friction(0.04)

    return


label AmandaMiniEvent_KitchenJealousy:

    "Аманда замечает, что вы уделяете кому-то другому слишком много внимания."

    "Ее работа сразу становится громче: миски стукают о стол, дверцы шкафов хлопают сильнее, а молчание делается почти театральным."

    "Аманда: Удивительно, как быстро исчезает работа, стоит некоторым улыбнуться."

    if "melissa" in list(getNPCids(CurLoc) or []):
        "Мелисса: Ты совсем не умеешь делать вид."
        "Аманда: Он тоже."

    menu:
        "Успокоить Аманду":
            "Она сопротивляется утешению из принципа, потом все же выдыхает и возвращается к работе."
            $ household_ai_reduce_drive("amanda", 0.10)
            $ AmandaVar["jealousy"] = max(0, amanda_ai_int(AmandaVar.get("jealousy", 0), 0) - 1)

        "Проигнорировать":
            "До конца утра Аманда становится заметно холоднее."
            $ household_ai_raise_friction(0.06)
            $ AmandaVar["jealousy"] = amanda_ai_int(AmandaVar.get("jealousy", 0), 0) + 1

        "Назвать это ревностью":
            "Аманда смотрит прямо на вас."
            "Аманда: Осторожнее. Если ты даешь чему-то имя, я могу решить это доказать."
            $ AmandaPreferenceKnown["being_watched"] = 1

    return


label AmandaMiniEvent_NewDressPressure:

    "Аманда то и дело поправляет старую ткань на себе во время работы."

    "Не потому, что ее нужно поправлять. А потому, что она хочет, чтобы вы заметили: ее давно пора заменить."

    "Аманда: Ирма могла бы сделать с этим платьем что-нибудь приличное."

    "Пауза."

    "Аманда: Если кому-то вообще есть дело, выгляжу я как служанка или как пугало."

    if amanda_ai_int(money, 0) < 100:
        "Аманда: Хотя, конечно, мечты дешевле ткани."

    menu:
        "Пообещать улучшения потом":
            "Аманда: Опять обещания на потом. Надо уже складывать их в отдельную корзину."
            $ AmandaVar["dress_request_day"] = dayspassed

        "Сказать, что позже поговорите с Ирмой":
            "Аманда на миг оживляется, но тут же прячет это."
            "Аманда: Позже, значит. Я запомню это слово."
            $ AmandaVar["revealing_dress_ordered"] = max(amanda_ai_int(AmandaVar.get("revealing_dress_ordered", 0), 0), 1)
            $ household_ai_reduce_drive("amanda", 0.12)

        "Сказать, что припасы важнее":
            "Аманда: Трактир всегда ест первым."
            $ household_ai_raise_friction(0.05)

    return


label AmandaMiniEvent_EavesdropCaught:

    "За дверью слышится движение."

    "Когда вы открываете дверь, Аманда замирает на месте."

    "Аманда: Я не подслушивала."

    "Она говорит это слишком быстро."

    menu:
        "Обвинить ее":
            "Аманда: Тогда перестаньте говорить так, будто тайны - это еда, а я голодная."
            $ household_ai_raise_friction(0.05)
            $ AmandaVar["eavesdrop_caught"] = amanda_ai_int(AmandaVar.get("eavesdrop_caught", 0), 0) + 1

        "Спросить, что она услышала":
            "Аманда отводит взгляд, потом снова смотрит на вас."
            "Аманда: Достаточно, чтобы понять: здесь каждый чего-то хочет."
            $ AmandaVar["gossip_interest"] = 1

        "Дать ей уйти":
            "Аманда тут же исчезает в коридоре, и это почти ответ."
            $ AmandaVar["eavesdrop_escaped_day"] = dayspassed

    return


label AmandaMiniEvent_HuntingInterest:

    "Аманда смотрит, как вы разбираете охотничьи припасы."

    "Мех, кожа, инструменты - маленькие признаки того, что мир за пределами трактира еще может принести в дом что-то полезное."

    "Аманда: Люди иначе выглядят, когда могут позволить себе хоть немного удобства."

    menu:
        "Пообещать лучшие дни":
            "Аманда: Тогда проживи достаточно долго, чтобы они случились."
            $ household_ai_raise_convergence(0.03)

        "Пообещать ей что-нибудь теплое позже":
            "Аманда делает вид, что ей все равно, и не справляется."
            $ AmandaVar["fur_interest"] = 1
            $ AmandaVar["comfort_promise_day"] = dayspassed

        "Сказать, что все стоит денег":
            "Аманда: Да. Я заметила. Поэтому и смотрю, что ты приносишь обратно."
            $ household_ai_raise_friction(0.04)

    return


label AmandaMiniEvent_BreakfastMockery:

    "Завтрак начинается тихо."

    "Даже слишком тихо."

    "Аманда: Ну что. Кто кого вчера разочаровал?"

    "Мелисса едва не давится напитком."

    if "sandra" in list(getNPCids(CurLoc) or []):
        "Сандра: Мы можем хоть одно утро прожить без яда?"
        "Аманда: Нет. Но можем подать его теплым."

    menu:
        "Дать столу выдохнуть":
            "Насмешки продолжаются, но никто не уходит. Иногда и это считается миром."
            $ household_ai_raise_friction(0.04)

        "Велеть Аманде вести себя прилично":
            "Аманда: Ты говоришь как Сандра."
            $ household_ai_reduce_drive("amanda", 0.06)

        "Спросить, кого она имеет в виду":
            "Аманда ухмыляется."
            "Аманда: Если ты не знаешь, это еще смешнее."
            $ AmandaVar["breakfast_mockery_day"] = dayspassed

    return


label AmandaMiniEvent_LateNightWindow:

    "Поздно ночью вы замечаете Аманду у окна."

    "Вообще-то она должна спать."

    "Аманда: Не смогла."

    "Она смотрит, как дождь стекает по стеклу."

    if amanda_ai_household_value("pressure", 0.0) > 0.6:
        "Аманда: Когда с деньгами туго, все чего-то хотят друг от друга. От этого стены будто становятся теснее."

    menu:
        "Сесть рядом":
            "Аманда чуть склоняется к вашему плечу, хотя никогда в этом не признается."
            $ Friends["amanda"] = amanda_ai_int(Friends.get("amanda", 0), 0) + 1
            $ household_ai_reduce_drive("amanda", 0.10)

        "Спросить, чего она хочет":
            "Аманда: Больше, чем это место сейчас может себе позволить. В этом ведь и проблема, да?"
            $ AmandaVar["future_security_talk_day"] = dayspassed

        "Велеть ей спать":
            "Аманда тихо смеется."
            "Аманда: Вот опять. Приказы."
            $ household_ai_raise_friction(0.03)

    return


label AmandaMiniEvent_AsksWorkDirection:

    "Аманда стоит, уперев руки в бока, и ждет."

    "Аманда: Пока потом никто не начал жаловаться, скажи сейчас: куда меня ставишь?"

    "Под полезным вопросом прячется вызов."

    menu:
        "Кухня":
            $ jobkitchen["amanda"] = "amanda"
            $ jobwaitress["amanda"] = ""
            $ jobcleaning["amanda"] = ""
            "Аманда: Ладно. Если еда сгорит, сперва обвиню огонь, потом тебя."
            $ household_ai_raise_convergence(0.04)

        "Зал":
            $ jobwaitress["amanda"] = "amanda"
            $ jobkitchen["amanda"] = ""
            $ jobcleaning["amanda"] = ""
            "Аманда: Значит, хочешь меня туда, где все могут глазеть. Полезно."
            $ AmandaPreferenceKnown["being_watched"] = 1

        "Уборка":
            $ jobcleaning["amanda"] = "amanda"
            $ jobkitchen["amanda"] = ""
            $ jobwaitress["amanda"] = ""
            "Аманда: Конечно. Самая блистательная судьба."
            $ household_ai_reduce_drive("amanda", 0.08)

        "Решить позже":
            "Аманда: Позже - это место, где планы гниют."
            $ household_ai_raise_friction(0.05)

    return


label AmandaMiniEvent_PovertyComplaint:

    "Аманда оглядывает комнату, потом полки, потом ваше лицо."

    "Аманда: Мы опять притворяемся."

    "Она кивает на обычные признаки нехватки: скудные припасы, усталые лица, работу, растянутую на слишком многих."

    "Аманда: Если на всех не хватает, все начинают становиться хитрее. Ты ведь это понимаешь?"

    menu:
        "Сказать, что вы понимаете":
            "Аманда чуть смягчается, потому что вы хотя бы не врете."
            $ household_ai_raise_convergence(0.05)

        "Велеть ей прекратить жаловаться":
            "Аманда: Жалобами люди называют правду, когда не могут позволить себе ее исправить."
            $ household_ai_raise_friction(0.06)

        "Спросить, что она исправила бы первым":
            "Аманда: Еду. Чистую ткань. Потом что-нибудь красивое, пока мы все не забыли, ради чего вообще стоит выживать."
            $ AmandaVar["scarcity_priority_hint"] = 1

    return
