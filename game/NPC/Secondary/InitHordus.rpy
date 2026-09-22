init python:
    class HordusData(PeopleData):
        code_name = "hordus"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Хордус Папирус",
                fullname="Хордус Папирус",
                genitive="Хордуса Папируса",
                dative="Хордусу Папирусу",
                default_location="",
                description="Хордус Папирус, по прозвищу Хорди, — таинственный торговец редкими товарами.",
                portrait="images/market/mistery_merchant.png",
                schedule_entries=[
                    NPCScheduleEntry(
                        location="MarketPlace",
                        weekdays=[1, 2, 3, 4, 5, 6],
                        start_hour=12,
                        end_hour=18,
                        priority=900,
                        label="monthly_market_visit",
                    ),
                ],
            )
            self.catalog = {
                "cursed_sofa_001": 600,
                "luxury_soap_001": 45,
                "libido_tincture_001": 60,
                "special_mushroom_001": 35,
            }

        def monthly_visit_days(self):
            from hashlib import sha256

            market = rooms.get("MarketPlace")
            if market is None:
                return ()
            # Ranking depends only on the month and its calendar weekdays;
            # reading a schedule never rolls or saves another calendar state.
            eligible = []
            for day in range(1, 29):
                weekday = (int(calendar_v2.week) - int(calendar_v2.day) + day - 1) % 7 + 1
                if weekday != 7 and market.is_open(weekday, 12):
                    eligible.append(day)
            ranked = sorted(
                eligible,
                key=lambda day: sha256(
                    ("hordus:%s:%s:%s" % (calendar_v2.cycle, calendar_v2.period, day)).encode("utf-8")
                ).digest(),
            )
            return tuple(sorted(ranked[:2]))

        def schedule_resolve(self, weekday_value=None, time_value=None):
            if int(calendar_v2.day) not in self.monthly_visit_days():
                return None
            if not rooms.get("MarketPlace").is_open(weekday_value, time_value):
                return None
            return super(HordusData, self).schedule_resolve(weekday_value, time_value)

    class HordusInfo(BaseNPC):
        talk_label = "IntHordusTalk"
        unknown_name = "Таинственный торговец"

        def __init__(self, name="hordus", **kwargs):
            super().__init__(name, **kwargs)
            self.data = HordusStaticData
            self.known = False
            self.last_trade_month = -1
            self.last_meeting_day = -1

        def update(self):
            super(HordusInfo, self).update()
            self.data = HordusStaticData
            return self

define HordusStaticData = HordusData()
default Hordus = HordusInfo()

label register_hordus_secondary:
    python:
        people.register(HordusStaticData, Hordus)
    return
