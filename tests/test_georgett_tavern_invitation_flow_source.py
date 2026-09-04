from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GEORGETT_TALK = ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy"


def test_successful_georgett_job_proposal_plays_before_next_day_report():
    source = GEORGETT_TALK.read_text(encoding="utf-8-sig")
    block = source.split("label IntGeorgettInviteTavern", 1)[1].split(
        "label IntGeorgettAskWork", 1
    )[0]

    rendered_text = block.index('"[scene_runtime.text]"')
    return_action = block.index('"Вернуться в трактир":')
    next_day = block.index('call NextDay("TavernMain", 1)')

    assert rendered_text < return_action < next_day
    assert "menu:" in block[rendered_text:return_action]
    assert "Sandra.set_job_value" not in block
    assert "Melissa.set_job_value" not in block
    assert "Amanda.set_job_value" not in block
