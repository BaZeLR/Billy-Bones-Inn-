        $ Draupnir.location = "StreetTavern"    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _stolyar_nav_ui_return = None
        while _stolyar_nav_ui_return is None:
            call screen main_ui
            $ _stolyar_nav_ui_return = _return
        jump StolyarWorkshop
        $ Draupnir.location = "StreetTavern"    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _stolyar_nav_ui_return = None
        while _stolyar_nav_ui_return is None:
            call screen main_ui
            $ _stolyar_nav_ui_return = _return
        jump StolyarWorkshop
        $ Draupnir.location = "StreetTavern"    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _stolyar_nav_ui_return = None
        while _stolyar_nav_ui_return is None:
            call screen main_ui
            $ _stolyar_nav_ui_return = _return
        jump StolyarWorkshop
# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init python:
    def stolyar_workshop_action_items():
        items = [MenuItem("Осмотреть", Call("StolyarWorkshopApply", "look"))]
        slogan_asked = Draupnir.var_int("SloganAsked", 0)
        hole_asked = Draupnir.var_int("HoleAsked", 0)
        glory_asked = Draupnir.var_int("GloryHoleAsked", 0)
        soap_barrel_asked = Draupnir.var_int("SoapBarrelAsked", 0)
        dog_booth_asked = Draupnir.var_int("DogBoothAsked", 0)
        georgett_whore = int(Georgett.job_value("jobWhoreAvail", 0) or 0) > 0
        glory_explained = int(Georgett.story_value("GloryHoleExplained", 0) or 0) == 1
        if player.tavern_management.slogan_state == 0 and slogan_asked == 0:
            items.append(MenuItem("Спросить о ремонте вывески", Call("StolyarWorkshopApply", "ask_slogan")))
        if player.tavern_management.slogan_state == 0 and slogan_asked > 0 and player.economy.money >= 200:
            items.append(MenuItem("Заплатить 200 мараведи за ремонт вывески", Call("StolyarWorkshopApply", "pay_slogan")))
        if georgett_whore and hole_asked == 0 and player.tavern_management.client_room_hole == 0:
            items.append(MenuItem("Спросить о дырке в стене", Call("StolyarWorkshopApply", "ask_hole")))
        if georgett_whore and hole_asked > 0 and player.tavern_management.client_room_hole == 0 and player.economy.money >= 100 and StolyarWorkshopRoom.is_open():
            items.append(MenuItem("Заплатить 100 мараведи за обзорное отверстие", Call("StolyarWorkshopApply", "pay_hole")))
        if georgett_whore and glory_asked == 0 and TavernGloryHole == 0 and glory_explained:
            items.append(MenuItem("Спросить о глорихоле", Call("StolyarWorkshopApply", "ask_glory")))
        if georgett_whore and glory_asked > 0 and TavernGloryHole == 0 and player.economy.money >= 700 and StolyarWorkshopRoom.is_open():
            items.append(MenuItem("Заплатить 700 мараведи за устройство глорихола", Call("StolyarWorkshopApply", "pay_glory")))
        if soap_recipe_chain_discovered() and not crafting.ash_barrel_installed and soap_barrel_asked == 0:
            items.append(MenuItem("Спросить о бочке для щелока", Call("StolyarWorkshopApply", "ask_soap_barrel")))
        if soap_recipe_chain_discovered() and not crafting.ash_barrel_installed and soap_barrel_asked > 0 and player.economy.money >= 75 and StolyarWorkshopRoom.is_open():
            items.append(MenuItem("Заплатить 75 мараведи за зольную бочку", Call("StolyarWorkshopApply", "pay_soap_barrel")))
        if dog.owned and dog.booth_built == 0 and dog_booth_asked == 0:
            items.append(MenuItem("Спросить о собачьей будке", Call("StolyarWorkshopApply", "ask_dog_booth")))
        if dog.owned and dog.booth_built == 0 and dog_booth_asked > 0 and player.economy.money >= 100 and StolyarWorkshopRoom.is_open():
            items.append(MenuItem("Заплатить 100 мараведи за собачью будку", Call("StolyarWorkshopApply", "pay_dog_booth")))
        if story_event_available("StolyarWorkshop", "enter"):
            items.append(MenuItem("Поговорить с Драупниром об отмычках", Call("checkTriggers", "StolyarWorkshop", "enter", 0)))
        items.append(MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter")))
        return items

    StolyarWorkshopRoom = Room(
        code_name="StolyarWorkshop",
        group_name=ROOM_GROUP_CITY,
        display_name="Мастерская Драупнира",
        bg_picture="images/draupnir/dwarf1.jpg",
        descriptions=[
            RoomDescription(
                text="Вы находитесь в мастерской известного столяра Драупнира. Всему городу известно что гном Драупнир хоть и дерет дорого, но работу свою исполняет не за страх, а за совесть. Мало кто, а точнее никто, может сравниться с ним в столярном ремесле. В его лавке приятно пахнет деревом и всюду висят рубанки, пилы, стамески, топоры и прочий инструмент. В глубине мастерской, за верстаком, что-то тачает сам хозяин - приземистый и крепко сбитый гном.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в квартал ремесленников", target="ArtisansQuarter", minutes_to_pass=10),
        ],
        schedule=RoomSchedule(
            weekdays=[1, 2, 3, 4, 5, 6],
            start="06:00",
            end="17:59",
            closed_text="В это время мастерская закрыта.",
        ),
    )

label StolyarWorkshop:
    $ CurrentRoom = StolyarWorkshopRoom
    $ CurLoc = CurrentRoom.code_name
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
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
    $ glory_explained = int(Georgett.story_value("GloryHoleExplained", 0) or 0) == 1
    $ can_ask_slogan = (player.tavern_management.slogan_state == 0 and slogan_asked == 0)
    $ can_pay_slogan = (player.tavern_management.slogan_state == 0 and slogan_asked > 0 and player.economy.money >= 200)
    $ can_ask_hole = (georgett_whore and hole_asked == 0 and player.tavern_management.client_room_hole == 0)
    $ can_pay_hole = (georgett_whore and hole_asked > 0 and player.tavern_management.client_room_hole == 0 and player.economy.money >= 100 and StolyarWorkshopRoom.is_open())
    $ can_ask_glory = (georgett_whore and glory_asked == 0 and TavernGloryHole == 0 and glory_explained)
    $ can_pay_glory = (georgett_whore and glory_asked > 0 and TavernGloryHole == 0 and money >= 700 and StolyarWorkshopRoom.is_open())
    $ can_ask_soap_barrel = (soap_recipe_chain_discovered() and not crafting.ash_barrel_installed and soap_barrel_asked == 0)
    $ can_pay_soap_barrel = (soap_recipe_chain_discovered() and not crafting.ash_barrel_installed and soap_barrel_asked > 0 and player.economy.money >= 75 and StolyarWorkshopRoom.is_open())
    $ can_ask_dog_booth = (dog.owned and dog.booth_built == 0 and dog_booth_asked == 0)
    $ can_pay_dog_booth = (dog.owned and dog.booth_built == 0 and dog.booth_built == 0 and dog_booth_asked > 0 and money >= 100 and StolyarWorkshopRoom.is_open())
    $ has_pending_orders = (can_pay_slogan or (hole_asked > 0 and player.tavern_management.client_room_hole == 0) or (glory_asked > 0 and TavernGloryHole == 0) or can_pay_soap_barrel or can_pay_dog_booth)

    if not CurrentRoom.is_open():
        $ MainTxt = CurrentRoom.schedule.closed_text
        $ CurLocDesc = MainTxt
        call ShowImageSeq("general", "", "LocArtisansQuarter", 4)
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        while True:
            call screen main_ui

    if player.tavern_management.slogan_state == 1 or TavernGloryHole == 1:
        $ MainTxt = "Мастерская закрыта, мастер Драупнир работает над вашим заказом."
        $ CurLocDesc = MainTxt
        call ShowImageSeq("general", "", "LocArtisansQuarter", 4)
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        while True:
            call screen main_ui

    call RoomEnterEventGate(CurLoc, False)

    $ _stolyar_desc_rows = CurrentRoom.visible_descriptions()
    if len(_stolyar_desc_rows) > 0:
        $ MainTxt = _stolyar_desc_rows[0].text
    else:
        $ MainTxt = "Вы находитесь в мастерской Драупнира."
    if has_pending_orders:
        $ MainTxt += "\n\nВы помните, что у него можно заказать следующее:"
        if can_pay_slogan:
            $ MainTxt += "\n\nРемонт вывески за 200 мараведи."
        if hole_asked > 0 and player.tavern_management.client_room_hole == 0:
            $ MainTxt += "\n\nДырку для подглядывания за 100 мараведи."
        if glory_asked > 0 and TavernGloryHole == 0:
            $ MainTxt += "\n\nГлорихол за 700 мараведи."
        if can_pay_soap_barrel:
            $ MainTxt += "\n\nЗольную бочку для щелока за 75 мараведи."
        if can_pay_dog_booth:
            $ MainTxt += "\n\nСобачью будку за 100 мараведи."
    $ CurLocDesc = MainTxt
    $ StolyarWorkshopSavedText = MainTxt
    $ StolyarWorkshopSavedText = MainTxt
    $ StolyarWorkshopSavedText = MainTxt
    $ CurrentRoom.mark_visited()
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

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _stolyar_nav_ui_return = None
        while _stolyar_nav_ui_return is None:
            call screen main_ui
            $ _stolyar_nav_ui_return = _return
        jump StolyarWorkshop

    if navigation_only_mode_enabled():
        $ MainTxt = MainTxt + "\n\n" + navigation_only_message() + "\n\n" + navigation_only_time_note()
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в квартал ремесленников", Jump("ArtisansQuarter"))]
        $ _stolyar_nav_ui_return = None
        while _stolyar_nav_ui_return is None:
            call screen main_ui
            $ _stolyar_nav_ui_return = _return
        jump StolyarWorkshop

    $ current_action_items = stolyar_workshop_action_items()
    while True:
        call screen main_ui


label StolyarWorkshopApply(choice_code=""):
    if str(choice_code or "") == "look":
    $ MainTxt = "Мастер Драупнир - типичный гном, невысокий и коренастый. Он около полутора метров роста и почти такой же в плечах, с окладистой рыжей бородой и огненными волосами. Он одет в штаны, кожаную жилетку с множеством ремешков и карманов, из которых торчат разнообразные инструменты, и деревяные башмаки. Он постоянно что-то пилит и строгает, отвлекаясь только на то, чтобы произвести в уме или на пальцах подсчеты будущих барышей. Вам ничего не известно о его семье или родне."
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopAskSlogan:
    $ MainTxt = "Вы рассказали мастеру Драупниру что вывеска на вашем трактире совсем обветшала. Что, в свою очередь, приводит к неисчислимым бедствиям для вас, а конкретно к тому, что далеко не все, кто зашел бы именно в ваш трактир действительно туда заходят. Из чего проистекает ваше текущее стесненное в средствах положение. После этого жалобного рассказа вы осторожно поинтересовались у мастера Драупнира, сколько будет стоить починить вывеску и нельзя ли это сделать в рассрочку. Мастер Драупнир внимательно выслушал вашу историю, но только и соизволил ответить: 'Двести мараведи. Вперед.' Дальнейшие уточнения на предмет не оговорился ли он и обязательно ли платить вперед ни к чему не привели."
    $ Draupnir.set_var_int("SloganAsked", 1)
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopPaySlogan:
    $ MainTxt = "Скрепя сердце вы отсчитали 200 мараведи мастеру Драупниру. Собрав свои инструменты работящий гном направил свои стопы к вашему трактиру."
    $ player.tavern_management.slogan_state = 1
    $ Draupnir.location = "StreetTavern"
    $ player.spend_money(200)
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopAskHole:
    $ MainTxt = "Вы рассказали мастеру Драупниру что, после появления в вашем заведении веселых девушек, в задней комнате стали происходить интересные вещи. Однако полностью оценить их интересность вы не можете, по причине досадного наличия отстутствия хорошего обзора. После этого вы поинтересовались, не имеется ли у мастера Драупнира длинного сверла, а также не хочет ли он, в компании с оным сверлом, навестить ваше заведение. Мастер Драупнир внимательно выслушал вашу историю, но только и соизволил ответить: 'Сто мараведи. И делать это, как ты сам понимаешь, надо с утра.'"
    $ Draupnir.set_var_int("HoleAsked", 1)
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopPayHole:
    $ MainTxt = "Скрепя сердце вы отсчитали 100 мараведи мастеру Драупниру. Взяв с собой дрель, стамески, пилу и еще пару инструментов, работящий гном отправился к вашему трактиру. Впрочем, долго он там не задержался, вернувшись и отрапортовав что все сделанно, потайное окошко готово."
    $ player.tavern_management.client_room_hole = 1
    $ player.spend_money(100)
    $ calendar_v2.hour = 8
    $ calendar_v2.minute = 0
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopAskGlory:
    $ MainTxt = "Вы рассказали мастеру Драупниру об новинке про которую вы слышали - глорихоле. Ну и о том, что вы хотели бы устроить таковую в своем трактире. Ну и что работы там всего чуть-чуть - сделать ширмочку, занавески, просверлить дырки, отполировать, покрасить и еще кое-чего по мелочи, может можно мараведи в 20 уложиться? А, да, еще и сделать так чтобы вы могли незаметно проверить, что там делается, ведь это совсем просто. Может еще 5 или даже 7 мараведи сверх. Вместе с материалами? Мастер Драупнир внимательно выслушал вашу историю, судя по всему на этот раз идея гному понравилась. Но все таки цену он заломил немножко выше предложенной: 'Семьсот мараведи. Ну и да, работа на весь день, начинать надо с утра.'"
    $ Draupnir.set_var_int("GloryHoleAsked", 1)
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopPayGlory:
    $ MainTxt = "Жестоко задавив в себе жабу пока она еще была в состоянии головастика, вы отсчитали 700 мараведи мастеру Драупниру. Загрузив ослика досками, собрав в ящичек разнообразные инструменты, а в специальный мешок ткани для занавески, трудолюбивый гном потопал к вашему трактиру."
    $ TavernGloryHole = 1
    $ player.spend_money(700)
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopAskSoapBarrel:
    $ MainTxt = "Вы расспросили мастера Драупнира о бочке с дырчатым дном, через которую можно готовить щелок для мыла. Гном почесал бороду, прикинул доски и буркнул: 'Сделаю. Семьдесят пять мараведи. Но ставить надо с утра, а потом жди, пока зола настоится.'"
    $ Draupnir.set_var_int("SoapBarrelAsked", 1)
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopPaySoapBarrel:
    $ MainTxt = "Вы отсчитали мастеру Драупниру 75 мараведи. Ворча себе под нос, он собрал инструменты, дошел до вашего заднего двора и поставил там зольную бочку для щелока."
    $ crafting.ash_barrel_installed = True
    $ crafting.ash_barrel_ready_day = int(current_game_day() or 0) + 7
    $ Draupnir.set_var_int("SoapBarrelAsked", 0)
    $ player.spend_money(75)
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopAskDogBooth:
    $ MainTxt = "Вы спрашиваете мастера Драупнира, не сможет ли он сколотить простую, но крепкую собачью будку для заднего двора. Гном прикидывает расход досок и бурчит: 'Сто мараведи. И ставить буду с утра.'"
    $ Draupnir.set_var_int("DogBoothAsked", 1)
    $ CurLocDesc = MainTxt
    $ current_action_items = stolyar_workshop_action_items()
    return


label StolyarWorkshopPayDogBooth:
    $ player.spend_money(100)
    call DogBackyardBuildBooth
    return

    $ current_action_items = stolyar_workshop_action_items()
return
