# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.store as store
    import renpy.exports as renpy

    def _kids_compat_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def _kids_compat_get(row_id, col, default=""):
        kids_list = getattr(store, "KidsList", [])
        for row in kids_list:
            if _kids_compat_int(row.get("KidId", 0), 0) == _kids_compat_int(row_id, 0):
                return row.get(col, default)
        return default

    def _kids_compat_set(row_id, col, value):
        kids_list = getattr(store, "KidsList", [])
        for row in kids_list:
            if _kids_compat_int(row.get("KidId", 0), 0) == _kids_compat_int(row_id, 0):
                row[col] = value
                return

    # Save/load compatibility symbol.
    def KidsPeekSexCode(MomName):
        mom_name = str(MomName or "")
        if mom_name == "":
            return 0

        days_passed = _kids_compat_int(getattr(store, "dayspassed", 0), 0)
        rows = [row.get("KidId", 0) for row in getattr(store, "KidsList", [])]
        real_name2 = getattr(store, "RealName2", None)
        if not isinstance(real_name2, dict):
            real_name2 = {}
            store.RealName2 = real_name2

        for row_id in rows:
            if str(_kids_compat_get(row_id, "MomName", "")) != mom_name:
                continue

            born_day = _kids_compat_int(_kids_compat_get(row_id, "DayBorn", 0), 0)
            if days_passed - born_day <= 365 * 2:
                continue

            if renpy.random.randint(1, 100) != 1:
                continue

            show_kid_menu = getattr(store, "ShowKidInteractionMenu", None)
            if callable(show_kid_menu):
                name = str(show_kid_menu(row_id))
            else:
                name = str(_kids_compat_get(row_id, "KidName", "ребенок"))

            kid_name = str(_kids_compat_get(row_id, "KidName", name))
            appearance = str(_kids_compat_get(row_id, "Appearance", "M"))[0:1]
            mom_real = str(real_name2.get(mom_name, mom_name))
            kid_role = "сыночек" if appearance == "M" else "дочка"

            renpy.say(
                None,
                "Вдруг вы заметили что из-за приоткрытой двери за вами удивленно следит " + name + ", " + kid_name + ", " + kid_role + " " + mom_real + ".",
            )

            current_rel = _kids_compat_int(_kids_compat_get(row_id, "MyRelation", 0), 0)
            _kids_compat_set(row_id, "MyRelation", current_rel + 1)
            break

        return 0
