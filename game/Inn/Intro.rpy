# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

default ONGLOAD = "loadg"
default ONGSAVE = "saveg"
default ONNEWLOC = "LOC"

default CurLoc = "Intro"
default location = "Intro"
default PrevLoc = ""
default MainTxt = ""
default CurLocDesc = ""
default MaxCounterToClean = 4
default DebugFlag = 0
default _layout_last_picture = ""
default GraphicsOn = 1

# Core player/time economy defaults.
default time = 0
default hour = 8
default minute = 0
default day = 1
default month = 1
default week = 1
default year = 1100
default age = 20
default money = 10000
default fun = 50
default energy = 100
default health = 100
default notoriety = 0
default reputation = 0
default exploration = 0
default charisma = 0
default rebellion = 0
default look = 100
default costumecondition = 100
default dayssincehaircut = 0
default PlayerHaircutDaySt = 0
default PlayerDressDaySt = {"villagedress": 0}
default dayssincewash = 0
default ashesdirtydays = 0
default upstairsroomsdirty = 0
default taverncleanliness = 60
default Arousal = {"You": 0}
default HadSex = {"You": 0}
default topdress = {}
default bottomdress = {}
default bra = {}
default panties = {}
default legs = {}
default shoes = {}
default topraised = {}
default bottomraised = {}
default RealName = {}
default RealName2 = {}
default RealName3 = {}
default DateOfBirth = {}
default age_girls = {}
default kids = {}
default beauty = {}
default pregfather = {}
default CurrentLoc = {}
default girltextdesc = {}
default cooking = {}
default cleaning = {}
default virginity = {}
default PussyWetStart = {}
default Drunk = {}
default LickPussy = {}
default pregnancy = {}
default TitsVisible = {}
default GrupenSex = {}
default PussyVisible = {}
default ShortSkirtNoPanties = {}
default CockInMouth = {}
default CockInPussy = {}
default CockInAss = {}
default CockInTits = {}
default SexInsertedContainer = {}
default EddieCockInMouth = {}
default EddieCockInPussy = {}
default EddieCockInTits = {}
default CumFaceYou = {}
default CumFaceOthers = {}
default CumTitsYou = {}
default CumTitsOthers = {}
default CumInsideYou = {}
default CumInsideOthers = {}
default TodaySexEvents = []
default sex_history_by_girl = {}
default sex_history_next_id = {}
default ClientsDayTotal = {}
default cancumdaily = 2
default cametoday = 0
default BlessedByEllona = 0
default CursedByEllona = 0
default CursedByEllonaDays = 0
default CursedByEllonaReduce = 0
default MyDresses = ["villagedress"]
default MyCurDress = "villagedress"
default EquippedWeapon = ""
default EquippedArmor = ""
default company_list = []
default PlayerFightSupply = {}
default FightWeaponLoaded = 0
default FightRetreatUsed = 0
default SickDays = 0
default FightEnemyState = {}
default HuntUnlocked = False
default HuntLastResult = {}
default FightSideLog = []
default FightEnemyParty = []
default FightEnemyId = ""
default playerItems = {}
default DressProduced = ""
default DressBuyer = ""
default FridayDancesCount = 0
default DanceSponsor = 0
default DanceWatchLine = {}
default GirlDance = []
default DanceStep = 0
default HandsDance = ""
default KissDance = 0
default TitsDance = 0
default CurrentActions = ""
default DailyEventsList = []
default KidsList = []
default KidsListNextId = 1
default _kids_functions_initialized = False
default KidsPosobie = 0
default KidBirthPosobie = ""
default ProstitutesKids = 0
default Breastfeed = {}
default Lactate = {}
default PregTotalSuspects = {}
default ZaletSuspectFinal = {}
default BlockTimeAdvance = 0
default householdmembers = 4
default tavernvisitors = 40
default productnum = 200
default winenum = 100
default tavernfame = 0
default SloganFixed = 0
default TavernHole = 0
default TavernGloryHole = 0
default GloryHoleLook = 0
default GloryHoleCurrentStep = 0
default BlockGloryHoleMenu = 0
default CockInGloryHole = 0
default CheatMoneyGrab = 0
default PlayerChoresWeek = {}
default UI_chores = {}
default WeeklyVisitorsTrack = {}
default WeeklyChoresLastEvalStamp = ""
default CurDay = {}
default TotalDay = {}
default ExtraEvents = ""
# Roster only; each girl is initialized by Init* labels.
default AllGirlNames = [
    "sandra",
    "melissa",
    "amanda",
    "georgett",
    "liza",
    "becky",
    "irma",
    "inga",
    "clara",
]

# Shared runtime maps used by multiple systems.

default amanda = {}
default AmandaVar = {}
default amandaEvents = []
default BeckyVar = {}
default ClaraVar = {}
default GeorgettVar = {}
default LizaVar = {}
default SandraVar = {}
default MelissaVar = {}
default IrmaVar = {}
default Friends = {}
default TalkedToday = {}
default FlirtedToday = {}
default GiftedToday = {}
default AskedToday = {}
default GiftPreferences = {}
default otkroven = {}
default neshlush = {}
default FightLevel = {"you": 1}
default HarassInstructions = {}
default waitress = {}
default dressdefault = {}
default topdressdef = {}
default bottomdressdef = {}
default DressTopPart = {}
default DressBottomPart = {}
default DressPartDesc = {}
default DressPartSlut = {}
default bradef = {}
default pantiesdef = {}
default legsdef = {}
default shoesdef = {}
default jobHallAvail = {}
default jobkitchen = {}
default jobcleaning = {}
default jobwaitress = {}
default jobkitchentomorrow = {}
default jobcleaningtomorrow = {}
default jobwaitresstomorrow = {}
default jobWhoreAvail = {}
default jobGloryHoleAvail = {}
default jobwhore = {}
default jobgloryhole = {}
default jobwhoreTommorow = {}
default jobgloryholeTommorow = {}

init python:
    def _intro_stop_channel_if_playing(channel_name):
        ch = str(channel_name or "").strip()
        if not ch:
            return
        try:
            if renpy.music.is_playing(channel=ch):
                renpy.music.stop(channel=ch)
        except Exception:
            pass





label Intro:
    scene black
    hide screen status
    hide screen main_ui

    python:
        _intro_notice = "-------------------------------------------------ТРАКТИР \"ДИКИЙ ЖЕРЕБЕЦ\"------------------------------------------\nВЕРСИЯ 0.05\nАВТОР БИЛЛИ БОНС\nХУДОЖНИКИ ULIBAKA11-11, FORCEFER, NIK287\n\nИГРА ПРЕДНАЗНАЧЕННА ТОЛЬКО ДЛЯ 18+. ЕСЛИ ВАМ НЕТ 18 ЛЕТ НЕМЕДЛЕННО ЗАКРОЙТЕ ЭТУ ИГРУ И СОТРИТЕ ЕЕ С КОМПЬЮТЕРА\n\nИГРА ПРЕДСТАВЛЯЕТ СОБОЙ ЧИСТУЮ ФАНТАЗИЮ, ВСЕ ЗАДЕЙСТВОВАННЫЕ МОДЕЛИ СТАРШЕ 18 ЛЕТ, ЛЮБЫЕ СОВПАДЕНИЯ С РЕАЛЬНЫМИ СОБЫТИЯМИ ИЛИ ЛЮДЬМИ СЛУЧАЙНЫ\n\nПОПЫТКИ ПОСТУПАТЬ В РЕАЛЬНОЙ ЖИЗНИ ТАК ЖЕ, КАК ПОСТУПАЮТ ГЕРОИ ДАННОЙ ИГРЫ, НАСТОЯТЕЛЬНО НЕ РЕКОМЕНДУЮТСЯ. ОНИ МОГУТ ПРИВЕСТИ К РАЗБИТОЙ ФИЗИОНОМИИ, НЕЖЕЛАТЕЛЬНОЙ БЕРЕМЕННОСТИ И/ИЛИ БРАКУ, ТЮРЕМНОМУ ЗАКЛЮЧЕНИЮ, ШТРАФУ, ПЕРЕЛОМУ КОНЕЧНОСТЕЙ, УВОЛЬНЕНИЮ, РАЗВОДУ, СКАНДАЛУ, ВСТУПЛЕНИЮ В ПАРТИЮ \"ЕДИНАЯ РОССИЯ\" ИЛИ В РЯДЫ ОППОЗИЦИИ, ИСКЛЮЧЕНИЮ ИЗ УЧЕБНОГО ЗАВЕДЕНИЯ И ПРОЧИМ РАЗНООБРАЗНЫМ НЕПРИЯТНОСТЯМ\n\nПри создании игры использовались модули меню и таблиц данных авторства Олегуса и две процедуры из игры \"Альбедо\" авторства ДеГросса\n---------------------------------------------------------------------------"
        _intro_story = "Вас зовут Стефан Лонгкок. Ваш дядя, Джон Лонгкок, был крестьянином, но, накопив достаточно денег, он купил небольшой трактир в пригороде большого портового города Коитополиса. Однако ему было не суждено стать трактирщиком - он так увлекся обмытием сделки, что упал пьяным в один из каналов и утонул. После похорон во владение трактиром \"Дикий Жеребец\" вступили вы, его племянник и наследник.\n\nК сожалению вы мало что понимаете в уборке, готовке и прочем. Но это не важно, ведь теперь вы управляете трактиром и должны руководить. Основную работу выполняет ваша команда: Сандра, Мелисса и Аманда. Ваше незавидное финансовое положение не позволяет вам пока нанять кого-то еще."
        CurLoc = "Intro"
        location = "Intro"
        PrevLoc = ""
        MainTxt = _intro_notice + "\n\n" + _intro_story
        CurLocDesc = MainTxt

    python:
        _intro_stop_channel_if_playing("music")
        _intro_stop_channel_if_playing("sound")
        _intro_stop_channel_if_playing("voice")

        STATUS_PANEL_ENABLED = 0
        
        GraphicsOn = 1
        hour = 8
        minute = 0
        day = 1
        month = 1
        week = 1
        year = 1100
        MaxCounterToClean = 4
        calendar_set_time_slot(0)

        Arousal = {"You": 0}
        topdress = {}
        bottomdress = {}
        bra = {}
        panties = {}
        topraised = {}
        bottomraised = {}
        age = 18
        money = 10000
        fun = 50
        energy = 100
        health = 100
        notoriety = 0
        exploration = 0
        charisma = 0
        rebellion = 0
        look = 100
        costumecondition = 100
        dayssincehaircut = 0
        PlayerHaircutDaySt = 0
        PlayerDressDaySt = {"villagedress": 0}
        dayssincewash = 0
        ashesdirtydays = 0
        upstairsroomsdirty = 0
        taverncleanliness = 60
        HadSex = {"You": 0}
        LickPussy = {}
        pregnancy = {}
        TitsVisible = {}
        PussyVisible = {}
        ShortSkirtNoPanties = {}
        CockInMouth = {}
        CockInPussy = {}
        CockInAss = {}
        CockInTits = {}
        SexInsertedContainer = {}
        EddieCockInMouth = {}
        EddieCockInPussy = {}
        EddieCockInTits = {}
        CumFaceYou = {}
        CumFaceOthers = {}
        CumTitsYou = {}
        CumTitsOthers = {}
        CumInsideYou = {}
        CumInsideOthers = {}
        LastDaySex = -1
        PlayerLastCumDay = -1
        PlayerSleepBottomLayer = "daywear"
        PlayerRoomLightClosed = 0
        PlayerMorningArousalDay = -1
        PlayerWakeStateNotice = ""
        PlayerArousalReasons = []
        PlayerObservedNakedNpcDay = {}
        PlayerLastHelpResult = {}
        cancumdaily = 2
        cametoday = 0
        BlessedByEllona = 0
        CursedByEllona = 0
        CursedByEllonaReduce = 0
        FightLevel = {"you": 1}
        otkroven = {}
        neshlush = {}
        MyDresses = ["villagedress"]
        MyCurDress = "villagedress"
        company_list = []
        PlayerFightSupply = {}
        FightWeaponLoaded = 0
        FightRetreatUsed = 0
        SickDays = 0
        FightEnemyState = {}
        HuntUnlocked = False
        HuntLastResult = {}
        FightSideLog = []
        FightEnemyParty = []
        FightEnemyId = ""
        TalkedToday = {}
        FlirtedToday = {}
        GiftedToday = {}
        AskedToday = {}
        GiftPreferences = {}
        playerItems = {}

        try:
            ShedRoom.game_items = ["old_axe_001", "lumber_001"]
            ShedRoom.objects = ShedRoom.game_items
        except Exception:
            pass

        try:
            TavernMainFireplaceObject.state = {"fire_started_minute": 0, "fire_until_minute": 0, "fire_units": 0, "fire_adds": 0, "ash_dirty": 0, "chopped_wood_stock": 0}
        except Exception:
            pass

        try:
            TavernKitchenHearthObject.state = {"fire_started_minute": 0, "fire_until_minute": 0, "fire_units": 0, "fire_adds": 0, "ash_dirty": 0, "chopped_wood_stock": 0}
        except Exception:
            pass

        try:
            TavernKitchenCauldronObject.state = {"hot_water_until_minute": 0, "hot_water_units": 0}
        except Exception:
            pass

        FridayDancesCount = 0
        BlockTimeAdvance = 0
        KidsList = []
        KidsListNextId = 1

        householdmembers = 4
        tavernvisitors = 40
        productnum = 200
        winenum = 100
        tavernfame = 0

        SloganFixed = 0
        TavernHole = 0
        TavernGloryHole = 0
        GloryHoleLook = 0
        GloryHoleCurrentStep = 0
        BlockGloryHoleMenu = 0
        CockInGloryHole = 0
        CheatMoneyGrab = 0

    call InitSecondaryNPC
    call InitDressDesc
    call NamesSet
    call CreateDonationsList
    call SexEventsTableCode
    call OtherFunctionsCode
    call ZaletOpinionCalc
    call KidsFunctions

    call InitAmanda
    call InitSandra
    call InitMelissa
    call InitGeorgett
    call InitLiza
    call InitBecky
    call InitInga
    call InitIrma
    call InitClara
    call InitPeople

    python:
        for _intro_girl_name in AllGirlNames:
            topraised[_intro_girl_name] = 0
            bottomraised[_intro_girl_name] = 0
            jobkitchentomorrow[_intro_girl_name] = int(jobkitchen.get(_intro_girl_name, 0) or 0)
            jobcleaningtomorrow[_intro_girl_name] = int(jobcleaning.get(_intro_girl_name, 0) or 0)
            jobwaitresstomorrow[_intro_girl_name] = int(jobwaitress.get(_intro_girl_name, 0) or 0)
            LickPussy[_intro_girl_name] = 0
            HadSex[_intro_girl_name] = 0
            HarassInstructions[_intro_girl_name] = ""

    call AmandaDynamicCommonBlocks
    python:
        try:
            _story_runtime_init = initStoryEventRuntime
        except NameError:
            _story_runtime_init = None
        if callable(_story_runtime_init):
            _story_runtime_init(True)
        try:
            _relationship_runtime_init = init_relationship_levels_runtime
        except NameError:
            _relationship_runtime_init = None
        if callable(_relationship_runtime_init):
            _relationship_runtime_init(True)

    "[MainTxt]"
    menu:
        "Приступить к управлению трактиром":
            jump dev_after_report_checkpoint
    return


label dev_after_report_checkpoint:
    call NextDay_NewDayEvents
    call CreateTavernEvents
    $ revision = 5
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    jump TavernMain
