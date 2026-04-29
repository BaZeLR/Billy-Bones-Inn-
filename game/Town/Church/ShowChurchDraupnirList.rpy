# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowChurchDraupnirList:
    python:
        StrList = []
        for IList in range(len(ChurchRepairDesc)):
            entry = "{}. {}: {} мараведи.".format(IList + 1, ChurchRepairDesc[IList], ChurchRepairCost[IList])
            if ChurchDonated[IList] > 0:
                entry = "[s]{}[/s]".format(entry)
            StrList.append(entry)
        show_list = "\n".join(StrList)
        SawDraupnirChurchList = 1

    $ MainTxt = "Вы с интересом ознакомились со счетом, выставленным мастером Драупниром:\n\n" + show_list
    if ChurchDonatedToday > 0:
        $ MainTxt = MainTxt + "\n\nВы сегодня уже сделали пожертвование святой церкви и на душе у вас благостно и возвышенно, а карманы малость полегчали."
    $ CurLocDesc = MainTxt
    call ShowImage("general", "", "LocChurchIspoved1")
    $ current_action_title = "Листок на столике"
    $ current_action_content = None
    $ current_action_items = []

    python:
        for IList in range(len(ChurchRepairDesc)):
            if money > ChurchRepairCost[IList] and ChurchDonatedToday == 0 and ChurchDonated[IList] == 0 and SawDraupnirChurchList > 0:
                current_action_items.append(MenuItem("Пожертвовать {} мараведи на {}".format(ChurchRepairCost[IList], ChurchRepairDonat[IList]), Call("ChurchDonate", IList)))

    $ current_action_items.append(MenuItem("Назад", Call("ChurchRestore")))
    $ renpy.restart_interaction()
    return


label ChurchDonate(donation_idx=0):
    $ idx = int(donation_idx or 0)
    $ cost = ChurchRepairCost[idx]
    $ ChurchDonated[idx] = 1
    $ ChurchDonatedToday = 1
    $ ChurchDonatedAmount += cost
    $ money -= cost

    $ MainTxt = "Решив, что грех будет не помочь святому отцу, вы полезли в кошелек и с радостным сердцем отсчитали {} мараведи.\n\n\"Вот, святой отец,\" сказали вы, \"жертвую на {}\"".format(cost, ChurchRepairDonat[idx])
    if cost < 100:
        $ MainTxt = MainTxt + "\n\n\"Да пребудет с тобой благословение Ильматера\", сказал жрец, немного скептически осмотрев ваше скромное пожертвование. Спрятав деньги, он осенил вас святым знаком и вернулся к своим делам.\n\nНа душе у вас сразу стало светло и празднично. Благовейно поклонившись статуе Ильматера вы направились восвояси."
    else:
        $ MainTxt = MainTxt + "\n\n\"Да пребудет с тобой благословение Ильматера\", радостно сказал жрец, одной рукой осеняя вас святым знаком а другой ловко пряча деньги. \"Побольше бы столь щедрых прихожан.\"\n\nНа душе у вас сразу стало светло и празднично. Благовейно поклонившись статуе Ильматера вы направились восвояси."
    $ CurLocDesc = MainTxt
    call ShowImageSeq("gerhard", "", "donate", 2)
    call stat
    $ current_action_title = "Пожертвование"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в собор", Call("ChurchRestore"))]
    return
