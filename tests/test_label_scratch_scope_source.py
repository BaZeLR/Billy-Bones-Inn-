from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_capitalized_event_scratch_is_dynamically_scoped():
    checks = {
        "game/Inn/TavernMain.rpy": ("GirlNameTS1", "GirlNameTS2"),
        "game/NPC/Girls/Amanda/AfterDanceLegare.rpy": ("AmandaNesluh", "AmandaArgue1", "AmandaArgue2", "Randvar", "AlberBribe"),
        "game/NPC/Girls/Amanda/AfterDanceSexLegare.rpy": ("AmandaLegareReactionRoll", "MaxStep"),
        "game/NPC/Girls/Becky/GeorgettBeckyVisit.rpy": ("BeckyGuestSexDesc", "KidsWatch"),
        "game/NPC/Girls/Common/MomDressComplaint.rpy": ("GirlSillyName", "TalkedBeforeTmp", "KidsOrPregTmp"),
    }

    for relative, names in checks.items():
        source = read(relative)
        for name in names:
            assert f'"{name}"' in source, (relative, name)
        assert "renpy.dynamic(" in source


def test_dead_dance_scratch_assignments_are_removed():
    becky_dance = read("game/NPC/Girls/Becky/IntBeckyDance.rpy")
    amanda_dance = read("game/NPC/Girls/Amanda/AmandaSexDanceStreet.rpy")

    assert "CounterToClean" not in becky_dance
    first_scene = amanda_dance.split("label AmandaSexDanceStreet:", 1)[0]
    assert "GirlNameASDS" not in first_scene
