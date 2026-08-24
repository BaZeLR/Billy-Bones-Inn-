# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -115 python:
    import renpy.exports as renpy

    MOVEMENT_TIME_COST_MINUTES = 5

    def _turn_i(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _time_advancement_allowed():
        if str(rooms.current_code or "") == "Intro":
            return False
        if _turn_i(calendar_v2.time_advance_blocked, 0) != 0:
            return False
        return True

    def navigation_has_saddled_horse():
        return player.horse.owns_horse() and bool(player.horse.saddled)

    def navigation_group_travel_minutes():
        return 15 if navigation_has_saddled_horse() else 30

    def _apply_movement_time_cost_without_sleep(minutes_to_add):
        current_minutes = _turn_i(calendar_v2.clock_minutes(), 0)
        target_minutes = current_minutes + max(0, _turn_i(minutes_to_add, 0))
        if target_minutes >= 1440:
            # Movement is never allowed to roll the calendar into the next day.
            calendar_v2.hour = 23
            calendar_v2.minute = 59
            return False
        calendar_v2.advance_minutes(max(0, _turn_i(minutes_to_add, 0)))
        return True

    def movement_actions(target_label="", movement_minutes=0):
        destination = str(target_label or rooms.current_code or "TavernMain")
        movement_cost = int(movement_minutes or MOVEMENT_TIME_COST_MINUTES)
        if room_in_group(str(rooms.current_code or ""), ROOM_GROUP_FOREST) and forest_after_dusk() and destination != "StreetTavern":
            destination = "StreetTavern"
        return [Function(apply_movement_time, movement_cost, destination), Jump(destination)]

    def apply_movement_time(movement_minutes=0, destination=""):
        main_ui_runtime.object_id = ""
        main_ui_runtime.girl_key = ""
        if not _time_advancement_allowed():
            return
        _apply_movement_time_cost_without_sleep(int(movement_minutes or MOVEMENT_TIME_COST_MINUTES))
        if destination == "StreetTavern" and room_in_group(str(rooms.current_code or ""), ROOM_GROUP_FOREST) and forest_after_dusk():
            scene_runtime.text = forest_after_dusk_return_text()
            scene_runtime.location_text = scene_runtime.text
