# ================================================================================
# Amanda dance event model.
# Owns Amanda Friday dance event checks that are specific to Amanda.
# Scene text stays in IntAmandaDance / AmandaLegareDanceSequence.
# ================================================================================

init -24 python:
    class AmandaDanceEvent(Event):
        def __init__(
            self,
            event_name,
            target,
            calendar_v2.day,
            calendar_v2.hour,
            evt_day,
            probability,
            requirements,
            item,
            location,
            action,
            priority,
            partner="mc",
            sequence=0,
            repeatable=False,
            stage_kind="",
        ):
            super(AmandaDanceEvent, self).__init__(
                (
                    target,
                    calendar_v2.day,
                    calendar_v2.hour,
                    evt_day,
                    probability,
                    requirements,
                    None,
                    item,
                    location,
                    action,
                    priority,
                ),
                "",
                False,
            )
            self.event_name = str(event_name or target or "")
            self.partner = str(partner or "mc")
            self.sequence = int(sequence or 0)
            self.repeatable = bool(repeatable)
            self.stage_kind = str(stage_kind or "")

        def canTrigger(self, evtDay=0):
            if not self.repeatable and story_event_fired_today(self):
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
            if not self.checkItem():
                return False
            if not _story_location_is_open(self.location):
                return False
            return True

        def checkConditions(self):
            return bool(Amanda.dance_event_conditions_met(self))


    def amanda_dance_event(event_name, target, location, action, priority, partner="mc", sequence=0, stage_kind="", repeatable=False):
        return AmandaDanceEvent(
            event_name=event_name,
            target=target,
            day=5,
            hour=(18, 21),
            evt_day=None,
            probability=1,
            requirements=None,
            item=None,
            location=location,
            action=action,
            priority=priority,
            partner=partner,
            sequence=sequence,
            repeatable=repeatable,
            stage_kind=stage_kind,
        )

