init python:
    def amanda_birth_ready():
        try:
            return bool(Amanda.birth_ready())
        except Exception:
            return (
                int(dayspassed or 0) > 0
                and int(pregnancy.get("amanda", 0) or 0) >= 240
                and str(pregfather.get("amanda", "") or "") != ""
            )

    def amanda_pregnancy_check(cum_place, repeat_count=1, dad_name="Вы", is_dude_random=0, dad_name_type=""):
        return Amanda.pregnancy_check(cum_place, repeat_count, dad_name, is_dude_random, dad_name_type)


label story_amanda_give_birth_0:
    call GiveBirth("amanda")
    return True
