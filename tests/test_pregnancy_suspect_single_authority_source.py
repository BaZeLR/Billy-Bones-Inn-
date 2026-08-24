from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pregnancy_suspects_belong_to_the_npc():
    script = (ROOT / "game/script.rpy").read_text(encoding="utf-8-sig")
    source = (ROOT / "game/NPC/Girls/Common/ZaletOpinionCalc.rpy").read_text(encoding="utf-8-sig")
    kids = (ROOT / "game/Utilities/General/Sex/KidsFunctions.rpy").read_text(encoding="utf-8-sig")

    assert "ZaletSuspectFinal" not in script + source
    assert "PregTotalSuspects" not in script + source + kids
    assert 'state["pregnancy_suspects"]' in source
    assert "ZaletSuspectLinesCount(MomName)" in kids
