from __future__ import annotations

from enum import Enum

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from infrastructure.army import ArmiesDict, Army, army_file_exists, load_armies


class ScreenName(Enum):
    MAIN_MENU = ("main_menu", "Main Menu")
    MANAGE_ARMIES = ("manage_armies", "Manage Armies")
    LOAD_ARMY = ("load_army", "Load Army")
    VIEW_ARMY = ("view_army", "View Army")
    NEW_ARMY = ("new_army", "New Army")
    MANAGE_WARSCROLLS = ("manage_warscrolls", "Manage Warscrolls")
    EXIT = ("exit", "Exit")

    def __new__(cls, value: str, display_name: str):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, value: str, display_name: str):
        self.display_name = display_name

    @property
    def as_tuple(self) -> tuple[str, str]:
        return self.value, self.display_name


class Screen:
    def show(self) -> ScreenName:
        raise NotImplementedError("This method has not been implemented")


class MainMenuScreen(Screen):
    def show(self) -> ScreenName:
        s = ScreenName
        options: list[tuple[str, str]] = [
            s.MANAGE_ARMIES.as_tuple,
            s.MANAGE_WARSCROLLS.as_tuple,
            s.EXIT.as_tuple,
        ]
        result: str = choice(
            message=HTML("<u>What do you want to do?</u>:"),
            options=options,
            default=s.MANAGE_ARMIES.as_tuple[0],
        )
        return ScreenName(result)


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
            default=s.LOAD_ARMY.as_tuple[0],
        )
        return ScreenName(result)


class LoadArmiesMenu(Screen):
    def __init__(self, army_path: str):
        # self.app_state: AppState = app_state
        self.army_path: str = army_path
        self.armies_dict: ArmiesDict | None
        self.current_army: Army

    def show(self) -> ScreenName:
        if not army_file_exists(self.army_path):
            print("No saved army files detected.")
            return ScreenName.MANAGE_ARMIES

        self.armies_dict = load_armies(army_path=self.army_path)
        if not self.armies_dict:
            print(f"No saved armies found in {self.army_path}")
            return ScreenName.MANAGE_ARMIES

        army_names = [(key, key) for key in self.armies_dict.keys()]
        result: str = choice(
            message=HTML("<u>Select an army: </u>"), options=army_names
        )

        print(HTML(f"You've selected <b>{result}</b>"))
        self.current_army = Army.from_dict(self.armies_dict[result])
        return ScreenName.VIEW_ARMY