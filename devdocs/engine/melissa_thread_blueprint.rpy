default MelissaThreadBlueprint = []
default MelissaLThreadBlueprint = []

init 100 python:
    def build_melissa_thread_blueprint():
        try:
            linear_threads = [
                LThreadData(0, "melissa", "BatsChain", None, [
                    ("melissa_bats_0", None, None, None, 1, None, "bool(melissa_bat_breakfast_seen()) and int(MelissaVar.get('storage_rat_last_help_day', -1) or -1) >= 0", None, "TavernMelissaRoom", "talk", 0),
                    ("melissa_bats_1", None, None, None, 1, None, "int(MelissaVar.get('AskedMCToSolveRoomProblem', 0) or 0) == 1", None, "TavernMelissaRoom", "inspect", 0),
                    ("melissa_bats_2", None, None, None, 1, None, "int(MelissaVar.get('room_holes_seen', 0) or 0) == 1", None, "TavernAtic", "inspect", 0),
                    ("melissa_bats_3", None, None, None, 1, None, "int(MelissaVar.get('attic_colony_found', 0) or 0) == 1", None, "TavernAtic", "inspect", 0),
                    ("melissa_bats_4", None, None, None, 1, None, "int(MelissaVar.get('attic_fall_scandal', 0) or 0) == 1", None, "TavernAtic", "inspect", 0),
                    ("melissa_bats_5", None, None, None, 1, None, "int(MelissaVar.get('bat_smoke_done', 0) or 0) == 1", None, "TavernAtic", "craft", 0),
                    ("melissa_bats_6", None, None, None, 1, None, "int(MelissaVar.get('roof_repair_order_day', -1) or -1) >= 0", None, "TavernAtic", "repair", 0),
                    ("melissa_bats_7", None, None, None, 1, None, "int(MelissaVar.get('room_pests_cleared', 0) or 0) == 1", None, "TavernMelissaRoom", "aftermath", 0),
                ], highlight=True, threaded=False),
            ]
            return linear_threads, list(linear_threads)
        except Exception:
            return [], []

    MelissaLThreadBlueprint, MelissaThreadBlueprint = build_melissa_thread_blueprint()


label melissa_bats_0:
    jump TavernMelissaRoom

label melissa_bats_1:
    jump TavernMelissaRoom

label melissa_bats_2:
    jump TavernAtic

label melissa_bats_3:
    jump TavernAtic

label melissa_bats_4:
    jump TavernAtic

label melissa_bats_5:
    jump TavernAtic

label melissa_bats_6:
    jump TavernAtic

label melissa_bats_7:
    jump TavernMelissaRoom
