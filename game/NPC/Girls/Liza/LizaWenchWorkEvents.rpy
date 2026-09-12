# ================================================================================
# Repeatable Lizette waitress-shift event. The daily tavern event definition owns
# availability; this label owns presentation, choice consequences, and return.
# ================================================================================

label EventLizaWenchStory(eyewitness=0):
    $ renpy.dynamic("_liza_wench_variant", "_liza_wench_picture", "_liza_wench_result", "_liza_team_job", "_liza_team_skill", "_liza_team_member", "_liza_team_info")
    $ _liza_wench_variant = procedural_randint(1, 4, "liza_wench_story_%s_%s" % (current_game_day(), calendar_v2.time_slot()))

    if eyewitness <= 0:
        if _liza_wench_variant == 1:
            return "Во время смены Лизетта ловко разносила выпивку и не оставляла посетителей без улыбки и доброго слова."
        elif _liza_wench_variant == 2:
            return "Во время смены Лизетта сумела очаровать одного из купцов и получила от него щедрые чаевые."
        elif _liza_wench_variant == 3:
            return "Во время короткой передышки Лизетта устроилась в углу зала, а затем снова вернулась к посетителям."
        return "Во время смены Лизетта сама поставила на место распустившего руки посетителя и продолжила работу."

    $ main_ui_begin_native_scene_state("Лизетта в зале")
    show screen main_ui

    if _liza_wench_variant == 1:
        $ _liza_wench_picture = LizaStaticData.image_path("tavern", "wench_serving")
        vscene _liza_wench_picture
        $ scene_runtime.text = "Лизетта легко лавирует между занятыми столами, удерживая поднос с полными кружками. Поставив выпивку перед нетерпеливым посетителем, она ловит ваш взгляд и отвечает веселой улыбкой — девушка прекрасно знает, что короткое платьице и стройные ноги привлекают не меньше внимания, чем поданное ею вино."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Похвалить Лизетту за ловкость":
                $ Liza.change_skill("waitress", 1)
                vscene LizaStaticData.image_path("tavern", "wench_happy")
                $ _liza_wench_result = "Вы отмечаете, что она быстро освоилась в переполненном зале. Лизетта довольно расправляет плечи и обещает, что ни один посетитель не останется без кружки."
            "Шепнуть, что вам нравится за ней наблюдать":
                $ Liza.change_social(friend_delta=1, open_delta=1)
                vscene LizaStaticData.image_path("tavern", "wench_happy")
                $ _liza_wench_result = "Проходя мимо, вы тихо говорите, что ее работа радует не только посетителей. Лизетта прикусывает губу, лукаво оглядывается через плечо и уносит поднос к следующему столу."

    elif _liza_wench_variant == 2:
        $ _liza_wench_picture = LizaStaticData.image_path("tavern", "wench_tip")
        vscene _liza_wench_picture
        $ scene_runtime.text = "Один из разомлевших от вина купцов задерживает Лизетту возле стола и вертит между пальцами монету. Девушка не спешит хватать чаевые: она улыбается, наклоняется чуть ближе и парой метких шуток заставляет весь стол заказать еще по кружке. Только после этого Лизетта принимает монету."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Разрешить Лизетте оставить чаевые себе":
                $ Liza.change_social(friend_delta=1)
                vscene LizaStaticData.image_path("tavern", "wench_happy")
                $ _liza_wench_result = "Вы киваете на монету и говорите, что она честно ее заработала. Лизетта прячет чаевые и благодарно подмигивает вам."
            "Похвалить ее умение обращаться с посетителями":
                $ Liza.change_skill("waitress", 1)
                vscene LizaStaticData.image_path("tavern", "wench_happy")
                $ _liza_wench_result = "Вы хвалите ее за то, что одна улыбка принесла трактиру еще несколько заказов. Лизетта смеется и отвечает, что у маменьки научилась добиваться своего без долгих уговоров."

    elif _liza_wench_variant == 3:
        $ _liza_wench_picture = LizaStaticData.image_path("tavern", "wench_corner")
        vscene _liza_wench_picture
        $ scene_runtime.text = "В короткую передышку Лизетта устраивается на лавке в углу зала. Подол ее короткого платьица чуть задрался, открывая край простых панталон, но девушка не спешит его поправлять. Заметив ваш взгляд, она улыбается: «Вы меня поторопить пришли, мастер Стефан, или полюбоваться?»"
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Признаться, что пришли полюбоваться":
                $ Liza.change_social(open_delta=1)
                $ _liza_wench_result = "«Тогда смотрите, пока посетители снова не позвали», — шепчет Лизетта и с невинным видом покачивает носком туфельки."
            "Дать ей спокойно передохнуть":
                $ Liza.change_social(friend_delta=1)
                $ _liza_wench_result = "Вы ставите рядом кружку воды и говорите, что несколько минут отдыха она заслужила. Лизетта благодарно улыбается и обещает скоро вернуться к столам."

    else:
        $ _liza_wench_picture = LizaStaticData.image_path("tavern", "wench_angry")
        vscene _liza_wench_picture
        $ scene_runtime.text = "Один из подвыпивших посетителей решает, что короткое платьице дает ему право хватать служанку за руку. Лизетта резко отступает, не расплескав ни одной кружки, и выставляет ладонь перед нахалом: «Платишь за выпивку — получаешь выпивку. А руки держи при себе!»"
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Поддержать Лизетту и выставить наглеца":
                $ Liza.change_social(friend_delta=1)
                vscene LizaStaticData.image_path("tavern", "wench_happy")
                $ _liza_wench_result = "Вы подтверждаете ее слова и велите посетителю извиниться либо покинуть зал. Когда тот убирается, Лизетта благодарно улыбается: она явно рада, что хозяин трактира не оставил ее одну против наглеца."
            "Доверить Лизетте самой уладить дело":
                $ Liza.change_skill("waitress", 1)
                vscene LizaStaticData.image_path("tavern", "wench_happy")
                $ _liza_wench_result = "Вы остаетесь рядом, но не вмешиваетесь. Лизетта заставляет нахала извиниться, получает оплату за разбитую кружку и уже через минуту снова разносит заказы с победной улыбкой."

    $ scene_runtime.text = _liza_wench_result
    $ scene_runtime.location_text = scene_runtime.text
    if _liza_wench_variant == 2:
        python:
            for _liza_team_job, _liza_team_skill in (("jobwaitress", "waitress"), ("jobcleaning", "cleaning")):
                for _liza_team_member in girls_by_job(_liza_team_job):
                    if _liza_team_member == "liza":
                        continue
                    _liza_team_info = people.get_info(_liza_team_member)
                    if _liza_team_info is not None and _liza_team_info.skill_value(_liza_team_skill, 0) < 100:
                        _liza_team_info.change_skill(_liza_team_skill, 1)
                        _liza_team_info.record_skill_gain(_liza_team_skill)
        $ scene_runtime.text += "\n\nОстальные официантки и уборщицы быстро перенимают ее манеру общаться с гостями: теперь каждая пытается заработать чаевые так же ловко."
        $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к своим делам":
            pass
    $ main_ui_end_native_scene_state()
    return ""
