from __future__ import annotations

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from regiment import Regiment
from unit import Unit, UnitNumbered
from warscroll_ui import warscroll_selection


def unit_selection_menu(regiment: Regiment) -> UnitNumbered:
    options = [
        (str(unit_num.unit_num), unit_num.warscroll.name) for unit_num in regiment.units
    ]
    options.append(("new_unit", "Add Unit"))

    result: str = choice(
        message=HTML("<u>Select a unit to edit: </u>:"),
        options=options,
        default="0",
        show_frame=True,
    )

    if result == "new_unit":
        return new_unit()
    else:
        return regiment.units[int(result)]


def new_unit() -> UnitNumbered:
    unit = Unit()

    print("<u>What warscroll do you want to use?:</u> ")
    warscroll_selection()

    unit_num: UnitNumbered = UnitNumbered(unit, 99)

    return unit_num


if __name__ == "__main__":
    new_unit()
