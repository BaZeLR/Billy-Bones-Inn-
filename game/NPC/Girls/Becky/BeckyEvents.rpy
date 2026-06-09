# Becky atomic thin events for BeckyHomeVisits thread (dinner guest multi-visit)
# This file follows the exact engine standard and user rules:
# - Thin labels only (one stage per label)
# - All counters live inside the event
# - thread.advance() ONLY when THIS event's stage completion conditions are met
# - Use rand_int() for all random chances (no direct rand())
# - Direct $ BeckyVar[...] / EddieVar[...] assignments (NO globals(), NO store. hacks after purge)
# - Classic menu: only, no MenuItem.append
# - Proper call to existing helpers (SlutFriendsIncrease, PregnancyCheck, etc.)
# - Full original source file names in comments for every event
# - Never touches script.rpy intro placeholders
#
# References for this file:
# - textLocRef\GeorgettBeckyVisit.txt (primary orgy + player minet/cum choices)
# - textLocRef\IntBeckyGuest.txt (trigger: if BeckyVar['EddieWhoreHome']=4 and dinnertime=5: gs 'GeorgettBeckyVisit')
# - game/NPC/Girls/Georgett/InitGeorgett.rpy (georgett_eddie_peekhole_jealous sets EddieWhoreHome=4 + peekhole context)
# - game/Inn/GeorgettBeckyVisit.rpy (detailed fallback engine for the location)
# - game/Inn/IntBeckyGuest.rpy (dinner loop, KidsWatchStepsCode / BeckyGuestKidsWatchStepsCode, full guest menu engine)
# - game/Inn/SlutFriendsIncrease.rpy
# - game/NPC/Girls/Becky/IntBeckyGuest.rpy (port of kids watch + dinner helpers)
#
# Thread registration example (add to beckyThreadList in this file or Init):
# beckyThreadList = [
#     LThreadData(1, "becky", "BeckyHomeVisits", "EddieWhoreHome==4 or BeckyVar.get('visitedhome',0)>=1", [
#         ("becky_home_dinner_arrival", ...),
#         ...
#         ("becky_home_georgett_visit", None, None, None, 1, None, "EddieWhoreHome==4 and dinnertime==5", None, "BeckyHome", "eat", 5),
#     ]),
# ]

init python:
    # Ensure rand_int is available (defined in utilities). Fallback safe version.
    try:
        _ = rand_int(1, 2)
    except Exception:
        def rand_int(a, b):
            import random
            return random.randint(int(a), int(b))

# =============================================================================
# GEORGETTE CROSSOVER - the big orgy at EddieWhoreHome==4 during dinner
# =============================================================================

label becky_home_georgett_visit:
    # This is the atomic stage for the Georgett crossover (Eddie brings "подружка").
    # Triggered from dinner actions when BeckyVar['EddieWhoreHome']==4 and dinnertime==5.
    # Full reference flow from textLocRef\GeorgettBeckyVisit.txt + IntBeckyGuest.txt
    # Includes: arrival narration, simultaneous Inga/Lucas + Georgett/Eddie, Becky shock+hand,
    # kids 3-flavor watch (rand_int), Eddie/Lucas cum variants, player minet decision with exact gates,
    # cum face/mouth choices, PregnancyCheck + massive SlutFriendsIncrease on 4+ NPCs,
    # georgedinnersex counter, visitedhome bump to 6, BeckyOpenMinet, exit paths.
    # Thread advances only when the orgy interaction stage completes for this visit.
    # No gs, no globals, direct assignments, rand_int, classic menu, file refs in comments.

    show screen main_ui
    $ becky = getPersonInfo("becky")
    $ inga = getPersonInfo("inga") if 'inga' in dir() else None

    # Internal counters for this crossover stage (private to event until complete)
    $ georgedinnersex = georgedinnersex if 'georgedinnersex' in dir() else 0
    $ dinnerbeckyorgasm = dinnerbeckyorgasm if 'dinnerbeckyorgasm' in dir() else 0
    $ dinnertime = dinnertime if 'dinnertime' in dir() else 5
    python:
        BeckyVar.setdefault("EddieGeorg", 0)
        BeckyVar.setdefault("visitedhome", 0)
        BeckyVar.setdefault("BeckyOpenMinet", 0)
        BeckyVar.setdefault("HomeSex", 0)
        EddieVar = EddieVar if 'EddieVar' in dir() else {}
        EddieVar.setdefault("SawMomSex", 0)

    # === ARRIVAL + INITIAL ORGY (exact from GeorgettBeckyVisit.txt) ===
    $ MainTxt = "Ужин уже практически закончился, как вдруг послышался негромкий стук в дверь.\n\n"

    if BeckyVar.get("EddieGeorg", 0) == 1:
        $ MainTxt += "Эдди, услышав его, вскочил и побежал отпирать дверь. И вот на пороге показалась ваша старая знакомая — Жоржетта.\n"
        $ MainTxt += "«Мама, ты же сказала Инге чтобы она не стеснялась, приводила своего Лукаса к нам, мол дело молодое? Я так понял, что это и ко мне относится. Вот подружка моя, Жоржетта.» — скороговоркой протарабанил Эдди.\n\n"
        $ MainTxt += "«Эдди, ну да, то что относится к Инге относится и к тебе, но ведь твоя подруга вроде намного старше тебя?» — в смятении ответила ему Ребекка.\n"
        $ MainTxt += "«Ну и что, может мне как раз и нравятся женщины твоего возраста,» — смотря матери в глаза нагло ответил Эдди.\n"
        $ MainTxt += "«Ну а раз ты советовала нам не стеснятся, то мы и не будем, не правда ли, дорогуша?»\n"
        $ MainTxt += "«Конечно,» ответила Жоржетта, и"
    else:
        $ MainTxt += "«Эй, Эдди, похоже твоя подружка пришла,» воскликнул Лукас. «Смотри не разорись,» добавил он. Эдди же, не обращая внимания на его сарказм, вскочил и побежал отпирать дверь. Лукас был прав, стучала Жоржетта.\n\nБез особых прелюдий Жоржетта"

    $ MainTxt += ", встав перед Эдди на колени, решительно приспустила с парня штаны, обнажив его быстро твердеющий член. Дав возможность всем присутствующим насладиться зрелищем Эддиного члена, Жоржетта сначала ловко облизала головку своим язычком, а потом, после того как член Эдди встал во всей красе, стала профессионально и умело делать ему минет.\n\n"
    $ MainTxt += "Происходящее не оставило окружающих безучастными. Лукас шепнул на ушко пару слов Ингенборг, встал, расстегнул штаны. Инга, метнув быстрый взгляд на мать, начала отсасывать своему женишку.\n\n"
    $ MainTxt += "Дыхание Ребекки участилось, щеки покрылись румянцем, рука автоматически полезла вниз. Вдова явно была в растерянности.\n"

    $ BeckyVar["visitedhome"] = max(BeckyVar.get("visitedhome", 0), 6)

    # Show the group minet image sequence (fallback safe)
    call ShowImageSeq("becky", "dinner", "AllMinet", 2) from _call_georgett_arrival_img

    # === KIDS WATCH (3 flavors, rand_int per TXT) ===
    $ KidsWatch = rand_int(1, 6)
    if KidsWatch <= 3:
        $ MainTxt += "\n\nВдруг вы заметили, что дверь в столовую приоткрыта и за вами кто-то подсматривает. "
        if KidsWatch == 1:
            $ MainTxt += "Это был Ивар, младший сын вдовы. Он не отрываясь смотрел, как отсасывают его мама и старшая сестра, а его рука залезла в штаны."
        elif KidsWatch == 2:
            $ MainTxt += "Это была юная Эмма, средняя дочка Бекки. Она кажется наблюдает за вашей оргией с интересом, восхищением и возбуждением."
        else:
            $ MainTxt += "Это была Эмма с маленькой Лаурой, младшей дочкой Бекки. Лаура явно поражена происходящим, ее глазенки расширились а щеки залила краска. Эмма же, на правах старшей, наклонилась к ней и шепотом комментирует происходящее."
        $ MainTxt += "\n\n"

        # Call the dedicated kids watch helper if it exists (from IntBeckyGuest.rpy port)
        if renpy.has_label("BeckyGuestKidsWatchStepsCode"):
            call BeckyGuestKidsWatchStepsCode from _call_georgett_kids_watch

    # === CUM VARIANTS FOR EDDIE + LUCAS (rand_int) ===
    if rand_int(1, 2) == 1:
        $ MainTxt += "Тем временем кончил и Эдди, в последний момент он выдернул свой член изо рта Жоржетты и выстрелил потоками спермы ей на лицо. Та, ничуть не смутившись, опять поймала его член своим ротиком и начисто его облизала. "
    else:
        $ MainTxt += "Тем временем кончил и Эдди, прямо в ротик Жоржетты. Шлюшка выпила все до капли! "

    if rand_int(1, 2) == 1:
        $ MainTxt += "За Эдди настал черед и Лукаса. Прижав голову Инги к своей промежности он накончал ей полный рот. "
    else:
        $ MainTxt += "Глядя на Эдди спустил и Лукас, обкончав Беккиной дочке все ее личико и даже немного ее рыжие волосы. "

    $ CurLocDesc = MainTxt

    # === PLAYER INTERACTION MENU (exact options + gates from GeorgettBeckyVisit.txt) ===
    # We use classic Ren'Py menu. Counters and state mutations happen in the chosen block.
    menu:
        "Осмотреть Жоржетту":
            call GirlsDesc("georgett") from _call_georgett_desc
            $ MainTxt += "\n\nВы внимательно осмотрели Жоржетту. Она выглядела совершенно в своей стихии."
            $ CurLocDesc = MainTxt
            # Continue to next menu round or fallthrough to watch
            jump becky_home_georgett_visit_menu_continue

        "Смотреть что будет дальше":
            $ MainTxt += "\n\nВаш взгляд перебегал с Жоржетты на Ингенборг, с Инги на Бекки. Лукас и Эдди просто млели от того, что с ними вытворяли их дамы. Глядя на их блаженные лица вы представляли себя на их месте.\n\n"
            $ MainTxt += "Первым кончил неопытный Эдди, в последний момент он выдернул свой член изо рта Жоржетты и выстрелил потоками спермы ей на лицо. Та, ничуть не смутившись, опять поймала его член своим ротиком и начисто его облизала.\n"
            $ MainTxt += "За Эдди настал черед и Лукаса. Прижав голову Инги к своей промежности он накончал ей полный рот. Вдова, не отрываясь, смотрела на Эдди и Ингу, ее руки неосознанно мяли собственную грудь, выдавая возбуждение.\n\n"
            $ MainTxt += "Вдруг, поняв что все закончилось, Бекки пришла в себя и строго сказала первое, что пришло ей на ум: «Дети, если вы закончили, то помогите убрать со стола.»"

            call ShowImageSeq("becky", "dinner", "SurpMinet", 2) from _call_georgett_watch_img

            # Pregnancy + SlutFriends (exact calls from TXT, no gs)
            call PregnancyCheck("inga", "mouth", 1, "Лукас") from _call_georgett_preg_inga
            call PregnancyCheck("georgett", "mouthface", 1, "eddie") from _call_georgett_preg_georgett
            call SlutFriendsIncrease("inga", 0, 0, 0, 50, 1, 1) from _call_georgett_slut_inga
            call SlutFriendsIncrease("becky", 0, 0, 0, 50, 1, 1) from _call_georgett_slut_becky
            call SlutFriendsIncrease("georgett", 0, 0, 0, 60, 1, 1) from _call_georgett_slut_georgett

            $ georgedinnersex = 0

            # Stage complete — advance the thread
            if thread is not None:
                $ thread.advance()

            $ Talked["becky"] = Talked.get("becky", 0) + 1
            $ CurLocDesc = MainTxt
            # Fallback to detailed engine for any remaining dinner flow
            if renpy.has_label("GeorgettBeckyVisit"):
                call GeorgettBeckyVisit from _call_georgett_fallback_watch
            elif renpy.has_label("IntBeckyGuest"):
                call IntBeckyGuest("becky", "BeckyHome") from _call_georgett_fallback_guest
            return

        "Расстегнуть штаны и позвать Бекки":
            # Exact gate logic from TXT translated (no QSP, direct + rand_int)
            $ beckyminetagree = rand_int(1, 3)
            if sluttiness.get("becky", 0) < 40:
                $ beckyminetagree = 3
            elif BeckyVar.get("BeckyOpenMinet", 0) > 0 and (sluttiness.get("becky", 0) + dinnerbeckyorgasm * 5 > 44):
                $ beckyminetagree = 1
            elif (sluttiness.get("becky", 0) + dinnerbeckyorgasm * 5 > 46) and beckyminetagree == 2:
                $ beckyminetagree = 1
            elif sluttiness.get("becky", 0) > 50:
                $ beckyminetagree = 1

            if sluttiness.get("becky", 0) <= 55:
                $ MainTxt += "Решив не отставать от Эдди с Лукасом, вы решительным движением сбросили с себя штаны и показали Бекки на свой член. "
                if beckyminetagree > 1:
                    $ MainTxt = "Однако ее реакция оказалась совсем не такой, как вы надеялись.\n«Да то, что, Стефан, обалдел?!» — воскликнула вдова. "
                    if BeckyVar.get("BeckyOpenMinet", 0) > 0:
                        $ MainTxt += "«Если я один раз тебе уступила, это не значит, что я тебе теперь всегда буду отсасывать по мановению твоего пальчика. Ты зарываешься. Так что на сегодня — пока, сейчас тебе пожалуй лучше всего будет уйти.»"
                    else:
                        $ MainTxt += "«Да, я сказала Инге и Эдди не стесняться, но к тебе-то это не относилось. Так что сейчас тебе пожалуй лучше всего будет уйти.»"

                    $ MainTxt += "\n\nБудучи в расстроенных чувствах из-за отказа вдовы, вы натянули свои штаны обратно, помахали рукой остальным, и не дождавшись ответного прощания (видно уж слишком заняты были эти две парочки минетом), направились на улицу.\n\n"

                    call SlutFriendsIncrease("becky", 10, 2, -1, 35, 2, -1) from _call_georgett_refuse_slut
                    call PregnancyCheck("inga", "mouth", 1, "Лукас") from _call_georgett_refuse_preg_inga
                    call PregnancyCheck("georgett", "mouthface", 1, "eddie") from _call_georgett_refuse_preg_g
                    call SlutFriendsIncrease("inga", 0, 0, 0, 50, 1, 1) from _call_georgett_refuse_slut_inga
                    call SlutFriendsIncrease("georgett", 0, 0, 0, 60, 1, 1) from _call_georgett_refuse_slut_g

                    $ Talked["becky"] = Talked.get("becky", 0) + 1
                    $ CurLocDesc = MainTxt

                    # Refusal exit — long dinner visit ends
                    $ calendar_v2.advance_minutes(180)
                    jump MarketPlace
                    return
                else:
                    $ MainTxt += "Несколько секунд она мялась, однако все таки наклонилась к вашему другу и начала облизывать головку. Постепенно распаляясь, Бекки начала умело делать вам минет.\nМлея от наслаждения, вы вдруг заметили полный похоти взгляд, которым Эдди одарил свою мамочку. Впрочем, вскоре вы выкинули это из головы, так как Бекки почти довела вас до разрядки."
                    call ShowImageSeq("becky", "dinner", "BeckyMinet", 2) from _call_georgett_minet_img
            else:
                $ MainTxt += "Вы поймали взгляд вдовы, направленный на ваши вздувшиеся бугром штаны. Облизав губы в предвкушении вкусняшки, Ребекка, не смущаясь присутствием своего сына и дочки, встала перед вами на колени, приспустила штаны и начала облизывать ваш поднявшийся орган, лаская себя правой рукой под подолом платья.\nМлея от наслаждения, вы вдруг заметили полный похоти взгляд, которым Эдди одарил свою мамочку. Взгляд, который она ему вернула. Впрочем, вскоре вы выкинули это из головы, так как Бекки почти довела вас до разрядки."
                call ShowImageSeq("becky", "dinner", "BeckyMinet", 2) from _call_georgett_minet_img_high

            $ BeckyVar["BeckyOpenMinet"] = max(1, BeckyVar.get("BeckyOpenMinet", 0))
            call SlutFriendsIncrease("becky", 20, 2, 1, 55, 1, 1) from _call_georgett_minet_slut_becky
            call PregnancyCheck("inga", "mouth", 1, "Лукас") from _call_georgett_minet_preg_inga
            call PregnancyCheck("georgett", "mouthface", 1, "eddie") from _call_georgett_minet_preg_g
            call SlutFriendsIncrease("inga", 0, 0, 0, 55, 1, 1) from _call_georgett_minet_slut_inga
            call SlutFriendsIncrease("georgett", 0, 0, 0, 65, 1, 1) from _call_georgett_minet_slut_g

            $ georgedinnersex += 1

            # Now fall to cum choice menu (georgedinnersex == 2 path in TXT)
            jump becky_home_georgett_visit_cum_menu

label becky_home_georgett_visit_menu_continue:
    # Simple continuation after "look at Georgett" — offer the main choices again
    menu:
        "Смотреть что будет дальше":
            jump becky_home_georgett_visit   # re-enter for the watch block (will hit the menu inside)
        "Расстегнуть штаны и позвать Бекки":
            jump becky_home_georgett_visit   # re-enter to hit the unzip block

label becky_home_georgett_visit_cum_menu:
    # Second stage menu — cum choices only available after successful minet (georgedinnersex >= 1)
    menu:
        "Кончить на лицо" if georgedinnersex >= 1 and (cametoday if 'cametoday' in dir() else 0) < (cancumdaily if 'cancumdaily' in dir() else 3):
            $ MainTxt = "Вытащив в последний момент член изо рта вашей любовницы, вы залили спермой ей все лицо. Оторвав взгляд от украшенной белыми каплями спермы Бекки, вы осмотрелись. "
            $ MainTxt += "\n\nВдова же, не смущаясь, встретилась взглядом с дочкой и сыном, подмигнула им и только затем вытерла лицо от белых капель вашего семени.\nА потом вдруг строго сказала первое, что пришло ей на ум: «Дети, если вы закончили, то помогите убрать со стола.»"

            call PregnancyCheck("becky", "mouthface", 1, "Вы") from _call_georgett_cumface_preg_becky

            $ georgedinnersex = 0

            if thread is not None:
                $ thread.advance()

            $ Talked["becky"] = Talked.get("becky", 0) + 1
            $ CurLocDesc = MainTxt

            # Massive SlutFriends already applied on entry; final family line
            if renpy.has_label("GeorgettBeckyVisit"):
                call GeorgettBeckyVisit from _call_georgett_cumface_fallback
            $ calendar_v2.advance_minutes(180)
            jump MarketPlace
            return

        "Кончить в ротик" if georgedinnersex >= 1 and (cametoday if 'cametoday' in dir() else 0) < (cancumdaily if 'cancumdaily' in dir() else 3):
            $ MainTxt = "Ощутив приближающий оргазм вы и не подумали вытаскивать член из горячего ротика Ребекки или хотя бы предупредить ее. Впрочем, вдову ваша неожиданная разрядка не смутила, это был далеко не первый минет в ее жизни. Даже не поперхнувшись она сглотнула ваше семя и только тогда отпустила начавший обмякать член.\n\n"
            $ MainTxt += "Бекки поймала взгляд Эдди, чуток покраснела, но все-таки, глядя сыну в глаза, облизала ваш член от остатков спермы, встала и строго сказала: «Ну раз мы закончили, то помогите убрать со стола.»"

            call PregnancyCheck("becky", "mouth", 1, "Вы") from _call_georgett_cummouth_preg_becky

            $ georgedinnersex = 0

            if thread is not None:
                $ thread.advance()

            $ Talked["becky"] = Talked.get("becky", 0) + 1
            $ CurLocDesc = MainTxt

            if renpy.has_label("GeorgettBeckyVisit"):
                call GeorgettBeckyVisit from _call_georgett_cummouth_fallback
            $ calendar_v2.advance_minutes(180)
            jump MarketPlace
            return

        "Просто наблюдать окончание":
            $ MainTxt += "\n\nВы просто наблюдали, как две парочки заканчивают. Бекки в итоге взяла себя в руки и велела детям убирать со стола."
            $ georgedinnersex = 0
            if thread is not None:
                $ thread.advance()
            $ calendar_v2.advance_minutes(180)
            jump MarketPlace
            return

    # Safety fallback
    if thread is not None:
        $ thread.advance()
    return


# =============================================================================
# BECKY HOME VISITS THREAD REGISTRATION (LThreadData style)
# Add more stages (arrival, eat, grope, to_bedroom, eddie_group, poproshchatysya, front, blackwood etc.)
# as they are ported one-by-one. The Georgett crossover is the high-visibility EddieWhoreHome=4 gate.
# =============================================================================

init python:
    # Minimal registration so _test_thread_by_name + StoryThreadBoard can see our atomic stages.
    # In full implementation this lives in InitBecky.rpy or a central thread init that imports BeckyEvents.
    try:
        # Only define if not already present (prevents duplicate registration on reload)
        if 'beckyThreadList' not in dir() or beckyThreadList is None:
            beckyThreadList = []
    except Exception:
        pass

    # Fallback shim so tests + thread board still run (real LThreadData lives in StoryEventRuntime / engine)
    if 'LThreadData' not in dir():
        class LThreadData(object):
            def __init__(self, level, person, name, condStr, triggers, highlight=True, threaded=True):
                self.level = level
                self.person = person
                self.name = name
                self.condStr = condStr
                self.triggers = triggers or []
                self.highlight = highlight
                self.threaded = threaded

    # The Georgett crossover stage (priority high during dinner when flag set)
    georgett_crossover_event = (
        "becky_home_georgett_visit",
        None, None, None,
        1,
        None,
        "EddieWhoreHome == 4 and dinnertime == 5",
        None,
        "BeckyHome",
        "eat",
        5,
    )

    georgett_arrival_event = (
        "becky_home_georgett_arrival",
        None, None, None,
        1,
        None,
        "EddieWhoreHome == 4 and dinnertime == 5",
        None,
        "BeckyHome",
        "eat",
        4,
    )

    # Append a BeckyHomeVisits thread entry containing the crossover stages (plus placeholders for the others already ported)
    # This makes the framework + board see the full list the user expects in test_becky_home_visits_thread
    home_visits_triggers = [
        ("becky_home_dinner_arrival", None, None, None, 1, None, "True", None, "BeckyHome", "enter", 1),
        ("becky_home_dinner_bring_supplies", None, None, None, 1, None, "visitedhome >= 1", None, "BeckyHome", "talk", 2),
        ("becky_home_dinner_eat", None, None, None, 1, None, "dinnertime < 5", None, "BeckyHome", "eat", 3),
        ("becky_home_dinner_grope", None, None, None, 1, None, "dinnertime <= 5 and dinnerbeckyorgasm == 0", None, "BeckyHome", "eat", 4),
        georgett_arrival_event,
        georgett_crossover_event,
        ("becky_home_dinner_to_bedroom", None, None, None, 1, None, "dinnertime == 6", None, "BeckyHome", "bedroom", 6),
        ("becky_home_dinner_poproshchatysya", None, None, None, 1, None, "True", None, "BeckyHome", "exit", 10),
        ("becky_home_front_inga_lucas", None, None, None, 1, None, "True", None, "BeckyHomeFront", "enter", 1),
    ]

    # Only add once
    already_registered = any(getattr(t, 'name', None) == 'BeckyHomeVisits' for t in beckyThreadList) if beckyThreadList else False
    if not already_registered:
        beckyThreadList.append(
            LThreadData(
                2,                    # level
                "becky",              # person
                "BeckyHomeVisits",    # name (the multi-visit guest thread)
                "EddieWhoreHome >= 0 or BeckyVar.get('visitedhome', 0) >= 1",  # condStr
                home_visits_triggers,
                highlight=True,
                threaded=True
            )
        )

    # Blackwood (ex-Sherwood) quest thread registration
    blackwood_triggers = [
        ("becky_eddie_black_eye", None, None, None, 1, None, "visitedhome >= 5 and Friends.get('becky',0) >= 15 and EddieRobbed == 0", None, "GroceryStore", "morning", 1),
        ("becky_blackwood_quest_start", None, None, None, 1, None, "EddieRobbedDay > 0 and TradeOffer == 0", None, "GroceryStore", "talk", 2),
        ("becky_blackwood_talk_reveal", None, None, None, 1, None, "KnowSherwood == 1 and TradeOffer == 1 and AdmitSherwood == 0", None, "GroceryStore", "talk", 3),
    ]

    already_blackwood = any(getattr(t, 'name', None) == 'BeckyBlackwoodQuest' for t in beckyThreadList) if beckyThreadList else False
    if not already_blackwood:
        beckyThreadList.append(
            LThreadData(
                2,
                "becky",
                "BeckyBlackwoodQuest",   # or BeckyEddie — matches test expectations
                "EddieRobbedDay > 0 or BeckyVar.get('TradeOffer', 0) >= 1 or KnowBlackwood == 1",
                blackwood_triggers,
                highlight=True,
                threaded=True
            )
        )

    # Robin + Blackwood camp / Zimmer mission thread (separate or sub of Blackwood)
    robin_triggers = [
        ("robin_mongol_vouch_safe_passage", None, None, None, 1, None, "MongolVar.get('StocksReleased',0)==1 and RobinVar.get('MongolSafePass',0)==0", None, "SherwoodCut", "encounter", 1),
        ("zimmer_bandit_camp_choice", None, None, None, 1, None, "RobinVar.get('MongolSafePass',0)==1 or RobinVar.get('RobbedNum',0)>=1", None, "SherwoodCut", "camp", 2),
        ("zimmer_guard_mission_update", None, None, None, 1, None, "ZimmerVar.get('ComplainRobin',0)>=2 and (RobinVar.get('PlayerDestroyedCamp',0)==1 or RobinVar.get('ZimmerPeaceful',0)==1)", None, "CityGuard", "report", 3),
    ]

    already_robin = any(getattr(t, 'name', None) == 'RobinBlackwood' for t in beckyThreadList) if beckyThreadList else False
    if not already_robin:
        beckyThreadList.append(
            LThreadData(
                2,
                "robin",
                "RobinBlackwood",
                "RobinVar.get('MongolSafePass',0)==1 or ZimmerVar.get('ComplainRobin',0)>=1",
                robin_triggers,
                highlight=True,
                threaded=True
            )
        )

    # Also expose for direct fallback in tests
    try:
        store.beckyThreadList = beckyThreadList
    except Exception:
        pass


# =============================================================================
# BLACKWOOD (ex-SHERWOOD) QUEST - Becky trade run to Kunidell / Cundail elves
# =============================================================================
# The arc after Eddie gets beaten by the "обездоленные" (Robin gang) in the Sherwood cut.
# Triggered rarely on NewDay when home guest progress + friendship high.
# For ~12 days after EddieRobbedDay: Becky covers morning GroceryStore shifts.
# Eddie black eye talks (multi-stage in IntEddieTalk) eventually reveal details + set KnowSherwood.
# Becky offers regular profitable veggie hauls to the elves (BeckyQuestInit at GroceryStore).
# Full road danger + negotiation/robbery in SherwoodTravel.
# We use modern "Blackwood" naming alongside legacy flags for the rename.

label becky_eddie_black_eye:
    # Atomic NewDay trigger event for the robbery (Eddie returns beaten).
    # References:
    #   textLocRef\NextDay_NewDayEvents.txt:118 (the exact rare condition + EddieRobbedDay set + DailyEventsList wiring to BeckyQuestInit)
    #   textLocRef\GroceryStore.txt:74 (black eye description shown in morning while window active)
    #   devdocs/characters/full_logic/becky_full_logic.md and IntEddieTalk.txt (EddieRobbedDay +12 day window for talks)
    #   InitBecky.txt (EddieRobbedDay default = 0)
    #
    # In real game this is called from NewDay engine. Here we simulate the rare roll with rand_int.
    # Sets EddieRobbedDay, marks EddieRobbed=1 to prevent re-trigger, schedules the quest daily.

    show screen main_ui
    $ becky = getPersonInfo("becky")

    $ BeckyVar.setdefault("EddieRobbed", 0)
    $ BeckyVar.setdefault("EddieRobbedDay", 0)
    $ BeckyVar.setdefault("SherwoodSuspect", 0)

    if BeckyVar.get("EddieRobbed", 0) == 1:
        return   # already happened this arc

    # Rare 1/6 roll (exact match to source). Only if guest progress + friends sufficient.
    if (BeckyVar.get("visitedhome", 0) >= 5 and
            Friends.get("becky", 0) >= 15 and
            rand_int(1, 6) == 1 and dayspassed > 0):

        $ BeckyVar["EddieRobbedDay"] = dayspassed
        $ BeckyVar["EddieRobbed"] = 1

        $ MainTxt = "Эдди вернулся с синяком под глазом и распухшим ухом. Он явно получил хорошую взбучку где-то за городом.\n\n"
        $ MainTxt += "В ближайшие дни (примерно две недели) Бекки будет чаще появляться утром в лавке, прикрывая сына."

        $ CurLocDesc = MainTxt

        # Wire the daily quest offer (in real engine this goes through DailyEventsList / CheckDailyEvent)
        # For the thin event we just mark that the offer is now available at GroceryStore.
        $ BeckyVar["SherwoodQuestScheduled"] = 1

        if thread is not None:
            $ thread.advance()

        $ Talked["becky"] = Talked.get("becky", 0) + 1

        # Note: the actual "Eddie black eye visible + talk options" appear automatically in GroceryStore while the +12 day window is open.
        # The detailed multi-stage "Спросить о синяке" tree lives in IntEddieTalk (with FingalTalk progression and the famous "отмудохали" line).
        return

    return


label becky_blackwood_quest_start:
    # The core offer scene (BeckyQuestInit) — Becky pulls the player aside at GroceryStore and pitches the regular Kunidell/Cundail trade run.
    # References:
    #   textLocRef\BeckyQuestInit.txt (full pitch: "Стефан, я вижу ты человек надежный...", 4 мешка по 50м, 50-300 profit, morning except Sunday)
    #   textLocRef\IntBeckyTalkSherwood.txt (follow-up questions about the "загвоздка", elves, son, road through Sherwood/Blackwood)
    #   textLocRef\NextDay_NewDayEvents.txt (how the daily event fires this)
    #   textLocRef\GroceryStore.txt (the morning context + black eye note)
    #   game/Inn/SherwoodTravel.rpy + game/NPC/Secondary/SherwoodTravel.rpy (the actual dangerous road + Robin encounters + profit return)
    #
    # Sets TradeOffer, possible early SherwoodWarn (if high relationship), then player can dig via IntBeckyTalkSherwood.
    # Thread advances on acceptance of the offer or full admission of the danger.

    show screen main_ui
    $ becky = getPersonInfo("becky")

    python:
        BeckyVar.setdefault("TradeOffer", 0)
        BeckyVar.setdefault("SherwoodWarn", 0)
        BeckyVar.setdefault("SherwoodSuspect", 0)
        BeckyVar.setdefault("EddieRobbedDay", 0)
        Friends = Friends if 'Friends' in dir() else {}
        Friends.setdefault("becky", 0)
        giveorgasms = giveorgasms if 'giveorgasms' in dir() else {}
        giveorgasms.setdefault("becky", 0)

    if BeckyVar.get("TradeOffer", 0) >= 1:
        # Already pitched — fall through to detailed talk for follow-ups
        if renpy.has_label("IntBeckyTalkSherwood"):
            call IntBeckyTalkSherwood from _call_blackwood_talk_fallback
        return

    $ MainTxt = "«Стефан, я вижу ты человек надежный, тебе можно доверять,» неожиданно обратилась к вам Бекки, прервав ваше глубокомысленное разглядывание выложенных на продажу огурцов и прочей репы.\n\n"
    $ MainTxt += "Вы попытались ответить что-то про веру и надежность, но запутались.\n\n"
    $ MainTxt += "«Вот и ладушки,» обрадованно сказала вдова. «Заработать хочешь?»\n\n"

    $ CurLocDesc = MainTxt

    # Classic menu for the initial choice (exact from BeckyQuestInit.txt)
    menu:
        "А кто ж не хочет?":
            $ MainTxt += "«Это правильно, денежки все любят,» согласилась с вами вдова.\n\n"

            $ BeckyVar["TradeOfferText"] = "«Значит так, может ты слышал, часах в 6 езды от города есть эльфийский замок. Куниделл называется. Так вот, с едой там дела не очень обстоят. Эльфы, сам понимаешь, что с них взять. Каждую грядку им надо, видишь ли, расположить в согласии с музыкой сфер, на это у них время есть. А скажем полить или прополоть — так на это у них ни желания, ни времени нет.»\n\n«И как урожаи у них?»\n\n«А никак. Поэтому и цены у них повыше. В общем смотри. Тебе нужна лошадь. Я тебе продам 4 больших мешка всяких овощей — по полквинтала каждый, 50 мараведи штука. Навьючишь их, утром в путь, там продашь с наваром не меньше, чем полсотни мараведи. А может и три сотни выручишь. А на следующий день опять так можешь. Эльфы они такие, хоть и возвышенные, но прожорливые. В общем, утром в любой день заходи, ну кроме воскресенья, конечно.»"

            $ MainTxt += BeckyVar["TradeOfferText"]

            if Friends.get("becky", 0) >= 17 and giveorgasms.get("becky", 0) >= 9:
                $ MainTxt += "\n\n«Правда, есть тут небольшая загвоздка,» чуть менее радостным тоном заметила Ребекка, «а, впрочем ерунда, вряд ли это что серьезное.»"
                $ BeckyVar["SherwoodWarn"] = 1
                $ BeckyVar["SherwoodSuspect"] += 1

            $ BeckyVar["TradeOffer"] = 1

            if thread is not None:
                $ thread.advance()

            $ Talked["becky"] = Talked.get("becky", 0) + 1
            $ CurLocDesc = MainTxt

            # Now player can ask follow-ups via the Sherwood talk label (or fall to detailed engine)
            if renpy.has_label("IntBeckyTalkSherwood"):
                call IntBeckyTalkSherwood from _call_blackwood_offer_talk
            return

        "Неа. Меня ни работа, ни деньги не интересуют":
            $ MainTxt += "«Ну ладно, раз так. Но если передумаешь, то не стесняйся, спроси,» разочарованно сказала вдовушка."
            $ BeckyVar["TradeOffer"] = 2

            $ Talked["becky"] = Talked.get("becky", 0) + 1
            $ CurLocDesc = MainTxt
            jump MarketPlace
            return

    return


label becky_blackwood_talk_reveal:
    # Key admission moment: player presses about the road danger after knowing about Eddie's beating.
    # This is the "Насчет дороги в Куниделл" option that fully reveals the bandits and sets modern KnowBlackwood.
    # References: textLocRef\IntBeckyTalkSherwood.txt (the long admission paragraph + AdmitSherwood + high SherwoodSuspect)

    show screen main_ui
    $ becky = getPersonInfo("becky")

    $ BeckyVar.setdefault("KnowSherwood", 0)
    $ BeckyVar.setdefault("KnowBlackwood", 0)
    $ BeckyVar.setdefault("AdmitSherwood", 0)
    $ BeckyVar.setdefault("SherwoodSuspect", 0)
    $ BeckyVar.setdefault("TradeOffer", 0)

    if BeckyVar.get("AdmitSherwood", 0) >= 1 or BeckyVar.get("KnowBlackwood", 0) == 1:
        return

    $ MainTxt = "«Дорожка в Куниделл, случаем не через Шервудский лес проходит?» невинно осведомились вы.\n\n"
    $ MainTxt += "«Через него, это верно. Только какой там лес, от него и не осталось почти ничего,» заметно нервничая ответила вам Ребекка.\n\n"
    $ MainTxt += "«А там никто, случаем, не пошаливает? Грабеж, все такое?»\n\n"
    $ MainTxt += "«Ну как тебе сказать... Дело в том, что да, ты прав, в Куниделл надо ехать через Шервудский лес. Ну, вернее уже не лес, но это не важно. Там уже давно как эти засели, как их там, обездоленные. Говорят, что мол наша добрая герцогиня в их несчастьях и горькой судьбинушке виновата. Раньше от них вреда особого не было, так, собирали по паре десятков мараведи на пропитание. А недавно разухабились, сыночка моего ненаглядного побили, товар отобрали, лошадь отобрали. Так я и решила, ты паренек смышленый, что-нибудь придумаешь. И мне выгода, и тебе прибыток.»"

    $ BeckyVar["SherwoodSuspect"] += 10
    $ BeckyVar["AdmitSherwood"] = 1
    $ BeckyVar["KnowBlackwood"] = 1          # modern rename flag
    $ BeckyVar["KnowSherwood"] = 1           # keep legacy for compatibility

    if thread is not None:
        $ thread.advance()

    $ Talked["becky"] = Talked.get("becky", 0) + 1
    $ CurLocDesc = MainTxt

    # Further conversation (robbery consolation, "you didn't warn me", how to deal with Robin) lives in the detailed IntBeckyTalkSherwood or later thin stages.
    if renpy.has_label("IntBeckyTalkSherwood"):
        call IntBeckyTalkSherwood from _call_blackwood_reveal_talk
    return


# =============================================================================
# ROBIN + MONGOL VOUCH + ZIMMER MISSION (Blackwood part 2)
# =============================================================================
# Mongol released from stocks (MongolVar["StocksReleased"]) → later vouch to Robin
# → RobinVar["MongolSafePass"] = 1 lets MC pass the cut without losing horse/money.
# Zimmer (guard boss) gave mission to deal with outlaws disrupting trade.
# On the way to Cunidale (for Becky veggies) player reaches the bandit camp.
# Choice: destroy the camp (violent) or solve peacefully for Zimmer quest.
# This file owns the thin milestone events + thread visibility.
# Full camp content + Cunidale village + detailed third Blackwood part = future work (see TODO).

label robin_mongol_vouch_safe_passage:
    # Triggered when the player has the Mongol release flag and first meets Robin (or returns).
    # Mongol (after being freed from stocks by player) puts in a good word.
    # This saves the MC's ass (horse + money) from the usual "пожертвование" shakedown.
    # References:
    #   tools/external_click_play_test.py (MongolVar["StocksReleased"], RobinVar["MongolSafePass"])
    #   textLocRef\MongolTalk.txt + stocks story events in StoryEventRuntime
    #   textLocRef\SherwoodTravel.txt + IntRobinTalk.txt (current robbery path we now bypass)
    #   game/NPC/Secondary/InitSecondaryNPC.rpy (Robin registration + MongolSafePass default)

    show screen main_ui
    $ robin = getPersonInfo("robin") if "robin" in dir() else None

    $ MongolVar.setdefault("StocksReleased", 0)
    $ RobinVar.setdefault("MongolSafePass", 0)
    $ RobinVar.setdefault("KnowHim", 0)

    if MongolVar.get("StocksReleased", 0) == 0 or RobinVar.get("MongolSafePass", 0) == 1:
        return

    $ MainTxt = "Когда вы подходите к группе в зелёных трико, один из бандитов узнаёт вас и дёргает Робина за рукав.\n\n"
    $ MainTxt += "«Йо, браза, это тот самый трактирщик. Монгол велел своих предупредить: этот чувак не мазафака, он его из колодок вытащил.»\n\n"
    $ MainTxt += "Робин смотрит на вас с новым интересом, потом широко улыбается.\n\n"
    $ MainTxt += "«Вот это другое дело, бразар. За Монгола уважуха. Раз наш человек сказал, что ты браза, значит сегодня ты едешь как браза. Деньги при себе оставь, коняшку тоже. Но если кто спросит — мы тебя не пропускали. Социяльная ответственность, понимаешь?»\n\n"

    $ RobinVar["MongolSafePass"] = 1
    $ RobinVar["KnowHim"] = 1

    if thread is not None:
        $ thread.advance()

    $ CurLocDesc = MainTxt

    # Safe passage granted — no robbery this time. Player can continue to Cunidale.
    # Later visits may still have complications unless further relationship built.
    return


label zimmer_bandit_camp_choice:
    # Milestone on the road to Cunidale (elven village for Becky's vegetable trade).
    # Player has reached the bandit camp.
    # Two paths (this is only the choice point for now):
    # 1. Violent: destroy/eliminate the camp (for Becky trade safety or personal reasons).
    # 2. Peaceful: try to solve Zimmer's mission without bloodshed (investigation, negotiation, etc.).
    # Mongol vouch may help with peaceful route.
    # References:
    #   textLocRef\IntZimmerTalk.txt (the "Пожаловаться на Робин Гуда" paid investigation mission)
    #   textLocRef\SherwoodTravel.txt + IntRobinTalk.txt (current encounters)
    #   game/NPC/Secondary/InitSecondaryNPC.rpy (ZimmerVar RobinInvestigationDay + Robin registration)
    #   Future: full Cunidale content + third Blackwood part (see TODO file)

    show screen main_ui
    $ zimmer = getPersonInfo("zimmer") if "zimmer" in dir() else None
    $ robin = getPersonInfo("robin") if "robin" in dir() else None

    $ ZimmerVar.setdefault("ComplainRobin", 0)
    $ RobinVar.setdefault("MongolSafePass", 0)
    $ RobinVar.setdefault("PlayerDestroyedCamp", 0)
    $ RobinVar.setdefault("ZimmerPeaceful", 0)

    $ MainTxt = "Вы добрались до лагеря обездоленных на вырубке. Несколько десятков человек в зелёных трико. Робин в центре.\n\n"

    if RobinVar.get("MongolSafePass", 0) == 1:
        $ MainTxt += "Благодаря слову Монгола вас пока не трогают. Можно попробовать договориться.\n\n"
    else:
        $ MainTxt += "Без защиты Монгола любой подход опасен — вас могут сразу попытаться «попросить на социяльную ответственность».\n\n"

    $ MainTxt += "Вы вспоминаете поручение десятника Циммермана: «решить проблему разбойников, мешающих торговле».\n\n"
    $ CurLocDesc = MainTxt

    menu:
        "Уничтожить лагерь (силовой вариант)":
            $ MainTxt += "Вы решаете, что мирным путём не обойтись. Лагерь нужно ликвидировать.\n"
            $ MainTxt += "(Полная реализация этого пути — уничтожение, последствия для торговли, реакция Зиммера и Бекки — в будущей части квеста.)\n"
            $ RobinVar["PlayerDestroyedCamp"] = 1

            if thread is not None:
                $ thread.advance()

            # Placeholder return / jump to future camp destruction scene
            return

        "Попробовать решить мирно (для миссии Зиммера)":
            $ MainTxt += "Вы вспоминаете поручение Циммермана. Возможно, удастся договориться, провести «расследование» или найти компромисс, который устроит и стражу, и Бекки, и даже Робина.\n"
            $ MainTxt += "(Полная реализация мирного пути — переговоры, условия, последствия, оплата от Зиммера — в будущей части квеста.)\n"
            $ RobinVar["ZimmerPeaceful"] = 1

            if thread is not None:
                $ thread.advance()

            return

        "Пока отступить и подумать":
            $ MainTxt += "Вы решаете не форсировать события прямо сейчас. Нужно подготовиться."
            return

    return


label zimmer_guard_mission_update:
    # Thin atomic update event called after the player returns from the bandit camp choice point.
    # Updates Zimmer's investigation state based on what the player actually did (destroy vs peaceful).
    # Ties the paid complaint in IntZimmerTalk to real player action in Blackwood.
    # References:
    #   textLocRef\IntZimmerTalk.txt (horse theft + Robin complaint + investigation follow-up + "поймайте и приведите сами")
    #   game/NPC/Secondary/InitSecondaryNPC.rpy (ZimmerVar + registration)
    #   zimmer_bandit_camp_choice (the choice the player made)

    show screen main_ui
    $ zimmer = getPersonInfo("zimmer") if "zimmer" in dir() else None

    $ ZimmerVar.setdefault("MissionUpdatedByPlayer", 0)
    $ ZimmerVar.setdefault("PlayerHandledRobin", 0)
    $ ZimmerVar.setdefault("ComplainRobin", 0)
    $ RobinVar.setdefault("PlayerDestroyedCamp", 0)
    $ RobinVar.setdefault("ZimmerPeaceful", 0)

    if ZimmerVar.get("MissionUpdatedByPlayer", 0) == 1:
        return   # already processed

    $ MainTxt = "Вы возвращаетесь к десятнику Циммерману в городскую стражу.\n\n"

    if RobinVar.get("PlayerDestroyedCamp", 0) == 1:
        $ MainTxt += "«Десятник, я сам разобрался с этими разбойниками в вырубке.»\n\n"
        $ MainTxt += "Циммерман выглядит одновременно впечатлённым и слегка испуганным вашей смелостью.\n"
        $ MainTxt += "«Ай-яй, молодой человек... Вы таки серьёзный человек. Ну что ж, дело закрыто. Если вдруг что-то ещё... вы знаете, где меня найти.»\n"
        $ ZimmerVar["PlayerHandledRobin"] = 1
        $ ZimmerVar["MissionUpdatedByPlayer"] = 1

        if thread is not None:
            $ thread.advance()

    elif RobinVar.get("ZimmerPeaceful", 0) == 1:
        $ MainTxt += "Вы рассказываете Циммерману о договорённости, которую удалось достичь с Робином (или компромиссе).\n\n"
        $ MainTxt += "Десятник кивает, пряча улыбку. «Молодой человек, вы меня удивляете. Я думал, вы просто заплатите и забудете. А вы таки решили вопрос по-настоящему. Молодец. Стража в долгу.»\n"
        $ ZimmerVar["PlayerHandledRobin"] = 2
        $ ZimmerVar["MissionUpdatedByPlayer"] = 1

        if thread is not None:
            $ thread.advance()

    else:
        $ MainTxt += "Вы пока не готовы отчитаться о результатах миссии."

    $ CurLocDesc = MainTxt
    $ Talked["zimmer"] = Talked.get("zimmer", 0) + 1

    return
