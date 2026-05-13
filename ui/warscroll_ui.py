from prompt_toolkit import HTML, choice

from infrastructure.warscroll import Warscrolls, WarscrollsDict
from ui.screen import Screen, ScreenName

# def army_selection(army_path: str) -> Army | None:
#     new_army_option: tuple[str, str] = ("new_army", "New Army")
#     load_army_option: tuple[str, str] = ("load_army", "Load Army")
#     exit_option: tuple[str, str] = ("exit", "Exit")
#     options: list[tuple[str, str]] = [
#         new_army_option,
#         load_army_option,
#         exit_option,
#     ]

#     if not warscroll_file_exists(army_path):
#         options.remove(load_army_option)

#     result: str = choice(
#         message=HTML(
#             "<u>Do you want to create a new army, or load an existing army?</u>:"
#         ),
#         options=options,
#         default="new_army",
#     )
#     if result == new_army_option[0]:
#         return new_army()
#     elif result == load_army_option[0]:
#         army = load_armies(army_path)
#         return army
#     else:
#         return None


class WarscrollsMenu(Screen):
    """A screen for viewing the Army metadata, as well as a summary of the regiments, units, and warsrolls that make it up. Allows editing the army name, and selecting a regiment to edit."""

    def __init__(self, warscroll_path: str):
        self.path = warscroll_path

    def show(self):
        warscrolls: WarscrollsDict = Warscrolls.load_warscrolls(self.path)
        options = [(key, ws["name"]) for key, ws in warscrolls.items()]

        _ = choice(
            message=HTML("<u>Select a Warscroll:</u>"),
            options=options,
            default=options[0],
        )
        return ScreenName.MANAGE_ARMIES
