# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Increase Skill helper label and function.
init python:
    def increase_skill(girl_name):
        """Compute potential skill gain for a tavern worker based on current assignments."""
        if not girl_name:
            return False

        info = people.get_info(girl_name)
        if info is None:
            return False
        job_kitchen = info.job_value("jobkitchen", 0)
        job_cleaning = info.job_value("jobcleaning", 0)
        job_waitress = info.job_value("jobwaitress", 0)

        girldiv = job_kitchen + job_cleaning + job_waitress
        if girldiv <= 0:
            girldiv = 1

        thresholds = ((50, 1), (65, 2), (80, 3), (90, 4))
        base = 3
        gained = False

        def attempt_gain(job_flag, skill_key):
            nonlocal gained
            if job_flag <= 0:
                return
            skill_value = info.skill_value(skill_key, 0)
            if skill_value >= 100:
                return
            incrfine = sum(bonus for threshold, bonus in thresholds if skill_value > threshold)
            roll_max = max(1, (base + incrfine) * girldiv)
            if procedural_randint(1, roll_max, key="procedural:Utilities/General/NPC/IncreaseSkill.rpy:procedural_randint:36:1") == 1:
                info.record_skill_gain(skill_key)
                info.set_skill(skill_key, skill_value + 1)
                gained = True

        attempt_gain(job_kitchen, "cooking")
        attempt_gain(job_cleaning, "cleaning")
        attempt_gain(job_waitress, "waitress")

        return gained

label IncreaseSkill(girl_name=None):
    # Help label: delegates to increase_skill() to evaluate daily skill gains.
    python:
        if girl_name:
            increase_skill(girl_name)
        else:
            pass
    return
