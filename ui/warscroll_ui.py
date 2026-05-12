from infrastructure.warscroll import (Warscrolls, WarscrollsDict,
                                      warscroll_file_exists)
from prompt_toolkit import HTML, choice

def army_selection(army_path: str) -> Army | None:
    new_army_option: tuple[str, str] = ("new_army", "New Army")
    load_army_option: tuple[str, str] = ("load_army", "Load Army")
    exit_option: tuple[str, str] = ("exit", "Exit")
    options: list[tuple[str, str]] = [
        new_army_option,
        load_army_option,
        exit_option,
    ]

    if not warscroll_file_exists(army_path):
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
        army = load_armies(army_path)
        return army
    else:
        return None


def warscroll_selection(warscroll_path: str) -> str:
    warscrolls: WarscrollsDict = Warscrolls.load_warscrolls(warscroll_path)
    for warscroll in warscrolls:
        print(warscroll)

    return "a_warscroll"
