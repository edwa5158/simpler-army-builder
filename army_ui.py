from __future__ import annotations

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from army import ArmiesDict, Army, army_file_contents, army_file_exists
from config import ARMY_PATH


def army_selection() -> Army | None:
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
        return new_army()
    elif result == load_army_option[0]:
        army = load_armies()
        return army
    else:
        return None


def new_army() -> Army:
    army_name = prompt(HTML("<u>Enter a name for your army:</u>    "))
    print(HTML(f"You named your army <strong>{army_name}</strong>"))
    return Army(army_name)


def load_armies(army_path: str = ARMY_PATH) -> Army | None:
    if not army_file_exists():
        print("No saved army files detected.")
        return None
    armies: ArmiesDict | None = army_file_contents(army_path=army_path)
    if not armies:
        print(f"No saved armies found in {army_path}")
        return None

    army_names = [(key, key) for key in armies.keys()]
    result: str = choice(message=HTML("<u>Select an army: </u>"), options=army_names)

    print(HTML(f"You've selected <b>{result}</b>"))
    army: Army = Army.from_dict(armies[result])
    return army


def main() -> None:
    army = army_selection() or Army("new_army")
    import regiment_ui as rui

    regiment = rui.regiment_selection_menu(army)
    

if __name__ == "__main__":
    main()
