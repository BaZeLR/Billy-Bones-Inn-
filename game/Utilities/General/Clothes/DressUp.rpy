# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.exports as renpy

    def dressup_ensure_dress_catalog_entry(code):
        key = str(code or "").strip()
        if not key:
            return
        item_obj = get_game_item("dress_" + key)
        if key not in ShortDressName:
            ShortDressName[key] = str(getattr(item_obj, "name", key) or key)
        if key not in FullDressDesc:
            FullDressDesc[key] = str(getattr(item_obj, "description", "") or "")

    def dressup_ensure_dress_parts(code):
        key = str(code or "").strip()
        if not key:
            return
        if key not in DressTopPart:
            DressTopPart[key] = ""
        if key not in DressBottomPart:
            DressBottomPart[key] = ""

label DressUp(GirlNameDress="", IsNewDayForDress=0):
    $ renpy.dynamic("_dress_girl_info", "_dress_wardrobe", "_dress_underwear", "TMPAllDressArray", "TMPBraArray", "TMPPantiesArray", "TMPStockingsArray")
    $ renpy.dynamic("DUCounter", "DecideNoBra", "DecideNoPanties", "DressSlutDesireLevel", "DressSlutDesireLevelTop", "DressSlutDesireLevelBottom")
    $ renpy.dynamic("TmpBottomSlutLevelMax", "TmpBottomSlutLevelMin", "TmpTopSlutLevelMax", "TmpTopSlutLevelMin", "TmpDressName", "TmpDressSelect", "TmpDressSelectMaxCur")
    $ renpy.dynamic("bottom_part", "bottom_slut", "cur_bottom", "cur_default", "cur_top", "dname", "girl_slut", "lname", "top_part", "top_slut")
    $ GirlNameDress = str(GirlNameDress or "").strip()
    if not GirlNameDress:
        return
    $ _dress_girl_info = people.get_info(GirlNameDress)
    if _dress_girl_info is None:
        return
    python:
        if not isinstance(getattr(_dress_girl_info, "wardrobe", None), dict):
            _dress_girl_info.wardrobe = {}
        _dress_wardrobe = _dress_girl_info.wardrobe
        _dress_underwear = _dress_wardrobe.setdefault("current_underwear", {})
        if not isinstance(_dress_underwear, dict):
            _dress_underwear = {}
            _dress_wardrobe["current_underwear"] = _dress_underwear
        cur_default = str(_dress_wardrobe.get("current_dress", "") or "")

        if int(IsNewDayForDress or 0) > 0 and procedural_randint(1, 2, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:82:1") == 1:
            TMPAllDressArray = list(_dress_wardrobe.get("owned", []) or [])
            TMPBraArray = []
            TMPPantiesArray = []
            TMPStockingsArray = []

            TmpDressSelect = 0
            TmpDressSelectMaxCur = -10000

            girl_slut = int(getattr(_dress_girl_info, "corruption", 0) or 0) if _dress_girl_info is not None else 0
            if girl_slut >= 70:
                TmpTopSlutLevelMax, TmpTopSlutLevelMin = 8, 3
                TmpBottomSlutLevelMax, TmpBottomSlutLevelMin = 8, 2
            elif girl_slut >= 55:
                TmpTopSlutLevelMax, TmpTopSlutLevelMin = 6, 2
                TmpBottomSlutLevelMax, TmpBottomSlutLevelMin = 6, 1
            elif girl_slut >= 45:
                TmpTopSlutLevelMax, TmpTopSlutLevelMin = 6, 2
                TmpBottomSlutLevelMax, TmpBottomSlutLevelMin = 4, 0
            elif girl_slut >= 35:
                TmpTopSlutLevelMax, TmpTopSlutLevelMin = 4, 2
                TmpBottomSlutLevelMax, TmpBottomSlutLevelMin = 3, 0
            elif girl_slut >= 20:
                TmpTopSlutLevelMax, TmpTopSlutLevelMin = 4, 0
                TmpBottomSlutLevelMax, TmpBottomSlutLevelMin = 2, 0
            elif girl_slut >= 10:
                TmpTopSlutLevelMax, TmpTopSlutLevelMin = 4, 0
                TmpBottomSlutLevelMax, TmpBottomSlutLevelMin = 1, 0
            else:
                TmpTopSlutLevelMax, TmpTopSlutLevelMin = 1, 0
                TmpBottomSlutLevelMax, TmpBottomSlutLevelMin = 1, 0

            for DUCounter, TmpDressName in enumerate(TMPAllDressArray):
                dname = str(TmpDressName or "")
                lname = dname.lower()
                if "bra" in lname:
                    TMPBraArray.append(dname)
                elif "panties" in lname:
                    TMPPantiesArray.append(dname)
                elif "stockings" in lname:
                    TMPStockingsArray.append(dname)
                else:
                    top_part = DressTopPart.get(dname, "")
                    bottom_part = DressBottomPart.get(dname, "")
                    top_slut = int(DressPartSlut.get(top_part, 0) or 0)
                    bottom_slut = int(DressPartSlut.get(bottom_part, 0) or 0)

                    DressSlutDesireLevelTop = top_slut - TmpTopSlutLevelMin
                    if top_slut > TmpTopSlutLevelMax:
                        DressSlutDesireLevelTop = TmpTopSlutLevelMax - top_slut

                    DressSlutDesireLevelBottom = bottom_slut - TmpBottomSlutLevelMin
                    if bottom_slut > TmpBottomSlutLevelMax:
                        DressSlutDesireLevelBottom = TmpBottomSlutLevelMax - bottom_slut

                    if DressSlutDesireLevelTop < 0 or DressSlutDesireLevelBottom < 0:
                        DressSlutDesireLevel = min(DressSlutDesireLevelTop, DressSlutDesireLevelBottom)
                    else:
                        DressSlutDesireLevel = DressSlutDesireLevelTop + DressSlutDesireLevelBottom

                    if DressSlutDesireLevel > 0:
                        DressSlutDesireLevel = min(DressSlutDesireLevel, 4) + procedural_randint(1, 7, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:144:2")
                    else:
                        DressSlutDesireLevel = min(DressSlutDesireLevel + procedural_randint(1, 5, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:146:3"), 3)

                    if DressSlutDesireLevel > TmpDressSelectMaxCur:
                        TmpDressSelectMaxCur = DressSlutDesireLevel
                        TmpDressSelect = DUCounter

            if TMPAllDressArray:
                cur_default = TMPAllDressArray[TmpDressSelect]

            DecideNoPanties = 0
            cur_bottom = DressBottomPart.get(cur_default, "")
            cur_top = DressTopPart.get(cur_default, "")

            if int(DressPartSlut.get(cur_bottom, 0) or 0) < 4 and girl_slut >= 43:
                DecideNoPanties = 1
            if girl_slut >= 53:
                DecideNoPanties = 1

            DecideNoBra = 0
            if int(DressPartSlut.get(cur_top, 0) or 0) < 4 and girl_slut >= 37:
                DecideNoBra = 1
            if girl_slut >= 51:
                DecideNoBra = 1

            if girl_slut < 56 and procedural_randint(1, 2, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:171:4") == 1:
                DecideNoPanties = 0
            if girl_slut < 74 and procedural_randint(1, 4, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:173:5") == 1:
                DecideNoPanties = 0
            if girl_slut < 56 and procedural_randint(1, 2, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:175:6") == 1:
                DecideNoBra = 0
            if girl_slut < 71 and procedural_randint(1, 4, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:177:7") == 1:
                DecideNoBra = 0

            _dress_underwear["bra"] = ""
            _dress_underwear["panties"] = ""
            _dress_underwear["legs"] = ""

            if len(TMPStockingsArray) > 0:
                _dress_underwear["legs"] = TMPStockingsArray[procedural_randint(0, len(TMPStockingsArray) - 1, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:185:8")]
            if len(TMPBraArray) > 0 and DecideNoBra == 0:
                _dress_underwear["bra"] = TMPBraArray[procedural_randint(0, len(TMPBraArray) - 1, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:187:9")]
            if len(TMPPantiesArray) > 0 and DecideNoPanties == 0:
                _dress_underwear["panties"] = TMPPantiesArray[procedural_randint(0, len(TMPPantiesArray) - 1, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:189:10")]

        _dress_wardrobe["current_dress"] = cur_default
        dressup_ensure_dress_catalog_entry(cur_default)
        dressup_ensure_dress_parts(cur_default)
        dressup_ensure_dress_catalog_entry(_dress_underwear.get("bra", ""))
        dressup_ensure_dress_catalog_entry(_dress_underwear.get("panties", ""))
        dressup_ensure_dress_catalog_entry(_dress_underwear.get("legs", ""))
        _dress_girl_info.reset_sex_clothing_state()
    return
