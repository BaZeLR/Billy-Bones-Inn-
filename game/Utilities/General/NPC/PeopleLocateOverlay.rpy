# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def people_locate_room_name(room_code=""):
        room_key = str(room_code or "").strip()
        if not room_key:
            return "неизвестно"
        try:
            room_obj = get_registered_room(room_key)
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
        try:
            if npc_social_actions_available_in_room(key, room_key):
                return "можно говорить"
        except Exception:
            pass
        try:
            if not npc_can_talk_now(key):
                return "занят(а) или спит"
        except Exception:
            pass
        try:
            if room_key and str(getLocation(key) or "") == room_key:
                return "на месте"
        except Exception:
            pass
        return "по расписанию"

    def people_locate_rows():
        people_sync_all()
        rows = []
        for person in people_known_ids():
            key = people_normalize_id(person)
            if key in ("you", "dog") or not key:
                continue
            info = getPersonInfo(key)
            try:
                loc = str(info.getLocation() if info is not None else getLocation(key) or "").strip()
            except Exception:
                loc = str(people_get_map("CurrentLoc").get(key, "") or "").strip()
            if not loc:
                loc = "неизвестно"
            rows.append({
                "id": key,
                "name": people_display_name(key),
                "location": loc,
                "location_name": people_locate_room_name(loc),
                "state": people_locate_state_text(key, loc),
                "can_jump": bool(loc and loc != "неизвестно" and renpy.has_label(loc)),
                "here": bool(str(CurLoc or "") == loc),
            })
        return sorted(rows, key=lambda row: (str(row.get("location_name", "")), str(row.get("name", ""))))

screen people_locate_overlay():
    use people_locate_panel(True)


screen people_locate_panel(standalone=False):
    modal True
    zorder 210

    on "show" action Function(people_sync_all)
    if standalone:
        key "K_ESCAPE" action Hide("people_locate_overlay")
    else:
        key "K_ESCAPE" action SetVariable("main_ui_overlay", "")

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
                    if standalone:
                        action Hide("people_locate_overlay")
                    else:
                        action SetVariable("main_ui_overlay", "")

            text "Локации берутся из того же getLocation(), что и иконки/действия NPC в комнатах." size 18 color "#b9b0a0"

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
                        $ _can_jump = bool(_row.get("can_jump", False))
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
                                if _can_jump:
                                    textbutton "Перейти":
                                        text_size 18
                                        if standalone:
                                            action [Hide("people_locate_overlay"), Jump(_loc)]
                                        else:
                                            action [SetVariable("main_ui_overlay", ""), Jump(_loc)]
                                else:
                                    text "нет перехода" size 17 color "#777777"
