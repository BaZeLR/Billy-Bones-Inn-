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

    STORY_BOARD_TARGET_TITLES = {
        "story_clara_market_booklet_0": "Clarissa market booklet: first sighting",
        "story_clara_market_booklet_2": "Clarissa market booklet: evening market",
        "story_clara_market_booklet_3": "Clarissa market booklet: Mongol deal",
        "story_clara_market_booklet_4": "Clarissa market booklet: confession",
        "story_clara_market_booklet_5": "Clarissa market booklet: arrest rumor",
        "story_clara_market_booklet_6": "Clarissa market booklet: stocks",
        "story_clara_market_booklet_7": "Clarissa market booklet: feed Mongol",
        "story_clara_market_booklet_8": "Clarissa market booklet: lockpicks",
        "story_clara_market_booklet_9": "Clarissa market booklet: release plan",
        "story_clara_tavern_visit_bar_0": "Clarissa tavern visit: jokes at the bar",
        "story_clara_tavern_visit_bar_1": "Clarissa tavern visit: after attic fall",
        "story_clara_tavern_visit_bar_2": "Clarissa tavern visit: almost caught",
        "story_clara_melissa_room_visit_0": "Clarissa and Melissa room: pillow fight",
        "story_clara_melissa_room_visit_1": "Clarissa and Melissa room: drawings",
        "story_clara_melissa_room_visit_2": "Clarissa and Melissa room: private doodles",
        "story_georgett_church_service_bench": "Georgette church: quiet bench",
        "story_georgett_church_service_doggy": "Georgette church: risky service",
        "story_georgett_church_service_with_liza": "Georgette church: Liza witnesses",
        "story_georgett_church_after_sermon": "Georgette church: after-sermon spy scene",
        "story_liza_church_after_sermon": "Lizette church: after-sermon scene",
        "story_becky_church_after_sermon": "Becky church: after-sermon confession",
    }

    STORY_BOARD_ACTION_TITLES = {
        "clara_tavern_visit": "Clarissa tavern visit",
        "clara_room_visit": "Clarissa visits Melissa room",
        "georgett_church_service_bench": "Georgette church / quiet place",
        "georgett_church_service_doggy": "Georgette church / right here",
        "georgett_church_service_with_liza": "Georgette church / with Lizette",
        "after_cermon_walk": "After-sermon walk",
        "street_clients": "Port street clients",
    }

    STORY_BOARD_TARGET_FILES = {
        "story_clara_market_booklet_0": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_market_booklet_2": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_market_booklet_3": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_market_booklet_4": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_market_booklet_5": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_market_booklet_6": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_market_booklet_7": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_market_booklet_8": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_market_booklet_9": "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
        "story_clara_tavern_visit_bar_0": "game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy",
        "story_clara_tavern_visit_bar_1": "game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy",
        "story_clara_tavern_visit_bar_2": "game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy",
        "story_clara_melissa_room_visit_0": "game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy",
        "story_clara_melissa_room_visit_1": "game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy",
        "story_clara_melissa_room_visit_2": "game/NPC/Girls/Clara/ClaraTavernVisitThread.rpy",
        "story_georgett_church_service_bench": "game/NPC/Girls/Georgett/InitGeorgettChurch.rpy",
        "story_georgett_church_service_doggy": "game/NPC/Girls/Georgett/InitGeorgettChurch.rpy",
        "story_georgett_church_service_with_liza": "game/NPC/Girls/Georgett/InitGeorgettChurch.rpy",
        "story_georgett_church_after_sermon": "game/NPC/Girls/Georgett/IntGeorgettAfterCermon.rpy",
        "story_liza_church_after_sermon": "game/NPC/Girls/Liza/IntLizettAfterCermon.rpy",
        "story_georgett_portstreet_clients": "game/NPC/Girls/Georgett/GeorgettEvents.rpy",
        "story_liza_portstreet_clients": "game/NPC/Girls/Liza/LizaEvents.rpy",
        "story_becky_church_after_sermon": "game/NPC/Girls/Becky/IntBeckyAfterCermon.rpy",
    }

    STORY_BOARD_COLORS = {
        "done": "#32c46a",
        "active": "#38bdf8",
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
            return STORY_BOARD_COLORS["active"]
        return STORY_BOARD_COLORS["future"]

    def story_board_thread_status_label(tinfo):
        status = story_board_thread_status(tinfo)
        labels = {
            "active": "Active",
            "complete": "Complete",
            "aborted": "Aborted",
            "blocked": "Blocked",
            "future": "Future",
        }
        return labels.get(status, "Unknown")

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
        key = str(target or "")
        if key in STORY_BOARD_TARGET_TITLES:
            return story_board_safe_text(STORY_BOARD_TARGET_TITLES[key])
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
            "clara_tavern_visit": "Clara tavern visit",
            "clara_room_visit": "Clara visits Melissa room",
            "clara_talk": "Talk Clarissa",
            "clara_fiance": "Clarissa fiance",
            "_story_enter": "Enter",
        }
        if action in STORY_BOARD_ACTION_TITLES:
            try:
                name = people_locate_room_name(loc)
            except Exception:
                name = loc
            return story_board_safe_text("%s / %s" % (name or loc, STORY_BOARD_ACTION_TITLES[action]))
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
        current_hour = int(hour or 0)
        def _hour_name(value):
            try:
                return "%02d:00" % (int(value) % 24)
            except Exception:
                return str(value)
        def _hour_range_ok(first, last):
            first_i = int(first)
            last_i = int(last)
            if first_i <= last_i:
                return first_i <= current_hour <= last_i
            return current_hour >= first_i or current_hour <= last_i
        if isinstance(evt_hour, list):
            return ",".join([story_board_show_hour(row) for row in evt_hour])
        if isinstance(evt_hour, tuple):
            return story_board_colorize("%s-%s" % (_hour_name(evt_hour[0]), _hour_name(evt_hour[1])), _hour_range_ok(evt_hour[0], evt_hour[1]))
        return story_board_colorize(_hour_name(evt_hour), current_hour == int(evt_hour))

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
        return " and ".join(story_board_condition_lines(conds))

    def story_board_condition_lines(conds):
        if conds is None:
            return ["None"]
        rows = []
        for cond in list(conds or []):
            try:
                rows.append(str(cond.show()).replace("[", "[["))
            except Exception:
                rows.append(story_board_safe_text(cond))
        if not rows:
            return ["None"]
        return rows

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
                            action NullAction()
                            hovered Show("story_thread_screen", None, _tinfo)
                            unhovered Hide("story_thread_screen")
                        hbox:
                            xpos 20 * _offset
                            for _idx in range(len(_tinfo.data.triggers)):
                                button style "scene":
                                    idle_background Solid(story_board_event_color(_tinfo, _idx))
                                    hover_background Solid("#ffff00")
                                    action NullAction()
                                    hovered Show("story_event_screen", None, _tinfo, _idx, _tinfo.getevent(_idx))
                                    unhovered Hide("story_event_screen")
                    $ _pos += 1


screen story_board_toggle_highlight(tinfo):
    text ("[[x]" if getattr(tinfo, "highlight", False) else "[[ ]") size 16 xsize 40


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
            text "Status: " + story_board_thread_status_label(tinfo) color story_board_thread_color(tinfo)
            text "Conditions:"
            for _cond_line in story_board_condition_lines(tinfo.data.conds):
                text _cond_line


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
                    text "Label: " + story_board_safe_text(evt.target)
                    text "Action: " + story_board_safe_text(evt.action)
                    if evt.target in STORY_BOARD_TARGET_FILES:
                        text "File: " + STORY_BOARD_TARGET_FILES[evt.target]
                vbox:
                    text "Min.Date: " + story_board_show_min_date(evt.evtDay, tinfo.day)
                    text "Day: " + story_board_show_day(evt.day)
                    text "Hour: " + story_board_show_hour(evt.hour)
            text "Stats: " + story_board_show_stats(evt.reqs)
            text "Conditions:"
            for _cond_line in story_board_condition_lines(evt.conds):
                text _cond_line
            if evt.prob is not None and evt.prob < 1:
                text "Random: %d%%" % int(evt.prob * 100)


screen story_event_detail(tinfo, event_index=0):
    use story_event_screen(tinfo, event_index, tinfo.getevent(event_index))


screen story_event_detail_panel(tinfo, event_index=0):
    use story_event_screen(tinfo, event_index, tinfo.getevent(event_index))


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
        text "Thread colors: active blue, complete green, blocked purple, aborted red, future gray. Event boxes: available white, waiting gold, done green." size 24 color "#cc9900"
