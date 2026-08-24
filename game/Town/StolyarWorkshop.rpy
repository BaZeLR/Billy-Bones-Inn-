# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init python:
    StolyarWorkshopRoomDefinition = Room(
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
    $ renpy.dynamic("slogan_asked", "hole_asked", "glory_asked", "soap_barrel_asked", "dog_booth_asked", "glory_explained", "can_ask_slogan", "can_pay_slogan", "can_ask_hole", "can_pay_hole", "can_ask_glory", "can_pay_glory", "can_ask_soap_barrel", "can_pay_soap_barrel", "can_ask_dog_booth", "can_pay_dog_booth", "has_pending_orders", "_stolyar_desc_rows", "georgett_whore")
    $ rooms.enter("StolyarWorkshop")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.object_id = ""
    $ dress_shop.girl_dress_block = 0
    $ slogan_asked = Draupnir.slogan_quote_received
    $ hole_asked = Draupnir.peep_hole_quote_received
    $ glory_asked = Draupnir.glory_hole_quote_received
    $ soap_barrel_asked = Draupnir.soap_barrel_quote_received
    $ dog_booth_asked = Draupnir.dog_booth_quote_received
    python:
        try:
            georgett_whore = int(Georgett.job_value("jobWhoreAvail", 0) or 0) > 0
        except Exception:
            georgett_whore = False
    $ glory_explained = int(Georgett.story_value("GloryHoleExplained", 0) or 0) == 1
    $ can_ask_slogan = (player.tavern_management.slogan_state == 0 and slogan_asked == 0)
    $ can_pay_slogan = (player.tavern_management.slogan_state == 0 and slogan_asked > 0 and player.economy.money >= 200)
    $ can_ask_hole = (georgett_whore and hole_asked == 0 and player.tavern_management.client_room_hole == 0)
    $ can_pay_hole = (georgett_whore and hole_asked > 0 and player.tavern_management.client_room_hole == 0 and player.economy.money >= 100 and rooms.get("StolyarWorkshop").is_open())
    $ can_ask_glory = (georgett_whore and glory_asked == 0 and player.tavern_management.glory_hole == 0 and glory_explained)
    $ can_pay_glory = (georgett_whore and glory_asked > 0 and player.tavern_management.glory_hole == 0 and player.economy.money >= 700 and rooms.get("StolyarWorkshop").is_open())
    $ can_ask_soap_barrel = (soap_recipe_chain_discovered() and not crafting.ash_barrel_installed and soap_barrel_asked == 0)
    $ can_pay_soap_barrel = (soap_recipe_chain_discovered() and not crafting.ash_barrel_installed and soap_barrel_asked > 0 and player.economy.money >= 75 and rooms.get("StolyarWorkshop").is_open())
    $ can_ask_dog_booth = (dog.owned and dog.booth_built == 0 and dog_booth_asked == 0)
    $ can_pay_dog_booth = (dog.owned and dog.booth_built == 0 and dog.booth_built == 0 and dog_booth_asked > 0 and player.economy.money >= 100 and rooms.get("StolyarWorkshop").is_open())
    $ has_pending_orders = (can_pay_slogan or (hole_asked > 0 and player.tavern_management.client_room_hole == 0) or (glory_asked > 0 and player.tavern_management.glory_hole == 0) or can_pay_soap_barrel or can_pay_dog_booth)

    if not rooms.current.is_open():
        $ scene_runtime.text = rooms.current.schedule.closed_text
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImageSeq("general", "", "LocArtisansQuarter", 4)
        $ main_ui_runtime.action_items = rooms.get("StolyarWorkshop").build_exit_items()
        while True:
            call screen main_ui

    if player.tavern_management.slogan_state == 1 or player.tavern_management.glory_hole == 1:
        $ scene_runtime.text = "Мастерская закрыта, мастер Драупнир работает над вашим заказом."
        $ scene_runtime.location_text = scene_runtime.text
        call ShowImageSeq("general", "", "LocArtisansQuarter", 4)
        $ main_ui_runtime.action_items = rooms.get("StolyarWorkshop").build_exit_items()
        while True:
            call screen main_ui

    call RoomEnterEventGate(rooms.current_code, False)

    $ _stolyar_desc_rows = rooms.current.visible_descriptions()
    if len(_stolyar_desc_rows) > 0:
        $ scene_runtime.text = _stolyar_desc_rows[0].text
    else:
        $ scene_runtime.text = "Вы находитесь в мастерской Драупнира."
    if has_pending_orders:
        $ scene_runtime.text += "\n\nВы помните, что у него можно заказать следующее:"
        if can_pay_slogan:
            $ scene_runtime.text += "\n\nРемонт вывески за 200 мараведи."
        if hole_asked > 0 and player.tavern_management.client_room_hole == 0:
            $ scene_runtime.text += "\n\nДырку для подглядывания за 100 мараведи."
        if glory_asked > 0 and player.tavern_management.glory_hole == 0:
            $ scene_runtime.text += "\n\nГлорихол за 700 мараведи."
        if can_pay_soap_barrel:
            $ scene_runtime.text += "\n\nЗольную бочку для щелока за 75 мараведи."
        if can_pay_dog_booth:
            $ scene_runtime.text += "\n\nСобачью будку за 100 мараведи."
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.current.mark_visited()
    call ShowImageSeq("draupnir", "", "dwarf", 3)

    $ main_ui_runtime.action_items = []
    if story_event_available("StolyarWorkshop", "enter"):
        $ main_ui_runtime.action_items.append(MenuItem("Поговорить с Драупниром об отмычках", Call("checkTriggers", "StolyarWorkshop", "enter", 0)))
    $ main_ui_runtime.action_items += rooms.get("StolyarWorkshop").build_exit_items()
    while True:
        call screen main_ui


label StolyarWorkshopLook:
    $ scene_runtime.text = "Мастер Драупнир - типичный гном, невысокий и коренастый. Он около полутора метров роста и почти такой же в плечах, с окладистой рыжей бородой и огненными волосами. Он одет в штаны, кожаную жилетку с множеством ремешков и карманов, из которых торчат разнообразные инструменты, и деревяные башмаки. Он постоянно что-то пилит и строгает, отвлекаясь только на то, чтобы произвести в уме или на пальцах подсчеты будущих барышей. Вам ничего не известно о его семье или родне."
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopAskSlogan:
    $ scene_runtime.text = "Вы рассказали мастеру Драупниру что вывеска на вашем трактире совсем обветшала. Что, в свою очередь, приводит к неисчислимым бедствиям для вас, а конкретно к тому, что далеко не все, кто зашел бы именно в ваш трактир действительно туда заходят. Из чего проистекает ваше текущее стесненное в средствах положение. После этого жалобного рассказа вы осторожно поинтересовались у мастера Драупнира, сколько будет стоить починить вывеску и нельзя ли это сделать в рассрочку. Мастер Драупнир внимательно выслушал вашу историю, но только и соизволил ответить: 'Двести мараведи. Вперед.' Дальнейшие уточнения на предмет не оговорился ли он и обязательно ли платить вперед ни к чему не привели."
    $ Draupnir.slogan_quote_received = True
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopPaySlogan:
    $ scene_runtime.text = "Скрепя сердце вы отсчитали 200 мараведи мастеру Драупниру. Собрав свои инструменты работящий гном направил свои стопы к вашему трактиру."
    $ player.tavern_management.slogan_state = 1
    $ player.spend_money(200)
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopAskHole:
    $ scene_runtime.text = "Вы рассказали мастеру Драупниру что, после появления в вашем заведении веселых девушек, в задней комнате стали происходить интересные вещи. Однако полностью оценить их интересность вы не можете, по причине досадного наличия отстутствия хорошего обзора. После этого вы поинтересовались, не имеется ли у мастера Драупнира длинного сверла, а также не хочет ли он, в компании с оным сверлом, навестить ваше заведение. Мастер Драупнир внимательно выслушал вашу историю, но только и соизволил ответить: 'Сто мараведи. И делать это, как ты сам понимаешь, надо с утра.'"
    $ Draupnir.peep_hole_quote_received = True
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopPayHole:
    $ scene_runtime.text = "Скрепя сердце вы отсчитали 100 мараведи мастеру Драупниру. Взяв с собой дрель, стамески, пилу и еще пару инструментов, работящий гном отправился к вашему трактиру. Впрочем, долго он там не задержался, вернувшись и отрапортовав что все сделанно, потайное окошко готово."
    $ player.tavern_management.client_room_hole = 1
    $ player.spend_money(100)
    $ calendar_v2.hour = 8
    $ calendar_v2.minute = 0
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopAskGlory:
    $ scene_runtime.text = "Вы рассказали мастеру Драупниру об новинке про которую вы слышали - глорихоле. Ну и о том, что вы хотели бы устроить таковую в своем трактире. Ну и что работы там всего чуть-чуть - сделать ширмочку, занавески, просверлить дырки, отполировать, покрасить и еще кое-чего по мелочи, может можно мараведи в 20 уложиться? А, да, еще и сделать так чтобы вы могли незаметно проверить, что там делается, ведь это совсем просто. Может еще 5 или даже 7 мараведи сверх. Вместе с материалами? Мастер Драупнир внимательно выслушал вашу историю, судя по всему на этот раз идея гному понравилась. Но все таки цену он заломил немножко выше предложенной: 'Семьсот мараведи. Ну и да, работа на весь день, начинать надо с утра.'"
    $ Draupnir.glory_hole_quote_received = True
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopPayGlory:
    $ scene_runtime.text = "Жестоко задавив в себе жабу пока она еще была в состоянии головастика, вы отсчитали 700 мараведи мастеру Драупниру. Загрузив ослика досками, собрав в ящичек разнообразные инструменты, а в специальный мешок ткани для занавески, трудолюбивый гном потопал к вашему трактиру."
    $ player.tavern_management.glory_hole = 1
    $ player.spend_money(700)
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopAskSoapBarrel:
    $ scene_runtime.text = "Вы расспросили мастера Драупнира о бочке с дырчатым дном, через которую можно готовить щелок для мыла. Гном почесал бороду, прикинул доски и буркнул: 'Сделаю. Семьдесят пять мараведи. Но ставить надо с утра, а потом жди, пока зола настоится.'"
    $ Draupnir.soap_barrel_quote_received = True
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopPaySoapBarrel:
    $ scene_runtime.text = "Вы отсчитали мастеру Драупниру 75 мараведи. Ворча себе под нос, он собрал инструменты, дошел до вашего заднего двора и поставил там зольную бочку для щелока."
    $ crafting.ash_barrel_installed = True
    $ crafting.ash_barrel_ready_day = int(current_game_day() or 0) + 7
    $ Draupnir.soap_barrel_quote_received = False
    $ player.spend_money(75)
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopAskDogBooth:
    $ scene_runtime.text = "Вы спрашиваете мастера Драупнира, не сможет ли он сколотить простую, но крепкую собачью будку для заднего двора. Гном прикидывает расход досок и бурчит: 'Сто мараведи. И ставить буду с утра.'"
    $ Draupnir.dog_booth_quote_received = True
    $ scene_runtime.location_text = scene_runtime.text
    return


label StolyarWorkshopPayDogBooth:
    $ player.spend_money(100)
    call DogBackyardBuildBooth
    return
