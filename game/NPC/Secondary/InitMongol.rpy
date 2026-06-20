init python:
    def mongol_story_defaults():
        return {
            "StocksReleased": 0,
            "WillTryToSteal": 0,
            "StocksFoodDay": -1,
            "StocksArrestDay": -1,
            "StocksSeen": 0,
            "GuardGiftSent": 0,
            "GuardCaptainKnown": 0,
            "MarketRollDay": -1,
            "MarketRoll": 0,
            "GypsyAsk": 0,
            "AskPriceIncr": 0,
            "ZimmerKnow": 0,
            "HorsePrice": 1000,
            "DiscountAsk": 0,
            "TheftAsk": 0,
            "AskSawStolen": 0,
            "SawStolen": 0,
            "HorsesBought": 0,
        }

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
                age=39,
                portrait="images/mongol/portrait1.jpg",
            )

    class MongolInfo(BaseNPC):
        """Mongol: horse trader, stocks prisoner, theft and Clara merchant hooks."""
        unknown_name = "Мужик в красной рубахе"

        def __init__(self, name="mongol", **kwargs):
            super().__init__(name, **kwargs)
            self.data = MongolStaticData
            self.age = 39
            self.known = False
            self.location = ""
            self.var = {}
            self.ensure_story_defaults()

        def update(self):
            self.name = people_normalize_id(self.name)
            self.data = MongolStaticData
            self.location = ""
            self.ensure_story_defaults()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in mongol_story_defaults().items():
                self.var.setdefault(key, value)
            self.promote_from_var(self.var)
            return self.var

        def story_value(self, key, default=0):
            self.ensure_story_defaults()
            return self.var.get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()
            self.var[key] = value
            self.promote_from_var(self.var)
            return value

        def var_int(self, key, default=0):
            self.ensure_story_defaults()
            return people_to_int(self.var.get(key, default), default)

        def set_var_int(self, key, value):
            self.ensure_story_defaults()
            value = people_to_int(value, 0)
            self.var[key] = value
            self.promote_from_var(self.var)
            return value

        def reset_market_trade(self):
            self.set_var_int("HorsePrice", 1100 if self.var_int("ZimmerKnow", 0) else 1000)
            self.set_var_int("DiscountAsk", 0)
            return self.var_int("HorsePrice", 1000)

        def prepare_market_roll(self):
            self.ensure_story_defaults()
            current_day = int(dayspassed or 0)
            if self.var_int("MarketRollDay", -1) != current_day:
                self.set_var_int("MarketRollDay", current_day)
                self.set_var_int("MarketRoll", 1 if procedural_randint(1, 4, "mongol_market_%s" % current_day) == 1 else 0)
            return self.var_int("MarketRoll", 0)

        def is_market_visible(self):
            if str(MyStallion or "") != "":
                return False
            try:
                if not MarketPlaceRoom.is_open(week, time):
                    return False
            except Exception:
                return False
            return self.prepare_market_roll() == 1

define MongolStaticData = MongolData()
default Mongol = MongolInfo()

label InitMongol:
    call register_mongol_secondary from _call_init_mongol_register
    return


label register_mongol_secondary:
    $ knowsMC.setdefault("mongol", False)
    python:
        peopleData["mongol"] = MongolStaticData
        Mongol.update()
        peopleInfo["mongol"] = Mongol
        if Mongol not in secondary_npcs:
            secondary_npcs.append(Mongol)
    return


label _auto_register_mongol:
    call register_mongol_secondary from _call_mongol_reg
    return
