# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# ChangeTommorowHallJob.rpy
# Converted from ChangeTommorowHallJob.txt

init python:
    def apply_tomorrow_hall_job(girl_name):
        person = str(girl_name or "").strip().lower()
        if not person:
            return

        info = people.get_info(person)
        if info is None:
            return
        for current_key, tomorrow_key in (
            ("jobkitchen", "jobkitchentomorrow"),
            ("jobcleaning", "jobcleaningtomorrow"),
            ("jobwaitress", "jobwaitresstomorrow"),
        ):
            value = int(info.job_value(tomorrow_key, 0) or 0)
            info.set_job_value(current_key, value)
            info.set_job_value(tomorrow_key, value)

