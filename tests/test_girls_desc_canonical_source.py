from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_girl_descriptions_use_registry_ids_without_name_aliases():
    source = (ROOT / "game/NPC/Girls/Common/GirlsDesc.rpy").read_text(encoding="utf-8-sig")

    assert "def _girls_desc_alias_name(" not in source
    assert "aliases = {" not in source
    assert "return people_normalize_id(girl_name)" in source
    for retired_alias in ("georgette", "lizette", "lizzette", "francesca", "franchesca", "francheska", "clarisse"):
        assert '"%s"' % retired_alias not in source
