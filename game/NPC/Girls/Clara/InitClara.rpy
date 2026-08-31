# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.exports as renpy

    class ClaraData(PeopleData):
        code_name = "clara"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Кларисса",
                fullname="Кларисса",
                genitive="Клариссы",
                dative="Клариссе",
                description="Кларисса, старшая дочь мессира Легаре, молодая девушка из зажиточного купеческого дома. Это очень приветливая и игривая блондинка чуть младше вас, с большими искрящимися серыми глазами, пухлыми губами и удивительно легкой, грациозной походкой. На ней обычно свободное длинное повседневное платье из легкой ткани, похожее на удобный сарафан; на ярком свету ткань кажется чуть прозрачной. Грудь Клариссы размера B мягко и соблазнительно колышется при каждом движении. От нее пахнет лавандой и дорогими модными духами.",
                gift_preferences=["dress_thiefdress", "soap_001", "special_mushroom_001", "dress_simplebra", "dress_simplepanties", "dress_blackstockings", "dress_redstockings", "libido_tincture_001", "werecat_caught_cat"],
            )
            self.birth_date = {"day":20, "period":11, "cycle": 1081}
            self.card_image = "images/clara/portrait1.jpg"
            self.schedule_source = "schedules/clara.json"

    class ClaraInfo(Girl):
        """Clara runtime: wine store, market booklet, paintings thread, social state."""
        talk_label = "IntClaraTalk"
        unknown_name = "Незнакомка"
        def __init__(self):
            super().__init__("clara")
            self.code_name = "clara"
            self.data = ClaraStaticData
            self.rel = 0
            self.openness = 0
            self.corruption = 10
            self.known = True
            self.flirt_count = 0
            self.drawings_secret_known = False
            self.market_intro_seen = False
            self.market_follow_failed_day = -1
            self.market_follow_failed_hour = -1
            self.market_day_roll_day = -1
            self.market_day_roll = False
            self.market_evening_roll_day = -1
            self.market_evening_roll = False
            self.day_location_override_day = -1
            self.day_location_override_code = ""
            self.merchant_contact_unlocked = False
            self.merchant_contact_month_key = -1
            self.old_water_pump_hint_seen = False
            self.commission_followup_day = 999999
            self.murder_day = 999999
            self.energy = 100
            self.energy_max = 100
            self.rebellion = 0
            self.anger_with_player = 0
            self.fun = 0
            self.trust = 0
            self.fear = 0
            self.mana = 25
            self.mana_corrupted = False
            self.mood = "neutral"
            self.reaction_log = []
            self.reaction_state = {
                "last_reaction": "",
                "last_reaction_day": None,
                "last_reaction_context": "",
                "last_reaction_score": 0,
                "last_mana_delta": 0,
                "last_mana_reasons": [],
                "pending_decision": "",
            }
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.stats = {
                "kids": 0,
                "beauty": 62,
                "sexacts": 0,
                "cuminside": 0,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 10,
                "PussyWetStart": 10,
                "virginity": True,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 10,
                "cleaning": 8,
                "waitress": 45,
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
            self.relationship_cap = 100
            self.talk_preferences = {
                "favorite_topics": ["fashion", "stories", "gossip", "money", "family_life"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["greenworkdress", "simplebra", "simplepanties", "simpleshoes"],
                "gifted": [],
                "current_dress": "greenworkdress",
                "current_underwear": {
                    "bra": "simplebra",
                    "panties": "simplepanties",
                    "legs": "",
                    "shoes": "simpleshoes",
                },
            }
        def update(self):
            super(ClaraInfo, self).update()
            self.data = ClaraStaticData
            return self

        def interaction_visible(self, room_code=""):
            room_key = str(room_code or "").strip()
            if room_key == "MarketPlace":
                return False
            if room_key == "WineStore":
                return wine_store_seller_id() == self.name
            return super(ClaraInfo, self).interaction_visible(room_code)

        def wine_store_talk_picture(self):
            candidates = [
                "images/clara/wineSellar_clara_talk.png",
                "images/clara/wine_sellar_clara_talk_2.png",
                "images/clara/wineSellar_clara_talk_3.png",
                "images/clara/wineSellar_clara_talk_4.png",
                "images/clara/wineSellar_clara_talk_5.png",
                "images/clara/wineSellar_clara_talk_6.png",
            ]
            loadable = [row for row in candidates if renpy.loadable(row)]
            return procedural_choice(loadable, key="procedural:NPC/Girls/Clara/InitClara.rpy:clara_wine_store_talk_picture") if len(loadable) > 0 else ""

        def wine_store_flirt_picture(self):
            candidates = [
                "images/clara/wineSellar_clara_flirt_0.png",
                "images/clara/wineSellar_clara_flirt_1.png",
                "images/clara/wineSellar_clara_flirt_2.png",
            ]
            loadable = [row for row in candidates if renpy.loadable(row)]
            return procedural_choice(loadable, key="procedural:NPC/Girls/Clara/InitClara.rpy:clara_wine_store_flirt_picture") if len(loadable) > 0 else ""

        def forest_picture(self, location_code=""):
            location_key = str(location_code or "").strip()
            candidates = []
            if location_key == "ForestClearing":
                candidates = [
                    "images/clara/forest_clara.png",
                    "images/clara/forest_clara_0.png",
                    "images/clara/forest_clara_1.png",
                    "images/clara/forest_clara_encounter.png",
                    "images/clara/forest_clara_encounter_2.png",
                ]
            elif location_key == "ForestSpring":
                candidates = [
                    "images/clara/forestSpring_clara.png",
                    "images/clara/forest_spring_clara_1.png",
                    "images/clara/forest_spring_clara_2.png",
                ]
            elif location_key == "ForestLake":
                candidates = [
                    "images/clara/forestlake_clara.png",
                    "images/clara/forestlake_clara_0.png",
                    "images/clara/forestLake_clara_2.png",
                ]
            loadable = [row for row in candidates if renpy.loadable(row)]
            return procedural_choice(loadable, key="procedural:NPC/Girls/Clara/InitClara.rpy:clara_forest_picture:%s" % location_key) if len(loadable) > 0 else ""

        def visible_at_friday_dance(self):
            return CheckIfDanceExist("amanda", "legare", rooms.get("FridayDance").dance_count) <= 0

        def set_day_location_override(self, location_code=""):
            location_key = str(location_code or "").strip()
            if location_key:
                self.day_location_override_day = int(calendar_v2.daysInGame or 0)
                self.day_location_override_code = location_key
            else:
                self.day_location_override_day = -1
                self.day_location_override_code = ""
            return location_key

        def getLocation(self, wday=None, hour=None):
            scheduled_location = super(ClaraInfo, self).getLocation(wday, hour)
            if scheduled_location == "BarberShop":
                return scheduled_location
            override_day = people_to_int(self.day_location_override_day, -1)
            override_location = str(self.day_location_override_code or "").strip()
            if override_location and override_day == int(calendar_v2.daysInGame or 0):
                return override_location
            return scheduled_location

        def can_start_social_events(self):
            update_stat_state()
            return int(player_charisma_breakdown().get("charisma", 0) or 0) >= 70 and int(self.rel or 0) >= 5

        def tavern_visit_active(self):
            clock_value = (int(calendar_v2.hour or 0) * 60 + int(calendar_v2.minute or 0)) % 1440
            if clock_value < 720 or clock_value > 1079:
                return False
            week_value = int(calendar_v2.week or 0)
            if week_value == 7:
                return False
            return ((current_game_day() + week_value) % 4) == 0

        def can_receive_gifts(self):
            update_stat_state()
            return int(player_charisma_breakdown().get("charisma", 0) or 0) >= 70 and int(self.rel or 0) >= 7

        def has_caught_cat_gift(self):
            return werecat_second_gift_available() and int(werecat_state().get("caught", 0) or 0) == 1

        def can_accept_horse_ride(self, location_code=""):
            location_key = str(location_code or rooms.current_code or "").strip()
            if location_key not in ("ForestClearing", "ForestLake"):
                return False
            if str(people.location(self.code_name) or "") != str(location_key or ""):
                return False
            return player.horse.owns_horse() and bool(player.horse.saddled)

        def giftable_entries(self):
            entries = []

            item_ids = ("soap_001", "special_mushroom_001", "lavender_001", "luxury_soap_001", "libido_tincture_001")
            for item_id in item_ids:
                if player.item_count(item_id) <= 0:
                    continue
                item_obj = get_game_item(item_id)
                if item_obj is None:
                    continue
                entries.append({
                    "source": "item",
                    "gift_id": str(item_id),
                    "gift_name": str(getattr(item_obj, "name", item_id) or item_id),
                })

            dress_codes = (
                "thiefdress",
                "simplebra",
                "simplepanties",
                "blackstockings",
                "redstockings",
            )
            for dress_code in dress_codes:
                if not player.appearance.has_dress(dress_code):
                    continue
                if str(player.appearance.current_dress or "") == str(dress_code or ""):
                    continue
                entries.append({
                    "source": "dress",
                    "gift_id": "dress_" + str(dress_code),
                    "gift_name": str(ShortDressName.get(dress_code, dress_code) or dress_code),
                    "dress_code": str(dress_code),
                })

            if self.has_caught_cat_gift():
                entries.append({
                    "source": "werecat",
                    "gift_id": "werecat_caught_cat",
                    "gift_name": "пойманная лесная кошка",
                })

            return entries

        def has_giftable_entries(self):
            return len(list(self.giftable_entries() or [])) > 0

        def remove_gift_entry(self, entry):
            row = dict(entry or {})
            source = str(row.get("source", "") or "")
            if source == "werecat":
                if not werecat_second_gift_available() or int(werecat_state().get("caught", 0) or 0) != 1:
                    return False
                werecat_apply_clara_gift_bonus()
                return True
            if source == "dress":
                dress_code = str(row.get("dress_code", "") or "")
                if dress_code == "" or not player.appearance.has_dress(dress_code):
                    return False
                if dress_code == str(player.appearance.current_dress or ""):
                    return False
                appearance = player.appearance
                result = appearance.remove_dress(dress_code)
                return result

            item_id = str(row.get("gift_id", "") or "")
            if item_id == "":
                return False
            return player.remove_item(item_id, 1)

        def initialize_new_game_state(self):
            self.prepare_daily_event_rolls()
            return self

        def prepare_daily_event_rolls(self):
            day_value = current_game_day()
            week_value = int(calendar_v2.week or 0)
            if people_to_int(self.market_day_roll_day, -1) != day_value:
                self.market_day_roll_day = day_value
                if week_value == 7:
                    self.market_day_roll = False
                else:
                    self.market_day_roll = procedural_randint(1, 2, "clara_market_day_%s_%s" % (day_value, week_value)) == 1
            if people_to_int(self.market_evening_roll_day, -1) != day_value:
                self.market_evening_roll_day = day_value
                if week_value in (5, 7):
                    self.market_evening_roll = False
                else:
                    self.market_evening_roll = procedural_randint(1, 3, "clara_market_evening_%s_%s" % (day_value, week_value)) == 1
            return self

define ClaraStaticData = ClaraData()
default Clara = ClaraInfo()

label InitClara:
    python:
        Clara.initialize_new_game_state()
        people.register(ClaraStaticData, Clara)
    return
