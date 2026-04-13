# Increase Skill helper label and function.
default cookincr = {}
default cleanincr = {}
default waitressincr = {}

init python:
    def increase_skill(girl_name):
        """Compute potential skill gain for a tavern worker based on current assignments."""
        if not girl_name:
            return False

        job_kitchen = jobkitchen.get(girl_name, 0)
        job_cleaning = jobcleaning.get(girl_name, 0)
        job_waitress = jobwaitress.get(girl_name, 0)

        girldiv = job_kitchen + job_cleaning + job_waitress
        if girldiv <= 0:
            girldiv = 1

        thresholds = ((50, 1), (65, 2), (80, 3), (90, 4))
        base = 3
        gained = False

        def attempt_gain(job_flag, skill_map, counter_map):
            nonlocal gained
            if job_flag <= 0:
                return
            skill_value = skill_map.get(girl_name, 0)
            if skill_value >= 100:
                return
            incrfine = sum(bonus for threshold, bonus in thresholds if skill_value > threshold)
            roll_max = max(1, (base + incrfine) * girldiv)
            if renpy.random.randint(1, roll_max) == 1:
                counter_map[girl_name] = counter_map.get(girl_name, 0) + 1
                skill_map[girl_name] = skill_value + 1
                gained = True

        attempt_gain(job_kitchen, cooking, cookincr)
        attempt_gain(job_cleaning, cleaning, cleanincr)
        attempt_gain(job_waitress, waitress, waitressincr)

        return gained

label IncreaseSkill(girl_name=None):
    # Help label: delegates to increase_skill() to evaluate daily skill gains.
    python:
        if girl_name:
            increase_skill(girl_name)
        else:
            pass
    return
