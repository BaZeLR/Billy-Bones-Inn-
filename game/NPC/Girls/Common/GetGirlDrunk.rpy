# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# GetGirlDrunk.rpy
# Converted from legacy script. Handles getting a girl drunk and stat changes.
# All logic and conditions preserved.

init python:
    def get_girl_drunk(girl_name):
        girl_info = people.get_info(girl_name)
        if girl_info is not None and int(girl_info.drunk or 0) == 0:
            girl_info.drunk = 1
            girl_info.change_social(friend_delta=2, corruption_delta=4)

# Usage: call from python with get_girl_drunk(girl_name)


label get_girl_drunk(girl_name=""):
    $ get_girl_drunk(girl_name)
    return
