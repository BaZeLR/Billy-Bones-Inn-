# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_bar_clara_melissa_gossip_available():
        return (
            str(rooms.current_code or "") == "TavernMain"
            and str(people.location("clara") or "") == "TavernMain"
            and str(people.location("melissa") or "") == "TavernMain"
            and story_event_available("TavernMain", "clara_tavern_visit")
        )

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
            ObjectAction(
                action_id="bar_random_event",
                label="Задержаться у стойки в ожидании истории",
                hook="call",
                target="TavernMainBarListenEvent",
            ),
        ],
        carriable=False,
        stackable=False,
    )


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


label TavernMainBarListenEvent:
    $ renpy.dynamic("_bar_events", "_bar_index")
    if tavern_bar_clara_melissa_gossip_available():
        call checkTriggers("TavernMain", "clara_tavern_visit", 0)
        return
    python:
        _bar_events = [
            "Вы задерживаетесь у стойки и ловите себя на мысли, что у бара всегда скапливаются самые удобные слухи: кто с кем поссорился, кто кому должен и у кого язык развязывается после второй кружки.",
            "Пока вы стоите у стойки, трактир словно ненадолго становится центром всего околотка. Именно отсюда удобнее всего подмечать чужие привычки, обрывки разговоров и назревающие истории.",
            "У барной стойки легче всего сделать вид, что вы просто заняты делом, и при этом слушать вполуха все, что происходит вокруг. Позже из таких мелочей наверняка будут рождаться новые события.",
        ]
        _bar_index = int(current_game_day() + int(calendar_v2.hour or 0) + int(calendar_v2.minute or 0)) % len(_bar_events)
        scene_runtime.text = _bar_events[_bar_index]
        scene_runtime.location_text = scene_runtime.text
    call TavernMainObjectMenu("bar_001")
    return
