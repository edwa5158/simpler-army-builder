from __future__ import annotations

from typing import Literal

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

type exit_menu_response = Literal["yes", "no", "cancel"]


def exit_menu(unsaved_changes: bool = False) -> exit_menu_response:
    result: exit_menu_response
    if unsaved_changes:
        options: list[tuple[str, str]] = [
            ("yes", "Yes"),
            ("no", "No"),
            ("cancel", "Cancel"),
        ]
        result = choice(
            message=HTML("<u>What do you want to do?</u>:"),
            options=options,
            default="yes",
        )  # type: ignore
    else:
        result = "no"

    return result
