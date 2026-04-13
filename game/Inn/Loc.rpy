init python:
    def prepare_location_entry(loc_name=""):
        loc_name = str(loc_name or CurLoc or location or "TavernMain")

        blocked_locations = {
            "TavernProstClients",
            "StreetClients",
            "SexPort",
            "SexProstTavern",
            "ChurchAfterCermon",
            "ChurchIspoved",
            "TavernGloryHole",
            "FridayDance",
            "DressTry",
            "BeckyHomeFront",
            "BeckyHome",
            "AfterDanceLegare",
            "TavernAmandaRoom",
            "AfterDanceSexLegare",
            "AmandaLoverSex",
            "SherwoodTravel",
        }

        try:
            loc_tavern_event = str(TavernEventOngoing or "")
        except NameError:
            loc_tavern_event = ""

        try:
            loc_signal_block = int(SignalBlockTime or 0)
        except NameError:
            loc_signal_block = 0

        block_time_advance = 0
        if loc_name in blocked_locations:
            block_time_advance = 1

        if loc_name == "TavernMain" and loc_tavern_event != "":
            block_time_advance = 1

        if loc_signal_block != 0:
            SignalBlockTime = 0
            block_time_advance = 1

        return loc_name, block_time_advance


label LOC(loc_name=""):
    call stat

    python:
        CurLoc, BlockTimeAdvance = prepare_location_entry(loc_name)
        location = CurLoc

    if BlockTimeAdvance == 0:
        call CheckDailyEvent("", "GiveBirth")

    return


label EnterLocation(loc_name=""):
    call LOC(loc_name)
    return
