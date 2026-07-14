# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default BlockTimeAdvance = 0

default BlockTimeAdvance = 0

default BlockTimeAdvance = 0

default BlockTimeAdvance = 0

default BlockTimeAdvance = 0

default BlockTimeAdvance = 0

init -115 python:
    import renpy.exports as renpy

    MOVEMENT_TIME_COST_MINUTES = 5

    def _turn_i(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _time_advancement_allowed():
        if str(CurLoc or "") == "Intro":
            return False
        if _turn_i(BlockTimeAdvance, 0) != 0:
            return False
        return True

    def navigation_has_saddled_horse():
        return bool(str(MyStallion or "").strip()) and _turn_i(HorseSaddled, 0) == 1

    def navigation_group_travel_minutes():
        return 15 if navigation_has_saddled_horse() else 30

    def _apply_movement_time_cost_without_sleep(minutes_to_add):
        current_minutes = _turn_i(clock_minutes, 0)
        target_minutes = current_minutes + max(0, _turn_i(minutes_to_add, 0))
        if target_minutes >= 1440:
            # Movement is never allowed to roll the calendar into the next day.
            calendar_v2.hour = 23
            calendar_v2.minute = 59
            return False
        calendar_v2.advance_minutes(max(0, _turn_i(minutes_to_add, 0)))
        return True

label AdvanceMovementTime(target_label="", movement_minutes=0):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    $ _movement_cost_minutes = int(movement_minutes or MOVEMENT_TIME_COST_MINUTES)
    $ current_object_id = ""
    $ current_girl_key = ""
    if _time_advancement_allowed():
        $ _movement_time_changed = _apply_movement_time_cost_without_sleep(_movement_cost_minutes)
        call stat
        if _movement_time_changed:
            $ checkpoint_tractir_progress("movement_time")
        python:
            try:
                _forest_dusk_fn = globals().get("forest_after_dusk", None)
                _forest_text_fn = globals().get("forest_after_dusk_return_text", None)
                if room_in_group(str(CurLoc or ""), ROOM_GROUP_FOREST) and callable(_forest_dusk_fn) and _forest_dusk_fn() and str(movement_target or "") != "StreetTavern":
                    movement_target = "StreetTavern"
                    if callable(_forest_text_fn):
                        MainTxt = _forest_text_fn()
                    else:
                        MainTxt = "Смеркается. Нужно возвращаться к трактиру."
                    CurLocDesc = MainTxt
            except Exception:
                pass
    if renpy.has_label(movement_target):
        jump expression movement_target
    jump TavernMain
