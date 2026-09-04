from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_georgett_sex_session_uses_existing_character_and_scene_owners():
    source = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    info = (ROOT / "game/NPC/Girls/Georgett/InitGeorgett.rpy").read_text(encoding="utf-8-sig")
    runtime = (ROOT / "game/Utilities/General/Classes/ModuleRuntime.rpy").read_text(encoding="utf-8-sig")
    shared = (ROOT / "game/Utilities/General/Sex/ShowCurrentSex.rpy").read_text(encoding="utf-8-sig")

    assert "module_runtime" not in source + runtime
    assert "def sex_location(self):" in info
    assert 'self.sex_state["location"]' in info
    assert "Georgett.sex_location()" in source
    assert "sex_scene_set_picture(" in source
    assert "scene_runtime.picture = picture_path" in shared
    assert "def georgett_sex_begin_text" not in source
    assert "def georgett_sex_add_text" not in source
    assert "def georgett_sex_set_picture" not in source
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
    events = (ROOT / "game/NPC/Girls/Georgett/GeorgettEvents.rpy").read_text(encoding="utf-8-sig")
    first_talk = talk.split('label IntGeorgettTalk(girl_name="georgett", girl_loc=""):', 1)[1].split("while True:", 1)[0]

    assert first_talk.index('main_ui_begin_talk_state("Разговор с Жоржеттой", girl_name)') < first_talk.index('call checkTriggers("talk_georgett", "intro", 0)')
    assert 'label story_georgett_portstreet_first_meet:' in events
    assert 'scene_runtime.text = "-Привет красавчик!' in events
    assert "Georgett.mark_known()" in events


def test_georgett_free_grope_rejection_returns_to_talk_owner():
    talk = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8-sig")
    grope = talk.split('label IntGeorgettGrope(girl_name="georgett", girl_loc="street"):', 1)[1].split("label IntGeorgettAskDad", 1)[0]

    assert "def georgett_grope_outcome" not in talk
    assert "if Georgett.rel < 10:" in grope
    rejection = grope.split("if Georgett.rel < 10:", 1)[1].split("return", 1)[0]
    assert "ShowCurrentSex" not in rejection
    assert "Сначала заплати, а потом уже лапай!" in rejection
    assert "call GeorgettSexStatus(girl_loc)" in grope
    assert "ShowCurrentSex" not in grope


def test_georgett_and_liza_share_scene_projection_without_state_mirrors():
    georgett = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    liza = (ROOT / "game/NPC/Girls/Liza/IntLizaSex.rpy").read_text(encoding="utf-8-sig")
    shared = (ROOT / "game/Utilities/General/Sex/ShowCurrentSex.rpy").read_text(encoding="utf-8-sig")

    for helper in ("sex_scene_begin_text", "sex_scene_add_text", "sex_scene_set_picture"):
        assert "def %s(" % helper in shared
        assert "def %s(" % helper not in georgett + liza
        assert "%s(" % helper in georgett
        assert "%s(" % helper in liza

    for source in (georgett, liza):
        assert 'main_ui_runtime.mode = "event"' in source
        assert 'main_ui_runtime.selected_char = ""' in source
        assert 'main_ui_runtime.girl_key = ""' in source
        assert 'main_ui_runtime.talk_picture = ""' in source
        assert "main_ui_runtime.action_items" not in source
        assert "MenuItem(" not in source


def test_liza_paid_sex_uses_native_scene_lifecycle_and_shared_state_owner():
    talk = (ROOT / "game/NPC/Girls/Liza/IntLizaTalk.rpy").read_text(encoding="utf-8-sig")
    sex = (ROOT / "game/NPC/Girls/Liza/IntLizaSex.rpy").read_text(encoding="utf-8-sig")
    port = (ROOT / "game/Utilities/General/Sex/SexPort.rpy").read_text(encoding="utf-8-sig")
    tavern = (ROOT / "game/Utilities/General/Sex/SexProstTavern.rpy").read_text(encoding="utf-8-sig")

    hire = talk.split('label IntLizaTalkHire(girl_name_ilt="liza", girl_loc_ilt=""):', 1)[1].split(
        "label IntLizaTalkGrope", 1
    )[0]
    assert "main_ui_end_talk_state()" in hire
    assert 'main_ui_begin_native_scene_state("Лизетта")' in hire
    assert "main_ui_end_native_scene_state()" in hire
    assert "if not player.intimacy.can_cum():" in hire
    assert "if not Liza.can_have_sex_today():" in hire
    assert "Liza.can_have_sex_today()" in talk.split("while True:", 1)[1].split("label IntLizaTalkSmalltalk", 1)[0]

    assert 'label IntLizaSex(GirlNameILSS="liza", GirlLocILSS="street", SceneTextILSS=""):' in sex
    assert "while True:" in sex
    assert "jump int_liza_sex_menu" not in sex
    assert sex.count("Liza.can_have_sex_today()") >= 6
    for target in ("mouth", "face", "tits", "inside"):
        assert 'Liza.player_cum("%s")' % target in sex
    assert "call PregnancyCheck" not in sex
    assert 'call IntLizaSex(GirlNameSP, "street", "Вы заплатили Лизетте' in port
    assert 'call IntLizaSex(GirlNameSP, "tavern", "Вы заплатили Лизетте' in tavern
    assert '\n        "Вы заплатили Лизетте' not in port + tavern


def test_liza_talk_choices_persist_and_refusal_keeps_talk_picture_owner():
    talk = (ROOT / "game/NPC/Girls/Liza/IntLizaTalk.rpy").read_text(encoding="utf-8-sig")
    menu = talk.split('label IntLizaTalk(girl_name_ilt="liza", girl_loc_ilt=""):', 1)[1].split(
        "label IntLizaTalkSmalltalk", 1
    )[0]
    grope = talk.split('label IntLizaTalkGrope(girl_name_ilt="liza", girl_loc_ilt=""):', 1)[1].split(
        "label IntLizaTalkAskDad", 1
    )[0]

    assert "while True:" in menu
    assert '"Закончить разговор":' in menu
    assert "main_ui_end_talk_state()" in menu
    assert 'Liza.can_ask_topic("pregnancy")' in menu
    smalltalk = talk.split('label IntLizaTalkSmalltalk(girl_name_ilt="liza", girl_loc_ilt="", _liza_busy_text=""):', 1)[1].split(
        "label IntLizaTalkAskClients", 1
    )[0]
    assert 'key="procedural:NPC/Girls/Liza/IntLizaTalk.rpy:smalltalk:%s" % Liza.talk_count()' in smalltalk
    rejection = grope.split("if Liza.rel < 5:", 1)[1].split("return", 1)[0]
    assert "ShowCurrentSex" not in rejection
    assert "call LizaSexStatus(girl_loc_ilt)" in grope


def test_georgett_daily_limit_uses_player_authority_and_canonical_text():
    sex = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    talk = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettTalk.rpy").read_text(encoding="utf-8-sig")
    intimacy = (ROOT / "game/Utilities/General/Sex/PlayerIntimacyState.rpy").read_text(encoding="utf-8-sig")
    cock = (ROOT / "game/Utilities/General/Sex/ShowCurrentCockState.rpy").read_text(encoding="utf-8-sig")

    assert "if not player.intimacy.can_cum():" in sex + talk
    assert "and Georgett.can_have_sex_today():" in talk
    assert "if not Georgett.can_have_sex_today():" in talk
    assert sex.count("Georgett.can_have_sex_today()") >= 7
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


def test_georgett_owns_the_friendship_reward_for_every_orgasm():
    info_source = (ROOT / "game/NPC/Girls/Georgett/InitGeorgett.rpy").read_text(encoding="utf-8-sig")
    sex_source = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    shared_source = (ROOT / "game/Utilities/General/Sex/ShowCurrentSex.rpy").read_text(encoding="utf-8-sig")
    people_source = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")

    assert "ORGASM_FRIENDSHIP_GAIN = 1" in info_source
    assert "def record_orgasm_given(self):" not in info_source
    orgasm_owner = people_source.split("def record_orgasm_given(self):", 1)[1].split("def record_sex_history", 1)[0]
    assert 'getattr(self, "ORGASM_FRIENDSHIP_GAIN", 0)' in orgasm_owner
    assert "self.change_social(friend_delta=friendship_gain)" in orgasm_owner
    georgett_custom_branch = sex_source.split("if _georgett_orgasm_count == 2:", 1)[1].split(
        'if Georgett.cock_in("pussy")', 1
    )[0]
    assert "add_relation" not in georgett_custom_branch
    georgett_shared_branch = shared_source.split('if _scs_key == "georgett"', 1)[1].split(
        'if _scs_key == "liza"', 1
    )[0]
    assert "change_social" not in georgett_shared_branch


def test_georgett_and_liza_friendship_rewards_are_class_values_with_one_owner():
    georgett_info = (ROOT / "game/NPC/Girls/Georgett/InitGeorgett.rpy").read_text(encoding="utf-8-sig")
    liza_info = (ROOT / "game/NPC/Girls/Liza/InitLiza.rpy").read_text(encoding="utf-8-sig")
    georgett_sex = (ROOT / "game/NPC/Girls/Georgett/IntGeorgettSex.rpy").read_text(encoding="utf-8-sig")
    liza_sex = (ROOT / "game/NPC/Girls/Liza/IntLizaSex.rpy").read_text(encoding="utf-8-sig")
    shared_status = (ROOT / "game/Utilities/General/Sex/ShowCurrentSex.rpy").read_text(encoding="utf-8-sig")
    people = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")

    assert "LICK_FRIENDSHIP_MILESTONES = {4: 1}" in georgett_info
    assert "LICK_FRIENDSHIP_MILESTONES = {7: 1}" in liza_info
    assert "ORGASM_FRIENDSHIP_GAIN = 1" in liza_info
    assert "ORGASM_FRIENDSHIP_MILESTONES" not in liza_info

    orgasm_owner = people.split("def record_orgasm_given(self):", 1)[1].split("def record_sex_history", 1)[0]
    lick_owner = people.split("def record_lick_pussy(self):", 1)[1].split("def lick_pussy_count", 1)[0]
    assert "ORGASM_FRIENDSHIP_MILESTONES" in orgasm_owner
    assert "LICK_FRIENDSHIP_MILESTONES" in lick_owner
    assert "self.change_social(friend_delta=friendship_gain)" in orgasm_owner
    assert "self.change_social(friend_delta=friendship_gain)" in lick_owner

    georgett_lick_text = georgett_sex.split("if _georgett_lick_count == 4:", 1)[1].split(
        "$ Georgett.add_arousal", 1
    )[0]
    liza_lick_text = liza_sex.split("if _liza_licks == 7:", 1)[1].split(
        "$ Liza.add_arousal", 1
    )[0]
    liza_orgasm_text = liza_sex.split("if _liza_orgasm_count == 3:", 1)[1].split(
        'if Liza.cock_in("pussy")', 1
    )[0]
    shared_liza_orgasm_text = shared_status.split('if _scs_key == "liza"', 1)[1].split(
        'if _scs_key == "becky"', 1
    )[0]
    for presentation_only in (georgett_lick_text, liza_lick_text, liza_orgasm_text, shared_liza_orgasm_text):
        assert "change_social" not in presentation_only
        assert "add_relation" not in presentation_only


def test_georgett_church_continue_beats_do_not_write_dummy_state():
    church = (ROOT / "game/NPC/Girls/Georgett/InitGeorgettChurch.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "TmpChurchGeorgSex" not in church
    assert church.count('"Дальше":\n            pass') >= 5
