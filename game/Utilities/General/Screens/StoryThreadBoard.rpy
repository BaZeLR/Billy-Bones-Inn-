# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default story_board_selected_person = "melissa"

init python:
    STORY_BOARD_PERSON_ORDER = [
        "melissa",
        "sandra",
        "clara",
        "mongol",
        "cityguard",
        "sherwood",
        "becky",
        "eddie",
        "irma",
        "church",
        "amanda",
        "liza",
        "georgett",
        "city",
    ]

    STORY_BOARD_TITLES = {
        "melissa": "Melissa",
        "sandra": "Sandra",
        "clara": "Clarissa",
        "mongol": "Mongol",
        "cityguard": "City guard",
        "sherwood": "Sherwood",
        "becky": "Becky",
        "eddie": "Eddie",
        "irma": "Irma",
        "church": "Church",
        "amanda": "Amanda",
        "liza": "Lizette",
        "georgett": "Georgette",
        "city": "Town life",
    }

    STORY_BOARD_COLORS = {
        "done": "#32c46a",
        "available": "#ffffff",
        "waiting": "#d7a925",
        "future": "#666666",
        "blocked": "#7c3aed",
        "aborted": "#d43f3f",
        "complete": "#1f9d55",
        "unknown": "#334155",
    }

    STORY_BOARD_TITLE_TEXT_SIZE = 24
    STORY_BOARD_LEGEND_TEXT_SIZE = 18
    STORY_BOARD_TAB_TEXT_SIZE = 18
    STORY_BOARD_SECTION_TEXT_SIZE = 18
    STORY_BOARD_ROW_TEXT_SIZE = 18
    STORY_BOARD_DETAIL_TEXT_SIZE = 18
    STORY_BOARD_CONTROL_TITLE_SIZE = 18
    STORY_BOARD_CELL_SIZE = 20

    def story_board_safe_text(value):
        return str(value or "").replace("[", "[[")

    def story_board_refresh():
        try:
            initStoryEventRuntime(True)
            findBlockedThreads(threads)
            findAvailableEvents(True)
        except Exception:
            pass

    def story_board_people():
        people = []
        try:
            for key, data_rows in dict(threadListsByGirl or {}).items():
                if list(data_rows or []):
                    people.append(str(key or ""))
        except Exception:
            pass
        try:
            for tinfo in list(dict(threads or {}).values()):
                person = str(getattr(getattr(tinfo, "data", None), "person", "") or "")
                if person and person not in people:
                    people.append(person)
        except Exception:
            pass
        order = list(STORY_BOARD_PERSON_ORDER)
        return sorted([row for row in people if row], key=lambda row: (order.index(row) if row in order else 999, row))

    def story_board_rows(person=""):
        key = str(person or "").strip()
        rows = []
        ordered_names = []
        try:
            for tdata in list(dict(threadListsByGirl or {}).get(key, []) or []):
                tname = str(getattr(tdata, "name", "") or "")
                if tname and tname not in ordered_names:
                    ordered_names.append(tname)
        except Exception:
            ordered_names = []
        try:
            for tname in ordered_names:
                if tname in dict(threads or {}):
                    rows.append((tname, dict(threads or {}).get(tname)))
        except Exception:
            rows = []
        try:
            for name, tinfo in sorted(dict(threads or {}).items()):
                if name in ordered_names:
                    continue
                if str(getattr(getattr(tinfo, "data", None), "person", "") or "") == key:
                    rows.append((name, tinfo))
        except Exception:
            pass
        return rows

    def story_board_projection_lines(limit=6):
        try:
            findAvailableEvents(True)
        except Exception:
            pass
        try:
            rows = list(story_event_projection_rows() or [])
        except Exception:
            rows = []
        if not rows:
            return ["No active projected story events for current time/location state."]
        out = []
        for row in rows[: max(1, int(limit or 6))]:
            person = str(row.get("person", "") or "")
            location_key = str(row.get("projected_location", row.get("location", "")) or "")
            action_key = str(row.get("action", "") or "")
            target = str(row.get("target", "") or "")
            first_step = str(row.get("first_step", "") or "")
            try:
                person_name = story_board_person_title(person) if person else "event"
            except Exception:
                person_name = person or "event"
            try:
                location_name = people_locate_room_name(location_key)
            except Exception:
                location_name = location_key
            route = " via %s" % first_step if first_step and first_step != location_key else ""
            missing = " missing %s" % str(row.get("item", "") or "") if bool(row.get("missing_item", False)) else ""
            out.append("%s: %s / %s -> %s%s%s" % (person_name, location_name, action_key, target, route, missing))
        if len(rows) > len(out):
            out.append("...and %d more." % (len(rows) - len(out)))
        return out

    def story_board_person_title(person=""):
        key = str(person or "").strip()
        if key in STORY_BOARD_TITLES:
            return STORY_BOARD_TITLES[key]
        try:
            return people_display_name(key)
        except Exception:
            try:
                return str(RealName.get(key, key) or key)
            except Exception:
                return key

    def story_board_thread_title(tinfo):
        data = getattr(tinfo, "data", None)
        if data is None:
            return ""
        subname = str(getattr(data, "subname", "") or "")
        person = story_board_person_title(str(getattr(data, "person", "") or ""))
        return "%s: %s" % (person, subname)

    def story_board_thread_status(tinfo):
        try:
            if bool(getattr(tinfo, "completed", False)):
                return "complete"
            if bool(getattr(tinfo, "aborted", False)):
                return "aborted"
            if bool(getattr(tinfo, "blocked", False)):
                return "blocked"
            if tinfo.checkActive():
                return "active"
        except Exception:
            pass
        return "future"

    def story_board_thread_color(tinfo):
        status = story_board_thread_status(tinfo)
        if status == "complete":
            return STORY_BOARD_COLORS["complete"]
        if status == "aborted":
            return STORY_BOARD_COLORS["aborted"]
        if status == "blocked":
            return STORY_BOARD_COLORS["blocked"]
        if status == "active":
            return STORY_BOARD_COLORS["available"]
        return STORY_BOARD_COLORS["future"]

    def story_board_event_available(tinfo, index):
        try:
            return any([evt.canTrigger(getattr(tinfo, "day", 0)) for evt in list(tinfo.data.triggers[index] or [])])
        except Exception:
            return False

    def story_board_event_status(tinfo, index):
        try:
            if index < len(tinfo.done) and bool(tinfo.done[index]):
                return "done"
            if bool(getattr(tinfo, "aborted", False)):
                return "aborted"
            if index < len(tinfo.blocks) and bool(tinfo.blocks[index]):
                return "blocked"
            if bool(getattr(tinfo, "completed", False)):
                return "done"
            if int(getattr(tinfo, "num", 0) or 0) == int(index or 0) and tinfo.checkActive():
                return "available" if story_board_event_available(tinfo, index) else "waiting"
            if int(index or 0) > int(getattr(tinfo, "num", 0) or 0):
                return "future"
            return "waiting"
        except Exception:
            return "unknown"

    def story_board_event_color(tinfo, index):
        return STORY_BOARD_COLORS.get(story_board_event_status(tinfo, index), STORY_BOARD_COLORS["unknown"])

    def story_board_colorize(msg, is_ok):
        return "{color=#%s}%s{/color}" % ("0f0" if is_ok else "f00", story_board_safe_text(msg))

    def story_board_show_target(target):
        fields = str(target or "").split("_")
        if len(fields) > 1:
            return story_board_safe_text(fields[0] + " " + fields[1])
        return story_board_safe_text(fields[0] if fields else "")

    def story_board_show_location(board_person, loc, action):
        loc = str(loc or "")
        action = str(action or "")
        lookup = {
            "enter": "Enter",
            "sleep": "Go to sleep",
            "overheard": "Overheard",
            "room_search": "Room search",
            "clara_paintings": "Clara paintings",
            "clara_talk": "Talk Clarissa",
            "clara_fiance": "Clarissa fiance",
            "_story_enter": "Enter",
        }
        if loc.startswith("menu_"):
            loc = loc[5:]
        if loc.startswith("talk"):
            person = action if loc == "talk" else loc[4:]
            if action != board_person and person:
                return "Talk " + story_board_person_title(person)
            return "Talk"
        if loc in lookup:
            return lookup[loc]
        if action in lookup:
            return "%s / %s" % (story_board_safe_text(loc), lookup[action])
        try:
            name = people_locate_room_name(loc)
            if name:
                return story_board_safe_text(name if not action else "%s / %s" % (name, action))
        except Exception:
            pass
        return story_board_safe_text(loc if not action else "%s / %s" % (loc, action))

    def story_board_show_min_date(evt_day, evt_num_day):
        if evt_day is None:
            return story_board_colorize("Available", True)
        if isinstance(evt_day, int):
            delta = int(evt_day)
        else:
            if isinstance(evt_day, tuple):
                evt_key, delta = evt_day
            else:
                evt_key, delta = evt_day, 1
            try:
                evt_num_day = threads[str(evt_key)[:-3]].day
            except Exception:
                try:
                    evt_num_day = globals()[str(evt_key)]
                except Exception:
                    evt_num_day = _story_num_day()
        wait_days = int(evt_num_day or 0) + int(delta or 0) - int(_story_num_day() or 0)
        if wait_days <= 0:
            return story_board_colorize("Available", True)
        if wait_days == 1:
            return story_board_colorize("Tomorrow", False)
        return story_board_colorize("Wait %d days" % wait_days, False)

    def story_board_show_day(evt_day):
        if evt_day is None:
            return "Any"
        if isinstance(evt_day, list):
            return ",".join([story_board_show_day(row) for row in evt_day])
        names = list(WEEKDAY_NAMES_RU) if "WEEKDAY_NAMES_RU" in globals() else ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        current_day = int(week or 0)
        if evt_day == (1, 5):
            return story_board_colorize("Weekday", current_day <= 5)
        if evt_day == (6, 7):
            return story_board_colorize("Weekend", current_day >= 6)
        if isinstance(evt_day, tuple):
            first = int(evt_day[0])
            last = int(evt_day[1])
            first_name = names[first - 1] if 1 <= first <= len(names) else str(first)
            last_name = names[last - 1] if 1 <= last <= len(names) else str(last)
            return story_board_colorize("%s-%s" % (first_name, last_name), first <= current_day <= last)
        try:
            day_index = int(evt_day)
            day_name = names[day_index - 1] if 1 <= day_index <= len(names) else str(evt_day)
            return story_board_colorize(day_name, current_day == day_index)
        except Exception:
            return story_board_safe_text(evt_day)

    def story_board_show_hour(evt_hour):
        if evt_hour is None:
            return "Any"
        current_hour = int(time or 0)
        def _slot_name(value):
            try:
                slot_info = TIME_SLOT_INFO.get(int(value), None) if "TIME_SLOT_INFO" in globals() else None
                if slot_info is not None:
                    return str(slot_info.get("name_ru", slot_info.get("name_en", value)) or value)
            except Exception:
                pass
            return str(value)
        if isinstance(evt_hour, list):
            return ",".join([story_board_show_hour(row) for row in evt_hour])
        if isinstance(evt_hour, tuple):
            return story_board_colorize("%s-%s" % (_slot_name(evt_hour[0]), _slot_name(evt_hour[1])), int(evt_hour[0]) <= current_hour <= int(evt_hour[1]))
        return story_board_colorize(_slot_name(evt_hour), current_hour == int(evt_hour))

    def story_board_show_item(item_id):
        if item_id is None:
            return "None"
        key = str(item_id or "")
        has_it = False
        try:
            has_it = _player_has_item_by_id(key)
        except Exception:
            pass
        try:
            item_obj = get_game_item(key)
            item_name = str(getattr(item_obj, "name", "") or key)
        except Exception:
            item_name = key
        return story_board_colorize(item_name, has_it)

    def story_board_show_stats(reqs):
        if reqs is None:
            return "None"
        msg = []
        for req, val in dict(reqs or {}).items():
            key = str(req or "")
            limit = int(val or 0)
            if key in peopleInfo:
                current = int(getattr(peopleInfo[key], "rel", 0) or 0)
                msg.append(story_board_colorize("%s Rel >= %d" % (story_board_person_title(key), limit), current >= limit))
            else:
                current = _story_named_number(key, 0)
                msg.append(story_board_colorize("%s >= %d" % (key, limit), current >= limit))
        return ", ".join(msg) if msg else "None"

    def story_board_show_conds(conds):
        if conds is None:
            return "None"
        rows = []
        for cond in list(conds or []):
            try:
                rows.append(cond.show())
            except Exception:
                rows.append(str(cond))
        if not rows:
            return "None"
        return story_board_safe_text(" and ".join(rows))

    def story_board_show_scene(tinfo, i):
        try:
            target = tinfo.getTarget(i)
        except Exception:
            return
        if not target:
            return
        try:
            renpy.hide_screen("story_event_screen")
            renpy.call_replay(target, {"thread": tinfo, "location": CurLoc})
        except Exception:
            pass

    def story_board_force_enable(thread_name=""):
        key = str(thread_name or "").strip()
        if key in threads:
            try:
                threads[key].forceEnable()
            except Exception:
                pass
        story_board_refresh()

    def story_board_abort(thread_name=""):
        key = str(thread_name or "").strip()
        if key in threads:
            try:
                threads[key].abort()
            except Exception:
                pass
        story_board_refresh()

    def story_board_reactivate(thread_name=""):
        key = str(thread_name or "").strip()
        if key in threads:
            try:
                threads[key].reactivate()
            except Exception:
                pass
        story_board_refresh()

    def story_board_reset(thread_name=""):
        key = str(thread_name or "").strip()
        if key in threads:
            try:
                threads[key].reset()
            except Exception:
                threads[key] = createThread(threads[key].data)
        story_board_refresh()


init -5:
    style scene is button
    style scene:
        xysize (20, 15)
        margin (5, 5, 5, 0)
        padding (0, 0)

    style board_text is default
    style board_text:
        size 16

    style event_text is default
    style event_text:
        size 20

    style board_button_text is button_text
    style board_button_text:
        size 24
        color "#444444"
        hover_color "#ffffff"
        selected_color "#cc9900"
        selected_hover_color "#ffffff"

    style threadmenu_button_text is button_text
    style threadmenu_button_text:
        size 20
        color "#cc9900"
        hover_color "#ffffff"

    style story_board_text is default
    style story_board_text:
        size 18

    style story_board_button_text is button_text
    style story_board_button_text:
        size 18
        color "#d6b35a"
        hover_color "#ffffff"
        selected_color "#ffffff"


screen story_thread_board(person=None):
    use story_thread_board_panel(person, True)


screen story_thread_board_panel(person=None, standalone=False):
    modal True
    zorder 210
    style_prefix "board"
    on "show" action Function(story_board_refresh)

    $ _people = story_board_people()
    if person is not None and person in _people:
        $ story_board_selected_person = person
    if story_board_selected_person not in _people and _people:
        $ story_board_selected_person = _people[0]
    $ person = story_board_selected_person
    $ _rows = story_board_rows(person)

    add Solid("#000000")

    textbutton "Help" action Show("story_board_help"):
        xalign 0.0
        yalign 0.0
        text_color "#00ff00"
        text_hover_color "#ffffff"

    textbutton "Back":
        xalign 1.0
        yalign 0.0
        text_color "#cc9900"
        text_hover_color "#ffffff"
        if standalone:
            action Hide("story_thread_board")
        else:
            action SetVariable("main_ui_overlay", "")

    vbox:
        spacing 5
        xpos 50
        ypos 50

        hbox:
            for _person in _people:
                textbutton story_board_person_title(_person):
                    selected (_person == person)
                    action [Hide("story_thread_board"), Show("story_thread_board", None, _person)]

        viewport:
            xsize 1760
            ysize 940
            draggable True
            mousewheel True

            vbox:
                spacing 5
                if not _rows:
                    text "No story threads registered for this person."
                $ _pos = 0
                for _thread_name, _tinfo in _rows:
                    hbox:
                        $ _offset = int(getattr(_tinfo.data, "level", 0) or 0)
                        use story_board_toggle_highlight(_tinfo)
                        textbutton story_board_thread_title(_tinfo) xsize 180 ysize 16:
                            text_color story_board_thread_color(_tinfo)
                            text_size 16
                            text_hover_color "#ffff00"
                            action Show("story_thread_control", None, _thread_name, _pos)
                            hovered Show("story_thread_screen", None, _tinfo)
                            unhovered Hide("story_thread_screen")
                        hbox:
                            xpos 20 * _offset
                            for _idx in range(len(_tinfo.data.triggers)):
                                button style "scene":
                                    idle_background Solid(story_board_event_color(_tinfo, _idx))
                                    hover_background Solid("#ffff00")
                                    action Function(story_board_show_scene, _tinfo, _idx)
                                    hovered Show("story_event_screen", None, _tinfo, _idx, _tinfo.getevent(_idx))
                                    unhovered Hide("story_event_screen")
                    $ _pos += 1


screen story_board_toggle_highlight(tinfo):
    textbutton ("[[x]" if getattr(tinfo, "highlight", False) else "[[ ]"):
        text_size 16
        xsize 40
        action ToggleField(tinfo, "highlight")


screen story_thread_screen(tinfo):
    style_prefix "event"
    zorder 211
    frame:
        xpos 920
        ypos 50
        background Solid("#000000")
        xsize 1000
        ysize 200
        vbox:
            text "Thread: " + tinfo.data.name
            text "Conditions: " + story_board_show_conds(tinfo.data.conds)


screen story_event_screen(tinfo, i, evt):
    style_prefix "event"
    zorder 211
    frame:
        xpos 920
        ypos 50
        background Solid("#000000")
        xsize 1000
        ysize 200
        vbox:
            hbox:
                spacing 20
                vbox:
                    xminimum 400
                    text "Event: " + story_board_show_target(evt.target)
                    text "Location: " + story_board_show_location(tinfo.data.person, evt.location, evt.action)
                    text "Item: " + story_board_show_item(evt.item)
                vbox:
                    text "Min.Date: " + story_board_show_min_date(evt.evtDay, tinfo.day)
                    text "Day: " + story_board_show_day(evt.day)
                    text "Hour: " + story_board_show_hour(evt.hour)
            text "Stats: " + story_board_show_stats(evt.reqs)
            text "Conditions: " + story_board_show_conds(evt.conds)
            if evt.prob is not None and evt.prob < 1:
                text "Random: %d%%" % int(evt.prob * 100)


screen story_event_detail(tinfo, event_index=0):
    use story_event_screen(tinfo, event_index, tinfo.getevent(event_index))


screen story_event_detail_panel(tinfo, event_index=0):
    use story_event_screen(tinfo, event_index, tinfo.getevent(event_index))


screen story_thread_control(thread_name="", pos=0):
    use story_thread_control_panel(thread_name, pos)


screen story_thread_control_panel(thread_name="", pos=0):
    style_prefix "threadmenu"
    modal True
    zorder 212
    $ _tinfo = threads.get(str(thread_name or ""), None) if isinstance(threads, dict) else None

    if _tinfo is not None:
        frame:
            background Solid("#000000")
            xpos 50
            ypos 80 + 21 * int(pos or 0)
            has vbox
            if _tinfo.blocked:
                textbutton "Force enabled [story_board_thread_title(_tinfo)]":
                    action [Function(story_board_force_enable, thread_name), Hide("story_thread_control")]
            if _tinfo.aborted:
                textbutton "Reactivate thread [story_board_thread_title(_tinfo)]":
                    action [Function(story_board_reactivate, thread_name), Hide("story_thread_control")]
            else:
                textbutton "Abort thread [story_board_thread_title(_tinfo)]":
                    action [Function(story_board_abort, thread_name), Hide("story_thread_control")]
            textbutton "Leave the thread status unchanged":
                action Hide("story_thread_control")


screen story_board_help():
    zorder 213
    modal True
    add Solid("#000000")
    textbutton "Back" action Hide("story_board_help"):
        xalign 0.0
        yalign 0.0
        text_size 24
        text_color "#cc9900"
        text_hover_color "#ffffff"
    vbox:
        xpos 50
        ypos 50
        xsize 1820
        spacing 10
        text "Threads are story lines. Each row is a thread, and each box is one event in that thread." size 24 color "#cc9900"
        text "Hover a thread name to see thread conditions. Hover an event box to see the event fields: target, location/action, item, minimum date, day, hour, stats, conditions, and random chance." size 24 color "#cc9900"
        text "Click a thread name to force, reactivate, or abort that thread. Click an event box to try replaying that event without changing current progress." size 24 color "#cc9900"
