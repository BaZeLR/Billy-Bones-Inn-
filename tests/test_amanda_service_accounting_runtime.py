from pathlib import Path
import textwrap


SOURCE = Path(__file__).resolve().parents[1] / "game/Inn/TavernRenovations.rpy"


class AmandaState:
    def __init__(self, reconciled=False):
        self.reconciled = reconciled

    def var_value(self, key, default=None):
        return {
            "legare_choice_outcome": "service",
            "legare_service_reconciled": self.reconciled,
        }.get(key, default)


def tavern_with_amanda(reconciled=False):
    source = SOURCE.read_text(encoding="utf-8-sig").split("init -30 python:", 1)[1]
    source = source.split("default tavern = TavernInfo()", 1)[0]
    amanda = AmandaState(reconciled)

    class PeopleRegistry:
        def get_info(self, key):
            return amanda if key == "amanda" else None

    namespace = {"TAVERN_RENOVATIONS": {}, "people": PeopleRegistry()}
    exec(textwrap.dedent(source), namespace)
    return namespace["TavernInfo"]()


def test_amanda_service_rates_do_not_change_other_workers():
    tavern = tavern_with_amanda()
    assert tavern.service_terms("amanda", "intimate") == {"price": 300, "house_percent": 60}
    assert tavern.service_terms("amanda", "gloryhole") == {"price": 20, "house_percent": 60}
    assert tavern.service_house_revenue("amanda", "intimate", 2) == 360
    assert tavern.service_worker_revenue("amanda", "intimate", 2) == 240
    assert tavern.service_house_revenue("amanda", "gloryhole", 2) == 24
    assert tavern.service_worker_revenue("amanda", "gloryhole", 2) == 16
    assert tavern.service_house_revenue("liza", "intimate", 2) == 6
    assert tavern.service_house_revenue("georgett", "gloryhole", 2) == 4


def test_amanda_service_rates_stop_after_reconciliation():
    tavern = tavern_with_amanda(reconciled=True)
    assert tavern.service_terms("amanda", "intimate") is None
    assert tavern.service_house_revenue("amanda", "intimate", 2) == 6
    assert tavern.service_worker_revenue("amanda", "intimate", 2) == 0
