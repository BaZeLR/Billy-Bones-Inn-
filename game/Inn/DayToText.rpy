label day_to_text(day_number):
    python:
        parts = calendar_day_number_to_parts(day_number)
        result = calendar_format_date_ru(parts["day"], parts["month"], parts["year"], parts["week"], True)
        renpy.store.Result = result
    return
