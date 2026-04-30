from __future__ import annotations

import json
import os
from typing import TypedDict

from config import ARMY_PATH
from regiment import Regiment, RegimentDict, regiments_from_dict


class ArmyDict(TypedDict):
    name: str
    _regiment_number: int
    regiments: list[RegimentDict]


type ArmiesDict = dict[str, ArmyDict]


def army_file_exists(army_path: str = ARMY_PATH) -> bool:
    return os.path.exists(army_path)

def army_file_contents(army_path: str = ARMY_PATH) -> ArmiesDict | None:
    if not army_file_exists(army_path):
        return None

    with open(army_path, "r") as f:
        army_json: ArmiesDict = json.load(f)
    return army_json


class Army:
    def __init__(self, name: str):
        self.name = name
        self.regiments: list[Regiment] = []
        self._regiment_number = 0

    def to_dict(self) -> ArmyDict:
        return {
            "name": self.name,
            "_regiment_number": self._regiment_number,
            "regiments": [r.to_dict() for r in self.regiments],
        }

    @classmethod
    def from_dict(cls, army_dict: ArmyDict) -> Army:
        army = Army(army_dict.get("name", ""))
        army.regiments = regiments_from_dict(army_dict["regiments"])
        return army

    def add_regiment(self) -> Regiment:
        regiment_name = f"Regiment {self._regiment_number:02}"
        regiment = Regiment(regiment_name)
        self.regiments.append(regiment)
        self._regiment_number += 1
        return regiment

    def save_army(self, army_path: str = ARMY_PATH) -> ArmiesDict:
        temp: ArmiesDict | None = army_file_contents(army_path)
        armies: ArmiesDict = temp if temp is not None else {}
        armies[self.name] = self.to_dict()

        json_str = json.dumps(armies, indent=4)

        # print(json_str)
        with open(army_path, "w") as f:
            f.write(json_str)
        print(f"Army saved to {army_path}")
        return armies

    def load_army(self, army_name: str, army_path: str = ARMY_PATH) -> ArmyDict | None:
        army_json: ArmiesDict | None = army_file_contents(army_path)

        result: ArmyDict | None = army_json.get(army_name, None) if army_json else None
        if not result:
            print(f"An army named `{army_name}` could not be found.")
        return result
