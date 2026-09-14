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


def test_eddie_group_sex_session_uses_only_eddie_owned_state():
    sex = (ROOT / "game/NPC/Girls/Becky/IntBeckySex.rpy").read_text(encoding="utf-8-sig")
    home = (ROOT / "game/Town/BeckyHome.rpy").read_text(encoding="utf-8-sig")

    assert "GrupenSex" not in sex
    assert "GrupenSex" not in home
    assert 'Eddie.set_sex_stat("group_sex", 1 if arrive_mode == "SvalnyiGreh" else 0)' in home
    assert 'int(Eddie.sex_stat("group_sex", 0) or 0)' in sex
    assert sex.count('Eddie.set_sex_stat("group_sex", 0)') == 3


def test_eddie_scene_helpers_exist_at_init_for_save_loading():
    source = (ROOT / "game/NPC/Secondary/IntEddieBeckySex.rpy").read_text(
        encoding="utf-8-sig"
    )
    init_block, runtime_block = source.split(
        'label IntEddieBeckySex(GirlNameIBS="becky"):', 1
    )

    assert "init python:" in init_block
    for helper_name in (
        "_iebs_set_arousal",
        "_iebs_arousal",
        "_iebs_inc_arousal",
        "_iebs_set_eddie_pos",
    ):
        assert init_block.count("def %s(" % helper_name) == 1
        assert "def %s(" % helper_name not in runtime_block
