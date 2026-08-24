            (player.tavern_management.breakfast, "text_pages", "TavernBreakfastTextPages", []),
            (player.tavern_management.breakfast, "text_page_index", "TavernBreakfastTextPageIndex", 0),
            (player.tavern_management.breakfast, "text_return_label", "TavernBreakfastTextReturnLabel", ""),        tractir_save_migrate_paged_panel_runtime()    def tractir_save_migrate_paged_panel_runtime():
        import renpy.store as store

        legacy_pages = list(getattr(store, "panel_paged_pages", []) or getattr(store, "tavern_event_pages", []) or [])
        if legacy_pages and not list(paged_panel.pages or []):
            paged_panel.pages = legacy_pages
        paged_panel.page_index = int(getattr(store, "panel_paged_page_index", getattr(store, "tavern_event_page_index", paged_panel.page_index)) or 0)
        paged_panel.next_title = str(getattr(store, "panel_paged_next_title", getattr(store, "tavern_event_next_title", paged_panel.next_title)) or "")
        paged_panel.next_items = list(getattr(store, "panel_paged_next_items", getattr(store, "tavern_event_next_items", paged_panel.next_items)) or [])
        paged_panel.style = str(getattr(store, "panel_paged_style", paged_panel.style) or "plain")
        paged_panel.raw_text = str(getattr(store, "panel_paged_raw_text", paged_panel.raw_text) or "")
        paged_panel.tavern_event_raw_text = str(getattr(store, "tavern_event_panel_raw_text", paged_panel.tavern_event_raw_text) or "")

        pending_text = str(getattr(store, "panel_paged_pending_text", "") or "")
        if pending_text and not list(paged_panel.pages or []):
            paged_panel.pages = build_tavern_event_pages(pending_text)
            paged_panel.page_index = 0
            paged_panel.next_title = str(getattr(store, "panel_paged_pending_title", "") or "")
            paged_panel.next_items = list(getattr(store, "panel_paged_pending_items", []) or [])
            paged_panel.style = str(getattr(store, "panel_paged_pending_style", "plain") or "plain")

        for legacy_name in (
            "tavern_event_panel_raw_text", "tavern_event_pages", "tavern_event_page_index",
            "tavern_event_next_title", "tavern_event_next_items", "panel_paged_raw_text",
            "panel_paged_pages", "panel_paged_page_index", "panel_paged_next_title",
            "panel_paged_next_items", "panel_paged_style", "panel_paged_pending_text",
            "panel_paged_pending_title", "panel_paged_pending_items", "panel_paged_pending_style",
        ):
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_domain_singletons()    def tractir_save_migrate_combat_singletons():
        import renpy.store as store

        for owner, legacy_name in ((fight, "Fight"), (hunt, "Hunt")):
            legacy_owner = getattr(store, legacy_name, None)
            if legacy_owner is not None and hasattr(legacy_owner, "__dict__"):
                owner.__dict__.update(dict(legacy_owner.__dict__ or {}))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_domain_singletons():
        import renpy.store as store

        singleton_rows = (
            (recipe_book, "RecipeBook"),
            (crafting, "Crafting"),
            (household, "Household"),
        )
        for owner, legacy_name in singleton_rows:
            legacy_owner = getattr(store, legacy_name, None)
            if legacy_owner is not None and hasattr(legacy_owner, "__dict__"):
                owner.__dict__.update(dict(legacy_owner.__dict__ or {}))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_time_and_lifecycle_state()    def tractir_save_migrate_report_and_progress_runtime():
        import renpy.store as store

        owner_fields = (
            (next_day_runtime, "report_title", "NextDayReportTitle", ""),
            (next_day_runtime, "report_body", "NextDayReportBody", ""),
            (tractir_progress, "activated_achievements", "tractir_activated_achievements", set()),
            (tractir_progress, "achieved", "tractir_achieved", set()),
            (tractir_progress, "endings", "tractir_endings", set()),
            (tractir_progress, "view", "tractir_progress_view", "achievements"),
            (tractir_progress, "ending_title", "TractirEndingTitle", ""),
            (tractir_progress, "ending_body", "TractirEndingBody", ""),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_room_entry_runtime():
        import renpy.store as store

        owner_fields = (
            ("present_ids", "RoomEnterPresentIds", []),
            ("last_room", "RoomEnterLastRoom", ""),
            ("last_event_fired", "RoomEnterLastEventFired", False),
        )
        for field_name, legacy_name, default_value in owner_fields:
            if not hasattr(room_entry_runtime, field_name):
                setattr(room_entry_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_time_and_lifecycle_state():
        import renpy.store as store

        owner_fields = (
            (player.economy, "child_birth_benefit_notice", "KidBirthPosobie", ""),
            (player, "sleep_wake_hour_override", "SleepWakeHourOverride", -1),
            (player, "sleep_wake_minute_override", "SleepWakeMinuteOverride", 0),
            (calendar_v2, "time_advance_blocked", "BlockTimeAdvance", 0),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_room_owned_state()    def tractir_save_migrate_room_owned_state():
        import renpy.store as store

        room_fields = (
            (ShedRoom, "notice_text", "ShedNoticeText", ""),
            (ShedRoom, "notice_pending", "ShedNoticePending", False),
            (ShedRoom, "bucket_found", "ShedBucketFound", False),
            (TavernMyRoom, "attic_hatch_found", "TavernMyRoomAtticHatchFound", False),
        )
        for room_obj, field_name, legacy_name, default_value in room_fields:
            room_obj.state = dict(getattr(room_obj, "state", {}) or {})
            if field_name not in room_obj.state:
                room_obj.state[field_name] = getattr(store, legacy_name, default_value)
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_module_runtime()    def tractir_save_migrate_dress_shop():
        import renpy.store as store

        field_rows = (
            ("produced", "DressProduced", ""),
            ("buyer", "DressBuyer", ""),
            ("measure_stage", "IrmaMeasureShopStage", 0),
            ("sex_step", "IrmaSexShopStep", 0),
            ("girl_dress_block", "GirlDressBlock", 0),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(dress_shop, field_name):
                setattr(dress_shop, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        if not hasattr(player.appearance, "girl_dresses_bought"):
            player.appearance.girl_dresses_bought = int(getattr(store, "GirlDressesBought", 0) or 0)
        if hasattr(store, "GirlDressesBought"):
            delattr(store, "GirlDressesBought")

    def tractir_save_migrate_module_runtime():
        import renpy.store as store

        field_rows = (
            ("kind", "active_module_kind", ""),
            ("return_label", "active_module_return_label", ""),
            ("return_room", "active_module_return_room", ""),
            ("actor", "active_module_actor", ""),
            ("somebody_cums", "SomebodyCums", 0),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(module_runtime, field_name):
                setattr(module_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_relationship_scores()    def tractir_save_migrate_town_workers():
        import renpy.store as store

        if not hasattr(TownStreet, "blackworker_candidates"):
            TownStreet.blackworker_candidates = list(getattr(store, "TavernBlackworkerCandidates", []) or [])
        if not hasattr(TownStreet, "blackworkers"):
            TownStreet.blackworkers = list(getattr(store, "TavernBlackworkers", []) or [])
        for legacy_name in ("TavernBlackworkerCandidates", "TavernBlackworkers"):
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_story_event_runtime():
        import renpy.store as store

        field_rows = (
            ("active_event", "active_event", None),
            ("random_events", "random_events", []),
            ("story_events", "story_events", []),
            ("tavern_work_events", "tavern_work_events", []),
            ("available", "availEvents", {}),
            ("evaluation_time", "evalTime", None),
            ("locations", "eventLocations", set()),
            ("people", "eventPeople", set()),
            ("talk", "eventTalk", set()),
            ("options", "eventOptions", set()),
            ("items", "eventItems", set()),
            ("paths", "eventPath", set()),
            ("projection_rows", "eventProjectionRows", []),
            ("route_hints", "eventRouteHints", {}),
            ("thread_levels", "story_thread_levels", {}),
            ("fired_day", "StoryEventFiredDay", -1),
            ("fired_keys_today", "StoryEventFiredKeysToday", []),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(event_runtime, field_name):
                setattr(event_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_daily_events():
        import renpy.store as store

        legacy_rows = getattr(store, "DailyEventsList", None)
        if isinstance(legacy_rows, list) and len(daily_events.rows) == 0:
            daily_events.rows = list(legacy_rows)
        if hasattr(store, "DailyEventsList"):
            delattr(store, "DailyEventsList")

    def tractir_save_migrate_francheska_schedule():
        import renpy.store as store

        if not hasattr(Francheska, "busy_slots"):
            legacy_busy = getattr(store, "FranBusy", {})
            if isinstance(legacy_busy, list):
                legacy_busy = dict((index, value) for index, value in enumerate(legacy_busy))
            Francheska.busy_slots = dict(legacy_busy or {})
        for slot in range(8):
            Francheska.busy_slots.setdefault(slot, 0)
        if hasattr(store, "FranBusy"):
            delattr(store, "FranBusy")

    def tractir_save_migrate_girl_decisions():
        import renpy.store as store

        legacy_results = getattr(store, "GirlDecisionLast", None)
        if isinstance(legacy_results, dict):
            for composite_key, result in legacy_results.items():
                person, separator, action = str(composite_key or "").partition(":")
                info = getPersonInfo(person)
                if separator and info is not None:
                    info.var.setdefault("decision_results", {})[action] = dict(result or {})
        if hasattr(store, "GirlDecisionLast"):
            delattr(store, "GirlDecisionLast")

    def tractir_save_migrate_relationship_scores():
        import renpy.store as store

        legacy_scores = getattr(store, "RelationshipInteractionScore", None)
        if isinstance(legacy_scores, dict):
            for person, score in legacy_scores.items():
                row = relationship_state(person)
                if row:
                    row["interaction_score"] = max(int(row.get("interaction_score", 0) or 0), int(score or 0))
        if hasattr(store, "RelationshipInteractionScore"):
            delattr(store, "RelationshipInteractionScore")
        tractir_save_migrate_player_owned_scalars()    def tractir_save_migrate_player_owned_scalars():
        import renpy.store as store

        owner_fields = (
            (player.tavern_management, "visitors", "tavernvisitors", 40),
            (player.tavern_management, "slogan_state", "SloganFixed", 0),
            (player.tavern_management, "client_room_hole", "TavernHole", 0),
            (player.tavern_management, "glory_hole", "TavernGloryHole", 0),
            (player.tavern_management, "glory_hole_look", "GloryHoleLook", 0),
            (player.tavern_management, "dance_sponsor", "DanceSponsor", 0),
            (player.tavern_management, "household_members", "householdmembers", 4),
            (player.economy, "church_donated_amount", "ChurchDonatedAmount", 0),
            (player.intimacy, "ellona_blessed", "BlessedByEllona", 0),
            (player.intimacy, "ellona_cursed", "CursedByEllona", 0),
            (player.intimacy, "ellona_curse_days", "CursedByEllonaDays", 0),
            (player.intimacy, "ellona_curse_reduction", "CursedByEllonaReduce", 0),
            (player.tavern_management.breakfast, "today", "BreakfastToday", False),
            (player.tavern_management.breakfast, "last_day", "TavernBreakfastLastDay", -1),
            (player.tavern_management.breakfast, "day", "TavernBreakfastDay", -1),
            (player.tavern_management.breakfast, "base_text", "TavernBreakfastBaseText", ""),
            (player.tavern_management.breakfast, "soap_announced_day", "TavernBreakfastSoapAnnouncedDay", -1),
            (player.tavern_management.breakfast, "barber_talk_day", "TavernBreakfastBarberTalkDay", -1),
            (player.tavern_management.breakfast, "listen_day", "TavernBreakfastListenDay", -1),
            (player.tavern_management.breakfast, "market_talk_day", "TavernBreakfastMarketTalkDay", -1),
            (player.tavern_management.breakfast, "motivation_day", "TavernBreakfastMotivationDay", -1),
            (player.tavern_management.breakfast, "absent_talk_day", "TavernBreakfastAbsentTalkDay", -1),
            (player.tavern_management.breakfast, "base_shown_day", "TavernBreakfastBaseShownDay", -1),
            (player.tavern_management.breakfast, "event_active", "TavernBreakfastEventActive", False),
            (player.tavern_management.breakfast, "sunday_dinner_last_day", "TavernSundayDinnerLastDay", -1),
            (player.tavern_management.breakfast, "sunday_dinner_barber_talk_day", "TavernSundayDinnerBarberTalkDay", -1),
            (player.tavern_management.breakfast, "spicy_drink_day", "TavernBreakfastSpicyDrinkDay", -1),
            (player.tavern_management.breakfast, "sunday_dinner_spicy_drink_day", "TavernSundayDinnerSpicyDrinkDay", -1),
            (player.tavern_management.breakfast, "georgett_liza_pending", "TavernBreakfastGeorgetteLizaPending", 0),
            (player.tavern_management.breakfast, "present_ids", "TavernBreakfastPresentIds", None),
            (player.tavern_management.breakfast, "melissa_amanda_gerhard_day", "TavernBreakfastMelissaAmandaGerhardDay", -1),
            (player.tavern_management.breakfast, "food_perk_day", "TavernBreakfastFoodPerkDay", -1),
            (player.tavern_management.breakfast, "drink_perk_day", "TavernBreakfastDrinkPerkDay", -1),
            (player.tavern_management.breakfast, "lewd_series_day", "TavernBreakfastLewdSeriesDay", -1),
            (player.tavern_management.breakfast, "appearance_perk_day", "TavernBreakfastAppearancePerkDay", -1),
            (player.tavern_management.breakfast, "sweet_perk_day", "TavernBreakfastSweetPerkDay", -1),
            (player.tavern_management.breakfast, "blind_pirate_team_pledge", "TavernBreakfastBlindPirateTeamPledge", 0),
            (player.tavern_management.breakfast, "milk_team_talk_done", "TavernBreakfastMilkTeamTalkDone", 0),
            (player.tavern_management.breakfast, "ale_team_talk_done", "TavernBreakfastAleTeamTalkDone", 0),
            (player.tavern_management.breakfast, "dance_sponsor_announced_day", "TavernBreakfastDanceSponsorAnnouncedDay", -1),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        if not hasattr(player.intimacy, "ellona_grace_blessings"):
            player.intimacy.ellona_grace_blessings = list(getattr(store, "GraceBlessing", [0, 0, 0, 0, 0, 0]) or [])
        if hasattr(store, "GraceBlessing"):
            delattr(store, "GraceBlessing")
            (player.tavern_management.breakfast, "text_pages", "TavernBreakfastTextPages", []),
            (player.tavern_management.breakfast, "text_page_index", "TavernBreakfastTextPageIndex", 0),
            (player.tavern_management.breakfast, "text_return_label", "TavernBreakfastTextReturnLabel", ""),        tractir_save_migrate_paged_panel_runtime()    def tractir_save_migrate_paged_panel_runtime():
        import renpy.store as store

        legacy_pages = list(getattr(store, "panel_paged_pages", []) or getattr(store, "tavern_event_pages", []) or [])
        if legacy_pages and not list(paged_panel.pages or []):
            paged_panel.pages = legacy_pages
        paged_panel.page_index = int(getattr(store, "panel_paged_page_index", getattr(store, "tavern_event_page_index", paged_panel.page_index)) or 0)
        paged_panel.next_title = str(getattr(store, "panel_paged_next_title", getattr(store, "tavern_event_next_title", paged_panel.next_title)) or "")
        paged_panel.next_items = list(getattr(store, "panel_paged_next_items", getattr(store, "tavern_event_next_items", paged_panel.next_items)) or [])
        paged_panel.style = str(getattr(store, "panel_paged_style", paged_panel.style) or "plain")
        paged_panel.raw_text = str(getattr(store, "panel_paged_raw_text", paged_panel.raw_text) or "")
        paged_panel.tavern_event_raw_text = str(getattr(store, "tavern_event_panel_raw_text", paged_panel.tavern_event_raw_text) or "")

        pending_text = str(getattr(store, "panel_paged_pending_text", "") or "")
        if pending_text and not list(paged_panel.pages or []):
            paged_panel.pages = build_tavern_event_pages(pending_text)
            paged_panel.page_index = 0
            paged_panel.next_title = str(getattr(store, "panel_paged_pending_title", "") or "")
            paged_panel.next_items = list(getattr(store, "panel_paged_pending_items", []) or [])
            paged_panel.style = str(getattr(store, "panel_paged_pending_style", "plain") or "plain")

        for legacy_name in (
            "tavern_event_panel_raw_text", "tavern_event_pages", "tavern_event_page_index",
            "tavern_event_next_title", "tavern_event_next_items", "panel_paged_raw_text",
            "panel_paged_pages", "panel_paged_page_index", "panel_paged_next_title",
            "panel_paged_next_items", "panel_paged_style", "panel_paged_pending_text",
            "panel_paged_pending_title", "panel_paged_pending_items", "panel_paged_pending_style",
        ):
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_domain_singletons()    def tractir_save_migrate_combat_singletons():
        import renpy.store as store

        for owner, legacy_name in ((fight, "Fight"), (hunt, "Hunt")):
            legacy_owner = getattr(store, legacy_name, None)
            if legacy_owner is not None and hasattr(legacy_owner, "__dict__"):
                owner.__dict__.update(dict(legacy_owner.__dict__ or {}))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_domain_singletons():
        import renpy.store as store

        singleton_rows = (
            (recipe_book, "RecipeBook"),
            (crafting, "Crafting"),
            (household, "Household"),
        )
        for owner, legacy_name in singleton_rows:
            legacy_owner = getattr(store, legacy_name, None)
            if legacy_owner is not None and hasattr(legacy_owner, "__dict__"):
                owner.__dict__.update(dict(legacy_owner.__dict__ or {}))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_time_and_lifecycle_state()    def tractir_save_migrate_report_and_progress_runtime():
        import renpy.store as store

        owner_fields = (
            (next_day_runtime, "report_title", "NextDayReportTitle", ""),
            (next_day_runtime, "report_body", "NextDayReportBody", ""),
            (tractir_progress, "activated_achievements", "tractir_activated_achievements", set()),
            (tractir_progress, "achieved", "tractir_achieved", set()),
            (tractir_progress, "endings", "tractir_endings", set()),
            (tractir_progress, "view", "tractir_progress_view", "achievements"),
            (tractir_progress, "ending_title", "TractirEndingTitle", ""),
            (tractir_progress, "ending_body", "TractirEndingBody", ""),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_room_entry_runtime():
        import renpy.store as store

        owner_fields = (
            ("present_ids", "RoomEnterPresentIds", []),
            ("last_room", "RoomEnterLastRoom", ""),
            ("last_event_fired", "RoomEnterLastEventFired", False),
        )
        for field_name, legacy_name, default_value in owner_fields:
            if not hasattr(room_entry_runtime, field_name):
                setattr(room_entry_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_time_and_lifecycle_state():
        import renpy.store as store

        owner_fields = (
            (player.economy, "child_birth_benefit_notice", "KidBirthPosobie", ""),
            (player, "sleep_wake_hour_override", "SleepWakeHourOverride", -1),
            (player, "sleep_wake_minute_override", "SleepWakeMinuteOverride", 0),
            (calendar_v2, "time_advance_blocked", "BlockTimeAdvance", 0),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_room_owned_state()    def tractir_save_migrate_room_owned_state():
        import renpy.store as store

        room_fields = (
            (ShedRoom, "notice_text", "ShedNoticeText", ""),
            (ShedRoom, "notice_pending", "ShedNoticePending", False),
            (ShedRoom, "bucket_found", "ShedBucketFound", False),
            (TavernMyRoom, "attic_hatch_found", "TavernMyRoomAtticHatchFound", False),
        )
        for room_obj, field_name, legacy_name, default_value in room_fields:
            room_obj.state = dict(getattr(room_obj, "state", {}) or {})
            if field_name not in room_obj.state:
                room_obj.state[field_name] = getattr(store, legacy_name, default_value)
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_module_runtime()    def tractir_save_migrate_dress_shop():
        import renpy.store as store

        field_rows = (
            ("produced", "DressProduced", ""),
            ("buyer", "DressBuyer", ""),
            ("measure_stage", "IrmaMeasureShopStage", 0),
            ("sex_step", "IrmaSexShopStep", 0),
            ("girl_dress_block", "GirlDressBlock", 0),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(dress_shop, field_name):
                setattr(dress_shop, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        if not hasattr(player.appearance, "girl_dresses_bought"):
            player.appearance.girl_dresses_bought = int(getattr(store, "GirlDressesBought", 0) or 0)
        if hasattr(store, "GirlDressesBought"):
            delattr(store, "GirlDressesBought")

    def tractir_save_migrate_module_runtime():
        import renpy.store as store

        field_rows = (
            ("kind", "active_module_kind", ""),
            ("return_label", "active_module_return_label", ""),
            ("return_room", "active_module_return_room", ""),
            ("actor", "active_module_actor", ""),
            ("somebody_cums", "SomebodyCums", 0),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(module_runtime, field_name):
                setattr(module_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_relationship_scores()    def tractir_save_migrate_town_workers():
        import renpy.store as store

        if not hasattr(TownStreet, "blackworker_candidates"):
            TownStreet.blackworker_candidates = list(getattr(store, "TavernBlackworkerCandidates", []) or [])
        if not hasattr(TownStreet, "blackworkers"):
            TownStreet.blackworkers = list(getattr(store, "TavernBlackworkers", []) or [])
        for legacy_name in ("TavernBlackworkerCandidates", "TavernBlackworkers"):
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_story_event_runtime():
        import renpy.store as store

        field_rows = (
            ("active_event", "active_event", None),
            ("random_events", "random_events", []),
            ("story_events", "story_events", []),
            ("tavern_work_events", "tavern_work_events", []),
            ("available", "availEvents", {}),
            ("evaluation_time", "evalTime", None),
            ("locations", "eventLocations", set()),
            ("people", "eventPeople", set()),
            ("talk", "eventTalk", set()),
            ("options", "eventOptions", set()),
            ("items", "eventItems", set()),
            ("paths", "eventPath", set()),
            ("projection_rows", "eventProjectionRows", []),
            ("route_hints", "eventRouteHints", {}),
            ("thread_levels", "story_thread_levels", {}),
            ("fired_day", "StoryEventFiredDay", -1),
            ("fired_keys_today", "StoryEventFiredKeysToday", []),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(event_runtime, field_name):
                setattr(event_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_daily_events():
        import renpy.store as store

        legacy_rows = getattr(store, "DailyEventsList", None)
        if isinstance(legacy_rows, list) and len(daily_events.rows) == 0:
            daily_events.rows = list(legacy_rows)
        if hasattr(store, "DailyEventsList"):
            delattr(store, "DailyEventsList")

    def tractir_save_migrate_francheska_schedule():
        import renpy.store as store

        if not hasattr(Francheska, "busy_slots"):
            legacy_busy = getattr(store, "FranBusy", {})
            if isinstance(legacy_busy, list):
                legacy_busy = dict((index, value) for index, value in enumerate(legacy_busy))
            Francheska.busy_slots = dict(legacy_busy or {})
        for slot in range(8):
            Francheska.busy_slots.setdefault(slot, 0)
        if hasattr(store, "FranBusy"):
            delattr(store, "FranBusy")

    def tractir_save_migrate_girl_decisions():
        import renpy.store as store

        legacy_results = getattr(store, "GirlDecisionLast", None)
        if isinstance(legacy_results, dict):
            for composite_key, result in legacy_results.items():
                person, separator, action = str(composite_key or "").partition(":")
                info = getPersonInfo(person)
                if separator and info is not None:
                    info.var.setdefault("decision_results", {})[action] = dict(result or {})
        if hasattr(store, "GirlDecisionLast"):
            delattr(store, "GirlDecisionLast")

    def tractir_save_migrate_relationship_scores():
        import renpy.store as store

        legacy_scores = getattr(store, "RelationshipInteractionScore", None)
        if isinstance(legacy_scores, dict):
            for person, score in legacy_scores.items():
                row = relationship_state(person)
                if row:
                    row["interaction_score"] = max(int(row.get("interaction_score", 0) or 0), int(score or 0))
        if hasattr(store, "RelationshipInteractionScore"):
            delattr(store, "RelationshipInteractionScore")
        tractir_save_migrate_player_owned_scalars()    def tractir_save_migrate_player_owned_scalars():
        import renpy.store as store

        owner_fields = (
            (player.tavern_management, "visitors", "tavernvisitors", 40),
            (player.tavern_management, "slogan_state", "SloganFixed", 0),
            (player.tavern_management, "client_room_hole", "TavernHole", 0),
            (player.tavern_management, "glory_hole", "TavernGloryHole", 0),
            (player.tavern_management, "glory_hole_look", "GloryHoleLook", 0),
            (player.tavern_management, "dance_sponsor", "DanceSponsor", 0),
            (player.tavern_management, "household_members", "householdmembers", 4),
            (player.economy, "church_donated_amount", "ChurchDonatedAmount", 0),
            (player.intimacy, "ellona_blessed", "BlessedByEllona", 0),
            (player.intimacy, "ellona_cursed", "CursedByEllona", 0),
            (player.intimacy, "ellona_curse_days", "CursedByEllonaDays", 0),
            (player.intimacy, "ellona_curse_reduction", "CursedByEllonaReduce", 0),
            (player.tavern_management.breakfast, "today", "BreakfastToday", False),
            (player.tavern_management.breakfast, "last_day", "TavernBreakfastLastDay", -1),
            (player.tavern_management.breakfast, "day", "TavernBreakfastDay", -1),
            (player.tavern_management.breakfast, "base_text", "TavernBreakfastBaseText", ""),
            (player.tavern_management.breakfast, "soap_announced_day", "TavernBreakfastSoapAnnouncedDay", -1),
            (player.tavern_management.breakfast, "barber_talk_day", "TavernBreakfastBarberTalkDay", -1),
            (player.tavern_management.breakfast, "listen_day", "TavernBreakfastListenDay", -1),
            (player.tavern_management.breakfast, "market_talk_day", "TavernBreakfastMarketTalkDay", -1),
            (player.tavern_management.breakfast, "motivation_day", "TavernBreakfastMotivationDay", -1),
            (player.tavern_management.breakfast, "absent_talk_day", "TavernBreakfastAbsentTalkDay", -1),
            (player.tavern_management.breakfast, "base_shown_day", "TavernBreakfastBaseShownDay", -1),
            (player.tavern_management.breakfast, "event_active", "TavernBreakfastEventActive", False),
            (player.tavern_management.breakfast, "sunday_dinner_last_day", "TavernSundayDinnerLastDay", -1),
            (player.tavern_management.breakfast, "sunday_dinner_barber_talk_day", "TavernSundayDinnerBarberTalkDay", -1),
            (player.tavern_management.breakfast, "spicy_drink_day", "TavernBreakfastSpicyDrinkDay", -1),
            (player.tavern_management.breakfast, "sunday_dinner_spicy_drink_day", "TavernSundayDinnerSpicyDrinkDay", -1),
            (player.tavern_management.breakfast, "georgett_liza_pending", "TavernBreakfastGeorgetteLizaPending", 0),
            (player.tavern_management.breakfast, "present_ids", "TavernBreakfastPresentIds", None),
            (player.tavern_management.breakfast, "melissa_amanda_gerhard_day", "TavernBreakfastMelissaAmandaGerhardDay", -1),
            (player.tavern_management.breakfast, "food_perk_day", "TavernBreakfastFoodPerkDay", -1),
            (player.tavern_management.breakfast, "drink_perk_day", "TavernBreakfastDrinkPerkDay", -1),
            (player.tavern_management.breakfast, "lewd_series_day", "TavernBreakfastLewdSeriesDay", -1),
            (player.tavern_management.breakfast, "appearance_perk_day", "TavernBreakfastAppearancePerkDay", -1),
            (player.tavern_management.breakfast, "sweet_perk_day", "TavernBreakfastSweetPerkDay", -1),
            (player.tavern_management.breakfast, "blind_pirate_team_pledge", "TavernBreakfastBlindPirateTeamPledge", 0),
            (player.tavern_management.breakfast, "milk_team_talk_done", "TavernBreakfastMilkTeamTalkDone", 0),
            (player.tavern_management.breakfast, "ale_team_talk_done", "TavernBreakfastAleTeamTalkDone", 0),
            (player.tavern_management.breakfast, "dance_sponsor_announced_day", "TavernBreakfastDanceSponsorAnnouncedDay", -1),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        if not hasattr(player.intimacy, "ellona_grace_blessings"):
            player.intimacy.ellona_grace_blessings = list(getattr(store, "GraceBlessing", [0, 0, 0, 0, 0, 0]) or [])
        if hasattr(store, "GraceBlessing"):
            delattr(store, "GraceBlessing")
            (player.tavern_management.breakfast, "text_pages", "TavernBreakfastTextPages", []),
            (player.tavern_management.breakfast, "text_page_index", "TavernBreakfastTextPageIndex", 0),
            (player.tavern_management.breakfast, "text_return_label", "TavernBreakfastTextReturnLabel", ""),        tractir_save_migrate_paged_panel_runtime()    def tractir_save_migrate_paged_panel_runtime():
        import renpy.store as store

        legacy_pages = list(getattr(store, "panel_paged_pages", []) or getattr(store, "tavern_event_pages", []) or [])
        if legacy_pages and not list(paged_panel.pages or []):
            paged_panel.pages = legacy_pages
        paged_panel.page_index = int(getattr(store, "panel_paged_page_index", getattr(store, "tavern_event_page_index", paged_panel.page_index)) or 0)
        paged_panel.next_title = str(getattr(store, "panel_paged_next_title", getattr(store, "tavern_event_next_title", paged_panel.next_title)) or "")
        paged_panel.next_items = list(getattr(store, "panel_paged_next_items", getattr(store, "tavern_event_next_items", paged_panel.next_items)) or [])
        paged_panel.style = str(getattr(store, "panel_paged_style", paged_panel.style) or "plain")
        paged_panel.raw_text = str(getattr(store, "panel_paged_raw_text", paged_panel.raw_text) or "")
        paged_panel.tavern_event_raw_text = str(getattr(store, "tavern_event_panel_raw_text", paged_panel.tavern_event_raw_text) or "")

        pending_text = str(getattr(store, "panel_paged_pending_text", "") or "")
        if pending_text and not list(paged_panel.pages or []):
            paged_panel.pages = build_tavern_event_pages(pending_text)
            paged_panel.page_index = 0
            paged_panel.next_title = str(getattr(store, "panel_paged_pending_title", "") or "")
            paged_panel.next_items = list(getattr(store, "panel_paged_pending_items", []) or [])
            paged_panel.style = str(getattr(store, "panel_paged_pending_style", "plain") or "plain")

        for legacy_name in (
            "tavern_event_panel_raw_text", "tavern_event_pages", "tavern_event_page_index",
            "tavern_event_next_title", "tavern_event_next_items", "panel_paged_raw_text",
            "panel_paged_pages", "panel_paged_page_index", "panel_paged_next_title",
            "panel_paged_next_items", "panel_paged_style", "panel_paged_pending_text",
            "panel_paged_pending_title", "panel_paged_pending_items", "panel_paged_pending_style",
        ):
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_domain_singletons()    def tractir_save_migrate_combat_singletons():
        import renpy.store as store

        for owner, legacy_name in ((fight, "Fight"), (hunt, "Hunt")):
            legacy_owner = getattr(store, legacy_name, None)
            if legacy_owner is not None and hasattr(legacy_owner, "__dict__"):
                owner.__dict__.update(dict(legacy_owner.__dict__ or {}))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_domain_singletons():
        import renpy.store as store

        singleton_rows = (
            (recipe_book, "RecipeBook"),
            (crafting, "Crafting"),
            (household, "Household"),
        )
        for owner, legacy_name in singleton_rows:
            legacy_owner = getattr(store, legacy_name, None)
            if legacy_owner is not None and hasattr(legacy_owner, "__dict__"):
                owner.__dict__.update(dict(legacy_owner.__dict__ or {}))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_time_and_lifecycle_state()    def tractir_save_migrate_report_and_progress_runtime():
        import renpy.store as store

        owner_fields = (
            (next_day_runtime, "report_title", "NextDayReportTitle", ""),
            (next_day_runtime, "report_body", "NextDayReportBody", ""),
            (tractir_progress, "activated_achievements", "tractir_activated_achievements", set()),
            (tractir_progress, "achieved", "tractir_achieved", set()),
            (tractir_progress, "endings", "tractir_endings", set()),
            (tractir_progress, "view", "tractir_progress_view", "achievements"),
            (tractir_progress, "ending_title", "TractirEndingTitle", ""),
            (tractir_progress, "ending_body", "TractirEndingBody", ""),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_room_entry_runtime():
        import renpy.store as store

        owner_fields = (
            ("present_ids", "RoomEnterPresentIds", []),
            ("last_room", "RoomEnterLastRoom", ""),
            ("last_event_fired", "RoomEnterLastEventFired", False),
        )
        for field_name, legacy_name, default_value in owner_fields:
            if not hasattr(room_entry_runtime, field_name):
                setattr(room_entry_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_time_and_lifecycle_state():
        import renpy.store as store

        owner_fields = (
            (player.economy, "child_birth_benefit_notice", "KidBirthPosobie", ""),
            (player, "sleep_wake_hour_override", "SleepWakeHourOverride", -1),
            (player, "sleep_wake_minute_override", "SleepWakeMinuteOverride", 0),
            (calendar_v2, "time_advance_blocked", "BlockTimeAdvance", 0),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_room_owned_state()    def tractir_save_migrate_room_owned_state():
        import renpy.store as store

        room_fields = (
            (ShedRoom, "notice_text", "ShedNoticeText", ""),
            (ShedRoom, "notice_pending", "ShedNoticePending", False),
            (ShedRoom, "bucket_found", "ShedBucketFound", False),
            (TavernMyRoom, "attic_hatch_found", "TavernMyRoomAtticHatchFound", False),
        )
        for room_obj, field_name, legacy_name, default_value in room_fields:
            room_obj.state = dict(getattr(room_obj, "state", {}) or {})
            if field_name not in room_obj.state:
                room_obj.state[field_name] = getattr(store, legacy_name, default_value)
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_module_runtime()    def tractir_save_migrate_dress_shop():
        import renpy.store as store

        field_rows = (
            ("produced", "DressProduced", ""),
            ("buyer", "DressBuyer", ""),
            ("measure_stage", "IrmaMeasureShopStage", 0),
            ("sex_step", "IrmaSexShopStep", 0),
            ("girl_dress_block", "GirlDressBlock", 0),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(dress_shop, field_name):
                setattr(dress_shop, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        if not hasattr(player.appearance, "girl_dresses_bought"):
            player.appearance.girl_dresses_bought = int(getattr(store, "GirlDressesBought", 0) or 0)
        if hasattr(store, "GirlDressesBought"):
            delattr(store, "GirlDressesBought")

    def tractir_save_migrate_module_runtime():
        import renpy.store as store

        field_rows = (
            ("kind", "active_module_kind", ""),
            ("return_label", "active_module_return_label", ""),
            ("return_room", "active_module_return_room", ""),
            ("actor", "active_module_actor", ""),
            ("somebody_cums", "SomebodyCums", 0),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(module_runtime, field_name):
                setattr(module_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        tractir_save_migrate_relationship_scores()    def tractir_save_migrate_town_workers():
        import renpy.store as store

        if not hasattr(TownStreet, "blackworker_candidates"):
            TownStreet.blackworker_candidates = list(getattr(store, "TavernBlackworkerCandidates", []) or [])
        if not hasattr(TownStreet, "blackworkers"):
            TownStreet.blackworkers = list(getattr(store, "TavernBlackworkers", []) or [])
        for legacy_name in ("TavernBlackworkerCandidates", "TavernBlackworkers"):
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_story_event_runtime():
        import renpy.store as store

        field_rows = (
            ("active_event", "active_event", None),
            ("random_events", "random_events", []),
            ("story_events", "story_events", []),
            ("tavern_work_events", "tavern_work_events", []),
            ("available", "availEvents", {}),
            ("evaluation_time", "evalTime", None),
            ("locations", "eventLocations", set()),
            ("people", "eventPeople", set()),
            ("talk", "eventTalk", set()),
            ("options", "eventOptions", set()),
            ("items", "eventItems", set()),
            ("paths", "eventPath", set()),
            ("projection_rows", "eventProjectionRows", []),
            ("route_hints", "eventRouteHints", {}),
            ("thread_levels", "story_thread_levels", {}),
            ("fired_day", "StoryEventFiredDay", -1),
            ("fired_keys_today", "StoryEventFiredKeysToday", []),
        )
        for field_name, legacy_name, default_value in field_rows:
            if not hasattr(event_runtime, field_name):
                setattr(event_runtime, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)

    def tractir_save_migrate_daily_events():
        import renpy.store as store

        legacy_rows = getattr(store, "DailyEventsList", None)
        if isinstance(legacy_rows, list) and len(daily_events.rows) == 0:
            daily_events.rows = list(legacy_rows)
        if hasattr(store, "DailyEventsList"):
            delattr(store, "DailyEventsList")

    def tractir_save_migrate_francheska_schedule():
        import renpy.store as store

        if not hasattr(Francheska, "busy_slots"):
            legacy_busy = getattr(store, "FranBusy", {})
            if isinstance(legacy_busy, list):
                legacy_busy = dict((index, value) for index, value in enumerate(legacy_busy))
            Francheska.busy_slots = dict(legacy_busy or {})
        for slot in range(8):
            Francheska.busy_slots.setdefault(slot, 0)
        if hasattr(store, "FranBusy"):
            delattr(store, "FranBusy")

    def tractir_save_migrate_girl_decisions():
        import renpy.store as store

        legacy_results = getattr(store, "GirlDecisionLast", None)
        if isinstance(legacy_results, dict):
            for composite_key, result in legacy_results.items():
                person, separator, action = str(composite_key or "").partition(":")
                info = getPersonInfo(person)
                if separator and info is not None:
                    info.var.setdefault("decision_results", {})[action] = dict(result or {})
        if hasattr(store, "GirlDecisionLast"):
            delattr(store, "GirlDecisionLast")

    def tractir_save_migrate_relationship_scores():
        import renpy.store as store

        legacy_scores = getattr(store, "RelationshipInteractionScore", None)
        if isinstance(legacy_scores, dict):
            for person, score in legacy_scores.items():
                row = relationship_state(person)
                if row:
                    row["interaction_score"] = max(int(row.get("interaction_score", 0) or 0), int(score or 0))
        if hasattr(store, "RelationshipInteractionScore"):
            delattr(store, "RelationshipInteractionScore")
        tractir_save_migrate_player_owned_scalars()    def tractir_save_migrate_player_owned_scalars():
        import renpy.store as store

        owner_fields = (
            (player.tavern_management, "visitors", "tavernvisitors", 40),
            (player.tavern_management, "slogan_state", "SloganFixed", 0),
            (player.tavern_management, "client_room_hole", "TavernHole", 0),
            (player.tavern_management, "glory_hole", "TavernGloryHole", 0),
            (player.tavern_management, "glory_hole_look", "GloryHoleLook", 0),
            (player.tavern_management, "dance_sponsor", "DanceSponsor", 0),
            (player.tavern_management, "household_members", "householdmembers", 4),
            (player.economy, "church_donated_amount", "ChurchDonatedAmount", 0),
            (player.intimacy, "ellona_blessed", "BlessedByEllona", 0),
            (player.intimacy, "ellona_cursed", "CursedByEllona", 0),
            (player.intimacy, "ellona_curse_days", "CursedByEllonaDays", 0),
            (player.intimacy, "ellona_curse_reduction", "CursedByEllonaReduce", 0),
            (player.tavern_management.breakfast, "today", "BreakfastToday", False),
            (player.tavern_management.breakfast, "last_day", "TavernBreakfastLastDay", -1),
            (player.tavern_management.breakfast, "day", "TavernBreakfastDay", -1),
            (player.tavern_management.breakfast, "base_text", "TavernBreakfastBaseText", ""),
            (player.tavern_management.breakfast, "soap_announced_day", "TavernBreakfastSoapAnnouncedDay", -1),
            (player.tavern_management.breakfast, "barber_talk_day", "TavernBreakfastBarberTalkDay", -1),
            (player.tavern_management.breakfast, "listen_day", "TavernBreakfastListenDay", -1),
            (player.tavern_management.breakfast, "market_talk_day", "TavernBreakfastMarketTalkDay", -1),
            (player.tavern_management.breakfast, "motivation_day", "TavernBreakfastMotivationDay", -1),
            (player.tavern_management.breakfast, "absent_talk_day", "TavernBreakfastAbsentTalkDay", -1),
            (player.tavern_management.breakfast, "base_shown_day", "TavernBreakfastBaseShownDay", -1),
            (player.tavern_management.breakfast, "event_active", "TavernBreakfastEventActive", False),
            (player.tavern_management.breakfast, "sunday_dinner_last_day", "TavernSundayDinnerLastDay", -1),
            (player.tavern_management.breakfast, "sunday_dinner_barber_talk_day", "TavernSundayDinnerBarberTalkDay", -1),
            (player.tavern_management.breakfast, "spicy_drink_day", "TavernBreakfastSpicyDrinkDay", -1),
            (player.tavern_management.breakfast, "sunday_dinner_spicy_drink_day", "TavernSundayDinnerSpicyDrinkDay", -1),
            (player.tavern_management.breakfast, "georgett_liza_pending", "TavernBreakfastGeorgetteLizaPending", 0),
            (player.tavern_management.breakfast, "present_ids", "TavernBreakfastPresentIds", None),
            (player.tavern_management.breakfast, "melissa_amanda_gerhard_day", "TavernBreakfastMelissaAmandaGerhardDay", -1),
            (player.tavern_management.breakfast, "food_perk_day", "TavernBreakfastFoodPerkDay", -1),
            (player.tavern_management.breakfast, "drink_perk_day", "TavernBreakfastDrinkPerkDay", -1),
            (player.tavern_management.breakfast, "lewd_series_day", "TavernBreakfastLewdSeriesDay", -1),
            (player.tavern_management.breakfast, "appearance_perk_day", "TavernBreakfastAppearancePerkDay", -1),
            (player.tavern_management.breakfast, "sweet_perk_day", "TavernBreakfastSweetPerkDay", -1),
            (player.tavern_management.breakfast, "blind_pirate_team_pledge", "TavernBreakfastBlindPirateTeamPledge", 0),
            (player.tavern_management.breakfast, "milk_team_talk_done", "TavernBreakfastMilkTeamTalkDone", 0),
            (player.tavern_management.breakfast, "ale_team_talk_done", "TavernBreakfastAleTeamTalkDone", 0),
            (player.tavern_management.breakfast, "dance_sponsor_announced_day", "TavernBreakfastDanceSponsorAnnouncedDay", -1),
        )
        for owner, field_name, legacy_name, default_value in owner_fields:
            if not hasattr(owner, field_name):
                setattr(owner, field_name, getattr(store, legacy_name, default_value))
            if hasattr(store, legacy_name):
                delattr(store, legacy_name)
        if not hasattr(player.intimacy, "ellona_grace_blessings"):
            player.intimacy.ellona_grace_blessings = list(getattr(store, "GraceBlessing", [0, 0, 0, 0, 0, 0]) or [])
        if hasattr(store, "GraceBlessing"):
            delattr(store, "GraceBlessing")
default saveVersion = 1
define currentVersion = 3

init -100 python:
    def beforeLoadTractirSave():
        ensure_game_item_registry()

    def tractir_save_patch_loaded_state():
        ensure_game_item_registry()
        tractir_save_normalize_rooms()
        tractir_save_remove_owned_unique_items_from_rooms()
        tractir_save_clear_room_ui_cache()

    def tractir_save_normalize_rooms():
        for room_obj in list(roomRegistry.values()):
            if room_obj is None or not hasattr(room_obj, "game_items"):
                continue
            room_obj.game_items = normalize_room_item_rows(getattr(room_obj, "game_items", []))
            room_obj.objects = room_obj.game_items

    def tractir_save_remove_owned_unique_items_from_rooms():
        inventory = _ensure_player_inventory_store()
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

        for room_obj in list(roomRegistry.values()):
            if room_obj is None or not hasattr(room_obj, "game_items"):
                continue
            next_rows = [row for row in normalize_room_item_rows(getattr(room_obj, "game_items", [])) if get_object_id(row) not in owned_unique]
            room_obj.game_items = list(next_rows)
            room_obj.objects = room_obj.game_items

    def tractir_save_clear_room_ui_cache():
        global CurrentRoom, current_action_title, current_action_content, current_action_items
        global current_object_id, main_ui_inventory_dropdown_open, main_ui_overlay
        global current_girl_key, UI_selected_char, UI_mode

        UI_mode = "scene"
        current_action_content = None
        current_action_items = []
        current_object_id = ""
        main_ui_inventory_dropdown_open = False
        main_ui_overlay = ""
        current_girl_key = ""
        UI_selected_char = ""

        room_code = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if room_code == "":
            return

        room_obj = get_registered_room(room_code)
        if room_obj is not None:
            CurrentRoom = room_obj
            current_action_title = str(getattr(CurrentRoom, "display_name", "") or room_code)

    def tractir_save_promote_werecat():
        saved_info = peopleInfo.get("werecat", None)
        if saved_info is not None and saved_info is not werecat:
            saved_var = getattr(saved_info, "var", getattr(saved_info, "state", {}))
            saved_stats = getattr(saved_info, "stats", {})
            if isinstance(saved_var, dict):
                werecat.var.update(saved_var)
            if isinstance(saved_stats, dict):
                werecat.stats.update(saved_stats)
        werecat.name = "werecat"
        werecat.data = WerecatStaticData
        peopleData["werecat"] = WerecatStaticData
        peopleInfo["werecat"] = werecat
        if werecat not in secondary_npcs:
            secondary_npcs.append(werecat)

    def updateSave():
        global saveVersion
        tractir_save_promote_werecat()

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

        tractir_save_patch_loaded_state()
        saveVersion = int(currentVersion or loaded_version)

    def updateSave_V1():
        tractir_save_patch_loaded_state()

    def updateSave_V2():
        tractir_save_patch_loaded_state()

    def updateSave_V4():
        werecat_state_obj = globals().get("werecat")
        state = getattr(werecat_state_obj, "var", None)
        if not isinstance(state, dict):
            return
        if int(state.get("adopted", 0) or 0) == 1:
            state["adopted_count"] = max(1, int(state.get("adopted_count", 0) or 0))

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
            ("wearing_bloomers", False),
        ):
            if not hasattr(dog_obj, field_name):
                setattr(dog_obj, field_name, default_value)
        dog_obj.name = "dog"
        dog_obj.data = DogStaticData
        peopleData["dog"] = DogStaticData
        peopleInfo["dog"] = dog_obj
        if dog_obj not in secondary_npcs:
            secondary_npcs.append(dog_obj)

        if not isinstance(getattr(player.combat, "special_supply", None), dict):
            player.combat.special_supply = {}
        player.combat.special_supply.setdefault("bees_bomb", 0)
        if not isinstance(getattr(fight, "enemy_state", None), dict):
            fight.enemy_state = {}
        if not isinstance(getattr(hunt, "last_result", None), dict):
            hunt.last_result = {}
        if not isinstance(getattr(fight, "side_log", None), list):
            fight.side_log = []
        if not isinstance(getattr(fight, "enemy_party", None), list):
            fight.enemy_party = []
        if not isinstance(getattr(fight, "status_state", None), dict):
            fight.status_state = {}
        player.set_stat("health", _player_clamp_stat(player.condition.health, 0, 100))


label before_load:
    $ beforeLoadTractirSave()
    return


label after_load:
    $ updateSave()
    $ renpy.block_rollback()
    return
