# ================================================================================
# Clarissa's private-room game continuation.
# Availability and progress belong to the claraPrivateGames thread. This label
# owns only the authored introduction and consent choices. Repeatable intimacy
# remains in the shared household engine.
# ================================================================================

# Event: after moving into the tavern and completing the earlier locked-room
# visits, Clarissa answers why the player was not invited into the girls' room.
# Choices:
# - accept Clarissa's rules: consensual touching and oral sex advance the thread
# - stop: no sexual action is recorded and the event can be retried another day
label story_clara_private_games_0:
    $ main_ui_begin_native_scene_state("Игры Клариссы")
    show screen main_ui
    vscene ClaraStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "Оставшись с Клариссой наедине, вы наконец спрашиваете, почему она и Мелисса прежде запирали дверь и не хотели пускать вас в комнату."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Выслушать Клариссу":
            pass

    $ scene_runtime.text = "Кларисса усмехается: «Потому что ты пока не умеешь играть, Стефан. Одного любопытства мало — надо быть достаточно смелым и слушать правила. Хочешь узнать, какие именно игры? Тогда всё будет только по взаимному желанию, и если кто-то скажет остановиться, мы сразу остановимся»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Согласиться на её правила":
            pass

        "Не настаивать":
            $ main_ui_end_native_scene_state()
            return True

    $ scene_runtime.text = "Кларисса подходит ближе, целует вас и сама направляет вашу ладонь между своих бёдер. Она не торопится, наблюдая за вашей реакцией, а затем шепчет с лукавой улыбкой: «Что, я заставляю тебя нервничать?»"
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить по её правилам":
            pass

        "Остановиться":
            $ main_ui_end_native_scene_state()
            return True

    $ scene_runtime.text = "Получив ясное согласие, Кларисса опускается перед вами и предлагает продолжить игру ртом. Дальше она позволяет вам самим выбирать темп, но напоминает, что остановится по первому слову."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить игру":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    call HouseholdSexEngine("clara", "TavernMelissaRoom", "blowjob")
    return True
