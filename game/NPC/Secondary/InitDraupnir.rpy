init python:
    class DraupnirData(PeopleData):
        code_name = "draupnir"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Драупнир",
                fullname="Мастер Драупнир",
                genitive="Драупнира",
                dative="Драупниру",
                default_location="",
                description="Драупнир - гном-столяр из квартала ремесленников. Дерет дорого, но вывески, отверстия, глорихолы, зольные бочки и будки делает на совесть.",
                birth_date={"day": 1, "period": 1, "cycle": 1055},
                portrait="images/draupnir/dwarf1.jpg",
                schedule_entries=[
                    NPCScheduleEntry(
                        location="StolyarWorkshop",
                        weekdays=[1, 2, 3, 4, 5, 6],
                        start_hour=6,
                        end_hour=18,
                        label="workshop",
                    ),
                ],
            )

    class DraupnirInfo(BaseNPC):
        """Draupnir: carpenter/artisan in StolyarWorkshop, gloryhole/soap/dog-booth quests."""
        talk_label = "IntDraupnirTalk"
        unknown_name = "Драупнир"

        def __init__(self, name="draupnir", **kwargs):
            super().__init__(name, **kwargs)
            self.soap_barrel_quote_received = False
            self.dog_booth_quote_received = False
            self.mongol_lockpick_order_day = -1

        def getLocation(self, wday=None, hour=None):
            job = tavern.active_renovation
            if job is not None:
                return TAVERN_RENOVATIONS[job.code].room
            return super(DraupnirInfo, self).getLocation(wday, hour)

        def social_action_allowed(self, action="", item_id=""):
            if tavern.active_renovation is not None:
                return False
            return super(DraupnirInfo, self).social_action_allowed(action, item_id)

define DraupnirStaticData = DraupnirData()
default Draupnir = DraupnirInfo()

label register_draupnir_secondary:
    python:
        people.register(DraupnirStaticData, Draupnir)
    return
