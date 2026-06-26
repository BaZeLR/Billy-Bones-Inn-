# ================================================================================
# Glory-hole assignment conflict check.
# ================================================================================

label GloryHoleBusy(girl_name):
    python:
        checked = str(girl_name or "")
        other_name = "georgett" if checked == "liza" else "liza" if checked == "georgett" else ""
        other = getPersonInfo(other_name) if other_name else None
        result = 1 if other is not None and people_to_int(other.job_value("jobgloryholeTommorow", 0), 0) == 1 else 0
    return result
