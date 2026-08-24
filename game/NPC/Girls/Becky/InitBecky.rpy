            knowsMC[name] = bool(self.known)            npc_schedule_sync_currentloc(name)        bodymodel_sync_character(GirlName, RealName[GirlName], "female")            self.current_location = "GroceryStore"        def story_value(self, key, default=0):
            return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            for table, stat_key in [
                (kids, "kids"),
                (beauty, "beauty"),
                (sexacts, "sexacts"),
                (cuminside, "cuminside"),
                (pregnancy, "pregnancy"),
                (pregfather, "pregfather"),
                (ConceptionChance, "ConceptionChance"),
                (PussyWetStart, "PussyWetStart"),
                (virginity, "virginity"),
                (Breastfeed, "breastfeed"),
            ]:
                table[name] = self.stats.get(stat_key)
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                table[name] = self.skills.get(skill_key, 0)
            self.ensure_story_defaults()[key] = value
            return value
            self.schedule_source = BeckyStaticData.schedule_source            self.schedule_source = BeckyStaticData.schedule_source
            self.current_location = "GroceryStore"        def install_schedule(self):
            name = self.code_name
            npc_interval_schedule_load_file(name)
            return self
            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            knowsMC[name] = bool(self.known)            npc_schedule_sync_currentloc(name)        bodymodel_sync_character(GirlName, RealName[GirlName], "female")            self.current_location = "GroceryStore"        def story_value(self, key, default=0):
                Becky.install_schedule()

        Becky.install_schedule()

    return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            for table, stat_key in [
                (kids, "kids"),
                (beauty, "beauty"),
                (sexacts, "sexacts"),
                (cuminside, "cuminside"),
                (pregnancy, "pregnancy"),
                (pregfather, "pregfather"),
                (ConceptionChance, "ConceptionChance"),
                (PussyWetStart, "PussyWetStart"),
                (virginity, "virginity"),
                (Breastfeed, "breastfeed"),
            ]:
                table[name] = self.stats.get(stat_key)
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                table[name] = self.skills.get(skill_key, 0)
            self.legacy_story_imported = False
            self.ensure_story_defaults()[key] = value
            return value
            self.schedule_source = BeckyStaticData.schedule_source            self.schedule_source = BeckyStaticData.schedule_source
            self.current_location = "GroceryStore"        def install_schedule(self):
            name = self.code_name
            npc_interval_schedule_load_file(name)
            return self
            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            knowsMC[name] = bool(self.known)            npc_schedule_sync_currentloc(name)        bodymodel_sync_character(GirlName, RealName[GirlName], "female")            self.current_location = "GroceryStore"        def story_value(self, key, default=0):
                Becky.install_schedule()

        Becky.install_schedule()

    return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            for table, stat_key in [
                (kids, "kids"),
                (beauty, "beauty"),
                (sexacts, "sexacts"),
                (cuminside, "cuminside"),
                (pregnancy, "pregnancy"),
                (pregfather, "pregfather"),
                (ConceptionChance, "ConceptionChance"),
                (PussyWetStart, "PussyWetStart"),
                (virginity, "virginity"),
                (Breastfeed, "breastfeed"),
            ]:
                table[name] = self.stats.get(stat_key)
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                table[name] = self.skills.get(skill_key, 0)
            self.legacy_story_imported = False
            self.ensure_story_defaults()[key] = value
            return value
            self.schedule_source = BeckyStaticData.schedule_source            self.schedule_source = BeckyStaticData.schedule_source
            self.current_location = "GroceryStore"        def install_schedule(self):
            name = self.code_name
            npc_interval_schedule_load_file(name)
            return self
            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel            self.relationship = self.rel# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def becky_story_defaults():
            Becky.install_schedule()

        Becky.install_schedule()

    return {
            "leftdances": 0,
            "danceinvitehome": 0,
            "visitedhome": 0,
            "husbandtalk": 0,
            "eddietalk": 0,
            "SawIngaFuck": 0,
            "IngaSexGreet": 0,
            "VisitScolded": 0,
            "TodayFrontSexCheck": 0,
            "HomeFrontCheckedDay": -1,
            "HomeEnterCheckedDay": -1,
            "HomeSex": 0,
            "EddieGeorg": 0,
            "EddieWhoreHome": 0,
            "BeckyOpenMinet": 0,
            "TimesVisited": 0,
            "TalkAboutEddie": 0,
            "GeorgMention": 0,
            "EddieIntrReact": 0,
            "PriestAdvice": 0,
            "GerhardBeckyTalk": 0,
            "AskedEddieFuck": 0,
            "EddieTryToFuck": 0,
            "EddieFailures": 0,
            "EddieRobbedDay": 0,
            "EddieRobbed": 0,
            "KnowSherwood": 0,
            "KnowSherwood": 0,
            "KnowSherwood": 0,
            "KnowSherwood": 0,
            "KnowSherwood": 0,
            "KnowSherwood": 0,
            "KnowBlackwood": 0,
            "SherwoodQuestScheduled": 0,
            "SherwoodSuspect": 0,
            "TradeOffer": 0,
            "SherwoodWarn": 0,
            "AskTradeElf": 0,
            "TradeOfferText": "",
            "FingalClarify": 0,
            "AdmitSherwood": 0,
            "RobbedByRobin": 0,
            "ConsoleRobbery": 0,
            "SandraKitchenVisitMonth": 0,
            "after_sermon_stage": 0,
            "last_store_orgasm_day": -1,
        }

    class BeckyData(PeopleData):
        code_name = "becky"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Бекки",
                fullname="Ребекка Блэнкеншип",
                genitive="Бекки",
                dative="Бекки",
                default_location="GroceryStore",
                description="Вдова Блэнкеншип, для друзей Бекки, высокая рыжеволосая женщина с полной грудью, чуть младше сорока лет.",
                gift_preferences=["soap_001", "wild_rose_001", "pig_lard_001", "libido_tincture_001", "drink_ale_001"],
            )
            # Original Becky init only defines age 36. This keeps that age at game start until a canonical birthday is written.
            self.birth_date = {"day": 1, "period": 1, "cycle": 1064}
            self.card_image = "images/becky/becky_card.jpg"
            self.schedule_source = "schedules/becky.json"

    class BeckyInfo(Girl):
        """Becky runtime: grocery work, home visits, Eddie, church, Sherwood trade, pregnancy."""
        unknown_name = "Незнакомка"

        def __init__(self):
            super().__init__("becky")
            self.code_name = "becky"
            self.data = BeckyStaticData
            self.uses_own_var_state = True
            self.rel = 0
            self.openness = 0
            self.corruption = 25
            self.known = True
            self.energy = 100
            self.energy_max = 100
            self.rebellion = 0
            self.anger_with_player = 0
            self.fun = 0
            self.trust = 0
            self.fear = 0
            self.mana = 10
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
                "kids": 5,
                "beauty": 45,
                "sexacts": 5352,
                "cuminside": 3593,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 5,
                "PussyWetStart": 25,
                "virginity": False,
                "breastfeed": 0,
                "orgasms_given": 0,
            }
            self.skills = {
                "cooking": 70,
                "cleaning": 50,
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
            self.gift_preferences = list(BeckyStaticData.gift_preferences)
            self.talk_preferences = {
                "favorite_topics": ["family", "husband", "eddie", "inga", "sherwood"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["openworkdress", "simplebra", "simplepanties", "blackstockings", "simpleshoes"],
                "gifted": [],
                "current_dress": "openworkdress",
                "current_underwear": {
                    "bra": "simplebra",
                    "panties": "simplepanties",
                    "legs": "blackstockings",
                    "shoes": "simpleshoes",
                },
            }
            self.var = {}
            self.legacy_story_imported = False
            self.ensure_story_defaults()

        def update(self):
            self.name = self.code_name
            self.data = BeckyStaticData
            self.ensure_story_defaults()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in becky_story_defaults().items():
                self.var.setdefault(key, value)
            return self.var

        def publish_profile_state(self):
            name = self.code_name
            RealName[name] = self.data.cname
            RealName2[name] = self.data.genitive
            RealName3[name] = self.data.dative
            DateOfBirth[name] = dict(self.data.birth_date)
            girltextdesc[name] = self.data.description
            self.location = str(self.current_location or "GroceryStore")
            GiftPreferences[name] = list(self.gift_preferences)
            dressdefault[name] = self.wardrobe["current_dress"]
            bradef[name] = self.wardrobe["current_underwear"]["bra"]
            pantiesdef[name] = self.wardrobe["current_underwear"]["panties"]
            legsdef[name] = self.wardrobe["current_underwear"]["legs"]
            shoesdef[name] = self.wardrobe["current_underwear"]["shoes"]
            topdress[name] = DressTopPart.get(dressdefault[name], "")
            bottomdress[name] = DressBottomPart.get(dressdefault[name], "")
            bra[name] = bradef[name]
            panties[name] = pantiesdef[name]
            legs[name] = legsdef[name]
            shoes[name] = shoesdef[name]
            self.wardrobe["current_layers"] = [row for row in [dressdefault[name], bradef[name], pantiesdef[name], legsdef[name], shoesdef[name]] if str(row or "")]
            self.ensure_story_defaults()
            return self

        def initialize_new_game_state(self):
            self.ensure_story_defaults()
            self.publish_profile_state()
            return self

        def reset_daily(self, full=False):
            super(BeckyInfo, self).reset_daily(full)
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.var["TodayFrontSexCheck"] = 0
            self.var["after_sermon_stage"] = 0
            return self

        def story_value(self, key, default=0):
            return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()[key] = value
            return value

        def add_story_value(self, key, amount=1):
            return self.set_story_value(key, people_to_int(self.story_value(key, 0), 0) + people_to_int(amount, 0))

        def set_story_value_min(self, key, value):
            current = people_to_int(self.story_value(key, 0), 0)
            return self.set_story_value(key, max(current, people_to_int(value, 0)))

        def add_relation(self, amount=1, cap=20):
            self.rel = max(0, min(people_to_int(cap, 20), people_to_int(self.rel, 0) + people_to_int(amount, 0)))
            return self.rel

        def add_corruption(self, amount=1, floor=0, cap=100):
            self.corruption = max(people_to_int(floor, 0), min(people_to_int(cap, 100), people_to_int(self.corruption, 0) + people_to_int(amount, 0)))
            return self.corruption

        def change_social(self, friend_delta=0, open_delta=0, corruption_delta=0):
            super(BeckyInfo, self).change_social(friend_delta, open_delta, corruption_delta)
            return self

        def apply_social_gate(self, rel_gate=0, open_delta=0, rel_delta=0, corruption_gate=0, corruption_delta=0, fallback_rel_delta=0):
            if people_to_int(self.rel, 0) >= people_to_int(rel_gate, 0):
                self.add_relation(rel_delta)
            elif fallback_rel_delta:
                self.add_relation(fallback_rel_delta)
            if people_to_int(self.corruption, 0) >= people_to_int(corruption_gate, 0):
                self.add_corruption(corruption_delta)
            self.openness = max(0, min(20, people_to_int(self.openness, 0) + people_to_int(open_delta, 0)))
            return self

        def apply_social_roll(self, limit_friend, friend_chance, inc_decr_friends, limit_corruption, corruption_chance, inc_decr_corruption):
            friend_delta = people_to_int(inc_decr_friends, 0)
            corruption_delta = people_to_int(inc_decr_corruption, 0)
            positive_friend_chance = social_friend_roll_chance(friend_chance, self.code_name, True)
            negative_friend_chance = social_friend_roll_chance(friend_chance, self.code_name, False)
            corruption_roll_chance = max(1, people_to_int(corruption_chance, 1))
            roll_index = 0
            while friend_delta < 0:
                roll_index += 1
                if people_to_int(self.rel, 0) > people_to_int(limit_friend, 0) and procedural_randint(1, negative_friend_chance, "becky_social_friend_down_%s_%s" % (people_to_int(current_game_day(), 0), roll_index)) == 1:
                    self.add_relation(-1, cap=100)
                friend_delta += 1
            while friend_delta > 0:
                roll_index += 1
                if people_to_int(self.rel, 0) < people_to_int(limit_friend, 0) and procedural_randint(1, positive_friend_chance, "becky_social_friend_up_%s_%s" % (people_to_int(current_game_day(), 0), roll_index)) == 1:
                    self.add_relation(1, cap=100)
                friend_delta -= 1
            while corruption_delta < 0:
                roll_index += 1
                if people_to_int(self.corruption, 0) > people_to_int(limit_corruption, 0) and procedural_randint(1, corruption_roll_chance, "becky_social_corruption_down_%s_%s" % (people_to_int(current_game_day(), 0), roll_index)) == 1:
                    self.add_corruption(-1)
                corruption_delta += 1
            while corruption_delta > 0:
                roll_index += 1
                if people_to_int(self.corruption, 0) < people_to_int(limit_corruption, 0) and procedural_randint(1, corruption_roll_chance, "becky_social_corruption_up_%s_%s" % (people_to_int(current_game_day(), 0), roll_index)) == 1:
                    self.add_corruption(1)
                corruption_delta -= 1
            return self

        def finish_talk(self):
            self.talked_today = people_to_int(self.talked_today, 0) + 1
            return self.talked_today

        def talk_count(self):
            return people_to_int(self.talked_today, 0)

        def home_visit_stage(self):
            return people_to_int(self.story_value("visitedhome", 0), 0)

        def home_sex_unlocked(self):
            return people_to_int(self.story_value("HomeSex", 0), 0) > 0

        def sherwood_trade_active(self):
            return people_to_int(self.story_value("TradeOffer", 0), 0) > 0

        def church_after_sermon_event_available(self):
            return (
                church_after_cermon_action_visible()
                and people_to_int(self.story_value("PriestAdvice", 0), 0) > 0
                and self.after_sermon_stage() < 4
                and CheckIfSexEventExist(self.code_name, 99, "Priest") > 0
            )

        def after_sermon_stage(self):
            return people_to_int(self.story_value("after_sermon_stage", 0), 0)

        def set_after_sermon_stage(self, value):
            return self.set_story_value("after_sermon_stage", people_to_int(value, 0))

        def pregnancy_days(self):
            return people_to_int(self.stats.get("pregnancy", 0), 0)

        def is_visibly_pregnant(self):
            return self.pregnancy_days() >= 120

        def can_drink_wine(self):
            return self.pregnancy_days() <= 30

        def record_orgasm_given(self, amount=1):
            self.stats["orgasms_given"] = people_to_int(self.stats.get("orgasms_given", 0), 0) + people_to_int(amount, 1)
            return self.stats["orgasms_given"]

        def store_lover_modest_reaction(self):
            return (people_to_int(self.corruption, 0) <= 45 or people_to_int(self.rel, 0) < 10) and people_to_int(self.corruption, 0) <= 55

        def mark_store_orgasm_today(self):
            return self.set_story_value("last_store_orgasm_day", people_to_int(current_game_day(), 0))

        def apply_pregnancy_check(self, cum_place, repeat_count, dad_name="", is_dude_random=0, dad_name_type=""):
            PregnancyCheck(self.code_name, cum_place, repeat_count, dad_name, is_dude_random, dad_name_type)
            self.stats["sexacts"] = people_to_int(sexacts.get(self.code_name, self.stats.get("sexacts", 0)), 0)
            self.stats["cuminside"] = people_to_int(cuminside.get(self.code_name, self.stats.get("cuminside", 0)), 0)
            self.stats["pregnancy"] = people_to_int(pregnancy.get(self.code_name, self.stats.get("pregnancy", 0)), 0)
            self.stats["pregfather"] = str(pregfather.get(self.code_name, self.stats.get("pregfather", "")) or "")
            return self

        def has_bra(self):
            return str(self.wardrobe.get("current_underwear", {}).get("bra", "") or "") != ""

        def has_panties(self):
            return str(self.wardrobe.get("current_underwear", {}).get("panties", "") or "") != ""

        def set_default_bra(self, item_id):
            self.wardrobe.setdefault("current_underwear", {})["bra"] = str(item_id or "")
            bradef[self.code_name] = str(item_id or "")
            bra[self.code_name] = str(item_id or "")
            return self

        def set_default_panties(self, item_id):
            self.wardrobe.setdefault("current_underwear", {})["panties"] = str(item_id or "")
            pantiesdef[self.code_name] = str(item_id or "")
            panties[self.code_name] = str(item_id or "")
            return self

        def friday_dance_base_ready(self):
            if not friday_dance_slot_is_active():
                return False
            location_now = str(getLocation("becky") or "")
            return (
                location_now in ("FridayDance", "MarketPlace")
                and int(self.var.get("leftdances", 0) or 0) == 0
                and people_to_int(friday_dance_count(), 0) < 5
                and people_to_int(DanceStep, 0) == 0
            )

        def dance_event_conditions_met(self, event_obj):
            partner = str(getattr(event_obj, "partner", "") or "")
            if partner == "mc":
                return self.friday_dance_base_ready()
            return False

        def pregnancy_stage(self):
            days = people_to_int(self.stats.get("pregnancy", 0), 0)
            if days <= 0:
                return "none"
            if days < 120:
                return "early"
            if days < 210:
                return "visible"
            if days < 270:
                return "late"
            return "birth_due"

        def install_schedule(self):
            name = self.code_name
            npc_interval_schedule_load_file(name)
            return self

        def install_schedule(self):
            name = self.code_name
            npc_interval_schedule_load_file(name)
            return self

        def install_schedule(self):
            name = self.code_name
            npc_interval_schedule_load_file(name)
            return self

define BeckyStaticData = BeckyData()
default Becky = BeckyInfo()

label InitBecky:
    python:
        GirlName = Becky.code_name
        peopleData[GirlName] = BeckyStaticData
        Becky.initialize_new_game_state()
        peopleInfo[GirlName] = Becky
        if Becky not in girls:
            girls.append(Becky)
        Becky.install_schedule()
    return
