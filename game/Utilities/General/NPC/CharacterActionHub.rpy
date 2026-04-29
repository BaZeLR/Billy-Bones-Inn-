# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default knowsMC = {}

default action_menu_entity_type = ""
default action_menu_entity_id = ""
default action_menu_where = ""
default action_menu_title = ""
default action_menu_entity_data = {}
default action_menu_actions = []
default action_menu_specs = []
default action_menu_selected = ""

init -40 python:
    import renpy.exports as renpy

    _npc_picture_cache = {}
    NPC_META = {
        "amanda": {
            "unknown_name": "Someone",
            "talk_label": "IntAmandaTalk",
            "talk_args": (),
            "examine_label": "ShowAmandaCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "melissa": {
            "unknown_name": "Someone",
            "talk_label": "IntMelissaTalk",
            "talk_args": (),
            "examine_label": "ShowMelissaCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "sandra": {
            "unknown_name": "Someone",
            "talk_label": "IntSandraTalk",
            "talk_args": (),
            "examine_label": "ShowSandraCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "clara": {
            "unknown_name": "Someone",
            "talk_label": "IntClaraTalk",
            "talk_args": (),
            "examine_label": "ShowClaraCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "becky": {
            "unknown_name": "Someone",
            "talk_label": "IntBeckyTalk",
            "talk_args": (),
            "examine_label": "ShowBeckyCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "eddie": {
            "unknown_name": "Someone",
            "talk_label": "IntEddieTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "man",
            "auto_card": False,
        },
        "inga": {
            "unknown_name": "Someone",
            "talk_label": "IntIngaTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "woman",
            "auto_card": False,
        },
        "lucas": {
            "unknown_name": "Лукас",
            "talk_label": "",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look"],
            "gender": "man",
            "auto_card": False,
            "can_examine_unknown": False,
        },
        "georgett": {
            "unknown_name": "Молодая женщина",
            "talk_label": "IntGeorgettTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "woman",
            "can_examine_unknown": False,
            "auto_card": False,
        },
        "liza": {
            "unknown_name": "Someone",
            "talk_label": "IntLizaTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "auto_card": False,
        },
        "irma": {
            "unknown_name": "Someone",
            "talk_label": "IntIrmaTalk",
            "talk_args": (),
            "examine_label": "ShowIrmaCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "alber": {
            "unknown_name": "Альбер",
            "talk_label": "IntAlberTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "man",
            "auto_card": False,
        },
        "zimmer": {
            "unknown_name": "Десятник Циммерман",
            "talk_label": "IntZimmerTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "man",
            "auto_card": False,
        },
        "werecat": {
            "unknown_name": "Кошкодевочка",
            "talk_label": "IntWerecatTalk",
            "talk_args": (),
            "examine_label": "ShowWerecatCard",
            "actions": ["look", "talk"],
            "auto_card": True,
        },
        "fran": {
            "unknown_name": "Старая жрица",
            "talk_label": "FrancheskaTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "woman",
            "can_examine_unknown": False,
            "auto_card": False,
        },
        "mongol": {
            "unknown_name": "Мужик в красной рубахе",
            "talk_label": "MarketPlaceTalkMongol",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "man",
            "can_examine_unknown": False,
            "auto_card": False,
        },
    }

    def npc_meta(npc_id=""):
        return dict(NPC_META.get(str(npc_id or "").strip().lower(), {}) or {})

    def npc_is_known(npc_id):
        key = str(npc_id or "").strip().lower()
        if not key:
            return False
        return bool(knowsMC.get(key, False))

    def npc_display_name(npc_id):
        key = str(npc_id or "").strip().lower()
        if not key:
            return ""
        if npc_is_known(key):
            return str(RealName.get(key, key) or key)
        return str(npc_meta(key).get("unknown_name", "Someone") or "Someone")

    def npc_talk_label(npc_id):
        return str(npc_meta(npc_id).get("talk_label", "") or "")

    def npc_talk_args(npc_id):
        value = npc_meta(npc_id).get("talk_args", ())
        return tuple(value or ())

    def npc_examine_label(npc_id):
        return str(npc_meta(npc_id).get("examine_label", "") or "")

    def npc_action_ids(npc_id):
        return list(npc_meta(npc_id).get("actions", []) or [])

    def npc_room_interaction_visible(npc_id="", room_code=""):
        key = str(npc_id or "").strip().lower()
        room_key = str(room_code or "").strip()
        if not key or not room_key:
            return False
        if key == "clara" and room_key == "MarketPlace":
            return False
        try:
            if key == "mongol" and room_key == "MarketPlace":
                return bool(marketplace_mongol_visible())
            if key == "georgett" and room_key == "PortStreets":
                return bool(port_streets_georgett_can_talk())
            if key == "liza" and room_key == "PortStreets":
                return bool(port_streets_liza_can_talk())
            if key == "fran" and room_key in ("EllonaTemple", "EllonaBirthRoom"):
                return bool(ellona_fran_visible())
            if room_key == "TavernMelissaRoom" and tavern_melissa_room_clara_visit_active():
                return False
            if key == "zimmer" and room_key == "CityGuard":
                return bool(city_guard_open_now())
            if key == "alber" and room_key == "WineStore":
                return int(time or 0) != 0
            if room_key == "BeckyHome":
                if key == "becky":
                    return True
                if key == "eddie":
                    return ArriveMode in ("SvalnyiGreh", "")
                if key in ("inga", "lucas"):
                    return IngaVar.get("Knowher", 0) >= 1 and ArriveMode == ""
            if room_key == "BeckyHomeFront":
                if key == "becky":
                    return ArriveMode == "FromDances"
                if key in ("inga", "lucas"):
                    return ViewIngaSex > 0
        except Exception:
            return False
        return True

    def npc_action_data_for_room(npc_id="", room_code=""):
        key = str(npc_id or "").strip().lower()
        room_key = str(room_code or "").strip()
        if not npc_room_interaction_visible(key, room_key):
            return None
        data = npc_meta(key)
        data["npc_id"] = key
        if key == "georgett":
            if room_key == "PortStreets":
                data["talk_args"] = ("georgett", "street")
            elif room_key == "TavernMain":
                data["talk_args"] = ("georgett", "tavern")
        return data

    def npc_social_actions_available_in_room(npc_id="", room_code=""):
        key = str(npc_id or "").strip().lower()
        room_key = str(room_code or CurLoc or "").strip()
        if key == "" or room_key == "":
            return False
        try:
            if room_key == "TavernKitchen" and bool(TavernBreakfastEventActive):
                return key in [str(row or "").strip().lower() for row in list(tavern_breakfast_present_ids() or [])]
        except Exception:
            pass
        return bool(npc_can_talk_now(key)) and str(getLocation(key) or "") == room_key

    def npc_flirt_action_available(npc_id="", room_code=""):
        key = str(npc_id or "").strip().lower()
        if not npc_social_actions_available_in_room(key, room_code):
            return False
        allowed, reason = relationship_social_action_allowed(key, "flirt")
        if not allowed:
            return False
        try:
            if key == "melissa" and not melissa_relationship_allows(key, "flirt"):
                return False
        except Exception:
            pass
        try:
            return bool(social_has_visible_topics(key, "flirt"))
        except Exception:
            return int(FlirtedToday.get(key, 0) or 0) <= 0

    def npc_gift_action_available(npc_id="", room_code=""):
        key = str(npc_id or "").strip().lower()
        if not npc_social_actions_available_in_room(key, room_code):
            return False
        if int(GiftedToday.get(key, 0) or 0) > 0:
            return False
        allowed, reason = relationship_social_action_allowed(key, "gift")
        if not allowed:
            return False
        try:
            if key == "melissa" and not melissa_relationship_allows(key, "gift"):
                return False
            if key in ("amanda", "sandra") and not family_social_threshold_met(key, "gift"):
                return False
            if key == "clara" and (not clara_can_receive_gifts() or not clara_has_giftable_entries()):
                return False
        except Exception:
            pass
        try:
            return len(list(player_card_giftable_item_ids() or [])) > 0
        except Exception:
            return True

    def dog_action_data(where_id=""):
        room_code = str(where_id or CurLoc or "").strip()
        return {
            "entity_type": "dog",
            "entity_id": "dog",
            "title": str(dog_display_name() or "Пес"),
            "talk_label": "IntDogTalk",
            "talk_args": (room_code,),
            "examine_id": "dog",
            "examine_label": "",
            "actions": ["look", "talk"],
            "can_examine": True,
            "auto_card": True,
        }

    def npc_unique_state(npc_id):
        key = str(npc_id or "").strip().lower()
        if key == "amanda":
            return AmandaVar
        if key == "melissa":
            return MelissaVar
        if key == "sandra":
            return SandraVar
        if key == "clara":
            return ClaraVar
        if key == "becky":
            return BeckyVar
        if key == "georgett":
            return GeorgettVar
        if key == "liza":
            return LizaVar
        if key == "irma":
            return IrmaVar
        return {}

    def _npc_explicit_picture(npc_data=None, action_hint=""):
        if not isinstance(npc_data, dict):
            return ""
        action_key = str(action_hint or "").strip().lower()
        if action_key:
            explicit = str(npc_data.get("%s_picture" % action_key, "") or "").strip()
            if explicit:
                return explicit
        return str(npc_data.get("picture_path", "") or "").strip()

    def _character_action_text(value, default=""):
        if callable(value):
            try:
                value = value()
            except TypeError:
                value = default
            except Exception:
                value = default
        return str(value or default or "")

    def _character_action_display_name(character_id):
        key = str(character_id or "").strip()
        if not key:
            return ""
        return str(RealName.get(key, key) or key)

    def mark_entity_known(entity_id=""):
        key = str(entity_id or "").strip().lower()
        if key:
            knowsMC[key] = True

    def entity_knows_mc(entity_id="", entity_data=None):
        key = str(entity_id or "").strip().lower()
        if not key or key in ("you", "dog"):
            return True
        return npc_is_known(key)

    def _entity_unknown_title(entity_data=None):
        if not isinstance(entity_data, dict):
            return "Someone"
        return _character_action_text(entity_data.get("unknown_name", "Someone"), "Someone")

    def entity_presented_name(entity_type="", entity_id="", entity_data=None):
        entity_key = str(entity_type or "").strip().lower()
        entity_id_value = str(entity_id or "").strip()
        if entity_key == "player":
            return "Стефан"
        if entity_key == "dog":
            return str(dog_display_name() or "Пес")
        if not entity_id_value:
            return ""
        if entity_key == "npc":
            return npc_display_name(entity_id_value)
        if entity_knows_mc(entity_id_value, entity_data):
            return _character_action_display_name(entity_id_value)
        return _entity_unknown_title(entity_data)

    def _entity_action_can_examine(entity_type="", entity_id="", entity_data=None):
        entity_key = str(entity_type or "").strip().lower()
        if entity_key in ("player", "dog"):
            return True
        if entity_key == "npc":
            actions = set([str(action or "").strip().lower() for action in npc_action_ids(entity_id)])
            if "look" not in actions:
                return False
            examine_target = npc_examine_label(entity_id)
            if examine_target:
                return renpy.has_label(examine_target)
            return True
        if not isinstance(entity_data, dict):
            return bool(str(entity_id or "").strip())
        examine_target = _character_action_text(entity_data.get("examine_label", entity_data.get("examine_id", entity_id)), entity_id)
        if not str(examine_target or "").strip():
            return False
        return room_rule_true(entity_data.get("can_examine", True))

    def _character_action_entity_talk_args(entity_data=None):
        if not isinstance(entity_data, dict):
            return ()
        talk_args = entity_data.get("talk_args", ())
        if callable(talk_args):
            try:
                talk_args = talk_args()
            except (AttributeError, TypeError, ValueError):
                talk_args = ()
        return tuple(talk_args or ())

    def _character_action_picture_files(character_id):
        key = str(character_id or "").strip().lower()
        if not key:
            return []
        if key in _npc_picture_cache:
            return list(_npc_picture_cache.get(key, []))
        prefix = "images/%s/" % key
        files = []
        try:
            for rel_path in list(renpy.list_files() or []):
                rel_value = str(rel_path or "").replace("\\", "/")
                if rel_value.lower().startswith(prefix.lower()):
                    files.append(rel_value)
        except Exception:
            files = []
        _npc_picture_cache[key] = list(files)
        return files

    def _character_action_room_picture_tokens(where_id="", entity_data=None, action_hint=""):
        room_code = str(where_id or CurLoc or "").strip()
        action_key = str(action_hint or "").strip().lower()
        tokens = []
        if isinstance(entity_data, dict):
            for raw_hint in list(entity_data.get("media_hints", ()) or ()):
                hint_value = str(raw_hint or "").strip().lower()
                if hint_value:
                    tokens.append(hint_value)
        room_hint_map = {
            "TavernMain": ("tavern", "hall", "waitress"),
            "TavernKitchen": ("kitchen", "tavern"),
            "TavernStorage": ("storage", "basement", "tavern"),
            "Backyard": ("backyard", "tavern"),
            "TavernSandraRoom": ("room", "bedroom", "home", "comfy"),
            "TavernMelissaRoom": ("room", "bedroom", "home", "comfy"),
            "TavernAmandaRoom": ("room", "bedroom", "home", "comfy"),
            "WineStore": ("wine", "cellar", "sellar"),
            "MarketPlace": ("market", "town"),
            "Church": ("church",),
            "GroceryStore": ("shop", "town"),
            "DressShop": ("shop", "town"),
            "BarberShop": ("shop", "town"),
            "HunterClub": ("club", "town"),
        }
        for raw_hint in tuple(room_hint_map.get(room_code, ())):
            hint_value = str(raw_hint or "").strip().lower()
            if hint_value:
                tokens.append(hint_value)
        if room_in_group(room_code, ROOM_GROUP_FOREST):
            tokens.append("forest")
        if action_key:
            tokens.insert(0, action_key)
        seen = []
        for token in tokens:
            if token and token not in seen:
                seen.append(token)
        return seen

    def npc_context_picture_path(character_id="", where_id="", action_hint="", entity_data=None):
        key = str(character_id or "").strip().lower()
        if not key:
            return ""
        if key == "you":
            return str(player_card_portrait_path() or "")
        if key == "dog":
            return str(dog_card_portrait_path() or "")

        if isinstance(entity_data, dict):
            fixed_path = _npc_explicit_picture(entity_data, action_hint)
            if fixed_path:
                return fixed_path
            resolver = entity_data.get("picture_resolver", None)
            if callable(resolver):
                try:
                    resolved = str(resolver(key, where_id, action_hint) or "").strip()
                except (AttributeError, TypeError, ValueError):
                    resolved = ""
                if resolved:
                    return resolved

        files = list(_character_action_picture_files(key) or [])
        tokens = _character_action_room_picture_tokens(where_id, entity_data, action_hint)
        best_score = -999
        best_paths = []
        for rel_path in files:
            rel_lower = str(rel_path or "").lower()
            score = 0
            for token in tokens:
                if token in rel_lower:
                    score += 4
            if "card" in rel_lower:
                score -= 3
            if "/tavern/" in rel_lower and room_in_group(where_id, ROOM_GROUP_TAVERN):
                score += 2
            if score > best_score:
                best_score = score
                best_paths = [rel_path]
            elif score == best_score:
                best_paths.append(rel_path)

        if len(best_paths) > 0 and best_score > 0:
            return str(sorted(best_paths)[0] or "")

        return str(girl_card_portrait_path(key) or "")

    def npc_picture_for_action(npc, where_id="", action_hint=""):
        npc_data = dict(npc or {})
        npc_id = str(npc_data.get("npc_id", "") or npc_data.get("entity_id", "") or "").strip().lower()
        if not npc_id:
            return ""
        action_key = str(action_hint or "").strip().lower()
        known = npc_is_known(npc_id)

        if action_key == "talk":
            explicit = _npc_explicit_picture(npc_data, "talk")
            if explicit:
                return explicit
            return npc_context_picture_path(npc_id, where_id, "talk", npc_data)

        if known:
            explicit = _npc_explicit_picture(npc_data, "idle")
            if explicit:
                return explicit
            return npc_context_picture_path(npc_id, where_id, "idle", npc_data)

        return str(npc_data.get("unknown_picture", "") or "")

    def call_label_with_args(label_name="", args=()):
        target_label = str(label_name or "").strip()
        target_args = tuple(args or ())
        if not target_label or not renpy.has_label(target_label):
            return
        if len(target_args) <= 0:
            renpy.call(target_label)
        elif len(target_args) == 1:
            renpy.call(target_label, target_args[0])
        elif len(target_args) == 2:
            renpy.call(target_label, target_args[0], target_args[1])
        elif len(target_args) == 3:
            renpy.call(target_label, target_args[0], target_args[1], target_args[2])
        else:
            renpy.call(target_label, target_args[0], target_args[1], target_args[2], target_args[3])

    def _character_action_call_label(target_label="", target_args=()):
        call_label_with_args(target_label, target_args)

    def show_npc_picture_main_ui_state(character_id="", where_id="", action_hint="", entity_data=None):
        npc_data = dict(entity_data or {})
        if character_id and "npc_id" not in npc_data:
            npc_data["npc_id"] = str(character_id or "").strip().lower()
        picture_path = str(npc_picture_for_action(npc_data, where_id, action_hint) or "").strip()
        if not picture_path:
            picture_path = str(npc_context_picture_path(character_id, where_id, action_hint, entity_data) or "").strip()
        if not picture_path:
            return
        try:
            ShowImage("", "", picture_path)
        except (AttributeError, NameError, TypeError, ValueError):
            global _layout_last_picture
            _layout_last_picture = picture_path

    def show_entity_examine_main_ui_state(entity_type="", entity_id="", where_id="", entity_data=None):
        entity_key = str(entity_type or "").strip().lower()
        entity_id_value = str(entity_id or "").strip()
        entity_state = dict(entity_data or {})
        if entity_key == "player" or entity_id_value.lower() == "you":
            show_player_card_main_ui_state()
            return
        if entity_key == "dog" or entity_id_value.lower() == "dog":
            show_dog_card_main_ui_state()
            return
        mark_entity_known(entity_id_value)
        examine_label = str(entity_state.get("examine_label", "") or "").strip()
        if examine_label != "" and renpy.has_label(examine_label):
            call_label_with_args(examine_label, ())
            return
        show_npc_picture_main_ui_state(entity_id_value, where_id, "idle", entity_state)

    def action_menu_handle_back_state():
        main_ui_restore_room_scene_state()

    def NpcActionTalkState(npc_id="", where_id="", entity_data=None):
        normalized = _normalize_entity_action_data("npc", npc_id, where_id, entity_data)
        npc_key = str(normalized.get("entity_id", "") or "").strip().lower()
        where_key = str(normalized.get("where_id", "") or CurLoc or "").strip()
        if not npc_key:
            return
        show_npc_picture_main_ui_state(npc_key, where_key, "talk", normalized)
        target_label = str(normalized.get("talk_label", "") or "").strip()
        target_args = tuple(normalized.get("talk_args", ()) or ())
        if target_label and renpy.has_label(target_label):
            call_label_with_args(target_label, target_args)
            mark_entity_known(npc_key)

    def NpcActionLookState(npc_id="", where_id="", entity_data=None):
        normalized = _normalize_entity_action_data("npc", npc_id, where_id, entity_data)
        npc_key = str(normalized.get("entity_id", "") or "").strip().lower()
        where_key = str(normalized.get("where_id", "") or CurLoc or "").strip()
        if not npc_key:
            return
        show_npc_picture_main_ui_state(npc_key, where_key, "idle", normalized)
        examine_label = str(normalized.get("examine_label", "") or "").strip()
        if examine_label and renpy.has_label(examine_label):
            call_label_with_args(examine_label, ())

    def DogActionTalkState(where_id=""):
        where_key = str(where_id or CurLoc or "").strip()
        show_npc_picture_main_ui_state("dog", where_key, "talk", dog_action_data(where_key))
        call_label_with_args("IntDogTalk", (where_key,))

    def DogActionLookState(where_id=""):
        show_dog_card_main_ui_state(where_id)

    def open_npc_action_menu_state(npc_id="", where_id="", entity_data=None):
        store = renpy.store
        normalized = _normalize_entity_action_data("npc", npc_id, where_id, entity_data)
        npc_key = str(normalized.get("entity_id", "") or "").strip().lower()
        where_key = str(normalized.get("where_id", "") or CurLoc or "").strip()
        if not npc_key:
            return

        store.action_menu_entity_type = "npc"
        store.action_menu_entity_id = npc_key
        store.action_menu_where = where_key
        store.action_menu_title = str(normalized.get("title", "") or npc_display_name(npc_key))
        store.action_menu_entity_data = dict(normalized)
        store.action_menu_selected = npc_key
        store.action_menu_actions = []
        store.action_menu_specs = []

        show_npc_picture_main_ui_state(npc_key, where_key, "idle", normalized)

        actions = set([str(action or "").strip().lower() for action in list(normalized.get("actions", []) or [])])
        social_available = npc_social_actions_available_in_room(npc_key, where_key)
        if "look" in actions:
            store.action_menu_specs.append({"id": "look", "text": "Осмотреть", "entity_type": "npc", "entity_id": npc_key, "where_id": where_key})
        if social_available and "talk" in actions and str(normalized.get("talk_label", "") or "").strip() and renpy.has_label(str(normalized.get("talk_label", "") or "").strip()):
            store.action_menu_specs.append({"id": "talk", "text": "Поговорить", "entity_type": "npc", "entity_id": npc_key, "where_id": where_key})
        if "flirt" in actions and npc_flirt_action_available(npc_key, where_key):
            store.action_menu_specs.append({"id": "flirt", "text": "Флиртовать", "entity_type": "npc", "entity_id": npc_key, "where_id": where_key})
        if "gift" in actions and npc_gift_action_available(npc_key, where_key):
            store.action_menu_specs.append({"id": "gift", "text": "Подарить", "entity_type": "npc", "entity_id": npc_key, "where_id": where_key})
        store.action_menu_specs.append({"id": "back", "text": "Назад"})

        store.current_action_title = store.action_menu_title
        store.current_action_content = None
        store.current_action_items = [
            MenuItem(str(spec.get("text", "") or ""), Call("ActionMenuRunSpec", str(spec.get("id", "") or ""), str(spec.get("entity_type", "") or ""), str(spec.get("entity_id", "") or ""), str(spec.get("where_id", "") or "")))
            for spec in list(store.action_menu_specs or [])
            if str(spec.get("id", "") or "") != "back"
        ]
        store.current_action_items.append(MenuItem("Назад", Function(action_menu_handle_back_state)))
        store.action_menu_specs = []

        restart_fn = getattr(renpy, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def open_dog_action_menu_state(where_id=""):
        store = renpy.store
        where_key = str(where_id or CurLoc or "").strip()
        dog_data = dog_action_data(where_key)

        store.action_menu_entity_type = "dog"
        store.action_menu_entity_id = "dog"
        store.action_menu_where = where_key
        store.action_menu_title = str(dog_data.get("title", "") or "Пес")
        store.action_menu_entity_data = dict(dog_data)
        store.action_menu_selected = "dog"
        store.action_menu_actions = []
        store.action_menu_specs = []

        show_npc_picture_main_ui_state("dog", where_key, "idle", dog_data)

        store.action_menu_specs.append({"id": "look", "text": "Осмотреть", "entity_type": "dog", "entity_id": "dog", "where_id": where_key})
        store.action_menu_specs.append({"id": "talk", "text": "Поговорить", "entity_type": "dog", "entity_id": "dog", "where_id": where_key})
        store.action_menu_specs.append({"id": "back", "text": "Назад"})

        store.current_action_title = store.action_menu_title
        store.current_action_content = None
        store.current_action_items = [
            MenuItem(str(spec.get("text", "") or ""), Call("ActionMenuRunSpec", str(spec.get("id", "") or ""), str(spec.get("entity_type", "") or ""), str(spec.get("entity_id", "") or ""), str(spec.get("where_id", "") or "")))
            for spec in list(store.action_menu_specs or [])
            if str(spec.get("id", "") or "") != "back"
        ]
        store.current_action_items.append(MenuItem("Назад", Function(action_menu_handle_back_state)))
        store.action_menu_specs = []

        restart_fn = getattr(renpy, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def action_menu_handle_talk_state():
        entity_state = dict(action_menu_entity_data or {})
        entity_id_value = str(action_menu_entity_id or "").strip()
        entity_where = str(action_menu_where or CurLoc or "").strip()
        entity_type_value = str(action_menu_entity_type or "").strip().lower()
        if entity_type_value == "npc":
            NpcActionTalkState(entity_id_value, entity_where)
            return
        if entity_type_value == "dog":
            DogActionTalkState(entity_where)
            return
        if entity_id_value:
            mark_entity_known(entity_id_value)
            show_npc_picture_main_ui_state(entity_id_value, entity_where, "talk", entity_state)
        call_label_with_args(entity_state.get("talk_label", ""), entity_state.get("talk_args", ()))

    def action_menu_handle_look_state():
        entity_type_value = str(action_menu_entity_type or "").strip().lower()
        if entity_type_value == "npc":
            NpcActionLookState(action_menu_entity_id, action_menu_where)
            return
        if entity_type_value == "dog":
            DogActionLookState(action_menu_where)
            return
        show_entity_examine_main_ui_state(action_menu_entity_type, action_menu_entity_id, action_menu_where, action_menu_entity_data)

    def _normalize_entity_action_data(entity_type="", entity_id="", where_id="", entity_data=None):
        normalized = npc_meta(entity_id) if str(entity_type or "").strip().lower() == "npc" else {}
        normalized.update(dict(entity_data or {}))
        normalized["entity_type"] = str(entity_type or normalized.get("entity_type", "npc") or "npc").strip().lower()
        normalized["entity_id"] = str(entity_id or normalized.get("entity_id", "") or "").strip()
        normalized["where_id"] = str(where_id or normalized.get("where_id", "") or CurLoc or "").strip()
        if normalized["entity_type"] == "npc":
            if not str(normalized.get("talk_label", "") or "").strip():
                normalized["talk_label"] = npc_talk_label(normalized["entity_id"])
            normalized["talk_args"] = tuple(normalized.get("talk_args", npc_talk_args(normalized["entity_id"])) or ())
            if not str(normalized.get("examine_label", "") or "").strip():
                normalized["examine_label"] = npc_examine_label(normalized["entity_id"])
            if not list(normalized.get("actions", []) or []):
                normalized["actions"] = npc_action_ids(normalized["entity_id"])
        elif normalized["entity_type"] == "dog":
            _dog_data = dog_action_data(normalized["where_id"])
            normalized.update(dict(_dog_data))
        else:
            normalized["talk_label"] = str(normalized.get("talk_label", "") or "").strip()
            normalized["talk_args"] = tuple(_character_action_entity_talk_args(normalized))
            normalized["examine_label"] = str(normalized.get("examine_label", "") or "").strip()
            normalized["actions"] = list(normalized.get("actions", []) or [])
        normalized["examine_id"] = _character_action_text(normalized.get("examine_id", normalized["entity_id"]), normalized["entity_id"])
        normalized["auto_card"] = bool(normalized.get("auto_card", False))
        normalized["can_examine"] = bool(_entity_action_can_examine(normalized["entity_type"], normalized["entity_id"], normalized))
        normalized["title"] = str(normalized.get("title", "") or entity_presented_name(normalized["entity_type"], normalized["entity_id"], normalized))
        return normalized

    def open_entity_action_menu_state(entity_type="", entity_id="", where_id="", entity_data=None):
        entity_type_value = str(entity_type or "").strip().lower()
        if entity_type_value == "dog":
            open_dog_action_menu_state(where_id)
            return
        store = renpy.store
        normalized = _normalize_entity_action_data(entity_type, entity_id, where_id, entity_data)
        entity_id_value = str(normalized.get("entity_id", "") or "").strip()
        entity_type_value = str(normalized.get("entity_type", "npc") or "npc").strip().lower()
        entity_where = str(normalized.get("where_id", "") or CurLoc or "").strip()

        store.action_menu_entity_type = entity_type_value
        store.action_menu_entity_id = entity_id_value
        store.action_menu_where = entity_where
        store.action_menu_title = str(normalized.get("title", "") or "Персонаж")
        store.action_menu_entity_data = dict(normalized)
        store.action_menu_selected = entity_id_value
        store.action_menu_actions = []
        store.action_menu_specs = []

        if entity_type_value == "player":
            show_player_card_main_ui_state()
            return

        if entity_id_value:
            show_npc_picture_main_ui_state(entity_id_value, entity_where, "idle", normalized)

        actions = set([str(action or "").strip().lower() for action in list(normalized.get("actions", []) or []) if str(action or "").strip()])
        social_available = True
        if entity_type_value == "npc":
            social_available = npc_social_actions_available_in_room(entity_id_value, entity_where)
        can_talk = social_available and ("talk" in actions) and bool(str(normalized.get("talk_label", "") or "").strip() and renpy.has_label(str(normalized.get("talk_label", "") or "").strip()))
        can_examine = ("look" in actions) and bool(normalized.get("can_examine", False))
        if can_examine:
            store.action_menu_specs.append({"id": "look", "text": "Осмотреть", "entity_type": entity_type_value, "entity_id": entity_id_value, "where_id": entity_where})
        if can_talk:
            store.action_menu_specs.append({"id": "talk", "text": "Поговорить", "entity_type": entity_type_value, "entity_id": entity_id_value, "where_id": entity_where})
        store.action_menu_specs.append({"id": "back", "text": "Назад"})

        store.current_action_title = store.action_menu_title
        store.current_action_content = None
        store.current_action_items = [
            MenuItem(str(spec.get("text", "") or ""), Call("ActionMenuRunSpec", str(spec.get("id", "") or ""), str(spec.get("entity_type", "") or ""), str(spec.get("entity_id", "") or ""), str(spec.get("where_id", "") or "")))
            for spec in list(store.action_menu_specs or [])
            if str(spec.get("id", "") or "") != "back"
        ]
        store.current_action_items.append(MenuItem("Назад", Function(action_menu_handle_back_state)))
        store.action_menu_specs = []

        restart_fn = getattr(renpy, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def _character_action_grid_entries(room):
        entries = [{
            "entity_type": "player",
            "id": "you",
            "title": "Стефан",
            "where_id": str(getattr(room, "code_name", "") or CurLoc or ""),
            "entity_data": {
                "entity_type": "player",
                "entity_id": "you",
                "title": "Стефан",
                "examine_id": "you",
                "can_examine": True,
            },
        }]
        if room is None or not hasattr(room, "visible_npcs"):
            return entries

        room_code = str(getattr(room, "code_name", "") or "")
        seen_ids = set()
        for npc in room.visible_npcs():
            if not isinstance(npc, dict):
                continue
            npc_id = str(npc.get("npc_id", "") or "").strip()
            if not npc_id:
                continue
            seen_ids.add(npc_id)
            row_data = _normalize_entity_action_data("npc", npc_id, room_code, npc)
            entries.append({
                "entity_type": "npc",
                "id": npc_id,
                "title": str(row_data.get("title", "") or npc_id),
                "where_id": room_code,
                "entity_data": row_data,
            })

        if room_code == "TavernKitchen" and bool(TavernBreakfastEventActive):
            for npc_id in list(tavern_breakfast_present_ids() or []):
                npc_key = str(npc_id or "").strip().lower()
                if not npc_key or npc_key in seen_ids:
                    continue
                row_data = _normalize_entity_action_data("npc", npc_key, room_code, npc_action_data_for_room(npc_key, room_code) or {})
                entries.append({
                    "entity_type": "npc",
                    "id": npc_key,
                    "title": str(row_data.get("title", "") or npc_key),
                    "where_id": room_code,
                    "entity_data": row_data,
                })
                seen_ids.add(npc_key)

        if room_code and dog_is_available_here(room_code):
            dog_data = _normalize_entity_action_data("dog", "dog", room_code, {})
            entries.append({
                "entity_type": "dog",
                "id": "dog",
                "title": str(dog_data.get("title", "") or "Пес"),
                "where_id": room_code,
                "entity_data": dog_data,
            })
        return entries[:9]


label OpenEntityActionMenu(entity_type="", entity_id="", where_id="", entity_data=None):
    $ open_entity_action_menu_state(entity_type, entity_id, where_id, entity_data)
    return


label OpenNpcActionMenu(npc_id="", where_id="", entity_data=None):
    $ open_npc_action_menu_state(npc_id, where_id, entity_data)
    return


label NpcActionTalk(npc_id="", where_id="", entity_data=None):
    $ NpcActionTalkState(npc_id, where_id, entity_data)
    return


label NpcActionLook(npc_id="", where_id="", entity_data=None):
    $ NpcActionLookState(npc_id, where_id, entity_data)
    return


label ActionMenuHandleTalk:
    $ action_menu_handle_talk_state()
    return


label ActionMenuHandleLook:
    $ action_menu_handle_look_state()
    return


label ActionMenuHandleBack:
    $ action_menu_handle_back_state()
    return


label ShowAmandaCard:
    $ show_girl_card_main_ui_state("amanda")
    return


label ShowMelissaCard:
    $ show_girl_card_main_ui_state("melissa")
    return


label ShowSandraCard:
    $ show_girl_card_main_ui_state("sandra")
    return


label ShowClaraCard:
    $ show_girl_card_main_ui_state("clara")
    return


label ShowBeckyCard:
    $ show_girl_card_main_ui_state("becky")
    return


label ShowIrmaCard:
    $ show_girl_card_main_ui_state("irma")
    return
