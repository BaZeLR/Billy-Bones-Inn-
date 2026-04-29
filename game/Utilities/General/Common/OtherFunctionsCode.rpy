# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def FOR_i(start_i, max_i, inc_i, expr_code):
        try:
            i = int(start_i)
        except Exception:
            i = 0

        try:
            max_i = int(max_i)
        except Exception:
            max_i = i

        try:
            inc_i = int(inc_i)
        except Exception:
            inc_i = 1

        if inc_i == 0:
            return 0

        local_ctx = {"i": i}

        while (inc_i > 0 and i <= max_i) or (inc_i < 0 and i >= max_i):
            local_ctx["i"] = i

            if callable(expr_code):
                try:
                    expr_code()
                except TypeError:
                    try:
                        expr_code(i)
                    except TypeError:
                        expr_code(i=i)
            elif isinstance(expr_code, str) and expr_code.strip() != "":
                try:
                    exec(expr_code, renpy.store.__dict__, local_ctx)
                except Exception:
                    pass

            i = local_ctx.get("i", i)
            i += inc_i

        return 0

    def FOR_xy(y_start, y_max, y_inc, x_start, x_max, x_inc, expr_code):
        try:
            y = int(y_start)
        except Exception:
            y = 0

        try:
            y_max = int(y_max)
        except Exception:
            y_max = y

        try:
            y_inc = int(y_inc)
        except Exception:
            y_inc = 1

        try:
            x_start = int(x_start)
        except Exception:
            x_start = 0

        try:
            x_max = int(x_max)
        except Exception:
            x_max = x_start

        try:
            x_inc = int(x_inc)
        except Exception:
            x_inc = 1

        if y_inc == 0 or x_inc == 0:
            return 0

        local_ctx = {"x": x_start, "y": y}

        while (y_inc > 0 and y <= y_max) or (y_inc < 0 and y >= y_max):
            local_ctx["y"] = y
            x = x_start

            while (x_inc > 0 and x <= x_max) or (x_inc < 0 and x >= x_max):
                local_ctx["x"] = x

                if callable(expr_code):
                    try:
                        expr_code()
                    except TypeError:
                        try:
                            expr_code(x, y)
                        except TypeError:
                            expr_code(x=x, y=y)
                elif isinstance(expr_code, str) and expr_code.strip() != "":
                    try:
                        exec(expr_code, renpy.store.__dict__, local_ctx)
                    except Exception:
                        pass

                x = local_ctx.get("x", x)
                x += x_inc

            y = local_ctx.get("y", y)
            y += y_inc

        return 0

label OtherFunctionsCode:
    return

label ArrestCode:
    $ BribeSize = 50
    if MyCurDress == "thiefdress":
        "\"Ага, так мы тебе и поверили, ворюга! А ну пошли!\" похоже ваша манера одеваться не прибавила вам убедительности."
        $ BribeSize = 500
    elif MyCurDress == "nobbledress":
        "\"А может это благородный?\" шепотом спросил один стражник другого. \"Не похоже, говорит не так. Но может лучше не рисковать.\""
        $ BribeSize = 10
    elif MyCurDress == "citydress":
        "\"Что буржуйчик, деньги кончились и решил у соседей натырить? Ну да мы тебя закатаем, чтоб неповадно было.\""
        $ BribeSize = 100
    elif MyCurDress == "sailordress":
        "\"Ага, морячок, с корабля и сразу на бал! Думаешь натыришь чего, ну а завтра в море и мы тебя не найдем! Так по твоему?\""
        $ BribeSize = 80
    else:
        "\"Чего ты лопочешь, мужичина? Такие как ты только и смотрят, как чего стянуть.\""

    "Вы сменили тактику, заявив, что у них на вас ничего нет и нечего вам дело шить. На что получили ответ что может и нет, но денек вам посидеть отдохнуть не помешает, а там судья разберется. Ну, если вы не договоритесь и не заплатите штраф прямо на месте."

    if money >= BribeSize:
        menu:
            "Дать [BribeSize] мараведи":
                $ money -= BribeSize
                "Вы вынули руку из кармана вместе с искомой суммой, и пожали стражнику его протянутую руку. \"Большое вам спасибо, сэр,\" вежливо сказали вы, слегка поклонившись. \"Ну вот все и объяснилось, конечно же вы законопослушный горожанин, как я и думал!\" ответил вам слуга закона и пошел своей дорогой."
                call stat
                menu:
                    "Вернуться к трактиру в расстроенных чувствах":
                        jump StreetTavern
    else:
        "Однако есть небольшая закавыка, нужной суммы у вас похоже нет."

    menu:
        "Я невиновен!":
            "Вы продолжили настаивать на своей невиновности. Слушали они вас внимательно, но недолго. Уже через минуту вам закрутили руки и отвели в кутузку. Хоть и просидели вы там всего одну ночь, судья, как и обещали, во всем разобрался, но слухи об этом успели распространиться, к тому же многие видели, как вас вели под конвоем. На репутации вашего заведения это маленькое приключение отразилось не лучшим образом."
            $ tavernfame -= 3
            menu:
                "Понуро вернуться в трактир на утро из каталажки":
                    call NextDay("TavernMain", 1)
    return

label ButtonToCurloc:
    menu:
        "Пойду-ка и я":
            if CurLoc != "":
                jump expression CurLoc
    return
