# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label ShowGirlSexHistory(args0="", result=""):
    $ renpy.dynamic("iTableLineNum", "table_rows", "_girl_name")
    python:
        iTableLineNum = [1]
        table_rows = ["<table border=1>"]

        def _day_to_text_local(day_number):
            parts = calendar_v2.day_number_to_parts(day_number)
            return calendar_v2.format_date_ru(parts["day"], parts["month"], parts["year"], parts["week"], True)

        def _append_history_rows(history_rows):
            for tmpSexActShow in history_rows:
                _day = _day_to_text_local((tmpSexActShow.get("Day", 0) or 0) - 1)
                _girl_name = str(tmpSexActShow.get("GirlName", "") or "")
                _real_name = people_display_name(_girl_name)
                _dude_name = str(tmpSexActShow.get("DudeName", "") or "")
                _is_dude_random = str(tmpSexActShow.get("IsDudeRandom", "") or "")
                _dude_name_type = str(tmpSexActShow.get("DudeNameType", "") or "")
                _cum_target = str(tmpSexActShow.get("CumTarget", "") or "")
                _zalet = "Залетела!" if int(tmpSexActShow.get("Zalet", 0) or 0) else ""

                table_rows.append("<tr>")
                table_rows.append(f"<td>{iTableLineNum[0]}</td>")
                table_rows.append(f"<td>{_day}</td>")
                table_rows.append(f"<td>{_real_name}</td>")
                table_rows.append(f"<td>{_dude_name}</td>")
                table_rows.append(f"<td>{_is_dude_random}</td>")
                table_rows.append(f"<td>{_dude_name_type}</td>")
                table_rows.append(f"<td>{_cum_target}</td>")
                table_rows.append(f"<td>{_zalet}</td>")
                table_rows.append("</tr>")
                iTableLineNum[0] += 1

        if args0 == "":
            for _girl_name in AllGirlNames:
                _append_history_rows(sex_history_rows(_girl_name))
        else:
            _append_history_rows(sex_history_rows(args0))

        table_rows.append("</table>")
        result = "".join(table_rows)

    "[result]"
    return
