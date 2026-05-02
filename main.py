import regiment_ui
import unit_ui
from army_ui import Army, army_selection


def main():
    army: Army = army_selection()  # type: ignore
    regiment = regiment_ui.regiment_selection_menu(army)
    unit = unit_ui.unit_selection_menu(regiment)

    print(f"You selected: {unit.to_dict()}")


if __name__ == "__main__":
    main()
