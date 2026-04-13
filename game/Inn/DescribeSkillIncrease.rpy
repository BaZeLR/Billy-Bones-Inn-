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

        name = RealName.get(girl_name, girl_name)
        messages = []

        if cookincr.get(girl_name, 0) > 0:
            level = level_text(cookincr[girl_name])
            messages.append(f"{name} {level} улучшила свое умение готовить.")

        if cleanincr.get(girl_name, 0) > 0:
            level = level_text(cleanincr[girl_name])
            messages.append(f"{name} {level} улучшила свое умение убираться.")

        if waitressincr.get(girl_name, 0) > 0:
            level = level_text(waitressincr[girl_name])
            messages.append(f"{name} {level} улучшила свои навыки официантки.")

        return messages

label DescribeSkillIncrease(girl_name=None):
    # Help label: shows describe_skill_increase() lines to the player.
    python:
        if girl_name is None:
            girl_name = GirlName if 'GirlName' in locals() else None
        if girl_name:
            for line in describe_skill_increase(girl_name):
                renpy_module.say(None, line)
    return
