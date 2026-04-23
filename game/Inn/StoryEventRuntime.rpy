default dayspassed = 0

default active_event = None
default random_events = []
default story_events = []
default tavern_work_events = []

default availEvents = {}
default evalTime = None
default thread = None
default eventLocations = set()
default eventPeople = set()
default eventTalk = set()
default eventOptions = set()
default eventItems = set()
default story_thread_levels = {}
default amanda_story_pending = ""

init -25 python:
    import builtins
    import renpy.exports as renpy
    _story_range_type = type(builtins.range(0))

    def _story_get(name, default=None):
        key = str(name or "").strip()
        if key == "":
            return default
        try:
            return globals()[key]
        except Exception:
            return default

    def _story_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def _story_num_day():
        return _story_to_int(_story_get("dayspassed", 0), 0)

    def _story_named_value(name, default=None):
        return _story_get(name, default)

    def _story_named_number(name, default=0):
        return _story_to_int(_story_named_value(name, default), default)

    def _story_named_callable(name):
        value = _story_named_value(name, None)
        return value if callable(value) else None

    def _story_condition_scope():
        scope = {}
        for key, value in dict(globals()).items():
            if str(key or "").startswith("_"):
                continue
            scope[key] = value
        return scope

    def _story_level_enabled(level):
        levels_map = _story_named_value("story_thread_levels", {})
        if not isinstance(levels_map, dict):
            return True
        return bool(levels_map.get(level, True))

    def _story_location_is_open(location_name):
        location_key = str(location_name or "").strip()
        if location_key == "":
            return True
        is_open_fn = _story_named_callable("isOpen")
        if callable(is_open_fn):
            try:
                return bool(is_open_fn(location_key))
            except Exception:
                return False
        return True

    def checkEventTime(current_value, spec):
        if spec is None:
            return True
        if callable(spec):
            try:
                return bool(spec(current_value))
            except TypeError:
                try:
                    return bool(spec())
                except Exception:
                    return False
            except Exception:
                return False
        if isinstance(spec, _story_range_type):
            return _story_to_int(current_value, 0) in spec
        if isinstance(spec, (list, tuple, set)):
            values = list(spec)
            if len(values) == 2 and all(isinstance(item, (int, float)) for item in values):
                current_int = _story_to_int(current_value, 0)
                return _story_to_int(values[0], 0) <= current_int <= _story_to_int(values[1], 0)
            current_int = _story_to_int(current_value, 0)
            normalized = [_story_to_int(item, item) for item in values]
            return current_int in normalized or current_value in values
        try:
            return _story_to_int(current_value, 0) == _story_to_int(spec, spec)
        except Exception:
            return current_value == spec

    def _story_eval_condition(expr):
        if expr in (None, "", True, "always"):
            return True
        if expr is False:
            return False
        if callable(expr):
            try:
                return bool(expr())
            except Exception:
                return False

        text = str(expr or "").strip()
        if text == "":
            return True
        if text.startswith("!"):
            return not _story_eval_condition(text[1:])
        if text.startswith("#"):
            text = text[1:].strip()

        scope = _story_condition_scope()
        if text in scope:
            return bool(scope[text])
        try:
            return bool(eval(text, {"__builtins__": {}}, scope))
        except Exception:
            return False

    class StoryCondition(object):
        def __init__(self, expr):
            self.expr = expr

        def eval(self):
            return _story_eval_condition(self.expr)

        def blocked(self):
            return False

    def makeConditions(cond_source):
        if cond_source in (None, "", []):
            return []
        if isinstance(cond_source, (list, tuple, set)):
            return [StoryCondition(item) for item in cond_source]
        return [StoryCondition(cond_source)]

    def _story_conditions_met(conditions):
        return all(cond.eval() for cond in list(conditions or []))

    def _story_conditions_blocked(conditions):
        has_none = False
        for cond in list(conditions or []):
            rv = cond.blocked()
            if rv is True:
                return True
            if rv is None:
                has_none = True
        if has_none:
            return None
        return False

    def checkBlocksList(evt_list):
        has_none = False
        for evt in list(evt_list or []):
            rv = evt.checkBlocks()
            if rv is True:
                return True
            if rv is None:
                has_none = True
        if has_none:
            return None
        return False

    def _story_marker_day(ref_name, fallback=0):
        ref = str(ref_name or "").strip()
        if ref == "":
            return fallback
        try:
            if ref in threads:
                return _story_to_int(getattr(threads[ref], "day", fallback), fallback)
        except Exception:
            pass
        short_ref = ref[:-3] if len(ref) > 3 else ref
        try:
            if short_ref in threads:
                return _story_to_int(getattr(threads[short_ref], "day", fallback), fallback)
        except Exception:
            pass
        return _story_named_number(ref, fallback)

    def _story_delay_ready(delay_spec, fallback_marker=0):
        if delay_spec is None:
            return True
        if isinstance(delay_spec, int):
            return _story_num_day() >= _story_to_int(fallback_marker, 0) + int(delay_spec)
        if isinstance(delay_spec, (tuple, list)):
            if len(delay_spec) <= 0:
                return True
            marker_name = delay_spec[0]
            delay_days = delay_spec[1] if len(delay_spec) > 1 else 1
            marker_day = _story_marker_day(marker_name, fallback_marker)
            return _story_num_day() >= marker_day + _story_to_int(delay_days, 1)
        if isinstance(delay_spec, str):
            marker_day = _story_marker_day(delay_spec, fallback_marker)
            return _story_num_day() >= marker_day + 1
        return True

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

        def checkDay(self):
            current_day = _story_named_number("week", 0)
            return checkEventTime(current_day, self.day)

        def checkHour(self):
            current_hour = _story_named_number("hour", _story_named_number("time", 0))
            return checkEventTime(current_hour, self.hour)

        def checkNumDay(self, evt_numDay):
            return _story_delay_ready(self.evtDay, evt_numDay)

        def checkReqs(self):
            if self.reqs is None:
                return True
            friends_map = _story_named_value("Friends", {})
            roster = list(_story_named_value("AllGirlNames", []) or [])
            for stat, limit in dict(self.reqs).items():
                threshold = _story_to_int(limit, 0)
                if stat in roster or (hasattr(friends_map, "get") and stat in friends_map):
                    current_value = _story_to_int(friends_map.get(stat, 0), 0)
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
            try:
                return renpy.random.random() < float(probability)
            except Exception:
                return False

        def checkItem(self):
            if not self.item:
                return True
            inventory = _story_named_value("playerItems", None)
            if inventory is None:
                return False
            try:
                if hasattr(inventory, "items"):
                    return int(inventory.get(self.item, 0) or 0) > 0
                return self.item in inventory
            except Exception:
                return False

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

    def initEvents():
        for _name, tdata in dict(threadData or {}).items():
            for evt_list in list(tdata.triggers or []):
                for evt in list(evt_list or []):
                    evt.initConditions()

    class ThreadData(object):
        def __init__(self, level, person, subname, condStr, triggers, highlight, threaded):
            self.level = level
            self.person = person
            self.subname = subname
            self.name = self.person + self.subname
            self.condStr = condStr
            self.conds = []
            self.highlight = highlight
            if isinstance(triggers, list):
                self.triggers = [
                    ([Event(evt, self.name, threaded) for evt in evt_list] if isinstance(evt_list, list) else [Event(evt_list, self.name, threaded)])
                    for evt_list in triggers
                ]
            else:
                self.triggers = [[Event(triggers, self.name, threaded)]]
            self.length = len(self.triggers)

        def initConditions(self):
            self.conds = makeConditions(self.condStr)

        def checkConditions(self):
            return _story_conditions_met(self.conds)

        def checkBlocks(self):
            return _story_conditions_blocked(self.conds)

    class LThreadData(ThreadData):
        def __init__(self, level, person, subname, condStr, triggers, highlight=True, threaded=True):
            super(LThreadData, self).__init__(level, person, subname, condStr, triggers, highlight, threaded)

    class RThreadData(ThreadData):
        def __init__(self, level, person, subname, condStr, triggers, highlight=True, threaded=True):
            super(RThreadData, self).__init__(level, person, subname, condStr, [triggers[1]] * triggers[0], highlight, threaded)
            for num in range(self.length):
                for evt in self.triggers[num]:
                    if str(evt.target or "").endswith("*"):
                        evt.target = "%s%d" % (evt.target[:-1], num)

    class UThreadData(ThreadData):
        def __init__(self, level, person, subname, condStr, triggers, highlight=True, threaded=True):
            super(UThreadData, self).__init__(level, person, subname, condStr, triggers, highlight, threaded)

    class ThreadInfo(object):
        def __init__(self, data):
            self.data = data
            self.done = [False] * self.data.length
            self.enabled = False
            self.metconds = False
            self.aborted = False
            self.completed = False
            self.blocked = False
            self.blocks = [False] * self.data.length
            self.highlight = self.data.highlight
            self.day = 0
            self.num = 0

        def checkActive(self):
            if not _story_level_enabled(self.data.level):
                return False
            if not self.metconds:
                self.metconds = self.data.checkConditions()
            return self.metconds and not self.aborted and not self.completed

        def complete(self):
            self.done = [True] * self.data.length
            self.completed = True

        def abort(self):
            self.aborted = True

        def enable(self):
            self.enabled = True
            self.day = _story_num_day()

        def setDay(self, delta=0):
            self.day = _story_num_day() + _story_to_int(delta, 0)

        def getTarget(self, i):
            return self.getevent(i).target

        def initBlocks(self):
            self.blocked = None
            self.blocks = [None] * self.data.length

        def adjustLen(self):
            delta = self.data.length - len(self.done)
            if delta > 0:
                self.done += [False] * delta
            elif delta < 0:
                self.done = self.done[: self.data.length]

        def checkBlocks(self):
            if self.completed:
                self.blocked = False
                self.blocks = [False] * self.data.length
                return False
            if self.aborted:
                self.blocked = True
                self.blocks = [True] * self.data.length
                return True
            if not self.metconds:
                rc = self.data.checkBlocks()
                if rc is True:
                    self.blocks = [True] * self.data.length
                    self.blocked = True
                    return True
                if rc is None:
                    return None
            for i, evt_list in enumerate(self.data.triggers):
                if self.blocks[i] is False:
                    continue
                if self.done[i]:
                    self.blocks[i] = False
                    continue
                rc = checkBlocksList(evt_list)
                if rc is True:
                    for j in range(i, self.data.length):
                        self.blocks[j] = True
                    self.blocked = True
                    return True
                if rc is None:
                    return None
                if rc is False:
                    self.blocks[i] = False
            self.blocked = False
            return False

        def statusText(self):
            if self.completed:
                return "complete"
            if self.aborted:
                return "aborted"
            if self.checkActive():
                return "active"
            return "future"

        def currentTarget(self):
            if self.completed or self.aborted or self.num >= self.data.length:
                return "-"
            try:
                return str(self.getevent(self.num).target)
            except Exception:
                return "-"

    class LThreadInfo(ThreadInfo):
        def __init__(self, data):
            super(LThreadInfo, self).__init__(data)

        def advance(self):
            if self.num < self.data.length:
                self.done[self.num] = True
            self.num += 1
            if self.num >= self.data.length:
                self.completed = True

        def reactivate(self, num=None):
            self.aborted = False
            if num is not None:
                self.num = num

        def reset(self):
            self.aborted = False
            self.completed = False
            self.done = [False] * self.data.length
            self.num = 0
            self.day = _story_num_day()
            self.metconds = False

        def getevent(self, i):
            return self.data.triggers[i][0]

        def getAvailableEvents(self):
            if not self.checkActive():
                return []
            return [evt for evt in self.data.triggers[self.num] if evt.canTrigger(self.day)]

    class RThreadInfo(ThreadInfo):
        def __init__(self, data):
            super(RThreadInfo, self).__init__(data)
            self.order = list(range(self.data.length))
            renpy.random.shuffle(self.order)

        def advance(self):
            self.done[self.order[self.num]] = True
            self.num += 1
            if self.num >= self.data.length:
                self.completed = True
                renpy.random.shuffle(self.order)

        def reactivate(self, num=None):
            self.aborted = False
            if num is not None:
                self.num = num

        def getevent(self, i):
            return self.data.triggers[i][0]

        def adjustLen(self):
            super(RThreadInfo, self).adjustLen()
            delta = self.data.length - len(self.order)
            if delta > 0:
                for n in range(len(self.order), self.data.length):
                    self.order.append(n)

        def getAvailableEvents(self):
            if not self.checkActive():
                return []
            return [evt for evt in self.data.triggers[self.order[self.num]] if evt.canTrigger(self.day)]

    class UThreadInfo(ThreadInfo):
        def __init__(self, data):
            super(UThreadInfo, self).__init__(data)

        def seen(self, num):
            self.done[num] = True
            self.num += 1
            if self.num >= self.data.length:
                self.completed = True

        def reactivate(self, num=None):
            self.aborted = False

        def getevent(self, i):
            return self.data.triggers[i][0]

        def getAvailableEvents(self):
            if not self.checkActive():
                return []
            return [
                evt
                for num in range(self.data.length)
                if not self.done[num]
                for evt in self.data.triggers[num]
                if evt.canTrigger(self.day)
            ]

    def loadThreadData(thread_list):
        return {tdata.name: tdata for tdata in list(thread_list or [])}

    def createThread(data):
        if isinstance(data, LThreadData):
            return LThreadInfo(data)
        if isinstance(data, RThreadData):
            return RThreadInfo(data)
        if isinstance(data, UThreadData):
            return UThreadInfo(data)
        raise Exception("createThread")

    def createThreads():
        return {name: createThread(data) for name, data in dict(threadData or {}).items()}

    def initThreads():
        global threads
        current_threads = _story_named_value("threads", {})
        if not isinstance(current_threads, dict):
            current_threads = {}
        for name, tdata in dict(threadData or {}).items():
            if name not in current_threads:
                current_threads[name] = createThread(tdata)
            else:
                current_threads[name].data = tdata
                current_threads[name].adjustLen()
        for _name, tdata in dict(threadData or {}).items():
            tdata.initConditions()
        threads = current_threads

    def findBlockedThreads(threads_in):
        if threads_in is threads:
            for _name, thread_info in dict(threads_in or {}).items():
                thread_info.initBlocks()
        pending = []
        while True:
            changed = False
            pending = []
            for _name, thread_info in dict(threads_in or {}).items():
                rv = thread_info.checkBlocks()
                if rv is None:
                    pending.append(thread_info)
                else:
                    changed = True
            if not pending or not changed:
                break
        return threads_in

    def findAvailableEvents(forced=False):
        global availEvents, evalTime
        global eventLocations, eventPeople, eventTalk, eventOptions, eventItems
        global story_events

        eval_key = (
            _story_num_day(),
            _story_named_number("week", 1),
            _story_named_number("time", 0),
            str(_story_named_value("CurLoc", "") or ""),
        )
        if (not forced) and evalTime == eval_key:
            return
        evalTime = eval_key

        tmp_events = []
        for _name, thread_info in dict(threads or {}).items():
            tmp_events.extend(thread_info.getAvailableEvents())

        availEvents = {}
        for evt in tmp_events:
            location_key = str(evt.location or "").strip()
            action_key = str(evt.action or "").strip()
            if location_key == "" or action_key == "":
                continue
            if location_key not in availEvents:
                availEvents[location_key] = {action_key: [evt]}
            elif action_key not in availEvents[location_key]:
                availEvents[location_key][action_key] = [evt]
            else:
                availEvents[location_key][action_key].append(evt)

        for location_name in list(availEvents.keys()):
            for action_name in list(availEvents[location_name].keys()):
                availEvents[location_name][action_name].sort(key=lambda item: int(item.priority or 0))
                chosen = None
                for evt in availEvents[location_name][action_name]:
                    if evt.checkItem():
                        chosen = evt
                        break
                if chosen is None and len(availEvents[location_name][action_name]) > 0:
                    chosen = availEvents[location_name][action_name][0]
                availEvents[location_name][action_name] = chosen

        eventLocations = set(availEvents.keys())
        eventPeople = set()
        eventTalk = set()
        eventOptions = set()
        eventItems = set()
        story_events = list(dict(threadData or {}).keys())

    def initStoryEventRuntime(force=False):
        initThreads()
        initEvents()
        findBlockedThreads(threads)
        findAvailableEvents(True if force else False)

    def _story_after_load_init():
        try:
            initStoryEventRuntime(True)
        except Exception:
            pass

    if _story_after_load_init not in config.after_load_callbacks:
        config.after_load_callbacks.append(_story_after_load_init)


init python:
    def story_amanda_clear_pending():
        global amanda_story_pending
        amanda_story_pending = ""

    def story_event_available(location_name="", action_name=""):
        location_key = str(location_name or "").strip()
        action_key = str(action_name or "").strip()
        if location_key == "" or action_key == "":
            return False
        try:
            findAvailableEvents(False)
        except Exception:
            return False
        return (
            isinstance(availEvents, dict)
            and location_key in availEvents
            and action_key in dict(availEvents.get(location_key, {}) or {})
            and availEvents[location_key].get(action_key, None) is not None
        )

    def story_thread_advance_current():
        global evalTime
        try:
            current_thread = thread
        except NameError:
            current_thread = None
        if current_thread is not None:
            try:
                current_thread.advance()
            except Exception:
                pass
        evalTime = None
        try:
            findAvailableEvents(True)
        except Exception:
            pass

    def _story_current_location():
        return str(_story_named_value("CurLoc", "") or "")

    def story_amanda_prepare_entry(location_name):
        global amanda_story_pending

        amanda_story_pending = ""
        current_location = _story_current_location()
        if current_location != str(location_name or ""):
            return False

        check_func = _story_named_callable("CheckIfSexEventExist")
        if not callable(check_func):
            return False

        cur_time = _story_named_number("time", 0)
        chance_to_notice = 5
        if current_location == "TavernMain":
            chance_to_notice = 3
        elif current_location == "MarketPlace":
            chance_to_notice = 7

        try:
            if renpy.random.randint(1, chance_to_notice) == 1 and _story_to_int(check_func("amanda", cur_time, "legarerun"), 0) > 0:
                amanda_story_pending = "run_to_legare"
                return True
        except Exception:
            return False

        if current_location == "StreetTavern":
            try:
                if renpy.random.randint(1, 5) == 1 and _story_to_int(check_func("amanda", cur_time, "lovermeet"), 0) > 0:
                    amanda_story_pending = "meet_lover"
                    return True
            except Exception:
                return False

        return False

    def story_amanda_tavern_entry_ready():
        return story_amanda_prepare_entry("TavernMain")

    def story_amanda_street_entry_ready():
        return story_amanda_prepare_entry("StreetTavern")

    def story_amanda_market_entry_ready():
        return story_amanda_prepare_entry("MarketPlace")

    # household_pests_arc
    # - rat_problem_thread
    # - cat_solution_thread
    # - bats_problem_thread
    # - attic_scandal_thread
    # - clarissa_booklet_thread
    #
    # Keep save-sensitive live thread names stable where possible.
    # The boolean helpers below are the explicit gate layer for the current runtime.
    def household_pests_rat_problem_storage_ready():
        return tavern_storage_rat_event_ready()

    def household_pests_rat_problem_complaints_ready():
        return werecat_rat_breakfast_ready()

    def household_pests_cat_solution_home_ready():
        return werecat_adoption_breakfast_ready()

    def household_pests_cat_solution_month_ready():
        return werecat_month_thanks_ready()

    def household_pests_cat_solution_hunter_rumor_ready():
        return werecat_hunter_tease_ready()

    def household_pests_bats_problem_breakfast_ready():
        return melissa_bat_breakfast_ready()

    def household_pests_bats_problem_night_talk_ready():
        return melissa_night_noise_ready()

    def household_pests_bats_attic_colony_ready():
        return melissa_bat_attic_colony_event_ready()

    def household_pests_bats_attic_window_ready():
        return melissa_bat_attic_window_event_ready()

    def household_pests_clarissa_booklet_under_bed_ready():
        return melissa_drawings_scene_ready()

    def household_pests_bats_cleanup_ready():
        return melissa_bat_attic_cleanup_event_ready()

    def household_pests_bats_completion_talk_ready():
        return melissa_bat_completion_talk_event_ready()

    def household_pests_clarissa_booklet_overheard_ready():
        return melissa_clara_overhear_ready()


define amandaThreadList = [
    LThreadData(0, "amanda", "TavernEntry", None,
        ("story_amanda_tavern_entry", None, None, None, 1, None, "story_amanda_tavern_entry_ready()", None, "TavernMain", "enter", 0),
        highlight=False,
        threaded=False,
    ),
    LThreadData(0, "amanda", "StreetEntry", None,
        ("story_amanda_street_entry", None, None, None, 1, None, "story_amanda_street_entry_ready()", None, "StreetTavern", "enter", 0),
        highlight=False,
        threaded=False,
    ),
    LThreadData(0, "amanda", "MarketEntry", None,
        ("story_amanda_market_entry", None, None, None, 1, None, "story_amanda_market_entry_ready()", None, "MarketPlace", "enter", 0),
        highlight=False,
        threaded=False,
    ),
]

define melissaThreadList = [
    #
    # household_pests_arc
    #
    # rat_problem_thread
    LThreadData(0, "melissa", "RatProblem", None, [
        ("story_melissa_storage_rat_0", None, None, None, 1, None, "household_pests_rat_problem_storage_ready()", None, "TavernStorage", "enter", 0),
    ], highlight=False, threaded=True),
    # cat_solution_thread
    LThreadData(0, "melissa", "WerecatRumor", None, [
        ("story_melissa_werecat_rumor_0", None, None, None, 1, None, "household_pests_cat_solution_hunter_rumor_ready()", None, "HunterClub", "overheard", 0),
    ], highlight=False, threaded=True),
    LThreadData(0, "melissa", "WerecatIntro", None, [
        ("story_melissa_werecat_intro_0", None, None, None, 1, None, "household_pests_rat_problem_complaints_ready()", None, "TavernKitchen", "enter", 0),
    ], highlight=False, threaded=True),
    LThreadData(0, "melissa", "WerecatHome", "WerecatVar.get('adopted', 0) == 1", [
        ("story_melissa_werecat_home_0", None, None, None, 1, None, "household_pests_cat_solution_home_ready()", None, "TavernKitchen", "enter", 0),
        ("story_melissa_werecat_home_1", None, None, None, 1, None, "household_pests_cat_solution_month_ready()", None, "TavernKitchen", "enter", 1),
    ], highlight=False, threaded=True),
    # bats_problem_thread
    LThreadData(0, "melissa", "BatProblem", None, [
        ("story_melissa_bat_problem_0", None, None, None, 1, None, "household_pests_bats_problem_breakfast_ready()", None, "TavernKitchen", "enter", 0),
        ("story_melissa_bat_problem_1", None, None, None, 1, None, "household_pests_bats_problem_night_talk_ready()", None, "TavernUpstairs", "enter", 1),
        ("story_melissa_bat_problem_2", None, None, None, 1, None, "household_pests_bats_attic_colony_ready()", None, "TavernAtic", "melissa_bats", 2),
        ("story_melissa_bat_problem_3", None, None, None, 1, None, "household_pests_bats_attic_window_ready()", None, "TavernAtic", "melissa_bats", 3),
        ("story_melissa_bat_problem_4", None, None, None, 1, None, "household_pests_bats_cleanup_ready()", None, "TavernAtic", "melissa_bats", 4),
        ("story_melissa_bat_problem_5", None, None, None, 1, None, "household_pests_clarissa_booklet_under_bed_ready()", None, "TavernAmandaRoom", "melissa_bats", 5),
        ("story_melissa_bat_problem_6", None, None, None, 1, None, "household_pests_bats_completion_talk_ready()", None, "TavernMain", "melissa_talk", 6),
    ], highlight=False, threaded=True),
    # clarissa_booklet_thread lead
    LThreadData(0, "melissa", "ClaraOverheard", None, [
        ("melissaClaraOverheard_0", None, None, None, 1, None, "household_pests_clarissa_booklet_overheard_ready() and int(ClaraVar.get('tavern_melissa_visit_count', 0) or 0) >= 2 and int(ClaraVar.get('tavern_melissa_overheard_2_seen', 0) or 0) == 0", None, "TavernMain", "overheard", 0),
        ("melissaClaraOverheard_1", None, None, None, 1, None, "household_pests_clarissa_booklet_overheard_ready() and int(ClaraVar.get('tavern_melissa_overheard_2_seen', 0) or 0) == 1 and int(ClaraVar.get('tavern_melissa_overheard_3_seen', 0) or 0) == 0 and int(ClaraVar.get('tavern_melissa_visit_count', 0) or 0) >= 3 and int(MelissaVar.get('bats_episode', 0) or 0) >= 6", None, "TavernMain", "overheard", 1),
    ], highlight=False, threaded=True),
]

define sandraThreadList = [
    LThreadData(0, "sandra", "WeeklyEvaluation", None, [
        ("sandraWeeklyEvaluation_0", None, None, None, 1, None, None, None, "TavernMyRoom", "sleep", 0),
        ("sandraWeeklyEvaluation_1", None, None, None, 1, None, None, None, "TavernMyRoom", "sleep", 1),
        ("sandraWeeklyEvaluation_2", None, None, None, 1, None, None, None, "TavernMyRoom", "sleep", 2),
        ("sandraWeeklyEvaluation_3", None, None, None, 1, None, None, None, "TavernMyRoom", "sleep", 3),
    ], highlight=False, threaded=True),
]
define claraThreadList = [
    LThreadData(0, "clara", "BookletMarket", None, [
        ("story_clara_market_booklet_0", None, None, None, 1, None, "str(_story_current_location() or '') == 'MarketPlace' and bool(clara_market_visit_active()) and (((int(_story_named_number('time', 0) or 0) == 2) and int(ClaraVar.get('booklet_market_seen', 0) or 0) == 0) or ((int(_story_named_number('time', 0) or 0) == 3) and int(ClaraVar.get('drawings_secret_known', 0) or 0) == 1 and int(ClaraVar.get('booklet_market_seen', 0) or 0) == 0))", None, "MarketPlace", "enter", 0),
        ("story_clara_market_booklet_1", None, None, None, 1, None, "str(_story_current_location() or '') == 'MarketPlace' and bool(clara_market_visit_active()) and (((int(_story_named_number('time', 0) or 0) == 2) and int(ClaraVar.get('market_intro_seen', 0) or 0) == 1) or ((int(_story_named_number('time', 0) or 0) == 3) and int(ClaraVar.get('drawings_secret_known', 0) or 0) == 1)) and int(ClaraVar.get('booklet_market_seen', 0) or 0) == 0", None, "MarketPlace", "enter", 1),
        ("story_clara_market_booklet_2", None, None, None, 1, None, "str(_story_current_location() or '') == 'MarketPlace' and bool(clara_market_visit_active()) and int(_story_named_number('time', 0) or 0) == 3 and int(ClaraVar.get('booklet_market_seen', 0) or 0) == 1 and int(ClaraVar.get('market_evening_intro_seen', 0) or 0) == 0", None, "MarketPlace", "enter", 2),
        ("story_clara_market_booklet_3", None, None, None, 1, None, "str(_story_current_location() or '') == 'MarketPlace' and bool(clara_market_visit_active()) and int(_story_named_number('time', 0) or 0) == 3 and int(ClaraVar.get('market_evening_intro_seen', 0) or 0) == 1 and int(ClaraVar.get('mongol_theft_seen', 0) or 0) == 0", None, "MarketPlace", "enter", 3),
        ("story_clara_market_booklet_4", None, None, None, 1, None, "str(_story_current_location() or '') == 'WineStore' and int(ClaraVar.get('mongol_theft_seen', 0) or 0) == 1 and int(ClaraVar.get('escape_confessed', 0) or 0) == 0", None, "WineStore", "clara_talk", 4),
        ("story_clara_market_booklet_5", None, None, None, 1, None, "str(_story_current_location() or '') == 'HunterClub' and int(ClaraVar.get('escape_confessed', 0) or 0) == 1 and int(MongolVar.get('StocksArrestDay', -1) or -1) < 0", None, "HunterClub", "overheard", 5),
        ("story_clara_market_booklet_6", None, None, None, 1, None, "str(_story_current_location() or '') == 'CityGuard' and int(MongolVar.get('StocksArrestDay', -1) or -1) >= 0 and int(MongolVar.get('StocksSeen', 0) or 0) == 0", None, "CityGuard", "enter", 6),
        ("story_clara_market_booklet_7", None, None, None, 1, None, "str(_story_current_location() or '') == 'CityGuard' and int(MongolVar.get('StocksSeen', 0) or 0) == 1 and int(MongolVar.get('StocksFoodDay', -1) or -1) < 0 and int(_story_named_number('time', 0) or 0) >= 4", None, "CityGuard", "enter", 7),
        ("story_clara_market_booklet_8", None, None, None, 1, None, "str(_story_current_location() or '') == 'StolyarWorkshop' and int(MongolVar.get('StocksFoodDay', -1) or -1) >= 0 and int(DraupnirVar.get('MongolLockpickOrderDay', -1) or -1) < 0 and int(_story_named_number('time', 0) or 0) < 3 and int(week or 0) != 7", None, "StolyarWorkshop", "enter", 8),
        ("story_clara_market_booklet_9", None, None, None, 1, None, "str(_story_current_location() or '') == 'CityGuard' and int(DraupnirVar.get('MongolLockpickOrderDay', -1) or -1) >= 0 and int(MongolVar.get('StocksReleased', 0) or 0) == 0 and int(_story_named_number('time', 0) or 0) >= 4 and int(dayspassed or 0) > int(MongolVar.get('StocksFoodDay', -1) or -1)", None, "CityGuard", "enter", 9),
    ], highlight=False, threaded=True),
]
define beckyThreadList = []
define lizaThreadList = []
define georgettThreadList = []

define threadListsByGirl = {
    "amanda": amandaThreadList,
    "melissa": melissaThreadList,
    "sandra": sandraThreadList,
    "clara": claraThreadList,
    "becky": beckyThreadList,
    "liza": lizaThreadList,
    "georgett": georgettThreadList,
}

define threadList = (
    amandaThreadList
    + melissaThreadList
    + sandraThreadList
    + claraThreadList
    + beckyThreadList
    + lizaThreadList
    + georgettThreadList
)

define threadData = loadThreadData(threadList)
default threads = createThreads()


label checkTriggers(location, action, numpop=0):
    $ _story_location = str(location or "")
    $ _story_action = str(action or "")
    if _story_location not in availEvents:
        return False
    if _story_action not in availEvents[_story_location]:
        return False
    $ evt = availEvents[_story_location][_story_action]
    if evt is None or not evt.target:
        return False
    if evt.item and not evt.checkItem():
        return False
    $ active_event = evt
    if numpop == 2:
        $ renpy.pop_call()
    elif numpop == 1:
        $ renpy.pop_call()
    call preEvent(evt.thread_name if evt.threaded else None)
    jump expression evt.target


label preEvent(thread_name=None):
    $ evalTime = None
    if thread_name:
        $ thread = threads[thread_name]
        $ thread.setDay()
    else:
        $ thread = None
    return


label story_amanda_tavern_entry:
    if str(amanda_story_pending or "") != "run_to_legare":
        jump TavernMain
    $ story_amanda_clear_pending()
    $ SignalBlockTime = 1
    "Неожиданно вы заметили, что Аманда потихоньку, и насколько это возможно незаметно, пробирается к выходу."
    $ ShowImage("amanda", "", "portrait")
    menu:
        "Что сделать?"
        "Проследить за ней":
            jump AfterDanceSexLegare
        "Оставить ее в покое":
            "\"Спешит куда-то? Ну и пусть себе спешит, не мое дело,\" подумали вы. А Аманда скоро скрылась за углом."
            if renpy.has_label("LegareAmandaLetGoCode"):
                call expression "LegareAmandaLetGoCode"
            jump TavernMain
        "Отправить ее обратно на работу":
            "Вы выскочили из трактира вслед за Амандой и увидели, что она намылилась куда-то далеко."
            $ AmandaYellNotWork()
            $ _story_amanda_back = str(AmandaDynamicTakeNextJump() or "StreetTavern")
            if renpy.has_label(_story_amanda_back):
                jump expression _story_amanda_back
            jump StreetTavern


label story_amanda_street_entry:
    $ _story_amanda_pending = str(amanda_story_pending or "")
    if _story_amanda_pending == "run_to_legare":
        $ story_amanda_clear_pending()
        $ SignalBlockTime = 1
        "Неожиданно вы заметили Аманду. Кажется, она не очень хочет, чтобы ее заметили, и поэтому постоянно озирается, передвигается от угла к углу и старается держаться в тени домов."
        $ ShowImage("amanda", "", "portrait")
        menu:
            "Что сделать?"
            "Проследить за ней":
                jump AfterDanceSexLegare
            "Оставить ее в покое":
                "\"Спешит куда-то? Ну и пусть себе спешит, не мое дело,\" подумали вы. А Аманда скоро скрылась за углом."
                if renpy.has_label("LegareAmandaLetGoCode"):
                    call expression "LegareAmandaLetGoCode"
                jump StreetTavern
            "Отправить ее обратно":
                $ AmandaYellNotWork()
                $ _story_amanda_back = str(AmandaDynamicTakeNextJump() or "StreetTavern")
                if renpy.has_label(_story_amanda_back):
                    jump expression _story_amanda_back
                jump StreetTavern
    elif _story_amanda_pending == "meet_lover":
        $ story_amanda_clear_pending()
        $ SignalBlockTime = 1
        "Проходя мимо трактира, вы вдруг заметили на улице знакомую фигуру."
        if renpy.random.randint(1, 2) == 1:
            menu:
                "Что сделать?"
                "Посмотреть поближе":
                    "Вы подошли поближе, но оказалось, что вы обознались."
                    jump street_tavern_menu
                "Идти дальше":
                    "\"Да мало ли кто это может быть? У меня есть дела поважнее!\" подумали вы и пошли дальше."
                    jump street_tavern_menu
        $ GetSexEventFromTable("amanda", time, "lovermeet")
        menu:
            "Что сделать?"
            "Посмотреть поближе":
                jump AmandaLoverSex
            "Идти дальше":
                "\"Да мало ли кто это может быть? У меня есть дела поважнее!\" подумали вы и пошли дальше."
                jump street_tavern_menu
    jump StreetTavern


label melissaClaraOverheard_0:
    $ household_mark_runtime_event_seen("melissa_clara_overhear")
    $ ClaraVar["tavern_melissa_overheard_2_seen"] = 1
    $ MainTxt = "Проходя мимо, вы слышите, как Мелисса, едва сдерживая смех, говорит Клариссе: \"Девчонка утром рано встала, песду о лавку почесала и села у окошка сечь, как бобик Жучку станет ебсть\".\n\nКларисса тут же подхватывает, уже совсем не скрывая довольной ухмылки: \"А бобик жарил Жучку раком, чего стесняться им, собакам!\" После этого обе разом заливаются таким дружным хохотом, будто давно уже спелись на этой пошлой волне."
    $ sluttiness["melissa"] = min(100, int(sluttiness.get("melissa", 0) or 0) + 3)
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + 1)
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/tavern_visit.png"):
        call ShowImage("", "", "images/clara/tavern_visit.png")
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отойти от чужого разговора", Call("TavernMainRestore"))]
    $ story_thread_advance_current()
    jump TavernMainView


label melissaClaraOverheard_1:
    $ household_mark_runtime_event_seen("melissa_clara_overhear")
    $ ClaraVar["tavern_melissa_overheard_3_seen"] = 1
    $ MainTxt = "Вы делаете вид, что заняты у барной стойки, но слух сам цепляет веселый шепот за спиной. Мелисса, уже откровенно дурачась, декламирует: \"Если б я была царица, говорит одна девица, я б пизду покрыла лаком и давала только раком\".\n\n\"Ой-ёй,\" тут же тянет Клара с ехидной ухмылкой, \"царь наш был мужичок скромный, у него был хуй огромный...\" Мелисса шутливо хлопает подружку по плечу и отвечает: \"Да говорю же, вот такой\", после чего раздвигает ладони сантиметров на двадцать.\n\nОбе многозначительно косятся на вас, а потом прыскают от смеха, пока вы изо всех сил делаете вид, будто целиком поглощены стойкой и делами трактира."
    $ sluttiness["melissa"] = min(100, int(sluttiness.get("melissa", 0) or 0) + 4)
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + 2)
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/tavern_visit_size.png"):
        call ShowImage("", "", "images/clara/tavern_visit_size.png")
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Сделать вид, что ничего не услышали", Call("TavernMainRestore"))]
    $ story_thread_advance_current()
    jump TavernMainView


label story_amanda_market_entry:
    if str(amanda_story_pending or "") != "run_to_legare":
        jump MarketPlace
    $ story_amanda_clear_pending()
    $ SignalBlockTime = 1
    "Неожиданно вы заметили Аманду, пробирающуюся между лавками, палатками и лотками. Кажется, она не очень хочет, чтобы ее заметили, и поэтому постоянно озирается и старается держаться в тени."
    $ ShowImage("amanda", "", "portrait")
    menu:
        "Что сделать?"
        "Проследить за ней":
            jump AfterDanceSexLegare
        "Оставить ее в покое":
            "\"Спешит куда-то? Ну и пусть себе спешит, не мое дело,\" подумали вы. А Аманда скоро скрылась за углом."
            if renpy.has_label("LegareAmandaLetGoCode"):
                call expression "LegareAmandaLetGoCode"
            jump MarketPlace
        "Отправить ее обратно":
            $ AmandaYellNotWork()
            $ _story_amanda_back = str(AmandaDynamicTakeNextJump() or "StreetTavern")
            if renpy.has_label(_story_amanda_back):
                jump expression _story_amanda_back
            jump StreetTavern


label story_clara_market_booklet_0:
    $ SignalBlockTime = 1
    $ _clara_evening_booklet_follow = int(time or 0) == 3 and int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1
    $ _clara_market_intro_seen = int(ClaraVar.get("market_intro_seen", 0) or 0) == 1
    if _clara_evening_booklet_follow:
        $ ClaraVar["market_evening_intro_seen"] = 1
        $ MainTxt = "Вечером вы замечаете Клариссу на рынке и уже знаете, что ее секрет связан не только с болтовней, но и с непристойными рисунками. Девушка быстро скользит мимо лавок, будто проверяя, нет ли за ней слежки, а затем сворачивает к неприметному закутку между рядами.\n\nЕсли сейчас держаться достаточно тихо, можно не только проследить за Клариссой, но и подслушать, с кем именно она ведет свои тайные дела."
        $ CurLocDesc = MainTxt
        if renpy.loadable("images/clara/market_night.png"):
            call ShowImage("", "", "images/clara/market_night.png")
        elif renpy.loadable("images/market/LocMarketPlace2.jpg"):
            call ShowImage("", "", "images/market/LocMarketPlace2.jpg")
    else:
        if _clara_market_intro_seen:
            $ MainTxt = "В следующий раз, заметив Клариссу на дневном рынке, вы уже не торопитесь окликнуть ее, а стараетесь держаться чуть поодаль. Девушка идет быстро и уверенно, но все равно время от времени проверяет, не узнал ли кто ее в толпе.\n\nЕсли уж вы хотите узнать, чем она занимается, сейчас самое время попробовать проследить за ней."
        else:
            $ ClaraVar["market_intro_seen"] = 1
            $ MainTxt = "На дневном рынке вы замечаете очаровательную дочку своего винного поставщика. Вы уже собираетесь приветственно махнуть ей рукой, но Кларисса, едва встретившись с вами взглядом, поспешно набрасывает на голову капюшон плаща и тут же исчезает между рядами лавок.\n\nПохоже, у нее здесь какие-то совсем частные дела, и узнавать себя она сейчас не хочет. Вы решаете выяснить, что это за тайны."
        $ CurLocDesc = MainTxt
        if renpy.loadable("images/clara/market_day.png"):
            call ShowImage("", "", "images/clara/market_day.png")
        else:
            call ShowImageSeq("general", "", "LocMarketPlace", 2)
    menu:
        "Что сделать?"
        "[('Проследить за Клариссой и подслушать разговор') if _clara_evening_booklet_follow else ('Проследить за Клариссой')]":
            if _clara_evening_booklet_follow and int(effective_player_exploration() or 0) < 100:
                $ MainTxt = "Вечерний рынок куда опаснее для слежки, чем дневной. Стоит вам зацепить чей-то ящик или лишний раз оглянуться, как Кларисса успевает скрыться в темном закутке и растворяется среди поздних покупателей.\n\nБез лучшей сноровки вы только выдадите себя и ничего не услышите."
                $ CurLocDesc = MainTxt
                $ current_action_title = "Вечерний рынок"
                $ current_action_content = None
                $ current_action_items = [MenuItem("Вернуться к своим делам", Call("MarketPlaceRestore"))]
                jump MarketPlaceView
            if (not _clara_evening_booklet_follow) and int(effective_player_exploration() or 0) < 80:
                $ MainTxt = "Вы стараетесь не отстать, но дневной рынок слишком шумный и тесный. Стоит вам замешкаться на пару шагов, как Кларисса ускользает между рядами и будто растворяется среди чужих спин.\n\nПохоже, без лучшей сноровки в слежке вы просто потеряете ее снова."
                $ CurLocDesc = MainTxt
                $ current_action_title = "Рынок"
                $ current_action_content = None
                $ current_action_items = [MenuItem("Продолжить идти по рынку", Call("MarketPlaceRestore"))]
                jump MarketPlaceView
            $ ClaraVar["booklet_market_seen"] = 1
            if _clara_evening_booklet_follow:
                $ MainTxt = "На этот раз вы не теряете Клариссу даже в вечерней толпе. Держась в тени, вы видите, как она подходит к неприметному торговцу, которому уже прежде, похоже, приносила товар. Несколько свернутых листков быстро переходят из ее рук в его ладонь, а потом вы успеваете расслышать главное: торговец ворчит, что непристойные книжечки у него разбирают быстрее обычного, и просит в следующий раз принести еще, пока у клиентов снова не кончились деньги.\n\nТеперь у вас нет сомнений. Кларисса действительно тайком сбывает через рынок свои непристойные рисунки и маленькие книжечки, а делает это давно и вполне уверенно."
            else:
                $ MainTxt = "На этот раз вы не теряете Клариссу в толпе. Держась в стороне, вы видите, как она сворачивает к неприметному торговцу, которого почти не видно с центральных рядов. Обмен короткий и явно привычный: Кларисса по одной передает ему тонкие книжечки, похожие на небольшие буклеты, а тот быстро сует их в сумку и так же быстро отсчитывает ей деньги.\n\nТеперь уже ясно, что речь идет не о простой прогулке по рынку. Кларисса что-то сбывает через этого таинственного торговца."
            $ CurLocDesc = MainTxt
            if renpy.loadable("images/clara/market_bookletDeal.png"):
                call ShowImage("", "", "images/clara/market_bookletDeal.png")
            $ current_action_title = "Слежка на рынке"
            $ current_action_content = None
            $ current_action_items = [MenuItem("Тихо уйти", Call("MarketPlaceRestore"))]
            if (not _clara_evening_booklet_follow) and (int(MelissaVar.get("drawings_found", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1):
                $ current_action_items.insert(0, MenuItem("Подойти к Клариссе и торговцу", Call("story_clara_market_booklet_confront")))
            $ story_thread_advance_current()
            $ story_thread_advance_current()
            if _clara_evening_booklet_follow:
                $ story_thread_advance_current()
            jump MarketPlaceView
        "Не вмешиваться":
            if _clara_evening_booklet_follow:
                $ current_action_title = "Вечерний рынок"
                $ current_action_items = [MenuItem("Вернуться к своим делам", Call("MarketPlaceRestore"))]
            else:
                $ current_action_title = "Рынок"
                $ current_action_items = [MenuItem("Продолжить идти по рынку", Call("MarketPlaceRestore"))]
            $ current_action_content = None
            jump MarketPlaceView


label story_clara_market_booklet_1:
    $ SignalBlockTime = 1
    $ _clara_evening_booklet_follow = int(time or 0) == 3 and int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1
    if _clara_evening_booklet_follow:
        $ ClaraVar["market_evening_intro_seen"] = 1
        $ MainTxt = "Вечером вы замечаете Клариссу на рынке и уже знаете, что ее секрет связан не только с болтовней, но и с непристойными рисунками. Девушка быстро скользит мимо лавок, будто проверяя, нет ли за ней слежки, а затем сворачивает к неприметному закутку между рядами.\n\nЕсли сейчас держаться достаточно тихо, можно не только проследить за Клариссой, но и подслушать, с кем именно она ведет свои тайные дела."
        $ CurLocDesc = MainTxt
        if renpy.loadable("images/clara/market_night.png"):
            call ShowImage("", "", "images/clara/market_night.png")
        elif renpy.loadable("images/market/LocMarketPlace2.jpg"):
            call ShowImage("", "", "images/market/LocMarketPlace2.jpg")
    else:
        $ MainTxt = "В следующий раз, заметив Клариссу на дневном рынке, вы уже не торопитесь окликнуть ее, а стараетесь держаться чуть поодаль. Девушка идет быстро и уверенно, но все равно время от времени проверяет, не узнал ли кто ее в толпе.\n\nЕсли уж вы хотите узнать, чем она занимается, сейчас самое время попробовать проследить за ней."
        $ CurLocDesc = MainTxt
        if renpy.loadable("images/clara/market_day.png"):
            call ShowImage("", "", "images/clara/market_day.png")
        else:
            call ShowImageSeq("general", "", "LocMarketPlace", 2)
    menu:
        "Что сделать?"
        "[('Проследить за Клариссой и подслушать разговор') if _clara_evening_booklet_follow else ('Проследить за Клариссой')]":
            if _clara_evening_booklet_follow and int(effective_player_exploration() or 0) < 100:
                $ MainTxt = "Вечерний рынок куда опаснее для слежки, чем дневной. Стоит вам зацепить чей-то ящик или лишний раз оглянуться, как Кларисса успевает скрыться в темном закутке и растворяется среди поздних покупателей.\n\nБез лучшей сноровки вы только выдадите себя и ничего не услышите."
                $ CurLocDesc = MainTxt
                $ current_action_title = "Вечерний рынок"
                $ current_action_content = None
                $ current_action_items = [MenuItem("Вернуться к своим делам", Call("MarketPlaceRestore"))]
                jump MarketPlaceView
            if (not _clara_evening_booklet_follow) and int(effective_player_exploration() or 0) < 80:
                $ MainTxt = "Вы стараетесь не отстать, но дневной рынок слишком шумный и тесный. Стоит вам замешкаться на пару шагов, как Кларисса ускользает между рядами и будто растворяется среди чужих спин.\n\nПохоже, без лучшей сноровки в слежке вы просто потеряете ее снова."
                $ CurLocDesc = MainTxt
                $ current_action_title = "Рынок"
                $ current_action_content = None
                $ current_action_items = [MenuItem("Продолжить идти по рынку", Call("MarketPlaceRestore"))]
                jump MarketPlaceView
            $ ClaraVar["booklet_market_seen"] = 1
            if _clara_evening_booklet_follow:
                $ MainTxt = "На этот раз вы не теряете Клариссу даже в вечерней толпе. Держась в тени, вы видите, как она подходит к неприметному торговцу, которому уже прежде, похоже, приносила товар. Несколько свернутых листков быстро переходят из ее рук в его ладонь, а потом вы успеваете расслышать главное: торговец ворчит, что непристойные книжечки у него разбирают быстрее обычного, и просит в следующий раз принести еще, пока у клиентов снова не кончились деньги.\n\nТеперь у вас нет сомнений. Кларисса действительно тайком сбывает через рынок свои непристойные рисунки и маленькие книжечки, а делает это давно и вполне уверенно."
            else:
                $ MainTxt = "На этот раз вы не теряете Клариссу в толпе. Держась в стороне, вы видите, как она сворачивает к неприметному торговцу, которого почти не видно с центральных рядов. Обмен короткий и явно привычный: Кларисса по одной передает ему тонкие книжечки, похожие на небольшие буклеты, а тот быстро сует их в сумку и так же быстро отсчитывает ей деньги.\n\nТеперь уже ясно, что речь идет не о простой прогулке по рынку. Кларисса что-то сбывает через этого таинственного торговца."
            $ CurLocDesc = MainTxt
            if renpy.loadable("images/clara/market_bookletDeal.png"):
                call ShowImage("", "", "images/clara/market_bookletDeal.png")
            $ current_action_title = "Слежка на рынке"
            $ current_action_content = None
            $ current_action_items = [MenuItem("Тихо уйти", Call("MarketPlaceRestore"))]
            if (not _clara_evening_booklet_follow) and (int(MelissaVar.get("drawings_found", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1):
                $ current_action_items.insert(0, MenuItem("Подойти к Клариссе и торговцу", Call("story_clara_market_booklet_confront")))
            $ story_thread_advance_current()
            if _clara_evening_booklet_follow:
                $ story_thread_advance_current()
            jump MarketPlaceView
        "Не вмешиваться":
            if _clara_evening_booklet_follow:
                $ current_action_title = "Вечерний рынок"
                $ current_action_items = [MenuItem("Вернуться к своим делам", Call("MarketPlaceRestore"))]
            else:
                $ current_action_title = "Рынок"
                $ current_action_items = [MenuItem("Продолжить идти по рынку", Call("MarketPlaceRestore"))]
            $ current_action_content = None
            jump MarketPlaceView


label story_clara_market_booklet_confront:
    $ ClaraVar["booklet_market_seen"] = 1
    $ ClaraVar["drawings_secret_known"] = 1
    $ ClaraVar["merchant_contact_unlocked"] = 1
    $ _clara_market_bonus = 1
    if str(MyCurDress or "") == "thiefdress":
        $ _clara_market_bonus += 1
    if int(Friends.get("clara", 0) or 0) >= 7:
        $ _clara_market_bonus += 1
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + _clara_market_bonus)
    $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + max(1, _clara_market_bonus - 1))
    if str(MyCurDress or "") == "thiefdress" and int(Friends.get("clara", 0) or 0) >= 7:
        $ MainTxt = "Вы выходите из-за лотка без лишней суеты и даете Клариссе понять, что уже видели похожие непристойные рисунки у Мелиссы. На секунду она белеет, но, заметив ваш бандитский костюм и поняв, что вы не собираетесь устраивать сцену, быстро берет себя в руки.\n\nКларисса коротко просит не устраивать разговор прямо здесь, а таинственный торговец запоминает вас уже без прежней враждебности. Похоже, с этого дня он готов показывать вам свой особый товар не чаще раза в месяц, а сама Кларисса становится с вами заметно откровеннее."
    else:
        $ MainTxt = "Вы подходите ближе и спокойно даете понять Клариссе, что уже видели похожие непристойные рисунки и догадываетесь, чем она тут занимается. Девушка сразу напрягается, но, услышав, что вы не собираетесь ее выдавать, все же выдыхает.\n\nБез долгих разговоров Кларисса просит не поднимать шум на рынке. Торговец рядом молча запоминает вас взглядом. Похоже, теперь и он будет считать вас своим человеком, а сама Кларисса станет откровеннее лишь если решит, что вам действительно можно доверять."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_bookletDeal.png"):
        call ShowImage("", "", "images/clara/market_bookletDeal.png")
    $ current_action_title = "Кларисса и тайный торговец"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отойти и оставить их", Jump("MarketPlaceView"))]
    jump MarketPlaceView


label story_clara_market_action_direct:
    call preEvent("claraBookletMarket")
    python:
        _clara_target = ""
        _clara_thread = thread if 'thread' in globals() else None
        _booklet_seen = int(ClaraVar.get("booklet_market_seen", 0) or 0)
        _market_intro_seen = int(ClaraVar.get("market_intro_seen", 0) or 0)
        _market_evening_intro_seen = int(ClaraVar.get("market_evening_intro_seen", 0) or 0)
        _drawings_secret_known = int(ClaraVar.get("drawings_secret_known", 0) or 0)
        _mongol_theft_seen = int(ClaraVar.get("mongol_theft_seen", 0) or 0)
        _time_value = int(time or 0)

        if _time_value == 2 and _booklet_seen == 0:
            _clara_target = "story_clara_market_booklet_1_direct_follow"
            if _clara_thread is not None and int(_clara_thread.num or 0) < 1:
                if len(list(_clara_thread.done or [])) > 0:
                    _clara_thread.done[0] = True
                _clara_thread.num = 1
            if _market_intro_seen == 0:
                ClaraVar["market_intro_seen"] = 1
        elif _time_value == 3 and _booklet_seen == 0 and _drawings_secret_known == 1:
            _clara_target = "story_clara_market_booklet_1_direct_follow"
            if _clara_thread is not None and int(_clara_thread.num or 0) < 1:
                if len(list(_clara_thread.done or [])) > 0:
                    _clara_thread.done[0] = True
                _clara_thread.num = 1
        elif _time_value == 3 and _booklet_seen == 1 and _market_evening_intro_seen == 0:
            _clara_target = "story_clara_market_booklet_2_direct_follow"
            if _clara_thread is not None and int(_clara_thread.num or 0) < 2:
                if len(list(_clara_thread.done or [])) > 0:
                    _clara_thread.done[0] = True
                if len(list(_clara_thread.done or [])) > 1:
                    _clara_thread.done[1] = True
                _clara_thread.num = 2
        elif _time_value == 3 and _market_evening_intro_seen == 1 and _mongol_theft_seen == 0:
            _clara_target = "story_clara_market_booklet_3"
            if _clara_thread is not None and int(_clara_thread.num or 0) < 3:
                if len(list(_clara_thread.done or [])) > 0:
                    _clara_thread.done[0] = True
                if len(list(_clara_thread.done or [])) > 1:
                    _clara_thread.done[1] = True
                if len(list(_clara_thread.done or [])) > 2:
                    _clara_thread.done[2] = True
                _clara_thread.num = 3
        evalTime = None
        findAvailableEvents(True)
    if str(_clara_target or "") == "":
        call MarketPlaceRestore
        return
    jump expression _clara_target


label story_clara_market_booklet_1_direct_follow:
    $ SignalBlockTime = 1
    $ _clara_evening_booklet_follow = int(time or 0) == 3 and int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1
    if _clara_evening_booklet_follow and int(effective_player_exploration() or 0) < 100:
        $ MainTxt = "Вечерний рынок куда опаснее для слежки, чем дневной. Стоит вам зацепить чей-то ящик или лишний раз оглянуться, как Кларисса успевает скрыться в темном закутке и растворяется среди поздних покупателей.\n\nБез лучшей сноровки вы только выдадите себя и ничего не услышите."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Вечерний рынок"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться к своим делам", Call("MarketPlaceRestore"))]
        jump MarketPlaceView
    if (not _clara_evening_booklet_follow) and int(effective_player_exploration() or 0) < 80:
        $ MainTxt = "Вы стараетесь не отстать, но дневной рынок слишком шумный и тесный. Стоит вам замешкаться на пару шагов, как Кларисса ускользает между рядами и будто растворяется среди чужих спин.\n\nПохоже, без лучшей сноровки в слежке вы просто потеряете ее снова."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Рынок"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Продолжить идти по рынку", Call("MarketPlaceRestore"))]
        jump MarketPlaceView
    $ ClaraVar["booklet_market_seen"] = 1
    if _clara_evening_booklet_follow:
        $ ClaraVar["market_evening_intro_seen"] = 1
        $ MainTxt = "На этот раз вы не теряете Клариссу даже в вечерней толпе. Держась в тени, вы видите, как она подходит к неприметному торговцу, которому уже прежде, похоже, приносила товар. Несколько свернутых листков быстро переходят из ее рук в его ладонь, а потом вы успеваете расслышать главное: торговец ворчит, что непристойные книжечки у него разбирают быстрее обычного, и просит в следующий раз принести еще, пока у клиентов снова не кончились деньги.\n\nТеперь у вас нет сомнений. Кларисса действительно тайком сбывает через рынок свои непристойные рисунки и маленькие книжечки, а делает это давно и вполне уверенно."
    else:
        $ MainTxt = "На этот раз вы не теряете Клариссу в толпе. Держась в стороне, вы видите, как она сворачивает к неприметному торговцу, которого почти не видно с центральных рядов. Обмен короткий и явно привычный: Кларисса по одной передает ему тонкие книжечки, похожие на небольшие буклеты, а тот быстро сует их в сумку и так же быстро отсчитывает ей деньги.\n\nТеперь уже ясно, что речь идет не о простой прогулке по рынку. Кларисса что-то сбывает через этого таинственного торговца."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_bookletDeal.png"):
        call ShowImage("", "", "images/clara/market_bookletDeal.png")
    $ current_action_title = "Слежка на рынке"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Тихо уйти", Call("MarketPlaceRestore"))]
    if (not _clara_evening_booklet_follow) and (int(MelissaVar.get("drawings_found", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1):
        $ current_action_items.insert(0, MenuItem("Подойти к Клариссе и торговцу", Call("story_clara_market_booklet_confront")))
    $ story_thread_advance_current()
    if _clara_evening_booklet_follow:
        $ story_thread_advance_current()
    jump MarketPlaceView


label story_clara_market_booklet_2_direct_follow:
    $ SignalBlockTime = 1
    $ ClaraVar["market_evening_intro_seen"] = 1
    if int(effective_player_exploration() or 0) < 100:
        $ MainTxt = "Вечерний рынок куда опаснее для слежки, чем дневной. Стоит вам задеть чью-то корзину и чуть замешкаться, как Кларисса вместе с Монголом растворяются в темном закутке между пустеющими рядами. Без лучшей сноровки здесь их не удержать."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Вечерний рынок"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться к своим делам", Call("MarketPlaceRestore"))]
        jump MarketPlaceView
    $ story_thread_advance_current()
    jump story_clara_market_booklet_3


label story_clara_market_booklet_2:
    $ SignalBlockTime = 1
    $ ClaraVar["market_evening_intro_seen"] = 1
    $ MainTxt = "Вечером вы снова замечаете Клариссу на рынке. На этот раз видно, что она идет с конкретной целью. Стоит ей заметить ваш взгляд, как девушка чуть сильнее натягивает капюшон и быстро уходит в сторону закутка у конного торга.\n\nПохоже, на этот раз дело идет уже не о книжечках, а о чем-то более грязном."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_night.png"):
        call ShowImage("", "", "images/clara/market_night.png")
    elif renpy.loadable("images/market/LocMarketPlace2.jpg"):
        call ShowImage("", "", "images/market/LocMarketPlace2.jpg")
    menu:
        "Что сделать?"
        "Тихо проследить за Клариссой":
            if int(effective_player_exploration() or 0) < 100:
                $ MainTxt = "Вечерний рынок куда опаснее для слежки, чем дневной. Стоит вам задеть чью-то корзину и чуть замешкаться, как Кларисса вместе с Монголом растворяются в темном закутке между пустеющими рядами. Без лучшей сноровки здесь их не удержать."
                $ CurLocDesc = MainTxt
                $ current_action_title = "Вечерний рынок"
                $ current_action_content = None
                $ current_action_items = [MenuItem("Вернуться к своим делам", Call("MarketPlaceRestore"))]
                jump MarketPlaceView
            $ story_thread_advance_current()
            jump expression "story_clara_market_booklet_3"
        "Не рисковать":
            $ current_action_title = "Вечерний рынок"
            $ current_action_content = None
            $ current_action_items = [MenuItem("Вернуться к своим делам", Call("MarketPlaceRestore"))]
            jump MarketPlaceView


label story_clara_market_booklet_3:
    $ SignalBlockTime = 1
    $ MainTxt = "На этот раз вы держитесь достаточно далеко и не выдаете себя ни шагом, ни тенью. Кларисса уводит вас к самому краю рынка, где ее уже ждет Монгол. Разговор идет быстро и вполголоса, но вы успеваете разобрать главное.\n\nКларисса велит ему взять не первую попавшуюся клячу, а хорошую лошадь, чтобы потом продать ее с наваром. Деньги она требует делить честно, потому что именно она нашла покупателя и подсказала, где можно взять товар так, чтобы шум поднялся не сразу. Монгол в ответ ухмыляется, обещает свою долю и, будто нарочно, поддевает ее, что в ее любимом бандитском костюме она выглядела бы среди его людей вовсе как своя.\n\nТеперь уже ясно, что Кларисса не просто прячет от вас книжечки. Она сознательно полезла в настоящую грязь."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_night.png"):
        call ShowImage("", "", "images/clara/market_night.png")
    elif renpy.loadable("images/market/mistery_merchant.png"):
        call ShowImage("", "", "images/market/mistery_merchant.png")
    $ ClaraVar["mongol_theft_seen"] = 1
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + 1)
    if renpy.loadable("images/clara/mongolTalk.png"):
        call ShowImage("", "", "images/clara/mongolTalk.png")
    $ current_action_title = "Подслушанный сговор"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Запомнить услышанное и уйти", Call("MarketPlaceRestore"))]
    $ story_thread_advance_current()
    jump MarketPlaceView


label story_clara_market_booklet_4:
    $ SignalBlockTime = 1
    $ ClaraVar["escape_confessed"] = 1
    $ ClaraVar["drawings_secret_known"] = 1
    $ _clara_escape_bonus = 1
    if str(MyCurDress or "") == "thiefdress":
        $ _clara_escape_bonus += 1
    if int(Friends.get("clara", 0) or 0) >= 7:
        $ _clara_escape_bonus += 1
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + _clara_escape_bonus)
    $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + max(1, _clara_escape_bonus - 1))
    $ MainTxt = "Вы дожидаетесь удобного момента и без окриков говорите Клариссе, что видели ее вечерний разговор с Монголом. Девушка сначала белеет, потом зло сжимает губы, но быстро понимает, что вы пришли не сдавать ее отцу.\n\n\"Да, это я его подбила,\" признается она наконец. \"Мне нужны деньги. Отец уже подбирает мне старого хрыча в столице, и весь этот брак будет не для меня, а для его торговли. Я не собираюсь ехать туда смирной куклой.\" Она нервно усмехается и добавляет, что книжечки, рисунки и все разговоры про свободу для нее давно перестали быть просто романтической чушью. \"Хочется хоть раз жить не по чужому счету. А Монгол обещал, что если я соберу достаточно денег, то в его тайном кругу мне найдут место. Хоть кем. Хоть рисовальщицей, хоть этой их девкой для сценок. Знаю, звучит грязно. Но это все равно лучше, чем лечь под старого вонючего дурака по приказу отца.\"\n\nСказав это, Кларисса смотрит на вас уже не как на случайного покупателя, а как на человека, который теперь знает слишком много."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/mongolTalk.png"):
        call ShowImage("", "", "images/clara/mongolTalk.png")
    $ current_action_title = "Откровение Клариссы"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Оставить услышанное между вами", Call("IntClaraTalkRefresh", "clara"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_wine_talk_direct:
    call preEvent("claraBookletMarket")
    python:
        _clara_thread = thread if 'thread' in globals() else None
        if _clara_thread is not None and int(_clara_thread.num or 0) < 4:
            if len(list(_clara_thread.done or [])) > 0:
                _clara_thread.done[0] = True
            if len(list(_clara_thread.done or [])) > 1:
                _clara_thread.done[1] = True
            if len(list(_clara_thread.done or [])) > 2:
                _clara_thread.done[2] = True
            if len(list(_clara_thread.done or [])) > 3:
                _clara_thread.done[3] = True
            _clara_thread.num = 4
        evalTime = None
        findAvailableEvents(True)
    jump story_clara_market_booklet_4


label story_clara_market_booklet_5:
    $ SignalBlockTime = 1
    $ MongolVar["StocksArrestDay"] = int(dayspassed or 0)
    $ MainTxt = "Едва вы входите в охотничий клуб, как из угла до вас доносится горячий пересказ свежей городской новости. Охотники с явным удовольствием обсуждают, как стража наконец-то сцапала конокрада, слишком уж долго крутившегося вокруг рынка и конного торга.\n\n\"Сидит теперь у караулки в колодках, вместе с парой таких же голодранцев,\" хмыкает один. \"Пусть народ посмотрит, может поумнеют.\" Другой замечает, что десятник Циммерман теперь ходит важный, как будто сам лично всю шайку выволок за шкирку.\n\nСудя по обрывкам слов, речь идет о Монголе."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/general/hunter_store_catInfo.png"):
        call ShowImage("", "", "images/general/hunter_store_catInfo.png")
    $ current_action_title = "Охотничьи слухи"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Идти проверить колодки у караулки", Jump("CityGuard")), MenuItem("Остаться в охотничьем клубе", Call("HunterClubRestore"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_hunter_direct:
    call preEvent("claraBookletMarket")
    python:
        _clara_thread = thread if 'thread' in globals() else None
        if _clara_thread is not None and int(_clara_thread.num or 0) < 5:
            for _clara_index in range(min(5, len(list(_clara_thread.done or [])))):
                _clara_thread.done[_clara_index] = True
            _clara_thread.num = 5
        evalTime = None
        findAvailableEvents(True)
    jump story_clara_market_booklet_5


label story_clara_market_booklet_6:
    $ SignalBlockTime = 1
    $ MongolVar["StocksSeen"] = 1
    $ MainTxt = "У караулки, прямо рядом с входом, стоят тяжелые колодки. В них вместе с еще парой помятых головорезов сидит и Монгол. От прежней ярмарочной ухмылки в нем мало что осталось: губа разбита, рубаха грязная, но глаза все еще бегают живо.\n\nЗаметив вас, он дергается и шипит сквозь зубы: \"Стефан, брат, не губи. Я тут с голоду загнусь раньше, чем меня судить начнут. Принеси ночью пожрать, а там, может, и поговорим. Я добро помню. И про Клариссу тоже помню.\""
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/mongolStock.png"):
        call ShowImage("", "", "images/mongolStock.png")
    $ current_action_title = "Монгол в колодках"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Запомнить его просьбу", Call("CityGuardRestore"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_city_guard_direct:
    call preEvent("claraBookletMarket")
    python:
        _clara_thread = thread if 'thread' in globals() else None
        if _clara_thread is not None and int(_clara_thread.num or 0) < 6:
            for _clara_index in range(min(6, len(list(_clara_thread.done or [])))):
                _clara_thread.done[_clara_index] = True
            _clara_thread.num = 6
        evalTime = None
        findAvailableEvents(True)
    jump story_clara_market_booklet_6


label story_clara_market_booklet_7:
    $ SignalBlockTime = 1
    $ MainTxt = "Ночью у караулки тихо, только где-то внутри переговариваются сонные стражи. Монгол в колодках шевелится и, увидев вас, сразу подается вперед.\n\n\"Ну что, принес чего-нибудь?\" шепчет он. \"Я тут второй день на одной воде. Помоги сейчас, и я потом не забуду.\""
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/mongolStock.png"):
        call ShowImage("", "", "images/mongolStock.png")
    $ current_action_title = "Ночная караулка"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Уйти и вернуться позже", Call("CityGuardRestore"))]
    if int(productnum or 0) > 0:
        $ current_action_items.insert(0, MenuItem("Передать Монголу еду из трактира", Call("story_clara_market_booklet_feed_mongol")))
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label story_clara_market_booklet_feed_mongol:
    $ productnum = max(0, int(productnum or 0) - 1)
    $ MongolVar["StocksFoodDay"] = int(dayspassed or 0)
    $ MainTxt = "Вы незаметно протягиваете Монголу завернутую в тряпицу еду из трактирной кухни. Тот жадно хватается за нее обеими руками, давится первыми кусками и тут же начинает шептать благодарности.\n\n\"Вот это по-людски, Стефан. Еще бы отмычки добыть, да стражу чем-нибудь отвлечь... Тогда я не просто вылезу, а еще и твой долг запомню. Если потом занесет к людям Робина, скажу им, кто ты такой.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ночная караулка"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Оставить Монгола жевать в темноте", Call("CityGuardRestore"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_feed_mongol_direct:
    call preEvent("claraBookletMarket")
    python:
        _clara_thread = thread if 'thread' in globals() else None
        if _clara_thread is not None and int(_clara_thread.num or 0) < 7:
            for _clara_index in range(min(7, len(list(_clara_thread.done or [])))):
                _clara_thread.done[_clara_index] = True
            _clara_thread.num = 7
        evalTime = None
        findAvailableEvents(True)
    jump story_clara_market_booklet_feed_mongol


label story_clara_market_booklet_8:
    $ SignalBlockTime = 1
    $ MainTxt = "Вы находите Драупнира за верстаком и без лишней прямоты объясняете, что вам нужны очень тонкие отмычки. Гном сперва косится на вас с подозрением, потом только фыркает.\n\n\"Ничего не знаю и знать не хочу, для какой двери тебе такая железяка,\" ворчит он. \"Но если работа тонкая и молчаливая, то это ко мне. За сорок мараведи сделаю хороший набор, который и в сапог спрятать не стыдно.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Заказ у Драупнира"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Не заказывать пока", Call("StolyarWorkshopBuildActions"))]
    if int(money or 0) >= 40:
        $ current_action_items.insert(0, MenuItem("Заплатить 40 мараведи за тонкие отмычки", Call("story_clara_market_booklet_lockpicks_order")))
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label story_clara_market_booklet_lockpicks_order:
    $ money = int(money or 0) - 40
    $ DraupnirVar["MongolLockpickOrderDay"] = int(dayspassed or 0)
    $ MainTxt = "Драупнир быстро прячет деньги, вытаскивает из ящика тонкий кожаный сверток и сует его вам почти не глядя.\n\n\"Вот. Только если с этим полезешь куда не надо, не вздумай потом ссылаться на меня,\" бурчит гном. Судя по тяжести свертка, набор отмычек у вас теперь есть."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Заказ у Драупнира"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Спрятать сверток и уйти", Call("StolyarWorkshopBuildActions"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_lockpicks_order_direct:
    call preEvent("claraBookletMarket")
    python:
        _clara_thread = thread if 'thread' in globals() else None
        if _clara_thread is not None and int(_clara_thread.num or 0) < 8:
            for _clara_index in range(min(8, len(list(_clara_thread.done or [])))):
                _clara_thread.done[_clara_index] = True
            _clara_thread.num = 8
        evalTime = None
        findAvailableEvents(True)
    jump story_clara_market_booklet_lockpicks_order


label story_clara_market_booklet_9:
    $ SignalBlockTime = 1
    $ MainTxt = "Следующей ночью вы возвращаетесь к караулке уже подготовленным. Монгол сразу понимает это по вашему лицу и только сильнее вжимается в колодки, чтобы не привлекать лишних взглядов.\n\nТеперь все упирается в одно: если вы хотите вытащить его отсюда, надо сперва умаслить стражу и отвлечь ее чем-то приятнее ночного дежурства."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/mongolStock.png"):
        call ShowImage("", "", "images/mongolStock.png")
    $ current_action_title = "Побег Монгола"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Передумать и уйти", Call("CityGuardRestore"))]
    if int(productnum or 0) > 0 and int(winenum or 0) > 0:
        $ current_action_items.insert(0, MenuItem("Послать стражникам вино и угощение, а затем освободить Монгола", Call("story_clara_market_booklet_release_mongol")))
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label story_clara_market_booklet_release_mongol:
    $ productnum = max(0, int(productnum or 0) - 1)
    $ winenum = max(0, int(winenum or 0) - 1)
    $ tavernfame = int(tavernfame or 0) + 2
    $ notoriety = min(100, int(notoriety or 0) + 2)
    $ Friends["zimmer"] = min(20, int(Friends.get("zimmer", 0) or 0) + 1)
    $ MongolVar["GuardGiftSent"] = 1
    $ MongolVar["GuardCaptainKnown"] = 1
    $ MongolVar["StocksReleased"] = 1
    $ RobinVar["MongolSafePass"] = 1
    $ MainTxt = "Вы заранее посылаете к караулке кувшин вина и хороший ужин из трактира с вежливой припиской: мол, \"Дикий Жеребец\" благодарит городскую стражу за поимку конокрадов. Стража мгновенно добреет к такой заботе. Сам десятник Циммерман замечает, что вот это уже разговор с уважаемым трактирщиком, который умеет ценить порядок в городе.\n\nКогда угощение делает свое дело и дежурные окончательно расслабляются, вы выбираете момент, приседаете к колодкам и пускаете в ход заказанные у Драупнира отмычки. Замок поддается не сразу, но все же тихо щелкает. Монгол выскальзывает из дерева, как уж, шепотом сыплет вам благодарностями и обещает, что люди Робина в Шервуде узнают, кому он обязан свободой.\n\nЕще до рассвета его и след простыл."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Побег Монгола"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Раствориться в ночи", Call("CityGuardRestore"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_release_mongol_direct:
    call preEvent("claraBookletMarket")
    python:
        _clara_thread = thread if 'thread' in globals() else None
        if _clara_thread is not None and int(_clara_thread.num or 0) < 9:
            for _clara_index in range(min(9, len(list(_clara_thread.done or [])))):
                _clara_thread.done[_clara_index] = True
            _clara_thread.num = 9
        evalTime = None
        findAvailableEvents(True)
    jump story_clara_market_booklet_release_mongol


label story_melissa_werecat_intro_0:
    $ SignalBlockTime = 1
    call MelissaRatBreakfastScene
    $ story_thread_advance_current()
    jump TavernKitchen


label story_melissa_werecat_rumor_0:
    $ SignalBlockTime = 1
    call WerecatHunterClubTease
    $ story_thread_advance_current()
    jump HunterClub


label story_melissa_storage_rat_0:
    $ SignalBlockTime = 1
    call TavernStorageRatEvent
    $ story_thread_advance_current()
    jump TavernStorageView


label story_melissa_werecat_home_0:
    $ SignalBlockTime = 1
    call WerecatAdoptionBreakfastScene
    $ story_thread_advance_current()
    jump TavernKitchen


label story_melissa_werecat_home_1:
    $ SignalBlockTime = 1
    call WerecatMonthThanksScene
    $ story_thread_advance_current()
    jump TavernKitchen


label story_melissa_bat_problem_0:
    $ SignalBlockTime = 1
    call MelissaBatBreakfastScene
    $ story_thread_advance_current()
    jump TavernKitchen


label story_melissa_bat_problem_1:
    $ SignalBlockTime = 1
    call MelissaNightNoiseScene
    jump TavernUpstairsView


label story_melissa_bat_problem_2:
    $ SignalBlockTime = 1
    call MelissaAtticColonySearch
    $ story_thread_advance_current()
    call TavernAticBuildActions
    jump TavernAticView


label story_melissa_bat_problem_3:
    $ SignalBlockTime = 1
    call MelissaAtticWindowPeek
    jump TavernAticView


label story_melissa_bat_problem_4:
    $ SignalBlockTime = 1
    if melissa_bats_stage() < 7 and int(_player_item_count_by_id("bat_repellent_001") or 0) > 0:
        call MelissaBurnAtticColony
    elif melissa_bats_stage() >= 7:
        call MelissaOrderRoofRepair
    else:
        call MelissaAtticCleanupScene
    jump TavernAticView


label story_melissa_bat_problem_5:
    $ SignalBlockTime = 1
    call MelissaFindDrawingsScene
    $ story_thread_advance_current()
    jump TavernAmandaRoomView


label story_melissa_bat_problem_6:
    $ SignalBlockTime = 1
    call MelissaBatsCompletionScene
    $ story_thread_advance_current()
    jump TavernMainView
