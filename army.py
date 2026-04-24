import json
from regiment import Regiment

class Army:
    def __init__(self, name: str):
        self.name = name
        self.regiments: list[Regiment] = []
        self._regiment_number = 0 
    
    def to_dict(self): 
        return {"name": self.name, "regiments": self.regiments}

    def add_regiment(self) -> Regiment:
        regiment_name = f"Regiment {self._regiment_number:03}"
        regiment = Regiment(regiment_name)
        self.regiments.append(regiment)
        self._regiment_number += 1
        return regiment
    
    def save_army(self):
        json_str = json.dumps(self.army, indent=4)
        with open("army.json", "w") as f:
            f.write(json_str)
        print("Army saved")

    # TODO: Make this a class method so that I can load an army before I've created one.
    def load_army(self) -> tuple[bool, str]:
        try:
            with open("army.json", "r") as f:
                self.army = json.load(f)
                reason = ""
                success = True
        except FileNotFoundError as e:
            reason = str(e)
            success = False
        except json.JSONDecodeError as e:
            success = False
            reason = str(e)
        return success, reason





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

