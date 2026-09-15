# One-time consensual continuation of Inga and Lucas's HomeFront encounter.
# Thread availability is owned by ingaLucasShare; this label owns only its scene.
label story_inga_lucas_share_0:
    $ main_ui_begin_native_scene_state("Инга и Лукас")
    show screen main_ui
    $ scene_runtime.picture = "images/inga/StreetSex/fuckyou1.jpg"
    vscene scene_runtime.picture
    $ scene_runtime.text = "Вы повторяете свое прежнее нахальное предложение, но на этот раз Лукас не отшучивается. Он вопросительно смотрит на Ингу, оставляя решение за ней. Инга раскрасневшись улыбается и сама манит вас ближе: «Если вы оба хотите, я тоже хочу. Только не заставляйте меня ждать»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Присоединиться":
            pass

    $ scene_runtime.picture = "images/inga/StreetSex/fuckyou2.jpg"
    vscene scene_runtime.picture
    $ scene_runtime.text = "Лукас отступает к стене, а Инга становится перед вами на колени и нетерпеливо приподнимает платье. Вы входите в нее сзади; она громко выдыхает и, оглянувшись на вас через плечо, начинает двигаться навстречу каждому толчку."
    $ scene_runtime.location_text = scene_runtime.text
    $ Inga.set_cock_position("pussy")
    $ player_apply_arousal_trigger("inga_lucas_share", max(0, 100 - int(player.intimacy.arousal_value() or 0)))
    menu:
        "Продолжить":
            pass

    $ scene_runtime.picture = "images/inga/StreetSex/fuckyou4.jpg"
    vscene scene_runtime.picture
    $ scene_runtime.text = "Инга все сильнее подается назад, не смущаясь внимательного взгляда Лукаса. Почувствовав, что вы уже близко, она прижимается к вам и прямо просит не останавливаться и кончить в нее."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Кончить внутрь":
            $ Inga.player_cum("inside")

    $ scene_runtime.picture = "images/inga/StreetSex/fuckyou5.jpg"
    vscene scene_runtime.picture
    $ scene_runtime.text = "Вы прижимаете Ингу к себе и разряжаетесь глубоко внутри. Она удовлетворенно смеется, а Лукас одобрительно хлопает вас по плечу: теперь прежняя шутка действительно стала общим приключением."
    $ scene_runtime.location_text = scene_runtime.text
    $ Inga.set_sex_busy(False)
    $ Inga.change_social(friend_delta=1, open_delta=1)
    $ event_runtime.active_thread.advance()
    menu:
        "Зайти в дом":
            $ main_ui_end_native_scene_state()
            return True
