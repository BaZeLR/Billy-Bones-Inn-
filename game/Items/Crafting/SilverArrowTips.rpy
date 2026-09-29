# The three coins from the Rosario settlement become one batch of three tips.
# The recipe book remains the owner of ingredients, time, and crafted output.
init 5 python:
    def silver_arrow_tips_recipe_known():
        favor = threads.get("nostarRosarioFavor")
        return bool(
            player_has_soap_recipe_book()
            and favor is not None
            and (favor.completed or int(favor.num or 0) >= 3)
        )

    SilverArrowTipItem = GameItem(
        object_id="silver_arrow_tip_001",
        name="серебряный наконечник стрелы",
        description="Небольшой литой наконечник из серебра тифлингши. Пока это отдельная заготовка, а не снаряжённая стрела.",
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafting_material",
            "material_kind": "silver_arrow_tip",
        },
    )

    SilverArrowTipsRecipePage = RecipePage(
        recipe_id="silver_arrow_tips_recipe",
        title="Литые серебряные наконечники",
        image="images/recipe_book/silver_arrow_tips_recipe.png",
        item_result="silver_arrow_tip_001",
        ingredients={
            "silver_coin_001": {"quantity": 3, "unit": "монеты"},
            "chopped_wood_001": {"quantity": 1, "unit": "полено"},
        },
        unlock_condition=silver_arrow_tips_recipe_known,
        result_quantity=3,
        craft_minutes=90,
        craft_text="Вы разводите сильный огонь и раскладываете три серебряные монеты рядом с нарисованной в книге формой. В тигле серебро сперва упрямо держит знакомый чеканный узор, затем сплавляется в одну светлую каплю. Вы осторожно разливаете её по трём гнёздам формы. Пока металл остывает, огонь доедает полено. Наконец вы раскрываете форму: на ладони лежат три серебряных наконечника, каждый со своей небольшой неровностью от литья. Теперь им нужны древки; сами по себе они ещё не стрелы.",
        craft_failure_text="Для отливки нужны все три серебряные монеты и топливо для огня.",
        notes=[
            "Чертёж показывает одну отливку из трёх монет: три наконечника за полтора часа работы.",
            "Колотое полено расходуется на жар. Готовые наконечники ещё надо будет закрепить на стрелах; этот рецепт не создаёт боеприпасы.",
        ],
    )
