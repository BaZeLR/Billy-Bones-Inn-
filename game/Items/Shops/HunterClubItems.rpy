# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    AleItem = GameItem(
        object_id="drink_ale_001",
        name="эль",
        description="Бутылка крепкого эля, которой можно подкрепиться в дороге или продать обратно торговцу.",
        actions=[
            ObjectAction(
                action_id="drink",
                label="Выпить эль",
                hook="call",
                target="UseDrinkItem",
                args=("drink_ale_001",),
            ),
        ],
        price=2,
        carriable=True,
        usable=True,
        stackable=True,
        custom_properties={
            "item_kind": "drink",
            "drink_kind": "ale",
            "consume_action": "drink",
            "consume_minutes": 30,
            "consume_energy": 0,
            "consume_fun": 10,
            "consume_text": "Вы аккуратно вынимаете пробку, не выбрасываете ее и неторопливо допиваете бутылку эля. После этого в вещах у вас остаются пустая бутылка и пробка.",
            "consume_outputs": (("empty_bottle_001", 1), ("cork_001", 1)),
            "gift_value": 1,
            "social_fun_bonus": 2,
            "social_openness_bonus": 1,
        },
    )

    DogBoneItem = GameItem(
        object_id="dog_bone_001",
        name="кость для собак",
        description="Крепкая кость, которой удобно приманивать или поощрять охотничьих собак.",
        price=1,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "dog_bone",
        },
    )

    DogCollarItem = GameItem(
        object_id="dog_collar_001",
        name="собачий ошейник",
        description="Простой крепкий ошейник. С ним можно забрать прирученного пса домой.",
        price=10,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "dog_collar",
        },
    )

    HuntingTrapItem = GameItem(
        object_id="hunting_trap_001",
        name="охотничья ловушка",
        description="Простая, но надежная ловушка для мелкой и средней добычи.",
        price=18,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "trap",
        },
    )

    ArrowsItem = GameItem(
        object_id="arrows_001",
        name="стрелы",
        description="Связка охотничьих стрел.",
        price=6,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "arrows",
        },
    )

    FlintItem = GameItem(
        object_id="flint_001",
        name="кремень",
        description="Кусок кремня для разведения огня в дороге.",
        price=4,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "flint",
        },
    )

    RopeItem = GameItem(
        object_id="rope_001",
        name="веревка",
        description="Прочная веревка, полезная в дороге, на охоте и в хозяйстве.",
        price=9,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "rope",
        },
    )

    TorchItem = GameItem(
        object_id="torch_001",
        name="факел",
        description="Смоляной факел для темных мест и ночных вылазок.",
        price=5,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "torch",
        },
    )

    GunpowderItem = GameItem(
        object_id="gunpowder_001",
        name="порох",
        description="Пороховой заряд, который пригодится для дальнейшего развития охотничьего снаряжения.",
        price=16,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "gunpowder",
        },
    )

    ShotDropletsItem = GameItem(
        object_id="droplets_001",
        name="дробь",
        description="Мелкая охотничья дробь для старого ружейного механизма и ближней стрельбы по зверю.",
        price=11,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "droplets",
        },
    )

    WeaponOilItem = GameItem(
        object_id="weapon_oil_001",
        name="оружейное масло",
        description="Небольшой пузырек густого масла для чистки и смазки старых механизмов.",
        price=7,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "weapon_oil",
        },
    )

    BandageItem = GameItem(
        object_id="bandage_001",
        name="бинт",
        description="Чистый перевязочный бинт. В бою помогает наскоро перехватить рану и немного восстановить силы.",
        actions=[
            ObjectAction(
                action_id="use_bandage",
                label="Перевязаться",
                hook="call",
                target="UseBandageItem",
            ),
        ],
        price=4,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "bandage",
        },
    )

    HealingPotionItem = GameItem(
        object_id="healing_potion_001",
        name="лечебное зелье",
        description="Крепкое травяное зелье для быстрого восстановления сил во время опасной схватки.",
        actions=[
            ObjectAction(
                action_id="drink_healing_potion",
                label="Выпить лечебное зелье",
                hook="call",
                target="UseHealingPotionItem",
            ),
        ],
        price=14,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "healing_potion",
        },
    )

    WolfSkinItem = GameItem(
        object_id="wolf_skin_001",
        name="серая волчья шкура",
        description="Снятая с обычного серого волка шкура. Ее можно продать или пустить на подарок.",
        price=25,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "animal_loot",
            "animal_kind": "wolf",
            "loot_kind": "skin",
            "gift_value": 1,
        },
    )

    WhiteWolfSkinItem = GameItem(
        object_id="white_wolf_skin_001",
        name="белая волчья шкура",
        description="Редкая белая волчья шкура. Охотники ценят ее заметно дороже обычной серой.",
        price=75,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "animal_loot",
            "animal_kind": "white_wolf",
            "loot_kind": "skin",
            "gift_value": 2,
        },
    )

    BoarFangItem = GameItem(
        object_id="boar_fang_001",
        name="кабаний клык",
        description="Крепкий кабаний клык, из которого позже можно сделать украшение или трофей.",
        price=50,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "animal_loot",
            "animal_kind": "boar",
            "loot_kind": "fang",
            "gift_value": 1,
        },
    )

    BoarMeatItem = GameItem(
        object_id="boar_meat_001",
        name="кабанье мясо",
        description="Тяжелый кусок свежего кабаньего мяса.",
        price=45,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "animal_loot",
            "animal_kind": "boar",
            "loot_kind": "meat",
        },
    )

    BearClawItem = GameItem(
        object_id="bear_claw_001",
        name="медвежий коготь",
        description="Крупный медвежий коготь, который ценят как трофей и основу для украшений.",
        price=50,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "animal_loot",
            "animal_kind": "bear",
            "loot_kind": "claw",
            "gift_value": 1,
        },
    )

    BrownBearFurItem = GameItem(
        object_id="bear_fur_brown_001",
        name="мех бурого медведя",
        description="Тяжелый, дорогой мех бурого медведя.",
        price=80,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "animal_loot",
            "animal_kind": "brown_bear",
            "loot_kind": "fur",
            "gift_value": 1,
        },
    )

    GrizzlyBearFurItem = GameItem(
        object_id="bear_fur_grizzly_001",
        name="мех гризли",
        description="Особенно ценный тяжелый мех огромного гризли.",
        price=130,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "animal_loot",
            "animal_kind": "grizzly",
            "loot_kind": "fur",
            "gift_value": 1,
        },
    )

    WarmFurCloakItem = GameItem(
        object_id="warm_fur_cloak_001",
        name="теплый меховой плащ",
        description="Плотный зимний плащ из выделанной шкуры и меха. Его можно носить самому, подарить или выгодно продать.",
        price=95,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "winter_cloak",
            "gift_value": 2,
            "social_friend_bonus": 1,
        },
    )

    FurBedrollItem = GameItem(
        object_id="fur_bedroll_001",
        name="меховая постель",
        description="Теплая свернутая постель из меха и плотной ткани. Хороша для зимовки, гостевой комнаты или продажи.",
        price=110,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "fur_bedroll",
            "gift_value": 2,
        },
    )

    SpecialMushroomItem = GameItem(
        object_id="special_mushroom_001",
        name="редкий гриб",
        description="Редкий лесной гриб, который ценится знахарями и поварами.",
        price=12,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "forest_resource",
            "resource_kind": "special_mushroom",
            "spawn_zones": ["ForestDarkWoods", "ForestCave"],
            "spawn_rarity": "редкий",
        },
    )

    SpecialHerbsItem = GameItem(
        object_id="special_herbs_001",
        name="редкие травы",
        description="Пучок редких трав с сильным терпким запахом.",
        price=10,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "forest_resource",
            "resource_kind": "special_herbs",
            "spawn_zones": ["ForestSpring", "ForestWaterfall", "ForestClearing"],
            "spawn_rarity": "редкие",
        },
    )

    LavenderItem = GameItem(
        object_id="lavender_001",
        name="лаванда",
        description="Пахучая лесная лаванда, которую можно продать или подарить.",
        price=8,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "forest_resource",
            "resource_kind": "lavender",
            "gift_value": 1,
            "spawn_zones": ["ForestClearing", "ForestSpring"],
            "spawn_rarity": "нечастая",
        },
    )

    WildRoseItem = GameItem(
        object_id="wild_rose_001",
        name="дикая роза",
        description="Свежая лесная роза, собранная на солнечной поляне.",
        price=8,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "forest_resource",
            "resource_kind": "wild_rose",
            "gift_value": 1,
            "spawn_zones": ["ForestClearing", "ForestLake"],
            "spawn_rarity": "нечастая",
        },
    )

    MossItem = GameItem(
        object_id="moss_001",
        name="мох",
        description="Сырой лесной мох, собранный в пещере или у влажных камней.",
        price=5,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "forest_resource",
            "resource_kind": "moss",
            "spawn_zones": ["ForestCave", "ForestWaterfall"],
            "spawn_rarity": "обычный во влажных местах",
        },
    )

label UseBandageItem:
    if int(_player_item_count_by_id("bandage_001") or 0) <= 0:
        $ MainTxt = "При себе у вас больше нет бинтов."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryMenu
        return
    if int(health or 0) >= 100:
        $ MainTxt = "Сейчас ваши раны уже перевязаны настолько хорошо, насколько это возможно."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryItemMenu("bandage_001", True)
        return

    $ _player_remove_item_by_id("bandage_001", 1)
    $ health = _player_clamp(health + 12, 0, 100)
    $ MainTxt = "Вы неторопливо перевязываете раны и чувствуете себя немного лучше."
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryItemMenu("bandage_001", True)
    return


label UseHealingPotionItem:
    if int(_player_item_count_by_id("healing_potion_001") or 0) <= 0:
        $ MainTxt = "При себе у вас больше нет лечебного зелья."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryMenu
        return

    $ _player_remove_item_by_id("healing_potion_001", 1)
    $ health = _player_clamp(health + 25, 0, 100)
    $ MainTxt = "Вы выпиваете лечебное зелье. Горечь быстро сменяется ощущением, что силы возвращаются."
    $ CurLocDesc = MainTxt
    call stat
    call PlayerCardInventoryItemMenu("healing_potion_001", True)
    return
