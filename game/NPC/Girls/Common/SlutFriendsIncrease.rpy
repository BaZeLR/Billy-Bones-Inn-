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
        # Friends and sluttiness are assumed to be dicts, girl is a string
        import random as random_module
        positive_friend_chance = social_friend_roll_chance(friend_chance, girl, True)
        negative_friend_chance = social_friend_roll_chance(friend_chance, girl, False)
        if inc_decr_friends < 0:
            if Friends[girl] > limit_friend and random_module.randint(1, negative_friend_chance) == 1:
                Friends[girl] -= 1
            inc_decr_friends += 1
        if inc_decr_friends > 0:
            if Friends[girl] < limit_friend and random_module.randint(1, positive_friend_chance) == 1:
                Friends[girl] += 1
            inc_decr_friends -= 1
        if inc_decr_sluttiness < 0:
            if sluttiness[girl] > limit_sluttiness and random_module.randint(1, sluttiness_chance) == 1:
                sluttiness[girl] -= 1
            inc_decr_sluttiness += 1
        if inc_decr_sluttiness > 0:
            if sluttiness[girl] < limit_sluttiness and random_module.randint(1, sluttiness_chance) == 1:
                sluttiness[girl] += 1
            inc_decr_sluttiness -= 1
        # Recursion if needed
        if inc_decr_sluttiness != 0 or inc_decr_friends != 0:
            slut_friends_increase(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness)

label SlutFriendsIncrease(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness):
    python:
        slut_friends_increase(girl, limit_friend, friend_chance, inc_decr_friends, limit_sluttiness, sluttiness_chance, inc_decr_sluttiness)
    return
