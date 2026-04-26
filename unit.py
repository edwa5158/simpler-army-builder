from __future__ import annotations

from typing import TypedDict

from warscroll import Warscroll, WarscrollDict


class Unit:
    def __init__(self):
        self.warscroll: Warscroll
        self.wargear: str = ""

    def to_dict(self) -> UnitDict:
        return {"warscroll": self.warscroll.to_dict(), "wargear": self.wargear}

    @classmethod
    def from_dict(cls, unit_dict: UnitDict) -> Unit:
        unit = Unit()
        unit.warscroll = Warscroll.from_dict(unit_dict.get("warscroll", {}))
        unit.wargear = unit_dict.get("wargear", "")
        return unit

    @classmethod
    def from_warscroll(cls, warscroll) -> Unit:
        unit = Unit()
        unit.warscroll = warscroll
        return unit


class UnitNumbered:
    def __init__(self, unit: Unit, unit_num: int):
        self.unit: Unit = unit
        self.unit_num: int = unit_num

    @property
    def warscroll(self) -> Warscroll:
        return self.unit.warscroll

    @warscroll.setter
    def warscroll(self, ws: Warscroll) -> None:
        self.unit.warscroll = ws

    @property
    def wargear(self) -> str:
        return self.unit.wargear

    @wargear.setter
    def wargear(self, wg: str) -> None:
        self.unit.wargear = wg

    @classmethod
    def from_dict(cls, numbered_unit: UnitNumDict) -> UnitNumbered:
        unit: Unit = Unit.from_dict(numbered_unit.get("unit"))
        num: int = numbered_unit.get("unit_num", 0)
        return UnitNumbered(unit, num)

    def to_dict(self) -> UnitNumDict:
        return {"unit": self.unit.to_dict(), "unit_num": self.unit_num}


class UnitDict(TypedDict):
    warscroll: WarscrollDict
    wargear: str


class UnitNumDict(TypedDict):
    unit: UnitDict
    unit_num: int
