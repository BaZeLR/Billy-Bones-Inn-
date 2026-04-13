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
