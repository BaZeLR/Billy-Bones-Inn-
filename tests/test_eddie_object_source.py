from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_eddie_has_own_data_info_and_var_owner():
    source = read_rel("game/NPC/Secondary/InitEddie.rpy")

    assert "class EddieData(PeopleData):" in source
    assert "class EddieInfo(BaseNPC):" in source
    assert "define EddieStaticData = EddieData()" in source
    assert "default Eddie = EddieInfo()" in source
    assert "self.var = {}" in source
    assert "def ensure_story_defaults(self):" in source
    assert "def var_int(self, key, default=0):" in source
    assert "def set_var_int(self, key, value):" in source
    assert "label InitEddie:" in source


def test_eddie_uses_class_state_not_old_var_bridge():
    combined = "\n".join(
        [
            read_rel("game/NPC/Secondary/InitEddie.rpy"),
            read_rel("game/NPC/Secondary/IntEddieTalk.rpy"),
            read_rel("game/Utilities/Time/NextDay_NewDayEvents.rpy"),
            read_rel("game/NPC/Girls/Becky/IntBeckyGuest.rpy"),
            read_rel("game/NPC/Girls/Georgett/IntGeorgettTalk.rpy"),
            read_rel("game/Utilities/General/Classes/StoryEventRuntime.rpy"),
            read_rel("game/Inn/TavernProstClients.rpy"),
        ]
    )

    assert "EddieVar" not in combined
    assert "Eddie.var =" not in combined
    assert 'getattr(renpy.store, "Eddie.var"' not in combined
    assert "getattr(renpy.store, 'Eddie.var'" not in combined
    assert '_ensure_dict("Eddie.var")' not in combined
    assert '"var": Eddie.var' not in combined
    assert "Eddie(var=" not in combined
    assert "EddieInfo(var=" not in combined
    assert "Eddie.var.setdefault" not in combined


def test_eddie_threads_and_dialog_use_class_state():
    talk_source = read_rel("game/NPC/Secondary/IntEddieTalk.rpy")
    threads_source = read_rel("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    people_source = read_rel("game/Utilities/General/NPC/PeopleRuntime.rpy")

    assert "Eddie.ensure_story_defaults()" in talk_source
    assert "Eddie.var.get('TalkedAboutGeorgett'" in threads_source
    assert "Eddie.var.get('SawMomSex'" in threads_source
    assert "Eddie.var.get('FingalTalk'" in threads_source
    assert "call InitEddie" in people_source
