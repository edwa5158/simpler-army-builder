from unit import create_unit
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