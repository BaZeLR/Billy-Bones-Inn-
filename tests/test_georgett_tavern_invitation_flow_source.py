from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GEORGETT_TALK = ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy"


def test_georgett_departure_has_its_own_room_return_choice():
    source = GEORGETT_TALK.read_text(encoding="utf-8-sig")
    block = source.split("label IntGeorgettTellLizaGerhard", 1)[1].split(
        "label IntGeorgettInviteTavern", 1
    )[0]
    departure = block.split("\n        return", 1)[0]

    assert "с этими словами она удаляется" in departure
    assert 'menu:\n            "На портовые улицы" if girl_loc == "street":' in departure
    assert '"Вернуться в трактир" if girl_loc == "tavern":' in departure
    assert departure.index("menu:") < departure.index("main_ui_end_talk_state()")
    assert departure.count('Georgett.mark_asked_topic("TalkChurchAfterCermonLiza")') == 1
    assert departure.count("Georgett.finish_talk()") == 1
    assert "jump PortStreets" not in block
    assert "rooms.enter(" not in block

    repeat = block.split("\n        return", 1)[1]
    assert "main_ui_end_talk_state()" not in repeat
    assert "menu:" not in repeat


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
