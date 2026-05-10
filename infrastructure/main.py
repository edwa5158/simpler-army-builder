from infrastructure.army import Army
from infrastructure.warscroll import Warscrolls


def save_all(army: Army, warscrolls: Warscrolls, warscroll_path: str, army_path: str):
    army.save_army(army_path)
    warscrolls.save_warscrolls(warscroll_path)
