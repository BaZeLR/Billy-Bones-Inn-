from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_georgett_sex_session_uses_existing_character_and_scene_owners():
    source = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    info = (ROOT / "game/NPC/Girls/Georgett/InitGeorgett.rpy").read_text(encoding="utf-8-sig")
    runtime = (ROOT / "game/Utilities/General/Classes/ModuleRuntime.rpy").read_text(encoding="utf-8-sig")

    assert "module_runtime" not in source + runtime
    assert "def sex_location(self):" in info
    assert 'self.sex_state["location"]' in info
    assert "Georgett.sex_location()" in source
    assert "scene_runtime.picture = picture_path" in source
    assert "default module_runtime" not in runtime
    assert "class ModuleRuntimeState" not in runtime
    assert "label BeginPaidSexModule(" in runtime
    assert "label FinishPaidSexModule(" in runtime
    assert "return_room" not in source + runtime
    for legacy_name in ("GeorgettSexGirlName", "GeorgettSexGirlLoc", "GeorgettSexReturnRoom", "GeorgettSexPicturePath"):
        assert legacy_name not in source


def test_georgett_sex_has_no_legacy_save_authority():
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    for legacy_name in ("GeorgettSexGirlName", "GeorgettSexGirlLoc", "GeorgettSexReturnRoom", "GeorgettSexPicturePath"):
        assert legacy_name not in migration
    assert "tractir_save_migrate_module_runtime" not in migration
    assert 'globals().pop("module_runtime", None)' in migration
    assert 'globals().pop("GirlNameIGSS", None)' in migration
    assert 'globals().pop("GirlLocIGSS", None)' in migration


def test_georgett_sex_choices_use_native_choice_screen_without_apply_panel():
    source = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    menu_source = source.split("label GeorgettSexMenu:", 1)[1]
    assert "menu:" in menu_source
    assert '$ main_ui_runtime.mode = "event"' in menu_source
    assert '$ main_ui_runtime.selected_char = ""' in menu_source
    assert '$ main_ui_runtime.girl_key = ""' in menu_source
    assert '$ main_ui_runtime.talk_picture = ""' in menu_source
    assert "renpy.display_menu" not in menu_source
    assert "GeorgettSexApply" not in source
    assert "georgett_sex_action_panel" not in source
    assert "main_ui_runtime.action_items" not in source
    assert "georgett_sex_state_lines" not in source


def test_georgett_hire_uses_authored_paid_routes_and_one_time_owner():
    talk = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8-sig")
    sex = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    port = (ROOT / "game/Utilities/General/Sex/SexPort.rpy").read_text(encoding="utf-8-sig")
    tavern = (ROOT / "game/Utilities/General/Sex/SexProstTavern.rpy").read_text(encoding="utf-8-sig")

    hire = talk.split('label IntGeorgettHire(girl_name="georgett", girl_loc="street"):', 1)[1].split("label IntGeorgettGrope", 1)[0]
    assert 'call SexProstTavern(1, "georgett")' in hire
    assert 'call SexPort(1, "georgett")' in hire
    assert 'call IntGeorgettSex(' not in hire
    assert "main_ui_end_talk_state()" in hire
    assert "main_ui_begin_native_scene_state" in hire
    assert "main_ui_end_native_scene_state" in hire
    assert "GeorgettSexFinish" not in sex
    assert '"Закончить":\n                $ Georgett.set_sex_busy(0)\n                return' in sex
    assert 'label IntGeorgettSex(GirlNameIGSS="georgett", GirlLocIGSS="street", SceneTextIGSS=""):' in sex
    assert 'call IntGeorgettSex(GirlNameSP, "street", "Вы заплатили Жоржетте' in port
    assert 'call IntGeorgettSex(GirlNameSP, "tavern", "Вы заплатили Жоржетте' in tavern
    assert '\n        "Вы заплатили Жоржетте' not in port + tavern


def test_georgett_first_meeting_snapshots_room_before_writing_npc_scene():
    talk = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8-sig")
    first_talk = talk.split('label IntGeorgettTalk(girl_name="georgett", girl_loc=""):', 1)[1].split("while True:", 1)[0]

    assert first_talk.index('main_ui_begin_talk_state("Разговор с Жоржеттой", girl_name)') < first_talk.index('scene_runtime.text = "-Привет красавчик!')
    assert "Georgett.mark_known()" in first_talk


def test_georgett_free_grope_rejection_returns_to_talk_owner():
    talk = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8-sig")
    grope = talk.split('label IntGeorgettGrope(girl_name="georgett", girl_loc="street"):', 1)[1].split("label IntGeorgettAskDad", 1)[0]

    assert "def georgett_grope_outcome" not in talk
    assert "if Georgett.rel < 10:" in grope
    rejection = grope.split("if Georgett.rel < 10:", 1)[1].split("return", 1)[0]
    assert "ShowCurrentSex" not in rejection
    assert "Сначала заплати, а потом уже лапай!" in rejection
    assert "call ShowCurrentSex(girl_name)" in grope


def test_georgett_daily_limit_uses_player_authority_and_canonical_text():
    sex = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    talk = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8-sig")
    intimacy = (ROOT / "game/Utilities/General/Sex/PlayerIntimacyState.rpy").read_text(encoding="utf-8-sig")
    cock = (ROOT / "game/Utilities/General/Sex/ShowCurrentCockState.rpy").read_text(encoding="utf-8-sig")

    assert "if not player.intimacy.can_cum():" in sex + talk
    assert "PLAYER_DAILY_EXHAUSTION_TEXT" in sex + talk
    assert intimacy.count("То что упало - подняться не может.") == 1
    assert "[PLAYER_DAILY_EXHAUSTION_TEXT]" in cock
    assert "То что упало - подняться не может." not in sex + talk + cock


def test_georgett_uses_shared_girl_visibility_without_saved_or_method_mirrors():
    info_source = (ROOT / "game/NPC/Girls/Georgett/InitGeorgett.rpy").read_text(encoding="utf-8-sig")
    sex_source = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    portrait_source = (ROOT / "game/NPC/Girls/Georgett/ShowGeorgettPortrait.rpy").read_text(encoding="utf-8-sig")
    kids_source = (ROOT / "game/Utilities/General/Sex/KidsFunctions.rpy").read_text(encoding="utf-8-sig")

    assert 'def visible_tits(self):' not in info_source
    assert 'def visible_pussy(self):' not in info_source
    assert 'def has_top(self):' not in info_source
    assert 'def has_bottom(self):' not in info_source
    assert 'def top_is_raised(self):' not in info_source
    assert 'def bottom_is_raised(self):' not in info_source
    assert "Georgett.tits_visible()" in sex_source + portrait_source
    assert "Georgett.pussy_visible()" in sex_source + portrait_source
    assert "info.tits_visible()" in kids_source
    assert "info.visible_tits()" not in kids_source
    assert 'Georgett.clothing_layer("top")' in sex_source
    assert 'Georgett.clothing_layer("bottom")' in sex_source
    assert 'Georgett.layer_raised("top")' in sex_source
    assert 'Georgett.layer_raised("bottom")' in sex_source
    assert 'def refresh_sex_visibility(self):' not in info_source
    assert 'state["tits_visible"]' not in info_source
    assert 'state["pussy_visible"]' not in info_source
    assert "refresh_sex_visibility" not in sex_source + portrait_source
    assert "CurSperm0" not in portrait_source
    assert "CurSperm1" not in portrait_source
    assert "CurSperm2" not in portrait_source


def test_georgett_does_not_wrap_player_intimacy_or_shared_lick_counter():
    info_source = (ROOT / "game/NPC/Girls/Georgett/InitGeorgett.rpy").read_text(encoding="utf-8-sig")
    sex_source = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    talk_source = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8-sig")

    for method_name in (
        "_player_intimacy",
        "player_arousal",
        "set_player_arousal",
        "add_player_arousal",
        "can_player_cum",
        "add_lick_pussy",
        "orgasm_count_given",
        "had_sex_count",
    ):
        assert "def %s(" % method_name not in info_source
        assert "Georgett.%s(" % method_name not in sex_source + talk_source

    assert "player.intimacy.arousal_value()" in sex_source
    assert "player.intimacy.add_arousal(" in sex_source
    assert "player.intimacy.can_cum()" in sex_source + talk_source
    assert "Georgett.record_lick_pussy()" in sex_source


def test_georgett_church_continue_beats_do_not_write_dummy_state():
    church = (ROOT / "game/NPC/Girls/Georgett/InitGeorgettChurch.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "TmpChurchGeorgSex" not in church
    assert church.count('"Дальше":\n            pass') >= 5
