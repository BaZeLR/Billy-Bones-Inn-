from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return path.read_text(encoding="utf-8-sig")


def test_dress_order_runtime_has_one_owner():
    runtime = read(ROOT / "game/Town/Arts/Dress/DressShop.rpy")
    assert "class DressShopRuntimeState" in runtime
    assert 'self.produced = ""' in runtime
    assert 'self.buyer = ""' in runtime
    assert "default dress_shop = DressShopRuntimeState()" in runtime

    gameplay = "\n".join(
        read(path)
        for path in (ROOT / "game").rglob("*.rpy")
    )
    assert "DressProduced" not in gameplay
    assert "DressBuyer" not in gameplay
    assert "GirlDressBlock" not in gameplay


def test_tailor_order_consumers_use_dress_shop_owner():
    paths = [
        ROOT / "game/Utilities/General/Clothes/DressTry.rpy",
        ROOT / "game/Utilities/Time/NextDay.rpy",
        ROOT / "game/Town/Arts/Dress/DressShopDressItems.rpy",
        ROOT / "game/Town/Arts/Dress/DressShopWorktable001.rpy",
    ]
    combined = "\n".join(read(path) for path in paths)
    assert "dress_shop.produced" in combined
    assert "dress_shop.buyer" in combined
