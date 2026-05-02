from regiment import Regiment
from unit import Unit
from warscroll import Warscroll

ws1 = Warscroll("Clanrats", 150, False)
ws2 = Warscroll("Grey Seer", 300, True)
ws3 = Warscroll("Ratling Gun", 200, False)


unit1 = Unit.from_warscroll(ws1)
unit2 = Unit.from_warscroll(ws2)


def test_regiment_add_unit():
    regiment = Regiment("Regiment 00", [])

    regiment.add_unit(unit2)
    regiment.add_unit(unit1)

    assert len(regiment.units) == 2
    assert regiment.units[0].unit == unit2
    assert regiment.units[1].unit == unit1


def test_regiment_init():
    regiment = Regiment("Regiment 00", [unit2, unit1])

    assert len(regiment.units) == 2
    assert regiment.units[0].unit == unit2
    assert regiment.units[1].unit == unit1


def test_regiment_remove_unit():
    regiment = Regiment(
        "Regiment 00",
        [
            unit2,
            unit1,
            unit2,
        ],
    )

    assert len(regiment.units) == 3
    assert regiment.units[0].unit == unit2
    assert regiment.units[1].unit == unit1
    assert regiment.units[2].unit == unit2

    regiment.remove_unit(unit2)

    assert len(regiment.units) == 2
    assert regiment.units[0].unit == unit1
    assert regiment.units[1].unit == unit2


def test_regiment_points():
    regiment = Regiment("Regiment 00", [unit2, unit1])

    assert regiment.points == 450


def test_regiment_header():
    regiment = Regiment("Regiment 00", [unit2, unit1])
    print(regiment.header())
    assert (
        regiment.header()
        == "Regiment 00                                                450 Points"
    )
