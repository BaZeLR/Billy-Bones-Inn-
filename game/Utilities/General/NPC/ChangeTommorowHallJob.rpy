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

        kitchen_value = int(jobkitchentomorrow.get(person, jobkitchen.get(person, 0)) or 0)
        cleaning_value = int(jobcleaningtomorrow.get(person, jobcleaning.get(person, 0)) or 0)
        waitress_value = int(jobwaitresstomorrow.get(person, jobwaitress.get(person, 0)) or 0)

        jobkitchen[person] = kitchen_value
        jobcleaning[person] = cleaning_value
        jobwaitress[person] = waitress_value

        jobkitchentomorrow[person] = kitchen_value
        jobcleaningtomorrow[person] = cleaning_value
        jobwaitresstomorrow[person] = waitress_value

label ChangeTommorowHallJob(girl_name=None):
    $ apply_tomorrow_hall_job(girl_name)
    return
