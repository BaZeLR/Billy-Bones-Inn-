# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    def old_axe_in_shed(_obj=None):
        return rooms.current is not None and str(getattr(rooms.current, "code_name", "") or "") == "Shed" and _room_has_item_by_id(rooms.current, "old_axe_001")

    def old_axe_player_has(_obj=None):
        return player.item_count("old_axe_001") > 0

    def old_axe_can_equip(_obj=None):
        return old_axe_player_has(_obj) and not player_has_equipped_weapon("old_axe_001")

    def old_axe_can_unequip(_obj=None):
        return old_axe_player_has(_obj) and player_has_equipped_weapon("old_axe_001")

    def old_axe_can_drop_to_shed(_obj=None):
        return old_axe_player_has(_obj) and str(rooms.current_code or "") == "Shed"

    def old_axe_can_chop_lumber(_obj=None):
        return old_axe_player_has(_obj) and rooms.current is not None and str(getattr(rooms.current, "code_name", "") or "") == "Shed" and _room_has_item_by_id(rooms.current, "lumber_001")

    OldAxeItem = GameItem(
        object_id="old_axe_001",
        name="старый топор",
        description="Старый, но еще годный топор для рубки и колки дров.",
        actions=[
            ObjectAction(action_id="take_old_axe", label="Взять топор", hook="call", target="OldAxeTake", condition=old_axe_in_shed),
            ObjectAction(action_id="equip_old_axe", label="Заткнуть топор за пояс", hook="call", target="OldAxeEquip", condition=old_axe_can_equip),
            ObjectAction(action_id="unequip_old_axe", label="Убрать топор в сумку", hook="call", target="OldAxeUnequip", condition=old_axe_can_unequip),
            ObjectAction(action_id="drop_old_axe", label="Повесить топор на место", hook="call", target="OldAxeDropToShed", condition=old_axe_can_drop_to_shed),
            ObjectAction(action_id="chop_lumber_with_old_axe", label="Колоть дрова", hook="call", target="Chop", args=("lumber_001", "Shed", "", "lumber_001"), condition=old_axe_can_chop_lumber),
        ],
        price=12,
        carriable=True,
        usable=True,
        weapon=True,
        state={
            "visible": 1,
            "curLoc": "Shed",
        },
        custom_properties={
            "item_kind": "weapon",
            "tool_kind": "axe",
            "weapon_kind": "axe",
            "attack_points": 10,
            "speed_penalty": 1,
            "curLoc": "Shed",
        },
    )


label OldAxeTake:
    if rooms.current is None or str(getattr(rooms.current, "code_name", "") or "") != "Shed" or not _room_has_item_by_id(rooms.current, "old_axe_001"):
        $ scene_runtime.text = "Здесь уже нет старого топора."
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ _room_remove_item_by_id(rooms.current, "old_axe_001")
    $ player.add_item("old_axe_001", 1)
    $ rooms.get("Shed").state["notice_text"] = "Вы сняли со стены старый топор и забрали его с собой."
    $ rooms.get("Shed").state["notice_pending"] = True
    $ scene_runtime.text = build_shed_description(True, "")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = build_shed_action_items()
    call stat
    return


label OldAxeEquip:
    if player.item_count("old_axe_001") <= 0:
        $ scene_runtime.text = "Старого топора у вас нет."
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ player.equip("old_axe_001", "weapon")
    $ scene_runtime.text = "Вы заткнули старый топор за пояс."
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    if str(rooms.current_code or "") == "Shed":
        $ main_ui_runtime.action_items = build_shed_action_items()
    else:
        call PlayerCardInventoryItemMenu("old_axe_001", True)
    return


label OldAxeUnequip:
    if player.item_count("old_axe_001") <= 0:
        $ scene_runtime.text = "Старого топора у вас нет."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if player_has_equipped_weapon("old_axe_001"):
        $ player.unequip("weapon")
        $ scene_runtime.text = "Вы убрали старый топор в сумку."
    else:
        $ scene_runtime.text = "Топор и так лежит в сумке."
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    if str(rooms.current_code or "") == "Shed":
        $ main_ui_runtime.action_items = build_shed_action_items()
    else:
        call PlayerCardInventoryItemMenu("old_axe_001", True)
    return


label OldAxeDropToShed:
    if str(rooms.current_code or "") != "Shed" or rooms.current is None:
        $ scene_runtime.text = "Повесить топор на место можно только в сарае."
        $ scene_runtime.location_text = scene_runtime.text
        call PlayerCardInventoryItemMenu("old_axe_001", True)
        return
    if player.item_count("old_axe_001") <= 0:
        $ scene_runtime.text = "Старого топора у вас нет."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = build_shed_action_items()
        return
    if player_has_equipped_weapon("old_axe_001"):
        $ player.unequip("weapon")
    $ player.remove_item("old_axe_001", 1)
    if not _room_has_item_by_id(rooms.current, "old_axe_001"):
        $ _room_add_item_by_id(rooms.current, "old_axe_001")
    else:
        $ player.add_item("old_axe_001", 1)
    $ rooms.get("Shed").state["notice_text"] = "Вы повесили старый топор обратно на его место."
    $ rooms.get("Shed").state["notice_pending"] = True
    $ scene_runtime.text = build_shed_description(True, "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    $ main_ui_runtime.action_items = build_shed_action_items()
    call stat
    return
