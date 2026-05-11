from __future__ import annotations

from enum import Enum

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from infrastructure.army import ArmiesDict, Army, army_file_exists, load_armies


class ScreenName(str, Enum):
    MAIN_MENU = "main_menu"
    MANAGE_ARMIES = "manage_armies"
    LOAD_ARMY = "load_army"
    VIEW_ARMY = "view_army"
    NEW_ARMY = "new_army"
    MANAGE_WARSCROLLS = "manage_warscrolls"
    EXIT = "exit"

    @property
    def display_name(self) -> str:
        if self is ScreenName.MAIN_MENU:
            return "Main Menu"
        if self is ScreenName.MANAGE_ARMIES:
            return "Manage Armies"
        if self is ScreenName.LOAD_ARMY:
            return "Load Army"
        if self is ScreenName.VIEW_ARMY:
            return "View Army"
        if self is ScreenName.NEW_ARMY:
            return "New Army"
        if self is ScreenName.MANAGE_WARSCROLLS:
            return "Manage Warscrolls"
        return "Exit"

    @property
    def as_tuple(self) -> tuple[str, str]:
        return (self.value, self.display_name)


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
            default=s.MANAGE_ARMIES.value,
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
            default=s.LOAD_ARMY.value,
        )
        return ScreenName(result)


class LoadArmiesMenu(Screen):
    def __init__(self, army_path: str):
        self.army_path: str = army_path
        self.armies_dict: ArmiesDict | None = None
        self.current_army: Army | None = None

    def show(self) -> ScreenName:
        if not army_file_exists(self.army_path):
            print("No saved army files detected.", flush=False)
            return ScreenName.MANAGE_ARMIES

        armies = load_armies(army_path=self.army_path)
        if not armies:
            print(f"No saved armies found in {self.army_path}", flush=False)
            return ScreenName.MANAGE_ARMIES

        self.armies_dict = armies
        army_names = [(key, key) for key in armies.keys()]
        result: str = choice(
            message=HTML("<u>Select an army: </u>"), options=army_names
        )

        print(f"You've selected {result}", flush=False)
        self.current_army = Army.from_dict(armies[result])
        return ScreenName.VIEW_ARMY
