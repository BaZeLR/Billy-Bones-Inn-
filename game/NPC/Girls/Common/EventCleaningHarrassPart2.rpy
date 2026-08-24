    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]    $ _next_title = "Ваши действия"
    $ _next_items = [MenuItem("Вернуться к делам", Jump("TavernMain"))]# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label event_cleaning_harrass_part2(girl_name, eyewitness=0, your_reaction1=0, harass_type=1):
    $ Eyewitness = eyewitness
    $ YourReaction1 = your_reaction1
    $ HarassType = harass_type

    call PartEventGirlHarrassmentReaction(girl_name, "cleaning", eyewitness)
    $ CurEventDescPart2 = _return

    if GirlSlapped > 0 and your_reaction1 != 3:
        if harass_type == 1:
            call HarassShowImage(girl_name, "tits", 1, eyewitness, "cleaning")
        elif harass_type == 2:
            call HarassShowImage(girl_name, "ass", 1, eyewitness, "cleaning")
        elif harass_type == 3:
            call HarassShowImage(girl_name, "dress", 1, eyewitness, "cleaning")
        else:
            call HarassShowImage(girl_name, "ass", 1, eyewitness, "cleaning")
    elif GirlRunAway > 0 and your_reaction1 != 3:
        if harass_type == 1:
            call HarassShowImage(girl_name, "tits", 2, eyewitness, "cleaning")
        elif harass_type == 2:
            call HarassShowImage(girl_name, "ass", 2, eyewitness, "cleaning")
        elif harass_type == 3:
            call HarassShowImage(girl_name, "dress", 2, eyewitness, "cleaning")
        else:
            call HarassShowImage(girl_name, "ass", 2, eyewitness, "cleaning")

    if GirlRunAway == 0:
        $ CurEventDescPart2 += "\n"
        $ _girl_info = getPersonInfo(girl_name)
        $ girl_slut = int(getattr(_girl_info, "corruption", 0) or 0)

        if girl_slut < 50:
            if harass_type == 1:
                $ CurEventDescPart2 += "{} спокойно продолжила вытирать стол, пока молоденький подмастерье тискал ее сисечки. Закончив прибирать, она выпрямилась и направилась к следующему столу, как ни в чем ни бывало.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "tits", 4, eyewitness, "cleaning")
            elif harass_type == 2:
                $ CurEventDescPart2 += "{} взвизгнула, но взяла себя в руки и продолжила убирать. Грузчик еще немного подурачился, имитируя половой акт, звонко шлепнул ее по попке и вернулся к своей компании.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "ass", 4, eyewitness, "cleaning")
            elif harass_type == 3:
                $ CurEventDescPart2 += "{} продолжила протирать полку, игнорируя что чьи-то руки шарят у нее под юбкой. Закончив с полкой, {} начала спускаться со стремянки. Моряк галантно подал ей руку, задрав при этом подол ее платья, {} чмокнула его в щечку и побежала дальше по своим делам.".format(RealName.get(girl_name, girl_name), RealName.get(girl_name, girl_name), RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "dress", 4, eyewitness, "cleaning")
            else:
                $ CurEventDescPart2 += "{} вернула стражнику его поцелуй, но без всякой страсти. Стражник потискал ее немного, ущипнул за задницу и позволил вернуться к работе.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "ass", 4, eyewitness, "cleaning")
        else:
            if harass_type == 1:
                $ CurEventDescPart2 += "{} растегнула пуговицу и направила похотливые ручонки молодого подмастерья себе под лиф, а затем продолжила вытирать стол, как ни в чем ни бывало. Ошалевший от такого оборота событий юноша радостно мял ее сиськи у нее под одеждой пока она не закончила со столом. А закончив, {} выпрямилась, поцеловала молодого человека и направилась к следующему столу, даже и не подумав застегнуть пуговицу обратно.".format(RealName.get(girl_name, girl_name), RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "tits", 5, eyewitness, "cleaning")
            elif harass_type == 2:
                $ CurEventDescPart2 += "{} с этунзиазмом восприняла предложенную ей игру, начав делать подмахивающие движения в такт грузчику и тереться попой о его ширинку, которая вскоре стала заметно оттопыриваться. Потом {} встала, еще немного потерлась о ширинку работяги и, послав ему воздушный поцелуй, направилась дальше. А на штанах у шутника расплылось мокрое пятно.".format(RealName.get(girl_name, girl_name), RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "ass", 5, eyewitness, "cleaning")
            elif harass_type == 3:
                $ CurEventDescPart2 += "{} продолжила протирать полку, расставив ноги пошире на стремянке дабы облегчить моряку доступ. Закончив с полкой, {} начала спускаться со стремянки, но на полдороге деланно оступилась и упала прямо на морского волка, а затем на пол, широко раставив ноги. Ее подол при этом задрался едва ли не до пояса, так что моряк судя по всему получил прекрасный вид на ".format(RealName.get(girl_name, girl_name), RealName.get(girl_name, girl_name))
                if panties.get(girl_name, ""):
                    $ CurEventDescPart2 += "панталончики "
                else:
                    $ CurEventDescPart2 += "обнаженную киску "
                $ CurEventDescPart2 += "{}. С трудом отведя взгляд от такого зрелища, моряк все-таки подал ей руку. {} встала, чмокнула его и побежала дальше по своим делам.".format(RealName2.get(girl_name, girl_name), RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "dress", 5, eyewitness, "cleaning")
            else:
                $ CurEventDescPart2 += "{} вернула стражнику его поцелуй, страстно переплетясь с ним языками. Затем егоза схватила стража порядка за член сквозь его форменные штаны. Сбитый с толку такой прытью страж отпустил вашу очаровательную уборщицу, а та, воспользовавшись этим, поцеловала его еще раз и вернулась к работе.".format(RealName.get(girl_name, girl_name))
                call HarassShowImage(girl_name, "ass", 5, eyewitness, "cleaning")

    call PartEventCustomerHarrassmentReaction(girl_name)
    $ CurEventDescPart2 += _return

    if eyewitness > 0:
        call PartEventAfterHarrassment(girl_name, GirlSlapped, your_reaction1)
        if isinstance(_return, dict):
            $ CurEventDescPart2 += _coerce_panel_text_value(_return.get("text", ""))
            $ _next_title = str(_return.get("title", _next_title) or _next_title)
            $ _next_items = list(_return.get("items", _next_items) or _next_items)
        else:
            $ CurEventDescPart2 += _coerce_panel_text_value(_return)

    if eyewitness > 0:
        $ Result = {"text": CurEventDescPart2, "title": _next_title, "items": _next_items}
    else:
        $ Result = CurEventDescPart2
    return Result
