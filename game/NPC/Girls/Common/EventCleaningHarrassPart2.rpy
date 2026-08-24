# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label event_cleaning_harrass_part2(girl_name, eyewitness=0, your_reaction1=0, harass_type=1, cur_event_desc_part2="", girl_run_away=0, girl_slapped=0, _girl_info=None, girl_slut=0):
    call PartEventGirlHarrassmentReaction(girl_name, "cleaning", eyewitness, your_reaction1)
    $ cur_event_desc_part2, girl_run_away, girl_slapped = _return

    if girl_slapped > 0 and your_reaction1 != 3:
        if harass_type == 1:
            call HarassShowImage(girl_name, "tits", 1, eyewitness, "cleaning")
        elif harass_type == 2:
            call HarassShowImage(girl_name, "ass", 1, eyewitness, "cleaning")
        elif harass_type == 3:
            call HarassShowImage(girl_name, "dress", 1, eyewitness, "cleaning")
        else:
            call HarassShowImage(girl_name, "ass", 1, eyewitness, "cleaning")
    elif girl_run_away > 0 and your_reaction1 != 3:
        if harass_type == 1:
            call HarassShowImage(girl_name, "tits", 2, eyewitness, "cleaning")
        elif harass_type == 2:
            call HarassShowImage(girl_name, "ass", 2, eyewitness, "cleaning")
        elif harass_type == 3:
            call HarassShowImage(girl_name, "dress", 2, eyewitness, "cleaning")
        else:
            call HarassShowImage(girl_name, "ass", 2, eyewitness, "cleaning")

    if girl_run_away == 0:
        $ cur_event_desc_part2 += "\n"
        $ _girl_info = people.get_info(girl_name)
        $ girl_slut = int(getattr(_girl_info, "corruption", 0) or 0)

        if girl_slut < 50:
            if harass_type == 1:
                $ cur_event_desc_part2 += "{} спокойно продолжила вытирать стол, пока молоденький подмастерье тискал ее сисечки. Закончив прибирать, она выпрямилась и направилась к следующему столу, как ни в чем ни бывало.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "tits", 4, eyewitness, "cleaning")
            elif harass_type == 2:
                $ cur_event_desc_part2 += "{} взвизгнула, но взяла себя в руки и продолжила убирать. Грузчик еще немного подурачился, имитируя половой акт, звонко шлепнул ее по попке и вернулся к своей компании.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "ass", 4, eyewitness, "cleaning")
            elif harass_type == 3:
                $ cur_event_desc_part2 += "{} продолжила протирать полку, игнорируя что чьи-то руки шарят у нее под юбкой. Закончив с полкой, {} начала спускаться со стремянки. Моряк галантно подал ей руку, задрав при этом подол ее платья, {} чмокнула его в щечку и побежала дальше по своим делам.".format(people_display_name(girl_name), people_display_name(girl_name), people_display_name(girl_name))
                call HarassShowImage(girl_name, "dress", 4, eyewitness, "cleaning")
            else:
                $ cur_event_desc_part2 += "{} вернула стражнику его поцелуй, но без всякой страсти. Стражник потискал ее немного, ущипнул за задницу и позволил вернуться к работе.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "ass", 4, eyewitness, "cleaning")
        else:
            if harass_type == 1:
                $ cur_event_desc_part2 += "{} растегнула пуговицу и направила похотливые ручонки молодого подмастерья себе под лиф, а затем продолжила вытирать стол, как ни в чем ни бывало. Ошалевший от такого оборота событий юноша радостно мял ее сиськи у нее под одеждой пока она не закончила со столом. А закончив, {} выпрямилась, поцеловала молодого человека и направилась к следующему столу, даже и не подумав застегнуть пуговицу обратно.".format(people_display_name(girl_name), people_display_name(girl_name))
                call HarassShowImage(girl_name, "tits", 5, eyewitness, "cleaning")
            elif harass_type == 2:
                $ cur_event_desc_part2 += "{} с этунзиазмом восприняла предложенную ей игру, начав делать подмахивающие движения в такт грузчику и тереться попой о его ширинку, которая вскоре стала заметно оттопыриваться. Потом {} встала, еще немного потерлась о ширинку работяги и, послав ему воздушный поцелуй, направилась дальше. А на штанах у шутника расплылось мокрое пятно.".format(people_display_name(girl_name), people_display_name(girl_name))
                call HarassShowImage(girl_name, "ass", 5, eyewitness, "cleaning")
            elif harass_type == 3:
                $ cur_event_desc_part2 += "{} продолжила протирать полку, расставив ноги пошире на стремянке дабы облегчить моряку доступ. Закончив с полкой, {} начала спускаться со стремянки, но на полдороге деланно оступилась и упала прямо на морского волка, а затем на пол, широко раставив ноги. Ее подол при этом задрался едва ли не до пояса, так что моряк судя по всему получил прекрасный вид на ".format(people_display_name(girl_name), people_display_name(girl_name))
                if people.get_info(girl_name).clothing_layer("panties"):
                    $ cur_event_desc_part2 += "панталончики "
                else:
                    $ cur_event_desc_part2 += "обнаженную киску "
                $ cur_event_desc_part2 += "{}. С трудом отведя взгляд от такого зрелища, моряк все-таки подал ей руку. {} встала, чмокнула его и побежала дальше по своим делам.".format(people_name(girl_name, 'genitive'), people_display_name(girl_name))
                call HarassShowImage(girl_name, "dress", 5, eyewitness, "cleaning")
            else:
                $ cur_event_desc_part2 += "{} вернула стражнику его поцелуй, страстно переплетясь с ним языками. Затем егоза схватила стража порядка за член сквозь его форменные штаны. Сбитый с толку такой прытью страж отпустил вашу очаровательную уборщицу, а та, воспользовавшись этим, поцеловала его еще раз и вернулась к работе.".format(people_display_name(girl_name))
                call HarassShowImage(girl_name, "ass", 5, eyewitness, "cleaning")

    call PartEventCustomerHarrassmentReaction(girl_name, girl_run_away, girl_slapped)
    $ cur_event_desc_part2 += _return

    if eyewitness > 0:
        $ scene_runtime.text = format_tavern_event_text(cur_event_desc_part2)
        $ scene_runtime.location_text = scene_runtime.text
        "[scene_runtime.text]"
        call PartEventAfterHarrassment(girl_name, girl_slapped, your_reaction1)
        return

    return cur_event_desc_part2
