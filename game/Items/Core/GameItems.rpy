# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
define item_catalog = {}
define game_items = []
define game_item_registry = {}
define menDress = []
define womenDress = []

init 5 python:
    def _all_game_item_objects():
        return [
            OldAxeItem,
            LumberItem,
            ChoppedWoodItem,
            MushroomItem,
            BerriesItem,
            HoneyCombItem,
            AleItem,
            DogBoneItem,
            DogCollarItem,
            HuntingTrapItem,
            ArrowsItem,
            ShotDropletsItem,
            FlintItem,
            RopeItem,
            TorchItem,
            GunpowderItem,
            WeaponOilItem,
            BandageItem,
            HealingPotionItem,
            WolfSkinItem,
            BoarFangItem,
            BoarMeatItem,
            BearClawItem,
            BrownBearFurItem,
            GrizzlyBearFurItem,
            WarmFurCloakItem,
            FurBedrollItem,
            SpecialMushroomItem,
            SpecialHerbsItem,
            LavenderItem,
            WildRoseItem,
            MossItem,
            RecipeBookItem,
            NightBowlItem,
            FancyNightBowlItem,
            BucketItem,
            EmptyBottleItem,
            CorkItem,
            PigLardItem,
            DriedMossItem,
            ClothScrapItem,
            SoapItem,
            OliveOilItem,
            LuxurySoapItem,
            EthanolItem,
            EnergyTeaItem,
            LibidoTinctureItem,
            SpecialCreamItem,
            FireBombItem,
            BatRepellentItem,
            AshBarrelItem,
            RustyHunterRifleItem,
            OldLeatherCuirassItem,
            FoodBaleItem,
            MilkPitcherItem,
            WineBarrelItem,
            TavernHelpBookItem,
            PeasantCostumeItem,
            BourgeoisCostumeItem,
            SailorCostumeItem,
            BanditCostumeItem,
            NobleCostumeItem,
            ModestWorkDressItem,
            ModestNiceDressItem,
            WorkDressItem,
            WorkDressZhiletItem,
            GreenWorkDressItem,
            OpenWorkDressItem,
            MiniDressItem,
            SlutDressItem,
            SimpleBraItem,
            SimplePantiesItem,
            WhiteStockingsItem,
            BlackStockingsItem,
            RedStockingsItem,
            NightshirtItem,
        ]

    def _game_item_catalog_entry(item_obj):
        return {
            "id": str(getattr(item_obj, "object_id", "") or ""),
            "name": str(getattr(item_obj, "name", "") or ""),
            "description": str(getattr(item_obj, "description", "") or ""),
            "picture": str(getattr(item_obj, "picture", "") or ""),
            "price": int(getattr(item_obj, "price", 0) or 0),
            "portable": bool(getattr(item_obj, "carriable", False)),
            "wearable": bool(getattr(item_obj, "wearable", False)),
            "readable": bool(getattr(item_obj, "readable", False)),
            "usable": bool(getattr(item_obj, "usable", False)),
            "weapon": bool(getattr(item_obj, "weapon", False)),
            "stackable": bool(getattr(item_obj, "stackable", False)),
            "custom_properties": dict(getattr(item_obj, "custom_properties", {}) or {}),
        }

    def ensure_game_item_registry():
        global game_items, item_catalog, game_item_registry, menDress, womenDress

        _objects = _all_game_item_objects()
        game_items = [str(row.object_id or "") for row in _objects if str(getattr(row, "object_id", "") or "").strip() != ""]

        item_catalog = {}
        game_item_registry = {}
        for _game_item in _objects:
            _item_id = str(getattr(_game_item, "object_id", "") or "").strip()
            if _item_id == "":
                continue
            _entry = _game_item_catalog_entry(_game_item)
            item_catalog[_item_id] = _entry
            game_item_registry[_item_id] = dict(_entry)

        menDress = [
            "dress_villagedress",
            "dress_citydress",
            "dress_sailordress",
            "dress_thiefdress",
            "dress_nobbledress",
        ]

        womenDress = [
            "dress_modestworkdress",
            "dress_modestnicedress",
            "dress_workdress",
            "dress_workdresszhilet",
            "dress_greenworkdress",
            "dress_openworkdress",
            "dress_minidress",
            "dress_slutdress",
            "dress_simplebra",
            "dress_simplepanties",
            "dress_whitestockings",
            "dress_blackstockings",
            "dress_redstockings",
            "dress_nightshirt",
        ]

    ensure_game_item_registry()
