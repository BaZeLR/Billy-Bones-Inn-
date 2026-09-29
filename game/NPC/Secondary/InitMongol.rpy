init python:
    class MongolData(PeopleData):
        code_name = "mongol"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Монгол",
                fullname="Монгол",
                genitive="Монгола",
                dative="Монголу",
                default_location="",
                description="Монгол - торговец лошадьми на рынке.",
                birth_date={"day": 1, "period": 1, "cycle": 1061},
                portrait="images/mongol/portrait1.jpg",
            )

    def mongol_tavern_stable_active():
        return bool(getattr(Mongol, "tavern_servant", False)) and "mongol" not in player.combat.party

    def mongol_hunting_party_active():
        return bool(getattr(Mongol, "tavern_servant", False)) and "mongol" in player.combat.party

    def mongol_schedule_entries():
        return [
            NPCScheduleEntry(location="Forest", weekdays=[1, 2, 3, 4, 5, 6, 7], start_hour=6, end_hour=23, awake=True, talkable=True, condition=mongol_hunting_party_active, priority=250, label="mongol_hunting_party"),
            NPCScheduleEntry(location="TavernStable", weekdays=[1, 2, 3, 4, 5, 6, 7], start_hour=6, end_hour=23, awake=True, talkable=True, condition=mongol_tavern_stable_active, priority=240, label="mongol_tavern_stableman"),
            NPCScheduleEntry(location="MarketPlace", weekdays=[1, 2, 3, 4, 5, 6], start_hour=6, end_hour=19, awake=True, talkable=True, condition=marketplace_mongol_visible, priority=100, label="market_horse_trade"),
        ]

    class MongolInfo(BaseNPC):
        """Mongol: horse trader, stocks prisoner, and Clara merchant hooks."""
        talk_label = "MarketPlaceTalkMongol"
        unknown_name = "Мужик в красной рубахе"

        def __init__(self, name="mongol", **kwargs):
            super().__init__(name, **kwargs)
            self.data = MongolStaticData
            self.known = False
            self.stocks_food_day = -1
            self.stocks_arrest_day = -1
            self.stocks_fate = ""
            self.guard_captain_known = False
            self.market_roll_day = -1
            self.market_roll = False
            self.asked_about_gypsy = False
            self.asked_price_increase = False
            self.zimmer_knows_horse_theft = False
            self.horse_price = 1000
            self.discount_asked = False
            self.theft_asked = False
            self.asked_about_seen_stolen = False
            self.seen_with_stolen_horse = False
            self.horses_bought = 0
            self.arrival_due_day = -1
            self.tavern_servant = False
            self.arrival_day = -1
            self.last_service_day = -1
            self.last_service_report = ""

        def update(self):
            self.name = people_normalize_id(self.name)
            self.data = MongolStaticData
            return self

        def perform_tavern_service(self):
            day = current_game_day()
            if not bool(getattr(self, "tavern_servant", False)) or int(getattr(self, "last_service_day", -1)) == day:
                return ""

            shed = rooms.get("Shed")
            report = []
            if _room_item_count_by_id(shed, "lumber_001") > 0:
                _room_remove_item_by_id(shed, "lumber_001")
                _room_add_item_units(shed, "chopped_wood_001", 10)
                report.append("расколол бревно на десять охапок дров")
            else:
                report.append("брёвен для колки пока нет")

            ash_count = 0
            for hearth in (TavernMainFireplaceObject, TavernKitchenHearthObject, TavernGuestRoomStoveObject, ShedHotWaterStoveObject):
                if _object_state_int(hearth, "ash_dirty", 0) > 0:
                    _set_object_state_int(hearth, "ash_dirty", 0)
                    ash_count += 1
            if ash_count:
                player.tavern_management.ashes_dirty_days = 0
                report.append("вычистил золу из %s печей" % ash_count)

            if tavern.renovation_complete("shed"):
                if _room_item_count_by_id(shed, "chopped_wood_001") > 0:
                    _room_remove_item_by_id(shed, "chopped_wood_001")
                    next_morning = (day + 1) * 1440 + 6 * 60
                    _set_object_state_int(ShedHotWaterStoveObject, "fire_started_minute", next_morning)
                    _set_object_state_int(ShedHotWaterStoveObject, "fire_until_minute", next_morning + 12 * 60)
                    _set_object_state_int(ShedHotWaterStoveObject, "hot_water_until_minute", (day + 2) * 1440)
                    _set_object_state_int(ShedHotWaterStoveObject, "boiledWaterToday", 1)
                    report.append("подготовил горячую воду в купальне на завтра")
                else:
                    report.append("купальня готова, но для горячей воды нужны колотые дрова")

            report.append("почистил лошадей и проверил карету")
            household.meta["convergence"] = min(1.0, float(household.meta.get("convergence", 0.0) or 0.0) + 0.01)
            for resident_id in household.resident_ids():
                resident = people.get_info(resident_id)
                if isinstance(resident, Girl):
                    behavior = household_ai_npc_state(resident_id)
                    behavior["obedience"] = min(1.0, float(behavior.get("obedience", 0.0) or 0.0) + 0.005)
                    if day % 7 == 0:
                        resident.reward_need_fulfilled(1, "mongol_household_help")
            self.last_service_day = day
            self.last_service_report = "Монгол докладывает: «%s»." % "; ".join(report)
            return "{b}%s{/b}\n" % self.last_service_report

        def reset_market_trade(self):
            self.horse_price = 1100 if self.zimmer_knows_horse_theft else 1000
            self.discount_asked = False
            return self.horse_price

        def prepare_market_roll(self, reroll=False):
            current_day = current_game_day()
            if bool(reroll) or self.market_roll_day != current_day:
                self.market_roll_day = current_day
                self.market_roll = procedural_randint(1, 4, "mongol_market_%s_%s" % (current_day, int(calendar_v2.clock_minutes() or 0))) == 1
            return self.market_roll

        def is_market_visible(self):
            if bool(getattr(self, "tavern_servant", False)):
                return False
            if str(self.stocks_fate or "") in ("released", "convicted"):
                return False
            if player.horse.owns_horse():
                return False
            if not rooms.get("MarketPlace").is_open():
                return False
            return self.prepare_market_roll() == 1

        def interaction_visible(self, room_code=""):
            if str(room_code or "").strip() == "MarketPlace":
                return self.is_market_visible()
            return super(MongolInfo, self).interaction_visible(room_code)

define MongolStaticData = MongolData()
default Mongol = MongolInfo()

label register_mongol_secondary:
    python:
        MongolStaticData.set_schedule(mongol_schedule_entries())
        people.register(MongolStaticData, Mongol)
    return
