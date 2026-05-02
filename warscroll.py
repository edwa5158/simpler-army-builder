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


class WarscrollDict(TypedDict):
    name: str
    points: int
    is_hero: bool


class Warscrolls:
    def __init__(self):
        self.catalog: dict[str, Warscroll] = {}
        self.serialized_catalog: dict[str, WarscrollDict] = {}
        self.warcrolls_file: str = WARSCROLL_PATH

    @classmethod
    def load_warscrolls(
        cls, warscroll_path: str = WARSCROLL_PATH
    ) -> dict[str, Warscroll]:
        fp = warscroll_path
        catalog: dict[str, Warscroll] = {}
        if Path(fp).exists():
            with open(fp, "r") as f:
                catalog = json.load(f)
        return catalog

    def save_warscrolls(self) -> None:
        with open(self.warcrolls_file, "w") as f:
            f.write(json.dumps(self.serialized_catalog))

    def print_warscrolls(self) -> None:
        from pprint import pprint

        pprint(self.catalog)

    def list_warscrolls(self):
        return [f"{k}: {ws}" for k, ws in self.catalog.items()]

    def append_warscroll(self, warscroll: Warscroll):
        name: str = warscroll.name
        self.catalog[name] = warscroll
        self.serialized_catalog[name] = warscroll.to_dict()
        return self.catalog
