import army_ui
import regiment_ui
import unit_ui


def main():
    army = army_ui.army_selection()
    regiment = regiment_ui.regiment_selection_menu(army)
    unit = unit_ui.unit_selection_menu(regiment)

    print(f"You selected: {unit.to_dict()}")


if __name__ == "__main__":
    main()