# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Amanda/Legare Dance Sequence Generator (Chained Event Logic)
# Converted from legacy script. Handles creation of Amanda/Legare dance event table and outcome logic.
# To be called from FridayDance or related event chains.

init python:
    def amanda_legare_claims_first_friday_dance():
        try:
            if str(getLocation("alber") or "") != "FridayDance":
                return False
        except Exception:
            return False
        try:
            if str(getLocation("clara") or "") == "FridayDance":
                return False
        except Exception:
            pass
        return True

    def build_legare_amanda_let_go_plan(use_forced_type=0, forced_type=0):
        if int(use_forced_type or 0) == 1:
            tmp_legare_sex_type = int(forced_type or 0)
        else:
            tmp_legare_sex_type = 1
            if tmp_legare_sex_type == 2 and procedural_randint(1, 6, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:27:1") <= 5:
                tmp_legare_sex_type = 1

        plan = {
            "sex_type": tmp_legare_sex_type,
            "sucklegare": 0,
            "fucklegare": 0,
            "deflowerlegare": 0,
            "set_virginity": None,
            "alberfriends_delta": 0,
            "slut_args": (),
            "pregnancy_target": "",
        }

        if tmp_legare_sex_type <= 1:
            plan["sucklegare"] = 1
            plan["alberfriends_delta"] = 1
            plan["slut_args"] = ("amanda", 0, 0, 0, 40, 1, 1)
            plan["pregnancy_target"] = "mouth"
        elif tmp_legare_sex_type == 2:
            plan["fucklegare"] = 1
            plan["deflowerlegare"] = 1
            plan["set_virginity"] = 0
            plan["alberfriends_delta"] = 2
            plan["slut_args"] = ("amanda", 0, 0, 0, 50, 1, 4)
            if procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:52:2") <= 2:
                plan["alberfriends_delta"] += 1
                plan["pregnancy_target"] = "inside"
            else:
                plan["alberfriends_delta"] += 2
                plan["pregnancy_target"] = "outside"
        else:
            plan["fucklegare"] = 1
            plan["slut_args"] = ("amanda", 0, 0, 0, 50, 1, 2)
            if procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:61:3") <= 2:
                plan["alberfriends_delta"] = 1
                plan["pregnancy_target"] = "inside"
            else:
                plan["alberfriends_delta"] = 2
                plan["pregnancy_target"] = "outside"

        return plan

    def apply_legare_amanda_let_go_code(use_forced_type=0, forced_type=0):
        plan = build_legare_amanda_let_go_plan(use_forced_type, forced_type)
        Amanda.set_var_int("sucklegare", int(plan.get("sucklegare", 0) or 0))
        Amanda.set_var_int("fucklegare", int(plan.get("fucklegare", 0) or 0))
        Amanda.set_var_int("deflowerlegare", int(plan.get("deflowerlegare", 0) or 0))
        if plan.get("set_virginity", None) is not None:
            Amanda.set_sex_stat("virginity", bool(int(plan.get("set_virginity", 0) or 0)))
        Amanda.set_var_int("alberfriends", Amanda.var_int("alberfriends", 0) + int(plan.get("alberfriends_delta", 0) or 0))
        slut_args = tuple(plan.get("slut_args", ()) or ())
        if slut_args:
            Amanda.apply_social_chance(slut_args[1], slut_args[2], slut_args[3], slut_args[4], slut_args[5], slut_args[6], "legare_dance_outcome")
        pregnancy_target = str(plan.get("pregnancy_target", "") or "")
        if pregnancy_target != "":
            Amanda.pregnancy_check(pregnancy_target, 1, "legare")
        return plan

label story_amanda_legare_dance_0:
    vscene "images/market/LocFridayDance.jpg"
    "У края танцующей толпы Аманда замечает, что месье Легаре смотрит на нее с терпеливым интересом."
    "Она делает вид, что ей все равно, но между песнями ее взгляд снова и снова возвращается к нему."
    $ Amanda.mark_legare_intro_seen()
    $ thread.advance()
    return

label story_amanda_legare_dance_1:
    vscene "images/market/LocFridayDance.jpg"
    $ Amanda.set_var_int("albernowdances", 1)
    $ Amanda.set_var_int("legare_dance_pending", 0)
    call EventAmandaLegareCreateDance
    $ FridayDanceRoom.state["dance_count"] += 1
    "Вы нашли Аманду как раз в тот момент, когда месье Легаре галантно склонился перед ней и протянул руку."
    "Аманда смущенно оглянулась по сторонам, но руку все же подала. Через миг они уже кружились среди танцующих."
    call ShowImage("amanda", "dance", "legare_step_0")
    $ DanceStep = 1
    $ Amanda.set_var_int("legare_dance_thread_stage", 1)
    $ thread.advance()
    call IntAmandaDance
    return

label story_amanda_legare_dance_2:
    vscene "images/market/LocFridayDance.jpg"
    $ Amanda.set_var_int("albernowdances", 1)
    $ Amanda.set_var_int("legare_dance_pending", 0)
    call EventAmandaLegareCreateDance
    $ FridayDanceRoom.state["dance_count"] += 1
    "На этот раз Аманда уже не выглядит случайно втянутой в танец. Она замечает Легаре раньше вас и сама делает к нему пару шагов."
    "Виноторговец улыбается слишком довольно, будто считал этот вечер уже выигранным."
    call ShowImage("amanda", "dance", "legare_step_0")
    $ Amanda.set_var_int("legare_dance_thread_stage", 2)
    $ Amanda.set_var_int("alberfriends", max(2, Amanda.var_int("alberfriends", 0)))
    $ DanceStep = 1
    $ thread.advance()
    call IntAmandaDance
    return

label story_amanda_legare_dance_3:
    vscene "images/market/LocFridayDance.jpg"
    $ Amanda.set_var_int("albernowdances", 1)
    $ Amanda.set_var_int("legare_dance_pending", 0)
    call EventAmandaLegareCreateDance
    $ FridayDanceRoom.state["dance_count"] += 1
    "Легаре больше не ограничивается учтивостью. Он говорит Аманде что-то на ухо, и она вспыхивает, но не отходит."
    "Теперь это уже не просто танец. Между ними появилась своя маленькая тайна, и Аманда слишком хорошо это понимает."
    call ShowImage("amanda", "dance", "legare_step_0")
    $ Amanda.set_var_int("legare_dance_thread_stage", 3)
    $ Amanda.set_var_int("legare_dance_private_seen", 1)
    $ Amanda.change_mana(-1, "friday_dance_legare_pressure")
    $ DanceStep = 1
    $ thread.advance()
    call IntAmandaDance
    return

label story_amanda_legare_dance_4:
    vscene "images/market/LocFridayDance.jpg"
    "Вы находите Аманду уже после танца. Легаре держит ее под руку и что-то тихо говорит, склонившись к самому уху."
    "Аманда краснеет, но не отстраняется. По ее взгляду понятно: решение уже принято, осталось только увидеть, вмешаетесь вы или нет."
    $ Amanda.set_var_int("albernowdances", 0)
    $ Amanda.set_var_int("legare_dance_pending", 0)
    $ Amanda.set_var_int("leftdances", 1)
    $ Amanda.set_var_int("legare_dance_thread_stage", 4)
    $ thread.advance()
    call LegareAmandaGoMenu
    return

label AmandaLegareDanceSequence:
    # Dev note: This event generates Amanda/Legare dance sequence and outcomes for the Friday dance event.
    $ DanceCreated = 0
    $ Amanda.set_var_int("EscapeUnnoticed", 0)
    if week == 5:
        $ GirlDance_Clear()
        $ ForceLegareFirstDance = amanda_legare_claims_first_friday_dance()
        # Friendship/prohibition logic
        if Amanda.var_int("alberprohibit", 0) == 1:
            $ Amanda.set_var_int("alberfriends", max(0, Amanda.var_int("alberfriends", 0) - 1))
            if Amanda.var_int("alberfriends", 0) >= 12:
                $ DanceCreated = procedural_randint(1,2, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:165:4")
            elif Amanda.var_int("alberfriends", 0) >= 8:
                $ DanceCreated = 1
            elif Amanda.var_int("alberfriends", 0) >= 4:
                if procedural_randint(1,2, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:169:5") == 1:
                    $ DanceCreated = 1
            else:
                if procedural_randint(1,4, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:172:6") == 1:
                    $ DanceCreated = 1
        elif Amanda.var_int("alberfriends", 0) >= 8:
            $ DanceCreated = procedural_randint(2,4, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:175:7")
        else:
            $ DanceCreated = procedural_randint(1,3, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:177:8")
        if ForceLegareFirstDance:
            $ DanceCreated = max(DanceCreated, 1)
        $ Amanda.set_var_int("LegareGo", 0)
        $ GoPhrase = ""
        if (Amanda.var_int("alberfriends", 0) >= 11 and Amanda.corruption >= 16) or (Amanda.var_int("alberfriends", 0) >= 5 and Amanda.corruption >= 30) or (Amanda.corruption >= 50):
            $ Amanda.set_var_int("LegareGo", 1)
            if Amanda.corruption < 20:
                $ GoPhrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Она замялась, и, потупив глаза, покачала головой. Альбер пожал плечами и снова закружился с ней в танце.'
                $ Amanda.set_var_int("LegareGo", 2)
            elif Amanda.corruption < 35:
                $ GoPhrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Она замялась, но, после небольшого раздумья, кивнула. Альбер взял Аманду под ручку и они поспешили прочь с площади.'
            else:
                if procedural_randint(1,2, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:190:9") == 1:
                    $ GoPhrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Даже не дослушав его, она обрадованно кивнула, поцеловала месье в губы и потянула прочь с площади. Тот последовал за ней.'
                else:
                    $ GoPhrase = 'Тут Аманда вдруг засмеялась, сказала что-то Альберу и потянула его за руку прочь. Тот несколько смутился от ее напора, но обрадованно последовал за ней.'
        # Create dance table entries
        $ i = 0
        $ j = 0
        while i < 5:
            if ForceLegareFirstDance and i == 0:
                $ j += 1
                if Amanda.var_int("LegareGo", 0) > 0 and DanceCreated <= 1:
                    $ GirlDance_Add('amanda', 'legare', 1, Amanda.var_int("LegareGo", 0), GoPhrase)
                    $ Amanda.set_var_int("LegareGo", 0)
                    $ j = DanceCreated
                else:
                    $ GirlDance_Add('amanda', 'legare', 1, 0, '')
            elif procedural_randint(1, max(1, 5-i), key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:206:10") <= DanceCreated-j:
                $ j += 1
                if Amanda.var_int("LegareGo", 0) > 0 and ((j > DanceCreated-1 and procedural_randint(1,2, key="procedural:NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy:procedural_randint:208:11") == 1) or j == DanceCreated):
                    $ GirlDance_Add('amanda', 'legare', i + 1, Amanda.var_int("LegareGo", 0), GoPhrase)
                    $ Amanda.set_var_int("LegareGo", 0)
                    $ j = DanceCreated
                else:
                    $ GirlDance_Add('amanda', 'legare', i + 1, 0, '')
            $ i += 1
        # End of dance creation
    return

# --- Amanda/Legare outcome menu and logic ---
label LegareAmandaGoMenu():
    # Dev note: This menu is shown when Amanda and Legare leave the dance together.
    $ Amanda.set_var_int("leftdances", 1)
    $ Amanda.set_var_int("LegareGo", 0)
    $ Amanda.set_var_int("albernowdances", 0)
    menu:
        "Проследить за ними":
            jump AfterDanceSexLegare
        "Продолжить танцевать":
            # Show message and run let-go code
            "Решив не вмешиваться в личную жизнь Аманды, вы проводили парочку взглядом и остались танцевать."
            call LegareAmandaLetGoCode
            jump FridayDance
        "Остановить их и отправить Аманду домой":
            call AfterDanceLegare("Prohibit")
            jump FridayDance
    return

# --- Amanda/Legare let-go outcome logic ---
label LegareAmandaLetGoCode(args=None):
    $ _legare_args = tuple(args or ())
    $ _legare_plan = apply_legare_amanda_let_go_code(*_legare_args)
    return

