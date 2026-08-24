# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    def lumber_in_shed(_obj=None):
        return CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "Shed" and _room_has_item_by_id(CurrentRoom, "lumber_001")

    def lumber_ready_for_chop(_obj=None):
        return lumber_in_shed(_obj) and _player_has_item_by_id("old_axe_001")

    LumberItem = GameItem(
        object_id="lumber_001",
        name="бревно",
        description="Тяжелое бревно, которое можно принести из леса и сложить в сарае.",
        actions=[
            ObjectAction(
                action_id="chop_lumber",
                label="Колоть бревно",
                hook="call",
                target="Chop",
                args=("lumber_001", "Shed", "", "lumber_001"),
                condition=lumber_ready_for_chop,
            ),
        ],
        price=0,
        carriable=True,
        stackable=True,
        state={
            "visible": 1,
            "curLoc": "Shed",
        },
        custom_properties={
            "item_kind": "resource",
            "resource_kind": "lumber",
            "curLoc": "Shed",
        },
    )


label Chop(what_id="", where_id="", fallback_text="", object_id=""):
    $ _chop_block = action_restriction_result("heavy_chore", "chop")
    if not _chop_block.get("ok", False):
        $ MainTxt = str(_chop_block.get("text", "") or fallback_text or "Сейчас это не получится.")
        $ CurLocDesc = MainTxt
        return
    $ item_id = get_object_id(what_id)
    $ _current_room_code = str(getattr(CurrentRoom, "code_name", "") or CurLoc or "")
    if item_id == "":
        $ MainTxt = "Непонятно, что именно вы собираетесь рубить."
        $ CurLocDesc = MainTxt
        return
    if not _player_has_item_by_id("old_axe_001"):
        $ MainTxt = "Без топора колоть дрова не выйдет. Сначала возьмите старый топор."
        $ CurLocDesc = MainTxt
        return
    if CurrentRoom is None:
        $ MainTxt = "Сейчас рубить дрова негде."
        $ CurLocDesc = MainTxt
        return
    if not _room_has_item_by_id(CurrentRoom, item_id) and not _player_has_item_by_id(item_id):
        $ MainTxt = "Колоть сейчас нечего. Сначала нужно принести бревен из леса."
        $ CurLocDesc = MainTxt
        return
    $ _chop_picture = "images/tavern/backyard/backyard_chop_woods.png"
    if renpy.loadable(_chop_picture):
        $ scene_image = _chop_picture
        $ _layout_last_picture = _chop_picture
        call ShowImage("", "", _chop_picture)
    python:
        _used_room_item = _room_has_item_by_id(CurrentRoom, item_id)
        if _used_room_item:
            _room_remove_item_by_id(CurrentRoom, item_id)
        else:
            player.remove_item(item_id)
        _room_add_item_units(CurrentRoom, "chopped_wood_001", 10)
        _chopped_item = get_game_item("chopped_wood_001", CurrentRoom)
        _chopped_total = _room_item_count_by_id(CurrentRoom, "chopped_wood_001")
        try:
            _pc_register_chore_success("chop_wood")
        except (AttributeError, NameError, TypeError, ValueError):
            pass
        calendar_v2.advance_minutes(60)
        update_stat_state()
        fun = _player_clamp(fun + 5, 0, 100)
        energy = _player_clamp(energy - 20, 0, 100)
        exploration = max(0, int(exploration or 0) + 15)
        ShedNoticeText = "Вы ставите бревно на колоду и рубите его на поленья. Из одного бревна выходит 10 охапок дров. В сарае теперь есть {}. Всего: {} охапок.".format(str(_chopped_item.name).strip(), _chopped_total)
        ShedNoticePending = True
    if _current_room_code == "Shed":
        $ MainTxt = build_shed_description(True, "")
        call ShedRoomActions
    else:
        $ MainTxt = str(ShedNoticeText or "")
    $ CurLocDesc = MainTxt
    call stat
    $ renpy.restart_interaction()
    return
