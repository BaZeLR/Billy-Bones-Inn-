# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Amanda/Legare Dance Sequence Generator (Chained Event Logic)
# Converted from legacy script. Handles creation of Amanda/Legare dance event table and outcome logic.
# To be called from FridayDance or related event chains.

label story_amanda_legare_dance_0:
    vscene "images/market/LocFridayDance.jpg"
    "У края танцующей толпы Аманда замечает, что месье Легаре смотрит на нее с терпеливым интересом."
    "Она делает вид, что ей все равно, но между песнями ее взгляд снова и снова возвращается к нему."
    $ Amanda.mark_legare_intro_seen()
    $ event_runtime.active_thread.advance()
    return
label story_amanda_legare_dance_1:
    vscene "images/market/LocFridayDance.jpg"
    $ GetDanceFromTable("amanda", "legare", rooms.get("FridayDance").dance_count)
    $ Amanda.dancing_with_legare = True
    call EventAmandaLegareCreateDance
    $ rooms.get("FridayDance").dance_count += 1
    "Вы нашли Аманду как раз в тот момент, когда месье Легаре галантно склонился перед ней и протянул руку."
    "Аманда смущенно оглянулась по сторонам, но руку все же подала. Через миг они уже кружились среди танцующих."
    call ShowImage("amanda", "dance", "legare_step_0")
    $ rooms.get("FridayDance").step = 1
    $ event_runtime.active_thread.advance()
    call IntAmandaDance
    return

label story_amanda_legare_dance_2:
    vscene "images/market/LocFridayDance.jpg"
    $ GetDanceFromTable("amanda", "legare", rooms.get("FridayDance").dance_count)
    $ Amanda.dancing_with_legare = True
    call EventAmandaLegareCreateDance
    $ rooms.get("FridayDance").dance_count += 1
    "На этот раз Аманда уже не выглядит случайно втянутой в танец. Она замечает Легаре раньше вас и сама делает к нему пару шагов."
    "Виноторговец улыбается слишком довольно, будто считал этот вечер уже выигранным."
    call ShowImage("amanda", "dance", "legare_step_0")
    $ Amanda.legare_affection = max(2, Amanda.legare_affection)
    $ rooms.get("FridayDance").step = 1
    $ event_runtime.active_thread.advance()
    call IntAmandaDance
    return

label story_amanda_legare_dance_3:
    vscene "images/market/LocFridayDance.jpg"
    $ GetDanceFromTable("amanda", "legare", rooms.get("FridayDance").dance_count)
    $ Amanda.dancing_with_legare = True
    call EventAmandaLegareCreateDance
    $ rooms.get("FridayDance").dance_count += 1
    "Легаре больше не ограничивается учтивостью. Он говорит Аманде что-то на ухо, и она вспыхивает, но не отходит."
    "Теперь это уже не просто танец. Между ними появилась своя маленькая тайна, и Аманда слишком хорошо это понимает."
    call ShowImage("amanda", "dance", "legare_step_0")
    $ Amanda.change_mana(-1, "friday_dance_legare_pressure")
    $ rooms.get("FridayDance").step = 1
    $ event_runtime.active_thread.advance()
    call IntAmandaDance
    return

label story_amanda_legare_dance_4:
    vscene "images/market/LocFridayDance.jpg"
    $ GetDanceFromTable("amanda", "legare", rooms.get("FridayDance").dance_count)
    "Вы находите Аманду уже после танца. Легаре держит ее под руку и что-то тихо говорит, склонившись к самому уху."
    "Аманда краснеет, но не отстраняется. По ее взгляду понятно: решение уже принято, осталось только увидеть, вмешаетесь вы или нет."
    $ Amanda.dancing_with_legare = False
    $ Amanda.left_friday_dance = True
    $ event_runtime.active_thread.advance()
    call LegareAmandaGoMenu
    return

label AmandaLegareDanceSequence(dance_created=0, force_legare_first_dance=False, go_phrase="", dance_index=0, created_index=0):
    # Dev note: This event generates Amanda/Legare dance sequence and outcomes for the Friday dance event.
    $ Amanda.escaped_dance_unnoticed = False
    if int(calendar_v2.week or 0) == 5:
        $ GirlDance_Clear()
        $ force_legare_first_dance = Amanda.legare_claims_first_friday_dance()
        # Friendship/prohibition logic
        if Amanda.legare_forbidden:
            $ Amanda.legare_affection = max(0, Amanda.legare_affection - 1)
            if Amanda.legare_affection >= 12:
                $ dance_created = procedural_randint(1,2, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:165:4")
            elif Amanda.legare_affection >= 8:
                $ dance_created = 1
            elif Amanda.legare_affection >= 4:
                if procedural_randint(1,2, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:169:5") == 1:
                    $ dance_created = 1
            else:
                if procedural_randint(1,4, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:172:6") == 1:
                    $ dance_created = 1
        elif Amanda.legare_affection >= 8:
            $ dance_created = procedural_randint(2,4, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:175:7")
        else:
            $ dance_created = procedural_randint(1,3, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:177:8")
        if force_legare_first_dance:
            $ dance_created = max(dance_created, 1)
        $ Amanda.legare_departure_code = 0
        if (Amanda.legare_affection >= 11 and Amanda.corruption >= 16) or (Amanda.legare_affection >= 5 and Amanda.corruption >= 30) or (Amanda.corruption >= 50):
            $ Amanda.legare_departure_code = 1
            if Amanda.corruption < 20:
                $ go_phrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Она замялась, и, потупив глаза, покачала головой. Альбер пожал плечами и снова закружился с ней в танце.'
                $ Amanda.legare_departure_code = 2
            elif Amanda.corruption < 35:
                $ go_phrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Она замялась, но, после небольшого раздумья, кивнула. Альбер взял Аманду под ручку и они поспешили прочь с площади.'
            else:
                if procedural_randint(1,2, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:190:9") == 1:
                    $ go_phrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Даже не дослушав его, она обрадованно кивнула, поцеловала месье в губы и потянула прочь с площади. Тот последовал за ней.'
                else:
                    $ go_phrase = 'Тут Аманда вдруг засмеялась, сказала что-то Альберу и потянула его за руку прочь. Тот несколько смутился от ее напора, но обрадованно последовал за ней.'
        # Create dance table entries
        while dance_index < 5:
            if force_legare_first_dance and dance_index == 0:
                $ created_index += 1
                if Amanda.legare_departure_code > 0 and dance_created <= 1:
                    $ GirlDance_Add('amanda', 'legare', 1, Amanda.legare_departure_code, go_phrase)
                    $ Amanda.legare_departure_code = 0
                    $ created_index = dance_created
                else:
                    $ GirlDance_Add('amanda', 'legare', 1, 0, '')
            elif procedural_randint(1, max(1, 5-dance_index), key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:206:10") <= dance_created-created_index:
                $ created_index += 1
                if Amanda.legare_departure_code > 0 and ((created_index > dance_created-1 and procedural_randint(1,2, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:208:11") == 1) or created_index == dance_created):
                    $ GirlDance_Add('amanda', 'legare', dance_index + 1, Amanda.legare_departure_code, go_phrase)
                    $ Amanda.legare_departure_code = 0
                    $ created_index = dance_created
                else:
                    $ GirlDance_Add('amanda', 'legare', dance_index + 1, 0, '')
            $ dance_index += 1
        # End of dance creation
    return

# --- Amanda/Legare outcome menu and logic ---
label LegareAmandaGoMenu():
    # Dev note: This menu is shown when Amanda and Legare leave the dance together.
    $ Amanda.left_friday_dance = True
    $ Amanda.legare_departure_code = 0
    $ Amanda.dancing_with_legare = False
    menu:
        "Проследить за ними":
            jump AfterDanceSexLegare
        "Продолжить танцевать":
            # Show message and run let-go code
            "Решив не вмешиваться в личную жизнь Аманды, вы проводили парочку взглядом и остались танцевать."
            $ Amanda.resolve_legare_let_go()
            jump FridayDance
        "Остановить их и отправить Аманду домой":
            call AfterDanceLegare("Prohibit")
            jump FridayDance
    return
