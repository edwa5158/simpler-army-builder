from __future__ import annotations

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice
from tabulate import tabulate

from army import Army


def list_regiments(army: Army) -> list[tuple[str,str]]:

    options: list[tuple[str, str]] = []
    for regiment in army.regiments:
        regiment_option = regiment.regiment_header()
        regiment_option += "\n"
        regiment_option += "-" * 75 + "\n"
        for unit_num in regiment.units:
            regiment_option += unit_num.unit.unit_row() + "\n"
        regiment_option += "\n"
        options.append((regiment.name, regiment_option))

    options.append(("new_regiment", "New Regiment"))
    return options

def regiment_menu() -> None:
    army = Army.from_dict(Army.load_army("two_regiment_army"))  # type: ignore
    options= list_regiments(army)
    
    result: str = choice(
        message=HTML("<u>Select a regiment to edit: </u>:"),
        options=options,
        default="new_regiment",
        show_frame=True,
    )

    print(HTML(f"You selected <b>{result}</b>"))


def main() -> None:
    regiment_menu()

if __name__ == "__main__":
    main()
