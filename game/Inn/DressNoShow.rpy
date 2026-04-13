# DressNoShow.rpy
# Converted from legacy script. Handles the event when the player fails to show up for a dress shopping trip.

label DressNoShow(girl_name_dns):
    $ _dress_no_show_restore_ui = True if (CurrentRoom is not None or str(CurLoc or "") != "") else False
    hide screen main_ui
    python:
        # Determine relationship type
        DressBuyIsRelative = 0
        if girl_name_dns == 'sandra':
            DressBuyIsRelative = 1  # Mother
        elif girl_name_dns in ['melissa', 'amanda']:
            DressBuyIsRelative = 2  # Sister
        # else: 0 = non-relative
        
        # Show appropriate image based on character
        if girl_name_dns == 'amanda':
            ShowImage(girl_name_dns, 'tavern', 'angry')
        elif girl_name_dns == 'becky':
            ShowImage(girl_name_dns, 'portraits', 'portrait1')
        elif girl_name_dns == 'sandra':
            ShowImage(girl_name_dns, 'tavern', 'cleaning1')
        elif girl_name_dns == 'melissa':
            ShowImage(girl_name_dns, 'tavern', 'angry')
        elif girl_name_dns == 'georgett':
            ShowImage(girl_name_dns, 'portraits', 'portrait3')
        # Liza intentionally omitted
        
        # Build initial dialogue with relationship-specific additions
        base_dialogue = f'"Ага!" воскликнула {RealName.get(girl_name_dns, girl_name_dns)} "Явился значит! Мы где договаривались встретиться? Я тебя ждала, как дура, битый час под дверью, а ты шлялся незнамо где! Ну и нафига было предлагать мне обновку купить если ты даже зад свой от кровати не способен вовремя оторвать!"'
        
        if DressBuyIsRelative == 1:
            base_dialogue += ' "Решил, значиться, поиздеваться над мамой! Ну и сыночка же я родила!"'
        elif DressBuyIsRelative == 2:
            base_dialogue += ' "Значит ты считаешь, что мол если я твоя младшая сестра, то ты можешь глумиться надо мной как тебе угодно! Ну знаешь, братик!"'
        else:
            base_dialogue += ' "Связалась я с тобой, на свою голову! Думала ты и правда мне подарочек хочешь сделать, а ты, оказывается, только издевался!"'
        
        renpy.say(None, base_dialogue)

    "Что ответить?"

    menu:
        "Что хочу, то и ворочу":
            python:
                # Build response based on relationship
                address_term = ""
                if DressBuyIsRelative == 1:
                    address_term = "мамочка"
                elif DressBuyIsRelative == 2:
                    address_term = "сестренка"
                else:
                    address_term = "дорогуша"
                
                response = f'"Знаешь, что, {address_term}?! Я своему слову хозяин. Захотел - позвал, захотел передумал! Я тебе подарок собирался купить, а не ты мне! Так что не надо мне тут ля-ля-тополя разводить. Не будешь тут мне надоедать, может опять передумаю и все-таки куплю тебе чего."'
                renpy.say(None, response)
                
                reaction = f'"Ты, ты, ты..." с трудом выдавила {RealName.get(girl_name_dns, girl_name_dns)}, пораженная вашим разумным, логичным и исполненным собственного достоинства ответом. "Ну и козел же ты!" - продолжила она, подтверждая лишний раз ту простую истину что женщинам недоступна логика, и отвернулась. Похоже, разговор с вами закончился.'
                renpy.say(None, reaction)
                
                renpy.call('SlutFriendsIncrease', girl_name_dns, 1, 1, -4, 0, 0, 0)
            jump DressNoShow_End
            
        "Извиниться":
            python:
                # Build apology based on relationship
                address_term = ""
                if DressBuyIsRelative == 1:
                    address_term = "мамусик"
                elif DressBuyIsRelative == 2:
                    address_term = "сестричка"
                else:
                    address_term = "котеночек"
                
                apology = f'"Ой, ты знаешь {address_term}, я забегался по делам и опоздал."'
                renpy.say(None, apology)
                
                conversation = f'"По каким-таким делам ты с утра пораньше бегал?" недоуменно ответила {RealName.get(girl_name_dns, girl_name_dns)}. "Да, надо было там сделать кое-что." туманно объяснили вы. "Прости, я виноват. Не дуйся."'
                renpy.say(None, conversation)
                
                # Determine next meeting day
                next_day = "завтра" if week != 6 else "понедельник"
                resolution = f'"Ну ладно, раз так, то давай будем считать, что мы перенесли наш поход на {next_day}."'
                renpy.say(None, resolution)
                
                ending = f'"Ну давай!" промямлили вы, будучи застигнутым врасплох таким оборотом дел. "Вот и ладушки, утром, как всегда!" сказала повеселевшая {RealName.get(girl_name_dns, girl_name_dns)} и убежала.'
                renpy.say(None, ending)
                
                # Add to daily events list
                DailyEventsList_Add(girl_name_dns, "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy")
            jump DressNoShow_End
            
        "Платить, но не каяться" if money > 50:
            python:
                # Build payment response based on relationship
                address_term = ""
                if DressBuyIsRelative == 1:
                    address_term = "мамусик"
                elif DressBuyIsRelative == 2:
                    address_term = "сестричка"
                else:
                    address_term = "котеночек"
                
                payment_speech = f'"Ой, ты знаешь {address_term}, я забегался по делам и опоздал, но не унывай, вот, деньги, которые я отложил для нашего похода за покупками."'
                renpy.say(None, payment_speech)
                
                continuation = '"Зашиваюсь я с делами совсем, так что давай ты купишь себе что-нибудь сама, а я побежал. Хорошо?"'
                renpy.say(None, continuation)
                
                reaction = f'"Ну ладно!" {RealName.get(girl_name_dns, girl_name_dns)} слегка повеселела.'
                renpy.say(None, reaction)
                
                renpy.call('SlutFriendsIncrease', girl_name_dns, 20, 2, 1, 0, 0, 0)
                money -= 50
                renpy.call('stat')
            jump DressNoShow_End

    label DressNoShow_End:
        "Вот и поболтали."
        if _dress_no_show_restore_ui:
            show screen main_ui
        return

    return

# Helper labels for missing functions
# label show_image(category, subcategory, image_name):
#     # Placeholder for image display
#     return

# label SlutFriendsIncrease(girl, param1, param2, param3, param4, param5, param6):
#     # Logic for increasing sluttiness and friendship values
#     return

# label Table_NewLine(table_name, param1, param2, param3, param4, param5, param6, param7, param8):
#     # Logic for adding to daily events table
#     return

# label stat():
#     # Update statistics display
#     return

# --- END ---
# This label can be called with `call DressNoShow(girl_name_dns)` to trigger the event. All logic and text are preserved and mapped to Ren'Py idioms.
