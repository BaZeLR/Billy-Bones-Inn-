# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def update_tavern_service_levels():
        sandradiv = int(jobkitchen.get("sandra", 0) or 0) + int(jobcleaning.get("sandra", 0) or 0) + int(jobwaitress.get("sandra", 0) or 0)
        melissadiv = int(jobkitchen.get("melissa", 0) or 0) + int(jobcleaning.get("melissa", 0) or 0) + int(jobwaitress.get("melissa", 0) or 0)
        amandadiv = int(jobkitchen.get("amanda", 0) or 0) + int(jobcleaning.get("amanda", 0) or 0) + int(jobwaitress.get("amanda", 0) or 0)

        if sandradiv == 0:
            sandradiv = 1
        if melissadiv == 0:
            melissadiv = 1
        if amandadiv == 0:
            amandadiv = 1

        kitchen_score = (
            int(jobkitchen.get("sandra", 0) or 0) * float(cooking.get("sandra", 0) or 0) / sandradiv
            + int(jobkitchen.get("melissa", 0) or 0) * float(cooking.get("melissa", 0) or 0) / melissadiv
            + int(jobkitchen.get("amanda", 0) or 0) * float(cooking.get("amanda", 0) or 0) / amandadiv
        )
        kitchen_max = max(
            int(jobkitchen.get("sandra", 0) or 0) * float(cooking.get("sandra", 0) or 0),
            int(jobkitchen.get("melissa", 0) or 0) * float(cooking.get("melissa", 0) or 0),
            int(jobkitchen.get("amanda", 0) or 0) * float(cooking.get("amanda", 0) or 0),
        )
        kitchen_score = min(kitchen_score, kitchen_max)

        clean_score = (
            int(jobcleaning.get("sandra", 0) or 0) * float(cleaning.get("sandra", 0) or 0) / sandradiv
            + int(jobcleaning.get("melissa", 0) or 0) * float(cleaning.get("melissa", 0) or 0) / melissadiv
            + int(jobcleaning.get("amanda", 0) or 0) * float(cleaning.get("amanda", 0) or 0) / amandadiv
        )

        waitress_score = (
            int(jobwaitress.get("sandra", 0) or 0) * float(waitress.get("sandra", 0) or 0) / sandradiv
            + int(jobwaitress.get("melissa", 0) or 0) * float(waitress.get("melissa", 0) or 0) / melissadiv
            + int(jobwaitress.get("amanda", 0) or 0) * float(waitress.get("amanda", 0) or 0) / amandadiv
        )
        waitress_max = max(
            int(jobwaitress.get("sandra", 0) or 0) * float(waitress.get("sandra", 0) or 0),
            int(jobwaitress.get("melissa", 0) or 0) * float(waitress.get("melissa", 0) or 0),
            int(jobwaitress.get("amanda", 0) or 0) * float(waitress.get("amanda", 0) or 0),
        )
        waitress_score = min(waitress_score, waitress_max)

        store.tavernkitchen_value = kitchen_score
        store.tavernclean_value = clean_score
        store.tavernwaitress_value = waitress_score

        if kitchen_score > 90:
            store.tavernkitchen = "божественно"
        elif kitchen_score > 70:
            store.tavernkitchen = "пальчики оближешь"
        elif kitchen_score > 60:
            store.tavernkitchen = "вкусно"
        elif kitchen_score > 50:
            store.tavernkitchen = "сносно"
        elif kitchen_score > 30:
            store.tavernkitchen = "терпимо"
        elif kitchen_score > 14:
            store.tavernkitchen = "отвратительно"
        else:
            store.tavernkitchen = "невыносимо"

        if clean_score > 90:
            store.tavernclean = "идеально чисто"
        elif clean_score > 80:
            store.tavernclean = "практически ни пылинки"
        elif clean_score > 55:
            store.tavernclean = "чисто"
        elif clean_score > 45:
            store.tavernclean = "скорее чисто, чем грязно"
        elif clean_score > 34:
            store.tavernclean = "грязновато"
        elif clean_score > 20:
            store.tavernclean = "грязно"
        elif clean_score > 5:
            store.tavernclean = "очень грязно"
        else:
            store.tavernclean = "тараканы с трудом могут пробраться сквозь липкую грязь покрывающую все"

        if waitress_score > 90:
            store.tavernwaitress = "идет так, что и король позавидовал бы"
        elif waitress_score > 80:
            store.tavernwaitress = "поставленно прекрасно"
        elif waitress_score > 70:
            store.tavernwaitress = "очень хорошее"
        elif waitress_score > 55:
            store.tavernwaitress = "на уровне"
        elif waitress_score > 40:
            store.tavernwaitress = "так себе"
        elif waitress_score > 25:
            store.tavernwaitress = "медленное и неумелое"
        elif waitress_score > 15:
            store.tavernwaitress = "почти не производится"
        elif waitress_score > 1:
            store.tavernwaitress = "идет так, что только счастливчики могут получить свой заказ, после пары часов ожидания. Обычно же приносят не то, что просили или не приносят вовсе."
        else:
            store.tavernwaitress = "не ведется вообще, заказать что-либо у вас невозможно."


label SetTavernServiceLevels:
    $ update_tavern_service_levels()
    return
