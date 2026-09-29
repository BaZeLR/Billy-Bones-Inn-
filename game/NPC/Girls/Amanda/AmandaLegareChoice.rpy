label story_amanda_legare_choice_0:
    $ renpy.dynamic("_amanda_legare_decision", "_amanda_job")
    $ _amanda_legare_decision = Amanda.decide("amanda_legare_choice")
    $ main_ui_begin_native_scene_state("Решение Аманды")
    show screen main_ui

    if _amanda_legare_decision["reaction"] == "good":
        $ Amanda.set_var("legare_choice_outcome", "tavern")
        vscene "images/player_room/amandaVisits/amanda_visit_0.jpg"
        $ scene_runtime.text = "На третий вечер Аманда сама приходит к вашей двери. Она говорит, что прекратила встречи с Легаре и хочет остаться здесь."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Выслушать Аманду":
                pass
        vscene "images/player_room/amandaVisits/remorse_visit_0.jpg"
        $ scene_runtime.text = "Аманда просит прощения. Теперь она ждет вашего ответа, а не пытается отшутиться."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Простить ее":
                $ Amanda.change_social(friend_delta=1)
            "Сказать, что вам нужно время":
                pass
        vscene "images/player_room/amandaVisits/remorse_visit_1.jpg"
        $ scene_runtime.text = "Она остается рядом еще ненадолго."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Пожелать спокойной ночи":
                pass
            "Предложить ей остаться" if Amanda.var_value("legare_choice_outcome", "") == "tavern":
                call IntAmandaSex("amanda", "mc_room")
                vscene "images/player_room/amandaVisits/hornynightsleep.jpg"
                $ scene_runtime.text = "Позднее вы засыпаете рядом."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Уснуть":
                        pass
        vscene "images/player_room/amandaVisits/remorese_visit_end.jpg"
        $ scene_runtime.text = "Утром вы вспомните, что решение Аманда приняла сама."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Продолжить":
                pass
    else:
        $ Amanda.set_var("legare_choice_outcome", "service")
        $ Amanda.set_var_int("legare_service_decision_day", int(current_game_day() or 0))
        python:
            for _amanda_job in ("jobkitchen", "jobcleaning", "jobwaitress", "jobkitchentomorrow", "jobcleaningtomorrow", "jobwaitresstomorrow"):
                Amanda.set_job_value(_amanda_job, 0)
        $ Amanda.enable_tavern_service("intimate")
        if tavern.renovation_complete("glory_hole"):
            $ Amanda.enable_tavern_service("gloryhole")
        $ Amanda.assign_tavern_service("intimate", tomorrow=True)
        $ scene_runtime.text = "Прошло три дня. Аманда говорит, что не станет прекращать встречи с Легаре. Она согласна зарабатывать в трактире на собственные расходы и с завтрашнего дня приступит к новой работе. Вы объявите условия дому за завтраком."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Принять ее решение":
                pass

    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return


label story_amanda_legare_service_breakfast:
    $ main_ui_begin_native_scene_state("Решение Аманды за завтраком")
    show screen main_ui
    vscene tavern_kitchen_breakfast_picture()
    $ scene_runtime.text = "За завтраком вы объявляете дому решение Аманды: она продолжит встречаться с Легаре и станет отдельно зарабатывать на собственные расходы. С этого дня она больше не считается частью обычной команды трактира."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Объявить условия":
            pass
    $ tavern.client_touch_policy = "hands_off"
    if Amanda.wardrobe.owns("slutdress"):
        $ Amanda.wardrobe.set_day_dress("slutdress")
    $ scene_runtime.text = "Вы устанавливаете цены для Аманды: 20 мараведи за услугу в глорихоле и 300 за встречу в гостевой комнате. Шестьдесят процентов поступают в кассу трактира, остальное остается ей. Для Лизетты и Жоржетты прежние условия не меняются. Остальных работниц гостям трогать запрещено."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ scene_runtime.text = "Сандра не скрывает слез. После завтрака Лизетта и Жоржетта провожают Аманду в ее комнату; за столом на несколько мгновений становится тихо." if Liza.is_tavern_worker() and Georgett.is_tavern_worker() else "Сандра не скрывает слез. За столом на несколько мгновений становится тихо."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить разговор":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_amanda_service_dress_order:
    $ renpy.dynamic("_amanda_dress_price")
    $ _amanda_dress_price = _gds_dress_cost("slutdress")
    $ main_ui_begin_native_scene_state("Покупка Аманды")
    show screen main_ui
    vscene "images/irma/portraits/portrait3.png"
    $ scene_runtime.text = "В лавке Ирмы вы застаете Аманду у образцов коротких платьев. Она сама выбрала наряд и отсчитывает портнихе %d мараведи из собственного заработка. Ирма обещает принести готовое платье завтра." % _amanda_dress_price
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить":
            pass
    $ Amanda.add_var_int("legare_service_savings", -_amanda_dress_price)
    $ dress_shop.produced = "slutdress"
    $ dress_shop.buyer = "amanda"
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
