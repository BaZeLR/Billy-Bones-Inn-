"""Checks scoped to the authored upstairs branch and its existing owners."""
import ast
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/NPC/Girls/Amanda/AmandaLegareStreetEvents.rpy"
USER_PARAGRAPHS = [
    "you decided to wait a liltle bit and when follows Amanda upstares to her room.",
    "Aamanda ,already in her neglege runs into you trembling with passion, and kisses you pationately .",
    "then she stops and goes toward second bed, which is empty. smailes misteriously .",
    "she slowly removes her last cloth giggling...and quickly hydes her lower body under blanket,,,",
    "like what you see, maister?",
    "You came claose and stand near bed,...",
    "Amanda removes her blanket ... make it quick how ever I want you to make me come,,,",
    "you enter her hot and wet shell which trebling with desires... deep moan is coming out of Amanda oohhh  I am cummining come inside me ,master gimme all your sweet skunk feel me with love..."
]
ASSETS = ["close up.jpg", "onbed.jpg", "Boobs.png", "onbedCloseUp.jpg", "beforeSex.jpg"]

def event():
    return SOURCE.read_text(encoding="utf-8-sig").split("label story_amanda_legare_tavern_visit_0:", 1)[0]

def test_supplied_wording_preserved_in_authored_order():
    text = event()
    strings = [ast.literal_eval(match) for match in re.findall(r'scene_runtime.text = ("[^"\\]*(?:\\.[^"\\]*)*")', text)]
    indices = [strings.index(paragraph) for paragraph in USER_PARAGRAPHS]
    assert indices == sorted(indices)
    assert all(strings.count(paragraph) == 1 for paragraph in USER_PARAGRAPHS)

def test_one_half_probability_roll_and_no_new_story_owner():
    text = event()
    assert text.count('procedural_random("amanda_tavern_seduction_bedroom") < 0.5') == 1
    assert text.index('"Позвать наверх" if') < text.index('procedural_random("amanda_tavern_seduction_bedroom")')
    assert text.count("label ") == 1
    assert "default " not in text
    assert "QueuePagedPanelText" not in text
    assert "current_action_items" not in text
    assert "jump TavernAmandaRoom" not in text

def test_assets_exist_in_sequence_and_original_is_preserved():
    text = event()
    paths = ["images/amanda/Room/flirtUpstares/" + name for name in ASSETS]
    indices = [text.index('vscene "' + path + '"') for path in paths]
    assert indices == sorted(indices)
    for path in paths:
        assert (ROOT / "game" / path).is_file()
    original = ROOT / "game/NPC/Girls/Amanda/flirts_new room.jpg"
    copy = ROOT / "game/images/amanda/Room/flirtUpstares/flirts_new room.jpg"
    assert hashlib.sha256(original.read_bytes()).digest() == hashlib.sha256(copy.read_bytes()).digest()

def test_common_finishing_remains_single_owned_path():
    text = event()
    assert text.count('call BeginPaidSexModule("amanda", "TavernAmandaRoom")') == 1
    assert text.count('call FinishPaidSexModule("amanda", "TavernAmandaRoom")') == 1
    assert text.count("Amanda.record_orgasm_given()") == 1
    assert text.count('Amanda.player_cum("inside")') == 1
    assert text.count('Amanda.player_cum("outside")') == 1
    assert 'Amanda.wear_night_clothes(0)' in text
    assert 'Amanda.wear_night_clothes(2)' in text
    assert text.count('"Далее":') == 8
    assert '"Завершить":' in text
    assert 'main_ui_end_native_scene_state()' in text
