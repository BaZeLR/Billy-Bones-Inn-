# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def _zalet_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def _zalet_text(value):
        if value is None:
            return ""
        return str(value).strip().lower()

    def _zalet_truthy(value):
        return _zalet_to_int(value, 0) != 0

    def _zalet_history_rows(girl_name):
        return sex_history_rows(girl_name)

    def ZaletSuspectLinesCount(girl_name):
        return len(ZaletSuspectFinal.get(str(girl_name), []))

    def ZaletSuspectGetValue(girl_name, row_ref, column, default=""):
        suspects = ZaletSuspectFinal.get(str(girl_name), [])
        row_index = _zalet_to_int(row_ref, 0) - 1
        if row_index < 0 or row_index >= len(suspects):
            return default
        return suspects[row_index].get(column, default)

    def ZaletClearSuspectList(girl_name):
        girl_name = str(girl_name)
        ZaletSuspectFinal[girl_name] = []
        PregTotalSuspects[girl_name] = 0
        return 0

    def ZaletGetExactDay(girl_name):
        tmp_cur_day = -1
        for row in _zalet_history_rows(girl_name):
            if not _zalet_truthy(row.get("Zalet", 0)):
                continue
            row_day = _zalet_to_int(row.get("Day", 0), 0)
            if row_day > tmp_cur_day:
                tmp_cur_day = row_day
        return tmp_cur_day

    def ZaletGetExactId(girl_name):
        tmp_cur_day = 0
        result = 0
        for row in _zalet_history_rows(girl_name):
            if not _zalet_truthy(row.get("Zalet", 0)):
                continue
            row_day = _zalet_to_int(row.get("Day", 0), 0)
            if row_day > tmp_cur_day:
                tmp_cur_day = row_day
                result = _zalet_to_int(row.get("RowId", 0), 0)
        return result

    def ZaletGetSuspectList(girl_name, day_span=0):
        girl_name = str(girl_name)
        zalet_day = ZaletGetExactDay(girl_name)
        day_span = _zalet_to_int(day_span, 0)
        if day_span == 0:
            day_span = 15

        ZaletClearSuspectList(girl_name)
        if zalet_day <= 0:
            return 0

        suspect_rows = []
        for row in _zalet_history_rows(girl_name):
            row_day = _zalet_to_int(row.get("Day", 0), 0)
            if _zalet_text(row.get("CumTarget", "")) != "inside":
                continue
            if not (row_day > zalet_day - day_span and row_day < zalet_day + day_span):
                continue

            row_dude_name = str(row.get("DudeName", ""))
            row_dude_name_type = str(row.get("DudeNameType", ""))
            row_is_dude_random = _zalet_to_int(row.get("IsDudeRandom", 0), 0)
            row_zalet = _zalet_to_int(row.get("Zalet", 0), 0)

            suspect_grade = 1
            if row_is_dude_random == 0:
                suspect_grade += 2
            if row_dude_name_type == "NPC":
                suspect_grade += 3
            if _zalet_text(row_dude_name) == "вы":
                suspect_grade += 2
            if girl_name == "amanda" and _zalet_text(row_dude_name) == "вы":
                suspect_grade += 2
            if girl_name == "becky" and _zalet_text(row_dude_name) == "эдди":
                suspect_grade += 5

            suspect_rows.append({
                "GirlName": str(row.get("GirlName", "")),
                "DudeName": row_dude_name,
                "DudeNameType": row_dude_name_type,
                "Zalet": row_zalet,
                "SuspectGrade": suspect_grade,
                "MatchField": (row_dude_name + row_dude_name_type).lower(),
            })

        suspect_rows.sort(key=lambda row: row.get("MatchField", ""))

        final_rows = []
        tmp_prev = None
        tmp_times_count = 0
        tmp_zalet = 0

        for row in suspect_rows:
            if tmp_prev is None or tmp_prev.get("MatchField", "") == row.get("MatchField", ""):
                tmp_times_count += 1
                if _zalet_truthy(row.get("Zalet", 0)):
                    tmp_zalet = 1
            else:
                final_rows.append({
                    "GirlName": tmp_prev.get("GirlName", ""),
                    "DudeName": tmp_prev.get("DudeName", ""),
                    "DudeNameType": tmp_prev.get("DudeNameType", ""),
                    "Zalet": tmp_zalet,
                    "SuspectGrade": _zalet_to_int(tmp_prev.get("SuspectGrade", 0), 0),
                    "MatchField": tmp_prev.get("MatchField", ""),
                    "Times": tmp_times_count,
                    "Rank": tmp_times_count * _zalet_to_int(tmp_prev.get("SuspectGrade", 0), 0),
                })
                tmp_times_count = 1
                tmp_zalet = 0
                if _zalet_truthy(row.get("Zalet", 0)):
                    tmp_zalet = 1

            tmp_prev = dict(row)

        if tmp_prev is not None:
            final_rows.append({
                "GirlName": tmp_prev.get("GirlName", ""),
                "DudeName": tmp_prev.get("DudeName", ""),
                "DudeNameType": tmp_prev.get("DudeNameType", ""),
                "Zalet": tmp_zalet,
                "SuspectGrade": _zalet_to_int(tmp_prev.get("SuspectGrade", 0), 0),
                "MatchField": tmp_prev.get("MatchField", ""),
                "Times": tmp_times_count,
                "Rank": tmp_times_count * _zalet_to_int(tmp_prev.get("SuspectGrade", 0), 0),
            })

        final_rows.sort(key=lambda row: _zalet_to_int(row.get("Rank", 0), 0), reverse=True)
        ZaletSuspectFinal[girl_name] = final_rows
        PregTotalSuspects[girl_name] = len(final_rows)
        return 0

    def DaddyAskBuildName(girl_name, dude_name, dude_name_type, times=0):
        dude_name_l = _zalet_text(dude_name)
        dude_type_l = _zalet_text(dude_name_type)

        if dude_type_l.startswith("неизвестный"):
            rand_var = renpy.random.randint(1, 4)
            unknown_type = dude_type_l.replace("неизвестный", "", 1).strip()
            if rand_var == 1:
                return "какой-то " + unknown_type + " как же его звали, а, вспомнила, " + str(dude_name)
            if rand_var == 2:
                return str(dude_name) + ", такой милый " + unknown_type + ". Даже не знаю, где он сейчас, помнит ли меня..."
            if rand_var == 3:
                return str(dude_name) + ", " + unknown_type + ", я с ним и виделась-то немного. Так, перепихнулись и разбежались"
            return "блин, на языке вертится, как же его звали, а, " + unknown_type + ", " + unknown_type + " " + str(dude_name) + "!"

        if "парень" in dude_type_l:
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "как-же этого парня звали, ну ту его видел, он недалеко от нас живет, а, вот: " + str(dude_name)
            if rand_var == 2:
                return str(dude_name) + ", такой милый мальчик. Интересно, помнит ли он меня..."
            return str(dude_name) + ", парень из соседнего квартала, да ты его знаешь. Дала я ему, уболтал он меня, гоблин языкастый!"

        if str(girl_name) == "amanda" and dude_name_l == "вы":
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "ты, Стефан, кто же еще? Завернул мне подол и обрюхатил меня. Думай теперь, как это объяснять"
            if rand_var == 2:
                return "не кто иной, как ты. Наспускал мне полную киску своего семени, вот у меня пузо и растет теперь"
            return "ты. Вот блин, от хозяина трактира понесла, стыд-то какой!"

        if str(girl_name) == "becky" and dude_name_l == "вы":
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "ты мальчик мой милый. Соблазнил меня, бедную вдову, а теперь еще и в положение ввел"
            if rand_var == 2:
                return "ты Стефанчик. Затяжеляла я, старая от тебя. Но ты не переживай, от такого и родить приятно"
            return "ты, Стефан, кто же еще!"

        if str(girl_name) == "liza" and dude_name_l == "вы":
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "ты Стефанчик. Помнишь, как доставал мне почти до маточки и туда спускал? Вот тогда, думаю, я и залетела"
            if rand_var == 2:
                return "ты наверное. Хорошо ты меня оттрахал тогда, помнишь? Сперма из меня ручьем текла. А ведь это аккурат между месячными было. Вот думаю тогда-то и заделал ты мне младенчика"
            return "ты наверное. Ты же любишь в меня спускать, вот и в тот месяц так было."

        if str(girl_name) == "georgett" and dude_name_l == "вы":
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "ты Стефанчик я думаю. Хотя конечно это не столь важно, все равно я точно отцов своих детей не знаю"
            if rand_var == 2:
                return "ты наверное. Мы тогда хорошо с тобой потрахались, ты в меня много накончал а потом у меня месячные и не пришли"
            return "ты наверное. Любишь спускать мне внутрь, вот я и думаю что ты"

        if str(girl_name) == "becky" and dude_name_l == "эдди":
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "Эдди, мой управляющий. Тяжело ведь мне одной без мужика, вот и баловалась с ним. А теперь он мне и заделал ребеночка"
            if rand_var == 2:
                return "Эдди. Сиротой его подобрала, помощником в лавку взяла, а теперь вот рожу от своего управляющего. Надеюсь не врал отец Герхарт, нет в этом большого греха"
            return "Эдди, мой рыжий помощник. Добаловались, докувыркались мы с ним"

        if str(girl_name) == "amanda" and "легаре" in dude_name_l:
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "Альберчик мой хороший. Он любит в меня кончать, вот и в тот день он прямо в меня спустил"
            if rand_var == 2:
                return "Альберчик, ух как с ним мы накувыркались"
            return "Альберчик, после танцев он тогда прямо в меня кончил, а потом и задержка была"

        if "легаре" in dude_name_l:
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "Мессир Легаре, ну ты знаешь, виноторговец"
            if rand_var == 2:
                return "виноторговец Альбер Легаре, степенный такой, обстоятельный, ну ты знаешь его"
            return "Мессир Легаре, такой степенный мужчина, у него еще лавка с вином на рынке есть"

        if "герхард" in dude_name_l:
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "Отец Герхард, настоятель святого храма Ильматера"
            if rand_var == 2:
                return "Падре Герхард осенил меня благодатью Ильматера, надеюсь и роды он благославит"
            return "Отец Герхард приобщил меня к благодати Ильматера. Ну и под подол мне залез.."

        if str(girl_name) == "inga" and "лукас" in dude_name_l:
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "мой парень, Лукас, от него я затяжелела"
            if rand_var == 2:
                return "женишок мой, Лукас меня обрюхатил"
            return "с Лукасом, моим женишком мы баловались, баловались и вот, он мне ребенка заделал"

        if "эдди" in dude_name_l:
            rand_var = renpy.random.randint(1, 3)
            if rand_var == 1:
                return "Эдди, управляющий лавкой вдовы Блэнкеншип, ну той у которой ты продукты покупаешь"
            if rand_var == 2:
                return "Эдди, ну знаешь ты его, он у Бекки в лавке работает"
            return "Эдди, ну видел ты его. Вот может он мне ребенка и заделал"

        return str(dude_name)

    def DaddyAskBuildTimePhrase(times_num):
        times_num = _zalet_to_int(times_num, 0)
        if times_num == 0:
            return ""
        if times_num == 1:
            return "Один только раз в меня кончил, но и этого хватило."
        if times_num <= 4:
            return str(times_num) + " раза в меня кончил, вот и залетела я."
        if times_num <= 10:
            return str(times_num + renpy.random.randint(-1, 3)) + " раз в меня кончил наверное, чтобы уж наверняка."
        if times_num <= 25:
            return "Раз двадцать наверное в меня спустил, чтобы значит наверняка меня обрюхатить."
        return "Даже и не упомнишь сколько раз в меня кончил. Спермы бы хватило чтобы наверное пол Коитополиса обрюхатить."

    def DaddyAskBuildPhrase(girl_name):
        girl_name = str(girl_name)
        if ZaletSuspectLinesCount(girl_name) == 0:
            ZaletGetSuspectList(girl_name)

        suspects = ZaletSuspectFinal.get(girl_name, [])
        total = _zalet_to_int(PregTotalSuspects.get(girl_name, 0), 0)
        real_name = RealName.get(girl_name, girl_name)
        tmp_daddy_name = []
        tmp_daddy_times = []

        for suspect in suspects:
            tmp_daddy_name.append(DaddyAskBuildName(girl_name, suspect.get("DudeName", ""), suspect.get("DudeNameType", ""), suspect.get("Times", 0)))
            tmp_daddy_times.append(_zalet_to_int(suspect.get("Times", 0), 0))

        if total == 0:
            return ""
        if total == 1 and len(tmp_daddy_name) >= 1:
            return "\"А чего мне гадать?\" отвечает вам " + str(real_name) + ". \"Я точно знаю кто отец моего ребеночка. Около того дня только он и кончал в меня. Это " + str(tmp_daddy_name[0]) + ". " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[0]))
        if total == 2 and len(tmp_daddy_name) >= 2:
            return "\"Ну, я на двоих думаю, больше вроде я никому в опасные дни не давала в меня кончать,\" отвечает вам " + str(real_name) + ". \"Во первых это " + str(tmp_daddy_name[0]) + ". " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[0])) + ".\nА если не он, то " + str(tmp_daddy_name[1]) + ". Тоже исключать нельзя. " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[1])) + " Вот теперь и думаю, кто из двоих."
        if total == 3 and len(tmp_daddy_name) >= 3:
            return "\"Ну, я думаю один из трех мужиков мог меня обрюхатить. Больше кроме них вроде некому,\" отвечает вам гулящая " + str(real_name) + ". \"Во первых это " + str(tmp_daddy_name[0]) + ". " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[0])) + ".\nВторой это " + str(tmp_daddy_name[1]) + ". Тоже исключать нельзя. " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[1])) + ". Ну а если не эти, то тогда это " + str(tmp_daddy_name[2]) + ". Я, конечно, на первых двоих больше думаю, но и последнего варианта не отбрасываю. " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[2])) + " "
        if len(tmp_daddy_name) >= 3:
            return "\"Ну, ты и вопросы задаешь,\" засмеялась " + str(real_name) + ". \"Я, сам понимаешь, тоже над этим думала. И получилось что не так уж и мало мужиков меня тогда трахали. Я насчитала " + str(total) + " кандидатов.\"\n\"Ну ты даешь!\" отозвались вы.\n\"Конечно даю, разве по пузу не видно. Дала то я может и большему количеству народа, но вот эти " + str(total) + " точно в меня в опасные дни кончали. Я, правда, склоняюсь к тому, что это один из трех, хотя конечно и остальные могли постараться. Во первых это " + str(tmp_daddy_name[0]) + ". " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[0])) + ".\nВторой это " + str(tmp_daddy_name[1]) + ". Тоже исключать нельзя. " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[1])) + ". Ну а если не эти, то тогда это " + str(tmp_daddy_name[2]) + ". Я, конечно, на первых двоих больше думаю, но и последнего варианта не отбрасываю. " + str(DaddyAskBuildTimePhrase(tmp_daddy_times[2])) + ".\"\n\"Ну и остальные " + str(total - 3) + " тоже могли,\" делитесь вы своим умозаключением.\n\"А то как же? Могли, спорить не буду. В общем родится, посмотрю на кого похож.\" "
        return ""

label ZaletOpinionCalc:
    return
