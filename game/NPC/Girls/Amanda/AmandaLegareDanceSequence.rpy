# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Amanda/Legare Dance Sequence Generator (Chained Event Logic)
# Converted from legacy script. Handles creation of Amanda/Legare dance event table and outcome logic.
# To be called from FridayDance or related event chains.

init python:
    def build_legare_amanda_let_go_plan(use_forced_type=0, forced_type=0):
        if int(use_forced_type or 0) == 1:
            tmp_legare_sex_type = int(forced_type or 0)
        else:
            tmp_legare_sex_type = 1
            if tmp_legare_sex_type == 2 and renpy.random.randint(1, 6) <= 5:
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
            if renpy.random.randint(1, 3) <= 2:
                plan["alberfriends_delta"] += 1
                plan["pregnancy_target"] = "inside"
            else:
                plan["alberfriends_delta"] += 2
                plan["pregnancy_target"] = "outside"
        else:
            plan["fucklegare"] = 1
            plan["slut_args"] = ("amanda", 0, 0, 0, 50, 1, 2)
            if renpy.random.randint(1, 3) <= 2:
                plan["alberfriends_delta"] = 1
                plan["pregnancy_target"] = "inside"
            else:
                plan["alberfriends_delta"] = 2
                plan["pregnancy_target"] = "outside"

        return plan

    def apply_legare_amanda_let_go_code(use_forced_type=0, forced_type=0):
        plan = build_legare_amanda_let_go_plan(use_forced_type, forced_type)
        AmandaVar["sucklegare"] = int(plan.get("sucklegare", 0) or 0)
        AmandaVar["fucklegare"] = int(plan.get("fucklegare", 0) or 0)
        AmandaVar["deflowerlegare"] = int(plan.get("deflowerlegare", 0) or 0)
        if plan.get("set_virginity", None) is not None:
            virginity["amanda"] = int(plan.get("set_virginity", 0) or 0)
        AmandaVar["alberfriends"] = int(AmandaVar.get("alberfriends", 0) or 0) + int(plan.get("alberfriends_delta", 0) or 0)
        slut_args = tuple(plan.get("slut_args", ()) or ())
        if slut_args:
            slut_friends_increase(slut_args[0], slut_args[1], slut_args[2], slut_args[3], slut_args[4], slut_args[5], slut_args[6])
        pregnancy_target = str(plan.get("pregnancy_target", "") or "")
        if pregnancy_target != "":
            PregnancyCheck("amanda", pregnancy_target, 1, "legare")
        return plan

label AmandaLegareDanceSequence:
    # Dev note: This event generates Amanda/Legare dance sequence and outcomes for the Friday dance event.
    $ DanceCreated = 0
    $ AmandaVar['EscapeUnnoticed'] = 0
    if week == 5:
        $ GirlDance_Clear()
        # Friendship/prohibition logic
        if AmandaVar.get('alberprohibit', 0) == 1:
            $ AmandaVar['alberfriends'] = max(0, AmandaVar['alberfriends'] - 1)
            if AmandaVar['alberfriends'] >= 12:
                $ DanceCreated = renpy.random.randint(1,2)
            elif AmandaVar['alberfriends'] >= 8:
                $ DanceCreated = 1
            elif AmandaVar['alberfriends'] >= 4:
                if renpy.random.randint(1,2) == 1:
                    $ DanceCreated = 1
            else:
                if renpy.random.randint(1,4) == 1:
                    $ DanceCreated = 1
        elif AmandaVar['alberfriends'] >= 8:
            $ DanceCreated = renpy.random.randint(2,4)
        else:
            $ DanceCreated = renpy.random.randint(1,3)
        $ AmandaVar['LegareGo'] = 0
        $ GoPhrase = ""
        if (AmandaVar['alberfriends'] >= 11 and sluttiness['amanda'] >= 16) or (AmandaVar['alberfriends'] >= 5 and sluttiness['amanda'] >= 30) or (sluttiness['amanda'] >= 50):
            $ AmandaVar['LegareGo'] = 1
            if sluttiness['amanda'] < 20:
                $ GoPhrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Она замялась, и, потупив глаза, покачала головой. Альбер пожал плечами и снова закружился с ней в танце.'
                $ AmandaVar['LegareGo'] = 2
            elif sluttiness['amanda'] < 35:
                $ GoPhrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Она замялась, но, после небольшого раздумья, кивнула. Альбер взял Аманду под ручку и они поспешили прочь с площади.'
            else:
                if renpy.random.randint(1,2) == 1:
                    $ GoPhrase = 'Тут месье Легаре что-то шепнул на ушко Аманде. Даже не дослушав его, она обрадованно кивнула, поцеловала месье в губы и потянула прочь с площади. Тот последовал за ней.'
                else:
                    $ GoPhrase = 'Тут Аманда вдруг засмеялась, сказала что-то Альберу и потянула его за руку прочь. Тот несколько смутился от ее напора, но обрадованно последовал за ней.'
        # Create dance table entries
        $ i = 0
        $ j = 0
        while i < 5:
            if renpy.random.randint(1, max(1, 5-i)) <= DanceCreated-j:
                $ j += 1
                if AmandaVar['LegareGo'] > 0 and ((j > DanceCreated-1 and renpy.random.randint(1,2) == 1) or j == DanceCreated):
                    $ GirlDance_Add('amanda', 'legare', i + 1, AmandaVar['LegareGo'], GoPhrase)
                    $ AmandaVar['LegareGo'] = 0
                    $ j = DanceCreated
                else:
                    $ GirlDance_Add('amanda', 'legare', i + 1, 0, '')
            $ i += 1
        # End of dance creation
    return

# --- Amanda/Legare outcome menu and logic ---
label LegareAmandaGoMenu():
    # Dev note: This menu is shown when Amanda and Legare leave the dance together.
    $ AmandaVar['leftdances'] = 1
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

