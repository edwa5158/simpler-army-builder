from infrastructure.unit import UnitNumbered
from typing import Callable
from config import ARMY_PATH, WARSCROLL_PATH
from infrastructure.army import ArmiesDict, Army
from infrastructure.main import save_all
from infrastructure.regiment import Regiment
from infrastructure.warscroll import Warscrolls
from ui.army_ui import army_menu, army_selection
from ui.exit_menu import exit_menu, exit_menu_response
from ui.main_menu import main_menu, main_menu_response
from ui.regiment_ui import regiment_selection_menu
from ui.unit_ui import unit_selection_menu
from ui.warscroll_ui import WarscrollsMenu


class AppState:
    def __init__(
        self, army_path: str = ARMY_PATH, warscroll_path: str = WARSCROLL_PATH
    ):
        self.current_army: Army | None = None
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
        if self.current_army:  # and self.army_dirty
            self.current_army.save_army(self.army_path)
        if self.warscrolls:  # and self.warscrolls_dirty
            self.warscrolls.save_warscrolls(self.warscroll_path)


class MainMenuController:
    def __init__(
        self, main_menu: Callable, warscroll_menu: Callable, exit_menu: Callable
    ):
        self.main_menu: Callable = main_menu
        self.warscroll_menu: Callable = warscroll_menu
        self.exit_menu: Callable = exit_menu


def main_menu_controller(app_state: AppState) -> None:
    """Controller for the main menu: Manage Armies, Manage Warscrolls, Exit"""
    result: main_menu_response = main_menu()
    if result == "manage_armies":
        army_menu(app_state.army_path)
    elif result == "manage_warscrolls":
        WarscrollsMenu(app_state.warscroll_path)
    elif result == "exit":
        pass  # exit_menu_controller()
    # TODO: Add a Manage Users functionality


def exit_menu_controller(
    army: Army,
    warscrolls: Warscrolls,
    army_path: str = ARMY_PATH,
    warscroll_path: str = WARSCROLL_PATH,
    unsaved_changes: bool = False,
) -> None:
    result: exit_menu_response = exit_menu(unsaved_changes)
    if result == "yes":
        save_all(
            army,
            warscrolls,
            army_path,
            warscroll_path,
        )


def warscroll_selection_controller() -> None:
    print("<u>What warscroll do you want to use?:</u> ")
    WarscrollsMenu(WARSCROLL_PATH)


def unit_selection_controller(regiment: Regiment) -> UnitNumbered:
    result = unit_selection_menu(regiment)
    if result == "new_unit":
        # new_unit_controller
        # return new_unit()
        raise NotImplementedError
    else:
        return regiment.units[int(result)]


def new_unit_controller() -> None:
    """_To be implemented_
    """
    # To be implemented
    pass


def main():
    app_state = AppState()

    main_menu_controller(app_state)

    army: Army = army_selection(ARMY_PATH)  # type: ignore
    _ = regiment_selection_menu(army)


if __name__ == "__main__":
    main()
