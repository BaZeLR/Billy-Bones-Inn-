# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.exports as renpy

    for _dress_runtime_helper_name in ("_ensure_dress_catalog_entry", "_ensure_dress_parts"):
        try:
            if hasattr(renpy.store, _dress_runtime_helper_name):
                delattr(renpy.store, _dress_runtime_helper_name)
        except Exception:
            pass

    def dressup_ensure_dress_catalog_entry(code):
        key = str(code or "").strip()
        if not key:
            return
        try:
            catalog = item_catalog if isinstance(item_catalog, dict) else {}
        except Exception:
            catalog = {}
        if key not in ShortDressName:
            _item = catalog.get("dress_" + key, {})
            ShortDressName[key] = str(_item.get("name", key) or key)
        if key not in FullDressDesc:
            _item = catalog.get("dress_" + key, {})
            FullDressDesc[key] = str(_item.get("description", "") or "")

    def dressup_ensure_dress_parts(code):
        key = str(code or "").strip()
        if not key:
            return
        if key not in DressTopPart:
            DressTopPart[key] = ""
        if key not in DressBottomPart:
            DressBottomPart[key] = ""

    def dressup_prune_legacy_runtime_helpers():
        for helper_name in ("_ensure_dress_catalog_entry", "_ensure_dress_parts"):
            try:
                if hasattr(renpy.store, helper_name):
                    delattr(renpy.store, helper_name)
            except Exception:
                pass


label DressUp(GirlNameDress="", IsNewDayForDress=0):
    $ GirlNameDress = str(GirlNameDress or "").strip()
    if not GirlNameDress:
        return
    python:
        dressup_prune_legacy_runtime_helpers()
        try:
            topdressdef
        except NameError:
            topdressdef = {}
        try:
            bottomdressdef
        except NameError:
            bottomdressdef = {}
        try:
            item_catalog
        except NameError:
            item_catalog = {}

        dressdefault.setdefault(GirlNameDress, "")
        topdressdef.setdefault(GirlNameDress, "")
        bottomdressdef.setdefault(GirlNameDress, "")
        bradef.setdefault(GirlNameDress, "")
        pantiesdef.setdefault(GirlNameDress, "")
        legsdef.setdefault(GirlNameDress, "")
        shoesdef.setdefault(GirlNameDress, "")
        topdress.setdefault(GirlNameDress, "")
        bottomdress.setdefault(GirlNameDress, "")
        bra.setdefault(GirlNameDress, "")
        panties.setdefault(GirlNameDress, "")
        legs.setdefault(GirlNameDress, "")
        shoes.setdefault(GirlNameDress, "")
        topraised.setdefault(GirlNameDress, 0)
        bottomraised.setdefault(GirlNameDress, 0)

        if int(IsNewDayForDress or 0) > 0 and procedural_randint(1, 2, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:82:1") == 1:
            dress_list_name = GirlNameDress + "Dresses"
            TMPAllDressArray = list(getattr(renpy.store, dress_list_name, []) or [])
            TMPBraArray = []
            TMPPantiesArray = []
            TMPStockingsArray = []

            TmpDressSelect = 0
            TmpDressSelectMaxCur = -10000

            girl_slut = int(sluttiness.get(GirlNameDress, 0) or 0)
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
                dressdefault[GirlNameDress] = TMPAllDressArray[TmpDressSelect]

            DecideNoPanties = 0
            cur_default = dressdefault.get(GirlNameDress, "")
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

            bradef[GirlNameDress] = ""
            pantiesdef[GirlNameDress] = ""
            legsdef[GirlNameDress] = ""

            if len(TMPStockingsArray) > 0:
                legsdef[GirlNameDress] = TMPStockingsArray[procedural_randint(0, len(TMPStockingsArray) - 1, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:185:8")]
            if len(TMPBraArray) > 0 and DecideNoBra == 0:
                bradef[GirlNameDress] = TMPBraArray[procedural_randint(0, len(TMPBraArray) - 1, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:187:9")]
            if len(TMPPantiesArray) > 0 and DecideNoPanties == 0:
                pantiesdef[GirlNameDress] = TMPPantiesArray[procedural_randint(0, len(TMPPantiesArray) - 1, key="procedural:Utilities/General/Clothes/DressUp.rpy:procedural_randint:189:10")]

        cur_default = dressdefault.get(GirlNameDress, "")
        dressup_ensure_dress_catalog_entry(cur_default)
        dressup_ensure_dress_parts(cur_default)
        topdressdef[GirlNameDress] = DressTopPart.get(cur_default, "")
        bottomdressdef[GirlNameDress] = DressBottomPart.get(cur_default, "")

        topdress[GirlNameDress] = topdressdef.get(GirlNameDress, "")
        bottomdress[GirlNameDress] = bottomdressdef.get(GirlNameDress, "")
        bra[GirlNameDress] = bradef.get(GirlNameDress, "")
        panties[GirlNameDress] = pantiesdef.get(GirlNameDress, "")
        legs[GirlNameDress] = legsdef.get(GirlNameDress, "")
        shoes[GirlNameDress] = shoesdef.get(GirlNameDress, "")
        dressup_ensure_dress_catalog_entry(bradef.get(GirlNameDress, ""))
        dressup_ensure_dress_catalog_entry(pantiesdef.get(GirlNameDress, ""))
        dressup_ensure_dress_catalog_entry(legsdef.get(GirlNameDress, ""))
        topraised[GirlNameDress] = 0
        bottomraised[GirlNameDress] = 0
        bodymodel_sync_character(GirlNameDress)
    return


label dress_up(girl_name="", is_new_day_for_dress=0):
    call DressUp(girl_name, is_new_day_for_dress)
    return
