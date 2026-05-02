from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from config import WARSCROLL_PATH


class Warscroll:
    def __init__(self, name: str, points: int, is_hero: bool):
        self.name = name
        self.points: int = points
        self.is_hero: bool = is_hero

    def to_dict(self) -> WarscrollDict:
        return {"name": self.name, "points": self.points, "is_hero": self.is_hero}

    @classmethod
    def from_dict(cls, ws_dict: WarscrollDict) -> Warscroll:
        return Warscroll(
            ws_dict.get("name", ""),
            ws_dict.get("points", 0),
            ws_dict.get("is_hero", False),
        )

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other: Warscroll) -> bool:  # type: ignore
        return (
            self.name == other.name
            and self.points == other.points
            and self.is_hero == other.is_hero
        )


class WarscrollDict(TypedDict):
    name: str
    points: int
    is_hero: bool


type WarscrollsDict = dict[str, WarscrollDict]


class Warscrolls:
    def __init__(self):
        self.catalog: dict[str, Warscroll] = {}
        self.serialized_catalog: WarscrollsDict = {}

    @classmethod
    def load_warscrolls(cls, warscroll_path: str = WARSCROLL_PATH) -> WarscrollsDict:
        fp = warscroll_path
        catalog: WarscrollsDict = {}
        if Path(fp).exists():
            with open(fp, "r") as f:
                catalog = json.load(f)
        return catalog

    def save_warscrolls(self, warscrolls_file: str = WARSCROLL_PATH) -> None:
        with open(warscrolls_file, "w") as f:
            f.write(json.dumps(self.serialized_catalog))

    @classmethod
    def from_dict(cls, warscrolls_dict: WarscrollsDict) -> Warscrolls:
        warscrolls = Warscrolls()
        warscrolls.serialized_catalog = warscrolls_dict

        for name, ws in warscrolls_dict.items():
            warscrolls.catalog[name] = Warscroll.from_dict(ws)

        return warscrolls

    def print_warscrolls(self) -> None:
        from pprint import pprint

        pprint(self.serialized_catalog)

    def append_warscroll(self, warscroll: Warscroll):
        name: str = warscroll.name
        self.catalog[name] = warscroll
        self.serialized_catalog[name] = warscroll.to_dict()
        return self.catalog

    def __eq__(self, other: Warscrolls) -> bool:  # type: ignore
        return (
            self.catalog == other.catalog
            and self.serialized_catalog == other.serialized_catalog
        )
