import json
from prompt_utils import prompt_user, Option
from regiment import add_regiment


def new_army():
    army = {}
    army["name"] = str(input("Enter a name for your army: "))
    print(f"You named your army {army.get('name', '')}\n")
    build_army(army)


def build_army(army):
    options: dict[int, Option] = {
        1: Option("Save Army", save_army, tuple(), {"army": army}),
        2: Option("Add Regiment", add_regiment),
        3: Option("Update Existing Regiment", lambda: print("UPDATING REGIMENT...\n")),
        4: Option("Exit", lambda: print("Exiting...\n")),
    }
    answer: int = 0
    while answer != 4:
        answer = prompt_user(options)[0]


def save_army(army: dict) -> None:
    json_str = json.dumps(army, indent=4)
    with open("army.json", "w") as f:
        f.write(json_str)
    print("Army saved")

def load_army() -> dict:
    with open("army.json", "r") as f:
        army = json.load(f)
    print(f"Loading army: {army.get('name', 'ERROR: army name not found')}\n")
    build_army(army)

