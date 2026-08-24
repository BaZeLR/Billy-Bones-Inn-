init -50 python:
    class StoryEventRuntimeState(object):
        def __init__(self):
            self.active_thread = None
            self.tavern_work_events = []
            self.tavern_played_today = []
            self.tavern_report_rows = []
            self.tavern_work_plan_day = -1
            self.available = {}
            self.evaluation_time = None
            self.locations = set()
            self.people = set()
            self.talk = set()
            self.options = set()
            self.items = set()
            self.paths = set()
            self.projection_rows = []
            self.route_hints = {}
            self.fired_day = -1
            self.fired_keys_today = []


default event_runtime = StoryEventRuntimeState()
