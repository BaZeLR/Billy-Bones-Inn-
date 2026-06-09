# Draft only. This file is not loaded by Ren'Py because it lives under devdocs.
# Purpose: historical calendar source model.
#
# Current override from the 2026-06-06 rescue plan:
# - live code uses `class Calendar`, not `class CalendarV2`;
# - `calendar_v2` remains the saved instance name during compatibility cleanup;
# - do not reintroduce a separate `game_calendar` helper object or a CalendarV2 class.
#
# Source of truth:
# - minute/hour are the exact hidden clock.
# - day/week/period/cycle/daysInGame are the fantasy date.
# - week means weekday, values 1..7. It is not a week number.
# - time is derived display text only.
# - moon phase is derived from day inside the 28-day period.
# - Sabbats are hidden event hooks. Event/thread code decides discovery and scenes.

init python:
    CALENDAR_V2_MINUTES_PER_HOUR = 60
    CALENDAR_V2_HOURS_PER_DAY = 24
    CALENDAR_V2_DAYS_PER_WEEK = 7
    CALENDAR_V2_DAYS_PER_PERIOD = 28
    CALENDAR_V2_PERIODS_PER_CYCLE = 13

    CALENDAR_V2_WEEKDAYS = (
        {"week": 1, "code_name": "monday", "display_name_ru": "Понедельник", "display_name_en": "Monday"},
        {"week": 2, "code_name": "tuesday", "display_name_ru": "Вторник", "display_name_en": "Tuesday"},
        {"week": 3, "code_name": "wednesday", "display_name_ru": "Среда", "display_name_en": "Wednesday"},
        {"week": 4, "code_name": "thursday", "display_name_ru": "Четверг", "display_name_en": "Thursday"},
        {"week": 5, "code_name": "friday", "display_name_ru": "Пятница", "display_name_en": "Friday"},
        {"week": 6, "code_name": "saturday", "display_name_ru": "Суббота", "display_name_en": "Saturday"},
        {"week": 7, "code_name": "sunday", "display_name_ru": "Воскресенье", "display_name_en": "Sunday"},
    )

    # Display-only fantasy time slots. Schedules and shops use hour/minute.
    CALENDAR_V2_TIME_SLOTS = (
        {"time": 0, "code_name": "early_morning", "display_name_ru": "раннее утро", "display_name_en": "early morning", "start": (6, 0), "end": (7, 59)},
        {"time": 1, "code_name": "morning", "display_name_ru": "утро", "display_name_en": "morning", "start": (8, 0), "end": (10, 59)},
        {"time": 2, "code_name": "noon", "display_name_ru": "полдень", "display_name_en": "noon", "start": (11, 0), "end": (12, 59)},
        {"time": 3, "code_name": "afternoon", "display_name_ru": "после полудня", "display_name_en": "afternoon", "start": (13, 0), "end": (15, 59)},
        {"time": 4, "code_name": "day", "display_name_ru": "день", "display_name_en": "day", "start": (16, 0), "end": (17, 59)},
        {"time": 5, "code_name": "evening", "display_name_ru": "вечер", "display_name_en": "evening", "start": (18, 0), "end": (20, 59)},
        {"time": 6, "code_name": "late_evening", "display_name_ru": "поздний вечер", "display_name_en": "late evening", "start": (21, 0), "end": (22, 59)},
        {"time": 7, "code_name": "night", "display_name_ru": "ночь", "display_name_en": "night", "start": (23, 0), "end": (5, 59)},
    )

    CALENDAR_V2_PERIODS = (
        {"period": 1, "code_name": "beth", "druid_month": "Beth", "sabbat": "Yule", "theme": "Rebirth, New Beginnings", "main_tree": "Birch"},
        {"period": 2, "code_name": "luis", "druid_month": "Luis", "sabbat": "Imbolc", "theme": "Purification, First Light", "main_tree": "Rowan"},
        {"period": 3, "code_name": "nion", "druid_month": "Nion", "sabbat": "", "theme": "Wisdom & Connection", "main_tree": "Ash"},
        {"period": 4, "code_name": "fearn", "druid_month": "Fearn", "sabbat": "Ostara", "theme": "Balance, Spring Awakening", "main_tree": "Alder"},
        {"period": 5, "code_name": "saille", "druid_month": "Saille", "sabbat": "Beltane", "theme": "Fertility, Fire, Passion", "main_tree": "Willow"},
        {"period": 6, "code_name": "huath", "druid_month": "Huath", "sabbat": "", "theme": "Love & Protection", "main_tree": "Hawthorn"},
        {"period": 7, "code_name": "duir", "druid_month": "Duir", "sabbat": "Litha", "theme": "Peak of Light, Strength", "main_tree": "Oak"},
        {"period": 8, "code_name": "tinne", "druid_month": "Tinne", "sabbat": "", "theme": "Balance & Defense", "main_tree": "Holly"},
        {"period": 9, "code_name": "coll", "druid_month": "Coll", "sabbat": "Lughnasadh", "theme": "First Harvest, Gratitude", "main_tree": "Hazel"},
        {"period": 10, "code_name": "muin", "druid_month": "Muin", "sabbat": "", "theme": "Prophecy & Intoxication", "main_tree": "Vine"},
        {"period": 11, "code_name": "gort", "druid_month": "Gort", "sabbat": "Mabon", "theme": "Second Harvest, Balance", "main_tree": "Ivy"},
        {"period": 12, "code_name": "ngetal", "druid_month": "Ngetal", "sabbat": "", "theme": "Harmony & Flexibility", "main_tree": "Reed"},
        {"period": 13, "code_name": "ruis", "druid_month": "Ruis", "sabbat": "Samhain", "theme": "Death, Rebirth, Ancestors", "main_tree": "Elder"},
    )

    CALENDAR_V2_MOON_PHASES = (
        {"index": 0, "code_name": "new_moon", "start_day": 1, "end_day": 4, "fertility_modifier": 0.15, "horny_modifier": 0.10, "mood_modifier": -0.05, "mana_modifier": 0.20},
        {"index": 1, "code_name": "waxing_crescent", "start_day": 5, "end_day": 7, "fertility_modifier": 0.30, "horny_modifier": 0.25, "mood_modifier": 0.00, "mana_modifier": 0.35},
        {"index": 2, "code_name": "first_quarter", "start_day": 8, "end_day": 11, "fertility_modifier": 0.45, "horny_modifier": 0.35, "mood_modifier": 0.05, "mana_modifier": 0.50},
        {"index": 3, "code_name": "waxing_gibbous", "start_day": 12, "end_day": 14, "fertility_modifier": 0.75, "horny_modifier": 0.65, "mood_modifier": 0.10, "mana_modifier": 0.70},
        {"index": 4, "code_name": "full_moon", "start_day": 15, "end_day": 18, "fertility_modifier": 0.95, "horny_modifier": 0.85, "mood_modifier": 0.20, "mana_modifier": 1.00},
        {"index": 5, "code_name": "waning_gibbous", "start_day": 19, "end_day": 21, "fertility_modifier": 0.70, "horny_modifier": 0.55, "mood_modifier": 0.05, "mana_modifier": 0.65},
        {"index": 6, "code_name": "last_quarter", "start_day": 22, "end_day": 25, "fertility_modifier": 0.40, "horny_modifier": 0.30, "mood_modifier": -0.05, "mana_modifier": 0.45},
        {"index": 7, "code_name": "waning_crescent", "start_day": 26, "end_day": 28, "fertility_modifier": 0.20, "horny_modifier": 0.15, "mood_modifier": -0.10, "mana_modifier": 0.25},
    )

    CALENDAR_V2_SABBAT_WINDOWS = (
        {"sabbat": "Yule", "period": 1, "day": 7, "week": 4, "hour": 23, "minute": 0, "places": ["ForestCave", "ForestStoneCircle"]},
        {"sabbat": "Imbolc", "period": 2, "day": 7, "week": 4, "hour": 23, "minute": 0, "places": ["ForestCave", "ForestSpring"]},
        {"sabbat": "Ostara", "period": 4, "day": 7, "week": 4, "hour": 23, "minute": 0, "places": ["ForestStoneCircle"]},
        {"sabbat": "Beltane", "period": 5, "day": 7, "week": 4, "hour": 23, "minute": 0, "places": ["ForestCave", "ForestClearing"]},
        {"sabbat": "Litha", "period": 7, "day": 7, "week": 4, "hour": 23, "minute": 0, "places": ["ForestStoneCircle"]},
        {"sabbat": "Lughnasadh", "period": 9, "day": 7, "week": 4, "hour": 23, "minute": 0, "places": ["ForestCave"]},
        {"sabbat": "Mabon", "period": 11, "day": 7, "week": 4, "hour": 23, "minute": 0, "places": ["ForestStoneCircle", "ForestDarkWoods"]},
        {"sabbat": "Samhain", "period": 13, "day": 7, "week": 4, "hour": 23, "minute": 0, "places": ["ForestCave", "ForestDarkWoods"]},
    )


    class Calendar(object):
        """
        One calendar object.

        Methods change calendar state.
        Labels/screens only display the resulting state.
        """

        def __init__(self, minute=0, hour=8, day=1, week=1, period=1, cycle=1100, daysInGame=0):
            self.minute = minute
            self.hour = hour
            self.day = day
            self.week = week
            self.period = period
            self.cycle = cycle
            self.daysInGame = daysInGame

        def advance_minutes(self, minutes):
            """Advance exact clock time."""
            self.minute += int(minutes or 0)

            while self.minute >= CALENDAR_V2_MINUTES_PER_HOUR:
                self.minute -= CALENDAR_V2_MINUTES_PER_HOUR
                self.hour += 1

            while self.hour >= CALENDAR_V2_HOURS_PER_DAY:
                self.hour -= CALENDAR_V2_HOURS_PER_DAY
                self.advance_day()

            return None

        def advance_day(self):
            """Advance one calendar day."""
            self.day += 1
            self.week += 1
            self.daysInGame += 1

            if self.week > CALENDAR_V2_DAYS_PER_WEEK:
                self.week = 1

            if self.day > CALENDAR_V2_DAYS_PER_PERIOD:
                self.day = 1
                self.period += 1

            if self.period > CALENDAR_V2_PERIODS_PER_CYCLE:
                self.period = 1
                self.cycle += 1

        def sleep_to_morning(self, wake_hour=8, wake_minute=0):
            """Start a new day at wake time."""
            self.advance_day()
            self.hour = int(wake_hour or 0)
            self.minute = int(wake_minute or 0)
            return None

        def set_clock(self, hour, minute=0):
            """Debug helper for exact schedule and shop-hour testing."""
            self.hour = int(hour or 0)
            self.minute = int(minute or 0)
            return None

        def set_date(self, day=None, week=None, period=None, cycle=None, daysInGame=None):
            """Debug helper for event and Sabbat testing."""
            if day is not None:
                self.day = int(day)
            if week is not None:
                self.week = int(week)
            if period is not None:
                self.period = int(period)
            if cycle is not None:
                self.cycle = int(cycle)
            if daysInGame is not None:
                self.daysInGame = int(daysInGame)
            return None

        def clock_minutes(self):
            """Exact hidden clock value for schedules, shops, curfew, and patrols."""
            return self.hour * CALENDAR_V2_MINUTES_PER_HOUR + self.minute

        def is_between_clock(self, start_hour, start_minute, end_hour, end_minute):
            """Check an exact interval. Supports overnight intervals."""
            current = self.clock_minutes()
            start = int(start_hour) * 60 + int(start_minute)
            end = int(end_hour) * 60 + int(end_minute)

            if start <= end:
                return start <= current <= end
            return current >= start or current <= end

        def time_slot(self):
            """Derived HUD slot. Not allowed for schedule logic."""
            for slot in CALENDAR_V2_TIME_SLOTS:
                start_hour, start_minute = slot["start"]
                end_hour, end_minute = slot["end"]
                if self.is_between_clock(start_hour, start_minute, end_hour, end_minute):
                    return slot
            return CALENDAR_V2_TIME_SLOTS[0]

        def weekday(self):
            """Current weekday row."""
            return CALENDAR_V2_WEEKDAYS[self.week - 1]

        def period_data(self):
            """Current Druid period row."""
            return CALENDAR_V2_PERIODS[self.period - 1]

        def moon_phase(self, offset=0):
            """Hidden phase derived from day 1..28."""
            moon_day = ((self.day - 1 + int(offset or 0)) % CALENDAR_V2_DAYS_PER_PERIOD) + 1
            for phase in CALENDAR_V2_MOON_PHASES:
                if phase["start_day"] <= moon_day <= phase["end_day"]:
                    return phase
            return CALENDAR_V2_MOON_PHASES[0]

        def girl_lunar_state(self, girl_info):
            """Girl-specific lunar offset belongs to the girl object."""
            lunar = getattr(girl_info, "lunar_fertility", {})
            offset = int(lunar.get("offset", 0) or 0) if isinstance(lunar, dict) else 0
            return self.moon_phase(offset)

        def sabbat_window(self):
            """Hidden event hook. Event/thread code owns discovery and presentation."""
            for row in CALENDAR_V2_SABBAT_WINDOWS:
                if (
                    row["period"] == self.period
                    and row["day"] == self.day
                    and row["week"] == self.week
                    and row["hour"] == self.hour
                    and row["minute"] == self.minute
                ):
                    return row
            return None

        def data(self):
            """Current state plus derived display/hidden calendar data."""
            time_slot = self.time_slot()
            weekday = self.weekday()
            period = self.period_data()
            moon_phase = self.moon_phase()
            return {
                "minute": self.minute,
                "hour": self.hour,
                "day": self.day,
                "week": self.week,
                "period": self.period,
                "cycle": self.cycle,
                "daysInGame": self.daysInGame,
                "time": time_slot["time"],
                "time_code_name": time_slot["code_name"],
                "time_name_ru": time_slot["display_name_ru"],
                "week_code_name": weekday["code_name"],
                "week_name_ru": weekday["display_name_ru"],
                "period_code_name": period["code_name"],
                "druid_month": period["druid_month"],
                "moon_phase": moon_phase["code_name"],
                "sabbat_window": self.sabbat_window(),
            }


    calendar_v2 = Calendar()
