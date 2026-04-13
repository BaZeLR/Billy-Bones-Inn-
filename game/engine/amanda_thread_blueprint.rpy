# Amanda thread blueprint.
# This file is a catalog of Amanda-specific R/L/U thread definitions and safe wrapper labels.
# It is intentionally not appended to the active threadList yet.
# To activate it later, merge AmandaThreadBlueprint into the engine's threadList.

default AmandaThreadBlueprint = []
default AmandaRThreadBlueprint = []
default AmandaLThreadBlueprint = []
default AmandaUThreadBlueprint = []

init 100 python:
    def _amanda_bp_i(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def _amanda_bp_var(name, default=0):
        return _amanda_bp_i(globals().get("AmandaVar", {}).get(name, default), default)

    def _amanda_bp_stat(table_name, key="amanda", default=0):
        table = globals().get(table_name, {})
        if not isinstance(table, dict):
            return default
        return _amanda_bp_i(table.get(key, default), default)

    def _amanda_bp_cur_loc():
        return str(globals().get("CurLoc", "") or "")

    def _amanda_bp_has_sex_event(place_name=""):
        finder = globals().get("CheckIfSexEventExist")
        if not callable(finder):
            return False
        cur_time = _amanda_bp_i(globals().get("time", 0), 0)
        try:
            return _amanda_bp_i(finder("amanda", cur_time, place_name), 0) > 0
        except Exception:
            return False

    def amanda_bp_tavern_entry_ready():
        func = globals().get("story_amanda_tavern_entry_ready")
        return bool(callable(func) and func())

    def amanda_bp_street_entry_ready():
        func = globals().get("story_amanda_street_entry_ready")
        return bool(callable(func) and func())

    def amanda_bp_market_entry_ready():
        func = globals().get("story_amanda_market_entry_ready")
        return bool(callable(func) and func())

    def amanda_bp_glory_try_ready():
        return _amanda_bp_has_sex_event("glorytry") and _amanda_bp_cur_loc() == "TavernMain"

    def amanda_bp_liza_arc_ready():
        return _amanda_bp_var("lizafriends") > 0 or _amanda_bp_var("prohibitliza") > 0

    def amanda_bp_liza_glory_ready():
        return _amanda_bp_var("glorytried") > 0 or _amanda_bp_var("gloryscold") > 0 or _amanda_bp_var("glorywalkout") > 0 or _amanda_bp_var("glorysuck") > 0

    def amanda_bp_legare_arc_ready():
        return _amanda_bp_var("alberfriends") >= 5 or _amanda_bp_var("alberprohibit") > 0 or _amanda_bp_var("knowlegaresex") > 0

    def amanda_bp_legare_dance_ready():
        return _amanda_bp_legare_arc_ready() and _amanda_bp_i(globals().get("week", 0), 0) == 5

    def amanda_bp_legare_aftermath_ready():
        return _amanda_bp_var("sawlegaresex") > 0 or _amanda_bp_var("knowyousawlegaresex") > 0 or _amanda_bp_var("knowlegaresex") > 0

    def amanda_bp_legare_sex_ready():
        return _amanda_bp_var("sucklegare") > 0 or _amanda_bp_var("fucklegare") > 0 or _amanda_bp_var("deflowerlegare") > 0

    def amanda_bp_room_ready():
        return _amanda_bp_var("kickyoufromroom") == 0

    def amanda_bp_dress_ready():
        return _amanda_bp_var("MomDressComplaint") > 0 or _amanda_bp_stat("sluttiness") >= 20

    def amanda_bp_warn_not_work_ready():
        return _amanda_bp_var("warnnotwork") > 0

    def amanda_bp_boys_talk_ready():
        return _amanda_bp_var("sawwithguys") > 0 or _amanda_bp_var("prohibitwithguys") > 0

    def amanda_bp_virginity_talk_ready():
        return _amanda_bp_var("knownotvirgin") > 0 or _amanda_bp_var("knowdeflowerlegare") > 0

    def amanda_bp_pregnancy_talk_ready():
        return _amanda_bp_stat("pregnancy") >= 120 or _amanda_bp_var("askzalettoday") == 0

    def build_amanda_thread_blueprint():
        if "RThreadData" not in globals() or "LThreadData" not in globals() or "UThreadData" not in globals():
            return [], [], [], []

        random_threads = [
            RThreadData(0, "amanda", "AmbientRandom", None, (4,
                [
                    ("story_amanda_tavern_entry", None, None, None, 1, None, "amanda_bp_tavern_entry_ready()", None, "TavernMain", "enter", 0),
                    ("story_amanda_street_entry", None, None, None, 1, None, "amanda_bp_street_entry_ready()", None, "StreetTavern", "enter", 0),
                    ("story_amanda_market_entry", None, None, None, 1, None, "amanda_bp_market_entry_ready()", None, "MarketPlace", "enter", 0),
                    ("amanda_bp_glory_try", None, None, None, 1, None, "amanda_bp_glory_try_ready()", None, "TavernMain", "enter", 5),
                ]),
                highlight=False,
                threaded=False,
            ),
        ]

        linear_threads = [
            LThreadData(0, "amanda", "LizaArc", None, [
                ("amanda_bp_liza_intro", None, None, None, 1, None, "amanda_bp_liza_arc_ready()", None, "TavernMain", "talk", 0),
                ("amanda_bp_liza_glory", None, None, None, 1, None, "amanda_bp_liza_glory_ready()", None, "TavernMain", "talk", 0),
            ], highlight=True),
            LThreadData(0, "amanda", "LegareArc", None, [
                ("amanda_bp_legare_talk", None, None, None, 1, None, "amanda_bp_legare_arc_ready()", None, "TavernMain", "talk", 0),
                ("amanda_bp_legare_dance", 5, None, None, 1, None, "amanda_bp_legare_dance_ready()", None, "FridayDance", "enter", 0),
                ("amanda_bp_legare_aftermath", None, None, None, 1, None, "amanda_bp_legare_aftermath_ready()", None, "TavernMain", "talk", 0),
                ("amanda_bp_legare_sex", None, None, None, 1, None, "amanda_bp_legare_sex_ready()", None, "TavernMain", "talk", 0),
            ], highlight=True),
            LThreadData(0, "amanda", "DressArc", None, [
                ("amanda_bp_dress_intro", None, None, None, 1, None, "amanda_bp_dress_ready()", None, "TavernMain", "talk", 0),
                ("amanda_bp_dress_room", None, None, None, 1, None, "amanda_bp_room_ready()", None, "TavernAmandaRoom", "enter", 0),
            ], highlight=True),
        ]

        unordered_threads = [
            UThreadData(0, "amanda", "TalkStates", None, [
                ("amanda_bp_warn_not_work", None, None, None, 1, None, "amanda_bp_warn_not_work_ready()", None, "TavernMain", "talk", 5),
                ("amanda_bp_boys_talk", None, None, None, 1, None, "amanda_bp_boys_talk_ready()", None, "TavernMain", "talk", 10),
                ("amanda_bp_virginity_talk", None, None, None, 1, None, "amanda_bp_virginity_talk_ready()", None, "TavernMain", "talk", 15),
                ("amanda_bp_pregnancy_talk", None, None, None, 1, None, "amanda_bp_pregnancy_talk_ready()", None, "TavernMain", "talk", 20),
            ], highlight=False),
        ]

        all_threads = list(random_threads) + list(linear_threads) + list(unordered_threads)
        return random_threads, linear_threads, unordered_threads, all_threads

    AmandaRThreadBlueprint, AmandaLThreadBlueprint, AmandaUThreadBlueprint, AmandaThreadBlueprint = build_amanda_thread_blueprint()

label amanda_bp_glory_try:
    jump AmandaAtGloryHole

label amanda_bp_liza_intro:
    call EventAmandaLizettTalk(1)
    if _return:
        "[_return]"
    if thread:
        $ thread.advance()
    jump TavernMain

label amanda_bp_liza_glory:
    call IntAmandaTalk()
    if thread:
        $ thread.advance()
    jump TavernMain

label amanda_bp_legare_talk:
    call IntAmandaTalk()
    if thread:
        $ thread.advance()
    jump TavernMain

label amanda_bp_legare_dance:
    call AmandaLegareDanceSequence
    if thread:
        $ thread.advance()
    jump FridayDance

label amanda_bp_legare_aftermath:
    jump AfterDanceLegare

label amanda_bp_legare_sex:
    jump AfterDanceSexLegare

label amanda_bp_dress_intro:
    call int_amanda_dress_change("amanda")
    if thread:
        $ thread.advance()
    jump TavernMain

label amanda_bp_dress_room:
    if thread:
        $ thread.advance()
    jump TavernAmandaRoom

label amanda_bp_warn_not_work:
    call IntAmandaTalk()
    if thread and hasattr(thread, "seen"):
        $ thread.seen(0)
    jump TavernMain

label amanda_bp_boys_talk:
    call IntAmandaTalk()
    if thread and hasattr(thread, "seen"):
        $ thread.seen(1)
    jump TavernMain

label amanda_bp_virginity_talk:
    call IntAmandaTalk()
    if thread and hasattr(thread, "seen"):
        $ thread.seen(2)
    jump TavernMain

label amanda_bp_pregnancy_talk:
    call IntAmandaTalk()
    if thread and hasattr(thread, "seen"):
        $ thread.seen(3)
    jump TavernMain
