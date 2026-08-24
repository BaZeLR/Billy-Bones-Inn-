from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_harness_detects_reparse_points_on_older_python():
    source = (ROOT / "tools/external_click_play_test.py").read_text(encoding="utf-8")

    assert "import stat" in source
    assert "os.lstat(path).st_file_attributes" in source
    assert "stat.FILE_ATTRIBUTE_REPARSE_POINT" in source


def test_external_harness_never_recurses_into_links_or_junctions():
    source = (ROOT / "tools/external_click_play_test.py").read_text(encoding="utf-8")
    cleanup = source.split("def remove_temp_tree(path: Path) -> None:", 1)[1].split(
        "def run_renpy", 1
    )[0]

    assert "not path.is_symlink() and not is_junction(path)" in cleanup
    assert "for child in path.iterdir():" in cleanup
