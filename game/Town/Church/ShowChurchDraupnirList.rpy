# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowChurchDraupnirList:
    $ renpy.dynamic("IList", "StrList", "entry", "show_list")
    python:
        StrList = []
        for IList in range(len(CHURCH_REPAIR_DESCRIPTIONS)):
            entry = "{}. {}: {} мараведи.".format(IList + 1, CHURCH_REPAIR_DESCRIPTIONS[IList], CHURCH_REPAIR_COSTS[IList])
            if player.economy.church_repair_is_donated(IList):
                entry = "[s]{}[/s]".format(entry)
            StrList.append(entry)
        show_list = "\n".join(StrList)

    $ scene_runtime.text = "Вы с интересом ознакомились со счетом, выставленным мастером Драупниром:\n\n" + show_list
    if player.economy.church_donated_today > 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nВы сегодня уже сделали пожертвование святой церкви и на душе у вас благостно и возвышенно, а карманы малость полегчали."
    $ scene_runtime.location_text = scene_runtime.text
    vscene "images/church/confessionEntry.png"
    $ main_ui_runtime.action_title = "Листок на столике"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []

    python:
        for IList in range(len(CHURCH_REPAIR_DESCRIPTIONS)):
            if player.economy.money > CHURCH_REPAIR_COSTS[IList] and player.economy.church_donated_today == 0 and not player.economy.church_repair_is_donated(IList):
                main_ui_runtime.action_items.append(MenuItem("Пожертвовать {} мараведи на {}".format(CHURCH_REPAIR_COSTS[IList], CHURCH_REPAIR_DONATION_TARGETS[IList]), Call("ChurchDonate", IList)))

    $ main_ui_runtime.action_items.append(MenuItem("Назад", Jump("Church")))
    $ renpy.restart_interaction()
    return


label ChurchDonate(donation_idx=0):
    $ renpy.dynamic("idx", "cost")
    $ idx = int(donation_idx or 0)
    $ cost = CHURCH_REPAIR_COSTS[idx]
    $ player.spend_money(cost)
    $ player.economy.record_church_donation(idx, cost)
    $ player.set_stat("notoriety", 0)

    $ scene_runtime.text = "Решив, что грех будет не помочь святому отцу, вы полезли в кошелек и с радостным сердцем отсчитали {} мараведи.\n\n\"Вот, святой отец,\" сказали вы, \"жертвую на {}\"".format(cost, CHURCH_REPAIR_DONATION_TARGETS[idx])
    if cost < 100:
        $ scene_runtime.text = scene_runtime.text + "\n\n\"Да пребудет с тобой благословение Ильматера\", сказал жрец, немного скептически осмотрев ваше скромное пожертвование. Спрятав деньги, он осенил вас святым знаком и вернулся к своим делам.\n\nНа душе у вас сразу стало светло и празднично. Благовейно поклонившись статуе Ильматера вы направились восвояси."
    else:
        $ scene_runtime.text = scene_runtime.text + "\n\n\"Да пребудет с тобой благословение Ильматера\", радостно сказал жрец, одной рукой осеняя вас святым знаком а другой ловко пряча деньги. \"Побольше бы столь щедрых прихожан.\"\n\nНа душе у вас сразу стало светло и празднично. Благовейно поклонившись статуе Ильматера вы направились восвояси."
    $ scene_runtime.location_text = scene_runtime.text
    call ShowImageSeq("gerhard", "", "donate", 2)
    call stat
    $ main_ui_runtime.action_title = "Пожертвование"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [MenuItem("Вернуться в собор", Jump("Church"))]
    return
