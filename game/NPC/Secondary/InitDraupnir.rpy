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

        def getLocation(self, wday=None, hour=None):
            if int(player.tavern_management.slogan_state or 0) == 1:
                return "StreetTavern"
            return super(DraupnirData, self).getLocation(wday, hour)

    class DraupnirInfo(BaseNPC):
        """Draupnir: carpenter/artisan in StolyarWorkshop, gloryhole/soap/dog-booth quests."""
        talk_label = "IntDraupnirTalk"
        unknown_name = "Драупнир"

        def __init__(self, name="draupnir", **kwargs):
            super().__init__(name, **kwargs)
            self.slogan_quote_received = False
            self.peep_hole_quote_received = False
            self.glory_hole_quote_received = False
            self.soap_barrel_quote_received = False
            self.dog_booth_quote_received = False
            self.mongol_lockpick_order_day = -1

        def social_action_allowed(self, action="", item_id=""):
            if int(player.tavern_management.slogan_state or 0) == 1:
                return False
            return super(DraupnirInfo, self).social_action_allowed(action, item_id)

define DraupnirStaticData = DraupnirData()
default Draupnir = DraupnirInfo()

label register_draupnir_secondary:
    python:
        people.register(DraupnirStaticData, Draupnir)
    return
