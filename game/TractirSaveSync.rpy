default saveVersion = 1
define currentVersion = 69

init -100 python:
    class ModuleRuntimeState(object):
        """Retired load-only type for saves made with the redundant module store."""
        pass

    class SergioPetData(PeopleData):
        """Retired load-only type for saves made with the accidental Sergio pet NPC."""
        pass

    class SergioPetInfo(BaseNPC):
        """Retired load-only type for saves made with the accidental Sergio pet NPC."""
        pass

    def beforeLoadTractirSave():
        ensure_game_item_registry()

    def tractir_save_patch_loaded_state():
        ensure_game_item_registry()
        people.repair()
        rooms.repair()
        tractir_save_normalize_tavern_staff_jobs()
        calendar_v2.time_advance_blocked = 0
        legacy_current_day = globals().pop("CurDay", None)
        next_day_runtime.update()
        if isinstance(legacy_current_day, dict):
            next_day_runtime.current_day = dict(legacy_current_day)
        globals().pop("TotalEventsSummary", None)
        tractir_save_clear_retired_npc_state()
        tractir_save_clear_retired_kids_scratch()
        tractir_save_normalize_player_arousal()
        tractir_save_normalize_player_church_state()
        tractir_save_normalize_sex_positions()
        tractir_save_normalize_rooms()
        tractir_save_remove_owned_unique_items_from_rooms()
        tractir_save_clear_room_ui_cache()

    def tractir_save_normalize_tavern_staff_jobs():
        for person in ("sandra", "melissa", "amanda"):
            info = people.get_info(person)
            jobs = getattr(info, "jobs", None) if info is not None else None
            if not isinstance(jobs, dict):
                continue
            for current_key, tomorrow_key in (
                ("jobkitchen", "jobkitchentomorrow"),
                ("jobcleaning", "jobcleaningtomorrow"),
                ("jobwaitress", "jobwaitresstomorrow"),
            ):
                if tomorrow_key not in jobs:
                    info.set_job_value(tomorrow_key, int(info.job_value(current_key, 0) or 0))

    def tractir_save_clear_retired_npc_state():
        globals().pop("SergioPet", None)
        globals().pop("SergioPetStaticData", None)
        people.runtime.pop("sergio_pet", None)
        people.definitions.pop("sergio_pet", None)

        for person_info in people.values():
            if person_info is not None and hasattr(person_info, "location"):
                delattr(person_info, "location")

        dog_obj = globals().get("dog")
        if isinstance(dog_obj, DogCompanion):
            if not hasattr(dog_obj, "stray_hidden_day"):
                dog_obj.stray_hidden_day = -1
            dog_obj.__dict__.pop("spawn_day", None)
            dog_obj.__dict__.pop("spawn_location", None)
            dog_obj.__dict__.pop("wearing_bloomers", None)

        amanda_obj = globals().get("Amanda")
        amanda_var = getattr(amanda_obj, "var", None)
        if isinstance(amanda_var, dict):
            for key in (
                "alberdanceadvance", "legare_dance_thread_stage", "legare_dance_private_seen", "legare_dance_pending",
                "tavern_seduction_seen_day", "legare_tavern_visit_seen_day",
                "street_legare_sighting_seen_day", "street_lover_encounter_seen_day",
                "liza_talk_seen_day", "liza_glory_invite_event_seen_day",
                "glory_tavern_aftermath_seen_day", "night_after_glory_seen_day",
                "liza_glory_hint_seen_day", "glory_liza_invite_seen",
                "glory_liza_invite_day", "glory_last_event_day",
                "talk_work_tip_day", "talk_look_opinion_day",
                "revealing_dress_code", "dress_request_satisfied", "attention_hint_day",
                "beauty_help_terms_accepted", "beauty_help_approved_day", "barber_request_interest",
                "night_tease_seen", "night_tease_scene_active", "night_tease_resolved",
                "mc_dance_after_seen", "mc_dance_makeout_seen", "mc_dance_sex_seen",
                "mc_dance_private_walks", "mc_dance_last_day", "body_state_stamp",
                "needs_bandage", "need_blocked",
                "night_bowl_window_seen_day", "attic_window_morning_day",
            ):
                amanda_var.pop(key, None)

        for character_name in ("Georgett", "Liza"):
            character_obj = globals().get(character_name)
            character_var = getattr(character_obj, "var", None)
            if isinstance(character_var, dict):
                character_var.pop("after_sermon_stage", None)

        gerhard_obj = globals().get("Gerhard")
        gerhard_var = getattr(gerhard_obj, "var", None)
        if isinstance(gerhard_var, dict):
            for key in (
                "confession_intro_done", "sermon_story_stage", "becky_advice_stage",
                "georgett_confession_stage", "liza_confession_stage", "lasttalkday",
            ):
                gerhard_var.pop(key, None)

        sandra_obj = globals().get("Sandra")
        sandra_var = getattr(sandra_obj, "var", None)
        if isinstance(sandra_var, dict):
            for key in (
                "WeeklyChoreCheckScore", "WeeklyChoreCheckCounter", "WeeklyChoreCheckEval",
                "Week5WakePending", "RoomUnlocked", "FinalRewardDone",
                "NightThanksReady", "NightThanksLastDay", "SandraSex",
            ):
                sandra_var.pop(key, None)
        if sandra_obj is not None:
            for field_name in (
                "weekly_chore_score", "weekly_chore_counter", "weekly_chore_eval",
                "weekly_wake_pending", "room_unlocked_flag", "final_reward_flag",
                "night_thanks_ready_flag", "night_thanks_last_day",
            ):
                if hasattr(sandra_obj, field_name):
                    delattr(sandra_obj, field_name)

        melissa_obj = globals().get("Melissa")
        if melissa_obj is not None:
            for field_name in (
                "intimacy_start_day", "intimacy_start_count", "intimacy_start_total",
            ):
                if hasattr(melissa_obj, field_name):
                    delattr(melissa_obj, field_name)

        robin_obj = globals().get("Robin")
        robin_var = getattr(robin_obj, "var", None)
        if isinstance(robin_var, dict):
            for key in ("PlayerDestroyedCamp", "ZimmerPeaceful"):
                robin_var.pop(key, None)

        zimmer_obj = globals().get("Zimmer")
        zimmer_var = getattr(zimmer_obj, "var", None)
        if isinstance(zimmer_var, dict):
            for key in ("MissionUpdatedByPlayer", "PlayerHandledRobin"):
                zimmer_var.pop(key, None)

    def tractir_save_normalize_sex_positions():
        legacy_names = (
            "CockInPussy", "CockInMouth", "CockInTits",
            "YouCockInPussy", "YouCockInMouth", "YouCockInTits",
            "EddieCockInPussy", "EddieCockInMouth", "EddieCockInTits",
        )
        legacy = {}
        for old_name in legacy_names:
            legacy[old_name] = dict(globals().pop(old_name, {}) or {})

        actor_sources = {
            "you": {
                "pussy": ("CockInPussy", "YouCockInPussy"),
                "mouth": ("CockInMouth", "YouCockInMouth"),
                "tits": ("CockInTits", "YouCockInTits"),
            },
            "eddie": {
                "pussy": ("EddieCockInPussy",),
                "mouth": ("EddieCockInMouth",),
                "tits": ("EddieCockInTits",),
            },
        }
        for actor_key, position_sources in actor_sources.items():
            target_ids = set()
            for source_names in position_sources.values():
                for source_name in source_names:
                    target_ids.update(legacy[source_name].keys())
            for target_id in target_ids:
                target = people.get_info(target_id)
                if target is None or target.cock_position(actor_key) != "none":
                    continue
                for position_key in ("pussy", "mouth", "tits"):
                    if any(people_to_int(legacy[source_name].get(target_id, 0), 0) for source_name in position_sources[position_key]):
                        target.set_cock_position(position_key, actor_key)
                        break

        player.intimacy.__dict__.pop("cock_positions", None)
        for person in people.values():
            state = getattr(person, "sex_state", None)
            if not isinstance(state, dict):
                continue
            positions = state.get("partner_positions", {})
            if not isinstance(positions, dict):
                positions = {}
            legacy_position = state.pop("cock_position", None)
            if legacy_position not in (None, "", "none") and "you" not in positions:
                positions["you"] = legacy_position
            for old_actor in list(positions.keys()):
                actor_key = str(old_actor or "you").strip().lower()
                if actor_key in ("mc", "stefan", "стефан"):
                    actor_key = "you"
                if actor_key != old_actor:
                    positions.setdefault(actor_key, positions.pop(old_actor))
            state["partner_positions"] = positions
            state.pop("cock_positions", None)

    def tractir_save_clear_retired_kids_scratch():
        if not isinstance(player.history, dict):
            return
        kids_state = player.history.get("kids")
        if isinstance(kids_state, dict):
            kids_state.pop("scratch", None)

    def tractir_save_normalize_player_arousal():
        legacy_arousal = globals().pop("Arousal", None)
        saved_arousal = getattr(player.intimacy, "arousal", 0)
        if hasattr(saved_arousal, "get"):
            saved_arousal = saved_arousal.get("You", saved_arousal.get("you", 0))
        elif hasattr(legacy_arousal, "get"):
            saved_arousal = legacy_arousal.get("You", legacy_arousal.get("you", saved_arousal))
        player.intimacy.arousal = player_clamp_value(saved_arousal, 0, 100)

    def tractir_save_normalize_player_church_state():
        intimacy = player.intimacy
        if not hasattr(intimacy, "ellona_blessed"):
            intimacy.ellona_blessed = 0
        if not hasattr(intimacy, "ellona_cursed"):
            intimacy.ellona_cursed = 0
        if not hasattr(intimacy, "ellona_curse_days"):
            intimacy.ellona_curse_days = 0
        if not hasattr(intimacy, "ellona_curse_reduction"):
            intimacy.ellona_curse_reduction = 0
        if not hasattr(intimacy, "ellona_grace_blessings") or len(list(intimacy.ellona_grace_blessings or [])) != 6:
            intimacy.ellona_grace_blessings = [0, 0, 0, 0, 0, 0]
        economy = player.economy
        if not hasattr(economy, "church_repairs_donated") or len(list(economy.church_repairs_donated or [])) != 10:
            economy.church_repairs_donated = [0] * 10

    def tractir_save_normalize_rooms():
        for room_obj in list(rooms.values()):
            if room_obj is None or not hasattr(room_obj, "game_items"):
                continue
            room_obj.game_items = normalize_room_item_rows(getattr(room_obj, "game_items", []))
            room_obj.__dict__.pop("objects", None)
            if str(getattr(room_obj, "code_name", "") or "") == "TavernMain":
                room_obj.state.pop("closed_text", None)
                room_obj.state.pop("georgett_available", None)
                room_obj.state.pop("liza_available", None)
                room_obj.state.pop("glory_desc", None)
                room_obj.state.pop("extra_desc", None)
                room_obj.state.pop("block_events", None)

    def tractir_save_remove_owned_unique_items_from_rooms():
        inventory = player.inventory.items
        owned_unique = set()
        for item_id, raw_count in list(inventory.items()):
            item_key = get_object_id(item_id)
            if not item_key:
                continue
            if int(raw_count or 0) <= 0:
                continue
            item_obj = get_game_item(item_key)
            if item_obj is not None and not bool(getattr(item_obj, "stackable", False)):
                owned_unique.add(item_key)

        equipped_weapon = get_object_id(player.equipment.weapon)
        if equipped_weapon:
            owned_unique.add(equipped_weapon)

        if not owned_unique:
            return

        for room_obj in list(rooms.values()):
            if room_obj is None or not hasattr(room_obj, "game_items"):
                continue
            next_rows = [row for row in normalize_room_item_rows(getattr(room_obj, "game_items", [])) if get_object_id(row) not in owned_unique]
            room_obj.game_items = list(next_rows)

    def tractir_save_clear_room_ui_cache():
        main_ui_runtime.mode = "scene"
        main_ui_runtime.action_content = None
        main_ui_runtime.action_items = []
        main_ui_runtime.object_id = ""
        main_ui_runtime.inventory_dropdown_open = False
        main_ui_runtime.overlay = ""
        main_ui_runtime.girl_key = ""
        main_ui_runtime.selected_char = ""

        room_code = str(rooms.current_code or "").strip()
        if room_code == "":
            return

        room_obj = rooms.get(room_code)
        if room_obj is not None:
            main_ui_runtime.action_title = str(getattr(room_obj, "display_name", "") or room_code)

    def tractir_save_upgrade_people_registry():
        """Consume pre-registry save state once; never recreate retired stores."""
        global people
        if not isinstance(people, PeopleRegistry):
            people = PeopleRegistry()

        retired_info = globals().pop("people" + "Info", {})
        retired_data = globals().pop("people" + "Data", {})
        globals().pop("girl" + "s", None)
        globals().pop("secondary_" + "npcs", None)

        if isinstance(retired_info, dict):
            for raw_key, info in list(retired_info.items()):
                key = people_normalize_id(raw_key)
                if not key or info is None or people.get_info(key) is not None:
                    continue
                data = retired_data.get(raw_key, retired_data.get(key, None)) if isinstance(retired_data, dict) else None
                if data is None:
                    data = getattr(info, "data", None)
                if data is not None:
                    people.register(data, info)

        people.repair()
        return people

    def updateSave():
        global saveVersion
        tractir_save_upgrade_people_registry()
        if not hasattr(player.economy, "church_donated_today"):
            player.economy.church_donated_today = 0
        if not hasattr(player.tavern_management, "service"):
            player.tavern_management.service = PlayerTavernServiceState()

        try:
            loaded_version = int(saveVersion or 1)
        except (TypeError, ValueError):
            loaded_version = 1

        if loaded_version < 2:
            updateSave_V1()
            loaded_version = 2

        if loaded_version < 3:
            updateSave_V2()
            loaded_version = 3

        if loaded_version < 4:
            updateSave_V3()
            loaded_version = 4

        if loaded_version < 5:
            updateSave_V4()
            loaded_version = 5

        if loaded_version < 6:
            updateSave_V5()
            loaded_version = 6

        if loaded_version < 7:
            updateSave_V6()
            loaded_version = 7

        if loaded_version < 8:
            updateSave_V7()
            loaded_version = 8

        if loaded_version < 9:
            updateSave_V8()
            loaded_version = 9

        if loaded_version < 10:
            updateSave_V9()
            loaded_version = 10

        if loaded_version < 11:
            updateSave_V10()
            loaded_version = 11

        if loaded_version < 12:
            updateSave_V11()
            loaded_version = 12

        if loaded_version < 13:
            updateSave_V12()
            loaded_version = 13

        if loaded_version < 14:
            updateSave_V13()
            loaded_version = 14

        if loaded_version < 15:
            updateSave_V14()
            loaded_version = 15

        if loaded_version < 16:
            updateSave_V15()
            loaded_version = 16

        if loaded_version < 17:
            updateSave_V16()
            loaded_version = 17

        if loaded_version < 18:
            updateSave_V17()
            loaded_version = 18

        if loaded_version < 19:
            updateSave_V18()
            loaded_version = 19

        if loaded_version < 20:
            updateSave_V19()
            loaded_version = 20

        if loaded_version < 21:
            updateSave_V20()
            loaded_version = 21

        if loaded_version < 22:
            updateSave_V21()
            loaded_version = 22

        if loaded_version < 23:
            updateSave_V22()
            loaded_version = 23

        if loaded_version < 24:
            updateSave_V23()
            loaded_version = 24

        if loaded_version < 25:
            updateSave_V24()
            loaded_version = 25

        if loaded_version < 26:
            updateSave_V25()
            loaded_version = 26

        if loaded_version < 27:
            updateSave_V26()
            loaded_version = 27

        if loaded_version < 28:
            updateSave_V27()
            loaded_version = 28

        if loaded_version < 29:
            updateSave_V28()
            loaded_version = 29

        if loaded_version < 30:
            updateSave_V29()
            loaded_version = 30

        if loaded_version < 31:
            updateSave_V30()
            loaded_version = 31

        if loaded_version < 32:
            updateSave_V31()
            loaded_version = 32

        if loaded_version < 33:
            updateSave_V32()
            loaded_version = 33

        if loaded_version < 34:
            updateSave_V33()
            loaded_version = 34

        if loaded_version < 35:
            updateSave_V34()
            loaded_version = 35

        if loaded_version < 36:
            updateSave_V35()
            loaded_version = 36

        if loaded_version < 37:
            updateSave_V36()
            loaded_version = 37

        if loaded_version < 38:
            updateSave_V37()
            loaded_version = 38

        if loaded_version < 39:
            updateSave_V38()
            loaded_version = 39

        if loaded_version < 40:
            updateSave_V39()
            loaded_version = 40

        if loaded_version < 41:
            updateSave_V40()
            loaded_version = 41

        if loaded_version < 42:
            updateSave_V41()
            loaded_version = 42

        if loaded_version < 43:
            updateSave_V42()
            loaded_version = 43

        if loaded_version < 44:
            updateSave_V43()
            loaded_version = 44

        if loaded_version < 45:
            updateSave_V44()
            loaded_version = 45

        if loaded_version < 46:
            updateSave_V45()
            loaded_version = 46

        if loaded_version < 47:
            updateSave_V46()
            loaded_version = 47

        if loaded_version < 48:
            updateSave_V47()
            loaded_version = 48

        if loaded_version < 49:
            updateSave_V48()
            loaded_version = 49

        if loaded_version < 50:
            updateSave_V49()
            loaded_version = 50

        if loaded_version < 51:
            updateSave_V50()
            loaded_version = 51

        if loaded_version < 52:
            updateSave_V51()
            loaded_version = 52

        if loaded_version < 53:
            updateSave_V52()
            loaded_version = 53

        if loaded_version < 54:
            updateSave_V53()
            loaded_version = 54

        if loaded_version < 55:
            updateSave_V54()
            loaded_version = 55

        if loaded_version < 56:
            updateSave_V55()
            loaded_version = 56

        if loaded_version < 57:
            updateSave_V56()
            loaded_version = 57

        if loaded_version < 58:
            updateSave_V57()
            loaded_version = 58

        if loaded_version < 59:
            updateSave_V58()
            loaded_version = 59

        if loaded_version < 60:
            updateSave_V59()
            loaded_version = 60

        if loaded_version < 61:
            updateSave_V60()
            loaded_version = 61

        if loaded_version < 62:
            updateSave_V61()
            loaded_version = 62

        if loaded_version < 63:
            updateSave_V62()
            loaded_version = 63

        if loaded_version < 64:
            updateSave_V63()
            loaded_version = 64

        if loaded_version < 65:
            updateSave_V64()
            loaded_version = 65

        if loaded_version < 66:
            updateSave_V65()
            loaded_version = 66

        if loaded_version < 67:
            updateSave_V66()
            loaded_version = 67

        if loaded_version < 68:
            updateSave_V67()
            loaded_version = 68

        if loaded_version < 69:
            updateSave_V68()
            loaded_version = 69

        tractir_save_patch_loaded_state()
        saveVersion = int(currentVersion or loaded_version)

    def updateSave_V1():
        tractir_save_patch_loaded_state()

    def updateSave_V2():
        tractir_save_patch_loaded_state()

    def updateSave_V3():
        # These room values were schedule mirrors in older saves.  Clear them
        # once on load instead of mutating character state from people.location().
        melissa_obj = globals().get("Melissa")
        if melissa_obj is not None:
            temp_room = str(getattr(melissa_obj, "var", {}).get("temp_room", "") or "").strip()
            if hasattr(melissa_obj, "location") and str(melissa_obj.location or "").strip() in (temp_room, "TavernMelissaRoom", "TavernAmandaRoom"):
                delattr(melissa_obj, "location")

        for character_name in ("Liza", "Georgett"):
            character_obj = globals().get(character_name)
            if character_obj is not None and hasattr(character_obj, "location") and str(character_obj.location or "").strip() in ("TavernMain", "TavernClientRoom"):
                delattr(character_obj, "location")

    def updateSave_V4():
        werecat_state_obj = globals().get("werecat")
        state = getattr(werecat_state_obj, "var", None)
        if not isinstance(state, dict):
            return
        if int(state.get("adopted", 0) or 0) == 1:
            state["adopted_count"] = max(1, int(state.get("adopted_count", 0) or 0))

    def updateSave_V5():
        for person_id, info in people.items():
            if info is not None and getattr(info, "data", None) is None:
                canonical_data = people.get_data(person_id)
                if canonical_data is not None:
                    info.data = canonical_data

    def updateSave_V6():
        now_minute = max(0, int(calendar_v2.daysInGame or 0)) * 1440 + (int(calendar_v2.hour or 0) * 60) + int(calendar_v2.minute or 0)
        for object_name in ("TavernMainFireplaceObject", "TavernKitchenHearthObject"):
            fire_object = globals().get(object_name)
            state = getattr(fire_object, "state", None)
            if not isinstance(state, dict):
                continue
            legacy_units = max(0, int(state.pop("fire_units", 0) or 0))
            if int(state.get("fire_until_minute", 0) or 0) <= 0 and legacy_units > 0:
                state["fire_until_minute"] = now_minute + (legacy_units * 12 * 60)
            if int(state.get("fire_started_minute", 0) or 0) <= 0 and int(state.get("fire_until_minute", 0) or 0) > now_minute:
                state["fire_started_minute"] = max(0, int(state["fire_until_minute"]) - (12 * 60))

        water_object = globals().get("TavernKitchenCauldronObject")
        water_state = getattr(water_object, "state", None)
        if isinstance(water_state, dict):
            legacy_units = max(0, int(water_state.pop("hot_water_units", 0) or 0))
            if int(water_state.get("hot_water_until_minute", 0) or 0) <= 0 and legacy_units > 0:
                water_state["hot_water_until_minute"] = now_minute + (legacy_units * 24 * 60)

    def updateSave_V7():
        becky_obj = globals().get("Becky")
        becky_var = getattr(becky_obj, "var", None)
        if hasattr(becky_var, "pop"):
            legacy_knowledge = max(
                people_to_int(becky_var.pop("KnowBlackwood", 0), 0),
                people_to_int(becky_var.pop("KnowSherwood", 0), 0),
            )
            Becky.knows_blackwood = bool(max(
                people_to_int(getattr(Becky, "knows_blackwood", False), 0),
                legacy_knowledge,
            ))

    def updateSave_V8():
        combat_state = getattr(globals().get("player"), "combat", None)
        if combat_state is None:
            return
        legacy_name = "sup" + "ply"
        legacy_supply = getattr(combat_state, legacy_name, None)
        if not isinstance(getattr(combat_state, "special_supply", None), dict):
            combat_state.special_supply = {}
        if isinstance(legacy_supply, dict):
            combat_state.special_supply["bees_bomb"] = max(int(combat_state.special_supply.get("bees_bomb", 0) or 0), int(legacy_supply.get("bees_bomb", 0) or 0))
        combat_state.special_supply.setdefault("bees_bomb", 0)
        if hasattr(combat_state, legacy_name):
            delattr(combat_state, legacy_name)

    def updateSave_V9():
        werecat_obj = globals().get("werecat")
        state = getattr(werecat_obj, "var", None)
        if not isinstance(state, dict):
            return
        trap_rows = state.get("trap_rooms", {})
        if not isinstance(trap_rows, dict):
            trap_rows = {}
        legacy_room = str(state.pop("trap_room", "") or "").strip()
        legacy_day = int(state.pop("trap_day", -1) or -1)
        legacy_active = int(state.pop("trap_active", 0) or 0)
        if legacy_active == 1 and legacy_room and legacy_room not in trap_rows:
            trap_rows[legacy_room] = {"day": legacy_day}
        state["trap_rooms"] = dict(trap_rows)

    def updateSave_V10():
        sandra_obj = globals().get("Sandra")
        sandra_var = getattr(sandra_obj, "var", None)
        if sandra_obj is None or not isinstance(sandra_var, dict):
            return
        field_map = {
            "WeeklyChoreCheckScore": ("weekly_chore_score", 0),
            "WeeklyChoreCheckCounter": ("weekly_chore_counter", 0),
            "WeeklyChoreCheckEval": ("weekly_chore_eval", ""),
            "Week5WakePending": ("weekly_wake_pending", 0),
            "RoomUnlocked": ("room_unlocked_flag", 0),
            "FinalRewardDone": ("final_reward_flag", 0),
            "NightThanksReady": ("night_thanks_ready_flag", 0),
            "NightThanksLastDay": ("night_thanks_last_day", -1),
        }
        for old_key, field_data in field_map.items():
            field_name, default_value = field_data
            if old_key not in sandra_var:
                continue
            old_value = sandra_var.pop(old_key)
            if field_name == "weekly_chore_eval":
                setattr(sandra_obj, field_name, str(old_value or ""))
            else:
                setattr(sandra_obj, field_name, int(old_value if old_value is not None else default_value))
        if "SandraSex" in sandra_var:
            sandra_obj.final_reward_flag = max(
                int(getattr(sandra_obj, "final_reward_flag", 0) or 0),
                int(sandra_var.pop("SandraSex") or 0),
            )
        for retired_key in ("MCVisitFirstReady", "MCVisitFirstPending", "MCVisitFirstDone"):
            sandra_var.pop(retired_key, None)

    def updateSave_V11():
        amanda_obj = globals().get("Amanda")
        amanda_var = getattr(amanda_obj, "var", None)
        if isinstance(amanda_var, dict):
            amanda_var.pop("cycle_phase", None)
            amanda_var.pop("cycle_day", None)
        if amanda_obj is not None and hasattr(amanda_obj, "fertility_cycle"):
            delattr(amanda_obj, "fertility_cycle")

    def updateSave_V12():
        for info in people.values():
            if info is None:
                continue
            for field_name in ("var", "sex_state"):
                if not isinstance(getattr(info, field_name, None), dict):
                    setattr(info, field_name, {})
            if hasattr(info, "stats") and not isinstance(getattr(info, "stats", None), dict):
                info.stats = {}
            if hasattr(info, "jobs") and not isinstance(getattr(info, "jobs", None), dict):
                info.jobs = {}

    def updateSave_V13():
        for info in people.values():
            if info is not None and hasattr(info, "lunar_fertility"):
                delattr(info, "lunar_fertility")

    def updateSave_V14():
        clara_obj = globals().get("Clara")
        clara_var = getattr(clara_obj, "var", None)
        if clara_obj is not None and isinstance(clara_var, dict) and "trust" in clara_var:
            clara_obj.trust = max(0, min(20, int(clara_var.pop("trust") or 0)))

    def updateSave_V15():
        # Tavern client selection is transient room state.  Builds through
        # version 15 copied it into persistent NPC location overrides.
        for character_name in ("Liza", "Georgett"):
            character_obj = globals().get(character_name)
            if character_obj is not None and hasattr(character_obj, "location") and str(character_obj.location or "").strip() in ("TavernMain", "TavernClientRoom"):
                delattr(character_obj, "location")

    def updateSave_V16():
        daily_runtime = globals().get("daily_events")
        rows = getattr(daily_runtime, "rows", None)
        if not isinstance(rows, list):
            return
        call_modes = {
            "BeckyQuestInit": "none",
            "GirlDressBuy": "girl",
            "DressNoShow": "girl",
            "MorningSickness": "girl",
            "GiveBirth": "girl",
            "MomDressComplaint": "girl",
            "CreateKid": "girl_location",
        }
        for row in rows:
            if not isinstance(row, dict):
                continue
            event_label = str(row.get("EventCode", "") or "").strip()
            row["CallMode"] = str(call_modes.get(event_label, "none"))

    def updateSave_V17():
        # These NPCs now derive presence from their schedule/default or from a
        # bounded class-owned story override. Clear stale permanent overrides.
        for character_name in ("Clara", "Draupnir", "Robin"):
            character_obj = globals().get(character_name)
            if character_obj is not None and hasattr(character_obj, "location"):
                delattr(character_obj, "location")

        dog_obj = globals().get("dog")
        if not isinstance(dog_obj, DogCompanion):
            dog_obj = DogCompanion()
            globals()["dog"] = dog_obj
        if not hasattr(dog_obj, "pet_name"):
            old_name = str(getattr(dog_obj, "name", "") or "").strip()
            dog_obj.pet_name = old_name if old_name and old_name != "dog" else "Пес"
        for field_name, default_value in (
            ("stray_played", False),
            ("last_play_day", -1),
            ("last_train_day", -1),
        ):
            if not hasattr(dog_obj, field_name):
                setattr(dog_obj, field_name, default_value)
        dog_obj.name = "dog"
        people.register(DogStaticData, dog_obj)

        if not isinstance(getattr(player.combat, "special_supply", None), dict):
            player.combat.special_supply = {}
        player.combat.special_supply.setdefault("bees_bomb", 0)
        if not isinstance(getattr(fight, "last_result", None), dict):
            fight.last_result = {}
        if not isinstance(getattr(fight, "enemy_party", None), list):
            fight.enemy_party = []
        if not isinstance(getattr(fight, "status_state", None), dict):
            fight.status_state = {}
        player.set_stat("health", _player_clamp_stat(player.condition.health, 0, 100))

    def updateSave_V18():
        # Presence for these NPCs is now schedule-owned. Older builds stored
        # their normal venue in the instance override, masking the schedule.
        legacy_schedule_locations = {
            "Eddie": "GroceryStore",
            "Alber": "WineStore",
            "Inga": "BeckyHome",
            "Sergio": "ArtisansQuarter",
        }
        for character_name, legacy_location in legacy_schedule_locations.items():
            character_obj = globals().get(character_name)
            if character_obj is not None and hasattr(character_obj, "location") and str(character_obj.location or "").strip() == legacy_location:
                delattr(character_obj, "location")

        mongol_obj = globals().get("Mongol")
        if mongol_obj is not None and hasattr(mongol_obj, "location"):
            delattr(mongol_obj, "location")

    def updateSave_V19():
        # Look is derived from PlayerAppearance. Promote the only temporary
        # appearance bonus, then remove the saved/stat and crafting mirrors.
        appearance = player.appearance
        legacy_until = int(getattr(crafting, "soap_look_bonus_until_day", -1) or -1)
        if not hasattr(appearance, "soap_look_bonus"):
            appearance.soap_look_bonus = 0
        if not hasattr(appearance, "soap_look_bonus_until_day"):
            appearance.soap_look_bonus_until_day = -1
        if legacy_until >= int(appearance.soap_look_bonus_until_day or -1):
            appearance.soap_look_bonus_until_day = legacy_until
            if legacy_until >= int(calendar_v2.daysInGame or 0):
                appearance.soap_look_bonus = max(10, int(appearance.soap_look_bonus or 0))

        crafting_state = getattr(crafting, "__dict__", None)
        if hasattr(crafting_state, "pop"):
            crafting_state.pop("soap_look_bonus_until_day", None)
        stats_state = getattr(player.stats, "__dict__", None)
        if hasattr(stats_state, "pop"):
            stats_state.pop("look", None)

    def updateSave_V20():
        # Trap placement is owned only by HuntInfo.trap_rooms. Promote the
        # former summary map once when loading an older save, then retire it.
        trap_rows = getattr(hunt, "trap_rooms", {})
        if not isinstance(trap_rows, dict):
            trap_rows = {}
        legacy_state = getattr(hunt, "trap_state", None)
        if isinstance(legacy_state, dict):
            legacy_room = str(legacy_state.get("room", "") or "").strip()
            if int(legacy_state.get("active", 0) or 0) == 1 and legacy_room and legacy_room not in trap_rows:
                trap_rows[legacy_room] = {
                    "day": int(legacy_state.get("day", -1) or -1),
                    "armed_count": max(1, int(legacy_state.get("armed_count", 1) or 1)),
                }
        hunt.trap_rooms = dict(trap_rows)
        if hasattr(hunt, "trap_state"):
            delattr(hunt, "trap_state")

        # A duplicate constructor in the previous build omitted these live
        # street-event collections from newly created runtime objects.
        if not isinstance(getattr(TownStreet, "blackworkers", None), list):
            TownStreet.blackworkers = []
        if not isinstance(getattr(TownStreet, "blackworker_candidates", None), list):
            TownStreet.blackworker_candidates = []

    def updateSave_V21():
        people.repair()

    def updateSave_V22():
        # Melissa's bat quest now keeps progression only in its story thread.
        # Promote the retired NPC phase once, then remove it permanently.
        melissa_obj = globals().get("Melissa")
        melissa_var = getattr(melissa_obj, "var", None)
        if not isinstance(melissa_var, dict) or "bats_episode" not in melissa_var:
            return
        initThreads()
        bat_thread = globals().get("threads", {}).get("melissaBatProblem", None)
        if bat_thread is None:
            return
        legacy_stage = max(0, min(int(melissa_var.pop("bats_episode", 0) or 0), 8))
        if legacy_stage >= 8:
            bat_thread.advanceTo(8, complete_at_end=True, force_active=False)
            return
        bat_thread.advanceTo(legacy_stage, force_active=legacy_stage > 0)

    def updateSave_V23():
        # Becky's husband history is one ordered story thread. Promote the
        # retired numeric NPC stage once and remove the four one-event threads.
        becky_obj = globals().get("Becky")
        becky_var = getattr(becky_obj, "var", None)
        initThreads()
        thread_rows = globals().get("threads", {})
        husband_thread = thread_rows.get("beckyHusbandBackstory", None)
        legacy_stage = 0
        if isinstance(becky_var, dict):
            legacy_stage = max(0, min(int(becky_var.pop("husbandtalk", 0) or 0), 5))
        if husband_thread is not None:
            target = max(0, legacy_stage - 1)
            husband_thread.advanceTo(target, complete_at_end=target >= 4, force_active=legacy_stage > 0 and target < 4)
        for retired_name in (
            "beckyHusbandFirstTalk",
            "beckyHusbandSecondTalk",
            "beckyHusbandThirdTalk",
            "beckyHusbandFourthTalk",
        ):
            thread_rows.pop(retired_name, None)

    def updateSave_V24():
        # Becky witnessing Inga and the three follow-up talks are one ordered
        # thread. Promote the retired NPC stage once, then remove old threads.
        becky_obj = globals().get("Becky")
        becky_var = getattr(becky_obj, "var", None)
        initThreads()
        thread_rows = globals().get("threads", {})
        inga_thread = thread_rows.get("beckyIngaLucasPath", None)
        legacy_stage = 0
        if isinstance(becky_var, dict):
            legacy_stage = max(0, min(int(becky_var.pop("SawIngaFuck", 0) or 0), 4))
            becky_var.pop("HomeFrontCheckedDay", None)
        if inga_thread is not None:
            inga_thread.advanceTo(
                legacy_stage,
                complete_at_end=legacy_stage >= 4,
                force_active=legacy_stage > 0 and legacy_stage < 4,
            )
        for retired_name in (
            "beckyIngaFirstTalk",
            "beckyIngaSecondTalk",
            "beckyLucasTalk",
            "beckyHomeFrontIngaLucas",
        ):
            thread_rows.pop(retired_name, None)

    def updateSave_V25():
        # Becky's two Eddie topics are one ordered story progression. Promote
        # the retired scalar once, then discard the former one-event threads.
        becky_obj = globals().get("Becky")
        becky_var = getattr(becky_obj, "var", None)
        initThreads()
        thread_rows = globals().get("threads", {})
        eddie_thread = thread_rows.get("beckyEddieBackstory", None)
        legacy_stage = 0
        if isinstance(becky_var, dict):
            legacy_stage = max(0, min(int(becky_var.pop("eddietalk", 0) or 0), 2))
        if eddie_thread is not None:
            eddie_thread.advanceTo(legacy_stage, complete_at_end=legacy_stage >= 2, force_active=legacy_stage > 0)
        for retired_name in ("beckyEddieFirstTalk", "beckyEddieGeorgettTalk"):
            thread_rows.pop(retired_name, None)

    def updateSave_V26():
        # These Becky choices are repeatable talk topics, not story threads.
        # Remove thread records created by the incorrect one-shot conversion.
        thread_rows = globals().get("threads", {})
        for retired_name in (
            "beckyHomeInviteTalk",
            "beckyHomeLastVisitTalk",
            "beckyEddieBehaviorTalk",
            "beckyEddieGeorgMentionTalk",
            "beckyEddieReactionTalk",
            "beckyEddieAfterSexTalk",
            "beckyPregnancyFatherTalk",
        ):
            thread_rows.pop(retired_name, None)

    def updateSave_V27():
        # Sherwood follow-ups are conditional Becky talk topics. Their branch
        # facts remain on Becky; the former one-event thread records do not.
        thread_rows = globals().get("threads", {})
        for retired_name in (
            "beckySherwoodOfferTalk",
            "beckySherwoodElvesTalk",
            "beckySherwoodFingalTalk",
            "beckySherwoodWarnTalk",
            "beckySherwoodRoadTalk",
            "beckySherwoodLiedTalk",
            "beckySherwoodRobbedTalk",
            "beckySherwoodHowToTalk",
            "beckySherwoodWarnedTalk",
        ):
            thread_rows.pop(retired_name, None)

    def updateSave_V28():
        thread_rows = threads
        if not isinstance(thread_rows, dict):
            return
        for retired_name in (
            "beckyHomeVisitEntry",
            "beckyHomeDanceArrival",
            "beckyHomeDinnerBedroom",
            "beckyHomeEddieBedroom",
        ):
            thread_rows.pop(retired_name, None)

    def updateSave_V29():
        # Sandra's weekly story progression now lives only in its event thread;
        # the chore system owns the last evaluated score and result.
        initThreads()
        sandra_obj = globals().get("Sandra")
        sandra_thread = globals().get("threads", {}).get("sandraWeeklyEvaluation", None)
        chores_obj = getattr(globals().get("player"), "chores", None)
        if sandra_obj is None or sandra_thread is None or chores_obj is None:
            return

        chores_obj.last_score = max(0, int(getattr(sandra_obj, "weekly_chore_score", getattr(chores_obj, "last_score", 0)) or 0))
        chores_obj.last_evaluation = str(getattr(sandra_obj, "weekly_chore_eval", getattr(chores_obj, "last_evaluation", "")) or "")

        legacy_counter = max(0, int(getattr(sandra_obj, "weekly_chore_counter", 0) or 0))
        legacy_pending = int(getattr(sandra_obj, "weekly_wake_pending", 0) or 0) > 0
        legacy_room_unlocked = int(getattr(sandra_obj, "room_unlocked_flag", 0) or 0) > 0
        legacy_night_ready = int(getattr(sandra_obj, "night_thanks_ready_flag", 0) or 0) > 0
        legacy_final_reward = int(getattr(sandra_obj, "final_reward_flag", 0) or 0) > 0

        if legacy_final_reward:
            sandra_thread.advanceTo(5, complete_at_end=True)
        elif legacy_night_ready:
            sandra_thread.advanceTo(4, force_active=True)
        elif legacy_pending:
            pending_stage = max(0, min(legacy_counter - 1, 3))
            sandra_thread.advanceTo(pending_stage, force_active=True)
            sandra_thread.day = int(current_game_day() or 0)
        else:
            if legacy_room_unlocked and int(sandra_thread.num or 0) < 1:
                sandra_thread.advanceTo(1)
            if int(sandra_thread.num or 0) >= 4 and bool(sandra_thread.completed):
                sandra_thread.advanceTo(4, force_active=True)
            elif not sandra_thread.completed:
                sandra_thread.disable()

    def updateSave_V30():
        # Street events now keep one daily event ledger. The former location,
        # label, plan, text, and context copies were saved mirrors.
        for retired_name in (
            "daily_plan",
            "last_event_text",
            "context",
            "fired_labels_today",
            "fired_locations_today",
        ):
            if hasattr(TownStreet, retired_name):
                delattr(TownStreet, retired_name)
        for retired_name in ("ending_title", "ending_body"):
            if hasattr(tractir_progress, retired_name):
                delattr(tractir_progress, retired_name)

    def updateSave_V31():
        # The vscene statement now owns its media/controller state as one
        # runtime object instead of three independent store variables.
        legacy_movie = bool(globals().pop("sceneMovie", False))
        legacy_fullscreen = bool(globals().pop("sceneFullScreen", False))
        globals().pop("vcFromTimer", None)
        scene_runtime.movie = legacy_movie
        scene_runtime.fullscreen = legacy_fullscreen
        scene_runtime.controller_from_timer = False

    def updateSave_V32():
        # Blind Pirate is one ordered two-chapter thread. Older saves kept the
        # breakfast chapter in player.history after completing the thread.
        # The retired checkpoint shim also stored two values that no system read.
        globals().pop("_tractir_progress_revision", None)
        globals().pop("_tractir_last_autosave_reason", None)
        history = getattr(player, "history", None)
        legacy_stage = int(history.pop("blind_pirate_stage", 0) or 0) if isinstance(history, dict) else 0
        blind_pirate_thread = threads.get("cityBlindPirateFall", None)
        if blind_pirate_thread is None:
            return
        if legacy_stage >= 2:
            blind_pirate_thread.advanceTo(blind_pirate_thread.data.length, complete_at_end=True)
        elif legacy_stage == 1:
            blind_pirate_thread.advanceTo(1, force_active=True)

    def updateSave_V33():
        # Room entry resolves presence and event results directly. The former
        # saved object only cached copies of those values.
        globals().pop("room_entry_runtime", None)

    def updateSave_V34():
        # SceneRuntimeState is the sole saved authority for the picture shown
        # by vscene and the main UI. Preserve the old layout value when that
        # name existed because it was the former resolver's first priority.
        legacy_layout_present = "_layout_last_picture" in globals()
        legacy_scene_present = "scene_image" in globals()
        legacy_layout = globals().pop("_layout_last_picture", "")
        legacy_scene = globals().pop("scene_image", "")
        if legacy_layout_present:
            scene_runtime.picture = str(legacy_layout or "")
        elif legacy_scene_present:
            scene_runtime.picture = str(legacy_scene or "")
        elif not hasattr(scene_runtime, "picture"):
            scene_runtime.picture = ""

    def updateSave_V35():
        # The room registry now owns the current location code and derives the
        # current Room object. Retire both former store-level authorities once.
        legacy_code = str(globals().pop("CurLoc", "") or "").strip()
        legacy_room = globals().pop("CurrentRoom", None)
        if legacy_code == "":
            legacy_code = str(getattr(legacy_room, "code_name", "") or "").strip()
        rooms.enter(legacy_code or "TavernMain")

    def updateSave_V36():
        # Schedule rules are clock intervals. Convert the retired display-slot
        # schema once, then remove it instead of keeping a live compatibility
        # branch in every NPC schedule read.
        slot_bounds = {
            0: (360, 480), 1: (480, 660), 2: (660, 780), 3: (780, 960),
            4: (960, 1080), 5: (1080, 1260), 6: (1260, 1380), 7: (1380, 360),
        }

        def legacy_interval(slot_values):
            slots = sorted(set([int(value or 0) for value in list(slot_values or [])]))
            if not slots:
                return (0, 1440)
            return (slot_bounds[slots[0]][0], slot_bounds[slots[-1]][1])

        def migrate_entry(entry):
            state = getattr(entry, "__dict__", {})
            old_slots = list(state.pop("time_slots", []) or [])
            if "start_minute" not in state or "end_minute" not in state:
                if old_slots:
                    state["start_minute"], state["end_minute"] = legacy_interval(old_slots)
                else:
                    state["start_minute"] = int(state.pop("start_hour", 0) or 0) * 60
                    state["end_minute"] = int(state.pop("end_hour", 24) or 0) * 60
            state.pop("start_hour", None)
            state.pop("end_hour", None)

        for data in people.data_values():
            for entry in list(getattr(data, "schedule_entries", []) or []):
                migrate_entry(entry)
            template = getattr(data, "daily_schedule_template", None)
            if not isinstance(template, dict):
                continue
            for old_key, new_key in (("default_slots", "default_intervals"), ("random_slots", "random_intervals")):
                rows = list(template.pop(old_key, []) or [])
                intervals = list(template.get(new_key, []) or [])
                for row in rows:
                    migrated = dict(row or {})
                    migrated["start_minute"], migrated["end_minute"] = legacy_interval([migrated.pop("slot", 0)])
                    intervals.append(migrated)
                template[new_key] = intervals

    def updateSave_V37():
        # MainUIRuntimeState is now the sole owner of display projection state.
        # Consume the former store-level values once; normal UI code never
        # reads or writes those names again.
        field_defaults = (
            ("current_action_title", "action_title", "Actions"),
            ("current_action_content", "action_content", None),
            ("current_action_items", "action_items", []),
            ("current_girl_key", "girl_key", ""),
            ("current_talk_picture", "talk_picture", ""),
            ("current_object_id", "object_id", ""),
            ("UI_mode", "mode", "scene"),
            ("UI_selected_char", "selected_char", ""),
            ("main_ui_inventory_dropdown_open", "inventory_dropdown_open", False),
            ("main_ui_overlay", "overlay", ""),
            ("player_inventory_view_mode", "inventory_view_mode", "profile"),
            ("player_inventory_view_section", "inventory_view_section", ""),
            ("player_inventory_view_item", "inventory_view_item", ""),
            ("player_card_inventory_origin", "inventory_origin", "profile"),
            ("story_board_selected_person", "story_board_person", "melissa"),
        )
        for old_name, field_name, default_value in field_defaults:
            value = globals().pop(old_name, default_value)
            if isinstance(default_value, list):
                value = list(value or [])
            setattr(main_ui_runtime, field_name, value)

    def updateSave_V38():
        # SceneRuntimeState owns the rendered text just as it owns the picture.
        # Preserve the two former meanings once: active text and the location
        # text restored after temporary object/card views.
        scene_runtime.text = globals().pop("MainTxt", getattr(scene_runtime, "text", ""))
        scene_runtime.location_text = globals().pop("CurLocDesc", getattr(scene_runtime, "location_text", ""))

    def updateSave_V39():
        # The tavern system owns the Glory Hole interaction session. Consume
        # scratch store values left by the former menu implementation once.
        if not hasattr(player.tavern_management, "glory_hole_session"):
            player.tavern_management.glory_hole_session = PlayerGloryHoleSessionState()
        for old_name in (
            "GirlNameTGH", "GloryHoleCurrentStep", "CockInGloryHole",
            "GloryHoleInside", "GloryHoleInsideOnce", "GloryHoleWorks",
            "GloryLine1", "GloryLine2", "GloryLine3",
            "GloryGirlLine0", "GloryGirlLine1", "GloryGirlLine2", "GloryGirlLine3",
            "BlockGloryHoleMenu", "AmandaAtGlory",
            "GloryHoleYouLine1", "GloryHoleYouLine2", "GloryHoleYouLine3",
        ):
            globals().pop(old_name, None)

    def updateSave_V40():
        # Retired event scratch was only assigned and never read.
        globals().pop("SignalBlockTime", None)

    def updateSave_V41():
        # Dress-choice acceptance is now local to each interaction label.
        globals().pop("AgreedToRedress", None)

    def updateSave_V42():
        # Return text/results now use label parameters and Ren'Py return values.
        globals().pop("Result", None)

    def updateSave_V43():
        # FridayDanceRoom owns both venue progress and the active dance session.
        old_room = rooms.get("FridayDance")
        definition = roomDefinitions.get("FridayDance", None)
        if definition is not None:
            upgraded_room = definition.runtime_copy()
            if old_room is not None:
                upgraded_room.state.update(dict(getattr(old_room, "state", {}) or {}))
            rooms.register(upgraded_room)
        dance_room = rooms.get("FridayDance")
        if dance_room is None:
            return
        legacy_fields = (
            ("DanceStep", "step"),
            ("HandsDance", "hands"),
            ("KissDance", "kiss"),
            ("TitsDance", "tits"),
        )
        for old_name, field_name in legacy_fields:
            if old_name in globals():
                setattr(dance_room, field_name, globals().pop(old_name))
        legacy_max = max(
            int(globals().pop("DanceMaxIAD", 0) or 0),
            int(globals().pop("DanceMaxIBD", 0) or 0),
        )
        if legacy_max > 0:
            dance_room.max_step = legacy_max

    def updateSave_V44():
        # Amanda/Legare dance construction scratch is local to its label call.
        for old_name in ("DanceCreated", "ForceLegareFirstDance", "GoPhrase"):
            globals().pop(old_name, None)
        # Harassment event outcomes now travel through label arguments/returns.
        for old_name in ("CurEventDescPart2", "GirlRunAway", "GirlSlapped", "HarassType", "Eyewitness"):
            globals().pop(old_name, None)
        # Remaining event-choice scratch is likewise local to authored labels.
        for old_name in ("CurEventDesc", "YourReaction1", "YourReaction2", "NotToSpeak"):
            globals().pop(old_name, None)
        globals().pop("module_runtime", None)
        globals().pop("GirlNameIGSS", None)
        globals().pop("GirlLocIGSS", None)
        globals().pop("SomebodyCums", None)

    def updateSave_V45():
        # Preserve legacy per-girl intimacy state once, then retire its maps.
        legacy_cum_maps = (
            ("CumInsideYou", "cum_inside_you"),
            ("CumFaceYou", "cum_face_you"),
            ("CumTitsYou", "cum_tits_you"),
            ("CumMouthYou", "cum_mouth_you"),
            ("CumInsideOthers", "cum_inside_others"),
            ("CumFaceOthers", "cum_face_others"),
            ("CumTitsOthers", "cum_tits_others"),
            ("CumMouthOthers", "cum_mouth_others"),
        )
        for old_name, state_key in legacy_cum_maps:
            old_values = globals().pop(old_name, {})
            if not isinstance(old_values, dict):
                continue
            for person_name, old_value in old_values.items():
                person = people.get_info(person_name)
                if not isinstance(person, Girl):
                    continue
                state = person.ensure_sex_state()
                state[state_key] = max(
                    people_to_int(state.get(state_key, 0), 0),
                    people_to_int(old_value, 0),
                )

        old_lick_values = globals().pop("LickPussy", {})
        if isinstance(old_lick_values, dict):
            for person_name, old_value in old_lick_values.items():
                person = people.get_info(person_name)
                if not isinstance(person, Girl):
                    continue
                state = person.ensure_sex_state()
                state["lick_pussy"] = max(
                    people_to_int(state.get("lick_pussy", 0), 0),
                    people_to_int(old_value, 0),
                )

        # Retired label-only scratch must not survive as saved store state.
        retired_scratch = (
            "IrmaMeasureShopStage", "IrmaSexShopStep",
            "HarrassmentAlreadyDiscussed", "InvitePoints", "ChangeMind",
            "TmpChurchGeorgSex", "CurSperm0", "CurSperm1", "CurSperm2",
            "BribeSize", "TodayEventsSummary", "TodayEventsSummaryTmp", "TimePeriodEvents",
            "_social_girl", "_social_mode", "_social_parent_mode", "_social_visible_ids",
            "_social_topic_id", "_social_result",
            "_hsi_picture", "_hsi_girl", "_hsi_action", "_hsi_reaction", "_hsi_eyewitness", "_hsi_info",
            "_hdi_girl", "_hdi_value", "_hdi_picture",
            "_discussion_text", "_girl_info", "_girl_corruption", "_harass_instruction", "_girl_dative",
            "GiveBirthTimer", "DaddySuspect1", "DaddySuspect2",
            "KidID", "KidDescription", "KidName", "KidGender",
            "GirlNameILT", "GirlLocILT",
            "BeckyStoreSexType", "ChooseOption", "GruzchikName", "GruzchikGirl",
            "GirlsCounter", "CurrentActions", "AddDancePhraseTmp",
            "RobinTmpDesc", "_fran_text", "_fran_topic_index", "_secret_item", "_secret_price",
            "DraupnirProfile", "ZimmerProfile", "RobinProfile", "EddieProfile", "LuisaProfile", "SergioProfile",
            "GirlNameTS1", "GirlNameTS2", "SexEventType",
            "AmandaNesluh", "AmandaArgue1", "AmandaArgue2", "Randvar", "AlberBribe",
            "AmandaLegareReactionRoll", "MaxStep", "VirginNotKnow", "GirlNameASDS", "GirlNameIAD",
            "BeckyGuestSexDesc", "KidsWatch", "GirlNameAC", "GirlNameIBD", "CounterToClean",
            "DressObman", "DressBuyIsRelative", "ShowOffLevel",
            "GirlSillyName", "TalkedBeforeTmp", "KidsOrPregTmp", "GirlNameSP",
            "TotalEventsSummary",
        )
        for old_name in retired_scratch:
            globals().pop(old_name, None)

    def updateSave_V46():
        # FightInfo owns encounter results; HuntInfo owns only hunt/trap state.
        # Promote the former cross-system result once, then retire the copy.
        legacy_hunt_result = getattr(hunt, "last_result", {})
        if not isinstance(getattr(fight, "last_result", None), dict):
            fight.last_result = {}
        if isinstance(legacy_hunt_result, dict) and not fight.last_result:
            fight.last_result = dict(legacy_hunt_result)
        if hasattr(hunt, "last_result"):
            delattr(hunt, "last_result")

        # Persistent ending state belongs to the progress system, not to the
        # transient enemy encounter. Preserve the old fatal enemy once.
        legacy_enemy_state = getattr(fight, "enemy_state", {})
        if not hasattr(tractir_progress, "boss_fatal_enemy"):
            tractir_progress.boss_fatal_enemy = ""
        if isinstance(legacy_enemy_state, dict) and int(legacy_enemy_state.get("fatal_loss", 0) or 0) > 0:
            tractir_progress.boss_fatal_enemy = str(legacy_enemy_state.get("fatal_enemy", "unknown") or "unknown")

        fight_state = getattr(fight, "__dict__", {})
        if hasattr(fight_state, "pop"):
            for retired_name in ("enemy_state", "side_log", "outcome_text", "outcome_popup"):
                fight_state.pop(retired_name, None)

        # PlayerCombat.party is the single combat-membership authority.
        dog_obj = globals().get("dog")
        if dog_obj is not None and bool(getattr(dog_obj, "in_company", False)):
            player.add_party_member("dog")
        dog_state = getattr(dog_obj, "__dict__", {})
        if hasattr(dog_state, "pop"):
            dog_state.pop("in_company", None)

    def updateSave_V47():
        # Appearance age is stored only as elapsed days. Older saves also kept
        # inverse countdowns and a haircut-day marker for the same facts.
        appearance = player.appearance
        state = getattr(appearance, "__dict__", {})
        if not hasattr(state, "get") or not hasattr(state, "pop"):
            return

        wash_elapsed = max(0, player_to_int(state.get("days_since_wash", 0), 0))
        if "washDays" in state:
            wash_elapsed = max(wash_elapsed, appearance.WASH_FRESH_DAYS - player_to_int(state.get("washDays"), appearance.WASH_FRESH_DAYS))
        appearance.days_since_wash = wash_elapsed

        haircut_elapsed = max(0, player_to_int(state.get("days_since_haircut", 0), 0))
        if "hairCutdays" in state:
            haircut_elapsed = max(haircut_elapsed, appearance.HAIRCUT_FRESH_DAYS - player_to_int(state.get("hairCutdays"), appearance.HAIRCUT_FRESH_DAYS))
        if "haircut_day" in state:
            haircut_elapsed = max(haircut_elapsed, current_game_day() - player_to_int(state.get("haircut_day"), current_game_day()))
        appearance.days_since_haircut = haircut_elapsed

        for retired_name in ("washDays", "hairCutdays", "haircut_day"):
            state.pop(retired_name, None)

    def updateSave_V48():
        melissa_var = getattr(Melissa, "var", None)
        if not isinstance(melissa_var, dict):
            return
        for retired_name in (
            "bat_recipe_unlocked", "private_context_place", "private_place_heat", "sex_times_today",
            "room_pests_last_help_day", "bats_completion_day",
        ):
            melissa_var.pop(retired_name, None)

    def updateSave_V49():
        # Common harassment instructions are NPC properties, not entries in
        # each character's untyped story map.
        for person_info in people.values():
            if person_info is None:
                continue
            if not hasattr(person_info, "harass_instruction_state"):
                person_info.harass_instruction_state = ""
            person_var = getattr(person_info, "var", None)
            if hasattr(person_var, "pop") and "harass_instruction" in person_var:
                person_info.harass_instruction_state = str(person_var.pop("harass_instruction", "") or "")

        # Sandra owns personal knowledge and her purchased revealing dress.
        # The dress conversation itself is an event thread; progress/endings
        # belong to TractirProgressRuntimeState.
        sandra_var = getattr(Sandra, "var", None)
        if not hasattr(Sandra, "knows_molodost"):
            Sandra.knows_molodost = False
        if not hasattr(Sandra, "revealing_dress_code"):
            Sandra.revealing_dress_code = ""
        if not hasattr(tractir_progress, "maid_revenge_ready"):
            tractir_progress.maid_revenge_ready = False
        if not hasattr(tractir_progress, "maid_revenge_reason"):
            tractir_progress.maid_revenge_reason = ""
        if not hasattr(tractir_progress, "sandra_secured_future_day"):
            tractir_progress.sandra_secured_future_day = -1

        legacy_dress_initiative_seen = False
        if hasattr(sandra_var, "pop"):
            Sandra.knows_molodost = bool(people_to_int(sandra_var.pop("knowmolodost", Sandra.knows_molodost), 0))
            legacy_dress_code = str(sandra_var.pop("revealing_dress_code", Sandra.revealing_dress_code) or "")
            if legacy_dress_code:
                Sandra.revealing_dress_code = legacy_dress_code
            sandra_var.pop("revealing_dress_ordered", None)
            legacy_dress_initiative_seen = bool(people_to_int(sandra_var.pop("revealing_dress_initiative_seen", 0), 0))

            legacy_secured_future = bool(people_to_int(sandra_var.pop("SecuredFuture", 0), 0))
            legacy_secured_day = people_to_int(sandra_var.pop("SecuredFutureDay", -1), -1)
            if legacy_secured_future:
                tractir_progress.sandra_secured_future_day = max(0, legacy_secured_day)

            legacy_maid_revenge = bool(people_to_int(sandra_var.pop("MaidRevengeEnding", 0), 0))
            legacy_maid_reason = str(sandra_var.pop("MaidRevengeReason", "") or "")
            if legacy_maid_revenge:
                tractir_progress.maid_revenge_ready = True
                tractir_progress.maid_revenge_reason = legacy_maid_reason

            # These counters were write-only and never affected a condition,
            # description, reward, or event.
            sandra_var.pop("kitchen_regular_breakfast_requests", None)
            sandra_var.pop("kitchen_client_manners_requests", None)

        melissa_var = getattr(Melissa, "var", None)
        if not hasattr(Melissa, "revealing_dress_code"):
            Melissa.revealing_dress_code = ""
        legacy_melissa_dress_request_seen = False
        if hasattr(melissa_var, "pop"):
            legacy_melissa_dress_code = str(melissa_var.pop("revealing_dress_code", Melissa.revealing_dress_code) or "")
            if legacy_melissa_dress_code:
                Melissa.revealing_dress_code = legacy_melissa_dress_code
            melissa_var.pop("revealing_dress_ordered", None)
            legacy_melissa_dress_request_seen = bool(people_to_int(melissa_var.pop("revealing_dress_request_seen", 0), 0))

        amanda_var = getattr(Amanda, "var", None)
        if not hasattr(Amanda, "revealing_dress_code"):
            Amanda.revealing_dress_code = ""
        legacy_amanda_dress_request_seen = False
        if hasattr(amanda_var, "pop"):
            legacy_amanda_dress_code = str(amanda_var.pop("revealing_dress_code", Amanda.revealing_dress_code) or "")
            if legacy_amanda_dress_code:
                Amanda.revealing_dress_code = legacy_amanda_dress_code
            amanda_var.pop("revealing_dress_ordered", None)
            legacy_amanda_dress_request_seen = bool(people_to_int(amanda_var.pop("revealing_dress_request_seen", 0), 0))

        initThreads()
        sandra_dress_thread = threads.get("sandraRevealingDressInitiative", None)
        if legacy_dress_initiative_seen and sandra_dress_thread is not None:
            sandra_dress_thread.advanceTo(sandra_dress_thread.data.length, complete_at_end=True)
        melissa_dress_thread = threads.get("melissaRevealingDressRequest", None)
        if legacy_melissa_dress_request_seen and melissa_dress_thread is not None:
            melissa_dress_thread.advanceTo(melissa_dress_thread.data.length, complete_at_end=True)
        amanda_dress_thread = threads.get("amandaRevealingDressRequest", None)
        if legacy_amanda_dress_request_seen and amanda_dress_thread is not None:
            amanda_dress_thread.advanceTo(amanda_dress_thread.data.length, complete_at_end=True)

    def updateSave_V50():
        # Melissa's authored state now has explicit NPC properties. The bat
        # thread remains the only progression-stage owner; this migration only
        # consumes the former untyped map once.
        melissa_var = getattr(Melissa, "var", None)
        if not isinstance(melissa_var, dict):
            melissa_var = {}

        Melissa.mom_dress_complaint_count = max(0, people_to_int(
            melissa_var.pop("MomDressComplaint", getattr(Melissa, "mom_dress_complaint_count", 0)), 0
        ))
        Melissa.asked_about_clara_day = people_to_int(
            melissa_var.pop("AskedAboutClaraDay", getattr(Melissa, "asked_about_clara_day", -1)), -1
        )
        melissa_var.pop("StartDay", None)
        melissa_var.pop("StartCount", None)
        melissa_var.pop("StartTotal", None)
        Melissa.private_context_day = people_to_int(
            melissa_var.pop("private_context_day", getattr(Melissa, "private_context_day", -1)), -1
        )
        Melissa.private_context_origin = str(
            melissa_var.pop("private_context_origin", getattr(Melissa, "private_context_origin", "")) or ""
        )
        Melissa.storage_thanks_day = people_to_int(
            melissa_var.pop("StorageThanksDay", getattr(Melissa, "storage_thanks_day", -1)), -1
        )
        Melissa.temp_room_code = str(
            melissa_var.pop("temp_room", getattr(Melissa, "temp_room_code", "")) or ""
        )

        legacy_rat_cleared = bool(people_to_int(melissa_var.pop("storage_rat_cleared", 0), 0))
        Melissa.storage_rat_help_day = people_to_int(
            melissa_var.pop("storage_rat_last_help_day", getattr(Melissa, "storage_rat_help_day", -1)), -1
        )
        if legacy_rat_cleared and Melissa.storage_rat_help_day < 0:
            Melissa.storage_rat_help_day = 0

        Melissa.bat_attic_check_day = people_to_int(
            melissa_var.pop("bat_attic_check_day", getattr(Melissa, "bat_attic_check_day", -1)), -1
        )
        Melissa.drawings_ready_day = people_to_int(
            melissa_var.pop("drawings_ready_day", getattr(Melissa, "drawings_ready_day", -1)), -1
        )
        Melissa.drawings_found = bool(people_to_int(
            melissa_var.pop("drawings_found", getattr(Melissa, "drawings_found", False)), 0
        ))
        Melissa.drawings_booklet_left = bool(people_to_int(
            melissa_var.pop("drawings_booklet_left", getattr(Melissa, "drawings_booklet_left", False)), 0
        ))
        Melissa.drawings_booklet_read = bool(people_to_int(
            melissa_var.pop("drawings_booklet_read", getattr(Melissa, "drawings_booklet_read", False)), 0
        ))
        Melissa.drawings_returned = bool(people_to_int(
            melissa_var.pop("drawings_returned", getattr(Melissa, "drawings_returned", False)), 0
        ))

        legacy_roof_order_day = people_to_int(melissa_var.pop("roof_repair_order_day", -1), -1)
        Melissa.roof_repair_complete_day = people_to_int(
            melissa_var.pop("roof_repair_complete_day", getattr(Melissa, "roof_repair_complete_day", -1)), -1
        )
        if Melissa.roof_repair_complete_day < 0 and legacy_roof_order_day >= 0:
            Melissa.roof_repair_complete_day = legacy_roof_order_day + 2

        Melissa.breakfast_tease_day = people_to_int(
            melissa_var.pop("breakfast_tease_day", getattr(Melissa, "breakfast_tease_day", -1)), -1
        )

        for retired_name in (
            "work_attitude", "ratKilled", "AskedMCToSolveRoomProblem",
            "bats_completed", "room_returned", "sex_engine_unlocked",
            "drawings_booklet_taken", "drawings_booklet_opened",
            "drawings_spy_option_unlocked",
        ):
            melissa_var.pop(retired_name, None)

    def updateSave_V51():
        # Clara owns her personal story facts. Recipe availability belongs to
        # crafting, while the earned Sergio discount belongs to game progress.
        clara_var = getattr(Clara, "var", None)
        if not isinstance(clara_var, dict):
            clara_var = {}

        Clara.flirt_count = max(0, people_to_int(
            clara_var.pop("flirt", getattr(Clara, "flirt_count", 0)), 0
        ))
        Clara.drawings_secret_known = bool(people_to_int(
            clara_var.pop("drawings_secret_known", getattr(Clara, "drawings_secret_known", False)), 0
        ))
        Clara.market_intro_seen = bool(people_to_int(
            clara_var.pop("market_intro_seen", getattr(Clara, "market_intro_seen", False)), 0
        ))
        Clara.market_follow_failed_day = people_to_int(
            clara_var.pop("market_follow_failed_day", getattr(Clara, "market_follow_failed_day", -1)), -1
        )
        Clara.market_follow_failed_hour = people_to_int(
            clara_var.pop("market_follow_failed_hour", getattr(Clara, "market_follow_failed_hour", -1)), -1
        )
        Clara.market_day_roll_day = people_to_int(
            clara_var.pop("market_day_roll_day", getattr(Clara, "market_day_roll_day", -1)), -1
        )
        Clara.market_day_roll = bool(people_to_int(
            clara_var.pop("market_day_roll", getattr(Clara, "market_day_roll", False)), 0
        ))
        Clara.market_evening_roll_day = people_to_int(
            clara_var.pop("market_evening_roll_day", getattr(Clara, "market_evening_roll_day", -1)), -1
        )
        Clara.market_evening_roll = bool(people_to_int(
            clara_var.pop("market_evening_roll", getattr(Clara, "market_evening_roll", False)), 0
        ))

        legacy_override = clara_var.pop("day_location_override", {})
        if hasattr(legacy_override, "get"):
            Clara.day_location_override_day = people_to_int(
                legacy_override.get("day", getattr(Clara, "day_location_override_day", -1)), -1
            )
            Clara.day_location_override_code = str(
                legacy_override.get("location", getattr(Clara, "day_location_override_code", "")) or ""
            )
        else:
            Clara.day_location_override_day = people_to_int(getattr(Clara, "day_location_override_day", -1), -1)
            Clara.day_location_override_code = str(getattr(Clara, "day_location_override_code", "") or "")

        Clara.merchant_contact_unlocked = bool(people_to_int(
            clara_var.pop("merchant_contact_unlocked", getattr(Clara, "merchant_contact_unlocked", False)), 0
        ))
        Clara.merchant_contact_month_key = people_to_int(
            clara_var.pop("merchant_contact_month_key", getattr(Clara, "merchant_contact_month_key", -1)), -1
        )
        Clara.old_water_pump_hint_seen = bool(people_to_int(
            clara_var.pop("old_water_pump_hint_seen", getattr(Clara, "old_water_pump_hint_seen", False)), 0
        ))
        Clara.commission_followup_day = people_to_int(
            clara_var.pop("commission_followup_day", getattr(Clara, "commission_followup_day", 999999)), 999999
        )
        Clara.murder_day = people_to_int(
            clara_var.pop("murder_day", getattr(Clara, "murder_day", 999999)), 999999
        )

        if not hasattr(crafting, "special_cream_recipe_unlocked"):
            crafting.special_cream_recipe_unlocked = False
        legacy_special_cream = bool(people_to_int(clara_var.pop("special_cream_recipe_unlocked", 0), 0))
        crafting.special_cream_recipe_unlocked = bool(crafting.special_cream_recipe_unlocked or legacy_special_cream)

        if not hasattr(tractir_progress, "sergio_discount_percent"):
            tractir_progress.sergio_discount_percent = 0
        legacy_sergio_discount = people_to_int(clara_var.pop("sergio_discount", 0), 0)
        tractir_progress.sergio_discount_percent = max(
            people_to_int(tractir_progress.sergio_discount_percent, 0),
            max(0, min(90, legacy_sergio_discount)),
        )

        for retired_name in (
            "booklet_market_seen", "market_evening_intro_seen", "mongol_theft_seen", "escape_confessed",
            "tavern_visit_bar_0_seen", "tavern_visit_bar_1_seen", "tavern_visit_bar_2_seen",
            "melissa_room_visit_0_seen", "melissa_room_visit_1_seen", "melissa_room_visit_2_seen",
            "melissa_room_visit_count", "knownotvirgin", "paintings_melissa_asked", "cellar_seen",
            "cellar_spanking_discovered", "cellar_confronted", "comfort_pending", "comfort_done",
            "second_ask_unlocked", "source_known", "sex_engine_unlocked", "necking_unlocked",
            "petting_unlocked", "fiance_church_seen", "fiance_seen_day", "fiance_barber_seen",
            "fiance_barber_night_roll_day", "fiance_barber_night_roll", "fiance_barber_secret_seen",
            "commission_started", "commission_followup_done", "peek_done", "confession_done",
            "drawings_betrayal_confessed", "murder_seen", "murder_solved", "anal_unlocked",
            "virginity_choice_unlocked",
        ):
            clara_var.pop(retired_name, None)

    def updateSave_V52():
        # Becky owns her personal/home/church/Sherwood facts directly. Her
        # husband, Inga/Lucas, and Eddie-backstory counters remain owned by
        # their existing event threads; consume the former map only once.
        becky_var = getattr(Becky, "var", None)
        if not hasattr(becky_var, "pop"):
            becky_var = {}

        Becky.left_dances = max(0, people_to_int(
            becky_var.pop("leftdances", getattr(Becky, "left_dances", 0)), 0
        ))
        Becky.home_visit_stage = max(0, people_to_int(
            becky_var.pop("visitedhome", getattr(Becky, "home_visit_stage", 0)), 0
        ))
        Becky.inga_sex_greeting_seen = bool(people_to_int(
            becky_var.pop("IngaSexGreet", getattr(Becky, "inga_sex_greeting_seen", False)), 0
        ))
        Becky.uninvited_visit_scolded = bool(people_to_int(
            becky_var.pop("VisitScolded", getattr(Becky, "uninvited_visit_scolded", False)), 0
        ))
        Becky.home_front_checked_today = bool(people_to_int(
            becky_var.pop("TodayFrontSexCheck", getattr(Becky, "home_front_checked_today", False)), 0
        ))
        Becky.home_sex_unlocked = bool(people_to_int(
            becky_var.pop("HomeSex", getattr(Becky, "home_sex_unlocked", False)), 0
        ))
        Becky.eddie_georgett_stage = max(0, people_to_int(
            becky_var.pop("EddieGeorg", getattr(Becky, "eddie_georgett_stage", 0)), 0
        ))
        Becky.eddie_home_visit_state = max(0, people_to_int(
            becky_var.pop("EddieWhoreHome", getattr(Becky, "eddie_home_visit_state", 0)), 0
        ))
        Becky.open_oral_stage = max(0, people_to_int(
            becky_var.pop("BeckyOpenMinet", getattr(Becky, "open_oral_stage", 0)), 0
        ))
        Becky.home_visit_count = max(0, people_to_int(
            becky_var.pop("TimesVisited", getattr(Becky, "home_visit_count", 0)), 0
        ))
        Becky.talked_about_eddie = bool(people_to_int(
            becky_var.pop("TalkAboutEddie", getattr(Becky, "talked_about_eddie", False)), 0
        ))
        Becky.georgett_mentioned = bool(people_to_int(
            becky_var.pop("GeorgMention", getattr(Becky, "georgett_mentioned", False)), 0
        ))
        Becky.eddie_intervention_reaction = max(0, people_to_int(
            becky_var.pop("EddieIntrReact", getattr(Becky, "eddie_intervention_reaction", 0)), 0
        ))
        Becky.priest_advice_stage = max(0, people_to_int(
            becky_var.pop("PriestAdvice", getattr(Becky, "priest_advice_stage", 0)), 0
        ))
        Becky.gerhard_talk_stage = max(0, people_to_int(
            becky_var.pop("GerhardBeckyTalk", getattr(Becky, "gerhard_talk_stage", 0)), 0
        ))
        Becky.asked_about_eddie_sex_stage = max(0, people_to_int(
            becky_var.pop("AskedEddieFuck", getattr(Becky, "asked_about_eddie_sex_stage", 0)), 0
        ))
        Becky.eddie_join_stage = max(0, people_to_int(
            becky_var.pop("EddieTryToFuck", getattr(Becky, "eddie_join_stage", 0)), 0
        ))
        Becky.eddie_join_failures = max(0, people_to_int(
            becky_var.pop("EddieFailures", getattr(Becky, "eddie_join_failures", 0)), 0
        ))
        Becky.eddie_robbed_day = max(0, people_to_int(
            becky_var.pop("EddieRobbedDay", getattr(Becky, "eddie_robbed_day", 0)), 0
        ))
        legacy_knows_sherwood = people_to_int(becky_var.pop("KnowSherwood", 0), 0)
        Becky.knows_blackwood = bool(max(
            people_to_int(becky_var.pop("KnowBlackwood", getattr(Becky, "knows_blackwood", False)), 0),
            legacy_knows_sherwood,
        ))
        Becky.sherwood_suspicion = max(0, people_to_int(
            becky_var.pop("SherwoodSuspect", getattr(Becky, "sherwood_suspicion", 0)), 0
        ))
        Becky.trade_offer_stage = max(0, people_to_int(
            becky_var.pop("TradeOffer", getattr(Becky, "trade_offer_stage", 0)), 0
        ))
        Becky.sherwood_warning_stage = max(0, people_to_int(
            becky_var.pop("SherwoodWarn", getattr(Becky, "sherwood_warning_stage", 0)), 0
        ))
        Becky.asked_about_elf_trade = bool(people_to_int(
            becky_var.pop("AskTradeElf", getattr(Becky, "asked_about_elf_trade", False)), 0
        ))
        Becky.fingal_connection_clarified = bool(people_to_int(
            becky_var.pop("FingalClarify", getattr(Becky, "fingal_connection_clarified", False)), 0
        ))
        Becky.admitted_sherwood_stage = max(0, people_to_int(
            becky_var.pop("AdmitSherwood", getattr(Becky, "admitted_sherwood_stage", 0)), 0
        ))
        Becky.robin_robbery_stage = max(0, people_to_int(
            becky_var.pop("RobbedByRobin", getattr(Becky, "robin_robbery_stage", 0)), 0
        ))
        Becky.robbery_consolation_count = max(0, people_to_int(
            becky_var.pop("ConsoleRobbery", getattr(Becky, "robbery_consolation_count", 0)), 0
        ))
        Becky.sandra_kitchen_visit_period = max(0, people_to_int(
            becky_var.pop("SandraKitchenVisitMonth", getattr(Becky, "sandra_kitchen_visit_period", 0)), 0
        ))
        Becky.last_store_orgasm_day = people_to_int(
            becky_var.pop("last_store_orgasm_day", getattr(Becky, "last_store_orgasm_day", -1)), -1
        )

        for retired_name in (
            "husbandtalk", "SawIngaFuck", "HomeFrontCheckedDay", "danceinvitehome", "eddietalk",
            "EddieRobbed", "SherwoodQuestScheduled", "TradeOfferText", "HomeEnterCheckedDay",
            "after_sermon_stage", "priest_incest_agree", "BarDrinkDay",
        ):
            becky_var.pop(retired_name, None)
        globals().pop("BeckyAdmit", None)

    def updateSave_V53():
        # Inga owns the two mutable facts from her Becky-home/Lucas story.
        # Consume the former untyped map once; the Becky discovery sequence
        # itself remains owned by its existing event thread.
        inga_var = getattr(Inga, "var", None)
        if not hasattr(inga_var, "pop"):
            inga_var = {}

        Inga.saw_lucas_sex = bool(people_to_int(
            inga_var.pop("SawLucassex", getattr(Inga, "saw_lucas_sex", False)), 0
        ))
        Inga.acquaintance_stage = max(0, people_to_int(
            inga_var.pop("Knowher", getattr(Inga, "acquaintance_stage", 0)), 0
        ))
        globals().pop("IngaVar", None)

    def updateSave_V54():
        # Zimmer's complaint and investigation facts are direct NPC state.
        # Consume the former untyped map once without retaining an alias.
        zimmer_var = getattr(Zimmer, "var", None)
        if not hasattr(zimmer_var, "pop"):
            zimmer_var = {}

        Zimmer.horse_complaint_stage = max(0, people_to_int(
            zimmer_var.pop("ComplainHorse", getattr(Zimmer, "horse_complaint_stage", 0)), 0
        ))
        Zimmer.sherwood_story_stage = max(0, people_to_int(
            zimmer_var.pop("SherwoodStory", getattr(Zimmer, "sherwood_story_stage", 0)), 0
        ))
        Zimmer.robin_complaint_stage = max(0, people_to_int(
            zimmer_var.pop("ComplainRobin", getattr(Zimmer, "robin_complaint_stage", 0)), 0
        ))
        Zimmer.robin_investigation_day = max(0, people_to_int(
            zimmer_var.pop("RobinInvestigationDay", getattr(Zimmer, "robin_investigation_day", 0)), 0
        ))
        Zimmer.street_patrol_pass = bool(people_to_int(
            zimmer_var.pop("street_pass", getattr(Zimmer, "street_patrol_pass", False)), 0
        ))
        globals().pop("ZimmerVar", None)

    def updateSave_V55():
        # Liza owns her church, work, client, and talk-history facts directly.
        # Consume the former untyped map once without retaining a live alias.
        liza_var = getattr(Liza, "var", None)
        if not hasattr(liza_var, "pop"):
            liza_var = {}

        Liza.witnessed_church_after_sermon = bool(max(
            people_to_int(liza_var.pop("SawChurchAfterCermon", 0), 0),
            people_to_int(getattr(Liza, "witnessed_church_after_sermon", False), 0),
        ))
        Liza.discussed_georgett_gerhard = bool(max(
            people_to_int(liza_var.pop("TalkChurchAfterCermonGeorgett", 0), 0),
            people_to_int(getattr(Liza, "discussed_georgett_gerhard", False), 0),
        ))
        Liza.prostitution_started = bool(max(
            people_to_int(liza_var.pop("ProstStart", 0), 0),
            people_to_int(getattr(Liza, "prostitution_started", False), 0),
        ))
        Liza.has_seen_clients = bool(max(
            people_to_int(liza_var.pop("seeclients", 0), 0),
            people_to_int(getattr(Liza, "has_seen_clients", False), 0),
        ))
        Liza.asked_about_clients = bool(max(
            people_to_int(liza_var.pop("askclients", 0), 0),
            people_to_int(getattr(Liza, "asked_about_clients", False), 0),
        ))
        Liza.asked_about_pregnancy = bool(max(
            people_to_int(liza_var.pop("askpregnancy", 0), 0),
            people_to_int(getattr(Liza, "asked_about_pregnancy", False), 0),
        ))
        Liza.asked_about_sex = bool(max(
            people_to_int(liza_var.pop("asksex", 0), 0),
            people_to_int(getattr(Liza, "asked_about_sex", False), 0),
        ))
        Liza.glory_hole_mentioned = bool(max(
            people_to_int(liza_var.pop("GloryHoleMentioned", 0), 0),
            people_to_int(getattr(Liza, "glory_hole_mentioned", False), 0),
        ))
        Liza.glory_hole_asked = bool(max(
            people_to_int(liza_var.pop("GloryHoleAsked", 0), 0),
            people_to_int(getattr(Liza, "glory_hole_asked", False), 0),
        ))
        Liza.portstreet_clients_seen_today = bool(max(
            people_to_int(liza_var.pop("portstreet_clients_seen_today", 0), 0),
            people_to_int(getattr(Liza, "portstreet_clients_seen_today", False), 0),
        ))

        # Initialized by the QSP source but never read or written by any scene.
        liza_var.pop("TalkChurchAfterCermon", None)
        globals().pop("LizaVar", None)

    def updateSave_V56():
        # Alber owns lasting personal/story facts directly. The old
        # LegareProvokeYou value was only temporary conversation flow.
        alber_var = getattr(Alber, "var", None)
        if not hasattr(alber_var, "pop"):
            alber_var = {}

        Alber.liza_encounter_seen = bool(max(
            people_to_int(alber_var.pop("sawwithliza", 0), 0),
            people_to_int(getattr(Alber, "liza_encounter_seen", False), 0),
        ))
        Alber.talked_about_liza = bool(max(
            people_to_int(alber_var.pop("talkedaboutliza", 0), 0),
            people_to_int(getattr(Alber, "talked_about_liza", False), 0),
        ))
        Alber.heard_about_wife = bool(max(
            people_to_int(alber_var.pop("hearabouthiswife", 0), 0),
            people_to_int(getattr(Alber, "heard_about_wife", False), 0),
        ))
        Alber.amanda_conflict_stage = max(0, people_to_int(
            alber_var.pop("FightYouAmanda", getattr(Alber, "amanda_conflict_stage", 0)), 0
        ))

        alber_var.pop("WhoreVisitFreq", None)
        alber_var.pop("LegareProvokeYou", None)
        globals().pop("LegareProvokeYou", None)
        globals().pop("AlberVar", None)

    def updateSave_V57():
        # Francheska owns her conversation history and Sunday-story cooldown.
        # The former FranBusy map is obsolete because her schedule owns duty.
        fran_var = getattr(Francheska, "var", None)
        if not hasattr(fran_var, "pop"):
            fran_var = {}

        Francheska.met = bool(max(
            people_to_int(fran_var.pop("meet", 0), 0),
            people_to_int(getattr(Francheska, "met", False), 0),
        ))
        Francheska.asked_about_ellona = bool(max(
            people_to_int(fran_var.pop("ellonaask", 0), 0),
            people_to_int(getattr(Francheska, "asked_about_ellona", False), 0),
        ))
        Francheska.graces_stage = max(
            people_to_int(fran_var.pop("graceask", 0), 0),
            people_to_int(getattr(Francheska, "graces_stage", 0), 0),
        )
        Francheska.asked_about_duchess = bool(max(
            people_to_int(fran_var.pop("conchitaask", 0), 0),
            people_to_int(getattr(Francheska, "asked_about_duchess", False), 0),
        ))
        Francheska.asked_about_duke = bool(max(
            people_to_int(fran_var.pop("dukeask", 0), 0),
            people_to_int(getattr(Francheska, "asked_about_duke", False), 0),
        ))
        Francheska.asked_about_stark = bool(max(
            people_to_int(fran_var.pop("starkask", 0), 0),
            people_to_int(getattr(Francheska, "asked_about_stark", False), 0),
        ))
        Francheska.asked_about_duchy = bool(max(
            people_to_int(fran_var.pop("stateask", 0), 0),
            people_to_int(getattr(Francheska, "asked_about_duchy", False), 0),
        ))
        Francheska.asked_about_king = bool(max(
            people_to_int(fran_var.pop("kingask", 0), 0),
            people_to_int(getattr(Francheska, "asked_about_king", False), 0),
        ))
        Francheska.asked_about_kingdom_relations = bool(max(
            people_to_int(fran_var.pop("rebelask", 0), 0),
            people_to_int(getattr(Francheska, "asked_about_kingdom_relations", False), 0),
        ))
        Francheska.asked_about_aliens = bool(max(
            people_to_int(fran_var.pop("alienask", 0), 0),
            people_to_int(getattr(Francheska, "asked_about_aliens", False), 0),
        ))
        Francheska.sunday_stories_seen_day = max(
            people_to_int(fran_var.pop("sunday_stories_seen_day", -1), -1),
            people_to_int(getattr(Francheska, "sunday_stories_seen_day", -1), -1),
        )

        globals().pop("FranVar", None)
        globals().pop("FranBusy", None)

    def updateSave_V58():
        # Robin owns his conversation, robbery, negotiation, and road progress.
        # Consume the former untyped map once without retaining a live alias.
        robin_var = getattr(Robin, "var", None)
        if not hasattr(robin_var, "pop"):
            robin_var = {}

        Robin.identity_known = bool(max(
            people_to_int(robin_var.pop("KnowHim", 0), 0),
            people_to_int(getattr(Robin, "identity_known", False), 0),
        ))
        Robin.complaint_explained = bool(max(
            people_to_int(robin_var.pop("KnowComplaint", 0), 0),
            people_to_int(getattr(Robin, "complaint_explained", False), 0),
        ))
        Robin.place_explained = bool(max(
            people_to_int(robin_var.pop("KnowPlace", 0), 0),
            people_to_int(getattr(Robin, "place_explained", False), 0),
        ))
        Robin.weapon_source_explained = bool(max(
            people_to_int(robin_var.pop("KnowWeapon", 0), 0),
            people_to_int(getattr(Robin, "weapon_source_explained", False), 0),
        ))
        Robin.robbery_count = max(
            people_to_int(robin_var.pop("RobbedNum", 0), 0),
            people_to_int(getattr(Robin, "robbery_count", 0), 0),
        )
        Robin.negotiation_stage = max(
            people_to_int(robin_var.pop("Negotiate", 0), 0),
            people_to_int(getattr(Robin, "negotiation_stage", 0), 0),
        )
        Robin.knows_big_tits_village = bool(max(
            people_to_int(robin_var.pop("KnowBigTitsVillage", 0), 0),
            people_to_int(getattr(Robin, "knows_big_tits_village", False), 0),
        ))
        Robin.mongol_safe_pass = bool(max(
            people_to_int(robin_var.pop("MongolSafePass", 0), 0),
            people_to_int(getattr(Robin, "mongol_safe_pass", False), 0),
        ))
        Robin.kunidell_opened = bool(max(
            people_to_int(robin_var.pop("KunidellOpened", 0), 0),
            people_to_int(getattr(Robin, "kunidell_opened", False), 0),
        ))
        Robin.kunidell_deliveries = max(
            people_to_int(robin_var.pop("KunidellDeliveries", 0), 0),
            people_to_int(getattr(Robin, "kunidell_deliveries", 0), 0),
        )
        Robin.blackwood_road_open = bool(max(
            people_to_int(robin_var.pop("BlackwoodRoadOpen", 0), 0),
            people_to_int(getattr(Robin, "blackwood_road_open", False), 0),
        ))

        globals().pop("RobinVar", None)

    def updateSave_V59():
        # Draupnir owns quote history and the Mongol lockpick order directly.
        # Consume the former untyped map once without retaining a live alias.
        draupnir_var = getattr(Draupnir, "var", None)
        if not hasattr(draupnir_var, "pop"):
            draupnir_var = {}

        Draupnir.slogan_quote_received = bool(max(
            people_to_int(draupnir_var.pop("SloganAsked", 0), 0),
            people_to_int(getattr(Draupnir, "slogan_quote_received", False), 0),
        ))
        Draupnir.peep_hole_quote_received = bool(max(
            people_to_int(draupnir_var.pop("HoleAsked", 0), 0),
            people_to_int(getattr(Draupnir, "peep_hole_quote_received", False), 0),
        ))
        Draupnir.glory_hole_quote_received = bool(max(
            people_to_int(draupnir_var.pop("GloryHoleAsked", 0), 0),
            people_to_int(getattr(Draupnir, "glory_hole_quote_received", False), 0),
        ))
        Draupnir.soap_barrel_quote_received = bool(max(
            people_to_int(draupnir_var.pop("SoapBarrelAsked", 0), 0),
            people_to_int(getattr(Draupnir, "soap_barrel_quote_received", False), 0),
        ))
        Draupnir.dog_booth_quote_received = bool(max(
            people_to_int(draupnir_var.pop("DogBoothAsked", 0), 0),
            people_to_int(getattr(Draupnir, "dog_booth_quote_received", False), 0),
        ))
        Draupnir.mongol_lockpick_order_day = max(
            people_to_int(draupnir_var.pop("MongolLockpickOrderDay", -1), -1),
            people_to_int(getattr(Draupnir, "mongol_lockpick_order_day", -1), -1),
        )

        globals().pop("DraupnirVar", None)

    def updateSave_V60():
        # Eddie owns personal conversation and witnessed-scene facts directly.
        # The visit frequency is immutable QSP configuration, not save state.
        eddie_var = getattr(Eddie, "var", None)
        if not hasattr(eddie_var, "pop"):
            eddie_var = {}

        Eddie.told_about_tavern_whores = bool(max(
            people_to_int(eddie_var.pop("TalkedAboutWhores", 0), 0),
            people_to_int(getattr(Eddie, "told_about_tavern_whores", False), 0),
        ))
        Eddie.seen_with_georgett = bool(max(
            people_to_int(eddie_var.pop("SawWithGeorgett", 0), 0),
            people_to_int(getattr(Eddie, "seen_with_georgett", False), 0),
        ))
        Eddie.talked_about_georgett = bool(max(
            people_to_int(eddie_var.pop("TalkedAboutGeorgett", 0), 0),
            people_to_int(getattr(Eddie, "talked_about_georgett", False), 0),
        ))
        Eddie.saw_mother_sex = bool(max(
            people_to_int(eddie_var.pop("SawMomSex", 0), 0),
            people_to_int(getattr(Eddie, "saw_mother_sex", False), 0),
        ))
        Eddie.fingal_talk_stage = max(
            people_to_int(eddie_var.pop("FingalTalk", 0), 0),
            people_to_int(getattr(Eddie, "fingal_talk_stage", 0), 0),
        )
        Eddie.asked_fingal_destination = bool(max(
            people_to_int(eddie_var.pop("FingalTalkDestination", 0), 0),
            people_to_int(getattr(Eddie, "asked_fingal_destination", False), 0),
        ))
        Eddie.asked_fingal_guard_complaint = bool(max(
            people_to_int(eddie_var.pop("FingalTalkComplain", 0), 0),
            people_to_int(getattr(Eddie, "asked_fingal_guard_complaint", False), 0),
        ))
        Eddie.ridiculed_follow_attempt = bool(max(
            people_to_int(eddie_var.pop("RidiculeFollow", 0), 0),
            people_to_int(getattr(Eddie, "ridiculed_follow_attempt", False), 0),
        ))
        Eddie.others_saw_with_mother = bool(max(
            people_to_int(eddie_var.pop("OthersSawWithMom", 0), 0),
            people_to_int(getattr(Eddie, "others_saw_with_mother", False), 0),
        ))

        eddie_var.pop("WhoreVisitFreq", None)
        globals().pop("EddieVar", None)

    def updateSave_V61():
        # Mongol owns horse-trade, theft, and personal encounter facts directly.
        # The Clara booklet thread remains the sole owner of seen/released stages.
        mongol_var = getattr(Mongol, "var", None)
        if not hasattr(mongol_var, "pop"):
            mongol_var = {}

        Mongol.will_try_to_steal = bool(max(
            people_to_int(mongol_var.pop("WillTryToSteal", 0), 0),
            people_to_int(getattr(Mongol, "will_try_to_steal", False), 0),
        ))
        Mongol.stocks_food_day = max(
            people_to_int(mongol_var.pop("StocksFoodDay", -1), -1),
            people_to_int(getattr(Mongol, "stocks_food_day", -1), -1),
        )
        Mongol.stocks_arrest_day = max(
            people_to_int(mongol_var.pop("StocksArrestDay", -1), -1),
            people_to_int(getattr(Mongol, "stocks_arrest_day", -1), -1),
        )
        Mongol.guard_captain_known = bool(max(
            people_to_int(mongol_var.pop("GuardCaptainKnown", 0), 0),
            people_to_int(getattr(Mongol, "guard_captain_known", False), 0),
        ))
        Mongol.market_roll_day = max(
            people_to_int(mongol_var.pop("MarketRollDay", -1), -1),
            people_to_int(getattr(Mongol, "market_roll_day", -1), -1),
        )
        Mongol.market_roll = bool(max(
            people_to_int(mongol_var.pop("MarketRoll", 0), 0),
            people_to_int(getattr(Mongol, "market_roll", False), 0),
        ))
        Mongol.asked_about_gypsy = bool(max(
            people_to_int(mongol_var.pop("GypsyAsk", 0), 0),
            people_to_int(getattr(Mongol, "asked_about_gypsy", False), 0),
        ))
        Mongol.asked_price_increase = bool(max(
            people_to_int(mongol_var.pop("AskPriceIncr", 0), 0),
            people_to_int(getattr(Mongol, "asked_price_increase", False), 0),
        ))
        Mongol.zimmer_knows_horse_theft = bool(max(
            people_to_int(mongol_var.pop("ZimmerKnow", 0), 0),
            people_to_int(getattr(Mongol, "zimmer_knows_horse_theft", False), 0),
        ))
        Mongol.horse_price = people_to_int(
            mongol_var.pop("HorsePrice", getattr(Mongol, "horse_price", 1000)), 1000
        )
        Mongol.discount_asked = bool(max(
            people_to_int(mongol_var.pop("DiscountAsk", 0), 0),
            people_to_int(getattr(Mongol, "discount_asked", False), 0),
        ))
        Mongol.theft_asked = bool(max(
            people_to_int(mongol_var.pop("TheftAsk", 0), 0),
            people_to_int(getattr(Mongol, "theft_asked", False), 0),
        ))
        Mongol.asked_about_seen_stolen = bool(max(
            people_to_int(mongol_var.pop("AskSawStolen", 0), 0),
            people_to_int(getattr(Mongol, "asked_about_seen_stolen", False), 0),
        ))
        Mongol.seen_with_stolen_horse = bool(max(
            people_to_int(mongol_var.pop("SawStolen", 0), 0),
            people_to_int(getattr(Mongol, "seen_with_stolen_horse", False), 0),
        ))
        Mongol.horses_bought = max(
            people_to_int(mongol_var.pop("HorsesBought", 0), 0),
            people_to_int(getattr(Mongol, "horses_bought", 0), 0),
        )

        mongol_var.pop("StocksSeen", None)
        mongol_var.pop("StocksReleased", None)
        globals().pop("MongolVar", None)

    def updateSave_V62():
        # Irma owns her disclosed personal history and the refused extra-fee fact.
        irma_var = getattr(Irma, "var", None)
        if not hasattr(irma_var, "pop"):
            irma_var = {}

        Irma.extra_fee_refused = bool(max(
            people_to_int(irma_var.pop("DeniedMinetMoney", 0), 0),
            people_to_int(getattr(Irma, "extra_fee_refused", False), 0),
        ))
        Irma.infertility_known = bool(max(
            people_to_int(irma_var.pop("KnowInfertility", 0), 0),
            people_to_int(getattr(Irma, "infertility_known", False), 0),
        ))
        Irma.father_story_known = bool(max(
            people_to_int(irma_var.pop("KnowDad", 0), 0),
            people_to_int(getattr(Irma, "father_story_known", False), 0),
        ))
        Irma.mother_story_known = bool(max(
            people_to_int(irma_var.pop("KnowMom", 0), 0),
            people_to_int(getattr(Irma, "mother_story_known", False), 0),
        ))
        Irma.sexual_history_known = bool(max(
            people_to_int(irma_var.pop("KnowSlut", 0), 0),
            people_to_int(getattr(Irma, "sexual_history_known", False), 0),
        ))

        globals().pop("IrmaVar", None)

    def updateSave_V63():
        # Amanda owns the night-bowl request, possession, and preference facts.
        amanda_var = getattr(Amanda, "var", None)
        if not hasattr(amanda_var, "pop"):
            amanda_var = {}

        Amanda.night_bowl_given = bool(max(
            people_to_int(amanda_var.pop("gave_night_bowl", 0), 0),
            people_to_int(getattr(Amanda, "night_bowl_given", False), 0),
        ))
        Amanda.night_bowl_request_day = max(
            people_to_int(amanda_var.pop("night_bowl_request_day", -1), -1),
            people_to_int(getattr(Amanda, "night_bowl_request_day", -1), -1),
        )
        Amanda.fancy_night_bowl_received = bool(max(
            people_to_int(amanda_var.pop("got_fancy_night_bowl", 0), 0),
            people_to_int(getattr(Amanda, "fancy_night_bowl_received", False), 0),
        ))
        Amanda.backyard_relief_preference = max(
            people_to_int(amanda_var.pop("prefers_backyard_relief", -1), -1),
            people_to_int(getattr(Amanda, "backyard_relief_preference", -1), -1),
        )

    def updateSave_V64():
        # Melissa's bat thread owns the attic-fall progression. Amanda owns
        # only her later breakfast response and teasing facts.
        amanda_var = getattr(Amanda, "var", None)
        if not hasattr(amanda_var, "pop"):
            amanda_var = {}

        amanda_var.pop("attic_window_busted", None)
        Amanda.attic_window_breakfast_bj_day = max(
            people_to_int(amanda_var.pop("attic_window_breakfast_bj_day", -1), -1),
            people_to_int(getattr(Amanda, "attic_window_breakfast_bj_day", -1), -1),
        )
        Amanda.attic_mock_response_day = max(
            people_to_int(amanda_var.pop("attic_mock_response_day", -1), -1),
            people_to_int(getattr(Amanda, "attic_mock_response_day", -1), -1),
        )
        Amanda.attic_mock_stopped = bool(max(
            people_to_int(amanda_var.pop("attic_mock_stopped", 0), 0),
            people_to_int(getattr(Amanda, "attic_mock_stopped", False), 0),
        ))
        Amanda.attic_mock_exposed = bool(max(
            people_to_int(amanda_var.pop("attic_mock_exposed", 0), 0),
            people_to_int(getattr(Amanda, "attic_mock_exposed", False), 0),
        ))
        Amanda.breakfast_tease_day = max(
            people_to_int(amanda_var.pop("breakfast_tease_day", -1), -1),
            people_to_int(getattr(Amanda, "breakfast_tease_day", -1), -1),
        )

    def updateSave_V65():
        # Amanda owns her work warning, daily pregnancy question, and repeated
        # dress-complaint count directly.
        amanda_var = getattr(Amanda, "var", None)
        if not hasattr(amanda_var, "pop"):
            amanda_var = {}

        Amanda.warned_about_not_working = bool(max(
            people_to_int(amanda_var.pop("warnnotwork", 0), 0),
            people_to_int(getattr(Amanda, "warned_about_not_working", False), 0),
        ))
        Amanda.pregnancy_risk_asked_today = bool(max(
            people_to_int(amanda_var.pop("askzalettoday", 0), 0),
            people_to_int(getattr(Amanda, "pregnancy_risk_asked_today", False), 0),
        ))
        Amanda.mom_dress_complaint_count = max(
            people_to_int(amanda_var.pop("MomDressComplaint", 0), 0),
            people_to_int(getattr(Amanda, "mom_dress_complaint_count", 0), 0),
        )

    def updateSave_V66():
        # Amanda directly owns the room rejection gate, escalation count, and
        # whether Sandra and Melissa have already been called to remove MC.
        amanda_var = getattr(Amanda, "var", None)
        if not hasattr(amanda_var, "pop"):
            amanda_var = {}

        Amanda.room_entry_blocked_today = bool(max(
            people_to_int(amanda_var.pop("kickyoufromroom", 0), 0),
            people_to_int(getattr(Amanda, "room_entry_blocked_today", False), 0),
        ))
        Amanda.room_rejection_count = max(
            people_to_int(amanda_var.pop("kickyoufromroomcount", 0), 0),
            people_to_int(getattr(Amanda, "room_rejection_count", 0), 0),
        )
        Amanda.room_rescue_called = bool(max(
            people_to_int(amanda_var.pop("kickedwithmomhelp", 0), 0),
            people_to_int(getattr(Amanda, "room_rescue_called", False), 0),
        ))

    def updateSave_V67():
        # Amanda owns the complete Legare relationship, Friday-dance state,
        # sexual history, and player-knowledge state directly.
        amanda_var = getattr(Amanda, "var", None)
        if not hasattr(amanda_var, "pop"):
            amanda_var = {}

        Amanda.legare_affection = max(
            people_to_int(amanda_var.pop("alberfriends", 0), 0),
            people_to_int(getattr(Amanda, "legare_affection", 0), 0),
        )
        Amanda.legare_departure_code = max(
            people_to_int(amanda_var.pop("LegareGo", 0), 0),
            people_to_int(getattr(Amanda, "legare_departure_code", 0), 0),
        )
        for old_key, field_name in (
            ("albernowdances", "dancing_with_legare"),
            ("leftdances", "left_friday_dance"),
            ("alberprohibit", "legare_forbidden"),
            ("EscapeUnnoticed", "escaped_dance_unnoticed"),
            ("sucklegare", "performed_oral_with_legare"),
            ("fucklegare", "had_sex_with_legare"),
            ("deflowerlegare", "lost_virginity_to_legare"),
            ("knowdeflowerlegare", "player_knows_legare_deflowered"),
            ("knowlegaresex", "player_knows_legare_sex"),
            ("sawlegaresex", "player_saw_legare_sex"),
            ("knowyousawlegaresex", "knows_player_saw_legare_sex"),
            ("knowyouseesex", "knows_player_is_watching_legare_sex"),
        ):
            setattr(Amanda, field_name, bool(max(
                people_to_int(amanda_var.pop(old_key, 0), 0),
                people_to_int(getattr(Amanda, field_name, False), 0),
            )))

    def updateSave_V68():
        # FightEnemyInstance now owns encounter state as direct fields rather
        # than forwarding every read and write through a duplicate data map.
        converted_party = []
        for position, old_enemy in enumerate(list(getattr(fight, "enemy_party", []) or []), 1):
            legacy_data = getattr(old_enemy, "data", None)
            if isinstance(old_enemy, FightEnemyInstance) and not hasattr(legacy_data, "get"):
                converted_party.append(old_enemy)
                continue
            if not hasattr(legacy_data, "get"):
                legacy_data = old_enemy if hasattr(old_enemy, "get") else {}

            enemy_id = str(legacy_data.get("id", getattr(fight, "enemy_id", "wolf")) or "wolf")
            converted = FightEnemyInstance(fight_enemy_template(enemy_id), legacy_data.get("index", position))
            converted.object_id = enemy_id
            converted.name = str(legacy_data.get("name", converted.name) or converted.name)
            converted.enemy_type = str(legacy_data.get("enemy_type", converted.enemy_type) or converted.enemy_type)
            converted.health = max(0, people_to_int(legacy_data.get("health", converted.health), converted.health))
            converted.health_max = max(1, people_to_int(legacy_data.get("health_max", converted.health_max), converted.health_max))
            converted.energy = max(0, people_to_int(legacy_data.get("energy", converted.energy), converted.energy))
            converted.energy_max = max(0, people_to_int(legacy_data.get("energy_max", converted.energy_max), converted.energy_max))
            converted.attack_min = people_to_int(legacy_data.get("attack_min", converted.attack_min), converted.attack_min)
            converted.attack_max = people_to_int(legacy_data.get("attack_max", converted.attack_max), converted.attack_max)
            converted.defence_min = people_to_int(legacy_data.get("defence_min", converted.defence_min), converted.defence_min)
            converted.defence_max = people_to_int(legacy_data.get("defence_max", converted.defence_max), converted.defence_max)
            converted.moves = list(legacy_data.get("moves", converted.moves) or [])
            converted.skills = list(legacy_data.get("skills", converted.skills) or [])
            converted.weapon = str(legacy_data.get("weapon", converted.weapon) or "")
            converted.tactics = str(legacy_data.get("tactics", converted.tactics) or "")
            converted.loot = dict(legacy_data.get("loot", converted.loot) or {})
            converted.money_min = max(0, people_to_int(legacy_data.get("money_min", converted.money_min), converted.money_min))
            converted.money_max = max(converted.money_min, people_to_int(legacy_data.get("money_max", converted.money_max), converted.money_max))
            converted.exploration_reward = max(0, people_to_int(legacy_data.get("exploration_reward", converted.exploration_reward), converted.exploration_reward))
            converted.status = dict(legacy_data.get("status", {}) or {})
            converted.__dict__.pop("data", None)
            converted_party.append(converted)
        fight.enemy_party = converted_party


label before_load:
    $ beforeLoadTractirSave()
    return


label after_load:
    $ updateSave()
    $ npc_schedule_after_load()
    $ renpy.block_rollback()
    return
