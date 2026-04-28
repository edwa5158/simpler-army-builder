from __future__ import annotations

from typing import TypedDict

from unit import Unit, UnitNumbered, UnitNumDict


class Regiment:
    def __init__(self, name: str, units: list[Unit] = []):
        self.name = name
        self.units: list[UnitNumbered] = []

        num: int = 0
        for unit in units:
            self.units.append(UnitNumbered(unit, num))
            num += 1

        self._unit_number: int = num

    def add_unit(self, unit: Unit) -> None:
        self.units.append(UnitNumbered(unit, self._unit_number))
        self._unit_number += 1

    def remove_unit(self, unit: Unit) -> None:

        # remove the first instance of a unit from the regiment
        for numbered_unit in self.units:
            if numbered_unit.unit == unit:
                self.units.remove(numbered_unit)
                break

        # renumber the units
        i: int = 0
        for numbered_unit in self.units:
            numbered_unit.unit_num = i
            i += 1

        # reset the unit number for the next unit added
        self._unit_number = i

    def to_dict(self) -> RegimentDict:
        return {
            "name": self.name,
            "units": [u.to_dict() for u in self.units],
            "_unit_number": self._unit_number,
        }

    @classmethod
    def from_dict(cls, regiment_dict) -> Regiment:
        regiment = Regiment(regiment_dict.get("name", ""))
        units: list[UnitNumbered] = []
        for unit in regiment_dict.get("units", {}):
            units.append(UnitNumbered.from_dict(unit))
        regiment.units = units
        return regiment


class RegimentDict(TypedDict):
    name: str
    units: list[UnitNumDict]
    _unit_number: int


def regiments_from_dict(regiments_json: list[RegimentDict]) -> list[Regiment]:
    regiments: list[Regiment] = [Regiment.from_dict(r) for r in regiments_json]
    return regiments
