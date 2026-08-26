import ast
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOCIAL_TOPICS = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "SocialTalkTopics.rpy"
MELISSA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "InitMelissa.rpy"
SANDRA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Sandra" / "InitSandra.rpy"
AMANDA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "InitAmanda.rpy"
CLARA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Clara" / "InitClara.rpy"


def _topic_ids_from_social_talk_source():
    source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")
    match = re.search(r"SOCIAL_TALK_TOPICS\s*=\s*\[(.*?)\n\s*\]", source, re.S)
    assert match is not None
    return set(re.findall(r'\{"id": "([^"]+)"', match.group(1)))


def _favorite_topics_from_init(path):
    source = path.read_text(encoding="utf-8-sig")
    match = re.search(r'"favorite_topics":\s*(\[[^\]]+\])', source)
    assert match is not None
    return ast.literal_eval(match.group(1))


def test_class_based_girls_have_five_valid_favorite_topics():
    valid_topics = _topic_ids_from_social_talk_source()
    favorite_sets = []

    for path in [AMANDA_INIT, MELISSA_INIT, SANDRA_INIT, CLARA_INIT]:
        favorites = _favorite_topics_from_init(path)
        assert len(favorites) == 5
        assert len(set(favorites)) == 5
        assert all(topic in valid_topics for topic in favorites)
        favorite_sets.append(frozenset(favorites))

    assert len(set(favorite_sets)) == 4


def test_amanda_favorite_topics_match_character_brief():
    assert _favorite_topics_from_init(AMANDA_INIT) == ["fashion", "dances", "gossip", "money", "stories"]


def test_favorite_topics_are_used_by_authoritative_social_topics():
    source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")

    assert "def social_favorite_topic_ids" in source
    assert 'getattr(info, "talk_preferences", {})' in source
    assert "topic_key in social_favorite_topic_ids(key)" in source
    assert 'procedural_randint(1, 2, "social_talk_%s_%s_%s"' in source
    assert "else -points" in source


def test_talk_cycle_keeps_native_menu_open_and_costs_five_minutes_per_topic():
    source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")
    label = source.split("label SocialTalkTopicMenu", 1)[1]

    assert "while True:" in label
    assert '"Закончить разговор" if _social_mode == "talk":' in label
    assert 'apply_social_interaction_base(key, "talk", score, 0, 5' in source
    assert "social_talk_session_remaining(_social_girl) <= 0" in label
    assert "Тем в этом разговоре" not in source
    assert "Обсуждено тем" not in source
    assert "все десять тем" not in source
    assert 'append_social_score_message(social_topic_text(key, mode_key, topic_key, score), actual_score, False)' in source


def test_ordinary_talk_has_no_second_profile_or_old_point_authority():
    source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")
    old_point = (PROJECT_ROOT / "game" / "NPC" / "Girls" / "Common" / "OldPointTalkSystem.rpy").read_text(encoding="utf-8-sig")

    assert "SOCIAL_TALK_PROFILES" not in source
    assert '"talk": {' not in source.split("SOCIAL_NPC_TOPIC_PACKS", 1)[1].split("SOCIAL_DEFAULT_FLIRT_PROFILE", 1)[0]
    assert "old_point_smalltalk" not in old_point
    assert "OldPointSmallTalkMenu" not in old_point


def test_all_four_favorite_topic_npcs_use_the_authoritative_talk_label():
    talk_files = [
        PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "IntAmandaTalk.rpy",
        PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "IntMelissaTalk.rpy",
        PROJECT_ROOT / "game" / "NPC" / "Girls" / "Sandra" / "IntSandraTalk.rpy",
        PROJECT_ROOT / "game" / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy",
    ]

    for path in talk_files:
        source = path.read_text(encoding="utf-8-sig")
        assert 'call SocialTalkTopicMenu(girl_name, "talk")' in source
        talk_call = source.split('call SocialTalkTopicMenu(girl_name, "talk")', 1)[1]
        assert "repeat_menu = True" in talk_call.split("\n", 2)[1]


def test_seen_topics_are_owned_by_each_npc_not_a_global_mirror():
    source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")

    assert "def social_topic_seen_state" in source
    assert 'info.var["social_topic_seen"] = state' in source
    assert "SocialTalkTopicSeen" not in source
    assert "info.talkToday.add(topic_key)" not in source
