# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def people_locate_room_name(room_code=""):
        room_key = str(room_code or "").strip()
        if not room_key:
            return "неизвестно"
        try:
            room_obj = rooms.get(room_key)
            if room_obj is not None:
                title = str(getattr(room_obj, "display_name", "") or "").strip()
                if title:
                    return title
        except Exception:
            pass
        return room_key

    def people_locate_state_text(person="", room_code=""):
        key = people_normalize_id(person)
        room_key = str(room_code or "").strip()
        if not key:
            return ""
        info = people.get_info(key)
        if info is not None and info.talk_available_in_room(room_key):
            return "можно говорить"
        try:
            if not people.can_talk(key):
                return "занят(а) или спит"
        except Exception:
            pass
        try:
            if room_key and str(people.location(key) or "") == room_key:
                return "на месте"
        except Exception:
            pass
        return "по расписанию"

    def people_locate_rows():
        rows = []
        for person in people.ids():
            key = people_normalize_id(person)
            if key in ("you", "dog") or not key:
                continue
            info = people.get_info(key)
            try:
                loc = str(info.getLocation() if info is not None else people.location(key) or "").strip()
            except Exception:
                loc = ""
            rows.append({
                "id": key,
                "name": people_display_name(key),
                "location": loc,
                "location_name": people_locate_room_name(loc) if loc else "неизвестно",
                "state": people_locate_state_text(key, loc),
                "here": bool(str(rooms.current_code or "") == loc),
            })
        return sorted(rows, key=lambda row: (str(row.get("location_name", "")), str(row.get("name", ""))))

screen people_locate_panel():
    modal True
    zorder 210

    key "K_ESCAPE" action SetField(main_ui_runtime, "overlay", "")

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize min(980, int(config.screen_width * 0.82))
        ysize min(760, int(config.screen_height * 0.82))
        padding (18, 16)
        background "#080808f2"

        vbox:
            spacing 12
            xfill True
            yfill True

            hbox:
                xfill True
                text "Где кто находится" size 28 bold True color "#f0e6d2"
                null width 20
                textbutton "Закрыть":
                    xalign 1.0
                    text_size 20
                    action SetField(main_ui_runtime, "overlay", "")

            text "Локации берутся из того же people.location(), что и иконки/действия NPC в комнатах." size 18 color "#b9b0a0"

            viewport:
                mousewheel True
                draggable True
                yfill True
                xfill True

                vbox:
                    spacing 6
                    xfill True

                    for _row in people_locate_rows():
                        $ _person = str(_row.get("id", "") or "")
                        $ _name = str(_row.get("name", "") or _person)
                        $ _loc = str(_row.get("location", "") or "")
                        $ _loc_name = str(_row.get("location_name", "") or _loc)
                        $ _state = str(_row.get("state", "") or "")
                        $ _here = bool(_row.get("here", False))
                        $ _row_bg = "#21301f" if _here else "#171717"

                        frame:
                            xfill True
                            padding (10, 8)
                            background _row_bg

                            hbox:
                                spacing 12
                                xfill True
                                text _name size 21 color "#f0e6d2" xsize 210
                                text _loc_name size 20 color "#d6c8ad" xsize 260
                                text _state size 18 color "#aeb8a5" xsize 180
                                if _here:
                                    text "здесь" size 18 color "#9adf8f" xminimum 70
                                else:
                                    null width 70
                                text "расписание" size 17 color "#777777"
