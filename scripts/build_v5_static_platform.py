from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from platform_core.v5_site_builder import build_site


def main() -> None:
    out = build_site()
    print(f"Built v5 static platform: {out}")
    print("Preview with: python -m http.server 8000 -d outputs/v5/site")


if __name__ == "__main__":
    main()
