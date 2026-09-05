# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_bar_observe_available(_bar_object=None):
        return bool(player.tavern_management.isTavernOpen)


    def tavern_bar_invite_targets():
        targets = []
        clara_info = people.get_info("clara")
        becky_info = people.get_info("becky")
        if str(people.location("clara") or "") == "TavernMain" and clara_info is not None and int(clara_info.gifted_today or 0) == 0:
            targets.append(("clara", "Клариссу"))
        if str(people.location("becky") or "") == "TavernMain" and becky_info is not None and int(becky_info.gifted_today or 0) == 0:
            targets.append(("becky", "Бекки"))
        for npc_id, caption in (
            ("sandra", "Сандру"),
            ("melissa", "Мелиссу"),
            ("amanda", "Аманду"),
        ):
            npc_info = people.get_info(npc_id)
            if str(people.location(npc_id) or "") == "TavernMain" and npc_info is not None and int(npc_info.gifted_today or 0) == 0:
                targets.append((npc_id, caption))
        return targets

    TavernMainBarObject = GameObject(
        object_id="bar_001",
        name="Барная стойка",
        description="Широкая барная стойка, за которой обычно выдают еду и выпивку.",
        picture="images/tavern/mainhall/bar_mainHall.png",
        actions=[
            ObjectAction(
                action_id="observe_hall",
                label="Наблюдать за происходящим в зале",
                hook="call",
                target="TavernMainBarObserveHall",
                condition=tavern_bar_observe_available,
            ),
            ObjectAction(
                action_id="drink_ale",
                label="Выпить эля",
                hook="call",
                target="Drink",
                args=("drink_ale_001", "TavernMain", "Кружка доброго эля помогает немного расслабиться.", "bar_001"),
            ),
            ObjectAction(
                action_id="invite_to_drink",
                label="Позвать кого-нибудь выпить",
                hook="call",
                target="TavernMainBarInviteMenu",
            ),
        ],
        carriable=False,
        stackable=False,
    )


label TavernMainBarObserveHall:
    $ renpy.dynamic("_tavern_observation", "_tavern_observation_text", "_tavern_observation_event")
    call RoomEnterEventGate("TavernMain", False)
    $ _tavern_observation_event = bool(_return)
    if not _tavern_observation_event:
        $ _tavern_observation = tavern_main_routine_visual_data()
        $ scene_runtime.picture = str(_tavern_observation.get("picture", "") or tavern_main_picture())
        $ _tavern_observation_text = str(_tavern_observation.get("text", "") or "").strip()
        if _tavern_observation_text:
            $ scene_runtime.text = "Вы проводите час у барной стойки, наблюдая за работой в главной зале.\n\n" + _tavern_observation_text
        else:
            $ scene_runtime.text = "Вы проводите час у барной стойки, наблюдая за тем, что происходит в главной зале."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Наблюдение за залом"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = [MenuItem("Назад", Call("TavernMainObjectMenu", "bar_001"))]
    $ calendar_v2.advance_minutes(60)
    return


label TavernMainBarInviteMenu:
    $ renpy.dynamic("_caption", "_npc_id")
    $ main_ui_runtime.action_title = "Кого позвать к стойке"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ scene_runtime.text = "У стойки сейчас можно спокойно перекинуться парой слов и разделить по кружке эля."
    $ scene_runtime.location_text = scene_runtime.text
    python:
        for _npc_id, _caption in tavern_bar_invite_targets():
            main_ui_runtime.action_items.append(MenuItem("Позвать %s выпить" % _caption, Call("TavernMainBarInviteApply", _npc_id)))
        if len(main_ui_runtime.action_items) <= 0:
            scene_runtime.text = "Сейчас рядом нет никого, кого стоило бы звать к стойке, или на сегодня вы уже угощали всех, кого могли."
            scene_runtime.location_text = scene_runtime.text
        main_ui_runtime.action_items.append(MenuItem("Назад", Call("TavernMainObjectMenu", "bar_001")))
    return


label TavernMainBarInviteApply(target_npc=""):
    $ renpy.dynamic("_bar_target", "_bar_info", "_bar_effect")
    $ _bar_target = str(target_npc or "").strip().lower()
    if _bar_target == "":
        call TavernMainBarInviteMenu
        return
    if int(player.economy.money or 0) < 2:
        $ scene_runtime.text = "На угощение сейчас не хватает денег."
        $ scene_runtime.location_text = scene_runtime.text
        call TavernMainBarInviteMenu
        return
    $ player.spend_money(2)
    $ calendar_v2.advance_minutes(30)
    $ _bar_info = people.get_info(_bar_target)
    if _bar_info is not None:
        $ _bar_info.mark_talked(1)
        $ _bar_info.gifted_today = int(_bar_info.gifted_today or 0) + 1
        $ _bar_info.change_social(friend_delta=1)
    $ player.change_stat("fun", 4)
    $ _bar_effect = player_apply_item_social_effects(_bar_target, "drink_ale_001", True)
    if _bar_target == "clara":
        $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
    $ scene_runtime.text = "Вы зовете %s к стойке и ставите по кружке эля. Разговор быстро становится свободнее и теплее обычного." % _action_display_name(_bar_target)
    if str((_bar_effect or {}).get("text", "") or "").strip() != "":
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n" + str((_bar_effect or {}).get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call TavernMainObjectMenu("bar_001")
    return
