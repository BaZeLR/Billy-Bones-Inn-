# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def wine_for_dance_costs():
        return {"wine": 50, "products": 40, "money": 20}

    def wine_for_dance_can_sponsor():
        costs = wine_for_dance_costs()
        return (
            int(player.tavern_management.winenum or 0) >= int(costs["wine"])
            and int(player.tavern_management.productnum or 0) >= int(costs["products"])
            and int(player.economy.money or 0) >= int(costs["money"])
        )

    def tavern_breakfast_can_offer_dance_sponsorship():
        return (
            int(calendar_v2.hour or 0) < 12
            and int(calendar_v2.week or 0) == 3
            and tavern_work_pending_mandatory_code("WineForDance", "TavernKitchen") == "WineForDance"
        )

    def consume_wine_for_dance_breakfast_event():
        return 1 if tavern_work_pop_mandatory_code("WineForDance", "TavernKitchen") == "WineForDance" else 0

    def wine_for_dance_breakfast_appreciation():
        present_ids = []
        for npc_id in ("sandra", "melissa", "amanda"):
            if str(people.location(npc_id) or "") == "TavernKitchen":
                present_ids.append(npc_id)
        if str(people.location("becky") or "") == "TavernKitchen":
            present_ids.append("becky")
        for npc_id in present_ids:
            npc_info = people.get_info(npc_id)
            if npc_info is not None:
                npc_info.change_social(friend_delta=1)
        return present_ids

label EventWineForDance(eyewitness=0, result=""):
    $ result = "К вам подошла Сандра, ваша кухарка и фактическая распорядительница трактирного хозяйства, и сказала:\n\"Стефан, дорогой, ты помнишь же, что в пятницу вечером будут гуляния и танцы? Мы можем тоже поучаствовать и выставить на них выпивку и угощение за счет нашего трактира. Это конечно обойдется в копеечку, так как, если уж мы за это возьмемся то придется выставить 5 бочонков вина и наготовить закуски из 4 мешков продуктов, да еще на шатер уйдет 20 мараведи. Но, с другой, стороны, такая щедрость привлечет к нам людей.\""

    if eyewitness > 0:
        $ main_ui_begin_native_scene_state("Пятничные танцы")
        $ result += "\n\nСобираетесь ли вы пожертвовать на общегородской праздник?"
        $ scene_runtime.text = result
        $ scene_runtime.location_text = scene_runtime.text
        show screen main_ui
        menu:
            "Отправить вино и начать готовить закуску" if wine_for_dance_can_sponsor():
                call WineForDanceOutcome(1)

            "Посокрушаться о нехватке запасов" if not wine_for_dance_can_sponsor():
                call WineForDanceOutcome(2)

            "Отказаться":
                call WineForDanceOutcome(3)
        $ main_ui_end_native_scene_state()
    else:
        $ result = ""

    return result

label WineForDanceOutcome(reaction_code=1, _crew_appreciation=None):
    $ consume_wine_for_dance_breakfast_event()
    if int(reaction_code or 0) == 1 and wine_for_dance_can_sponsor():
        $ player.tavern_management.dance_sponsor = 1
        $ player.tavern_management.dance_sponsor_pledge_day = current_game_day()
        $ player.tavern_management.winenum -= 50
        $ player.tavern_management.productnum -= 40
        $ player.spend_money(20)
        $ scene_runtime.text = "Вы соглашаетесь выставить на пятничных танцах пять бочонков вина, закуску и шатер от имени трактира. Сандра одобрительно кивает и сразу начинает прикидывать приготовления."
    elif int(reaction_code or 0) == 2:
        $ scene_runtime.text = "Вы с сожалением признаете, что сейчас в кладовой и кошельке не хватает запасов для такого щедрого жеста. Сандра принимает ответ и откладывает разговор."
    else:
        $ scene_runtime.text = "Вы решаете не тратить припасы трактира на городские танцы. Сандра спорить не начинает, хотя явно рассчитывала на другой ответ."
    $ scene_runtime.location_text = scene_runtime.text
    if int(player.tavern_management.dance_sponsor or 0) == 1 and str(rooms.current_code or "") == "TavernKitchen" and int(calendar_v2.hour or 0) < 12:
        $ _crew_appreciation = wine_for_dance_breakfast_appreciation()
        $ player.change_stat("fun", 20)
        if len(list(_crew_appreciation or [])) > 0:
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nЗа столом решение встречают заметно теплее. Домашние переглядываются с одобрением: щедрый жест явно поднимает всем настроение."
            $ scene_runtime.location_text = scene_runtime.text
    call stat
    if str(rooms.current_code or "") == "TavernKitchen" and bool(player.tavern_management.breakfast.event_active):
        $ tavern_kitchen_set_saved_text(scene_runtime.text)
        call TavernKitchenBreakfastShowText(scene_runtime.text)
        return
    menu:
        "Вернуться к своим делам":
            pass
    return
