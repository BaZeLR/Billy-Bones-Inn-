from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Town/Temple/GiveBirth.rpy"
STEP_SOURCE = ROOT / "game/Town/Temple/GiveBirthStep2.rpy"
PRAYER_SOURCE = ROOT / "game/Town/Temple/EllonaBirthPrayMenu.rpy"
FINISH_SOURCE = ROOT / "game/Town/Temple/GiveBirthFinish.rpy"


def test_give_birth_keeps_authored_label_flow_and_uses_system_apis_directly():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert 'label GiveBirth(GirlName=""):' in source
    assert "label give_birth_menu:" in source
    assert source.count("\n        menu:\n") >= 2
    assert "RandomNameCode(" in source
    assert "GetSexNum(" in source
    assert "slut_friends_increase(" in source
    assert "if not Sandra.knows_molodost:" in source
    assert "$ Sandra.knows_molodost = True" in source
    assert 'Sandra.var.get("knowmolodost"' not in source


def test_give_birth_has_no_local_api_wrappers_or_hidden_fallbacks():
    source = SOURCE.read_text(encoding="utf-8-sig")

    for wrapper in (
        "_strcomp",
        "_sfi",
        "_corruption",
        "_random_name",
        "_get_sex_num",
        "_mama_molodost_heard",
    ):
        assert wrapper not in source
    assert "except NameError" not in source
    assert "except Exception" not in source
    assert "renpy.say(" not in source


def test_birth_labor_progress_is_local_and_passed_directly_between_labels():
    give_birth = SOURCE.read_text(encoding="utf-8-sig")
    step = STEP_SOURCE.read_text(encoding="utf-8-sig")
    prayer = PRAYER_SOURCE.read_text(encoding="utf-8-sig")
    finish = FINISH_SOURCE.read_text(encoding="utf-8-sig")
    active_source = give_birth + step + prayer + finish

    assert 'label GiveBirthStep2(girl_name="", daddy_suspect_1="", daddy_suspect_2="", give_birth_timer=0):' in step
    assert "while True:" in step
    assert "$ give_birth_timer += 1" in step
    assert "if give_birth_timer > 3:" in step
    assert "call GiveBirthFinish(girl_name)" in step
    assert "call EllonaBirthPrayMenu(girl_name)" in step
    assert "$ give_birth_timer += int(_return or 0)" in step
    assert "return 2" in prayer
    assert "jump GiveBirthStep2" not in active_source
    assert "jump EllonaBirthPrayMenu" not in active_source
    assert "GiveBirthTimer" not in active_source


def test_birth_scene_scratch_is_not_persistent_game_state():
    give_birth = SOURCE.read_text(encoding="utf-8-sig")
    finish = FINISH_SOURCE.read_text(encoding="utf-8-sig")
    active_source = give_birth + finish

    assert 'renpy.dynamic("daddy_suspect_1", "daddy_suspect_2"' in give_birth
    assert 'renpy.dynamic("real_name", "real_name3", "kid_id"' in finish
    assert "DaddySuspect1" not in active_source
    assert "DaddySuspect2" not in active_source
    for legacy_name in ("KidID", "KidDescription", "KidName", "KidGender"):
        assert f"$ {legacy_name} =" not in active_source
        assert f"[{legacy_name}]" not in active_source
