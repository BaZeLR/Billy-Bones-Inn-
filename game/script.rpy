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


init -95 python:
    # Unified in-script game calendar/time engine.
    # Keeps legacy globals while adding total counters.

    CALENDAR_START_YEAR = 1100

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
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )
    MONTH_NAMES_RU = (
        "Января",
        "Февраля",
        "Марта",
        "Апреля",
        "Мая",
        "Июня",
        "Июля",
        "Августа",
        "Сентября",
        "Октября",
        "Ноября",
        "Декабря",
    )

    TIME_SLOT_INFO = {
        0: {"name_en": "morning", "name_ru": "утро", "hour": 8},
        1: {"name_en": "noon", "name_ru": "полдень", "hour": 12},
        2: {"name_en": "day", "name_ru": "день", "hour": 16},
        3: {"name_en": "evening", "name_ru": "вечер", "hour": 20},
        4: {"name_en": "night", "name_ru": "ночь", "hour": 23},
    }

    def _cal_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _cal_days_in_month(month, year):
        if month == 2:
            return 28
        if month in (4, 6, 9, 11):
            return 30
        return 31

    def _cal_days_before_month(month, year):
        month = max(1, min(12, _cal_int(month, 1)))
        total = 0
        m = 1
        while m < month:
            total += _cal_days_in_month(m, year)
            m += 1
        return total

    def _cal_sync_slot_from_hour():
        global time, hour
        try:
            h = _cal_int(hour, 8) % 24
        except Exception:
            hour = 8
            h = 8
        if 6 <= h <= 9:
            time = 0
        elif 10 <= h <= 13:
            time = 1
        elif 14 <= h <= 17:
            time = 2
        elif 18 <= h <= 21:
            time = 3
        else:
            time = 4

    def _cal_sync_hour_from_slot():
        global hour, minute, time
        try:
            slot = _cal_int(time, 0)
        except Exception:
            time = 0
            slot = 0
        slot = 0 if slot < 0 else 4 if slot > 4 else slot
        time = slot
        hour = _cal_int(TIME_SLOT_INFO[slot]["hour"], 8)
        try:
            minute = _cal_int(minute, 0) % 60
        except Exception:
            minute = 0

    def _cal_normalize_date():
        global day, month, year, week
        try:
            day = _cal_int(day, 1)
        except Exception:
            day = 1
        try:
            month = _cal_int(month, 1)
        except Exception:
            month = 1
        try:
            year = _cal_int(year, CALENDAR_START_YEAR)
        except Exception:
            year = CALENDAR_START_YEAR
        try:
            week = _cal_int(week, 1)
        except Exception:
            week = 1

        if year < CALENDAR_START_YEAR:
            year = CALENDAR_START_YEAR
        if month < 1:
            month = 1
        while month > 12:
            month -= 12
            year += 1
            try:
                age
                _has_age = True
            except Exception:
                _has_age = False
            if _has_age:
                age = _cal_int(age, 18) + 1

        if week < 1:
            week = 1
        while week > 7:
            week -= 7

        if day < 1:
            day = 1

        while True:
            dim = _cal_days_in_month(month, year)
            if day <= dim:
                break
            day -= dim
            month += 1
            if month > 12:
                month = 1
                year += 1
                try:
                    age
                    _has_age = True
                except Exception:
                    _has_age = False
                if _has_age:
                    age = _cal_int(age, 18) + 1

    def _cal_apply_counters_and_names():
        global dayspassed
        global game_days_count, game_months_count, game_years_count
        global day_of_year, datestr
        global month_name, week_name, month_name_en, week_name_en
        global calendar_month_name_ru, calendar_weekday_name_ru
        global calendar_month_name_en, calendar_weekday_name_en
        global calendar_time_slot_name_ru, calendar_time_slot_name_en

        _year = _cal_int(year, CALENDAR_START_YEAR)
        _month = _cal_int(month, 1)
        _day = _cal_int(day, 1)
        _week = _cal_int(week, 1)
        _slot = _cal_int(time, 0)

        if _month < 1:
            _month = 1
        if _month > 12:
            _month = 12
        if _week < 1:
            _week = 1
        if _week > 7:
            _week = 7
        if _slot < 0:
            _slot = 0
        if _slot > 4:
            _slot = 4

        dayspassed = (_year - CALENDAR_START_YEAR) * 365 + _cal_days_before_month(_month, _year) + (_day - 1)
        if dayspassed < 0:
            dayspassed = 0

        game_days_count = dayspassed
        game_months_count = (_year - CALENDAR_START_YEAR) * 12 + (_month - 1)
        game_years_count = _year - CALENDAR_START_YEAR
        day_of_year = _cal_days_before_month(_month, _year) + _day

        week_name = WEEKDAY_NAMES_RU[_week - 1]
        month_name = MONTH_NAMES_RU[_month - 1]
        week_name_en = WEEKDAY_NAMES_EN[_week - 1]
        month_name_en = MONTH_NAMES_EN[_month - 1]
        calendar_weekday_name_ru = week_name
        calendar_month_name_ru = month_name
        calendar_weekday_name_en = week_name_en
        calendar_month_name_en = month_name_en
        calendar_time_slot_name_ru = TIME_SLOT_INFO[_slot]["name_ru"]
        calendar_time_slot_name_en = TIME_SLOT_INFO[_slot]["name_en"]

        datestr = "%s, %d %s %d" % (week_name_en, _day, month_name_en, _year)

    def calendar_sync_state():
        global hour, minute, day, month, year, week, location, time
        try:
            day
        except Exception:
            day = 1
        try:
            month
        except Exception:
            month = 1
        try:
            year
        except Exception:
            year = CALENDAR_START_YEAR
        try:
            week
        except Exception:
            week = 1

        try:
            hour
            has_hour = True
        except Exception:
            hour = 8
            has_hour = False
        try:
            minute
            has_minute = True
        except Exception:
            minute = 0
            has_minute = False
        try:
            time
            has_slot = True
        except Exception:
            time = 0
            has_slot = False
        if has_hour and has_minute:
            hour = _cal_int(hour, 8) % 24
            minute = _cal_int(minute, 0) % 60

            slot_from_hour = 4
            if 6 <= hour <= 9:
                slot_from_hour = 0
            elif 10 <= hour <= 13:
                slot_from_hour = 1
            elif 14 <= hour <= 17:
                slot_from_hour = 2
            elif 18 <= hour <= 21:
                slot_from_hour = 3

            if has_slot:
                slot_value = _cal_int(time, 0)
                slot_value = 0 if slot_value < 0 else 4 if slot_value > 4 else slot_value
                # Legacy scripts often change only `time`; prefer it on mismatch.
                if slot_value != slot_from_hour:
                    _cal_sync_hour_from_slot()
                else:
                    _cal_sync_slot_from_hour()
            else:
                _cal_sync_slot_from_hour()
        else:
            _cal_sync_hour_from_slot()

        try:
            location
        except Exception:
            try:
                location = CurLoc
            except Exception:
                location = "TavernMain"

        _cal_normalize_date()
        _cal_apply_counters_and_names()
        return

    def calendar_set_time_slot(slot):
        global time
        slot_i = _cal_int(slot, 0)
        if slot_i < 0:
            slot_i = 0
        if slot_i > 4:
            slot_i = 4
        time = slot_i
        _cal_sync_hour_from_slot()
        calendar_sync_state()
        return

    def calendar_advance_minutes(minutes_to_add):
        global hour, minute, day, month, year, week
        calendar_sync_state()
        minutes_to_add = max(0, _cal_int(minutes_to_add, 0))

        while minutes_to_add > 0:
            minute += 1
            if minute >= 60:
                minute = 0
                hour += 1
                if hour >= 24:
                    hour = 0
                    day += 1
                    week += 1
                    if week > 7:
                        week = 1
                    dim = _cal_days_in_month(month, year)
                    if day > dim:
                        day = 1
                        month += 1
                        if month > 12:
                            month = 1
                            year += 1
                            try:
                                age
                                _has_age = True
                            except Exception:
                                _has_age = False
                            if _has_age:
                                age = _cal_int(age, 18) + 1
            minutes_to_add -= 1

        _cal_sync_slot_from_hour()
        _cal_apply_counters_and_names()
        return

    def calendar_advance_slots(slots_to_add=1):
        global time, day, month, year, week
        calendar_sync_state()
        steps = max(0, _cal_int(slots_to_add, 1))
        while steps > 0:
            time += 1
            if time > 4:
                time = 0
                day += 1
                week += 1
                if week > 7:
                    week = 1
                dim = _cal_days_in_month(month, year)
                if day > dim:
                    day = 1
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
                        try:
                            age
                            _has_age = True
                        except Exception:
                            _has_age = False
                        if _has_age:
                            age = _cal_int(age, 18) + 1
            _cal_sync_hour_from_slot()
            steps -= 1
        _cal_apply_counters_and_names()
        return

    def calendar_advance_days(days_to_add=1):
        global day, month, year, week
        calendar_sync_state()
        steps = max(0, _cal_int(days_to_add, 1))
        while steps > 0:
            day += 1
            week += 1
            if week > 7:
                week = 1
            dim = _cal_days_in_month(month, year)
            if day > dim:
                day = 1
                month += 1
                if month > 12:
                    month = 1
                    year += 1
                    try:
                        age
                        _has_age = True
                    except Exception:
                        _has_age = False
                    if _has_age:
                        age = _cal_int(age, 18) + 1
            steps -= 1
        _cal_apply_counters_and_names()
        return

    # Compatibility aliases used by existing status and skip-time code.
    ensure_calendar_state = calendar_sync_state
    advance_minutes = calendar_advance_minutes

    # Ensure counters exist from startup.
    calendar_sync_state()



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
    jump Intro
    return


