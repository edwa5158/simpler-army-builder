from unit import create_unit
from classes_for_later import Unit
class Regiment:
    def __init__(self, name: str):
        self.name = name
        self.units: list[Unit] = []

    def add_unit(self, unit: Unit) -> None:
        self.units.append(unit)

    def remove_unit(self, unit: Unit) -> None:
        self.units.remove(unit)

def add_regiment(army: dict) -> dict:
    regiment = create_regiment()
    if "regiments" not in army.keys():
        army["regiments"] = []
    army["regiments"].append(regiment)

def add_unit_to_regiment(regiment: dict):
    unit: dict = create_unit()
    regiment["units"].append(unit)

def create_regiment() -> dict:
    return {
        "units": [],
        "points": 0
        }