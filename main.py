from prompt_utils import prompt_user, Option
from regiment import Regiment
from army import Army

def new_army():
    army_name= str(input("Enter a name for your army: "))
    army = Army(army_name)
    print(f"You named your army {army_name}\n")
    build_army(army)

def build_army(army: Army):
    options: dict[int, Option] = {
        1: Option("Save Army", army.save_army, (), {}),
        2: Option("Add Regiment", add_regiment, army),
        3: Option("Update Existing Regiment", lambda: print("UPDATING REGIMENT...\n")),
        4: Option("Exit", lambda: print("Exiting...\n")),
    }
    prompt_user(options)


def add_regiment(army: Army):
    regiment: Regiment = army.add_regiment()
    print(f"Added regiment {regiment.name} has been added to your army")
    # Add the ability to update the regiment right away by adding a unit?

def main():
    options: dict[int, Option] = {
        1: Option("New Army", new_army),
        2: Option("Load Army", load_army),
        3: Option("Exit", lambda: print("Exiting...\n")),
    }
    prompt_user(options)


if __name__ == "__main__":
    main()
