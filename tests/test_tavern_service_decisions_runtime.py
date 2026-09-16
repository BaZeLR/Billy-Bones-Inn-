from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "game/Utilities/General/NPC/GirlDecisionModel.rpy"
RUNTIME = ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy"


class Worker:
    registry_group = "girl"

    def __init__(self, name, corruption):
        self.code_name = name
        self.rel = 10
        self.openness = 5
        self.corruption = corruption
        self.mana = 10
        self.rebellion = 0
        self.stats = {"PussyWetStart": 20, "sexacts": 1}
        self.var = {}
        self.reaction_state = {}

    def arousal_value(self):
        return 20

    def sex_stat(self, key, default=0):
        return self.stats.get(key, default)


def decision_model():
    # Exercise the real reward owner, not a second test implementation of mana.
    runtime = RUNTIME.read_text(encoding="utf-8-sig")
    start = runtime.index("        def change_mana(")
    end = runtime.index("        def harass_instruction(", start)
    reward_owner = {"people_to_int": lambda value, default=0: int(value)}
    exec(textwrap.dedent(runtime[start:end]), reward_owner)
    for method in ("change_mana", "mana_bad_probability", "reward_need_fulfilled"):
        setattr(Worker, method, reward_owner[method])

    workers = {"liza": Worker("liza", 35), "georgett": Worker("georgett", 80)}
    anger = {key: 0 for key in workers}
    issues = {key: "" for key in workers}
    namespace = {
        "people": SimpleNamespace(get_info=workers.get, location=lambda _key: "TavernMain"),
        "people_birth_date": lambda _key: {"day": 1},
        "current_game_day": lambda: 7,
        "calendar_v2": SimpleNamespace(week=7, hour=17, minute=0, time_slot=lambda: 3),
        "household": SimpleNamespace(
            barber_visit_last_day={}, barber_appointments={}, soap_request_last_day={}
        ),
        "crafting": SimpleNamespace(soap_requests={}),
        "player": SimpleNamespace(
            economy=SimpleNamespace(church_donated_today=0, church_donated_amount=0)
        ),
        "tavern_breakfast_player_perk_score": lambda _key: 0,
        "household_morning_issue_type": lambda key: issues[key],
        "relationship_anger": lambda key: anger[key],
    }
    source = MODEL.read_text(encoding="utf-8-sig").split("init -34 python:", 1)[1]
    exec(textwrap.dedent(source), namespace)
    return namespace, workers, anger, issues


@pytest.mark.parametrize("girl", ("liza", "georgett"))
def test_personal_premium_improves_only_recipient_service_decision(girl):
    model, workers, _anger, _issues = decision_model()
    probability = model["girl_decision_good_probability"]
    before = {key: probability(key, "tavern_service") for key in workers}
    other = next(key for key in workers if key != girl)

    workers[girl].reward_need_fulfilled(4, "personal_premium")

    assert workers[girl].mana == 14
    assert probability(girl, "tavern_service") > before[girl]
    assert probability(other, "tavern_service") == before[other]
    assert workers[girl].reaction_state["last_mana_reasons"] == ["personal_premium"]
    assert workers[girl].rel == 10
    assert girl not in model["GIRL_DECISION_PREFS"]


@pytest.mark.parametrize("girl", ("liza", "georgett"))
def test_service_morale_is_a_score_not_the_old_refusal_floor(girl):
    model, workers, _anger, _issues = decision_model()
    probabilities = model["girl_decision_probabilities"]
    service = probabilities(girl, "tavern_service")

    assert service["bad"] < 0.9
    assert service["good"] > 0.1
    sequence = []
    for morale in (0, 10, 25, 50, 75, 100):
        workers[girl].mana = morale
        sequence.append(model["girl_decision_good_probability"](girl, "tavern_service"))
    assert all(low < high for low, high in zip(sequence, sequence[1:]))


@pytest.mark.parametrize("girl", ("liza", "georgett"))
@pytest.mark.parametrize("action", ("favor", "intimate_help"))
def test_existing_professional_decisions_do_not_gain_the_household_refusal_floor(girl, action):
    model, workers, _anger, _issues = decision_model()
    profile = model["build_girl_decision_profile"](girl)
    assert profile["mana_value"] == workers[girl].mana
    assert profile["mana_bad_probability"] == pytest.approx(0.9)
    old_profile = dict(profile, mana_value=0, mana_bad_probability=0.0)
    probabilities = model["girl_decision_probabilities"]

    assert probabilities(girl, action, profile) == probabilities(girl, action, old_profile)
    assert probabilities(girl, action, profile)["bad"] < 0.9


@pytest.mark.parametrize("girl", ("amanda", "melissa", "sandra"))
@pytest.mark.parametrize("action", ("favor", "intimate_help"))
def test_existing_household_decisions_keep_their_morale_rule(girl, action):
    model, _workers, _anger, _issues = decision_model()
    profile = {"girl": girl, "trust": 0.5, "openness": 0.25, "mana_bad_probability": 0.9}
    result = model["girl_decision_probabilities"](girl, action, profile)

    assert result["bad"] == pytest.approx(0.9)
    assert result["good"] <= 0.1
    assert result["caprice"] == 0.0


@pytest.mark.parametrize("girl", ("liza", "georgett"))
def test_personal_corruption_gain_improves_only_recipient_service_decision(girl):
    model, workers, _anger, _issues = decision_model()
    probability = model["girl_decision_good_probability"]
    before = {key: probability(key, "tavern_service") for key in workers}
    other = next(key for key in workers if key != girl)

    workers[girl].corruption += 1

    assert probability(girl, "tavern_service") > before[girl]
    assert probability(other, "tavern_service") == before[other]
    assert workers[girl].mana == 10


@pytest.mark.parametrize("girl", ("liza", "georgett"))
def test_service_reads_personal_relationship_mood_and_unmet_needs(girl):
    model, workers, anger, issues = decision_model()
    probability = model["girl_decision_good_probability"]
    baseline = probability(girl, "tavern_service")
    workers[girl].rel = 15
    assert probability(girl, "tavern_service") > baseline
    workers[girl].rel = 10
    workers[girl].openness = 10
    assert probability(girl, "tavern_service") > baseline
    workers[girl].openness = 5
    anger[girl] = 3
    assert probability(girl, "tavern_service") < baseline
    anger[girl] = 0
    issues[girl] = "sick"
    assert probability(girl, "tavern_service") < baseline


@pytest.mark.parametrize(
    "relative_path,label,next_label",
    (
        ("Liza/IntLizaTalk.rpy", "IntLizaTalkHire", "IntLizaTalkGrope"),
        ("Georgett/IntGeorgettTalk.rpy", "IntGeorgettHire", "IntGeorgettGrope"),
    ),
)
def test_authored_paid_hire_does_not_consume_the_voluntary_service_score(
    relative_path, label, next_label
):
    source = (ROOT / "game/NPC/Girls" / relative_path).read_text(encoding="utf-8-sig")
    hire = source.split("label " + label + "(", 1)[1].split("label " + next_label + "(", 1)[0]

    assert "player.spend_money(4)" in hire
    assert "player.spend_money(8)" in hire
    assert "tavern_service" not in hire
    assert ".decide(" not in hire
