# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def irma_pick_image_path(*candidates):
        for candidate in candidates:
            path = str(candidate or "").strip()
            if path and renpy.loadable(path):
                return path
        return "images/irma/portraits/portrait3.png"

    def irma_default_portrait_path():
        return "images/irma/portraits/portrait2.png"

    def irma_card_portrait_path():
        if int(Friends.get("irma", 0) or 0) >= 5:
            return "images/irma/portraits/flirts.png"
        return irma_default_portrait_path()

    def irma_working_picture_path():
        return "images/irma/portraits/portrait3.png"

    def irma_talk_picture_path():
        return "images/irma/talks.png"

    def irma_measuring_picture_path():
        return "images/irma/measure/measure0.png"

    def irma_measure_picture_path(stage=0):
        try:
            stage_id = int(stage or 0)
        except Exception:
            stage_id = 0
        stage_id = max(0, min(stage_id, 3))
        measure_paths = [
            "images/irma/measure/measure0.png",
            "images/irma/measure/measure1.png",
            "images/irma/measure/measure2.jpg",
            "images/irma/measure/measure3.jpg",
        ]
        return measure_paths[stage_id]

    def irma_flirting_picture_path():
        return "images/irma/flirts.png"

    def irma_sex_picture_path(stage=0):
        try:
            stage_id = int(stage or 0)
        except Exception:
            stage_id = 0
        return irma_pick_image_path(
            "images/irma/sex/sex" + str(stage_id) + ".png",
            "images/irma/sex/sex" + str(stage_id) + ".jpg",
            "images/irma/sex/topless.jpg",
        )

    def irma_clara_fitting_picture_path(stage=0):
        try:
            stage_id = int(stage or 0)
        except Exception:
            stage_id = 0
        clara_paths = [
            "images/irma/clara_visit/tailorShop_clara.png",
            "images/irma/clara_visit/tailorShop_clara_1.png",
            "images/irma/clara_visit/tailor_shop_clara_2.png",
            "images/irma/clara_visit/tailor_shop_clara_3.png",
        ]
        return clara_paths[max(0, min(stage_id, len(clara_paths) - 1))]

    def irma_shop_end_picture_path():
        return "images/irma/portraits/portrait2.png"

    def irma_angry_picture_path():
        return "images/irma/portraits/portrait1.png"

    def irma_story_defaults():
        return {
            "DeniedMinetMoney": 0,
            "KnowInfertility": 0,
            "KnowDad": 0,
            "KnowMom": 0,
            "KnowSlut": 0,
        }

    class IrmaData(PeopleData):
        code_name = "irma"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Ирма",
                fullname="Ирма Фараго",
                genitive="Ирмы",
                dative="Ирме",
                default_location="DressShop",
                portrait="images/irma/portraits/portrait2.png",
                description="Ирма Фараго - молодая женщина, владелица небольшой лавки. Ее хрупкое телосложение, высокая и очень стройная фигура, светлая, почти белоснежная кожа, заостренные, немного резкие черты лица и выбивающиеся из под русых волос слегка заостренные ушки выдают ее полуэльфийское происхождение.",
                gift_preferences=["lavender_001", "wild_rose_001", "soap_001"],
            )
            self.birth_date = {"day": 12, "period": 6, "cycle": 1078}
            self.card_image = "images/irma/portraits/portrait2.png"
            self.schedule_source = "schedules/irma.json"

    class IrmaInfo(Girl):
        """Irma runtime: tailor shop, measuring scenes, relationship state."""
        unknown_name = "Незнакомка"

        def __init__(self):
            super().__init__("irma")
            self.code_name = "irma"
            self.data = IrmaStaticData
            self.rel = 0
            self.relationship = self.rel
            self.openness = 0
            self.corruption = 45
            self.known = True
            self.energy = 100
            self.energy_max = 100
            self.rebellion = 0
            self.anger_with_player = 0
            self.fun = 0
            self.trust = 0
            self.fear = 0
            self.mana = 20
            self.mana_corrupted = False
            self.mood = "neutral"
            self.talked_today = 0
            self.flirted_today = 0
            self.gifted_today = 0
            self.asked_today = 0
            self.fucked_today = 0
            self.drunk = 0
            self.stats = {
                "kids": 0,
                "beauty": 65,
                "sexacts": 1876,
                "cuminside": 948,
                "pregnancy": 0,
                "pregfather": "",
                "ConceptionChance": 0,
                "PussyWetStart": 25,
                "virginity": False,
                "breastfeed": 0,
            }
            self.skills = {
                "cooking": 30,
                "cleaning": 30,
                "waitress": 35,
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
            self.gift_preferences = list(IrmaStaticData.gift_preferences)
            self.schedule_source = IrmaStaticData.schedule_source
            self.current_location = "DressShop"
            self.talk_preferences = {
                "favorite_topics": ["fashion", "tailoring", "family", "secrets", "work"],
                "blocked_topics": [],
            }
            self.wardrobe = {
                "owned": ["openworkdress", "simplepanties", "redstockings", "simpleshoes"],
                "gifted": [],
                "current_dress": "openworkdress",
                "current_underwear": {
                    "bra": "",
                    "panties": "simplepanties",
                    "legs": "redstockings",
                    "shoes": "simpleshoes",
                },
            }
            self.var = {}
            self.ensure_story_defaults()

        def update(self):
            super(IrmaInfo, self).update()
            self.data = IrmaStaticData
            self.relationship = self.rel
            self.sync_from_irma_maps()
            return self

        def ensure_story_defaults(self):
            if not isinstance(self.var, dict):
                self.var = {}
            for key, value in irma_story_defaults().items():
                self.var.setdefault(key, value)
            return self.var

        def sync_from_irma_maps(self):
            self.var = IrmaVar
            self.rel = people_to_int(Friends.get("irma", self.rel), self.rel)
            self.relationship = self.rel
            self.openness = people_to_int(otkroven.get("irma", self.openness), self.openness)
            self.corruption = people_to_int(sluttiness.get("irma", self.corruption), self.corruption)
            self.drunk = people_to_int(Drunk.get("irma", self.drunk), self.drunk)
            self.talked_today = people_to_int(TalkedToday.get("irma", self.talked_today), self.talked_today)
            self.flirted_today = people_to_int(FlirtedToday.get("irma", self.flirted_today), self.flirted_today)
            self.gifted_today = people_to_int(GiftedToday.get("irma", self.gifted_today), self.gifted_today)
            self.asked_today = people_to_int(AskedToday.get("irma", self.asked_today), self.asked_today)
            self.fucked_today = people_to_int(FuckedToday.get("irma", self.fucked_today), self.fucked_today)
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
                if "irma" in table:
                    self.stats[stat_key] = table.get("irma")
            for table, job_key in [
                (jobkitchen, "jobkitchen"),
                (jobcleaning, "jobcleaning"),
                (jobwaitress, "jobwaitress"),
                (jobHallAvail, "jobHallAvail"),
                (jobWhoreAvail, "jobWhoreAvail"),
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                if "irma" in table:
                    self.jobs[job_key] = table.get("irma")
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                if "irma" in table:
                    self.skills[skill_key] = table.get("irma")
            self.ensure_story_defaults()
            return self

        def sync_irma_maps(self):
            name = self.code_name
            RealName[name] = self.data.cname
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
            FlirtedToday[name] = people_to_int(self.flirted_today, 0)
            GiftedToday[name] = people_to_int(self.gifted_today, 0)
            AskedToday[name] = people_to_int(self.asked_today, 0)
            FuckedToday[name] = people_to_int(self.fucked_today, 0)
            self.location = str(self.current_location or "DressShop")
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
                (jobwhore, "jobwhore"),
                (jobgloryhole, "jobgloryhole"),
            ]:
                table[name] = self.jobs.get(job_key, 0)
            for table, skill_key in [(cooking, "cooking"), (cleaning, "cleaning"), (waitress, "waitress")]:
                table[name] = self.skills.get(skill_key, 0)
            self.ensure_story_defaults()
            for key, value in self.var.items():
                IrmaVar[key] = value
            return self

        def initialize_new_game_state(self):
            self.var = IrmaVar
            self.ensure_story_defaults()
            self.sync_irma_maps()
            return self

        def install_schedule(self):
            npc_interval_schedule_load_file(self.code_name)
            npc_schedule_sync_currentloc(self.code_name)
            return self

define IrmaStaticData = IrmaData()
default Irma = IrmaInfo()

label InitIrma:
    python:
        GirlName = Irma.code_name
        peopleData[GirlName] = IrmaStaticData
        Irma.initialize_new_game_state()
        peopleInfo[GirlName] = Irma
        if Irma not in girls:
            girls.append(Irma)
        Irma.install_schedule()
    return
