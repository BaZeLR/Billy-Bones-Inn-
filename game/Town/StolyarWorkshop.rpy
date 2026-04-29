# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label StolyarWorkshop:
    call EnterLocation("StolyarWorkshop")
    $ CurLoc = "StolyarWorkshop"
    $ location = CurLoc
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_object_id = ""
    $ GirlDressBlock = 0
    $ slogan_asked = DraupnirVar.get("SloganAsked", 0)
    $ hole_asked = DraupnirVar.get("HoleAsked", 0)
    $ glory_asked = DraupnirVar.get("GloryHoleAsked", 0)
    $ soap_barrel_asked = DraupnirVar.get("SoapBarrelAsked", 0)
    $ dog_booth_asked = DraupnirVar.get("DogBoothAsked", 0)
    python:
        try:
            georgett_whore = int(jobWhoreAvail.get("georgett", 0) or 0) > 0
        except Exception:
            georgett_whore = False
    $ glory_explained = int(GeorgettVar.get("GloryHoleExplained", 0) or 0) == 1
    $ can_ask_slogan = (SloganFixed == 0 and slogan_asked == 0)
    $ can_pay_slogan = (SloganFixed == 0 and slogan_asked > 0 and money >= 200)
    $ can_ask_hole = (georgett_whore and hole_asked == 0 and TavernHole == 0)
    $ can_pay_hole = (georgett_whore and hole_asked > 0 and TavernHole == 0 and money >= 100 and time == 0)
    $ can_ask_glory = (georgett_whore and glory_asked == 0 and TavernGloryHole == 0 and glory_explained)
    $ can_pay_glory = (georgett_whore and glory_asked > 0 and TavernGloryHole == 0 and money >= 700 and time == 0)
    $ can_ask_soap_barrel = (soap_recipe_chain_discovered() and SoapAshBarrelInstalled == 0 and soap_barrel_asked == 0)
    $ can_pay_soap_barrel = (soap_recipe_chain_discovered() and SoapAshBarrelInstalled == 0 and soap_barrel_asked > 0 and money >= 75 and time == 0)
    $ can_ask_dog_booth = (dog.owned and dog.booth_built == 0 and dog_booth_asked == 0)
    $ can_pay_dog_booth = (dog.owned and dog.booth_built == 0 and dog_booth_asked > 0 and money >= 100 and time == 0)
    $ has_pending_orders = (can_pay_slogan or (hole_asked > 0 and TavernHole == 0) or (glory_asked > 0 and TavernGloryHole == 0) or can_pay_soap_barrel or can_pay_dog_booth)

    if week == 7 or time >= 3:
        $ MainTxt = "В это время мастерская закрыта."
        $ CurLocDesc = MainTxt
        call ShowImageSeq("general", "", "LocArtisansQuarter", 4)
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _stolyar_closed_ui_return = None
        while _stolyar_closed_ui_return is None:
            call screen main_ui
            $ _stolyar_closed_ui_return = _return
        jump StolyarWorkshop

    if SloganFixed == 1 or TavernGloryHole == 1:
        $ MainTxt = "Мастерская закрыта, мастер Драупнир работает над вашим заказом."
        $ CurLocDesc = MainTxt
        call ShowImageSeq("general", "", "LocArtisansQuarter", 4)
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _stolyar_order_ui_return = None
        while _stolyar_order_ui_return is None:
            call screen main_ui
            $ _stolyar_order_ui_return = _return
        jump StolyarWorkshop

    if story_event_available("StolyarWorkshop", "enter"):
        call checkTriggers("StolyarWorkshop", "enter", 0)

    $ MainTxt = "Вы находитесь в мастерской известного столяра Драупнира. Всему городу известно что гном Драупнир хоть и дерет дорого, но работу свою исполняет не за страх, а за совесть. Мало кто, а точнее никто, может сравниться с ним в столярном ремесле. В его лавке приятно пахнет деревом и всюду висят рубанки, пилы, стамески, топоры и прочий инструмент. В глубине мастерской, за верстаком, что-то тачает сам хозяин - приземистый и крепко сбитый гном."
    if has_pending_orders:
        $ MainTxt += "\n\nВы помните, что у него можно заказать следующее:"
        if can_pay_slogan:
            $ MainTxt += "\n\nРемонт вывески за 200 мараведи."
        if hole_asked > 0 and TavernHole == 0:
            $ MainTxt += "\n\nДырку для подглядывания за 100 мараведи."
        if glory_asked > 0 and TavernGloryHole == 0:
            $ MainTxt += "\n\nГлорихол за 700 мараведи."
        if can_pay_soap_barrel:
            $ MainTxt += "\n\nЗольную бочку для щелока за 75 мараведи."
        if can_pay_dog_booth:
            $ MainTxt += "\n\nСобачью будку за 100 мараведи."
    $ CurLocDesc = MainTxt
    $ StolyarWorkshopSavedText = MainTxt
    call ShowImageSeq("draupnir", "", "dwarf", 3)

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _stolyar_nav_ui_return = None
        while _stolyar_nav_ui_return is None:
            call screen main_ui
            $ _stolyar_nav_ui_return = _return
        jump StolyarWorkshop

    call StolyarWorkshopBuildActions
    $ _stolyar_ui_return = None
    while _stolyar_ui_return is None:
        call screen main_ui
        $ _stolyar_ui_return = _return
    jump StolyarWorkshop


label StolyarWorkshopBuildActions:
    $ slogan_asked = DraupnirVar.get("SloganAsked", 0)
    $ hole_asked = DraupnirVar.get("HoleAsked", 0)
    $ glory_asked = DraupnirVar.get("GloryHoleAsked", 0)
    $ soap_barrel_asked = DraupnirVar.get("SoapBarrelAsked", 0)
    $ dog_booth_asked = DraupnirVar.get("DogBoothAsked", 0)
    python:
        try:
            georgett_whore = int(jobWhoreAvail.get("georgett", 0) or 0) > 0
        except Exception:
            georgett_whore = False
    $ glory_explained = int(GeorgettVar.get("GloryHoleExplained", 0) or 0) == 1
    $ can_ask_slogan = (SloganFixed == 0 and slogan_asked == 0)
    $ can_pay_slogan = (SloganFixed == 0 and slogan_asked > 0 and money >= 200)
    $ can_ask_hole = (georgett_whore and hole_asked == 0 and TavernHole == 0)
    $ can_pay_hole = (georgett_whore and hole_asked > 0 and TavernHole == 0 and money >= 100 and time == 0)
    $ can_ask_glory = (georgett_whore and glory_asked == 0 and TavernGloryHole == 0 and glory_explained)
    $ can_pay_glory = (georgett_whore and glory_asked > 0 and TavernGloryHole == 0 and money >= 700 and time == 0)
    $ can_ask_soap_barrel = (soap_recipe_chain_discovered() and SoapAshBarrelInstalled == 0 and soap_barrel_asked == 0)
    $ can_pay_soap_barrel = (soap_recipe_chain_discovered() and SoapAshBarrelInstalled == 0 and soap_barrel_asked > 0 and money >= 75 and time == 0)
    $ can_ask_dog_booth = (dog.owned and dog.booth_built == 0 and dog_booth_asked == 0)
    $ can_pay_dog_booth = (dog.owned and dog.booth_built == 0 and dog_booth_asked > 0 and money >= 100 and time == 0)
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Call("StolyarWorkshopApply", "look")))
    $ current_action_items.append(MenuItem("Поболтать с гномом", Call("IntDraupnirTalk")))
    if can_ask_slogan:
        $ current_action_items.append(MenuItem("Спросить о ремонте вывески", Call("StolyarWorkshopApply", "ask_slogan")))
    if can_pay_slogan:
        $ current_action_items.append(MenuItem("Заплатить 200 мараведи за ремонт вывески", Call("StolyarWorkshopApply", "pay_slogan")))
    if can_ask_hole:
        $ current_action_items.append(MenuItem("Спросить о дырке в стене", Call("StolyarWorkshopApply", "ask_hole")))
    if can_pay_hole:
        $ current_action_items.append(MenuItem("Заплатить 100 мараведи за обзорное отверстие", Call("StolyarWorkshopApply", "pay_hole")))
    if can_ask_glory:
        $ current_action_items.append(MenuItem("Спросить о глорихоле", Call("StolyarWorkshopApply", "ask_glory")))
    if can_pay_glory:
        $ current_action_items.append(MenuItem("Заплатить 700 мараведи за устройство глорихола", Call("StolyarWorkshopApply", "pay_glory")))
    if can_ask_soap_barrel:
        $ current_action_items.append(MenuItem("Спросить о бочке для щелока", Call("StolyarWorkshopApply", "ask_soap_barrel")))
    if can_pay_soap_barrel:
        $ current_action_items.append(MenuItem("Заплатить 75 мараведи за зольную бочку", Call("StolyarWorkshopApply", "pay_soap_barrel")))
    if can_ask_dog_booth:
        $ current_action_items.append(MenuItem("Спросить о собачьей будке", Call("StolyarWorkshopApply", "ask_dog_booth")))
    if can_pay_dog_booth:
        $ current_action_items.append(MenuItem("Заплатить 100 мараведи за собачью будку", Call("StolyarWorkshopApply", "pay_dog_booth")))
    if int(MongolVar.get("StocksFoodDay", -1) or -1) >= 0 and int(DraupnirVar.get("MongolLockpickOrderDay", -1) or -1) < 0 and int(time or 0) < 3 and int(week or 0) != 7 and int(money or 0) >= 40:
        $ current_action_items.append(MenuItem("Заплатить 40 мараведи за тонкие отмычки", Call("story_clara_market_booklet_lockpicks_order_direct")))
    $ current_action_items.append(MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter")))
    return


label StolyarWorkshopApply(choice_code=""):
    if str(choice_code or "") == "look":
        $ MainTxt = "Мастер Драупнир - типичный гном, невысокий и коренастый. Он около полутора метров роста и почти такой же в плечах, с окладистой рыжей бородой и огненными волосами. Он одет в штаны, кожаную жилетку с множеством ремешков и карманов, из которых торчат разнообразные инструменты, и деревяные башмаки. Он постоянно что-то пилит и строгает, отвлекаясь только на то, чтобы произвести в уме или на пальцах подсчеты будущих барышей. Вам ничего не известно о его семье или родне."
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "ask_slogan":
        $ MainTxt = "Вы рассказали мастеру Драупниру что вывеска на вашем трактире совсем обветшала. Что, в свою очередь, приводит к неисчислимым бедствиям для вас, а конкретно к тому, что далеко не все, кто зашел бы именно в ваш трактир действительно туда заходят. Из чего проистекает ваше текущее стесненное в средствах положение. После этого жалобного рассказа вы осторожно поинтересовались у мастера Драупнира, сколько будет стоить починить вывеску и нельзя ли это сделать в рассрочку. Мастер Драупнир внимательно выслушал вашу историю, но только и соизволил ответить: 'Двести мараведи. Вперед.' Дальнейшие уточнения на предмет не оговорился ли он и обязательно ли платить вперед ни к чему не привели."
        $ DraupnirVar["SloganAsked"] = 1
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "pay_slogan":
        $ MainTxt = "Скрепя сердце вы отсчитали 200 мараведи мастеру Драупниру. Собрав свои инструменты работящий гном направил свои стопы к вашему трактиру."
        $ SloganFixed = 1
        $ money -= 200
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "ask_hole":
        $ MainTxt = "Вы рассказали мастеру Драупниру что, после появления в вашем заведении веселых девушек, в задней комнате стали происходить интересные вещи. Однако полностью оценить их интересность вы не можете, по причине досадного наличия отстутствия хорошего обзора. После этого вы поинтересовались, не имеется ли у мастера Драупнира длинного сверла, а также не хочет ли он, в компании с оным сверлом, навестить ваше заведение. Мастер Драупнир внимательно выслушал вашу историю, но только и соизволил ответить: 'Сто мараведи. И делать это, как ты сам понимаешь, надо с утра.'"
        $ DraupnirVar["HoleAsked"] = 1
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "pay_hole":
        $ MainTxt = "Скрепя сердце вы отсчитали 100 мараведи мастеру Драупниру. Взяв с собой дрель, стамески, пилу и еще пару инструментов, работящий гном отправился к вашему трактиру. Впрочем, долго он там не задержался, вернувшись и отрапортовав что все сделанно, потайное окошко готово."
        $ TavernHole = 1
        $ money -= 100
        $ calendar_set_time_slot(1)
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "ask_glory":
        $ MainTxt = "Вы рассказали мастеру Драупниру об новинке про которую вы слышали - глорихоле. Ну и о том, что вы хотели бы устроить таковую в своем трактире. Ну и что работы там всего чуть-чуть - сделать ширмочку, занавески, просверлить дырки, отполировать, покрасить и еще кое-чего по мелочи, может можно мараведи в 20 уложиться? А, да, еще и сделать так чтобы вы могли незаметно проверить, что там делается, ведь это совсем просто. Может еще 5 или даже 7 мараведи сверх. Вместе с материалами? Мастер Драупнир внимательно выслушал вашу историю, судя по всему на этот раз идея гному понравилась. Но все таки цену он заломил немножко выше предложенной: 'Семьсот мараведи. Ну и да, работа на весь день, начинать надо с утра.'"
        $ DraupnirVar["GloryHoleAsked"] = 1
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "pay_glory":
        $ MainTxt = "Жестоко задавив в себе жабу пока она еще была в состоянии головастика, вы отсчитали 700 мараведи мастеру Драупниру. Загрузив ослика досками, собрав в ящичек разнообразные инструменты, а в специальный мешок ткани для занавески, трудолюбивый гном потопал к вашему трактиру."
        $ TavernGloryHole = 1
        $ money -= 700
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "ask_soap_barrel":
        $ MainTxt = "Вы расспросили мастера Драупнира о бочке с дырчатым дном, через которую можно готовить щелок для мыла. Гном почесал бороду, прикинул доски и буркнул: 'Сделаю. Семьдесят пять мараведи. Но ставить надо с утра, а потом жди, пока зола настоится.'"
        $ DraupnirVar["SoapBarrelAsked"] = 1
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "pay_soap_barrel":
        $ MainTxt = "Вы отсчитали мастеру Драупниру 75 мараведи. Ворча себе под нос, он собрал инструменты, дошел до вашего заднего двора и поставил там зольную бочку для щелока."
        $ SoapAshBarrelInstalled = 1
        $ SoapAshBarrelReadyDay = int(dayspassed or 0) + 7
        $ DraupnirVar["SoapBarrelAsked"] = 0
        $ money -= 75
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "ask_dog_booth":
        $ MainTxt = "Вы спрашиваете мастера Драупнира, не сможет ли он сколотить простую, но крепкую собачью будку для заднего двора. Гном прикидывает расход досок и бурчит: 'Сто мараведи. И ставить буду с утра.'"
        $ DraupnirVar["DogBoothAsked"] = 1
        $ CurLocDesc = MainTxt
        call StolyarWorkshopBuildActions
        return

    if str(choice_code or "") == "pay_dog_booth":
        $ money -= 100
        call DogBackyardBuildBooth
        return

    call StolyarWorkshopBuildActions
    return
