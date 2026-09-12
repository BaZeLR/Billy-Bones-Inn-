label story_amanda_tavern_seduction_0:
    $ renpy.dynamic("_amanda_seduction_finish", "_amanda_seduction_profile")
    $ main_ui_begin_native_scene_state("Флирт Аманды")
    show screen main_ui
    call ShowImage("", "", AmandaStaticData.portrait)
    $ scene_runtime.text = "В зале Аманда задержалась у стойки дольше обычного. Она будто ждала, пока вы заметите ее новое платье, поправила волосы и улыбнулась слишком невинно."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ scene_runtime.text = "Это еще не прямое приглашение, но уже и не простая болтовня работницы с хозяином."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    menu:
        "Подыграть":
            $ scene_runtime.text = "Вы ответили ей в том же тоне. Аманда вспыхнула, но не отступила, только ниже опустила голос и пообещала вечером быть послушнее, если вы тоже будете к ней внимательнее."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
            $ Amanda.change_mana(1, "tavern_seduction_attention")
            $ Amanda.apply_social_chance(0, 0, 1, 2, 0, 0, "tavern_seduction_attention")
            $ main_ui_end_native_scene_state()
            return True
        "Позвать наверх" if int(Amanda.rel or 0) >= 12 and int(Amanda.corruption or 0) >= 35 and not bool(Amanda.sex_stat("virginity", True)) and Amanda.date_intimacy_available() and player.intimacy.can_cum():
            $ scene_runtime.text = "Вы тихо предложили ей оставить зал на пару минут. Аманда посмотрела на лестницу, прикусила губу и пошла первой."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"

            $ main_ui_runtime.action_title = "Аманда у окна"
            vscene "NPC/Girls/Amanda/flirts_new room.jpg"
            $ scene_runtime.text = "Едва дверь закрылась, Аманда подвела вас к окну и чуть раздвинула занавеску. Во дворе снова разыгрывалось знакомое представление.\n\n" + attic_neighbor_sex_scene_text()
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"

            $ scene_runtime.text = "Аманда смотрела не отрываясь. Потом она обернулась, задрала подол до пояса и, опершись ладонями о подоконник, вызывающе подалась к вам бедрами."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Подойти к Аманде сзади":
                    pass

            call BeginPaidSexModule("amanda", "TavernAmandaRoom")
            $ Amanda.set_layer_raised("bottom", 1)
            $ Amanda.remove_clothing_layer("panties")
            $ Amanda.set_cock_position("pussy")
            $ Amanda.set_var_int("knownotvirgin", 1)
            $ Amanda.set_var_int("fuckyou", 1)
            $ player.intimacy.set_arousal(100)
            $ Amanda.set_arousal(100)
            $ scene_runtime.text = "Вы вошли в Аманду одним уверенным движением и быстро взяли жесткий ритм. Она не отводила взгляда от соседнего двора и двигалась вам навстречу, будто старалась попасть в такт доносившимся оттуда ударам и стонам."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"

            menu:
                "Шлепнуть Аманду по ягодицам":
                    $ scene_runtime.text = "Ваша ладонь звонко опустилась на ее ягодицу. Аманда вскрикнула, тут же прикусила край занавески, но уже через мгновение сама подставилась под следующий шлепок."
                    $ scene_runtime.location_text = scene_runtime.text
                    "[scene_runtime.text]"

            $ scene_runtime.text = "Вы ускорились. Аманда больше не пыталась сдерживаться: ее громкие стоны смешались со стонами женщины за окном, и на несколько минут обе пары словно устроили негласное соревнование. Наконец Аманда задрожала всем телом и шумно кончила, продолжая прижиматься к вам."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
            $ Amanda.record_orgasm_given()
            $ Amanda.set_arousal(20)

            menu:
                "Кончить в Аманду":
                    $ _amanda_seduction_finish = "inside"
                    $ scene_runtime.text = "Вы крепко удержали Аманду за бедра и кончили глубоко внутри. Она тихо охнула, почувствовав, как горячее семя наполняет ее, а затем еще раз вздрогнула у вас в руках."
                    $ scene_runtime.location_text = scene_runtime.text
                    "[scene_runtime.text]"
                    $ Amanda.player_cum("inside")

                "Вытащить и кончить на ягодицы":
                    $ _amanda_seduction_finish = "outside"
                    $ scene_runtime.text = "В последний момент вы вышли из Аманды и густо залили ее разгоряченные ягодицы. Она оглянулась через плечо, тяжело дыша и довольно улыбаясь."
                    $ scene_runtime.location_text = scene_runtime.text
                    "[scene_runtime.text]"
                    $ Amanda.player_cum("outside")

            $ _amanda_seduction_profile = build_girl_decision_profile("amanda")
            if bool(_amanda_seduction_profile.get("likes_player", 0.0)):
                vscene "images/amanda/sexroom/minet9.jpg"
                $ scene_runtime.text = "Когда вы отступили, Аманда развернулась, опустилась перед вами на колени и с неожиданной заботой взяла ваш обмякший член в рот. Она медленно очистила его губами и языком, не оставив ни капли, а потом подняла на вас довольный взгляд."
                $ scene_runtime.location_text = scene_runtime.text
                "[scene_runtime.text]"
                $ Amanda.set_var_int("suckyou", 1)
            else:
                vscene "NPC/Girls/Amanda/flirts_new room.jpg"
                $ scene_runtime.text = "Аманда торопливо привела себя в порядок и протянула вам кусок ткани, чтобы вытереться."
                $ scene_runtime.location_text = scene_runtime.text
                "[scene_runtime.text]"

            $ scene_runtime.text = "Вы оба быстро оделись и вернулись в зал по одному, стараясь не привлекать внимания посетителей."
            $ scene_runtime.location_text = scene_runtime.text
            "[scene_runtime.text]"
            $ Amanda.set_arousal(0)
            $ Amanda.set_sex_busy(False)
            call FinishPaidSexModule("amanda", "TavernAmandaRoom")
            $ main_ui_end_native_scene_state()
            return True
        "Вернуть к работе":
            $ scene_runtime.text = ""
            $ scene_runtime.location_text = ""
            $ Amanda.yell_not_work()
            $ main_ui_end_native_scene_state()
            return True


label story_amanda_legare_tavern_visit_0:
    show screen main_ui
    call ShowImage("alber", "", "portrait")
    "Ближе к вечеру в трактир заглянул месье Легаре. Он заказал кувшин вина не у стойки, а так, чтобы Аманда сама подошла к его столу."
    "Аманда старалась держаться деловито, но ее улыбка выдавала, что этот визит не совсем случайный."
    menu:
        "Понаблюдать":
            "Вы не вмешались. Легаре говорил тихо и обходительно, Аманда отвечала коротко, но задерживалась у его стола каждый раз чуть дольше, чем требовала работа."
            $ Amanda.legare_affection = min(20, Amanda.legare_affection + 1)
            return True
        "Отозвать Аманду":
            "Вы позвали Аманду к стойке и нашли ей работу подальше от столика Легаре. Она подчинилась, но бросила на вас недовольный взгляд."
            $ Amanda.legare_affection = max(0, Amanda.legare_affection - 1)
            $ Amanda.change_mana(-1, "blocked_legare_tavern_visit")
            return True
        "Прямо запретить":
            "Вы велели Аманде не крутиться у стола Легаре. Виноторговец вежливо поднял руки, будто ни при чем, а Аманда побледнела от злости и стыда."
            $ Amanda.legare_forbidden = True
            $ Amanda.legare_affection = max(0, Amanda.legare_affection - 2)
            $ Amanda.change_mana(-2, "forbid_legare_tavern_visit")
            return True


label story_amanda_street_legare_sighting_0:
    $ renpy.dynamic("_amanda_legare_event")
    show screen main_ui
    $ _amanda_legare_event = None
    call ShowImage("", "", AmandaStaticData.portrait)
    if str(rooms.current_code or "") == "MarketPlace":
        "Между лавками вы заметили Аманду. Она шла быстро, то и дело оглядываясь, а впереди у винных рядов ее явно ждал месье Легаре."
    else:
        "У выхода из трактира Аманда скользнула вдоль стены так осторожно, будто сама понимала, насколько неубедительно выглядит ее тайная прогулка."
        "За углом мелькнул знакомый силуэт Легаре."
    menu:
        "Проследить за ней":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun") <= 0:
                return False
            $ _amanda_legare_event = GetSexEventFromTable("amanda", calendar_v2.time_slot(), "legarerun")
            jump AfterDanceSexLegare
        "Оставить ее в покое":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun") <= 0:
                return False
            $ _amanda_legare_event = GetSexEventFromTable("amanda", calendar_v2.time_slot(), "legarerun")
            "Вы решили не устраивать сцену на улице. Аманда скоро скрылась за поворотом, почти наверняка догнав Легаре."
            $ Amanda.resolve_legare_let_go()
            return True
        "Отправить ее обратно на работу":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun") <= 0:
                return False
            $ _amanda_legare_event = GetSexEventFromTable("amanda", calendar_v2.time_slot(), "legarerun")
            $ Amanda.yell_not_work()
            return True


label story_amanda_street_lover_encounter_0:
    show screen main_ui
    call ShowImage("", "", AmandaStaticData.portrait)
    "На улице вы заметили Аманду рядом с каким-то молодым горожанином. Он что-то торопливо доказывал, а она смеялась и не спешила уходить."
    menu:
        "Подойти ближе":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "lovermeet") <= 0:
                return False
            $ GetSexEventFromTable("amanda", calendar_v2.time_slot(), "lovermeet")
            jump AmandaLoverSex
        "Окликнуть Аманду и вернуть к работе":
            if CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "lovermeet") <= 0:
                return False
            $ GetSexEventFromTable("amanda", calendar_v2.time_slot(), "lovermeet")
            $ Amanda.yell_not_work()
            return True
        "Не вмешиваться":
            "Вы прошли мимо. Если Аманда решила искать себе приключения, то этот разговор еще можно будет отложить до вечера."
            return True
