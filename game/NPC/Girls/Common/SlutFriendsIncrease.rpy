# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def social_friend_roll_chance(friend_chance, girl_name="", positive_delta=True):
        chance = max(1, int(friend_chance or 1))
        bonus = int(player_social_interaction_bonus() or 0)
        bonus += int(tavern_crew_interaction_bonus(girl_name) or 0)
        if positive_delta:
            return max(1, chance - bonus)
        return max(1, chance + bonus)

    def slut_friends_increase(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness):
        girl_info = people.get_info(girl)
        if girl_info is None:
            return
        positive_friend_chance = social_friend_roll_chance(friend_chance, girl, True)
        negative_friend_chance = social_friend_roll_chance(friend_chance, girl, False)
        friend_steps = abs(int(inc_decr_friends or 0))
        friend_direction = 1 if int(inc_decr_friends or 0) > 0 else -1
        corruption_steps = abs(int(inc_decr_sluttiness or 0))
        corruption_direction = 1 if int(inc_decr_sluttiness or 0) > 0 else -1
        for step in range(friend_steps):
            if friend_direction < 0 and girl_info.rel > int(limit_friend or 0) and procedural_randint(1, negative_friend_chance, "slut_friend_%s_%s_%s_down" % (girl, current_game_day(), step)) == 1:
                girl_info.change_social(friend_delta=-1)
            elif friend_direction > 0 and girl_info.rel < int(limit_friend or 0) and procedural_randint(1, positive_friend_chance, "slut_friend_%s_%s_%s_up" % (girl, current_game_day(), step)) == 1:
                girl_info.change_social(friend_delta=1)
        for step in range(corruption_steps):
            if corruption_direction < 0 and girl_info.corruption > int(limit_sluttiness or 0) and procedural_randint(1, int(sluttiness_chance or 1), "slut_corr_%s_%s_%s_down" % (girl, current_game_day(), step)) == 1:
                girl_info.change_social(corruption_delta=-1)
            elif corruption_direction > 0 and girl_info.corruption < int(limit_sluttiness or 0) and procedural_randint(1, int(sluttiness_chance or 1), "slut_corr_%s_%s_%s_up" % (girl, current_game_day(), step)) == 1:
                girl_info.change_social(corruption_delta=1)

label SlutFriendsIncrease(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness):
    python:
        slut_friends_increase(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness)
    return
