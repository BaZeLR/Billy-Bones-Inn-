# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label day_to_text(day_number):
    python:
        parts = calendar_v2.day_number_to_parts(day_number)
        result = calendar_v2.format_date_ru(parts["day"], parts["month"], parts["year"], parts["week"], True)
        renpy.store.Result = result
    return
