from __future__ import annotations

class Warscroll:
    def __init__(self, name: str):
        self.name = name
        self.points: int = 0

class Unit:
    def __init__(self):
        self.warscroll = Warscroll()
        self.wargear = ""


    @classmethod
    def from_warscroll(cls, warscroll) -> Unit:
        unit = Unit()
        unit.warscroll = warscroll


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
