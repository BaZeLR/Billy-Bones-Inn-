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

        girl_key = str(girl_name or "").strip().lower()
        girl_info = people.get_info(girl_key)
        if girl_info is not None:
            if people_to_int(girl_info.job_value("jobwhoreTommorow", 0), 0) == 1:
                girl_info.set_job_value("jobwhore", 1)
                girl_info.set_job_value("jobgloryhole", 0)

            if people_to_int(girl_info.job_value("jobgloryholeTommorow", 0), 0) == 1:
                girl_info.set_job_value("jobwhore", 0)
                girl_info.set_job_value("jobgloryhole", 1)

            if people_to_int(girl_info.job_value("jobwhore", 0), 0) and people_to_int(girl_info.job_value("jobgloryhole", 0), 0):
                girl_info.set_job_value("jobwhore", 1)
                girl_info.set_job_value("jobgloryhole", 0)

            if people_to_int(girl_info.job_value("jobwhore", 0), 0) == 0 and people_to_int(girl_info.job_value("jobgloryhole", 0), 0) == 0:
                girl_info.set_job_value("jobwhore", 1)
                girl_info.set_job_value("jobgloryhole", 0)

            if people_to_int(girl_info.job_value("jobWhoreAvail", 0), 0) == 0:
                girl_info.set_job_value("jobwhore", 0)
            if people_to_int(girl_info.job_value("jobGloryHoleAvail", 0), 0) == 0:
                girl_info.set_job_value("jobgloryhole", 0)

            girl_info.set_job_value("jobwhoreTommorow", girl_info.job_value("jobwhore", 0))
            girl_info.set_job_value("jobgloryholeTommorow", girl_info.job_value("jobgloryhole", 0))
            return

    def glory_hole_busy(girl_name):
        """Возвращает True, если место у глорихола уже занято."""
        if not girl_name:
            return False

        if girl_name == 'liza':
            return _girl_job_value('georgett', 'jobgloryholeTommorow') == 1
        if girl_name == 'georgett':
            return _girl_job_value('liza', 'jobgloryholeTommorow') == 1
        return False

    def change_tomorrow_hall_job(girl_name):
        """Копирует завтрашние назначения по кухне, уборке и залу."""
        apply_tomorrow_hall_job(girl_name)

