# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# BeckyInviteHome.rpy
# Converted from legacy script. Handles Becky inviting the player home after dancing.
# All logic, conditions, and dev notes preserved.

label BeckyInviteHome(girl_name="becky"):
    if str(player.appearance.current_dress or "") == "citydress" and int(player_charisma_breakdown().get("charisma", 0) or 0) > 75 and Becky.rel >= 10 and Becky.corruption > 20 and int(DanceStep or 0) >= 3 and int(DanceStep or 0) < int(DanceMaxIBD or 0) and Becky.var.get("danceinvitehome", 0) == 0 and procedural_randint(1, 5, "becky_dance_home_invite_%s_%s" % (current_game_day(), DanceStep)) == 1:
        if Becky.var.get("visitedhome", 0) > 0 and Becky.stats.get("sexacts", 0) > 0 and Becky.corruption > 48:
            "Стефан, милый, чем нам здесь танцевать, пойдем-ка лучше ко мне, я уже вся теку!" # развратная вдовушка
        elif Becky.var.get("visitedhome", 0) > 0 and Becky.stats.get("sexacts", 0) > 0:
            "Стефан, милый, а может пойдем ко мне, ну, помнишь, как в прошлый раз?" # Бекки, глядя прямо в глаза
        else:
            "Стефан, а может ко мне в гости зайдешь, вина немного выпьем?" # неожиданно приглашает вдовушка
        $ Becky.var["danceinvitehome"] = 1
    return
