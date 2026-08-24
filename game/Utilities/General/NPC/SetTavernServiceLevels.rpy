# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def update_tavern_service_levels():
        service = player.tavern_management.service
        sandradiv = int(Sandra.job_value("jobkitchen", 0) or 0) + int(Sandra.job_value("jobcleaning", 0) or 0) + int(Sandra.job_value("jobwaitress", 0) or 0)
        melissadiv = int(Melissa.job_value("jobkitchen", 0) or 0) + int(Melissa.job_value("jobcleaning", 0) or 0) + int(Melissa.job_value("jobwaitress", 0) or 0)
        amandadiv = int(Amanda.job_value("jobkitchen", 0) or 0) + int(Amanda.job_value("jobcleaning", 0) or 0) + int(Amanda.job_value("jobwaitress", 0) or 0)

        if sandradiv == 0:
            sandradiv = 1
        if melissadiv == 0:
            melissadiv = 1
        if amandadiv == 0:
            amandadiv = 1

        kitchen_score = (
            int(Sandra.job_value("jobkitchen", 0) or 0) * float(Sandra.skill_value("cooking", 0) or 0) / sandradiv
            + int(Melissa.job_value("jobkitchen", 0) or 0) * float(Melissa.skill_value("cooking", 0) or 0) / melissadiv
            + int(Amanda.job_value("jobkitchen", 0) or 0) * float(Amanda.skill_value("cooking", 0) or 0) / amandadiv
        )
        kitchen_max = max(
            int(Sandra.job_value("jobkitchen", 0) or 0) * float(Sandra.skill_value("cooking", 0) or 0),
            int(Melissa.job_value("jobkitchen", 0) or 0) * float(Melissa.skill_value("cooking", 0) or 0),
            int(Amanda.job_value("jobkitchen", 0) or 0) * float(Amanda.skill_value("cooking", 0) or 0),
        )
        kitchen_score = min(kitchen_score, kitchen_max)

        clean_score = (
            int(Sandra.job_value("jobcleaning", 0) or 0) * float(Sandra.skill_value("cleaning", 0) or 0) / sandradiv
            + int(Melissa.job_value("jobcleaning", 0) or 0) * float(Melissa.skill_value("cleaning", 0) or 0) / melissadiv
            + int(Amanda.job_value("jobcleaning", 0) or 0) * float(Amanda.skill_value("cleaning", 0) or 0) / amandadiv
        )

        waitress_score = (
            int(Sandra.job_value("jobwaitress", 0) or 0) * float(Sandra.skill_value("waitress", 0) or 0) / sandradiv
            + int(Melissa.job_value("jobwaitress", 0) or 0) * float(Melissa.skill_value("waitress", 0) or 0) / melissadiv
            + int(Amanda.job_value("jobwaitress", 0) or 0) * float(Amanda.skill_value("waitress", 0) or 0) / amandadiv
        )
        waitress_max = max(
            int(Sandra.job_value("jobwaitress", 0) or 0) * float(Sandra.skill_value("waitress", 0) or 0),
            int(Melissa.job_value("jobwaitress", 0) or 0) * float(Melissa.skill_value("waitress", 0) or 0),
            int(Amanda.job_value("jobwaitress", 0) or 0) * float(Amanda.skill_value("waitress", 0) or 0),
        )
        waitress_score = min(waitress_score, waitress_max)

        service.kitchen_score = kitchen_score
        service.cleanliness_score = clean_score
        service.waitress_score = waitress_score

        if kitchen_score > 90:
            service.kitchen_quality = "божественно"
        elif kitchen_score > 70:
            service.kitchen_quality = "пальчики оближешь"
        elif kitchen_score > 60:
            service.kitchen_quality = "вкусно"
        elif kitchen_score > 50:
            service.kitchen_quality = "сносно"
        elif kitchen_score > 30:
            service.kitchen_quality = "терпимо"
        elif kitchen_score > 14:
            service.kitchen_quality = "отвратительно"
        else:
            service.kitchen_quality = "невыносимо"

        if clean_score > 90:
            service.cleanliness_quality = "идеально чисто"
        elif clean_score > 80:
            service.cleanliness_quality = "практически ни пылинки"
        elif clean_score > 55:
            service.cleanliness_quality = "чисто"
        elif clean_score > 45:
            service.cleanliness_quality = "скорее чисто, чем грязно"
        elif clean_score > 34:
            service.cleanliness_quality = "грязновато"
        elif clean_score > 20:
            service.cleanliness_quality = "грязно"
        elif clean_score > 5:
            service.cleanliness_quality = "очень грязно"
        else:
            service.cleanliness_quality = "тараканы с трудом могут пробраться сквозь липкую грязь покрывающую все"

        if waitress_score > 90:
            service.waitress_quality = "идет так, что и король позавидовал бы"
        elif waitress_score > 80:
            service.waitress_quality = "поставленно прекрасно"
        elif waitress_score > 70:
            service.waitress_quality = "очень хорошее"
        elif waitress_score > 55:
            service.waitress_quality = "на уровне"
        elif waitress_score > 40:
            service.waitress_quality = "так себе"
        elif waitress_score > 25:
            service.waitress_quality = "медленное и неумелое"
        elif waitress_score > 15:
            service.waitress_quality = "почти не производится"
        elif waitress_score > 1:
            service.waitress_quality = "идет так, что только счастливчики могут получить свой заказ, после пары часов ожидания. Обычно же приносят не то, что просили или не приносят вовсе."
        else:
            service.waitress_quality = "не ведется вообще, заказать что-либо у вас невозможно."


label SetTavernServiceLevels:
    $ update_tavern_service_levels()
    return
