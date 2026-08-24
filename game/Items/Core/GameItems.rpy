# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
define MALE_DRESS_ITEM_IDS = (
    "dress_villagedress",
    "dress_citydress",
    "dress_sailordress",
    "dress_thiefdress",
    "dress_nobbledress",
)

define FEMALE_DRESS_ITEM_IDS = (
    "dress_modestworkdress",
    "dress_modestnicedress",
    "dress_workdress",
    "dress_workdresszhilet",
    "dress_greenworkdress",
    "dress_openworkdress",
    "dress_minidress",
    "dress_slutdress",
    "dress_simplebra",
    "dress_simplepanties",
    "dress_whitestockings",
    "dress_blackstockings",
    "dress_redstockings",
    "dress_nightshirt",
)


init 5 python:
    def ensure_game_item_registry():
        """Compatibility-free initialization hook; items self-register on construction."""
        return game_item_registry
