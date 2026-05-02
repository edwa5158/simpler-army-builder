from infrastructure.unit import Unit
from infrastructure.warscroll import Warscroll, WarscrollDict

ws1 = Warscroll("Clanrats", 150, False)
ws2 = Warscroll("Grey Seer", 300, True)
ws3 = Warscroll("Ratling Gun", 200, False)


def setup_units() -> tuple[Unit, Unit, Unit, Unit]:
    unit1 = Unit.from_warscroll(ws1)
    unit1.wargear = "unit_01_wargear"

    unit2 = Unit.from_warscroll(ws1)
    unit2.wargear = "unit_02_wargear"

    unit3 = Unit.from_warscroll(ws2)
    unit3.wargear = "unit_03_wargear"

    unit4 = Unit.from_warscroll(ws3)
    unit4.wargear = "unit_04_wargear"

    return unit1, unit2, unit3, unit4


def test_basic_properties():
    unit1, unit2, unit3, unit4 = setup_units()

    assert unit1.wargear == "unit_01_wargear"
    assert unit1.points == 150
    assert unit1.warscroll == ws1

    assert unit2.wargear == "unit_02_wargear"
    assert unit2.points == 150
    assert unit2.warscroll == ws1

    assert unit3.wargear == "unit_03_wargear"
    assert unit3.points == 300
    assert unit3.warscroll == ws2

    assert unit4.points == 200
    assert unit4.warscroll == ws3
    assert unit4.wargear == "unit_04_wargear"


def test_from_warscroll():
    unit = Unit.from_warscroll(ws1)
    assert unit.warscroll == ws1


def test_from_dict_to_dict():
    ws_dict: WarscrollDict = ws1.to_dict()
    ws_new = Warscroll.from_dict(ws_dict)

    assert ws_new == ws1

def test_equality():
    unit1, unit2, _ , _ = setup_units()

    assert unit1 == unit1
    assert unit1 != unit2