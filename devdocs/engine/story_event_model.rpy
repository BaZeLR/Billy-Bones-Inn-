default active_event = None

default random_events = []
default story_events = []
default tavern_work_events = []

default availEvents = {}
default evalTime = -1
default thread = None
default eventLocations = set()
default eventPeople = set()
default eventTalk = set()
default eventOptions = set()
default eventItems = set()
default story_thread_levels = {}
default amanda_story_pending = ""

init python:
    import renpy.exports as renpy

    def _story_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def _story_num_day():
        return _story_to_int(dayspassed, 0)

    def _story_days_since(marker_day, default=0):
        return _story_num_day() - _story_to_int(marker_day, default)

    def _story_known_values():
        values = {}

        def _put(name, value):
            values[name] = value

        try:
            _put("story_thread_levels", story_thread_levels)
        except Exception:
            _put("story_thread_levels", {})
        try:
            _put("dayspassed", dayspassed)
        except Exception:
            pass
        try:
            _put("week", week)
        except Exception:
            pass
        try:
            _put("time", time)
        except Exception:
            pass
        try:
            _put("day", day)
        except Exception:
            pass
        try:
            _put("month", month)
        except Exception:
            pass
        try:
            _put("year", year)
        except Exception:
            pass
        try:
            _put("CurLoc", CurLoc)
        except Exception:
            pass
        try:
            _put("AmandaDynamicNextJump", AmandaDynamicNextJump)
        except Exception:
            pass
        try:
            _put("money", money)
        except Exception:
            pass
        try:
            _put("fun", fun)
        except Exception:
            pass
        try:
            _put("energy", energy)
        except Exception:
            pass
        try:
            _put("health", health)
        except Exception:
            pass
        try:
            _put("notoriety", notoriety)
        except Exception:
            pass
        try:
            _put("exploration", exploration)
        except Exception:
            pass
        try:
            _put("charisma", charisma)
        except Exception:
            pass
        try:
            _put("rebellion", rebellion)
        except Exception:
            pass
        try:
            _put("look", look)
        except Exception:
            pass
        try:
            _put("playerItems", playerItems)
        except Exception:
            pass
        try:
            _put("Friends", Friends)
        except Exception:
            pass
        try:
            _put("sluttiness", sluttiness)
        except Exception:
            pass
        try:
            _put("pregnancy", pregnancy)
        except Exception:
            pass
        try:
            _put("CurrentLoc", CurrentLoc)
        except Exception:
            pass
        try:
            _put("MelissaVar", MelissaVar)
        except Exception:
            pass
        try:
            _put("SandraVar", SandraVar)
        except Exception:
            pass
        try:
            _put("ClaraVar", ClaraVar)
        except Exception:
            pass
        try:
            _put("BeckyVar", BeckyVar)
        except Exception:
            pass
        try:
            _put("IngaVar", IngaVar)
        except Exception:
            pass
        try:
            _put("EddieVar", EddieVar)
        except Exception:
            pass
        try:
            _put("AlberVar", AlberVar)
        except Exception:
            pass
        try:
            _put("MongolVar", MongolVar)
        except Exception:
            pass
        try:
            _put("ZimmerVar", ZimmerVar)
        except Exception:
            pass
        try:
            _put("DraupnirVar", DraupnirVar)
        except Exception:
            pass
        try:
            _put("story_amanda_tavern_entry_ready", story_amanda_tavern_entry_ready)
        except Exception:
            pass
        try:
            _put("story_amanda_street_entry_ready", story_amanda_street_entry_ready)
        except Exception:
            pass
        try:
            _put("story_amanda_market_entry_ready", story_amanda_market_entry_ready)
        except Exception:
            pass
        try:
            _put("CheckIfSexEventExist", CheckIfSexEventExist)
        except Exception:
            pass
        try:
            _put("GetSexEventFromTable", GetSexEventFromTable)
        except Exception:
            pass
        try:
            _put("LegareAmandaLetGoCode", LegareAmandaLetGoCode)
        except Exception:
            pass
        try:
            _put("AmandaYellNotWork", AmandaYellNotWork)
        except Exception:
            pass
        return values

    def _story_named_value(name, default=None):
        return _story_known_values().get(str(name or "").strip(), default)

    def _story_named_number(name, default=0):
        return _story_to_int(_story_named_value(name, default), default)

    def _story_named_callable(name):
        value = _story_named_value(name, None)
        return value if callable(value) else None

    def _story_condition_scope():
        return dict(_story_known_values())

    def _story_level_enabled(level):
        levels_map = _story_named_value("story_thread_levels", {})
        if not isinstance(levels_map, dict):
            return True
        return bool(levels_map.get(level, True))

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
        if isinstance(spec, range):
            return _story_to_int(current_value, 0) in spec
        if isinstance(spec, (list, tuple, set)):
            values = list(spec)
            if len(values) == 2 and all(isinstance(item, (int, float)) for item in values):
                low = _story_to_int(values[0], 0)
                high = _story_to_int(values[1], 0)
                current_int = _story_to_int(current_value, 0)
                return low <= current_int <= high
            current_int = _story_to_int(current_value, 0)
            normalized = []
            for item in values:
                normalized.append(_story_to_int(item, item))
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
        if not text:
            return True
        if text.startswith("!"):
            return not _story_eval_condition(text[1:])
        if text.startswith("#"):
            text = text[1:].strip()
        scope = _story_condition_scope()
        if text in scope:
            return bool(scope[text])
        try:
            return bool(eval(text, {"__builtins__": __builtins__}, scope))
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

    def checkBlocksList(evt_list):
        has_none = False
        for evt in evt_list:
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
        if not ref:
            return fallback
        if ref in threads:
            return getattr(threads[ref], "day", fallback)
        short_ref = ref[:-3] if len(ref) > 3 else ref
        if short_ref in threads:
            return getattr(threads[short_ref], "day", fallback)
        return _story_named_number(ref, fallback)

    def _story_delay_ready(delay_spec, fallback_marker=0):
        if delay_spec is None:
            return True

        if isinstance(delay_spec, int):
            return _story_days_since(fallback_marker, 0) >= int(delay_spec)

        if isinstance(delay_spec, (tuple, list)):
            if len(delay_spec) <= 0:
                return True
            marker_name = delay_spec[0]
            delay_days = delay_spec[1] if len(delay_spec) > 1 else 1
            marker_day = _story_marker_day(marker_name, fallback_marker)
            return _story_days_since(marker_day, 0) >= _story_to_int(delay_days, 1)

        if isinstance(delay_spec, str):
            marker_day = _story_marker_day(delay_spec, fallback_marker)
            return _story_days_since(marker_day, 0) >= 1

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
            return True

        def checkDay(self):
            return checkEventTime(week, self.day)

        def checkHour(self):
            return checkEventTime(time, self.hour)

        def checkNumDay(self, evt_numDay):
            return _story_delay_ready(self.evtDay, evt_numDay)

        def checkReqs(self):
            if self.reqs is None:
                return True
            for stat, limit in dict(self.reqs).items():
                threshold = _story_to_int(limit, 0)
                if stat in peopleInfo:
                    current_value = _story_to_int(getattr(peopleInfo[stat], "rel", 0), 0)
                else:
                    current_value = _story_named_number(stat, 0)
                if threshold > 0 and current_value < threshold:
                    return False
                if threshold <= 0 and current_value >= -threshold:
                    return False
            return True

        def checkConditions(self):
            return all(cond.eval() for cond in self.conds)

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
            has_none = False
            for cond in self.conds:
                rv = cond.blocked()
                if rv is True:
                    return True
                if rv is None:
                    has_none = True
            if has_none:
                return None
            return False

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
        for _name, tdata in threadData.items():
            for evt_list in tdata.triggers:
                for evt in evt_list:
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
            return all(cond.eval() for cond in self.conds)

        def checkBlocks(self):
            has_none = False
            for cond in self.conds:
                rv = cond.blocked()
                if rv is True:
                    return True
                if rv is None:
                    has_none = True
            if has_none:
                return None
            return False

    class LThreadData(ThreadData):
        def __init__(self, level, person, subname, condStr, triggers, highlight=True, threaded=True):
            super(LThreadData, self).__init__(level, person, subname, condStr, triggers, highlight, threaded)

    class RThreadData(ThreadData):
        def __init__(self, level, person, subname, condStr, triggers, highlight=True, threaded=True):
            super(RThreadData, self).__init__(level, person, subname, condStr, [triggers[1]] * triggers[0], highlight, threaded)
            for num in range(self.length):
                for evt in self.triggers[num]:
                    if str(evt.target).endswith("*"):
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
            return [evt for num in range(self.data.length) if not self.done[num] for evt in self.data.triggers[num] if evt.canTrigger(self.day)]

    def loadThreadData(threadList):
        return {tdata.name: tdata for tdata in threadList}

    def createThread(data):
        if isinstance(data, LThreadData):
            return LThreadInfo(data)
        if isinstance(data, RThreadData):
            return RThreadInfo(data)
        if isinstance(data, UThreadData):
            return UThreadInfo(data)
        raise Exception("createThread")

    def createThreads():
        return {name: createThread(data) for name, data in threadData.items()}

    def initThreads():
        global threads
        for name, tdata in threadData.items():
            if name not in threads:
                threads[name] = createThread(tdata)
            else:
                threads[name].data = tdata
                threads[name].adjustLen()
        for _name, tdata in threadData.items():
            tdata.initConditions()

    def findBlockedThreads(threads_in):
        if threads_in is threads:
            for _name, thread_info in threads_in.items():
                thread_info.initBlocks()
        pending = []
        while True:
            changed = False
            pending = []
            for _name, thread_info in threads_in.items():
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

        eval_key = (_story_num_day(), _story_to_int(week, 1), _story_to_int(time, 0))
        if (not forced) and evalTime == eval_key:
            return
        evalTime = eval_key

        tmp_events = []
        for _name, thread_info in threads.items():
            tmp_events.extend(thread_info.getAvailableEvents())

        availEvents = {}
        for evt in tmp_events:
            if evt.location not in availEvents:
                availEvents[evt.location] = {evt.action: [evt]}
            elif evt.action not in availEvents[evt.location]:
                availEvents[evt.location][evt.action] = [evt]
            else:
                availEvents[evt.location][evt.action].append(evt)

        for location_name in availEvents:
            for action_name in availEvents[location_name]:
                availEvents[location_name][action_name].sort(key=lambda item: item.priority)
                for evt in availEvents[location_name][action_name]:
                    if evt.checkItem():
                        availEvents[location_name][action_name] = evt
                        break
                else:
                    availEvents[location_name][action_name] = availEvents[location_name][action_name][0]

        eventLocations = set(availEvents.keys())
        eventPeople = set()
        eventTalk = set()
        eventOptions = set()
        eventItems = set()

    def initStoryEventRuntime(force=False):
        initThreads()
        initEvents()
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

    def _story_current_location():
        return str(_story_named_value("CurLoc", "") or "")

    def _story_take_amanda_jump(default_target=""):
        global AmandaDynamicNextJump
        next_label = str(_story_named_value("AmandaDynamicNextJump", "") or "")
        AmandaDynamicNextJump = ""
        return next_label or str(default_target or "")

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

    def story_amanda_run_to_legare(location_name):
        global AmandaDynamicNextJump, SignalBlockTime

        story_amanda_clear_pending()

        get_func = _story_named_callable("GetSexEventFromTable")
        let_go_func = _story_named_callable("LegareAmandaLetGoCode")
        yell_func = _story_named_callable("AmandaYellNotWork")
        if not callable(get_func):
            return str(location_name or _story_current_location())

        cur_loc_name = str(location_name or _story_current_location())
        cur_time = _story_named_number("time", 0)
        if _story_to_int(get_func("amanda", cur_time, "legarerun"), 0) <= 0:
            return cur_loc_name

        SignalBlockTime = 1
        if cur_loc_name == "TavernMain":
            renpy.say(None, "Неожиданно вы заметили что Аманда, ваша младшая сестренка, потихоньку, и насколько это возможно незаметно, пробирается к выходу.")
        elif cur_loc_name == "MarketPlace":
            renpy.say(None, "Неожиданно вы пробирающуюся между лавками, палатками и лотками вашу сестренку Аманду. Кажется, она не очень хочет чтобы ее заметили и поэтому постоянно озирается, прячется за лотками, старается быть в тени. Хотя достигает она таким поведением результатов прямо противоположных ожидаемым - все на рынке оглядываются на нее.")
        else:
            renpy.say(None, "Неожиданно вы пробирающуюся вдоль стеночки вашу сестренку Аманду. Кажется, она не очень хочет чтобы ее заметили и поэтому постоянно озирается, передвигается от угла к углу, старается спрятаться в тени домов. Хотя достигает она таким поведением результатов прямо противоположных ожидаемым - прохожие все как один оглядываются на нее.")

        ShowImage("amanda", "", "portrait")
        choice = renpy.display_menu([
            ("Проследить за ней", "follow"),
            ("Оставить ее в покое", "leave"),
            ("Отправить ее обратно на работу", "work"),
        ])

        if choice == "follow":
            AmandaDynamicNextJump = "AfterDanceSexLegare"
        elif choice == "leave":
            renpy.say(None, "\"Спешит куда-то? Ну и пусть себе спешит, не мое дело,\" подумали вы. А Аманда скоро скрылась за углом.")
            if callable(let_go_func):
                let_go_func()
            AmandaDynamicNextJump = cur_loc_name
        else:
            if cur_loc_name == "TavernMain":
                renpy.say(None, "Вы выскочили из трактира вслед за Амандой и увидели что она намылилась куда-то далеко.")
            if callable(yell_func):
                yell_func()
            else:
                AmandaDynamicNextJump = "StreetTavern"

        return _story_take_amanda_jump(cur_loc_name)

    def story_amanda_meet_lover():
        global AmandaDynamicNextJump, SignalBlockTime

        story_amanda_clear_pending()

        cur_time = _story_named_number("time", 0)
        get_func = _story_named_callable("GetSexEventFromTable")

        SignalBlockTime = 1
        renpy.say(None, "Проходя мимо трактира вы вдруг заметили на улице знакомую фигуру.")

        if renpy.random.randint(1, 2) == 1:
            choice = renpy.display_menu([
                ("Посмотреть поближе", "look"),
                ("Идти дальше", "go"),
            ])
            if choice == "look":
                renpy.say(None, "Вы подошли поближе но оказалось что вы обознались.")
            else:
                renpy.say(None, "\"Да мало ли кто это может быть? У меня есть дела поважнее!\" подумали вы и пошли дальше.")
            return ""

        if callable(get_func):
            get_func("amanda", cur_time, "lovermeet")

        choice = renpy.display_menu([
            ("Посмотреть поближе", "look"),
            ("Идти дальше", "go"),
        ])
        if choice == "look":
            AmandaDynamicNextJump = "AmandaLoverSex"
        else:
            renpy.say(None, "\"Да мало ли кто это может быть? У меня есть дела поважнее!\" подумали вы и пошли дальше.")

        return _story_take_amanda_jump("")


define threadList = [
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

define threadData = loadThreadData(threadList)

default threads = createThreads()

label checkTriggers(location, action, numpop=0):
    if location not in availEvents:
        return False
    if action not in availEvents[location]:
        return False
    $ evt = availEvents[location][action]
    if not evt.target:
        return False
    if evt.item and not evt.checkItem():
        return False
    if numpop == 2:
        $ renpy.pop_call()
    elif numpop == 1:
        $ renpy.pop_call()
    call preEvent(evt.thread_name if evt.threaded else None)
    jump expression evt.target

label preEvent(thread_name=None):
    $ evalTime = -1
    if thread_name:
        $ thread = threads[thread_name]
        $ thread.setDay()
    else:
        $ thread = None
    return

label event_activate(event_obj=None):
    if event_obj is None:
        return
    python:
        _event_text = ""
        if hasattr(event_obj, "show"):
            _event_text = event_obj.show()
    if _event_text:
        "[_event_text]"
    return

label story_amanda_tavern_entry:
    $ _story_amanda_jump = story_amanda_run_to_legare("TavernMain")
    if _story_amanda_jump and renpy.has_label(_story_amanda_jump):
        jump expression _story_amanda_jump
    jump TavernMain

label story_amanda_street_entry:
    $ _story_amanda_pending = str(amanda_story_pending or "")
    if _story_amanda_pending == "run_to_legare":
        $ _story_amanda_jump = story_amanda_run_to_legare("StreetTavern")
        if _story_amanda_jump and renpy.has_label(_story_amanda_jump):
            jump expression _story_amanda_jump
        jump StreetTavern
    elif _story_amanda_pending == "meet_lover":
        $ _story_amanda_jump = story_amanda_meet_lover()
        if _story_amanda_jump and renpy.has_label(_story_amanda_jump):
            jump expression _story_amanda_jump
        jump street_tavern_menu
    jump StreetTavern

label story_amanda_market_entry:
    $ _story_amanda_jump = story_amanda_run_to_legare("MarketPlace")
    if _story_amanda_jump and renpy.has_label(_story_amanda_jump):
        jump expression _story_amanda_jump
    jump MarketPlace

screen board():
    modal True
    frame:
        background Frame("gui/frame.png", 6, 6)
        align (0.5, 0.5)
        xmaximum 1100
        ymaximum 760
        padding (20, 20)
        vbox:
            spacing 12
            text "Story Threads" size 32 color "#c90"
            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                ymaximum 620
                vbox:
                    spacing 6
                    if not threads:
                        text "No thread data loaded." size 18 color "#fff"
                    else:
                        for _thread_name, _thread_info in sorted(threads.items()):
                            $ _thread_status = _thread_info.statusText()
                            $ _thread_target = _thread_info.currentTarget()
                            text "[_thread_name]: [_thread_status] -> [_thread_target]" size 18 color "#fff"
            textbutton "Close":
                action Hide("board")

