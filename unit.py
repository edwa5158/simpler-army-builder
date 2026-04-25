from __future__ import annotations

from warscroll import Warscroll


class Unit:
    def __init__(self):
        self.warscroll: Warscroll
        self.wargear: str = ""

    def to_dict(self) -> dict:
        return {"warscroll": self.warscroll.to_dict(), "wargear": self.wargear}

    @classmethod
    def from_dict(cls, unit_dict) -> Unit:
        unit = Unit()
        unit.warscroll = Warscroll.from_dict(unit_dict.get("warscroll", {}))
        unit.wargear = unit_dict.get("wargear", "")
        return unit

    @classmethod
    def from_warscroll(cls, warscroll) -> Unit:
        unit = Unit()
        unit.warscroll = warscroll
        return unit
