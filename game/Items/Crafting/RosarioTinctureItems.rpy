# Rosario's fantasy tincture uses the existing item registry and recipe catalog.
# Asking the Sofa about its former owner reveals the recipe.
init 5 python:
    def rosario_tincture_recipe_known():
        sofa_story = threads.get("claraForestSofa")
        return bool(
            Sofa.installed
            and bool(getattr(Sofa, "rosario_recipe_taught", False))
            and sofa_story is not None
            and (sofa_story.completed or int(sofa_story.num or 0) >= 7)
            and player_has_soap_recipe_book()
        )

    RosarioDroppingsItem = GameItem(
        object_id="chinchilla_droppings_001",
        name="шарик помёта Розарио",
        description="Один крошечный шарик из клетки леди Ностар. Сам Розарио едва ли подозревает, что его хозяйство пользуется спросом у алхимиков.",
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "ingredient",
            "ingredient_kind": "chinchilla_droppings",
        },
    )

    RosarioSilverCoinItem = GameItem(
        object_id="silver_coin_001",
        name="серебряная монета",
        description="Настоящая серебряная монета, не мараведи. Три такие монеты пригодятся для особых наконечников стрел.",
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafting_material",
            "material_kind": "silver_coin",
        },
    )

    RosarioTinctureItem = GameItem(
        object_id="rosario_arousal_tincture_001",
        name="настойка Розарио",
        description="Редкая медово-грибная настойка по рецепту говорящего дивана. Состав звучит как шутка, но бутылка обещает два дня необычайного жара.",
        picture="images/recipe_book/rosario_tincture_bottle.png",
        carriable=True,
        stackable=True,
        usable=True,
        actions=[
            ObjectAction(
                action_id="drink",
                label="Выпить настойку",
                hook="call",
                target="UseDrinkItem",
                args=("rosario_arousal_tincture_001",),
            ),
        ],
        custom_properties={
            "item_kind": "drink",
            "crafted_kind": "rosario_tincture",
            "drink_kind": "libido_tincture",
            "consume_action": "drink",
            "consume_minutes": 10,
            "consume_fun": 5,
            "consume_text": "Вы осторожно пробуете настойку Розарио. Вкус неожиданно медовый, а грибная острота быстро разгоняет кровь. Вы решаете, что о последнем ингредиенте лучше никому не напоминать. Остаются пустая бутылка и пробка.",
            "consume_outputs": (("empty_bottle_001", 1), ("cork_001", 1)),
            "player_libido_days": 2,
            "player_daily_cum_limit": 4,
            "shared_arousal_bonus": 15,
            "shared_fertility_days": 2,
            "shared_conception_permille": 550,
            "shared_effect_text": "От настойки её бросает в жар; действие редкого гриба сохранится на два дня.",
            "gift_value": 1,
        },
    )

    RosarioTinctureRecipePage = RecipePage(
        recipe_id="rosario_arousal_tincture_recipe",
        title="Настойка Розарио",
        image="images/recipe_book/rosario_tincture_recipe.png",
        item_result="rosario_arousal_tincture_001",
        ingredients={
            "chinchilla_droppings_001": {"quantity": 1, "unit": "шарик"},
            "honey_comb_001": {"quantity": 1, "unit": "кусок сот"},
            "ethanol_001": {"quantity": 1, "unit": "бутылка"},
            "special_mushroom_001": {"quantity": 1, "unit": "гриб"},
        },
        unlock_condition=rosario_tincture_recipe_known,
        result_quantity=1,
        craft_minutes=45,
        craft_text="Диван велел сначала растереть редкий гриб с мёдом, а к спирту подойти только после того, как вы перестанете морщиться. Последний шарик вы бросаете в смесь, задержав дыхание. Она на миг пахнет конюшней после дождя, затем внезапно становится сладкой и пряной. «Розарио — гений, — торжественно объявляет диван. — Только не говорите ему, в какой области». Вы закупориваете настойку и подписываете бутылку именем невольного алхимика.",
        craft_failure_text="Розарио не признаёт рецепт без всех четырёх ингредиентов.",
        notes=[
            "По словам дивана, нужны помёт Розарио, мёд, крепкий спирт и редкий гриб; обычная пряная настойка не заменит эту смесь.",
            "Одна порция расходует каждый из четырёх ингредиентов ровно один раз.",
            "Если ещё не договорились с тифлингшей, оставьте пять шариков для обмена на три серебряные монеты.",
        ],
    )
