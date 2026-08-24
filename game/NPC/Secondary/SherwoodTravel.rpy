    $ Robin.location = "BlackwoodRoad"    $ Robin.location = "BlackwoodRoad"    $ Robin.location = "BlackwoodRoad"# ================================================================================
# Robin / Blackwood road story labels.
#
# Room owns place data: BlackwoodRoadRoom.
# Event availability is owned by sherwoodThreadList in StoryEventRuntime.rpy.
# These labels own only authored scene flow, images, choices, and state mutation.
# ================================================================================

default BlackwoodTravelOnHorse = 0

default BlackwoodTravelOnHorse = 0

default BlackwoodTravelOnHorse = 0

init python:
    BlackwoodRoadRoom = Room(
        code_name="BlackwoodRoad",
        group_name=ROOM_GROUP_FOREST,
        display_name="Блэквудская вырубка",
        bg_picture="images/Robin/robin.png",
        descriptions=[
            RoomDescription(
                text="Дорога к Куниделлу проходит через Блэквудскую вырубку: редкие пни, молодая поросль и тропа, где слишком легко устроить засаду.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в трактир", target="TavernMain", minutes_to_pass=60),
        ],
        custom_properties={
            "legacy_location": "SherwoodTravel",
            "legacy_location": "SherwoodTravel",
            "legacy_location": "SherwoodTravel",
        },
    )


label SherwoodRobbedHorseTakeCode:
    $ MyStallion = ""
    $ peopleInfo["mongol"].var["WillTryToSteal"] = 0
    $ Robin.set_var_min("KnowBigTitsVillage", 1)
    return


label SherwoodRobbedAndGoCode:
    $ money = max(0, int(money or 0) - 50)
    $ Becky.var["RobbedByRobin"] = max(1, int(Becky.var.get("RobbedByRobin", 0) or 0))
    $ Robin.add_var_int("RobbedNum", 1)
    if Robin.var_int("Negotiate", 0) == 1:
        $ Robin.set_var_int("Negotiate", 2)
    $ calendar_v2.hour = 16
    $ calendar_v2.minute = 0
    call stat
    return


label SherwoodKunidellOpenedCode(OnHorse=0):
    $ Robin.set_var_int("MongolSafePassUsed", 1)
    $ Robin.set_var_int("KunidellOpened", 1)
    $ calendar_v2.hour = 16
    $ calendar_v2.minute = 0
    if int(OnHorse or 0) == 1:
        $ _blackwood_trade_profit = procedural_randint(50, 300, "blackwood_kunidell_trade_%s" % int(current_game_day() or 0))
        $ money += 200 + _blackwood_trade_profit
        $ Robin.add_var_int("KunidellDeliveries", 1)
    call stat
    return


label SherwoodTravel(OnHorse=0):
    $ BlackwoodTravelOnHorse = int(OnHorse or 0)
    jump BlackwoodRoad


label SherwoodTravel(OnHorse=0):
    $ BlackwoodTravelOnHorse = int(OnHorse or 0)
    jump BlackwoodRoad


label SherwoodTravel(OnHorse=0):
    $ BlackwoodTravelOnHorse = int(OnHorse or 0)
    jump BlackwoodRoad


label SherwoodTravel(OnHorse=0):
    $ BlackwoodRoadRoom.custom_properties["on_horse"] = int(OnHorse or 0)
    jump BlackwoodRoad


label SherwoodTravel(OnHorse=0):
    $ BlackwoodRoadRoom.custom_properties["on_horse"] = int(OnHorse or 0)
    jump BlackwoodRoad


label SherwoodTravel(OnHorse=0):
    $ BlackwoodRoadRoom.custom_properties["on_horse"] = int(OnHorse or 0)
    jump BlackwoodRoad


label BlackwoodRoad:
    $ CurrentRoom = BlackwoodRoadRoom
    $ CurLoc = "BlackwoodRoad"
    $ scene_image = BlackwoodRoadRoom.bg_picture
    $ _layout_last_picture = scene_image
    $ MainTxt = BlackwoodRoadRoom.visible_descriptions()[0].text
    $ CurLocDesc = MainTxt
    $ BlackwoodRoadRoom.mark_visited()
    call RoomEnterEventGate(CurLoc, False)
    $ current_action_title = "Блэквудская вырубка"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вернуться в трактир", Call("MoveToRoom", "TavernMain", 60)),
    ]
    while True:
        call screen main_ui


label story_robin_blackwood_ambush_0:
    show screen main_ui
    $ SignalBlockTime = 1
    $ UI_mode = "event"
    $ Robin.location = "BlackwoodRoad"
    $ Robin.set_var_int("BlackwoodRoadSeen", 1)
    $ _blackwood_on_horse = int(BlackwoodTravelOnHorse or 0)
    $ _blackwood_travel_verb = "едете" if _blackwood_on_horse == 1 else "идете"
    vscene "images/Robin/robin.png"
    $ MainTxt = "Насвистывая, вы [_blackwood_travel_verb] по дороге к Куниделлу. Через несколько часов поля и перелески уступают место вырубке. Дорога превращается почти в тропинку между пнями и молодым кустарником.\n\n"
    if Robin.var_int("RobbedNum", 0) == 0:
        $ MainTxt += "Вдруг впереди вы замечаете группу мужчин в зеленых трико."
    elif Robin.var_int("KnowHim", 0) == 0:
        $ MainTxt += "Вдруг впереди вы замечаете уже знакомых грабителей."
    else:
        $ MainTxt += "Вдруг впереди вы замечаете старых знакомых: несчастных безработных лесорубов во главе с Робин Гудом."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Идти дальше":
            jump story_robin_blackwood_approach

        "Вернуться обратно в Коитополис":
            jump story_robin_blackwood_return_to_city


label story_robin_blackwood_approach:
    call IntRobinTalk
    if Robin.var_int("MongolSafePass", 0) == 1:
        jump story_robin_blackwood_mongol_pass
    if Robin.var_int("RobbedNum", 0) == 0:
        jump story_robin_blackwood_first_robbery
    jump story_robin_blackwood_repeat_robbery


label story_robin_blackwood_mongol_pass:
    vscene "images/Robin/mongolAndRobin1.png"
    $ MainTxt = "Вы уже приготовились к привычному разговору о добровольных пожертвованиях, но один из разбойников вдруг прищурился и дернул Робина за рукав.\n\n\"Йо, браза,\" сказал он. \"Это тот самый трактирщик. Монгол велел своих предупредить: этот чувак не мазафака, он его из колодок вытащил.\"\n\nРобин некоторое время смотрит на вас с новым интересом, потом широко улыбается.\n\n\"Вот это другое дело, бразар. За Монгола уважуха. Раз наш человек сказал, что ты браза, значит сегодня ты едешь как браза. Деньги при себе оставь, коняшку тоже. Но если кто спросит - мы тебя не пропускали. Социяльная ответственность, понимаешь?\""
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    call SherwoodKunidellOpenedCode(BlackwoodRoadRoom.custom_properties.get("on_horse", 0))
    if int(BlackwoodTravelOnHorse or 0) == 1:
        $ MainTxt = "До Куниделла вы добрались уже без приключений. Эльфы встретили мешки Беккиных овощей с таким видом, будто вы привезли им редчайшие дары заморских королевств.\n\nТорговля прошла удачно, дорога теперь открыта."
    else:
        $ MainTxt = "Без груза и без лошади делать в Куниделле было особенно нечего, но теперь дорога хотя бы стала понятной. Слово Монгола действительно сработало: люди Робина вас пропустили."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ event_runtime.active_thread.advance()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


label story_robin_blackwood_first_robbery:
    show screen main_ui
    vscene "images/Robin/portrait2.jpg"
    $ _robbers_head = "Робин Гуд" if Robin.var_int("KnowHim", 0) else "предводитель"
    $ MainTxt = "\"Семь бед - один ответ!\" думаете вы и продолжаете путь. Мужики в трико заметно оживляются, в руках у них появляются луки, стрелы и разное колюще-режущее железо.\n\nКогда вы приближаетесь, их [_robbers_head], здоровенный человек с золотой цепью и капюшоном, выходит навстречу и широко улыбается: \"Йо, браза! Куда идешь?\"\n\n\"В Куниделл,\" скромно отвечаете вы.\n\nПосле этого его лицо становится серьезным. \"Хей, мэн, я и мои браза - простые лесорубы, доведенные обстоятельствами до отчаяния. Я вижу, ты хочешь сделать добровольное пожертвование на наше благое дело.\""
    if int(BlackwoodTravelOnHorse or 0) == 1:
        $ MainTxt += " \"Все деньги. Ну и лошадь конечно, она нам тоже пригодится.\""
    else:
        $ MainTxt += " \"Все имеющиеся у тебя деньги.\""
    $ Becky.var["SherwoodSuspect"] = int(Becky.var.get("SherwoodSuspect", 0) or 0) + 10
    $ Becky.var["KnowSherwood"] = 1
    $ Becky.var["KnowSherwood"] = 1
    $ Becky.var["KnowSherwood"] = 1
    $ Becky.var["KnowSherwood"] = 1
    $ Becky.var["KnowSherwood"] = 1
    $ Becky.var["KnowSherwood"] = 1
    $ Becky.var["KnowBlackwood"] = 1
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Попрощаться":
            jump story_robin_blackwood_robbed_return


label story_robin_blackwood_repeat_robbery:
    show screen main_ui
    vscene "images/Robin/portrait2.jpg"
    $ _robbers_head = "Робин Гуд" if Robin.var_int("KnowHim", 0) else "предводитель"
    $ MainTxt = "При виде вас [_robbers_head] и его друзья очень удивляются.\n\n\"Слышь мужики, а я думал, что он трактирщик,\" недоуменно бормочет главарь. Потом он сменяет тон на радостный: \"Йо, бразар, ты нам донату занес? Ты кул, бразар, видно что не мазафака.\""
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Ага, вот ваши денежки":
            jump story_robin_blackwood_robbed_return


label story_robin_blackwood_robbed_return:
    $ MainTxt = "Вы пытаетесь сохранить лицо, но трудовые мозолистые руки быстро разлучают вас с кошельком."
    if int(money or 0) >= 50:
        $ MainTxt += "\n\nХорошо еще, что вы взяли с собой только 50 мараведи."
    if int(BlackwoodTravelOnHorse or 0) == 1:
        $ MainTxt += "\n\nЕще один лесоруб заботливо забирает поводья вашей лошади. \"Йо, бразас, в Большие Сиськи теперь легче будет добраться!\""
        call SherwoodRobbedHorseTakeCode
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    call SherwoodRobbedAndGoCode
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


label story_robin_blackwood_return_to_city:
    vscene "images/Robin/robin.png"
    if Robin.var_int("RobbedNum", 0) == 0:
        $ Becky.var["SherwoodSuspect"] = int(Becky.var.get("SherwoodSuspect", 0) or 0) + 2
        $ Becky.var["KnowSherwood"] = 1
        $ Becky.var["KnowSherwood"] = 1
        $ Becky.var["KnowSherwood"] = 1
        $ Becky.var["KnowSherwood"] = 1
        $ Becky.var["KnowSherwood"] = 1
        $ Becky.var["KnowSherwood"] = 1
        $ Becky.var["KnowBlackwood"] = 1
        $ MainTxt = "Решив, что встреча со странными мужиками в трико на пустынной вырубке ничего хорошего не принесет, вы разворачиваетесь и уходите обратно."
    elif Robin.var_int("KnowHim", 0) == 0:
        $ MainTxt = "Решив, что новая встреча с грабителями ничего хорошего не принесет, вы разворачиваетесь и уходите обратно."
    else:
        $ MainTxt = "Решив, что новая встреча с Робин Гудом на пустынной вырубке ничего хорошего не принесет, вы разворачиваетесь и уходите обратно."
    $ MainTxt += "\n\nМожет, вас преследовали, может, нет, но вы благополучно выбрались с вырубки на обжитую местность. Уже смеркалось, и вам осталось только вернуться в Коитополис."
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ calendar_v2.hour = 16
    $ calendar_v2.minute = 0
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True
