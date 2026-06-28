# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label day_to_text(day_number):
    $ _day_to_text_parts = calendar_v2.day_number_to_parts(day_number)
    $ Result = calendar_v2.format_date_ru(_day_to_text_parts["day"], _day_to_text_parts["month"], _day_to_text_parts["year"], _day_to_text_parts["week"], True)
    return
