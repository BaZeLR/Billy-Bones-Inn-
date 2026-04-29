# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def irma_pick_image_path(*candidates):
        for candidate in candidates:
            path = str(candidate or "").strip()
            if path and renpy.loadable(path):
                return path
        return "images/irma/portraits/portrait1.jpg"

    def irma_default_portrait_path():
        return irma_pick_image_path(
            "images/irma/Irma_portrait.png",
            "images/irma/portraits/portrait1.jpg",
        )

    def irma_card_portrait_path():
        if int(Friends.get("irma", 0) or 0) >= 5:
            return irma_pick_image_path(
                "images/irma/Irma_sitting _portrait.png",
                "images/irma/Irma_portrait.png",
                "images/irma/portraits/portrait2.jpg",
            )
        return irma_default_portrait_path()

    def irma_working_picture_path():
        return irma_pick_image_path(
            "images/irma/Irma_working_portrait.png",
            "images/irma/Irma_portrait.png",
            "images/irma/portraits/portrait1.jpg",
        )

    def irma_talk_picture_path():
        return irma_pick_image_path(
            "images/irma/Irma_talks.png",
            "images/irma/Irma_portrait.png",
            "images/irma/portraits/portrait1.jpg",
        )

    def irma_measuring_picture_path():
        return irma_pick_image_path(
            "images/irma/Irma_mesure_standing.png",
            "images/irma/irma_measuring.png",
            "images/irma/Irma_working_portrait.png",
            "images/irma/portraits/portrait1.jpg",
        )

    def irma_flirting_picture_path():
        return irma_pick_image_path(
            "images/irma/Irma_flirting pose.png",
            "images/irma/Irma_talks.png",
            "images/irma/portraits/smile.jpg",
            "images/irma/portraits/portrait2.jpg",
        )

    def irma_angry_picture_path():
        return irma_pick_image_path(
            "images/irma/portraits/angry.jpg",
            "images/irma/Irma_talks.png",
            "images/irma/Irma_portrait.png",
            "images/irma/portraits/portrait1.jpg",
        )

label InitIrma:
    python:
        knowsMC["irma"] = True
        # Initialize Irma's attributes
        GirlName = 'irma'

        RealName[GirlName] = 'Ирма'
        RealName2[GirlName] = 'Ирмы'
        RealName3[GirlName] = 'Ирме'
        age_girls[GirlName] = 22
        DateOfBirth[GirlName] = calendar_make_birth_record(age_girls[GirlName])
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
