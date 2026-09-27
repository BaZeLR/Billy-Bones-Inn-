from pathlib import Path
import textwrap


MODEL = Path(__file__).resolve().parents[1] / "game/Utilities/General/NPC/GirlDecisionModel.rpy"


def choice_probability(mana, trust, friendship, legare, first_partner="", corruption=0):
    namespace = {}
    source = MODEL.read_text(encoding="utf-8-sig").split("init -34 python:", 1)[1]
    exec(textwrap.dedent(source), namespace)
    profile = {
        "girl": "amanda",
        "mana_value": mana,
        "amanda_trust": trust,
        "friend_value": friendship,
        "amanda_alberfriends": legare,
        "amanda_first_partner": first_partner,
        "sexual_openness_value": corruption,
    }
    return namespace["girl_decision_probabilities"]("amanda", "amanda_legare_choice", profile)["good"]


def test_mana_trust_and_friendship_each_raise_tavern_choice():
    baseline = choice_probability(20, 20, 4, 10)
    assert choice_probability(60, 20, 4, 10) > baseline
    assert choice_probability(20, 60, 4, 10) > baseline
    assert choice_probability(20, 20, 12, 10) > baseline
    assert choice_probability(20, 20, 4, 15) < baseline


def test_first_partner_is_a_bias_and_unknown_is_neutral():
    tied = choice_probability(50, 50, 10, 10)
    assert tied == 0.5
    assert choice_probability(50, 50, 10, 10, "mc") > tied
    assert choice_probability(50, 50, 10, 10, "legare") < tied
    assert choice_probability(50, 50, 10, 10, "unknown") == tied
    assert choice_probability(50, 50, 10, 10, corruption=100) == tied


def test_low_household_values_favor_other_branch():
    assert choice_probability(5, 5, 1, 10, "mc") < 0.5
