init python:
    import re

    def strcomp(value, pattern):
        try:
            return 1 if re.search(pattern, str(value), flags=re.IGNORECASE) else 0
        except Exception:
            return 0
