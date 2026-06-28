from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_mongol_has_own_data_info_and_var_owner():
    source = read_rel("game/NPC/Secondary/InitMongol.rpy")

    assert "class MongolData(PeopleData):" in source
    assert "class MongolInfo(BaseNPC):" in source
    assert "define MongolStaticData = MongolData()" in source
    assert "default Mongol = MongolInfo()" in source
    assert "self.var = {}" in source
    assert "def ensure_story_defaults(self):" in source
    assert "def is_market_visible(self):" in source


def test_mongol_uses_class_state_not_old_var_bridge():
    combined = "\n".join(
        [
            read_rel("game/NPC/Secondary/InitMongol.rpy"),
            read_rel("game/NPC/Secondary/IntMongolTalk.rpy"),
            read_rel("game/Town/Market/MarketPlace.rpy"),
            read_rel("game/Inn/TavernStable.rpy"),
            read_rel("game/Utilities/Time/NextDay_NewDayEvents.rpy"),
        ]
    )

    assert "MongolVar" not in combined
    assert "Mongol.var =" not in combined
    assert 'getattr(renpy.store, "Mongol.var"' not in combined
    assert "getattr(renpy.store, 'Mongol.var'" not in combined
    assert '_ensure_dict("Mongol.var")' not in combined
    assert '"var": Mongol.var' not in combined
    assert "Mongol(var=" not in combined
    assert "MongolInfo(var=" not in combined


def test_mongol_market_flow_uses_class_methods():
    source = read_rel("game/Town/Market/MarketPlace.rpy")

    assert "return bool(Mongol.is_market_visible())" in source
    assert "Mongol.reset_market_trade()" in source
    assert 'Mongol.var_int("HorsePrice", 1000)' in source
