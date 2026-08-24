from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_dress_acceptance_is_local_to_each_interaction_label():
    amanda = read_rel("game/NPC/Girls/Amanda/IntAmandaDressChange.rpy")
    becky = read_rel("game/NPC/Girls/Becky/IntBeckyDressChange.rpy")
    liza = read_rel("game/NPC/Girls/Liza/IntLizaDressChange.rpy")
    gameplay = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    for label_name in (
        "IntAmandaDressChangeOfferBra",
        "IntAmandaDressChangeOfferPanties",
        "IntAmandaDressChangeShameBra",
        "IntAmandaDressChangeShamePanties",
    ):
        assert re.search(r"label %s\([^\n]*agreed_to_redress=0\)" % label_name, amanda)
    assert 'label IntBeckyDressChange(GirlName="becky", agreed_to_redress=0):' in becky
    assert 'label IntLizaDressChange(GirlNameILT="liza", agreed_to_redress=0):' in liza
    assert re.search(r"\bAgreedToRedress\b", gameplay) is None
    assert 'globals().pop("AgreedToRedress", None)' in read_rel("game/TractirSaveSync.rpy")


def test_becky_and_liza_own_their_custom_dress_reactions():
    becky_info = read_rel("game/NPC/Girls/Becky/InitBecky.rpy")
    becky_labels = read_rel("game/NPC/Girls/Becky/IntBeckyDressChange.rpy")
    becky_talk = read_rel("game/NPC/Girls/Becky/IntBeckyTalk.rpy")
    liza_info = read_rel("game/NPC/Girls/Liza/InitLiza.rpy")
    liza_labels = read_rel("game/NPC/Girls/Liza/IntLizaDressChange.rpy")

    assert "def dress_change_flags(self" in becky_info
    assert "def dress_change_has_options(self" in becky_info
    assert "def dress_change_other_saw_text(self" in becky_info
    assert "becky_dress_change_flags" not in becky_labels
    assert "becky_dress_change_has_options" not in becky_talk
    assert "becky_dress_change_other_saw_text" not in becky_labels
    assert "Becky.dress_change_flags(GirlName)" in becky_labels
    assert "Becky.dress_change_has_options(_becky_name)" in becky_talk
    assert "Becky.dress_change_other_saw_text" in becky_labels

    assert "def dress_change_other_saw_text(self" in liza_info
    assert "OtherSawLizaCode" not in liza_labels
    assert "Liza.dress_change_other_saw_text(agreed_to_redress)" in liza_labels
