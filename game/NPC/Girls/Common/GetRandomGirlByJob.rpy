# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# GetRandomGirlByJob.rpy
# Converted from legacy script. Returns a random girl name by job type.
# All logic and conditions preserved.

init python:
    def _get_job_dict_by_name(jobtype):
        if jobtype == "jobkitchen":
            return jobkitchen
        if jobtype == "jobcleaning":
            return jobcleaning
        if jobtype == "jobwaitress":
            return jobwaitress
        if jobtype == "jobwhore":
            return jobwhore
        if jobtype == "jobgloryhole":
            return jobgloryhole
        return {}

    def get_random_girl_by_job(jobtype):
        # jobtype: string, the name of the job map (for example "jobwaitress")
        candidates = []
        job_map = _get_job_dict_by_name(jobtype)

        for girl in AllGirlNames:
            if int(job_map.get(girl, 0) or 0) > 0:
                candidates.append(girl)

        if candidates:
            return renpy.random.choice(candidates)
        return ""

# Usage: result = get_random_girl_by_job('Waitress')
