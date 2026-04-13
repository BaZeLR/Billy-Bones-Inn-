# ChangeTommorowHallJob.rpy
# Converted from ChangeTommorowHallJob.txt

label ChangeTommorowHallJob(girl_name=None):
    python:
        GirlName = girl_name
        jobkitchen[GirlName] = jobkitchentomorrow[GirlName]
        jobcleaning[GirlName] = jobcleaningtomorrow[GirlName]
        jobwaitress[GirlName] = jobwaitresstomorrow[GirlName]
    return
