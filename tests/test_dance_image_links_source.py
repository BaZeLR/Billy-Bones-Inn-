import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
DANCE_SOURCES = [
    GAME / "NPC" / "Girls" / "Amanda" / "IntAmandaDance.rpy",
    GAME / "NPC" / "Girls" / "Amanda" / "AmandaLegareDanceSequence.rpy",
    GAME / "NPC" / "Girls" / "Amanda" / "AmandaSexDanceStreet.rpy",
    GAME / "NPC" / "Girls" / "Becky" / "IntBeckyDance.rpy",
]


def test_folder_based_dance_image_calls_do_not_bypass_their_folders():
    for path in DANCE_SOURCES:
        dance_calls = [
            line
            for line in path.read_text(encoding="utf-8-sig").splitlines()
            if "ShowImage(" in line and '"dance"' in line
        ]
        assert dance_calls
        assert all(not re.search(r'\.(?:png|jpg|jpeg|webp|gif|mp4)"', line, re.IGNORECASE) for line in dance_calls)


def test_direct_dance_image_paths_exist():
    for path in DANCE_SOURCES:
        source = path.read_text(encoding="utf-8-sig")
        for image_ref in re.findall(r'"(images/(?:amanda|becky)/dance/[^"\n]+\.(?:png|jpg|jpeg|webp|gif|mp4))"', source, re.IGNORECASE):
            if "%" in image_ref:
                continue
            assert (GAME / image_ref).is_file(), "Missing dance image: {}".format(image_ref)


def test_static_folder_based_dance_images_exist():
    for path in DANCE_SOURCES:
        girl = "becky" if "Becky" in path.parts else "amanda"
        source = path.read_text(encoding="utf-8-sig")
        image_names = re.findall(r'ShowImage\([^,]+,\s*"dance",\s*"([^"]+)"\)\s*$', source, re.MULTILINE)
        for image_name in image_names:
            candidates = [(GAME / "images" / girl / "dance" / image_name).with_suffix(ext) for ext in [".png", ".jpg", ".webp", ".gif", ".mp4"]]
            assert any(candidate.is_file() for candidate in candidates), "Missing {} dance image: {}".format(girl, image_name)


def test_dynamic_amanda_dance_variants_exist():
    dance_dir = GAME / "images" / "amanda" / "dance"
    for name in ["wait1.png", "wait2.png"] + ["legare_step_{}.png".format(index) for index in range(4)]:
        assert (dance_dir / name).is_file(), "Missing Amanda dance image: {}".format(name)


def test_dynamic_becky_dance_variants_exist():
    dance_dir = GAME / "images" / "becky" / "dance"
    for index in range(2, 6):
        name = "you_dance_{}.png".format(index)
        assert (dance_dir / name).is_file(), "Missing Becky dance image: {}".format(name)
