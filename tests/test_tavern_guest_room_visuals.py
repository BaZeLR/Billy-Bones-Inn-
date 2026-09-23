"""Run the actual room picture selector; keep lighting separate from progression."""

from types import SimpleNamespace
import textwrap

import pytest

from tests.test_tavern_renovations_runtime import GAME, _exec_definitions


@pytest.mark.parametrize("hour", [0, 5, 6, 12, 17, 18, 23])
@pytest.mark.parametrize("view", ["lounge", "bedroom"])
@pytest.mark.parametrize("complete", [False, True])
@pytest.mark.parametrize("installed", [False, True])
@pytest.mark.parametrize("fire_lit", [False, True])
def test_guest_room_visual_obeys_completion_and_actual_hour(hour, view, complete, installed, fire_lit):
    namespace = {
        "calendar_v2": SimpleNamespace(hour=hour),
        "tavern": SimpleNamespace(renovation_complete=lambda code: complete),
        "rooms": {"TavernEmptyRoom": SimpleNamespace(bg_picture="bg amanda_room")},
        "Sofa": SimpleNamespace(installed=installed),
        "TavernGuestRoomStoveObject": object(),
        "_pc_fire_is_active": lambda obj: fire_lit,
    }
    _exec_definitions("Inn/TavernEmptyRoom.rpy", {"tavern_empty_room_picture"}, namespace)
    picture = namespace["tavern_empty_room_picture"](view)
    if not complete and not installed:
        assert picture == ("images/amanda/Room/emptyroom.jpg" if view == "bedroom" else "bg amanda_room")
    else:
        assert picture == "images/tavern/guest_room/%s_%s_%s.png" % (
            "sofa" if installed else "lounge", "day" if 6 <= hour < 18 else "night", "lit" if fire_lit else "cold",
        )
    if picture.startswith("images/"):
        assert (GAME / picture).is_file()


def test_entry_inspection_and_empty_peek_use_room_picture_owner():
    room = (GAME / "Inn/TavernEmptyRoom.rpy").read_text(encoding="utf-8-sig")
    renovation = (GAME / "Inn/TavernRenovations.rpy").read_text(encoding="utf-8-sig")
    assert "$ scene_runtime.picture = tavern_empty_room_picture()" in room
    assert 'vscene "guest_room_peek"' in room
    assert 'DynamicImage("[tavern_empty_room_picture(\'bedroom\')]")' in room
    assert 'elif _renovation.code == "guest_room":\n        vscene tavern_empty_room_picture()' in renovation


def test_sofa_portrait_is_owned_by_npc_data_and_used_by_talk():
    namespace = {
        "PeopleData": type("PeopleData", (), {"__init__": lambda self, name, **kwargs: self.__dict__.update(kwargs)}),
        "NPCScheduleEntry": lambda **kwargs: kwargs,
    }
    _exec_definitions("Inn/TavernCursedSofa.rpy", {"SofaData"}, namespace)
    data = namespace["SofaData"]()
    assert data.portrait == "images/tavern/guest_room/sofa_day_cold.png"
    assert data.schedule_entries == [{"location": "TavernEmptyRoom"}]
    assert (GAME / data.portrait).is_file()
    source = (GAME / "Inn/TavernCursedSofa.rpy").read_text(encoding="utf-8-sig")
    assert "vscene tavern_empty_room_picture()" in source


def test_guest_stove_uses_its_own_fire_state_not_the_hall():
    namespace = {
        "get_object_id": str,
        "TavernGuestRoomStoveObject": object(),
        "TavernMainFireplaceObject": object(),
        "TavernKitchenHearthObject": object(),
    }
    _exec_definitions("Inn/PlayerChoresSystem.rpy", {"_pc_fire_object"}, namespace)
    select = namespace["_pc_fire_object"]
    assert select("TavernEmptyRoom") is namespace["TavernGuestRoomStoveObject"]
    assert select("", "guest_room_stove_001") is namespace["TavernGuestRoomStoveObject"]
    assert select("TavernMain", "fireplace_001") is namespace["TavernMainFireplaceObject"]
    assert select("TavernKitchen", "kitchen_hearth_001") is namespace["TavernKitchenHearthObject"]


def test_peephole_frame_has_a_real_transparent_opening():
    from PIL import Image
    with Image.open(GAME / "images/tavern/guest_room/peephole_frame.png") as image:
        assert image.mode == "RGBA" and image.size == (1536, 1024)
        assert image.getpixel((768, 512))[3] == 0
        assert image.getpixel((10, 10))[3] > 200


@pytest.mark.parametrize("source,loadable,registered,errors", [
    ('"guest_room_peek"', False, True, []),
    ('"images/tavern/guest_room/sofa_day_cold.png"', True, False, []),
    ('"missing_image"', False, False, ["Unable to find missing_image"]),
    ('tavern_empty_room_picture()', False, False, []),
])
def test_vscene_lint_accepts_registered_images_but_reports_missing_assets(source, loadable, registered, errors):
    actual_errors = []
    namespace = {"renpy": SimpleNamespace(
        python=SimpleNamespace(py_eval=lambda expression: eval(expression, {})),
        loadable=lambda filename: loadable,
        has_image=lambda filename: registered,
        error=actual_errors.append,
    )}
    script = (GAME / "01vscene.rpy").read_text(encoding="utf-8-sig")
    function = "    def vscene_lint(obj):" + script.split("    def vscene_lint(obj):", 1)[1].split("    renpy.register_statement", 1)[0]
    exec(compile(textwrap.dedent(function), "01vscene.rpy", "exec"), namespace)
    namespace["vscene_lint"]((source, False))
    assert actual_errors == errors
