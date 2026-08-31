# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def irma_tailor_wolf_skin_count():
        return int(player.item_count("wolf_skin_001") or 0) + int(player.item_count("white_wolf_skin_001") or 0)

    def irma_tailor_bear_fur_count():
        return int(player.item_count("bear_fur_brown_001") or 0) + int(player.item_count("bear_fur_grizzly_001") or 0)

    def irma_can_make_warm_cloak():
        return int(player.economy.money or 0) >= 35 and (irma_tailor_bear_fur_count() >= 1 or irma_tailor_wolf_skin_count() >= 2)

    def irma_can_make_fur_bedding():
        return int(player.economy.money or 0) >= 55 and (irma_tailor_bear_fur_count() >= 2 or (irma_tailor_bear_fur_count() >= 1 and irma_tailor_wolf_skin_count() >= 2) or irma_tailor_wolf_skin_count() >= 4)

    def irma_remove_best_bear_fur(amount=1):
        removed = 0
        while removed < int(amount or 0):
            if int(player.item_count("bear_fur_grizzly_001") or 0) > 0:
                player.remove_item("bear_fur_grizzly_001", 1)
                removed += 1
                continue
            if int(player.item_count("bear_fur_brown_001") or 0) > 0:
                player.remove_item("bear_fur_brown_001", 1)
                removed += 1
                continue
            break
        return removed

    def irma_remove_wolf_skins(amount=1):
        removed = 0
        while removed < int(amount or 0):
            if int(player.item_count("wolf_skin_001") or 0) > 0:
                player.remove_item("wolf_skin_001", 1)
                removed += 1
                continue
            if int(player.item_count("white_wolf_skin_001") or 0) > 0:
                player.remove_item("white_wolf_skin_001", 1)
                removed += 1
                continue
            break
        return removed

    def irma_make_warm_cloak():
        if not irma_can_make_warm_cloak():
            return False
        if irma_tailor_bear_fur_count() >= 1:
            if int(irma_remove_best_bear_fur(1) or 0) != 1:
                return False
        elif int(irma_remove_wolf_skins(2) or 0) != 2:
            return False
        player.spend_money(35)
        player.add_item("warm_fur_cloak_001", 1)
        return True

    def irma_make_fur_bedding():
        if not irma_can_make_fur_bedding():
            return False
        if irma_tailor_bear_fur_count() >= 2:
            if int(irma_remove_best_bear_fur(2) or 0) != 2:
                return False
        elif irma_tailor_bear_fur_count() >= 1 and irma_tailor_wolf_skin_count() >= 2:
            if int(irma_remove_best_bear_fur(1) or 0) != 1:
                return False
            if int(irma_remove_wolf_skins(2) or 0) != 2:
                return False
        elif int(irma_remove_wolf_skins(4) or 0) != 4:
            return False
        player.spend_money(55)
        player.add_item("fur_bedroll_001", 1)
        return True


label IntIrmaTalk:
    $ renpy.dynamic("_irma_talk_new")
    $ _irma_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != "irma"
    $ main_ui_begin_talk_state("Разговор с Ирмой", "irma")
    if _irma_talk_new:
        $ scene_runtime.text = "Ирма отвлекается от работы и вопросительно смотрит на вас."
        $ scene_runtime.location_text = scene_runtime.text
        $ scene_runtime.picture = irma_talk_picture_path()
    while True:
        menu:
            "Осмотреть":
                call ShowGirlCard("irma")

            "Подарить маленький подарок" if social_interaction_allowed_for_npc("irma", "gift"):
                call PlayerCardGiftToFixedTargetMenu("irma")

            "Спросить, когда будет готово" if str(dress_shop.produced or "") != "":
                $ scene_runtime.text = "Вы осведомились у Ирмы, скоро ли будет готов ваш заказ. Она ответила, что закончит работу к завтрашнему утру."
                $ scene_runtime.location_text = scene_runtime.text

            "Спросить про теплые плащи и постели":
                $ scene_runtime.text = "Ирма объясняет: для теплого плаща нужен один медвежий мех или две волчьи шкуры и 35 мараведи. Для меховой постели — два медвежьих меха, один медвежий и две волчьи шкуры или четыре волчьи, а за работу 55 мараведи."
                $ scene_runtime.location_text = scene_runtime.text

            "Заказать теплый меховой плащ" if irma_can_make_warm_cloak():
                $ irma_make_warm_cloak()
                $ scene_runtime.text = "Вы отдаете Ирме мех и серебро и получаете добротный теплый меховой плащ."
                $ scene_runtime.location_text = scene_runtime.text

            "Заказать меховую постель" if irma_can_make_fur_bedding():
                $ irma_make_fur_bedding()
                $ scene_runtime.text = "Ирма принимает мех и выдает вам плотную меховую постель."
                $ scene_runtime.location_text = scene_runtime.text

            "Назад":
                $ main_ui_end_talk_state()
                return
