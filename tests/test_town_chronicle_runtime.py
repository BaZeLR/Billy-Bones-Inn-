import ast
from pathlib import Path
import textwrap
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
TOWN_SOURCE = (ROOT / "game/Town/RandomTownEvents.rpy").read_text(encoding="utf-8-sig")


def _runtime(hook, hour=9, week=2, wash_days=0, reputation=20):
    selections = []

    def choose(rows, key=""):
        if isinstance(rows[0], dict) and "text" in rows[0]:
            entry = next(row for row in rows if hook in row["hooks"])
            selections.append(entry)
            return entry
        return rows[0]

    scope = {
        "procedural_choice": choose,
        "procedural_random": lambda **kwargs: 1.0,
        "RandomNameCode": lambda **kwargs: "Петер",
        "RandomStreetNameCode": lambda: "кожевенников",
        "RandomStallionNameCode": lambda: "Бурый",
    }
    player_source = (ROOT / "game/Utilities/General/Player/Player.rpy").read_text(encoding="utf-8-sig")
    player_tree = ast.parse(textwrap.dedent(player_source.split("init -998 python:", 1)[1].split("\ndefault player", 1)[0]))
    names = {"player_to_int", "player_clamp_value", "PlayerAppearance", "PlayerStats"}
    owners = ast.Module(body=[node for node in player_tree.body if getattr(node, "name", "") in names], type_ignores=[])
    exec(compile(owners, "<player owners>", "exec"), scope)
    exec(textwrap.dedent(TOWN_SOURCE.split("init -20 python:", 1)[1].split("\ndefault TownStreet", 1)[0]), scope)

    appearance = scope["PlayerAppearance"]()
    appearance.days_since_wash = wash_days
    stats = scope["PlayerStats"]()
    stats.reputation = reputation
    player = SimpleNamespace(appearance=appearance, stats=stats)
    player.change_stat = stats.change
    calendar = SimpleNamespace(
        hour=hour, week=week, daysInGame=7,
        clock_minutes=lambda: hour * 60,
        time_slot=lambda: 0 if hour < 12 else 2 if hour < 18 else 3 if hour < 22 else 4,
    )
    scope.update(
        player=player,
        calendar_v2=calendar,
        rooms=SimpleNamespace(current_code="StreetTavern"),
        renpy=SimpleNamespace(dynamic=lambda *names: None),
        main_ui_begin_native_scene_state=lambda title: None,
        scene_runtime=SimpleNamespace(picture="", text="", location_text=""),
    )
    scope["TownStreet"] = scope["TownStreetRuntime"]()
    return scope, selections


def _run_native_event_prelude(scope):
    body = TOWN_SOURCE.split("label TownRandomChronicleEvent:", 1)[1].split("\n    menu:", 1)[0]
    lines = []
    for line in textwrap.dedent(body).splitlines():
        stripped = line.lstrip()
        indent = line[:len(line) - len(stripped)]
        if stripped.startswith("$ "):
            lines.append(indent + stripped[2:])
        elif stripped.startswith("if "):
            lines.append(line)
    exec("\n".join(lines), scope)


@pytest.mark.parametrize(
    "hook,hour,penalty,image",
    [
        ("window_waste", 9, 3, "window_waste_mishap.png"),
        ("bird_droppings", 14, 1, "bird_droppings_mishap.png"),
    ],
)
@pytest.mark.parametrize("wash_days", [0, 2])
def test_mishaps_bind_the_selected_image_and_apply_consequences_once(hook, hour, penalty, image, wash_days):
    scope, selections = _runtime(hook, hour=hour, wash_days=wash_days)
    _run_native_event_prelude(scope)
    player = scope["player"]
    scene = scope["scene_runtime"]

    assert len(selections) == 1
    assert player.appearance.days_since_wash == wash_days + penalty
    assert player.stats.reputation == 19
    assert player.appearance.dress_life_days == {"villagedress": player.appearance.DRESS_LIFE_DAYS}
    assert scene.picture == "images/town stories/" + image
    assert (ROOT / "game" / scene.picture).is_file()
    assert scene.text == scene.location_text
    assert "[улица]" not in scene.text
    assert "Репутация -1." in scene.text
    assert scope["TownStreet"].events_today == 1
    assert not scope["TownStreet"].interactive_allowed("StreetTavern")
    player.appearance.wash()
    assert player.appearance.days_since_wash == 0
    assert player.stats.reputation == 19


@pytest.mark.parametrize("hook,hour", [("window_waste", 9), ("bird_droppings", 14)])
def test_mishap_reputation_penalty_keeps_the_existing_zero_floor(hook, hour):
    scope, _ = _runtime(hook, hour=hour, reputation=0)
    _run_native_event_prelude(scope)
    assert scope["player"].stats.reputation == 0


def test_chronicle_selection_does_not_apply_player_penalties_itself():
    scope, selections = _runtime("window_waste")
    chronicle = scope["TownStreet"].random_chronicle("morning")
    assert len(selections) == 1
    assert chronicle["wash_days"] == 3
    assert chronicle["reputation"] == -1
    assert scope["player"].appearance.days_since_wash == 0
    assert scope["player"].stats.reputation == 20


def test_market_story_uses_its_picture_and_maravedi_without_player_penalties():
    scope, selections = _runtime("market_day", hour=21, week=6)
    _run_native_event_prelude(scope)
    assert len(selections) == 1
    assert scope["scene_runtime"].picture == "images/town stories/market_day_witch_bounty.png"
    assert "50 мараведи" in scope["scene_runtime"].text
    assert "50 золотых" not in scope["scene_runtime"].text
    assert scope["player"].appearance.days_since_wash == 0
    assert scope["player"].stats.reputation == 20


@pytest.mark.parametrize(
    "hook,hour,image",
    [
        ("bounty", 9, "images/general/LocMarketPlace1.jpg"),
        ("bandits", 19, "images/general/harbor_street.png"),
        ("horse", 23, "images/general/harbor_street.png"),
    ],
)
def test_unillustrated_stories_keep_their_existing_backgrounds_and_player_state(hook, hour, image):
    scope, selections = _runtime(hook, hour=hour)
    _run_native_event_prelude(scope)
    assert len(selections) == 1
    assert scope["scene_runtime"].picture == image
    assert scope["scene_runtime"].text
    assert scope["player"].appearance.days_since_wash == 0
    assert scope["player"].stats.reputation == 20
