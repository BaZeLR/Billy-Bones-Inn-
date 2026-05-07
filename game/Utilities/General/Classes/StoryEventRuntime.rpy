# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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
default eventPath = set()
default eventProjectionRows = []
default eventRouteHints = {}
default story_thread_levels = {}

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

    def _story_current_location():
        return str(_story_named_value("CurLoc", _story_named_value("location", "")) or "")

    def _story_map_int(map_name, key, default=0):
        source = _story_named_value(map_name, {})
        try:
            return _story_to_int(source.get(key, default), default)
        except Exception:
            return default

    def _story_condition_scope():
        scope = {}
        for key, value in dict(globals()).items():
            if str(key or "").startswith("_"):
                continue
            scope[key] = value
        scope.update({
            "bool": bool,
            "float": float,
            "int": int,
            "len": len,
            "max": max,
            "min": min,
            "str": str,
        })
        return scope

    def _story_relationship_level(person):
        key = str(person or "").strip().lower()
        if key == "":
            return 0
        rel_fn = _story_named_callable("npc_relationship_level")
        if callable(rel_fn):
            try:
                profile = dict(rel_fn(key) or {})
                return _story_to_int(profile.get("phase_index", 0), 0)
            except Exception:
                pass
        friends_map = _story_named_value("Friends", {})
        corruption_map = _story_named_value("sluttiness", {})
        try:
            friend_value = _story_to_int(friends_map.get(key, 0), 0)
        except Exception:
            friend_value = 0
        try:
            corruption_value = _story_to_int(corruption_map.get(key, 0), 0)
        except Exception:
            corruption_value = 0
        if friend_value >= 15 and corruption_value >= 55:
            return 6
        if friend_value >= 11 and corruption_value >= 35:
            return 5
        if friend_value >= 8 and corruption_value >= 20:
            return 4
        if friend_value >= 11:
            return 3
        if friend_value >= 8:
            return 2
        if friend_value >= 5:
            return 1
        return 0

    def _story_level_enabled(level, person=None):
        required_level = _story_to_int(level, 0)
        person_key = str(person or "").strip().lower()
        if required_level <= 0:
            return True
        if person_key and person_key not in ("event", "story", "system"):
            return _story_relationship_level(person_key) >= required_level
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

    def _story_thread_lookup(thread_name):
        key = str(thread_name or "").strip()
        if key == "":
            return None
        current_threads = _story_named_value("threads", {})
        if isinstance(current_threads, dict) and key in current_threads:
            return current_threads[key]
        return None

    def _story_thread_step_lookup(token):
        text = str(token or "").strip()
        if "_" not in text:
            return (None, None)
        thread_name, step_text = text.rsplit("_", 1)
        try:
            step_index = int(step_text)
        except Exception:
            return (None, None)
        thread_info = _story_thread_lookup(thread_name)
        if thread_info is None:
            return (None, None)
        return (thread_info, step_index)

    def _story_split_enabler(enabler):
        if not enabler:
            return None
        thread_info, step_index = _story_thread_step_lookup(enabler)
        if thread_info is not None:
            return (thread_info, step_index)
        thread_info = _story_thread_lookup(enabler)
        if thread_info is not None:
            return (thread_info, 0)
        return None

    class StoryCondition(object):
        def show(self):
            return "{color=#%s}%s{/color}" % ("0f0" if self.eval() else "f00", str(self))

        def eval(self):
            return False

        def blocked(self):
            return False

    class StoryConditionExpression(StoryCondition):
        def __init__(self, expression, enabler=None):
            self.expression = expression
            self.enabler = _story_split_enabler(enabler)

        def __str__(self):
            return str(self.expression)

        def eval(self):
            return _story_eval_condition(self.expression)

        def blocked(self):
            if self.eval():
                return False
            if self.enabler is None:
                return False
            enabler_thread, enabler_index = self.enabler
            try:
                return bool(enabler_thread.blocks[enabler_index])
            except Exception:
                return False

    class StoryConditionCallable(StoryConditionExpression):
        def __str__(self):
            return getattr(self.expression, "__name__", str(self.expression)).replace("_", " ")

    class StoryConditionCompleted(StoryCondition):
        def __init__(self, thread_name):
            self.thread_name = str(thread_name or "")
            self.thread = _story_thread_lookup(self.thread_name)

        def __str__(self):
            return "thread %s done" % self.thread_name

        def eval(self):
            return bool(self.thread is not None and self.thread.completed)

        def blocked(self):
            if self.eval():
                return False
            if self.thread is None:
                return True
            try:
                return bool(self.thread.blocks[-1])
            except Exception:
                return None

    class StoryConditionNotCompleted(StoryConditionCompleted):
        def __str__(self):
            return "thread %s not done" % self.thread_name

        def eval(self):
            return bool(self.thread is not None and not self.thread.completed)

        def blocked(self):
            if self.thread is None:
                return True
            return True if self.thread.completed else False

    class StoryConditionAborted(StoryConditionCompleted):
        def __str__(self):
            return "thread %s aborted" % self.thread_name

        def eval(self):
            return bool(self.thread is not None and self.thread.aborted)

        def blocked(self):
            return False

    class StoryConditionEnabled(StoryCondition):
        def __init__(self, thread_name, enabler=None):
            self.thread_name = str(thread_name or "")
            self.thread = _story_thread_lookup(self.thread_name)
            self.enabler = _story_split_enabler(enabler)

        def __str__(self):
            return "thread %s enabled" % self.thread_name

        def eval(self):
            return bool(self.thread is not None and self.thread.enabled)

        def blocked(self):
            if self.eval():
                return False
            if self.enabler is None:
                return False
            enabler_thread, enabler_index = self.enabler
            try:
                if enabler_thread.done[enabler_index]:
                    return True
                return bool(enabler_thread.blocks[enabler_index])
            except Exception:
                return None

    class StoryConditionProgress(StoryCondition):
        def __init__(self, thread_name, step_index):
            self.thread_name = str(thread_name or "")
            self.thread = _story_thread_lookup(self.thread_name)
            self.step_index = int(step_index)

        def __str__(self):
            return "event %s %d done" % (self.thread_name, self.step_index)

        def eval(self):
            try:
                return bool(self.thread is not None and self.thread.done[self.step_index])
            except Exception:
                return False

        def blocked(self):
            if self.eval():
                return False
            try:
                return bool(self.thread.blocks[self.step_index])
            except Exception:
                return None

    class StoryConditionNotProgress(StoryConditionProgress):
        def __str__(self):
            return "event %s %d not done" % (self.thread_name, self.step_index)

        def eval(self):
            try:
                return bool(self.thread is not None and not self.thread.done[self.step_index])
            except Exception:
                return False

        def blocked(self):
            try:
                return True if self.thread.done[self.step_index] else False
            except Exception:
                return None

    class StoryConditionAt(StoryConditionProgress):
        def __str__(self):
            return "thread %s at event %d" % (self.thread_name, self.step_index)

        def eval(self):
            return bool(self.thread is not None and self.thread.num == self.step_index)

        def blocked(self):
            if self.thread is None:
                return True
            if self.thread.num == self.step_index:
                return False
            if self.thread.num > self.step_index:
                return True
            if self.step_index > 0:
                try:
                    return bool(self.thread.blocks[self.step_index - 1])
                except Exception:
                    return None
            return self.thread.blocked

    class StoryConditionNotAt(StoryConditionAt):
        def __str__(self):
            return "thread %s not at event %d" % (self.thread_name, self.step_index)

        def eval(self):
            return bool(self.thread is not None and self.thread.num != self.step_index)

        def blocked(self):
            if self.eval():
                return False
            try:
                return bool(self.thread.blocks[self.step_index])
            except Exception:
                return None

    def makeConditions(cond_source):
        if cond_source in (None, "", []):
            return []
        if isinstance(cond_source, list):
            return [makeConditionT(item) for item in cond_source]
        if isinstance(cond_source, set):
            return [makeConditionT(item) for item in list(cond_source)]
        return [makeConditionT(cond_source)]

    def makeConditionT(cond_source):
        if isinstance(cond_source, tuple):
            condition = cond_source[0] if len(cond_source) > 0 else None
            enabler = cond_source[1] if len(cond_source) > 1 else None
            return makeCondition(condition, enabler)
        return makeCondition(cond_source, None)

    def makeCondition(condition, enabler=None):
        if callable(condition):
            return StoryConditionCallable(condition, enabler)
        text = str(condition or "").strip()
        if text == "" or text == "always":
            return StoryConditionExpression(True, enabler)
        if text.startswith("#"):
            return StoryConditionExpression(text[1:], enabler)
        if text.endswith("Done"):
            if text.startswith("!"):
                return StoryConditionNotCompleted(text[1:-4])
            if _story_thread_lookup(text[:-4]) is not None:
                return StoryConditionCompleted(text[:-4])
        if text.endswith("Aborted") and _story_thread_lookup(text[:-7]) is not None:
            return StoryConditionAborted(text[:-7])
        if text.endswith("Enabled") and _story_thread_lookup(text[:-7]) is not None:
            return StoryConditionEnabled(text[:-7], enabler)
        fields = text.split()
        if len(fields) == 1 and "_" in text:
            invert = text.startswith("!")
            thread_info, step_index = _story_thread_step_lookup(text[1:] if invert else text)
            if thread_info is not None:
                thread_name = thread_info.data.name
                if invert:
                    return StoryConditionNotProgress(thread_name, step_index)
                return StoryConditionProgress(thread_name, step_index)
        if len(fields) == 3 and fields[0].endswith("Num") and fields[1] in ("==", "!="):
            thread_name = fields[0][:-3]
            if _story_thread_lookup(thread_name) is not None:
                if fields[1] == "==":
                    return StoryConditionAt(thread_name, _story_to_int(fields[2], 0))
                return StoryConditionNotAt(thread_name, _story_to_int(fields[2], 0))
        return StoryConditionExpression(condition, enabler)

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
            if rv is False:
                return False
            if rv is None:
                has_none = True
        if has_none:
            return None
        return True

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
            current_hour = _story_named_number("time", _story_named_number("hour", 0))
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
            if not _story_level_enabled(self.data.level, self.data.person):
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

        def forceEnable(self):
            self.metconds = True
            self.enabled = True
            self.blocked = False
            self.aborted = False
            self.completed = False
            try:
                self.blocks = [False] * int(self.data.length or 0)
            except Exception:
                self.blocks = []

        def advanceTo(self, num, complete_at_end=False, force_active=False):
            target = max(0, min(_story_to_int(num, 0), int(self.data.length or 0)))
            self.adjustLen()
            for index in range(len(self.done)):
                self.done[index] = index < target
            self.num = target
            if force_active:
                self.forceEnable()
            elif target < int(self.data.length or 0):
                self.completed = False
            elif complete_at_end:
                self.completed = True
            return self.num

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

    def story_sync_melissa_rat_solution_thread():
        try:
            tinfo = threads.get("melissaRatSolution", None)
        except Exception:
            tinfo = None
        if tinfo is None:
            return
        target_num = 0
        if _story_map_int("MelissaVar", "storage_rat_cleared", 0) == 1:
            target_num = max(target_num, 1)
        if _story_map_int("WerecatVar", "rat_breakfast_seen", 0) == 1:
            target_num = max(target_num, 2)
        if _story_map_int("WerecatVar", "hunter_tease_day", -1) >= 0:
            target_num = max(target_num, 3)
        if _story_map_int("WerecatVar", "adoption_breakfast_seen", 0) == 1:
            target_num = max(target_num, 4)
        if _story_map_int("WerecatVar", "first_month_thanks_day", -1) >= 0:
            target_num = max(target_num, 5)
        if target_num <= 0:
            return
        try:
            if target_num > int(getattr(tinfo, "num", 0) or 0):
                tinfo.advanceTo(target_num, complete_at_end=True)
        except Exception:
            pass

    def initThreads():
        global threads
        current_threads = _story_named_value("threads", {})
        if not isinstance(current_threads, dict):
            current_threads = {}
        thread_renames = {
            "melissaRatProblem": "melissaRatSolution",
            "werecatRatProblem": "melissaRatSolution",
            "werecatRatSolution": "melissaRatSolution",
            "melissaWerecatRumor": "melissaRatSolution",
            "werecatWerecatRumor": "melissaRatSolution",
            "melissaWerecatIntro": "melissaRatSolution",
            "werecatWerecatIntro": "melissaRatSolution",
            "melissaWerecatHome": "melissaRatSolution",
            "werecatWerecatHome": "melissaRatSolution",
        }
        for old_name, new_name in dict(thread_renames).items():
            if old_name in current_threads:
                if new_name not in current_threads:
                    current_threads[new_name] = current_threads[old_name]
                try:
                    del current_threads[old_name]
                except Exception:
                    pass
        for name, tdata in dict(threadData or {}).items():
            if name not in current_threads:
                current_threads[name] = createThread(tdata)
            else:
                current_threads[name].data = tdata
                current_threads[name].adjustLen()
        for _name, tdata in dict(threadData or {}).items():
            tdata.initConditions()
        threads = current_threads
        story_sync_melissa_rat_solution_thread()

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
        try:
            tinfo = dict(threads or {}).get(thread_name, None)
            data = getattr(tinfo, "data", None)
            person = str(getattr(data, "person", "") or "").strip().lower()
            if person and person not in ("event", "story", "system"):
                return person
        except Exception:
            pass
        return ""

    def _story_person_location(person):
        key = str(person or "").strip().lower()
        if not key:
            return ""
        try:
            loc = getLocation(key)
            if loc:
                return str(loc)
        except Exception:
            pass
        try:
            return str(CurrentLoc.get(key, "") or "")
        except Exception:
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
        try:
            room_obj = get_registered_room(room_key)
        except Exception:
            room_obj = None
        if room_obj is None:
            return []
        out = []
        try:
            exits = list(room_obj.visible_exits())
        except Exception:
            exits = list(getattr(room_obj, "exits", []) or [])
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
        global eventLocations, eventPeople, eventTalk, eventOptions, eventItems
        global eventPath, eventProjectionRows, eventRouteHints

        current_location = str(_story_named_value("CurLoc", _story_named_value("location", "")) or "").strip()
        eventLocations = set()
        eventPeople = set()
        eventTalk = set()
        eventOptions = set()
        eventItems = set()
        eventPath = set()
        eventProjectionRows = []
        eventRouteHints = {}

        for raw_location, action_map in sorted(dict(availEvents or {}).items()):
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
                    eventLocations.add(projected_location)
                    if first_step:
                        eventPath.add(first_step)
                        eventRouteHints[projected_location] = first_step
                if person_key:
                    eventPeople.add(person_key)
                if location_key.startswith("talk_") or location_key == "talk" or action_key.endswith("_talk"):
                    if person_key:
                        eventTalk.add(person_key)
                if action_key and action_key not in ("enter", "sleep"):
                    eventOptions.add(action_key)
                if missing_item:
                    eventItems.add(str(getattr(evt, "item", "") or ""))

                eventProjectionRows.append({
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
        try:
            findAvailableEvents(False)
        except Exception:
            pass
        return list(eventProjectionRows or [])

    def story_event_path_targets():
        try:
            findAvailableEvents(False)
        except Exception:
            pass
        return set(eventPath or set())

    def story_event_location_has_signal(location_name=""):
        key = str(location_name or "").strip()
        if not key:
            return False
        try:
            findAvailableEvents(False)
        except Exception:
            pass
        return key in set(eventLocations or set()) or key in set(eventPath or set())

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

        _story_project_available_events()
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

define amandaThreadList = []

define melissaThreadList = [
    #
    # melissa_rat_solution_arc
    #
    # Event tuple columns:
    # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
    #
    LThreadData(0, "melissa", "RatSolution", None, [
        (
            "story_melissa_storage_rat_0",
            (1, 6), 0, None,
            1,
            None,
            [
                "#int(MelissaVar.get('storage_rat_cleared', 0) or 0) == 0",
                "#str(getLocation('melissa') or '') == 'TavernStorage'",
                "#not household_runtime_event_seen_today('melissa_storage_rat')",
            ],
            None,
            "TavernStorage",
            "enter",
            0,
        ),
        (
            "story_melissa_werecat_rumor_0",
            None, None, None,
            1,
            None,
            [
                "#not (int(WerecatVar.get('sold', 0) or 0) == 0 and int(WerecatVar.get('adopted_count', 0) or 0) >= 1)",
                "#int(WerecatVar.get('rats_problem_active', 0) or 0) == 1",
                "#int(MelissaVar.get('storage_rat_cleared', 0) or 0) == 1",
                "#int(MelissaVar.get('storage_rat_last_help_day', -1) or -1) >= 0",
                "#int(WerecatVar.get('adopted', 0) or 0) == 0",
                "#int(WerecatVar.get('sold', 0) or 0) == 0",
                "#int(WerecatVar.get('hunter_tease_day', -1) or -1) < 0",
            ],
            None,
            "HunterClub",
            "overheard",
            1,
        ),
        (
            "story_melissa_werecat_intro_0",
            (1, 7), 0, None,
            1,
            None,
            [
                "#int(WerecatVar.get('rats_problem_active', 0) or 0) == 1",
                "#int(WerecatVar.get('rat_breakfast_seen', 0) or 0) == 0",
                "#int(WerecatVar.get('hunter_tease_day', -1) or -1) >= 0",
                "#not bool(BreakfastToday)",
            ],
            None,
            "TavernKitchen",
            "enter",
            2,
        ),
        (
            "story_melissa_werecat_home_0",
            (1, 7), 0, None,
            1,
            None,
            [
                "#int(WerecatVar.get('adopted', 0) or 0) == 1",
                "#int(WerecatVar.get('adoption_breakfast_seen', 0) or 0) == 0",
                "#int(WerecatVar.get('adopted_day', -1) or -1) >= 0",
                "#int(dayspassed or 0) > int(WerecatVar.get('adopted_day', -1) or -1)",
                "#not bool(BreakfastToday)",
            ],
            None,
            "TavernKitchen",
            "enter",
            3,
        ),
        (
            "story_melissa_werecat_home_1",
            (1, 7), 0, None,
            1,
            None,
            [
                "#int(WerecatVar.get('adopted', 0) or 0) == 1",
                "#int(WerecatVar.get('adoption_breakfast_seen', 0) or 0) == 1",
                "#int(WerecatVar.get('adopted_day', -1) or -1) >= 0",
                "#int(dayspassed or 0) >= int(WerecatVar.get('adopted_day', -1) or -1) + 30",
                "#int(WerecatVar.get('first_month_thanks_day', -1) or -1) < int(WerecatVar.get('adopted_day', -1) or -1) + 30",
                "#not bool(BreakfastToday)",
            ],
            None,
            "TavernKitchen",
            "enter",
            4,
        ),
    ], highlight=False, threaded=True),
    # bats_problem_thread
    # Rat cleanup in storage is the household trigger; this ordered bat problem
    # starts at the next available breakfast.
    LThreadData(0, "melissa", "BatProblem", "melissaRatSolution_0", [
        (
            "story_melissa_bat_problem_0",
            (1, 7), 0, None,
            1,
            None,
            [
                "#melissa_bats_stage() <= 0",
                "#int(MelissaVar.get('storage_rat_last_help_day', -1) or -1) >= 0",
                "#not bool(BreakfastToday)",
            ],
            None,
            "TavernKitchen",
            "enter",
            0,
        ),
        (
            "story_melissa_bat_problem_1",
            None, 4, None,
            1,
            None,
            [
                "#melissa_bats_stage() == 1",
            ],
            None,
            "TavernUpstairs",
            "enter",
            1,
        ),
        (
            "story_melissa_bat_problem_2",
            None, None, None,
            1,
            None,
            [
                "#melissa_bats_stage() == 3",
                "#int(dayspassed or 0) >= int(MelissaVar.get('bat_attic_check_day', -1) or -1)",
            ],
            None,
            "TavernAtic",
            "melissa_bats",
            2,
        ),
        (
            "story_melissa_bat_problem_3",
            None, None, None,
            1,
            None,
            [
                "#melissa_bats_stage() in (4, 5)",
            ],
            None,
            "TavernAtic",
            "melissa_bats",
            3,
        ),
        (
            "story_melissa_bat_problem_5",
            None, None, None,
            1,
            None,
            [
                "#melissa_bats_stage() >= 6",
                "#melissa_bats_stage() < 8",
                "#str(MelissaVar.get('temp_room', '') or '') == 'TavernAmandaRoom'",
                "#int(MelissaVar.get('drawings_found', 0) or 0) == 0",
                "#int(dayspassed or 0) >= int(MelissaVar.get('drawings_ready_day', -1) or -1)",
            ],
            None,
            "TavernMelissaRoom",
            "room_search",
            4,
        ),
        (
            "story_melissa_bat_problem_4",
            None, None, None,
            1,
            None,
            [
                "#melissa_bats_stage() >= 6",
                "#melissa_bats_stage() < 8",
            ],
            None,
            "TavernAtic",
            "melissa_bats",
            5,
        ),
        (
            "story_melissa_bat_problem_6",
            None, None, None,
            1,
            None,
            [
                "#melissa_bats_stage() == 7",
                "#int(MelissaVar.get('roof_repair_complete_day', -1) or -1) >= 0",
                "#int(dayspassed or 0) >= int(MelissaVar.get('roof_repair_complete_day', -1) or -1)",
                "#int(MelissaVar.get('drawings_returned', 0) or 0) == 1",
            ],
            None,
            "TavernMain",
            "melissa_talk",
            6,
        ),
    ], highlight=False, threaded=True),
    #
    # melissa_clarissa_overheard_lead
    #
    LThreadData(0, "melissa", "ClaraOverheard", None, [
        (
            "melissaClaraOverheard_0",
            None, 2, None,
            1,
            None,
            [
                "#str(getLocation('melissa') or '') == 'TavernMain'",
                "#str(getLocation('clara') or '') == 'TavernMain'",
                "#not household_runtime_event_seen_today('melissa_clara_overhear')",
                "#int(ClaraVar.get('tavern_melissa_visit_count', 0) or 0) >= 1",
                "#int(ClaraVar.get('tavern_melissa_overheard_2_seen', 0) or 0) == 0",
            ],
            None,
            "TavernMain",
            "overheard",
            0,
        ),
        (
            "melissaClaraOverheard_1",
            None, 2, None,
            1,
            None,
            [
                "#str(getLocation('melissa') or '') == 'TavernMain'",
                "#str(getLocation('clara') or '') == 'TavernMain'",
                "#not household_runtime_event_seen_today('melissa_clara_overhear')",
                "#int(ClaraVar.get('tavern_melissa_overheard_2_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('tavern_melissa_overheard_3_seen', 0) or 0) == 0",
                "#int(ClaraVar.get('tavern_melissa_visit_count', 0) or 0) >= 2",
                "#int(AmandaVar.get('attic_window_busted', 0) or 0) == 1",
                "#int(MelissaVar.get('bats_episode', 0) or 0) >= 6",
            ],
            None,
            "TavernMain",
            "overheard",
            1,
        ),
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
        (
            "story_clara_market_booklet_0",
            [1, 2, 3, 4, 5, 6], 2, None,
            1,
            None,
            [
                "#clara_market_daytime_roll_active(dayspassed, week)",
                "#int(ClaraVar.get('booklet_market_seen', 0) or 0) == 0",
            ],
            None,
            "MarketPlace",
            "enter",
            0,
        ),
        (
            "story_clara_market_booklet_1",
            None, None, None,
            1,
            None,
            [
                "#int(ClaraVar.get('booklet_market_seen', 0) or 0) == 0",
                "#((int(week or 0) in (1, 2, 3, 4, 5, 6) and int(time or 0) == 2 and clara_market_daytime_roll_active(dayspassed, week) and int(ClaraVar.get('market_intro_seen', 0) or 0) == 1) or (int(week or 0) in (1, 2, 3, 4, 6) and int(time or 0) == 3 and clara_market_evening_roll_active(dayspassed, week) and int(ClaraVar.get('drawings_secret_known', 0) or 0) == 1))",
            ],
            None,
            "MarketPlace",
            "enter",
            1,
        ),
        (
            "story_clara_market_booklet_2",
            [1, 2, 3, 4, 6], 3, None,
            1,
            None,
            [
                "#clara_market_evening_roll_active(dayspassed, week)",
                "#int(ClaraVar.get('booklet_market_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('market_evening_intro_seen', 0) or 0) == 0",
            ],
            None,
            "MarketPlace",
            "enter",
            2,
        ),
        (
            "story_clara_market_booklet_3",
            [1, 2, 3, 4, 6], 3, None,
            1,
            None,
            [
                "#clara_market_evening_roll_active(dayspassed, week)",
                "#int(ClaraVar.get('market_evening_intro_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('mongol_theft_seen', 0) or 0) == 0",
            ],
            None,
            "MarketPlace",
            "enter",
            3,
        ),
        (
            "story_clara_market_booklet_4",
            None, None, None,
            1,
            None,
            [
                "#int(ClaraVar.get('mongol_theft_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('escape_confessed', 0) or 0) == 0",
            ],
            None,
            "WineStore",
            "clara_talk",
            4,
        ),
        (
            "story_clara_market_booklet_5",
            None, None, None,
            1,
            None,
            [
                "#int(ClaraVar.get('escape_confessed', 0) or 0) == 1",
                "#int(MongolVar.get('StocksArrestDay', -1) or -1) < 0",
            ],
            None,
            "HunterClub",
            "overheard",
            5,
        ),
        (
            "story_clara_market_booklet_6",
            None, None, None,
            1,
            None,
            [
                "#int(MongolVar.get('StocksArrestDay', -1) or -1) >= 0",
                "#int(MongolVar.get('StocksSeen', 0) or 0) == 0",
            ],
            None,
            "CityGuard",
            "enter",
            6,
        ),
        (
            "story_clara_market_booklet_7",
            None, 4, None,
            1,
            None,
            [
                "#int(MongolVar.get('StocksSeen', 0) or 0) == 1",
                "#int(MongolVar.get('StocksFoodDay', -1) or -1) < 0",
            ],
            None,
            "CityGuard",
            "enter",
            7,
        ),
        (
            "story_clara_market_booklet_8",
            (1, 6), (0, 2), None,
            1,
            None,
            [
                "#int(MongolVar.get('StocksFoodDay', -1) or -1) >= 0",
                "#int(DraupnirVar.get('MongolLockpickOrderDay', -1) or -1) < 0",
            ],
            None,
            "StolyarWorkshop",
            "enter",
            8,
        ),
        (
            "story_clara_market_booklet_9",
            None, 4, None,
            1,
            None,
            [
                "#int(DraupnirVar.get('MongolLockpickOrderDay', -1) or -1) >= 0",
                "#int(MongolVar.get('StocksReleased', 0) or 0) == 0",
                "#int(dayspassed or 0) > int(MongolVar.get('StocksFoodDay', -1) or -1)",
            ],
            None,
            "CityGuard",
            "enter",
            9,
        ),
    ], highlight=False, threaded=True),
    #
    # clara_paintings_path
    #
    # Event tuple columns:
    # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
    #
    LThreadData(1, "clara", "PaintingsPath", None, [
        (
            "story_clara_paintings_melissa_0",
            None, None, None,
            1,
            None,
            [
                "#int(MelissaVar.get('drawings_found', 0) or 0) == 1",
                "#int(ClaraVar.get('paintings_melissa_asked', 0) or 0) == 0",
            ],
            None,
            "talk_melissa",
            "clara_paintings",
            0,
        ),
        (
            "story_clara_paintings_cellar_1",
            None, [1, 2], None,
            1,
            None,
            [
                "#int(ClaraVar.get('paintings_melissa_asked', 0) or 0) == 1",
                "#int(ClaraVar.get('cellar_seen', 0) or 0) == 0",
                "#int(ClaraVar.get('flirt', 0) or 0) > 0",
            ],
            None,
            "WineStore",
            "clara_paintings",
            1,
        ),
        (
            "story_clara_paintings_comfort_2",
            None, 0, None,
            1,
            None,
            [
                "#int(ClaraVar.get('comfort_pending', 0) or 0) == 1",
                "#int(ClaraVar.get('comfort_done', 0) or 0) == 0",
                "#str(getLocation('clara') or '') == 'WineStore'",
            ],
            None,
            "WineStore",
            "clara_paintings",
            2,
        ),
        (
            "story_clara_paintings_second_ask_3",
            None, None, None,
            1,
            None,
            [
                "#int(ClaraVar.get('second_ask_unlocked', 0) or 0) == 1",
                "#int(ClaraVar.get('source_known', 0) or 0) == 0",
            ],
            None,
            "WineStore",
            "clara_talk",
            3,
        ),
        (
            "story_clara_paintings_church_4",
            7, (0, 2), None,
            1,
            None,
            [
                "#int(ClaraVar.get('source_known', 0) or 0) == 1",
                "#int(ClaraVar.get('fiance_church_seen', 0) or 0) == 0",
            ],
            None,
            "Church",
            "clara_paintings",
            4,
        ),
        (
            "story_clara_paintings_barber_5",
            None, None, None,
            1,
            None,
            [
                "#int(ClaraVar.get('fiance_church_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('fiance_barber_seen', 0) or 0) == 0",
                "#(int(time or 0) == 0 or (int(time or 0) >= 4 and int(ClaraVar.get('fiance_barber_night_roll', 0) or 0) == 1))",
            ],
            None,
            "BarberShop",
            "clara_fiance",
            5,
        ),
        (
            "story_clara_paintings_commission_6",
            None, None, None,
            1,
            None,
            [
                "#int(ClaraVar.get('fiance_barber_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('commission_started', 0) or 0) == 0",
                "#str(getLocation('clara') or '') == 'TavernMain'",
            ],
            None,
            "TavernMain",
            "clara_paintings",
            6,
        ),
        (
            "story_clara_paintings_commission_followup_7",
            None, 0, None,
            1,
            None,
            [
                "#int(ClaraVar.get('commission_started', 0) or 0) == 1",
                "#int(ClaraVar.get('commission_followup_done', 0) or 0) == 0",
                "#int(dayspassed or 0) >= int(ClaraVar.get('commission_followup_day', 999999) or 999999)",
                "#str(getLocation('clara') or '') == 'WineStore'",
            ],
            None,
            "WineStore",
            "clara_paintings",
            7,
        ),
        (
            "story_clara_paintings_evening_peek_8",
            None, 3, None,
            1,
            None,
            [
                "#int(ClaraVar.get('commission_followup_done', 0) or 0) == 1",
                "#int(ClaraVar.get('peek_done', 0) or 0) == 0",
                "#str(getLocation('clara') or '') == 'WineStore'",
            ],
            None,
            "WineStore",
            "clara_paintings",
            8,
        ),
        (
            "story_clara_paintings_confession_9",
            None, None, None,
            1,
            None,
            [
                "#int(ClaraVar.get('peek_done', 0) or 0) == 1",
                "#int(ClaraVar.get('confession_done', 0) or 0) == 0",
                "#str(getLocation('clara') or '') == 'TavernMelissaRoom'",
                "#str(getLocation('melissa') or '') == 'TavernMelissaRoom'",
            ],
            None,
            "TavernMelissaRoom",
            "clara_paintings",
            9,
        ),
        (
            "story_clara_paintings_murder_10",
            None, None, None,
            1,
            None,
            [
                "#int(ClaraVar.get('confession_done', 0) or 0) == 1",
                "#int(ClaraVar.get('murder_seen', 0) or 0) == 0",
                "#int(dayspassed or 0) >= int(ClaraVar.get('murder_day', 999999) or 999999)",
            ],
            None,
            "CityGuard",
            "enter",
            10,
        ),
    ], highlight=False, threaded=True),
]
define beckyThreadList = []
define eddieThreadList = []
define irmaThreadList = []
define churchThreadList = []
define mongolThreadList = []
define cityGuardThreadList = []
define sherwoodThreadList = []
define cityThreadList = [
    RThreadData(0, "city", "StreetChronicles", None, [1, [
        # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
        (
            "TownStreetPatrolEvent", None, (3, 4), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",
                "#town_street.patrol_allowed(CurLoc)",
            ],
            None,
            "StreetTavern",
            "enter",
            700,
        ),
        (
            "TownStreetThugsEvent", None, (2, 3, 4), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#int(TownStreetFightToday or 0) == 0",
                "#town_street.thug_allowed(CurLoc)",
            ],
            None,
            "StreetTavern",
            "enter",
            710,
        ),
        (
            "TownStreetHelpEvent", None, (0, 1, 2, 3), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.help_allowed(CurLoc)",
            ],
            None,
            "StreetTavern",
            "enter",
            720,
        ),
        (
            "TownRandomChronicleEvent", None, None, None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
            ],
            None,
            "StreetTavern",
            "enter",
            900,
        ),
        (
            "TownStreetPatrolEvent", None, (3, 4), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",
                "#town_street.patrol_allowed(CurLoc)",
            ],
            None,
            "MarketPlace",
            "enter",
            700,
        ),
        (
            "TownStreetThugsEvent", None, (2, 3, 4), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#int(TownStreetFightToday or 0) == 0",
                "#town_street.thug_allowed(CurLoc)",
            ],
            None,
            "MarketPlace",
            "enter",
            710,
        ),
        (
            "TownStreetHelpEvent", None, (0, 1, 2, 3), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.help_allowed(CurLoc)",
            ],
            None,
            "MarketPlace",
            "enter",
            720,
        ),
        (
            "TownRandomChronicleEvent", None, None, None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
            ],
            None,
            "MarketPlace",
            "enter",
            900,
        ),
        (
            "TownStreetPatrolEvent", None, (3, 4), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",
                "#town_street.patrol_allowed(CurLoc)",
            ],
            None,
            "PortStreets",
            "enter",
            700,
        ),
        (
            "TownStreetThugsEvent", None, (2, 3, 4), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#int(TownStreetFightToday or 0) == 0",
                "#town_street.thug_allowed(CurLoc)",
            ],
            None,
            "PortStreets",
            "enter",
            710,
        ),
        (
            "TownStreetHelpEvent", None, (0, 1, 2, 3), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.help_allowed(CurLoc)",
            ],
            None,
            "PortStreets",
            "enter",
            720,
        ),
        (
            "TownRandomChronicleEvent", None, None, None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
            ],
            None,
            "PortStreets",
            "enter",
            900,
        ),
        (
            "TownStreetPatrolEvent", None, (3, 4), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",
                "#town_street.patrol_allowed(CurLoc)",
            ],
            None,
            "ArtisansQuarter",
            "enter",
            700,
        ),
        (
            "TownStreetThugsEvent", None, (2, 3, 4), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#int(TownStreetFightToday or 0) == 0",
                "#town_street.thug_allowed(CurLoc)",
            ],
            None,
            "ArtisansQuarter",
            "enter",
            710,
        ),
        (
            "TownStreetHelpEvent", None, (0, 1, 2, 3), None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.help_allowed(CurLoc)",
            ],
            None,
            "ArtisansQuarter",
            "enter",
            720,
        ),
        (
            "TownRandomChronicleEvent", None, None, None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
            ],
            None,
            "ArtisansQuarter",
            "enter",
            900,
        ),
    ]], highlight=False, threaded=False),
]
define lizaThreadList = []
define georgettThreadList = []

default ClaraMarketFollowExtraAdvance = 0

define threadListsByGirl = {
    "amanda": amandaThreadList,
    "melissa": melissaThreadList,
    "sandra": sandraThreadList,
    "clara": claraThreadList,
    "mongol": mongolThreadList,
    "cityguard": cityGuardThreadList,
    "sherwood": sherwoodThreadList,
    "becky": beckyThreadList,
    "eddie": eddieThreadList,
    "irma": irmaThreadList,
    "church": churchThreadList,
    "liza": lizaThreadList,
    "georgett": georgettThreadList,
    "city": cityThreadList,
}

define threadList = (
    amandaThreadList
    + melissaThreadList
    + sandraThreadList
    + claraThreadList
    + mongolThreadList
    + cityGuardThreadList
    + sherwoodThreadList
    + beckyThreadList
    + eddieThreadList
    + irmaThreadList
    + churchThreadList
    + lizaThreadList
    + georgettThreadList
    + cityThreadList
)

define threadData = loadThreadData(threadList)
default threads = createThreads()


label checkTriggers(location, action, numpop=0):
    $ _story_location = str(location or "").strip()
    $ _story_action = str(action or "").strip()
    $ findAvailableEvents(True)
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
        if thread_name in threads:
            $ thread = threads[thread_name]
            $ thread.setDay()
        else:
            $ thread = None
    else:
        $ thread = None
    return


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
    return


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
    return


label story_clara_market_booklet_0:
    $ SignalBlockTime = 1
    $ _clara_evening_booklet_follow = int(time or 0) == 3 and int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1
    $ _clara_market_intro_seen = int(ClaraVar.get("market_intro_seen", 0) or 0) == 1
    if _clara_evening_booklet_follow:
        $ ClaraVar["market_evening_intro_seen"] = 1
        $ MainTxt = "Вечером рынок уже закрыт. На площади остаются только несколько поздних прохожих, и среди них вы замечаете фигуру в плаще. Человек идет быстро, но когда фонарь на мгновение выхватывает лицо из-под капюшона, вы узнаете Клариссу.\n\nДевушка тоже замечает ваш взгляд, тут же глубже натягивает капюшон и ускоряет шаг между закрытыми лавками. Хм. Очень интересно, что она делает здесь в такое время.\n\nЕсли сейчас держаться достаточно тихо, можно не только проследить за Клариссой, но и подслушать, с кем именно она ведет свои тайные дела."
        $ CurLocDesc = MainTxt
        if renpy.loadable("images/clara/market_night.png"):
            call ShowImage("", "", "images/clara/market_night.png")
        elif renpy.loadable("images/market/LocMarketPlace2.jpg"):
            call ShowImage("", "", "images/market/LocMarketPlace2.jpg")
    else:
        if _clara_market_intro_seen:
            $ MainTxt = "Днем на рынке снова мелькает фигура в легком плаще. Вы узнаете Клариссу раньше, чем она успевает скрыть лицо. Девушка замечает вас, поспешно натягивает капюшон и идет быстрее, будто совершенно не хочет, чтобы ее здесь окликали.\n\nЕсли уж вы хотите узнать, чем она занимается, сейчас самое время попробовать проследить за ней."
        else:
            $ ClaraVar["market_intro_seen"] = 1
            $ MainTxt = "На дневном рынке среди покупателей вы замечаете фигуру в плаще. Сначала это просто случайный силуэт в толпе, но затем вы узнаете Клариссу, дочку своего винного поставщика.\n\nВы уже собираетесь окликнуть ее, но Кларисса, едва встретившись с вами взглядом, поспешно набрасывает на голову капюшон и сразу идет быстрее между рядами лавок. Похоже, у нее здесь какие-то совсем частные дела, и узнавать себя она сейчас не хочет."
        $ CurLocDesc = MainTxt
        if renpy.loadable("images/clara/market_day.png"):
            call ShowImage("", "", "images/clara/market_day.png")
        else:
            call ShowImageSeq("general", "", "LocMarketPlace", 2)
    $ ClaraMarketFollowExtraAdvance = 1
    $ current_action_title = "Вечерний рынок" if _clara_evening_booklet_follow else "Рынок"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Проследить за Клариссой и подслушать разговор" if _clara_evening_booklet_follow else "Проследить за Клариссой", Call("story_clara_market_booklet_1_direct_follow")),
        MenuItem("Не вмешиваться", Call("story_clara_market_booklet_ignore")),
    ]
    call screen main_ui
    jump MarketPlace


label story_clara_market_booklet_1:
    $ SignalBlockTime = 1
    $ _clara_evening_booklet_follow = int(time or 0) == 3 and int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1
    if _clara_evening_booklet_follow:
        $ ClaraVar["market_evening_intro_seen"] = 1
        $ MainTxt = "Вечером рынок уже закрыт. На площади остаются только несколько поздних прохожих, и среди них вы замечаете фигуру в плаще. Человек идет быстро, но когда фонарь на мгновение выхватывает лицо из-под капюшона, вы узнаете Клариссу.\n\nДевушка тоже замечает ваш взгляд, тут же глубже натягивает капюшон и ускоряет шаг между закрытыми лавками. Хм. Очень интересно, что она делает здесь в такое время.\n\nЕсли сейчас держаться достаточно тихо, можно не только проследить за Клариссой, но и подслушать, с кем именно она ведет свои тайные дела."
        $ CurLocDesc = MainTxt
        if renpy.loadable("images/clara/market_night.png"):
            call ShowImage("", "", "images/clara/market_night.png")
        elif renpy.loadable("images/market/LocMarketPlace2.jpg"):
            call ShowImage("", "", "images/market/LocMarketPlace2.jpg")
    else:
        $ MainTxt = "Днем на рынке снова мелькает фигура в легком плаще. Вы узнаете Клариссу раньше, чем она успевает скрыть лицо. Девушка замечает вас, поспешно натягивает капюшон и идет быстрее, будто совершенно не хочет, чтобы ее здесь окликали.\n\nЕсли уж вы хотите узнать, чем она занимается, сейчас самое время попробовать проследить за ней."
        $ CurLocDesc = MainTxt
        if renpy.loadable("images/clara/market_day.png"):
            call ShowImage("", "", "images/clara/market_day.png")
        else:
            call ShowImageSeq("general", "", "LocMarketPlace", 2)
    $ ClaraMarketFollowExtraAdvance = 0
    $ current_action_title = "Вечерний рынок" if _clara_evening_booklet_follow else "Рынок"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Проследить за Клариссой и подслушать разговор" if _clara_evening_booklet_follow else "Проследить за Клариссой", Call("story_clara_market_booklet_1_direct_follow")),
        MenuItem("Не вмешиваться", Call("story_clara_market_booklet_ignore")),
    ]
    call screen main_ui
    jump MarketPlace


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
    $ current_action_items = [MenuItem("Отойти и оставить их", Jump("MarketPlace"))]
    call screen main_ui
    jump MarketPlace


label story_clara_market_action_direct:
    call preEvent("claraBookletMarket")
    $ _clara_target = ""
    if int(time or 0) == 2 and int(ClaraVar.get("booklet_market_seen", 0) or 0) == 0:
        if int(ClaraVar.get("market_intro_seen", 0) or 0) == 0:
            $ _clara_target = "story_clara_market_booklet_0"
        else:
            $ _clara_target = "story_clara_market_booklet_1"
        if _clara_target == "story_clara_market_booklet_1" and thread is not None and int(thread.num or 0) < 1:
            $ thread.advanceTo(1)
    elif int(time or 0) == 3 and int(ClaraVar.get("booklet_market_seen", 0) or 0) == 0 and int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1:
        if int(ClaraVar.get("market_intro_seen", 0) or 0) == 0:
            $ _clara_target = "story_clara_market_booklet_0"
        else:
            $ _clara_target = "story_clara_market_booklet_1"
        if _clara_target == "story_clara_market_booklet_1" and thread is not None and int(thread.num or 0) < 1:
            $ thread.advanceTo(1)
    elif int(time or 0) == 3 and int(ClaraVar.get("booklet_market_seen", 0) or 0) == 1 and int(ClaraVar.get("market_evening_intro_seen", 0) or 0) == 0:
        $ _clara_target = "story_clara_market_booklet_2"
        if thread is not None and int(thread.num or 0) < 2:
            $ thread.advanceTo(2)
    elif int(time or 0) == 3 and int(ClaraVar.get("market_evening_intro_seen", 0) or 0) == 1 and int(ClaraVar.get("mongol_theft_seen", 0) or 0) == 0:
        $ _clara_target = "story_clara_market_booklet_2"
        if thread is not None:
            $ thread.advanceTo(2)
    $ evalTime = None
    $ findAvailableEvents(True)
    if str(_clara_target or "") == "":
        jump MarketPlace
        return
    jump expression _clara_target


label story_clara_market_booklet_ignore:
    $ _clara_evening_booklet_follow = int(time or 0) == 3 and int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1
    if _clara_evening_booklet_follow:
        $ current_action_title = "Вечерний рынок"
        $ current_action_items = [MenuItem("Вернуться к своим делам", Jump("MarketPlace"))]
    else:
        $ current_action_title = "Рынок"
        $ current_action_items = [MenuItem("Продолжить идти по рынку", Jump("MarketPlace"))]
    $ current_action_content = None
    call screen main_ui
    jump MarketPlace


label story_clara_market_booklet_1_direct_follow:
    $ SignalBlockTime = 1
    $ _clara_evening_booklet_follow = int(time or 0) == 3 and int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1
    if _clara_evening_booklet_follow and int(effective_player_exploration() or 0) < 100:
        $ ClaraVar["market_follow_failed_day"] = int(dayspassed or 0)
        $ ClaraVar["market_follow_failed_time"] = int(time or 0)
        $ MainTxt = "Вечерний рынок куда опаснее для слежки, чем дневной. Стоит вам зацепить чей-то ящик или лишний раз оглянуться, как Кларисса успевает скрыться в темном закутке и растворяется среди поздних покупателей.\n\nБез лучшей сноровки вы только выдадите себя и ничего не услышите."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Вечерний рынок"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться к своим делам", Jump("MarketPlace"))]
        call screen main_ui
        jump MarketPlace
    if (not _clara_evening_booklet_follow) and int(effective_player_exploration() or 0) < 80:
        $ ClaraVar["market_follow_failed_day"] = int(dayspassed or 0)
        $ ClaraVar["market_follow_failed_time"] = int(time or 0)
        $ MainTxt = "Вы стараетесь не отстать, но дневной рынок слишком шумный и тесный. Стоит вам замешкаться на пару шагов, как Кларисса ускользает между рядами и будто растворяется среди чужих спин.\n\nПохоже, без лучшей сноровки в слежке вы просто потеряете ее снова."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Рынок"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Продолжить идти по рынку", Jump("MarketPlace"))]
        call screen main_ui
        jump MarketPlace
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
    $ current_action_items = [MenuItem("Тихо уйти", Jump("MarketPlace"))]
    if (not _clara_evening_booklet_follow) and (int(MelissaVar.get("drawings_found", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1):
        $ current_action_items.insert(0, MenuItem("Подойти к Клариссе и торговцу", Call("story_clara_market_booklet_confront")))
    $ story_thread_advance_current()
    while int(ClaraMarketFollowExtraAdvance or 0) > 0:
        $ ClaraMarketFollowExtraAdvance = int(ClaraMarketFollowExtraAdvance or 0) - 1
        $ story_thread_advance_current()
    if _clara_evening_booklet_follow:
        $ story_thread_advance_current()
    $ ClaraMarketFollowExtraAdvance = 0
    call screen main_ui
    jump MarketPlace


label story_clara_market_booklet_2_direct_follow:
    $ SignalBlockTime = 1
    $ ClaraVar["market_evening_intro_seen"] = 1
    if int(effective_player_exploration() or 0) < 100:
        $ ClaraVar["market_follow_failed_day"] = int(dayspassed or 0)
        $ ClaraVar["market_follow_failed_time"] = int(time or 0)
        $ MainTxt = "Закрытый вечерний рынок куда опаснее для слежки, чем дневная толпа. Стоит вам задеть чью-то корзину и чуть замешкаться, как Кларисса вместе с Монголом растворяются в темном закутке между пустеющими рядами. Без лучшей сноровки здесь их не удержать."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Вечерний рынок"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Вернуться к своим делам", Jump("MarketPlace"))]
        call screen main_ui
        jump MarketPlace
    $ story_thread_advance_current()
    jump story_clara_market_booklet_3


label story_clara_market_booklet_2:
    $ SignalBlockTime = 1
    $ ClaraVar["market_evening_intro_seen"] = 1
    $ MainTxt = "Вечером рынок закрыт, и площадь выглядит почти пустой. У закрытых лавок задержались лишь несколько человек, поэтому фигура в плаще сразу бросается в глаза. Когда она проходит ближе к фонарю, вы узнаете Клариссу.\n\nСтоит ей заметить ваш взгляд, как девушка глубже натягивает капюшон и быстро уходит в сторону закутка у конного торга. Хм. Очень интересно, что она делает здесь в такое время.\n\nПохоже, на этот раз дело идет уже не о книжечках, а о чем-то более грязном."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_night.png"):
        call ShowImage("", "", "images/clara/market_night.png")
    elif renpy.loadable("images/market/LocMarketPlace2.jpg"):
        call ShowImage("", "", "images/market/LocMarketPlace2.jpg")
    $ current_action_title = "Вечерний рынок"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Тихо проследить за Клариссой", Call("story_clara_market_booklet_2_direct_follow")),
        MenuItem("Не рисковать", Call("story_clara_market_booklet_2_ignore")),
    ]
    call screen main_ui
    jump MarketPlace


label story_clara_market_booklet_2_ignore:
    $ current_action_title = "Вечерний рынок"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться к своим делам", Jump("MarketPlace"))]
    call screen main_ui
    jump MarketPlace


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
    $ current_action_items = [MenuItem("Запомнить услышанное и уйти", Jump("MarketPlace"))]
    $ story_thread_advance_current()
    call screen main_ui
    jump MarketPlace


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
    if thread is not None and int(thread.num or 0) < 4:
        $ thread.advanceTo(4)
    $ evalTime = None
    $ findAvailableEvents(True)
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


label story_clara_market_booklet_6:
    $ SignalBlockTime = 1
    $ MongolVar["StocksSeen"] = 1
    $ MainTxt = "На рыночной площади, возле караулки, стоят тяжелые колодки. В них вместе с еще парой помятых головорезов сидит и Монгол. От прежней ярмарочной ухмылки в нем мало что осталось: губа разбита, рубаха грязная, но глаза все еще бегают живо.\n\nЗаметив вас, он дергается и шипит сквозь зубы: \"Стефан, брат, не губи. Я тут с голоду загнусь раньше, чем меня судить начнут. Принеси ночью пожрать, а там, может, и поговорим. Я добро помню. И про Клариссу тоже помню.\""
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
    if thread is not None and int(thread.num or 0) < 6:
        $ thread.advanceTo(6)
    $ evalTime = None
    $ findAvailableEvents(True)
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
    if thread is not None and int(thread.num or 0) < 7:
        $ thread.advanceTo(7)
    $ evalTime = None
    $ findAvailableEvents(True)
    jump story_clara_market_booklet_feed_mongol


label story_clara_market_booklet_8:
    $ SignalBlockTime = 1
    $ MainTxt = "Вы находите Драупнира за верстаком и, не мудрствуя лукаво, объясняете, что вам нужны очень тонкие отмычки. Гном сперва косится на вас с подозрением, потом только фыркает.\n\n\"Ничего не знаю и знать не хочу, для какой двери тебе такая железяка,\" ворчит он. \"Но если работа тонкая и молчаливая, то это ко мне. За сорок мараведи сделаю хороший набор, который и в сапог спрятать не стыдно.\""
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
    if thread is not None and int(thread.num or 0) < 8:
        $ thread.advanceTo(8)
    $ evalTime = None
    $ findAvailableEvents(True)
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
    if thread is not None and int(thread.num or 0) < 9:
        $ thread.advanceTo(9)
    $ evalTime = None
    $ findAvailableEvents(True)
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
    call screen main_ui
    jump TavernStorage


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
    call screen main_ui
    jump TavernMelissaRoom


label story_melissa_bat_problem_2:
    $ SignalBlockTime = 1
    call MelissaAtticColonySearch
    $ story_thread_advance_current()
    call TavernAticBuildActions
    call screen main_ui
    jump TavernAtic


label story_melissa_bat_problem_3:
    $ SignalBlockTime = 1
    call MelissaAtticWindowPeek
    call screen main_ui
    jump TavernAtic


label story_melissa_bat_problem_4:
    $ SignalBlockTime = 1
    if melissa_bats_stage() < 7 and int(_player_item_count_by_id("bat_repellent_001") or 0) > 0:
        call MelissaBurnAtticColony
    elif melissa_bats_stage() >= 7:
        call MelissaOrderRoofRepair
    else:
        call MelissaAtticCleanupScene
    call screen main_ui
    jump TavernAtic


label story_melissa_bat_problem_5:
    $ SignalBlockTime = 1
    call MelissaFindDrawingsScene
    call screen main_ui
    jump TavernAmandaRoom


label story_melissa_bat_problem_6:
    $ SignalBlockTime = 1
    call MelissaBatsCompletionScene
    $ story_thread_advance_current()
    jump TavernMain
