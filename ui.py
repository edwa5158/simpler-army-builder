from __future__ import annotations

# def main():
#     army: Army = Army("new_army")  # temporary name that's overwritten
#     options: dict[int, Option] = {
#         1: Option("New Army", new_army),
#         2: Option("Load Army", army.load_army),
#         3: Option("Exit", lambda: print("Exiting...\n")),
#     }
#     prompt_user(options)
#     build_army(army)
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from army import Army, army_file_exists
from main import load_army, new_army

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
        new_army(army)
    elif result == load_army_option[0]:
        load_army(army)
    else :
        return
    


def main() -> None:


if __name__ == "__main__":
    main()
