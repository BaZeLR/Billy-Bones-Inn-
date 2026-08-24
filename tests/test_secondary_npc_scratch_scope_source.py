from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_secondary_talk_scratch_is_label_local():
    francheska = read("game/NPC/Secondary/IntFrancheskaTalk.rpy")
    robin = read("game/NPC/Secondary/IntRobinTalk.rpy")
    mongol = read("game/NPC/Secondary/IntMongolTalk.rpy")

    assert 'renpy.dynamic("_fran_text", "_fran_topic_index")' in francheska
    assert 'renpy.dynamic("_robin_tmp_desc")' in robin
    assert "RobinTmpDesc" not in robin
    assert 'renpy.dynamic("_secret_item", "_secret_price")' in mongol


def test_secondary_profiles_have_one_data_owner_not_store_scalars():
    sources = "\n".join(
        read(relative)
        for relative in (
            "game/NPC/Secondary/InitDraupnir.rpy",
            "game/NPC/Secondary/InitZimmer.rpy",
            "game/NPC/Secondary/InitRobin.rpy",
            "game/NPC/Secondary/InitEddie.rpy",
            "game/NPC/Secondary/InitSecondaryNPC.rpy",
        )
    )

    for old_name in (
        "DraupnirProfile",
        "ZimmerProfile",
        "RobinProfile",
        "EddieProfile",
        "LuisaProfile",
        "SergioProfile",
    ):
        assert f"$ {old_name} =" not in sources

    assert sources.count("description=") >= 6
