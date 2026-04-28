import os

from army import ArmiesDict, Army
from unit import Unit
from warscroll import Warscroll

TEST_ARMY_PATH = "test_army.json"

army_name = "army_01"
reg_name_01 = "Regiment 00"
reg_name_02 = "Regiment 01"

ws1 = Warscroll("Clanrats", 150, False)
ws2 = Warscroll("Grey Seer", 300, True)

unit_01 = Unit.from_warscroll(ws1)
unit_02 = Unit.from_warscroll(ws2)


def init_army() -> Army:
    return Army(army_name)


def one_regiment_army() -> Army:
    army = init_army()
    army.add_regiment()
    army.regiments[0].add_unit(unit_01)
    army.regiments[0].add_unit(unit_02)

    return army


def two_regiment_army() -> Army:
    army = init_army()
    army.add_regiment()
    army.add_regiment()

    army.regiments[0].add_unit(unit_01)
    army.regiments[0].add_unit(unit_02)

    army.regiments[1].add_unit(unit_01)
    army.regiments[1].add_unit(unit_01)
    army.regiments[1].add_unit(unit_02)

    return army


def save_two_regiment_army():
    army = two_regiment_army()
    return army.save_army(TEST_ARMY_PATH)


def delete_army_json_file() -> None:
    if os.path.exists(TEST_ARMY_PATH):
        os.remove(TEST_ARMY_PATH)


def test_army_init():
    army = init_army()

    assert army.name == army_name
    assert army.regiments == []
    assert army._regiment_number == 0


def test_add_regiment():
    army = init_army()

    reg_01 = army.add_regiment()

    assert len(army.regiments) == 1
    assert army._regiment_number == 1
    assert army.regiments[0].name == reg_name_01
    assert reg_01.name == reg_name_01


def test_add_multiple_regiments():
    army = init_army()

    reg_01 = army.add_regiment()
    reg_02 = army.add_regiment()

    assert len(army.regiments) == 2
    assert army._regiment_number == 2
    assert reg_01.name == reg_name_01
    assert army.regiments[0].name == reg_name_01
    assert reg_02.name == reg_name_02
    assert army.regiments[1].name == reg_name_02


def test_save_army_with_no_regiments():
    delete_army_json_file()

    army = init_army()
    army.save_army(TEST_ARMY_PATH)
    assert os.path.exists(TEST_ARMY_PATH)


def test_load_army_with_no_regiments():
    # arrange
    delete_army_json_file()
    # saved_army = Army("army_999")
    # saved_army.save_army(TEST_ARMY_PATH)

    # act
    army = init_army()
    army.load_army("army_01", TEST_ARMY_PATH)

    # assert
    assert army.name == "army_01"

    # cleanup
    # delete_army_json_file()


def test_save_with_two_regiments():
    # arrange
    delete_army_json_file()
    result: ArmiesDict = save_two_regiment_army()

    # assert
    assert os.path.exists(TEST_ARMY_PATH)
    assert result is not None and len(result) > 0
    # cleanup
    delete_army_json_file()


def test_load_with_two_regiments():
    # arrange
    delete_army_json_file()
    save_two_regiment_army()

    army = init_army()
    army_dict = army.load_army(army_name, TEST_ARMY_PATH)
    if army_dict is None:
        raise ValueError
    army = army.from_dict(army_dict)    

    assert army.name == army_name
    assert len(army.regiments) == 2

    assert army.regiments[0].units[0].warscroll.name == "Clanrats"
    assert army.regiments[0].units[1].warscroll.name == "Grey Seer"

    assert army.regiments[1].units[0].warscroll.name == "Clanrats"
    assert army.regiments[1].units[1].warscroll.name == "Clanrats"
    assert army.regiments[1].units[2].warscroll.name == "Grey Seer"


def test_saving_multiple_armies():
    delete_army_json_file()

    army_01 = one_regiment_army()
    army_02 = two_regiment_army()

    army_01.name = "one_regiment_army"
    army_02.name = "two_regiment_army"

    armies = army_01.save_army(TEST_ARMY_PATH)

    assert len(armies) == 1

    armies = army_02.save_army(TEST_ARMY_PATH)

    assert len(armies) == 2

    delete_army_json_file()


def test_loading_from_multiple_armies():
    delete_army_json_file()

    army_01 = one_regiment_army()
    army_02 = two_regiment_army()

    army_01.name = "one_regiment_army"
    army_02.name = "two_regiment_army"

    _ = army_01.save_army(TEST_ARMY_PATH)
    armies = army_02.save_army(TEST_ARMY_PATH)

    army_one = Army("").load_army("one_regiment_army", TEST_ARMY_PATH) or {}
    assert army_one.get("name", "") == "one_regiment_army"
    assert len(army_one.get("regiments", [])) == 1

    army = Army("").load_army("two_regiment_army", TEST_ARMY_PATH) or {}
    assert army.get("name", "") == "two_regiment_army"
    assert len(army.get("regiments", [])) == 2

    delete_army_json_file()
