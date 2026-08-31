# ================================================================================
# Clarissa's night-market, hidden-stash, and cursed-sofa continuation.
# Availability is owned by claraForestSofa in StoryEventRuntime.rpy.
# ================================================================================

label story_clara_forest_sofa_market_0:
    $ main_ui_begin_native_scene_state("Кларисса на ночном рынке")
    show screen main_ui
    vscene "images/clara/market_night.png"
    $ scene_runtime.text = "На закрытом рынке вы снова замечаете Клариссу рядом с тем самым тайным торговцем. На этот раз она приносит не рисунки: девушка пересчитывает долю с грязной сделки и сердито спорит, что Монгол обещал больше. Получив тяжелый кошелек, Кларисса прячет его под плащ и уходит не к винной лавке, а к дороге за город."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Проследить до окраины":
            pass
    $ scene_runtime.text = "Вы держитесь в тени и видите, как у лесной дороги Кларисса проверяет узел на поясе, потом сворачивает к старой водокачке за скрытой тропой. Дальше идти за ней слишком опасно: на открытом месте она сразу заметит хвост. Но теперь вы знаете район тайника. Точные приметы нанесены на внутреннюю сторону потерянных ею панталон, а закопанный кошелек без лопаты из мерзлой земли не достать."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться на площадь":
            pass
    $ calendar_v2.advance_minutes(30)
    $ player.change_stat("energy", -5)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_forest_sofa_stash_1:
    $ main_ui_begin_native_scene_state("Тайник Клариссы")
    show screen main_ui
    vscene "images/forest/hidden_path.png"
    $ scene_runtime.text = "Сверяясь с угольными отметками на панталонах Клариссы, вы находите за старой водокачкой дерево с вырезанным знаком. Походная лопата вскоре ударяется о завернутый в промасленную ткань сверток. Внутри лежат шестьсот мараведи — доля Клариссы от ее рыночной аферы."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Забрать спрятанные деньги":
            pass
    $ player.add_money(600)
    $ player.change_stat("energy", -10)
    $ calendar_v2.advance_minutes(60)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
