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

    class MongolInfo(BaseNPC):
        """Mongol: horse trader, stocks prisoner, theft and Clara merchant hooks."""
        talk_label = "MarketPlaceTalkMongol"
        unknown_name = "Мужик в красной рубахе"

        def __init__(self, name="mongol", **kwargs):
            super().__init__(name, **kwargs)
            self.data = MongolStaticData
            self.known = False
            self.will_try_to_steal = False
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

        def update(self):
            self.name = people_normalize_id(self.name)
            self.data = MongolStaticData
            return self

        def reset_market_trade(self):
            self.horse_price = 1100 if self.zimmer_knows_horse_theft else 1000
            self.discount_asked = False
            return self.horse_price

        def prepare_market_roll(self, reroll=False):
            current_day = current_game_day()
            if bool(reroll) or self.market_roll_day != current_day:
                self.market_roll_day = current_day
                self.market_roll = renpy.random.randint(1, 4) == 1
            return self.market_roll

        def is_market_visible(self):
            if str(self.stocks_fate or "") == "convicted":
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
        MongolStaticData.set_schedule([
            NPCScheduleEntry(location="MarketPlace", weekdays=[1, 2, 3, 4, 5, 6], start_hour=6, end_hour=19, awake=True, talkable=True, condition=marketplace_mongol_visible, priority=100, label="market_horse_trade"),
        ])
        people.register(MongolStaticData, Mongol)
    return
