from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]


def cycle_runtime(girl, pregnancy_days):
    source = (ROOT / "game/Utilities/General/NPC/GirlDecisionModel.rpy").read_text(encoding="utf-8-sig")
    start = source.index("    def girl_decision_cycle_state(")
    end = source.index("\n    def ", start + 1)
    info = SimpleNamespace(registry_group="girl", pregnancy_days=lambda: pregnancy_days)
    clock = {"day": 0}
    namespace = {
        "people": SimpleNamespace(get_info=lambda key: info if key == girl else None),
        "people_birth_date": lambda key: {"day": 1},
        "girl_decision_int": lambda value, default=0: int(value),
        "current_game_day": lambda: clock["day"],
    }
    exec(textwrap.dedent(source[start:end]), namespace)
    return namespace["girl_decision_cycle_state"], clock


@pytest.mark.parametrize("girl", ("amanda", "melissa", "sandra", "liza", "georgett", "becky", "inga", "clara"))
@pytest.mark.parametrize("pregnancy_days", (1, 14, 90, 240, 285))
def test_pregnancy_suppresses_periods_and_fertile_phase_for_entire_cycle(girl, pregnancy_days):
    cycle, clock = cycle_runtime(girl, pregnancy_days)
    for day in range(28):
        clock["day"] = day
        state = cycle(girl)
        assert state == {"phase": "pregnant", "horny": 0.0, "critical": 0.0, "fertility": 0.0}


@pytest.mark.parametrize("girl", ("amanda", "melissa", "sandra", "liza", "georgett", "becky", "inga", "clara"))
def test_nonpregnant_cycle_keeps_existing_timing(girl):
    cycle, clock = cycle_runtime(girl, 0)
    phases = []
    for day in range(28):
        clock["day"] = day
        phases.append(cycle(girl)["phase"])
    assert phases.count("critical") == 3
    assert phases.count("fertile") == 6
    assert phases.count("restless") == 7
    assert phases.count("steady") == 12


def test_unregistered_person_has_no_cycle():
    cycle, _clock = cycle_runtime("amanda", 0)
    assert cycle("missing")["phase"] == "none"
