# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def irma_tailor_wolf_skin_count():
        return int(player.item_count("wolf_skin_001") or 0) + int(player.item_count("white_wolf_skin_001") or 0)

    def irma_tailor_bear_fur_count():
        return int(player.item_count("bear_fur_brown_001") or 0) + int(player.item_count("bear_fur_grizzly_001") or 0)

    def irma_can_make_warm_cloak():
        return int(money or 0) >= 35 and (irma_tailor_bear_fur_count() >= 1 or irma_tailor_wolf_skin_count() >= 2)

    def irma_can_make_fur_bedding():
        return int(money or 0) >= 55 and (irma_tailor_bear_fur_count() >= 2 or (irma_tailor_bear_fur_count() >= 1 and irma_tailor_wolf_skin_count() >= 2) or irma_tailor_wolf_skin_count() >= 4)

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
        global money
        global money
        global money
        if not irma_can_make_warm_cloak():
            return False
        if irma_tailor_bear_fur_count() >= 1:
            if int(irma_remove_best_bear_fur(1) or 0) != 1:
                return False
        elif int(irma_remove_wolf_skins(2) or 0) != 2:
            return False
        money = int(money or 0) - 35
        player.add_item("warm_fur_cloak_001", 1)
        return True

    def irma_make_fur_bedding():
        global money
        global money
        global money
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
        money = int(money or 0) - 55
        player.add_item("fur_bedroll_001", 1)
        return True


    def irma_talk_action_items():
        items = [MenuItem("Осмотреть", Call("IntIrmaTalkApply", "inspect"))]
        if str(dress_shop.produced or "") != "":
            items.append(MenuItem("Спросить, когда будет готово", Call("IntIrmaTalkApply", "ask_ready")))
        items.append(MenuItem("Спросить про теплые плащи и постели", Call("IntIrmaTalkApply", "ask_winter_work")))
        if irma_can_make_warm_cloak():
            items.append(MenuItem("Заказать теплый меховой плащ", Call("IntIrmaTalkApply", "make_cloak")))
        if irma_can_make_fur_bedding():
            items.append(MenuItem("Заказать меховую постель", Call("IntIrmaTalkApply", "make_bedding")))
        items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
        return items


    def irma_talk_action_items():
        items = [MenuItem("Осмотреть", Call("IntIrmaTalkApply", "inspect"))]
        if str(dress_shop.produced or "") != "":
            items.append(MenuItem("Спросить, когда будет готово", Call("IntIrmaTalkApply", "ask_ready")))
        items.append(MenuItem("Спросить про теплые плащи и постели", Call("IntIrmaTalkApply", "ask_winter_work")))
        if irma_can_make_warm_cloak():
            items.append(MenuItem("Заказать теплый меховой плащ", Call("IntIrmaTalkApply", "make_cloak")))
        if irma_can_make_fur_bedding():
            items.append(MenuItem("Заказать меховую постель", Call("IntIrmaTalkApply", "make_bedding")))
        items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
        return items


    def irma_talk_action_items():
        items = [MenuItem("Осмотреть", Call("IntIrmaTalkApply", "inspect"))]
        if str(dress_shop.produced or "") != "":
            items.append(MenuItem("Спросить, когда будет готово", Call("IntIrmaTalkApply", "ask_ready")))
        items.append(MenuItem("Спросить про теплые плащи и постели", Call("IntIrmaTalkApply", "ask_winter_work")))
        if irma_can_make_warm_cloak():
            items.append(MenuItem("Заказать теплый меховой плащ", Call("IntIrmaTalkApply", "make_cloak")))
        if irma_can_make_fur_bedding():
            items.append(MenuItem("Заказать меховую постель", Call("IntIrmaTalkApply", "make_bedding")))
        items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
        return items


label IntIrmaTalk(show_menu=True):
    if not bool(show_menu):
        call GirlsDesc("irma")
        return

    $ main_ui_begin_talk_state("Разговор с Ирмой", "irma")
    $ current_action_title = "Разговор с Ирмой"
    $ current_action_content = None
    $ MainTxt = "Ирма отвлекается от работы и вопросительно смотрит на вас."
    $ CurLocDesc = MainTxt
    $ _layout_last_picture = irma_talk_picture_path()
    call ShowImage("", "", irma_talk_picture_path())
    call IntIrmaTalkRefresh
    return


label IntIrmaTalkRefresh(girl_name="irma"):
    $ main_ui_begin_talk_state("Разговор с Ирмой", "irma")
    $ current_action_title = "Разговор с Ирмой"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Осмотреть", Call("IntIrmaTalkApply", "inspect"))]

    if str(DressProduced or "") != "":
        $ current_action_items.append(MenuItem("Спросить, когда будет готово", Call("IntIrmaTalkApply", "ask_ready")))
    $ current_action_items.append(MenuItem("Спросить про теплые плащи и постели", Call("IntIrmaTalkApply", "ask_winter_work")))
    if irma_can_make_warm_cloak():
        $ current_action_items.append(MenuItem("Заказать теплый меховой плащ", Call("IntIrmaTalkApply", "make_cloak")))
    if irma_can_make_fur_bedding():
        $ current_action_items.append(MenuItem("Заказать меховую постель", Call("IntIrmaTalkApply", "make_bedding")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntIrmaTalkApply(choice_code="", dress_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard("irma", "DressShopRoomActions")
        return

    if str(choice_code or "") == "ask_ready":
        $ MainTxt = "Вы осведомились у Ирмы, скоро ли будет готов ваш заказ.\n\nОна подняла на вас удивленный взгляд и ответила, что, как она и говорила, закончит работу она к завтрашнему утру."
        $ CurLocDesc = MainTxt
        $ _layout_last_picture = irma_talk_picture_path()
        call ShowImage("", "", irma_talk_picture_path())
        call IntIrmaTalkRefresh
        return

    if str(choice_code or "") == "ask_winter_work":
        $ MainTxt = "Вы спрашиваете Ирму, что она может сделать из шкур и меха к холодам. Швея сразу оживляется и начинает перечислять без лишней лирики.\n\n\"На теплый меховой плащ мне либо один хороший медвежий мех нужен, либо две волчьи шкуры. За работу возьму 35 мараведи. А если хочешь теплую постель в комнату или для гостевой, то неси два медвежьих меха. В крайнем случае сгодится один медвежий и две волчьи шкуры, или четыре волчьи. За такую работу возьму 55 мараведи,\" деловито говорит Ирма."
        $ CurLocDesc = MainTxt
        $ _layout_last_picture = irma_talk_picture_path()
        call ShowImage("", "", irma_talk_picture_path())
        call IntIrmaTalkRefresh
        return

    if str(choice_code or "") == "make_cloak":
        if not irma_make_warm_cloak():
            $ MainTxt = "Пока что у вас не хватает либо шкур, либо денег на такой заказ."
        else:
            $ MainTxt = "Вы договариваетесь с Ирмой о работе, отдаете ей мех и серебро, и спустя некоторое время получаете добротный теплый меховой плащ. Такая вещь пригодится и в хозяйстве, и как дорогой подарок."
        $ CurLocDesc = MainTxt
        $ _layout_last_picture = irma_talk_picture_path()
        call ShowImage("", "", irma_talk_picture_path())
        call IntIrmaTalkRefresh
        return

    if str(choice_code or "") == "make_bedding":
        if not irma_make_fur_bedding():
            $ MainTxt = "Пока что у вас не хватает либо меха, либо денег на такую работу."
        else:
            $ MainTxt = "Ирма быстро прикидывает раскрой, принимает мех и через некоторое время выдает вам плотную меховую постель. Ее можно оставить себе, пристроить в гостевую комнату или выгодно сбыть."
        $ CurLocDesc = MainTxt
        $ _layout_last_picture = irma_talk_picture_path()
        call ShowImage("", "", irma_talk_picture_path())
        call IntIrmaTalkRefresh
        return

    call DressShopRoomActions
    return
