# The Robin resolution opens this one-time arrival three game days after Becky
# receives Eddie's horse and purse. Mongol owns his service date and status.

label story_mongol_tavern_arrival_0:
    $ renpy.dynamic("_mongol_reward_horse")
    $ main_ui_begin_native_scene_state("Монгол возвращается")
    show screen main_ui
    vscene "images/mongol/portrait1.jpg"
    $ scene_runtime.text = "У ворот «Дикого жеребца» раздаётся стук копыт. Монгол придерживает жеребца, а за ним стоит дорожная карета. «Три дня искал, чем отплатить, мастер Стефан. Дорога теперь свободна — пусть и у тебя в конюшне будет прибавление. Конь, карета и мои руки к твоим услугам»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Принять Монгола на службу":
            pass
    $ _mongol_reward_horse = RandomStallionNameCode()
    if player.horse.owns_horse():
        $ player.horse.add_stable_horse(_mongol_reward_horse)
    else:
        $ player.horse.acquire(_mongol_reward_horse, 0, True)
    $ player.horse.carriage_ready = True
    $ Mongol.tavern_servant = True
    $ Mongol.arrival_day = current_game_day()
    $ Mongol.known = True
    $ tractir_activate_achievement("mongol_household")
    $ event_runtime.active_thread.advance()
    $ scene_runtime.text = "Монгол заводит %s в свободный денник и ставит карету под навес. «Дрова наколю из ваших брёвен, золу вычищу, коней причешу. Если купальня уже готова и есть топливо, вода к утру будет горячая. Без брёвен чудес не обещаю, зато отчитаюсь честно»." % _mongol_reward_horse
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Осмотреть пополнение в конюшне позже":
            pass
    $ main_ui_end_native_scene_state()
    call TractirShowPendingAchievements
    return True
