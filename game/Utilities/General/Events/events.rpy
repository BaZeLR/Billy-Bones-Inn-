# ================================================================================
# Story event runtime.
# Owns Event objects, availability projection, and trigger entry labels.
# ================================================================================

init -25 python:
    import renpy.exports as renpy

    class Event(object):
        def __init__(self, evt, thread_name, threaded):
            self.target = evt[0]
            self.day = evt[1]
            self.hour = evt[2]
            self.evtDay = evt[3]
            self.prob = evt[4]
            self.reqs = evt[5]
            self.condStr = evt[6]
            self.item = evt[7]
            self.location = evt[8]
            self.action = evt[9]
            self.priority = evt[10]
            self.thread_name = thread_name
            self.threaded = threaded
            self.conds = []

        def initConditions(self):
            self.conds = makeConditions(self.condStr)

        def canTrigger(self, evtDay=0):
            if not bool(getattr(self, "repeatable", False)) and story_event_fired_today(self):
                return False
            if not self.checkDay():
                return False
            if not self.checkHour():
                return False
            if not self.checkConditions():
                return False
            if not self.checkNumDay(evtDay):
                return False
            if not self.checkReqs():
                return False
            if not self.checkProb():
                return False
            if not _story_location_is_open(self.location):
                return False
            return True

        def auditChecks(self, evtDay=0, include_item=True, roll_probability=False):
            rows = []

            def add(field, ok, detail=""):
                rows.append({
                    "field": str(field or ""),
                    "ok": bool(ok),
                    "detail": str(detail or ""),
                })

            target_key = str(self.target or "").strip()
            target_ok = bool(target_key and renpy.has_label(target_key))
            add("target", target_ok, target_key)

            location_key = str(self.location or "").strip()
            action_key = str(self.action or "").strip()
            add("binding", bool(location_key and action_key), "%s/%s" % (location_key or "-", action_key or "-"))
            add("day", self.checkDay(), str(self.day))
            add("hour", self.checkHour(), str(self.hour))
            add("delay", self.checkNumDay(evtDay), str(self.evtDay))
            add("requirements", self.checkReqs(), str(self.reqs))
            add("conditions", self.checkConditions(), str(self.condStr))
            if include_item:
                add("item", self.checkItem(), str(self.item or "None"))
            add("location_open", _story_location_is_open(self.location), location_key or "-")
            if self.prob in (None, 1, 1.0):
                add("probability", True, "100%")
            elif roll_probability:
                add("probability", self.checkProb(), str(self.prob))
            else:
                add("probability", True, "%d%% chance" % int(float(self.prob) * 100))
            return rows

        def checkDay(self):
            return checkEventTime(calendar_v2.week, self.day)

        def checkHour(self):
            return checkEventTime(calendar_v2.hour, self.hour)

        def checkNumDay(self, evt_numDay):
            return _story_delay_ready(self.evtDay, evt_numDay)

        def checkReqs(self):
            if self.reqs is None:
                return True
            roster = list(_story_named_value("AllGirlNames", []) or [])
            for stat, limit in dict(self.reqs).items():
                threshold = _story_to_int(limit, 0)
                person_info = people.get_info(stat) if stat in roster else None
                if person_info is not None:
                    current_value = _story_to_int(getattr(person_info, "rel", 0), 0)
                else:
                    current_value = _story_named_number(stat, 0)
                if threshold > 0 and current_value < threshold:
                    return False
                if threshold <= 0 and current_value >= -threshold:
                    return False
            return True

        def checkConditions(self):
            return _story_conditions_met(self.conds)

        def checkProb(self):
            probability = self.prob
            if probability in (None, 1, 1.0):
                return True
            return procedural_random(key="procedural:Utilities/General/Events/events.rpy:procedural_random:140:1") < float(probability)

        def checkItem(self):
            if not self.item:
                return True
            return player.item_count(self.item) > 0

        def checkBlocks(self):
            return _story_conditions_blocked(self.conds)

        def __str__(self):
            return "%s %s %s %s %s %s %s %s" % (
                str(self.target),
                str(self.day),
                str(self.hour),
                str(self.evtDay),
                str(self.prob),
                str(self.reqs),
                str(self.conds),
                str(self.item),
            )

    def story_event_day_key(evt):
        daily_key = str(getattr(evt, "daily_key", "") or "").strip()
        if daily_key:
            return daily_key
        return "%s:%s:%s" % (
            str(getattr(evt, "target", "") or "").strip(),
            str(getattr(evt, "location", "") or "").strip(),
            str(getattr(evt, "action", "") or "").strip(),
        )

    def story_event_reset_fired_today_if_needed():
        day_value = _story_num_day()
        fired_day_value = event_runtime.fired_day
        if int(fired_day_value if fired_day_value is not None else -1) != int(day_value):
            event_runtime.fired_day = int(day_value)
            event_runtime.fired_keys_today = []

    def story_event_fired_today(evt):
        story_event_reset_fired_today_if_needed()
        key = story_event_day_key(evt)
        return bool(key and key in list(event_runtime.fired_keys_today or []))

    def story_event_mark_fired_today(evt):
        story_event_reset_fired_today_if_needed()
        key = story_event_day_key(evt)
        if key and key not in event_runtime.fired_keys_today:
            event_runtime.fired_keys_today.append(key)

    def initEvents():
        for _name, tdata in dict(threadData or {}).items():
            for evt_list in list(tdata.triggers or []):
                for evt in list(evt_list or []):
                    evt.initConditions()

    def _story_event_person(evt):
        action_key = str(getattr(evt, "action", "") or "").strip()
        location_key = str(getattr(evt, "location", "") or "").strip()
        if action_key.endswith("_talk") and "_" in action_key:
            return action_key.rsplit("_", 1)[0].strip().lower()
        if location_key.startswith("talk_"):
            return location_key[5:].strip().lower()
        if location_key == "talk":
            return action_key.strip().lower()
        if location_key == "gift":
            return action_key.strip().lower()
        thread_name = str(getattr(evt, "thread_name", "") or "").strip()
        tinfo = dict(threads or {}).get(thread_name, None)
        data = getattr(tinfo, "data", None)
        person = str(getattr(data, "person", "") or "").strip().lower()
        if person and person not in ("event", "story", "system"):
            return person
        return ""

    def _story_person_location(person):
        key = str(person or "").strip().lower()
        if not key:
            return ""
        loc = people.location(key)
        if loc:
            return str(loc)
        return ""

    def _story_event_projection_location(evt):
        location_key = str(getattr(evt, "location", "") or "").strip()
        action_key = str(getattr(evt, "action", "") or "").strip()
        person_key = _story_event_person(evt)
        if location_key.startswith("talk_") or location_key in ("talk", "gift"):
            person_loc = _story_person_location(person_key)
            return person_loc or location_key
        if action_key.endswith("_talk") and person_key:
            person_loc = _story_person_location(person_key)
            if person_loc:
                return person_loc
        if location_key.startswith("menu_"):
            return location_key[5:]
        return location_key

    def _story_room_neighbors(room_code):
        room_key = str(room_code or "").strip()
        if not room_key:
            return []
        room_obj = rooms.get(room_key)
        if room_obj is None:
            return []
        out = []
        exits = list(room_obj.visible_exits())
        for exit_row in exits:
            target = str(getattr(exit_row, "target", "") or "").strip()
            if target and target not in out:
                out.append(target)
        return out

    def _story_first_route_step(start_location, target_location):
        start_key = str(start_location or "").strip()
        target_key = str(target_location or "").strip()
        if not start_key or not target_key or start_key == target_key:
            return ""
        visited = set([start_key])
        queue = [(start_key, [])]
        while queue:
            current, path = queue.pop(0)
            for neighbor in _story_room_neighbors(current):
                if neighbor in visited:
                    continue
                next_path = path + [neighbor]
                if neighbor == target_key:
                    return next_path[0] if next_path else target_key
                visited.add(neighbor)
                queue.append((neighbor, next_path))
        return target_key

    def _story_project_available_events():
        current_location = str(rooms.current_code or "").strip()
        event_runtime.locations = set()
        event_runtime.people = set()
        event_runtime.talk = set()
        event_runtime.options = set()
        event_runtime.items = set()
        event_runtime.paths = set()
        event_runtime.projection_rows = []
        event_runtime.route_hints = {}

        for raw_location, action_map in sorted(dict(event_runtime.available or {}).items()):
            for raw_action, evt in sorted(dict(action_map or {}).items()):
                if evt is None:
                    continue
                location_key = str(raw_location or "").strip()
                action_key = str(raw_action or "").strip()
                person_key = _story_event_person(evt)
                projected_location = _story_event_projection_location(evt)
                missing_item = bool(getattr(evt, "item", None) and not evt.checkItem())
                first_step = _story_first_route_step(current_location, projected_location)

                if projected_location:
                    event_runtime.locations.add(projected_location)
                    if first_step:
                        event_runtime.paths.add(first_step)
                        event_runtime.route_hints[projected_location] = first_step
                if person_key:
                    event_runtime.people.add(person_key)
                if location_key.startswith("talk_") or location_key == "talk" or action_key.endswith("_talk"):
                    if person_key:
                        event_runtime.talk.add(person_key)
                if action_key and action_key not in ("enter", "sleep"):
                    event_runtime.options.add(action_key)
                if missing_item:
                    event_runtime.items.add(str(getattr(evt, "item", "") or ""))

                event_runtime.projection_rows.append({
                    "thread": str(getattr(evt, "thread_name", "") or ""),
                    "target": str(getattr(evt, "target", "") or ""),
                    "person": person_key,
                    "location": location_key,
                    "projected_location": projected_location,
                    "action": action_key,
                    "item": str(getattr(evt, "item", "") or ""),
                    "missing_item": missing_item,
                    "first_step": first_step,
                    "priority": int(getattr(evt, "priority", 0) or 0),
                    "highlight": bool(getattr(dict(threads or {}).get(str(getattr(evt, "thread_name", "") or ""), None), "highlight", False)),
                })

    def story_event_projection_rows():
        findAvailableEvents(False)
        return list(event_runtime.projection_rows or [])

    def story_event_path_targets():
        findAvailableEvents(False)
        return set(event_runtime.paths or set())

    def story_event_location_has_signal(location_name=""):
        key = str(location_name or "").strip()
        if not key:
            return False
        findAvailableEvents(False)
        return key in set(event_runtime.locations or set()) or key in set(event_runtime.paths or set())

    def findAvailableEvents(forced=False):
        eval_key = (
            _story_num_day(),
            int(calendar_v2.week),
            int(calendar_v2.hour),
            int(calendar_v2.minute),
            str(rooms.current_code or ""),
        )
        if (not forced) and event_runtime.evaluation_time == eval_key:
            return
        event_runtime.evaluation_time = eval_key

        initEvents()

        tmp_events = []
        for _name, thread_info in dict(threads or {}).items():
            tmp_events.extend(thread_info.getAvailableEvents())

        event_runtime.available = {}
        for evt in tmp_events:
            location_key = str(evt.location or "").strip()
            action_key = str(evt.action or "").strip()
            if location_key == "" or action_key == "":
                continue
            if location_key not in event_runtime.available:
                event_runtime.available[location_key] = {action_key: [evt]}
            elif action_key not in event_runtime.available[location_key]:
                event_runtime.available[location_key][action_key] = [evt]
            else:
                event_runtime.available[location_key][action_key].append(evt)

        for location_name in list(event_runtime.available.keys()):
            for action_name in list(event_runtime.available[location_name].keys()):
                event_runtime.available[location_name][action_name].sort(key=lambda item: int(item.priority or 0))
                chosen = None
                for evt in event_runtime.available[location_name][action_name]:
                    if evt.checkItem():
                        chosen = evt
                        break
                if chosen is None and len(event_runtime.available[location_name][action_name]) > 0:
                    chosen = event_runtime.available[location_name][action_name][0]
                event_runtime.available[location_name][action_name] = chosen

        _story_project_available_events()

    def initStoryEventRuntime(force=False):
        initThreads()
        initEvents()
        findBlockedThreads(threads)
        findAvailableEvents(True if force else False)

    def _story_after_load_init():
        initStoryEventRuntime(True)

    if _story_after_load_init not in config.after_load_callbacks:
        config.after_load_callbacks.append(_story_after_load_init)


init python:
    def story_event_action_caption(evt):
        action_key = str(getattr(evt, "action", "") or "").strip()
        location_key = str(getattr(evt, "location", "") or "").strip()
        person_key = _story_event_person(evt)

        if action_key == "clara_paintings":
            return "Поговорить о рисунках"
        if action_key == "melissa_bats":
            if location_key == "TavernAtic":
                return "Проверить шумы на чердаке"
            if location_key == "TavernAmandaRoom":
                return "Осмотреть рисунки Мелиссы"
            return "Поговорить о летучих мышах"
        if action_key == "street_clients":
            return "Пойти проверить подворотню"
        if action_key == "after_cermon_walk":
            return "Обойти храм после службы"
        if action_key == "dress_change":
            return "Поговорить об одежде"
        if action_key == "amanda_grope":
            return "Подойти к Аманде"
        if action_key == "sandra_night_thanks":
            return "Принять ночную благодарность Сандры"
        if person_key:
            person_info = people.get_info(person_key)
            person_name = str(getattr(person_info, "name", "") or person_key)
            if action_key.endswith("_talk"):
                return "Поговорить с %s" % person_name
            return "%s: %s" % (person_name, action_key.replace("_", " "))
        return action_key.replace("_", " ").strip().capitalize()

    def story_event_action_items(location_name="", excluded_actions=None):
        location_key = str(location_name or "").strip()
        if not location_key:
            return []
        findAvailableEvents(False)
        action_map = dict(event_runtime.available.get(location_key, {}) or {})
        if not action_map:
            return []

        excluded = set(str(row or "").strip() for row in list(excluded_actions or []) if str(row or "").strip())
        items = []
        for action_key in sorted(action_map.keys()):
            action_name = str(action_key or "").strip()
            if not action_name or action_name in ("enter", "sleep") or action_name in excluded:
                continue
            evt = action_map.get(action_name, None)
            if evt is None:
                continue
            caption = story_event_action_caption(evt)
            if not str(caption or "").strip():
                continue
            items.append(MenuItem(str(caption), Call("checkTriggers", location_key, action_name, 0)))
        return items

    def story_event_available(location_name="", action_name=""):
        location_key = str(location_name or "").strip()
        action_key = str(action_name or "").strip()
        if location_key == "" or action_key == "":
            return False
        # Authored labels can change event conditions without advancing
        # the calendar or changing rooms.current_code. A direct query must inspect
        # that current state instead of the passive HUD projection cache.
        findAvailableEvents(True)
        return (
            isinstance(event_runtime.available, dict)
            and location_key in event_runtime.available
            and action_key in dict(event_runtime.available.get(location_key, {}) or {})
            and event_runtime.available[location_key].get(action_key, None) is not None
        )

    def story_thread_advance_current():
        current_thread = event_runtime.active_thread
        if current_thread is not None:
            current_thread.advance()
        event_runtime.evaluation_time = None
        findAvailableEvents(True)

label before_main_menu:
    $ initStoryEventRuntime(True)
    return


label checkTriggers(location, action, numpop=0):
    $ renpy.dynamic("_story_location", "_story_action", "evt")
    $ _story_location = str(location or "").strip()
    $ _story_action = str(action or "").strip()
    $ findAvailableEvents(False)
    if _story_location not in event_runtime.available:
        return False
    if _story_action not in event_runtime.available[_story_location]:
        return False
    $ evt = event_runtime.available[_story_location][_story_action]
    if evt is None or not evt.target:
        return False
    if evt.item and not evt.checkItem():
        return False
    $ story_event_mark_fired_today(evt)
    if numpop == 2:
        $ renpy.pop_call()
    elif numpop == 1:
        $ renpy.pop_call()
    call preEvent(evt.thread_name if evt.threaded else None)
    if str(rooms.current_code or "") != "Intro":
        show screen main_ui
    jump expression evt.target


label preEvent(thread_name=None):
    $ event_runtime.evaluation_time = None
    if thread_name:
        if thread_name in threads:
            $ event_runtime.active_thread = threads[thread_name]
            $ event_runtime.active_thread.setDay()
        else:
            $ event_runtime.active_thread = None
    else:
        $ event_runtime.active_thread = None
    return
