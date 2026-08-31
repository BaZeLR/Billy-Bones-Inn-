from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_child_records_have_one_player_history_authority():
    kids = source("game/Utilities/General/Sex/KidsFunctions.rpy")
    stat = source("game/Utilities/General/Screens/stat.rpy")
    georgett = source("game/NPC/Girls/Georgett/IntGeorgettTalk.rpy")

    assert 'runtime.history.setdefault("kids", {})' in kids
    assert 'state.setdefault("list", [])' in kids
    assert 'state.setdefault("next_id", 1)' in kids
    assert 'mom_info.set_sex_stat("kids"' in kids
    assert "return GetKidData(KidId)[\"KidName\"]" in kids
    assert "return len(_kids_list())" in stat
    assert 'kids_count_for_mothers("georgett", "liza")' in georgett


def test_kids_runtime_has_no_qsp_scratch_or_parallel_child_maps():
    runtime = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    kids = source("game/Utilities/General/Sex/KidsFunctions.rpy")

    for retired in (
        "_kids_get",
        "_kids_set",
        "_kids_result",
        "ProstitutesKids",
        "store.KidID",
        "store.KidDescription",
    ):
        assert retired not in runtime
    assert '"scratch"' not in kids
    assert "default KidsList" not in runtime
    assert "default kids =" not in runtime


def test_birth_consequences_write_real_owners_directly():
    kids = source("game/Utilities/General/Sex/KidsFunctions.rpy")
    finish = source("game/Town/Temple/GiveBirthFinish.rpy")

    assert "player.economy.add_child_support(1)" in kids
    assert "player.tavern_management.household_members =" in kids
    assert "$ kid_id = CreateKid(girl_name)" in finish
    assert "$ newborn = GetKidData(kid_id)" in finish
    assert 'renpy.dynamic("real_name", "real_name3", "kid_id"' in finish
    assert "except Exception" not in finish
    assert "if kid_id:" not in finish


def test_kids_and_lactation_text_stays_in_owning_room_or_story_label():
    kids = source("game/Utilities/General/Sex/KidsFunctions.rpy")
    tavern = source("game/Inn/TavernMain.rpy")
    becky_talk = source("game/NPC/Girls/Becky/IntBeckyTalk.rpy")
    current_sex = source("game/Utilities/General/Sex/ShowCurrentSex.rpy")

    assert "renpy.say(" not in kids
    assert 'return "\\n".join(lines)' in kids
    assert 'scene_runtime.location_text += "\\n\\n" + "\\n\\n".join(_tavern_kids_description)' in tavern
    assert 'scene_runtime.text += "\\n\\n" + _grocery_breastfeeding_text' in becky_talk
    assert '"[_scs_kids_peek_text]"' in current_sex
