# ================================================================================
# Story event conditions runtime.
# Conditions are readable gates used by thread/event definitions and board display.
# ================================================================================

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
        info = getPersonInfo(key)
        friend_value = _story_to_int(getattr(info, "rel", 0), 0) if info is not None else 0
        corruption_value = _story_to_int(getattr(info, "corruption", 0), 0) if info is not None else 0
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
                first = _story_to_int(values[0], 0)
                last = _story_to_int(values[1], 0)
                if first <= last:
                    return first <= current_int <= last
                return current_int >= first or current_int <= last
            current_int = _story_to_int(current_value, 0)
            for item in values:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    if checkEventTime(current_int, item):
                        return True
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
