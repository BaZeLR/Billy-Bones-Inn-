#!/usr/bin/env python3
"""One-off helper for extracting Sandra real-name entries."""

from __future__ import annotations

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INIT_SANDRA_PATH = PROJECT_ROOT / "game" / "Inn" / "InitSandra.txt"


def main() -> int:
    text = INIT_SANDRA_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r"\$RealName\[$GirlName\]=\s*'([^']+)'")
    for name in pattern.findall(text):
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
