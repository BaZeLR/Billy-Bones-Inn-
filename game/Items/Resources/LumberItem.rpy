# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    def lumber_in_shed(_obj=None):
        return rooms.current is not None and str(getattr(rooms.current, "code_name", "") or "") == "Shed" and _room_has_item_by_id(rooms.current, "lumber_001")

    def lumber_ready_for_chop(_obj=None):
        return lumber_in_shed(_obj) and player.item_count("old_axe_001") > 0

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
    $ renpy.dynamic("_chop_block", "item_id", "_current_room_code", "_chop_picture", "_chopped_item", "_chopped_total", "_used_room_item")
    $ _chop_block = action_restriction_result("heavy_chore", "chop")
    if not _chop_block.get("ok", False):
        $ scene_runtime.text = str(_chop_block.get("text", "") or fallback_text or "Сейчас это не получится.")
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ item_id = get_object_id(what_id)
    $ _current_room_code = str(getattr(rooms.current, "code_name", "") or rooms.current_code or "")
    if item_id == "":
        $ scene_runtime.text = "Непонятно, что именно вы собираетесь рубить."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if player.item_count("old_axe_001") <= 0:
        $ scene_runtime.text = "Без топора колоть дрова не выйдет. Сначала возьмите старый топор."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if rooms.current is None:
        $ scene_runtime.text = "Сейчас рубить дрова негде."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if not _room_has_item_by_id(rooms.current, item_id) and player.item_count(item_id) <= 0:
        $ scene_runtime.text = "Колоть сейчас нечего. Сначала нужно принести бревен из леса."
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ _chop_picture = "images/tavern/backyard/backyard_chop_woods.png"
    if renpy.loadable(_chop_picture):
        $ scene_runtime.picture = _chop_picture
        call ShowImage("", "", _chop_picture)
    python:
        _used_room_item = _room_has_item_by_id(rooms.current, item_id)
        if _used_room_item:
            _room_remove_item_by_id(rooms.current, item_id)
        else:
            player.remove_item(item_id)
        _room_add_item_units(rooms.current, "chopped_wood_001", 10)
        _chopped_item = get_game_item("chopped_wood_001", rooms.current)
        _chopped_total = _room_item_count_by_id(rooms.current, "chopped_wood_001")
        try:
            _pc_register_chore_success("chop_wood")
        except (AttributeError, NameError, TypeError, ValueError):
            pass
        calendar_v2.advance_minutes(60)
        update_stat_state()
        player.change_stat("fun", 5)
        player.change_stat("energy", -20)
        player.change_stat("exploration", 15)
        rooms.get("Shed").state["notice_text"] = "Вы ставите бревно на колоду и рубите его на поленья. Из одного бревна выходит 10 охапок дров. В сарае теперь есть {}. Всего: {} охапок.".format(str(_chopped_item.name).strip(), _chopped_total)
        rooms.get("Shed").state["notice_pending"] = True
    if _current_room_code == "Shed":
        $ scene_runtime.text = build_shed_description(True, "")
        $ main_ui_runtime.action_items = build_shed_action_items()
    else:
        $ scene_runtime.text = str(rooms.get("Shed").state.get("notice_text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    $ renpy.restart_interaction()
    return
