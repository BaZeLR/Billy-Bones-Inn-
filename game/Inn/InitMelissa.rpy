label InitMelissa:
    python:
        # Initialize Melissa's attributes
        GirlName = 'melissa'

        RealName[GirlName] = 'Мелисса'
        RealName2[GirlName] = 'Мелиссы'
        RealName3[GirlName] = 'Мелиссе'
        DateOfBirth[GirlName] = renpy.random.randint(15, 350)
        age_girls[GirlName] = 18
        kids[GirlName] = 0
        beauty[GirlName] = 55
        sluttiness[GirlName] = 3
        sexacts[GirlName] = 0
        cuminside[GirlName] = 0
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 15
        CurrentLoc[GirlName] = 'TavernMain'
        PussyWetStart[GirlName] = 10
        virginity[GirlName] = True

        # Description and default dress
        girltextdesc[GirlName] = 'Мелисса - молодая девушка. В ее сложении немного проступают восточные черты. Она немного отличается от остальных работниц трактира. У нее оливкового цвета кожа, черные глаза, волосы цвета вороньего крыла и полные, похожие на мячи груди размера С.'
        dressdefault[GirlName] = 'workdress'

        # Default clothing
        bradef[GirlName] = 'simplebra'
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = ''
        shoesdef[GirlName] = 'simpleshoes'

        # Skills
        cooking[GirlName] = 30
        cleaning[GirlName] = 40
        waitress[GirlName] = 30

        # Job-related data
        otkroven[GirlName] = 0
        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 1
        jobwaitress[GirlName] = 1
        Friends[GirlName] = 5
        jobHallAvail[GirlName] = 1
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0

        # Custom variables
        MelissaVar['MomDressComplaint'] = 0
        MelissaVar['AskedAboutClaraDay'] = -1
        GiftPreferences[GirlName] = ["soap_001", "lavender_001", "wild_rose_001", "energy_tea_001", "drink_ale_001", "libido_tincture_001"]

    return
