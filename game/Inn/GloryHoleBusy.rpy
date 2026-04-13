label GloryHoleBusy(girl_name):
    python:
        result = 0
        if girl_name == "liza":
            if jobgloryholeTommorow.get("georgett", 0) == 1:
                result = 1
        elif girl_name == "georgett":
            if jobgloryholeTommorow.get("liza", 0) == 1:
                result = 1
    return result
