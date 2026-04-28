from __future__ import annotations

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice
from prompt_toolkit import print_formatted_text as print

from army import ArmiesDict, Army, army_file_contents, army_file_exists
from config import ARMY_PATH


def army_selection():
    army = Army("new army")
    new_army_option: tuple[str, str] = ("new_army", "New Army")
    load_army_option: tuple[str, str] = ("load_army", "Load Army")
    exit_option: tuple[str, str] = ("exit", "Exit")

    options: list[tuple[str, str]] = [
        new_army_option,
        load_army_option,
        exit_option,
    ]

    if not army_file_exists():
        options.remove(load_army_option)

    result: str = choice(
        message=HTML(
            "<u>Do you want to create a new army, or load an existing army?</u>:"
        ),
        options=options,
        default="new_army",
    )
    if result == new_army_option[0]:
        army.name = new_army()
    elif result == load_army_option[0]:
        load_armies()
    else:
        return


def new_army() -> str:
    army_name = prompt(HTML("<u>Enter a name for your army:</u>    "))
    print(HTML(f"You named your army <strong>{army_name}</strong>"))
    return army_name


def load_armies(army_path: str = ARMY_PATH) -> ArmiesDict | None:
    if not army_file_exists():
        print("No saved army files detected.")
        return None

    return army_file_contents(army_path=army_path)


def main() -> None:
    army_selection()


if __name__ == "__main__":
    main()
