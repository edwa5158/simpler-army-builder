from __future__ import annotations

import argparse

from config import WARSCROLL_PATH
from ui.warscroll_preview_ui import WarscrollsPreviewMenu


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Launch the warscroll preview UI for manual testing."
    )
    parser.add_argument(
        "warscroll_path",
        nargs="?",
        default=WARSCROLL_PATH,
        help="Path to the warscroll JSON file to load.",
    )
    args = parser.parse_args()

    menu = WarscrollsPreviewMenu(args.warscroll_path)
    menu.show()

    if menu.selected_warscroll_key:
        print(f"Selected warscroll: {menu.selected_warscroll_key}")
    else:
        print("No warscroll selected.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
