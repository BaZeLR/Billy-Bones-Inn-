# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# NamesList.rpy
# Converted from QSP-like script to Ren'Py

init python:
    def get_names_list(jobtype, AllGirlNames, RealName, job_dicts):
        """
        jobtype: string, the name of the job dict (e.g. 'waitress', 'cleaning', etc.)
        AllGirlNames: list of girl keys
        RealName: dict mapping girl keys to real names
        job_dicts: dict of all job dicts, e.g. {'waitress': {...}, 'cleaning': {...}}
        Returns: string with names list or 'никто'
        """
        strtmp = ''
        totalnum = 0
        # Count total number of girls with this job
        for girl in AllGirlNames:
            totalnum += job_dicts[jobtype].get(girl, 0)
        curnum = 0
        for girl in AllGirlNames:
            if job_dicts[jobtype].get(girl, 0) > 0:
                if curnum > 0 and curnum == totalnum - 1:
                    strtmp += ' и '
                elif curnum > 0 and curnum < totalnum - 1:
                    strtmp += ', '
                strtmp += RealName.get(girl, girl)
                curnum += 1
        if totalnum == 0:
            strtmp = 'никто'
        return strtmp

# Example usage in script:
# $result = get_names_list('waitress', AllGirlNames, RealName, {'waitress': waitress, ...})
