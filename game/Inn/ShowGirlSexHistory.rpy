label ShowGirlSexHistory(args0=""):
    python:
        iTableLineNum = [1]
        table_rows = ["<table border=1>"]

        def _day_to_text_local(day_number):
            DayToTransform = int(day_number or 0) + 1
            WeekToTransform = DayToTransform % 7
            YearToTransform = 1100 + (DayToTransform - (DayToTransform % 365)) // 365
            DayToTransform = DayToTransform % 365

            MonthToTransf = 1
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for days in days_in_month:
                if DayToTransform > days:
                    MonthToTransf += 1
                    DayToTransform -= days
                else:
                    break

            week_names = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
            month_names = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
            return f"{week_names[WeekToTransform]}, {DayToTransform} {month_names[MonthToTransf - 1]} {YearToTransform} года"

        def _append_history_rows(history_rows):
            for tmpSexActShow in history_rows:
                _day = _day_to_text_local((tmpSexActShow.get("Day", 0) or 0) - 1)
                _girl_name = str(tmpSexActShow.get("GirlName", "") or "")
                _real_name = RealName.get(_girl_name, _girl_name)
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
        Result = "".join(table_rows)

    "[Result]"
    return
