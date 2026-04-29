import json

from army import Army
from prompt_utils import Option, prompt_user
from regiment import Regiment
from warscroll import Warscroll, Warscrolls


def build_army(army: Army):
    options: dict[int, Option] = {
        1: Option("Save Army", army.save_army, (), {}),
        2: Option("Add Regiment", add_regiment, (army,), {}),
        3: Option("Update Existing Regiment", lambda: print("UPDATING REGIMENT...\n")),
        4: Option("Exit", lambda: print("Exiting...\n")),
    }
    prompt_user(options)

    answer: int = 0
    while answer != 4:
        answer = prompt_user(options)[0]


def add_regiment(army: Army):
    regiment: Regiment = army.add_regiment()
    print(f"Added regiment {regiment.name} has been added to your army")
    # Add the ability to update the regiment right away by adding a unit?


def get_warscroll_inputs() -> tuple[str, int, bool]:
    name: str = ""
    points: int = 0

    while True:
        user_inputs: str = input(
            "Enter the name, points, and if the warscroll is a hero (True / False)"
        )
        name_in, points_in, is_hero_in = user_inputs.split(", ")
        try:
            name = str(name_in)
        except ValueError:
            print("name must be a string")

        try:
            points = int(points_in)
        except ValueError:
            print("points must be an integer")

        is_hero: bool = True if is_hero_in.lower() == "true" else False

        break

    return (name, points, is_hero)


def user_chooses_overwrite_warscroll() -> bool:
    ans = prompt_user(
        {
            1: Option("Overwrite", lambda: print("Overwriting warscroll")),
            2: Option("Cancel", lambda: print("Cancelling warscroll creation")),
        }
    )
    return ans == 1


def create_warscroll() -> Warscroll:
    name, points, is_hero = get_warscroll_inputs()
    warscrolls = Warscrolls()
    warscrolls.load_warscrolls()
    overwrite: bool = True

    if name in warscrolls.catalog:
        overwrite = user_chooses_overwrite_warscroll()

    if not overwrite:
        warscroll = warscrolls.catalog[name]
    else:
        warscroll = Warscroll(name, points, is_hero)
        warscrolls.append_warscroll(warscroll)
        warscrolls.save_warscrolls()
    return warscroll


def save_army(army: dict) -> None:
    json_str = json.dumps(army, indent=4)
    with open("army.json", "w") as f:
        f.write(json_str)
    print("Army saved")


def main():
    army: Army = Army("new_army")  # temporary name that's overwritten

    options: dict[int, Option] = {
        1: Option("New Army", new_army),
        2: Option("Load Army", army.load_army),
        3: Option("Exit", lambda: print("Exiting...\n")),
    }
    prompt_user(options)
    build_army(army)


if __name__ == "__main__":
    main()
