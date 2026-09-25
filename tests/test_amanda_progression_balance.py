from pathlib import Path
from types import SimpleNamespace
import textwrap


ROOT = Path(__file__).resolve().parents[1]
BREAKFAST = ROOT / "game/Inn/TavernKitchenBreakfast.rpy"


class GirlInfo:
    def __init__(self):
        self.rel = 5
        self.openness = 3
        self.corruption = 0
        self.arousal = 0

    def change_social(self, friend_delta=0, open_delta=0, corruption_delta=0):
        self.rel += friend_delta
        self.openness += open_delta
        self.corruption += corruption_delta

    def add_arousal(self, amount):
        self.arousal += amount


def test_group_breakfast_perks_do_not_permanently_advance_amanda():
    source = BREAKFAST.read_text(encoding="utf-8-sig")
    start = source.index("    def tavern_breakfast_apply_group_social(")
    end = source.index("\n    def tavern_breakfast_take_perk_item", start)
    namespace = {}
    exec(textwrap.dedent(source[start:end]), namespace)
    amanda, melissa = GirlInfo(), GirlInfo()
    infos = {"amanda": amanda, "melissa": melissa}
    namespace["people"] = SimpleNamespace(get_info=infos.get)
    namespace["player"] = SimpleNamespace(change_stat=lambda *_args: None)
    namespace["tavern_breakfast_core_present_ids"] = lambda: list(infos)

    namespace["tavern_breakfast_apply_group_social"](
        ["amanda", "melissa"], friend_delta=1, open_delta=1,
        corruption_delta=1, fun_delta=2,
    )

    assert (amanda.rel, amanda.corruption, amanda.openness, amanda.arousal) == (5, 0, 4, 4)
    assert (melissa.rel, melissa.corruption, melissa.openness) == (6, 1, 4)


def test_amanda_daily_breakfast_is_not_an_automatic_friendship_source():
    source = BREAKFAST.read_text(encoding="utf-8-sig")
    block = source.split("def tavern_breakfast_apply_social_bonus():", 1)[1].split(
        "\n    def tavern_sunday_dinner_dialogue_lines", 1
    )[0]
    assert 'if npc_id == "amanda":\n                continue' in block
    assert 'tavern_breakfast_apply_group_social(targets, 1, 0, 0, 2)' in source
    talk = source.split("def tavern_breakfast_talk_result():", 1)[1].split(
        "\n    def tavern_breakfast_melissa_amanda_gerhard_ready", 1
    )[0]
    assert 'if npc_id == "amanda":' in talk
    assert 'Amanda.cycle_state().get("horny", 0.0)' in talk
    assert "Amanda.arousal_value()" in talk


def test_yard_observation_is_one_time_and_walk_home_is_not_corruption():
    window = (ROOT / "game/Inn/TavernMyRoomWindow001.rpy").read_text(encoding="utf-8-sig")
    scene = window.split("label story_amanda_night_bowl_window_0:", 1)[1]
    assert 'if not getattr(Amanda, "backyard_relief_seen", False):' in scene
    assert scene.count("Amanda.change_social(corruption_delta=1)") == 1
    assert "Amanda.backyard_relief_seen = True" in scene

    dance = (ROOT / "game/NPC/Girls/Amanda/AmandaSexDanceStreet.rpy").read_text(encoding="utf-8-sig")
    walk = dance.split("label AmandaAfterDanceMCWalkHome:", 1)[1].split(
        "label AmandaAfterDanceMCReturn:", 1
    )[0]
    assert "Amanda.add_arousal(5)" in walk
    assert "corruption_delta" not in walk


def test_qsp_drunk_bonus_and_next_day_reversal_are_preserved():
    drunk = (ROOT / "game/NPC/Girls/Common/GetGirlDrunk.rpy").read_text(encoding="utf-8-sig")
    day = (ROOT / "game/Utilities/General/NPC/DailySetstatdefault.rpy").read_text(encoding="utf-8-sig")
    assert "girl_info.change_social(friend_delta=2, corruption_delta=4)" in drunk
    assert "_dssd_info.change_social(friend_delta=-2, corruption_delta=-4)" in day
