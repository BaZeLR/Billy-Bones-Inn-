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
        if int(people.get_info("irma").rel or 0) >= 5:
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

    class IrmaData(PeopleData):
        code_name = "irma"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Ирма",
                fullname="Ирма Фараго",
                genitive="Ирмы",
                dative="Ирме",
                default_location="",
                portrait="images/irma/portraits/portrait2.png",
                description="Ирма Фараго - молодая женщина, владелица небольшой лавки. Ее хрупкое телосложение, высокая и очень стройная фигура, светлая, почти белоснежная кожа, заостренные, немного резкие черты лица и выбивающиеся из под русых волос слегка заостренные ушки выдают ее полуэльфийское происхождение.",
                gift_preferences=["lavender_001", "wild_rose_001", "soap_001"],
            )
            self.birth_date = {"day": 12, "period": 6, "cycle": 1078}
            self.card_image = "images/irma/portraits/portrait2.png"
            self.schedule_source = "schedules/irma.json"

    class IrmaInfo(Girl):
        """Irma runtime: tailor shop, measuring scenes, relationship state."""
        talk_label = "IntIrmaTalk"
        unknown_name = "Незнакомка"

        def __init__(self):
            super().__init__("irma")
            self.code_name = "irma"
            self.data = IrmaStaticData
            self.rel = 0
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
            self.extra_fee_refused = False
            self.infertility_known = False
            self.father_story_known = False
            self.mother_story_known = False
            self.sexual_history_known = False
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
        def update(self):
            super(IrmaInfo, self).update()
            self.data = IrmaStaticData
            return self

define IrmaStaticData = IrmaData()
default Irma = IrmaInfo()

label InitIrma:
    python:
        people.register(IrmaStaticData, Irma)
    return
