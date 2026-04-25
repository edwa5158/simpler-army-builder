import json
from pathlib import Path


class Warscroll:
    def __init__(self, name: str, points: int, is_hero: bool):
        self.name = name
        self.points: int = points
        self.is_hero: bool = is_hero

    def to_dict(self):
        return {"name": self.name, "points": self.points, "is_hero": self.is_hero}

    def __repr__(self):
        return json.dumps(self.to_dict())


class Warscrolls:
    def __init__(self):
        self.catalog: dict[str, Warscroll] = {}
        self.warcrolls_file: str = "warscrolls.json"

    def load_warscrolls(self) -> dict:
        fp = self.warcrolls_file
        if Path(fp).exists():
            with open(fp, "r") as f:
                self.catalog = json.load(f)
        return self.catalog

    def save_warscrolls(self) -> None:
        with open(self.warcrolls_file, "w") as f:
            f.write(json.dumps(self.catalog))

    def print_warscrolls(self) -> None:
        from pprint import pprint

        pprint(self.catalog)

    def list_warscrolls(self):
        return [f"{k}: {ws}" for k, ws in self.catalog.items()]
    

    def append_warscroll(self, warscroll):
        name: str = warscroll["name"]
        self.catalog[name] = warscroll
        return self.catalog

def append_warscroll(warscrolls, warscroll):
    name: str = warscroll["name"]
    warscrolls[name] = warscroll
    return warscrolls