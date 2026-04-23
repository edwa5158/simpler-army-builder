import json
from prompt_utils import Option, prompt_user
from pathlib import Path

class Warscroll:
    def __init__(self, name: str, points: int, is_hero: bool):
        self.name = name
        self.points: int = points
        self.is_hero: bool = is_hero
    
    def to_dict(self):
        return {"name": self.name, "points": self.points, "is_hero": self.is_hero}



    def __repr__(self):
        return json.dumps(self.to_dict())

class Warscrolls:
    WARSCROLLs_FILE: str = "warscrolls.json"
    def __init__(self):
        self.catalog = {}

    def load_warscrolls(self) -> dict:
        fp = super().WARSCROLLS_FILE        
        if Path(fp).exists():
            with open(fp, "r") as f:
                self.catalog = json.load(f)
        return self.catalog
            
    def save_warscrolls(self) -> None:
        with open(super().WARSCROLLS_FILE, "w") as f:
            f.write(json.dumps(self.catalog))

    def print_warscrolls(self) -> None:
        from pprint import pprint
        pprint(self.catalog)

    def list_warscrolls(self):
        result = []
        for k, ws in self.warscrolls.items:
            result.append(f"{k}: {ws}")
        return result

    def append_warscroll(self, warscroll):
        name: str = warscroll["name"]
        self.warscrolls[name] = warscroll
        return self.warscrolls

def get_user_inputs() -> tuple[str, int, bool]:
    is_valid: bool = False
    while not is_valid:
        user_inputs: str = input("Enter the name, points, and if the warscroll is a hero (True / False)")
        name_in, points_in, is_hero_in = user_inputs.split(", ")
        try:
            name: str = str(name_in)
            points: int = int(points_in)
            if is_hero_in.lower() == "true":
                is_hero: bool = True
            elif is_hero_in.lower() == "false":
                is_hero: bool = False
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
def append_warscroll(warscrolls, warscroll):
    name: str = warscroll["name"]
    warscrolls[name] = warscroll
    return warscrolls

def create_warscroll() -> dict:
    name, points, is_hero = get_user_inputs()
    warscrolls = load_warscrolls()
    overwrite: bool = True

    if name in warscrolls:
        ans = prompt_user(
            {
                1: Option("Overwrite", lambda: print("Overwriting warscroll")),
                2: Option("Cancel", lambda: print("Cancelling warscroll creation"))
            }
        )
        overwrite = (ans == 1)

    if not overwrite:
        warscroll = warscrolls[name]
    else:
        warscroll = new_warscroll(name, points, is_hero)
        append_warscroll(warscrolls, warscroll)
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