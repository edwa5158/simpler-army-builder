from __future__ import annotations

from enum import Enum



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


