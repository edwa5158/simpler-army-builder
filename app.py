from __future__ import annotations

from datetime import datetime

import ui.screen as s
from config import ARMY_PATH, WARSCROLL_PATH
from infrastructure.army import ArmiesDict, Army, army_file_exists
from infrastructure.warscroll import Warscrolls
from ui.army_ui import (
    LoadArmiesMenu,
    ManageArmiesScreen,
    NewArmyMenu,
    ViewArmyMenu,
    army_file_contents,
)
from ui.main_menu import MainMenuScreen
from ui.screen import ScreenName as sn


class AppState:
    def __init__(self, army_path: str, warscroll_path: str):
        self.current_army: Army = Army(
            f"new_army - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.armies_dict: ArmiesDict | None = None
        self.warscrolls: Warscrolls | None = None
        self.army_dirty: bool = False
        self.warscrolls_dirty: bool = False
        self.army_path: str = army_path
        self.warscroll_path: str = warscroll_path

    @property
    def has_unsaved_changes(self) -> bool:
        return self.army_dirty or self.warscrolls_dirty

    def save(self) -> None:
        if self.current_army:
            self.current_army.save_army(self.army_path)
        if self.warscrolls:
            self.warscrolls.save_warscrolls(self.warscroll_path)

    def get_armies(self) -> ArmiesDict | None:
        if not army_file_exists:
            return None
        return army_file_contents(self.army_path)


def registry(app_state: AppState) -> dict[s.ScreenName, s.Screen]:
    screen_registry: dict[s.ScreenName, s.Screen] = {
        sn.MAIN_MENU: MainMenuScreen(),
        sn.MANAGE_ARMIES: ManageArmiesScreen(),
        sn.LOAD_ARMY: LoadArmiesMenu(app_state.get_armies()),
        sn.NEW_ARMY: NewArmyMenu(app_state.current_army, app_state.army_path),
        sn.VIEW_ARMY: ViewArmyMenu(app_state.current_army),
    }
    return screen_registry


class App:
    def __init__(self, first_screen: s.ScreenName, state: AppState):
        self.stack: list[s.ScreenName] = [first_screen]
        self.state: AppState = state

    def run(self) -> None:
        screen_registry = registry(self.state)
        while self.stack:
            screen_name = self.stack.pop()
            if screen_name == sn.EXIT:
                break
            current_screen = screen_registry[screen_name]
            next_screen = current_screen.show()
            print("\n")
            self.stack.append(next_screen)


if __name__ == "__main__":
    state = AppState(ARMY_PATH, WARSCROLL_PATH)
    app = App(sn.MAIN_MENU, state)
    app.run()
