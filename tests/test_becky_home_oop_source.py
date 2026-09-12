from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "game/Town/BeckyHome.rpy").read_text(encoding="utf-8-sig")
OBJECTS = (ROOT / "game/Town/BeckyHomeObjects.rpy").read_text(encoding="utf-8-sig")
HOME_FRONT = (ROOT / "game/Town/BeckyHomeFront.rpy").read_text(encoding="utf-8-sig")
DINNER = (ROOT / "game/NPC/Girls/Becky/IntBeckyGuest.rpy").read_text(encoding="utf-8-sig")
GEORGETT_VISIT = (ROOT / "game/NPC/Girls/Becky/GeorgettBeckyVisit.rpy").read_text(encoding="utf-8-sig")


def test_becky_home_has_no_active_boolean_or_restore_builder_wrappers():
    assert "BeckyHomeActive" not in SOURCE
    assert "label BeckyHomeBuildActions:" not in SOURCE
    assert "label BeckyHomeRestore:" not in SOURCE
    assert "label BeckyHomeReturnFromObject:" not in SOURCE
    assert "call BeckyHomeBuildActions" not in SOURCE
    assert "call BeckyHomeRestore" not in SOURCE
    assert "def becky_home_action_items():" not in SOURCE


def test_becky_home_preserves_arrival_story_without_invented_objects():
    for mode in ("FromDances", "FromDinner", "SvalnyiGreh"):
        assert mode in SOURCE
    for object_id in ("becky_home_bed", "becky_home_chests", "becky_home_dinner_table"):
        assert object_id not in SOURCE
    assert "GameObject(" not in OBJECTS
    assert "call IntEddieBeckySex" in SOURCE
    assert 'call checkTriggers("BeckyHome", "enter", 0)' in SOURCE
    assert "call IntBeckyGuest" in SOURCE
    assert "call IntBeckySex(GirlName)" in SOURCE
    assert "call IntBeckySex(GirlName)\n        jump BeckyHomeAfterSex" in SOURCE
    assert 'threads["beckyHome"].advanceTo(2, force_active=True)' in SOURCE
    assert 'rooms.get("BeckyHome").build_exit_items()' in SOURCE
    assert "label BeckyHomeObjectMenu" not in SOURCE
    assert "label BeckyHomeObjectText" not in SOURCE


def test_becky_home_is_not_closed_before_its_evening_story_event():
    room_definition = SOURCE.split("BeckyHomeRoomDefinition = Room(", 1)[1].split("label BeckyHome", 1)[0]

    assert "schedule=" not in room_definition
    assert "game_items=[]" in room_definition
    assert '"object_menu_label"' not in room_definition
    assert "<br>" not in SOURCE


def test_becky_dinner_owns_event_ui_until_an_authored_exit():
    assert '$ main_ui_begin_native_scene_state("Ужин у Бекки")' in DINNER
    assert "if dinnertime > 6" not in DINNER
    assert '"Попрощаться и идти домой" if dinnertime > 5' in DINNER
    assert '$ calendar_v2.advance_minutes(60)\n                $ main_ui_end_native_scene_state()\n                jump MarketPlace' in DINNER
    assert DINNER.count("$ main_ui_end_native_scene_state()") == 5
    assert '$ main_ui_begin_native_scene_state("Дом Бекки")' in SOURCE


def test_becky_dinner_preserves_qsp_picture_and_social_rules():
    entry = DINNER.split("label IntBeckyGuest:", 1)[1].split("while True:", 1)[0]
    assert "DinnerStart.jpg" not in entry
    assert '$ get_girl_drunk("becky")' in DINNER
    assert '$ get_girl_drunk("inga")' in DINNER
    assert '$ slut_friends_increase("eddie", 5, 1, -1, 0, 0, 0)' in DINNER
    assert '$ slut_friends_increase("eddie", 5, 2, -1, 0, 0, 0)' in DINNER
    assert '$ slut_friends_increase("eddie", 5, 5, -1, 0, 0, 0)' in DINNER
    assert "Eddie.change_social(friend_delta=-1)" not in DINNER
    assert "call ShowImage('becky', 'dinner', 'DinnerInga')" in SOURCE
    assert SOURCE.index("Итак, вы сидите за столом") < SOURCE.index("call IntBeckyGuest")


def test_becky_invited_homefront_has_only_original_event_choices_and_knowledge_write():
    first_menu = HOME_FRONT.split("menu:", 1)[1].split("# --- SUBLABELS", 1)[0]
    assert '"Вернуться на рынок"' not in first_menu
    peek = HOME_FRONT.split("label becky_homefront_peek:", 1)[1].split("label becky_homefront_share_with_becky:", 1)[0]
    assert "Inga.saw_lucas_sex = True" not in peek
    assert "Inga.acquaintance_stage = max" not in peek
    share = HOME_FRONT.split("label becky_homefront_share_with_becky:", 1)[1].split("label becky_homefront_ignore:", 1)[0]
    assert "Inga.saw_lucas_sex = True" in share
    assert "Inga.acquaintance_stage = max" in share


def test_georgett_dinner_watcher_text_stays_with_chosen_result():
    setup = GEORGETT_VISIT.split("$ KidsWatch =", 1)[1].split("while georgedinnersex > 0:", 1)[0]
    assert '$ BeckyGuestSexDesc += "Вдруг вы заметили' in setup
    assert '\n        "Вдруг вы заметили' not in setup
    assert "$ georgedinnersex = 0\n                        $ main_ui_end_native_scene_state()\n                        jump MarketPlace" in GEORGETT_VISIT
