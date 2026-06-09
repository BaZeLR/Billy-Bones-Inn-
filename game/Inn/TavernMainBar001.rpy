# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def tavern_bar_clara_melissa_gossip_available():
        return (
            str(CurLoc or "") == "TavernMain"
            and str(getLocation("clara") or "") == "TavernMain"
            and str(getLocation("melissa") or "") == "TavernMain"
            and int(time or 0) == 2
            and story_event_available("TavernMain", "overheard")
        )

    def tavern_bar_invite_targets():
        targets = []
        if str(getLocation("clara") or "") == "TavernMain" and int(GiftedToday.get("clara", 0) or 0) == 0:
            targets.append(("clara", "Клариссу"))
        if str(getLocation("becky") or "") == "TavernMain" and int(GiftedToday.get("becky", 0) or 0) == 0:
            targets.append(("becky", "Бекки"))
        for npc_id, caption in (
            ("sandra", "Сандру"),
            ("melissa", "Мелиссу"),
            ("amanda", "Аманду"),
        ):
            if str(getLocation(npc_id) or "") == "TavernMain" and int(GiftedToday.get(npc_id, 0) or 0) == 0:
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
                target="TavernMainBarPlaceholderEvent",
            ),
        ],
        carriable=False,
        stackable=False,
    )


label TavernMainBarInviteMenu:
    $ current_action_title = "Кого позвать к стойке"
    $ current_action_content = None
    $ current_action_items = []
    $ MainTxt = "У стойки сейчас можно спокойно перекинуться парой слов и разделить по кружке эля."
    $ CurLocDesc = MainTxt
    python:
        for _npc_id, _caption in tavern_bar_invite_targets():
            current_action_items.append(MenuItem("Позвать %s выпить" % _caption, Call("TavernMainBarInviteApply", _npc_id)))
        if len(current_action_items) <= 0:
            MainTxt = "Сейчас рядом нет никого, кого стоило бы звать к стойке, или на сегодня вы уже угощали всех, кого могли."
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Call("TavernMainObjectMenu", "bar_001")))
    return


label TavernMainBarInviteApply(target_npc=""):
    $ _bar_target = str(target_npc or "").strip().lower()
    if _bar_target == "":
        call TavernMainBarInviteMenu
        return
    if int(money or 0) < 2:
        $ MainTxt = "На угощение сейчас не хватает денег."
        $ CurLocDesc = MainTxt
        call TavernMainBarInviteMenu
        return
    $ money = int(money or 0) - 2
    $ calendar_v2.advance_minutes(30)
    $ Talked[_bar_target] = int(Talked.get(_bar_target, 0) or 0) + 1
    $ TalkedToday[_bar_target] = int(TalkedToday.get(_bar_target, 0) or 0) + 1
    $ GiftedToday[_bar_target] = int(GiftedToday.get(_bar_target, 0) or 0) + 1
    $ Friends[_bar_target] = min(20, int(Friends.get(_bar_target, 0) or 0) + 1)
    $ fun = _player_clamp(int(fun or 0) + 4, 0, 100)
    $ _bar_effect = player_apply_item_social_effects(_bar_target, "drink_ale_001", True)
    if _bar_target == "clara":
        $ ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 1)
    if _bar_target == "becky":
        $ BeckyVar["BarDrinkDay"] = int(dayspassed or 0)
    $ MainTxt = "Вы зовете %s к стойке и ставите по кружке эля. Разговор быстро становится свободнее и теплее обычного." % _action_display_name(_bar_target)
    if str((_bar_effect or {}).get("text", "") or "").strip() != "":
        $ MainTxt = str(MainTxt or "") + "\n\n" + str((_bar_effect or {}).get("text", "") or "")
    $ CurLocDesc = MainTxt
    call stat
    call TavernMainObjectMenu("bar_001")
    return


label TavernMainBarPlaceholderEvent:
    if tavern_bar_clara_melissa_gossip_available():
        call checkTriggers("TavernMain", "overheard", 0)
        return
    python:
        _bar_events = [
            "Вы задерживаетесь у стойки и ловите себя на мысли, что у бара всегда скапливаются самые удобные слухи: кто с кем поссорился, кто кому должен и у кого язык развязывается после второй кружки.",
            "Пока вы стоите у стойки, трактир словно ненадолго становится центром всего околотка. Именно отсюда удобнее всего подмечать чужие привычки, обрывки разговоров и назревающие истории.",
            "У барной стойки легче всего сделать вид, что вы просто заняты делом, и при этом слушать вполуха все, что происходит вокруг. Позже из таких мелочей наверняка будут рождаться новые события.",
        ]
        _bar_index = int((dayspassed or 0) + (hour or 0) + (minute or 0)) % len(_bar_events)
        MainTxt = _bar_events[_bar_index]
        CurLocDesc = MainTxt
    call TavernMainObjectMenu("bar_001")
    return
