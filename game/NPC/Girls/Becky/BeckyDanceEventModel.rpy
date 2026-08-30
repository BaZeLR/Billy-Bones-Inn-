# ================================================================================
# Becky dance event model.
# Owns Becky Friday dance event checks; scene text stays in IntBeckyDance.
# ================================================================================

init -24 python:
    class BeckyDanceEvent(Event):
        def __init__(
            self,
            event_name,
            target,
            location,
            action,
            priority,
            partner="mc",
            sequence=0,
            repeatable=False,
            stage_kind="",
        ):
            super(BeckyDanceEvent, self).__init__(
                (
                    target,
                    None,
                    None,
                    None,
                    1,
                    None,
                    None,
                    None,
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

        def checkConditions(self):
            return bool(Becky.dance_event_conditions_met(self))


    BeckyFridayDanceMC = BeckyDanceEvent(
        "BeckyDance_0", "story_becky_friday_dance_mc_0", "FridayDance", "becky_dance_mc", 10,
        partner="mc", sequence=0, repeatable=True, stage_kind="mc_dance",
    )
