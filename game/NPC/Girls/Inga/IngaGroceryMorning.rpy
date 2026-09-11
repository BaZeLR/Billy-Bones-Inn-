# The morning encounter is an alternative opening of the existing
# Inga/Lucas thread; its later Becky conversations keep their original stages.
label story_inga_grocery_morning_0:
    $ main_ui_begin_native_scene_state("Ранний покупатель")
    $ scene_runtime.picture = rooms.get("GroceryStore").bg_picture
    vscene scene_runtime.picture
    $ scene_runtime.text = "Лавка уже открыта, но за прилавком никого нет. Из-за занавески доносится приглушенный смех. «Лукас, тише, покупатели услышат!» — шепчет знакомый женский голос."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Деликатно кашлянуть":
            $ scene_runtime.text = "За занавеской мгновенно становится тихо. «Одну минуту!» — отзывается девушка. Вы отворачиваетесь к полкам, оставляя парочке возможность привести себя в порядок."
        "Подождать у прилавка":
            $ scene_runtime.text = "Вы разглядываете банки с пряностями и делаете вид, что ничего не слышите. Через минуту занавеска шевелится; девушка тихонько смеется, а ее спутник просит хотя бы не рассказывать об этом всей площади."
        "Зайти в другой раз":
            $ main_ui_end_native_scene_state()
            $ apply_movement_time(10, "MarketPlace")
            jump MarketPlace
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    if Inga.known:
        $ scene_runtime.text = "Из-за занавески выходит Инга, поправляя передник. За ней появляется молодой человек с весьма довольным видом. «Доброе утро, Стефан. Знакомься, это Лукас, мой жених. Он помогал мне открыть лавку», — говорит она, изо всех сил стараясь не рассмеяться."
    else:
        $ scene_runtime.text = "Из-за занавески выходит рыжеволосая девушка, поправляя передник. За ней появляется молодой человек с весьма довольным видом. «Я Ингенборг, дочка Бекки. По утрам подменяю ее в лавке. А это Лукас, мой жених», — представляется она."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "«Вижу, утро у вас началось удачно», — замечаете вы. Лукас вдруг очень заинтересовывается мешком крупы. Инга прыскает: «Хороший завтрак — залог хорошего дня. Но покупателя мы голодным тоже не отпустим!»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к покупкам":
            $ Inga.mark_known()
            $ Inga.acquaintance_stage = max(Inga.acquaintance_stage, 1)
            $ event_runtime.active_thread.advance()
            $ main_ui_end_native_scene_state()
            return True
