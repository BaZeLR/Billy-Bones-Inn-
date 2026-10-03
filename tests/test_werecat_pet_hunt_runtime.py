from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]


def namespace():
    class BaseNPC:
        def __init__(self, name):
            self.name = name
            self.var = {}

        def display_name(self):
            return self.name

    ns = {"BaseNPC": BaseNPC}
    owner = (ROOT / "game/NPC/Secondary/WerecatNPC.rpy").read_text(encoding="utf-8-sig")
    code = owner.split("init -8 python:\n", 1)[1].split("    WERECAT_MILK_ITEM_IDS", 1)[0]
    exec(textwrap.dedent(code), ns)
    ns["werecat"] = ns["WerecatInfo"]()
    ns["werecat_hunt"] = ns["WerecatHuntState"]()
    ns.update({
        "rooms": SimpleNamespace(current_code="Forest"),
        "Melissa": SimpleNamespace(storage_rat_help_day=0),
        "people_to_int": lambda value, default=0: default if value is None else int(value),
        "current_game_day": lambda: 35,
        "day_delta_ready": lambda day, delay: 35 - day >= delay,
        "player": SimpleNamespace(tavern_management=SimpleNamespace(breakfast=SimpleNamespace(today=False))),
    })
    quest = (ROOT / "game/NPC/Secondary/MelissaWerecatQuest.rpy").read_text(encoding="utf-8-sig")
    code = quest.split("init -1 python:\n", 1)[1].split("\n\nlabel WerecatSetTrap", 1)[0]
    exec(textwrap.dedent(code).replace("import renpy.exports as renpy", ""), ns)
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    code = "    def updateSave_V110():" + migration.split("    def updateSave_V110():", 1)[1].split("    # Saved objects", 1)[0]
    ns["WerecatStaticData"] = SimpleNamespace(invalidate_daily_schedule=lambda: None)
    ns["people"] = SimpleNamespace(register=lambda data, pet: None)
    ns["initThreads"] = lambda: None
    exec(textwrap.dedent(code), ns)
    return ns


@pytest.mark.parametrize("owned", [False, True])
def test_sales_and_gifting_do_not_block_further_catches_or_remove_pet(owned):
    ns = namespace()
    pet = ns["werecat"]
    pet.owned = owned
    pet.pet_name = "Луна"
    hunt = ns["werecat_state"]()
    hunt.update(sold_count=12, gifted_clara=1, hunter_tease_day=0)
    assert ns["werecat_can_search"]("Forest")
    assert ns["werecat_is_living_with_household"]() == owned
    assert pet.pet_name == "Луна"
    hunt["caught"] = 1
    assert not ns["werecat_can_search"]("Forest")
    hunt["caught"] = 0
    assert ns["werecat_can_search"]("Forest")


@pytest.mark.parametrize("adopted,sold", [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_migration_preserves_adoption_separately_from_sales(adopted, sold):
    ns = namespace()
    pet = ns["werecat"]
    for field in ("owned", "pet_name", "adopted_day", "adoption_breakfast_seen", "first_month_thanks_day"):
        delattr(pet, field)
    pet.var = {"adopted": adopted, "adopted_count": adopted, "sold": sold,
        "name": "Луна", "adopted_day": 0, "adoption_breakfast_seen": 1,
        "first_month_thanks_day": -1, "gifted_clara": 1, "trap_rooms": {"Forest": {"day": 12}}}
    pet.stats.update(trust=13, comfort=15, milk_day=34)
    ns["updateSave_V110"]()
    assert pet.owned == bool(adopted)
    assert pet.pet_name == "Луна" and pet.adopted_day == 0
    assert pet.adoption_breakfast_seen and pet.first_month_thanks_day == -1
    assert pet.stats["trust"] == 13 and pet.stats["comfort"] == 15
    assert pet.stats["milk_day"] == 34
    hunt = ns["werecat_state"]()
    assert hunt["sold_count"] == sold and hunt["gifted_clara"] == 1
    assert hunt["trap_rooms"] == {"Forest": {"day": 12}}
    assert pet.var == {}
    assert not {"adopted", "adopted_count", "sold", "name", "adopted_day"}.intersection(hunt)
    before = dict(hunt), dict(pet.stats), pet.pet_name, pet.owned
    ns["updateSave_V110"]()
    assert before == (dict(hunt), dict(pet.stats), pet.pet_name, pet.owned)
    assert ns["werecat_month_thanks_ready"]() == bool(adopted)


def test_pending_pet_breakfast_uses_adoption_day_zero():
    ns = namespace()
    ns["werecat"].owned = True
    ns["werecat"].adopted_day = 0
    assert ns["werecat_adoption_breakfast_ready"]()
    ns["werecat"].adoption_breakfast_seen = True
    assert not ns["werecat_adoption_breakfast_ready"]()


def test_pet_and_hunt_defaults_do_not_share_state():
    ns = namespace()
    pet, hunt = ns["werecat"], ns["werecat_state"]()
    assert not pet.owned and pet.pet_name == "Луна"
    assert pet.var == {}
    assert hunt["sold_count"] == 0 and hunt["caught"] == 0
    assert not {"adopted", "sold", "name", "adopted_day", "trust", "comfort"}.intersection(hunt)
