from __future__ import annotations

import json

from config import ARMY_PATH
from regiment import Regiment, regiments_from_dict


class Army:
    def __init__(self, name: str):
        self.name = name
        self.regiments: list[Regiment] = []
        self._regiment_number = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "_regiment_number": self._regiment_number,
            "regiments": [r.to_dict() for r in self.regiments],
        }

    @classmethod
    def from_dict(cls, army_dict: dict) -> Army:
        army = Army(army_dict.get("name", ""))
        army.regiments = regiments_from_dict(army_dict.get("regiments", []))
        return army

    def add_regiment(self) -> Regiment:
        regiment_name = f"Regiment {self._regiment_number:02}"
        regiment = Regiment(regiment_name)
        self.regiments.append(regiment)
        self._regiment_number += 1
        return regiment

    def save_army(self, army_path: str = ARMY_PATH):
        json_str = json.dumps(self.to_dict(), indent=4)
        with open(army_path, "w") as f:
            f.write(json_str)
        print(f"Army saved to {army_path}")

    def load_army(self, army_path: str = ARMY_PATH) -> tuple[bool, str]:
        try:
            with open(army_path, "r") as f:
                army_json = json.load(f)
                print(army_json)

                army = Army.from_dict(army_json)
                self.name = army.name
                self.regiments = army.regiments

                reason = ""
                success = True
        except FileNotFoundError as e:
            reason = str(e)
            success = False
        except json.JSONDecodeError as e:
            success = False
            reason = str(e)
        return success, reason
