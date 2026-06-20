default today_tavern_events = []
init python:
    from collections import defaultdict
    import renpy as renpy_module

    class TavernEvent(python_object):
        __slots__ = ("event_id", "category", "label", "weight", "repeatable", "requires_presence", "summary")

        def __init__(self, category, payload):
            self.category = category
            self.event_id = payload.get("id")
            self.label = payload.get("label", self.event_id)
            self.weight = max(1, int(payload.get("weight", 1)))
            self.repeatable = bool(payload.get("repeatable", False))
            self.requires_presence = bool(payload.get("requires_presence", False))
            self.summary = payload.get("summary")

        def to_dict(self):
            return {
                "id": self.event_id,
                "category": self.category,
                "label": self.label,
                "requires_presence": self.requires_presence,
                "summary": self.summary,
            }

    class TavernEventCatalog(python_object):
        def __init__(self):
            self.defaults = {"max_events": 5, "category_cycle": []}
            self.categories = defaultdict(list)
            self.loaded = False

        def load(self):
            if self.loaded:
                return
            config = load_tavern_events_config() or {}
            self.defaults.update(config.get("defaults", {}))
            for category, items in config.get("categories", {}).items():
                self.categories[category] = [TavernEvent(category, item) for item in items]
            self.loaded = True

        def iter_category(self, name):
            self.load()
            return list(self.categories.get(name, ()))

    catalog = TavernEventCatalog()

    def _rng():
        # use Ren'Py random so seeds respect save/rollback
        return renpy_module.random

    def _available_events(events, used_ids, state=None):
        available = []
        for event in events:
            if (not event.repeatable) and (event.event_id in used_ids):
                continue
            # Placeholder for future state-based checks
            available.append(event)
        return available

    def _choose_event(events, state=None):
        if not events:
            return None
        weights = [evt.weight for evt in events]
        return _rng().choices(events, weights=weights, k=1)[0]

    def clear_daily_tavern_events():
        today_tavern_events[:] = []

    def get_daily_tavern_events():
        return list(today_tavern_events)

    def generate_daily_tavern_events(state=None, max_events=None, category_cycle=None):
        catalog.load()
        max_events = max_events or catalog.defaults.get("max_events", 5)
        cycle = category_cycle or catalog.defaults.get("category_cycle")
        if not cycle:
            cycle = list(catalog.categories.keys())
        plan = []
        used_ids = set()
        if max_events <= 0 or not cycle:
            today_tavern_events[:] = plan
            return plan
        # iterate through cycle until filled or no events
        attempts = 0
        max_attempts = max_events * max(1, len(cycle))
        while len(plan) < max_events and attempts < max_attempts:
            category = cycle[attempts % len(cycle)]
            events = catalog.iter_category(category)
            available = _available_events(events, used_ids, state)
            if available:
                selected = _choose_event(available, state)
                if selected:
                    entry = selected.to_dict()
                    entry['slot'] = len(plan)
                    plan.append(entry)
                    if not selected.repeatable:
                        used_ids.add(selected.event_id)
            attempts += 1
        today_tavern_events[:] = plan
        return plan
