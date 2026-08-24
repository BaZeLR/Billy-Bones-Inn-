# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _girl_job_value(girl_name, jobtype):
        info = people.get_info(girl_name)
        jobs = getattr(info, "jobs", {}) if info is not None else {}
        try:
            return int(jobs.get(str(jobtype or ""), 0) or 0)
        except Exception:
            return 0

    def girls_by_job(jobtype, room_code=None):
        job_key = str(jobtype or "").strip()
        room_key = str(room_code or "").strip()
        candidates = []
        for girl in list(AllGirlNames or []):
            girl_key = str(girl or "").strip().lower()
            if not girl_key:
                continue
            if _girl_job_value(girl_key, job_key) <= 0:
                continue
            if room_key and str(people.location(girl_key) or "") != room_key:
                continue
            candidates.append(girl_key)
        return candidates

    def get_random_girl_by_job(jobtype):
        candidates = girls_by_job(jobtype)
        if candidates:
            return procedural_choice(candidates, key="procedural:NPC/Girls/Common/GetRandomGirlByJob.rpy:procedural_choice:31:1")
        return ""
