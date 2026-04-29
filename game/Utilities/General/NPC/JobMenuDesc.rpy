# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def JobMenuDesc(assignment_status, job_type):
        """Формирует строки для назначения или отмены завтрашней работы."""
        job_texts = {
            1: ("кухне", "Кухня"),
            2: ("уборке", "Уборка"),
            3: ("обслуживании в зале", "Обслуживание в зале"),
        }
        assign_phrase, remove_phrase = job_texts.get(job_type, ("работе", "Работа"))

        if assignment_status == 0:
            return f"Назначить завтра работать на {assign_phrase}"
        return f"{remove_phrase} - отменить завтрашнее назначение"
