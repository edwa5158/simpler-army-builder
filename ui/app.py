from __future__ import annotations

from enum import Enum, auto

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from config import ARMY_PATH
from infrastructure.army import army_file_exists, Army, ArmiesDict, load_armies
from infrastructure.warscroll import Warscrolls


class ScreenName(Enum):
    MAIN_MENU = ("main_menu", "Main Menu")
    MANAGE_ARMIES = ("manage_armies", "Manage Armies")
    LOAD_ARMY = ("load_army", "Load Army")
    VIEW_ARMY = ("view_army", "View Army")
    NEW_ARMY = ("new_army", "New Army")
    MANAGE_WARSCROLLS = ("manage_warscrolls", "Manage Warscrolls")
    EXIT = ("exit", "Exit")



class Screen:
    def show(self) -> ScreenName:
        raise NotImplementedError("This method has not been implemented")


class MainMenuScreen(Screen):
    def show(self) -> ScreenName:
        s = ScreenName
        options: list[tuple[str, str]] = [
            s.MANAGE_ARMIES.value,
            s.MANAGE_WARSCROLLS.value,
            s.EXIT.value,
        ]
        result: str = choice(
            message=HTML("<u>What do you want to do?</u>:"),
            options=options,
            default=s.MANAGE_ARMIES.value[0],
        )
        return ScreenName(result)

class ManageArmiesScreen(Screen):
    def show(self) -> ScreenName:
        s = ScreenName
        options: list[tuple[str, str]] = [
            s.NEW_ARMY.value,
            s.LOAD_ARMY.value,
            s.EXIT.value,
        ]
        result: str = choice(
            message=HTML("<u>What do you want to do?</u>:"),
            options=options,
            default=s.LOAD_ARMY.value[0],
        )
        return ScreenName(result)

class LoadArmiesMenu(Screen):

    def __init__(self, app_state: AppState):
        self.app_state: AppState = app_state

    def show(self) -> ScreenName:
        if not army_file_exists(self.app_state.army_path):
            print("No saved army files detected.")
            return ScreenName.MANAGE_ARMIES

        self.app_state.armies_dict = load_armies(army_path=self.app_state.army_path)
        if not self.app_state.armies_dict:
            print(f"No saved armies found in {self.app_state.army_path}")
            return ScreenName.MANAGE_ARMIES

        army_names = [(key, key) for key in self.app_state.armies_dict.keys()]
        result: str = choice(message=HTML("<u>Select an army: </u>"), options=army_names)

        print(HTML(f"You've selected <b>{result}</b>"))
        self.app_state.current_army = Army.from_dict(self.app_state.armies_dict[result])
        return ScreenName.VIEW_ARMY


def registry(app_state: AppState) -> dict[ScreenName, Screen]:
    screen_registry: dict[ScreenName, Screen] = {
        ScreenName.MAIN_MENU: MainMenuScreen(),
        ScreenName.MANAGE_ARMIES: ManageArmiesScreen(),
        ScreenName.LOAD_ARMY: LoadArmiesMenu(app_state)
    }
    return screen_registry

class AppState:
    def __init__(self, army_path: str, warscroll_path: str):
        self.current_army: Army | None = None
        self.armies_dict: ArmiesDict | None = None
        self.warscrolls: Warscrolls | None = None
        self.army_dirty: bool = False
        self.warscrolls_dirty: bool = False
        self.army_path: str = army_path
        self.warscroll_path: str = warscroll_path

        @property
        def has_unsaved_changes(self) -> bool:
            return (self.army_dirty or self.warscrolls_dirty)

        def save(self):
            if self.current_army: # and self.army_dirty
                self.current_army.save_army(self.army_path)
            if self.warscrolls: # and self.warscrolls_dirty
                self.warscrolls.save_warscrolls(self.warscroll_path)


class App:
    def __init__(self, first_screen: Screen, state: AppState):
        self.stack: list[Screen] = [first_screen]
        self.state: AppState = state


    def run(self):
        screen_registry = registry(self.state)
        while self.stack
            current_screen = self.stack.pop()
            next_screen = screen_registry[current_screen.show()]
            self.stack.append(next_screen)


if __name__ == "__main__":
    app = App(MainMenuScreen())
