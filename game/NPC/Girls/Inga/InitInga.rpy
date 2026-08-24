# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitInga:
    python:
        people.register(IngaStaticData, Inga)
    return

init python:
    def inga_grocery_store_active(weekday_value=None):
        week_now = int(calendar_v2.week if weekday_value is None else weekday_value or 0)
        if week_now == 7:
            return False
        return str(people.get_data("eddie").getLocation(week_now, calendar_v2.hour) or "") != "GroceryStore"

    class IngaData(PeopleData):
        code_name = "inga"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Ингенборг",
                fullname="Ингенборг Блэнкеншип",
                genitive="Ингенборг",
                dative="Ингенборг",
                default_location="",
                description="Старшей дочке вдовы Блэнкеншип в привлекательности не откажешь. Рыжая, высокая, зеленоглазая, с большой налитой грудью, Ингенборг выглядит как молодая и еще более привлекательная копия своей матушки.",
                birth_date={"day": 1, "period": 1, "cycle": 1078},
                portrait="images/inga/StreetSex/minet1.jpg",
                schedule_entries=[
                    NPCScheduleEntry(
                        location="GroceryStore",
                        weekdays=[1, 2, 3, 4, 5, 6],
                        start_hour=6,
                        end_hour=8,
                        awake=True,
                        talkable=True,
                        condition=inga_grocery_store_active,
                        priority=230,
                        label="inga_grocery_cover",
                    ),
                    NPCScheduleEntry(
                        location="Church",
                        weekdays=[7],
                        start_minute=8 * 60,
                        end_minute=9 * 60 + 30,
                        awake=True,
                        talkable=False,
                        priority=220,
                        label="inga_sunday_church",
                    ),
                    NPCScheduleEntry(
                        location="BeckyHome",
                        weekdays=[1, 2, 3, 4, 5, 6, 7],
                        start_hour=6,
                        end_hour=23,
                        awake=True,
                        talkable=True,
                        priority=20,
                        label="inga_home_awake",
                    ),
                    NPCScheduleEntry(
                        location="BeckyHome",
                        weekdays=[1, 2, 3, 4, 5, 6, 7],
                        start_hour=23,
                        end_hour=6,
                        awake=False,
                        talkable=False,
                        priority=10,
                        label="inga_home_sleep",
                    ),
                ],
            )

    class IngaInfo(Girl):
        """Inga Blankenship: secondary NPC with Becky-home story state."""
        talk_label = "IntIngaTalk"
        code_name = "inga"
        unknown_name = "Незнакомка"
        registry_group = "secondary"

        def __init__(self, name="inga", **kwargs):
            super().__init__(name, **kwargs)
            self.data = IngaStaticData
            self.rel = 0
            self.openness = 0
            self.corruption = 30
            self.saw_lucas_sex = False
            self.acquaintance_stage = 0
            self.stats = {
                "kids": 0,
                "beauty": 55,
                "sexacts": 134,
                "cuminside": 42,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 10,
                "PussyWetStart": 25,
                "virginity": False,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 40,
                "cleaning": 20,
                "waitress": 40,
            }
            self.jobs = {
                "jobkitchen": 0,
                "jobcleaning": 0,
                "jobwaitress": 0,
                "jobHallAvail": 0,
                "jobWhoreAvail": 0,
                "jobwhore": 0,
                "jobgloryhole": 0,
            }
            self.gift_preferences = ["wild_rose_001", "soap_001", "lavender_001"]
            self.wardrobe = {
                "owned": ["openworkdress", "simplebra", "simplepanties", "redstockings", "simpleshoes"],
                "gifted": [],
                "current_dress": "openworkdress",
                "current_underwear": {
                    "bra": "simplebra",
                    "panties": "simplepanties",
                    "legs": "redstockings",
                    "shoes": "simpleshoes",
                },
            }
        def update(self):
            super(IngaInfo, self).update()
            self.data = IngaStaticData
            return self

        def interaction_visible(self, room_code=""):
            if str(room_code or "").strip() == "BeckyHome":
                return self.acquaintance_stage >= 1 and rooms.get("BeckyHomeFront").state["arrival_mode"] == ""
            return super(IngaInfo, self).interaction_visible(room_code)

        def action_data(self, where_id=""):
            data = super(IngaInfo, self).action_data(where_id)
            if str(where_id or "").strip() == "GroceryStore":
                if not self.known:
                    data["title"] = "Торговец"
                data["picture_path"] = grocery_store_grocer_picture(self.name)
                data["talk_picture"] = data["picture_path"]
            return data

define IngaStaticData = IngaData()
default Inga = IngaInfo()
