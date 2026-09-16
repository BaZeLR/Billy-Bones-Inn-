from pathlib import Path
from textwrap import dedent
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]


def test_amanda_gloryhole_scene_state_is_owned_by_amanda():
    event = (ROOT / "game/NPC/Girls/Amanda/AmandaAtGloryHole.rpy").read_text(
        encoding="utf-8-sig"
    )
    room = (ROOT / "game/Inn/TavernGloryHole.rpy").read_text(encoding="utf-8-sig")

    assert "AmandaGloryCurState" not in event + room
    assert 'Amanda.var_int("glory_cur_state", 0)' in event
    assert 'Amanda.set_var_int("glory_cur_state",' in event
    assert 'Amanda.set_var_int("glory_cur_state",' in room
    assert "default AmandaGloryCurState" not in event


def test_gloryhole_story_event_requires_revealed_current_liza_session():
    source = (ROOT / "game/NPC/Girls/Amanda/AmandaEventModel.rpy").read_text(
        encoding="utf-8-sig"
    )
    event_class = "    class AmandaGloryHoleTryEvent(AmandaEvent):"
    class_source = event_class + source.split(event_class, 1)[1].split(
        "    class AmandaMorningWindowEpisodeEvent", 1
    )[0]
    namespace = {"AmandaEvent": object}
    exec(dedent(class_source), namespace)
    event_type = namespace["AmandaGloryHoleTryEvent"]
    event = event_type.__new__(event_type)

    cases = (
        (0, 1, 1, "liza", 1, False),
        (10, 0, 1, "liza", 1, False),
        (10, 1, 0, "liza", 1, False),
        (10, 1, 1, "georgett", 1, False),
        (10, 1, 1, "liza", 0, False),
        (1, 1, 1, "liza", 1, True),
    )
    for stage, present, works, worker, menu_blocked, expected in cases:
        namespace["Amanda"] = SimpleNamespace(var_int=lambda key, default=0: stage)
        session = SimpleNamespace(
            amanda_present=present,
            works=works,
            girl_name=worker,
            menu_blocked=menu_blocked,
        )
        namespace["player"] = SimpleNamespace(
            tavern_management=SimpleNamespace(glory_hole_session=session)
        )
        assert bool(event.checkAmandaConditions()) is expected
