import ast
from pathlib import Path
import textwrap
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SUGGEST = ROOT / "game/NPC/Girls/Common/GirlDressSuggest.rpy"
SHOP = ROOT / "game/Town/Arts/Dress/DressShop.rpy"
CLOTHES = ROOT / "game/Items/Clothes/InitDressDesc.rpy"


class Wardrobe:
    def __init__(self, *dress_codes):
        self.owned_items = list(dress_codes)

    def owns(self, dress_code):
        return dress_code in self.owned_items


def dress_rules():
    namespace = {}
    clothes_source = CLOTHES.read_text(encoding="utf-8-sig").split("init python:\n", 1)[1].split("\nlabel InitDressDesc:", 1)[0]
    exec(compile(ast.parse(textwrap.dedent(clothes_source)), str(CLOTHES), "exec"), namespace)
    suggest_source = SUGGEST.read_text(encoding="utf-8-sig").split("init python:\n", 1)[1].split("\nlabel GirlDressSuggest", 1)[0]
    function_names = {
        "_gds_dress_top_bottom_slut",
        "_gds_peer_owns_dress",
        "_gds_interested_in_dress",
        "_gds_dress_objection",
        "_gds_has_new_acceptable_dress",
    }
    nodes = [node for node in ast.parse(textwrap.dedent(suggest_source)).body if isinstance(node, ast.FunctionDef) and node.name in function_names]
    assert {node.name for node in nodes} == function_names
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SUGGEST), "exec"), namespace)

    girls = {}
    team = {"sandra", "melissa", "amanda"}
    namespace["people"] = SimpleNamespace(get_info=girls.get, girl_items=lambda: list(girls.items()))
    namespace["tavern"] = SimpleNamespace(is_team_member=lambda girl: girl in team)
    namespace["household"] = SimpleNamespace(outfit_requests={})
    namespace["threads"] = {
        "sandraRevealingDressInitiative": SimpleNamespace(completed=False),
        "melissaRevealingDressRequest": SimpleNamespace(completed=False),
        "amandaRevealingDressRequest": SimpleNamespace(completed=False),
    }

    def add_girl(name, corruption, *dress_codes):
        girls[name] = SimpleNamespace(
            corruption=corruption,
            wardrobe=Wardrobe(*dress_codes),
            revealing_dress_code="",
            data=SimpleNamespace(base_clothing={"day_dress": dress_codes[0] if dress_codes else ""}),
        )
        return girls[name]

    return SimpleNamespace(namespace=namespace, girls=girls, add_girl=add_girl)


def test_corruption_thresholds_control_new_dresses():
    game = dress_rules()
    amanda = game.add_girl("amanda", 0, "modestworkdress")
    objection = game.namespace["_gds_dress_objection"]
    has_offer = game.namespace["_gds_has_new_acceptable_dress"]

    assert not has_offer("amanda")
    assert objection("amanda", "workdress") == "top_open"
    amanda.corruption = 10
    assert objection("amanda", "modestnicedress") == ""
    assert has_offer("amanda")
    amanda.corruption = 20
    assert objection("amanda", "workdress") == ""
    assert objection("amanda", "minidress") == "bottom_short"
    amanda.corruption = 35
    assert objection("amanda", "minidress") == ""
    assert objection("amanda", "slutdress") == "top_extreme"
    amanda.corruption = 55
    assert objection("amanda", "slutdress") == ""


def test_request_allows_one_step_but_not_every_dress():
    game = dress_rules()
    game.add_girl("amanda", 0, "modestworkdress")
    objection = game.namespace["_gds_dress_objection"]

    game.namespace["household"].outfit_requests["amanda"] = "surprise"
    assert objection("amanda", "modestnicedress") == ""
    assert objection("amanda", "workdress") == "top_open"
    assert objection("amanda", "slutdress") == "top_extreme"

    game.namespace["household"].outfit_requests.clear()
    game.namespace["threads"]["amandaRevealingDressRequest"].completed = True
    assert objection("amanda", "modestnicedress") == ""
    game.girls["amanda"].revealing_dress_code = "minidress"
    assert objection("amanda", "modestnicedress") == "top_bold"


def test_exact_team_dress_creates_precedent_but_outsider_dress_does_not():
    game = dress_rules()
    game.add_girl("amanda", 0, "modestworkdress")
    game.add_girl("becky", 70, "slutdress")
    objection = game.namespace["_gds_dress_objection"]

    assert objection("amanda", "slutdress") == "top_extreme"
    melissa = game.add_girl("melissa", 0, "workdress")
    assert objection("amanda", "workdress") == "top_open"  # Starter clothing is not a purchase.
    melissa.data.base_clothing["day_dress"] = "modestworkdress"
    assert objection("amanda", "workdress") == ""
    assert objection("becky", "workdress") != ""
    sandra = game.add_girl("sandra", 0, "slutdress")
    sandra.data.base_clothing["day_dress"] = "workdresszhilet"
    assert objection("amanda", "slutdress") == ""
    game.girls["amanda"].wardrobe.owned_items.append("slutdress")
    assert objection("amanda", "slutdress") == "owned"


def test_tailor_buttons_and_shop_share_dress_willingness():
    catalog = SHOP.read_text(encoding="utf-8-sig")
    buying = (ROOT / "game/NPC/Girls/Common/GirlDressBuy.rpy").read_text(encoding="utf-8-sig")
    assert '_dress_objection = _gds_dress_objection(_girl_name, _dress_code)' in catalog
    assert 'if _girl_name and not _dress_objection:' in catalog
    assert catalog.index('if _girl_name and not _dress_objection:') < catalog.index('textbutton "Выбрать":')
    assert 'if not _gds_dress_objection(GirlName, dress_shop_item_code(item))' in buying

    gates = (
        "game/Utilities/General/NPC/PeopleRuntime.rpy",
        "game/NPC/Girls/Sandra/IntSandraDressChange.rpy",
        "game/NPC/Girls/Melissa/IntMelissaTalk.rpy",
        "game/NPC/Girls/Amanda/InitAmanda.rpy",
        "game/NPC/Girls/Amanda/IntAmandaDressChange.rpy",
        "game/NPC/Girls/Becky/InitBecky.rpy",
        "game/NPC/Girls/Georgett/IntGeorgettDressChange.rpy",
        "game/NPC/Girls/Liza/IntLizaDressChange.rpy",
    )
    for path in gates:
        assert "_gds_has_new_acceptable_dress(" in (ROOT / path).read_text(encoding="utf-8-sig"), path
