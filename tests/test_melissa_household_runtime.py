"""Execute Melissa's household owners and the existing weekly/achievement engines."""

from types import SimpleNamespace

import pytest

from tests.test_tavern_renovations_runtime import _exec_definitions


@pytest.fixture
def runtime():
    calendar = SimpleNamespace(daysInGame=7, cycle=1100, period=1, day=7, week=7, hour=22)
    calendar.time_slot = lambda: 7
    player = SimpleNamespace(
        chores=SimpleNamespace(weekly={}, last_score=0, last_evaluation=""),
        tavern_management=SimpleNamespace(
            productnum=0, winenum=0, weekly_visitors={}, weekly_chores_last_eval_stamp="",
        ),
    )
    namespace = {
        "calendar_v2": calendar,
        "current_game_day": lambda: calendar.daysInGame,
        "player": player,
        "Girl": type("Girl", (), {"__init__": lambda self, name: None}),
        "GirlWardrobeState": SimpleNamespace(from_base=lambda clothing: None),
        "MelissaStaticData": SimpleNamespace(base_clothing={}),
        "threads": {
            "melissaBatProblem": SimpleNamespace(num=0),
            "sandraWeeklyEvaluation": SimpleNamespace(completed=True),
        },
    }
    for path, names in (
        ("Utilities/General/NPC/PeopleRuntime.rpy", {"people_to_int"}),
        ("NPC/Secondary/WerecatNPC.rpy", {"werecat_story_defaults", "werecat_state"}),
        ("Inn/TavernRenovations.rpy", {"TavernInfo"}),
        ("NPC/Girls/Melissa/InitMelissa.rpy", {"MelissaInfo"}),
        ("Utilities/General/Common/AchievementsEndings.rpy", {
            "tractir_achievements", "TractirProgressRuntimeState", "tractir_activate_achievement",
        }),
        ("Inn/PlayerChoresSystem.rpy", {
            "PLAYER_CHORE_KEYS", "PLAYER_CHORE_TARGETS", "PLAYER_CORE_OTHER_GIRLS",
            "_pc_to_int", "_ensure_player_chores_state", "player_chore_target",
            "weekly_chores_evaluation_preview", "evaluate_weekly_chores_and_rewards",
        }),
    ):
        _exec_definitions(path, names, namespace)

    namespace["werecat"] = SimpleNamespace(var=namespace["werecat_story_defaults"]())
    namespace["tavern"] = namespace["TavernInfo"]()
    namespace["Melissa"] = namespace["MelissaInfo"]()
    namespace["tractir_progress"] = namespace["TractirProgressRuntimeState"]()
    namespace["Sandra"] = SimpleNamespace(
        rel=10, trust=0, anger_with_player=0, rebellion=0,
        change_mana=lambda *args: None, change_fear=lambda *args: None,
    )
    amanda = SimpleNamespace(openness=0, rebel_baseline=0)
    namespace["people"] = SimpleNamespace(
        get_info=lambda key: namespace["Melissa"] if key == "melissa" else amanda,
    )
    # Existing household relationship rewards are outside this feature's scope.
    namespace["relationship_apply_weekly_chore_evaluation"] = lambda preview: None
    return SimpleNamespace(
        namespace=namespace, melissa=namespace["Melissa"], player=player, calendar=calendar,
        tavern=namespace["tavern"], rats=namespace["werecat"].var,
        bat_thread=namespace["threads"]["melissaBatProblem"],
        progress=namespace["tractir_progress"],
        evaluate=namespace["evaluate_weekly_chores_and_rewards"],
    )


def test_new_game_starts_without_comfort_or_stock_rewards(runtime):
    assert runtime.melissa.comfort_components == {
        "rats": 0, "room": 0, "yard": 0, "toilet": 0,
        "cleaning": 0, "bathroom_laundry": 0,
    }
    assert runtime.melissa.comfort == 0
    assert runtime.melissa.household_satisfaction == 0


@pytest.mark.parametrize("stage,due,day,expected", [
    (6, 7, 7, 0), (7, -1, 7, 0), (7, 8, 7, 0), (7, 7, 7, 1), (11, 7, 20, 1),
])
def test_room_comfort_uses_actual_roof_completion(runtime, stage, due, day, expected):
    runtime.bat_thread.num = stage
    runtime.melissa.roof_repair_complete_day = due
    runtime.calendar.daysInGame = day
    assert runtime.melissa.comfort_components["room"] == expected
    assert runtime.melissa.comfort == expected


def test_fixed_comfort_is_derived_live_and_never_accumulates(runtime):
    runtime.rats["rats_problem_active"] = 0
    runtime.bat_thread.num = 7
    runtime.melissa.roof_repair_complete_day = 7
    runtime.tavern.renovation_due_days.update(backyard=8, shed=9)
    assert runtime.melissa.comfort == 2
    runtime.calendar.daysInGame = 8
    assert runtime.melissa.comfort_components["yard"] == 1
    assert runtime.melissa.comfort_components["toilet"] == 1
    assert runtime.melissa.comfort == 4
    runtime.calendar.daysInGame = 9
    for _ in range(3):
        assert runtime.melissa.comfort == 6
    runtime.calendar.daysInGame = 100
    assert runtime.melissa.comfort == 6
    assert runtime.melissa.comfort_cleaning_score == 0
    assert runtime.melissa.household_satisfaction == 0
    assert "comfort" not in vars(runtime.melissa)
    runtime.rats["rats_problem_active"] = 1
    assert runtime.melissa.comfort == 5


@pytest.mark.parametrize("score", [-5, -1, 0, 1, 5])
def test_signed_cleaning_score_is_part_of_comfort(runtime, score):
    runtime.melissa.comfort_cleaning_score = score
    assert runtime.melissa.comfort_components["cleaning"] == score
    assert runtime.melissa.comfort == score


@pytest.mark.parametrize("cleanings,delta", [(0, -1), (1, 1), (3, 1), (8, 1)])
def test_weekly_cleaning_applies_once_before_counter_reset(runtime, cleanings, delta):
    runtime.player.chores.weekly["clean_upstairs_rooms"] = cleanings
    runtime.evaluate()
    assert runtime.melissa.comfort_cleaning_score == delta
    assert runtime.player.chores.weekly["clean_upstairs_rooms"] == 0
    runtime.evaluate()
    assert runtime.melissa.comfort_cleaning_score == delta
    assert runtime.melissa.household_satisfaction == 0


def test_each_missed_week_can_reduce_comfort_below_zero(runtime):
    runtime.evaluate()
    runtime.calendar.day += 7
    runtime.calendar.daysInGame += 7
    runtime.evaluate()
    assert runtime.melissa.comfort_cleaning_score == -2
    runtime.calendar.day += 7
    runtime.calendar.daysInGame += 7
    runtime.player.chores.weekly["clean_upstairs_rooms"] = 1
    runtime.evaluate()
    assert runtime.melissa.comfort_cleaning_score == -1


@pytest.mark.parametrize("weekday,hour", [(6, 22), (1, 6)])
def test_weekly_cleaning_does_not_apply_on_other_days(runtime, weekday, hour):
    runtime.calendar.week = weekday
    runtime.calendar.hour = hour
    runtime.player.chores.weekly["clean_upstairs_rooms"] = 1
    runtime.evaluate()
    assert runtime.melissa.comfort_cleaning_score == 0
    assert runtime.player.chores.weekly["clean_upstairs_rooms"] == 1


def test_weekly_cleaning_handles_sunday_finished_after_midnight(runtime):
    runtime.calendar.week = 1
    runtime.calendar.day = 8
    runtime.calendar.hour = 1
    runtime.player.chores.weekly["clean_upstairs_rooms"] = 1
    runtime.evaluate()
    runtime.evaluate()
    assert runtime.melissa.comfort_cleaning_score == 1


@pytest.mark.parametrize("food,wine,unlocked", [
    (100, 499, False), (100, 500, False), (101, 499, False), (101, 500, True),
])
def test_stock_growth_uses_inventory_boundaries_and_separate_score(runtime, food, wine, unlocked):
    runtime.player.tavern_management.productnum = food
    runtime.player.tavern_management.winenum = wine
    relationship = (runtime.melissa.rel, runtime.melissa.openness, runtime.melissa.corruption)
    runtime.melissa.record_stock_growth()
    assert runtime.melissa.household_satisfaction == 2
    assert runtime.melissa.comfort == 0
    assert (runtime.melissa.rel, runtime.melissa.openness, runtime.melissa.corruption) == relationship
    assert (runtime.player.tavern_management.productnum, runtime.player.tavern_management.winenum) == (food, wine)
    assert runtime.progress.activated_achievements == ({"melissa_full_storeroom"} if unlocked else set())


def test_existing_achievement_engine_deduplicates_stock_rewards(runtime):
    runtime.player.tavern_management.productnum = 101
    runtime.player.tavern_management.winenum = 500
    runtime.melissa.record_stock_growth()
    runtime.melissa.record_stock_growth()
    assert runtime.melissa.household_satisfaction == 4
    assert runtime.progress.activated_achievements == {"melissa_full_storeroom"}
    runtime.progress.activated_achievements.clear()
    runtime.progress.achieved.add("melissa_full_storeroom")
    runtime.melissa.record_stock_growth()
    assert runtime.melissa.household_satisfaction == 6
    assert runtime.progress.activated_achievements == set()
    assert runtime.progress.achieved == {"melissa_full_storeroom"}


def test_stock_threshold_alone_does_not_reward_on_comfort_read(runtime):
    runtime.player.tavern_management.productnum = 101
    runtime.player.tavern_management.winenum = 500
    for _ in range(3):
        assert runtime.melissa.comfort == 0
    assert runtime.melissa.household_satisfaction == 0
    assert runtime.progress.activated_achievements == set()
