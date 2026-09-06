# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# BeckyInviteHome.rpy
# Converted from legacy script. Handles Becky inviting the player home after dancing.
# All logic, conditions, and dev notes preserved.

label BeckyInviteHome(girl_name="becky"):
    $ renpy.dynamic("_becky_dance_picture_before_invite")
    if Becky.rel >= 10 and Becky.corruption > 20 and int(rooms.get("FridayDance").step or 0) >= 3 and int(rooms.get("FridayDance").step or 0) < int(rooms.get("FridayDance").max_step or 0) and not bool(rooms.get("FridayDance").becky_home_invited) and procedural_randint(1, 5, "becky_dance_home_invite_%s_%s_%s" % (current_game_day(), rooms.get("FridayDance").dance_count, rooms.get("FridayDance").step)) == 1:
        $ _becky_dance_picture_before_invite = scene_runtime.picture
        vscene "images/becky/dance/dance_finish.webm"
        $ renpy.music.set_volume(0.0, delay=0.0, channel="movie")
        menu:
            "Закрыть видео":
                pass
        vscene _becky_dance_picture_before_invite
        if int(threads["beckyHome"].num or 0) > 0 and Becky.stats.get("sexacts", 0) > 0 and Becky.corruption > 48:
            "Стефан, милый, чем нам здесь танцевать, пойдем-ка лучше ко мне, я уже вся теку!" # развратная вдовушка
        elif int(threads["beckyHome"].num or 0) > 0 and Becky.stats.get("sexacts", 0) > 0:
            "Стефан, милый, а может пойдем ко мне, ну, помнишь, как в прошлый раз?" # Бекки, глядя прямо в глаза
        else:
            "Стефан, а может ко мне в гости зайдешь, вина немного выпьем?" # неожиданно приглашает вдовушка
        $ rooms.get("FridayDance").becky_home_invited = True
    return
