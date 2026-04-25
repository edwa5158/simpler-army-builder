from __future__ import annotations



class Regiment:
    def __init__(self, name: str):
        self.name = name
        self.units: list[Unit] = []

    def add_unit(self, unit: Unit) -> None:
        self.units.append(unit)

    def remove_unit(self, unit: Unit) -> None:
        self.units.remove(unit)


class Army:
    def __init__(self, name: str):
        self.name = str(name)
        self.regiments: list[Regiment] = []

    def add_regiment(self, regiment: Regiment) -> None:
        self.regiments.append(regiment)

    def remove_regiment(self, regiment: Regiment) -> None:
        self.regiments.remove(regiment)
