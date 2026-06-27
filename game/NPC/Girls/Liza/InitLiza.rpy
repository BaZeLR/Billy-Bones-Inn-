# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitLiza:
    python:
        GirlName = Liza.code_name
        peopleData[GirlName] = LizaStaticData
        Liza.initialize_new_game_state()
        peopleInfo[GirlName] = Liza
        if Liza not in girls:
            girls.append(Liza)

    return

init python:
    def liza_story_defaults():
        return {
            "SawChurchAfterCermon": 0,
            "TalkChurchAfterCermon": 0,
            "TalkChurchAfterCermonGeorgett": 0,
            "ProstStart": 0,
            "seeclients": 0,
            "askclients": 0,
            "askpregnancy": 0,
            "asksex": 0,
            "after_sermon_stage": 0,
            "GloryHoleMentioned": 0,
            "GloryHoleAsked": 0,
        }

    class LizaData(PeopleData):
        code_name = "liza"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Лизетта",
                fullname="Лизетта",
                genitive="Лизетты",
                dative="Лизетте",
                default_location="PortStreets",
                description="Лизетта Брюно - худенькая молоденькая мулатка, ростом чуть меньше 145 сантиметров. У нее шоколадная кожа, зеленые глаза и маленькие грудки. Ее длинные темные волосы собранны в две косички. У нее стройные длинные ножки и немного оттопыреная попка, привлекающая мужские взгляды.",
                gift_preferences=["berries_001", "wild_rose_001", "soap_001"],
            )
            self.birth_date = {"day": 1, "period": 1, "cycle": 1082}
            self.schedule_source = "schedules/liza.json"

    class LizaInfo(Girl):
        """Lizette runtime: port work, tavern relocation, church story, pregnancy state."""
        unknown_name = "Молодая женщина"

        def __init__(self):
            super().__init__("liza")
            self.code_name = "liza"
            self.data = LizaStaticData
            self.uses_own_var_state = True
            self.rel = 0
            self.relationship = self.rel
            self.openness = 0
            self.corruption = 35
            self.known = True
            self.hired = False
            self.talked_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.stats = {
                "kids": 0,
                "beauty": 72,
                "sexacts": 89,
                "cuminside": 7,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 10,
                "PussyWetStart": 20,
                "virginity": False,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 20,
                "cleaning": 20,
                "waitress": 25,
            }
            self.jobs = {
                "jobkitchen": 0,
                "jobcleaning": 0,
                "jobwaitress": 0,
                "jobHallAvail": 0,
                "jobWhoreAvail": 0,
                "jobGloryHoleAvail": 0,
                "jobwhore": 0,
                "jobgloryhole": 0,
                "jobwhoreTommorow": 0,
                "jobgloryholeTommorow": 0,
            }
            self.gift_preferences = list(LizaStaticData.gift_preferences)
            self.schedule_source = LizaStaticData.schedule_source
            self.current_location = "PortStreets"
            self.talk_preferences = {
                "favorite_topics": ["clients", "sex", "pregnancy", "family", "work"],
                "blocked_topics": ["flirt"],
            }
            self.wardrobe = {
                "owned": ["minidress", "simplepanties", "blackstockings", "highshoes"],
                "gifted": [],
                "current_dress": "minidress",
                "current_underwear": {
                    "bra": "",
                    "panties": "simplepanties",
                    "legs": "blackstockings",
                    "shoes": "highshoes",
                },
            }
            self.var = {}
            self.ensure_story_defaults()

        def update(self):
            super(LizaInfo, self).update()
            self.data = LizaStaticData
            self.relationship = self.rel
            self.sync_from_shared_state()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in liza_story_defaults().items():
                self.var.setdefault(key, value)
            return self.var

        def sync_from_shared_state(self):
            self.rel = people_to_int(Friends.get("liza", self.rel), self.rel)
            self.relationship = self.rel
            self.openness = people_to_int(otkroven.get("liza", self.openness), self.openness)
            self.corruption = people_to_int(sluttiness.get("liza", self.corruption), self.corruption)
            self.drunk = people_to_int(Drunk.get("liza", self.drunk), self.drunk)
            self.talked_today = people_to_int(TalkedToday.get("liza", self.talked_today), self.talked_today)
            self.gifted_today = people_to_int(GiftedToday.get("liza", self.gifted_today), self.gifted_today)
            self.asked_today = people_to_int(AskedToday.get("liza", self.asked_today), self.asked_today)
            self.fucked_today = people_to_int(FuckedToday.get("liza", self.fucked_today), self.fucked_today)
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
                if "liza" in table:
                    self.stats[stat_key] = table.get("liza")
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobGloryHoleAvail, "jobGloryHoleAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
                (jobwhoreTommorow, "jobwhoreTommorow"),
                (jobgloryholeTommorow, "jobgloryholeTommorow"),
            ]:
                if "liza" in table:
                    self.jobs[job_key] = table.get("liza")
            self.hired = people_to_int(self.jobs.get("jobWhoreAvail", 0), 0) > 0
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                if "liza" in table:
                    self.skills[skill_key] = table.get("liza")
            self.ensure_story_defaults()
            return self

        def sync_shared_state(self):
            name = self.code_name
            RealName[name] = self.data.fullname
            RealName2[name] = self.data.genitive
            RealName3[name] = self.data.dative
            DateOfBirth[name] = dict(self.data.birth_date)
            girltextdesc[name] = self.data.description
            knowsMC[name] = bool(self.known)
            Friends[name] = people_to_int(self.rel, 0)
            otkroven[name] = people_to_int(self.openness, 0)
            sluttiness[name] = people_to_int(self.corruption, 0)
            Drunk[name] = people_to_int(self.drunk, 0)
            TalkedToday[name] = people_to_int(self.talked_today, 0)
            GiftedToday[name] = people_to_int(self.gifted_today, 0)
            AskedToday[name] = people_to_int(self.asked_today, 0)
            FuckedToday[name] = people_to_int(self.fucked_today, 0)
            self.location = str(self.current_location or "PortStreets")
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
                (jobGloryHoleAvail, "jobGloryHoleAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
                (jobwhoreTommorow, "jobwhoreTommorow"),
                (jobgloryholeTommorow, "jobgloryholeTommorow"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            self.hired = people_to_int(self.jobs.get("jobWhoreAvail", 0), 0) > 0
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                table[name] = self.skills.get(skill_key, 0)
            self.ensure_story_defaults()
            return self

        def initialize_new_game_state(self):
            self.ensure_story_defaults()
            self.sync_shared_state()
            return self

        def reset_daily(self, full=False):
            super(LizaInfo, self).reset_daily(full)
            self.talked_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.var["after_sermon_stage"] = 0
            self.var["portstreet_clients_seen_today"] = 0
            self.sync_shared_state()
            return self

        def story_value(self, key, default=0):
            return self.ensure_story_defaults().get(key, default)

        def set_story_value(self, key, value):
            self.ensure_story_defaults()[key] = value
            self.sync_shared_state()
            return value

        def talk_count(self):
            return people_to_int(Talked.get(self.code_name, 0), 0)

        def can_talk_today(self, limit=2):
            return self.talk_count() < people_to_int(limit, 2)

        def add_relation(self, amount=1, cap=20):
            self.rel = max(0, min(people_to_int(cap, 20), people_to_int(self.rel, 0) + people_to_int(amount, 0)))
            self.relationship = self.rel
            self.sync_shared_state()
            return self.rel

        def finish_talk(self):
            self.talked_today = people_to_int(self.talked_today, 0) + 1
            Talked[self.code_name] = self.talk_count() + 1
            self.sync_shared_state()
            return Talked[self.code_name]

        def mark_asked_topic(self, topic_flag, relation_gain=1):
            flag = str(topic_flag or "")
            first_time = people_to_int(self.story_value(flag, 0), 0) == 0
            if first_time:
                self.set_story_value(flag, 1)
                if relation_gain:
                    self.add_relation(relation_gain)
            self.asked_today = people_to_int(self.asked_today, 0) + 1
            self.sync_shared_state()
            return first_time

        def can_ask_topic(self, topic):
            key = str(topic or "")
            if not self.can_talk_today():
                return False
            rel_value = people_to_int(self.rel, 0)
            if key == "clients":
                return people_to_int(self.story_value("seeclients", 0), 0) > 0 and rel_value >= 5
            if key in ("sex", "pregnancy"):
                return people_to_int(self.story_value("askclients", 0), 0) > 0 and rel_value >= 5
            if key == "georgett_gerhard":
                return (
                    people_to_int(Georgett.story_value("SawChurchAfterCermon", 0), 0) > 0
                    and rel_value >= 5
                    and people_to_int(self.story_value("TalkChurchAfterCermonGeorgett", 0), 0) == 0
                )
            if key == "work":
                return self.can_work_tavern()
            if key == "holglor":
                return self.can_work_tavern() and people_to_int(self.story_value("GloryHoleAsked", 0), 0) == 0 and people_to_int(self.story_value("GloryHoleMentioned", 0), 0) == 1
            return False

        def getLocation(self, wday=None, hour=None):
            location_value = super(LizaInfo, self).getLocation(wday, hour)
            return location_value

        def can_work_portstreets(self):
            return people_to_int(self.story_value("ProstStart", 0), 0) > 0 and not self.can_work_tavern()

        def portstreet_work_hour(self):
            calendar_v2.sync_state()
            return people_to_int(calendar_v2.hour, 0) >= 19 and people_to_int(week, 0) != 5

        def portstreet_work_active(self):
            return (
                self.can_work_portstreets()
                and str(self.getLocation() or "") == "PortStreets"
                and Georgett.portstreet_story_unblocked()
                and self.portstreet_work_hour()
            )

        def set_portstreet_visible(self, visible=True):
            self.var["portstreet_visible_now"] = 1 if visible else 0
            return bool(visible)

        def portstreet_visible_now(self):
            return people_to_int(self.var.get("portstreet_visible_now", 0), 0) > 0

        def portstreet_client_event_available(self):
            return self.portstreet_work_active() and people_to_int(self.var.get("portstreet_clients_seen_today", 0), 0) == 0 and CheckIfSexEventExist(self.code_name, 3, "Prostitution") > 0

        def mark_portstreet_clients_seen(self):
            self.var["portstreet_clients_seen_today"] = 1
            return self.set_story_value("seeclients", 1)

        def can_work_tavern(self):
            self.hired = people_to_int(self.jobs.get("jobWhoreAvail", 0), 0) > 0 or people_to_int(jobWhoreAvail.get("liza", 0), 0) > 0
            return self.hired

        def set_hired(self, hired=True):
            self.hired = bool(hired)
            self.jobs["jobWhoreAvail"] = 1 if self.hired else 0
            self.jobs["jobwhore"] = 1 if self.hired else 0
            self.current_location = "TavernMain" if self.hired else "PortStreets"
            self.sync_shared_state()
            return self.hired

        def can_use_gloryhole(self):
            return people_to_int(self.jobs.get("jobGloryHoleAvail", 0), 0) > 0 or people_to_int(jobGloryHoleAvail.get("liza", 0), 0) > 0

        def can_ask_about_clients(self):
            return people_to_int(self.story_value("seeclients", 0), 0) > 0 and people_to_int(self.rel, 0) >= 5

        def can_ask_about_priest(self):
            return people_to_int(self.story_value("SawChurchAfterCermon", 0), 0) > 0

        def can_trigger_after_sermon_event(self):
            return self.can_trigger_church_service_event()

        def can_trigger_church_service_event(self):
            return people_to_int(Georgett.story_value("churchlizaadmit", 0), 0) > 0

        def after_sermon_stage(self):
            return people_to_int(self.story_value("after_sermon_stage", 0), 0)

        def set_after_sermon_stage(self, value):
            return self.set_story_value("after_sermon_stage", people_to_int(value, 0))

        def church_after_sermon_event_available(self):
            self.sync_from_shared_state()
            return (
                church_after_cermon_action_visible()
                and self.can_trigger_church_service_event()
                and self.after_sermon_stage() < 4
                and CheckIfSexEventExist(self.code_name, 99, "Priest") > 0
            )

        def can_schedule_dress_shop_visit(self):
            return self.can_work_tavern() and people_to_int(self.rel, 0) > 5

        def can_schedule_barber_visit(self):
            return self.can_work_tavern()

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

define LizaStaticData = LizaData()
default Liza = LizaInfo()
