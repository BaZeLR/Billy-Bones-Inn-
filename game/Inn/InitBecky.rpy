label InitBecky:
    python:
        # Initialize Becky's attributes
        GirlName = 'becky'

        RealName[GirlName] = 'Бекки'
        RealName2[GirlName] = 'Бекки'
        RealName3[GirlName] = 'Бекки'
        DateOfBirth[GirlName] = renpy.random.randint(15, 350)
        age_girls[GirlName] = 36
        kids[GirlName] = 5
        beauty[GirlName] = 45
        sluttiness[GirlName] = 25
        sexacts[GirlName] = 5352
        cuminside[GirlName] = 3593
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 5
        PussyWetStart[GirlName] = 25
        virginity[GirlName] = False

        # Description and default dress
        girltextdesc[GirlName] = 'Вдова Блэнкеншип, для друзей Бекки, высокая рыжеволосая женщина с полной грудью, чуть младше сорока лет.'
        dressdefault[GirlName] = 'openworkdress'

        # Default clothing
        bradef[GirlName] = 'simplebra'
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = 'blackstockings'
        shoesdef[GirlName] = 'simpleshoes'

        # Skills
        cooking[GirlName] = 70
        cleaning[GirlName] = 50
        waitress[GirlName] = 40

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
        BeckyVar['leftdances'] = 0
        BeckyVar['danceinvitehome'] = 0
        BeckyVar['visitedhome'] = 0
        BeckyVar['husbandtalk'] = 0
        BeckyVar['eddietalk'] = 0
        BeckyVar['SawIngaFuck'] = 0
        BeckyVar['IngaSexGreet'] = 0
        BeckyVar['VisitScolded'] = 0
        BeckyVar['TodayFrontSexCheck'] = 0
        BeckyVar['HomeSex'] = 0
        BeckyVar['EddieGeorg'] = 0
        BeckyVar['EddieWhoreHome'] = 0
        BeckyVar['BeckyOpenMinet'] = 0
        BeckyVar['TimesVisited'] = 0
        BeckyVar['TalkAboutEddie'] = 0
        BeckyVar['GeorgMention'] = 0
        BeckyVar['EddieIntrReact'] = 0
        BeckyVar['PriestAdvice'] = 0
        BeckyVar['GerhardBeckyTalk'] = 0
        BeckyVar['AskedEddieFuck'] = 0
        BeckyVar['EddieTryToFuck'] = 0
        BeckyVar['EddieFailures'] = 0
        BeckyVar['EddieRobbedDay'] = 0
        BeckyVar['KnowSherwood'] = 0
        BeckyVar['SherwoodSuspect'] = 0
        BeckyVar['TradeOffer'] = 0
        BeckyVar['SherwoodWarn'] = 0
        BeckyVar['AskTradeElf'] = 0
        BeckyVar['TradeOfferText'] = ''
        BeckyVar['FingalClarify'] = 0
        BeckyVar['AdmitSherwood'] = 0
        BeckyVar['RobbedByRobin'] = 0
        BeckyVar['ConsoleRobbery'] = 0
        BeckyVar['SandraKitchenVisitMonth'] = 0
        GiftPreferences[GirlName] = ["soap_001", "wild_rose_001", "pig_lard_001", "libido_tincture_001", "drink_ale_001"]

    return

init python:
    def becky_monthly_sandra_kitchen_visit_due(month_value=None, day_value=None, time_slot=None):
        month_now = int(month if month_value is None else month_value or 0)
        day_now = int(day if day_value is None else day_value or 0)
        time_now = int(time if time_slot is None else time_slot or 0)
        if time_now != 1 or day_now != 12:
            return False
        return int(BeckyVar.get("SandraKitchenVisitMonth", 0) or 0) != month_now

    def becky_tavern_visit_active(month_value=None, day_value=None, time_slot=None):
        month_now = int(month if month_value is None else month_value or 0)
        day_now = int(day if day_value is None else day_value or 0)
        time_now = int(time if time_slot is None else time_slot or 0)
        if time_now != 2:
            return False
        return ((day_now + month_now) % 6) == 0
