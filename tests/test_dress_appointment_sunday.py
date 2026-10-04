import ast
from pathlib import Path
import textwrap


SOURCE = Path(__file__).resolve().parents[1] / "game/Utilities/General/Common/CheckDailyEvent.rpy"


def daily_runtime():
    body = SOURCE.read_text(encoding="utf-8-sig").split("init -25 python:\n", 1)[1].split("\ndefault daily_events", 1)[0]
    tree = ast.parse(textwrap.dedent(body))
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "DailyEventRuntime")
    namespace = {
        "_daily_int": lambda value, default=0: int(value),
        "procedural_randint": lambda low, high, key="": low,
    }
    exec(compile(ast.Module(body=[cls], type_ignores=[]), str(SOURCE), "exec"), namespace)
    return namespace["DailyEventRuntime"]()


def test_saturday_dress_appointment_waits_until_monday():
    daily = daily_runtime()
    daily.add("melissa", "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")

    daily.end_day(6)
    assert daily.exists("melissa", "BuyDressTom")
    assert not daily.exists("melissa", "BuyDress")

    daily.end_day(7)
    assert not daily.exists("melissa", "BuyDressTom")
    assert daily.exists("melissa", "BuyDress")


def test_weekday_dress_appointment_remains_next_morning():
    daily = daily_runtime()
    daily.add("melissa", "dressshop", 0, "=", 1, 1, "BuyDressTom", "GirlDressBuy", "girl_location")

    daily.end_day(3)
    assert not daily.exists("melissa", "BuyDressTom")
    assert daily.exists("melissa", "BuyDress")
