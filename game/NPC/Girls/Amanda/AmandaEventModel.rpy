# Amanda-specific story event records.
# Event fields own time, probability, binding, and priority.  Each subclass owns
# only the Amanda-specific facts that remain after those common checks.

init -24 python:
    class AmandaEvent(Event):
        def __init__(
            self,
            code_name,
            target,
            day,
            hour,
            probability,
            location,
            action,
            priority,
            daily_key="",
            source_refs=None,
            event_day=None,
        ):
            super(AmandaEvent, self).__init__(
                (
                    target,
                    day,
                    hour,
                    event_day,
                    probability,
                    None,
                    None,
                    None,
                    location,
                    action,
                    priority,
                    False,
                ),
                "",
                False,
            )
            self.code_name = str(code_name or target or "")
            self.daily_key = str(daily_key or "amanda:%s" % self.code_name)
            self.source_refs = list(source_refs or [])

        def checkConditions(self):
            return bool(super(AmandaEvent, self).checkConditions() and self.checkAmandaConditions())

        def checkAmandaConditions(self):
            return True


    class AmandaTavernSeductionEvent(AmandaEvent):
        def __init__(self):
            super(AmandaTavernSeductionEvent, self).__init__(
                "tavern_seduction",
                "story_amanda_tavern_seduction_0",
                (1, 2, 3, 4, 6),
                (12, 21),
                0.35,
                "TavernMain",
                "enter",
                210,
                source_refs=["AmandaLegareStreetEvents.txt"],
            )

        def checkAmandaConditions(self):
            return (
                str(people.location("amanda") or "") == "TavernMain"
                and int(Amanda.rel or 0) >= 8
                and int(Amanda.corruption or 0) >= 25
                and not Amanda.room_entry_blocked_today
            )


    class AmandaRoomNightApproachEvent(AmandaEvent):
        def __init__(self):
            super(AmandaRoomNightApproachEvent, self).__init__(
                "room_night_approach",
                "story_amanda_room_grope_0",
                None,
                (18, 23),
                1,
                "TavernAmandaRoom",
                "amanda_grope",
                30,
                source_refs=["TavernAmandaRoom.txt"],
            )

        def checkAmandaConditions(self):
            return (
                str(people.location("amanda") or "") == "TavernAmandaRoom"
                and not people.is_awake("amanda")
                and player.intimacy.can_cum()
            )

    class AmandaGloryHoleTryEvent(AmandaEvent):
        def __init__(self):
            super(AmandaGloryHoleTryEvent, self).__init__(
                "gloryhole_try",
                "story_amanda_gloryhole_try_0",
                None,
                (12, 21),
                1,
                "TavernGloryHole",
                "check_glory_hole",
                40,
                source_refs=["AmandaAtGloryHole.txt"],
            )

        def checkAmandaConditions(self):
            session = player.tavern_management.glory_hole_session
            return (
                Amanda.var_int("glory_cur_state", 0) >= 1
                and session.amanda_present == 1
                and session.works == 1
                and session.girl_name == "liza"
                and session.menu_blocked == 1
            )


    class AmandaMorningWindowEpisodeEvent(AmandaEvent):
        def __init__(self):
            super(AmandaMorningWindowEpisodeEvent, self).__init__(
                "morning_window_episode",
                "story_amanda_room_morning_window_0",
                None,
                (6, 7),
                1,
                "TavernAmandaRoom",
                "enter",
                25,
                source_refs=["TavernAmandaRoom.rpy"],
            )

        def checkAmandaConditions(self):
            return (
                Amanda.attic_busted()
                and str(household_morning_issue_type("amanda") or "") == "sleepy"
            )


    class AmandaNightBowlWindowEvent(AmandaEvent):
        def __init__(self):
            super(AmandaNightBowlWindowEvent, self).__init__(
                "night_bowl_window",
                "story_amanda_night_bowl_window_0",
                None,
                (18, 5),
                1,
                "TavernMyRoom",
                "window_look",
                25,
                source_refs=["TavernMyRoomWindow001.rpy", "SoapCraftAndAtticItems.rpy"],
            )

        def checkAmandaConditions(self):
            return (
                Amanda.has_given_night_bowl()
                and player.item_count("night_bowl_001") > 0
                and (
                    not Amanda.fancy_night_bowl_received
                    or Amanda.backyard_relief_preference == 1
                )
            )


    class AmandaKitchenWindowFavorEvent(AmandaEvent):
        def __init__(self):
            super(AmandaKitchenWindowFavorEvent, self).__init__(
                "kitchen_window_favor",
                "story_amanda_kitchen_window_favor_0",
                None,
                None,
                1,
                "TavernKitchen",
                "enter",
                -20,
                source_refs=["TavernAmandaRoom.rpy", "TavernKitchen.rpy"],
            )

        def checkAmandaConditions(self):
            return (
                int(Amanda.attic_window_favor_stage or 0) in (1, 2)
                and not bool(player.tavern_management.breakfast.event_active)
            )


    class AmandaBirthEvent(AmandaEvent):
        def __init__(self):
            super(AmandaBirthEvent, self).__init__(
                "birth", "story_amanda_give_birth_0", None, None, 1, "TavernMain", "enter", 7,
                source_refs=["GiveBirth.txt"],
            )

        def checkAmandaConditions(self):
            return bool(Amanda.birth_ready())


    class AmandaLegareTavernVisitEvent(AmandaEvent):
        def __init__(self):
            super(AmandaLegareTavernVisitEvent, self).__init__(
                "legare_tavern_visit",
                "story_amanda_legare_tavern_visit_0",
                (1, 2, 3, 4, 6),
                (18, 21),
                0.5,
                "TavernMain",
                "enter",
                205,
                source_refs=["AmandaLegareStreetEvents.txt"],
            )

        def checkAmandaConditions(self):
            return (
                str(people.location("amanda") or "") == "TavernMain"
                and str(people.location("alber") or "") == "TavernMain"
                and Amanda.legare_affection >= 5
                and not Amanda.legare_forbidden
            )


    class AmandaStreetLegareSightingEvent(AmandaEvent):
        def __init__(self, location):
            super(AmandaStreetLegareSightingEvent, self).__init__(
                "street_legare_sighting",
                "story_amanda_street_legare_sighting_0",
                (1, 2, 3, 4, 6),
                (12, 21),
                0.25,
                location,
                "enter",
                650,
                source_refs=["AmandaLegareStreetEvents.txt"],
            )

        def checkAmandaConditions(self):
            return (
                str(rooms.current_code or "") in ("StreetTavern", "MarketPlace")
                and CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun") > 0
            )


    class AmandaStreetLoverEncounterEvent(AmandaEvent):
        def __init__(self, location):
            super(AmandaStreetLoverEncounterEvent, self).__init__(
                "street_lover_encounter",
                "story_amanda_street_lover_encounter_0",
                (1, 2, 3, 4, 6),
                (12, 21),
                0.2,
                location,
                "enter",
                660,
                source_refs=["AmandaLoverSex.txt"],
            )

        def checkAmandaConditions(self):
            discipline = threads.get("amandaStreetDiscipline", None)
            discipline_pending = bool(
                discipline is not None
                and bool(getattr(discipline, "metconds", False))
                and not bool(getattr(discipline, "aborted", False))
                and not bool(getattr(discipline, "completed", False))
            )
            return (
                not discipline_pending
                and str(rooms.current_code or "") in ("StreetTavern", "MarketPlace")
                and CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "lovermeet") > 0
            )


    class AmandaStreetLoverBreakfastEvent(AmandaEvent):
        def __init__(self, code_name, target, priority=0):
            super(AmandaStreetLoverBreakfastEvent, self).__init__(
                code_name,
                target,
                None,
                (6, 11),
                1,
                "TavernKitchen",
                "enter",
                priority,
                event_day=1,
            )

        def checkAmandaConditions(self):
            present_ids = list(tavern_breakfast_present_ids() or [])
            return (
                tavern_breakfast_available()
                and "amanda" in present_ids
                and "sandra" in present_ids
            )


    AmandaTavernSeduction = AmandaTavernSeductionEvent()
    AmandaRoomNightApproach = AmandaRoomNightApproachEvent()
    AmandaGloryHoleTry = AmandaGloryHoleTryEvent()
    AmandaMorningWindowEpisode = AmandaMorningWindowEpisodeEvent()
    AmandaNightBowlWindow = AmandaNightBowlWindowEvent()
    AmandaKitchenWindowFavor = AmandaKitchenWindowFavorEvent()
    AmandaBirth = AmandaBirthEvent()
    AmandaLegareTavernVisit = AmandaLegareTavernVisitEvent()
    AmandaStreetLegareSightingStreet = AmandaStreetLegareSightingEvent("StreetTavern")
    AmandaStreetLegareSightingMarket = AmandaStreetLegareSightingEvent("MarketPlace")
    AmandaStreetLoverEncounterStreet = AmandaStreetLoverEncounterEvent("StreetTavern")
    AmandaStreetLoverEncounterMarket = AmandaStreetLoverEncounterEvent("MarketPlace")
    AmandaStreetPunishmentBreakfast = AmandaStreetLoverBreakfastEvent(
        "street_punishment_breakfast",
        "story_amanda_street_punishment_breakfast_1",
        priority=-30,
    )
    AmandaStreetLegareWarningBreakfast = AmandaStreetLoverBreakfastEvent(
        "street_legare_warning_breakfast",
        "story_amanda_street_legare_warning_breakfast_2",
        priority=-29,
    )
