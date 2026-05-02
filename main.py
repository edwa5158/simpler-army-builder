import config
from infrastructure.army import Army
from ui.army_ui import army_selection
from ui.regiment_ui import regiment_selection_menu
from ui.unit_ui import unit_selection_menu


def main():
    config.ARMY_PATH
    config.WARSCROLL_PATH

    army: Army = army_selection()  # type: ignore
    regiment = regiment_selection_menu(army)
    unit = unit_selection_menu(regiment)

    print(f"You selected: {unit.to_dict()}")


if __name__ == "__main__":
    main()
