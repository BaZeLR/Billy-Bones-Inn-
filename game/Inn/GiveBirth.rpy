label GiveBirth(GirlName=""):
    if GirlName == "":
        return

    python:
        import re
        import random

        def _strcomp(value, pattern):
            try:
                return 1 if re.search(pattern, str(value), flags=re.IGNORECASE) else 0
            except Exception:
                return 0

        def _sfi(girl_name, lf, fc, idf, ls, sc, ids):
            try:
                slut_friends_increase(girl_name, lf, fc, idf, ls, sc, ids)
                return
            except NameError:
                pass
            except Exception:
                pass
            if renpy.has_label("SlutFriendsIncrease"):
                try:
                    renpy.call("SlutFriendsIncrease", girl_name, lf, fc, idf, ls, sc, ids)
                except Exception:
                    pass

        def _random_name(gender):
            try:
                return RandomNameCode(gender)
            except NameError:
                pass
            except Exception:
                pass
            if gender == "male":
                names = ["Питер", "Жан", "Карло", "Андреас"]
            else:
                names = ["Анна", "Мария", "Кармела", "Лорен"]
            return random.choice(names)

        def _get_sex_num(*args):
            try:
                return GetSexNum(*args)
            except Exception:
                return 0

        def _mama_molodost_heard():
            if SandraVar.get("knowmolodost", 0) == 0:
                renpy.say(None, "Мама, услышав такое замечание, немного покраснела. Интересно, от чего? И что эти слова значат?")
                SandraVar["knowmolodost"] = 1
            else:
                renpy.say(None, "Вы понимающе усмехнулись, услышав эти слова.")

    if ZaletSuspectLinesCount(GirlName) == 0:
        $ ZaletGetSuspectList(GirlName)
    $ DaddySuspect1 = str(ZaletSuspectGetValue(GirlName, 1, "DudeName", "") or "").lower()
    $ DaddySuspect2 = str(ZaletSuspectGetValue(GirlName, 2, "DudeName", "") or "").lower()

    $ real_name = RealName.get(GirlName, GirlName)
    $ real_name2 = RealName2.get(GirlName, real_name)
    $ real_name3 = RealName3.get(GirlName, real_name)

    "Вы спокойно себе шли по своим делам, как вдруг услышали крик о помощи."
    if GirlName == "sandra":
        "Мелисса и Аманда звали вас к маме: у нее начались схватки."
    elif GirlName in ("melissa", "amanda"):
        "Матушка позвала вас: у [real_name2] отошли воды."
    elif GirlName == "becky":
        "Эдди в панике позвал вас к Ребекке: начались роды."
    elif GirlName == "liza":
        "Жоржетта попросила помочь Лизетте добраться до храма."
    elif GirlName == "georgett":
        "Лизетта попросила вас помочь Жоржетте во время родов."
    elif GirlName == "inga":
        "Бекки попросила вас помочь Инге: начались схватки."

    $ _give_birth_calmed = 0

    label give_birth_menu:
        menu:
            "Успокоить" if _give_birth_calmed == 0:
                "\"Не волнуйся, все будет хорошо,\" сказали вы [real_name3]."

                if GirlName == "georgett":
                    "Жоржетта уверенно ответила, что уже не раз рожала и знает, что делать."
                    if sluttiness.get("liza", 0) < 55:
                        "Лизетта от маминых подробностей смутилась."
                    else:
                        "\"Мамочка, ты у меня такая блядь!\" — воскликнула Лизетта."
                    python:
                        _sfi(GirlName, 0, 0, 0, 60, 1, 1)

                elif GirlName == "liza":
                    if kids.get(GirlName, 0) == 0:
                        "Лизетта нервничала перед первыми родами, а Жоржетта подбадривала ее в привычной манере."
                    else:
                        "Лизетта пожаловалась, что рожать ей все равно страшно, даже не в первый раз."

                elif GirlName == "becky":
                    "Бекки сказала, что уже рожала и справится, хотя в этот раз переживает больше обычного."
                    if DaddySuspect1 == "эдди":
                        "Она призналась, что боится пересудов, если отцом окажется Эдди."
                    elif DaddySuspect1 == "вы":
                        "Она намекнула, что считает вас самым вероятным отцом."
                    elif _strcomp(DaddySuspect1, "герхард"):
                        "Она сказала, что подозревает отца Герхарда."

                elif GirlName in ("amanda", "melissa"):
                    if kids.get(GirlName, 0) == 0:
                        "[real_name] возмущенно заметила, что ей страшно рожать без мужа и жениха."
                    else:
                        $ friend_name = _random_name("female")
                        "[real_name] сказала, что в их возрасте такое в городе уже никого не удивляет, и упомянула подружку [friend_name]."

                    if PregTotalSuspects.get(GirlName, 0) > 2:
                        if sluttiness.get("sandra", 0) < 45:
                            "Мама отчитала [real_name2] за слишком длинный список кандидатов в отцы."
                            if sluttiness.get(GirlName, 0) > 60:
                                python:
                                    _sfi(GirlName, 0, 0, 0, 63, 1, 1)
                            else:
                                python:
                                    _sfi(GirlName, 0, 0, 0, 35, 1, -1)
                        else:
                            "Мама сказала, что поддержит [real_name3], и что семья поможет с ребенком."
                            if sluttiness.get(GirlName, 0) > 60:
                                python:
                                    _sfi(GirlName, 0, 0, 0, 65, 1, 1)
                            else:
                                python:
                                    _sfi(GirlName, 0, 0, 0, 35, 1, -1)
                        python:
                            _mama_molodost_heard()

                    if DaddySuspect1 == "вы" or DaddySuspect2 == "вы":
                        "Мама прямо сказала, что вы, вероятно, отец будущего ребенка."
                        if sluttiness.get("sandra", 0) < 55:
                            if sluttiness.get(GirlName, 0) > 65:
                                python:
                                    _sfi(GirlName, 20, 1, 1, 68, 1, 1)
                            else:
                                python:
                                    _sfi(GirlName, 0, 0, 0, 35, 1, -1)
                    elif _strcomp(DaddySuspect1, "легаре"):
                        "Разговор перешел на месье Легаре как на одного из главных подозреваемых."
                        if sluttiness.get(GirlName, 0) > 65:
                            python:
                                _sfi(GirlName, 0, 0, 0, 65, 1, 1)
                        else:
                            if sluttiness.get("sandra", 0) < 50:
                                python:
                                    _sfi(GirlName, 0, 0, 0, 35, 1, -1)
                            else:
                                python:
                                    _sfi(GirlName, 0, 0, 0, 55, 1, 1)

                elif GirlName == "sandra":
                    "\"Спасибо, сыночек, что помогаешь,\" — улыбнулась мама."
                    if DaddySuspect1 == "вы" or DaddySuspect2 == "вы":
                        "Сандра смущенно добавила, что вы можете быть отцом."
                        if min(sluttiness.get("amanda", 0), sluttiness.get("melissa", 0)) < 55:
                            if sluttiness.get(GirlName, 0) <= 62:
                                python:
                                    _sfi(GirlName, 7, 1, -1, 25, 1, -1)
                        else:
                            python:
                                _sfi(GirlName, 20, 1, 1, 65, 1, 1)

                elif GirlName == "inga":
                    "\"Спасибо, что помогаешь,\" — сказала Инга."
                    if sluttiness.get("becky", 0) > 30:
                        python:
                            _sfi(GirlName, 14, 1, 1, 35, 1, 1)
                    "Бекки попросила поторопиться в храм."

                $ _give_birth_calmed = 1
                jump give_birth_menu

            "Идти в храм":
                jump give_birth_to_temple

    label give_birth_to_temple:
        "Подставив [real_name3] плечо, вы поспешили в храм Эллоны."
        "На пороге вас встретила Франческа и сразу оценила ситуацию."

        if age_girls.get(GirlName, 99) <= 18:
            "Франческа бодро заявила, что все пройдет хорошо и роды будут легкими."
        elif GirlName in ("sandra", "becky"):
            "Франческа поприветствовала роженицу как старую знакомую."
        elif GirlName == "georgett":
            "Франческа с улыбкой начала гадать, на кого будет похож ребенок Жоржетты."
        elif kids.get(GirlName, 0) == 0:
            "Франческа заметила, что для [real_name2] это первые роды."
        else:
            "Франческа сказала, что снова рада видеть [real_name2] в родильной комнате."

        if sluttiness.get(GirlName, 0) < 48:
            "[real_name] смутилась от такого приема."
            python:
                _sfi(GirlName, 10, 1, -1, 45, 2, 1)
        else:
            "[real_name2] заметно успокоилась."
            python:
                _sfi(GirlName, 15, 1, 1, 50, 2, 1)

        menu:
            "Идти внутрь":
                "Франческа проводила вас в родильную залу и уложила [real_name3] на ложе."

                if sluttiness.get(GirlName, 0) < 44:
                    "[real_name] смущенно отвела взгляд."
                    python:
                        _sfi(GirlName, 0, 0, 0, 35, 1, -1)
                else:
                    "[real_name] ответила на ваш взгляд улыбкой."
                    python:
                        _sfi(GirlName, 15, 2, 1, 50, 3, 1)

                "Франческа осмотрела роженицу и сказала, что ждать осталось недолго."

                if _get_sex_num(GirlName, "", "inside", "", dayspassed - 2):
                    "Жрица заметила следы спермы и с усмешкой прокомментировала, что время зря не теряли."
                    if GirlName in ("georgett", "liza"):
                        "[real_name] ответила, что работа есть работа."
                    elif sluttiness.get(GirlName, 0) > 58:
                        "[real_name] ответила, что беременность не мешает ей получать удовольствие."
                    elif sluttiness.get(GirlName, 0) > 42:
                        "[real_name] сказала, что раз уже беременна, то запрещать бессмысленно."
                    else:
                        "[real_name] только смущенно покраснела."
                    python:
                        _sfi(GirlName, 0, 0, 0, 55, 2, 1)

                menu:
                    "Ждать дальше":
                        "Схватки усиливались, Франческа продолжала помогать [real_name3]."
                        if kids.get(GirlName, 0) == 0:
                            "Франческа мягко объяснила, как правильно дышать при первых родах."
                        else:
                            "Франческа напомнила, что опыт есть, и попросила не паниковать."

                        if PregTotalSuspects.get(GirlName, 0) < 4:
                            "[real_name] уверенно заявила, что знает, от кого ребенок."
                        else:
                            "[real_name] призналась, что кандидатов в отцы слишком много."

                        menu:
                            "Родовые схватки продолжаются":
                                $ GiveBirthTimer = 0
                                if renpy.has_label("GiveBirthStep2"):
                                    call GiveBirthStep2
                                return

    return
