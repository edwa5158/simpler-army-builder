import json
from prompt_utils import Option, prompt_user

def create_warscroll() -> dict:

    is_valid: bool = False
    while not is_valid:
        name, points, is_hero = input("Enter the name, points, and if the warscroll is a hero (True / False)").split()
        try:
            name = str(name)
            points = int(points)
            is_hero = bool(is_hero)
            is_valid = True
        except (ValueError, AttributeError):
            print("Invalid entry. The name must be a string, points must be an integer, and is_hero a boolean.")
            is_valid = False


    warscrolls = load_warscrolls()
    new_warscroll =  {"name": name, "points": points, "is_hero": is_hero}

    if name in warscrolls.keys():
        ans = prompt_user(
            {
                1: Option("Overwrite", lambda: print("Overwriting warscroll")),
                2: Option("Cancel", lambda: print("Cancelling warscroll creation"))
            }
        )
        if ans != 1:
            return warscrolls[name]
    warscrolls[name] = new_warscroll
    save_warscrolls(warscrolls)
    return new_warscroll


def save_warscrolls(warscrolls: dict):
    with open("warscrolls.json", "w") as f:
        f.wrint(json.dumps(warscrolls))

def load_warscrolls() -> dict:
    with open("warscrolls.json", "r") as f:
        warscrolls = json.load(f)
    return warscrolls