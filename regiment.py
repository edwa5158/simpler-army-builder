from __future__ import annotations

from unit import Unit


class Regiment:
    def __init__(self, name: str, units: list[Unit] = []):
        self.name = name
        self.units: list[Unit] = units

    def add_unit(self, unit: Unit) -> None:
        self.units.append(unit)

    def remove_unit(self, unit: Unit) -> None:
        self.units.remove(unit)

    def to_dict(self) -> dict:
        return {"name": self.name, "units": [u.to_dict() for u in self.units]}

    @classmethod
    def from_dict(cls, regiment_dict) -> Regiment:
        regiment = Regiment(regiment_dict.get("name", ""))
        units: list[Unit] = []
        for unit in regiment_dict.get("units", {}):
            units.append(Unit.from_dict(unit))
        regiment.units = units
        return regiment


def regiments_from_dict(regiments_json: list[dict]) -> list[Regiment]:
    regiments: list[Regiment] = [Regiment.from_dict(r) for r in regiments_json]
    return regiments
