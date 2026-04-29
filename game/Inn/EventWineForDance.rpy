# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def wine_for_dance_costs():
        return {"wine": 50, "products": 40, "money": 20}

    def wine_for_dance_can_sponsor():
        costs = wine_for_dance_costs()
        return (
            int(winenum or 0) >= int(costs["wine"])
            and int(productnum or 0) >= int(costs["products"])
            and int(money or 0) >= int(costs["money"])
        )

    def wine_for_dance_apply_choice(reaction_code=1):
        code = int(reaction_code or 0)
        costs = wine_for_dance_costs()

        if code == 1:
            return {
                "text": "Вы решили поддержать народные гуляния.",
                "dance_sponsor": 1,
                "wine_delta": -int(costs["wine"]),
                "product_delta": -int(costs["products"]),
                "money_delta": -int(costs["money"]),
            }
        if code == 2:
            return {
                "text": "Вы бы были и рады поддержать оные гуляния, но, к сожалению, у вас было недостаточно вина и продуктов для столь благородной затеи.",
                "dance_sponsor": 0,
                "wine_delta": 0,
                "product_delta": 0,
                "money_delta": 0,
            }
        return {
            "text": "Вы решили что ваши финансы не позволяют участвовать в такой затее.",
            "dance_sponsor": 0,
            "wine_delta": 0,
            "product_delta": 0,
            "money_delta": 0,
        }

    def tavern_breakfast_can_offer_dance_sponsorship():
        return (
            int(hour or 0) < 12
            and int(week or 0) in (3, 4)
            and int(EventsCount.get(10, 0) or 0) > 0
            and str(NewEvents.get("10_" + str(int(EventsCount.get(10, 0) or 0) - 1), "") or "") == "WineForDance"
        )

    def consume_wine_for_dance_breakfast_event():
        mandatory_count = int(EventsCount.get(10, 0) or 0)
        if mandatory_count <= 0:
            return 0
        event_idx = mandatory_count - 1
        event_key = "10_" + str(event_idx)
        if str(NewEvents.get(event_key, "") or "") != "WineForDance":
            return 0
        EventsCount[10] = event_idx
        return 1

    def wine_for_dance_breakfast_appreciation():
        present_ids = []
        for npc_id in ("sandra", "melissa", "amanda"):
            if str(getLocation(npc_id) or "") == "TavernKitchen":
                present_ids.append(npc_id)
        if str(getLocation("becky") or "") == "TavernKitchen":
            present_ids.append("becky")
        for npc_id in present_ids:
            Friends[npc_id] = min(20, int(Friends.get(npc_id, 0) or 0) + 1)
        return present_ids

label EventWineForDance(eyewitness=0):
    $ YourReaction1 = 0
    $ Result = "К вам подошла Сандра, ваша кухарка и фактическая распорядительница трактирного хозяйства, и сказала:\n\"Стефан, дорогой, ты помнишь же, что в пятницу вечером будут гуляния и танцы? Мы можем тоже поучаствовать и выставить на них выпивку и угощение за счет нашего трактира. Это конечно обойдется в копеечку, так как, если уж мы за это возьмемся то придется выставить 5 бочонков вина и наготовить закуски из 4 мешков продуктов, да еще на шатер уйдет 20 мараведи. Но, с другой, стороны, такая щедрость привлечет к нам людей.\""

    if eyewitness > 0:
        $ current_action_title = "Ваше решение"
        $ current_action_content = None
        $ _wine_choices = []

        if wine_for_dance_can_sponsor():
            $ _wine_choices.append(MenuItem("Отправить вино и начать готовить закуску", [SetVariable("current_action_items", []), Call("EventWineForDanceApply", 1)]))
        else:
            $ _wine_choices.append(MenuItem("Вы посокрушались о нехватке запасов", [SetVariable("current_action_items", []), Call("EventWineForDanceApply", 2)]))

        $ _wine_choices.append(MenuItem("Отказаться", [SetVariable("current_action_items", []), Call("EventWineForDanceApply", 3)]))
        $ current_action_items = _wine_choices
        $ Result += "\n\nСобираетесь ли вы пожертвовать на общегородской праздник?"
    else:
        $ current_action_items = []
        $ Result = ""

    return Result

label EventWineForDanceApply(reaction_code=1):
    $ consume_wine_for_dance_breakfast_event()
    $ YourReaction1 = reaction_code
    $ _wine_outcome = wine_for_dance_apply_choice(reaction_code)
    $ MainTxt = str(_wine_outcome.get("text", "") or "")
    $ CurLocDesc = MainTxt
    $ DanceSponsor = int(_wine_outcome.get("dance_sponsor", 0) or 0)
    $ winenum += int(_wine_outcome.get("wine_delta", 0) or 0)
    $ productnum += int(_wine_outcome.get("product_delta", 0) or 0)
    $ money += int(_wine_outcome.get("money_delta", 0) or 0)
    if int(DanceSponsor or 0) == 1 and str(CurLoc or "") == "TavernKitchen" and int(hour or 0) < 12:
        $ _crew_appreciation = wine_for_dance_breakfast_appreciation()
        $ fun = _player_clamp(int(fun or 0) + 2, 0, 100)
        if len(list(_crew_appreciation or [])) > 0:
            $ MainTxt = str(MainTxt or "") + "\n\nЗа столом решение встречают заметно теплее. Домашние переглядываются с одобрением: щедрый жест явно поднимает всем настроение."
            $ CurLocDesc = MainTxt
    call stat
    if str(CurLoc or "") == "TavernKitchen" and bool(TavernBreakfastEventActive):
        $ TavernKitchenSavedText = MainTxt
        call TavernKitchenBreakfastShowText(MainTxt, "TavernKitchenBreakfastMenu")
        return
    $ current_action_title = ""
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться к своим делам", Call("EventWineForDanceFinish"))]
    call ReturnToMainUI
    return


label EventWineForDanceFinish:
    $ _wine_return_room = str(getattr(CurrentRoom, "code_name", "") or CurLoc or "TavernMain")
    if _wine_return_room == "TavernKitchen":
        jump TavernKitchen
    elif _wine_return_room == "TavernMain":
        jump TavernMain
    call RefreshCurrentActionMenu(_wine_return_room, "", True)
    $ main_ui_restore_room_scene_state()
    call ReturnToMainUI
    return
