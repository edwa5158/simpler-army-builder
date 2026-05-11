from __future__ import annotations

from typing import Optional

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice
from screen import Screen, ScreenName

from infrastructure.army import ArmiesDict, Army, army_file_exists
from infrastructure.army import load_armies as army_file_contents


def army_menu(army_path: str) -> str:
    raise NotImplementedError()

    # View Armies?
    # Delete Army
    # New Army
    return ""


def army_selection(army_path: str) -> Army | None:
    new_army_option: tuple[str, str] = ("new_army", "New Army")
    load_army_option: tuple[str, str] = ("load_army", "Load Army")
    exit_option: tuple[str, str] = ("exit", "Exit")
    options: list[tuple[str, str]] = [
        new_army_option,
        load_army_option,
        exit_option,
    ]

    if not army_file_exists(army_path):
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
    if result == load_army_option[0]:
        return load_armies(army_path)
    return None


def new_army() -> Army:
    army_name = prompt(HTML("<u>Enter a name for your army:</u>    "))
    print(HTML(f"You named your army <b>{army_name}</b>"), flush=False)
    return Army(army_name)


def load_armies(army_path: str) -> Army | None:
    if not army_file_exists(army_path):
        print("No saved army files detected.", flush=False)
        return None
    armies: ArmiesDict | None = army_file_contents(army_path=army_path)
    if not armies:
        print(f"No saved armies found in {army_path}", flush=False)
        return None

    army_names = [(key, key) for key in armies.keys()]
    result: str = choice(message=HTML("<u>Select an army: </u>"), options=army_names)

    print(HTML(f"You've selected <b>{result}</b>"), flush=False)
    army: Army = Army.from_dict(armies[result])
    return army


def main() -> None:
    import ui.regiment_ui as rui

    _ = rui.regiment_selection_menu(Army("new_army"))


class ManageArmiesScreen(Screen):
    def show(self) -> ScreenName:
        s = ScreenName
        options: list[tuple[str, str]] = [
            s.NEW_ARMY.as_tuple,
            s.LOAD_ARMY.as_tuple,
            s.EXIT.as_tuple,
        ]
        result: str = choice(
            message=HTML("<u>What do you want to do?</u>:"),
            options=options,
            default=s.LOAD_ARMY.value,
        )
        return ScreenName(result)


class LoadArmiesMenu(Screen):
    def __init__(self, armies_dict: Optional[ArmiesDict]):
        self.armies_dict: ArmiesDict | None = armies_dict
        self.current_army: Army | None = None

    def show(self) -> ScreenName:
        if not self.armies_dict:
            print("No saved saved armies detected.", flush=False)
            return ScreenName.MANAGE_ARMIES

        army_names = [(key, key) for key in self.armies_dict.keys()]
        result: str = choice(
            message=HTML("<u>Select an army: </u>"), options=army_names
        )

        print(f"You've selected {result}", flush=False)
        self.current_army = Army.from_dict(self.armies_dict[result])
        return ScreenName.VIEW_ARMY


if __name__ == "__main__":
    main()
