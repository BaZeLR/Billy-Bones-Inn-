from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_amanda_sex_actions_keep_authored_text_picture_and_native_menu():
    source = read("game/NPC/Girls/Amanda/IntAmandaSex.rpy")

    assert 'main_ui_begin_native_scene_state("Аманда")' in source
    assert 'scene_runtime.text = "\\n\\n".join' in source
    assert "vscene scene_runtime.picture" in source
    assert '"Кончить в ротик" if' in source
    assert '"Закончить":\n                    $ _ias_scene_active = False' in source


def test_reaching_full_arousal_waits_for_an_explicit_finish_choice():
    source = read("game/Utilities/General/Sex/ShowCurrentCockState.rpy")
    ready_branch = source.split("elif cur_arousal < 100:", 1)[1].split("else:", 1)[1].split("else:", 1)[0]

    assert "Вы готовы кончить и можете выбрать, как закончить." in ready_branch
    assert "player_record_orgasm" not in ready_branch


def test_amanda_home_flow_does_not_inject_generic_description_after_sex():
    source = read("game/NPC/Girls/Amanda/AmandaAtHomeCode.rpy")
    scene = source.split("label CodeAmandaSexScene:", 1)[1].split("label CodeAmandaSexPush:", 1)[0]

    assert 'call IntAmandaSex("amanda", "home"' in scene
    assert 'call GirlsDesc("amanda")' not in scene
