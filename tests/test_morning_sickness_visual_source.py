import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CHARACTER_ASSETS = {
    "amanda": ("Amanda", "images/amanda/morning_sickness/amanda_morning_sickness.png"),
    "georgett": ("Georgett", "images/georgett/morning_sickness/georgett_morning_sickness.png"),
    "sandra": ("Sandra", "images/sandra/morning_sickness/sandra_morning_sickness.png"),
    "melissa": ("Melissa", "images/melissa/morning_sickness/melissa_morning_sickness.png"),
    "liza": ("Liza", "images/Liza/morning_sickness/liza_morning_sickness.png"),
}


def test_each_requested_npc_owns_one_morning_sickness_picture():
    for _girl, (source_dir, relative_asset) in CHARACTER_ASSETS.items():
        source = (ROOT / "game/NPC/Girls" / source_dir / ("Init%s.rpy" % source_dir)).read_text(
            encoding="utf-8-sig"
        )
        assert '"morning": {' in source
        assert '"sickness": ["%s"]' % relative_asset in source


def test_morning_sickness_event_reads_the_npc_manifest_and_restores_its_cg():
    source = (ROOT / "game/NPC/Girls/Common/MorningSickness.rpy").read_text(encoding="utf-8-sig")
    label = source.split("label MorningSickness(girl_name):", 1)[1].split(
        "label morning_sickness_step2", 1
    )[0]

    assert "girl_data = people.get_data(girl_name)" in label
    assert 'girl_data.image_path("morning", "sickness")' in label
    assert label.count("vscene morning_sickness_picture") == 2
    assert '$ scene_runtime.text = ""' in label
    assert '$ scene_runtime.location_text = ""' in label
    assert "images/" not in label


def test_morning_sickness_assets_are_landscape_game_cgs():
    for _girl, (_source_dir, relative_asset) in CHARACTER_ASSETS.items():
        asset = ROOT / "game" / relative_asset
        data = asset.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", data[16:24])
        assert (width, height) == (1536, 1024)
