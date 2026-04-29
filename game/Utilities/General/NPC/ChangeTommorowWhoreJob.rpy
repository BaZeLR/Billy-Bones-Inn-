# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Tavern job helpers.
init python:
    import renpy as renpy_module

    def change_tomorrow_whore_job(girl_name):
        """Применяет завтрашние назначения на интимные работы с учетом доступности."""
        if not girl_name:
            return

        if jobwhoreTommorow.get(girl_name) == 1:
            jobwhore[girl_name] = 1
            jobgloryhole[girl_name] = 0

        if jobgloryholeTommorow.get(girl_name) == 1:
            jobwhore[girl_name] = 0
            jobgloryhole[girl_name] = 1

        if jobwhore.get(girl_name, 0) and jobgloryhole.get(girl_name, 0):
            jobwhore[girl_name] = 1
            jobgloryhole[girl_name] = 0

        if jobwhore.get(girl_name, 0) == 0 and jobgloryhole.get(girl_name, 0) == 0:
            jobwhore[girl_name] = 1
            jobgloryhole[girl_name] = 0

        if jobWhoreAvail.get(girl_name, 0) == 0:
            jobwhore[girl_name] = 0
        if jobGloryHoleAvail.get(girl_name, 0) == 0:
            jobgloryhole[girl_name] = 0

        jobwhoreTommorow[girl_name] = jobwhore.get(girl_name, 0)
        jobgloryholeTommorow[girl_name] = jobgloryhole.get(girl_name, 0)

    def glory_hole_busy(girl_name):
        """Возвращает True, если место у глорихола уже занято."""
        if not girl_name:
            return False

        if girl_name == 'liza':
            return jobgloryholeTommorow.get('georgett') == 1
        if girl_name == 'georgett':
            return jobgloryholeTommorow.get('liza') == 1
        return False

    def change_tomorrow_hall_job(girl_name):
        """Копирует завтрашние назначения по кухне, уборке и залу."""
        if not girl_name:
            return

        job_kitchen[girl_name] = job_kitchen_tomorrow.get(girl_name, 0)
        job_cleaning[girl_name] = job_cleaning_tomorrow.get(girl_name, 0)
        job_waitress[girl_name] = job_waitress_tomorrow.get(girl_name, 0)

    def get_random_girl_by_job(job_dict_name):
        """Возвращает случайное имя девушки, назначенной на работу из указанного словаря."""
        all_names = AllGirlNames
        job_dict_key = str(job_dict_name or "")
        if job_dict_key == "jobwhore":
            job_dict = jobwhore
        elif job_dict_key == "jobgloryhole":
            job_dict = jobgloryhole
        elif job_dict_key == "jobkitchen":
            job_dict = jobkitchen
        elif job_dict_key == "jobcleaning":
            job_dict = jobcleaning
        elif job_dict_key == "jobwaitress":
            job_dict = jobwaitress
        else:
            job_dict = {}
        if not isinstance(job_dict, dict):
            return ''
        eligible = [name for name in all_names if job_dict.get(name, 0)]
        if not eligible:
            return ''
        return renpy_module.random.choice(eligible)

label ChangeTommorowWhoreJob(girl_name=None):
    # Help label: синхронизирует завтрашние интимные назначения для девушки.
    python:
        if girl_name is None:
            girl_name = GirlName if 'GirlName' in locals() else None
        if girl_name:
            change_tomorrow_whore_job(girl_name)
    return

## NOTE: GloryHoleBusy and ChangeTommorowHallJob are defined in their own files.

label GetRandomGirlByJob(job_dict_name=None):
    # Help label: заносит в RESULT случайную девушку, работающую в заданном словаре.
    python:
        if job_dict_name is None:
            job_dict_name = jobtype if 'jobtype' in locals() else None
        if job_dict_name:
            RESULT = get_random_girl_by_job(job_dict_name)
        else:
            RESULT = ''
    return
