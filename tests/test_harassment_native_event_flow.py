from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "game/NPC/Girls/Common/EventWaitressHarrass.rpy",
    ROOT / "game/NPC/Girls/Common/EventWaitressHarrassPart2.rpy",
    ROOT / "game/NPC/Girls/Common/EventCleaningHarrass.rpy",
    ROOT / "game/NPC/Girls/Common/EventCleaningHarrassPart2.rpy",
    ROOT / "game/Utilities/General/NPC/PartEventAfterHarrassment.rpy",
    ROOT / "game/NPC/Girls/Common/IntHarrassmentDiscuss.rpy",
]
REACTION = ROOT / "game/Utilities/General/NPC/PartEventYourFirstReaction.rpy"
GIRL_REACTION = ROOT / "game/NPC/Girls/Common/PartEventGirlHarrassmentReaction.rpy"
CUSTOMER_REACTION = ROOT / "game/Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy"
SAVE_SYNC = ROOT / "game/TractirSaveSync.rpy"


def test_witnessed_harassment_uses_native_label_menus_without_panel_dispatch():
    source = "\n".join(path.read_text(encoding="utf-8-sig") for path in FILES)
    reaction = REACTION.read_text(encoding="utf-8-sig")
    reaction_flow = reaction[reaction.index("label PartEventYourFirstReaction(") :]

    for forbidden in (
        "main_ui_runtime.action_items",
        "MenuItem(",
        "queue_paged_panel_text",
        "ReturnToMainUI",
        "PartEventYourFirstReactionShow",
        "PartEventYourFirstReactionApply",
        "IntHarrassmentDiscussApply",
        "_reaction_menu",
        "_discussion_menu",
    ):
        assert forbidden not in source
        assert forbidden not in reaction_flow

    assert 'label PartEventYourFirstReactionOutcome(' in reaction_flow
    assert 'label IntHarrassmentDiscussOutcome(' in source
    assert reaction_flow.count("\n    menu:\n") >= 1
    assert source.count("\n    menu:\n") >= 2


def test_harassment_event_state_is_passed_between_returnable_labels():
    source = "\n".join(path.read_text(encoding="utf-8-sig") for path in FILES)
    reaction = GIRL_REACTION.read_text(encoding="utf-8-sig")
    customer = CUSTOMER_REACTION.read_text(encoding="utf-8-sig")

    assert "return (result, girl_run_away, girl_slapped)" in reaction
    assert "your_reaction1 == 3" in reaction
    assert "YourReaction1" not in reaction
    assert "GirlRunAway" not in reaction
    assert "GirlSlapped" not in reaction
    assert "label PartEventCustomerHarrassmentReaction(GirlNamePECHR, girl_run_away=0, girl_slapped=0" in customer
    assert "GirlRunAway" not in customer
    assert "GirlSlapped" not in customer
    assert "_girl_reaction_text, girl_run_away, girl_slapped = _return" in source
    assert 'pass (GirlNamePEYFR, Eyewitness, reaction_code, HarassType, _player_reaction_text)' in REACTION.read_text(encoding="utf-8-sig")
    assert "_event_text=cur_event_desc_part2" in source
    assert "PartEventCustomerHarrassmentReaction(girl_name, girl_run_away, girl_slapped)" in source
    for retired in ("CurEventDescPart2", "$ HarassType =", "$ Eyewitness =", "$ YourReaction1 ="):
        assert retired not in source

    migration = SAVE_SYNC.read_text(encoding="utf-8-sig")
    for retired in ("CurEventDescPart2", "GirlRunAway", "GirlSlapped", "HarassType", "Eyewitness"):
        assert '"%s"' % retired in migration


def test_harassment_render_and_discussion_scratch_is_label_local():
    amanda_data = (ROOT / "game/NPC/Girls/Amanda/InitAmanda.rpy").read_text(
        encoding="utf-8-sig"
    )
    discussion = (ROOT / "game/NPC/Girls/Common/IntHarrassmentDiscuss.rpy").read_text(
        encoding="utf-8-sig"
    )
    show_image = (ROOT / "game/Utilities/General/Sex/HarassShowImage.rpy").read_text(
        encoding="utf-8-sig"
    )
    discuss_image = (ROOT / "game/Utilities/General/Sex/HarassDiscussImage.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "HarrassmentAlreadyDiscussed" not in discussion
    assert "_discussion_text=\"\"" in discussion
    assert "_hsi_picture=\"\"" in show_image
    assert "_hdi_picture=\"\"" in discuss_image
    assert 'MelissaStaticData.image_path("grope", "ass_ok")' in show_image
    assert 'MelissaStaticData.image_path("grope", "tits_shy")' in show_image
    assert 'MelissaStaticData.image_path("grope", "ass_angry")' in show_image
    assert 'MelissaStaticData.image_path("grope", "tit_angry")' in show_image
    for amanda_single_picture in (
        "intro",
        "ass_shy",
        "ass_angry",
        "tit_angry",
        "dress_naked_angry",
        "dress_panties",
    ):
        assert 'AmandaStaticData.image_path("grope", "%s")' % amanda_single_picture in show_image
    for amanda_sequence in ("ass_ok", "tit_ok", "tits_shy", "dress_naked"):
        assert 'AmandaStaticData.cycle_image("grope", "%s"' % amanda_sequence in show_image
    for amanda_asset in (
        "inter.jpg",
        "assangry.jpg",
        "assshy.jpg",
        "assok1.jpg",
        "assok2.jpg",
        "titangry.jpg",
        "titshy1.jpg",
        "titshy2.jpg",
        "titok1.jpg",
        "titok2.jpg",
        "dresspanties.jpg",
        "dressnakedangry.jpg",
        "dressnaked1.jpg",
        "dressnaked2.jpg",
        "scold.jpg",
    ):
        assert '"images/amanda/grope/%s"' % amanda_asset in amanda_data
    assert 'AmandaStaticData.image_path("grope", "scold")' in discuss_image
    assert 'MelissaStaticData.image_path("grope", "scold_agree")' in discuss_image
    assert 'MelissaStaticData.image_path("grope", "throw_delinquent")' in discuss_image
    assert 'call HarassDiscussImage(GirlNameMHD, 3)' in discussion
    assert discuss_image.index("if _hdi_value == 3:") < discuss_image.index('elif _hdi_girl == "melissa":')
    for retired_asset in ("assok1", "assok2", "titshy1", "titshy2", "scoldok"):
        assert retired_asset not in show_image + discuss_image


def test_harassment_picture_text_and_choices_share_one_event_context():
    waitress = (ROOT / "game/NPC/Girls/Common/EventWaitressHarrass.rpy").read_text(encoding="utf-8-sig")
    cleaning = (ROOT / "game/NPC/Girls/Common/EventCleaningHarrass.rpy").read_text(encoding="utf-8-sig")
    reaction = REACTION.read_text(encoding="utf-8-sig")
    after = (ROOT / "game/Utilities/General/NPC/PartEventAfterHarrassment.rpy").read_text(encoding="utf-8-sig")
    discussion = (ROOT / "game/NPC/Girls/Common/IntHarrassmentDiscuss.rpy").read_text(encoding="utf-8-sig")

    for event in (waitress, cleaning):
        assert 'main_ui_begin_native_scene_state("Событие в трактире")' in event
        assert event.index("main_ui_begin_native_scene_state") < event.index("call HarassShowImage")
        assert "Что вы будете делать?" in event
        assert "main_ui_end_native_scene_state()" in event
        assert '"[scene_runtime.text]"' not in event

    assert '"[scene_runtime.text]"' not in reaction + after + discussion
    assert '_event_text + "\\n\\n" + result' in after
    assert 'elif GirlNamePEAH == "amanda":' not in after


def test_rejected_customer_can_be_redirected_to_an_available_tavern_worker():
    people = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
    customer = CUSTOMER_REACTION.read_text(encoding="utf-8-sig")
    clients = (ROOT / "game/Inn/TavernProstClients.rpy").read_text(encoding="utf-8-sig")
    glory = (ROOT / "game/Inn/TavernGloryHole.rpy").read_text(encoding="utf-8-sig")

    assert "def can_accept_tavern_client(self):" in people
    assert "def tavern_service_busy_now(self):" in people
    assert "def available_tavern_service_workers(self, person_ids=()):" in people
    assert 'SexEvents.today_index(self.name, calendar_v2.time_slot(), "Prostitution") > 0' in people
    assert 'SexEvents.today_index(self.name, calendar_v2.time_slot(), "Glory") > 0' in people
    assert 'SexEvents.add_today(self.name, calendar_v2.time_slot(), event_type, place)' in people
    assert 'self.set_sex_stat("clients_day_total", self.sex_stat("clients_day_total", 0) + 1)' in people
    assert '("georgett", "liza")' in customer
    assert "people.available_tavern_service_workers" in customer
    assert "girl_key != people_normalize_id(GirlNamePECHR)" in customer
    assert "accept_tavern_client(1)" in customer
    assert 'elif girl_run_away == 1 and girl_slapped == 0:' in customer
    assert "default " not in customer
    assert 'GetSexEventFromTable(girl_name, client_time, "Prostitution")' in clients
    assert 'CheckIfSexEventExist(girl_name, client_time, "Prostitution")' in clients
    assert 'SexEvents.today_index(girl_key, calendar_v2.time_slot(), "Glory") > 0' in glory
    assert "candidates = booked_workers or workers" in glory
