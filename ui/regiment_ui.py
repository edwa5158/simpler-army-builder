from __future__ import annotations

from typing import Callable

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice

from config import ARMY_PATH
from core.shared import header_underline, left_side_of_regiment
from infrastructure.army import Army
from infrastructure.regiment import Regiment
from infrastructure.unit import Unit
from infrastructure.warscroll import Warscroll, Warscrolls
from ui.screen import Screen, ScreenName


def list_regiments(army: Army) -> tuple[list[tuple[str, str]], dict[str, Regiment]]:
    options: list[tuple[str, str]] = []
    regiment_dict: dict[str, Regiment] = {}
    for regiment in army.regiments:
        regiment_option = regiment.header()
        regiment_option += "\n"
        regiment_option += header_underline()
        regiment_option += "\n"
        for unit_num in regiment.units:
            regiment_option += unit_num.unit.unit_row() + "\n"
        regiment_option += "\n"
        options.append((regiment.name, regiment_option))
        regiment_dict[regiment.name] = regiment
    options.append(("new_regiment", "New Regiment"))
    return options, regiment_dict


def regiment_selection_menu(army: Army) -> Regiment:
    options, regiment_dict = list_regiments(army)

    result: str = choice(
        message=HTML("<u>Select a regiment to edit: </u>:"),
        options=options,
        default="new_regiment",
        show_frame=True,
    )
    print("\n")

    print(HTML(f"You selected <b>{result}</b>\n"), flush=False)
    return army.add_regiment() if result == "new_regiment" else regiment_dict[result]


class ViewRegimentMenu(Screen):
    """A screen showing one regiment's units, with options to add a unit or go back to the army."""

    def __init__(
        self,
        get_army: Callable[[], Army],
        get_regiment: Callable[[], Regiment | None],
        army_path: str,
        warscroll_path: str,
    ):
        self.get_army: Callable[[], Army] = get_army
        self.get_regiment: Callable[[], Regiment | None] = get_regiment
        self.army_path: str = army_path
        self.warscroll_path: str = warscroll_path

    def show(self) -> ScreenName:
        army = self.get_army()
        regiment = self.get_regiment()
        if regiment is None:
            return ScreenName.VIEW_ARMY

        print(HTML(f"<u>Army Name:</u> {army.name}"))
        print(" " * left_side_of_regiment + regiment.header())
        print(header_underline())
        for unit_num in regiment.units:
            print(unit_num.unit.unit_row())
        if not regiment.units:
            print("        (no units)")

        result: str = choice(
            message=HTML(f"<u>Edit {regiment.name}</u>:"),
            options=[("add_unit", "Add Unit"), ("back", "Back to Army")],
            default="add_unit",
        )
        if result == "add_unit":
            self.add_unit(army, regiment)
            return ScreenName.VIEW_REGIMENT
        return ScreenName.VIEW_ARMY

    def add_unit(self, army: Army, regiment: Regiment) -> None:
        warscrolls = Warscrolls.load_warscrolls(self.warscroll_path)
        if not warscrolls:
            print("No saved warscrolls detected.", flush=False)
            return

        options: list[tuple[str, str]] = [
            (
                key,
                f"{ws['name']}{' (hero)' if ws['is_hero'] else ''}: {ws['points']} points",
            )
            for key, ws in warscrolls.items()
        ]
        options.append(("cancel", "Cancel"))
        result: str = choice(
            message=HTML("<u>Select a warscroll for the new unit:</u>"),
            options=options,
            default=options[0][0],
        )
        if result == "cancel":
            return

        unit = Unit.from_warscroll(Warscroll.from_dict(warscrolls[result]))
        regiment.add_unit(unit)
        army.save_army(self.army_path)
        print(
            HTML(f"Added <b>{unit.warscroll.name}</b> to {regiment.name}"), flush=False
        )


def main() -> None:
    army_dict = Army.load_army("two_regiment_army", ARMY_PATH)
    if army_dict is None:
        return

    army = Army.from_dict(army_dict)
    regiment_selection_menu(army)


if __name__ == "__main__":
    main()
