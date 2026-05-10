from __future__ import annotations

from typing import Literal

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

type main_menu_response = Literal["manage_armies", "manage_warscrolls", "exit"]


def main_menu() -> main_menu_response:
    options: list[tuple[str, str]] = [
        ("manage_armies", "Manage Armies"),
        ("manage_warscrolls", "Manage Warscrolls"),
        ("exit", "Exit"),
    ]
    result: main_menu_response = choice(
        message=HTML("<u>What do you want to do?</u>:"),
        options=options,
        default="manage_armies",
    )  # type: ignore
    return result
