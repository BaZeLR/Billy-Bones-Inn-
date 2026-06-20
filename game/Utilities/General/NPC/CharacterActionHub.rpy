# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default knowsMC = {}

init -40 python:
    import renpy.exports as renpy

    _npc_picture_cache = {}
    NPC_META = {
        "amanda": {
            "unknown_name": "Незнакомка",
            "talk_label": "AmandaTalkHubEventEntry",
            "talk_args": (),
            "examine_label": "ShowAmandaCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "melissa": {
            "unknown_name": "Незнакомка",
            "talk_label": "IntMelissaTalk",
            "talk_args": (),
            "examine_label": "ShowMelissaCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "sandra": {
            "unknown_name": "Незнакомка",
            "talk_label": "IntSandraTalk",
            "talk_args": (),
            "examine_label": "ShowSandraCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "clara": {
            "unknown_name": "Незнакомка",
            "talk_label": "IntClaraTalk",
            "talk_args": (),
            "examine_label": "ShowClaraCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "becky": {
            "unknown_name": "Незнакомка",
            "talk_label": "IntBeckyTalk",
            "talk_args": (),
            "examine_label": "ShowBeckyCard",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": True,
        },
        "eddie": {
            "unknown_name": "Незнакомец",
            "talk_label": "IntEddieTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "man",
            "auto_card": False,
        },
        "inga": {
            "unknown_name": "Незнакомка",
            "talk_label": "IntIngaTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk", "gift", "flirt"],
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
            "actions": ["look", "talk", "gift", "flirt"],
            "gender": "woman",
            "can_examine_unknown": False,
            "auto_card": False,
        },
        "liza": {
            "unknown_name": "Молодая женщина",
            "talk_label": "IntLizaTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk", "gift", "flirt"],
            "auto_card": False,
        },
        "irma": {
            "unknown_name": "Незнакомка",
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
        "draupnir": {
            "unknown_name": "Драупнир",
            "talk_label": "IntDraupnirTalk",
            "talk_args": (),
            "examine_label": "",
            "actions": ["look", "talk"],
            "gender": "man",
            "auto_card": False,
        },
        "sergio": {
            "unknown_name": "Серджио",
            "talk_label": "BarberShopTalk",
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
        try:
            info = getPersonInfo(key)
            if info is not None:
                return bool(getattr(info, "known", False))
        except Exception:
            pass
        return bool(knowsMC.get(key, False))

    def _is_generic_unknown_name(value=""):
        return str(value or "").strip().lower() in ("", "someone", "somebody")

    def _unknown_role_name(meta=None, fallback=""):
        data = dict(meta or {})
        gender = str(data.get("gender", "") or "").strip().lower()
        if gender == "man":
            return "Незнакомец"
        if gender == "woman" or "flirt" in [str(row or "").strip().lower() for row in list(data.get("actions", []) or [])]:
            return "Незнакомка"
        return str(fallback or "Персонаж")

    def npc_display_name(npc_id):
        key = str(npc_id or "").strip().lower()
        if not key:
            return ""
        info = None
        try:
            info = getPersonInfo(key)
        except Exception:
            info = None
        if npc_is_known(key):
            if info is not None and hasattr(info, "display_name"):
                try:
                    return str(info.display_name() or key)
                except Exception:
                    pass
            return str(people_display_name(key) or key)
        class_unknown_name = ""
        if info is not None:
            class_unknown_name = str(getattr(info, "unknown_name", "") or "").strip()
        if not _is_generic_unknown_name(class_unknown_name):
            return class_unknown_name
        meta = npc_meta(key)
        unknown_name = str(meta.get("unknown_name", "") or "").strip()
        if not _is_generic_unknown_name(unknown_name):
            return unknown_name
        return _unknown_role_name(meta, key)

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
                return bool(Francheska.visible_now())
            if key == "zimmer" and room_key == "CityGuard":
                return bool(city_guard_open_now())
            if key == "alber" and room_key == "WineStore":
                return str(getLocation("alber") or "") == "WineStore" and bool(npc_can_talk_now("alber"))
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
        if room_key == "GroceryStore" and key in ("eddie", "becky", "inga"):
            data = npc_meta(key)
            data["npc_id"] = key
            data["unknown_name"] = "Торговец"
            if not npc_is_known(key):
                data["title"] = "Торговец"
            try:
                data["picture_path"] = grocery_store_grocer_picture(key)
                data["talk_picture"] = data["picture_path"]
            except (NameError, AttributeError, TypeError, ValueError):
                pass
            return data
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
        if not (bool(npc_can_talk_now(key)) and str(getLocation(key) or "") == room_key):
            return False
        try:
            info = getPersonInfo(key)
            if info is not None and hasattr(info, "social_action_allowed"):
                return bool(info.social_action_allowed("talk"))
        except Exception:
            pass
        return True

    def npc_flirt_action_available(npc_id="", room_code=""):
        key = str(npc_id or "").strip().lower()
        if not npc_social_actions_available_in_room(key, room_code):
            return False
        try:
            info = getPersonInfo(key)
            if info is not None and hasattr(info, "social_action_allowed") and not info.social_action_allowed("flirt"):
                return False
        except Exception:
            pass
        if not social_interaction_allowed_for_npc(key, "flirt"):
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
        try:
            info = getPersonInfo(key)
            if info is not None and hasattr(info, "social_action_allowed") and not info.social_action_allowed("gift"):
                return False
        except Exception:
            pass
        if not relationship_any_gift_allowed(key):
            return False
        try:
            if key == "melissa" and not melissa_relationship_allows(key, "gift"):
                return False
            if key == "clara" and (not Clara.can_receive_gifts() or not Clara.has_giftable_entries()):
                return False
        except Exception:
            pass
        try:
            return len(list(player_card_giftable_item_ids() or [])) > 0
        except Exception:
            return True

    def npc_unique_state(npc_id):
        info = getPersonInfo(str(npc_id or "").strip().lower())
        state = getattr(info, "var", None) if info is not None else None
        return state if isinstance(state, dict) else {}

    def _npc_explicit_picture(npc_data=None, action_hint=""):
        if not isinstance(npc_data, dict):
            return ""
        action_key = str(action_hint or "").strip().lower()
        if action_key:
            explicit = str(npc_data.get("%s_picture" % action_key, "") or "").strip()
            if explicit:
                return explicit
        return str(npc_data.get("picture_path", "") or "").strip()

    def mark_entity_known(entity_id=""):
        key = str(entity_id or "").strip().lower()
        if not key:
            return False
        try:
            info = getPersonInfo(key)
            if info is not None and hasattr(info, "mark_known"):
                return bool(info.mark_known())
        except Exception:
            pass
        knowsMC[key] = True
        return True

    def npc_context_picture_path(character_id="", where_id="", action_hint="", entity_data=None):
        key = str(character_id or "").strip().lower()
        if not key:
            return ""
        if key == "you":
            return str(player_card_portrait_path() or "")

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

    def NpcActionTalkState(npc_id="", where_id="", entity_data=None):
        normalized = npc_action_data(npc_id, where_id, entity_data)
        npc_key = str(normalized.get("entity_id", "") or "").strip().lower()
        where_key = str(normalized.get("where_id", "") or CurLoc or "").strip()
        if not npc_key:
            return
        show_npc_picture_main_ui_state(npc_key, where_key, "talk", normalized)
        target_label = str(normalized.get("talk_label", "") or "").strip()
        target_args = tuple(normalized.get("talk_args", ()) or ())
        if target_label and renpy.has_label(target_label):
            renpy.call_in_new_context(target_label, *target_args)
            mark_entity_known(npc_key)

    def NpcActionLookState(npc_id="", where_id="", entity_data=None):
        normalized = npc_action_data(npc_id, where_id, entity_data)
        npc_key = str(normalized.get("entity_id", "") or "").strip().lower()
        where_key = str(normalized.get("where_id", "") or CurLoc or "").strip()
        if not npc_key:
            return
        show_npc_picture_main_ui_state(npc_key, where_key, "idle", normalized)
        try:
            player_observe_npc_body(npc_key, where_key)
        except Exception:
            pass
        examine_label = str(normalized.get("examine_label", "") or "").strip()
        if examine_label and renpy.has_label(examine_label):
            renpy.call_in_new_context(examine_label)

    def open_npc_action_menu_state(npc_id="", where_id="", entity_data=None):
        global current_action_title, current_action_content, current_action_items
        normalized = npc_action_data(npc_id, where_id, entity_data)
        npc_key = str(normalized.get("entity_id", "") or "").strip()
        room_key = str(normalized.get("where_id", "") or CurLoc or "").strip()

        if npc_key:
            show_npc_picture_main_ui_state(npc_key, room_key, "idle", normalized)

        actions = set([str(action or "").strip().lower() for action in list(normalized.get("actions", []) or []) if str(action or "").strip()])
        social_available = npc_social_actions_available_in_room(npc_key, room_key)
        can_talk = social_available and ("talk" in actions) and bool(str(normalized.get("talk_label", "") or "").strip() and renpy.has_label(str(normalized.get("talk_label", "") or "").strip()))
        can_examine = ("look" in actions) and bool(normalized.get("can_examine", False))

        menu_items = []
        if can_examine:
            menu_items.append(MenuItem("Осмотреть", Function(NpcActionLookState, npc_key, room_key, dict(normalized))))
        if can_talk:
            menu_items.append(MenuItem("Поговорить", Function(NpcActionTalkState, npc_key, room_key, dict(normalized))))
        if "flirt" in actions and npc_flirt_action_available(npc_key, room_key):
            menu_items.append(MenuItem("Флиртовать", Call("SocialTalkTopicMenu", npc_key, "flirt", social_topic_return_label(npc_key))))
        if "gift" in actions and npc_gift_action_available(npc_key, room_key):
            if npc_key == "clara":
                menu_items.append(MenuItem("Подарить", Call("IntClaraGiftMenu", npc_key)))
            else:
                menu_items.append(MenuItem("Подарить", Call("PlayerCardGiftToFixedTargetMenu", npc_key)))
        try:
            _amanda_ai_enabled = bool(AmandaAIIntegrationEnabled)
        except NameError:
            _amanda_ai_enabled = False
        if npc_key == "amanda" and _amanda_ai_enabled:
            try:
                _amanda_ai_intent = amanda_ai_room_intent_code(room_key)
            except Exception:
                _amanda_ai_intent = ""
            if str(_amanda_ai_intent or "") != "":
                menu_items.append(MenuItem(amanda_ai_menu_label(_amanda_ai_intent), Call("AmandaAIIntentRoomEvent", room_key, _amanda_ai_intent)))

        current_action_title = str(normalized.get("title", "") or "Персонаж")
        current_action_content = None
        current_action_items = menu_items
        current_action_items.append(MenuItem("Назад", Jump(str(CurLoc or ""))))

        restart_fn = getattr(renpy, "restart_interaction", None)
        if callable(restart_fn):
            restart_fn()

    def npc_action_data(npc_id="", where_id="", entity_data=None):
        normalized = npc_meta(npc_id)
        normalized.update(dict(entity_data or {}))
        normalized["entity_type"] = "npc"
        normalized["entity_id"] = str(npc_id or normalized.get("entity_id", "") or normalized.get("npc_id", "") or "").strip()
        normalized["npc_id"] = normalized["entity_id"]
        normalized["where_id"] = str(where_id or normalized.get("where_id", "") or CurLoc or "").strip()
        if not str(normalized.get("talk_label", "") or "").strip():
            normalized["talk_label"] = npc_talk_label(normalized["entity_id"])
        normalized["talk_args"] = tuple(normalized.get("talk_args", npc_talk_args(normalized["entity_id"])) or ())
        if not str(normalized.get("examine_label", "") or "").strip():
            normalized["examine_label"] = npc_examine_label(normalized["entity_id"])
        if not list(normalized.get("actions", []) or []):
            normalized["actions"] = npc_action_ids(normalized["entity_id"])
        normalized["examine_id"] = str(normalized.get("examine_id", normalized["entity_id"]) or normalized["entity_id"])
        normalized["auto_card"] = bool(normalized.get("auto_card", False))
        actions = set([str(action or "").strip().lower() for action in list(normalized.get("actions", []) or [])])
        examine_target = str(normalized.get("examine_label", "") or "").strip()
        normalized["can_examine"] = bool("look" in actions and (not examine_target or renpy.has_label(examine_target)))
        normalized["title"] = str(normalized.get("title", "") or npc_display_name(normalized["entity_id"]))
        return normalized

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
