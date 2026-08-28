from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOG = (ROOT / "game/NPC/Secondary/DogCompanion.rpy").read_text(encoding="utf-8-sig")
WERECAT = (ROOT / "game/NPC/Secondary/WerecatNPC.rpy").read_text(encoding="utf-8-sig")


def test_dog_talk_uses_native_menu_without_dispatcher():
    assert "label IntDogTalkRefresh" not in DOG
    assert "IntDogTalkRefresh" not in DOG
    assert "def dog_main_ui_action_items" not in DOG
    assert "label IntDogTalkApply" not in DOG
    menu_source = DOG.split('label IntDogTalk(room_code=""):', 1)[1].split("label DogTrainingMenu", 1)[0]
    assert "label IntDogTalkMenu:" not in DOG
    assert "jump IntDogTalkMenu" not in DOG
    assert "while True:" in menu_source
    assert "menu:" in menu_source
    assert '"[scene_runtime.text]"' not in menu_source
    assert "show screen main_ui" not in menu_source
    for caption in ("Позвать пса", "Попробовать погладить", "Попробовать поиграть", "Взять пса на охоту", "Оставить сторожить дом"):
        assert f'"{caption}"' in menu_source
    assert "main_ui_end_talk_state()" in menu_source


def test_dog_card_and_adoption_choices_stay_inside_main_ui():
    card_source = DOG.split('label ShowDogCard(return_label=""):', 1)[1].split('label IntDogTalk(room_code=""):', 1)[0]
    adopt_source = DOG.split('label IntDogAdoptNameMenu(room_code=""):', 1)[1].split("label DogTrainingMenu", 1)[0]

    assert 'main_ui_runtime.mode = "dog"' in card_source
    assert "menu:" in card_source
    assert '"[scene_runtime.text]"' not in card_source
    assert "label HideDogCard" not in DOG
    assert "show screen main_ui" not in adopt_source
    assert "$ scene_runtime.text =" in adopt_source
    assert "menu:" in adopt_source


def test_werecat_talk_uses_native_menu_without_dispatcher():
    assert "def werecat_talk_action_items" not in WERECAT
    assert "label IntWerecatTalkApply" not in WERECAT
    assert "label IntWerecatTalkRefresh" not in WERECAT
    assert "IntWerecatTalkRefresh" not in WERECAT
    menu_source = WERECAT.split('label IntWerecatTalk(room_code=""):', 1)[1].split("label ShowWerecatCard", 1)[0]
    assert "label IntWerecatTalkMenu:" not in WERECAT
    assert "jump IntWerecatTalkMenu" not in WERECAT
    assert "while True:" in menu_source
    assert "menu:" in menu_source
    for caption in ("Погладить кошку", "Дать молока", "Поиграть с кошкой", "Понаблюдать за кошкой", "Поиграть с кошкой и псом"):
        assert f'"{caption}"' in menu_source
    assert "main_ui_end_talk_state()" in menu_source
