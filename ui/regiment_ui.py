from __future__ import annotations

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from infrastructure.army import Army
from infrastructure.regiment import Regiment
from core.shared import header_underline


def list_regiments(army: Army) -> tuple[list[tuple[str, str]], dict[str, Regiment]]:

    options: list[tuple[str, str]] = []
    regiment_dict: dict[str, Regiment] = {}
    for regiment in army.regiments:
        regiment_option = regiment.header()
        regiment_option += "\n"
        regiment_option += header_underline()
        regiment_option += "\n"
        for unit_num in regiment.units:
            regiment_option += unit_num.unit.unit_row() + "\n"
        regiment_option += "\n"
        options.append((regiment.name, regiment_option))
        regiment_dict[regiment.name] = regiment
    options.append(("new_regiment", "New Regiment"))
    return options, regiment_dict


def regiment_selection_menu(army: Army) -> Regiment:
    options, regiment_dict = list_regiments(army)

    result: str = choice(
        message=HTML("<u>Select a regiment to edit: </u>:"),
        options=options,
        default="new_regiment",
        show_frame=True,
    )
    print("\n")

    print(HTML(f"You selected <b>{result}</b>\n"))
    return army.add_regiment() if result == "new_regiment" else regiment_dict[result]


def main() -> None:
    army = Army.from_dict(Army.load_army("two_regiment_army"))  # type: ignore
    regiment_selection_menu(army)


if __name__ == "__main__":
    main()
