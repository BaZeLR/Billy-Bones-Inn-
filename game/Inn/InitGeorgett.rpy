label InitGeorgett:
    python:
        knowsMC["georgett"] = False
        # Initialize Georgett's attributes
        GirlName = 'georgett'

        RealName[GirlName] = 'Жоржетта'
        RealName2[GirlName] = 'Жоржетты'
        RealName3[GirlName] = 'Жоржетте'
        age_girls[GirlName] = 28
        DateOfBirth[GirlName] = calendar_make_birth_record(age_girls[GirlName])
        kids[GirlName] = 4
        beauty[GirlName] = 67
        sluttiness[GirlName] = 80
        sexacts[GirlName] = 6452
        cuminside[GirlName] = 3276
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 5
        CurrentLoc[GirlName] = 'PortStreets'
        PussyWetStart[GirlName] = 30
        virginity[GirlName] = False

        # Description and default dress
        girltextdesc[GirlName] = 'Жоржетта Брюно - молодая женщина, не очень высокого роста, чуть пухленькая и с большой налитой грудью. Она белокура и кареглаза. Ее внешность и повадки не дают никаких сомнений в том, что она выбрала себе путь отнюдь не монашки.'
        dressdefault[GirlName] = 'slutdress'

        # Default clothing
        bradef[GirlName] = ''
        pantiesdef[GirlName] = ''
        legsdef[GirlName] = 'blackstockings'
        shoesdef[GirlName] = 'highshoes'
        topdress[GirlName] = DressTopPart.get(dressdefault[GirlName], '')
        bottomdress[GirlName] = DressBottomPart.get(dressdefault[GirlName], '')
        bra[GirlName] = bradef[GirlName]
        panties[GirlName] = pantiesdef[GirlName]
        legs[GirlName] = legsdef[GirlName]
        shoes[GirlName] = shoesdef[GirlName]

        _georgett_dresses = []
        if dressdefault[GirlName]:
            _georgett_dresses.append(dressdefault[GirlName])
        if pantiesdef[GirlName]:
            _georgett_dresses.append(pantiesdef[GirlName])
        if bradef[GirlName]:
            _georgett_dresses.append(bradef[GirlName])
        if legsdef[GirlName]:
            _georgett_dresses.append(legsdef[GirlName])
        setattr(renpy.store, GirlName + 'Dresses', _georgett_dresses)

        # Skills
        cooking[GirlName] = 50
        cleaning[GirlName] = 20
        waitress[GirlName] = 50

        # Job-related data
        otkroven[GirlName] = 0
        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 0
        jobwaitress[GirlName] = 0
        jobHallAvail[GirlName] = 0
        jobWhoreAvail[GirlName] = 0
        jobGloryHoleAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0
        jobwhoreTommorow[GirlName] = 0
        jobgloryholeTommorow[GirlName] = 0
        Friends[GirlName] = 0

        # Character-specific variables (TXT parity)
        GeorgettVar['seeclients'] = 0
        GeorgettVar['askclients'] = 0
        GeorgettVar['askkids'] = 0
        GeorgettVar['askparents'] = 0
        GeorgettVar['askpregnancy'] = 0
        GeorgettVar['asksex'] = 0
        GeorgettVar['TellAboutEddieMomSex'] = 0
        GeorgettVar['foundinchurch'] = 0
        GeorgettVar['fuckinchurch'] = 0
        GeorgettVar['lizasawinchurch'] = 0
        GeorgettVar['georgettadmit'] = 0
        GeorgettVar['churchgeorgettadmit'] = 0
        GeorgettVar['churchlizaadmit'] = 0
        GeorgettVar['SawChurchAfterCermon'] = 0
        GeorgettVar['TalkChurchAfterCermon'] = 0
        GeorgettVar['TalkChurchAfterCermonLiza'] = 0
        GeorgettVar['GloryHoleExplained'] = 0
        GeorgettVar['GloryHoleAgreed'] = 0
        ChurchAfterCermon[GirlName + 'AC'] = 0
        GiftPreferences[GirlName] = ["drink_ale_001", "wild_rose_001", "soap_001", "libido_tincture_001", "ethanol_001"]

    call WhoreNextDayClients(GirlName, 3, 3)
    return
