import json
from prompt_utils import Option, prompt_user

def get_user_inputs() -> tuple[str, int, bool]:
    is_valid: bool = False
    while not is_valid:
        user_inputs: str = input("Enter the name, points, and if the warscroll is a hero (True / False)")
        name, points, is_hero = user_inputs.split(", ")
        try:
            name = str(name)
            points = int(points)
            if is_hero.lower() == "true":
                is_hero = True
            elif is_hero.lower() == "false":
                is_hero = False
            else:
                ValueError("You must enter True or False to indicate if the warscroll is a hero.")
            is_valid = True
        except (ValueError, AttributeError):
            print("Invalid entry. The name must be a string, points must be an integer, and is_hero a boolean.")
            is_valid = False
    return (name, points, is_hero)

def new_warscroll(name: str, points: int, is_hero: bool) -> dict:
    return  {"name": name, "points": points, "is_hero": is_hero}


 # TODO : Extract the part of this that appends the warscroll to the existing list so it can be tested on its own
def create_warscroll() -> dict:

    name, points, is_hero = get_user_inputs()
    warscrolls = load_warscrolls()
    overwrite: bool = True

    if name in warscrolls.keys():
        ans = prompt_user(
            {
                1: Option("Overwrite", lambda: print("Overwriting warscroll")),
                2: Option("Cancel", lambda: print("Cancelling warscroll creation"))
            }
        )
        overwrite = ans == 1

    if not overwrite:
        warscroll = warscrolls[name]
    
    else:
        warscroll = new_warscroll(name, points, is_hero)
        warscrolls[name] = warscroll
        save_warscrolls(warscrolls)
    
    return warscroll


def save_warscrolls(warscrolls: dict):
    with open("warscrolls.json", "w") as f:
        f.write(json.dumps(warscrolls))

def list_warscrolls():
    warscrolls = load_warscrolls()
    result = []
    for k, ws in warscrolls.items:
        result.append(f"{k}: {ws}")
    return result

def load_warscrolls() -> dict:
    from pathlib import Path
    if not Path("warscrolls.json").exists():
        save_warscrolls({})
    with open("warscrolls.json", "r") as f:
        warscrolls = json.load(f)
    return warscrolls

def print_warscrolls():
    warscrolls = load_warscrolls()
    from pprint import pprint

    pprint(warscrolls)

if __name__ == "__main__":
    print_warscrolls()