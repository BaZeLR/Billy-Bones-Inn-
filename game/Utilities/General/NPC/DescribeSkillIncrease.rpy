# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Describe skill increases helper.
init python:
    import renpy as renpy_module

    def describe_skill_increase(girl_name):
        """Build lines describing how strongly a girl's skills improved."""
        if not girl_name:
            return []

        def level_text(amount):
            if amount > 4:
                return 'очень сильно'
            if amount > 2:
                return 'значительно'
            if amount > 1:
                return 'заметно'
            return 'немного'

        info = people.get_info(girl_name)
        if info is None:
            return []
        name = people_display_name(girl_name)
        gains = getattr(info, "skill_gains_today", {}) or {}
        messages = []

        if gains.get("cooking", 0) > 0:
            level = level_text(gains["cooking"])
            messages.append(f"{name} {level} улучшила свое умение готовить.")

        if gains.get("cleaning", 0) > 0:
            level = level_text(gains["cleaning"])
            messages.append(f"{name} {level} улучшила свое умение убираться.")

        if gains.get("waitress", 0) > 0:
            level = level_text(gains["waitress"])
            messages.append(f"{name} {level} улучшила свои навыки официантки.")

        return messages

label DescribeSkillIncrease(girl_name=""):
    # Help label: shows describe_skill_increase() lines to the player.
    $ renpy.dynamic("line")
    python:
        if girl_name:
            for line in describe_skill_increase(girl_name):
                renpy_module.say(None, line)
    return
