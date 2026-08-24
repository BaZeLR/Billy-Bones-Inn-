from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


TALK_FILES = (
    "game/NPC/Girls/Amanda/IntAmandaTalk.rpy",
    "game/NPC/Girls/Clara/IntClaraTalk.rpy",
    "game/NPC/Girls/Melissa/IntMelissaTalk.rpy",
    "game/NPC/Girls/Sandra/IntSandraTalk.rpy",
    "game/NPC/Secondary/IntDraupnirTalk.rpy",
    "game/NPC/Secondary/IntMongolTalk.rpy",
)


def test_talk_exits_restore_the_caller_ui_without_reentering_rooms():
    for relative_path in TALK_FILES:
        source = (ROOT / relative_path).read_text(encoding="utf-8-sig")
        assert "main_ui_end_talk_state" in source, relative_path
        assert "jump expression str(CurLoc" not in source, relative_path

    draupnir = (ROOT / TALK_FILES[4]).read_text(encoding="utf-8-sig")
    mongol = (ROOT / TALK_FILES[5]).read_text(encoding="utf-8-sig")
    assert 'main_ui_begin_talk_state("Разговор с Драупниром", "draupnir")' in draupnir
    assert 'main_ui_begin_talk_state("Разговор с Монголом", "mongol")' in mongol
    assert 'Jump("MarketPlace")' not in mongol.split("label ClaraSecretMerchantMenu:", 1)[0]


def test_mongol_horse_purchase_keeps_the_qsp_stable_destination():
    mongol = (ROOT / TALK_FILES[5]).read_text(encoding="utf-8-sig")

    purchase_exits = re.findall(
        r"player\.horse\.acquire\([^\n]+\).*?\$ main_ui_end_talk_state\(\)\s+jump TavernStable",
        mongol,
        flags=re.DOTALL,
    )
    assert len(purchase_exits) == 2
    assert mongol.count("jump TavernStable") == 2
