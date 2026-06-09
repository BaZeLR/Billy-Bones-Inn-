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

label InitIrma:
    python:
        knowsMC["irma"] = True
        # Initialize Irma's attributes
        GirlName = 'irma'

        RealName[GirlName] = 'Ирма'
        RealName2[GirlName] = 'Ирмы'
        RealName3[GirlName] = 'Ирме'
        age_girls[GirlName] = 22
        kids[GirlName] = 0
        beauty[GirlName] = 65
        sluttiness[GirlName] = 45
        sexacts[GirlName] = 1876
        cuminside[GirlName] = 948
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 0
        PussyWetStart[GirlName] = 25
        virginity[GirlName] = False

        # Description and default dress
        girltextdesc[GirlName] = 'Ирма Фараго - молодая женщина, владелица небольшой лавки. Ее хрупкое телосложение, высокая и очень стройная фигура, светлая, почти белоснежная кожа, заостренные, немного резкие черты лица и выбивающиеся из под русых волос слегка заостренные ушки выдают ее полуэльфийское происхождение.'
        dressdefault[GirlName] = 'openworkdress'

        # Default clothing
        bradef[GirlName] = ''
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = 'redstockings'
        shoesdef[GirlName] = 'simpleshoes'

        # Skills
        cooking[GirlName] = 30
        cleaning[GirlName] = 30
        waitress[GirlName] = 35

        # Job-related data
        otkroven[GirlName] = 0
        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 0
        jobwaitress[GirlName] = 0
        Friends[GirlName] = 0
        jobHallAvail[GirlName] = 0
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0

        # Custom variables
        IrmaVar['DeniedMinetMoney'] = 0
        IrmaVar['KnowInfertility'] = 0
        IrmaVar['KnowDad'] = 0
        IrmaVar['KnowMom'] = 0
        IrmaVar['KnowSlut'] = 0
        GiftPreferences[GirlName] = ["lavender_001", "wild_rose_001", "soap_001"]
        CurrentLoc[GirlName] = "DressShop"
        npc_schedule_set(GirlName, [
            NPCScheduleEntry(location="DressShop", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0, 1, 2], awake=True, talkable=True, priority=100, label="tailor_shop"),
        ])
        npc_schedule_sync_currentloc(GirlName)

    return

# Auto-attach .var for PeopleInfo consistency (requested)
init python:
    if 'peopleInfo' not in dir() or not isinstance(peopleInfo, dict):
        peopleInfo = {}
    # Per user request: class Irma(Girl) defined in game/NPC/Girls/Irma/InitIrma.rpy
    if 'irma' not in peopleInfo or not isinstance(peopleInfo.get('irma'), Irma):
        class Irma(Girl):
            """Irma."""
            def __init__(self, name="irma", **kwargs):
                super().__init__(name, **kwargs)
                if 'IrmaVar' in dir() and isinstance(IrmaVar, dict):
                    self.var = IrmaVar
                    self.promote_from_var(IrmaVar)
        peopleInfo['irma'] = Irma(var=IrmaVar if 'IrmaVar' in dir() else {})
    else:
        if 'IrmaVar' in dir() and isinstance(IrmaVar, dict):
            peopleInfo['irma'].var = IrmaVar
    if 'girls' not in dir() or not isinstance(girls, list):
        girls = []
    if peopleInfo.get('irma') not in girls:
        girls.append(peopleInfo['irma'])
