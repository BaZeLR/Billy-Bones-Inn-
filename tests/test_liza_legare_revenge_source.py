from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy"
POST = ROOT / "game/NPC/Girls/Clara/ClaraPostResolutionThreads.rpy"
LIZA_TALK = ROOT / "game/NPC/Girls/Liza/IntLizaTalk.rpy"


def source(path):
    return path.read_text(encoding="utf-8-sig")


def test_liza_talk_owns_revenge_opening_after_clarissa_moves_in():
    runtime = source(RUNTIME)
    opening = runtime.split('"story_clara_legare_revenge_request_1"', 1)[1].split(
        '"story_clara_legare_revenge_fight_2"', 1
    )[0]
    talk = source(LIZA_TALK)
    scene = source(POST).split("label story_clara_legare_revenge_request_1:", 1)[1].split(
        "\nlabel ", 1
    )[0]

    assert "#Clara.tavern_resident()" in opening
    assert "#room_in_group(str(people.location('liza') or ''), ROOM_GROUP_TAVERN)" in opening
    assert "#int(Liza.rel or 0) >= 5" in opening
    assert '"talk_liza"' in opening
    assert '"legare_revenge"' in opening
    assert 'story_event_available("talk_liza", "legare_revenge")' in talk
    assert 'call checkTriggers("talk_liza", "legare_revenge", 0)' in talk
    assert "Клиент да клиент и жарит неплохо" in scene
    assert "ответственное поручение" in scene
    assert "event_runtime.active_thread.advance()" in scene


def test_wine_store_fight_waits_for_pauline_route_even_on_old_saves():
    runtime = source(RUNTIME)
    fight = runtime.split('"story_clara_legare_revenge_fight_2"', 1)[1].split(
        "], highlight=False, threaded=True)", 1
    )[0]

    assert '"#False"' in fight
    assert '"talk_pauline"' in fight
    assert '"legare_revenge_continuation"' in fight
    assert '"WineStore",\n            "enter"' not in fight
