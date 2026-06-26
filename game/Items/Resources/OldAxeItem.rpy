# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    def old_axe_in_shed(_obj=None):
        return CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "Shed" and _room_has_item_by_id(CurrentRoom, "old_axe_001")

    def old_axe_player_has(_obj=None):
        return _player_has_item_by_id("old_axe_001")

    def old_axe_can_equip(_obj=None):
        return old_axe_player_has(_obj) and not player_has_equipped_weapon("old_axe_001")

    def old_axe_can_unequip(_obj=None):
        return old_axe_player_has(_obj) and player_has_equipped_weapon("old_axe_001")

    def old_axe_can_drop_to_shed(_obj=None):
        return old_axe_player_has(_obj) and str(CurLoc or "") == "Shed"

    def old_axe_can_chop_lumber(_obj=None):
        return old_axe_player_has(_obj) and CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "Shed" and _room_has_item_by_id(CurrentRoom, "lumber_001")

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
    if CurrentRoom is None or str(getattr(CurrentRoom, "code_name", "") or "") != "Shed" or not _room_has_item_by_id(CurrentRoom, "old_axe_001"):
        $ MainTxt = "Здесь уже нет старого топора."
        $ CurLocDesc = MainTxt
        return
    $ _room_remove_item_by_id(CurrentRoom, "old_axe_001")
    $ _player_add_item_by_id("old_axe_001", 1)
    $ ShedNoticeText = "Вы сняли со стены старый топор и забрали его с собой."
    $ ShedNoticePending = True
    $ MainTxt = build_shed_description(True, "")
    $ CurLocDesc = MainTxt
    call ShedRoomActions
    call stat
    return


label OldAxeEquip:
    if not _player_has_item_by_id("old_axe_001"):
        $ MainTxt = "Старого топора у вас нет."
        $ CurLocDesc = MainTxt
        return
    $ player_state().equip("old_axe_001", "weapon")
    $ MainTxt = "Вы заткнули старый топор за пояс."
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    if str(CurLoc or "") == "Shed":
        call ShedRoomActions
    else:
        call PlayerCardInventoryItemMenu("old_axe_001", True)
    return


label OldAxeUnequip:
    if not _player_has_item_by_id("old_axe_001"):
        $ MainTxt = "Старого топора у вас нет."
        $ CurLocDesc = MainTxt
        return
    if player_has_equipped_weapon("old_axe_001"):
        $ player_state().unequip("weapon")
        $ MainTxt = "Вы убрали старый топор в сумку."
    else:
        $ MainTxt = "Топор и так лежит в сумке."
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    if str(CurLoc or "") == "Shed":
        call ShedRoomActions
    else:
        call PlayerCardInventoryItemMenu("old_axe_001", True)
    return


label OldAxeDropToShed:
    if str(CurLoc or "") != "Shed" or CurrentRoom is None:
        $ MainTxt = "Повесить топор на место можно только в сарае."
        $ CurLocDesc = MainTxt
        call PlayerCardInventoryItemMenu("old_axe_001", True)
        return
    if not _player_has_item_by_id("old_axe_001"):
        $ MainTxt = "Старого топора у вас нет."
        $ CurLocDesc = MainTxt
        call ShedRoomActions
        return
    if player_has_equipped_weapon("old_axe_001"):
        $ player_state().unequip("weapon")
    $ _player_remove_item_by_id("old_axe_001", 1)
    if not _room_has_item_by_id(CurrentRoom, "old_axe_001"):
        $ _room_add_item_by_id(CurrentRoom, "old_axe_001")
    else:
        $ _player_add_item_by_id("old_axe_001", 1)
    $ ShedNoticeText = "Вы повесили старый топор обратно на его место."
    $ ShedNoticePending = True
    $ MainTxt = build_shed_description(True, "")
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    call ShedRoomActions
    call stat
    return
