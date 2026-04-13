label day_to_text(day_number):
    python:
        # Calculate day, week, year
        DayToTransform = day_number + 1
        WeekToTransform = DayToTransform % 7
        YearToTransform = 1100 + (DayToTransform - (DayToTransform % 365)) // 365
        DayToTransform = DayToTransform % 365
        # Month calculation
        MonthToTransf = 1
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        for i, days in enumerate(days_in_month):
            if DayToTransform > days:
                MonthToTransf += 1
                DayToTransform -= days
            else:
                break
        # Weekday names
        week_names = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        # Month names
        month_names = [
            'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
            'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'
        ]
        week_str = week_names[WeekToTransform]
        month_str = month_names[MonthToTransf-1]
        # Compose result
        result = f"{week_str}, {DayToTransform} {month_str} {YearToTransform} года"
        renpy.store.Result = result
    return
