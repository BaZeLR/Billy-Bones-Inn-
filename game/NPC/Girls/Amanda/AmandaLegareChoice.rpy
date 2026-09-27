label story_amanda_legare_choice_0:
    $ renpy.dynamic("_amanda_legare_decision")
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
        $ Amanda.enable_tavern_service("intimate")
        if tavern.renovation_complete("glory_hole"):
            $ Amanda.enable_tavern_service("gloryhole")
        $ Amanda.assign_tavern_service("intimate", tomorrow=True)
        $ scene_runtime.text = "Прошло три дня. Аманда говорит, что не станет прекращать встречи с Легаре. Она согласна зарабатывать в трактире на собственные расходы и с завтрашнего дня приступит к новой работе."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Принять ее решение":
                pass

    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return
