# Mongol's one-time guide to the same full-moon clearing Clarissa visits.
# The thread owns availability; the forest encounter does not alter Clara's thread.

label story_mongol_moon_sabbath_guide_0:
    $ main_ui_begin_native_scene_state("Лесная тропа Монгола")
    show screen main_ui
    vscene "images/mongol/portrait1.jpg"
    $ scene_runtime.text = "Монгол опускает голос: «Сегодня суббота, мастер, и луна круглая. На старой поляне опять соберутся те, кого добрые горожане днем предпочитают не знать. Я покажу тропу, но у костров не шуми: нас там никто не звал»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пойти за Монголом":
            pass
        "Остаться в трактире":
            $ main_ui_end_native_scene_state()
            return False

    vscene "images/forest/hidden_path.png"
    $ scene_runtime.text = "За конюшней Монгол сворачивает с дороги. Он идёт уверенно, без фонаря; вам остаётся следить за его спиной и редкими просветами лунного света между ветвей. Впереди слышны смех и музыка. Монгол останавливается у края поляны и показывает, где укрыться."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Осторожно посмотреть на поляну":
            pass

    $ scene_runtime.text = "Вокруг костров идёт ночное сборище. В пляске и объятиях мелькают незнакомые лица; чуть поодаль Кларисса склонилась над листом и быстро зарисовывает увиденное. Монгол кивает в её сторону: «Вот почему она знает эту дорогу. Оставим художнице её секрет»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Незаметно вернуться с Монголом":
            pass

    $ calendar_v2.advance_minutes(60)
    $ player.change_stat("energy", -5)
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
