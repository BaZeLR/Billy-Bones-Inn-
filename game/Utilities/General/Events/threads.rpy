# ================================================================================
# Story thread runtime.
# Owns ThreadData/ThreadInfo objects and blocked-thread resolution.
# ================================================================================

init -25 python:
    import renpy.exports as renpy

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
        pending_signature = None
        max_passes = max(1, len(dict(threads_in or {})) + 1)
        for _pass_index in range(max_passes):
            pending = []
            for _name, thread_info in dict(threads_in or {}).items():
                rv = thread_info.checkBlocks()
                if rv is None:
                    pending.append(thread_info)
            if not pending:
                break
            next_signature = tuple([id(row) for row in pending])
            if next_signature == pending_signature:
                break
            pending_signature = next_signature
        for thread_info in list(pending or []):
            if getattr(thread_info, "blocked", None) is None:
                thread_info.blocked = False
            try:
                thread_info.blocks = [False if row is None else row for row in list(thread_info.blocks or [])]
            except Exception:
                pass
        return threads_in
