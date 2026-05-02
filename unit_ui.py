from __future__ import annotations

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from regiment import Regiment
from unit import UnitNumbered


def unit_selection_menu(regiment: Regiment) -> UnitNumbered:
    options = [
        (str(unit_num.unit_num), unit_num.warscroll.name) for unit_num in regiment.units
    ]

    result: str = choice(
        message=HTML("<u>Select a unit to edit: </u>:"),
        options=options,
        default="0",
        show_frame=True,
    )

    return regiment.units[int(result)]
