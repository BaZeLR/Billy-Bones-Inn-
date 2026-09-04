from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_eddie_group_sex_positions_use_becky_owned_actor_state():
    sources = [
        (ROOT / "game/NPC/Girls/Becky/IntBeckySex.rpy").read_text(encoding="utf-8-sig"),
        (ROOT / "game/NPC/Secondary/IntEddieBeckySex.rpy").read_text(encoding="utf-8-sig"),
    ]

    for source in sources:
        assert "Eddie.stats" not in source
        assert 'Eddie.sex_stat("group_sex", 0)' in source
        assert "Eddie(1 if Becky.cock_in" not in source
        assert 'Becky.cock_in("pussy", "eddie")' in source
        assert 'Becky.cock_in("mouth", "eddie")' in source
        assert 'Becky.cock_in("tits", "eddie")' in source
