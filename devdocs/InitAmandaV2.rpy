# Draft only. This file is not loaded by Ren'Py because it lives under devdocs.
# Purpose: Amanda class/default model built from the current InitAmanda dict values.
#
# Time contract:
# - NPC schedules use hidden exact engine time: clock_minutes / JSON intervals.
# - Normal HUD shows fantasy time-slot names only, never real clock text.
# - Real clock values belong to debug tools and schedule authoring.

init python:
    class AmandaData(PeopleData):
        code_name = "amanda"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Аманда",
                fullname="Аманда",
                genitive="Аманды",
                dative="Аманде",
                default_location="TavernMain",
                description="Аманда - молодая девушка. У нее очень светлая кожа, белокурые волосы и голубые глаза. Ее груди небольшие, размера А.",
                gift_preferences=[
                    "wild_rose_001",
                    "soap_001",
                    "berries_001",
                    "energy_tea_001",
                    "drink_ale_001",
                ],
            )
            self.starting_age = 18
            self.birth_record = calendar_make_birth_record(self.starting_age)
            self.schedule_source = "schedules/amanda.json"
            self.schedule_uses_clock_minutes = True
            self.hud_time_display = "time_slot_only"
            self.stats = {
                "kids": 0,
                "beauty": 52,
                "sluttiness": 0,
                "sexacts": 0,
                "cuminside": 0,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 10,
                "PussyWetStart": 0,
                "virginity": True,
                "cooking": 20,
                "cleaning": 30,
                "waitress": 15,
                "otkroven": 3,
                "Friends": 5,
            }
            self.clothing = {
                "dressdefault": "modestworkdress",
                "bradef": "simplebra",
                "pantiesdef": "simplepanties",
                "legsdef": "",
                "shoesdef": "simpleshoes",
            }
            self.jobs = {
                "jobkitchen": 0,
                "jobcleaning": 1,
                "jobwaitress": 1,
                "jobHallAvail": 1,
                "jobWhoreAvail": 0,
                "jobwhore": 0,
                "jobgloryhole": 0,
            }
            self.story_defaults = {
                "lizafriends": 0,
                "prohibitliza": 0,
                "alberfriends": 0,
                "albernowdances": 0,
                "alberdanceadvance": 0,
                "leftdances": 0,
                "alberprohibit": 0,
                "LegareGo": 0,
                "EscapeUnnoticed": 0,
                "glorytried": 0,
                "gloryyouknow": 0,
                "gloryscold": 0,
                "glorywalkout": 0,
                "glorysuck": 0,
                "glorysdiscover": 0,
                "glorydeflower": 0,
                "suckyou": 0,
                "fuckyou": 0,
                "knowsexactive": 0,
                "knownotvirgin": 0,
                "knowlegaresex": 0,
                "sawlegaresex": 0,
                "sucklegare": 0,
                "fucklegare": 0,
                "deflowerlegare": 0,
                "knowdeflowerlegare": 0,
                "beddeflower": 0,
                "kickyoufromroom": 0,
                "kickyoufromroomcount": 0,
                "kickedwithmomhelp": 0,
                "knowyousawlegaresex": 0,
                "knowyouseesex": 0,
                "warnnotwork": 0,
                "sawwithguys": 0,
                "prohibitwithguys": 0,
                "askzalettoday": 0,
                "MomDressComplaint": 0,
                "gave_night_bowl": 0,
                "night_bowl_request_day": -1,
                "night_bowl_window_seen_day": -1,
                "got_fancy_night_bowl": 0,
                "prefers_backyard_relief": -1,
                "attic_window_busted": 0,
                "attic_window_breakfast_bj_day": -1,
                "attic_window_morning_day": -1,
                "attic_mock_response_day": -1,
                "attic_mock_stopped": 0,
                "attic_mock_exposed": 0,
                "breakfast_tease_day": -1,
            }

        def current_age(self):
            return calendar_age_from_birth_record(self.birth_record)

        def schedule_intervals(self):
            # Draft of the JSON schedule shape. Engine resolves by hidden clock_minutes.
            # `to_minute` is exclusive. HUD still displays only fantasy time slot names.
            return [
                {"location": "TavernMain", "weekdays": [1, 2, 3, 4, 5, 6], "from_minute": 360, "to_minute": 480, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:TavernMain:morning", "priority": 300, "label": "morning_hall"},
                {"location": "TavernKitchen", "weekdays": [1, 2, 3, 4, 5, 6], "from_minute": 360, "to_minute": 480, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:TavernKitchen:morning", "priority": 300, "label": "morning_kitchen"},
                {"location": "TavernStorage", "weekdays": [1, 2, 3, 4, 5, 6], "from_minute": 360, "to_minute": 480, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:TavernStorage:morning", "priority": 300, "label": "morning_storage"},
                {"location": "Backyard", "weekdays": [1, 2, 3, 4, 5, 6], "from_minute": 360, "to_minute": 480, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:Backyard:morning", "priority": 300, "label": "morning_backyard"},
                {"location": "TavernAmandaRoom", "weekdays": [1, 2, 3, 4, 5, 6], "from_minute": 360, "to_minute": 480, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:TavernAmandaRoom:morning", "priority": 300, "label": "morning_room"},
                {"location": "TavernMain", "weekdays": [1, 2, 3, 4, 6], "from_minute": 480, "to_minute": 960, "awake": True, "talkable": True, "priority": 200, "label": "working_hall"},
                {"location": "FridayDance", "weekdays": [5], "from_minute": 780, "to_minute": 960, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:FridayDance:friday_evening", "priority": 250, "label": "friday_dance"},
                {"location": "Church", "weekdays": [7], "from_minute": 360, "to_minute": 660, "awake": True, "talkable": False, "priority": 260, "label": "sunday_church"},
                {"location": "TavernAmandaRoom", "weekdays": [7], "from_minute": 660, "to_minute": 960, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:TavernAmandaRoom:sunday", "priority": 240, "label": "sunday_room"},
                {"location": "Backyard", "weekdays": [7], "from_minute": 660, "to_minute": 960, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:Backyard:sunday", "priority": 240, "label": "sunday_backyard"},
                {"location": "TavernMain", "weekdays": [7], "from_minute": 660, "to_minute": 960, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:TavernMain:sunday", "priority": 240, "label": "sunday_hall"},
                {"location": "TavernKitchen", "weekdays": [7], "from_minute": 660, "to_minute": 960, "awake": True, "talkable": True, "condition": "tavern_team_match:amanda:TavernKitchen:sunday", "priority": 240, "label": "sunday_kitchen"},
                {"location": "TavernAmandaRoom", "weekdays": [1, 2, 3, 4, 5, 6, 7], "from_minute": 1380, "to_minute": 1440, "awake": False, "talkable": False, "priority": 10, "label": "sleep_late"},
                {"location": "TavernAmandaRoom", "weekdays": [1, 2, 3, 4, 5, 6, 7], "from_minute": 0, "to_minute": 360, "awake": False, "talkable": False, "priority": 10, "label": "sleep_early"},
            ]


    class AmandaInfo(Girl):
        code_name = "amanda"

        def __init__(self, var=None):
            super().__init__(self.code_name, var=var)
            self.data = AmandaStaticData
            self.age = AmandaStaticData.starting_age
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.relationship = AmandaStaticData.stats["Friends"]
            self.openness = AmandaStaticData.stats["otkroven"]
            self.rebellion = 0
            self.fun = 0
            self.trust = 0
            self.fear = 0
            self.mood = "neutral"
            self.fertility_cycle = {
                "cycle_day": 0,
                "cycle_length": 28,
                "fertile_window_start": 11,
                "fertile_window_end": 16,
                "last_updated_day": None,
            }
            self.reaction_state = {
                "last_reaction": "",
                "last_reaction_day": None,
                "last_reaction_context": "",
                "pending_decision": "",
            }
            self.talk_preferences = {
                "likes": ["kindness", "family", "work_help", "small_gifts"],
                "dislikes": ["cruelty", "public_pressure", "dirty_jokes_early"],
                "favorite_topics": ["tavern_life", "family", "dreams", "chores"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["modestworkdress", "simplebra", "simplepanties", "simpleshoes"],
                "gifted": [],
                "current_dress": "modestworkdress",
                "current_underwear": {
                    "bra": "simplebra",
                    "panties": "simplepanties",
                    "legs": "",
                    "shoes": "simpleshoes",
                },
            }
            self.schedule_id = self.code_name
            self.schedule_source = AmandaStaticData.schedule_source
            self.schedule_uses_clock_minutes = True
            self.current_location = AmandaStaticData.default_location
            self.bday_asked = False
            self.birthday_known = False
            self.last_birthday_checked_day = None
            self.last_birthday_gift_day = None
            self.var = dict(AmandaStaticData.story_defaults)
            if isinstance(var, dict):
                self.var.update(var)

        def update(self):
            self.name = self.code_name
            self.data = AmandaStaticData
            self.sync_from_maps()
            return self

        def check_birthday(self):
            if self.last_birthday_checked_day == dayspassed:
                return False
            self.last_birthday_checked_day = dayspassed
            if calendar_is_birth_record_today(self.data.birth_record):
                self.age += 1
                return True
            return False

        def birthday_gift_bonus_available(self):
            return (
                self.birthday_known
                and calendar_is_birth_record_today(self.data.birth_record)
                and self.last_birthday_gift_day != dayspassed
            )


define AmandaStaticData = AmandaData()
default AmandaNPC = AmandaInfo()
