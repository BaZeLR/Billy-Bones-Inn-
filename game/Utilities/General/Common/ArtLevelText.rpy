# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Art Level Text (Skill Level Descriptor)
# Converted from legacy script. Returns a string describing the professional skill level for cooking, waitering, cleaning, etc.
# Arguments: value (int)

label art_level_text(value):
    python:
        if value < 10:
            result = 'совсем неумелая'
        elif value < 20:
            result = 'неумелая'
        elif value < 30:
            result = 'начинающая'
        elif value < 40:
            result = 'посредственная'
        elif value < 50:
            result = 'средняя'
        elif value < 60:
            result = 'умелая'
        elif value < 70:
            result = 'опытная'
        elif value < 80:
            result = 'очень опытная'
        elif value < 90:
            result = 'профессиональная'
        else:
            result = 'просто потрясающая'
        _return = result
    return
