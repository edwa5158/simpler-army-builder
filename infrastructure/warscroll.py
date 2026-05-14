from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import NotRequired, Optional, TypedDict, cast


class WarscrollDict(TypedDict):
    name: str
    type: str
    descr: str
    points: int
    is_hero: bool
    move: NotRequired[str]
    save: NotRequired[str]
    control: NotRequired[str]
    health: NotRequired[str]
    unit_size: NotRequired[int]
    base_size: NotRequired[str]
    can_be_reinforced: NotRequired[bool]
    regiment_options: NotRequired[list[str]]
    abilities: NotRequired[dict]
    keywords: NotRequired[list[str]]
    weapons: NotRequired[dict]


WarscrollsDict = dict[str, WarscrollDict]


def warscroll_file_exists(warscroll_path: str) -> bool:
    return os.path.exists(warscroll_path)


def load_warscrolls(warscroll_path: str) -> WarscrollsDict | None:
    if not warscroll_file_exists(warscroll_path):
        return None

    with open(warscroll_path, "r") as f:
        warscrolls_json: WarscrollsDict = cast(WarscrollsDict, json.load(f))
    return warscrolls_json


class Warscroll:
    def __init__(
        self,
        name: str,
        warscroll_type: str | int,
        descr: Optional[str] | bool = None,
        points: Optional[int] = None,
        is_hero: Optional[bool] = None,
        move: str = "",
        save: str = "",
        control: str = "",
        health: str = "",
        unit_size: int = 0,
        base_size: str = "",
        can_be_reinforced: bool = False,
        regiment_options: Optional[list[str]] = None,
        abilities: Optional[dict] = None,
        keywords: Optional[list[str]] = None,
        weapons: Optional[dict] = None,
    ):
        normalized_type = warscroll_type if isinstance(warscroll_type, str) else ""
        normalized_descr = descr if isinstance(descr, str) else ""

        if isinstance(warscroll_type, int):
            if not isinstance(descr, bool):
                raise TypeError(
                    "Warscroll requires either (name, points, is_hero) or (name, type, descr, points, is_hero)."
                )

            points = warscroll_type
            is_hero = descr
        elif points is None or is_hero is None:
            raise TypeError(
                "Warscroll requires either (name, points, is_hero) or (name, type, descr, points, is_hero)."
            )

        self.name = name
        self.type = normalized_type
        self.points = points
        self.is_hero = is_hero
        self.descr = normalized_descr
        self.move: str = move
        self.save: str = save
        self.control: str = control
        self.health: str = health
        self.unit_size: int = unit_size
        self.base_size: str = base_size
        self.can_be_reinforced: bool = can_be_reinforced
        self.regiment_options: list[str] = list(regiment_options or [])
        self.abilities: dict = deepcopy(abilities or {})
        self.keywords: list[str] = list(keywords or [])
        self.weapons: dict = deepcopy(weapons or {})

    def to_dict(self) -> WarscrollDict:
        return {
            "name": self.name,
            "type": self.type,
            "descr": self.descr,
            "points": self.points,
            "is_hero": self.is_hero,
            "move": self.move,
            "save": self.save,
            "control": self.control,
            "health": self.health,
            "unit_size": self.unit_size,
            "base_size": self.base_size,
            "can_be_reinforced": self.can_be_reinforced,
            "regiment_options": list(self.regiment_options),
            "abilities": deepcopy(self.abilities),
            "keywords": list(self.keywords),
            "weapons": deepcopy(self.weapons),
        }

    @classmethod
    def from_dict(cls, ws_dict: WarscrollDict) -> Warscroll:
        return Warscroll(
            ws_dict.get("name", ""),
            ws_dict.get("type", ""),
            ws_dict.get("descr", ""),
            ws_dict.get("points", 0),
            ws_dict.get("is_hero", False),
            ws_dict.get("move", ""),
            ws_dict.get("save", ""),
            ws_dict.get("control", ""),
            ws_dict.get("health", ""),
            ws_dict.get("unit_size", 0),
            ws_dict.get("base_size", ""),
            ws_dict.get("can_be_reinforced", False),
            ws_dict.get("regiment_options", []),
            ws_dict.get("abilities", {}),
            ws_dict.get("keywords", []),
            ws_dict.get("weapons", {}),
        )

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Warscroll):
            return NotImplemented

        return self.to_dict() == other.to_dict()


class Warscrolls:
    def __init__(self):
        self.catalog: dict[str, Warscroll] = {}
        self.serialized_catalog: WarscrollsDict = {}

    @classmethod
    def load_warscrolls(cls, warscroll_path: str) -> WarscrollsDict:
        fp = warscroll_path
        catalog: WarscrollsDict = {}
        if Path(fp).exists():
            with open(fp, "r") as f:
                catalog = cast(WarscrollsDict, json.load(f))
        return catalog

    def save_warscrolls(self, warscrolls_file: str) -> None:
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
