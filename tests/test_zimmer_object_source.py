from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_zimmer_has_own_data_info_and_var_owner():
    source = read_rel("game/NPC/Secondary/InitZimmer.rpy")

    assert "class ZimmerData(PeopleData):" in source
    assert "class ZimmerInfo(BaseNPC):" in source
    assert "define ZimmerStaticData = ZimmerData()" in source
    assert "default Zimmer = ZimmerInfo()" in source
    assert "self.var = {}" in source
    assert "def ensure_story_defaults(self):" in source
    assert "def var_int(self, key, default=0):" in source
    assert "def set_var_int(self, key, value):" in source


def test_zimmer_uses_class_state_not_old_var_bridge():
    combined = "\n".join(
        [
            read_rel("game/NPC/Secondary/InitZimmer.rpy"),
            read_rel("game/NPC/Secondary/IntZimmerTalk.rpy"),
            read_rel("game/Utilities/Time/NextDay_TavernDaily.rpy"),
            read_rel("game/Utilities/General/Screens/stat.rpy"),
            read_rel("game/NPC/Girls/Clara/ClaraPaintingsThread.rpy"),
            read_rel("game/NPC/Girls/Becky/BeckyEvents.rpy"),
        ]
    )

    assert "ZimmerVar" not in combined
    assert "Zimmer.var =" not in combined
    assert 'getattr(renpy.store, "Zimmer.var"' not in combined
    assert "getattr(renpy.store, 'Zimmer.var'" not in combined
    assert '_ensure_dict("Zimmer.var")' not in combined
    assert '"var": Zimmer.var' not in combined
    assert "Zimmer(var=" not in combined
    assert "ZimmerInfo(var=" not in combined
    assert "Zimmer.var.setdefault" not in combined


def test_zimmer_dialog_and_events_use_class_defaults():
    talk_source = read_rel("game/NPC/Secondary/IntZimmerTalk.rpy")
    event_source = read_rel("game/NPC/Girls/Becky/BeckyEvents.rpy")

    assert "Zimmer.ensure_story_defaults()" in talk_source
    assert "Zimmer.ensure_story_defaults()" in event_source
    assert "label IntZimmerTalkRefresh" not in talk_source
    assert "label IntZimmerTalkApply" not in talk_source
    assert 'str(choice_code or "")' not in talk_source
