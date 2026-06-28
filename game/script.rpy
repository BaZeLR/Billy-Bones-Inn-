init python:
    # Base style for the button itself
    style.warning_button = Style(style.default)
    style.warning_button.background = "#FFFFFF"
    style.warning_button.hover_background = "#DDDDDD"
    style.warning_button.xminimum = 200
    style.warning_button.padding = (10, 20)

    # Custom text style with outlines for clarity
    style.warning_button_text = Style(style.default)
    style.warning_button_text.color = "#000000"  # Default text color (overridden in buttons)
    style.warning_button_text.outlines = [(2, "#000000", 0, 0)]  # Black outline

    # Default intro sequence data as fallback
    default_intro_sequence = [
        ("images/general/intro1.png", "Welcome to Tractir!"),
        ("images/general/intro2.png", "A game of adventure and intrigue..."),
        ("images/general/intro3.png", "Your journey begins now!")
    ]

    # Fallback for missing gui/button/*.png files (prevents DynamicImage crash on main menu)
    # These override Ren'Py's default button styles that look for non-existent images.
    style.button.background = Solid("#444444")
    style.button.hover_background = Solid("#666666")
    style.button.insensitive_background = Solid("#222222")
    style.button.selected_background = Solid("#555555")

    style.button_text.color = "#ffffff"
    style.button_text.hover_color = "#ffffff"
    style.button_text.insensitive_color = "#888888"
    style.button_text.selected_color = "#ffffff"

# =============================================================================
# PLAYER STATE VARIABLES - Centralized initialization (recommended in script.rpy)
# These should be defaulted early so they are always available.
# =============================================================================
#some general defaults
default CurLoc = "TavernMain"
# Core stats
default tavernfame=0
default health = 100
default fun = 50
default energy = 100
default age = 18
default money = 10000
default charisma = 0
default reputation = 0
default notoriety = 0
default exploration = 0
default rebellion = 0
default tavernvisitors = 40
default productnum = 200
default winenum = 100
default look = 40
#inventory and equipment
default inventory = []
default playerItems = {}
default EquippedWeapon = ""
default EquippedArmor = ""
# Daily reset flags
default cametoday = 0
default bathedToday = False
default swamToday = False
default PussyWetStart = {}
default Drunk = {}
default pregnancy = {}
default Breastfeed = {}
default Lactate = {}
default ZaletSuspectFinal = {}
default PregTotalSuspects = {}
default virginity = {}
default age_girls = {}
default DateOfBirth = {}
default kids = {}
default beauty = {}
default pregfather = {}
default girltextdesc = {}
default GiftPreferences = {}
default cooking = {}
default cleaning = {}
default waitress = {}
default jobkitchen = {}
default jobcleaning = {}
default jobwaitress = {}
default jobwhore = {}
default jobgloryhole = {}
default jobHallAvail = {}
default jobWhoreAvail = {}
default jobGloryHoleAvail = {}
default jobkitchentomorrow = {}
default jobcleaningtomorrow = {}
default jobwaitresstomorrow = {}
default jobwhoreTommorow = {}
default jobgloryholeTommorow = {}
default SloganFixed = 0
default TavernHole = 0
default TavernGloryHole = 0
default GloryHoleLook = 0
default DanceSponsor = 0
default ChurchDonatedAmount = 0
default CursedByEllona = 0
default CursedByEllonaDays = 0
default householdmembers = 4
default KidsPosobie = 0
default KidBirthPosobie = ""
default ProstitutesKids = 0

# Intimacy / sex limits
default cancumdaily = 2
default LastDaySex = -1
default PlayerLastCumDay = -1

# Sleep / morning state
default PlayerMorningArousalDay = -1
default PlayerWakeStateNotice = ""
default PlayerArousalReasons = []
default PlayerObservedNakedNpcDay = {}
default SleepWakeHourOverride = -1
default SleepWakeMinuteOverride = 0

# Health & Injury system (new)
# Health recovers +20 (or to max 100) during sleep.
# If health drops below 25 due to fight or hunt injury, player gets 3-day forest ban.
default PlayerForestBanUntilDay = 0   # If this > current dayspassed → blocked from forest
default SickDays = 0

# Player chore counters (generic actions)
# These (and the weekly tracking below) are reset/cleared after Sandra's weekly chore check.
default bring_woods = 0          # target 3 (weekly)
default chop_wood = 0            # target 3 (weekly)
default make_fire = 0            # target 3 (weekly)
default clean_ashes = 0          # target 3 (weekly)
default boil_water = 0           # target 7 (weekly)
default clean_upstairs_rooms = 0 # target 3 (weekly)
default PlayerChoresWeek = {}
default UI_chores = {}
default taverncleanliness = 60
default upstairsroomsdirty = 0
default ashesdirtydays = 0

# Weekly chore + visitor tracking state (managed with chores, reset by Sandra weekly eval)
default WeeklyVisitorsTrack = {"sum": 0, "days": 0, "prev_avg": 0.0}
default WeeklyChoresLastEvalStamp = ""

# Restriction / rebel tracking (otkroven = openness, neshlush = rebellion baseline)
# Tied to household weekly evaluation alongside chores.
default otkroven = {}
default neshlush = {}

# Core NPC/player relation state maps.
default CurrentLoc = {}
default HadSex = {}
default GiveOrgasms = {}
default LickPussy = {}
default DayLastOrgasmGiven = {}
default CumFaceYou = {}
default CumFaceOthers = {}
default CumTitsYou = {}
default CumTitsOthers = {}
default CumInsideYou = {}
default CumInsideOthers = {}
default CockInMouth = {}
default CockInPussy = {}
default CockInTits = {}
default CockInAss = {}
default EddieCockInMouth = {}
default EddieCockInPussy = {}
default EddieCockInTits = {}
default YouCockInMouth = {}
default YouCockInPussy = {}
default YouCockInTits = {}
default GrupenSex = {}
default TitsVisible = {}
default PussyVisible = {}
default ShortSkirtNoPanties = {}

# Daily tracking
default FlirtedToday = {}
default GiftedToday = {}
default FuckedToday = {}
default AskedToday = {}
# Player appearance compatibility mirrors. Player.appearance owns these values.
default washDays = 3
default hairCutdays = 14
default dayssincewash = 0
default dayssincehaircut = 0
default PlayerHaircutDaySt = 0
default PlayerDressDaySt = {"villagedress": 0}
default PlayerDressLifeDays = {"villagedress": 42}
default PlayerDestroyedDresses = []
default PlayerItemLifeDays = {}
default costumecondition = 100
# Calendar defaults. calendar_v2 is the single initialized Calendar instance.
# The scalar values below are display/legacy mirrors for existing labels and screens.
default day = 1
default month = 1
default year = CALENDAR_START_CYCLE
default week = 1
default hour = 8
default minute = 0
default time = 0
default dayspassed = 0
default clock_minutes = 480
default calendar_v2 = Calendar(minute=0, hour=8, day=1, week=1, period=1, cycle=CALENDAR_START_CYCLE, daysInGame=0)
default week_name = "Понедельник"
default month_name = "Луна Волка"
default week_name_en = "Monday"
default month_name_en = "Wolf Moon"
default calendar_weekday_name_ru = "Понедельник"
default calendar_month_name_ru = "Луна Волка"
default calendar_weekday_name_en = "Monday"
default calendar_month_name_en = "Wolf Moon"
default calendar_cycle_name_ru = "Цикл 1"
default calendar_cycle_name_en = "Cycle 1"
default calendar_time_slot_name_ru = "Утро"
default calendar_time_slot_name_en = "morning"
default datestr = ""
default ClientsDayTotal = {}
init python:
    def load_intro_sequence():
        try:
            import json
            import os

            # First try to load from game/json directory
            try:
                path = renpy.loader.transfn("json/intro_sequence.json")
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [(item['image'], item['text']) for item in data]
            except Exception:
                # If that fails, try to create the directory and file with default data
                try:
                    json_dir = os.path.join(renpy.config.gamedir, "json")
                    if not os.path.exists(json_dir):
                        os.makedirs(json_dir)

                    json_path = os.path.join(json_dir, "intro_sequence.json")
                    default_data = [{"image": img, "text": txt} for img, txt in default_intro_sequence]

                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(default_data, f, indent=2, ensure_ascii=False)

                    return default_intro_sequence
                except Exception:
                    # If creating the file fails too, just return the defaults
                    return default_intro_sequence
        except Exception as e:
            renpy.notify(f"Error loading intro sequence: {e}")
            return default_intro_sequence

    def procedural_seed(key=""):
        key_text = str(key or "")
        key_total = 0
        for index, char_value in enumerate(key_text):
            key_total += (index + 1) * ord(char_value)
        try:
            day_value = int(day or 0)
        except Exception:
            day_value = 0
        try:
            month_value = int(month or 0)
        except Exception:
            month_value = 0
        try:
            week_value = int(week or 0)
        except Exception:
            week_value = 0
        try:
            time_value = int(time or 0)
        except Exception:
            time_value = 0
        return (
            current_game_day() * 1009
            + day_value * 97
            + month_value * 53
            + week_value * 31
            + time_value * 17
            + key_total
        )

    def current_game_day(day_value=None):
        if day_value is not None:
            try:
                return int(day_value)
            except Exception:
                return 0
        try:
            return int(calendar_v2.daysInGame)
        except Exception:
            try:
                return int(dayspassed or 0)
            except Exception:
                return 0

    def day_delta_since(start_day, current_day=None):
        try:
            start_value = int(start_day)
        except Exception:
            start_value = 0
        return max(0, current_game_day(current_day) - start_value)

    def day_delta_ready(start_day, delta_days=1, current_day=None):
        try:
            start_value = int(start_day)
        except Exception:
            start_value = 0
        try:
            delta_value = int(delta_days)
        except Exception:
            delta_value = 1
        return current_game_day(current_day) >= start_value + max(0, delta_value)

    def day_timer_decrement(value, amount=1):
        try:
            current_value = int(value)
        except Exception:
            current_value = 0
        try:
            amount_value = int(amount)
        except Exception:
            amount_value = 1
        return max(0, current_value - max(0, amount_value))

    def procedural_index(count=0, key=""):
        count_value = int(count or 0)
        if count_value <= 0:
            return 0
        return abs(int(procedural_seed(key))) % count_value

    def procedural_choice(seq, key=""):
        values = list(seq or [])
        if len(values) <= 0:
            return None
        return values[procedural_index(len(values), key)]

    def procedural_random(key=""):
        return procedural_index(1000000, key) / 1000000.0

    def procedural_shuffle(seq, key=""):
        if seq is None:
            return []
        keyed_values = []
        for index, value in enumerate(list(seq)):
            keyed_values.append((procedural_seed("%s:%s:%s" % (key, index, value)), value))
        keyed_values.sort(key=lambda row: row[0])
        ordered_values = [value for _, value in keyed_values]
        try:
            seq[:] = ordered_values
            return seq
        except Exception:
            return ordered_values

    def procedural_randint(a, b=None, key=""):
        if b is None:
            low_value = 0
            high_value = int(a or 0)
        else:
            low_value = int(a or 0)
            high_value = int(b or 0)
        if high_value < low_value:
            low_value, high_value = high_value, low_value
        return low_value + procedural_index(high_value - low_value + 1, key)

# explicit picture are allowed in this project
init -95 python:
    # Calendar/time engine.
    # calendar_v2 is the mutable source of truth.
    # day/month/year/week/hour/minute/time/dayspassed/clock_minutes are mirrors
    # for existing labels, screens, schedules, and save displays.

    CALENDAR_START_CYCLE = 1100
    CALENDAR_START_YEAR = CALENDAR_START_CYCLE

    WEEKDAY_NAMES_EN = (
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    )
    WEEKDAY_NAMES_RU = (
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье",
    )
    MONTH_NAMES_EN = (
        "Wolf Moon",
        "Ashen Veil Moon",
        "Thorn Crown Moon",
        "Blood Rose Moon",
        "Honeyed Moon",
        "Stag Crown Moon",
        "Emberwake Moon",
        "Reaper's Lantern Moon",
        "Widowfrost Moon",
        "Hunt-Bell Moon",
        "Long Dark Moon",
        "Root-and-Bone Moon",
        "Black Eclipse Moon",
    )
    MONTH_NAMES_RU = (
        "Луна Волка",
        "Луна Пепельной Завесы",
        "Луна Тернового Венца",
        "Луна Кровавой Розы",
        "Медовая Луна",
        "Луна Оленьего Венца",
        "Луна Тлеющего Пробуждения",
        "Луна Фонаря Жнеца",
        "Луна Вдовьего Мороза",
        "Луна Охотничьего Колокола",
        "Луна Долгой Тьмы",
        "Луна Корней и Костей",
        "Луна Черного Затмения",
    )

    # Fancy moon month / period names (improved flavor for the game world)
    # These are used for display while keeping the numeric period system untouched.
    FANCY_MOON_NAMES_EN = MONTH_NAMES_EN

    FANCY_MOON_NAMES_RU = MONTH_NAMES_RU

    # Simple moon phase names (flavor only, derived from day within the ~28-day period)
    MOON_PHASE_NAMES_EN = (
        "New Moon",
        "Waxing Crescent",
        "First Quarter",
        "Waxing Gibbous",
        "Full Moon",
        "Waning Gibbous",
        "Last Quarter",
        "Waning Crescent",
    )

    MOON_PHASE_NAMES_RU = (
        "Новолуние",
        "Растущий Серп",
        "Первая Четверть",
        "Растущая Луна",
        "Полнолуние",
        "Убывающая Луна",
        "Последняя Четверть",
        "Убывающий Серп",
    )

    TIME_SLOT_INFO = {
        0: {"name_en": "early morning", "name_ru": "раннее утро", "hour": 6},
        1: {"name_en": "morning", "name_ru": "утро", "hour": 8},
        2: {"name_en": "noon", "name_ru": "полдень", "hour": 11},
        3: {"name_en": "afternoon", "name_ru": "после полудня", "hour": 13},
        4: {"name_en": "day", "name_ru": "день", "hour": 16},
        5: {"name_en": "evening", "name_ru": "вечер", "hour": 18},
        6: {"name_en": "late evening", "name_ru": "поздний вечер", "hour": 21},
        7: {"name_en": "night", "name_ru": "ночь", "hour": 23},
    }

    def _cal_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    class Calendar(object):
        def __init__(self, minute=0, hour=8, day=1, week=1, period=1, cycle=CALENDAR_START_CYCLE, daysInGame=0):
            self.minute = _cal_int(minute, 0)
            self.hour = _cal_int(hour, 8)
            self.day = _cal_int(day, 1)
            self.week = _cal_int(week, 1)
            self.period = _cal_int(period, 1)
            self.cycle = _cal_int(cycle, CALENDAR_START_CYCLE)
            self.daysInGame = _cal_int(daysInGame, 0)

        def advance_minutes(self, minutes):
            self.minute += max(0, _cal_int(minutes, 0))

            while self.minute >= 60:
                self.minute -= 60
                self.hour += 1

            while self.hour >= 24:
                self.hour -= 24
                self.day += 1
                self.week += 1
                self.daysInGame += 1

                if self.week > 7:
                    self.week = 1

                if self.day > 28:
                    self.day = 1
                    self.period += 1

                if self.period > 13:
                    self.period = 1
                    self.cycle += 1
            self.sync_state()

        def clock_minutes(self):
            return self.hour * 60 + self.minute

        def is_between_clock(self, start_hour, start_minute, end_hour, end_minute):
            current = self.clock_minutes()
            start = (_cal_int(start_hour, 0) % 24) * 60 + (_cal_int(start_minute, 0) % 60)
            end = (_cal_int(end_hour, 0) % 24) * 60 + (_cal_int(end_minute, 0) % 60)

            if start <= end:
                return start <= current <= end
            return current >= start or current <= end

        def time_slot(self):
            return self.slot_from_hour(self.hour)

        def hud_data(self):
            """Calendar values prepared for the right-side HUD."""
            week_index = max(0, min(6, _cal_int(self.week, 1) - 1))
            period_index = max(0, min(12, _cal_int(self.period, 1) - 1))
            slot = max(0, min(7, self.time_slot()))
            return {
                "time_name_ru": TIME_SLOT_INFO[slot]["name_ru"],
                "time_name_en": TIME_SLOT_INFO[slot]["name_en"],
                "week_name_ru": WEEKDAY_NAMES_RU[week_index],
                "week_name_en": WEEKDAY_NAMES_EN[week_index],
                "day": int(self.day),
                "period_name_ru": MONTH_NAMES_RU[period_index],
                "period_name_en": MONTH_NAMES_EN[period_index],
                "cycle": int(self.cycle),
                "days_in_game": int(self.daysInGame),
            }

        def slot_from_hour(self, hour_value):
            h = _cal_int(hour_value, 8) % 24
            if 6 <= h < 8:
                return 0
            if 8 <= h < 11:
                return 1
            if 11 <= h < 13:
                return 2
            if 13 <= h < 16:
                return 3
            if 16 <= h < 18:
                return 4
            if 18 <= h < 21:
                return 5
            if 21 <= h < 23:
                return 6
            return 7

        # --- Moon name helpers (flavor only, no changes to time variables or slots) ---

        def moon_name_en(self, period=None, cycle=None):
            p = _cal_int(period if period is not None else month, 1)
            p = max(1, min(13, p))
            if p > len(FANCY_MOON_NAMES_EN):
                p = len(FANCY_MOON_NAMES_EN)
            return FANCY_MOON_NAMES_EN[p - 1]

        def moon_name_ru(self, period=None, cycle=None):
            p = _cal_int(period if period is not None else month, 1)
            p = max(1, min(13, p))
            if p > len(FANCY_MOON_NAMES_RU):
                p = len(FANCY_MOON_NAMES_RU)
            return FANCY_MOON_NAMES_RU[p - 1]

        def moon_phase_name_en(self, day_in_period=None, period=None):
            d = _cal_int(day_in_period if day_in_period is not None else day, 1)
            phase_index = ((d - 1) // 4) % 8   # 28 days / 8 phases
            return MOON_PHASE_NAMES_EN[phase_index]

        def moon_phase_name_ru(self, day_in_period=None, period=None):
            d = _cal_int(day_in_period if day_in_period is not None else day, 1)
            phase_index = ((d - 1) // 4) % 8
            return MOON_PHASE_NAMES_RU[phase_index]

        def clock_text(self, hour_value=None, minute_value=None):
            h = _cal_int(hour if hour_value is None else hour_value, 8) % 24
            m = _cal_int(minute if minute_value is None else minute_value, 0) % 60
            return "%02d:%02d" % (h, m)

        # Display/test conversion only. This does not advance gameplay time.
        # Live uses: DayToText, sex-history date display, external test probes.
        def day_number_to_parts(self, day_number):
            day_index = max(0, _cal_int(day_number, 0))
            cycle = CALENDAR_START_CYCLE + (day_index // 364)
            remaining = day_index % 364
            period = (remaining // 28) + 1
            return {
                "day": (remaining % 28) + 1,
                "month": period,
                "year": cycle,
                "week": (day_index % 7) + 1,
            }

        def format_date_ru(self, day_value=None, month_value=None, year_value=None, week_value=None, include_weekday=True):
            cycle = _cal_int(year if year_value is None else year_value, CALENDAR_START_CYCLE)
            period = _cal_int(month if month_value is None else month_value, 1)
            day_num = _cal_int(day if day_value is None else day_value, 1)
            weekday = max(1, min(7, _cal_int(week if week_value is None else week_value, 1)))
            period = max(1, min(13, period))
            base = "%d %s, цикл %d" % (day_num, self.moon_name_ru(period, cycle), cycle)
            if include_weekday:
                return "%s, %s" % (WEEKDAY_NAMES_RU[weekday - 1], base)
            return base

        def format_date_en(self, day_value=None, month_value=None, year_value=None, week_value=None, include_weekday=True):
            cycle = _cal_int(year if year_value is None else year_value, CALENDAR_START_CYCLE)
            period = _cal_int(month if month_value is None else month_value, 1)
            day_num = _cal_int(day if day_value is None else day_value, 1)
            weekday = max(1, min(7, _cal_int(week if week_value is None else week_value, 1)))
            period = max(1, min(13, period))
            base = "%d %s, Cycle %d" % (day_num, self.moon_name_en(period, cycle), cycle)
            if include_weekday:
                return "%s, %s" % (WEEKDAY_NAMES_EN[weekday - 1], base)
            return base

        def time_status_text(self):
            self.sync_state()
            slot = self.slot_from_hour(self.hour)
            slot_name = TIME_SLOT_INFO.get(slot, TIME_SLOT_INFO[1])["name_ru"]
            return "%s (%s)" % (self.clock_text(self.hour, self.minute), slot_name)

        def apply_counters_and_names(self):
            global dayspassed
            global game_days_count, game_months_count, game_years_count
            global day_of_year, datestr
            global month_name, week_name, month_name_en, week_name_en
            global calendar_month_name_ru, calendar_weekday_name_ru
            global calendar_month_name_en, calendar_weekday_name_en
            global calendar_cycle_name_ru, calendar_cycle_name_en
            global calendar_time_slot_name_ru, calendar_time_slot_name_en

            _year = _cal_int(year, CALENDAR_START_CYCLE)
            _month = max(1, min(13, _cal_int(month, 1)))
            _day = _cal_int(day, 1)
            _week = max(1, min(7, _cal_int(week, 1)))
            _slot = max(0, min(7, _cal_int(time, 0)))

            game_days_count = dayspassed
            game_months_count = max(0, dayspassed // 28)
            game_years_count = _year - CALENDAR_START_CYCLE
            day_of_year = ((_month - 1) * 28) + _day

            week_name = WEEKDAY_NAMES_RU[_week - 1]
            month_name = MONTH_NAMES_RU[_month - 1]
            week_name_en = WEEKDAY_NAMES_EN[_week - 1]
            month_name_en = MONTH_NAMES_EN[_month - 1]
            calendar_weekday_name_ru = week_name
            calendar_month_name_ru = month_name
            calendar_weekday_name_en = week_name_en
            calendar_month_name_en = month_name_en
            calendar_cycle_name_ru = "Цикл %d" % _year
            calendar_cycle_name_en = "Cycle %d" % _year
            calendar_time_slot_name_ru = TIME_SLOT_INFO[_slot]["name_ru"]
            calendar_time_slot_name_en = TIME_SLOT_INFO[_slot]["name_en"]
            datestr = self.format_date_en(_day, _month, _year, _week, True)

        def sync_state(self):
            global day, month, year, week, hour, minute, time, dayspassed, clock_minutes, location
            day = int(self.day)
            month = int(self.period)
            year = int(self.cycle)
            week = int(self.week)
            hour = int(self.hour)
            minute = int(self.minute)
            time = int(self.time_slot())
            dayspassed = int(self.daysInGame)
            clock_minutes = int(self.clock_minutes())
            try:
                location
            except Exception:
                try:
                    location = CurLoc
                except Exception:
                    location = "TavernMain"
            self.apply_counters_and_names()
            return

screen splash_screen():
    tag menu
    window:
        background "#000000"
        xfill True
        yfill True

    # Custom image overlay with resize
    add Transform("images/general/kitty_splash.png", zoom=0.4, fit="contain") xalign 0.5 yalign 0.2

    # Humorous warning text
    vbox:
        xalign 0.5
        yalign 0.7
        spacing 15

        text "⚠️ WARNING: THIS GAME IS FOR GROWN-UPS! ⚠️" size 32 color "#FF0000" xalign 0.5
        text "If you’re reading this, congratulations – you can read!" color "#ffffff" xalign 0.5
        text "Before you jump into this wild ride, be warned:\nMature themes, dangerous levels of sass,\nand plotlines that could make your grandma faint!" color "#ffffff" xalign 0.5

        # Centered final lines
        text "For your own safety, you MUST be at least 18 years old to continue." color "#ffffff" xalign 0.5
        text "👑 Are you brave? Hit the Green button to Continue.\n🚫 Not 18? Hit the red button to Exit and never come back!" color "#ffffff" xalign 0.5

    # Buttons
    hbox:
        xalign 0.5
        yalign 0.9
        spacing 50

        textbutton "Continue" action Return() style "warning_button":
            foreground "#006400"
            hover_foreground "#228B22"
            text_style "warning_button_text"  # Apply text style with outlines

        textbutton "Exit" action Quit(confirm=False) style "warning_button":
            foreground "#8B0000"
            hover_foreground "#FF0000"
            text_style "warning_button_text"  # Apply text style with outlines

transform fade:
    alpha 0.0
    linear 1.0 alpha 1.0

transform fade_in:
    alpha 0.0
    linear 1.0 alpha 1.0

transform fade_out:
    alpha 1.0
    linear 1.0 alpha 0.0

screen cinematic_intro(images_texts):
    tag menu
    modal True
    default idx = 0

    if not images_texts:
        timer 0.01 action Return()
    else:
        $ _img = images_texts[idx][0]
        $ _txt = images_texts[idx][1]

        if renpy.loadable(_img):
            add _img at fade_in
        else:
            add Solid("#000")

        window:
            background "#00000080"
            xalign 0.5
            yalign 0.5
            xsize 1000
            ysize None
            padding (20, 20)

            text _txt:
                xalign 0.5
                color "#FFFFFF"
                text_align 0.5
                size 24
                layout "subtitle"
                min_width 960

        hbox:
            xalign 0.5
            yalign 0.92
            spacing 24

            textbutton "Continue" action If(
                idx < len(images_texts) - 1,
                SetScreenVariable("idx", idx + 1),
                Return()
            )

            textbutton "Skip" action Return()

        key "mouseup_1" action If(
            idx < len(images_texts) - 1,
            SetScreenVariable("idx", idx + 1),
            Return()
        )
        key "K_SPACE" action If(
            idx < len(images_texts) - 1,
            SetScreenVariable("idx", idx + 1),
            Return()
        )
        key "K_RETURN" action If(
            idx < len(images_texts) - 1,
            SetScreenVariable("idx", idx + 1),
            Return()
        )

label splashscreen:
    call screen splash_screen
    return

label start:
    jump Intro

#label intro:
#    jump Intro

label introduction:
    $ intro_data = load_intro_sequence()
    if intro_data:
        call screen cinematic_intro(intro_data) with dissolve
    else:
        "Introduction sequence is not available yet."
    return

label tutorial:
    "Tutorial is a placeholder for now."
    return

label about_game:
    "About the game is a placeholder for now."
    return

label cinematic_intro:
    $ intro_data = load_intro_sequence()
    if intro_data:
        call screen cinematic_intro(intro_data) with dissolve
    else:
        "Introduction sequence is not available yet."
    return
