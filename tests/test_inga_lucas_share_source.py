from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONT = (ROOT / "game/Town/BeckyHomeFront.rpy").read_text(encoding="utf-8-sig")
SCENE = (ROOT / "game/NPC/Girls/Inga/IngaLucasShare.rpy").read_text(encoding="utf-8-sig")
RUNTIME = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")


def test_inga_thread_owns_progress_and_uses_existing_prerequisites():
    inga_threads = RUNTIME.split("define ingaThreadList = [", 1)[1].split(
        "define eddieThreadList = [", 1
    )[0]
    thread = inga_threads.split('LThreadData(0, "inga", "LucasShare"', 1)[1]

    assert "threads['beckyIngaLucasPath'].completed" in thread
    assert "Inga.acquaintance_stage" in thread
    assert "threads['beckyDinner'].num" in thread
    assert '"story_inga_lucas_share_0"' in thread
    assert '"BeckyHomeFront"' in thread
    assert '"inga_lucas_share"' in thread
    assert "player.intimacy.can_cum()" in thread
    assert "Inga.can_have_sex_today()" in thread
    assert "Inga.sex_busy()" in thread
    assert "beckyIngaLucasPath.advance" not in thread


def test_homefront_exposes_only_the_thread_owned_share_action():
    approach = FRONT.split("label becky_homefront_approach:", 1)[1].split("# --- END OF LOCATION ---", 1)[0]
    assert approach.count('story_event_available("BeckyHomeFront", "inga_lucas_share")') == 1
    assert approach.count('call checkTriggers("BeckyHomeFront", "inga_lucas_share", 0)') == 1
    assert "ingaLucasShare" not in approach


def test_inga_owns_the_share_scene_and_pregnancy_capable_finish():
    assert "label story_inga_lucas_share_0:" in SCENE
    assert 'main_ui_begin_native_scene_state("Инга и Лукас")' in SCENE
    assert SCENE.count('images/inga/StreetSex/fuckyou') >= 4
    assert 'Inga.set_cock_position("pussy")' in SCENE
    assert 'Inga.player_cum("inside")' in SCENE
    assert "event_runtime.active_thread.advance()" in SCENE
    assert "LucasInfo" not in SCENE
    assert "default " not in SCENE
