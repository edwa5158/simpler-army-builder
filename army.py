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
        json_str = json.dumps(self, indent=4)
        with open("army.json", "w") as f:
            f.write(json_str)
        print("Army saved")

    def load_army(self) -> tuple[bool, str]:
        try:
            with open("army.json", "r") as f:
                army_json = json.load(f)
                self.name = army_json.get("name", None)
                self.regiments = [Regiment(k) for k,v in army_json.get("regiments").items()]
                
                reason = ""
                success = True
        except FileNotFoundError as e:
            reason = str(e)
            success = False
        except json.JSONDecodeError as e:
            success = False
            reason = str(e)
        return success, reason







