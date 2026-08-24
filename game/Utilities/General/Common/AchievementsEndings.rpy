        global player.intimacy.can_cum_daily        global player.intimacy.can_cum_daily        global player.intimacy.can_cum_daily        global player.intimacy.can_cum_daily        global player.intimacy.can_cum_daily        global player.intimacy.can_cum_daily# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default tractir_activated_achievements = set()
default tractir_achieved = set()
default tractir_endings = set()
default tractir_progress_view = "achievements"
default TractirEndingTitle = ""
default TractirEndingBody = ""

default tractir_activated_achievements = set()
default tractir_achieved = set()
default tractir_endings = set()
default tractir_progress_view = "achievements"
default TractirEndingTitle = ""
default TractirEndingBody = ""

default tractir_activated_achievements = set()
default tractir_achieved = set()
default tractir_endings = set()
default tractir_progress_view = "achievements"
default TractirEndingTitle = ""
default TractirEndingBody = ""

define tractir_achievement_order = [
    "first_month_survived",
    "sandra_secured_future",
    "notoriety_25",
    "notoriety_50",
    "notoriety_75",
]

define tractir_achievements = {
    "first_month_survived": (
        "Первый месяц",
        "Вы удержали трактир на ногах первый лунный период. Теперь домочадцы смотрят на вас как на хозяина, с которым надо считаться.",
    ),
    "sandra_secured_future": (
        "Сандра выбрала сторону",
        "Сандра отблагодарила вас после первого серьезного хозяйского месяца и стала заметно крепче удерживать свое место в доме.",
    ),
    "notoriety_25": (
        "На слуху",
        "О вас уже говорят в городе. Не всегда хорошо, но достаточно часто, чтобы это начало работать на репутацию.",
    ),
    "notoriety_50": (
        "Скандальная фигура",
        "Ваше имя стало удобным объяснением для самых разных слухов, драк и неприличных разговоров.",
    ),
    "notoriety_75": (
        "Опасная известность",
        "Город уже знает, что рядом с вами редко бывает спокойно. Это открывает одни двери и закрывает другие.",
    ),
}

define tractir_ending_desc = {
    "bankrupt": (
        "Разорение",
        "Денег больше нет. Кредиторы и городские чиновники быстро объяснили, что трактир без хозяина с деньгами становится трактиром без хозяина.",
    ),
    "empty_tavern": (
        "Пустой зал",
        "Дурная слава стала сильнее вывески. Когда в трактир перестали заходить даже самые упрямые завсегдатаи, содержать его дальше стало невозможно.",
    ),
    "maid_revenge": (
        "Тихая месть",
        "Улыбки домочадцев оказались не прощением. Вы слишком долго принимали их покорность за безопасность.",
    ),
    "boss_death": (
        "Неравная драка",
        "Вы полезли в бой, который не могли вытянуть. В городе быстро забывают смельчаков, которые путают дерзость с силой.",
    ),
}

init -20 python:
    def _tractir_progress_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def tractir_activate_achievement(achievement_id):
        aid = str(achievement_id or "").strip()
        if aid == "" or aid not in tractir_achievements:
            return False
        if aid in tractir_achieved:
            return False
        tractir_activated_achievements.add(aid)
        return True

    def tractir_record_ending(ending_id):
        eid = str(ending_id or "").strip()
        if eid == "" or eid not in tractir_ending_desc:
            return False
        tractir_endings.add(eid)
        return True

    def tractir_check_achievements_apply():
        day_count = _tractir_progress_int(globals().get("dayspassed", 0), 0)
        notoriety_value = _tractir_progress_int(globals().get("notoriety", 0), 0)

        if day_count >= 28:
            tractir_activate_achievement("first_month_survived")

        if _tractir_progress_int(Sandra.var.get("SecuredFuture", 0), 0) > 0:
            tractir_activate_achievement("sandra_secured_future")

        if notoriety_value >= 25:
            tractir_activate_achievement("notoriety_25")
        if notoriety_value >= 50:
            tractir_activate_achievement("notoriety_50")
        if notoriety_value >= 75:
            tractir_activate_achievement("notoriety_75")
        return True

    def tractir_first_active_ending():
        if _tractir_progress_int(globals().get("money", 0), 0) <= 0:
            return "bankrupt"
        if _tractir_progress_int(globals().get("player.tavern_management.visitors", 0), 0) <= 0:
            return "empty_tavern"
        if _tractir_progress_int(Sandra.var.get("MaidRevengeEnding", 0), 0) > 0:
            return "maid_revenge"
        try:
            if _tractir_progress_int(fight.enemy_state.get("fatal_loss", 0), 0) > 0:
                return "boss_death"
        except Exception:
            pass
        return ""

    def tractir_mark_maid_revenge_ready(reason=""):
        Sandra.var["MaidRevengeEnding"] = 1
        Sandra.var["MaidRevengeReason"] = str(reason or "")
        return True

    def tractir_mark_boss_fatal_loss(enemy_id=""):
        try:
            fight_state = fight.enemy_state
        except Exception:
            return False
        fight_state["fatal_loss"] = 1
        fight_state["fatal_enemy"] = str(enemy_id or "")
        return True

    def tractir_apply_sandra_secured_future():
        global player.intimacy.can_cum_daily
        global player.intimacy.can_cum_daily
        if _tractir_progress_int(globals().get("dayspassed", 0), 0) < 28:
            return False
        if _tractir_progress_int(Sandra.var.get("SecuredFuture", 0), 0) > 0:
            return False
        Sandra.var["SecuredFuture"] = 1
        Sandra.var["SecuredFutureDay"] = _tractir_progress_int(globals().get("dayspassed", 0), 0)
        player.intimacy.can_cum_daily = max(1, _tractir_progress_int(player.intimacy.can_cum_daily, 2) - 1)
        tractir_activate_achievement("sandra_secured_future")
        try:
            renpy.notify("После ночи с Сандрой сил на чужие постели стало меньше.")
        except Exception:
            pass
        return True

    def tractir_progress_rows(mode="achievements"):
        rows = []
        if str(mode or "") == "endings":
            for eid in sorted(tractir_ending_desc.keys()):
                title, desc = tractir_ending_desc[eid]
                rows.append({
                    "id": eid,
                    "title": title,
                    "desc": desc,
                    "unlocked": eid in tractir_endings,
                })
            return rows
        for aid in tractir_achievement_order:
            title, desc = tractir_achievements[aid]
            rows.append({
                "id": aid,
                "title": title,
                "desc": desc,
                "unlocked": aid in tractir_achieved,
            })
        return rows


label TractirCheckAchievements:
    $ tractir_check_achievements_apply()
    return


label TractirShowPendingAchievements:
    $ _tractir_pending = [aid for aid in list(tractir_activated_achievements) if aid not in tractir_achieved]
    $ _tractir_pending.sort(key=lambda aid: tractir_achievement_order.index(aid) if aid in tractir_achievement_order else 999)
    while len(_tractir_pending) > 0:
        $ _tractir_aid = _tractir_pending.pop(0)
        $ _tractir_title = tractir_achievements.get(_tractir_aid, ("Достижение", ""))[0]
        $ tractir_achieved.add(_tractir_aid)
        $ renpy.notify("Достижение: " + str(_tractir_title))
    return


label TractirShowEnding(ending_id):
    $ _tractir_eid = str(ending_id or "").strip()
    if _tractir_eid == "" or _tractir_eid not in tractir_ending_desc:
        return
    $ tractir_record_ending(_tractir_eid)
    $ TractirEndingTitle = tractir_ending_desc[_tractir_eid][0]
    $ TractirEndingBody = tractir_ending_desc[_tractir_eid][1]
    call screen tractir_result_card_overlay(TractirEndingTitle, TractirEndingBody)
    return


label TractirCheckEndings:
    $ _tractir_ending_id = tractir_first_active_ending()
    if _tractir_ending_id != "":
        call TractirShowEnding(_tractir_ending_id)
    return _tractir_ending_id


screen tractir_result_card_overlay(title="", body=""):
    modal True
    zorder 145
    add Solid("#00000099")
    frame:
        xalign 0.5
        yalign 0.5
        xsize int(config.screen_width * 0.58)
        ymaximum int(config.screen_height * 0.68)
        padding (28, 24)
        background "#20140d"
        vbox:
            spacing 16
            text str(title or "Итог") size 30 color "#f2d49a" xalign 0.5
            viewport:
                xfill True
                ymaximum int(config.screen_height * 0.45)
                draggable True
                mousewheel True
                text str(body or "") size 22 color "#f7f0de"
            textbutton "Продолжить":
                xalign 0.5
                text_size 22
                action Return()


screen tractir_progress_panel():
    frame:
        xalign 0.5
        yalign 0.5
        xsize int(config.screen_width * 0.62)
        ysize int(config.screen_height * 0.74)
        padding (18, 16)
        background "#000000ee"
        vbox:
            spacing 12
            hbox:
                spacing 12
                textbutton "Достижения":
                    text_size 20
                    action SetVariable("tractir_progress_view", "achievements")
                textbutton "Финалы":
                    text_size 20
                    action SetVariable("tractir_progress_view", "endings")
                textbutton "Закрыть":
                    xalign 1.0
                    text_size 20
                    action SetVariable("main_ui_overlay", "")
            viewport:
                xfill True
                yfill True
                draggable True
                mousewheel True
                vbox:
                    spacing 8
                    for _row in tractir_progress_rows(tractir_progress_view):
                        $ _unlocked = bool(_row.get("unlocked", False))
                        $ _title_color = "#f2d49a" if _unlocked else "#777777"
                        $ _row_bg = "#1f1a14" if _unlocked else "#121212"
                        frame:
                            xfill True
                            padding (10, 8)
                            background _row_bg
                            vbox:
                                spacing 4
                                text str(_row.get("title", "")) size 20 color _title_color
                                if _unlocked:
                                    text str(_row.get("desc", "")) size 16 color "#e8dec9"
                                else:
                                    text "Пока не открыто." size 16 color "#777777"
