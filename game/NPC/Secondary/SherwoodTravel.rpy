# ================================================================================
# Robin / Blackwood road story labels.
#
# Room owns place data: rooms.get("BlackwoodRoad").
# Event availability is owned by sherwoodThreadList in StoryEventRuntime.rpy.
# These labels own only authored scene flow, images, choices, and state mutation.
# ================================================================================

init python:
    BlackwoodRoadRoomDefinition = Room(
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
            "on_horse": 0,
        },
    )


label SherwoodRobbedHorseTakeCode:
    $ player.horse.remove()
    $ Mongol.will_try_to_steal = False
    $ Robin.knows_big_tits_village = True
    return


label SherwoodRobbedAndGoCode:
    $ player.spend_money(50)
    $ Becky.robin_robbery_stage = max(1, int(Becky.robin_robbery_stage or 0))
    $ Robin.robbery_count += 1
    if Robin.negotiation_stage == 1:
        $ Robin.negotiation_stage = 2
    $ calendar_v2.hour = 16
    $ calendar_v2.minute = 0
    call stat
    return


label SherwoodKunidellOpenedCode(OnHorse=0):
    $ renpy.dynamic("_blackwood_trade_profit")
    $ Robin.kunidell_opened = True
    $ calendar_v2.hour = 16
    $ calendar_v2.minute = 0
    if int(OnHorse or 0) == 1:
        $ _blackwood_trade_profit = procedural_randint(50, 300, "blackwood_kunidell_trade_%s" % int(current_game_day() or 0))
        $ player.add_money(200 + _blackwood_trade_profit)
        $ Robin.kunidell_deliveries += 1
    call stat
    return


label BlackwoodRoad:
    $ rooms.enter("BlackwoodRoad")
    $ scene_runtime.picture = rooms.get("BlackwoodRoad").bg_picture
    $ scene_runtime.text = rooms.get("BlackwoodRoad").visible_descriptions()[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.get("BlackwoodRoad").mark_visited()
    call RoomEnterEventGate(rooms.current_code, False)
    $ main_ui_runtime.action_title = "Блэквудская вырубка"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [
        MenuItem("Вернуться в трактир", movement_actions("TavernMain", 60)),
    ]
    while True:
        call screen main_ui


label story_robin_blackwood_ambush_0:
    $ renpy.dynamic("_blackwood_on_horse", "_blackwood_travel_verb")
    show screen main_ui
    $ main_ui_runtime.mode = "event"
    $ _blackwood_on_horse = int(rooms.get("BlackwoodRoad").custom_properties.get("on_horse", 0) or 0)
    $ _blackwood_travel_verb = "едете" if _blackwood_on_horse == 1 else "идете"
    vscene "images/Robin/robin.png"
    $ scene_runtime.text = "Насвистывая, вы %s по дороге к Куниделлу. Через несколько часов поля и перелески уступают место вырубке. Дорога превращается почти в тропинку между пнями и молодым кустарником.\n\n" % str(_blackwood_travel_verb)
    if Robin.robbery_count == 0:
        $ scene_runtime.text += "Вдруг впереди вы замечаете группу мужчин в зеленых трико."
    elif not Robin.identity_known:
        $ scene_runtime.text += "Вдруг впереди вы замечаете уже знакомых грабителей."
    else:
        $ scene_runtime.text += "Вдруг впереди вы замечаете старых знакомых: несчастных безработных лесорубов во главе с Робин Гудом."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Идти дальше":
            jump story_robin_blackwood_approach

        "Вернуться обратно в Коитополис":
            jump story_robin_blackwood_return_to_city


label story_robin_blackwood_approach:
    call IntRobinTalk
    if Robin.mongol_safe_pass:
        jump story_robin_blackwood_mongol_pass
    if Robin.robbery_count == 0:
        jump story_robin_blackwood_first_robbery
    jump story_robin_blackwood_repeat_robbery


label story_robin_blackwood_mongol_pass:
    vscene "images/Robin/mongolAndRobin1.png"
    $ scene_runtime.text = "Вы уже приготовились к привычному разговору о добровольных пожертвованиях, но один из разбойников вдруг прищурился и дернул Робина за рукав.\n\n\"Йо, браза,\" сказал он. \"Это тот самый трактирщик. Монгол велел своих предупредить: этот чувак не мазафака, он его из колодок вытащил.\"\n\nРобин некоторое время смотрит на вас с новым интересом, потом широко улыбается.\n\n\"Вот это другое дело, бразар. За Монгола уважуха. Раз наш человек сказал, что ты браза, значит сегодня ты едешь как браза. Деньги при себе оставь, коняшку тоже. Но если кто спросит - мы тебя не пропускали. Социяльная ответственность, понимаешь?\""
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    call SherwoodKunidellOpenedCode(rooms.get("BlackwoodRoad").custom_properties.get("on_horse", 0))
    if int(rooms.get("BlackwoodRoad").custom_properties.get("on_horse", 0) or 0) == 1:
        $ scene_runtime.text = "До Куниделла вы добрались уже без приключений. Эльфы встретили мешки Беккиных овощей с таким видом, будто вы привезли им редчайшие дары заморских королевств.\n\nТорговля прошла удачно, дорога теперь открыта."
    else:
        $ scene_runtime.text = "Без груза и без лошади делать в Куниделле было особенно нечего, но теперь дорога хотя бы стала понятной. Слово Монгола действительно сработало: люди Робина вас пропустили."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ event_runtime.active_thread.advance()
    $ main_ui_runtime.mode = "scene"
    return True


label story_robin_blackwood_first_robbery:
    $ renpy.dynamic("_robbers_head")
    show screen main_ui
    vscene "images/Robin/portrait2.jpg"
    $ _robbers_head = "Робин Гуд" if Robin.identity_known else "предводитель"
    $ scene_runtime.text = "\"Семь бед - один ответ!\" думаете вы и продолжаете путь. Мужики в трико заметно оживляются, в руках у них появляются луки, стрелы и разное колюще-режущее железо.\n\nКогда вы приближаетесь, их %s, здоровенный человек с золотой цепью и капюшоном, выходит навстречу и широко улыбается: \"Йо, браза! Куда идешь?\"\n\n\"В Куниделл,\" скромно отвечаете вы.\n\nПосле этого его лицо становится серьезным. \"Хей, мэн, я и мои браза - простые лесорубы, доведенные обстоятельствами до отчаяния. Я вижу, ты хочешь сделать добровольное пожертвование на наше благое дело.\"" % str(_robbers_head)
    if int(rooms.get("BlackwoodRoad").custom_properties.get("on_horse", 0) or 0) == 1:
        $ scene_runtime.text += " \"Все деньги. Ну и лошадь конечно, она нам тоже пригодится.\""
    else:
        $ scene_runtime.text += " \"Все имеющиеся у тебя деньги.\""
    $ Becky.sherwood_suspicion = int(Becky.sherwood_suspicion or 0) + 10
    $ Becky.knows_blackwood = True
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Попрощаться":
            jump story_robin_blackwood_robbed_return


label story_robin_blackwood_repeat_robbery:
    $ renpy.dynamic("_robbers_head")
    show screen main_ui
    vscene "images/Robin/portrait2.jpg"
    $ _robbers_head = "Робин Гуд" if Robin.identity_known else "предводитель"
    $ scene_runtime.text = "При виде вас %s и его друзья очень удивляются.\n\n\"Слышь мужики, а я думал, что он трактирщик,\" недоуменно бормочет главарь. Потом он сменяет тон на радостный: \"Йо, бразар, ты нам донату занес? Ты кул, бразар, видно что не мазафака.\"" % str(_robbers_head)
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"

    menu:
        "Ага, вот ваши денежки":
            jump story_robin_blackwood_robbed_return


label story_robin_blackwood_robbed_return:
    $ scene_runtime.text = "Вы пытаетесь сохранить лицо, но трудовые мозолистые руки быстро разлучают вас с кошельком."
    if int(player.economy.money or 0) >= 50:
        $ scene_runtime.text += "\n\nХорошо еще, что вы взяли с собой только 50 мараведи."
    if int(rooms.get("BlackwoodRoad").custom_properties.get("on_horse", 0) or 0) == 1:
        $ scene_runtime.text += "\n\nЕще один лесоруб заботливо забирает поводья вашей лошади. \"Йо, бразас, в Большие Сиськи теперь легче будет добраться!\""
        call SherwoodRobbedHorseTakeCode
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    call SherwoodRobbedAndGoCode
    $ main_ui_runtime.mode = "scene"
    return True


label story_robin_blackwood_return_to_city:
    vscene "images/Robin/robin.png"
    if Robin.robbery_count == 0:
        $ Becky.sherwood_suspicion = int(Becky.sherwood_suspicion or 0) + 2
        $ Becky.knows_blackwood = True
        $ scene_runtime.text = "Решив, что встреча со странными мужиками в трико на пустынной вырубке ничего хорошего не принесет, вы разворачиваетесь и уходите обратно."
    elif not Robin.identity_known:
        $ scene_runtime.text = "Решив, что новая встреча с грабителями ничего хорошего не принесет, вы разворачиваетесь и уходите обратно."
    else:
        $ scene_runtime.text = "Решив, что новая встреча с Робин Гудом на пустынной вырубке ничего хорошего не принесет, вы разворачиваетесь и уходите обратно."
    $ scene_runtime.text += "\n\nМожет, вас преследовали, может, нет, но вы благополучно выбрались с вырубки на обжитую местность. Уже смеркалось, и вам осталось только вернуться в Коитополис."
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ calendar_v2.hour = 16
    $ calendar_v2.minute = 0
    $ main_ui_runtime.mode = "scene"
    return True
