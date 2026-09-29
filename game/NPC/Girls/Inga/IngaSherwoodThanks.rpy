# Inga owns her response to the reopened Cunidale road. The first invitation is
# an event; later visits use the same scene through her NPC conversation menu.

label story_inga_sherwood_gratitude_0:
    $ main_ui_begin_native_scene_state("Инга: свободная дорога")
    show screen main_ui
    vscene "images/inga/newInga/inga_store_openworkdress.png"
    $ scene_runtime.text = "Инга встречает вас улыбкой, которую уже не прячет за прилавком. «Мама сказала, что конь Эдди вернулся, а Робина больше нет на дороге. Лукас опять может возить товар, не оглядываясь на каждом повороте. Спасибо, Стефан. Я сама хотела это сказать»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Принять её приглашение":
            $ main_ui_end_native_scene_state()
            call IngaSherwoodPrivateTime
            if _return:
                $ event_runtime.active_thread.advance()
                return True
            return False
        "Поговорить об этом позже":
            $ main_ui_end_native_scene_state()
            return False


label IngaSherwoodPrivateTime:
    $ renpy.dynamic("_inga_with_lucas", "_inga_private_picture")
    $ _inga_with_lucas = False
    $ _inga_private_picture = "images/inga/newInga/inga_store_openworkdress.png"
    $ main_ui_begin_native_scene_state("Наедине с Ингой")
    show screen main_ui
    vscene _inga_private_picture
    $ scene_runtime.text = "Инга берёт вас за руку. «Я рада, что ты пришёл. Но сначала спроси меня саму, чего я хочу сегодня»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Побыть с Ингой вдвоём":
            pass
        "Пригласить Лукаса" if threads["ingaLucasShare"].completed and (str(rooms.current_code or "") in ("BeckyHome", "TavernMain") or (str(rooms.current_code or "") == "GroceryStore" and 6 <= int(calendar_v2.hour or 0) < 8)):
            $ _inga_with_lucas = True
        "Оставить на другой раз":
            $ main_ui_end_native_scene_state()
            return False

    if _inga_with_lucas:
        $ scene_runtime.text = "Лукас замечает ваш взгляд и поворачивается к Инге. Она кивает только после того, как вы оба даёте ей время решить. «Сегодня — вместе», — говорит она и закрывает за вами дверь."
    else:
        $ scene_runtime.text = "Инга усмехается, запирает дверь и остаётся с вами наедине. Когда вы снова выходите к людям, её щёки всё ещё горят, а благодарность уже не нуждается в словах."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить вместе":
            $ Inga.player_cum("inside")
        "Закончить без риска беременности":
            $ Inga.player_cum("outside")
    $ Inga.set_sex_busy(False)
    $ main_ui_end_native_scene_state()
    return True
