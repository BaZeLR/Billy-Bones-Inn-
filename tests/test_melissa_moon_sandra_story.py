from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "game/NPC/Girls/Melissa/MelissaMoonNoise.rpy").read_text(encoding="utf-8-sig")


def test_sandra_tells_the_complete_stove_spirit_legend():
    scene = SOURCE.split("label story_melissa_moon_sandra_story_3:", 1)[1].split(
        "label story_melissa_moon_old_stove_4:", 1
    )[0]

    assert 'Amanda.sex_stat("virginity", True)' in scene
    assert 'Clara.sex_stat("virginity", True)' in scene
    assert "ровно в полночь" in scene
    assert "три раза сказать" in scene
    assert "Олли, Олли" in scene
    assert "печному окошку" in scene
    assert "мягкая мохнатая рука" in scene
    assert "Вспомнить старую печь в сарае" in scene
