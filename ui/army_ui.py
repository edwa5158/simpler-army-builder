from __future__ import annotations

from typing import Callable, Optional

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from infrastructure.army import ArmiesDict, Army, army_file_exists
from infrastructure.army import load_armies as army_file_contents
from infrastructure.regiment import Regiment
from ui.screen import Screen, ScreenName


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
    def __init__(
        self,
        get_armies: Callable[[], Optional[ArmiesDict]],
        on_load: Callable[[Army], None],
    ):
        # Read the file at show() time so armies saved during this run show up.
        self.get_armies: Callable[[], Optional[ArmiesDict]] = get_armies
        self.on_load: Callable[[Army], None] = on_load

    def show(self) -> ScreenName:
        armies_dict = self.get_armies()
        if not armies_dict:
            print("No saved saved armies detected.", flush=False)
            return ScreenName.MANAGE_ARMIES

        army_names = [(key, key) for key in armies_dict.keys()]
        result: str = choice(
            message=HTML("<u>Select an army: </u>"), options=army_names
        )

        # print(f"You've selected {result}", flush=False)
        self.on_load(Army.from_dict(armies_dict[result]))
        return ScreenName.VIEW_ARMY


class NewArmyMenu(Screen):
    def __init__(self, army_path: str, on_create: Callable[[Army], None]):
        self.army_path: str = army_path
        self.on_create: Callable[[Army], None] = on_create

    def show(self) -> ScreenName:
        army = Army(prompt(HTML("<u>Enter the name of an army: </u>")))
        army.save_army(self.army_path)
        self.on_create(army)

        return ScreenName.VIEW_ARMY


class ViewArmyMenu(Screen):
    """A screen for viewing the Army metadata, as well as a summary of the regiments, units, and warsrolls that make it up. Allows editing the army name, and selecting a regiment to edit."""

    def __init__(
        self,
        get_army: Callable[[], Army],
        army_path: str,
        on_select_regiment: Callable[[Regiment], None],
    ):
        # Read the army at show() time: the current army changes after startup.
        self.get_army: Callable[[], Army] = get_army
        self.army_path: str = army_path
        self.on_select_regiment: Callable[[Regiment], None] = on_select_regiment

    def show(self) -> ScreenName:
        army = self.get_army()
        print(HTML(f"<u>Army Name:</u> {army.name}"))
        print(HTML(f"<u>Total Points:</u> {army.points}"))
        from ui.regiment_ui import list_regiments

        options, regiment_dict = list_regiments(army)
        options.append(("back", "Back"))

        result: str = choice(
            message=HTML("<u>Select a regiment to edit: </u>:"),
            options=options,
            default="new_regiment",
            show_frame=True,
        )
        if result == "new_regiment":
            regiment = army.add_regiment()
            army.save_army(self.army_path)
            print(HTML(f"Added <b>{regiment.name}</b>"), flush=False)
            return ScreenName.VIEW_ARMY
        if result in regiment_dict:
            self.on_select_regiment(regiment_dict[result])
            return ScreenName.VIEW_REGIMENT
        return ScreenName.MANAGE_ARMIES


if __name__ == "__main__":
    main()
