init python:
    class FranData(PeopleData):
        code_name = "fran"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Франческа",
                fullname="Франческа",
                genitive="Франчески",
                dative="Франческе",
                default_location="",
                description="Франческа - старая жрица Эллоны, встречает прихожан в храме и помогает роженицам.",
                birth_date={"day": 1, "period": 1, "cycle": 1048},
                portrait="images/ellona/Fran1.jpg",
            )
            self.set_daily_schedule(random_intervals=[
                {
                    "label": "francheska_birth_duty_%d" % index,
                    "start_minute": start_minute,
                    "end_minute": end_minute,
                    "priority": 500,
                    "choices": [
                        {"location": "EllonaBirthRoom", "weight": 1, "awake": True, "talkable": False},
                        {"location": "EllonaTemple", "weight": 2, "awake": True, "talkable": True},
                    ],
                }
                for index, (start_minute, end_minute) in enumerate([
                    (360, 480),
                    (480, 660),
                    (660, 780),
                    (780, 960),
                    (960, 1080),
                    (1080, 1260),
                    (1260, 1380),
                    (1380, 360),
                ])
            ])

    class FrancheskaInfo(BaseNPC):
        """Francheska: Ellona temple priestess, talk flags, birth-room state."""
        talk_label = "FrancheskaTalk"
        unknown_name = "Старая жрица"

        def __init__(self, name="fran", **kwargs):
            super().__init__(name, **kwargs)
            self.met = False
            self.asked_about_ellona = False
            self.graces_stage = 0
            self.asked_about_duchess = False
            self.asked_about_duke = False
            self.asked_about_stark = False
            self.asked_about_duchy = False
            self.asked_about_king = False
            self.asked_about_kingdom_relations = False
            self.asked_about_aliens = False
            self.sunday_stories_seen_day = -1

        def busy_now(self):
            return self.getLocation() == "EllonaBirthRoom"

        def visible_now(self):
            return not self.busy_now()

        def interaction_visible(self, room_code=""):
            if str(room_code or "").strip() in ("EllonaTemple", "EllonaBirthRoom"):
                return self.visible_now()
            return super(FrancheskaInfo, self).interaction_visible(room_code)

        def birth_room_available(self):
            return self.visible_now()

        def known_now(self):
            return self.visible_now() and bool(self.known)

        def unknown_now(self):
            return self.visible_now() and not bool(self.known)

        def sleep_note_now(self):
            minute_value = int(calendar_v2.clock_minutes() or 0) % 1440
            return self.visible_now() and (minute_value < 8 * 60 or minute_value >= 21 * 60)

        def sunday_stories_available(self):
            minute_value = int(calendar_v2.clock_minutes() or 0) % 1440
            return (
                int(calendar_v2.week or 0) == 7
                and 8 * 60 <= minute_value <= 12 * 60
                and self.visible_now()
                and int(self.sunday_stories_seen_day or -1) < int(current_game_day() or 0)
            )

define FranStaticData = FranData()
default Francheska = FrancheskaInfo()

label register_francheska_secondary:
    python:
        people.register(FranStaticData, Francheska)
    return
