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
                    5,
                    (18, 21),
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
            return bool(Amanda.dance_event_conditions_met(self))


    AmandaLegareDanceIntro = AmandaDanceEvent(
        "AmandaLegareDance_0", "story_amanda_legare_dance_0", "FridayDance", "enter", 0,
        partner="legare_intro", sequence=0, stage_kind="intro",
    )
    AmandaLegareDanceTalking = AmandaDanceEvent(
        "AmandaLegareDance_1", "story_amanda_legare_dance_1", "FridayDance", "amanda_dance_legare", 1,
        partner="legare", sequence=1, stage_kind="talking",
    )
    AmandaLegareDanceGroping = AmandaDanceEvent(
        "AmandaLegareDance_2", "story_amanda_legare_dance_2", "FridayDance", "amanda_dance_legare", 2,
        partner="legare", sequence=2, stage_kind="groping",
    )
    AmandaLegareDanceKissing = AmandaDanceEvent(
        "AmandaLegareDance_3", "story_amanda_legare_dance_3", "FridayDance", "amanda_dance_legare", 3,
        partner="legare", sequence=3, stage_kind="kissing",
    )
    AmandaLegareDanceAfter = AmandaDanceEvent(
        "AmandaLegareDance_4", "story_amanda_legare_dance_4", "FridayDance", "amanda_dance_legare", 4,
        partner="legare", sequence=4, stage_kind="after_dance",
    )
    AmandaFridayDanceMC = AmandaDanceEvent(
        "AmandaDance_0", "story_amanda_friday_dance_mc_0", "FridayDance", "amanda_dance_mc", 10,
        partner="mc", sequence=0, stage_kind="mc_dance", repeatable=True,
    )
    AmandaFridayDanceLegare = AmandaDanceEvent(
        "AmandaFridayDanceLegare_0", "story_amanda_friday_dance_legare_0", "FridayDance", "amanda_dance_legare", 20,
        partner="legare", sequence=1, stage_kind="talking", repeatable=True,
    )

